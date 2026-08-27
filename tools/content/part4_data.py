"""Inventories, data protection, backups and continuity."""

CARDS = {

    "asset-inventory": dict(
        priority=1,
        plain_english=(
            "Do you know what you have. Data, software, hardware. At minimum, every "
            "PC and what is installed on it."),
        misunderstanding=(
            "One might think this is only for finance. It matters just as much for "
            "security. The asset inventory is where you see software and firmware "
            "versions, and where you match them against published vulnerabilities "
            "to work out what needs patching. Without it, patching is guesswork and "
            "so is answering the vulnerability questions further down the form."),
        skeptic_case=(
            "Some kind of inventory is always needed, but you may already have it "
            "without knowing. If you run Intune, or Jamf, or almost any RMM tool, "
            "the list is already being collected and you just have to export it. "
            "Buying an asset management product before checking what your existing "
            "tools already know is the common mistake here."),
        applies_if=["any_business_data"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. An inventory of hardware, software and information assets "
            "is maintained. The mechanism and refresh frequency are described below."),
        default_verdict="cheap-checkbox",
        question="Could you produce a list of every PC and what is on it today?",
        options=[
            ("tool", "Yes, from Intune or similar", "already-solved",
             "Export it and attach it. You already own this one and most people in "
             "your position do not realise it."),
            ("sheet", "There is a spreadsheet somewhere", "cheap-checkbox",
             "Good enough to answer, as long as it is roughly current. Put a "
             "reminder in the calendar to check it twice a year and that closes it."),
            ("no", "No", "do-it-properly",
             "This one is worth doing properly because everything else leans on it. "
             "Patching, vulnerability management and incident response all start "
             "with knowing what you have."),
        ],
        ladder=(3,
                "Rung 4 wants automated inventory that updates as the organisation "
                "changes. If you already manage devices centrally, you are at rung "
                "4 without buying anything, which is why this is worth checking "
                "before spending. If you do not, the tool is a real cost for a "
                "list a person could maintain.",
                [(1, "Nobody knows what is out there.", "do-it-properly"),
                 (2, "A partial list, out of date.", "cheap-checkbox"),
                 (3, "Covers everything, checked periodically.", "already-solved"),
                 (4, "Automated and current by itself.", "already-solved")]),
        costs={"export what your device tool already collects": "€",
               "a maintained spreadsheet": "€",
               "asset management product": "€€€"},
        sec=3, chk=3,
        evidence=("We know what we have.",
                  "An exported inventory with make, model and installed software.",
                  "The inventory, its source system, the refresh frequency, and an "
                  "owner per asset class."),
        frameworks=["nist-csf-id.am-01", "nist-csf-id.am-02", "iso27002-5.9", "nis2-art21"],
        patterns=["framework-inheritance"],
        already_have=["device-compliance"],
    ),

    "supplier-inventory": dict(
        priority=1,
        plain_english=(
            "Do you have a list of your suppliers, and have you looked at which of "
            "them could hurt you."),
        misunderstanding=(
            "This is not the same list finance keeps. Finance knows who you pay. "
            "Security needs to know who can reach your systems or your data, and "
            "those are different sets. The cleaning company is on one list. The "
            "firm that remotes into your production line is on the other, and often "
            "gets paid so little that nobody notices them."),
        skeptic_case=(
            "You do not need a supplier risk platform. Take the finance list, mark "
            "the ones that hold your data or can log in, and you are done in an "
            "afternoon. That marked subset is usually under ten names, and those "
            "ten are the ones worth any further effort."),
        applies_if=["has_suppliers"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. The suppliers who can log in, or who hold our data, are "
            "identified and recorded separately from the general supplier list."),
        default_verdict="write-it-down",
        question="Could you name every supplier who holds your data or can log in?",
        options=[
            ("yes", "Yes, it is a short list", "already-solved",
             "Then write it down where somebody else can find it, with what each "
             "one can reach. That is the control."),
            ("no", "Not off the top of my head", "write-it-down",
             "An afternoon with the finance list and a highlighter. This underpins "
             "every third-party question further down the form."),
        ],
        ladder=(2,
                "Rung 4 wants the list automatically updated as the organisation "
                "changes, which means a supplier management platform. In a company "
                "with under fifty suppliers the list changes a few times a year and "
                "a person updating it is faster than a system nobody feeds.",
                [(1, "No list beyond who gets paid.", "write-it-down"),
                 (2, "A list of who holds data or has access.", "already-solved"),
                 (3, "Full list with criticality, reviewed yearly.", "cheap-checkbox"),
                 (4, "Automatically maintained supplier register.", "cheap-checkbox")]),
        costs={"mark up the finance list": "€",
               "criticality and yearly review": "€€",
               "supplier management platform": "€€€"},
        sec=2, chk=3,
        evidence=("We know who our suppliers are.",
                  "A list naming the suppliers who can log in or hold data.",
                  "The list, with what each can reach, a criticality rating and a "
                  "dated review."),
        frameworks=["nist-csf-gv.sc-04", "nist-csf-id.am-04", "nis2-art21"],
        patterns=[],
        already_have=[],
    ),

    "data-classification": dict(
        priority=1,
        plain_english=(
            "Is your data marked as Public, Internal or Confidential, or whatever "
            "labels you chose."),
        misunderstanding=(
            "This should be straightforward and it is actually quite rare. The "
            "reason it matters is that every other data control depends on it. You "
            "cannot decide what to encrypt, what to stop leaving, or what to keep "
            "for seven years, until somebody has said which data is which."),
        skeptic_case=(
            "Companies try to dodge the tedious part by declaring that all our data "
            "is confidential, especially when facing retrospective classification of "
            "twenty years of files. That is a defensible answer if you mean it and "
            "you then treat it all that way. It is a bad answer if you say it and "
            "carry on emailing spreadsheets around, because now you have written "
            "evidence that you knew. Three labels, applied going forward, beats a "
            "project to classify the archive."),
        applies_if=["any_business_data"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. A classification scheme is defined and applied to "
            "information created going forward. The treatment of legacy data is "
            "described below."),
        default_verdict="write-it-down",
        question="If I picked a file at random, would anything tell me how secret it is?",
        options=[
            ("yes", "Yes, it is labelled", "already-solved",
             "Then answer with the scheme and how it is applied. You are ahead of "
             "most companies asked this."),
            ("no", "No", "write-it-down",
             "Pick three labels, write one line each saying how to handle them, and "
             "apply them going forward. Do not start with the archive or you will "
             "never finish."),
        ],
        ladder=(2,
                "Rung 4 wants classification applied regularly, at every significant "
                "change, across all use cases. That is a data governance function "
                "with tooling. A three-label scheme applied to new documents, with "
                "the old material left alone unless it moves, is honest and it is "
                "what most companies at rung 4 are actually doing anyway.",
                [(1, "No scheme, or one nobody uses.", "write-it-down"),
                 (2, "A scheme exists and is applied to new material.", "already-solved"),
                 (3, "Applied consistently, drives handling rules.", "cheap-checkbox"),
                 (4, "Reviewed at every change, covers everything.", "cheap-checkbox")]),
        costs={"three labels and a handling rule each": "€",
               "labelling built into the office tools": "€€",
               "retrospective classification project": "€€€€"},
        sec=2, chk=3,
        evidence=("We know what is sensitive.",
                  "A written classification scheme with handling rules per label.",
                  "The scheme, evidence it is applied in the document tools, and "
                  "the rules that follow from each label."),
        frameworks=["nist-csf-id.am-05", "iso27002-5.12", "iso27002-5.13"],
        patterns=["outcome-as-process"],
        already_have=["external-sharing-controls"],
    ),

    "secure-procurement": dict(
        priority=2,
        plain_english=(
            "Does procurement have a way of judging supplier risk before signing, "
            "and do your contracts mention security and privacy at all."),
        misunderstanding=(
            "Security gets asked after the contract is signed, which is the one "
            "moment when you have no leverage left. Before signature you can ask "
            "for anything. After it you are asking a favour. The same applies to "
            "equipment: the time to ask whether a machine can be patched is before "
            "it arrives on a pallet."),
        skeptic_case=(
            "Do not build a procurement gate that everybody routes around. Two "
            "questions on the purchase form, one about whether the supplier will "
            "hold company or personal data and one about whether they need access "
            "to systems, catches the purchases that matter. Everything else goes "
            "through unchanged."),
        applies_if=["has_suppliers"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. Security and privacy requirements are considered before "
            "purchase where the supplier will hold data or require access, and are "
            "reflected in contracts."),
        default_verdict="write-it-down",
        question="Does anyone ask about security before you sign with a new supplier?",
        options=[
            ("yes", "Yes, it is part of the process", "already-solved",
             "Write down what gets asked, so it survives the person who currently "
             "asks it leaving."),
            ("no", "It comes up afterwards, if at all", "write-it-down",
             "Add two questions to the purchase form. It costs nothing and it moves "
             "the conversation to the only point where you have leverage."),
        ],
        ladder=None,
        costs={"two questions on the purchase form": "€",
               "standard security terms in contracts": "€€",
               "formal supplier assessment before signing": "€€€"},
        sec=2, chk=2,
        evidence=("We think about security when buying.",
                  "The purchase process showing where security is considered.",
                  "The process, the standard contract clauses, and examples from "
                  "recent purchases."),
        frameworks=["nist-csf-gv.sc-05", "nist-csf-gv.sc-06", "iso27002-5.20"],
        patterns=[],
        already_have=[],
    ),

    "encryption": dict(
        priority=1,
        plain_english=(
            "Is your data encrypted where it sits and where it travels, and does "
            "anyone look after the keys."),
        misunderstanding=(
            "Many think everything is encrypted by default now. It is not. And even "
            "where it is, you need a way to manage the keys. What happens when an "
            "encrypted PC will not boot and the recovery key is in an account "
            "nobody can get into? If you operate internationally there is another "
            "trap: some countries limit which encryption you may use or import, and "
            "that is a legal question rather than a technical one."),
        skeptic_case=(
            "Disk encryption and encryption in transit are both already on in any "
            "modern setup and cost nothing. The expensive version is holding your "
            "own keys in a hardware module so the cloud provider cannot read your "
            "data. That is a real control for a handful of regulated businesses and "
            "an expensive way to lock yourself out for everyone else."),
        applies_if=["any_business_data"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. Data is encrypted at rest and in transit using platform "
            "capabilities. Key management responsibilities and any legal "
            "restrictions in our operating countries are described below."),
        default_verdict="already-solved",
        question="If a laptop was stolen tonight, could someone read the disk?",
        options=[
            ("no", "No, it is encrypted", "already-solved",
             "Then answer with the mechanism and, more importantly, say where the "
             "recovery keys are held. The keys are the part people fail on."),
            ("yes", "Probably", "do-it-properly",
             "Turn on disk encryption. It is built into Windows and macOS, it costs "
             "nothing, and it converts a lost laptop from a data breach into a "
             "hardware loss."),
            ("dontknow", "No idea", "need-one-fact",
             "Go and check one machine. It takes two minutes and it decides whether "
             "this is a five-minute answer or a week of work."),
        ],
        ladder=(3,
                "Rung 4 usually means customer-managed keys in a hardware security "
                "module. That is a real control if a regulator requires it and an "
                "expensive way to lose access to your own data if not. Platform "
                "encryption with keys you can actually recover is where most "
                "companies should stop.",
                [(1, "Nothing encrypted.", "do-it-properly"),
                 (2, "Some systems, no key management.", "cheap-checkbox"),
                 (3, "At rest and in transit, keys recoverable and held safely.", "already-solved"),
                 (4, "Customer-managed keys in dedicated hardware.", "cheap-checkbox")]),
        costs={"turn on platform encryption": "€",
               "documented key management": "€€",
               "customer-managed keys in an HSM": "€€€€"},
        sec=2, chk=3,
        evidence=("Our data is encrypted.",
                  "Policy plus evidence that disk encryption is enforced on "
                  "devices.",
                  "The policy, a device compliance report, and a written statement "
                  "of where recovery keys are held and who can get them."),
        frameworks=["nist-csf-pr.ds-01", "nist-csf-pr.ds-02", "iso27002-8.24", "nis2-art21"],
        patterns=["framework-inheritance"],
        already_have=["data-at-rest-encryption", "email-encryption-in-transit"],
    ),

    "full-disk-encryption": dict(
        priority=2,
        plain_english=(
            "Are laptops and phones encrypted so that finding one does not mean "
            "reading it."),
        misunderstanding=(
            "Nothing is foolproof, but you make it harder. File encryption and full "
            "disk encryption used to be two competing strategies. On PCs and phones "
            "today the whole disk is encrypted and that argument is over. The "
            "remaining question is whether it is actually switched on and whether "
            "you can prove it."),
        skeptic_case=(
            "There is no case against this. BitLocker and FileVault are included, "
            "they are a policy toggle on a managed device, and the performance "
            "argument died a decade ago. The only real work is making sure recovery "
            "keys are escrowed somewhere you can reach them."),
        applies_if=["has_employees"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. Full disk encryption is enforced on company laptops and "
            "mobile devices, with recovery keys escrowed centrally."),
        default_verdict="already-solved",
        question="Could you prove today that every laptop is encrypted?",
        options=[
            ("report", "Yes, there is a compliance report", "already-solved",
             "Attach it. This is one of the questions you close with a screenshot "
             "rather than a paragraph."),
            ("probably", "Probably, but I could not prove it", "cheap-checkbox",
             "Get the report out of your device management tool. The control is "
             "almost certainly already on. What you are missing is the evidence."),
            ("no", "No", "do-it-properly",
             "Turn it on. It is free, it is an afternoon on a managed estate, and a "
             "lost laptop stops being a notifiable event."),
        ],
        ladder=(3,
                "Rung 4 extends encryption to every connecting device including "
                "personal ones and IoT. On a phone or personal laptop you cannot "
                "enforce it, so the honest control is containing company data "
                "instead. Full coverage of company devices is the real target.",
                [(1, "Not encrypted.", "do-it-properly"),
                 (2, "Some devices.", "cheap-checkbox"),
                 (3, "All company devices, with keys escrowed.", "already-solved"),
                 (4, "Everything that connects, including personal kit.", "cheap-checkbox")]),
        costs={"turn on BitLocker or FileVault": "€",
               "central key escrow and reporting": "€"},
        sec=2, chk=3,
        evidence=("Laptops are encrypted.",
                  "A device compliance report showing encryption status.",
                  "The report covering all devices, plus evidence that recovery "
                  "keys are escrowed and retrievable."),
        frameworks=["nist-csf-pr.ds-01", "iso27002-8.24"],
        patterns=["framework-inheritance"],
        already_have=["data-at-rest-encryption", "device-compliance"],
    ),

    "tenant-segregation": dict(
        priority=2,
        plain_english=(
            "If you hold data for several customers, is one customer's data kept "
            "apart from another's."),
        misunderstanding=(
            "This is genuinely tricky in practice, especially on older systems that "
            "were built when you had one customer. It is also the question where a "
            "vague answer does the most damage, because the customer asking is "
            "asking whether their competitor can see their data."),
        skeptic_case=(
            "If you do not hold data for multiple customers, this does not apply and "
            "you should say so rather than reaching for something that sounds "
            "similar. If you do, this is not a checkbox, it is an architecture "
            "question, and the honest answer is either separate databases, a tenant "
            "identifier enforced in code, or you do not know. The third answer is "
            "the one worth acting on."),
        applies_if=["multi_customer_saas", "has_customer_data"],
        applies_never_if=["single_customer"],
        how_to_say_no=(
            "Not applicable. We do not host data for multiple customers in shared "
            "systems. Customer data received under this contract is held separately "
            "and is described below."),
        default_verdict="need-one-fact",
        question="Do you hold data for more than one customer in the same system?",
        options=[
            ("no", "No", "not-applicable",
             "Say so plainly. This is a SaaS question and it does not apply to most "
             "companies who receive it."),
            ("yes_separate", "Yes, separate databases per customer", "already-solved",
             "That is the strongest answer available. Say it and say how a new "
             "customer gets provisioned."),
            ("yes_shared", "Yes, shared, separated in the application", "do-it-properly",
             "Then somebody needs to be able to point at the code and the tests "
             "that enforce it. This is the failure mode that ends companies, so it "
             "is worth the review even though nobody enjoys it."),
        ],
        ladder=None,
        costs={"document the separation you already have": "€",
               "review and test the enforcement": "€€€",
               "re-architect to separate stores": "€€€€€"},
        sec=3, chk=3,
        evidence=("Customer data is separated.",
                  "A written description of how separation is enforced.",
                  "The description, plus test cases proving one tenant cannot reach "
                  "another, run recently."),
        frameworks=["nist-csf-pr.ds-01", "iso27002-8.31"],
        patterns=[],
        already_have=["external-sharing-controls"],
    ),

    "email-security": dict(
        priority=1,
        plain_english=(
            "Do you stop viruses, spam and phishing arriving by email."),
        misunderstanding=(
            "This should go both ways, not just inbound. Stopping annoying mail and "
            "stopping dangerous mail are two different jobs, though usually the same "
            "tool does both. Genuinely bad items should not be releasable by the "
            "user who received them, but there is a thin line there and false "
            "positives cause real problems when somebody cannot get the invoice "
            "they were waiting for."),
        skeptic_case=(
            "Microsoft 365 and Google Workspace both filter malware and spam by "
            "default, on every tier, and have done for years. You almost certainly "
            "already have this and can answer the question with a screenshot. The "
            "add-on products are worth money when you are being targeted "
            "specifically, not as a general upgrade."),
        applies_if=["has_employees"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. Inbound and outbound mail is filtered for malware and "
            "spam by our mail platform. The controls in place are listed below."),
        default_verdict="already-solved",
        question="Who provides your email?",
        options=[
            ("m365", "Microsoft 365 or Google Workspace", "already-solved",
             "Then malware and spam filtering are already on, included, and have "
             "been since you signed up. Screenshot the settings and close three "
             "questions at once."),
            ("own", "We run our own mail server", "do-it-properly",
             "Then this is genuinely your problem, and it is one of the better "
             "arguments for moving to a hosted platform. Filtering, patching and "
             "reputation management are a real job."),
        ],
        ladder=(3,
                "Rung 4 adds external sender warnings, macro blocking, attachment "
                "detonation and threat counting. Most of that is in the higher "
                "business tier you may already have. The external sender banner in "
                "particular is free and stops more invoice fraud than any product.",
                [(1, "No filtering.", "do-it-properly"),
                 (2, "Default platform filtering.", "already-solved"),
                 (3, "Filtering plus external sender warnings and macro blocking.", "already-solved"),
                 (4, "Full mail security suite with detonation and reporting.", "cheap-checkbox")]),
        costs={"what your platform already does": "€",
               "external sender banner and macro blocking": "€",
               "dedicated mail security product": "€€€"},
        sec=3, chk=3,
        evidence=("We have spam filtering.",
                  "Screenshots of the malware and spam policies in the mail "
                  "platform.",
                  "The policies, plus the external sender warning, macro handling, "
                  "and a sample of blocked message reporting."),
        frameworks=["nist-csf-pr.ps-05", "nist-csf-de.cm-01", "iso27002-8.7"],
        patterns=["framework-inheritance"],
        already_have=["email-malware-filtering", "email-spam-filtering",
                      "email-encryption-in-transit"],
    ),

    "dns-filtering": dict(
        priority=3,
        plain_english=(
            "Do you block dangerous or unwanted websites by name. Malware sites, "
            "and whatever else you have decided people should not reach."),
        misunderstanding=(
            "This used to be a product of its own. Nowadays it is usually done in "
            "the firewall, or in the endpoint agent, or in a zero trust policy, so "
            "people answer no when they actually have it in three places. Check "
            "before you buy anything."),
        skeptic_case=(
            "As a security control it is a useful extra layer and nothing more. It "
            "will not stop a determined attack and it does not replace endpoint "
            "protection. Where it earns its money is stopping the callback after "
            "something already got in, and for that a free or cheap DNS service "
            "does most of the job."),
        applies_if=["has_network"],
        applies_never_if=[],
        how_to_say_no=(
            "Partially applicable. Web and DNS filtering is provided through our "
            "firewall and endpoint protection rather than a separate service. The "
            "categories blocked are described below."),
        default_verdict="cheap-checkbox",
        question="Does anything stop a click on a malware link from connecting?",
        options=[
            ("yes", "Yes, firewall or endpoint blocks it", "already-solved",
             "Then answer with which, and do not buy a separate filtering service. "
             "You already have the control."),
            ("no", "Nothing", "cheap-checkbox",
             "A filtering DNS service is a few euros per user per month and a "
             "twenty-minute change. Cheap layer, no argument against it."),
        ],
        ladder=(2,
                "Rung 4 wants command and control detection and content-based "
                "categorisation on top. That is a secure web gateway, priced per "
                "user per month forever. Blocking known-bad domains gets most of "
                "the benefit at a fraction of the cost.",
                [(1, "No filtering at all.", "cheap-checkbox"),
                 (2, "Known-bad domains blocked.", "already-solved"),
                 (3, "Category filtering with a policy behind it.", "cheap-checkbox"),
                 (4, "Full gateway with command and control detection.", "cheap-checkbox")]),
        costs={"filtering DNS service": "€", "firewall web filtering you already own": "€",
               "secure web gateway": "€€€"},
        sec=1, chk=2,
        evidence=("We block bad websites.",
                  "The filtering configuration showing which categories are "
                  "blocked.",
                  "The configuration, the coverage across sites and remote users, "
                  "and a sample of blocked requests."),
        frameworks=["nist-csf-pr.ir-01", "nist-csf-de.cm-01"],
        patterns=["technology-prescription"],
        already_have=[],
    ),

    "backups": dict(
        priority=1,
        plain_english=(
            "Do you have backups. Are you certain they work. Do they match what you "
            "decided about downtime and data loss."),
        misunderstanding=(
            "It is not enough to have a backup. You must test that it works, and "
            "you must be able to restore in a reasonable time. A backup that has "
            "never been restored is not a backup, it is a hope. The second thing "
            "people miss is scope: databases and servers get backed up, and the "
            "file share somebody set up on a spare PC does not."),
        skeptic_case=(
            "In full cloud the concept gets vague. If there is no legal retention "
            "requirement, a small company can often be fine with the data sitting in "
            "the cloud service, provided the provider keeps enough history and you "
            "accept the supplier risk. That is a legitimate answer. It stops being "
            "legitimate the moment somebody deletes a mailbox and you find out the "
            "retention was thirty days."),
        applies_if=["any_business_data"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. Backups are taken for the systems supporting this "
            "contract, and restore capability is tested. Scope and frequency are "
            "described below."),
        default_verdict="do-it-properly",
        question="When did you last restore something from backup?",
        options=[
            ("recent", "Recently, and it worked", "already-solved",
             "Then you are in a small minority. Answer with the date and what you "
             "restored, because that single fact is worth more than the whole "
             "backup policy."),
            ("long", "A while ago", "cheap-checkbox",
             "Do one now, on one system, and write down the date and how long it "
             "took. An hour of work and it turns your answer from a claim into "
             "evidence."),
            ("never", "Never", "do-it-properly",
             "Then you do not know whether you have backups. Test one this week. "
             "This is the single highest-value hour on the entire questionnaire."),
        ],
        ladder=(3,
                "Rung 4 asks for automated backup, frequency by criticality, "
                "restore testing by criticality, offsite and disconnected copies "
                "and periodic auditing. The offsite and disconnected part matters "
                "and is covered separately. The auditing programme is where the "
                "cost runs away for little extra protection.",
                [(1, "No backups, or nobody knows.", "do-it-properly"),
                 (2, "Backups run, never tested.", "do-it-properly"),
                 (3, "Backups run, scope is known, restores tested.", "already-solved"),
                 (4, "Frequency and testing driven by criticality, audited.", "cheap-checkbox")]),
        costs={"cloud provider retention you already pay for": "€",
               "backup product for servers and endpoints": "€€",
               "tested restores on a schedule": "€€",
               "full backup programme with auditing": "€€€€"},
        sec=3, chk=3,
        evidence=("Backups are taken.",
                  "A backup schedule listing which systems are covered.",
                  "The schedule, plus a dated restore test record with how long it "
                  "took."),
        frameworks=["nist-csf-pr.ds-11", "nist-csf-rc.rp-01", "iso27002-8.13", "nis2-art21"],
        patterns=["outcome-as-process"],
        already_have=["backup-encryption", "retention-policy"],
    ),

    "offline-backups": dict(
        priority=1,
        plain_english=(
            "Is there a backup copy somewhere that is not reachable from your "
            "network."),
        misunderstanding=(
            "Tapes are not always used any more and often the only backup sits on a "
            "NAS, on the same network. So when everything gets encrypted, so does "
            "the backup. And if there is a fire, that burns too. It should be easy "
            "and a lot of companies still fail it."),
        skeptic_case=(
            "There is no argument against having one copy out of reach, and it is "
            "cheap now: immutable storage in the cloud, or a rotated drive in a "
            "different building. The expensive version is a full second site. You do "
            "not need a second site. You need one copy that ransomware cannot "
            "delete."),
        applies_if=["any_business_data"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. At least one backup copy is held offline or in immutable "
            "storage, separate from the systems it protects."),
        default_verdict="do-it-properly",
        question="If ransomware hit tonight, could it reach your backups too?",
        options=[
            ("yes", "Probably, it is on the same network", "do-it-properly",
             "This is the one to fix first. Immutable cloud storage costs very "
             "little, and it is the difference between a bad week and paying a "
             "ransom."),
            ("no", "No, there is a copy out of reach", "already-solved",
             "Then say where and how it is protected. This is one of the strongest "
             "answers you can give on the whole form."),
        ],
        ladder=(2,
                "Rung 4 adds separate credentials, periodic auditing and validation "
                "of the offline copy. Separate credentials are worth doing and "
                "nearly free. The rest is programme overhead. One immutable copy, "
                "with its own credentials, tested once, is the control.",
                [(1, "Everything reachable from the network.", "do-it-properly"),
                 (2, "One copy immutable or offline.", "already-solved"),
                 (3, "Offline copy with separate credentials, tested.", "already-solved"),
                 (4, "Audited and validated on a schedule.", "cheap-checkbox")]),
        costs={"immutable cloud storage": "€€",
               "rotated drives held offsite": "€€",
               "second site with replication": "€€€€"},
        sec=3, chk=2,
        evidence=("We have backups somewhere else.",
                  "A description of the offline or immutable copy and how it is "
                  "isolated.",
                  "The description, evidence of immutability settings or rotation "
                  "records, and separate credentials."),
        frameworks=["nist-csf-pr.ds-11", "nist-csf-rc.rp-03", "iso27002-8.13"],
        patterns=[],
        already_have=["backup-encryption"],
    ),

    "bia": dict(
        priority=1,
        plain_english=(
            "Do you have an estimate of what different kinds of incident would cost "
            "you."),
        misunderstanding=(
            "It is not rocket science. It is a spreadsheet saying that if our main "
            "server dies we lose ten thousand euros a day. That is a business impact "
            "analysis. Everything the frameworks add on top is refinement of that "
            "one number, and the one number is what actually changes decisions."),
        skeptic_case=(
            "If you run a business, you should know roughly what it costs when "
            "things go wrong, and you probably already do without having written it "
            "down. The consultant version produces a document with recovery time "
            "objectives per process and a dependency map. Useful in a bank. In a "
            "company of forty, four lines in a spreadsheet gets the same decisions "
            "made."),
        applies_if=["any_business_data"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. The business impact of losing key systems has been "
            "estimated and is used to prioritise recovery."),
        default_verdict="write-it-down",
        question="What does a day of downtime cost you?",
        options=[
            ("know", "I could give you a figure", "write-it-down",
             "Then write it down. That figure is what tells you whether any of the "
             "expensive controls on this form are worth buying."),
            ("dont", "No idea", "need-one-fact",
             "Work it out roughly. Revenue per day, plus the people sitting idle, "
             "plus whatever you have to do twice. An hour of arithmetic and every "
             "other decision here gets easier."),
        ],
        ladder=(2,
                "Rung 4 wants every kind of loss modelled separately: sales you "
                "never made, the extra cost of working round it, kit that "
                "insurance will not replace. That is an "
                "actuarial exercise. Revenue per day plus idle salaries gets you "
                "within the right order of magnitude, which is all a decision needs.",
                [(1, "No idea what an outage costs.", "write-it-down"),
                 (2, "A rough figure per day, written down.", "already-solved"),
                 (3, "Per-system impact driving recovery priorities.", "cheap-checkbox"),
                 (4, "Full financial modelling across impact types.", "cheap-checkbox")]),
        costs={"an hour with a spreadsheet": "€",
               "per-system impact analysis": "€€",
               "consultant-run financial modelling": "€€€€"},
        sec=2, chk=3,
        evidence=("Downtime would be expensive.",
                  "A written estimate of daily loss for key systems.",
                  "The estimate, its basis, and evidence it is used to set recovery "
                  "priorities."),
        frameworks=["nist-csf-id.ra-04", "nist-csf-gv.oc-04", "iso27002-5.30", "nis2-art21"],
        patterns=["outcome-as-process"],
        already_have=[],
    ),

    "bcp": dict(
        priority=1,
        plain_english=(
            "Do you have a plan for what to do when it all goes wrong."),
        misunderstanding=(
            "A business continuity plan is not about IT. It is about being ready for "
            "different kinds of trouble: illness, war, flooding, political mess, and "
            "IT incidents as one item on that list. People hand this to the IT "
            "person and get back a disaster recovery plan for the servers, which is "
            "a useful document and not the one that was asked for."),
        skeptic_case=(
            "Many small companies skip it, and it is still useful to have. When "
            "something happens you are too busy staying afloat to work out who "
            "calls the insurer. But the useful version is short. Who decides, who "
            "calls whom, where do people go, what do we tell customers, how do we "
            "keep taking orders. Five pages. The hundred-page plan is written to be "
            "audited, not used."),
        applies_if=["any_business_data"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. A business continuity plan covering our critical services "
            "is maintained, and the technical recovery plan sits underneath it."),
        default_verdict="write-it-down",
        question="If the building were unusable tomorrow, would anyone know what to do?",
        options=[
            ("yes", "Yes, there is a plan", "already-solved",
             "Answer with the date it was last updated and whether it has been "
             "tested. Testing is covered separately and it is what an auditor will "
             "actually push on."),
            ("no", "We would work it out", "write-it-down",
             "Write five pages while nothing is on fire. Who decides, who calls "
             "whom, where people go, what customers are told. That is the plan."),
        ],
        ladder=(2,
                "Rung 4 wants continuity and technical recovery plans for every part "
                "of the business, practised annually, covering supplier failure and "
                "data corruption as separate scenarios. Practised annually is worth "
                "it. Covering every part of the business is where small companies "
                "generate paperwork nobody reads.",
                [(1, "No plan.", "write-it-down"),
                 (2, "A short plan for the critical services.", "already-solved"),
                 (3, "Plans for all businesses, reviewed.", "cheap-checkbox"),
                 (4, "All businesses, practised annually, all scenarios.", "cheap-checkbox")]),
        costs={"five pages, written in-house": "€",
               "plans per business area": "€€",
               "consultant-written continuity programme": "€€€€"},
        sec=2, chk=3,
        evidence=("We would cope.",
                  "A written continuity plan naming roles and contacts.",
                  "The plan, dated, with evidence of the last review and the last "
                  "exercise."),
        frameworks=["nist-csf-rc.rp-01", "nist-csf-id.im-02", "iso27002-5.29", "nis2-art21"],
        patterns=["documentation-only"],
        already_have=[],
    ),

    "continuity-testing": dict(
        priority=1,
        plain_english=(
            "Do you test the continuity and recovery plans, or do they just exist."),
        misunderstanding=(
            "A plan is not a plan if it has not been tested. That is the whole card. "
            "Every untested recovery plan contains at least one thing that does not "
            "work, and you find out which one at the worst possible time."),
        skeptic_case=(
            "A full failover exercise is expensive and disruptive and most companies "
            "will never do one. They do not have to. Restore one system from backup "
            "and time it. Walk through the plan around a table for an hour. Write "
            "down what did not work. That is a test, it costs a morning, and it "
            "finds the same broken things the expensive version finds."),
        applies_if=["any_business_data"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. Recovery capability is tested and the results are "
            "recorded. The scope and frequency of testing are described below."),
        default_verdict="do-it-properly",
        question="Has anyone ever actually tried the recovery plan?",
        options=[
            ("yes", "Yes, and we wrote down what broke", "already-solved",
             "That is a better answer than most large companies can give. Attach "
             "the report."),
            ("partial", "We restored a file once", "cheap-checkbox",
             "Do it properly once on one system, end to end, and time it. Half a "
             "day, and it turns a claim into evidence."),
            ("no", "No", "do-it-properly",
             "Then the plan is a document, not a capability. One tabletop and one "
             "restore test. A morning each."),
        ],
        ladder=(2,
                "Rung 4 wants every process that has to come back exercised, with "
                "everybody who would be involved, on a planned cycle, written up "
                "each time. For most companies one tabletop and one real restore "
                "per year finds everything the full programme would.",
                [(1, "Never tested.", "do-it-properly"),
                 (2, "One tabletop or one restore test per year, written up.", "already-solved"),
                 (3, "Planned exercises covering critical systems.", "cheap-checkbox"),
                 (4, "Full programme with all personnel and post-exercise reports.", "cheap-checkbox")]),
        costs={"a tabletop and a restore test": "€",
               "annual exercise programme": "€€",
               "full failover testing": "€€€€"},
        sec=3, chk=3,
        evidence=("The plan exists.",
                  "A dated record of a restore test or tabletop exercise.",
                  "The record, what failed, what changed as a result, and the date "
                  "of the next one."),
        frameworks=["nist-csf-id.im-02", "nist-csf-rc.rp-05", "iso27002-5.30"],
        patterns=["outcome-as-process"],
        already_have=[],
    ),

    "antivirus-exclusions": dict(
        priority=2,
        plain_english=(
            "Do you have a process for systems where antivirus cannot be installed. "
            "Usually production and OT systems."),
        misunderstanding=(
            "Air-gapped is usually not good enough. Every system eventually gets "
            "connected to external media or a network, so some protection is needed. "
            "Where it genuinely cannot be installed, the exception has to be "
            "approved and the system hardened instead. The version of this question "
            "that catches people out is the negative phrasing. It is worded so "
            "that agreeing means the opposite of what it looks like. Read it "
            "twice before ticking."),
        skeptic_case=(
            "There is no version of this you get to skip, but there is a "
            "version that takes one line. If endpoint protection is running "
            "everywhere and nobody has turned it off, say exactly that and "
            "you are done. What you cannot do is answer yes while a machine "
            "in the corner has it disabled, because that is the machine the "
            "question is about. Anywhere it is off, or anywhere a vendor has "
            "made you exclude a folder or a process so their software will "
            "run, that is an exception: it needs a name, a reason, somebody "
            "who approved it, and something else protecting the box instead. "
            "That list is usually short and almost never written down, which "
            "is why the question gets asked."),
        applies_if=["has_ot", "has_servers"],
        applies_never_if=["all_systems_protected"],
        how_to_say_no=(
            "Not applicable. All systems in scope run endpoint protection with no "
            "vendor-required exclusions."),
        default_verdict="need-one-fact",
        question="Is there anywhere endpoint protection is off, or scanning "
                 "something less than everything?",
        options=[
            ("none", "No, it is on everywhere and untouched", "not-applicable",
             "Then say that in one line. It is the right answer for most "
             "companies getting this question, and it is the only version of "
             "this row that costs you nothing."),
            ("excluded", "It runs, but some folders are excluded", "write-it-down",
             "Those exclusions came from somewhere, usually a vendor telling "
             "you their software breaks otherwise. List which paths, whose "
             "software required it, and who agreed. An unexplained exclusion "
             "is the thing that survives on a machine for six years."),
            ("some", "A few machines cannot run it", "write-it-down",
             "Then write down which ones, why, who approved it, and what "
             "protects them instead. Usually network isolation and locked-down "
             "access. That is a complete answer."),
        ],
        ladder=None,
        costs={"document the exceptions": "€",
               "isolate and harden the excepted systems": "€€€"},
        sec=2, chk=2,
        evidence=("Everything has antivirus.",
                  "A list of systems without endpoint protection, and of the "
                  "exclusions configured on the ones that have it, with reasons.",
                  "The list, the approval for each exception, and a description of "
                  "the compensating controls."),
        frameworks=["nist-csf-pr.ps-05", "iso27002-8.7"],
        patterns=["technology-prescription"],
        already_have=[],
    ),
}
