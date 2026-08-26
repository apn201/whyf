"""The fixed verdict vocabulary. Six values, nothing else, ever.

The whole point is that the agent has a model of the world instead of a
paragraph generator. The moment a seventh verdict appears, or the model is
allowed to free-text one, that stops being true. So this module is the single
source of truth and the output validator rejects anything not in it.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Verdict:
    id: str
    headline: str
    subtitle: str
    #: Does the user need to spend money to satisfy the questionnaire?
    costs_money: bool
    #: Does the user need to spend money to fix the underlying risk?
    fix_costs_money: bool


VERDICTS = {
    v.id: v for v in (
        Verdict(
            id="not-applicable",
            headline="Not applicable",
            subtitle="Here is how to say so without looking evasive.",
            costs_money=False,
            fix_costs_money=False,
        ),
        Verdict(
            id="already-solved",
            headline="Already solved",
            subtitle="Go find the screenshot.",
            costs_money=False,
            fix_costs_money=False,
        ),
        Verdict(
            id="write-it-down",
            headline="Write it down",
            subtitle="Documentation control. An afternoon of work.",
            costs_money=False,
            fix_costs_money=False,
        ),
        Verdict(
            id="cheap-checkbox",
            headline="Cheap checkbox, expensive fix",
            subtitle="Satisfy the question. Do not buy the product yet.",
            costs_money=False,
            fix_costs_money=True,
        ),
        Verdict(
            id="do-it-properly",
            headline="Do it properly",
            subtitle="Real risk, real money, here is why.",
            costs_money=True,
            fix_costs_money=True,
        ),
        Verdict(
            id="cannot-tell-yet",
            headline="Cannot tell yet",
            subtitle="One question first.",
            costs_money=False,
            fix_costs_money=False,
        ),
    )
}

#: The card schema uses `need-one-fact` as a friendlier alias while writing.
ALIASES = {"need-one-fact": "cannot-tell-yet"}

VALID_IDS = frozenset(VERDICTS) | frozenset(ALIASES)


def resolve(verdict_id: str) -> Verdict:
    """Look up a verdict, or raise. Never invent one."""
    key = ALIASES.get(verdict_id, verdict_id)
    try:
        return VERDICTS[key]
    except KeyError:
        raise ValueError(
            "{!r} is not one of the six verdicts: {}".format(
                verdict_id, ", ".join(sorted(VERDICTS))
            )
        ) from None
