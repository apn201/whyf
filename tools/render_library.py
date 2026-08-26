"""Render the patterns and already-have libraries.

Same idea as render_cards.py: the prose lives in one place so the shape stays
identical across files, and the generated bits stay out of the way.

The already-have cards are the highest value per line of writing in the repo.
Half the PROTECT questions on a supplier questionnaire are already true for
anyone on a normal business subscription, and the owner has no idea. Each card
says what is already true, where the evidence lives, and when the claim is
wrong.

    python tools/render_library.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from library_content import ALREADY_HAVE, PATTERNS  # noqa: E402
from render_cards import block, flow, qstr  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
K = ROOT / "knowledge"


def render_pattern(pid, p):
    out = ["id: {}".format(pid),
           "name: {}".format(p["name"]),
           "status: done",
           "",
           "# How you recognise it.",
           "tell: >",
           block(p["tell"]),
           "",
           "# What the asker actually wants, underneath the wording.",
           "what_it_means: >",
           block(p["what_it_means"]),
           "",
           "# The cheap correct move.",
           "what_to_do: >",
           block(p["what_to_do"]),
           "",
           "# How companies overspend when they read the question literally.",
           "trap: >",
           block(p["trap"]),
           "",
           "# Phrases that make the classifier suspect this pattern. Lowercased,",
           "# matched against the normalised question.",
           "signals:"]
    for s in p["signals"]:
        out.append("  - {}".format(qstr(s)))
    out.append("")
    out.append("concepts: {}".format(flow(p.get("concepts", []))))
    out.append("")
    return "\n".join(out)


def render_already(aid, a):
    out = ["id: {}".format(aid),
           "title: {}".format(a["title"]),
           "status: done",
           "",
           "# What is already true for anyone on a normal business subscription.",
           "claim: >",
           block(a["claim"]),
           "",
           "microsoft365:",
           "  applies_to: {}".format(qstr(a["m365"][0])),
           "  where_to_look: {}".format(qstr(a["m365"][1])),
           "  evidence: {}".format(qstr(a["m365"][2])),
           "",
           "google_workspace:",
           "  applies_to: {}".format(qstr(a["google"][0])),
           "  where_to_look: {}".format(qstr(a["google"][1])),
           "  evidence: {}".format(qstr(a["google"][2])),
           "",
           "# When the claim is NOT true. There is always a case, and leaving it",
           "# out is how this becomes a liability generator.",
           "caveat: >",
           block(a["caveat"]),
           "",
           "concepts: {}".format(flow(a.get("concepts", []))),
           ""]
    return "\n".join(out)


def main():
    n = 0
    for pid, p in PATTERNS.items():
        (K / "patterns" / "{}.yaml".format(pid)).write_text(
            render_pattern(pid, p), encoding="utf-8")
        n += 1
    for aid, a in ALREADY_HAVE.items():
        (K / "already-have" / "{}.yaml".format(aid)).write_text(
            render_already(aid, a), encoding="utf-8")
        n += 1

    existing = {p.stem for p in (K / "patterns").glob("*.yaml")}
    missing = existing - set(PATTERNS)
    if missing:
        print("patterns with no content: {}".format(sorted(missing)))
    existing = {p.stem for p in (K / "already-have").glob("*.yaml")}
    missing = existing - set(ALREADY_HAVE)
    if missing:
        print("already-have with no content: {}".format(sorted(missing)))

    print("rendered {} library files".format(n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
