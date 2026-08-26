"""Privacy and data-transfer cards.

A whole section of a modern questionnaire is GDPR machinery aimed at a
supplier acting as a processor. It is mostly contractual, mostly cheap, and
mostly answered badly because people reach for the security answer when the
question is a legal one.
"""

CARDS = {

    "dpa": dict(
        priority=1,
        plain_english=(
            "Do you have a standard data processing agreement, and does it "
            "contain what Article 28 requires."),
        misunderstanding=(
            "People treat this as paperwork and it is, but it is paperwork "
            "with a fixed shape. Article 28 lists what has to be in it: act "
            "only on documented instructions, confidentiality obligations on "
            "staff, security measures, rules for subprocessors, help with data "
            "subject requests, help with breach notification, delete or return "
            "at the end, and allow audits. A DPA missing any of those is not a "
            "DPA. The other half people miss is which side of it they are on: "
            "if you decide why the data is processed you are a controller and "
            "this is a different conversation entirely."),
        skeptic_case=(
            "Do not have a lawyer draft one from nothing. The clauses are "
            "prescribed by the regulation, every large processor publishes "
            "theirs, and the sensible move is to start from a good published "
            "one and have a lawyer check the edits. What is worth paying for "
            "is the review, not the drafting. And do not sign the customer's "
            "version unread: customer DPAs routinely contain audit rights and "
            "notification windows that are fine for a large supplier and "
            "impossible for a small one."),
        applies_if=["processes_personal_data", "has_customer_data"],
        applies_never_if=["no_personal_data"],
        how_to_say_no=(
            "Not applicable. We do not process personal data on behalf of "
            "customers in delivering this service. Where personal data is "
            "involved we act as controller, and our privacy notice describes "
            "that separately."),
        default_verdict="write-it-down",
        question="Do you handle personal data because a customer told you to?",
        options=[
            ("no", "No personal data at all", "not-applicable",
             "Then say so and the whole privacy section shortens dramatically. "
             "Be sure though: names and work email addresses of your "
             "customer's staff are personal data."),
            ("controller", "Yes, but we decide what happens to it", "write-it-down",
             "Then you are a controller, not a processor, and a DPA is the "
             "wrong instrument. Say which role you are in. Getting this "
             "backwards is the most common mistake in this section."),
            ("processor", "Yes, on their instructions", "do-it-properly",
             "Then you need a DPA and it is not optional. Start from a "
             "published one, get it checked, and have it ready before the next "
             "questionnaire rather than during it."),
        ],
        ladder=None,
        costs={"adapt a published DPA": "€",
               "legal review of your standard terms": "€€",
               "negotiating each customer's version separately": "€€€"},
        sec=0, chk=3,
        evidence=("We have terms and conditions.",
                  "A standard DPA covering the Article 28 requirements.",
                  "The DPA, signed with customers, plus the subprocessor list "
                  "it refers to."),
        frameworks=["gdpr-art30", "gdpr-art32", "iso27002-5.20"],
        patterns=["documentation-only"],
        already_have=[],
        answer_risk="warranty",
    ),

    "subprocessors": dict(
        priority=1,
        plain_english=(
            "Do you keep a list of the other companies that touch your "
            "customers' data, and do you tell customers before it changes."),
        misunderstanding=(
            "Everybody thinks of the obvious ones and forgets the rest. Your "
            "hosting provider is a subprocessor. So is your email platform, "
            "your support desk tool, your analytics, your backup service, and "
            "the freelancer who logs in occasionally. If customer personal "
            "data passes through it, it belongs on the list. The notification "
            "half is the part with teeth: most DPAs give the customer a window "
            "to object before you add one, and adding a subprocessor without "
            "telling anyone is a contractual breach even when the new supplier "
            "is better than the old one."),
        skeptic_case=(
            "There is nothing to buy and the list is short, usually under "
            "fifteen names. The cost is remembering to update it, which is why "
            "it belongs next to the procurement question rather than in a "
            "security folder. Publishing it on your website with an email "
            "subscribe link is the cheapest possible way to meet the "
            "notification obligation, and it converts a recurring contractual "
            "risk into a page you update."),
        applies_if=["processes_personal_data", "has_customer_data"],
        applies_never_if=["no_personal_data"],
        how_to_say_no=(
            "Not applicable. We engage no subprocessors in the delivery of "
            "this service. Any change to that position would be notified in "
            "advance under our data processing agreement."),
        default_verdict="write-it-down",
        question="Could you list today everyone whose systems touch a customer's data?",
        options=[
            ("yes", "Yes, there is a list", "already-solved",
             "Publish it and add an email notification list. That satisfies "
             "the advance notice obligation permanently and costs an hour."),
            ("no", "Not without going through invoices", "write-it-down",
             "An afternoon with the finance list, marking everything that "
             "touches customer data. It is nearly always fewer than fifteen "
             "and it answers several questions at once."),
        ],
        ladder=(2,
                "Rung 4 wants the list maintained automatically as the "
                "organisation changes. In a company with fifteen subprocessors "
                "that changes twice a year, a published page and a habit beats "
                "a system nobody feeds.",
                [(1, "No list.", "write-it-down"),
                 (2, "A current list, published, with notification.", "already-solved"),
                 (3, "Criticality assessed, contracts flow down obligations.", "cheap-checkbox"),
                 (4, "Maintained automatically with change notification.", "cheap-checkbox")]),
        costs={"a list and a published page": "€",
               "flow-down clauses in each contract": "€€",
               "subprocessor management tooling": "€€€"},
        sec=1, chk=3,
        evidence=("We know who our suppliers are.",
                  "A current subprocessor list naming each company, what it "
                  "does and where it is.",
                  "The list, published or contractually provided, plus the "
                  "notification mechanism and evidence it has been used."),
        frameworks=["gdpr-art30", "nist-csf-gv.sc-04", "iso27002-5.20"],
        patterns=[],
        already_have=[],
        answer_risk="warranty",
    ),

    "data-transfers": dict(
        priority=1,
        plain_english=(
            "Does customer data leave Europe, and if it does, what makes that "
            "legal."),
        misunderstanding=(
            "People answer this about their own servers and forget everything "
            "else. Your support tool, your error tracking, your analytics and "
            "your AI features may all move data outside the EEA without anyone "
            "deciding to. The legal part has two halves and most answers only "
            "cover one: the mechanism, usually Standard Contractual Clauses or "
            "an adequacy decision, and the assessment of whether the "
            "destination country's authorities could compel access anyway. "
            "That second half is the one that has been litigated and the one "
            "buyers in regulated sectors actually read."),
        skeptic_case=(
            "You are not going to build your own transfer impact assessment "
            "from first principles, and you do not have to. The large "
            "providers publish theirs, the clauses are standard text you adopt "
            "rather than negotiate, and for most suppliers the honest answer "
            "is a short list of where data goes and which mechanism covers "
            "each. Where it gets genuinely expensive is promising to keep data "
            "in one region, so do not promise that unless you have checked "
            "every tool in the path."),
        applies_if=["processes_personal_data", "operates_in_eu"],
        applies_never_if=["no_personal_data"],
        how_to_say_no=(
            "Applicable and limited. Customer data is processed within the "
            "EEA. Where a subprocessor operates outside it, the transfer "
            "mechanism and the countries involved are listed below."),
        default_verdict="need-one-fact",
        question="Do you know every country your customer data touches?",
        options=[
            ("eea", "It all stays in the EEA", "already-solved",
             "Then say so and name the regions. Check your support desk and "
             "error tracking before you commit to it, because those are where "
             "the surprise usually is."),
            ("some", "Some of it goes to the US or elsewhere", "write-it-down",
             "List which tools, which countries, and which mechanism covers "
             "each. That list is the whole answer and it takes an afternoon."),
            ("unknown", "Not really", "do-it-properly",
             "Then that is the work, and it is the same list as the "
             "subprocessor one with a country column added. You cannot answer "
             "any of this section without it."),
        ],
        ladder=(2,
                "Rung 4 is a documented transfer impact assessment per "
                "destination with legal review. That is real work and it is "
                "proportionate for a large processor. Knowing where the data "
                "goes and which mechanism applies is the step that closes most "
                "of the exposure.",
                [(1, "Nobody knows where the data goes.", "do-it-properly"),
                 (2, "Destinations and mechanisms listed.", "already-solved"),
                 (3, "Transfer assessments documented per destination.", "cheap-checkbox"),
                 (4, "Assessed, legally reviewed and reviewed on change.", "cheap-checkbox")]),
        costs={"list the destinations and mechanisms": "€",
               "adopt standard contractual clauses": "€",
               "transfer impact assessment with legal review": "€€€",
               "guaranteeing regional data residency": "€€€€"},
        sec=0, chk=3,
        evidence=("Our data is in Europe.",
                  "A list of processing locations with the transfer mechanism "
                  "for each.",
                  "The list, the executed clauses, and an assessment of "
                  "government access risk for each destination."),
        frameworks=["gdpr-art30", "gdpr-art32", "iso27002-5.34"],
        patterns=[],
        already_have=[],
        answer_risk="warranty",
    ),

    "personal-data-breach": dict(
        priority=1,
        plain_english=(
            "If personal data leaks, do you know who you have to tell, and how "
            "fast."),
        misunderstanding=(
            "This is not the same question as incident response, and answering "
            "it with your incident plan misses the point. A personal data "
            "breach has its own clock and its own audience. As a processor "
            "your first obligation is usually to your customer, without undue "
            "delay, and your contract probably sets a tighter number than the "
            "regulation does, often twenty-four or forty-eight hours. The "
            "controller then has seventy-two hours to the regulator. And it is "
            "not only about theft: losing access to personal data, or "
            "destroying it by accident, is also a personal data breach, which "
            "surprises people whose plan only covers attackers."),
        skeptic_case=(
            "Nothing to buy. The whole control is a page saying who decides it "
            "is a personal data breach, who they tell, in what order, and by "
            "when, with the contractual deadlines written down rather than "
            "looked up on the day. What is expensive is discovering during an "
            "incident that three customer contracts each specify a different "
            "notification window."),
        applies_if=["processes_personal_data"],
        applies_never_if=["no_personal_data"],
        how_to_say_no=(
            "Applicable. A defined process covers identification, assessment "
            "and notification of personal data breaches, including the "
            "contractual notification timeframes agreed with customers."),
        default_verdict="write-it-down",
        question="What is the shortest breach notification deadline in any of your customer contracts?",
        options=[
            ("known", "I know the number", "already-solved",
             "Then write it down next to the incident plan with the customer "
             "contact route. You are ahead of most suppliers."),
            ("unknown", "No idea", "do-it-properly",
             "Go and look. It is usually twenty-four or forty-eight hours, it "
             "is shorter than the regulation, and it is the deadline you will "
             "actually miss. An hour with the contracts now."),
        ],
        ladder=(2,
                "Rung 4 wants breach handling integrated across the incident "
                "process, tested, with templates ready. Templates are worth "
                "having. The step that matters is much earlier: knowing the "
                "contractual deadline before the day you need it.",
                [(1, "No process, deadlines unknown.", "do-it-properly"),
                 (2, "Process written, contractual deadlines known.", "already-solved"),
                 (3, "Templates prepared, contacts confirmed.", "cheap-checkbox"),
                 (4, "Exercised as part of incident response.", "cheap-checkbox")]),
        costs={"a page, and reading your contracts": "€",
               "prepared templates and contact routes": "€€",
               "legal on standby for notifications": "€€€"},
        sec=1, chk=3,
        evidence=("We would tell the customer.",
                  "A written process naming who assesses, who notifies, and "
                  "within what deadline.",
                  "The process, the per-customer deadlines, templates, and "
                  "evidence it has been exercised or used."),
        frameworks=["gdpr-art32", "nist-csf-rs.co-02", "nis2-art23"],
        patterns=[],
        already_have=[],
        answer_risk="warranty",
    ),

    "dsar": dict(
        priority=2,
        plain_english=(
            "Can you find, export or delete one person's data when they ask, "
            "or when your customer asks on their behalf."),
        misunderstanding=(
            "As a processor you are rarely the one who answers the request, "
            "but you are contractually obliged to help the customer answer it, "
            "and that means being able to find one person's data across your "
            "systems within days. People discover the real problem at that "
            "point: the data is in the product database, and the support desk, "
            "and the backups, and an analytics tool, and nobody has ever tried "
            "to assemble it. Backups are the argument that always comes up, "
            "and the accepted position is that you do not have to unpick a "
            "backup, you have to not restore the deleted data back into "
            "production."),
        skeptic_case=(
            "Do not buy a privacy platform for this. The control is knowing "
            "where personal data lives, which is the data inventory question "
            "again, and having tried the exercise once. Run one search for a "
            "real person and time it. That single dry run tells you more than "
            "any policy and gives you a defensible answer."),
        applies_if=["processes_personal_data"],
        applies_never_if=["no_personal_data"],
        how_to_say_no=(
            "Applicable. We assist customers in responding to data subject "
            "requests within the timeframes set out in our data processing "
            "agreement. The systems in scope and the process are described "
            "below."),
        default_verdict="write-it-down",
        question="Could you find everything you hold about one named person this week?",
        options=[
            ("yes", "Yes, we have done it", "already-solved",
             "Then say so and say how long it took. A tested answer beats a "
             "described one everywhere on this form."),
            ("probably", "Probably, never tried", "write-it-down",
             "Try it once with a real record. You will find one system nobody "
             "remembered, which is exactly the point of doing it now rather "
             "than under a deadline."),
            ("no", "No", "do-it-properly",
             "Start with where personal data actually lives. This is the data "
             "inventory question wearing a different hat, and it blocks "
             "several answers in this section."),
        ],
        ladder=None,
        costs={"one dry run and write down what happened": "€",
               "documented process across systems": "€€",
               "privacy request tooling": "€€€"},
        sec=0, chk=2,
        evidence=("We would help if asked.",
                  "A written process covering which systems are searched and "
                  "within what timeframe.",
                  "The process, plus a record of a completed or rehearsed "
                  "request and how long it took."),
        frameworks=["gdpr-art30", "iso27002-5.34"],
        patterns=[],
        already_have=["retention-policy"],
    ),

    "data-retention": dict(
        priority=1,
        plain_english=(
            "Do you have rules about how long you keep things, and do you "
            "actually delete when the time is up."),
        misunderstanding=(
            "The instinct is to keep everything forever because storage is "
            "cheap, and that instinct is the risk. Data you no longer hold "
            "cannot leak, cannot be demanded in a dispute, and cannot appear "
            "in a breach notification. The other half people miss is that "
            "deletion has to reach the copies: the export somebody made, the "
            "support ticket with the attachment, the backup that will restore "
            "it all next month. And retention is not one number. Invoices have "
            "a legal minimum, personal data has a legal maximum, and those "
            "pull in opposite directions."),
        skeptic_case=(
            "Do not build a records management programme. Pick the handful of "
            "data types that matter, put a number against each, and turn on "
            "the retention settings your platforms already have. Where it gets "
            "expensive is retrofitting deletion into an old product that was "
            "built assuming nothing ever goes away, and that is worth knowing "
            "before you promise a customer a deletion timeframe."),
        applies_if=["any_business_data"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. Retention periods are defined by data type and "
            "deletion is applied at expiry. Periods and the systems they cover "
            "are described below."),
        default_verdict="write-it-down",
        question="What happens to a customer's data a year after they leave?",
        options=[
            ("deleted", "It gets deleted on a schedule", "already-solved",
             "Then state the periods and say what covers backups. That last "
             "part is what gets asked next."),
            ("kept", "It is still there", "write-it-down",
             "Decide the numbers and turn on the retention settings you "
             "already pay for. Data you do not hold cannot be breached, and "
             "this is the rare control that reduces both risk and cost."),
        ],
        ladder=(2,
                "Rung 4 wants retention applied and evidenced across every "
                "system including backups and archives, reviewed on change. "
                "Backups are the expensive part and the accepted position is "
                "that they age out rather than being unpicked. Defined periods "
                "actually applied to live systems is the useful level.",
                [(1, "Everything kept forever.", "write-it-down"),
                 (2, "Periods defined and applied to live systems.", "already-solved"),
                 (3, "Applied across systems, backups age out on schedule.", "cheap-checkbox"),
                 (4, "Evidenced everywhere and reviewed on change.", "cheap-checkbox")]),
        costs={"decide the periods, turn on platform retention": "€",
               "apply it across systems": "€€",
               "retrofit deletion into an old product": "€€€€"},
        sec=2, chk=3,
        evidence=("We delete things eventually.",
                  "A retention schedule by data type with the periods.",
                  "The schedule, the platform settings enforcing it, and how "
                  "backups and exports are covered."),
        frameworks=["gdpr-art30", "iso27002-5.33", "nist-csf-pr.ds-01"],
        patterns=["documentation-only"],
        already_have=["retention-policy"],
    ),

    "secure-disposal": dict(
        priority=2,
        plain_english=(
            "When a laptop is reassigned or a disk is thrown away, is the data "
            "gone."),
        misunderstanding=(
            "Physical destruction gets all the attention and matters least for "
            "most companies. If the disk is encrypted and you destroy the key, "
            "the data is gone without a shredder, and that is what a wipe on a "
            "modern device does. The real gaps are elsewhere: the machine that "
            "went to a member of staff's family, the phone traded in, the "
            "server returned to the leasing company, and cloud storage that "
            "was never deleted because nobody owned it."),
        skeptic_case=(
            "Certified destruction with certificates per drive is priced for "
            "organisations disposing of hundreds. For a company retiring five "
            "laptops a year, a documented wipe procedure and a note of what "
            "happened to each device is a complete and defensible answer. "
            "Spend the effort on the leaving process instead, because "
            "equipment that is never returned cannot be wiped at all."),
        applies_if=["has_employees"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. Devices are wiped or cryptographically erased before "
            "reassignment or disposal, and a record is kept. The procedure is "
            "described below."),
        default_verdict="write-it-down",
        question="Where is the last laptop that left the company?",
        options=[
            ("known", "I know, and it was wiped", "already-solved",
             "Then write the procedure down and keep the record per device. "
             "That record is the evidence, and it is a line in a spreadsheet."),
            ("unknown", "Not sure", "write-it-down",
             "Start the record now. The procedure is the easy part; knowing "
             "which devices exist and where they went is the part that fails."),
        ],
        ladder=None,
        costs={"a wipe procedure and a spreadsheet": "€",
               "certified destruction with certificates": "€€€"},
        sec=2, chk=2,
        evidence=("We wipe machines before reuse.",
                  "A written disposal procedure covering wipe and disposal "
                  "routes.",
                  "The procedure plus a per-device record of what was done and "
                  "when."),
        frameworks=["iso27002-7.14", "nist-csf-pr.ds-01"],
        patterns=[],
        already_have=["data-at-rest-encryption", "device-compliance"],
    ),
}
