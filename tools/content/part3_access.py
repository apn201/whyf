"""Identity, access and the devices people carry."""

CARDS = {

    "mfa": dict(
        priority=1,
        plain_english=(
            "Is there a second step on top of the password, in the places that "
            "matter. A code, or a prompt on your phone."),
        misunderstanding=(
            "Passwords are weak. Phishing works, keyloggers exist, and no password "
            "policy will save you. MFA is also attackable, but it gives very good "
            "protection against phishing and that is the main goal. Many forget "
            "that. SSO and the rest are related but do not replace it. The other "
            "half people get wrong: MFA should not be asked when it is not needed, "
            "because it just annoys people. Write the policy so that a known device "
            "on your own network doing a low-risk task is not challenged, and "
            "somebody in another country trying your credentials is. Companies "
            "overdo it and then staff go looking for workarounds. And MFA is not "
            "the control against someone stealing your laptop. It is the control "
            "against someone using your credentials from the internet."),
        skeptic_case=(
            "There is not much of one, which is rare on this list. Admin MFA is "
            "included in what you already pay Microsoft or Google, it takes an "
            "afternoon, and it stops the single most common way small companies get "
            "taken. The only real argument is against the expensive version: "
            "hardware tokens for everybody, or a separate MFA product when your "
            "identity provider already does it."),
        applies_if=["has_employees"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. Multi-factor authentication is enforced for administrative "
            "and remote access. Where it is not enforced, the risk basis for that "
            "decision is stated below."),
        default_verdict="do-it-properly",
        question="Can an admin account be used with just a password?",
        options=[
            ("yes", "Yes", "do-it-properly",
             "Fix it this week. It is included in the licence you already have, it "
             "takes an afternoon, and it is the difference between a phished "
             "password being an annoyance and being a ransomware event."),
            ("admins_only", "Admins are covered, users are not", "cheap-checkbox",
             "That covers the worst of it, and it is a legitimate answer. Extend it "
             "to remote access next, and leave the office network alone unless "
             "somebody gives you a reason."),
            ("all", "Everyone, everywhere", "already-solved",
             "Check people are not being challenged so often that they have built "
             "workarounds. Over-applied MFA gets defeated by the people it protects."),
        ],
        ladder=(3,
                "Rung 4 is MFA everywhere plus continuous alignment to emerging "
                "threats, which in practice means phishing-resistant hardware keys "
                "for the whole company. Keys cost money per head and get lost. "
                "Admins and remote access covered, with app-based factors, is where "
                "the risk curve flattens.",
                [(1, "No MFA anywhere.", "do-it-properly"),
                 (2, "Some accounts, not all admins.", "do-it-properly"),
                 (3, "All admin and all remote access covered.", "already-solved"),
                 (4, "Everything, with phishing-resistant hardware factors.", "cheap-checkbox")]),
        costs={"turn on what your licence includes": "€",
               "conditional policies tuned by risk": "€€",
               "hardware keys for everyone": "€€€"},
        sec=3, chk=3,
        evidence=("The policy says MFA is required.",
                  "A screenshot of the conditional access or MFA policy showing "
                  "which accounts it covers.",
                  "The policy, a report of accounts covered versus total, and the "
                  "list of exceptions with reasons."),
        frameworks=["nist-csf-pr.aa-03", "iso27002-5.17", "iso27002-8.5", "nis2-art21"],
        patterns=["framework-inheritance"],
        already_have=["admin-mfa"],
    ),

    "sso": dict(
        priority=2,
        plain_english=(
            "Do people sign in to your business applications through one login "
            "rather than a separate password for each."),
        misunderstanding=(
            "It sounds backwards but SSO is good for security. The goal of security "
            "is to make the business frictionless: remove friction for real use, add "
            "it for malicious use. Done properly SSO does exactly that. People use "
            "the systems with their identity without logging in to each one "
            "separately, which means fewer passwords, fewer sticky notes, and one "
            "place to switch someone off when they leave."),
        skeptic_case=(
            "The trap is the per-application licence uplift. Plenty of SaaS vendors "
            "charge extra for the SSO connector, sometimes doubling the price, and "
            "for a five-person tool that is not worth it. Do SSO for the systems "
            "everybody uses and the ones holding customer data. Leave the long tail "
            "on their own logins with a password manager."),
        applies_if=["has_employees", "has_cloud"],
        applies_never_if=["sole_trader"],
        how_to_say_no=(
            "Partially applicable. Single sign-on covers our core business "
            "applications. Applications outside that scope are listed, with the "
            "reason, below."),
        default_verdict="cheap-checkbox",
        question="How many separate passwords does a new joiner get handed?",
        options=[
            ("one", "One", "already-solved",
             "You already have this. Say so, and name the applications that sit "
             "outside it, because there always are some."),
            ("several", "A handful", "cheap-checkbox",
             "Normal. Cover the ones everybody uses and the ones with customer data "
             "in them, and be honest about the rest. That is a real answer."),
            ("many", "I have lost count", "do-it-properly",
             "That is a leaver problem more than a login problem. When somebody "
             "goes, you will not close all of those accounts, and you will not know "
             "which you missed."),
        ],
        ladder=(3,
                "Rung 4 asks for SSO across everything including administrative "
                "access, kept aligned to emerging threats. The blocker is rarely "
                "technical, it is the licence uplift vendors charge for the "
                "connector. Cover the core and the customer data, and document the "
                "exceptions instead of paying for them.",
                [(1, "Separate login for everything.", "do-it-properly"),
                 (2, "SSO on a few systems.", "cheap-checkbox"),
                 (3, "SSO across core business and admin systems.", "already-solved"),
                 (4, "Everything, including the long tail.", "cheap-checkbox")]),
        costs={"SSO on what already supports it": "€",
               "connectors for the main applications": "€€",
               "SSO licence uplift across every tool": "€€€€"},
        sec=2, chk=2,
        evidence=("People mostly use one login.",
                  "A list of applications behind SSO.",
                  "The list, plus the exceptions with a reason, and evidence that "
                  "disabling the identity closes access."),
        frameworks=["nist-csf-pr.aa-04", "iso27002-5.16"],
        patterns=[],
        already_have=[],
    ),

    "password-policy": dict(
        priority=2,
        plain_english=(
            "Do you have a rule stopping people choosing stupid passwords."),
        misunderstanding=(
            "In Windows you usually have this already, but best practice has moved "
            "and standard Windows does not always support where it moved to. The "
            "eight-character complex password is not recommended any more. It makes "
            "life difficult for your users while attackers phish instead and never "
            "touch the password rules. Passphrases are getting common. When a "
            "password is long enough, sixteen characters and up, you do not need to "
            "expire it and you do not need complexity rules. It is just maths."),
        skeptic_case=(
            "Forced ninety-day rotation is the clearest example on this whole form "
            "of a control that makes things worse. People respond with Summer2025! "
            "then Autumn2025!, and you have spent goodwill to get a predictable "
            "password. If a questionnaire insists on an expiry interval, answer "
            "what you actually do and say why. Nobody has ever lost a deal over it."),
        applies_if=["has_employees"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. Password rules are enforced centrally. We use a minimum "
            "length with breached-password screening rather than short passwords "
            "with forced rotation, and the basis for that is stated below."),
        default_verdict="already-solved",
        question="Do you still force everyone to change passwords every 90 days?",
        options=[
            ("yes", "Yes", "write-it-down",
             "Turn it off and raise the minimum length instead. It is a settings "
             "change, it costs nothing, and your users will like you more. Write "
             "down why, because somebody will ask."),
            ("no", "No, we use long passwords", "already-solved",
             "That is current best practice. Say so, cite the length, and be ready "
             "to explain it to an auditor working from a 2010 checklist."),
        ],
        ladder=(3,
                "Rung 4 asks for the same configuration standard across every "
                "system including databases and network kit. Getting the last "
                "legacy appliance in line is usually a rebuild, and those systems "
                "are better handled by not exposing them at all.",
                [(1, "No rules, anything goes.", "do-it-properly"),
                 (2, "Rules on the main directory only.", "cheap-checkbox"),
                 (3, "Consistent rules across the systems people log in to.", "already-solved"),
                 (4, "Every system including legacy and network kit.", "cheap-checkbox")]),
        costs={"change the settings you already have": "€",
               "breached-password screening add-on": "€€",
               "bringing legacy systems into line": "€€€"},
        sec=1, chk=2,
        evidence=("There is a password policy somewhere.",
                  "A screenshot of the enforced settings from the directory.",
                  "The settings, the systems they cover, and the list of systems "
                  "they do not."),
        frameworks=["nist-csf-pr.aa-01", "iso27002-5.17"],
        patterns=["documentation-only"],
        already_have=["password-hashing"],
    ),

    "default-passwords": dict(
        priority=2,
        plain_english=(
            "Do you have a process making sure no password is ever left as it came "
            "out of the box, and that the ones you hand to new users are not "
            "guessable either."),
        misunderstanding=(
            "Many think this only covers infrastructure, so they change the "
            "firewall password and then create every new user with Welcome2026. "
            "Both ends count. The router in the corner and the temporary password "
            "in the welcome email are the same weakness."),
        skeptic_case=(
            "There is nothing to buy and no reason to skip it. The only cost is "
            "remembering, which is why it belongs in the setup checklist for new "
            "kit and the onboarding script for new people rather than in a policy "
            "nobody reads."),
        applies_if=["has_network"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. Default credentials are changed at commissioning, and "
            "initial user credentials are unique and must be changed at first use."),
        default_verdict="write-it-down",
        question="If I opened your new-user script, what password would it set?",
        options=[
            ("pattern", "The same one every time", "do-it-properly",
             "Change it to a random one per user that must be changed at first "
             "login. It is a one-line change and it removes a genuinely easy way in."),
            ("random", "A random one, changed at first login", "already-solved",
             "Good. Now check the same discipline reaches the network kit and any "
             "machine on the factory floor."),
        ],
        ladder=None,
        costs={"fix the onboarding script": "€",
               "commissioning checklist for new kit": "€",
               "credential vault for shared devices": "€€"},
        sec=2, chk=2,
        evidence=("We change default passwords.",
                  "A commissioning checklist including credential change.",
                  "The checklist, plus a sample of devices showing it was done, "
                  "plus the onboarding script."),
        frameworks=["nist-csf-pr.aa-01", "nist-csf-pr.ps-01"],
        patterns=[],
        already_have=[],
    ),

    "passwords": dict(
        priority=2,
        plain_english=(
            "Is there a safe place for the system and infrastructure passwords. The "
            "ones that are not tied to a person."),
        misunderstanding=(
            "Nothing fancy here. If they are on paper in a fireproof safe, that "
            "might be good enough. Have a process, write it down, and you are "
            "probably fine. The failure is not the storage method. It is that the "
            "passwords live in one person's head or in a spreadsheet on their "
            "desktop, and that person is on holiday when the server dies."),
        skeptic_case=(
            "A password manager is cheap and worth it, but the honest small-company "
            "answer of a sealed envelope in a safe with a signed-out log is a real "
            "control and passes an audit. What does not pass is a spreadsheet "
            "called passwords.xlsx on a shared drive, and that is what most "
            "companies actually have."),
        applies_if=["has_servers", "has_network"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. Shared and system credentials are held in a controlled "
            "store with recorded access. The mechanism is described below."),
        default_verdict="write-it-down",
        question="Where is the admin password for your main server right now?",
        options=[
            ("head", "In somebody's head", "do-it-properly",
             "That is a continuity problem before it is a security one. Get it "
             "written down and stored properly, because the day you need it is the "
             "day that person is unreachable."),
            ("sheet", "In a spreadsheet somewhere", "do-it-properly",
             "Move it. A password manager costs a few euros a month, or a sealed "
             "envelope in the safe costs nothing. Either beats a file anyone with "
             "the share can open."),
            ("vault", "In a password manager or a safe", "already-solved",
             "Answer with which, and whether access is logged. That is the whole "
             "control."),
        ],
        ladder=None,
        costs={"sealed envelope in a safe": "€",
               "team password manager": "€€",
               "privileged access management platform": "€€€€"},
        sec=2, chk=2,
        evidence=("Somebody knows where the passwords are.",
                  "A named store, with who has access to it.",
                  "The store, the access list, and a record of check-out for "
                  "shared credentials."),
        frameworks=["nist-csf-pr.aa-01", "iso27002-5.17"],
        patterns=[],
        already_have=["password-hashing"],
    ),

    "identity-lifecycle": dict(
        priority=1,
        plain_english=(
            "Is there a clear process for adding people and, more importantly, "
            "removing them."),
        misunderstanding=(
            "Identity is not quite the same as user, but here it is close enough. "
            "You need a process to create them when needed and delete them when not "
            "needed, or when the person asks, which matters under GDPR. Joining is "
            "never the problem. Somebody chases it because the new person cannot "
            "work. Leaving is the problem, because nobody is chasing it and the "
            "account keeps working perfectly."),
        skeptic_case=(
            "Do not buy identity governance tooling for this. In a company under a "
            "few hundred people the control is a checklist that HR triggers on the "
            "leaving date, and the fix for most of the risk is SSO, so there is one "
            "account to disable instead of fifteen. Automation is worth it when the "
            "list of systems gets long enough that people forget, not before."),
        applies_if=["has_employees"],
        applies_never_if=["sole_trader"],
        how_to_say_no=(
            "Applicable. Accounts are created and removed through a defined "
            "process triggered by HR, and access is reviewed on role change."),
        default_verdict="do-it-properly",
        question="If someone left last month, is their account definitely gone?",
        options=[
            ("yes", "Yes, definitely", "already-solved",
             "Then write the process down so somebody else could run it, and point "
             "at the last leaver as evidence."),
            ("think", "I think so", "do-it-properly",
             "Go and check. Not as a paperwork exercise. Dormant accounts belonging "
             "to people who left angry are how a lot of small companies get hurt."),
            ("no", "Probably not", "do-it-properly",
             "This is worth real effort. A leaver checklist tied to the HR date, "
             "and SSO underneath so there is one switch rather than fifteen."),
        ],
        ladder=(3,
                "Rung 4 wants automated provisioning and de-provisioning across "
                "every system, kept aligned to emerging risk. The automation is a "
                "project and a licence. A checklist that HR actually triggers, with "
                "SSO underneath it, closes the same gap for a fraction of the "
                "money.",
                [(1, "Accounts are removed when somebody remembers.", "do-it-properly"),
                 (2, "A leaver checklist exists and is mostly followed.", "cheap-checkbox"),
                 (3, "HR triggers it, SSO makes it one switch, it is recorded.", "already-solved"),
                 (4, "Fully automated joiner, mover and leaver.", "cheap-checkbox")]),
        costs={"a leaver checklist": "€",
               "SSO so there is one account to disable": "€€",
               "automated provisioning tooling": "€€€€"},
        sec=3, chk=3,
        evidence=("We remove accounts when people leave.",
                  "A written joiner and leaver process with a named trigger.",
                  "The process, plus evidence for recent leavers showing dates and "
                  "who confirmed."),
        frameworks=["nist-csf-pr.aa-01", "nist-csf-pr.aa-05", "iso27002-5.16",
                    "iso27002-5.18", "nis2-art21"],
        patterns=[],
        already_have=["admin-role-separation"],
    ),

    "privileged-accounts": dict(
        priority=1,
        plain_english=(
            "Do you protect the accounts that can destroy things, and are they "
            "separate from the accounts those people use to read email."),
        misunderstanding=(
            "Privileged accounts are the ones that can change or destroy important "
            "things, or hand out access to them. Nobody should have those "
            "permissions on their daily account. Not because we do not trust the "
            "person, but because they can be hacked too, and when they are, the "
            "attacker gets whatever the account had. A separate admin account means "
            "the phishing email lands in a mailbox that cannot do any damage."),
        skeptic_case=(
            "The separate-account discipline is free and worth it. Everything above "
            "that gets expensive fast: session recording, just-in-time elevation, a "
            "full privileged access management platform. Those are built for "
            "organisations with dozens of administrators. If you have three, the "
            "control is separate accounts, MFA on them, and a yearly look at who "
            "still needs them."),
        applies_if=["has_servers", "has_employees"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. Administrative access is granted through dedicated "
            "accounts, separate from day-to-day accounts, and reviewed."),
        default_verdict="do-it-properly",
        question="Does your admin read email with the same account they use to run the servers?",
        options=[
            ("yes", "Yes", "do-it-properly",
             "Split it. It is an afternoon, it costs nothing, and it turns a "
             "successful phish from a company-ending event into a bad morning."),
            ("no", "No, separate accounts", "already-solved",
             "Then put MFA on the admin accounts if it is not there, and review the "
             "list once a year. That is the whole control."),
        ],
        ladder=(3,
                "Rung 4 wants privileged access restricted by risk of the elevation "
                "and actively monitored, which means a PAM platform and somebody "
                "watching it. That is priced for organisations with a team. "
                "Separate accounts, MFA, and an annual review is where the value "
                "is.",
                [(1, "Everyone works as admin.", "do-it-properly"),
                 (2, "Some separation, not consistent.", "do-it-properly"),
                 (3, "Dedicated admin accounts with MFA, reviewed yearly.", "already-solved"),
                 (4, "PAM with session recording and just-in-time elevation.", "cheap-checkbox")]),
        costs={"separate admin accounts": "€",
               "MFA and a yearly review": "€",
               "privileged access management platform": "€€€€"},
        sec=3, chk=3,
        evidence=("Admins know to be careful.",
                  "A list of privileged accounts and who holds them.",
                  "The list, evidence of separation from daily accounts, MFA "
                  "coverage, and a dated review."),
        frameworks=["nist-csf-pr.aa-05", "iso27002-8.2", "iso27002-8.18", "nis2-art21"],
        patterns=[],
        already_have=["admin-role-separation", "admin-mfa", "audit-logging"],
    ),

    "sod": dict(
        priority=2,
        plain_english=(
            "Can the same person who orders something also approve paying for it."),
        misunderstanding=(
            "This turns up in security questionnaires but it is mostly a finance "
            "control, and it is the one on this whole form that most reliably "
            "prevents actual money leaving. It is also the answer to executive "
            "impersonation fraud, which no amount of email filtering fully stops."),
        skeptic_case=(
            "In a company of five you cannot fully separate duties and pretending "
            "otherwise is dishonest. The workable version is a threshold: below a "
            "figure, one person; above it, two, one of whom is the owner. Write "
            "the figure down. That is a real answer and an auditor will take it."),
        applies_if=["has_employees"],
        applies_never_if=["sole_trader"],
        how_to_say_no=(
            "Partially applicable. Given our size, full segregation of duties is "
            "not achievable for all processes. Compensating controls, including "
            "approval thresholds and owner review, are described below."),
        default_verdict="write-it-down",
        question="Could one person here order something and pay for it alone?",
        options=[
            ("yes_any", "Yes, for any amount", "do-it-properly",
             "Set a threshold above which a second person signs. It costs nothing, "
             "it takes one conversation, and it is the control that stops the "
             "invoice fraud email."),
            ("threshold", "Only below a limit", "already-solved",
             "That is the honest small-company answer. Say what the limit is and "
             "who the second approver is."),
            ("never", "Never, always two people", "already-solved",
             "Answer it and move on. This one you have."),
        ],
        ladder=None,
        costs={"agree a threshold and write it down": "€",
               "enforce it in the finance system": "€€"},
        sec=3, chk=2,
        evidence=("We trust each other.",
                  "A written approval threshold naming who approves what.",
                  "The threshold enforced in the finance system, plus a sample of "
                  "approvals showing two names."),
        frameworks=["nist-csf-pr.aa-05", "iso27002-5.3"],
        patterns=[],
        already_have=[],
    ),

    "plc-access": dict(
        priority=2,
        plain_english=(
            "Do you control who can get at the systems that run production. The "
            "controllers, and the code loaded onto them."),
        misunderstanding=(
            "On the factory floor the engineering laptop is usually the real "
            "control point, not the PLC. Many controllers have no meaningful "
            "authentication at all and cannot be given any, so protecting them "
            "means protecting what can reach them: the laptop, the switch port and "
            "the door. Asking whether the PLC has a strong password often has no "
            "useful answer."),
        skeptic_case=(
            "Do not go looking for a way to put passwords on twenty-year-old "
            "controllers. It will not work and the vendor may void support. Control "
            "the engineering workstation, control the network path, control the "
            "door. Say that plainly instead of pretending the controller does "
            "something it cannot."),
        applies_if=["has_ot"],
        applies_never_if=["has_ot_none"],
        how_to_say_no=(
            "Not applicable. We do not operate programmable logic controllers or "
            "hold embedded source code. Access control for our IT systems is "
            "described separately."),
        default_verdict="not-applicable",
        question="Do you have controllers running machines?",
        options=[
            ("no", "No machines", "not-applicable",
             "Say so. This is an industrial question that arrived at the wrong "
             "company, which happens on most of these forms."),
            ("yes_old", "Yes, and they are old", "write-it-down",
             "Then say what actually protects them: the engineering laptop, the "
             "network segment, the locked door. That is a truthful answer and it is "
             "better than claiming a password the device cannot enforce."),
            ("yes_modern", "Yes, and they support accounts", "do-it-properly",
             "Then use them. Named accounts on the controllers, and the engineering "
             "laptop treated as a privileged device."),
        ],
        ladder=None,
        costs={"document what actually protects them": "€",
               "lock down the engineering workstation": "€€",
               "network segmentation for the cell": "€€€"},
        sec=3, chk=2,
        evidence=("Only our engineers touch the machines.",
                  "A description of what controls access: workstation, network "
                  "path, physical door.",
                  "The same, plus named accounts where the equipment supports them "
                  "and a record of who has them."),
        frameworks=["nist-csf-pr.aa-01", "iec62443-3-3:2013"],
        patterns=["technology-prescription"],
        already_have=[],
    ),

    "remote-access": dict(
        priority=1,
        plain_english=(
            "Do you have a process controlling how people reach your systems from "
            "outside, and can you switch it off."),
        misunderstanding=(
            "VPN is still widely used and often it is not needed. Why would "
            "somebody at home need the same access they have at work? Zero trust "
            "thinking is getting more popular and the useful part of it is simple: "
            "only give access to the things they actually need. The other half "
            "people miss is suppliers. The remote access that hurts is usually not "
            "an employee, it is a maintenance session somebody opened in 2019 and "
            "never closed."),
        skeptic_case=(
            "A full zero trust rebuild is a multi-year programme and vendors will "
            "happily sell you one. You do not need it to answer this. MFA on the "
            "VPN, a list of who has access, and a rule that supplier sessions are "
            "opened on request and closed afterwards covers most of the actual "
            "risk for a fraction of the price."),
        applies_if=["has_remote_workers", "has_servers"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. Remote access requires multi-factor authentication, is "
            "limited to named users, and can be revoked centrally. Third-party "
            "access is described separately."),
        default_verdict="do-it-properly",
        question="Could you list everyone who can reach your network from outside today?",
        options=[
            ("yes", "Yes, it is a short list", "already-solved",
             "Then answer with how the list is controlled and how quickly you can "
             "remove somebody. That is the question underneath the question."),
            ("no", "Not without checking", "do-it-properly",
             "Go and look. Old supplier accounts and forgotten VPN users are one of "
             "the most common ways in, and the fix is deleting things rather than "
             "buying anything."),
        ],
        ladder=(3,
                "Rung 4 wants both site-to-site and per-user encrypted access with "
                "continuous policy enforcement, which is where the zero trust "
                "platforms live. MFA on the VPN, a reviewed user list and closed "
                "supplier sessions is the point where the risk drops sharply and "
                "the price has not yet.",
                [(1, "Remote access with a password only, or nobody knows who has it.", "do-it-properly"),
                 (2, "VPN with MFA, user list roughly known.", "cheap-checkbox"),
                 (3, "MFA, reviewed list, supplier sessions opened on request.", "already-solved"),
                 (4, "Per-application zero trust access with continuous policy.", "cheap-checkbox")]),
        costs={"MFA on the existing VPN": "€",
               "reviewed access list and session control": "€€",
               "zero trust network access platform": "€€€€"},
        sec=3, chk=3,
        evidence=("Remote access needs a VPN.",
                  "A list of who has remote access and the MFA policy covering it.",
                  "The list, dated review, evidence of MFA enforcement, and the "
                  "process for opening and closing supplier sessions."),
        frameworks=["nist-csf-pr.aa-03", "nist-csf-pr.ir-01", "iso27002-6.7", "nis2-art21"],
        patterns=[],
        already_have=["admin-mfa", "device-compliance"],
    ),

    "remote-work-model": dict(
        priority=2,
        plain_english=(
            "Do you have rules for working from home. Not the connection, the "
            "arrangement."),
        misunderstanding=(
            "People read this as remote access and answer with VPN. It is wider "
            "than that. Rights and responsibilities, furniture, printers, "
            "electricity, insurance, and how you keep a clean desk policy alive in "
            "somebody's kitchen. Whether personal devices are allowed at all is "
            "part of it, and that is a decision somebody has to actually make "
            "rather than let happen."),
        skeptic_case=(
            "Most of this is an HR document, not a security purchase. The security "
            "part is two decisions: are personal devices allowed to reach company "
            "data, and what happens to paper at home. Answer those two, write them "
            "into the remote working policy that HR already needs, and stop."),
        applies_if=["has_remote_workers"],
        applies_never_if=["no_remote_work"],
        how_to_say_no=(
            "Not applicable. Staff work from company premises and are not "
            "permitted to access company systems from elsewhere."),
        default_verdict="write-it-down",
        question="Can somebody use their own laptop for work?",
        options=[
            ("no", "No, company devices only", "already-solved",
             "That is the cleanest answer on this whole question and it makes "
             "several others easy. Write it down and enforce it at the login."),
            ("yes_unmanaged", "Yes, whatever they have", "do-it-properly",
             "Decide what that device is allowed to reach. Browser-only access to "
             "cloud apps is a reasonable middle ground and costs nothing."),
            ("yes_managed", "Yes, if it is enrolled", "already-solved",
             "Fine. Say that access requires an enrolled device and point at the "
             "compliance policy."),
        ],
        ladder=(2,
                "Rung 4 wants remote working covered in business continuity plans, "
                "tabletop exercises and monitoring of every connecting device. Most "
                "companies learned the continuity part in 2020 by doing it. A "
                "written policy and a device rule is the part that was never "
                "actually written down.",
                [(1, "No rules, people work out their own arrangement.", "write-it-down"),
                 (2, "A written policy covering devices and paper.", "already-solved"),
                 (3, "Policy plus enforced device compliance.", "cheap-checkbox"),
                 (4, "Remote working built into continuity plans and exercises.", "cheap-checkbox")]),
        costs={"write the policy": "€", "enforce enrolled devices": "€€",
               "issue company devices to everyone": "€€€"},
        sec=2, chk=2,
        evidence=("People work from home sometimes.",
                  "A written remote working policy covering devices and information "
                  "handling.",
                  "The policy, plus a device compliance rule enforced at login."),
        frameworks=["nist-csf-pr.aa-05", "iso27002-6.7"],
        patterns=["documentation-only"],
        already_have=["device-compliance", "mobile-app-protection"],
    ),

    "screen-lock": dict(
        priority=3,
        plain_english=(
            "Do machines lock themselves when people walk away from them."),
        misunderstanding=(
            "The standard Windows screensaver is enough, as long as it asks for a "
            "password when you come back. That is the whole control. People "
            "over-think it and then set the timeout to two minutes, which just "
            "teaches everybody to jiggle the mouse."),
        skeptic_case=(
            "This is already on in any managed Windows or Mac estate and is set "
            "centrally in Intune or the equivalent. If it is not on, it is a policy "
            "toggle, not a project. The only real judgement is the timeout, and "
            "fifteen minutes in an office with a locked front door is a defensible "
            "answer even when a checklist says five."),
        applies_if=["has_employees", "has_office"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. Workstations lock automatically after a defined period of "
            "inactivity and require re-authentication."),
        default_verdict="already-solved",
        question="Does your device lock itself if you go for a coffee?",
        options=[
            ("yes", "Yes", "already-solved",
             "Go and screenshot the policy that sets it. This is one of the "
             "questions you can close in five minutes with a picture."),
            ("no", "No", "write-it-down",
             "Turn it on centrally. It is included in what you already have, it "
             "takes ten minutes, and it closes the question permanently."),
        ],
        ladder=None,
        costs={"turn on the policy you already have": "€"},
        sec=1, chk=2,
        evidence=("People lock their screens.",
                  "A screenshot of the group policy or device policy setting the "
                  "timeout.",
                  "The policy plus a compliance report showing which devices it "
                  "applies to."),
        frameworks=["nist-csf-pr.aa-05", "iso27002-7.7"],
        patterns=["framework-inheritance"],
        already_have=["screen-lock", "device-compliance"],
    ),

    "removable-media": dict(
        priority=2,
        plain_english=(
            "Do you have a policy about USB sticks and external drives."),
        misunderstanding=(
            "Removable media used to be the main event. Not so much any more, but "
            "it is still a good way to get malware into protected areas, "
            "particularly OT networks where the engineer's USB stick is the only "
            "thing that crosses the boundary. Do you have a process for that?"),
        skeptic_case=(
            "Blocking USB storage everywhere annoys people who have a legitimate "
            "reason and pushes them onto personal cloud accounts, which is worse. "
            "Block it where it matters, which is the production network and any "
            "machine handling sensitive data, and leave the office alone unless you "
            "have a reason. The blocking itself is a policy setting you already own."),
        applies_if=["has_employees"],
        applies_never_if=[],
        how_to_say_no=(
            "Partially applicable. Removable media is restricted on systems where "
            "it presents a risk. The scope of that restriction is described below."),
        default_verdict="cheap-checkbox",
        question="Does anything of yours sit on a network that a USB stick could reach?",
        options=[
            ("ot", "Yes, production kit", "do-it-properly",
             "Then this is a real control rather than a checkbox. Scanning station "
             "at the boundary, and a rule that engineers do not carry sticks "
             "between the office and the line."),
            ("office", "Just office machines", "cheap-checkbox",
             "Restrict it centrally where it costs you nothing, say what you did, "
             "and do not make a project of it."),
            ("cloud", "We are cloud only, nothing local", "not-applicable",
             "Then say that. There is no data on the endpoint worth taking on a "
             "stick, and that is a better answer than a policy."),
        ],
        ladder=(2,
                "Rung 4 wants an authorisation process for every removal of media "
                "from the premises, logged. In a manufacturing site with a "
                "controlled boundary that is real. In an office it is a form that "
                "nobody fills in.",
                [(1, "No restriction, no policy.", "write-it-down"),
                 (2, "Restricted where it matters, written down.", "already-solved"),
                 (3, "Central control with exceptions approved.", "cheap-checkbox"),
                 (4, "Authorisation and logging for every removal.", "cheap-checkbox")]),
        costs={"policy setting on managed devices": "€",
               "scanning station for the OT boundary": "€€€"},
        sec=2, chk=2,
        evidence=("We tell people not to use USB sticks.",
                  "The device policy showing removable storage restricted, and "
                  "where.",
                  "The policy, the exception list, and for OT the scanning "
                  "procedure at the boundary."),
        frameworks=["nist-csf-pr.ds-01", "iso27002-7.10"],
        patterns=[],
        already_have=["device-compliance"],
    ),

    "mobile-device-management": dict(
        priority=2,
        plain_english=(
            "Can you wipe company data off a phone when it goes missing."),
        misunderstanding=(
            "MDM covers a lot of ground, but in its simplest form it means you can "
            "remove your data in an emergency. It can also deploy phones, manage "
            "applications and push endpoint protection, but you do not always need "
            "that. Start with the wipe. The rest is optional."),
        skeptic_case=(
            "Full device management on a phone somebody bought themselves is a "
            "fight you will lose, and in some countries a legal problem. Application "
            "level protection, where the company data lives in a container you can "
            "wipe and the holiday photos are untouched, is included in Microsoft 365 "
            "and Google Workspace business tiers and answers this question honestly."),
        applies_if=["has_mobile_devices"],
        applies_never_if=["no_mobile_access"],
        how_to_say_no=(
            "Partially applicable. Company data on mobile devices is contained and "
            "can be removed remotely. Full device management is not applied to "
            "personally owned devices, and the boundary is described below."),
        default_verdict="cheap-checkbox",
        question="If a phone with company email vanished today, could you clear it?",
        options=[
            ("yes", "Yes, remotely", "already-solved",
             "Then answer with the mechanism and whether it covers personal "
             "devices too. You already own this."),
            ("no", "No", "write-it-down",
             "Turn on app protection in the licence you already have. It contains "
             "the company data without touching the rest of the phone, and it takes "
             "an afternoon."),
        ],
        ladder=(2,
                "Rung 4 wants full management on every connecting device including "
                "personally owned ones. That is a per-device licence and an "
                "argument with staff. Containing company data so it can be wiped "
                "separately is the control that matters and it is already in the "
                "subscription.",
                [(1, "No way to remove company data from a phone.", "write-it-down"),
                 (2, "App-level protection, company data can be wiped.", "already-solved"),
                 (3, "Full management on company devices, containers on personal.", "cheap-checkbox"),
                 (4, "Full management on everything that connects.", "cheap-checkbox")]),
        costs={"app protection in your existing licence": "€",
               "full MDM on company devices": "€€",
               "managed devices for everyone": "€€€"},
        sec=2, chk=2,
        evidence=("We could ask them to change their password.",
                  "A screenshot of the app protection or device policy.",
                  "The policy, the devices it covers, and a record of a wipe having "
                  "been performed."),
        frameworks=["nist-csf-pr.aa-05", "iso27002-8.1"],
        patterns=["framework-inheritance"],
        already_have=["mobile-app-protection", "device-compliance"],
    ),

    "third-party-access": dict(
        priority=1,
        plain_english=(
            "Do you have a process for letting outside people into your systems. "
            "The HVAC repairman, the network technician, the supplier who maintains "
            "your production line."),
        misunderstanding=(
            "Access must be tightly limited and watched. Sessions should be opened "
            "for a single job and closed afterwards, and ideally recorded. The "
            "thing people miss is that this is where the famous breaches actually "
            "started: not a clever exploit, a maintenance account with a password "
            "from 2015 that nobody switched off."),
        skeptic_case=(
            "Session recording and a privileged access platform are the expensive "
            "answer and they are aimed at organisations with dozens of suppliers "
            "logging in. If you have four, the control is a named account per "
            "supplier instead of a shared one, MFA on it, and a rule that it is "
            "disabled between jobs. That is free and it removes most of the risk."),
        applies_if=["has_suppliers", "has_servers"],
        applies_never_if=["no_third_party_access"],
        how_to_say_no=(
            "Not applicable. No third party holds access to our information "
            "systems. Supplier work is performed on site under supervision."),
        default_verdict="do-it-properly",
        question="Does any supplier have a login to your systems right now?",
        options=[
            ("none", "No", "not-applicable",
             "Say so, and say how supplier work gets done instead. Clean answer."),
            ("shared", "Yes, and it is a shared account", "do-it-properly",
             "Split it into named accounts per person, put MFA on them, and disable "
             "them between jobs. A shared supplier account is the single most "
             "reliable way into a small company."),
            ("named", "Yes, named accounts, MFA", "already-solved",
             "Then answer with how they are reviewed and how quickly you can turn "
             "one off. Add logging if it is not there."),
        ],
        ladder=(3,
                "Rung 4 wants every third-party session logged, reviewed and "
                "usually recorded, which means a platform. Named accounts, MFA, "
                "disabled between jobs and reviewed twice a year gets you almost "
                "all of the protection with none of the licence cost.",
                [(1, "Shared supplier account, always on.", "do-it-properly"),
                 (2, "Named accounts, but always on.", "do-it-properly"),
                 (3, "Named accounts with MFA, opened per job, reviewed.", "already-solved"),
                 (4, "Full session logging and recording through a platform.", "cheap-checkbox")]),
        costs={"named accounts and MFA": "€",
               "open and close per job, reviewed": "€€",
               "session recording platform": "€€€€"},
        sec=3, chk=3,
        evidence=("Suppliers get access when they need it.",
                  "A list of third parties with access and what each can reach.",
                  "The list, evidence of MFA, a dated review, and logs showing "
                  "sessions opened and closed."),
        frameworks=["nist-csf-pr.aa-05", "nist-csf-gv.sc-07", "iso27002-5.20", "nis2-art21"],
        patterns=[],
        already_have=["audit-logging"],
    ),
}
