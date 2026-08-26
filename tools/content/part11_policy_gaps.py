"""The last of the gaps found by testing against real question sets.

Deliberately not written: cards named after one company's tooling. A question
set drawn from an internal IT policy carries product names and internal
naming schemes, and a card called after somebody's privilege-elevation product
would be useless to everyone else and awkward for the company it came from.
The generic control underneath is what gets a card.
"""

CARDS = {

    "ropa": dict(
        priority=1,
        plain_english=(
            "Do you have a written record of what personal data you handle, "
            "why, and who else sees it. GDPR calls it a record of processing "
            "activities."),
        misunderstanding=(
            "There is a small-company exemption in Article 30 and almost "
            "nobody qualifies for it, because it falls away the moment "
            "processing is regular rather than occasional, and payroll alone "
            "is regular. So the practical answer for most companies is that "
            "they need one. The other misunderstanding is scale: this is a "
            "table, not a project. Each row is a purpose, and most companies "
            "have between eight and fifteen: payroll, recruitment, customers, "
            "marketing, CCTV, and so on."),
        skeptic_case=(
            "No tool required and no consultant. Most supervisory authorities "
            "publish a template spreadsheet for exactly this, free, and it is "
            "the same table a privacy platform would sell you. Where it earns "
            "its keep is not compliance: filling it in is the only exercise "
            "that reliably shows you where personal data actually lives, which "
            "is the prerequisite for answering deletion, transfer and subject "
            "request questions."),
        applies_if=["processes_personal_data"],
        applies_never_if=["no_personal_data"],
        how_to_say_no=(
            "Applicable. A record of processing activities is maintained "
            "covering the purposes for which we process personal data, the "
            "categories involved, recipients, transfers and retention."),
        default_verdict="write-it-down",
        question="Is there a table anywhere listing what personal data you hold and why?",
        options=[
            ("yes", "Yes, and it is current", "already-solved",
             "Then say so and note when it was last reviewed. It also answers "
             "the data inventory, transfer and retention questions, so point "
             "at it repeatedly."),
            ("old", "There was one, years ago", "write-it-down",
             "Update it rather than starting again. An out-of-date record is "
             "still most of the work already done."),
            ("no", "No", "write-it-down",
             "Download your supervisory authority's template and spend a "
             "morning on it. Eight to fifteen rows. It unlocks several other "
             "answers on this form."),
        ],
        ladder=None,
        costs={"a template spreadsheet, filled in": "€",
               "reviewed yearly with an owner": "€",
               "privacy management platform": "€€€"},
        sec=1, chk=3,
        evidence=("We know what data we hold.",
                  "A record of processing activities with purposes and "
                  "categories.",
                  "The record, with recipients, transfers, retention periods "
                  "and a review date."),
        frameworks=["gdpr-art30", "nist-csf-id.am-05", "iso27002-5.34"],
        patterns=["documentation-only"],
        already_have=[],
        answer_risk="warranty",
    ),

    "monitoring-privacy": dict(
        priority=1,
        plain_english=(
            "You monitor company systems for security. Are you allowed to, and "
            "have you told anybody."),
        misunderstanding=(
            "Almost every answer to the logging and monitoring questions on a "
            "questionnaire describes capability and ignores legality. In "
            "Europe monitoring employees is employment law and data protection "
            "law before it is a security control: it needs a lawful basis, it "
            "has to be proportionate to an actual purpose, people have to be "
            "told, and in several countries the works council has to be "
            "consulted before you switch it on. Doing it quietly is not a "
            "grey area, it is the thing that produces a fine and an "
            "unenforceable dismissal."),
        skeptic_case=(
            "This costs a page and a conversation, and skipping it can "
            "invalidate the monitoring you already paid for. The trap in the "
            "other direction is over-collecting because a tool offers it: "
            "keystroke logging, screen capture and browsing histories are "
            "rarely proportionate for a normal company and each one raises the "
            "bar you have to justify. Collect what security genuinely needs, "
            "say so, and leave the rest switched off."),
        applies_if=["has_employees"],
        applies_never_if=["sole_trader"],
        how_to_say_no=(
            "Applicable. Monitoring is limited to what is necessary for "
            "security and operational integrity, staff are informed, and "
            "access to any user content is authorised and proportionate. The "
            "lawful basis and consultation position are described below."),
        default_verdict="write-it-down",
        question="Have your staff been told what is monitored?",
        options=[
            ("yes", "Yes, in writing", "already-solved",
             "Then say so and name where. That single fact turns your "
             "monitoring answers from a capability claim into a defensible "
             "one."),
            ("no", "Not really", "do-it-properly",
             "Write it down and tell people. In parts of Europe you may also "
             "need to consult the works council before monitoring continues, "
             "and that is a legal question rather than a security one."),
        ],
        ladder=(2,
                "Rung 4 wants documented proportionality assessments per "
                "monitoring capability with legal review. Proportionate for a "
                "large employer. A written notice, a stated purpose and "
                "authorised access to content is the level that makes the "
                "monitoring lawful and usable.",
                [(1, "Monitoring happens, nobody has been told.", "do-it-properly"),
                 (2, "Staff informed, purpose and limits written down.", "already-solved"),
                 (3, "Lawful basis documented, content access authorised.", "cheap-checkbox"),
                 (4, "Assessed per capability with legal and council review.", "cheap-checkbox")]),
        costs={"a page in the handbook": "€",
               "legal review of the basis": "€€",
               "works council consultation": "€€€"},
        sec=1, chk=2,
        evidence=("We log things.",
                  "A written notice to staff describing what is monitored and "
                  "why.",
                  "The notice, the lawful basis, who may access user content "
                  "and under what authorisation, and any consultation record."),
        frameworks=["gdpr-art32", "iso27002-5.34", "iso27002-8.15"],
        patterns=[],
        already_have=["audit-logging"],
    ),

    "local-admin-rights": dict(
        priority=1,
        plain_english=(
            "Can people install and run whatever they like on their own "
            "laptop, or do they have to ask."),
        misunderstanding=(
            "Removing local admin rights is treated as an unpopular "
            "restriction and it is the single highest-value endpoint control "
            "there is: most malware that lands on a laptop needs those rights "
            "to persist. The mistake is doing it without an escape hatch. If "
            "the only way to install a legitimate tool is a three-day ticket, "
            "people find a workaround and you have traded a technical control "
            "for a social one. Temporary elevation on request, logged, is what "
            "makes the removal stick."),
        skeptic_case=(
            "The removal itself is free and is a policy setting. The elevation "
            "tooling that makes it bearable is a per-seat licence, and it is "
            "worth it above roughly twenty machines because below that the "
            "requests can go through a person. Where companies waste money is "
            "buying the tooling first and never actually removing the rights, "
            "which is the common outcome and produces a licence bill and no "
            "control."),
        applies_if=["has_employees"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. Standing local administrator rights are not granted "
            "by default. Where they are required they are justified, recorded "
            "and reviewed, and temporary elevation is logged."),
        default_verdict="do-it-properly",
        question="Can the average person here install software on their laptop?",
        options=[
            ("yes", "Yes, everybody can", "do-it-properly",
             "This is the highest-value endpoint change available to you, and "
             "it costs nothing to make. Pair it with a fast route to get "
             "elevation when it is genuinely needed, or people will route "
             "around it."),
            ("some", "Some people have it", "cheap-checkbox",
             "Then write down who, why, and when it gets reviewed. A short "
             "justified list is a good answer; an undocumented one is not."),
            ("no", "No, and there is a request route", "already-solved",
             "That is the strong answer. Say whether elevation requests are "
             "logged, because that is what gets asked next."),
        ],
        ladder=(3,
                "Rung 4 wants every elevated session recorded and reviewed. "
                "Recording is a licence tier and reviewing it is somebody's "
                "time. Rights removed by default, with justified exceptions "
                "and logged elevation, is where the risk actually drops.",
                [(1, "Everyone is a local administrator.", "do-it-properly"),
                 (2, "Removed for most, undocumented exceptions.", "cheap-checkbox"),
                 (3, "Removed by default, exceptions justified, elevation logged.", "already-solved"),
                 (4, "Elevated sessions recorded and reviewed.", "cheap-checkbox")]),
        costs={"remove the rights, handle requests manually": "€",
               "temporary elevation tooling per seat": "€€",
               "elevation with session recording and review": "€€€€"},
        sec=3, chk=3,
        evidence=("Most people are not administrators.",
                  "The policy plus a report of who holds local admin rights.",
                  "The report, the justification and review date for each "
                  "exception, and logs of temporary elevation."),
        frameworks=["nist-csf-pr.aa-05", "nist-csf-pr.ps-01", "iso27002-8.2"],
        patterns=[],
        already_have=["device-compliance", "admin-role-separation"],
    ),

    "evidence-preservation": dict(
        priority=2,
        plain_english=(
            "During an incident, does anybody stop to preserve what happened "
            "before wiping the machine and moving on."),
        misunderstanding=(
            "The instinct under pressure is to get the business running again, "
            "and that instinct destroys the answer to what happened. Rebuild "
            "the server and the evidence goes with it. Pull the power and you "
            "lose everything that was only in memory. It matters more than "
            "people expect, because you cannot tell a customer or a regulator "
            "what was accessed if you deleted the means of finding out, and "
            "not knowing usually means notifying everybody."),
        skeptic_case=(
            "Forensic readiness as a discipline, with imaging kit and chain of "
            "custody forms, is for organisations that expect litigation. For "
            "everyone else this is one line in the incident plan: before you "
            "rebuild anything, take a snapshot and copy the logs off. In a "
            "virtualised or cloud environment that is a button, it takes "
            "minutes, and it is the difference between an investigation and a "
            "shrug."),
        applies_if=["has_servers", "any_business_data"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. Our incident process requires preservation of system "
            "state and logs before affected systems are rebuilt or restored."),
        default_verdict="write-it-down",
        question="If a server were compromised tonight, what would happen to it first?",
        options=[
            ("rebuild", "It would get rebuilt fast", "do-it-properly",
             "Add one line to the incident plan: snapshot and export the logs "
             "before rebuilding. It costs minutes and it is the difference "
             "between knowing what was taken and having to assume the worst."),
            ("snapshot", "Snapshot first, then rebuild", "already-solved",
             "Then say so. It is a short answer and a genuinely strong one, "
             "because almost nobody does it."),
        ],
        ladder=None,
        costs={"one line in the incident plan": "€",
               "somewhere to keep images and logs": "€€",
               "forensic readiness with chain of custody": "€€€€"},
        sec=2, chk=2,
        evidence=("We would investigate.",
                  "The incident process requiring preservation before "
                  "rebuild.",
                  "The process, plus where images and logs are kept and for "
                  "how long."),
        frameworks=["nist-csf-rs.an-06", "nist-csf-rs.an-07", "iso27002-5.28"],
        patterns=[],
        already_have=["audit-logging"],
    ),

    "byod": dict(
        priority=1,
        plain_english=(
            "Are people allowed to use their own phones and laptops for work, "
            "and what are they allowed to reach."),
        misunderstanding=(
            "The question people argue about is whether to allow it. The "
            "question that matters is what a personal device is allowed to "
            "reach, and those are different decisions. Email on a personal "
            "phone with the data contained is a very different exposure from a "
            "personal laptop with a copy of the customer database on it. The "
            "second trap is legal: you cannot wipe somebody's own phone, and "
            "in several countries attempting to would be a serious problem, so "
            "any answer that promises remote wipe of personal devices is "
            "promising something you should not do."),
        skeptic_case=(
            "Banning personal devices outright is clean and expensive, because "
            "it means issuing a phone to everybody who needs email. The middle "
            "ground is where most companies should sit: personal devices get "
            "browser or contained app access only, company devices get "
            "everything, and the boundary is enforced at login rather than in "
            "a policy nobody reads."),
        applies_if=["has_employees", "has_mobile_devices"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. Personally owned devices may access defined services "
            "only, through controls that contain company data. Full device "
            "management is not applied to devices we do not own, and the "
            "boundary is described below."),
        default_verdict="write-it-down",
        question="Can somebody read work email on a phone the company did not buy?",
        options=[
            ("no", "No, company devices only", "already-solved",
             "Cleanest answer available and it simplifies several other "
             "questions. Say how it is enforced, because saying it is policy "
             "is weaker than saying it is enforced at login."),
            ("contained", "Yes, but the data is contained", "already-solved",
             "That is the sensible middle and it is included in the licence "
             "you probably already have. Say what can be wiped and what "
             "cannot."),
            ("open", "Yes, no particular controls", "do-it-properly",
             "Decide what a personal device may reach. Browser-only access to "
             "cloud apps costs nothing and removes most of the exposure "
             "without a fight about people's own property."),
        ],
        ladder=(2,
                "Rung 4 wants management on every connecting device including "
                "personal ones. On a device you do not own that is a licence "
                "cost, an argument, and in some countries a legal problem. "
                "Containment plus a defined boundary is the achievable target.",
                [(1, "Personal devices reach anything.", "do-it-properly"),
                 (2, "Defined boundary, company data contained.", "already-solved"),
                 (3, "Enforced at login with device conditions.", "cheap-checkbox"),
                 (4, "Full management on personally owned devices.", "cheap-checkbox")]),
        costs={"decide the boundary and write it down": "€",
               "app containment in your existing licence": "€",
               "issue company devices to everyone": "€€€€"},
        sec=2, chk=2,
        evidence=("People use their own phones sometimes.",
                  "A written statement of what personal devices may access.",
                  "The statement, the technical control enforcing it, and what "
                  "can be removed from a personal device."),
        frameworks=["nist-csf-pr.aa-05", "iso27002-6.7", "iso27002-8.1"],
        patterns=[],
        already_have=["mobile-app-protection", "device-compliance"],
    ),
}
