"""The Classifier: work out what was pasted, and which concept it is.

It never sees all eighty concepts. Tier 1 hands it a shortlist of fifteen,
which is why this is one small cheap call rather than a long one, and why the
model cannot answer with a concept that does not exist.

Measured on the real corpus, that shortlist contains the right concept 91% of
the time. The classifier's job is to pick from it, or to say none of them fit,
which is the honest answer often enough to be worth allowing.
"""
from ..schema import Classification

SYSTEM = """\
You classify one row copied out of a supplier security questionnaire.

You are given the row and a shortlist of concepts. Pick the concept the row is
asking about. If none of them fit, answer with the literal string 'none' rather
than forcing the closest one; a wrong concept produces a confidently wrong
answer, and saying 'none' costs nothing.

Judge the row on what it asks, not on how it is phrased. These rows arrive
badly translated, renumbered, pasted out of PDFs and written by people
describing a product they bought rather than a risk they have.

Four things beyond the concept:

question_class. Most rows are controls. Some are not, and those must not be
treated as controls:
  disclosure  - a statement of fact about the past. "Have you ever been
                breached." Answering wrong is a misrepresentation.
  admin       - company details. Headcount, contact email, number of sites.
  attestation - a claim about holding a certificate or an insurance policy.

form. binary_statement is a sentence you are asked to agree with. Statement
form matters: agreeing to it is a contractual act, which is why the tool never
answers on the user's behalf.

negated. Some rows are phrased so that agreeing means the opposite of what it
looks like. Read twice before setting this.

translation_damage. Set it when the row is mangled enough that its meaning is
genuinely uncertain. Better to flag it than to guess.
"""


def build_prompt(question, shortlist, library):
    """The shortlist, with enough of each card to tell them apart."""
    lines = ["Row pasted by the user:", "", question.strip(), "",
             "Shortlist of candidate concepts:", ""]
    for match in shortlist:
        card = library.concept(match.concept) or {}
        plain = " ".join((card.get("plain_english") or "").split())
        lines.append("- {} ({}): {}".format(
            match.concept, card.get("class", "control"), plain[:180]))
    lines += ["", "Pick one concept id from that list, or 'none'."]
    return "\n".join(lines)


def classify(question, shortlist, library, model, budget):
    """One structured call. Returns (Classification, usage) or (None, reason)."""
    from strands import Agent

    if not budget.can_afford_model_call():
        return None, "budget"

    agent = Agent(model=model, system_prompt=SYSTEM,
                  structured_output_model=Classification,
                  callback_handler=None)
    result = agent(build_prompt(question, shortlist, library))

    usage = {}
    if getattr(result, "metrics", None):
        usage = result.metrics.accumulated_usage or {}
    budget.spend_model_call(usage.get("inputTokens", 0),
                            usage.get("outputTokens", 0))

    classification = result.structured_output
    if classification is None:
        return None, "no structured output"

    # The model was told to pick from the shortlist. If it invented one anyway,
    # that is the same failure as inventing a control number, and it gets the
    # same treatment.
    allowed = {m.concept for m in shortlist} | {"none"}
    if classification.concept not in allowed:
        classification.concept = "none"
        classification.confidence = "low"

    return classification, usage
