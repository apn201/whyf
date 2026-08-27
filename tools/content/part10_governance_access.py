"""Gaps the coverage report named, in governance and access.

Written from tools/coverage_report.py output rather than from reading another
questionnaire. Each of these was either declined outright or reached as a near
miss with the gap named.
"""

CARDS = {

    "rto": dict(
        priority=1,
        plain_english=(
            "How long you can be down before it really hurts. The sister "
            "question to how much work you can afford to lose, and the one "
            "that gets forgotten."),
        misunderstanding=(
            "People answer this with how long a restore takes, which is "
            "backwards. The recovery time objective is a business decision "
            "about tolerable downtime, made before anyone looks at the "
            "technology. Then you find out what your actual recovery time is, "
            "and the gap between the two is the thing worth money. Most "
            "companies have never measured the second number, which is why "
            "the honest answer to this question is usually a shrug dressed up "
            "as four hours."),
        skeptic_case=(
            "Every hour you shave off recovery costs more than the last one, "
            "and the curve gets vertical near the end. Going from a day to "
            "four hours is usually process and practice. Going from four hours "
            "to fifteen minutes is standby infrastructure you pay for "
            "continuously and use once. Decide the number from what downtime "
            "actually costs you, which is the business impact question, and be "
            "suspicious of any target somebody picked because it sounded "
            "professional."),
        applies_if=["any_business_data"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. Recovery time objectives are defined for the systems "
            "supporting this contract, and our tested recovery time against "
            "them is stated below."),
        default_verdict="need-one-fact",
        question="If your main system died this morning, when would it start costing real money?",
        options=[
            ("day", "End of the day", "write-it-down",
             "Then your target is a day, a normal backup and restore meets it, "
             "and this is a documentation job. Write the number down and time "
             "one restore so the claim has evidence behind it."),
            ("hours", "Within a few hours", "cheap-checkbox",
             "Answer with the target honestly and check what your actual "
             "recovery time is. The gap between them is the only thing here "
             "worth spending on, and you cannot see it without measuring."),
            ("minutes", "Almost immediately", "do-it-properly",
             "Then you need standby capacity and a tested failover, and that "
             "is a real cost. It is also the right cost, because at that "
             "tolerance an outage is more expensive than the infrastructure."),
            ("unknown", "I have never worked it out", "need-one-fact",
             "Start with what an hour of downtime costs. Everything else here "
             "follows from that one number and it takes an afternoon."),
        ],
        ladder=(2,
                "Rung 4 is automated failover tested regularly, which means "
                "paying for a second environment permanently. That is right "
                "for a service somebody depends on by the minute and wasteful "
                "for one measured in days. A stated target with a measured "
                "actual recovery time is the level that survives scrutiny.",
                [(1, "No target, no idea how long recovery takes.", "do-it-properly"),
                 (2, "Target stated, one restore timed against it.", "already-solved"),
                 (3, "Targets per system, tested on a schedule.", "cheap-checkbox"),
                 (4, "Automated failover, regularly exercised.", "cheap-checkbox")]),
        costs={"decide the number and time a restore": "€",
               "shorten recovery through process and practice": "€€",
               "warm standby infrastructure": "€€€€",
               "automated failover": "€€€€€"},
        sec=2, chk=3,
        evidence=("We would get back up quickly.",
                  "A stated recovery time objective per critical system.",
                  "The objectives, plus a dated test showing what recovery "
                  "actually took against them."),
        frameworks=["nist-csf-rc.rp-02", "nist-csf-id.ra-04", "iso27002-5.30", "nis2-art21"],
        patterns=["outcome-as-process"],
        already_have=[],
    ),

    "risk-acceptance": dict(
        priority=1,
        plain_english=(
            "When you cannot meet a control, is there a way to say so on "
            "purpose and have someone accept the risk in writing."),
        misunderstanding=(
            "The absence of this is why questionnaires get lied on. Without an "
            "exception process the only options are pretend you have the "
            "control or admit a gap with nothing attached to it, so people "
            "pretend. With one, a gap becomes a documented decision with an "
            "owner, a reason and a review date, which is a far better answer "
            "and a true one. The other half people get wrong is who accepts: "
            "it has to be someone who carries the consequence, which is "
            "management, not the person who found the gap."),
        skeptic_case=(
            "There is nothing to buy and it takes one page. The only real "
            "argument is against letting it become a queue of permanent "
            "exceptions that nobody revisits, which is what happens when there "
            "is no expiry date. Put a date on every one. An exception without "
            "an expiry is just a gap with better paperwork."),
        applies_if=["any_business_data"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. Controls that cannot be met are recorded as time-"
            "limited exceptions with a named owner, a stated reason, "
            "compensating measures and a review date."),
        default_verdict="write-it-down",
        question="What happens when you cannot do something the policy requires?",
        options=[
            ("documented", "It gets written down and accepted", "already-solved",
             "Then say so and mention the review dates. This is one of the "
             "strongest governance answers available and it costs nothing."),
            ("ignored", "It just does not happen", "write-it-down",
             "One page turns that into a decision. It also makes the rest of "
             "this questionnaire answerable honestly rather than optimistically."),
        ],
        ladder=(2,
                "Rung 4 wants exceptions tracked in a register, tied to the "
                "risk assessment, reviewed at management level on a cycle. The "
                "register is worth having. The tooling around it is not, for a "
                "company with fewer than a dozen live exceptions.",
                [(1, "No process, gaps are silent.", "write-it-down"),
                 (2, "Exceptions written down with owner and expiry.", "already-solved"),
                 (3, "Register maintained and reviewed.", "cheap-checkbox"),
                 (4, "Tied to risk assessment with management sign-off.", "cheap-checkbox")]),
        costs={"one page and a spreadsheet": "€",
               "reviewed register with expiry tracking": "€€"},
        sec=2, chk=3,
        evidence=("We know where our gaps are.",
                  "A written exception process and a current list of "
                  "exceptions.",
                  "The process, the register with owners and expiry dates, and "
                  "evidence that expired ones were revisited."),
        frameworks=["nist-csf-gv.rm-04", "nist-csf-id.ra-06", "iso27002-5.36"],
        patterns=["documentation-only"],
        already_have=[],
    ),

    "security-metrics": dict(
        priority=2,
        plain_english=(
            "Do you measure anything about security, and does anyone look at "
            "the numbers."),
        misunderstanding=(
            "Metrics get confused with reporting. Counting blocked emails is "
            "reporting; it goes up and down and changes nothing. A metric is a "
            "number attached to a decision: how long a critical patch takes to "
            "land, how many admin accounts exist, how long since the last "
            "restore test. Three numbers that would change what you do next "
            "beat a dashboard of forty that nobody acts on."),
        skeptic_case=(
            "Security dashboards are sold on the promise that measurement is "
            "improvement, and mostly they produce a slide. For a company of "
            "this size, pick three numbers, write them down twice a year, and "
            "look at whether they moved. That is a metrics programme and it "
            "costs an hour. The expensive version starts with buying a tool to "
            "collect numbers nobody has decided to act on."),
        applies_if=["any_business_data"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable and deliberately small. A defined set of security "
            "measures is tracked and reviewed with management. The measures "
            "and their frequency are stated below."),
        default_verdict="write-it-down",
        question="Name one security number you could quote right now.",
        options=[
            ("yes", "I could name a few", "already-solved",
             "Then write them down as the official set, with who sees them and "
             "how often. You are describing something you already do."),
            ("no", "Not really", "write-it-down",
             "Pick three: patch latency, admin account count, days since the "
             "last restore test. All three come from systems you already have "
             "and all three would change a decision."),
        ],
        ladder=(2,
                "Rung 4 wants objectives with targets, tracked continuously "
                "and reported to the board with trends. That is a reporting "
                "function. Three numbers reviewed twice a year, that actually "
                "influence what gets done, is where the value is.",
                [(1, "Nothing measured.", "write-it-down"),
                 (2, "A few numbers tracked and reviewed.", "already-solved"),
                 (3, "Objectives with targets, reviewed on a cycle.", "cheap-checkbox"),
                 (4, "Continuous measurement reported with trends.", "cheap-checkbox")]),
        costs={"pick three numbers, review twice a year": "€",
               "objectives with targets and tracking": "€€",
               "a security dashboard product": "€€€"},
        sec=1, chk=2,
        evidence=("We keep an eye on things.",
                  "A written set of security measures with their targets.",
                  "The measures, dated records over time, and evidence that "
                  "management reviewed them."),
        frameworks=["nist-csf-gv.ov-01", "nist-csf-gv.ov-03", "iso27002-5.36"],
        patterns=["documentation-only"],
        already_have=[],
    ),

    "shared-accounts": dict(
        priority=1,
        plain_english=(
            "Does every person have their own login, or do people share one."),
        misunderstanding=(
            "Shared accounts are usually defended as practical and they are, "
            "right up to the first thing that goes wrong. The cost is not "
            "really security, it is that your logs become useless: you can see "
            "what was done and never who did it, which breaks incident "
            "response, breaks accountability, and makes the leaver process "
            "impossible because you cannot remove one person from a shared "
            "password without disrupting everyone. Where sharing is genuinely "
            "unavoidable, on old machinery or a legacy system, the answer is "
            "to name it as an exception and control who can check the "
            "credential out."),
        skeptic_case=(
            "There is almost nothing to buy. Named accounts are free in every "
            "system that supports them, and where a system does not support "
            "them the fix is a password manager with check-out, not a "
            "replacement system. The one legitimate exception is machinery "
            "that physically cannot do it, and the honest answer there is to "
            "say so and describe what compensates."),
        applies_if=["has_employees"],
        applies_never_if=["sole_trader"],
        how_to_say_no=(
            "Applicable. Individual named accounts are used. Where a system "
            "does not support them, the account is listed as an exception with "
            "controlled access and the compensating measures stated."),
        default_verdict="do-it-properly",
        question="Does anyone here log in with a password that other people also know?",
        options=[
            ("no", "No, everyone has their own", "already-solved",
             "Then say so and note any service accounts, because those are the "
             "ones that get asked about next."),
            ("few", "One or two old systems", "write-it-down",
             "Name them as exceptions with what controls access to the "
             "credential. That is a truthful answer and an auditor will take "
             "it. Pretending otherwise is where this goes wrong."),
            ("yes", "Yes, quite a few", "do-it-properly",
             "Worth fixing, and not for the questionnaire. Shared logins mean "
             "your logs cannot tell you who did anything, which is exactly "
             "what you need on the worst day."),
        ],
        ladder=None,
        costs={"create named accounts where systems support it": "€",
               "password manager with check-out for the rest": "€€",
               "replacing a system that cannot do it": "€€€€"},
        sec=3, chk=3,
        evidence=("Everyone has their own login.",
                  "A list of any shared or generic accounts and what they are "
                  "for.",
                  "The list, who can access each, and the record of check-out "
                  "or the compensating control."),
        frameworks=["nist-csf-pr.aa-01", "iso27002-5.16", "iso27002-8.15"],
        patterns=[],
        already_have=["admin-role-separation", "audit-logging"],
    ),

    "least-privilege": dict(
        priority=1,
        plain_english=(
            "Do people have only the access they need, or does everybody end "
            "up with everything."),
        misunderstanding=(
            "Access accumulates. Somebody covers for a colleague, joins a "
            "project, moves department, and each time they gain rights and "
            "never lose any. After three years the finance assistant can reach "
            "systems nobody would grant them today, and no single decision was "
            "wrong. That is the mover half of joiners, movers and leavers, and "
            "it is the half everybody skips. Role-based access is the usual "
            "answer, and it helps, but only if somebody prunes the roles."),
        skeptic_case=(
            "An access governance platform is priced for organisations with "
            "thousands of identities. Below that, the control is a review: "
            "once or twice a year, print who has access to the systems that "
            "matter and ask each manager whether their people still need it. "
            "It is dull, it takes a morning, and it removes more standing "
            "access than any product."),
        applies_if=["has_employees"],
        applies_never_if=["sole_trader"],
        how_to_say_no=(
            "Applicable. Access is granted on the basis of role and reviewed "
            "periodically. Review frequency and the systems covered are stated "
            "below."),
        default_verdict="cheap-checkbox",
        question="When somebody changes job internally, does their old access go away?",
        options=[
            ("yes", "Yes, it gets adjusted", "already-solved",
             "Then say so, and say when access was last reviewed. The review "
             "date is what gets asked for."),
            ("no", "It just accumulates", "do-it-properly",
             "Do one review. Print the access list for your main systems and "
             "walk it with the managers. A morning, and it will surprise you."),
        ],
        ladder=(2,
                "Rung 4 wants automated recertification across every system on "
                "a risk-based frequency. That is an identity governance "
                "platform. A manual review of the systems that matter, once or "
                "twice a year and recorded, removes most of the standing "
                "access a platform would.",
                [(1, "Access only ever accumulates.", "do-it-properly"),
                 (2, "Role-based, adjusted on change.", "cheap-checkbox"),
                 (3, "Reviewed periodically and recorded.", "already-solved"),
                 (4, "Automated recertification across all systems.", "cheap-checkbox")]),
        costs={"an annual review with managers": "€",
               "role definitions maintained": "€€",
               "identity governance tooling": "€€€€"},
        sec=3, chk=3,
        evidence=("People have what they need.",
                  "A description of how access is granted by role.",
                  "The role definitions, plus a dated access review with what "
                  "was removed as a result."),
        frameworks=["nist-csf-pr.aa-05", "iso27002-5.15", "iso27002-5.18"],
        patterns=[],
        already_have=["admin-role-separation", "device-compliance"],
    ),

    "attack-surface": dict(
        priority=1,
        plain_english=(
            "Do you know what of yours is reachable from the internet."),
        misunderstanding=(
            "This is not the same as the asset inventory and it is not the "
            "same as vulnerability scanning. It is the list of things an "
            "outsider can see and reach without any credentials: your website, "
            "the VPN, a mail server, a forgotten test environment somebody "
            "spun up in 2022, the admin interface of an appliance that was "
            "never meant to be public. Attackers enumerate this automatically "
            "and continuously. The question is only whether you have seen the "
            "same list they have."),
        skeptic_case=(
            "Attack surface management is now a product category with a price "
            "to match. You do not need one to start. Your own domain list, a "
            "free external port scan and a look at what your hosting account "
            "actually has running will find the forgotten test environment, "
            "which is the thing that gets exploited. Buy the product when the "
            "estate is too big to eyeball, not before."),
        applies_if=["has_website", "has_network"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. Internet-facing systems and services are inventoried "
            "and reviewed. The scope and review frequency are stated below."),
        default_verdict="do-it-properly",
        question="Could you list everything of yours that answers on the public internet?",
        options=[
            ("yes", "Yes, it is a short list", "already-solved",
             "Then say so and say when you last checked it against reality. "
             "Checking is the part that matters, because the list drifts."),
            ("no", "Not confidently", "do-it-properly",
             "Scan your own ranges and look at what the hosting account is "
             "running. Almost everyone finds something they had forgotten, and "
             "forgotten is exactly what gets exploited."),
        ],
        ladder=(2,
                "Rung 4 is continuous external discovery with alerting on "
                "change, which is a subscription. A list, checked a few times "
                "a year against an actual scan, catches the forgotten test box "
                "that continuous monitoring would also catch, just later.",
                [(1, "Nobody knows what is exposed.", "do-it-properly"),
                 (2, "A list, checked periodically against a scan.", "already-solved"),
                 (3, "Reviewed on change with an owner per service.", "cheap-checkbox"),
                 (4, "Continuous discovery with change alerting.", "cheap-checkbox")]),
        costs={"free external scan and a list": "€",
               "regular scanning with an owner per service": "€€",
               "attack surface management platform": "€€€€"},
        sec=3, chk=3,
        evidence=("We know what we host.",
                  "A list of internet-facing systems with an owner for each.",
                  "The list, a recent external scan confirming it, and the "
                  "date it was last reconciled."),
        frameworks=["nist-csf-id.am-01", "nist-csf-de.cm-09", "iso27002-8.20"],
        patterns=[],
        already_have=[],
    ),

    "credential-monitoring": dict(
        priority=3,
        plain_english=(
            "Do you watch for your staff's email addresses and passwords "
            "turning up in other people's data breaches."),
        misunderstanding=(
            "The dark web framing makes this sound exotic and it is not. "
            "Somebody used their work email on a shopping site, that site got "
            "breached, and now a password they may also have used at work is "
            "in a list. The useful control is not watching a marketplace, it "
            "is making the exposure not matter: a leaked password is harmless "
            "against an account with a second factor."),
        skeptic_case=(
            "Dark web monitoring is sold on fear and it mostly produces a "
            "monthly report of old breaches you can do nothing about. Before "
            "buying any of it: turn on MFA, and turn on breached-password "
            "screening in your identity platform, which blocks known-leaked "
            "passwords at the point somebody tries to set one. That is the "
            "control the monitoring service would eventually tell you to "
            "implement, and you can have it now."),
        applies_if=["has_employees"],
        applies_never_if=[],
        how_to_say_no=(
            "Partially applicable. We do not subscribe to a credential "
            "monitoring service. Exposure of leaked credentials is mitigated "
            "by enforced multi-factor authentication and breached-password "
            "screening, described below."),
        default_verdict="cheap-checkbox",
        question="If a staff password leaked tomorrow, would it get anybody in?",
        options=[
            ("no", "No, MFA everywhere that matters", "already-solved",
             "Then a monitoring subscription buys you very little. Say what "
             "you have instead, which is a stronger answer than the service "
             "would be."),
            ("maybe", "Possibly", "do-it-properly",
             "Fix that first. MFA and breached-password screening cost nothing "
             "on your existing licence and they make the leak irrelevant, "
             "which monitoring never does."),
        ],
        ladder=(1,
                "Every rung above the first is a subscription that tells you "
                "about an exposure you should already have made harmless. The "
                "control that changes outcomes is the second factor, not the "
                "alert.",
                [(1, "MFA and breached-password screening in place.", "already-solved"),
                 (2, "Occasional checks against public breach data.", "cheap-checkbox"),
                 (3, "Monitoring service with alerting.", "cheap-checkbox"),
                 (4, "Continuous monitoring with automated response.", "cheap-checkbox")]),
        costs={"MFA and breached-password screening": "€",
               "free public breach lookup": "€",
               "credential monitoring subscription": "€€€"},
        sec=1, chk=2,
        evidence=("We have not seen anything.",
                  "A statement of what mitigates leaked credentials, naming "
                  "MFA coverage.",
                  "The MFA coverage report, the breached-password setting, and "
                  "any monitoring source used."),
        frameworks=["nist-csf-pr.aa-03", "nist-csf-id.ra-02"],
        patterns=["technology-prescription"],
        already_have=["admin-mfa", "password-hashing"],
    ),

    "shadow-it": dict(
        priority=1,
        plain_english=(
            "Do you know which cloud services and SaaS tools your people "
            "actually use, and is there a way to get a new one approved."),
        misunderstanding=(
            "The reason this matters is not that people use tools. It is that "
            "somebody signs up with a company card, uploads customer data, and "
            "that tool is now a subprocessor nobody has assessed, in a country "
            "nobody has checked, with an account that survives their "
            "departure. Blocking is the instinct and it fails: the tool moves "
            "to a personal account and you lose all visibility instead of "
            "some. An approval route that takes a day is the control, because "
            "people route around a process that takes a month. "
            "The half everyone misses is the tool nobody signed up for. A "
            "free PDF converter, an image compressor, an online translator, "
            "a site that signs documents for you: no account, no company "
            "card, no trace in finance, and somebody has just uploaded the "
            "payroll file to it. The register built from card statements "
            "cannot see any of this, so a company can have a tidy SaaS list "
            "and still be leaking its most sensitive documents through a "
            "browser tab. It is the same rule as the one in the AI policy, "
            "and it is worth writing once in a form that covers both: "
            "confidential data does not go into a service nobody approved, "
            "whether that service is an AI assistant or a file converter."),
        skeptic_case=(
            "A cloud access security broker is a serious purchase aimed at "
            "large estates. You can get most of the way with two free things: "
            "look at what the company card has been paying for, and ask "
            "finance to flag new software subscriptions. That finds the paid "
            "tools. It will not find the free ones, and no amount of looking "
            "at invoices will, so the free ones are covered by a written rule "
            "rather than by discovery: one line saying what must never be "
            "uploaded to a service the company has not approved. Then a "
            "one-page approval route so the next one arrives through the "
            "front door."),
        applies_if=["has_cloud", "has_employees"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. Cloud and SaaS services used for company data are "
            "recorded, and new services are subject to an approval route. The "
            "register and the process are described below."),
        default_verdict="write-it-down",
        question="If somebody wanted a new SaaS tool tomorrow, who would they ask?",
        options=[
            ("someone", "There is a route", "already-solved",
             "Then write it down and keep the register current. Point at it "
             "for the subprocessor question too; it is the same list."),
            ("nobody", "They would just sign up", "write-it-down",
             "Two things: go through the card statements to find what is "
             "already in use, and put a one-page approval route in place so "
             "the next one is visible. Both cheap, both today."),
        ],
        ladder=(2,
                "Rung 4 wants discovery tooling enforcing policy across every "
                "service. That is a broker product and a project. A register "
                "built from the card statement, plus an approval route people "
                "will actually use, gets the visibility that matters.",
                [(1, "No idea what is in use.", "write-it-down"),
                 (2, "A register, and a route for approving new services.", "already-solved"),
                 (3, "Services assessed before approval, register reviewed.", "cheap-checkbox"),
                 (4, "Automated discovery and policy enforcement.", "cheap-checkbox")]),
        costs={"card statements and a one-page route": "€",
               "assessment before approval": "€€",
               "cloud access security broker": "€€€€"},
        sec=2, chk=3,
        evidence=("People use the tools we provide.",
                  "A register of cloud and SaaS services in use.",
                  "The register, the approval route, and evidence a recent "
                  "request went through it."),
        frameworks=["nist-csf-id.am-04", "nist-csf-gv.sc-04", "iso27002-5.23"],
        patterns=[],
        already_have=["external-sharing-controls"],
    ),
}
