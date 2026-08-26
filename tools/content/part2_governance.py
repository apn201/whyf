"""Governance, risk and the policy questions."""

CARDS = {

    "business-context": dict(
        priority=1,
        plain_english=(
            "What is it that brings money in. If you make pencils, it is selling "
            "pencils. All security has to line up behind that."),
        misunderstanding=(
            "Many think the goal is maximum security. That is wrong. The goal is "
            "to sell pencils safely. So only do things that either help the "
            "business or stop a risk that would hurt the business, directly or "
            "indirectly. Everything else is somebody's hobby."),
        skeptic_case=(
            "There is no argument against this one. You have to know what your "
            "business is, and it takes an afternoon to write down. The argument is "
            "against the version consultants sell, where this becomes a workshop "
            "series and a stakeholder map. One page: what we sell, what stops us "
            "selling it, which systems that depends on."),
        applies_if=["any_business_data"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. Our critical services and the systems supporting them are "
            "identified and reviewed."),
        default_verdict="write-it-down",
        question="Could you name the three systems that stop the money if they die?",
        options=[
            ("yes", "Easily", "write-it-down",
             "Then you already did the thinking. Put it on one page so somebody "
             "else can read it, and this whole section of the questionnaire "
             "answers itself."),
            ("no", "I would have to think", "do-it-properly",
             "That is the gap, and it is not a paperwork gap. Every other decision "
             "here, what to back up, what to segment, what to spend on, depends on "
             "that answer."),
        ],
        ladder=(2,
                "Rung 4 wants this reviewed on a cycle with named stakeholders and "
                "documented dependencies. For a company under a few hundred people "
                "the answer changes maybe once a year, when you add a product or "
                "lose a customer. Update it then.",
                [(1, "Nobody wrote down what the business depends on.", "write-it-down"),
                 (2, "One page naming the critical services and systems.", "already-solved"),
                 (3, "Reviewed yearly, dependencies mapped.", "cheap-checkbox"),
                 (4, "Continuous review with stakeholder sign-off.", "cheap-checkbox")]),
        costs={"one page, written once": "€", "reviewed yearly": "€",
               "full dependency mapping": "€€€"},
        sec=2, chk=2,
        evidence=("Somebody can describe the business in a meeting.",
                  "A written list of critical services and the systems behind them.",
                  "The same list, dated, with an owner per service and evidence it "
                  "was reviewed."),
        frameworks=["nist-csf-gv.oc-01", "nist-csf-gv.oc-04", "nis2-art21"],
        patterns=["documentation-only"],
        already_have=[],
    ),

    "acceptable-use": dict(
        priority=2,
        plain_english=(
            "A policy telling people the do's and don'ts with company equipment "
            "and accounts."),
        misunderstanding=(
            "It does not need to be long. Sometimes shorter is better, because a "
            "page people read beats twelve pages they sign without reading. The "
            "whole thing fits in four lines: do not use company kit to commit "
            "crimes or harm the company, do not install illegal software, do not "
            "tamper with security controls, limited private use is fine on breaks."),
        skeptic_case=(
            "If you are a one-person company, there is nobody to hand the policy "
            "to and you should say so. Beyond that there is no real argument "
            "against it, because it costs an afternoon and it is the document that "
            "lets you act when somebody does something stupid. Without it, "
            "dismissing someone for what they did with a company laptop gets "
            "complicated."),
        applies_if=["has_employees"],
        applies_never_if=["sole_trader"],
        how_to_say_no=(
            "Not applicable. The company has no employees other than the owner, so "
            "there is no user population for an acceptable use policy to govern."),
        default_verdict="cheap-checkbox",
        question="How many people use company equipment?",
        options=[
            ("one", "Just me", "not-applicable",
             "Say so. A policy is an instruction from the company to its people. "
             "With one person there is nobody to instruct."),
            ("few", "A handful", "write-it-down",
             "One page, signed at onboarding. An afternoon of work and the "
             "question is closed for good."),
            ("many", "Enough that I do not know them all", "write-it-down",
             "Same one page, but attach it to onboarding properly so you can show "
             "who accepted it and when. Still not a project."),
        ],
        ladder=None,
        costs={"one page, signed at onboarding": "€",
               "policy set with yearly re-acceptance": "€€"},
        sec=1, chk=2,
        evidence=("Somebody says everyone knows the rules.",
                  "A written acceptable use policy.",
                  "The policy plus a record of who accepted it and when."),
        frameworks=["nist-csf-gv.po-01", "iso27002-5.10"],
        patterns=["documentation-only"],
        already_have=[],
    ),

    "personnel-security": dict(
        priority=2,
        plain_english=(
            "How do you know who to trust before you hand them a key, a laptop or "
            "an admin account. Background checks, references, contracts."),
        misunderstanding=(
            "People file this under physical security and stop at the front door. "
            "It goes wider than that. The cleaner with a master key, the contractor "
            "with a VPN account and the new hire in finance are the same problem: "
            "somebody is being trusted, and you should know on what basis. In much "
            "of Europe what you are allowed to check is limited by law, so the "
            "honest answer is often smaller than the question implies."),
        skeptic_case=(
            "Do not buy a screening service. For most roles a reference call and a "
            "signed contract is the whole control, and in several countries a "
            "criminal record check is simply not available to a private employer. "
            "Spend the effort on the handful of roles that can actually cause "
            "damage: admins, finance, anyone with unescorted site access."),
        applies_if=["has_employees"],
        applies_never_if=["sole_trader"],
        how_to_say_no=(
            "Partially applicable. Pre-employment screening is limited by local "
            "employment law in our operating countries. Our practice, and what it "
            "covers, is described below."),
        default_verdict="write-it-down",
        question="Do you check anything before someone gets admin rights or a site key?",
        options=[
            ("nothing", "Not really", "write-it-down",
             "Decide what you check and for which roles, then write the two lines "
             "down. The checking is usually already happening informally, it is "
             "just not recorded."),
            ("some", "References and a contract", "already-solved",
             "That is the control for most roles. Say so and name the roles where "
             "you do more."),
            ("formal", "Formal screening for sensitive roles", "already-solved",
             "Answer it and attach the role list. Nothing more to buy."),
        ],
        ladder=(2,
                "Rung 4 wants screening repeated periodically for everyone. That "
                "is a running cost per head, it annoys long-serving staff, and in "
                "several European countries you cannot do it anyway. Screen at "
                "hire, screen again on promotion into a sensitive role, stop.",
                [(1, "Nobody checks anything.", "write-it-down"),
                 (2, "References and contracts, more for sensitive roles.", "already-solved"),
                 (3, "Documented screening standard per role.", "cheap-checkbox"),
                 (4, "Repeated screening on a cycle.", "cheap-checkbox")]),
        costs={"references and a contract": "€",
               "formal screening for sensitive roles": "€€",
               "repeat screening for everyone": "€€€"},
        sec=1, chk=2,
        evidence=("We know the people we hire.",
                  "A written statement of what is checked, for which roles.",
                  "The same, plus records per hire showing it happened."),
        frameworks=["nist-csf-gv.rr-04", "iso27002-6.1", "nis2-art21"],
        patterns=["documentation-only"],
        already_have=[],
    ),

    "nis2-scope": dict(
        priority=1,
        plain_english=(
            "Does your company fall under NIS2. This is a scope question, not a "
            "control question, and getting it wrong in either direction costs you."),
        misunderstanding=(
            "NIS1 was telecoms and a short list of obvious infrastructure. NIS2 "
            "pulls in a lot of normal companies, including ones that are only in "
            "scope because they are part of a food production chain, or waste, or "
            "manufacturing of certain products. Nobody will write to you and tell "
            "you. There is no letter. Your own people have to work it out from the "
            "annexes and the national transposition, and the national laws are not "
            "identical."),
        skeptic_case=(
            "There is no argument for skipping this, but there is a strong "
            "argument against doing anything else until it is answered. If you are "
            "not in scope, half the questions in a NIS2-flavoured questionnaire "
            "are not obligations on you, and you can say so. If you are in scope, "
            "registration and incident reporting deadlines are legal duties with "
            "personal liability attached to management, and no amount of tooling "
            "substitutes for having registered."),
        applies_if=["operates_in_eu"],
        applies_never_if=["no_eu_operations"],
        how_to_say_no=(
            "Not applicable. We have assessed our sector and size against Annexes I "
            "and II of Directive (EU) 2022/2555 and the national transposition in "
            "our operating countries, and we do not fall within scope."),
        default_verdict="need-one-fact",
        question="Has anyone actually checked whether NIS2 covers you?",
        options=[
            ("checked_out", "Checked, we are out of scope", "not-applicable",
             "Good. Say so in one line and cite the annex you checked against. "
             "That closes a lot of questions in one go."),
            ("checked_in", "Checked, we are in scope", "do-it-properly",
             "Then registration and the reporting deadlines are legal duties, not "
             "good practice. This stops being a security project and becomes a "
             "compliance one with your management personally on the hook."),
            ("not_checked", "Nobody has looked", "need-one-fact",
             "That is the job, and it is a legal question rather than a technical "
             "one. A day of somebody's time now, or a nasty surprise later."),
        ],
        ladder=None,
        costs={"read the annexes yourself": "€",
               "legal opinion on scope": "€€",
               "registration and reporting readiness if in scope": "€€€€"},
        sec=0, chk=3,
        evidence=("Somebody has an opinion about whether NIS2 applies.",
                  "A written scope assessment naming the annex and the sector.",
                  "The assessment, dated, reviewed by legal, plus registration "
                  "confirmation if in scope."),
        frameworks=["nis2-art3", "nis2-art21", "nis2-art23"],
        patterns=["framework-inheritance"],
        already_have=[],
        answer_risk="certification",
    ),

    "board-oversight": dict(
        priority=1,
        plain_english=(
            "Do the owners or the board know that security is theirs, and do they "
            "back it. Not whether they attend a meeting. Whether they own it."),
        misunderstanding=(
            "Many think cyber security is an IT problem. It is a business problem. "
            "A fire can stop a factory and so can ransomware, and nobody calls a "
            "fire an IT problem. Under NIS2 in the EU this gets sharper: top "
            "management are personally responsible, and being told about it "
            "afterwards is not a defence."),
        skeptic_case=(
            "If there is no board, this does not apply and you say so. Where there "
            "is one, the questionnaire wants quarterly reporting with metrics and "
            "risk indicators, and for a company of thirty people that is theatre. "
            "Twice a year, twenty minutes, three slides: what changed, what "
            "happened, what we want money for. Minute it. That is the control."),
        applies_if=["has_board"],
        applies_never_if=["no_board"],
        how_to_say_no=(
            "Partially applicable. The company has no separate board. Security is "
            "reported to and owned by the managing director, and this is recorded."),
        default_verdict="write-it-down",
        question="When did the owners last hear about security?",
        options=[
            ("never", "They have not", "do-it-properly",
             "Not because of the questionnaire. If they have never heard about it, "
             "you will not get money when you need it, and under NIS2 they are "
             "carrying a liability they do not know about."),
            ("adhoc", "When something went wrong", "write-it-down",
             "Put it on the agenda twice a year instead. Same effort, and it stops "
             "being a conversation that only happens on bad days."),
            ("regular", "It is a standing agenda item", "already-solved",
             "Then answer with the frequency and point at the minutes. Done."),
        ],
        ladder=(2,
                "Rung 4 wants quarterly board reporting with key risk indicators "
                "and financial thresholds. Building that reporting pack is a "
                "consulting engagement, and in a company where the owner is in the "
                "building every day it tells them nothing they did not know. Twice "
                "yearly and minuted is a real answer.",
                [(1, "Security never reaches the owners.", "do-it-properly"),
                 (2, "Discussed twice a year and minuted.", "already-solved"),
                 (3, "Standing item with metrics and a roadmap.", "cheap-checkbox"),
                 (4, "Quarterly, with risk indicators and thresholds.", "cheap-checkbox")]),
        costs={"put it on the agenda": "€", "a proper reporting pack": "€€€"},
        sec=2, chk=3,
        evidence=("The owner says they care about security.",
                  "Minutes showing security was discussed, with a date.",
                  "Minutes across several meetings, plus a named executive owner "
                  "and evidence a decision followed."),
        frameworks=["nist-csf-gv.ov-01", "nist-csf-gv.rr-01", "nis2-art20"],
        patterns=["documentation-only"],
        already_have=[],
    ),

    "executive-protection": dict(
        priority=3,
        plain_english=(
            "Do directors and senior people get extra protection on their personal "
            "accounts and devices."),
        misunderstanding=(
            "These days everyone needs roughly the same protection. A blue-collar "
            "worker's PC is as good an entry point as the CEO's, and attackers "
            "know that the person with the weakest setup is often not the person "
            "with the biggest title. Where executives are genuinely different is "
            "fraud: they get impersonated, and their approval is what moves money."),
        skeptic_case=(
            "The questionnaire lists personal vulnerability assessments, identity "
            "theft monitoring and a personal incident response provider. That is a "
            "product bundle aimed at people who can afford it, and it is close to "
            "irrelevant for a company of thirty. Put the effort into payment "
            "approval rules instead, which is where executive impersonation "
            "actually costs money."),
        applies_if=["has_employees"],
        applies_never_if=["sole_trader"],
        how_to_say_no=(
            "Not applicable as a separate programme. Protection is applied "
            "uniformly across all users rather than by seniority. Payment approval "
            "controls covering executive impersonation are described separately."),
        default_verdict="not-applicable",
        question="Can one email from the boss move money?",
        options=[
            ("yes", "Probably, yes", "do-it-properly",
             "Then the fix is not personal cyber insurance for the boss. It is a "
             "rule that no payment moves on an email alone, whoever sent it. Cheap, "
             "and it stops the actual attack."),
            ("no", "No, payments need two people", "already-solved",
             "Then say that. The control the question is groping towards is "
             "already in place, and you can skip the executive protection bundle."),
        ],
        ladder=(1,
                "Every rung above the first is a purchase aimed at wealthy "
                "individuals rather than at the company's risk. Unless you have a "
                "specific, named threat against a specific person, the money is "
                "better spent on the payment controls.",
                [(1, "Same protection for everyone, payment rules in place.", "already-solved"),
                 (2, "Extra monitoring on a few senior accounts.", "cheap-checkbox"),
                 (3, "Personal device and account protection provided.", "cheap-checkbox"),
                 (4, "Full personal protection programme with a retainer.", "cheap-checkbox")]),
        costs={"payment approval rules": "€",
               "extra monitoring on senior accounts": "€€",
               "personal protection bundle per executive": "€€€€"},
        sec=1, chk=1,
        evidence=("Nobody has thought about it.",
                  "A written statement that protection is applied uniformly, plus "
                  "the payment approval rule.",
                  "The same, plus evidence the payment rule has been tested."),
        frameworks=["nist-csf-pr.aa-01"],
        patterns=["technology-prescription"],
        already_have=["admin-mfa"],
    ),

    "security-policy": dict(
        priority=1,
        plain_english=(
            "Do you have a written policy saying how you handle security. The "
            "document itself, not the controls in it."),
        misunderstanding=(
            "People think this means a policy set: twenty documents, a numbering "
            "scheme, a review board. It means one document that says what you "
            "protect, who decides, and what everyone is expected to do. If you "
            "cannot describe your security in ten pages, the problem is not the "
            "document."),
        skeptic_case=(
            "This is the cheapest tick on the whole form and it stays cheap as "
            "long as you write it yourself. The moment you buy a policy pack you "
            "get sixty pages describing controls you do not have, which is worse "
            "than nothing: now you have written evidence of a gap. Write what is "
            "true today, date it, review it when something changes."),
        applies_if=["has_employees"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. Our information security policy is maintained and "
            "available to staff. Scope and review date are stated below."),
        default_verdict="write-it-down",
        question="Is there a document, and does it describe what you actually do?",
        options=[
            ("none", "No document", "write-it-down",
             "An afternoon. Ten pages maximum, describing what is true. This one "
             "question sits underneath a dozen others on most forms."),
            ("bought", "We bought a template pack", "do-it-properly",
             "Read it. If it describes controls you do not have, it is a liability "
             "rather than an answer. Cut it down to what is true before anyone "
             "audits against it."),
            ("real", "Yes, and it matches reality", "already-solved",
             "Answer with the date of the last review and move on."),
        ],
        ladder=(2,
                "Rung 4 wants the policy set reviewed, communicated and "
                "enforced on a cycle with evidence at each step. For a small "
                "company that is a documentation industry. One policy, reviewed "
                "when something changes, with a date on it, answers the question.",
                [(1, "No policy, or one nobody has read.", "write-it-down"),
                 (2, "One policy, current, staff have seen it.", "already-solved"),
                 (3, "Policy set, reviewed yearly, acceptance recorded.", "cheap-checkbox"),
                 (4, "Reviewed, communicated and enforced with evidence throughout.", "cheap-checkbox")]),
        costs={"write it yourself": "€", "a template pack, cut down": "€€",
               "consultant-written policy set": "€€€"},
        sec=1, chk=3,
        evidence=("Somebody says there is a policy.",
                  "The policy, with a date and an owner.",
                  "The policy, its review history, and a record that staff have "
                  "seen it."),
        frameworks=["nist-csf-gv.po-01", "nist-csf-gv.po-02", "iso27002-5.1", "nis2-art21"],
        patterns=["documentation-only"],
        already_have=[],
    ),

    "security-roles": dict(
        priority=1,
        plain_english=(
            "Who does what in security. Named people, not a box on an org chart."),
        misunderstanding=(
            "This does not require a CISO. In a company of forty the honest answer "
            "is often one name for everything, and that is a perfectly good "
            "answer as long as the name is written down and the person knows. "
            "What fails an audit is not having one person doing it all. It is "
            "nobody being able to say who that person is."),
        skeptic_case=(
            "Do not create a security committee. Do not invent a RACI matrix. "
            "Write down who decides, who runs it day to day, and who to call at "
            "night. Three lines. If those three lines are the same name, write "
            "the name three times."),
        applies_if=["has_employees"],
        applies_never_if=["sole_trader"],
        how_to_say_no=(
            "Applicable. Security responsibilities are assigned by name and "
            "recorded. Given our size, several responsibilities sit with the same "
            "person, which is stated explicitly rather than obscured."),
        default_verdict="write-it-down",
        question="If I asked three people here who owns security, would I get one answer?",
        options=[
            ("yes", "Yes, same name", "already-solved",
             "Then write it down where a stranger can find it and the question is "
             "answered. You are further ahead than most."),
            ("no", "Probably not", "write-it-down",
             "Fix it with a document, not a hire. Ambiguity about who decides is "
             "what turns a small incident into a long one."),
        ],
        ladder=(2,
                "Rung 4 wants roles, responsibilities and authorities defined "
                "across the whole organisation with resourcing tied to the risk "
                "strategy. In a small company that is a page of fiction. Name the "
                "people, state that some wear several hats, move on.",
                [(1, "Nobody is named.", "write-it-down"),
                 (2, "Names written down, people know.", "already-solved"),
                 (3, "Roles documented with deputies and escalation.", "cheap-checkbox"),
                 (4, "Full role framework with resourcing tied to risk.", "cheap-checkbox")]),
        costs={"write down the names": "€", "documented roles and deputies": "€€",
               "hire someone for the role": "€€€€€"},
        sec=2, chk=3,
        evidence=("Everyone knows who to ask.",
                  "A document naming who owns security and who deputises.",
                  "The same, plus it appearing in job descriptions and an "
                  "escalation contact list."),
        frameworks=["nist-csf-gv.rr-02", "nist-csf-gv.rr-03", "nis2-art20", "iso27002-5.2"],
        patterns=["documentation-only"],
        already_have=[],
    ),

    "risk-appetite": dict(
        priority=1,
        plain_english=(
            "Has management said how much risk they are willing to carry. The "
            "number, or at least the sentence, that everything else gets measured "
            "against."),
        misunderstanding=(
            "This is the basis for everything else in security and almost nobody "
            "has it. Without a target risk level you cannot say whether a gap "
            "matters, so every finding looks equally urgent and nothing gets "
            "prioritised. If management is not interested in security, get this one "
            "thing from them and you can do the rest yourself."),
        skeptic_case=(
            "The questionnaire wants financial quantification and return on "
            "security investment modelling. Skip that. One sentence from the owner, "
            "something like a day of downtime is survivable and a week is not, is "
            "enough to sort a risk register. The modelling only pays for itself in "
            "companies large enough to have someone whose job is modelling."),
        applies_if=["any_business_data"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. Management has stated the level of disruption and loss "
            "the business will tolerate, and controls are prioritised against it."),
        default_verdict="write-it-down",
        question="Could the owner tell you how long an outage they can survive?",
        options=[
            ("yes", "Yes, roughly", "write-it-down",
             "Then get it in writing, one sentence, signed off. That sentence is "
             "what lets you say no to the next expensive suggestion."),
            ("no", "No idea", "need-one-fact",
             "Ask them. It takes one conversation, and without it you cannot rank "
             "anything, including whether this questionnaire matters."),
        ],
        ladder=(2,
                "Rung 4 is consistent evaluation using financial metrics aligned "
                "to tolerance thresholds. That is a quantitative risk function, "
                "which is a person and a tool. A stated tolerance and a ranked list "
                "gets you the same decisions in a company under a few hundred "
                "people.",
                [(1, "Nobody has said what is tolerable.", "write-it-down"),
                 (2, "Management has stated it and it is written down.", "already-solved"),
                 (3, "Applied consistently to prioritise controls.", "cheap-checkbox"),
                 (4, "Financially quantified against tolerance thresholds.", "cheap-checkbox")]),
        costs={"one conversation, written down": "€",
               "a ranked risk register against it": "€€",
               "quantified risk modelling": "€€€€"},
        sec=2, chk=2,
        evidence=("Management cares about risk.",
                  "A written statement of tolerable loss or downtime, signed off.",
                  "The statement, plus a risk register showing decisions made "
                  "against it."),
        frameworks=["nist-csf-gv.rm-01", "nist-csf-gv.rm-02", "iso27002-5.19", "nis2-art21"],
        patterns=["documentation-only"],
        already_have=[],
    ),

    "risk-assessment": dict(
        priority=1,
        plain_english=(
            "Have you actually sat down and worked out what could go wrong, and "
            "written it down."),
        misunderstanding=(
            "Frameworks bury this and consultants arrive with complicated risk "
            "matrices. In simple form it is a spreadsheet. List the risks, add a "
            "probability and a cost. Now you know what you should be willing to pay "
            "for the control, and the rule is easy: a control cannot cost more than "
            "the risk it removes. Add a note to review it once a year and you have "
            "the tick as well. Without a consultant."),
        skeptic_case=(
            "The expensive version of this produces a document nobody reads and a "
            "heat map nobody acts on. Twenty rows in a spreadsheet, written by the "
            "people who actually run the place, beats a hundred rows written by "
            "somebody who arrived on Tuesday. The value is entirely in the "
            "conversation that produces it."),
        applies_if=["any_business_data"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. An information security risk assessment is maintained and "
            "reviewed. Scope and review date are stated below."),
        default_verdict="write-it-down",
        question="Is there a list of what could go wrong, with numbers next to it?",
        options=[
            ("none", "No list", "write-it-down",
             "A morning with a spreadsheet and the two or three people who know how "
             "the place works. Twenty rows. This is the cheapest real security work "
             "there is."),
            ("list", "Yes, and it gets looked at", "already-solved",
             "Answer with the review date. This is one of the few places where "
             "having done the boring thing pays back immediately."),
            ("consultant", "A consultant did one once", "cheap-checkbox",
             "Check whether it still describes your business. If it does, use it "
             "and put a review date on it. If it does not, twenty rows of your own "
             "beats forty of theirs."),
        ],
        ladder=(2,
                "Rung 4 wants a standardised method for calculating and "
                "prioritising risk, applied consistently and fed into enterprise "
                "risk management. That is a function, not a document. A "
                "spreadsheet reviewed yearly by people who know the business gets "
                "the same decisions made.",
                [(1, "No assessment.", "write-it-down"),
                 (2, "A spreadsheet with risks, likelihood and cost.", "already-solved"),
                 (3, "Reviewed on a schedule and driving a treatment plan.", "cheap-checkbox"),
                 (4, "Standardised method feeding enterprise risk management.", "cheap-checkbox")]),
        costs={"a spreadsheet, done in-house": "€",
               "reviewed yearly with a treatment plan": "€€",
               "consultant-run assessment": "€€€"},
        sec=2, chk=3,
        evidence=("We know what our risks are.",
                  "A risk register with likelihood, impact and an owner per row.",
                  "The register, dated, with a treatment plan and evidence of the "
                  "last review."),
        frameworks=["nist-csf-id.ra-01", "nist-csf-id.ra-05", "iso27002-5.6", "nis2-art21"],
        patterns=["documentation-only"],
        already_have=[],
    ),

    "improvement": dict(
        priority=2,
        plain_english=(
            "When something goes wrong, do you write down what you learned so it "
            "does not happen again."),
        misunderstanding=(
            "People hear lessons learned and picture a formal post-incident review "
            "with a facilitator. It is a paragraph. What broke, why, what we "
            "changed. The failure is not the format, it is that the paragraph never "
            "gets written and the same thing happens again in eight months."),
        skeptic_case=(
            "There is nothing to buy here and no reason to skip it. The only "
            "argument is against the industrial version, where every minor incident "
            "generates a report and a corrective action with a due date, and people "
            "start not reporting things to avoid the paperwork. Keep it to real "
            "incidents and keep it short."),
        applies_if=["any_business_data"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. Incidents and exercises are followed by a recorded review, "
            "and resulting changes are tracked."),
        default_verdict="write-it-down",
        question="Could you say what changed after the last thing that went wrong?",
        options=[
            ("yes", "Yes, we changed something", "already-solved",
             "Then write those down as they happen and you have the evidence "
             "without doing extra work."),
            ("no", "Nothing changed", "write-it-down",
             "That is the gap, and it is free to close. One paragraph per incident. "
             "If nothing needed changing, write that down too, with why."),
        ],
        ladder=(2,
                "Rung 4 wants improvement fed from incidents, exercises, audits and "
                "monitoring into a managed programme. That is a quality function. "
                "A paragraph per incident, kept in one place, is the version that "
                "survives contact with a busy week.",
                [(1, "Nothing is recorded after an incident.", "write-it-down"),
                 (2, "A short written review after real incidents.", "already-solved"),
                 (3, "Reviews after incidents and exercises, actions tracked.", "cheap-checkbox"),
                 (4, "Improvement programme fed from every source.", "cheap-checkbox")]),
        costs={"a paragraph per incident": "€", "tracked actions with owners": "€€"},
        sec=2, chk=2,
        evidence=("We talk about what went wrong.",
                  "Written reviews for past incidents.",
                  "Reviews plus a tracked list of changes made, with dates."),
        frameworks=["nist-csf-id.im-01", "nist-csf-id.im-03", "iso27002-8.29", "nis2-art21"],
        patterns=["documentation-only"],
        already_have=[],
    ),

    "legal-compliance": dict(
        priority=2,
        plain_english=(
            "Do you have a way of knowing which laws and regulations apply to you "
            "in every country you operate in, and staying inside them."),
        misunderstanding=(
            "This goes well beyond finance and chemicals. Employment law shapes "
            "what you may monitor and what you may screen. Export control rules can "
            "limit which encryption you are allowed to ship or even carry across a "
            "border. Data protection law decides what you may keep and for how "
            "long. It is not optional and it is not IT's call."),
        skeptic_case=(
            "You cannot skip it, but you can scope it. The question is not whether "
            "you have read every statute. It is whether somebody is responsible for "
            "noticing when a rule that affects you changes. In a small company that "
            "is a named person, an industry newsletter and a yearly check with a "
            "lawyer, not a compliance department."),
        applies_if=["any_business_data"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. Legal and regulatory requirements relevant to our "
            "operations are identified, assigned to an owner and reviewed."),
        default_verdict="write-it-down",
        question="Is there a named person who would notice if the rules changed?",
        options=[
            ("yes", "Yes", "already-solved",
             "Write down who, and what sources they watch. That is the whole "
             "control and you already have it."),
            ("no", "Not really", "write-it-down",
             "Name someone. It does not have to be a lawyer. It has to be somebody "
             "whose job includes noticing."),
        ],
        ladder=(2,
                "Rung 4 wants a tracked register of every legal and contractual "
                "requirement, aligned with the security strategy and reviewed on a "
                "cycle. In a company that operates in two countries, a one-page "
                "list and a named owner does the same job.",
                [(1, "Nobody is tracking legal requirements.", "write-it-down"),
                 (2, "A named owner and a short list of what applies.", "already-solved"),
                 (3, "A maintained register, reviewed yearly.", "cheap-checkbox"),
                 (4, "Full register aligned to strategy and contracts.", "cheap-checkbox")]),
        costs={"name an owner, list what applies": "€",
               "yearly review with a lawyer": "€€",
               "maintained compliance register": "€€€"},
        sec=1, chk=3,
        evidence=("We follow the law.",
                  "A list of applicable legal and regulatory requirements with an "
                  "owner.",
                  "The list, dated, with evidence of review and of legal input."),
        frameworks=["nist-csf-gv.oc-03", "iso27002-5.31", "iso27002-5.34", "nis2-art21"],
        patterns=["documentation-only"],
        already_have=[],
    ),

    "threat-intelligence": dict(
        priority=2,
        plain_english=(
            "Do you collect information about who might attack you and how."),
        misunderstanding=(
            "Usually nonsense, and a lot of people are proud of the time they waste "
            "on it. You need to be prepared for anything anyway. Think about how to "
            "protect the business. Do not spend your week caring which group is "
            "threatening it. The one useful slice is vulnerability advisories for "
            "the specific products you run, and that is a mailing list, not an "
            "intelligence programme."),
        skeptic_case=(
            "For almost every company being asked this question, a paid threat "
            "intelligence feed is money set on fire. The reports are written for "
            "organisations with a team to act on them. Subscribe to the vendor "
            "advisories for what you actually run, and to your national CERT. Both "
            "free. That is a complete and honest answer."),
        applies_if=["any_business_data"],
        applies_never_if=[],
        how_to_say_no=(
            "Partially applicable. We do not operate a threat intelligence "
            "function. We subscribe to vendor security advisories for the products "
            "in use and to national CERT bulletins, and act on them through "
            "vulnerability management."),
        default_verdict="cheap-checkbox",
        question="Do you get told when the software you run has a serious hole?",
        options=[
            ("yes", "Yes, we are on the vendor lists", "already-solved",
             "That is the useful part of threat intelligence and you have it. Say "
             "so, name the sources, and do not buy a feed."),
            ("no", "Not systematically", "write-it-down",
             "Sign up to the advisories for your main products and your national "
             "CERT. Free, an hour of work, and it feeds patching, which is where "
             "the actual risk is."),
        ],
        ladder=(2,
                "Rung 4 wants intelligence correlated against your environment and "
                "audited for effectiveness. That is a team. Vendor advisories plus "
                "a CERT feed, acted on through patching, is the honest answer for "
                "almost everyone and it is free.",
                [(1, "No sources at all.", "write-it-down"),
                 (2, "Vendor advisories and a CERT feed, acted on.", "already-solved"),
                 (3, "Sources correlated against your own asset list.", "cheap-checkbox"),
                 (4, "Full intelligence function with effectiveness review.", "cheap-checkbox")]),
        costs={"vendor advisories and CERT feeds": "€",
               "correlated against your asset inventory": "€€",
               "commercial intelligence feed": "€€€€"},
        sec=1, chk=2,
        evidence=("We keep an eye on the news.",
                  "A list of the advisory sources subscribed to.",
                  "The sources, plus examples of advisories that triggered a patch "
                  "or a change."),
        frameworks=["nist-csf-id.ra-02", "nist-csf-id.ra-03", "nis2-art21"],
        patterns=["technology-prescription"],
        already_have=[],
    ),
}
