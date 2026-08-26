"""Generate skeletons for the non-concept libraries.

incidents, patterns and already-have skeletons. Never overwrites an existing
file, so it is safe to run after you have started writing.

Frameworks are not here. nist-csf.yaml comes from the source workbook via
tools/parse_annex.py, and the rest are written by tools/render_frameworks.py
with a description per control id.

    python tools/gen_library.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
K = ROOT / "knowledge"

# --------------------------------------------------------------------------
# incidents. Eighteen records. Every number in these files must be traceable to
# the source url. Nothing here is prefilled from model memory on purpose -
# the figures are blank because you are going to verify them.
# --------------------------------------------------------------------------
INCIDENTS = [
    ("stuxnet",             "Stuxnet / Natanz",                   2010, "nuclear",       True),
    ("saudi-aramco-shamoon", "Saudi Aramco / Shamoon",            2012, "energy",        False),
    ("target-hvac",         "Target / HVAC vendor credentials",   2013, "retail",        False),
    ("german-steel-mill",   "German steel mill",                  2014, "manufacturing", True),
    ("ukraine-grid-2015",   "Ukraine power grid",                 2015, "energy",        True),
    ("kemuri-water",        "Kemuri Water Company",               2016, "utilities",     True),
    ("maersk-notpetya",     "Maersk / NotPetya",                  2017, "logistics",     False),
    ("merck-notpetya",      "Merck / NotPetya",                   2017, "pharma",        False),
    ("wannacry-nhs",        "WannaCry / NHS",                     2017, "healthcare",    False),
    ("triton-trisis",       "Triton / Trisis safety system",      2017, "chemicals",     True),
    ("norsk-hydro",         "Norsk Hydro / LockerGoga",           2019, "manufacturing", False),
    ("solarwinds",          "SolarWinds Orion supply chain",      2020, "software",      False),
    ("colonial-pipeline",   "Colonial Pipeline",                  2021, "energy",        False),
    ("kaseya-vsa",          "Kaseya VSA / REvil",                 2021, "msp",           False),
    ("oldsmar-water",       "Oldsmar water treatment",            2021, "utilities",     True),
    ("okta-lapsus",         "Okta / Lapsus$ via support vendor",  2022, "identity",      False),
    ("moveit",              "MOVEit Transfer mass exploitation",  2023, "software",      False),
    ("change-healthcare",   "Change Healthcare",                  2024, "healthcare",    False),
]

INCIDENT_TPL = """\
id: {iid}
name: {name}
year: {year}
sector: {sector}
ot: {ot}                     # did it hit operational technology / a physical process

status: skeleton            # -> done only when every figure below has a source

# VERIFY EVERY NUMBER. This is the field that kills the submission if it is
# wrong. If you cannot find a figure you would defend in a boardroom, delete
# the field rather than estimating. The agent may only cite what is here.
source_url: ""              # primary source. Company filing or regulator beats press.
source_note: ""             # e.g. "10-K, page 42" or "company press release"

one_line: >
  TODO one sentence a non-technical reader understands.

what_happened: >
  TODO three or four sentences. Mechanism, not drama.

what_it_cost:
  figure: ""                # e.g. "USD 300 million" - only if sourced
  basis: ""                 # e.g. "company statement, Q3 2017 results"

the_control_that_would_have_helped: >
  TODO. Be honest. Often it is one boring thing, and often it is not the
  control the questionnaire is asking about.

concepts: []                # concept ids this incident is legitimate evidence for
"""

# --------------------------------------------------------------------------
# patterns. Yours entirely. This is the twenty-years-of-pattern-recognition
# lookup table.
# --------------------------------------------------------------------------
PATTERNS = [
    ("documentation-only",
     "The question asks for a document, not an outcome",
     "Anything that asks whether a written policy exists. Satisfied by writing one."),
    ("technology-prescription",
     "The question names a product category instead of a risk",
     "Asks whether you bought a category of product. Names the shelf, not the problem."),
    ("outcome-as-process",
     "The question asks whether you decided something, not whether you bought something",
     "Asks whether a number has been chosen. You already chose it. Say what it is."),
    ("framework-inheritance",
     "The control is inherited from your platform vendor and you did not know",
     "Half of PROTECT is Microsoft 365 or Google Workspace default configuration."),
    ("certificate-shortcut",
     "A certification the asker already accepts makes forty rows go away",
     "Naming a certificate the asker already trusts can close a whole section."),
]

PATTERN_TPL = """\
id: {pid}
name: {name}
status: skeleton

tell: >
  {tell}

what_it_means: >
  TODO. What the asker actually wants, underneath the wording.

what_to_do: >
  TODO. The cheap correct move.

trap: >
  TODO. How companies overspend when they take this question literally.

# Phrases that make the classifier suspect this pattern. Lowercased, matched
# against the normalised question. Keep them boring and specific.
signals: []

example_rows: []            # line numbers in questions.txt
"""

# --------------------------------------------------------------------------
# already-have. Highest value per line of writing in the whole repo.
# --------------------------------------------------------------------------
ALREADY_HAVE = [
    ("password-hashing",            "Passwords are stored hashed",                     [17]),
    ("email-malware-filtering",     "Email is scanned for malware",                    [76]),
    ("email-spam-filtering",        "Email is filtered for spam",                      [77]),
    ("email-encryption-in-transit", "Email is encrypted in transit",                   [27]),
    ("screen-lock",                 "Workstations lock themselves",                    [29]),
    ("admin-mfa",                   "Admin accounts require MFA",                      [18]),
    ("backup-encryption",           "Backups are encrypted at rest",                   [32]),
    ("data-at-rest-encryption",     "Stored data is encrypted at rest",                [45, 59]),
    ("audit-logging",               "Admin and sign-in activity is logged",            [100, 102]),
    ("device-compliance",           "Only managed devices reach company data",         [54]),
    ("mobile-app-protection",       "Company data on phones is contained",             [60, 61]),
    ("external-sharing-controls",   "Sharing outside the company is controlled",       [26]),
    ("retention-policy",            "Deleted items are retained and recoverable",      [33]),
    ("admin-role-separation",       "Admin roles are separate from user accounts",     [16]),
    ("basic-dlp",                   "Built-in leak protection exists without buying anything", [31]),
]

AH_TPL = """\
id: {aid}
title: {title}
status: skeleton

# The claim: this control is already true for anyone on a normal business
# subscription, and the owner does not know it. Be precise about which tier -
# "Business Premium yes, Business Basic no" is exactly the useful detail.

claim: >
  TODO one sentence. What is already true.

microsoft365:
  applies_to: ""            # e.g. "all tiers" or "Business Premium and above"
  where_to_look: ""         # exact console path
  evidence: ""              # what to screenshot or export

google_workspace:
  applies_to: ""
  where_to_look: ""
  evidence: ""

caveat: >
  TODO. When the claim is NOT true. There is always one. If you skip this the
  tool becomes a liability generator.

answers_rows: {rows}        # line numbers in questions.txt this closes out
concepts: []                # concept ids that should link here
"""


def write(path: Path, text: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return True


def main():
    n = 0
    for iid, name, year, sector, ot in INCIDENTS:
        n += write(K / "incidents" / (iid + ".yaml"), INCIDENT_TPL.format(
            iid=iid, name=name, year=year, sector=sector,
            ot="true" if ot else "false",
        ))

    for pid, name, tell in PATTERNS:
        n += write(K / "patterns" / (pid + ".yaml"), PATTERN_TPL.format(
            pid=pid, name=name, tell=tell,
        ))

    for aid, title, rows in ALREADY_HAVE:
        n += write(K / "already-have" / (aid + ".yaml"), AH_TPL.format(
            aid=aid, title=title, rows="[" + ", ".join(map(str, rows)) + "]",
        ))

    print("created {} library files".format(n))
    for sub in ("incidents", "patterns", "already-have"):
        print("  {}: {}".format(sub, len(list((K / sub).glob("*.yaml")))))


if __name__ == "__main__":
    main()
