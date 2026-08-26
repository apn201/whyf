"""One-line glosses for every framework control the cards can cite.

Three different copyright situations, handled three different ways.

NIST CSF 2.0 is a US government publication and is public domain. Its
subcategory text is reproduced verbatim in nist-csf.yaml, straight from the
source workbook. Nothing to paraphrase.

NIS2 and GDPR are EU legislation. The text is published for public use, so the
glosses below describe what each article actually requires and quote the
deadlines, because those deadlines are the useful part and getting them
slightly wrong would be worse than useless.

ISO/IEC 27001, 27002 and IEC 62443 are sold standards. The control *numbers*
are facts and cross over freely. The titles do not, so every gloss below is
written here, describing what the control is about in plain words. If you
compare them to the standard they will not match, and that is deliberate.
"""

# ---------------------------------------------------------------------------
# EU law. Describing what the article requires, with the numbers that matter.
# ---------------------------------------------------------------------------
NIS2 = {
    "nis2-art3": (
        "Scope. Defines which organisations count as essential entities and "
        "which as important, by sector and by size. This is the article that "
        "decides whether any of the rest applies to you, and nobody will write "
        "and tell you the answer."),
    "nis2-art20": (
        "Governance. Management bodies have to approve the risk-management "
        "measures, oversee how they are implemented, and can be held personally "
        "liable for failing to. They are also required to undergo training."),
    "nis2-art21": (
        "The risk-management measures themselves. Article 21(2) lists the "
        "minimum set: risk analysis and policy, incident handling, business "
        "continuity and backup, supply chain security, security in acquisition "
        "and development, testing the effectiveness of measures, basic cyber "
        "hygiene and training, cryptography, personnel and access control, and "
        "multi-factor or continuous authentication. Most of the corpus maps "
        "here."),
    "nis2-art23": (
        "Reporting. An early warning within 24 hours of becoming aware of a "
        "significant incident, an incident notification within 72 hours, and a "
        "final report within one month. The clock starts at awareness, not at "
        "the end of your investigation, which is the part that catches people."),
}

GDPR = {
    "gdpr-art30": (
        "Records of processing activities. A written record of what personal "
        "data you process, why, who you share it with, and how long you keep "
        "it. Small organisations get a partial exemption, but it rarely "
        "survives contact with regular processing of personal data."),
    "gdpr-art32": (
        "Security of processing. Requires technical and organisational measures "
        "appropriate to the risk, and specifically names pseudonymisation and "
        "encryption, confidentiality, integrity, availability and resilience, "
        "the ability to restore access after an incident, and regular testing "
        "of the measures."),
}

# ---------------------------------------------------------------------------
# Sold standards. Numbers are facts; the words below are ours.
# ---------------------------------------------------------------------------
ISO27001 = {
    "iso27001-clause4.1": "Working out what the organisation is and what affects it",
    "iso27001-clause6": "Planning the management system and what it has to achieve",
    "iso27001-clause6.1.2": "How information security risk gets assessed",
    "iso27001-clause6.1.3": "How assessed risk gets treated, and who accepts what is left",
    "iso27001-clause7.4": "Deciding what gets communicated about security, to whom, and when",
    "iso27001-clause8.3": "Carrying out the risk treatment plan and keeping evidence",
    "iso27001-clause9.3": "Management formally reviewing whether the system is working",
}

ISO27002 = {
    "iso27002-5.1": "The written security policies, approved and published",
    "iso27002-5.2": "Who is responsible for what in security",
    "iso27002-5.3": "Splitting conflicting duties so one person cannot do it all",
    "iso27002-5.4": "Management requiring staff to actually follow the rules",
    "iso27002-5.5": "Keeping a working line to regulators and law enforcement",
    "iso27002-5.6": "Staying connected to industry and security groups",
    "iso27002-5.9": "A list of information and the things that hold it",
    "iso27002-5.10": "Rules for how people may use company information and equipment",
    "iso27002-5.12": "Sorting information by how sensitive it is",
    "iso27002-5.13": "Marking information so the classification is visible",
    "iso27002-5.14": "Rules for moving information in, out and between systems",
    "iso27002-5.15": "Deciding who is allowed to reach what",
    "iso27002-5.16": "Creating and managing identities over their whole life",
    "iso27002-5.17": "Handling passwords and the other secrets used to log in",
    "iso27002-5.18": "Granting, reviewing and removing access rights",
    "iso27002-5.19": "Managing the security risk that comes from suppliers",
    "iso27002-5.20": "Putting security requirements into supplier agreements",
    "iso27002-5.21": "Security risk further down the technology supply chain",
    "iso27002-5.22": "Watching suppliers deliver what they promised, and handling changes",
    "iso27002-5.23": "Security when using cloud services",
    "iso27002-5.24": "Planning for incidents before one happens",
    "iso27002-5.25": "Deciding which events are actually incidents",
    "iso27002-5.26": "Handling an incident once it has been declared",
    "iso27002-5.27": "Using what went wrong to stop it happening again",
    "iso27002-5.28": "Collecting and preserving evidence so it holds up later",
    "iso27002-5.29": "Keeping security working while the business is disrupted",
    "iso27002-5.30": "Technology being ready to support the continuity plan",
    "iso27002-5.31": "Identifying the legal and contractual rules that apply",
    "iso27002-5.32": "Respecting software licences and intellectual property",
    "iso27002-5.33": "Keeping records safe, findable and readable for as long as needed",
    "iso27002-5.34": "Protecting personal data",
    "iso27002-5.35": "Somebody independent checking that security works",
    "iso27002-5.36": "Checking that people actually follow the policy",
    "iso27002-6.1": "Checking people before you hire them",
    "iso27002-6.2": "Security duties written into the employment contract",
    "iso27002-6.3": "Teaching staff what to watch for, and repeating it",
    "iso27002-6.5": "What stays true after somebody leaves or changes role",
    "iso27002-6.6": "Confidentiality and non-disclosure agreements",
    "iso27002-6.7": "Rules for working away from the office",
    "iso27002-7.1": "Defining the boundary around an area that needs protecting",
    "iso27002-7.2": "Controlling who gets through the door",
    "iso27002-7.3": "Protecting the rooms and buildings themselves",
    "iso27002-7.4": "Watching the premises for people who should not be there",
    "iso27002-7.5": "Protecting against fire, water, weather and deliberate damage",
    "iso27002-7.6": "Rules for what people may do inside a secure area",
    "iso27002-7.7": "Not leaving sensitive things visible on desks or screens",
    "iso27002-7.8": "Where equipment sits and what protects it there",
    "iso27002-7.9": "Protecting equipment once it leaves the building",
    "iso27002-7.10": "Handling disks, tapes and USB storage",
    "iso27002-7.11": "Power, cooling and the other services equipment depends on",
    "iso27002-7.12": "Protecting cabling from damage and from being tapped",
    "iso27002-7.13": "Maintaining equipment without creating a hole while you do it",
    "iso27002-7.14": "Wiping equipment before it is disposed of or reused",
    "iso27002-8.1": "Protecting the machines people actually work on",
    "iso27002-8.2": "Controlling admin-level access",
    "iso27002-8.3": "Restricting access to the information itself, not just the system",
    "iso27002-8.4": "Controlling who can read and change source code",
    "iso27002-8.5": "Making the act of logging in hard to fake",
    "iso27002-8.6": "Having enough capacity, and knowing before you run out",
    "iso27002-8.7": "Stopping malicious code",
    "iso27002-8.8": "Finding and fixing known weaknesses in what you run",
    "iso27002-8.9": "Building systems to a standard configuration and keeping them there",
    "iso27002-8.12": "Stopping sensitive data leaving",
    "iso27002-8.13": "Backups, and being able to restore from them",
    "iso27002-8.14": "Spare capacity so one failure does not stop everything",
    "iso27002-8.15": "Recording what happened, and keeping the record",
    "iso27002-8.18": "Controlling the tools that bypass normal security controls",
    "iso27002-8.19": "Controlling what software gets installed on live systems",
    "iso27002-8.20": "Securing the network itself",
    "iso27002-8.21": "Security requirements for network services you buy",
    "iso27002-8.22": "Splitting the network so a problem stays in one part",
    "iso27002-8.24": "Using encryption, and looking after the keys",
    "iso27002-8.25": "Building security into how software gets made",
    "iso27002-8.26": "Deciding what an application has to do securely before building it",
    "iso27002-8.27": "Designing systems on secure principles rather than fixing later",
    "iso27002-8.29": "Testing security before something goes live",
    "iso27002-8.30": "Managing developers you do not employ",
    "iso27002-8.31": "Keeping development, test and live environments apart",
    "iso27002-8.32": "Approving changes before they are made",
}

IEC62443 = {
    "iec62443-2-1:2009": (
        "Setting up a security programme for industrial automation and control "
        "systems. The policy, organisation and process half"),
    "iec62443-3-3:2013": (
        "Technical security requirements for a control system, and the security "
        "levels those requirements are grouped into"),
}

# framework id -> (display name, url, note, {control id: gloss})
FRAMEWORKS = {
    "nis2": ("NIS2 Directive (EU) 2022/2555",
             "https://eur-lex.europa.eu/eli/dir/2022/2555/oj",
             "EU legislation, freely reproducible. Cited by article. Answer the "
             "scope question in Article 3 before treating any of the rest as an "
             "obligation; most companies asked about NIS2 are not in scope.",
             NIS2),
    "gdpr": ("GDPR (EU) 2016/679",
             "https://eur-lex.europa.eu/eli/reg/2016/679/oj",
             "EU legislation, freely reproducible. Cited by article, and only "
             "where personal data is genuinely involved.",
             GDPR),
    "iso27001": ("ISO/IEC 27001:2022",
                 "",
                 "Management system clauses. Numbers only. Every description "
                 "below is written for this repository and does not reproduce "
                 "the standard's own wording.",
                 ISO27001),
    "iso27002": ("ISO/IEC 27002:2022",
                 "",
                 "Control numbers only, for the same reason. Descriptions are "
                 "ours. If one reads oddly against the standard, that is the "
                 "point.",
                 ISO27002),
    "iec62443": ("IEC 62443",
                 "",
                 "The OT one. Reach for it when the question says ICS, PLC or "
                 "industrial. The Annex I crosswalk only distinguishes parts of "
                 "the standard, not individual requirements, so these are "
                 "coarse.",
                 IEC62443),
}
