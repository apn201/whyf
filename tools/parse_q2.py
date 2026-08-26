"""Parse questions2.txt into normalised corpus rows.

questions2.txt is two questionnaires concatenated, both extracted out of PDFs,
so it arrives with page furniture, zero-width placeholder characters and words
hyphenated across line breaks ("organiza- tion"). This turns it into a TSV with
one row per question and, crucially, a `form` column.

The form column is new. The first corpus was 116 binary statements of the shape
"X is implemented." This one is mostly four-rung maturity ladders and check-all
lists, plus a handful of questions that are not about controls at all - company
headcount, and disclosure questions about past breaches. Those need different
handling, so they get classified here rather than being pretended into the same
mould.

    python tools/parse_q2.py                    # writes corpus/q2-vendor-cyber.tsv
    python tools/parse_q2.py --report           # summary only, writes nothing
"""
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(r"D:\Users\juha_\Downloads\questions2.txt")
OUT = ROOT / "corpus" / "q2-vendor-cyber.tsv"

# Lines that are page furniture from the PDF extraction, not content.
FURNITURE = re.compile(
    r"^\s*(page \d+ of \d+"
    r"|cyber security questionnaire"
    r"|vendor cyber security questionnaire"
    r"|\d{1,2}/\d{1,2}/\d{2},\s*\d{1,2}:\d{2}\s*[ap]m"
    r")\s*$", re.I)

# Whitelisted section headings. A heuristic here would misfire on option text,
# and there are only two dozen of them.
SECTIONS = {
    "compliance with eu network and information security 2 (nis2) directive":
        "NIS2 Compliance",
    "about your organization": "Organization Profile",
    "critical systems & data": "Critical Systems & Data",
    "recent incidents": "Recent Incidents",
    "data security": "Data Security",
    "governance": "Governance",
    "risk management": "Risk Management",
    "access control": "Access Control",
    "password configuration": "Password Configuration",
    "multi-factor authentication": "Multi-Factor Authentication",
    "endpoint and systems security": "Endpoint & Systems Security",
    "vulnerability management": "Vulnerability Management",
    "asset inventory": "Asset Inventory",
    "secure configuration": "Secure Configuration",
    "logging & monitoring": "Logging & Monitoring",
    "network security": "Network Security",
    "wireless": "Wireless",
    "network penetration testing": "Network Penetration Testing",
    "network capacity": "Network Capacity",
    "physical security": "Physical Security",
    "application security": "Application Security",
    "third party": "Third Party",
    "business resilience": "Business Resilience",
    "remote work": "Remote Work",
}

QUESTION_RE = re.compile(r"^\s*(\d{1,3})([a-z])?\.\s*(.*)$")

# First rung of a maturity ladder. If the first option says the control is
# absent, the options are a ladder rather than a menu.
LADDER_HEAD = re.compile(
    r"^\s*(control[s]? not implemented"
    r"|control not currently deployed"
    r"|process(/procedure)? is not currently deployed"
    r"|process(/procedure)? not (currently )?deployed"
    r"|automated tool not currently deployed"
    r"|no penetration testing is conducted"
    r"|no users receive"
    r"|audit logging is not enabled"
    r"|access is not revoked"
    r"|access rights re-certification does not occur"
    r"|administrator access rights are not restricted"
    r"|multi-factor authentication is not deployed"
    r"|sso is not deployed"
    r"|application allow listing not currently deployed"
    r"|vpn not in place"
    r"|data (at rest|in transit) is not encrypted"
    r"|third parties are not contractually"
    r"|incident response plans are not reviewed"
    r"|there (is|are) no "
    r"|rarely"
    r"|never or limited"
    r"|not applicable"
    r"|periodic access audits"
    r")", re.I)

ADMIN_RE = re.compile(
    r"organization name|contact name|contact email|total headcount"
    r"|it headcount|security headcount|number of (in-house|external) data cent",
    re.I)

DISCLOSURE_RE = re.compile(
    r"have any of the following events occurred"
    r"|have you ever sustained"
    r"|has any customer or other person or entity alleged"
    r"|please describe the event", re.I)


def clean(line: str) -> str:
    """Strip zero-width junk and normalise whitespace."""
    line = unicodedata.normalize("NFKC", line)
    line = line.replace("\u200b", "").replace("\u00a0", " ")
    line = "".join(c for c in line if unicodedata.category(c) != "Cf")
    return line.rstrip()


def dehyphenate(text: str) -> str:
    """'organiza- tion' -> 'organization'. The PDF broke words at the margin."""
    text = re.sub(r"(\w)-\s+(\w)", r"\1\2", text)
    return re.sub(r"\s+", " ", text).strip()


def is_continuation(line: str) -> bool:
    """A wrapped fragment of the line above rather than a new item."""
    s = line.strip()
    if not s:
        return False
    if s == "*":
        return True
    if re.match(r"^(check all that|apply\b)", s, re.I):
        return True
    return s[0].islower()


def strip_bullets(text: str) -> str:
    return re.sub(r"^[\s\u2022\uf0a7\-\u25a1\u2610\*]+", "", text).strip()


def classify(question: str, options: list) -> str:
    if ADMIN_RE.search(question):
        return "admin"
    if DISCLOSURE_RE.search(question):
        return "disclosure"
    if not options:
        return "binary"
    # A ladder never offers "none of the above" - you are always on some rung.
    if re.match(r"none of the above", options[-1], re.I):
        return "check_all"
    if LADDER_HEAD.match(options[0]):
        return "maturity_ladder"
    if re.search(r"check all that apply", question, re.I):
        return "check_all"
    if 2 <= len(options) <= 4:
        return "maturity_ladder"
    return "check_all"


def parse(path: Path):
    raw = [clean(line) for line in path.read_text(encoding="utf-8").splitlines()]

    rows, section, part, last_number = [], "", 1, 0
    current = None          # {number, suffix, qlines, options}
    mode = None             # "question" | "options"

    def flush():
        if current is None:
            return
        question = dehyphenate(" ".join(current["qlines"]))
        question = re.sub(r"\s*\*\s*$", "", question).strip()
        options = [dehyphenate(strip_bullets(o)) for o in current["options"]]
        options = [o for o in options if o]
        rows.append({
            "id": "q2.{}.{}{}".format(part, current["number"], current["suffix"]),
            "part": part,
            "number": "{}{}".format(current["number"], current["suffix"]),
            "section": current["section"],
            "question": question,
            "form": classify(question, options),
            "option_count": len(options),
            "options": " | ".join(options),
        })

    for line in raw:
        if not line.strip() or FURNITURE.match(line):
            continue

        key = line.strip().lower().rstrip(":")
        if key in SECTIONS:
            flush()
            current, mode = None, None
            section = SECTIONS[key]
            continue

        m = QUESTION_RE.match(line)
        if m and not (mode == "options" and is_continuation(line)):
            number, suffix, rest = int(m.group(1)), m.group(2) or "", m.group(3)
            # Both documents number from 1. A number going backwards means the
            # second questionnaire has started.
            if number < last_number and not suffix:
                part += 1
            last_number = number
            flush()
            current = {"number": number, "suffix": suffix,
                       "qlines": [rest], "options": [], "section": section}
            mode = "question"
            continue

        if current is None:
            continue

        if mode == "question":
            # "...administrative access (i.e." / "AD, DNS, Hypervisors...)" - an
            # unclosed bracket means the question has not finished, whatever
            # case the next line starts in.
            open_bracket = ("".join(current["qlines"]).count("(")
                            > "".join(current["qlines"]).count(")"))
            if is_continuation(line) or open_bracket:
                current["qlines"].append(line.strip())
            else:
                mode = "options"
                current["options"].append(line)
        else:
            if is_continuation(line) and current["options"]:
                current["options"][-1] += " " + line.strip()
            else:
                current["options"].append(line)

    flush()
    return rows


def main():
    if not SRC.exists():
        sys.exit("cannot find {}".format(SRC))
    rows = parse(SRC)

    forms = {}
    sections = {}
    for r in rows:
        forms[r["form"]] = forms.get(r["form"], 0) + 1
        sections[r["section"]] = sections.get(r["section"], 0) + 1

    print("{} questions parsed from {}".format(len(rows), SRC.name))
    print("\nby form:")
    for f, n in sorted(forms.items(), key=lambda kv: -kv[1]):
        print("  {:<16} {:>3}".format(f, n))
    print("\nby section:")
    for s, n in sorted(sections.items(), key=lambda kv: -kv[1]):
        print("  {:<28} {:>3}".format(s or "(none)", n))

    if "--report" in sys.argv:
        print("\nsample:")
        for r in rows[:3] + rows[40:43]:
            print("  [{}] {} ({}, {} options)".format(
                r["id"], r["question"][:72], r["form"], r["option_count"]))
        return

    OUT.parent.mkdir(parents=True, exist_ok=True)
    cols = ["id", "part", "number", "section", "form", "question",
            "option_count", "options"]
    with OUT.open("w", encoding="utf-8", newline="") as fh:
        fh.write("\t".join(cols) + "\n")
        for r in rows:
            fh.write("\t".join(str(r[c]).replace("\t", " ") for c in cols) + "\n")
    print("\nwrote {}".format(OUT.relative_to(ROOT)))


if __name__ == "__main__":
    main()
