"""Cards added after testing against realistic questions.

The first 80 concepts came out of three real questionnaires. These came out of
the questions those questionnaires happened not to contain and real people ask
anyway: a data protection officer, a ransom payment policy, an ISMS, a clean
desk. Every one was confirmed as a gap by putting the question through the
agent and watching it either decline or reach for the nearest neighbour.
"""

CARDS = {

    "dpo": dict(
        priority=1,
        plain_english=(
            "Have you appointed a Data Protection Officer. A specific role "
            "under GDPR, not the same as whoever looks after security."),
        misunderstanding=(
            "Two things get muddled here. First, most companies do not need "
            "one. GDPR requires a DPO only if you are a public body, or your "
            "core activity is large-scale systematic monitoring, or large-scale "
            "processing of special category data. A normal supplier processing "
            "customer contact details is none of those. Second, the DPO cannot "
            "be the person who decides how data gets used. That is a conflict "
            "of interest written into the regulation, so the CEO, the head of "
            "IT and the head of marketing are all disqualified."),
        skeptic_case=(
            "If you are not required to have one, appointing one anyway is a "
            "mistake dressed as diligence. Once you name a DPO and tell the "
            "supervisory authority, you have taken on the whole apparatus: "
            "independence, protection from dismissal over their advice, "
            "resourcing, a reporting line to the top. Companies do this to "
            "look good on a questionnaire and then discover they cannot fire "
            "somebody. Work out whether you need one. If you do not, say so "
            "and name whoever actually owns data protection instead."),
        applies_if=["processes_personal_data", "operates_in_eu"],
        applies_never_if=["no_eu_operations"],
        how_to_say_no=(
            "Not required. We have assessed our processing against Article "
            "37(1) GDPR and do not meet the criteria for mandatory designation. "
            "Responsibility for data protection is assigned and is stated "
            "below."),
        default_verdict="need-one-fact",
        question="Is watching people, or handling health or biometric data, the main thing you do?",
        options=[
            ("no", "No, we just have normal customer data", "not-applicable",
             "Then you almost certainly do not need a DPO. Say that you "
             "assessed it against Article 37 and name whoever owns data "
             "protection instead. That is a complete answer."),
            ("yes", "Yes, at scale", "do-it-properly",
             "Then it is a legal requirement, not a control choice, and the "
             "independence rules matter. This is a conversation with a lawyer "
             "rather than with your IT provider."),
            ("unsure", "Not sure", "need-one-fact",
             "Read Article 37(1). It is three bullet points and it takes ten "
             "minutes. Getting this wrong in either direction is expensive."),
        ],
        ladder=None,
        costs={"assess whether you need one, write it down": "€",
               "name an internal owner who is not conflicted": "€",
               "external DPO on retainer": "€€€",
               "employ one": "€€€€€"},
        sec=0, chk=3,
        evidence=("Somebody deals with data protection.",
                  "A written assessment against Article 37 with the conclusion.",
                  "The assessment, the named owner, and where a DPO is "
                  "required, the notification to the supervisory authority."),
        frameworks=["gdpr-art30", "nist-csf-gv.rr-02"],
        patterns=["documentation-only"],
        already_have=[],
        answer_risk="certification",
    ),

    "ransom-payment": dict(
        priority=1,
        plain_english=(
            "Have you decided in advance whether you would pay a ransom, and "
            "who gets to make that call."),
        misunderstanding=(
            "People think this is a moral question to be settled on the day. "
            "It is a decision to be made on a quiet afternoon, because on the "
            "day you will be making it at 3am with the plant down, your lawyer "
            "unreachable and somebody quoting a countdown timer at you. The "
            "question is not really would you pay. It is: who is allowed to "
            "authorise it, what would you need to know first, and have you "
            "checked whether paying is even legal for you."),
        skeptic_case=(
            "There is nothing to buy and it costs an hour. The argument is "
            "only against the elaborate version, where this becomes a "
            "twelve-page playbook with decision trees. One page: who decides, "
            "who they must consult, what has to be true before payment is "
            "considered, and the sanctions check. The sanctions check is the "
            "part people miss and it is the part that turns a bad day into a "
            "criminal matter, because paying an entity under sanctions is an "
            "offence regardless of the circumstances."),
        applies_if=["any_business_data"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. Authority to consider or authorise any extortion "
            "payment is defined and reserved to named individuals, and is "
            "subject to legal and sanctions review. Our position is stated "
            "below."),
        default_verdict="write-it-down",
        question="If ransomware hit tonight, who would be allowed to say yes to paying?",
        options=[
            ("named", "A specific person, and they know it", "already-solved",
             "Then write it down with the constraints, including the sanctions "
             "check, and you have the whole control. Most companies cannot "
             "answer this at all."),
            ("board", "It would go to the owners", "write-it-down",
             "Fine, but say so in advance and work out how you would reach "
             "them at 3am on a Sunday. That contact detail is the control."),
            ("nobody", "No idea", "do-it-properly",
             "This is an hour of work that will not feel urgent until the "
             "worst possible moment. Decide the authority now, and check the "
             "sanctions position, because paying a sanctioned entity is an "
             "offence whatever the pressure."),
        ],
        ladder=(2,
                "Rung 4 is a full extortion playbook with negotiation support "
                "and a pre-agreed cryptocurrency route. That is a service, and "
                "buying it in advance mostly signals that you expect to pay. "
                "The decision authority, the legal check and a phone number "
                "are what change the outcome.",
                [(1, "Nobody has thought about it.", "do-it-properly"),
                 (2, "Authority named, sanctions position checked, written down.", "already-solved"),
                 (3, "Part of a rehearsed incident plan with legal on call.", "cheap-checkbox"),
                 (4, "Full playbook with negotiation and payment routes ready.", "cheap-checkbox")]),
        costs={"one page, decided in advance": "€",
               "legal and sanctions review of the position": "€€",
               "extortion response retainer": "€€€€"},
        sec=1, chk=3,
        evidence=("We would not pay. Probably.",
                  "A written position naming who may authorise and on what "
                  "basis.",
                  "The position, evidence of legal and sanctions review, and "
                  "the contact route to reach the decision maker out of hours."),
        frameworks=["nist-csf-rs.ma-03", "nist-csf-gv.po-01", "iso27002-5.24"],
        patterns=["documentation-only"],
        already_have=[],
        answer_risk="warranty",
    ),

    "clean-desk": dict(
        priority=2,
        plain_english=(
            "Do you have a rule about not leaving sensitive things lying "
            "around. Paper on desks, whiteboards left written on, screens "
            "facing the window."),
        misunderstanding=(
            "It gets dismissed as the most trivial line on the form, and it is "
            "nearly free, so it is a strange one to fail. What people miss is "
            "that most of the risk moved home. A clean desk policy written for "
            "an office says nothing about the printed customer list on somebody's "
            "kitchen table, or the video call taken in a co-working space with "
            "the screen visible to the room."),
        skeptic_case=(
            "Do not buy anything and do not audit desks. The whole control is "
            "two lines in the acceptable use policy and a lockable drawer where "
            "people need one. Where it genuinely matters is a shared or public "
            "space, so write it for that rather than for a room only your own "
            "staff can enter."),
        applies_if=["has_employees"],
        applies_never_if=["sole_trader"],
        how_to_say_no=(
            "Applicable. Requirements for handling information on desks, "
            "screens and printed material are set out in our acceptable use "
            "policy and extend to remote working."),
        default_verdict="write-it-down",
        question="Where does the printing happen?",
        options=[
            ("none", "We barely print anything", "write-it-down",
             "Then say that, add two lines to the acceptable use policy for "
             "the rare occasions, and stop. Nobody expects a paper handling "
             "regime from a company with no paper."),
            ("office", "In the office", "already-solved",
             "Two lines in the policy and a lockable drawer near the printer. "
             "This is one of the cheapest closed questions on the form."),
            ("home", "People print at home", "write-it-down",
             "That is where the actual exposure is, and almost no clean desk "
             "policy mentions it. Cover home printing and disposal explicitly "
             "and your answer is better than most large companies'."),
        ],
        ladder=None,
        costs={"two lines in the acceptable use policy": "€",
               "lockable storage and a shredder": "€€"},
        sec=1, chk=2,
        evidence=("People are tidy.",
                  "The written requirement, in the acceptable use policy or "
                  "its own page.",
                  "The policy, evidence staff accepted it, and secure disposal "
                  "arranged for paper."),
        frameworks=["iso27002-7.7", "nist-csf-pr.ds-01"],
        patterns=["documentation-only", "framework-inheritance"],
        already_have=["screen-lock"],
    ),

    "ai-governance": dict(
        priority=1,
        plain_english=(
            "Do you have rules about staff using AI tools, and do you know "
            "which ones are in use."),
        misunderstanding=(
            "Two different questions get asked as one. Which AI tools are in "
            "use is an inventory problem. Whether people may paste customer "
            "data into them is a policy problem, and it is the one that has "
            "already happened at your company whether or not anybody has "
            "written it down. The instinct to ban everything is the mistake: "
            "a ban you do not enforce moves the same behaviour onto personal "
            "accounts where you cannot see it at all."),
        skeptic_case=(
            "You do not need an AI governance framework, an AI risk committee "
            "or an ISO 42001 certificate. You need one page that says which "
            "tools are approved, what must never be pasted into any of them, "
            "and who to ask about a new one. Buy the business tier of whatever "
            "people are already using, because the consumer tier is usually "
            "where the training-on-your-data terms live and the business tier "
            "usually is not. That single purchase does more than the policy."),
        applies_if=["has_employees"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. Approved AI tools, and the categories of information "
            "that may not be submitted to them, are defined. Where the EU AI "
            "Act applies to our use, that assessment is stated separately."),
        default_verdict="write-it-down",
        question="Has anyone here pasted company data into an AI tool this month?",
        options=[
            ("yes", "Certainly", "write-it-down",
             "Then the choice is not whether it happens, only whether it "
             "happens somewhere you can see. One page of rules and a business "
             "tier subscription beats a ban nobody obeys."),
            ("no", "I do not think so", "write-it-down",
             "Write the rules while that is still true. This is the cheapest "
             "it will ever be, and it will not stay true."),
            ("banned", "We have banned it", "cheap-checkbox",
             "Check whether the ban is real or just stated. An unenforced ban "
             "pushes the same activity onto personal accounts, which is the "
             "worse outcome and the harder one to answer for."),
        ],
        ladder=(2,
                "Rung 4 is an AI governance programme with model inventories, "
                "impact assessments and a review board. That is built for "
                "organisations deploying models, not for one using tools. A "
                "written rule, an approved list and the business tier is where "
                "the risk actually drops.",
                [(1, "No rules, nobody knows what is in use.", "write-it-down"),
                 (2, "Approved tools listed, rules on what may be pasted.", "already-solved"),
                 (3, "Inventory maintained, terms reviewed, training given.", "cheap-checkbox"),
                 (4, "Full governance programme with impact assessments.", "cheap-checkbox")]),
        costs={"one page of rules": "€",
               "business tier instead of consumer tier": "€€",
               "AI governance programme": "€€€€"},
        sec=2, chk=3,
        evidence=("We have talked about it.",
                  "A written policy naming approved tools and prohibited data "
                  "categories.",
                  "The policy, the tool inventory, and evidence that the "
                  "approved tools are on terms that do not train on your data."),
        frameworks=["nist-csf-id.am-02", "nist-csf-gv.po-01"],
        patterns=["documentation-only"],
        already_have=["external-sharing-controls", "basic-dlp"],
    ),
}
