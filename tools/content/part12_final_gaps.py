"""The last three, from the 329-question coverage run.

Everything else in that run's no-card list turned out to be a sub-question of
a card that already exists. These three are not.
"""

CARDS = {

    "vulnerability-disclosure": dict(
        priority=1,
        plain_english=(
            "If a stranger finds a hole in your product or your website, do "
            "they have a way to tell you."),
        misunderstanding=(
            "This gets read as a bug bounty question and it is not. A bounty "
            "is a programme with a budget and a triage queue. Disclosure is "
            "just having a route: a published address and a promise not to sue "
            "the person who uses it. Without one, a researcher who finds "
            "something has three options, and two of them are publishing it "
            "and selling it. The absence of a route does not mean nobody finds "
            "your bugs. It means you hear about them last."),
        skeptic_case=(
            "Do not start a bounty. Bounties generate volume, most of it low "
            "quality, and they need somebody to triage every submission or "
            "your reputation gets worse rather than better. The whole control "
            "at this size is a security.txt file on your website, a monitored "
            "mailbox behind it, and one paragraph saying you will not take "
            "legal action against somebody reporting in good faith. That "
            "paragraph is the part that matters and it costs nothing."),
        applies_if=["has_website", "sells_software"],
        applies_never_if=[],
        how_to_say_no=(
            "Partially applicable. We do not operate a bug bounty programme. A "
            "published route exists for reporting security issues and is "
            "described below, along with our response commitment."),
        default_verdict="write-it-down",
        question="If a stranger found a flaw in your website today, where would they send it?",
        options=[
            ("published", "There is a published address", "already-solved",
             "Then say so, name it, and mention the safe-harbour wording. That "
             "is a complete answer and better than most bounty programmes."),
            ("guess", "They would guess at an address", "write-it-down",
             "Publish a security.txt and point it at a mailbox somebody reads. "
             "An hour of work, and it decides whether you hear about your own "
             "bugs before your customers do."),
            ("bounty", "We run a bounty", "cheap-checkbox",
             "Then answer with it. Be ready for the follow-up about how "
             "quickly you respond, because that is what the buyer is really "
             "asking."),
        ],
        ladder=(2,
                "Rung 4 is a paid bounty with response-time commitments. That "
                "is a queue and a budget, and it makes sense once you have "
                "somebody whose job includes triage. A published route with a "
                "safe-harbour statement is where the risk of learning late "
                "actually drops.",
                [(1, "No route, no address.", "write-it-down"),
                 (2, "Published address with safe-harbour wording.", "already-solved"),
                 (3, "Defined triage and response commitment.", "cheap-checkbox"),
                 (4, "Paid bounty programme.", "cheap-checkbox")]),
        costs={"security.txt and a monitored mailbox": "€",
               "a stated response commitment": "€€",
               "bug bounty with payouts and triage": "€€€€"},
        sec=2, chk=2,
        evidence=("People could email us.",
                  "A published disclosure route, usually security.txt or a "
                  "page on the site.",
                  "The route, the safe-harbour statement, and evidence of a "
                  "report being received and handled."),
        frameworks=["nist-csf-id.ra-01", "nist-csf-rs.ma-02", "iso27002-5.5"],
        patterns=[],
        already_have=[],
    ),

    "supplier-monitoring": dict(
        priority=1,
        plain_english=(
            "You checked the supplier before signing. Do you ever look again."),
        misunderstanding=(
            "Almost every third-party control happens once, at onboarding, and "
            "then never. But the supplier you assessed three years ago has "
            "been acquired, moved its hosting, lost the people who answered "
            "your questionnaire, and possibly been breached. The assessment "
            "you hold describes a company that no longer exists. This is the "
            "half of supplier risk that gets skipped, and it is the half where "
            "the incident actually arrives from."),
        skeptic_case=(
            "Continuous supplier risk monitoring is a subscription with a "
            "score per vendor, and the score is derived from things visible "
            "from the outside, which is not the same as their security. For a "
            "handful of critical suppliers, two free things beat it: a news "
            "alert on each supplier's name, and a contract clause obliging "
            "them to tell you when they have an incident. The second is worth "
            "more than any score, because a supplier who has to tell you is a "
            "supplier you find out about on day one rather than from the "
            "press."),
        applies_if=["has_suppliers"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable and proportionate. Critical suppliers are reassessed "
            "periodically and are contractually obliged to notify us of "
            "security incidents. Ongoing monitoring beyond that is described "
            "below."),
        default_verdict="write-it-down",
        question="How would you find out your main supplier had been breached?",
        options=[
            ("contract", "They would have to tell us", "already-solved",
             "That is the control worth having, and it is a contract clause "
             "rather than a product. Say so, and say which suppliers it "
             "covers."),
            ("news", "I would probably read about it", "write-it-down",
             "Add a notification clause at the next renewal and set a news "
             "alert on the critical few in the meantime. Both free."),
            ("never", "I might not", "do-it-properly",
             "That is the gap. Your incident becomes their incident with a "
             "delay, and the delay is where the damage compounds."),
        ],
        ladder=(2,
                "Rung 4 is a monitoring platform scoring every supplier "
                "continuously. It measures what is visible from outside, which "
                "correlates loosely with what matters. A notification clause "
                "and a periodic reassessment of the critical few is the "
                "version that actually tells you something.",
                [(1, "Assessed once, never revisited.", "do-it-properly"),
                 (2, "Critical suppliers reassessed, notification in contract.", "already-solved"),
                 (3, "Scheduled reassessment with criticality tiers.", "cheap-checkbox"),
                 (4, "Continuous monitoring across the supplier base.", "cheap-checkbox")]),
        costs={"notification clause and a news alert": "€",
               "periodic reassessment of the critical few": "€€",
               "supplier risk monitoring subscription": "€€€€"},
        sec=2, chk=3,
        evidence=("We would hear about it.",
                  "A reassessment schedule for critical suppliers plus the "
                  "notification obligation in contract.",
                  "The schedule with dated reassessments, the contract clause, "
                  "and evidence of a notification being received or requested."),
        frameworks=["nist-csf-gv.sc-07", "nist-csf-gv.sc-10", "iso27002-5.22"],
        patterns=[],
        already_have=[],
    ),

    "disciplinary-process": dict(
        priority=2,
        plain_english=(
            "If somebody breaks the security rules on purpose, what actually "
            "happens to them."),
        misunderstanding=(
            "This looks like the most bureaucratic line on the form and it is "
            "the one that makes every other policy real. A rule with no "
            "consequence is advice. The part people get wrong is the "
            "direction: this is not about punishing the person who clicked a "
            "phishing link, and treating it that way is actively harmful "
            "because it teaches people to hide incidents. It is about "
            "deliberate or grossly negligent breach, and it needs to say so "
            "explicitly, or your reporting culture pays for it."),
        skeptic_case=(
            "Nothing to buy and no reason to skip it, because HR almost "
            "certainly has a disciplinary process already and the security "
            "answer is a cross-reference to it. What is worth the extra "
            "sentence is the carve-out: reporting your own mistake is not a "
            "disciplinary matter. Without that written down, the first person "
            "to lose a laptop will not tell you for three days."),
        applies_if=["has_employees"],
        applies_never_if=["sole_trader"],
        how_to_say_no=(
            "Applicable. Deliberate or negligent breaches of security policy "
            "are handled through our disciplinary process. Self-reported "
            "mistakes are explicitly excluded, and the reason is stated below."),
        default_verdict="write-it-down",
        question="If somebody reported that they had just clicked a phishing link, what would happen?",
        options=[
            ("thanked", "They would be thanked", "already-solved",
             "That is the right culture. Write it down so it survives a change "
             "of manager, and cross-reference the disciplinary process for the "
             "deliberate cases."),
            ("trouble", "They would be in some trouble", "do-it-properly",
             "Fix that before anything else on this page. People who fear the "
             "consequence report late, and late reporting is what turns a "
             "contained incident into a notifiable one."),
        ],
        ladder=None,
        costs={"cross-reference the HR process, add the carve-out": "€"},
        sec=2, chk=2,
        evidence=("HR would deal with it.",
                  "The security policy referencing the disciplinary process, "
                  "with the self-reporting carve-out stated.",
                  "The reference, the carve-out, and evidence staff have "
                  "accepted the policy containing it."),
        frameworks=["nist-csf-gv.rr-04", "iso27002-6.4", "iso27002-6.2"],
        patterns=["documentation-only"],
        already_have=[],
    ),
}
