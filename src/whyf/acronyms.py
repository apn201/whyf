"""Acronym expansion for the retrieval stage only.

A questionnaire row that says "Do you have PAM?" and one that says "Do you
have privileged access management?" are the same row. The second one finds its
card. The first one does not, and the reason is dull: the letters P A M appear
nowhere in the corpus, so neither the lexical index nor the embeddings have
anything to grip. The right card never reaches the shortlist, so the model
never gets the chance to pick it.

That failure is worth naming precisely, because it looks like a comprehension
problem and it is not. The model understands PAM perfectly well. It is a
retrieval problem, and it has to be fixed here rather than by letting the cold
path write a fresh answer, which would replace a missing card with an invented
one and look more convincing while being worse.

Two rules for this table:

  Only unambiguous expansions. If an acronym means two things in a
  questionnaire, expanding it wrong is worse than not expanding it.

  Expansions are appended, never substituted. The original wording still
  carries signal and nothing here is confident enough to throw it away.
"""
import re

# Acronym -> the words a card would actually use. Keep these in the vocabulary
# of the cards, not of the standards: the point is to collide with the corpus.
GLOSSARY = {
    # access and identity
    "pam": "privileged access management admin accounts",
    "pim": "privileged identity management admin accounts",
    "rbac": "role based access control least privilege",
    "abac": "attribute based access control",
    "iam": "identity and access management accounts",
    "jit": "just in time elevation temporary admin rights",
    "polp": "least privilege",
    "scim": "account provisioning deprovisioning joiners leavers",

    # detection and response
    "siem": "security monitoring log collection alerting",
    "soar": "security monitoring automated response playbooks",
    "ueba": "user behaviour monitoring anomaly detection",
    "xdr": "endpoint detection and response monitoring",
    "mdr": "managed detection and response outsourced monitoring",
    "ndr": "network detection and response monitoring",
    "ioc": "indicators of compromise threat intelligence",
    "ttp": "attacker tactics techniques threat intelligence",
    "mttr": "mean time to respond incident response",
    "mttd": "mean time to detect security monitoring",
    "rca": "root cause analysis lessons learned",
    "csirt": "incident response team",
    "cert": "incident response team",

    # network and perimeter
    "nac": "network access control what can connect to the network",
    "waf": "web application firewall perimeter",
    "casb": "cloud access security broker shadow it",
    "ztna": "zero trust network access remote access",
    "sase": "secure access service edge network perimeter",
    "vlan": "network segmentation",
    "dmz": "network segmentation perimeter",
    "ips": "intrusion prevention perimeter monitoring",
    "ids": "intrusion detection monitoring",

    # software and supply chain
    "sbom": "software bill of materials list of components in our software",
    "sca": "software composition analysis scanning open source libraries",
    "sast": "static application security testing code scanning",
    "dast": "dynamic application security testing",
    "iast": "interactive application security testing",
    "ssdlc": "secure software development lifecycle",
    "sdlc": "software development lifecycle secure development",
    "cve": "vulnerability management known vulnerabilities patching",
    "cvss": "vulnerability severity scoring prioritisation",
    "vdp": "vulnerability disclosure reporting a flaw",
    "tprm": "third party risk management supplier assessment",
    "vrm": "vendor risk management supplier assessment",

    # privacy and legal
    "dpia": "data protection impact assessment privacy risk",
    "pia": "privacy impact assessment",
    "ropa": "record of processing activities",
    "pii": "personal data",
    "phi": "health data personal data",
    "baa": "business associate agreement health data contract",
    "aoc": "attestation of compliance certificate",
    "scc": "standard contractual clauses international transfers",
    "sccs": "standard contractual clauses international transfers",
    "tia": "transfer impact assessment international transfers",

    # continuity
    "drp": "disaster recovery plan continuity",
    "bcdr": "business continuity and disaster recovery",
    "ha": "high availability resilience",

    # operations
    "cmdb": "asset inventory configuration database",
    "iac": "infrastructure as code change management",
    "otp": "one time code multi factor authentication",
    "totp": "authenticator app multi factor authentication",
    "fido": "security key phishing resistant multi factor authentication",
    "hsm": "key management encryption keys",
    "kms": "key management encryption keys",
    "pki": "certificates key management",
    "tls": "encryption in transit",
    "vdi": "virtual desktop remote access",
}

# Written as two tokens often enough to be worth its own rule.
PHRASES = {
    r"\bci\s*/?\s*cd\b": "build pipeline deployment automation",
    r"\bpen\s*test\w*\b": "penetration testing",
    r"\bzero\s*trust\b": "least privilege network access control",
    r"\bleast\s*privilege\b": "least privilege admin rights",
}

# SOC means two unrelated things and the digit is what separates them.
# "SOC 2" is an audit report and already matches its card; a bare "SOC" is a
# security operations centre.
SOC_REPORT = re.compile(r"\bsoc\s*-?\s*[123]\b", re.I)
SOC_BARE = re.compile(r"\bsoc\b", re.I)

_WORD = {a: re.compile(r"\b{}\b".format(re.escape(a)), re.I) for a in GLOSSARY}


def expand(text):
    """Append expansions for any acronyms present. Never removes anything.

    Used for matching only. The user keeps seeing the row they pasted, and the
    tier-0 cache key is untouched, so this cannot silently merge two different
    questions into one cached answer.
    """
    if not text:
        return text
    found = [expansion for acronym, expansion in GLOSSARY.items()
             if _WORD[acronym].search(text)]

    for pattern, expansion in PHRASES.items():
        if re.search(pattern, text, re.I):
            found.append(expansion)

    if SOC_BARE.search(text) and not SOC_REPORT.search(text):
        found.append("security operations centre monitoring")

    return "{} {}".format(text, " ".join(found)) if found else text
