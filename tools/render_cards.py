"""Render concept cards from tools/content/.

The cards were written by hand in a hurry: real knowledge, dumped into whichever
field was nearest, with typos and half the fields left as TODO. This renders the
finished version. The content lives in tools/content/*.py, one dict per concept,
so the prose is edited in one place and the YAML shape stays identical across
all eighty cards.

Everything below the generated marker in each card file is left alone - that
block belongs to tools/gen_skeletons.py.

    python tools/render_cards.py             # write the cards
    python tools/render_cards.py --dry-run   # report only
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from card_content import CONTENT  # noqa: E402
from corpus_map import CONCEPTS  # noqa: E402
from gen_skeletons import LEGACY_MARKS, MARK  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CARDS = ROOT / "knowledge" / "concepts"

VERDICTS = {"not-applicable", "already-solved", "write-it-down",
            "cheap-checkbox", "do-it-properly", "need-one-fact"}


def block(text, indent="  "):
    """A YAML folded scalar, wrapped at a sane width."""
    words, lines, cur = str(text).split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > 74:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return "\n".join(indent + ln for ln in lines)


def flow(items):
    return "[" + ", ".join(str(i) for i in items) + "]"


def qstr(s):
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


def incidents_for(cid, c):
    """Which finished incidents this concept may cite.

    Taken from the incidents themselves. Each record names the concepts it is
    legitimate evidence for, written by the person who verified its figures,
    which is a better source for that judgement than the card. Unfinished
    records are skipped, so a card cannot cite a blank one, and the list grows
    on its own as the remaining incidents get written.
    """
    named = list(c.get("incidents", []))
    for iid, incident in _finished_incidents().items():
        if cid in (incident.get("concepts") or []) and iid not in named:
            named.append(iid)
    return sorted(named)


_INCIDENT_CACHE = {}


def _finished_incidents():
    if not _INCIDENT_CACHE:
        import yaml
        folder = ROOT / "knowledge" / "incidents"
        for path in sorted(folder.glob("*.yaml")):
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            if data.get("status") == "done":
                _INCIDENT_CACHE[data.get("id") or path.stem] = data
    return _INCIDENT_CACHE


def render_control(cid, c):
    spec = CONCEPTS[cid]
    out = []
    a = out.append

    a("id: {}".format(cid))
    a("title: {}".format(spec["title"]))
    a("status: done")
    a("class: control")
    a("csf: {}".format(spec["csf"]))
    a("priority: {}".format(c.get("priority", 2)))
    a("")
    a("# What the question is actually asking, for someone who has never heard")
    a("# the term and runs the company themselves.")
    a("plain_english: >")
    a(block(c["plain_english"]))
    a("")
    a("# The thing everyone gets wrong.")
    a("misunderstanding: >")
    a(block(c["misunderstanding"]))
    a("")
    a("# The honest argument for not doing it. The Skeptic agent gets this verbatim.")
    a("skeptic_case: >")
    a(block(c["skeptic_case"]))
    a("")
    a("# Facts about the company that make the question relevant, and the ones")
    a("# that make it a clean 'not applicable'.")
    a("applies_if: {}".format(flow(c.get("applies_if", []))))
    a("applies_never_if: {}".format(flow(c.get("applies_never_if", []))))
    a("")
    a("# Wording for the comment box when it does not apply. States scope. Never")
    a("# asserts a fact about the company.")
    a("how_to_say_no: >")
    a(block(c["how_to_say_no"]))
    a("")
    a("default_verdict: {}".format(c["default_verdict"]))
    a("")

    if c.get("question"):
        a("# The one fact that moves the verdict. Buttons, no typing.")
        a("deciding_question:")
        a("  text: {}".format(qstr(c["question"])))
        a("  options:")
        for oid, label, verdict, why in c["options"]:
            a("    - id: {}".format(oid))
            a("      label: {}".format(qstr(label)))
            a("      verdict: {}".format(verdict))
            a("      why: >")
            a(block(why, "        "))
    else:
        a("# The verdict does not move on one fact here. See skeptic_case.")
        a("deciding_question: null")
    a("")

    if c.get("ladder"):
        enough, why_not, rungs = c["ladder"]
        a("# Which rung is enough, and what the top one actually costs. This is a")
        a("# judgement per concept and per sector, not a number off a table.")
        a("maturity_ladder:")
        a("  enough_rung: {}".format(enough))
        a("  why_not_4: >")
        a(block(why_not, "    "))
        a("  rungs:")
        for level, gist, verdict in rungs:
            a("    - level: {}".format(level))
            a("      gist: {}".format(qstr(gist)))
            a("      verdict: {}".format(verdict))
    else:
        a("# The corpus never asks this as a ladder.")
        a("maturity_ladder: null")
    a("")

    a("# What it costs, by how far you take it.")
    a("cost_bands:")
    for label, band in c["costs"].items():
        a("  {}: {}".format(qstr(label), qstr(band)))
    a("")
    a("# 0-3 each. The gap between them is the whole point.")
    a("security_value: {}".format(c["sec"]))
    a("checkbox_value: {}".format(c["chk"]))
    a("")
    a("# What an auditor actually accepts.")
    a("evidence:")
    for grade, text in zip(("weak", "better", "strong"), c["evidence"]):
        a("  {}: {}".format(grade, qstr(text)))
    a("")
    a("answer_risk: {}".format(c.get("answer_risk", "none")))
    a("")
    a("")
    a("# Words a questionnaire uses for this that the card above does not. This")
    a("# feeds retrieval only and is never shown: a row saying \"former employees\"")
    a("# has to reach a card titled \"joiners, movers and leavers\".")
    a("aka: {}".format(flow(qstr(x) for x in c.get("aka", []))))
    a("")
    a("frameworks: {}".format(flow(c.get("frameworks", []))))
    a("incidents: {}".format(flow(incidents_for(cid, c))))
    a("patterns: {}".format(flow(c.get("patterns", []))))
    a("already_have: {}".format(flow(c.get("already_have", []))))
    a("")
    return "\n".join(out)


def render_other(cid, c):
    spec = CONCEPTS[cid]
    out = []
    a = out.append
    a("id: {}".format(cid))
    a("title: {}".format(spec["title"]))
    a("status: done")
    a("class: {}".format(spec["class"]))
    a("csf: {}".format(spec["csf"]))
    a("priority: {}".format(c.get("priority", 2)))
    a("")
    a("# Not a security control, so it never gets one of the six verdicts.")
    a("")
    a("plain_english: >")
    a(block(c["plain_english"]))
    a("")
    a("# What the tool says back.")
    a("response: >")
    a(block(c["response"]))
    a("")
    a("answer_risk: {}".format(c.get("answer_risk", "none")))
    a("")
    a("# Who to actually talk to, if anyone.")
    a("refer_to: >")
    a(block(c["refer_to"]))
    a("")
    a("frameworks: {}".format(flow(c.get("frameworks", []))))
    a("patterns: {}".format(flow(c.get("patterns", []))))
    a("")
    return "\n".join(out)


def main():
    dry = "--dry-run" in sys.argv
    written, missing, problems = 0, [], []

    for cid in CONCEPTS:
        if cid not in CONTENT:
            missing.append(cid)
            continue
        c = CONTENT[cid]
        klass = CONCEPTS[cid]["class"]
        head = render_control(cid, c) if klass == "control" else render_other(cid, c)

        if klass == "control":
            if c["default_verdict"] not in VERDICTS:
                problems.append("{}: bad default_verdict {!r}".format(cid, c["default_verdict"]))
            for _, _, v, _ in c.get("options", []):
                if v not in VERDICTS:
                    problems.append("{}: bad option verdict {!r}".format(cid, v))
            if c.get("ladder"):
                for _, _, v in c["ladder"][2]:
                    if v not in VERDICTS:
                        problems.append("{}: bad rung verdict {!r}".format(cid, v))

        path = CARDS / "{}.yaml".format(cid)
        tail = ""
        if path.exists():
            text = path.read_text(encoding="utf-8")
            for mark in [MARK] + LEGACY_MARKS:
                if mark in text:
                    tail = mark + text.split(mark, 1)[1]
                    break
        if not dry:
            path.write_text(head + tail, encoding="utf-8")
        written += 1

    print("{}rendered {} cards".format("would have " if dry else "", written))
    if missing:
        print("no content yet for {}: {}".format(len(missing), " ".join(missing)))
    if problems:
        print("\nPROBLEMS")
        for p in problems:
            print("  x " + p)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
