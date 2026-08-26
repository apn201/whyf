"""Generate the public, synthetic corpus.

The real corpus is three questionnaires somebody else wrote, plus a completed
assessment of a named company. None of that can go in a public repository:
the questionnaire text is the asker's, the vendor instrument behind q2 is a
commercial product, and the assessment is confidential. See corpus/README.md.

So the real rows live in `private/` and never leave this machine, and the repo
ships this instead: questions written here, from the concept catalog, in plain
English. The underlying controls are industry-standard and nobody owns "do
admin accounts need a second factor" - what is owned is a particular set of
questions, in a particular wording and arrangement, and none of that is copied.

The synthetic corpus is not a paraphrase of the real one. It is generated from
`CONTROLS` below, which was written against concept ids, and it has never been
diffed against the source text. It exists so that:

  * the repo is runnable from clean, which the submission rules require;
  * a judge can paste something in and watch the tiers fire;
  * the tests have a corpus even when `private/` is absent.

It is deliberately blander than the real thing. Real questionnaires are worse
written than this, and the coverage numbers reported against the private corpus
are the honest measure of whether the agent copes.

    python tools/gen_synthetic.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "corpus" / "synthetic.tsv"

# concept id -> (control phrase, direct question, ladder?)
#
# The phrase completes "X ...". The question is asked straight. `ladder` marks
# concepts that also get a four-rung maturity version, which is how roughly two
# thirds of real questionnaire rows arrive.
CONTROLS = {
    # -- governance ---------------------------------------------------------
    "dpo": (
        "a data protection officer has been appointed where the law requires one",
        "Does anyone here have data protection as their actual job?", False),
    "ransom-payment": (
        "somebody has decided in advance who may authorise paying an extortion demand",
        "If ransomware hit tonight, who could say yes to paying?", True),
    "clean-desk": (
        "staff are told not to leave sensitive paper or screens on show",
        "What happens to a printed customer list at the end of the day?", False),
    "ai-governance": (
        "there are rules about which AI tools may be used and what may be put into them",
        "Can staff paste customer data into an AI tool?", True),

    "business-context": (
        "the organisation has written down what it does and which services matter most",
        "Which of your services would hurt most if they stopped?", False),
    "acceptable-use": (
        "staff are told in writing what they may and may not do with company equipment",
        "Is there an acceptable use policy staff have seen?", False),
    "personnel-security": (
        "background checks are carried out before someone is given sensitive access",
        "Are new staff screened before they get access to sensitive systems?", True),
    "nis2-scope": (
        "the organisation has established whether NIS2 applies to it",
        "Has anyone checked whether NIS2 covers your sector and size?", False),
    "cyber-insurance": (
        "the organisation holds a cyber insurance policy",
        "Do you carry cyber insurance?", False),
    "board-oversight": (
        "the owners or board are told regularly how security is going",
        "How often do the owners hear about security?", True),
    "executive-protection": (
        "senior people get extra protection on their personal accounts and devices",
        "Are directors' personal accounts protected any differently?", True),
    "security-policy": (
        "a written security policy exists and is kept current",
        "Do you have a security policy, and when was it last touched?", True),
    "security-roles": (
        "somebody is named as responsible for security",
        "Who is responsible for security here?", True),
    "risk-appetite": (
        "security spending decisions are weighed against the risk they remove",
        "How do you decide what a security fix is worth?", True),
    "improvement": (
        "what went wrong last time is written down and acted on",
        "Do you write down what you learned after something went wrong?", True),
    "legal-compliance": (
        "the laws that apply to the organisation's data have been identified",
        "Which data protection rules apply to you?", False),

    "isms": (
        "the security policy, risk work and management review happen on a cycle",
        "Does anything review your security on a schedule?", True),
    "soc2": (
        "a SOC 2 report covering the relevant criteria is available under NDA",
        "Do you have a SOC 2 report, and which criteria does it cover?", False),
    "pci-dss": (
        "card data either does not touch your systems or the scope is documented",
        "Do card numbers ever touch your systems?", False),
    "hipaa": (
        "a business associate agreement is in place where US health data is handled",
        "Do you handle US health data for a customer?", False),
    "dora": (
        "contracts with financial customers carry audit, notification and exit terms",
        "Do you supply anyone in EU financial services?", False),
    "dpa": (
        "a data processing agreement covering the required clauses is in place",
        "Do you process personal data because a customer told you to?", False),
    "subprocessors": (
        "the other companies that touch customer data are listed and notified on change",
        "Which other companies touch your customers data?", True),
    "data-transfers": (
        "where customer data leaves Europe, the transfer mechanism is documented",
        "Does customer data ever leave Europe?", True),
    "personal-data-breach": (
        "there is a defined process and deadline for telling customers about a data breach",
        "How fast must you tell a customer their data leaked?", True),
    "dsar": (
        "one persons data can be found and exported across systems on request",
        "Could you find everything you hold about one named person?", False),
    "data-retention": (
        "how long each kind of data is kept is decided, and deletion happens at expiry",
        "What happens to a customers data a year after they leave?", True),
    "secure-disposal": (
        "devices are wiped before reassignment or disposal and a record is kept",
        "Where is the last laptop that left the company?", False),
    "risk-acceptance": (
        "controls that cannot be met are recorded as time-limited exceptions",
        "What happens when you cannot do what the policy requires?", True),
    "security-metrics": (
        "a small set of security measures is tracked and reviewed with management",
        "Name one security number you could quote right now.", True),
    "shared-accounts": (
        "every person has their own login rather than sharing one",
        "Does anyone log in with a password other people also know?", False),
    "least-privilege": (
        "people hold only the access their job needs, and it is reviewed",
        "When somebody changes job, does their old access go away?", True),
    "attack-surface": (
        "what of yours answers on the public internet is listed and checked",
        "Could you list everything of yours reachable from the internet?", True),
    "credential-monitoring": (
        "leaked staff credentials are made harmless by a second factor",
        "If a staff password leaked tomorrow, would it get anybody in?", True),
    "shadow-it": (
        "the cloud services people actually use are known and new ones get approved",
        "If somebody wanted a new SaaS tool tomorrow, who would they ask?", True),
    "rto": (
        "how long the business can be down before it hurts is decided per system",
        "If your main system died this morning, when would it cost real money?", True),

    "ropa": (
        "there is a written record of what personal data is held and why",
        "Is there a table listing what personal data you hold and why?", False),
    "monitoring-privacy": (
        "staff have been told what is monitored, and the basis for it is written down",
        "Have your staff been told what is monitored?", True),
    "local-admin-rights": (
        "people cannot install what they like on a work laptop without asking",
        "Can the average person here install software on their laptop?", True),
    "evidence-preservation": (
        "a compromised machine is snapshotted before anybody rebuilds it",
        "If a server were compromised tonight, what happens to it first?", False),
    "byod": (
        "what a personally owned phone or laptop may reach is decided and enforced",
        "Can somebody read work email on a phone the company did not buy?", True),

    # -- identify -----------------------------------------------------------
    "rpo": (
        "the amount of recent work the organisation can afford to lose is decided per system",
        "If everything broke this afternoon, how much work could you afford to lose?", True),
    "ics-inventory": (
        "a list of industrial control equipment is kept up to date",
        "Do you have a list of your industrial control equipment?", True),
    "supplier-inventory": (
        "the outside firms that can log in anywhere are written down somewhere",
        "Which outside firms can log in to your systems?", True),
    "asset-inventory": (
        "a list of computers, software and services in use is kept up to date",
        "Do you know what computers and software you own?", True),
    "data-classification": (
        "data is sorted into categories so the sensitive parts can be treated differently",
        "Do you separate sensitive data from ordinary data?", True),
    "secure-procurement": (
        "security is looked at before equipment is bought, not after",
        "Do you check security before buying equipment?", False),
    "risk-assessment": (
        "the organisation has thought through what could go wrong and written it down",
        "Have you written down what could go wrong?", True),
    "threat-intelligence": (
        "somebody watches for news of attacks relevant to this organisation",
        "Does anyone track threats aimed at your industry?", True),

    # -- access -------------------------------------------------------------
    "mfa": (
        "a second authentication factor is required for administrator accounts",
        "Do administrator accounts need a second factor?", True),
    "sso": (
        "staff sign in to business applications through one identity provider",
        "Do your applications share one login?", True),
    "password-policy": (
        "password rules are set centrally and applied everywhere",
        "What are your password rules?", True),
    "default-passwords": (
        "passwords shipped with equipment are changed before it is used",
        "Do you change the password that came with new equipment?", False),
    "passwords": (
        "stored passwords cannot be read back, only checked",
        "How are stored passwords protected?", False),
    "identity-lifecycle": (
        "accounts are created when someone joins and closed when they leave",
        "What happens to an account when somebody leaves?", True),
    "privileged-accounts": (
        "administrator accounts are separate from ordinary accounts and reviewed",
        "Do admins use a separate account for admin work?", True),
    "sod": (
        "no single person can complete a sensitive transaction alone",
        "Can one person approve and make a payment on their own?", False),
    "plc-access": (
        "controllers and the code that runs on them are protected from casual access",
        "Can anyone on the factory floor reach the controllers?", False),
    "remote-access": (
        "access from outside the office is controlled and can be switched off",
        "How do people connect from outside the office?", True),
    "remote-work-model": (
        "the organisation has decided what people may reach from home and on which devices",
        "What can staff reach when working from home?", True),

    # -- data ---------------------------------------------------------------
    "dlp": (
        "tooling watches for sensitive data leaving the organisation",
        "Is anything watching for sensitive data leaving?", True),
    "full-disk-encryption": (
        "laptop and phone storage is encrypted",
        "Are laptop drives encrypted?", True),
    "encryption": (
        "stored and transmitted data is encrypted and the keys are looked after",
        "Is your data encrypted, and who holds the keys?", True),
    "tenant-segregation": (
        "one customer's data cannot be reached from another customer's account",
        "Can one customer see another customer's data?", False),
    "email-security": (
        "incoming mail is filtered and sensitive mail is protected in transit",
        "What happens to a malicious attachment sent to your staff?", True),
    "dns-filtering": (
        "requests to known-bad web addresses are blocked before they connect",
        "Are known-bad websites blocked?", True),
    "removable-media": (
        "use of USB storage is limited to what the work actually needs",
        "Can staff plug a USB stick into a work machine?", True),
    "screen-lock": (
        "unattended machines lock themselves",
        "Do machines lock when nobody is at them?", False),
    "backups": (
        "backups are taken, encrypted, and cover the systems that matter",
        "What do your backups actually cover?", True),
    "offline-backups": (
        "at least one backup copy cannot be reached from the systems it protects",
        "Could ransomware reach your backups too?", True),

    # -- continuity ---------------------------------------------------------
    "bia": (
        "the organisation has worked out which processes must come back first",
        "Which part of the business has to come back first?", True),
    "continuity-testing": (
        "recovery plans are tried out rather than only written",
        "When did you last try restoring from a backup?", True),
    "bcp": (
        "a plan exists for carrying on when systems are unavailable",
        "What is the plan if your systems are down for a week?", True),

    # -- operations ---------------------------------------------------------
    "patch-management": (
        "updates are applied on a schedule and unsupported equipment is tracked",
        "How quickly do security updates get installed?", True),
    "vulnerability-management": (
        "systems are scanned for known weaknesses and the findings are fixed",
        "Does anything scan your systems for known weaknesses?", True),
    "hardening": (
        "systems are built from a standard configuration rather than one at a time",
        "Are machines set up the same way every time?", True),
    "application-allowlisting": (
        "only approved software is allowed to run",
        "Can staff install whatever software they like?", True),
    "endpoint-protection": (
        "computers run software that detects and stops malicious code",
        "What is running on the laptops to catch malware?", True),
    "change-management": (
        "changes to systems are approved before they are made",
        "Who approves a change before it goes in?", True),
    "capacity-management": (
        "there is enough headroom that normal growth does not cause an outage",
        "Do you track whether systems are running out of room?", True),

    # -- network ------------------------------------------------------------
    "wireless-security": (
        "the wireless network is protected and guests are kept separate",
        "Is your guest wifi separate from the office network?", True),
    "ddos-protection": (
        "there is some protection against being flooded off the internet",
        "What happens if someone floods your internet connection?", True),
    "network-segmentation": (
        "the network is divided so a problem in one part does not reach the rest",
        "Can a compromised laptop reach the factory network?", True),
    "perimeter-defence": (
        "traffic in and out of the network passes through a firewall that is configured on purpose",
        "Who decides what your firewall lets through?", True),
    "mobile-device-management": (
        "company data on phones can be managed and removed",
        "Can you wipe company data off a lost phone?", True),

    # -- applications -------------------------------------------------------
    "secure-development": (
        "software is written with security in mind and test data is not real data",
        "Do your developers work against real customer data?", True),
    "application-security-testing": (
        "applications are tested for weaknesses before they are released",
        "Is the software tested for security before it ships?", True),

    # -- physical and people ------------------------------------------------
    "physical-environmental-protection": (
        "equipment is protected from fire, water, heat and power loss",
        "What happens to the server room if the power goes?", True),
    "hardware-tampering": (
        "equipment is checked for signs of having been interfered with",
        "Would you notice if someone opened one of your machines?", True),
    "surveillance": (
        "entrances are monitored and visitors are recorded",
        "Are visitors signed in and accompanied?", True),
    "physical-access-control": (
        "only the people who need to be somewhere can get in",
        "Who can walk into the room where the servers are?", True),
    "security-awareness": (
        "staff are told what to watch for and reminded regularly",
        "When did staff last get security training?", True),

    # -- detect -------------------------------------------------------------
    "security-monitoring": (
        "somebody actually looks at security alerts",
        "Who looks at the security alerts?", True),
    "logging": (
        "systems keep records of who did what, and the records are protected",
        "Would you be able to tell what happened after a break-in?", True),
    "audits-and-pentests": (
        "an outsider tests the defences from time to time",
        "Has anyone from outside tried to break in on purpose?", True),

    # -- respond ------------------------------------------------------------
    "incident-reporting": (
        "there is a decision made in advance about who has to be told, and how fast",
        "Who has to be told if you are breached, and within how long?", True),
    "incident-response-testing": (
        "the response plan is rehearsed with the people who would run it",
        "Have you ever walked through an incident as a rehearsal?", True),
    "ir-retainer": (
        "the people who would be called in an emergency are lined up in advance",
        "Who would you call at 2am?", True),
    "ics-emergency-modes": (
        "production can be stopped or run in a reduced mode safely",
        "Can you stop the line safely if you need to?", False),
    "crisis-management": (
        "there is a named group who take charge when something serious happens",
        "Who takes charge when something serious happens?", True),
    "incident-response": (
        "there is a written process for handling a security incident",
        "What do you do in the first hour after a breach?", True),

    # -- third parties ------------------------------------------------------
    "cloud-provider-assurance": (
        "the organisation knows what its cloud providers are responsible for",
        "What is your cloud provider responsible for, and what are you?", True),
    "third-party-access": (
        "supplier access to systems is logged and reviewed",
        "Do you know which suppliers logged in last month?", True),
    "third-party-contracts": (
        "supplier contracts say what is expected of them on security",
        "Do your supplier contracts mention security at all?", True),
    "antivirus-exclusions": (
        "vendor software does not require security tooling to be turned off for it",
        "Does any vendor ask you to exclude their software from scanning?", False),
    "third-party-risk": (
        "suppliers are assessed before they are given access",
        "Do you check a supplier's security before signing?", True),
}

# Not controls. These exercise the classifier's other three classes.
NON_CONTROL = {
    "company-profile": [
        ("Organisation name", "admin", ""),
        ("Number of employees", "admin", ""),
        ("Name and email of the person completing this form", "admin", ""),
    ],
    "incident-history": [
        ("Has the organisation suffered a security breach in the last five years? "
         "If so, describe it.", "disclosure", ""),
        ("Has any customer claimed their data was exposed by you?", "disclosure", ""),
    ],
    "certification": [
        ("Which security certifications does the organisation hold?", "attestation",
         "ISO/IEC 27001 | SOC 2 | Cyber Essentials | None of these"),
    ],
}

# Generic four-rung ladder. Every questionnaire in the wild uses some version of
# this shape, which is why it is worth having a card field for it.
RUNGS = [
    "Not in place",
    "In place for some systems",
    "In place for all systems",
    "In place for all systems, risk-based, and reviewed at least annually",
]


def sentence(phrase):
    return phrase[0].upper() + phrase[1:] + "."


def main():
    rows = []
    n = 0

    for cid, (phrase, question, ladder) in CONTROLS.items():
        n += 1
        rows.append({
            "id": "syn.{:03d}a".format(n), "concept": cid, "form": "binary_statement",
            "question": sentence(phrase), "options": "",
        })
        rows.append({
            "id": "syn.{:03d}b".format(n), "concept": cid, "form": "binary",
            "question": question, "options": "",
        })
        if ladder:
            rows.append({
                "id": "syn.{:03d}c".format(n), "concept": cid, "form": "maturity_ladder",
                "question": "To what extent is it true that {}?".format(phrase),
                "options": " | ".join(RUNGS),
            })

    for cid, items in NON_CONTROL.items():
        for question, form, options in items:
            n += 1
            rows.append({
                "id": "syn.{:03d}a".format(n), "concept": cid, "form": form,
                "question": question, "options": options,
            })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    cols = ["id", "concept", "form", "question", "options"]
    with OUT.open("w", encoding="utf-8", newline="") as fh:
        fh.write("\t".join(cols) + "\n")
        for r in rows:
            fh.write("\t".join(str(r[c]).replace("\t", " ") for c in cols) + "\n")

    forms = {}
    for r in rows:
        forms[r["form"]] = forms.get(r["form"], 0) + 1
    concepts = {r["concept"] for r in rows}
    print("{} synthetic rows over {} concepts".format(len(rows), len(concepts)))
    for f, c in sorted(forms.items(), key=lambda kv: -kv[1]):
        print("  {:<18} {:>3}".format(f, c))
    print("\nwrote {}".format(OUT.relative_to(ROOT)))

    try:
        sys.path.insert(0, str(ROOT / "tools"))
        from corpus_map import CONCEPTS
        gaps = sorted(set(CONCEPTS) - concepts)
        if gaps:
            print("\nconcepts with no synthetic row: {}".format(gaps))
            return 1
        print("every concept has at least one synthetic row")
    except ImportError:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
