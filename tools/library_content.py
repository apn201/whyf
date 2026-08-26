"""Content for the patterns and already-have libraries.

Licence tiers move. Everything in `applies_to` below says where to look rather
than promising what somebody's specific subscription includes, and every card
carries a caveat saying when the claim is wrong. That is deliberate: a tool
that tells a company a control is already on when it is not is worse than a
tool that says nothing.
"""

PATTERNS = {

    "documentation-only": dict(
        name="The question asks for a document, not an outcome",
        tell=("Anything that asks whether a written policy, procedure or plan "
              "exists. The verb is has or is established, never works or was "
              "tested."),
        what_it_means=("Somebody wants evidence that a decision was made on "
                       "purpose rather than by accident. They are not asking "
                       "whether the thing is any good. Nobody will read the "
                       "document; they will note that it has a date and an "
                       "owner."),
        what_to_do=("Write the document. Keep it short and true. An afternoon "
                    "of work closes the question permanently, and the "
                    "questions underneath it usually close too, because most "
                    "policy questions are the same policy asked five ways."),
        trap=("Buying a policy pack. You get sixty pages describing controls "
              "you do not have, which is worse than having nothing: now there "
              "is written evidence that you knew what you were supposed to be "
              "doing and were not doing it."),
        signals=["a formal policy", "is documented", "has been established",
                 "documented and implemented", "policy is in place",
                 "formalized", "formalised"],
        concepts=["security-policy", "acceptable-use", "bcp", "incident-response",
                  "change-management", "crisis-management"],
    ),

    "technology-prescription": dict(
        name="The question names a product category instead of a risk",
        tell=("The question asks whether a solution or a tool is implemented. "
              "It names the shelf in the shop rather than the problem you were "
              "trying to solve."),
        what_it_means=("Whoever wrote the question had a product in mind, "
                       "usually because their own company bought one. What "
                       "they are worried about is the underlying risk, and "
                       "they will accept any credible answer that addresses "
                       "it."),
        what_to_do=("Answer the risk, not the shelf. Say what you do about the "
                    "underlying problem, and check whether the platform you "
                    "already pay for includes a version of the product. It "
                    "usually does, switched off."),
        trap=("Buying the product category because the question named it. This "
              "is how a company of thirty ends up with a data loss prevention "
              "platform, a threat intelligence feed and a security operations "
              "contract, none of which anyone has time to run."),
        signals=["a solution is implemented", "do you utilize", "do you deploy",
                 "tool is in place", "do you use a", "solution is in place"],
        concepts=["dlp", "threat-intelligence", "security-monitoring",
                  "application-allowlisting", "dns-filtering", "ddos-protection"],
    ),

    "outcome-as-process": dict(
        name="The question asks whether you decided, not whether you bought",
        tell=("It asks whether a number, a level or an objective has been "
              "specified, defined or determined. The thing it asks about is "
              "already true of you; the question is whether anyone chose it."),
        what_it_means=("You have an answer whether you like it or not. Your "
                       "backups run nightly, so your tolerable data loss is "
                       "already 24 hours. The question is whether that was a "
                       "decision or an accident."),
        what_to_do=("Say the number. Write it down first so it becomes a "
                    "decision, then answer with it. This is usually the "
                    "cheapest question on the whole form and people mistake it "
                    "for the most expensive."),
        trap=("Reading it as a demand for the best possible number and pricing "
              "the technology to deliver that. The question does not ask for a "
              "good number. It asks for a chosen one."),
        signals=["has been specified", "has been defined", "is determined",
                 "maximum accepted", "objectives are defined", "has been established"],
        concepts=["rpo", "bia", "data-classification", "patch-management",
                  "continuity-testing", "ics-inventory"],
    ),

    "framework-inheritance": dict(
        name="You already have it and nobody told you",
        tell=("A PROTECT-section question about something a mail, identity or "
              "device platform does by default. Malware filtering, screen lock, "
              "password storage, encryption at rest."),
        what_it_means=("The control exists. It came with the subscription, it "
                       "was configured by the vendor, and nobody at your end "
                       "ever had to think about it. The asker assumes you "
                       "bought something."),
        what_to_do=("Go and find the setting, screenshot it, and answer yes "
                    "with evidence. See the already-have cards for where each "
                    "one lives. This is the single fastest way to shorten a "
                    "questionnaire."),
        trap=("Answering no because nobody here implemented it, and then "
              "buying a product to close a gap that was never open. Or the "
              "opposite trap: answering yes without checking, on a "
              "subscription tier where it is genuinely not included."),
        signals=["protected against malware", "secured against spam",
                 "passwords are stored", "automatically lock", "encrypted at rest",
                 "backups are encrypted"],
        concepts=["email-security", "screen-lock", "passwords", "encryption",
                  "full-disk-encryption", "endpoint-protection", "logging"],
    ),

    "certificate-shortcut": dict(
        name="One certificate closes a whole section",
        tell=("A block of questions covering ground that a recognised "
              "certification already audits, usually preceded or followed by a "
              "question asking which certifications you hold."),
        what_it_means=("The asker has a process that accepts certificates in "
                       "place of answers. They would rather read one "
                       "certificate than forty of your paragraphs, and their "
                       "own form usually says so somewhere."),
        what_to_do=("If you hold one, name it and attach the scope statement, "
                    "then check whether the rest of the section can be "
                    "answered by reference. If you do not hold one, this is "
                    "worth a commercial calculation rather than a security "
                    "one: count how many of these questionnaires you filled in "
                    "last year."),
        trap=("Getting certified because a questionnaire mentioned it. "
              "Certification is expensive and it consumes the same people who "
              "would otherwise be fixing things. It is a sales cost, and it "
              "should be justified as one."),
        signals=["certification", "iso/iec 27001", "soc 2", "cyber essentials",
                 "certification report", "attach your certificate"],
        concepts=["certification", "third-party-risk", "cloud-provider-assurance"],
    ),
}


ALREADY_HAVE = {

    "password-hashing": dict(
        title="Passwords are stored hashed",
        claim=("If your accounts live in Microsoft Entra ID or Google "
               "Workspace, passwords are stored as one-way hashes and neither "
               "you nor the provider's support staff can read them back. You "
               "did not configure this and you cannot turn it off."),
        m365=("All tiers using Entra ID accounts",
              "No setting to show. Cite the platform.",
              "The platform's published security documentation, plus the fact "
              "that password reset issues a new password rather than showing "
              "the old one."),
        google=("All editions using Google accounts",
                "No setting to show. Cite the platform.",
                "The same: reset issues a new password, it never reveals one."),
        caveat=("Only true for accounts held in the platform. If you also run "
                "a line-of-business application with its own user table, that "
                "is a separate answer and it may well be storing passwords "
                "badly. The question usually means all systems, so check the "
                "old ones before answering yes for everything."),
        concepts=["passwords", "password-policy"],
    ),

    "email-malware-filtering": dict(
        title="Email is scanned for malware",
        claim=("Microsoft 365 and Google Workspace both scan inbound mail for "
               "malware by default, on every business plan that includes their "
               "mail service. It has been on since the day you signed up."),
        m365=("Any plan including Exchange Online",
              "Microsoft Defender portal, Email and collaboration, Policies "
              "and rules, Anti-malware",
              "Screenshot of the default anti-malware policy showing it "
              "enabled and its scope."),
        google=("All Google Workspace editions",
                "Admin console, Apps, Google Workspace, Gmail, Safety",
                "Screenshot of the attachment and link protection settings."),
        caveat=("If you run your own mail server, or route mail through a "
                "third party before it reaches the platform, this is not "
                "automatic and you must answer for whatever is actually in the "
                "path. Also check nobody has excluded a domain or a sender "
                "from scanning to fix a delivery problem years ago."),
        concepts=["email-security"],
    ),

    "email-spam-filtering": dict(
        title="Email is filtered for spam",
        claim=("Both major platforms filter spam by default on every business "
               "plan. This is a separate policy from malware filtering and it "
               "is also already on."),
        m365=("Any plan including Exchange Online",
              "Microsoft Defender portal, Email and collaboration, Policies "
              "and rules, Anti-spam",
              "Screenshot of the default anti-spam inbound policy."),
        google=("All Google Workspace editions",
                "Admin console, Apps, Google Workspace, Gmail, Spam, phishing "
                "and malware",
                "Screenshot of the spam settings."),
        caveat=("Same as malware filtering: self-hosted mail, or a third-party "
                "gateway in front, changes the answer. Allow-lists added over "
                "the years are the common weakness, because a sender on the "
                "allow-list bypasses the filtering entirely."),
        concepts=["email-security"],
    ),

    "email-encryption-in-transit": dict(
        title="Email is encrypted in transit",
        claim=("Mail between your platform and any other modern mail service "
               "travels over TLS by default. Both major platforms do this "
               "without configuration and have for years."),
        m365=("All tiers",
              "Exchange admin center, Mail flow, Connectors, plus the platform "
              "documentation",
              "The platform's published statement on transport encryption, and "
              "message headers showing TLS on a delivered message."),
        google=("All editions",
                "Admin console, Apps, Google Workspace, Gmail, plus the "
                "transparency report on email encryption",
                "Message headers showing TLS, and the published encryption "
                "reporting."),
        caveat=("This is opportunistic encryption. If the recipient's mail "
                "server does not support TLS, delivery may fall back to "
                "plaintext unless you have configured enforced TLS for that "
                "domain. So the honest answer is encrypted in transit where "
                "the recipient supports it, which is nearly everywhere but not "
                "everywhere. It is also not the same as encrypting the message "
                "content itself, which is a different question."),
        concepts=["email-security", "encryption"],
    ),

    "screen-lock": dict(
        title="Workstations lock themselves",
        claim=("Automatic screen lock with a password on return is a policy "
               "setting on any centrally managed Windows or Mac estate. On "
               "unmanaged machines it is a default the user can change."),
        m365=("Business Premium and above, where Intune is included; also "
              "available through Active Directory group policy on domain-"
              "joined machines",
              "Intune admin center, Devices, Configuration, or Group Policy "
              "under screen saver settings",
              "Screenshot of the policy showing the timeout, plus a device "
              "compliance report listing which machines it reached."),
        google=("Editions including endpoint management",
                "Admin console, Devices, Mobile and endpoints, Settings",
                "Screenshot of the screen lock policy and the devices it "
                "applies to."),
        caveat=("Central enforcement needs a management tool. If your machines "
                "are not enrolled in anything, the lock may well be on because "
                "it is a default, but you cannot prove it and a user can turn "
                "it off. Say which of those two situations you are in rather "
                "than claiming enforcement you do not have."),
        concepts=["screen-lock"],
    ),

    "admin-mfa": dict(
        title="Admin accounts require MFA",
        claim=("Multi-factor authentication for administrator accounts is "
               "available on every business tier of both platforms at no extra "
               "cost. Microsoft's security defaults switch it on for "
               "privileged accounts without any licensing beyond the base "
               "subscription."),
        m365=("All tiers; security defaults, or conditional access on higher "
              "tiers",
              "Entra admin center, Identity, Overview, Properties, Manage "
              "security defaults; or Protection, Conditional Access",
              "Screenshot showing security defaults enabled, or the "
              "conditional access policy and the accounts it covers."),
        google=("All editions",
                "Admin console, Security, Authentication, 2-step verification",
                "Screenshot of the enforcement setting and the group it "
                "applies to."),
        caveat=("Available is not the same as enabled. Check it is actually "
                "on, and check for exclusions: break-glass accounts are a "
                "legitimate exception but they need to be named, monitored and "
                "few. An emergency account excluded from MFA and forgotten "
                "about is a common finding."),
        concepts=["mfa", "privileged-accounts", "executive-protection", "remote-access"],
    ),

    "backup-encryption": dict(
        title="Backups are encrypted at rest",
        claim=("Data held in Microsoft 365 or Google Workspace, including the "
               "provider's own copies, is encrypted at rest by default. You "
               "did not configure it and cannot switch it off."),
        m365=("All tiers",
              "Service Trust Portal and the platform's encryption "
              "documentation",
              "The provider's published encryption statement, cited by name "
              "and date."),
        google=("All editions",
                "The platform's published encryption documentation",
                "The same."),
        caveat=("This covers the provider's storage. If you also run your own "
                "backups, to a NAS or to a third-party backup service, those "
                "are your responsibility and they may not be encrypted. Check "
                "before answering yes for everything. Encryption also does "
                "nothing about the risk that actually hurts, which is the "
                "backup being reachable from the network it protects."),
        concepts=["backups", "offline-backups", "rpo"],
    ),

    "data-at-rest-encryption": dict(
        title="Stored data is encrypted at rest",
        claim=("Data held in either platform is encrypted at rest as standard. "
               "On endpoints, BitLocker on Windows and FileVault on macOS are "
               "included with the operating system at no extra cost."),
        m365=("All tiers for cloud storage; BitLocker included with Windows "
              "Pro and above",
              "For endpoints: Intune admin center, Devices, Configuration, "
              "disk encryption. For cloud: the platform's encryption "
              "documentation",
              "A device compliance report showing encryption status, plus the "
              "provider's encryption statement."),
        google=("All editions for cloud storage; endpoint encryption depends "
                "on the operating system",
                "Admin console, Devices, plus the platform's encryption "
                "documentation",
                "Device inventory showing encryption status."),
        caveat=("Endpoint encryption is included but not always switched on, "
                "particularly on machines that were set up by hand. Being able "
                "to show a report is the difference between a claim and "
                "evidence. Servers and any on-premises storage are separate "
                "and usually not encrypted unless somebody chose to."),
        concepts=["encryption", "full-disk-encryption"],
    ),

    "audit-logging": dict(
        title="Admin and sign-in activity is logged",
        claim=("Both platforms record administrator actions and sign-in "
               "activity centrally, without you configuring anything. Who "
               "logged in, from where, and what an admin changed are all "
               "already being written down."),
        m365=("All tiers, with retention varying by tier",
              "Microsoft Purview compliance portal, Audit; and Entra admin "
              "center, Monitoring, Sign-in logs",
              "A screenshot of a search over the audit log covering a real "
              "date range."),
        google=("All editions, with retention varying by edition",
                "Admin console, Reporting, Audit and investigation",
                "An export from the admin audit log."),
        caveat=("Retention is the catch and it varies a lot by tier. The "
                "questionnaire often asks for 90 days or more, and the "
                "entry-level retention may be shorter than that. Check yours "
                "before answering, and if it is short, extending it is usually "
                "a licence question rather than a configuration one."),
        concepts=["logging", "privileged-accounts", "third-party-access"],
    ),

    "device-compliance": dict(
        title="Only managed devices reach company data",
        claim=("Both platforms can require that a device is enrolled and "
               "meets a policy before it is allowed to reach company data. "
               "This is included in the business tiers that bundle device "
               "management."),
        m365=("Business Premium and above, where Intune is included",
              "Intune admin center, Devices, Compliance policies; and Entra "
              "Conditional Access to require compliance",
              "Screenshot of the compliance policy and the conditional access "
              "rule enforcing it, plus a device compliance report."),
        google=("Editions including endpoint management",
                "Admin console, Devices, Mobile and endpoints, Settings, "
                "Universal settings",
                "Screenshot of the device approval requirement and the device "
                "list."),
        caveat=("This is a real licensing line. Entry tiers such as Business "
                "Basic do not include Intune, so on those the control is not "
                "available without an add-on. Check what you actually pay for "
                "before claiming it. Enrolment also has to be enforced, not "
                "just offered, or unmanaged devices keep working."),
        concepts=["remote-work-model", "asset-inventory", "hardening", "screen-lock",
                  "removable-media", "endpoint-protection", "mobile-device-management",
                  "patch-management", "remote-access", "application-allowlisting",
                  "full-disk-encryption"],
    ),

    "mobile-app-protection": dict(
        title="Company data on phones is contained",
        claim=("Both platforms can keep company data inside managed apps on a "
               "phone, so it can be removed without touching anything personal "
               "on the device. This works on phones the company does not own."),
        m365=("Business Premium and above, where Intune is included",
              "Intune admin center, Apps, App protection policies",
              "Screenshot of the app protection policy and the users it "
              "covers."),
        google=("Editions including mobile management",
                "Admin console, Devices, Mobile and endpoints, Settings, "
                "Universal, Data sharing",
                "Screenshot of the work profile or data sharing restrictions."),
        caveat=("Same licensing line as device compliance: entry tiers may not "
                "include it. Also, containment is not the same as full device "
                "management, and it is worth saying which one you have. "
                "Wiping company data from a container is possible; wiping a "
                "personal phone usually is not, and in some countries "
                "attempting to would be a legal problem."),
        concepts=["mobile-device-management", "remote-work-model"],
    ),

    "external-sharing-controls": dict(
        title="Sharing outside the company is controlled",
        claim=("File sharing with people outside the organisation is governed "
               "by a central setting in both platforms. The defaults are "
               "usually more permissive than owners expect, but the control "
               "exists and costs nothing to tighten."),
        m365=("All tiers with SharePoint or OneDrive",
              "SharePoint admin center, Policies, Sharing",
              "Screenshot of the external sharing level for the tenant and for "
              "individual sites."),
        google=("All editions with Drive",
                "Admin console, Apps, Google Workspace, Drive and Docs, "
                "Sharing settings",
                "Screenshot of the external sharing configuration."),
        caveat=("The default often allows sharing with anyone who has the "
                "link, which is not what most owners assume. Check before you "
                "answer, because answering yes and then discovering that "
                "anonymous links are enabled is worse than answering honestly "
                "the first time."),
        concepts=["data-classification", "dlp", "tenant-segregation"],
    ),

    "retention-policy": dict(
        title="Deleted items are retained and recoverable",
        claim=("Both platforms keep deleted mail and files recoverable for a "
               "period after deletion, without you configuring anything. This "
               "covers the accidental-deletion case that people usually mean "
               "when they ask about backups."),
        m365=("All tiers, with the period varying; longer retention through "
              "Purview on higher tiers",
              "Purview compliance portal, Data lifecycle management; and the "
              "mailbox recoverable items settings",
              "Screenshot of the retention configuration and the recoverable "
              "period."),
        google=("All editions, with configurable retention through Vault on "
                "editions that include it",
                "Admin console, plus Google Vault where included",
                "Screenshot of the retention rules."),
        caveat=("Default retention is measured in weeks, not years, and it is "
                "not a backup. It will not help you against ransomware "
                "encrypting files in place, or against a malicious admin, or "
                "against a retention period expiring before anyone noticed the "
                "data was gone. Say what the actual period is rather than "
                "implying indefinite recovery."),
        concepts=["backups", "rpo"],
    ),

    "admin-role-separation": dict(
        title="Admin roles are separate from user accounts",
        claim=("Both platforms let you assign administrative roles to separate "
               "accounts, and both provide granular roles so somebody who only "
               "manages users does not also control everything else. Included "
               "at every tier."),
        m365=("All tiers",
              "Entra admin center, Identity, Roles and administrators",
              "A list of who holds which administrative role, plus evidence "
              "those are separate accounts from the holders' daily ones."),
        google=("All editions",
                "Admin console, Account, Admin roles",
                "The admin role assignment list."),
        caveat=("The capability is free; using it is a decision. The common "
                "finding is a handful of accounts holding Global Administrator "
                "because it was easier, and those same accounts being used to "
                "read email. Answering yes means separate accounts actually "
                "exist, not that the platform supports them."),
        concepts=["privileged-accounts", "identity-lifecycle"],
    ),

    "basic-dlp": dict(
        title="Built-in leak protection exists without buying anything",
        claim=("Both platforms include policies that can detect and block "
               "recognisable sensitive data, such as card numbers and national "
               "identifiers, leaving the organisation. They ship switched off, "
               "or in report-only mode, and most owners never look."),
        m365=("Business Premium and above; check entry tiers before claiming "
              "it",
              "Microsoft Purview compliance portal, Data loss prevention, "
              "Policies",
              "Screenshot of an enabled policy and the locations it covers."),
        google=("Enterprise editions; not available on the entry business "
                "editions",
                "Admin console, Security, Data protection",
                "Screenshot of the configured rules."),
        caveat=("This is the clearest licensing trap of the set. Data loss "
                "prevention is genuinely not included in the cheaper editions "
                "of either platform, so check what you pay for before "
                "answering. Even where it is included, a policy in report-only "
                "mode is monitoring rather than prevention, and the difference "
                "matters if somebody audits the answer."),
        concepts=["dlp"],
    ),
}
