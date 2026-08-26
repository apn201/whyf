"""Operations, network and application security."""

CARDS = {

    "patch-management": dict(
        priority=1,
        plain_english=(
            "Do you have a process to update vulnerable systems within a set number "
            "of days."),
        misunderstanding=(
            "Not only the operating system. All software and firmware has to be "
            "patched. Best is to patch everything immediately, but in complex "
            "networks and OT environments that is not easy. Instead of doing "
            "nothing, get an approved exception for the things you cannot patch. A "
            "usual rule looks like: anything scoring CVSS 9 or above within 5 days, "
            "the rest within 15. Pick numbers you can actually meet and write them "
            "down."),
        skeptic_case=(
            "There is no argument against patching. There is a strong argument "
            "against buying a patch management platform before you have turned on "
            "the automatic updates that are already free. Windows Update, the "
            "browser's own updater and the app store cover most of the estate at "
            "zero cost. The platform earns its money when you have servers and OT "
            "that need scheduling around production."),
        applies_if=["has_servers", "has_employees"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. Patches are applied within defined timeframes based on "
            "severity. Systems that cannot be patched are subject to a documented "
            "exception with compensating controls."),
        default_verdict="do-it-properly",
        question="How long between a critical patch appearing and it being installed?",
        options=[
            ("days", "Days", "already-solved",
             "Then write the number down as a rule and you have both the control "
             "and the answer. Most companies cannot say this."),
            ("weeks", "Weeks, when someone gets to it", "cheap-checkbox",
             "Turn on automatic updates for everything that can take them, then set "
             "a rule for the rest. Most of the gap closes for free."),
            ("unknown", "No idea", "do-it-properly",
             "This is where most real compromises start, and it is not a "
             "paperwork gap. Start with automatic updates on the endpoints, then "
             "work out what is left."),
        ],
        ladder=(3,
                "Rung 4 wants out-of-band patch notifications correlated against "
                "your own environment with external sources reviewed annually. The "
                "correlation is only possible if the asset inventory is good, and "
                "that is the real prerequisite. Defined timeframes, met and "
                "evidenced, is the level that actually reduces risk.",
                [(1, "Patching happens when somebody remembers.", "do-it-properly"),
                 (2, "Automatic updates on endpoints, servers ad hoc.", "cheap-checkbox"),
                 (3, "Defined timeframes by severity, met and recorded.", "already-solved"),
                 (4, "Out-of-band notification correlated to the asset inventory.", "cheap-checkbox")]),
        costs={"turn on automatic updates": "€",
               "patch tooling for servers": "€€",
               "OT patching with production windows": "€€€€"},
        sec=3, chk=3,
        evidence=("We keep things up to date.",
                  "A written patching standard with timeframes by severity.",
                  "The standard, plus a report showing actual patch levels against "
                  "it and the approved exceptions."),
        frameworks=["nist-csf-id.ra-01", "nist-csf-pr.ps-02", "iso27002-8.8", "nis2-art21"],
        patterns=["outcome-as-process"],
        already_have=["device-compliance"],
    ),

    "vulnerability-management": dict(
        priority=1,
        plain_english=(
            "Related to patching. Do you have a way of finding weaknesses and "
            "fixing them."),
        misunderstanding=(
            "People treat this as the same thing as patching and it is not quite. "
            "Patching fixes the holes the vendor has already admitted to. "
            "Vulnerability management is finding out what you have that is exposed, "
            "including the things nobody has issued a patch for, and deciding what "
            "to do. Half of what a scan finds is a configuration you can change for "
            "free."),
        skeptic_case=(
            "An enterprise scanner with a per-asset licence is a big commitment for "
            "a small estate. If your external footprint is a website and a firewall, "
            "an external scan a few times a year plus vendor advisories covers it. "
            "The scanner is worth it when you have enough servers that nobody can "
            "hold the picture in their head."),
        applies_if=["has_servers", "has_website"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. Vulnerabilities are identified through scanning and vendor "
            "advisories, and remediated within defined timeframes."),
        default_verdict="cheap-checkbox",
        question="Has anything ever scanned your systems from outside?",
        options=[
            ("regular", "Yes, regularly", "already-solved",
             "Answer with the frequency and what happens to the findings. The "
             "findings part is what gets checked."),
            ("once", "Once, a while ago", "cheap-checkbox",
             "Do it again and put it in the calendar. External scanning is cheap "
             "and it tells you what an attacker sees."),
            ("never", "Never", "do-it-properly",
             "Start with the outside. What faces the internet is what gets found "
             "automatically by everyone else, so you should see it first."),
        ],
        ladder=(3,
                "Rung 4 wants every asset scanned against remediation deadlines "
                "with critical findings closed in 48 hours. Forty-eight hours is a "
                "commitment you will break, and a broken written commitment is "
                "worse than an honest longer one. Full coverage with realistic "
                "deadlines is the level that holds up.",
                [(1, "No scanning.", "do-it-properly"),
                 (2, "Occasional scans, findings not tracked.", "cheap-checkbox"),
                 (3, "Regular scans, findings tracked to a deadline.", "already-solved"),
                 (4, "All assets, tight SLAs, critical findings in 48 hours.", "cheap-checkbox")]),
        costs={"external scan a few times a year": "€",
               "scanner covering internal systems": "€€€",
               "continuous scanning with tight SLAs": "€€€€"},
        sec=3, chk=3,
        evidence=("We would notice a problem.",
                  "A recent scan report.",
                  "Scan reports over time, a tracked remediation list, and the "
                  "timeframes findings are closed against."),
        frameworks=["nist-csf-id.ra-01", "nist-csf-de.cm-09", "iso27002-8.8", "nis2-art21"],
        patterns=[],
        already_have=[],
    ),

    "hardening": dict(
        priority=2,
        plain_english=(
            "Have you turned off the things you do not use."),
        misunderstanding=(
            "Systems ship full of features you will never use and each one is a "
            "possible weak spot. Hardening means, especially on servers and "
            "sensitive systems, removing and disabling what is not needed and "
            "switching on the protections that do make sense. The second half of "
            "the question is about building machines the same way every time, so "
            "that hardening does not have to be redone by hand."),
        skeptic_case=(
            "Do not start from a CIS benchmark with a thousand settings and try to "
            "apply all of it. You will break something and then turn the whole thing "
            "off. Start from the vendor's own baseline, which Microsoft and Apple "
            "both publish free and both ship in their management tools, and deviate "
            "where you have to. That is a defensible answer and it costs nothing."),
        applies_if=["has_servers", "has_employees"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. Systems are built from a standard configuration with "
            "unnecessary services disabled. The baseline used is stated below."),
        default_verdict="cheap-checkbox",
        question="Are two new laptops set up the same way?",
        options=[
            ("yes", "Yes, from a standard build", "already-solved",
             "Then name the baseline and say how deviations are handled. That is "
             "the whole answer."),
            ("no", "Whoever sets it up does it their way", "write-it-down",
             "Adopt the vendor baseline in your device management tool. It is free, "
             "it is a day of work, and it makes every future machine consistent."),
        ],
        ladder=(3,
                "Rung 4 wants configurations updated continuously against emerging "
                "threats, which means somebody tracking benchmark changes and "
                "re-testing. A vendor baseline applied to everything, reviewed when "
                "the vendor updates it, gets the same security for a fraction of "
                "the attention.",
                [(1, "Every machine is different.", "write-it-down"),
                 (2, "A standard build is defined, not applied everywhere.", "cheap-checkbox"),
                 (3, "Baseline enforced on all endpoints and servers.", "already-solved"),
                 (4, "Continuously updated against emerging threats.", "cheap-checkbox")]),
        costs={"vendor baseline in your management tool": "€",
               "hardened server build documented": "€€",
               "full benchmark compliance with monitoring": "€€€€"},
        sec=2, chk=3,
        evidence=("We set machines up sensibly.",
                  "A named baseline and the policy applying it.",
                  "The baseline, a compliance report against it, and the documented "
                  "deviations."),
        frameworks=["nist-csf-pr.ps-01", "iso27002-8.9"],
        patterns=["framework-inheritance"],
        already_have=["device-compliance"],
    ),

    "application-allowlisting": dict(
        priority=2,
        plain_english=(
            "A policy that blocks everything by default and only allows certain "
            "applications to run."),
        misunderstanding=(
            "Blocklisting does nothing. Malware is compiled fresh for every attack. "
            "Allowlisting works, but it is hard to maintain in a complex "
            "environment. Depending how you do it, it breaks on software updates, "
            "or you allow a path and malware simply uses the same path. The common "
            "misunderstanding is that this is about installing. It is about "
            "executing. Nobody should have admin rights, which mostly stops "
            "installing, but it does not stop executing."),
        skeptic_case=(
            "Maintaining it is always more work than you expect. On a larger "
            "estate you genuinely need somebody resourced to support it before you "
            "switch it on, or you will spend your first month unblocking "
            "legitimate software and your second month with it disabled. Removing "
            "admin rights delivers a large share of the benefit and costs nothing."),
        applies_if=["has_employees"],
        applies_never_if=[],
        how_to_say_no=(
            "Partially applicable. Software execution is controlled through removal "
            "of administrative rights and an approved software list. Full "
            "allow-listing technology is not deployed, and the reason is stated "
            "below."),
        default_verdict="cheap-checkbox",
        question="Do your users have admin rights on their own machines?",
        options=[
            ("yes", "Yes", "do-it-properly",
             "Take them away before you look at any allow-listing product. That one "
             "change stops most of what allow-listing would have stopped, and it is "
             "free."),
            ("no", "No", "already-solved",
             "Then answer honestly: admin rights removed, approved software list, "
             "no allow-listing product. That is a legitimate rung and an auditor "
             "will take it."),
        ],
        ladder=(2,
                "Rung 4 covers executables, libraries and scripts including macros "
                "and PowerShell. Script-level allow-listing is where the "
                "maintenance load becomes a job, and it is aimed at organisations "
                "with a team. Removing admin rights and keeping an approved "
                "software list is where a small company should stop.",
                [(1, "Users are admins, anything runs.", "do-it-properly"),
                 (2, "Admin rights removed, approved software list.", "already-solved"),
                 (3, "Allow-listing on executables, maintained.", "cheap-checkbox"),
                 (4, "Executables, libraries and scripts covered.", "cheap-checkbox")]),
        costs={"remove admin rights": "€",
               "approved software list": "€",
               "allow-listing product plus the person to run it": "€€€€"},
        sec=3, chk=2,
        evidence=("People cannot install things.",
                  "The policy showing admin rights removed, plus the approved "
                  "software list.",
                  "The policy, a report of who still holds local admin and why, "
                  "and the exception process."),
        frameworks=["nist-csf-pr.ps-01", "iso27002-8.19"],
        patterns=["technology-prescription"],
        already_have=["device-compliance"],
    ),

    "endpoint-protection": dict(
        priority=1,
        plain_english=(
            "Endpoint protection is the new name for antivirus, because a virus is "
            "no longer the only threat. Is there something on every computer "
            "protecting it."),
        misunderstanding=(
            "It is not the same as antivirus, but in practice it is. Salespeople "
            "have made it confusing with EPP, EDR, NDR, XDR and MDR, partly bundled "
            "into the same products. What you need to know: is something running, "
            "is it updating, and would anyone find out if it alerted."),
        skeptic_case=(
            "Windows Defender is included, it is genuinely good now, and it tests "
            "at the top of the independent comparisons. For most companies buying a "
            "third-party product is replacing something free and adequate with "
            "something paid and adequate. Where the money goes further is the "
            "managed part: somebody watching the alerts. That is a different "
            "purchase from the agent."),
        applies_if=["has_employees"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. Endpoint protection with malware detection and prevention "
            "is deployed and centrally managed. Coverage is stated below."),
        default_verdict="already-solved",
        question="Would you know if a laptop had malware on it right now?",
        options=[
            ("yes", "Yes, alerts come somewhere", "already-solved",
             "Then answer with where they go and who reads them. Having the agent "
             "is common. Someone reading the alerts is not."),
            ("installed", "Something is installed, nobody watches it", "cheap-checkbox",
             "That is most companies. Point the alerts at a mailbox somebody "
             "actually opens. Free, and it turns a licence into a control."),
            ("no", "No", "do-it-properly",
             "Turn on Defender centrally, or whatever your estate has. It is "
             "included, and running unprotected in 2026 is not a defensible "
             "position on any form."),
        ],
        ladder=(3,
                "Rung 4 adds forensic capability and central event collection, "
                "which is EDR with somebody to use it. The agent is free. The "
                "person watching is the cost, and that is covered under monitoring. "
                "Everything protected and updating, with alerts going somewhere, is "
                "the level that matters.",
                [(1, "Nothing installed.", "do-it-properly"),
                 (2, "Installed on some devices.", "cheap-checkbox"),
                 (3, "All devices, updating, alerts reaching a person.", "already-solved"),
                 (4, "EDR with forensics and central event collection.", "cheap-checkbox")]),
        costs={"Defender or the built-in agent": "€",
               "third-party endpoint product": "€€",
               "managed detection and response": "€€€€"},
        sec=3, chk=3,
        evidence=("We have antivirus.",
                  "A console screenshot showing coverage and update status.",
                  "The coverage report, where alerts are sent, and evidence "
                  "somebody acted on one."),
        frameworks=["nist-csf-pr.ps-05", "nist-csf-de.cm-01", "iso27002-8.7"],
        patterns=["framework-inheritance"],
        already_have=["device-compliance"],
    ),

    "change-management": dict(
        priority=1,
        plain_english=(
            "Is there a process requiring approval before somebody changes "
            "something that could break things."),
        misunderstanding=(
            "Change management is not just a part of ITIL and the other frameworks. "
            "It can be based on email. Always ask your boss before you change "
            "something. It does not have to be a fancy automated system with hard "
            "controls. What matters is that somebody other than the person making "
            "the change knows it is happening."),
        skeptic_case=(
            "A change advisory board in a company of thirty is theatre and it slows "
            "things down until people start making changes without telling anyone, "
            "which is the outcome you were trying to prevent. An email to a second "
            "person before touching production, kept in a folder, is a real control "
            "and it passes audit."),
        applies_if=["has_servers"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. Changes to production systems are approved before "
            "implementation and recorded. The mechanism is proportionate to our "
            "size and is described below."),
        default_verdict="write-it-down",
        question="Can one person change production without telling anyone?",
        options=[
            ("yes", "Yes", "write-it-down",
             "Add one step: tell somebody first, in writing. Email is fine. It "
             "costs nothing and it catches the change that was going to take the "
             "line down on a Friday."),
            ("no", "No, it gets approved", "already-solved",
             "Then say how, and keep the approvals where you can find them. Email "
             "in a folder counts."),
        ],
        ladder=(2,
                "Rung 4 wants security impact assessment on every change, with "
                "high-risk requests denied by policy and everything in a workflow "
                "tool. The tool and the assessment step are where change management "
                "starts getting routed around. Written approval before production "
                "changes is the control that survives.",
                [(1, "Anyone changes anything.", "write-it-down"),
                 (2, "Changes approved in writing before production.", "already-solved"),
                 (3, "Approvals recorded with impact considered.", "cheap-checkbox"),
                 (4, "Formal workflow with security impact assessment.", "cheap-checkbox")]),
        costs={"an email before changing production": "€",
               "a ticket system you already have": "€",
               "formal change management tooling": "€€€"},
        sec=2, chk=3,
        evidence=("We talk to each other before changing things.",
                  "A record of change approvals, even if it is an email folder.",
                  "The process written down, approval records over a period, and "
                  "evidence that emergency changes get reviewed afterwards."),
        frameworks=["nist-csf-pr.ps-01", "iso27002-8.32", "iso27002-8.9"],
        patterns=["documentation-only"],
        already_have=[],
    ),

    "capacity-management": dict(
        priority=3,
        plain_english=(
            "In a security context this usually means your infrastructure. Do you "
            "know when you will need more compute, memory or disk."),
        misunderstanding=(
            "Capacity can mean people in a factory, or HR headcount. In IT it "
            "usually means is our server big enough and is the network fast enough. "
            "It is in the security questionnaire because running out of disk takes "
            "systems down just as effectively as an attacker, and because the "
            "backup that silently stopped running is nearly always a full disk."),
        skeptic_case=(
            "No fancy system is needed. What you need is to find out you are running "
            "out before you run out. A disk space alert on the servers, which every "
            "monitoring tool does free, covers the majority of real incidents. "
            "Capacity planning as a discipline is for people who buy hardware in "
            "advance, and in the cloud that problem mostly went away."),
        applies_if=["has_servers"],
        applies_never_if=["has_saas_only"],
        how_to_say_no=(
            "Partially applicable. Our systems are cloud-hosted and scale on "
            "demand. Monitoring of resource limits is described below."),
        default_verdict="write-it-down",
        question="Would you find out before a disk filled up?",
        options=[
            ("yes", "Yes, there is an alert", "already-solved",
             "That is the control. Say so and name where the alert goes."),
            ("no", "We find out when something breaks", "write-it-down",
             "Turn on disk and memory alerts. Every monitoring tool does it free "
             "and it takes an hour. It is also the most common cause of a backup "
             "silently failing."),
        ],
        ladder=(2,
                "Rung 4 wants managed redundancy across all workloads including "
                "protection against flooding attacks. That is capacity planning "
                "merged with resilience engineering. Alerts before you run out, and "
                "somewhere to add capacity when you do, is enough for almost "
                "everyone.",
                [(1, "Nobody watches it.", "write-it-down"),
                 (2, "Alerts on the critical systems.", "already-solved"),
                 (3, "Documented plan with headroom for growth.", "cheap-checkbox"),
                 (4, "Managed redundancy across all workloads.", "cheap-checkbox")]),
        costs={"alerts in your existing monitoring": "€",
               "a written capacity plan": "€€",
               "redundant capacity held spare": "€€€€"},
        sec=1, chk=2,
        evidence=("We have not run out yet.",
                  "Alerting configuration for disk, memory and bandwidth.",
                  "The alerting, plus a written statement of how additional "
                  "capacity is obtained and how quickly."),
        frameworks=["nist-csf-pr.ir-04", "iso27002-8.6"],
        patterns=[],
        already_have=[],
    ),

    "wireless-security": dict(
        priority=2,
        plain_english=(
            "Is the wireless network secured, and are guests kept off your internal "
            "network."),
        misunderstanding=(
            "People answer this with the encryption standard and stop. The "
            "encryption is the easy part and has been fine since WPA2. The part "
            "that matters is whether the guest network can reach anything internal, "
            "and whether an access point somebody plugged in themselves is sitting "
            "in a meeting room broadcasting your office network."),
        skeptic_case=(
            "You do not need wireless intrusion detection. You need a guest network "
            "that only reaches the internet, WPA2 or better on the office one, and "
            "somebody to notice unfamiliar access points. Two of those are settings "
            "you already have."),
        applies_if=["has_office", "has_network"],
        applies_never_if=["no_office"],
        how_to_say_no=(
            "Partially applicable. We operate no corporate wireless network at our "
            "sites. Where wireless is provided, it is isolated from internal "
            "systems and described below."),
        default_verdict="cheap-checkbox",
        question="Can a guest on your wifi reach the office network?",
        options=[
            ("yes", "Yes, or I am not sure", "do-it-properly",
             "Split it. Guest wireless that only reaches the internet is a setting "
             "on almost every business access point, and it removes the easiest "
             "physical way onto your network."),
            ("no", "No, guests are separated", "already-solved",
             "Then answer with that plus the encryption standard and you are done."),
        ],
        ladder=(3,
                "Rung 4 wants rogue access point detection and host-based firewalls "
                "on every wireless device. Rogue detection needs controller-grade "
                "kit. Separated guest network, modern encryption, changed defaults "
                "and wireless off where it is not needed is the practical target.",
                [(1, "One flat wireless network, default settings.", "do-it-properly"),
                 (2, "Modern encryption, defaults changed.", "cheap-checkbox"),
                 (3, "Guest network separated, wireless off where unneeded.", "already-solved"),
                 (4, "Rogue access point detection and monitoring.", "cheap-checkbox")]),
        costs={"separate the guest SSID": "€",
               "business access points with proper segmentation": "€€",
               "controller with rogue detection": "€€€"},
        sec=2, chk=2,
        evidence=("The wifi has a password.",
                  "The wireless configuration showing encryption and guest "
                  "separation.",
                  "The configuration, the network segments each SSID lands in, and "
                  "a record of the last check for unauthorised access points."),
        frameworks=["nist-csf-pr.ir-01", "iso27002-8.20"],
        patterns=[],
        already_have=[],
    ),

    "ddos-protection": dict(
        priority=3,
        plain_english=(
            "Do you have anything to stop someone flooding your servers with "
            "rubbish until they fall over."),
        misunderstanding=(
            "Many assume their hosting provider takes care of it, and often the "
            "provider does handle the crude volumetric attacks. But special controls "
            "are still needed even in AWS and the rest, and the protection that is "
            "on by default usually stops the network flood while leaving the "
            "application-level attack to you."),
        skeptic_case=(
            "If you do not run a public service that matters by the minute, this is "
            "somebody else's problem and you should say so. A brochure website going "
            "down for two hours costs almost nothing. Cloudflare's free tier in "
            "front of a website is a complete answer for most companies asked this "
            "question."),
        applies_if=["has_website"],
        applies_never_if=["no_internet_facing_service"],
        how_to_say_no=(
            "Not applicable in the form asked. We operate no internet-facing "
            "service where availability is contractually committed. Protection "
            "provided by our hosting arrangements is described below."),
        default_verdict="cheap-checkbox",
        question="Does it cost you money if your website is down for two hours?",
        options=[
            ("no", "Not really", "not-applicable",
             "Then say so. Availability protection you do not need is the easiest "
             "money to not spend, and the honest answer is a good answer."),
            ("yes", "Yes, it is how we sell", "do-it-properly",
             "Then put a filtering service in front of it. The entry tiers cost "
             "almost nothing and they handle the attacks that actually happen."),
        ],
        ladder=(2,
                "Rung 4 wants redundancy managed across all workloads to absorb "
                "flooding. That is capacity you pay for and never use. A filtering "
                "service in front of the public service, which is what everyone at "
                "rung 4 also has, is the actual control.",
                [(1, "Nothing at all.", "cheap-checkbox"),
                 (2, "Provider-level protection, filtering on the public service.", "already-solved"),
                 (3, "Filtering plus tested failover.", "cheap-checkbox"),
                 (4, "Redundant capacity across all workloads.", "cheap-checkbox")]),
        costs={"provider default protection": "€",
               "filtering service in front of the website": "€",
               "held redundant capacity": "€€€€"},
        sec=1, chk=2,
        evidence=("Our host deals with that.",
                  "A statement of what protection exists and who provides it.",
                  "The protection described, plus the provider's terms and any "
                  "test or incident record."),
        frameworks=["nist-csf-pr.ir-04", "iso27002-8.6"],
        patterns=["technology-prescription"],
        already_have=[],
    ),

    "network-segmentation": dict(
        priority=1,
        plain_english=(
            "Have you split the network up so a problem in one part does not reach "
            "everything else."),
        misunderstanding=(
            "Segmentation happens at several levels: LAN, WAN, layer 2, layer 3. "
            "What you need depends on the case. On any larger network, layer 2 "
            "segmentation protects against physical problems, loops and noise from "
            "a faulty network card taking the whole thing down. At layer 3 it "
            "separates the IP traffic and lets you allow only certain things "
            "through a firewall, so a vulnerable OT network is not exposed to "
            "everything from the office. It can be virtual, physical or both. Many "
            "say that in OT all cables and infrastructure must be separate, and "
            "that is bullshit. Some segmentation, even virtual, is better than "
            "none. On the WAN it means sites should not see each other by default. "
            "Real zero trust blocks everything and allows only what is needed, and "
            "it is a nightmare to manage."),
        skeptic_case=(
            "Full microsegmentation is a multi-year programme with a licence "
            "attached and most companies who start one do not finish. The first "
            "split is where nearly all the value is: office away from production, "
            "or servers away from workstations. One VLAN and a firewall rule. Do "
            "that, then stop and see whether you need more."),
        applies_if=["has_network"],
        applies_never_if=["has_saas_only"],
        how_to_say_no=(
            "Applicable. Network environments are separated so that critical "
            "systems are isolated from general user traffic. The segments and the "
            "controls between them are described below."),
        default_verdict="do-it-properly",
        question="Can a laptop in reception reach the machines that run production?",
        options=[
            ("yes", "Yes, it is one flat network", "do-it-properly",
             "This is the single most valuable network change available to you. One "
             "VLAN and a firewall rule between office and production. Everything "
             "else in network security is secondary to it."),
            ("no", "No, they are separated", "already-solved",
             "Then answer with the segments and what is allowed between them. That "
             "is a strong answer."),
            ("dontknow", "I would have to check", "need-one-fact",
             "Go and check. It takes ten minutes with a laptop and it is the "
             "difference between a contained incident and a total one."),
        ],
        ladder=(2,
                "Rung 4 wants all sensitive data isolated with segmentation "
                "reassessed annually, which in vendor terms means microsegmentation "
                "and a per-workload licence. The step from one flat network to a "
                "handful of segments removes most of the blast radius. Everything "
                "after that is expensive refinement.",
                [(1, "One flat network.", "do-it-properly"),
                 (2, "Critical systems on their own segment.", "already-solved"),
                 (3, "All critical systems and data separated, rules documented.", "cheap-checkbox"),
                 (4, "Microsegmentation reassessed annually.", "cheap-checkbox")]),
        costs={"a VLAN and a firewall rule": "€",
               "proper segment design across sites": "€€€",
               "microsegmentation platform": "€€€€€"},
        sec=3, chk=3,
        evidence=("The network is split up.",
                  "A network diagram showing segments and the controls between "
                  "them.",
                  "The diagram, the firewall rules enforcing it, and evidence the "
                  "rules were reviewed."),
        frameworks=["nist-csf-pr.ir-01", "iso27002-8.22", "nis2-art21", "iec62443-3-3:2013"],
        patterns=[],
        already_have=[],
    ),

    "perimeter-defence": dict(
        priority=2,
        plain_english=(
            "Can mean a physical or a virtual perimeter. Do you have a way of "
            "keeping the wrong people out of your premises and your networks."),
        misunderstanding=(
            "It can mean physical security, doors, locks, guards and a reception, or "
            "it can mean the firewall watching traffic at the network edge. The "
            "physical side is more often neglected, and it can be "
            "counter-intuitive. In a small company badges can be "
            "counter-productive, because they give an attacker credibility and they "
            "can be faked. Without badges somebody actually has to know you before "
            "they let you in."),
        skeptic_case=(
            "Next-generation firewall licences renew every year and most of the "
            "modules never get turned on. Before adding another one, check what the "
            "firewall you already own is doing. The blocking that matters, inbound "
            "denied by default and outbound restricted to what is needed, is in "
            "every firewall ever sold."),
        applies_if=["has_network", "has_office"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. Perimeter controls are in place at network boundaries and "
            "at site entrances. The specific controls are described below."),
        default_verdict="cheap-checkbox",
        question="Does your firewall block outbound traffic, or only inbound?",
        options=[
            ("both", "Both", "already-solved",
             "That puts you ahead of most. Outbound restriction is what stops "
             "malware calling home, and almost nobody does it."),
            ("inbound", "Inbound only", "cheap-checkbox",
             "Normal, and worth improving when you have a quiet week. Start by "
             "blocking outbound on the servers, which is the low-risk half."),
            ("dontknow", "No idea", "need-one-fact",
             "Somebody should look at the rules. Firewalls accumulate rules for a "
             "decade and nobody ever removes one."),
        ],
        ladder=(3,
                "Rung 4 wants the full set of perimeter tools across the entire "
                "network: intrusion prevention, web filtering, malware detection, "
                "egress control. That is a licence bundle renewed yearly. Inbound "
                "denied by default with outbound restricted on servers is where the "
                "risk actually drops.",
                [(1, "No firewall, or nobody knows the rules.", "do-it-properly"),
                 (2, "Firewall with inbound blocked.", "cheap-checkbox"),
                 (3, "Inbound and outbound controlled, rules reviewed.", "already-solved"),
                 (4, "Full tool set across the whole network.", "cheap-checkbox")]),
        costs={"use the firewall you have properly": "€",
               "reviewed rule set": "€€",
               "next-generation firewall licence bundle": "€€€"},
        sec=2, chk=3,
        evidence=("We have a firewall.",
                  "The firewall rule set with a review date.",
                  "The rules, evidence of review, and a description of physical "
                  "perimeter controls at each site."),
        frameworks=["nist-csf-pr.ir-01", "iso27002-8.20", "iso27002-7.1"],
        patterns=[],
        already_have=[],
    ),

    "secure-development": dict(
        priority=2,
        plain_english=(
            "Do you have rules for how to develop software safely."),
        misunderstanding=(
            "Web pages and Excel macros count. People answer no because they do not "
            "have a development team, while somebody in finance maintains a macro "
            "that touches customer data and somebody in marketing edits the website. "
            "That is development, and it is where the unreviewed code lives."),
        skeptic_case=(
            "If you genuinely develop nothing, say so and move on, but check first. "
            "Where there is development, the two controls worth having cost nothing: "
            "keep development away from production, and do not test with real "
            "customer data. Formal secure coding training for developers is worth it "
            "when you have enough developers for a course to make sense."),
        applies_if=["develops_software"],
        applies_never_if=["no_development"],
        how_to_say_no=(
            "Not applicable. We do not develop software in-house or through "
            "contractors. Configuration changes to purchased systems are handled "
            "through change management, described separately."),
        default_verdict="need-one-fact",
        question="Does anyone here write code, a script, or a spreadsheet macro that matters?",
        options=[
            ("no", "Nobody", "not-applicable",
             "Say so, and say that changes to bought systems go through change "
             "management. Clean answer, and it closes several questions."),
            ("informal", "Sort of, scripts and macros", "write-it-down",
             "Then write down two rules: nobody tests on live customer data, and "
             "somebody other than the author looks at it before it goes live. Free, "
             "and it covers the realistic risk."),
            ("yes", "Yes, we build software", "do-it-properly",
             "Then separate development from production, mask test data, and get "
             "the developers trained. This is the real version of the question."),
        ],
        ladder=(2,
                "Rung 4 wants secure coding practices, environment separation, "
                "duty separation between developers and production support, data "
                "masking and annual training aligned to emerging threats. In a team "
                "of three developers, separation of duties between development and "
                "production support is not achievable and pretending otherwise is "
                "dishonest. Separated environments and no live data in test is the "
                "achievable target.",
                [(1, "Development on production, live data in test.", "do-it-properly"),
                 (2, "Separate environments, no live customer data in test.", "already-solved"),
                 (3, "Code review and secure coding standards applied.", "cheap-checkbox"),
                 (4, "Full lifecycle with duty separation and annual training.", "cheap-checkbox")]),
        costs={"separate environments and mask test data": "€",
               "code review as standard practice": "€€",
               "developer security training programme": "€€€"},
        sec=2, chk=2,
        evidence=("Our developers are careful.",
                  "A written development standard covering environments and test "
                  "data.",
                  "The standard, evidence of code review, and confirmation that "
                  "test environments hold no live customer data."),
        frameworks=["nist-csf-pr.ps-06", "iso27002-8.25", "iso27002-8.31"],
        patterns=[],
        already_have=[],
    ),

    "application-security-testing": dict(
        priority=2,
        plain_english=(
            "How do you test the security of applications you develop, whether for "
            "internal use or for customers."),
        misunderstanding=(
            "One might think this applies only to companies that ship software to "
            "customers. A website, or even an Excel macro, can contain malicious "
            "code, and you should have a process to manage that. The other half is "
            "the web application firewall question, which people answer with the "
            "network firewall. Those are different things protecting different "
            "layers."),
        skeptic_case=(
            "Many companies really do not develop anything. If there is a clear "
            "policy and change management in place, and you are sure nothing is "
            "developed, this is not needed and you should say so. Where you do "
            "develop, a scan of the public website costs very little. The full "
            "static and dynamic analysis toolchain is priced for software companies, "
            "because that is who it is for."),
        applies_if=["develops_software", "has_website"],
        applies_never_if=["no_development"],
        how_to_say_no=(
            "Not applicable. We do not develop applications. Purchased software is "
            "assessed through supplier management, described separately."),
        default_verdict="need-one-fact",
        question="Do you put code in front of the internet?",
        options=[
            ("no", "No", "not-applicable",
             "Then say so plainly. Application security testing for a company with "
             "no applications is a question that arrived at the wrong address."),
            ("website", "Just a website", "cheap-checkbox",
             "An external web scan a couple of times a year is enough and it is "
             "cheap. Do not buy a testing toolchain for a brochure site."),
            ("product", "Yes, it is our product", "do-it-properly",
             "Then testing before release is not optional, and this is one of the "
             "few places on the form where the expensive answer is the right one."),
        ],
        ladder=(2,
                "Rung 4 wants static, dynamic, interactive and composition analysis "
                "plus threat modelling and runtime protection. That is a full "
                "application security programme and it is priced for software "
                "companies. Testing before release, with the findings fixed, is the "
                "level that matters for everyone else.",
                [(1, "Nothing is tested.", "do-it-properly"),
                 (2, "External scanning of what faces the internet.", "already-solved"),
                 (3, "Testing before release, findings tracked.", "cheap-checkbox"),
                 (4, "Full static, dynamic and composition analysis.", "cheap-checkbox")]),
        costs={"external web scan": "€",
               "testing before each release": "€€",
               "full application security toolchain": "€€€€"},
        sec=2, chk=2,
        evidence=("We test our software.",
                  "A recent scan or test report for the application.",
                  "Test reports across releases, plus evidence that findings were "
                  "fixed before going live."),
        frameworks=["nist-csf-pr.ps-06", "nist-csf-id.ra-01", "iso27002-8.29"],
        patterns=[],
        already_have=[],
    ),
}
