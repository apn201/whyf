"""Assemble a verdict from a card. No model involved.

This is the part that makes the anti-hallucination claim true rather than
aspirational. On the warm path the model contributes exactly one thing: which
concept. Every word the user reads after that was written by a human and is
sitting in knowledge/concepts.

The cold path is different and lives in pipeline.py, where a model does write
prose. Even there it may not invent a reference: the ids go through
Library.validate_references first.
"""
from .schema import Verdict
from .verdicts import resolve as resolve_verdict


def _clean(text):
    return " ".join((text or "").split())


def from_card(question, card, library, classification=None, telemetry=None):
    """Render a card into a verdict. Deterministic."""
    klass = card.get("class", "control")

    out = Verdict(
        question=question,
        concept=card.get("id"),
        concept_title=card.get("title"),
        question_class=klass,
        plain_english=_clean(card.get("plain_english")),
        answer_risk=card.get("answer_risk", "none"),
        telemetry=telemetry,
    )

    if klass != "control":
        # Not a control, so it never gets one of the six. The card answers in
        # its own words instead.
        out.response = _clean(card.get("response"))
        out.refer_to = _clean(card.get("refer_to"))
        if klass == "disclosure":
            out.notes.append(
                "This is a statement of fact about your past, not a control. "
                "Answering it wrongly is a misrepresentation and can void an "
                "insurance policy. The tool will not help you word it.")
        return out

    verdict_id = card.get("default_verdict") or "cannot-tell-yet"
    meta = resolve_verdict(verdict_id)

    out.verdict = meta.id
    out.headline = meta.headline
    out.subtitle = meta.subtitle
    out.misunderstanding = _clean(card.get("misunderstanding"))
    out.skeptic_case = _clean(card.get("skeptic_case"))
    out.how_to_say_no = _clean(card.get("how_to_say_no"))
    out.security_value = card.get("security_value", 0)
    out.checkbox_value = card.get("checkbox_value", 0)
    out.cost_bands = card.get("cost_bands") or {}
    out.evidence = card.get("evidence") or {}
    out.maturity_ladder = card.get("maturity_ladder") or {}
    out.deciding_question = card.get("deciding_question")

    refs = {
        "frameworks": card.get("frameworks") or [],
        "incidents": card.get("incidents") or [],
        "patterns": card.get("patterns") or [],
        "already_have": card.get("already_have") or [],
    }
    kept, dropped = library.validate_references(refs)
    out.references = kept
    out.reference_text = {
        kind: {rid: library.describe(kind, rid) for rid in ids}
        for kind, ids in kept.items() if ids
    }
    if dropped and telemetry:
        telemetry.dropped_references = dropped

    if classification:
        if classification.negated:
            out.notes.append(
                "This row is phrased so that agreeing means the opposite of "
                "what it looks like. Read it twice before ticking anything.")
        if classification.translation_damage:
            out.notes.append(
                "The wording of this row is mangled enough that its meaning is "
                "uncertain. Check what was actually meant before answering.")
        if getattr(classification, "policy_question", False):
            out.notes.insert(0,
                "This asks what your policy SAYS, not what you do. That is the "
                "cheapest kind of question on the form: a paragraph in a "
                "document closes it, and the same document usually closes the "
                "twenty rows around it. The control below is what the "
                "paragraph should describe.")
        if classification.form == "maturity_ladder" and out.maturity_ladder:
            enough = out.maturity_ladder.get("enough_rung")
            if enough:
                out.notes.append(
                    "This arrived as a four-rung ladder. Rung {} is enough for "
                    "most companies; see why the top rung usually is not worth "
                    "buying.".format(enough))

    if out.answer_risk == "warranty":
        out.notes.append(
            "This answer is an insurance or contractual warranty. Getting it "
            "wrong can void cover. Check before you tick.")
    elif out.answer_risk == "certification":
        out.notes.append(
            "This is a claim about something you either hold or do not. "
            "Attach the evidence rather than describing it.")

    return out


def answered(question, card, library, option, telemetry=None):
    """The same card, after the user has tapped one answer.

    This is the whole product in one function. The first verdict was the
    honest one available without knowing anything about the company. One fact
    arrives and the verdict changes, because the card said in advance what
    each answer would mean. No model is involved: the option carries its own
    verdict and its own reasoning, both written by a human.
    """
    out = from_card(question, card, library, telemetry=telemetry)

    verdict_id = option.get("verdict")
    if verdict_id:
        meta = resolve_verdict(verdict_id)
        was = out.headline
        out.verdict = meta.id
        out.headline = meta.headline
        out.subtitle = meta.subtitle
        if meta.headline != was:
            out.notes.insert(0, "Changed from \"{}\" because you answered: "
                                "{}".format(was, option.get("label")))

    why = _clean(option.get("why"))
    if why:
        out.plain_english = why
    out.deciding_question = None      # asked and answered
    return out


def near_miss(question, card, library, missing_topic, telemetry=None):
    """The closest card, shown as a near miss rather than as an answer.

    A flat "I have no card" throws away something useful: the neighbouring
    concept usually IS worth reading, it just does not answer the specific
    thing asked. Saying which part is missing is more use than either
    pretending to cover it or refusing to speak.
    """
    out = from_card(question, card, library, telemetry=telemetry)
    gap = _clean(missing_topic) or "the specific thing you asked about"

    out.covers_question = False
    out.notes.insert(0,
        "Closest thing here, but it does not cover {}. Background rather than "
        "an answer.".format(gap))

    # The verdict belongs to the concept, not to the question that was asked.
    # Leaving it on the card would be the confidently-wrong outcome this whole
    # path exists to avoid.
    out.verdict = None
    out.headline = "Closest match: " + (card.get("title") or card.get("id"))
    out.subtitle = "Does not cover " + gap
    out.deciding_question = None
    return out


def cold(question, cold_verdict, near_card, library, telemetry=None):
    """A tier-2 verdict: written for this row, because no card covered it.

    Labelled as generated, every time and without an option to hide it. The
    whole claim this tool makes is that the answer came from a human, so the
    one place that is not true has to say so where the reader cannot miss it.
    """
    meta = resolve_verdict(cold_verdict.verdict)

    out = Verdict(
        question=question,
        concept=None,
        concept_title=None,
        question_class="control",
        verdict=meta.id,
        headline=meta.headline,
        subtitle=meta.subtitle,
        plain_english=_clean(cold_verdict.plain_english),
        misunderstanding=_clean(cold_verdict.misunderstanding),
        skeptic_case=_clean(cold_verdict.skeptic_case),
        how_to_say_no=_clean(cold_verdict.how_to_say_no),
        security_value=cold_verdict.security_value,
        checkbox_value=cold_verdict.checkbox_value,
        covers_question=True,
        telemetry=telemetry,
    )

    refs = {}
    for ref in cold_verdict.references:
        refs.setdefault(ref.kind, []).append(ref.id)
    kept, dropped = library.validate_references(refs)
    out.references = kept
    out.reference_text = {
        kind: {rid: library.describe(kind, rid) for rid in ids}
        for kind, ids in kept.items() if ids
    }
    if dropped and telemetry:
        telemetry.dropped_references = dropped

    if meta.id == "cannot-tell-yet":
        # The verdict's stock subtitle is "One question first.", which is true
        # on a card: the card carries the question and its answers. Tier 2 has
        # no question to offer, so the stock wording promised something that
        # never appeared underneath it.
        settles = _clean(cold_verdict.what_would_settle_it)
        out.subtitle = settles or (
            "This row is too broadly worded to answer as written.")
        if settles:
            out.notes.append(
                "Worth putting back to whoever sent the questionnaire: "
                "answering it as written means guessing what they meant.")

    out.notes.insert(0,
        "No card covers this row, so this was written for it just now rather "
        "than taken from the knowledge base. Everything else this tool says "
        "comes from a card a human wrote. Treat this one as a starting point "
        "and check it before you rely on it.")
    if near_card:
        out.notes.append(
            "The nearest concept in the knowledge base is {}, which is worth "
            "reading as background.".format(
                near_card.get("title") or near_card.get("id")))
    return out


def declined(question, reason, telemetry=None):
    """No card, and not enough confidence to write one.

    Kept short on purpose. Somebody who pasted a row wants to know whether
    there is an answer, not how the knowledge base is put together. The
    internal reason goes in the telemetry, where it is useful to us and
    invisible to them.
    """
    out = Verdict(question=question, telemetry=telemetry)
    out.covers_question = False
    out.headline = "No card for this one"
    out.subtitle = "Nothing here covers it well enough to be worth reading."
    out.notes.append(
        "The knowledge base is drawn from real supplier questionnaires. This "
        "row falls outside it.")
    return out


def _clip(text, width):
    text = _clean(text)
    return text if len(text) <= width else text[:width - 1].rstrip() + "…"


def to_text(v):
    """Terminal rendering. Ugly on purpose; the PWA is a later problem."""
    w = []
    a = w.append
    a("")
    a("  " + v.question.strip())
    a("  " + "-" * min(len(v.question.strip()), 72))
    a("")

    if v.question_class != "control":
        a("  NOT A SECURITY CONTROL  ({})".format(v.question_class))
        if v.concept_title:
            a("  {}".format(v.concept_title))
        a("")
        if v.plain_english:
            a("  " + v.plain_english)
            a("")
        if v.response:
            a("  " + v.response)
            a("")
        if v.refer_to:
            a("  Who to ask: " + v.refer_to)
            a("")
    elif v.verdict:
        a("  {}".format(v.headline.upper()))
        a("  {}".format(v.subtitle))
        a("")
        a("  Concept: {} ({})".format(v.concept_title, v.concept))
        a("  Security value {}/3   Checkbox value {}/3".format(
            v.security_value, v.checkbox_value))
        a("")
        for label, text in (("What it is", v.plain_english),
                            ("What everyone gets wrong", v.misunderstanding),
                            ("The case against", v.skeptic_case),
                            ("If it does not apply", v.how_to_say_no)):
            if text:
                a("  {}:".format(label))
                for line in _wrap(text, 72):
                    a("    " + line)
                a("")
        if v.cost_bands:
            a("  Cost:")
            for k, band in v.cost_bands.items():
                a("    {:<44} {}".format(str(k)[:44], band))
            a("")
        if v.maturity_ladder.get("enough_rung"):
            a("  Ladder: rung {} is enough".format(
                v.maturity_ladder["enough_rung"]))
            a("")
        if v.deciding_question and v.deciding_question.get("text"):
            a("  One question would change this:")
            a("    " + v.deciding_question["text"])
            for opt in (v.deciding_question.get("options") or []):
                a("      [{}] -> {}".format(opt.get("label"), opt.get("verdict")))
            a("")
    else:
        a("  {}".format(v.headline.upper()))
        a("  {}".format(v.subtitle))
        a("")

    for note in v.notes:
        for line in _wrap("! " + note, 72):
            a("  " + line)
        a("")

    if any(v.references.values()):
        a("  References:")
        for kind, ids in v.references.items():
            if not ids:
                continue
            a("    {}:".format(kind))
            for rid in ids:
                text = (v.reference_text.get(kind) or {}).get(rid)
                # For a framework the id is what an auditor cites and the text
                # is a gloss, sometimes a long one. For an incident it is the
                # other way round: the name and the figure are the argument.
                if kind == "frameworks":
                    a("      - {} - {}".format(rid, _clip(text, 46)))
                else:
                    a("      - {}".format(_clip(text, 68) or rid))
        a("")

    t = v.telemetry
    if t:
        bits = ["tier: " + t.tier,
                "{} model call{}".format(t.model_calls,
                                         "" if t.model_calls == 1 else "s"),
                "{} search{}".format(t.searches,
                                     "" if t.searches == 1 else "es"),
                "{:.1f} s".format(t.elapsed_s)]
        if t.degraded:
            bits.append("DEGRADED: " + t.degraded_reason)
        a("  " + "  |  ".join(bits))
        if t.dropped_references:
            a("  dropped invented references: {}".format(t.dropped_references))
    a("")
    return "\n".join(w)


def _wrap(text, width):
    words, lines, cur = text.split(), [], ""
    for word in words:
        if len(cur) + len(word) + 1 > width:
            lines.append(cur)
            cur = word
        else:
            cur = (cur + " " + word).strip()
    if cur:
        lines.append(cur)
    return lines
