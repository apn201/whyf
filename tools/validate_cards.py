"""Validate the knowledge corpus and report writing progress.

Three jobs:

1. Schema. A malformed card fails here, at build time, not at runtime in front
   of a judge. The required fields depend on the card's class - a disclosure
   card has no cost bands and should not pretend to.
2. Referential integrity. Every framework / incident / pattern / already-have
   id cited by a concept card must exist. Same rule the runtime validator
   applies to model output, applied to the corpus itself.
3. Coverage. How much of the 364-row corpus is answerable from cards that are
   actually finished. That number is the stopping rule for the writing, and it
   is the demo statistic.

    python tools/validate_cards.py             # errors on 'done' cards only
    python tools/validate_cards.py --strict    # errors on every card
    python tools/validate_cards.py --progress  # the scoreboard, nothing else
"""
import sys
from collections import Counter
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("pyyaml is not installed. Run: pip install -r requirements.txt")

sys.path.insert(0, str(Path(__file__).resolve().parent))
from corpus_map import CONCEPTS, build_map, load_rows  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
K = ROOT / "knowledge"

# Must stay in step with src/whyf/verdicts.py. Six verdicts; `need-one-fact`
# is the writing-friendly alias for `cannot-tell-yet`.
VERDICTS = {
    "not-applicable", "already-solved", "write-it-down",
    "cheap-checkbox", "do-it-properly", "cannot-tell-yet", "need-one-fact",
}
CSF = {"GV", "ID", "PR", "DE", "RS", "RC"}
STATUS = {"skeleton", "draft", "done"}
CLASSES = {"control", "disclosure", "admin", "attestation"}
ANSWER_RISK = {"none", "disclosure", "warranty", "certification"}

CONTROL_REQUIRED = [
    "id", "title", "status", "class", "csf", "plain_english", "misunderstanding",
    "skeptic_case", "applies_if", "how_to_say_no", "default_verdict",
    "cost_bands", "security_value", "checkbox_value", "evidence", "answer_risk",
    "frameworks", "incidents", "patterns", "already_have",
    "common_form", "corpus_hits",
]
NONCONTROL_REQUIRED = [
    "id", "title", "status", "class", "csf", "plain_english", "response",
    "answer_risk", "refer_to", "common_form", "corpus_hits",
]


def load(path):
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        return {"__parse_error__": str(exc)}


def has_todo(value):
    if isinstance(value, str):
        return "TODO" in value
    if isinstance(value, dict):
        return any(has_todo(v) for v in value.values())
    if isinstance(value, list):
        return any(has_todo(v) for v in value)
    return False


def main():
    strict = "--strict" in sys.argv
    progress_only = "--progress" in sys.argv

    cards = {p.stem: load(p) for p in sorted((K / "concepts").glob("*.yaml"))}
    libs = {}
    for sub in ("frameworks", "incidents", "patterns", "already-have"):
        libs[sub] = {p.stem: load(p) for p in sorted((K / sub).glob("*.yaml"))}

    framework_ids = {
        c["id"]
        for f in libs["frameworks"].values()
        for c in (f.get("controls") or [])
        if isinstance(c, dict) and c.get("id")
    }
    incident_ids = set(libs["incidents"])
    pattern_ids = set(libs["patterns"])
    already_ids = set(libs["already-have"])

    errors, warnings = [], []

    for cid, card in cards.items():
        where = "concepts/{}.yaml".format(cid)
        if "__parse_error__" in card:
            errors.append("{}: YAML will not parse: {}".format(where, card["__parse_error__"]))
            continue

        status = card.get("status")
        klass = card.get("class")
        gate = errors if (strict or status == "done") else warnings

        if card.get("id") != cid:
            errors.append("{}: id field is {!r}, must match filename".format(where, card.get("id")))
        if status not in STATUS:
            errors.append("{}: status {!r} not in {}".format(where, status, sorted(STATUS)))
        if klass not in CLASSES:
            errors.append("{}: class {!r} not in {}".format(where, klass, sorted(CLASSES)))
        if card.get("csf") not in CSF:
            errors.append("{}: csf {!r} not in {}".format(where, card.get("csf"), sorted(CSF)))
        if card.get("answer_risk") not in ANSWER_RISK and not has_todo(card.get("answer_risk")):
            errors.append("{}: answer_risk {!r} not in {}".format(
                where, card.get("answer_risk"), sorted(ANSWER_RISK)))

        required = CONTROL_REQUIRED if klass == "control" else NONCONTROL_REQUIRED
        for field in required:
            if field not in card:
                errors.append("{}: missing required field '{}'".format(where, field))

        if klass == "control":
            if card.get("default_verdict") not in VERDICTS:
                errors.append("{}: default_verdict {!r} not in the six".format(
                    where, card.get("default_verdict")))

            for opt in ((card.get("deciding_question") or {}).get("options") or []):
                if not isinstance(opt, dict):
                    errors.append("{}: deciding_question option is not a mapping".format(where))
                    continue
                if opt.get("verdict") not in VERDICTS and not has_todo(opt.get("verdict")):
                    gate.append("{}: option {!r} has verdict {!r}, not in the six".format(
                        where, opt.get("id"), opt.get("verdict")))

            ladder = card.get("maturity_ladder") or {}
            forms = card.get("question_forms") or []
            if "maturity_ladder" in forms and not ladder and status == "done":
                errors.append("{}: the corpus asks this as a ladder but the card has "
                              "no maturity_ladder block".format(where))
            if ladder:
                enough = ladder.get("enough_rung")
                levels = [r.get("level") for r in (ladder.get("rungs") or [])
                          if isinstance(r, dict)]
                if not isinstance(enough, int) or enough not in levels:
                    gate.append("{}: enough_rung {!r} is not one of the rung "
                                "levels {}".format(where, enough, levels))
                for rung in (ladder.get("rungs") or []):
                    if not isinstance(rung, dict):
                        continue
                    v = rung.get("verdict")
                    if v not in VERDICTS and not has_todo(v):
                        gate.append("{}: rung {} has verdict {!r}, not in the six".format(
                            where, rung.get("level"), v))

            for value in (card.get("security_value"), card.get("checkbox_value")):
                if not isinstance(value, int) or not 0 <= value <= 3:
                    gate.append("{}: security_value/checkbox_value must be 0-3".format(where))
                    break
        else:
            if card.get("default_verdict"):
                errors.append("{}: class is {!r}, so it must not carry a verdict. "
                              "Only controls get one of the six.".format(where, klass))

        for field, valid in (("frameworks", framework_ids), ("incidents", incident_ids),
                             ("patterns", pattern_ids), ("already_have", already_ids)):
            for ref in (card.get(field) or []):
                if ref not in valid:
                    errors.append("{}: {} id {!r} does not exist in the library".format(
                        where, field, ref))

        if status == "done" and has_todo(card):
            errors.append("{}: status is 'done' but the card still contains TODO".format(where))

        # A finished card must not point at an unfinished library entry. The id
        # resolves, so the validator would pass it through and the agent would
        # render an empty reference at the user. That is the failure mode the
        # whole id-referencing scheme exists to prevent.
        if status == "done":
            for field, sub in (("patterns", "patterns"),
                               ("already_have", "already-have"),
                               ("incidents", "incidents")):
                for ref in (card.get(field) or []):
                    item = libs[sub].get(ref) or {}
                    if item.get("status") != "done":
                        errors.append(
                            "{}: cites {} {!r}, which is still {}. A done card "
                            "must not reference an unwritten one.".format(
                                where, sub, ref, item.get("status") or "missing"))

    for sub, items in libs.items():
        for iid, item in items.items():
            where = "{}/{}.yaml".format(sub, iid)
            if "__parse_error__" in item:
                errors.append("{}: YAML will not parse: {}".format(where, item["__parse_error__"]))
                continue
            if item.get("id") != iid:
                errors.append("{}: id field is {!r}, must match filename".format(where, item.get("id")))
            if item.get("status") == "done" and has_todo(item):
                errors.append("{}: status is 'done' but still contains TODO".format(where))
            if sub == "incidents" and item.get("status") == "done":
                if not item.get("source_url"):
                    errors.append("{}: incident marked done with no source_url".format(where))
                cost = item.get("what_it_cost") or {}
                if cost.get("figure") and not cost.get("basis"):
                    errors.append("{}: cost figure with no basis. This is the "
                                  "one that kills the submission.".format(where))

    # ---- scoreboard -------------------------------------------------------
    rows = load_rows()
    assigned, _ = build_map(rows)
    per_concept = Counter(assigned.values())
    total_rows = len(rows)

    def tally(items):
        out = Counter()
        for it in items.values():
            out[it.get("status") if it.get("status") in STATUS else "other"] += 1
        return out

    print("WRITING PROGRESS")
    for name, items in ([("concepts", cards)] +
                        [(s, libs[s]) for s in
                         ("already-have", "patterns", "incidents", "frameworks")]):
        t = tally(items)
        total = len(items) or 1
        bar = "#" * int(20 * (t["done"] / total))
        print("  {:<14} {:>3} done  {:>3} draft  {:>3} skeleton  of {:>3}  {}".format(
            name, t["done"], t["draft"], t["skeleton"], len(items), bar))

    # Coverage is measured against the REAL corpus when it is present. The
    # synthetic rows are ours; covering them proves nothing, and folding them
    # into the percentage would flatter the number by a third.
    real_rows = {rid: r for rid, r in rows.items() if r["source"] != "syn"}
    scope = real_rows or rows
    scope_label = " + ".join(sorted({r["source"] for r in scope.values()}))
    per_scope = Counter(c for rid, c in assigned.items() if rid in scope)
    total = len(scope)

    covered = sum(per_scope[c] for c, v in cards.items() if v.get("status") == "done")
    drafted = sum(per_scope[c] for c, v in cards.items()
                  if v.get("status") in ("done", "draft"))
    print("\nCORPUS COVERAGE  {} rows across {}".format(total, scope_label))
    if not real_rows:
        print("  (synthetic only - private/ is not on this machine)")
    print("  answerable from finished cards : {:>3} rows  ({:.0f}%)".format(
        covered, 100 * covered / total))
    print("  including drafts               : {:>3} rows  ({:.0f}%)".format(
        drafted, 100 * drafted / total))

    unwritten = [c for c, v in cards.items() if v.get("status") == "skeleton"]
    if unwritten and not progress_only:
        ranked = sorted(unwritten, key=lambda c: -per_scope[c])
        running = drafted
        print("\nWRITE THESE NEXT - each line shows coverage after that card")
        for c in ranked[:10]:
            running += per_scope[c]
            print("  {:<32} +{:>2} rows -> {:.0f}% of corpus".format(
                c, per_scope[c], 100 * running / total))

    if progress_only:
        return 0

    if warnings:
        print("\n{} warnings (unfinished cards, not yet blocking)".format(len(warnings)))
        for w in warnings[:8]:
            print("  ! " + w)
        if len(warnings) > 8:
            print("  ... and {} more".format(len(warnings) - 8))

    if errors:
        print("\n{} ERRORS".format(len(errors)))
        for e in errors[:30]:
            print("  x " + e)
        if len(errors) > 30:
            print("  ... and {} more".format(len(errors) - 30))
        return 1

    print("\ncorpus is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
