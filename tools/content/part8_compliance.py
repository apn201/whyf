"""Certification and regulatory-scope cards.

Thirty-odd questions in a modern supplier questionnaire are not about controls
at all. They ask whether you hold a certificate, whether a regulation applies
to you, and whether you will send the document. Answering those as if they
were controls produces confident nonsense, so they are attestations: the card
says what the thing is, whether it applies, and what to send.

The recurring lie in this section is scope. A certificate that does not cover
the service being bought is worth nothing to the buyer and everything to the
seller, and almost nobody checks.
"""

CARDS = {

    "isms": dict(
        priority=1,
        plain_english=(
            "Do you have an information security management system. Not a "
            "policy, not a tool. The management loop around security: decide, "
            "do, check, fix, repeat."),
        response=(
            "An ISMS is the machinery, not the documents. Policy, risk "
            "assessment, a treatment plan, objectives, internal review, and "
            "management actually looking at the results. If you have those and "
            "they happen on a schedule, you have an ISMS whether or not anyone "
            "has used the word. If you have a folder of policies and nothing "
            "reviews them, you do not, and saying you do is the kind of claim "
            "that unravels in an audit. You do not need certification to have "
            "one, and that distinction is worth making explicitly in your "
            "answer: aligned with ISO 27001 is a true statement, certified is "
            "a different and checkable one."),
        refer_to=(
            "Nobody external, unless you are pursuing certification. If you "
            "are, an auditor will tell you in an hour whether what you have "
            "counts, which is cheaper than guessing for six months."),
        answer_risk="certification",
    ),

    "soc2": dict(
        priority=1,
        plain_english=(
            "Do you have a SOC 2 report. An American audit report about how "
            "you run your service, produced by an accounting firm."),
        response=(
            "Two things decide whether this is worth anything to the asker. "
            "Type I says your controls were designed sensibly on one day. "
            "Type II says they actually operated over a period, usually six or "
            "twelve months, and it is the only one most buyers accept. And the "
            "Trust Services Criteria: every report covers Security, but "
            "Availability, Confidentiality, Processing Integrity and Privacy "
            "are each optional, so a report can be genuine and still not cover "
            "what the buyer is asking about. Say which criteria yours covers "
            "rather than saying yes. If the audit period ended before today, "
            "they will ask for a bridge letter, which is a short statement "
            "from you that nothing material has changed since; it is normal, "
            "it is free, and you write it yourself. Reports go out under NDA, "
            "always. If you do not have one, say so plainly: SOC 2 is a "
            "serious cost and a European supplier not having one is entirely "
            "normal, so do not imply that one is imminent unless it is."),
        refer_to=(
            "Whoever holds the report, and your lawyer for the NDA. If you are "
            "considering getting one, count how many customers have asked "
            "first; it is a sales cost and should clear a sales bar."),
        answer_risk="certification",
    ),

    "pci-dss": dict(
        priority=1,
        plain_english=(
            "Does the card payment standard apply to you. It applies if you "
            "store, process or transmit cardholder data, and to anything that "
            "can affect the security of the systems that do."),
        response=(
            "Most companies who think they are in scope are not, and the ones "
            "who are usually could be less so. If payments go through a hosted "
            "page or a redirect at your payment provider, and card numbers "
            "never touch your systems, your obligation is usually the shortest "
            "self-assessment questionnaire rather than an audit. The way to "
            "reduce this is not better controls, it is removing card data from "
            "your environment entirely, and that is a change to how checkout "
            "works rather than a security project. If you are genuinely in "
            "scope, the buyer will want your Attestation of Compliance and, "
            "for anything shared, a responsibility matrix saying which "
            "requirements are yours and which are theirs. Your own payment "
            "provider and anyone touching that flow can affect your compliance, "
            "so they belong in your supplier list."),
        refer_to=(
            "Your payment provider first. They know your merchant level and "
            "which self-assessment applies, and they will usually tell you "
            "free. A QSA only if the provider says you need one."),
        answer_risk="certification",
    ),

    "hipaa": dict(
        priority=2,
        plain_english=(
            "Do you handle American health data, and will you sign the "
            "agreement that comes with it."),
        response=(
            "This one is binary and it is contractual before it is technical. "
            "If you handle protected health information on behalf of a US "
            "healthcare customer, you are a business associate and you have to "
            "sign a Business Associate Agreement. No BAA means you cannot take "
            "the work. If you do not serve US healthcare, say so in one line "
            "and the whole section disappears. Do not answer these questions "
            "aspirationally: signing a BAA commits you to breach notification "
            "timeframes and to safeguards you then have to actually have, and "
            "it is enforceable by a US regulator against a European company "
            "through the contract."),
        refer_to=(
            "A lawyer, before signing a BAA, not after. This is one of the few "
            "places on a questionnaire where the answer creates a legal "
            "obligation rather than describing one."),
        answer_risk="warranty",
    ),

    "dora": dict(
        priority=1,
        plain_english=(
            "Do you supply financial-sector customers in the EU. If you do, "
            "their regulator now reaches you through their contract with you."),
        response=(
            "DORA does not regulate you directly unless you are designated "
            "critical, but it obliges your financial customers to put specific "
            "things in their contracts with you, so it arrives as contract "
            "terms rather than as a law you read. The recurring four: audit "
            "and access rights for the customer and their regulator, incident "
            "notification to the customer on their timetable, a documented "
            "exit plan so they can leave without the service collapsing, and "
            "visibility of your own critical subcontractors, because their "
            "supply chain now includes yours. If you have no financial "
            "customers, say so and skip it. If you have one, expect these "
            "terms and decide in advance which you can actually live with; "
            "agreeing to unlimited on-site audit rights and then refusing the "
            "first request is worse than negotiating now."),
        refer_to=(
            "Your lawyer, and whoever owns the financial-sector customer "
            "relationship. These are contract negotiations, not security "
            "controls, and the security answer is the easy half."),
        answer_risk="warranty",
    ),
}
