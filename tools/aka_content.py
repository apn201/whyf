"""Retrieval vocabulary. Not prose, and nobody reads it.

A card is written to be understood by somebody who has never heard the term.
A questionnaire row is written by somebody who has heard nothing else. Those
are different vocabularies, and where they fail to overlap the card becomes
unreachable no matter how good it is.

The measured example: a row asking about "former employees retaining access"
never reached a card titled "Joiners, movers and leavers", because the words
"former", "retain" and "revoke" appear nowhere on it. The classifier was never
shown the card, so it declined. That looks like the tool not knowing the
answer. It is the tool not finding an answer it already had.

Rules, so this stays a search index and does not turn into a second corpus:

  Written from scratch, in the vocabulary of standards and questionnaires.
  Nothing here is lifted from the source questionnaires, which do not ship.

  Terms only, not sentences. This is matched against, never displayed.

  Add a phrase when a real row failed to find the card. Not speculatively.
"""

AKA = {
    # -- access and identity ------------------------------------------------
    "identity-lifecycle": [
        "former employees retaining access", "terminated staff accounts",
        "revoke access on termination", "offboarding deprovisioning",
        "onboarding provisioning", "access removed when someone leaves",
        "role change access rights updated", "dormant inactive accounts",
        "orphaned accounts", "starters movers leavers",
    ],
    "least-privilege": [
        "need to know basis", "minimum necessary access",
        "role based access control", "access granted on business need",
        "excessive permissions", "access rights reviewed periodically",
        "user access recertification", "entitlement review",
    ],
    "privileged-accounts": [
        "privileged access management", "administrative accounts",
        "elevated rights", "domain admin", "root access",
        "superuser accounts", "privileged session recording",
        "break glass emergency access",
    ],
    "mfa": [
        "two factor authentication", "multi factor authentication",
        "second factor", "strong authentication",
        "authenticator app hardware token", "step up authentication",
        "administrative accounts protected with mfa",
    ],
    "shared-accounts": [
        "generic accounts", "service accounts", "functional accounts",
        "accounts used by more than one person", "unique user identification",
    ],
    "local-admin-rights": [
        "local administrator privileges", "workstation admin rights",
        "users running as administrator", "privilege elevation on endpoints",
    ],

    # -- policy and people --------------------------------------------------
    "acceptable-use": [
        "prohibited from bypassing security controls",
        "circumventing or disabling security tools", "misuse of company systems",
        "acceptable use of information technology", "rules of behaviour",
        "personal use of company equipment", "prohibited activities",
        "users must not install unapproved software",
        "sanctions for violations of the policy",
    ],
    "security-policy": [
        "information security policy", "formal documented policy",
        "policy approved by management", "policy reviewed annually",
        "policy communicated to staff", "policy framework and standards",
    ],
    "security-awareness": [
        "security training programme", "phishing simulation",
        "annual mandatory training", "user education",
        "training records and completion rates",
    ],
    "personnel-security": [
        "background screening", "pre employment checks",
        "criminal record check", "reference verification",
        "confidentiality agreements signed", "vetting of contractors",
    ],
    "disciplinary-process": [
        "sanctions for policy violations", "enforcement action",
        "consequences of non compliance", "formal disciplinary procedure",
    ],
    "shadow-it": [
        "unapproved cloud services", "unsanctioned SaaS",
        "uploading company files to free online tools",
        "online file converter or compressor", "web based tools staff use",
        "approval route for new software", "register of cloud services",
    ],
    "ai-governance": [
        "artificial intelligence tools", "generative ai usage policy",
        "large language model", "chatbot",
        "pasting company data into ai tools", "approved ai tools",
    ],
    "antivirus-exclusions": [
        "antivirus exclusions documented", "scanning exclusions approved",
        "systems where antivirus cannot be installed",
        "endpoint protection disabled exception",
        "compensating controls for unprotected systems",
    ],

    "risk-acceptance": [
        "documented exceptions to policy", "policy waivers",
        "compensating controls for exceptions", "time bound exception approval",
        "residual risk accepted and signed off", "deviation approval",
    ],

    # -- data ---------------------------------------------------------------
    "data-classification": [
        "information classification scheme", "confidential internal public",
        "handling rules by sensitivity", "labelling of information",
        "data owner assigned",
    ],
    "encryption": [
        "encryption in transit", "tls protocols", "cryptographic controls",
        "key management", "data encrypted at rest and in transit",
    ],
    "secure-disposal": [
        "secure deletion of data", "media sanitisation",
        "certificate of destruction", "return or destroy customer data",
        "data deleted at end of contract",
    ],
    "data-retention": [
        "retention schedule", "how long data is kept",
        "deletion after retention period", "legal hold",
    ],
    "dlp": [
        "data loss prevention", "preventing exfiltration",
        "secure file transfer for sensitive data",
        "controls on external sharing",
    ],

    # -- operations ---------------------------------------------------------
    "patch-management": [
        "security patches applied", "patching cadence and timelines",
        "emergency out of band patching", "expedited fixes for critical flaws",
        "end of life unsupported software",
    ],
    "vulnerability-management": [
        "vulnerability scanning", "authenticated credentialed scanning",
        "remediation timeframes by severity", "cve cvss prioritisation",
        "vulnerabilities in third party components",
        "tracking findings to closure",
    ],
    "security-monitoring": [
        "security information and event management",
        "security operations centre", "alerts investigated",
        "24x7 monitoring", "detection of suspicious activity",
    ],
    "logging": [
        "audit logs retained", "log retention period",
        "logs of access to sensitive systems", "tamper resistant logs",
        "administrative activity logged",
    ],
    "backups": [
        "backup schedule and frequency", "restore testing",
        "recovery of data verified", "backup coverage of critical systems",
    ],
    "change-management": [
        "change control process", "changes approved before deployment",
        "emergency change procedure", "segregation of duties in changes",
    ],
    "asset-inventory": [
        "inventory of assets", "configuration management database",
        "unknown or unmanaged devices", "hardware and software inventory",
        "ownership assigned to assets",
    ],

    # -- supplier and compliance --------------------------------------------
    "third-party-risk": [
        "supplier due diligence", "vendor risk assessment",
        "criticality tiering of suppliers", "fourth party subcontractor risk",
    ],
    "third-party-contracts": [
        "security requirements in contracts",
        "incident notification obligations on suppliers",
        "right to audit clause", "contractual security schedule",
    ],
    "supplier-monitoring": [
        "ongoing supplier oversight", "reassessment of critical suppliers",
        "monitoring supplier security posture",
    ],
    "certification": [
        "iso 27001 certified", "scope of certification",
        "statement of applicability", "certificate covers services purchased",
    ],
    "audits-and-pentests": [
        "penetration testing", "independent security assessment",
        "red team exercise", "findings tracked to remediation",
        "executive summary of test results",
    ],
    "incident-response": [
        "incident response plan", "containment and eradication",
        "compromised supplier response", "escalation procedures",
        "post incident review lessons learned",
    ],
    "incident-reporting": [
        "notification timeframes", "reporting to customers and regulators",
        "who is authorised to communicate externally",
        "breach notification obligations",
    ],
}
