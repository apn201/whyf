"""Extract the peer benchmark from the completed assessment report.

questions4.txt is not a questionnaire. It is a finished cyber maturity
assessment of one company, and its own scoring page says what it is:

    9 Security Domains > 35 Control Areas > 110 Questions

That is the same instrument as corpus source q2 part 2, which is already
ingested as 111 rows. So this file adds no questions. What it adds is the
answer key: for each of the 35 control areas, the average score across 3,936
peer companies.

Useful, but narrower than it first looks. READ THIS BEFORE QUOTING IT.

The assessed company is an industrial manufacturer. The report shows three
different numbers on the same page - the company's own score, an "industry
average", and a "global average" - and the global figure is higher than the
industry one. The per-control-area peer column does not say which pool it is
drawn from, and we did not ask.

So this is a benchmark for one segment, probably manufacturing, and it is not
a statement about companies in general. Regulated sectors score higher; a bank
is not the peer group of a packaging plant. Anything written off the back of
these numbers has to carry that scope, and `enough_rung` has to be a judgement
per concept AND per sector, not a single global answer read off a table.

What survives the caveat is the shape rather than the value: on this ladder,
in this segment, real companies cluster around the middle and the top rung is
rare. That is worth knowing while writing `why_not_4`. The numbers themselves
are the assessor's data and do not leave private/.

PRIVACY
-------
The report is a named company's confidential third-party assessment. It names
the sector, the headquarters country, the turnover-relative loss estimate, the
assessment date, and - in free-text comment fields - the company's own
admissions about its weaknesses. None of that is extracted here and none of it
belongs in a public repository. This script takes the peer column and the
control-area taxonomy, and deliberately ignores the "Your Score" column.

The output goes to private/, which is gitignored. The peer averages are the
assessor's proprietary benchmark data, so they do not ship either - they reach
you through private/context/*.md while you write cards, and what ships is the
sentence you write in `why_not_4` off the back of them.

    python tools/parse_benchmarks.py
"""
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# The source is not published. Point WHYF_SOURCE at it, or drop it in
# private/ under this name. This was a hardcoded path to one machine, which
# put a Windows username into a file that ships.
SRC = Path(os.environ.get("WHYF_SOURCE") or ROOT / "private" / "questions4.txt")
OUT = ROOT / "private" / "benchmarks.yaml"

# 9 domains, 35 control areas. Taken from the report's own Category Scores page
# and cross-checked against the section headings of corpus source q2, which is
# the same instrument. concept id is ours.
TAXONOMY = [
    ("Data Security", "Data Classification", "data-classification"),
    ("Data Security", "User Awareness Training", "security-awareness"),
    ("Data Security", "Data Protection", "encryption"),
    ("Data Security", "Governance", "board-oversight"),
    ("Data Security", "Risk Management", "risk-appetite"),

    ("Access Control", "Access Management", "privileged-accounts"),
    ("Access Control", "Password Configuration", "password-policy"),
    ("Access Control", "Two-Factor Authentication", "mfa"),

    ("Endpoint & Systems Security", "Endpoint Protection", "endpoint-protection"),
    ("Endpoint & Systems Security", "Vulnerability Management", "vulnerability-management"),
    ("Endpoint & Systems Security", "Asset Inventory", "asset-inventory"),
    ("Endpoint & Systems Security", "Secure Configuration", "hardening"),
    ("Endpoint & Systems Security", "Logging and Monitoring", "logging"),

    ("Network Security", "Network Environment", "network-segmentation"),
    ("Network Security", "Wireless", "wireless-security"),
    ("Network Security", "Network Penetration Testing", "audits-and-pentests"),
    ("Network Security", "Network Capacity", "capacity-management"),

    ("Physical Security", "Physical Access", "physical-access-control"),
    ("Physical Security", "Physical Penetration Testing", "audits-and-pentests"),
    ("Physical Security", "Tampering & Alteration", "hardware-tampering"),
    ("Physical Security", "Environmental", "physical-environmental-protection"),

    ("Application Security", "Software security Training", "secure-development"),
    ("Application Security", "Secure Development", "secure-development"),
    ("Application Security", "Software Management", "application-allowlisting"),

    ("Third Party", "Third Party Contracts", "third-party-contracts"),
    ("Third Party", "Due Diligence", "third-party-risk"),
    ("Third Party", "Third Party Inventory", "supplier-inventory"),

    ("Business Resilience", "Business Continuity/DR", "bcp"),
    ("Business Resilience", "Incident Response", "incident-response"),
    ("Business Resilience", "Backup", "backups"),

    ("Remote Work", "Remote Connectivity", "remote-access"),
    ("Remote Work", "Authentication & Identity", "identity-lifecycle"),
    ("Remote Work", "Device Vulnerability & Monitoring", "remote-work-model"),
    ("Remote Work", "Remote Business Continuity", "continuity-testing"),
    ("Remote Work", "Remote Security Awareness", "security-awareness"),
]

DOMAINS = ["Data Security", "Access Control", "Endpoint & Systems Security",
           "Network Security", "Physical Security", "Application Security",
           "Third Party", "Business Resilience", "Remote Work"]

# "Data Classification 1,0 1,9 Network Environment 2,9 2,8" - three columns of
# (name, your score, peer score) flattened onto one line by the PDF extractor.
PAIR = re.compile(r"([A-Za-z][A-Za-z &/&\-]*?)\s+(\d,\d)\s+(\d,\d)")


def num(s):
    return float(s.replace(",", "."))


def main():
    if not SRC.exists():
        sys.exit("cannot find {}".format(SRC))
    text = SRC.read_text(encoding="utf-8", errors="replace")
    # column headers leak into the middle of rows
    text = re.sub(r"\b(You|Peer|Your)\b", " ", text)

    peer = {}
    for name, _mine, theirs in PAIR.findall(text):
        name = re.sub(r"\s+", " ", name).strip().lower()
        # The PDF flattens three table columns onto one line, so a captured
        # name can carry the previous column's header on its front. Match the
        # tail, not the whole string. No area name is a suffix of another.
        # The "Your" column is never extracted - only `theirs` is used.
        for _domain, area, _concept in TAXONOMY:
            if name == area.lower() or name.endswith(" " + area.lower()):
                peer.setdefault(area, num(theirs))
        for domain in DOMAINS:
            if name == domain.lower():
                peer.setdefault("domain:" + domain, num(theirs))

    areas = [(d, a, c) for d, a, c in TAXONOMY]
    found = [a for _, a, _ in areas if a in peer]
    missing = [a for _, a, _ in areas if a not in peer]

    print("control areas   : {} of {} scored".format(len(found), len(areas)))
    print("domains         : {} of {} scored".format(
        sum(1 for d in DOMAINS if "domain:" + d in peer), len(DOMAINS)))
    if missing:
        print("no peer score found for: {}".format(missing))

    values = [peer[a] for a in found]
    print("peer range      : {:.1f} to {:.1f}, mean {:.2f}".format(
        min(values), max(values), sum(values) / len(values)))

    out = [
        "# Peer maturity benchmark, 35 control areas across 9 security domains.",
        "#",
        "# Source: the peer column of a completed cyber maturity assessment, drawn",
        "# from the assessor's benchmark database of 3,936 companies. The assessed",
        "# company's own scores are NOT here and must not be added - the report is",
        "# confidential and identifies its subject.",
        "#",
        "# SCOPE. The assessed company is an industrial manufacturer, and the",
        "# report carries both an industry average and a higher global average.",
        "# Which pool this per-area column is drawn from is not stated. Treat it",
        "# as one segment, probably manufacturing - NOT as companies in general.",
        "# Regulated sectors score higher. A bank is not the peer group of a",
        "# packaging plant, and a card that assumes otherwise will be wrong for",
        "# half its readers.",
        "#",
        "# Scale is 1 initial / 2 basic / 3 managed / 4 advanced, the same scale as",
        "# the four-rung ladders throughout the corpus.",
        "",
        "segment: industrial manufacturing (inferred, not stated in the source)",
        "pool_unclear: true        # industry average or global average? unknown",
        "",
        "scale:",
        "  1: initial",
        "  2: basic",
        "  3: managed",
        "  4: advanced",
        "peer_count: 3936",
        "",
        "domains:",
    ]
    for d in DOMAINS:
        key = "domain:" + d
        if key in peer:
            out.append('  - name: "{}"'.format(d))
            out.append("    peer_score: {}".format(peer[key]))

    out.append("")
    out.append("control_areas:")
    for domain, area, cid in areas:
        out.append('  - area: "{}"'.format(area))
        out.append('    domain: "{}"'.format(domain))
        out.append("    concept: {}".format(cid))
        if area in peer:
            out.append("    peer_score: {}".format(peer[area]))
    OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("\nwrote {}".format(OUT.relative_to(ROOT)))


if __name__ == "__main__":
    main()
