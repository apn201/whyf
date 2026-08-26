"""The four cards that are not controls, plus the three demo cards."""

CARDS = {

    # ---- not controls -----------------------------------------------------

    "company-profile": dict(
        priority=1,
        plain_english=(
            "Background questions about your company. Name, headcount, how many "
            "data centres, sometimes revenue. They often feel too detailed for a "
            "security assessment, because they are."),
        response=(
            "This is not a security question and there is no verdict to give. "
            "Type in what you are willing to type in. Revenue and headcount "
            "breakdowns are not needed to assess your security, and you are "
            "allowed to leave them blank or answer roughly. Nobody has ever lost "
            "a contract over an approximate headcount. If a field is mandatory "
            "and you do not want to give the exact figure, give a range and say "
            "it is a range."),
        refer_to=(
            "Nobody. This is admin. If the form demands financial detail you are "
            "not comfortable sharing, that is a question for whoever owns the "
            "customer relationship, not for security."),
        answer_risk="none",
    ),

    "incident-history": dict(
        priority=1,
        plain_english=(
            "Have you been breached, and if so what happened. Sometimes phrased as "
            "five years, sometimes ever. Often sitting right next to a question "
            "about whether any customer has ever complained."),
        response=(
            "This tool will not help you word this answer. That is not caution, it "
            "is the whole rule: everything else here is an opinion about a control, "
            "but this is a statement of fact about your past. Get it wrong and it "
            "is a misrepresentation, not a failed control. If there is an insurance "
            "policy anywhere near this contract, a wrong answer here can void it. "
            "Go and find out what actually happened before you tick anything. "
            "Separately, and this is the useful part: you should be keeping this "
            "list anyway. Write down what happened, when, why, and what you changed "
            "afterwards. Then answering questions like this is five minutes instead "
            "of a week of asking around."),
        refer_to=(
            "Your insurance broker before you answer, if you have cyber cover or "
            "are applying for it. Your lawyer if the incident involved personal "
            "data or a customer claim. Not IT, and not this tool."),
        answer_risk="disclosure",
    ),

    "certification": dict(
        priority=2,
        plain_english=(
            "Do you hold a certificate. ISO 27001, SOC 2, Cyber Essentials, that "
            "family."),
        response=(
            "Sometimes a certificate is required by law, by regulation, or by a "
            "customer who will not sign without it. When it is not required, fixing "
            "your processes is worth more than certifying them. A certificate is "
            "not proof that you are secure. It is proof that somebody looked at "
            "your process on one day and it matched what you said it was. It is "
            "expensive and it eats the same people who would otherwise be fixing "
            "things, so getting certified is not a goal on its own. What it does "
            "buy you is a shortcut: one line on the form can close a whole section "
            "of questions, and that is a real commercial saving if you are getting "
            "these questionnaires every month. Count how many you got last year "
            "before you decide."),
        refer_to=(
            "Whoever owns the biggest customer relationship. They know whether a "
            "certificate is actually being asked for or whether somebody just put "
            "it on a wish list."),
        answer_risk="certification",
    ),

    "cyber-insurance": dict(
        priority=2,
        plain_english=(
            "Do you have a cyber insurance policy."),
        response=(
            "Cyber insurance is there to carry the risk you cannot mitigate away, "
            "which is the last slice after you have done the affordable controls. "
            "It is difficult to get now and the questions are hard, and that is "
            "the second reason to look at it: an insurer's application form is a "
            "free gap analysis with money attached at the end. Having a policy "
            "also signals maturity, because insurers do not hand them out to "
            "companies with no MFA. Careful with the answers, though. An insurance "
            "application is a warranty. If you say you have something and you do "
            "not, the policy may not pay when you need it."),
        refer_to=(
            "A broker who does cyber, not your general business insurance contact. "
            "Ask them for the application form before you commit to anything, and "
            "read it as a to-do list."),
        answer_risk="warranty",
    ),

    # ---- demo card 1: the agent declining to do work ----------------------

    "ics-inventory": dict(
        priority=1,
        plain_english=(
            "Do you know which systems control your machines. The PLCs, the SCADA "
            "boxes, the controllers on the line. A list of them, kept current."),
        misunderstanding=(
            "Nothing fancy. ICS, OT, IIoT all mean roughly the same thing here: "
            "the computers that control machines rather than people. The word "
            "cartography turns up in these questions and scares people. It means a "
            "list. If you have no machines, you have no list to make, and that is "
            "the whole answer."),
        skeptic_case=(
            "If you do not run a factory, a plant, a pumping station or a building "
            "management system, this does not apply to you at all and you should "
            "say so rather than inventing something. These questions come from "
            "industrial templates and get sent to accountants and software "
            "companies without anyone rereading them. Answering as if you had OT "
            "when you do not is how you end up committing to controls you will "
            "never build."),
        applies_if=["has_ot"],
        applies_never_if=["has_ot_none"],
        how_to_say_no=(
            "Not applicable. We do not operate industrial control systems, "
            "SCADA or PLC equipment. Our IT asset inventory is described under the "
            "asset management questions."),
        default_verdict="not-applicable",
        question="Do you have machines with their own control computers?",
        options=[
            ("no_ot", "No machines", "not-applicable",
             "Say so plainly and point them at your normal IT asset list. This is "
             "an industrial template landing on the wrong company. It happens "
             "constantly and nobody minds."),
            ("some_ot", "A few, in a building or a workshop", "write-it-down",
             "Then it is a short list, not a project. Building management, access "
             "control, a couple of machines. An afternoon with a notepad and you "
             "are done."),
            ("real_ot", "A plant or production line", "do-it-properly",
             "This one is genuinely worth the work, and not because of the "
             "questionnaire. You cannot patch, segment or recover what you have not "
             "listed, and OT is where the expensive outages live."),
        ],
        ladder=(2,
                "Rung 4 wants the list tied into a live discovery tool that keeps "
                "itself current. On an OT network, passive discovery kit is five "
                "figures and it will find things your engineers already knew about. "
                "A spreadsheet that someone actually updates when a machine changes "
                "beats an expensive tool nobody looks at.",
                [(1, "Nobody has written down what is on the line.", "do-it-properly"),
                 (2, "A list exists, per site, and it is roughly right.", "already-solved"),
                 (3, "List covers everything and is checked on a schedule.", "cheap-checkbox"),
                 (4, "Automated discovery keeps the list current by itself.", "cheap-checkbox")]),
        costs={"a list in a spreadsheet": "€",
               "list plus a yearly walk-around": "€€",
               "passive OT discovery tooling": "€€€€"},
        sec=2, chk=3,
        evidence=("Somebody says they know what is out there.",
                  "A spreadsheet per site with make, model and firmware version.",
                  "The list, plus a dated record of the last time it was checked "
                  "against reality, plus who owns each machine."),
        frameworks=["nist-csf-id.am-01", "nist-csf-id.am-02", "nis2-art21"],
        patterns=["outcome-as-process"],
        already_have=[],
        answer_risk="none",
    ),

    # ---- demo card 2: the security-versus-commercial split ----------------

    "dlp": dict(
        priority=1,
        plain_english=(
            "Do you have a control to stop sensitive data leaving your company "
            "electronically. Email, USB, uploads, someone forwarding a customer "
            "list to their private address."),
        misunderstanding=(
            "Many think it is just a tool. It is a process and a policy, and the "
            "tool is the last part. Somebody first has to decide what sensitive "
            "means here. Is it your IP, or personal data, or card numbers? Then "
            "somebody has to decide what happens when the tool blocks something, "
            "and who is allowed to release it. That should not be IT. IT does not "
            "know whether that spreadsheet was supposed to go to that customer."),
        skeptic_case=(
            "The question names a product category, so people go and buy the "
            "product category. A real DLP rollout is months of tuning, a queue of "
            "false positives nobody has time to clear, and a permanent argument "
            "with sales about attachments. Meanwhile Microsoft 365 and Google "
            "Workspace both ship basic policies that catch card numbers and "
            "national ID numbers, off by default, free, and enough to answer this "
            "question honestly. Turn those on, write down what you class as "
            "sensitive, and only buy a platform when you can name the leak you are "
            "trying to stop."),
        applies_if=["has_customer_data", "processes_personal_data"],
        applies_never_if=[],
        how_to_say_no=(
            "Not applicable in the product sense. We do not operate a dedicated "
            "data loss prevention platform. Our data handling rules and the "
            "controls that enforce them are described in the data classification "
            "and email security answers."),
        default_verdict="cheap-checkbox",
        question="Has anyone written down what counts as sensitive here?",
        options=[
            ("no_idea", "Not really", "write-it-down",
             "Start there, not with a purchase. One page listing what must not "
             "leave and who decides. Without it you cannot configure any tool, and "
             "you cannot answer this question honestly either."),
            ("written", "Yes, it is written down", "cheap-checkbox",
             "Then turn on the built-in policies in the mail and file platform you "
             "already pay for, point at those, and stop. That answers the question "
             "and costs nothing."),
            ("regulated", "Yes, and losing it would be reportable", "do-it-properly",
             "Card data, health data, or a regulator who will ask. Now the tool is "
             "worth the tuning cost, because the alternative is a notification "
             "letter."),
        ],
        ladder=(2,
                "Rung 4 adds monitoring on top of blocking: somebody watching the "
                "release queue and tuning the rules. That is most of a full-time "
                "job, or a managed service on a monthly bill. For the great "
                "majority of companies asked this question, the risk it removes is "
                "smaller than the salary it costs.",
                [(1, "No rules, no tooling, nobody has thought about it.", "write-it-down"),
                 (2, "Sensitive is defined, built-in policies are on.", "already-solved"),
                 (3, "A tool blocks, and someone owns the exceptions.", "cheap-checkbox"),
                 (4, "Blocking plus monitoring plus continuous tuning.", "cheap-checkbox")]),
        costs={"decide what sensitive means": "€",
               "turn on what M365 or Workspace already has": "€",
               "a real DLP platform, licensed": "€€€",
               "the same platform, tuned and watched": "€€€€"},
        sec=1, chk=3,
        evidence=("The policy says data must be handled carefully.",
                  "A written definition of sensitive data, plus screenshots of the "
                  "policies switched on in your mail platform.",
                  "The definition, the enabled policies, a sample of blocked "
                  "events, and the name of the person outside IT who releases them."),
        frameworks=["nist-csf-pr.ds-01", "nist-csf-pr.ds-02", "iso27002-8.12"],
        patterns=["technology-prescription", "framework-inheritance"],
        already_have=["basic-dlp", "external-sharing-controls"],
        answer_risk="none",
    ),

    # ---- demo card 3: the verdict that flips ------------------------------

    "rpo": dict(
        priority=1,
        plain_english=(
            "How much recent work you can afford to lose if a system dies. Not how "
            "often you back up. How much you are willing to redo."),
        misunderstanding=(
            "Backup frequency is not an RPO. Nightly backups mean you already "
            "decided on 24 hours, you just did not decide it on purpose. The "
            "question is not asking whether you have backups. It is asking whether "
            "anyone chose the number."),
        skeptic_case=(
            "For most companies the honest answer is 24 hours and that is fine. "
            "Going below it means continuous replication, which means paying for "
            "the same storage twice and building a restore process nobody will "
            "test. If losing a day of work would cost you less than the "
            "difference, do not buy anything. Write the number down and move on."),
        applies_if=["any_business_data"],
        applies_never_if=[],
        how_to_say_no=(
            "Not applicable in the form asked. This control assumes the supplier "
            "holds or processes your data. We do not. Our own maximum tolerable "
            "data loss is defined for the systems supporting this contract and is "
            "stated below."),
        default_verdict="need-one-fact",
        question="If everything broke at 3pm, could you live with losing today's work?",
        options=[
            ("yes_fine", "Annoying, not fatal", "write-it-down",
             "Your RPO is 24 hours and the nightly backup already meets it. This is "
             "a documentation job, not a purchase. One paragraph, one afternoon."),
            ("painful", "Painful, we would survive", "cheap-checkbox",
             "Answer 24 hours honestly, then decide separately whether the two or "
             "three systems that actually hurt deserve a shorter one. Do not buy a "
             "platform to fix three systems."),
            ("no_way", "Business stops", "do-it-properly",
             "A day of lost transactions is not a documentation problem. The "
             "questionnaire has accidentally found something worth money."),
            ("dont_know", "No idea", "need-one-fact",
             "Then that is the work. Ask the person who would have to redo it. Ten "
             "minutes to get the answer, and it changes what you spend."),
        ],
        ladder=(2,
                "Rung 4 is continuous replication with a tested failover. That is "
                "six figures of storage and engineering to move from losing a day "
                "to losing a minute. No questionnaire has ever been failed for "
                "answering rung 2 with a real number and a restore test attached.",
                [(1, "Nobody decided. Backups happen, or they do not.", "write-it-down"),
                 (2, "A number exists per system and the nightly backup meets it.", "already-solved"),
                 (3, "Per-system numbers by criticality, restores tested on a schedule.", "do-it-properly"),
                 (4, "Continuous replication and automated failover.", "cheap-checkbox")]),
        costs={"24 hours": "€", "4 hours": "€€", "1 hour": "€€€", "15 minutes": "€€€€"},
        sec=1, chk=3,
        evidence=("Policy says backups are taken.",
                  "Policy plus a backup schedule per system.",
                  "A documented number per system, backup reports, and a record of "
                  "the last restore test."),
        frameworks=["nist-csf-pr.ds-11", "nist-csf-rc.rp-01", "iso27002-8.13", "nis2-art21"],
        patterns=["outcome-as-process"],
        already_have=["retention-policy", "backup-encryption"],
        answer_risk="none",
    ),
}
