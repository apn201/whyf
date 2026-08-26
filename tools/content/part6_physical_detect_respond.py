"""Physical security, detection, response and third parties."""

CARDS = {

    "physical-access-control": dict(
        priority=1,
        plain_english=(
            "Do you have a process for managing doors and locks."),
        misunderstanding=(
            "Not difficult, but it needs a process. Who can get which key. How do "
            "you get the key back. How do you know who went where. The failure is "
            "almost never the lock. It is that nobody knows how many keys exist to "
            "the server room, or that the code has been the same since 2018."),
        skeptic_case=(
            "An access control system with cards and a controller is a real cost per "
            "door and it is aimed at sites with a lot of doors and a lot of people. "
            "In a small office the control is a key register: who has what, signed "
            "for, returned on the way out. A page in a folder. That passes audit and "
            "it actually gets used."),
        applies_if=["has_office"],
        applies_never_if=["fully_remote"],
        how_to_say_no=(
            "Partially applicable. We operate no premises of our own. Physical "
            "security of the facilities we occupy is provided by the landlord, and "
            "our arrangements are described below."),
        default_verdict="write-it-down",
        question="How many keys are there to the room with the servers in it?",
        options=[
            ("known", "I could tell you exactly", "already-solved",
             "Then you have the control. Write the register down and note when keys "
             "get returned."),
            ("unknown", "No idea", "write-it-down",
             "Start the register. An afternoon, and it is the honest answer to "
             "several physical security questions at once."),
            ("nokeys", "We do not have our own premises", "not-applicable",
             "Say so and describe what the landlord provides. That is a complete "
             "answer and it is increasingly common."),
        ],
        ladder=(3,
                "Rung 4 wants periodic access audits at all facilities, run more "
                "often after changes. Access control systems with automated review "
                "are priced per door. A key register plus removal on the leaving "
                "date covers the risk in a building where everybody knows "
                "everybody.",
                [(1, "No idea who holds keys.", "write-it-down"),
                 (2, "A key register that is roughly current.", "cheap-checkbox"),
                 (3, "Register maintained, access removed when people leave.", "already-solved"),
                 (4, "Access control system with periodic audits.", "cheap-checkbox")]),
        costs={"a key register": "€",
               "coded locks on sensitive rooms": "€€",
               "card access system across the site": "€€€€"},
        sec=2, chk=3,
        evidence=("Only staff can get in.",
                  "A key or badge register showing who holds access to what.",
                  "The register, evidence that access is removed on leaving, and a "
                  "dated review."),
        frameworks=["nist-csf-pr.aa-06", "iso27002-7.1", "iso27002-7.2"],
        patterns=[],
        already_have=[],
    ),

    "physical-environmental-protection": dict(
        priority=2,
        plain_english=(
            "Do you protect the systems and the building against burglars, water, "
            "fire and power cuts."),
        misunderstanding=(
            "This turns up in the security questionnaire and gets sent to IT, who "
            "answer about the server room. It is a facilities question. The bit that "
            "genuinely belongs to IT is short: does the equipment survive a power "
            "cut long enough to shut down cleanly, and is the server cupboard also "
            "the room where the cleaner keeps the mop bucket."),
        skeptic_case=(
            "The questionnaire lists air conditioning, water detection, humidity "
            "sensors, raised floors, fire suppression and 48 hours of uninterruptible "
            "power. That is a data centre specification, and if your servers are in "
            "a cupboard the honest answer is that they are in a cupboard. Better "
            "still, if the systems are in the cloud, most of this question is now "
            "your provider's problem and you should say so."),
        applies_if=["has_office", "has_servers"],
        applies_never_if=["has_saas_only"],
        how_to_say_no=(
            "Partially applicable. Our production systems are hosted with cloud "
            "providers whose facility controls are covered by their certifications. "
            "On-site equipment and its protections are described below."),
        default_verdict="cheap-checkbox",
        question="Where do your servers actually live?",
        options=[
            ("cloud", "In the cloud", "not-applicable",
             "Then most of this question belongs to your provider, and citing their "
             "certification is a legitimate answer. Say what is left on site."),
            ("datacentre", "In a data centre", "already-solved",
             "Same answer, with the data centre's certifications attached."),
            ("cupboard", "In a room here", "write-it-down",
             "Then describe honestly what protects it: the lock, the smoke alarm, "
             "the UPS if there is one. An honest short answer beats claiming a "
             "specification you do not have."),
        ],
        ladder=(2,
                "Rung 4 wants the full facility specification including 48 hours of "
                "uninterruptible power at every site. That is a data centre build. "
                "Enough UPS to shut down cleanly, a smoke detector, and equipment "
                "not stored under a water pipe is the version that applies to a "
                "normal building.",
                [(1, "No protection, equipment in an open area.", "write-it-down"),
                 (2, "Locked room, smoke detection, UPS for clean shutdown.", "already-solved"),
                 (3, "Environmental monitoring and fire suppression.", "cheap-checkbox"),
                 (4, "Full facility specification with extended power.", "cheap-checkbox")]),
        costs={"lock the cupboard, add a UPS": "€€",
               "environmental monitoring": "€€€",
               "data centre specification on site": "€€€€€"},
        sec=2, chk=2,
        evidence=("The servers are in a locked room.",
                  "A description of the room and its protections, or the provider's "
                  "certification.",
                  "The description plus evidence: UPS test records, or the "
                  "provider's current certificate."),
        frameworks=["nist-csf-pr.ir-02", "iso27002-7.5", "iso27002-7.8", "iso27002-7.11"],
        patterns=["framework-inheritance"],
        already_have=[],
    ),

    "hardware-tampering": dict(
        priority=3,
        plain_english=(
            "Do you stop people physically interfering with your hardware. Servers, "
            "network kit, cabling."),
        misunderstanding=(
            "It does not really mean breaking things. It is easy to get into a "
            "server if you can stand next to it and boot from a USB stick. You can "
            "reach a protected network just by changing which port a cable is "
            "patched into. Some equipment has tamper alarms on the chassis, but in "
            "simple terms this asks whether you can stop people getting near these "
            "systems in the first place."),
        skeptic_case=(
            "Tamper-evident seals and physical inspection routines are for "
            "environments where somebody genuinely might interfere with equipment: "
            "payment terminals, unattended cabinets, remote sites. For a server in a "
            "locked room in a staffed office, the lock is the control and the "
            "inspection routine is paperwork."),
        applies_if=["has_servers", "has_office"],
        applies_never_if=["has_saas_only"],
        how_to_say_no=(
            "Partially applicable. Equipment is held in access-controlled areas "
            "rather than subject to a separate tamper inspection programme. Where "
            "equipment is unattended or remote, the controls are described below."),
        default_verdict="cheap-checkbox",
        question="Is there any of your equipment somewhere nobody would notice a stranger?",
        options=[
            ("no", "No, everything is in staffed or locked areas", "already-solved",
             "Then the access control is the answer. Say so rather than inventing "
             "an inspection routine."),
            ("yes", "Yes, remote sites or unattended cabinets", "do-it-properly",
             "Then seals and a check when somebody visits are worth it, because "
             "that is exactly the situation this control was designed for."),
        ],
        ladder=(2,
                "Rung 4 wants tamper inspection on all systems, more often after "
                "maintenance. That is a routine somebody has to run and record. "
                "Where equipment sits behind a locked door in a staffed building, "
                "the door is the control and adding an inspection log adds "
                "paperwork rather than security.",
                [(1, "Equipment accessible to anyone.", "do-it-properly"),
                 (2, "Equipment in locked or staffed areas.", "already-solved"),
                 (3, "Seals or inspection on unattended equipment.", "cheap-checkbox"),
                 (4, "Inspection programme across all systems.", "cheap-checkbox")]),
        costs={"lock the room": "€", "tamper seals on remote cabinets": "€€",
               "inspection programme with records": "€€€"},
        sec=1, chk=1,
        evidence=("Equipment is in a locked room.",
                  "A statement of where equipment sits and what controls access.",
                  "The same, plus inspection or seal records for anything "
                  "unattended."),
        frameworks=["nist-csf-pr.ir-02", "iso27002-7.8"],
        patterns=[],
        already_have=[],
    ),

    "surveillance": dict(
        priority=2,
        plain_english=(
            "Do you have CCTV or other physical monitoring, and do you record who "
            "visits."),
        misunderstanding=(
            "Cameras get bought and then nothing is ever watched or retained long "
            "enough to be useful. The visitor part is the cheaper half and the one "
            "auditors actually check: a book at reception with name, time in, time "
            "out and who they came to see. In the EU there is a second half people "
            "forget, which is that CCTV is personal data processing and needs a "
            "lawful basis, signage and a retention period."),
        skeptic_case=(
            "A camera system is a real cost and it is mostly useful after the fact. "
            "The visitor book costs nothing and prevents more than the cameras do, "
            "because somebody has to sign in and be collected. If you are choosing "
            "between them, start with the book."),
        applies_if=["has_office"],
        applies_never_if=["fully_remote"],
        how_to_say_no=(
            "Partially applicable. We operate no premises of our own. Where "
            "surveillance is provided by the landlord, it is described below, along "
            "with our visitor handling."),
        default_verdict="cheap-checkbox",
        question="If a stranger walked in today, would there be a record of it?",
        options=[
            ("book", "Yes, they would sign in", "already-solved",
             "That is the control. Say so and note the retention period."),
            ("camera", "There is a camera", "cheap-checkbox",
             "Check somebody could actually retrieve the footage and that the "
             "retention is documented. In the EU it also needs signage and a lawful "
             "basis."),
            ("neither", "No", "write-it-down",
             "Start a visitor book. It costs nothing, it is the thing auditors ask "
             "for, and it works better than a camera nobody watches."),
        ],
        ladder=(2,
                "Rung 4 wants intrusion detection and CCTV covering both offices and "
                "industrial systems, monitored. Monitored means somebody watching, "
                "which is a service contract. Recorded footage, a documented "
                "retention period and a visitor book covers what an assessment "
                "actually looks for.",
                [(1, "No record of who comes and goes.", "write-it-down"),
                 (2, "Visitor log kept, entrances covered.", "already-solved"),
                 (3, "CCTV with documented retention plus visitor log.", "cheap-checkbox"),
                 (4, "Monitored intrusion detection and CCTV.", "cheap-checkbox")]),
        costs={"a visitor book": "€", "CCTV with retention": "€€€",
               "monitored alarm and camera service": "€€€€"},
        sec=1, chk=2,
        evidence=("There are cameras.",
                  "A visitor log and a statement of camera coverage and retention.",
                  "The log, the retention policy, signage and lawful basis for "
                  "recording, and evidence footage can be retrieved."),
        frameworks=["nist-csf-de.cm-02", "iso27002-7.4", "gdpr-art32"],
        patterns=[],
        already_have=[],
    ),

    "security-awareness": dict(
        priority=1,
        plain_english=(
            "Do you train your people not to fall for things."),
        misunderstanding=(
            "Easiest done with an external service that sends fake phishing and runs "
            "automatic training, but even a regular newsletter might count. What "
            "does not count is a slide deck shown once at induction three years ago. "
            "The point is repetition, and the point of the fake phishing is not to "
            "catch people out, it is to give them a safe place to make the mistake."),
        skeptic_case=(
            "Simulated phishing platforms are sold per user per month forever and "
            "they produce a click rate that goes down and then plateaus. After that "
            "you are paying for a metric. A short session at induction, a reminder "
            "email when something relevant happens, and an easy way to report a "
            "suspicious message gets most of the benefit. The reporting button in "
            "particular is free and it is the one that actually catches attacks in "
            "progress."),
        applies_if=["has_employees"],
        applies_never_if=["sole_trader"],
        how_to_say_no=(
            "Applicable. Staff receive security awareness training at induction and "
            "at intervals thereafter. Content and frequency are described below."),
        default_verdict="cheap-checkbox",
        question="When somebody gets a suspicious email, do they know what to do with it?",
        options=[
            ("yes", "Yes, they forward it to someone", "already-solved",
             "That is the control that matters most. Make sure the route is a "
             "button rather than a memory, and say so."),
            ("no", "They would probably just delete it", "write-it-down",
             "Turn on the report button in your mail platform and tell people it "
             "exists. Free, ten minutes, and it turns your whole staff into "
             "detection."),
        ],
        ladder=(3,
                "Rung 4 wants training within 30 days of joining, refreshed "
                "annually, with specific content for groups like privileged users. "
                "That last part is a platform feature you pay for per head. "
                "Induction plus an annual refresh plus a reporting route is the "
                "level where the risk drops.",
                [(1, "No training.", "do-it-properly"),
                 (2, "Something at induction, nothing after.", "cheap-checkbox"),
                 (3, "Induction and annual refresh, reporting route in place.", "already-solved"),
                 (4, "Role-specific content and simulated phishing.", "cheap-checkbox")]),
        costs={"induction session and a report button": "€",
               "annual refresh material": "€€",
               "phishing simulation platform per user": "€€€"},
        sec=3, chk=3,
        evidence=("We tell people to be careful.",
                  "Training material and a record of who completed it and when.",
                  "The records, the refresh schedule, the reporting route, and "
                  "evidence people use it."),
        frameworks=["nist-csf-pr.at-01", "nist-csf-pr.at-02", "iso27002-6.3", "nis2-art21"],
        patterns=[],
        already_have=["email-malware-filtering"],
    ),

    "logging": dict(
        priority=1,
        plain_english=(
            "When something goes wrong, will the log files still be there."),
        misunderstanding=(
            "Normal backups are usually not considered good enough for this. Logs "
            "should be in a SIEM or something like it, so you also get value from "
            "them at normal times, and so they are still available when your network "
            "is toast. The second half is protection: if an attacker can delete the "
            "logs that show what they did, the logs were decoration."),
        skeptic_case=(
            "A SIEM is a licence plus a person, and a SIEM with nobody reading it is "
            "an expensive disk. Start with retention: make sure your cloud platform "
            "and your servers keep logs for ninety days somewhere the local admin "
            "account cannot wipe. In Microsoft 365 and Google Workspace that is a "
            "settings change. Then worry about analysis."),
        applies_if=["has_servers", "has_cloud"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. Security-relevant events are logged and retained. "
            "Retention period and protection against alteration are described "
            "below."),
        default_verdict="cheap-checkbox",
        question="If something happened three months ago, could you still see it?",
        options=[
            ("yes", "Yes", "already-solved",
             "Then say the retention period and where the logs are held. Ninety "
             "days is the number most assessments look for."),
            ("no", "No, or I do not know", "write-it-down",
             "Check the retention settings on your mail and identity platform "
             "first. It is usually a slider, and extending it is the cheapest thing "
             "on this whole page."),
        ],
        ladder=(2,
                "Rung 4 wants logs from every system, synchronised, fed to a SIEM "
                "with categorised use cases. The SIEM and the person to run it are "
                "the cost, and that is really the monitoring question. Retained "
                "for 90 days, protected from deletion, covering the systems that "
                "matter, is the logging answer.",
                [(1, "Logging off or retained for days.", "do-it-properly"),
                 (2, "Logs retained 90 days on the systems that matter.", "already-solved"),
                 (3, "Centralised and protected from alteration.", "cheap-checkbox"),
                 (4, "Everything into a SIEM with defined use cases.", "cheap-checkbox")]),
        costs={"extend retention on what you have": "€",
               "central log collection": "€€",
               "SIEM licence and storage": "€€€€"},
        sec=2, chk=3,
        evidence=("Systems keep logs.",
                  "The retention configuration and which systems it covers.",
                  "The configuration, evidence logs cannot be altered by local "
                  "administrators, and a sample retrieval."),
        frameworks=["nist-csf-de.cm-01", "nist-csf-de.ae-03", "iso27002-8.15", "iso27002-5.22"],
        patterns=["framework-inheritance"],
        already_have=["audit-logging"],
    ),

    "security-monitoring": dict(
        priority=1,
        plain_english=(
            "Is anybody actually reading the security logs."),
        misunderstanding=(
            "If you have a hundred CCTV cameras and nobody watching them, is that "
            "security? Same question. Collecting the logs is the cheap half and "
            "most companies stop there because it feels like progress. Detection "
            "only exists when a human, or a service, looks at the alert and does "
            "something."),
        skeptic_case=(
            "This is the most expensive control on the entire form and the one "
            "where the gap between the checkbox and the reality is widest. A "
            "24-hour managed detection service is a serious monthly bill. Before "
            "you go there: point the alerts from your endpoint tool and your "
            "identity platform at a mailbox somebody opens every morning. That is "
            "not a SOC, and you should not claim it is, but it is a real "
            "improvement over nobody and it costs nothing."),
        applies_if=["has_servers", "has_cloud"],
        applies_never_if=[],
        how_to_say_no=(
            "Partially applicable. We do not operate a security operations centre. "
            "Alerts from endpoint and identity platforms are reviewed by named "
            "staff, and the arrangement is described below rather than overstated."),
        default_verdict="cheap-checkbox",
        question="If your endpoint tool raised an alert at 2am, who would see it?",
        options=[
            ("service", "A monitoring service", "already-solved",
             "Then answer with who and what their hours are. This is a strong "
             "answer and you are paying for it, so use it."),
            ("morning", "Somebody, in the morning", "cheap-checkbox",
             "That is an honest answer and better than most. Say it in exactly "
             "those words rather than implying round-the-clock cover."),
            ("nobody", "Nobody", "do-it-properly",
             "Point the alerts at a mailbox that gets opened. It costs nothing and "
             "it is the difference between having a tool and having detection."),
        ],
        ladder=(2,
                "Rung 4 is a monitoring team tuning use cases against threat "
                "intelligence and investigating events, which means a service "
                "contract or a hire. Alerts arriving somewhere a human looks daily "
                "is where a small company gets most of the value. Be honest about "
                "which rung you are on. Claiming a SOC you do not have is the "
                "answer that comes back to hurt.",
                [(1, "Alerts go nowhere.", "do-it-properly"),
                 (2, "Alerts reviewed by named staff during working hours.", "already-solved"),
                 (3, "Central collection with defined alert handling.", "cheap-checkbox"),
                 (4, "Managed detection with 24-hour investigation.", "cheap-checkbox")]),
        costs={"point alerts at a monitored mailbox": "€",
               "central alerting with a handling procedure": "€€",
               "managed detection and response": "€€€€€"},
        sec=3, chk=3,
        evidence=("We have monitoring.",
                  "A statement of which alerts go where and who reviews them.",
                  "The routing, the hours covered, the handling procedure, and "
                  "examples of alerts that were investigated."),
        frameworks=["nist-csf-de.cm-01", "nist-csf-de.ae-02", "iso27002-5.25", "nis2-art21"],
        patterns=["technology-prescription"],
        already_have=["audit-logging"],
    ),

    "audits-and-pentests": dict(
        priority=1,
        plain_english=(
            "Do you regularly test whether your security controls actually work."),
        misunderstanding=(
            "Penetration tests are not rocket science and not only for big "
            "companies. It is a good idea to test once a year whether somebody in a "
            "yellow vest can walk into your site. It is also worth testing in "
            "practice that your firewalls and network controls stop an attack, and "
            "that a visitor cannot reach sensitive systems."),
        skeptic_case=(
            "Very small companies can get away without penetration testing. If you "
            "have more than ten devices on your network, or a public website, an "
            "annual test is a good idea. What is not a good idea is buying a "
            "quarterly test programme because the questionnaire mentions "
            "frequency. One good test a year, with the findings actually fixed, is "
            "worth four tests whose reports sit in a folder."),
        applies_if=["has_network"],
        applies_never_if=[],
        how_to_say_no=(
            "Partially applicable. Given our size and exposure we conduct external "
            "testing at a frequency proportionate to risk. Scope and last test date "
            "are stated below."),
        default_verdict="cheap-checkbox",
        question="Has anyone from outside ever tried to break in on purpose?",
        options=[
            ("yes", "Yes, and we fixed what they found", "already-solved",
             "That is the strong answer, and the second half is the part that "
             "counts. Attach the report and the remediation record."),
            ("report", "Yes, there is a report somewhere", "cheap-checkbox",
             "Go and check what was fixed. An old report with open findings is "
             "worse evidence than no report, because it shows you knew."),
            ("no", "No", "cheap-checkbox",
             "An external test of what faces the internet is not expensive and it "
             "tells you what everyone scanning the internet already knows about "
             "you."),
        ],
        ladder=(2,
                "Rung 4 wants annual third-party testing with critical findings "
                "fixed within two weeks, covering network and physical. Two weeks "
                "is a commitment you will miss, and a missed written commitment is "
                "worse than an honest longer one. Annual external testing with "
                "findings tracked to closure is the target.",
                [(1, "Never tested.", "cheap-checkbox"),
                 (2, "Occasional external testing, findings tracked.", "already-solved"),
                 (3, "Annual third-party testing of network and premises.", "cheap-checkbox"),
                 (4, "Annual testing with tight remediation deadlines.", "cheap-checkbox")]),
        costs={"automated external scan": "€",
               "annual external penetration test": "€€€",
               "network and physical testing programme": "€€€€"},
        sec=2, chk=3,
        evidence=("We think our controls work.",
                  "A test report with a date and a scope.",
                  "The report, the tracked remediation of its findings, and the "
                  "date of the next test."),
        frameworks=["nist-csf-id.im-02", "nist-csf-id.ra-01", "iso27002-8.29"],
        patterns=[],
        already_have=[],
    ),

    "incident-response": dict(
        priority=1,
        plain_english=(
            "Do you know what counts as an incident here, and what happens when one "
            "occurs."),
        misunderstanding=(
            "This is not difficult. A simple policy saying what the declaration "
            "criteria are and what happens next. What is an event, what is an "
            "incident, what is a major incident, what triggers the incident "
            "response team, what triggers the crisis management team. And who calls "
            "the shots. That last one is the question that wastes the first two "
            "hours of every real incident."),
        skeptic_case=(
            "Nobody needs a fifty-page incident response plan and nobody reads one "
            "during an incident anyway. Two pages: what counts, who decides, who "
            "gets called, in what order, and the phone numbers. Printed, because if "
            "it is only on the file share you cannot read it during a ransomware "
            "event."),
        applies_if=["any_business_data"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. An incident response process is defined, covering "
            "identification, investigation, containment, reporting and recovery."),
        default_verdict="write-it-down",
        question="If you found ransomware at 11pm, who makes the call to shut things down?",
        options=[
            ("named", "A specific person", "already-solved",
             "Then write the name and number down and print it. You have the hard "
             "part already."),
            ("depends", "It would depend", "do-it-properly",
             "Decide now. Authority to disconnect, and authority to spend, are the "
             "two decisions that stall real incidents. Both are free to sort out on "
             "a quiet day."),
        ],
        ladder=(2,
                "Rung 4 wants the plan covering identification, triage, "
                "containment, eradication, reporting and recovery, executed with "
                "third parties. Those stages are worth listing. The programme "
                "around them is not, for a company of this size. Two pages, "
                "printed, with the decision authority named.",
                [(1, "No plan.", "do-it-properly"),
                 (2, "Two pages, decision authority named, contacts printed.", "already-solved"),
                 (3, "Full process covering all stages, reviewed.", "cheap-checkbox"),
                 (4, "Executed with third parties, all stages evidenced.", "cheap-checkbox")]),
        costs={"two pages and a printed contact list": "€",
               "a full process document": "€€",
               "consultant-built response programme": "€€€€"},
        sec=3, chk=3,
        evidence=("We would deal with it.",
                  "A written incident response process naming who decides.",
                  "The process, the contact list, evidence it has been used or "
                  "exercised, and the review date."),
        frameworks=["nist-csf-rs.ma-01", "nist-csf-rs.ma-02", "iso27002-5.26", "nis2-art21"],
        patterns=["documentation-only"],
        already_have=[],
    ),

    "incident-response-testing": dict(
        priority=2,
        plain_english=(
            "Assuming you have an incident response team and a policy, how often do "
            "they practise."),
        misunderstanding=(
            "It does not need to be a fancy red team exercise. A tabletop once a "
            "year is a good starting point. Nothing technical. Just a scenario and a "
            "discussion of who would have done what. The value is almost entirely in "
            "discovering that two people thought the other one was going to call the "
            "insurer."),
        skeptic_case=(
            "A facilitated exercise with an external provider is a real cost and it "
            "is worth it once, to see how it is done. After that you can run it "
            "yourself over lunch. What you must not do is skip it because the "
            "external version looks expensive. The unrehearsed plan is the one that "
            "fails."),
        applies_if=["any_business_data"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. The incident response process is exercised and the "
            "outcomes recorded. Frequency and format are described below."),
        default_verdict="write-it-down",
        question="Have you ever walked through an incident with the people who would handle it?",
        options=[
            ("yes", "Yes", "already-solved",
             "Then attach the date and what came out of it. The findings are the "
             "evidence, more than the exercise."),
            ("no", "No", "write-it-down",
             "Book two hours. Pick a scenario, sit the relevant people down, and "
             "ask what happens next at each step. You will find three broken things "
             "before the coffee gets cold."),
        ],
        ladder=(2,
                "Rung 4 wants tabletops based on emerging threats, involving senior "
                "management and every stakeholder in the plan, with documented "
                "improvement actions. Senior management being there is worth "
                "insisting on. The rest is a programme. One exercise a year, "
                "written up, is what actually finds the gaps.",
                [(1, "Never practised.", "write-it-down"),
                 (2, "One tabletop a year, written up.", "already-solved"),
                 (3, "Exercises involving management, actions tracked.", "cheap-checkbox"),
                 (4, "Threat-driven programme with full stakeholder involvement.", "cheap-checkbox")]),
        costs={"two hours around a table": "€",
               "facilitated exercise": "€€€",
               "annual programme with external facilitation": "€€€€"},
        sec=3, chk=3,
        evidence=("We have a plan.",
                  "A dated record of an exercise and who attended.",
                  "The record, what did not work, and the changes made afterwards."),
        frameworks=["nist-csf-id.im-02", "nist-csf-rs.ma-01", "iso27002-5.24"],
        patterns=["outcome-as-process"],
        already_have=[],
    ),

    "incident-reporting": dict(
        priority=1,
        plain_english=(
            "Do you have rules on how and when to report incidents, inside the "
            "company and outside it."),
        misunderstanding=(
            "GDPR and NIS2 both come with tight clocks. Under GDPR it is 72 hours "
            "to the supervisory authority for a personal data breach. NIS2 adds an "
            "early warning inside 24 hours for entities in scope. The clock starts "
            "when you become aware, not when you finish investigating, and that is "
            "the part that catches people out."),
        skeptic_case=(
            "There is nothing to buy. The whole control is knowing in advance who "
            "reports, to whom, and by when, so nobody spends the first day of an "
            "incident looking up the rules. Whether the clocks apply to you at all "
            "depends on the NIS2 scope question, so answer that one first."),
        applies_if=["processes_personal_data", "operates_in_eu"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. Reporting obligations and timeframes are identified and "
            "assigned. Whether the NIS2 timeframes apply depends on our scope "
            "assessment, which is stated separately."),
        default_verdict="write-it-down",
        question="Do you know who you would have to tell, and how fast?",
        options=[
            ("yes", "Yes, it is written down", "already-solved",
             "Then answer with the timeframes and who owns the notification. Good "
             "position to be in."),
            ("no", "Not really", "write-it-down",
             "One page: which regulator, which customers by contract, which "
             "insurer, and the deadline for each. Free, and it removes the worst "
             "day-one confusion there is."),
        ],
        ladder=(2,
                "Rung 4 wants reporting integrated with third parties and evidenced "
                "across every stage. The step that matters is much earlier: knowing "
                "the deadlines and who owns them before an incident, rather than "
                "reading the regulation on the day.",
                [(1, "Nobody knows the obligations.", "write-it-down"),
                 (2, "Obligations and deadlines written down with an owner.", "already-solved"),
                 (3, "Templates prepared and contacts confirmed.", "cheap-checkbox"),
                 (4, "Fully integrated reporting including third parties.", "cheap-checkbox")]),
        costs={"one page listing obligations and deadlines": "€",
               "prepared templates and confirmed contacts": "€€",
               "legal review of the notification process": "€€€"},
        sec=1, chk=3,
        evidence=("We would tell the right people.",
                  "A written list of reporting obligations with timeframes and an "
                  "owner.",
                  "The list, prepared notification templates, and confirmed "
                  "regulator and customer contacts."),
        frameworks=["nist-csf-rs.co-02", "nist-csf-rc.co-04", "nis2-art23", "gdpr-art32"],
        patterns=[],
        already_have=[],
    ),

    "ir-retainer": dict(
        priority=2,
        plain_english=(
            "A retainer is a contract with an incident response company signed up "
            "front, before anything happens."),
        misunderstanding=(
            "When something happens it is too late to go looking for a vendor and "
            "get approvals. A retainer means it is all handled beforehand, so when "
            "an incident happens you get help immediately. They differ: in some you "
            "pay up front, in others it is just a contract with your background "
            "details already lodged."),
        skeptic_case=(
            "The paid-up-front kind is a real annual cost for something you hope "
            "never to use, and for a small company that money often does more good "
            "spent on backups. But the zero-fee version, where you sign the contract "
            "and lodge your details in advance and only pay if you call, is close to "
            "free and there is no reason not to have one. Many cyber insurance "
            "policies include access to a panel, so check before buying separately."),
        applies_if=["any_business_data"],
        applies_never_if=[],
        how_to_say_no=(
            "Partially applicable. We do not hold a paid incident response "
            "retainer. Arrangements for obtaining specialist support during an "
            "incident are described below."),
        default_verdict="cheap-checkbox",
        question="Who would you call at 2am if you found ransomware?",
        options=[
            ("named", "I have a number", "already-solved",
             "Then say who, and whether there is a contract behind it. A number "
             "with a signed contract behind it is the strong answer."),
            ("insurer", "The insurer's panel", "already-solved",
             "That counts and it is already paid for. Check the number is somewhere "
             "you can reach it when the network is down."),
            ("nobody", "I would start searching", "write-it-down",
             "Sign a zero-fee retainer, or confirm your insurer's panel. Either "
             "takes an afternoon and neither costs money up front."),
        ],
        ladder=(2,
                "Rung 4 wants a full panel lined up: breach coach, legal, public "
                "relations, forensics, notification. That is what an insurer "
                "provides, which is why buying it separately is usually paying "
                "twice. A contract in place and the number printed is the control.",
                [(1, "No arrangement.", "write-it-down"),
                 (2, "A contract or insurer panel, number available offline.", "already-solved"),
                 (3, "Retainer with agreed response times.", "cheap-checkbox"),
                 (4, "Full panel across legal, PR and forensics.", "cheap-checkbox")]),
        costs={"zero-fee retainer or insurer panel": "€",
               "paid retainer with response times": "€€€",
               "full panel on retainer": "€€€€"},
        sec=2, chk=2,
        evidence=("We would find somebody.",
                  "A signed retainer or a documented insurer panel contact.",
                  "The contract, agreed response times, and evidence the contact "
                  "details are available offline."),
        frameworks=["nist-csf-rs.ma-01", "nist-csf-gv.sc-08"],
        patterns=[],
        already_have=[],
    ),

    "crisis-management": dict(
        priority=1,
        plain_english=(
            "Do you have a crisis management plan and a team. The people who sit in "
            "a war room when something bad happens. Not limited to cyber."),
        misunderstanding=(
            "Some think it is the same as the incident response team and only about "
            "cyber. It is usually the non-IT extension of incident response. When "
            "there is a fire, or ransomware, and the plant is out for a week: who "
            "informs customers, who informs the authorities, how do you reroute "
            "logistics. All the non-IT parts, and of course IT as well, belong to "
            "crisis management."),
        skeptic_case=(
            "In a small company the crisis team is the management team and writing "
            "that down takes ten minutes. What is worth the extra effort is the "
            "contact directory and the deputy for each role, because crises have a "
            "habit of starting while somebody is on a plane. The full crisis "
            "management framework with exercise programmes is aimed at "
            "organisations where the crisis team does not already eat lunch "
            "together."),
        applies_if=["has_employees"],
        applies_never_if=["sole_trader"],
        how_to_say_no=(
            "Applicable. Crisis roles, contacts and responsibilities are defined. "
            "Given our size the crisis team is the management team, which is stated "
            "explicitly."),
        default_verdict="write-it-down",
        question="If the plant were down for a week, who tells the customers?",
        options=[
            ("named", "A specific person", "already-solved",
             "Then write down the whole set: who tells customers, who tells "
             "authorities, who talks to press, and their deputies. One page."),
            ("unclear", "We would work it out", "write-it-down",
             "Work it out now instead. The list of who calls whom is the entire "
             "deliverable, and it is ten minutes of thinking on a good day versus "
             "two hours of confusion on a bad one."),
        ],
        ladder=(2,
                "Rung 4 wants a crisis policy, a role directory, defined actions per "
                "role, awareness sessions and periodic exercises, including for "
                "industrial systems. The directory and the defined actions are worth "
                "having. The exercise programme is where a small company generates "
                "documents instead of readiness.",
                [(1, "No plan, no named team.", "write-it-down"),
                 (2, "Roles and contacts written down with deputies.", "already-solved"),
                 (3, "Defined actions per role, awareness sessions held.", "cheap-checkbox"),
                 (4, "Full programme with periodic exercises.", "cheap-checkbox")]),
        costs={"one page of roles and contacts": "€",
               "defined actions and a directory": "€€",
               "full crisis programme with exercises": "€€€€"},
        sec=2, chk=3,
        evidence=("Management would handle it.",
                  "A crisis role and contact directory with deputies.",
                  "The directory, the actions per role, and a record of the last "
                  "exercise or real activation."),
        frameworks=["nist-csf-rs.co-02", "nist-csf-rc.co-03", "iso27002-5.29"],
        patterns=["documentation-only"],
        already_have=[],
    ),

    "ics-emergency-modes": dict(
        priority=2,
        plain_english=(
            "Do the production systems, the pumps and the motors, have controls that "
            "stop them before somebody gets hurt."),
        misunderstanding=(
            "It is not really IT related. A single emergency stop button counts. "
            "More complex systems have more complex controls, and degraded mode "
            "means the plant can keep running in a reduced, safe state rather than "
            "only having on and off. It appears in a cyber questionnaire because "
            "ransomware on the control network and a mechanical fault produce the "
            "same question: can you stop safely."),
        skeptic_case=(
            "If you have no machinery, this does not apply and you say so. Where you "
            "do have machinery, safety systems are almost certainly already there "
            "because machinery safety law required them long before anyone asked a "
            "cyber question. The answer is usually already in your machinery safety "
            "documentation, and it belongs to your safety engineer rather than to "
            "IT."),
        applies_if=["has_ot"],
        applies_never_if=["has_ot_none"],
        how_to_say_no=(
            "Not applicable. We operate no industrial machinery or process control "
            "systems."),
        default_verdict="not-applicable",
        question="Do you have machinery that could hurt somebody?",
        options=[
            ("no", "No machinery", "not-applicable",
             "Say so. This is a plant question and it reaches a lot of offices."),
            ("yes", "Yes", "already-solved",
             "Then the answer already exists in your machinery safety "
             "documentation. Get it from the safety engineer and reference it "
             "rather than writing something new."),
        ],
        ladder=None,
        costs={"reference existing machinery safety documentation": "€",
               "degraded mode design for the process": "€€€€"},
        sec=2, chk=2,
        evidence=("The machines have stop buttons.",
                  "The machinery safety documentation covering emergency stop and "
                  "safe states.",
                  "The documentation, plus evidence the safe states have been "
                  "tested and cover loss of the control system."),
        frameworks=["nist-csf-rs.mi-02", "iec62443-3-3:2013"],
        patterns=[],
        already_have=[],
    ),

    "third-party-risk": dict(
        priority=1,
        plain_english=(
            "Do you assess the risk coming from your suppliers and other third "
            "parties."),
        misunderstanding=(
            "This is the question you are currently answering, pointed back at you. "
            "The company sending you this questionnaire is doing third-party risk "
            "management, and now they want to know whether you do it to your own "
            "suppliers. The mistake is treating it as a paperwork exercise in both "
            "directions, when the actual risk is concentrated in the two or three "
            "suppliers who could stop your business or leak your data."),
        skeptic_case=(
            "Do not build the thing that is currently annoying you. Sending a "
            "sixty-question form to every supplier produces a filing cabinet and no "
            "safety. Take the list of suppliers who hold your data or can log in, "
            "which should be under ten names, and for each one ask what happens if "
            "they fail and what happens if they are breached. Write the answers "
            "down. That is a defensible third-party risk process."),
        applies_if=["has_suppliers"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. Suppliers with access to our systems or data are assessed "
            "before engagement and reviewed. The approach is proportionate to the "
            "criticality of the supplier and is described below."),
        default_verdict="write-it-down",
        question="Which supplier would hurt most if they were breached tomorrow?",
        options=[
            ("named", "I can name them", "write-it-down",
             "Then write down what you would do about it, for each of the top few. "
             "That short document is your third-party risk process and it beats a "
             "questionnaire programme."),
            ("unsure", "I would have to think", "do-it-properly",
             "Start with the supplier list and work out which ones hold data or "
             "have access. Nearly every large breach of a small company came in "
             "through a supplier."),
        ],
        ladder=(2,
                "Rung 4 wants all third parties assessed and reassessed as "
                "agreements change, with thresholds, escalation and financial "
                "modelling. That is a supplier risk function with a platform. "
                "Assessing the handful that hold your data or can log in, and "
                "reviewing them yearly, gets the same protection.",
                [(1, "Nobody assesses suppliers.", "do-it-properly"),
                 (2, "The critical few assessed and written down.", "already-solved"),
                 (3, "All suppliers assessed, reviewed on change.", "cheap-checkbox"),
                 (4, "Formal methodology with thresholds and modelling.", "cheap-checkbox")]),
        costs={"assess the critical few yourself": "€",
               "yearly review with documented criteria": "€€",
               "supplier risk platform and programme": "€€€€"},
        sec=3, chk=3,
        evidence=("We use reputable suppliers.",
                  "A written assessment of the suppliers who hold data or have "
                  "access.",
                  "The assessments, dated, with criticality, what was checked, and "
                  "the review schedule."),
        frameworks=["nist-csf-gv.sc-04", "nist-csf-gv.sc-07", "iso27002-5.19", "nis2-art21"],
        patterns=["certificate-shortcut"],
        already_have=[],
    ),

    "third-party-contracts": dict(
        priority=1,
        plain_english=(
            "Do your third-party contracts say anything about security and privacy."),
        misunderstanding=(
            "Required under NIS2 for entities in scope, and under GDPR wherever a "
            "supplier processes personal data for you. And it is the reason these "
            "questionnaires exist in the first place: somebody put a clause in a "
            "contract, and the clause has to be evidenced. The escrow question in "
            "the same section is a different animal, and it is nearly always "
            "answered no for good reason."),
        skeptic_case=(
            "Do not renegotiate every contract you have. Add standard security and "
            "data protection terms to your template so new agreements carry them, "
            "and only reopen an existing contract when it is up for renewal or when "
            "the supplier is one of the critical few. Software escrow in particular "
            "is expensive, rarely invoked, and usually delivers source code nobody "
            "can build."),
        applies_if=["has_suppliers"],
        applies_never_if=[],
        how_to_say_no=(
            "Applicable. Security and data protection requirements are included in "
            "contracts with suppliers who hold our data or access our systems. "
            "Legacy agreements are updated at renewal."),
        default_verdict="write-it-down",
        question="Does your standard contract template mention security at all?",
        options=[
            ("yes", "Yes", "already-solved",
             "Then answer with what it covers and how legacy contracts get updated. "
             "The legacy part is what gets asked next."),
            ("no", "No", "write-it-down",
             "Add a clause to the template. One conversation with a lawyer, and "
             "every new agreement carries it from then on. Do not reopen the old "
             "ones."),
        ],
        ladder=(2,
                "Rung 4 wants every third party contractually bound to service "
                "levels and indemnities, updated as services change. Getting a "
                "small supplier to accept an indemnity is a negotiation you will "
                "usually lose. Standard terms in your template, applied at renewal, "
                "is the version that actually happens.",
                [(1, "Contracts say nothing about security.", "write-it-down"),
                 (2, "Standard terms in the template, applied to new agreements.", "already-solved"),
                 (3, "Critical suppliers under specific security terms.", "cheap-checkbox"),
                 (4, "All suppliers bound to service levels and indemnities.", "cheap-checkbox")]),
        costs={"add a clause to the template": "€",
               "specific terms for critical suppliers": "€€",
               "renegotiate the whole supplier base": "€€€€"},
        sec=1, chk=3,
        evidence=("Our contracts are standard.",
                  "The standard security and data protection clauses in the "
                  "contract template.",
                  "The clauses, plus signed examples from critical suppliers and "
                  "the plan for updating legacy agreements."),
        frameworks=["nist-csf-gv.sc-05", "iso27002-5.20", "nis2-art21"],
        patterns=["documentation-only"],
        already_have=[],
    ),

    "cloud-provider-assurance": dict(
        priority=1,
        plain_english=(
            "How do you satisfy yourself that your cloud providers are reliable."),
        misunderstanding=(
            "This is part of normal vendor management. Saying that Google makes no "
            "special contracts is not an excuse. You should have a way of deciding "
            "how much risk a provider represents and then checking whether that is "
            "acceptable. The other half people miss is the shared responsibility "
            "line: the provider secures the platform, you secure what you put on it, "
            "and a lot of assumed protection sits on your side of that line."),
        skeptic_case=(
            "You are not going to audit Microsoft and they are not going to answer "
            "your questionnaire. What you do instead is read the certification "
            "report they already publish, note the date, and write down which parts "
            "of the responsibility model are yours. That is a complete and honest "
            "answer, it costs an afternoon, and it is what every large company "
            "does too."),
        applies_if=["has_cloud"],
        applies_never_if=["no_cloud"],
        how_to_say_no=(
            "Applicable. Cloud providers are assessed using their published "
            "certifications and audit reports, and the division of responsibility is "
            "documented."),
        default_verdict="write-it-down",
        question="Do you know which parts of cloud security are yours rather than theirs?",
        options=[
            ("yes", "Yes", "already-solved",
             "Then write it down per provider. The shared responsibility split is "
             "the whole answer to this question and almost nobody documents it."),
            ("no", "Not clearly", "write-it-down",
             "Get the provider's shared responsibility model and mark your side. An "
             "afternoon, and it will show you two or three things you assumed were "
             "covered and are not."),
        ],
        ladder=(2,
                "Rung 4 wants regular risk assessments of every cloud provider by "
                "solution type, with continuity and incident response evidence from "
                "each. For hyperscalers that evidence is their published audit "
                "report, so the work is reading and recording rather than "
                "assessing. Collecting the reports and documenting your side of the "
                "line is the real control.",
                [(1, "Nobody has looked at provider assurance.", "write-it-down"),
                 (2, "Certifications collected, responsibility split documented.", "already-solved"),
                 (3, "Providers rated by criticality and reviewed yearly.", "cheap-checkbox"),
                 (4, "Formal assessment per solution type with evidence.", "cheap-checkbox")]),
        costs={"collect the certifications and read them": "€",
               "documented responsibility model per provider": "€€",
               "formal cloud assurance programme": "€€€"},
        sec=2, chk=3,
        evidence=("We use major providers.",
                  "Current certification reports for the main providers.",
                  "The reports with their dates, plus a written statement of which "
                  "controls are yours under each provider's responsibility model."),
        frameworks=["nist-csf-gv.sc-07", "nist-csf-id.am-04", "iso27002-5.23"],
        patterns=["certificate-shortcut"],
        already_have=[],
    ),
}
