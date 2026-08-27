"""The loop. Three tiers, and the telemetry that says which one fired.

    tier 0  exact match     normalise, hash, look it up. Zero model calls.
    tier 1  concept match   lexical + embedding shortlist, one small call to
                            pick from it, then render from the card.
    tier 2  cold path       no card. Research and write one, then cache it.

The interesting property is tier 1: the model contributes a concept id and
nothing else. Every word rendered was written by a human. That is what makes
the anti-hallucination claim checkable rather than a promise.
"""
import time

from . import render
from .config import load as load_config
from .knowledge.library import load as load_library
from .limits import BudgetExceeded, RequestBudget
from .match import ConceptMatcher
from .acronyms import expand as expand_acronyms
from .normalise import row_hash
from .schema import Telemetry, TraceStep


class Pipeline:
    def __init__(self, config=None, library=None, cache=None):
        self.config = config or load_config()
        self.library = library or load_library()
        self.cache = cache            # DynamoDB later; None means tier 0 off
        self.lexical = ConceptMatcher.from_cards()
        self._embeddings = None
        self._models = {}

    # ---- lazily built, so importing the module costs nothing -------------

    @property
    def embeddings(self):
        if self._embeddings is None and self.config.embeddings_enabled:
            try:
                from .embed import EmbeddingMatcher
                self._embeddings = EmbeddingMatcher.load(region=self.config.region)
            except Exception:
                self._embeddings = False   # tried once, degrade quietly
        return self._embeddings or None

    def model(self, which):
        if which not in self._models:
            from strands.models import BedrockModel
            model_id = getattr(self.config, which + "_model")
            self._models[which] = BedrockModel(
                region_name=self.config.region,
                model_id=model_id,
                max_tokens=self.config.limits.max_output_tokens_per_call,
            )
        return self._models[which]

    # ---- tier 1 shortlist -------------------------------------------------

    def shortlist(self, question, budget):
        """Lexical always; embeddings when affordable. Hybrid when both."""
        width = self.config.tier1_shortlist
        matcher = self.embeddings
        # Retrieval sees the row with its acronyms spelled out. The user still
        # sees what they pasted, and the cache key is still the raw row.
        question = expand_acronyms(question)
        if matcher is None or not budget.can_afford_model_call():
            return self.lexical.match(question, limit=width), False
        try:
            from .embed import hybrid
            return hybrid(self.lexical, matcher, question, limit=width), True
        except Exception:
            # The embedding call is an optimisation. Losing it costs accuracy,
            # not correctness, so it must never take the request down.
            return self.lexical.match(question, limit=width), False

    # ---- tier 2 -----------------------------------------------------------

    def cold_verdict(self, question, near_card, budget, telemetry):
        """Write a verdict for a row no card covers. None if not possible.

        Returning None is a normal outcome, not a failure: the caller falls
        back to the near miss, which is a decent answer. Tier 2 is an upgrade
        on that, never a replacement for it.
        """
        step = time.time()
        if not self.config.tier2_enabled:
            return None
        if not self.config.synthesiser_model:
            return None
        if budget.degraded or not budget.can_afford_model_call():
            return None

        try:
            from .agents.synthesiser import synthesise
            cold, detail = synthesise(question, near_card, self.library,
                                      self.model("synthesiser"), budget)
        except Exception as exc:
            telemetry.cold_declined = "synthesiser unavailable: {}".format(
                type(exc).__name__)
            return None

        if cold is None:
            telemetry.cold_declined = str(detail)
            return None

        telemetry.tier = "cold"
        telemetry.model_calls = budget.model_calls
        self._step(
            telemetry, step, "synthesise", "Understudy",
            "No card covers this row, so this stage wrote one for it. Its "
            "citations were checked against the library and anything invented "
            "was dropped.",
            model=self.config.synthesiser_model)
        return render.cold(question, cold, near_card, self.library, telemetry)

    # ---- the tap question -------------------------------------------------

    def answer(self, question, concept_id, option_id):
        """Re-resolve after the user taps one of the deciding question's
        options. Zero model calls: the card already said what each answer
        means, so this is a lookup and the verdict changes on screen in
        milliseconds."""
        started = time.time()
        telemetry = Telemetry(tier="cache", model_calls=0)

        card = self.library.concept(concept_id)
        if not card:
            telemetry.tier = "declined"
            telemetry.elapsed_s = time.time() - started
            telemetry.declined_because = "unknown concept id"
            return render.declined(question, "", telemetry)

        options = ((card.get("deciding_question") or {}).get("options")) or []
        chosen = next((o for o in options if str(o.get("id")) == str(option_id)),
                      None)
        if chosen is None:
            telemetry.elapsed_s = time.time() - started
            return render.from_card(question, card, self.library,
                                    telemetry=telemetry)

        telemetry.elapsed_s = time.time() - started
        return render.answered(question, card, self.library, chosen, telemetry)

    # ---- the entry point --------------------------------------------------

    @staticmethod
    def _step(telemetry, started, stage, label, detail="", model="",
              skipped=False):
        """Record what a stage did. Called by the stage, after it ran."""
        telemetry.trace.append(TraceStep(
            stage=stage, label=label, detail=detail, model=model,
            skipped=skipped, ms=int((time.time() - started) * 1000)))

    def resolve(self, question):
        started = time.time()
        budget = RequestBudget(limits=self.config.limits)
        telemetry = Telemetry(tier="concept")

        # ---- tier 0 --------------------------------------------------------
        step = time.time()
        if self.cache is not None:
            hit = self.cache.get(row_hash(question))
            if hit is not None:
                self._step(telemetry, step, "cache", "Recogniser",
                           "This exact row has been answered before. Replaying "
                           "it, with no model involved.")
                telemetry.tier = "cache"
                telemetry.elapsed_s = time.time() - started
                hit.telemetry = telemetry
                return hit
            self._step(telemetry, step, "cache", "Recogniser",
                       "Normalised the row and looked for it in the cache. "
                       "Not seen before.")
        else:
            self._step(telemetry, step, "cache", "Recogniser",
                       "No cache configured.", skipped=True)

        # ---- daily ceiling -------------------------------------------------
        # Checked before the work, not after. Over the ceiling the agent still
        # answers, from the free matcher, and says that it is degraded. A
        # public demo URL that silently stops working is worse than a slow one.
        if self.cache is not None:
            from .cache import UNAVAILABLE
            spent = self.cache.add_spend(1)
            if spent is UNAVAILABLE:
                # Carry on. The per-request caps still apply, and an agent that
                # stops answering because a counter is unreachable is a worse
                # outcome than one that briefly cannot count.
                telemetry.counter_unavailable = True
            elif spent is not None and                     spent > self.config.limits.daily_model_call_ceiling:
                budget.degrade("daily model call ceiling reached")

        # ---- tier 1 --------------------------------------------------------
        step = time.time()
        candidates, used_embeddings = self.shortlist(question, budget)
        telemetry.shortlist_size = len(candidates)
        if used_embeddings:
            budget.spend_model_call(30, 0)     # the embedding call
        self._step(
            telemetry, step, "retrieve", "Librarian",
            "Expanded the acronyms, then searched {} concept cards two ways - "
            "by wording and by meaning - and put the closest {} in front of "
            "the next stage.".format(len(self.library.concepts), len(candidates)),
            model=self.config.embedding_model if used_embeddings else "")

        if not candidates:
            telemetry.tier = "declined"
            telemetry.elapsed_s = time.time() - started
            telemetry.declined_because = "shortlist was empty"
            return render.declined(question, "", telemetry)

        classification = None
        step = time.time()
        try:
            if budget.degraded:
                raise BudgetExceeded("daily ceiling", 0, 0)
            from .agents.classifier import classify
            classification, _ = classify(
                question, candidates, self.library,
                self.model("classifier"), budget)
            if classification is not None:
                self._step(
                    telemetry, step, "classify", "Reader",
                    "Read the row and picked {} from the shortlist. Judged "
                    "separately whether that card actually answers what was "
                    "asked: {}.".format(
                        classification.concept,
                        "it does" if classification.covers_the_question
                        else "it does not"),
                    model=self.config.classifier_model)
        except BudgetExceeded as exc:
            if not budget.degraded:
                budget.degrade(str(exc))
        except Exception as exc:
            # A model failure falls back to the free matcher rather than
            # failing the request.
            # The type alone is not enough to act on. A deployed ImportError
            # and a deployed TypeError both meant "the bundle is wrong", and
            # both took a redeploy to identify because the message was thrown
            # away here.
            budget.degrade("classifier unavailable: {}: {}".format(
                type(exc).__name__, str(exc)[:200]))
            self._step(telemetry, step, "classify", "Reader",
                       "Unavailable, so the free matcher decided instead.",
                       skipped=True)

        concept_id = None
        if classification and classification.concept != "none":
            concept_id = classification.concept
        elif budget.degraded:
            confident = self.lexical.confident(question)
            concept_id = confident.concept if confident else None

        card = self.library.concept(concept_id) if concept_id else None

        telemetry.model_calls = budget.model_calls
        telemetry.searches = budget.searches
        telemetry.degraded = budget.degraded
        telemetry.degraded_reason = budget.degraded_reason
        telemetry.elapsed_s = time.time() - started

        if card and classification and not classification.covers_the_question:
            # Closest, but it does not answer the row. Tier 2 may write one.
            # The gate is here rather than inside the synthesiser: something
            # has already judged a security concept to be the nearest thing to
            # this row, and that judgement is not one the pasted text controls.
            cold = self.cold_verdict(question, card, budget, telemetry)
            if cold is not None:
                return cold

            telemetry.tier = "near-miss"
            self._step(
                telemetry, time.time(), "render", "Scribe",
                "Showed the nearest card as background and named what it does "
                "not cover, rather than dressing it up as an answer.")
            return render.near_miss(question, card, self.library,
                                    classification.missing_topic, telemetry)

        if card:
            self._step(
                telemetry, time.time(), "render", "Scribe",
                "Assembled the answer from the card. No model wrote any of "
                "this text - the verdict, the counter-argument and the costs "
                "were written by a person and are read back word for word.")
            verdict = render.from_card(question, card, self.library,
                                       classification, telemetry)
            if self.cache is not None:
                self.cache.put(row_hash(question), verdict)
            return verdict

        # ---- tier 2 --------------------------------------------------------
        # Not built yet. Declining is the correct behaviour in the meantime,
        # and it is the behaviour the plan asks for when a concept is missing.
        telemetry.tier = "declined"
        telemetry.declined_because = (
            "no concept matched" if classification is None
            or classification.concept == "none"
            else "matched {} but that card is unfinished".format(concept_id))
        return render.declined(question, telemetry.declined_because, telemetry)
