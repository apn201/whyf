"""Generate concept card skeletons from the corpus registry.

Safe to run repeatedly. A card file is created only if it does not exist. For
cards that already exist, only the generated block at the bottom is replaced,
so nothing written by hand is ever lost.

    python tools/gen_skeletons.py            # create missing, refresh generated
    python tools/gen_skeletons.py --dry-run  # say what it would do
    python tools/gen_skeletons.py --migrate  # rewrite status:skeleton cards from
                                             # the current template. Never touches
                                             # a card at draft or done.
"""
import csv
import re
import sys
from collections import Counter
from pathlib import Path

from corpus_map import CONCEPTS, build_map, load_rows

ROOT = Path(__file__).resolve().parent.parent
CARDS = ROOT / "knowledge" / "concepts"
PRIVATE = ROOT / "private"
CROSSWALK = PRIVATE / "crosswalk.tsv"
BENCHMARKS = PRIVATE / "benchmarks.yaml"
CONTEXT = PRIVATE / "context"
MARK = "# ---8<--- generated from the corpus. do not hand-edit below this line."
# Markers used by earlier versions. A card written against one of these must
# have its old block replaced rather than a second one appended.
LEGACY_MARKS = ["# ---8<--- generated from questions.txt. do not hand-edit below this line."]

FORM_LABEL = {
    "binary_statement": "binary_statement",
    "binary": "binary_statement",
    "maturity_ladder": "maturity_ladder",
    "check_all": "check_all",
    "admin": "admin_field",
    "disclosure": "disclosure",
}


def q(s):
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


def load_crosswalk():
    """csf subcategory id -> {framework: [control ids]}"""
    out = {}
    if not CROSSWALK.exists():
        return out
    with CROSSWALK.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            out.setdefault(r["csf_subcategory"], {})[r["framework"]] = \
                r["control_ids"].split(",")
    return out


def load_benchmarks():
    """concept id -> [(control area, peer score)]. Empty if the file is gone,
    which is a supported state: the benchmark comes from a confidential report
    and may have to be dropped before the repo is published."""
    out = {}
    if not BENCHMARKS.exists():
        return out
    try:
        import yaml
    except ImportError:
        return out
    data = yaml.safe_load(BENCHMARKS.read_text(encoding="utf-8")) or {}
    for entry in data.get("control_areas") or []:
        if entry.get("peer_score") is not None:
            out.setdefault(entry["concept"], []).append(
                (entry["area"], entry["peer_score"]))
    return out


def generated_block(cid, rows, assigned, benchmarks):
    """The block written into the card. Publishable: counts and forms, and
    example wording taken only from the synthetic corpus.

    The real questionnaire rows never appear here. They go to
    private/context/<concept>.md, which is gitignored, because the card files
    are the thing that ships and the questionnaire wording is not ours.
    """
    mine = [rows[rid] for rid, c in assigned.items() if c == cid]
    per_source = Counter(r["source"] for r in mine)
    forms = sorted({FORM_LABEL.get(r.get("form", ""), r.get("form", ""))
                    for r in mine})
    syn = sorted((r for r in mine if r["source"] == "syn"), key=lambda r: r["id"])
    real = sum(n for s, n in per_source.items() if s != "syn")

    out = [MARK]
    out.append("corpus_hits: {}".format(len(mine)))
    out.append("corpus_sources: {{{}}}".format(
        ", ".join("{}: {}".format(s, n) for s, n in sorted(per_source.items()))))
    out.append("question_forms: [" + ", ".join(forms) + "]")
    if real:
        out.append("# {} real questionnaire rows map here. Their wording is not ours to".format(real))
        out.append("# publish, so it lives in private/context/{}.md instead.".format(cid))
    if benchmarks.get(cid):
        out.append("# A peer benchmark figure exists for this concept. It is the "
                   "assessor's")
        out.append("# proprietary data, so it stays in private/context/{}.md. "
                   "Express what".format(cid))
        out.append("# it told you in your own words in `why_not_4`.")

    out.append("# Synthetic examples, written here from the concept. Safe to publish.")
    out.append("common_form:")
    for r in syn:
        out.append("  - {}   # {}".format(q(r["question"]), r["id"]))
    return "\n".join(out) + "\n"


def write_context(cid, rows, assigned, crosswalk, benchmarks):
    """The writing aid. Everything derived from private sources, in one file
    per concept, kept out of the repository."""
    mine = [rows[rid] for rid, c in assigned.items() if c == cid
            and rows[rid]["source"] != "syn"]
    if not mine:
        return False
    mine.sort(key=lambda r: (r["source"], r.get("line", 0), r["id"]))

    subcats = ["nist-csf-" + r["id"][3:].lower() for r in mine if r["source"] == "q3"]
    suggested = {}
    for sc in subcats:
        for fw, ids in crosswalk.get(sc, {}).items():
            suggested.setdefault(fw, set()).update(ids)
    it = Counter(r.get("class_it", "") for r in mine if r["source"] == "q3")
    ot = Counter(r.get("class_ot", "") for r in mine if r["source"] == "q3")

    lines = [
        "# Writing context: {}".format(cid),
        "",
        "NOT FOR PUBLICATION. Derived from the questionnaires and the assessment",
        "report in private/. Read it while writing the card; do not paste it in.",
        "",
        "## How it is actually asked ({} rows)".format(len(mine)),
        "",
    ]
    for r in mine:
        lines.append("- `{}` {}".format(r["id"], r["question"]))
        if r.get("options"):
            for opt in r["options"].split(" | "):
                lines.append("    - {}".format(opt))
    if it or ot:
        lines += ["", "## Relevance (source checklist)", ""]
        if it:
            lines.append("- IT: {}".format(it.most_common(1)[0][0] or "unrated"))
        if ot:
            lines.append("- OT: {}".format(ot.most_common(1)[0][0] or "unrated"))
    if suggested:
        lines += ["", "## Reachable framework ids (Annex I crosswalk)", "",
                  "Pick the two or three that matter and put them in the card's",
                  "`frameworks:` field. Do not cite all of them.", ""]
        for fw in sorted(suggested):
            lines.append("- {}: {}".format(fw, ", ".join(sorted(suggested[fw]))))
    for area, score in benchmarks.get(cid, []):
        lines += ["", "## Peer benchmark", "",
                  "- \"{}\" averages {} across 3,936 companies on the 1-4 ladder.".format(
                      area, score),
                  "- Set `enough_rung` against that, not against what the question implies."]

    CONTEXT.mkdir(parents=True, exist_ok=True)
    (CONTEXT / "{}.md".format(cid)).write_text(
        "\n".join(lines) + "\n", encoding="utf-8")
    return True


CONTROL_SKELETON = """\
id: {cid}
title: {title}
status: skeleton            # skeleton -> draft -> done. only 'done' ships.
class: control              # control | disclosure | admin | attestation
csf: {csf}                        # GV | ID | PR | DE | RS | RC
priority: {priority}                 # 1 = write first, 3 = last

# One or two sentences. No jargon, no acronym unless you immediately kill it.
# Written for someone who runs a 30-person company and has never heard the term.
plain_english: >
  TODO

# The thing everyone gets wrong. This is the "why the f" answer and it is where
# the product has a personality.
misunderstanding: >
  TODO

# The honest argument for NOT doing this. The Skeptic agent gets this verbatim.
skeptic_case: >
  TODO

# Facts about the company that make this question relevant. Reuse existing tags.
applies_if: []
# Facts that make it a clean "not applicable". Drives verdict 1.
applies_never_if: []

# Verbatim wording for the questionnaire's comment box when it does not apply.
# States scope. Never asserts a fact about the company.
how_to_say_no: >
  TODO

# One of: not-applicable | already-solved | write-it-down | cheap-checkbox
#         do-it-properly | need-one-fact
default_verdict: need-one-fact

# The single fact that would change the verdict. Symbols and buttons, no typing.
# Set to null if the verdict genuinely never moves.
deciding_question:
  text: "TODO"
  options:
    - id: TODO
      label: "TODO"
      verdict: TODO
      why: "TODO"

# Fill this in when question_forms below includes maturity_ladder.
#
# Roughly two thirds of the corpus is four-rung ladders: "not implemented" /
# "some systems" / "all systems" / "all systems, risk-based, reviewed annually".
# Rung 4 is written by someone selling rung 4.
#
# If a peer_score appears in the generated block below, that is the average
# across 3,936 real companies on this exact ladder. They cluster around 2.3 and
# no control area anywhere reaches 3.5. Set enough_rung against that evidence,
# not against what the question implies you should aspire to.
maturity_ladder:
  enough_rung: 2            # the rung a sane company should answer and stop at
  why_not_4: >
    TODO. What rung 4 costs and what it buys, which is usually an annual review
    meeting and a line in a report.
  rungs:
    - level: 1
      gist: "TODO"
      verdict: TODO
    - level: 2
      gist: "TODO"
      verdict: TODO
    - level: 3
      gist: "TODO"
      verdict: TODO
    - level: 4
      gist: "TODO"
      verdict: TODO

# Keys are levels of the thing bought, values are 1-5 euro symbols.
cost_bands:
  TODO: "€"

# Both 0-3. The gap between them is the entire product.
security_value: 0
checkbox_value: 0

# What proof actually satisfies an auditor.
evidence:
  weak: "TODO"
  better: "TODO"
  strong: "TODO"

# Does answering this wrong have consequences beyond looking bad?
#   none | disclosure  - a statement of past fact, a misrepresentation if wrong
#   warranty           - an insurance or contractual warranty
#   certification      - a claim about holding a certificate
answer_risk: none

# ids only. The validator drops anything not in the library, so an id invented
# here silently vanishes rather than reaching a user.
frameworks: []
incidents: []
patterns: []
already_have: []

"""

NONCONTROL_SKELETON = """\
id: {cid}
title: {title}
status: skeleton            # skeleton -> draft -> done. only 'done' ships.
class: {klass}
csf: {csf}
priority: {priority}

# This is NOT a security control, so it does not get one of the six verdicts.
# The classifier routes it here instead, and the card only has to say the right
# short thing. That is the whole point of having a class: the tool admits when a
# question is not about security.

plain_english: >
  TODO. What this question is actually for.

# What the tool says. Short. For `disclosure` this must make clear that the tool
# will not help word the answer - a wrong answer here is a misrepresentation,
# not a failed control, and it can void an insurance policy.
response: >
  TODO

answer_risk: {answer_risk}

# Who the user should actually talk to, if anyone. Insurer, lawyer, broker,
# nobody. Be specific and be willing to say "nobody, just type it in".
refer_to: >
  TODO

frameworks: []
patterns: []

"""

RISK_BY_CLASS = {"disclosure": "disclosure", "attestation": "certification",
                 "admin": "none", "control": "none"}


def priority_for(cid, hits):
    if cid in {"rpo", "dlp", "ics-inventory"}:
        return 1                      # demo arc
    if hits >= 6:
        return 1
    if hits >= 3:
        return 2
    return 3


def main():
    dry = "--dry-run" in sys.argv
    migrate = "--migrate" in sys.argv

    rows = load_rows()
    assigned, _ = build_map(rows)
    crosswalk = load_crosswalk()
    benchmarks = load_benchmarks()
    counts = Counter(assigned.values())
    CARDS.mkdir(parents=True, exist_ok=True)

    created = refreshed = migrated = contexts = 0
    for cid, spec in sorted(CONCEPTS.items()):
        path = CARDS / "{}.yaml".format(cid)
        block = generated_block(cid, rows, assigned, benchmarks)
        if PRIVATE.exists():
            contexts += write_context(cid, rows, assigned, crosswalk, benchmarks)
        klass = spec["class"]
        template = CONTROL_SKELETON if klass == "control" else NONCONTROL_SKELETON
        body = template.format(
            cid=cid, title=spec["title"], csf=spec["csf"], klass=klass,
            answer_risk=RISK_BY_CLASS[klass],
            priority=priority_for(cid, counts[cid]),
        )

        if not path.exists():
            if not dry:
                path.write_text(body + block, encoding="utf-8")
            created += 1
            continue

        text = path.read_text(encoding="utf-8")
        is_skeleton = "\nstatus: skeleton" in text
        if migrate and is_skeleton:
            if not dry:
                path.write_text(body + block, encoding="utf-8")
            migrated += 1
            continue

        head = text
        for mark in [MARK] + LEGACY_MARKS:
            head = head.split(mark)[0]
        new = head + block
        if new != text:
            if not dry:
                path.write_text(new, encoding="utf-8")
            refreshed += 1

    orphans = sorted(p.name for p in CARDS.glob("*.yaml") if p.stem not in CONCEPTS)
    verb = "would " if dry else ""
    print("{}created {}, {}refreshed {}, {}migrated {}".format(
        verb, created, verb, refreshed, verb, migrated))
    if contexts:
        print("wrote {} private/context/*.md writing aids (gitignored)".format(contexts))
    elif not PRIVATE.exists():
        print("private/ absent - cards generated from the synthetic corpus only")
    if orphans:
        print("cards with no entry in corpus_map.py: {}".format(orphans))
    if not migrate and any("\nstatus: skeleton" in (CARDS / f"{c}.yaml").read_text(
            encoding="utf-8") for c in CONCEPTS if (CARDS / f"{c}.yaml").exists()):
        print("tip: --migrate rewrites untouched skeletons from the current template")


if __name__ == "__main__":
    main()
