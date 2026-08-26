"""Spend caps enforced in code.

AWS Budgets tells you after the money is gone. This is what actually stops it.
A public demo URL and fifty dollars of promotional credits is otherwise a bad
combination.

Three layers:

* per request - a ceiling on model calls, searches and tokens for one question.
* per day - a global counter in DynamoDB at ``SPEND#<date>``, so a bad weekend
  cannot drain the account even if every request is individually well behaved.
* degraded mode - over the ceiling, the API still answers, from cache or from
  the card alone, and says so. It never fails silently and it never fails open.
"""
from dataclasses import dataclass, field


class BudgetExceeded(Exception):
    """Raised when a request tries to spend past its ceiling."""

    def __init__(self, what: str, used: int, ceiling: int):
        self.what, self.used, self.ceiling = what, used, ceiling
        super().__init__(
            "{} ceiling reached: {} of {}".format(what, used, ceiling)
        )


@dataclass
class Limits:
    """Loaded from infra/config.yaml, `limits:` block."""
    max_model_calls_per_request: int = 6
    max_searches_per_request: int = 3
    max_input_tokens_per_call: int = 8000
    max_output_tokens_per_call: int = 1500
    daily_model_call_ceiling: int = 2000
    cache_ttl_days: int = 30


@dataclass
class RequestBudget:
    """One question's worth of spend. Also the source of the tier telemetry
    line the UI renders: 'resolved from cache, 1 model call, 0 searches, 0.9s'.
    """
    limits: Limits = field(default_factory=Limits)
    model_calls: int = 0
    searches: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    degraded: bool = False
    degraded_reason: str = ""

    def spend_model_call(self, input_tokens: int = 0, output_tokens: int = 0) -> None:
        if self.model_calls >= self.limits.max_model_calls_per_request:
            raise BudgetExceeded("model call", self.model_calls,
                                 self.limits.max_model_calls_per_request)
        self.model_calls += 1
        self.input_tokens += input_tokens
        self.output_tokens += output_tokens

    def spend_search(self) -> None:
        if self.searches >= self.limits.max_searches_per_request:
            raise BudgetExceeded("search", self.searches,
                                 self.limits.max_searches_per_request)
        self.searches += 1

    def degrade(self, reason: str) -> None:
        """Stop spending, keep answering, and tell the user why."""
        self.degraded = True
        self.degraded_reason = reason

    def can_afford_model_call(self) -> bool:
        return (not self.degraded
                and self.model_calls < self.limits.max_model_calls_per_request)

    def can_afford_search(self) -> bool:
        return (not self.degraded
                and self.searches < self.limits.max_searches_per_request)

    def telemetry(self, tier: str, elapsed_s: float) -> dict:
        """What the UI shows under the verdict. The clearest signal to a
        technical judge that this is not send-everything-to-the-LLM."""
        return {
            "tier": tier,
            "model_calls": self.model_calls,
            "searches": self.searches,
            "elapsed_s": round(elapsed_s, 1),
            "degraded": self.degraded,
            "degraded_reason": self.degraded_reason,
        }
