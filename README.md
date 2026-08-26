# WHY THE F?

**Why the f are they asking this?**

Paste one row from a supplier security questionnaire. Get one verdict.

It does not answer the questionnaire. It explains what the question is really
about, whether it applies to you at all, what proof would satisfy it, and
whether the underlying thing is worth spending money on. It is allowed to
conclude that it is not.

> It will not fill in your questionnaire. It will stop you from lying in it by
> accident.

Built for the Agents for Humans hackathon, Professional Agents track, on the
Strands Agents SDK and AWS Bedrock.

## The hard rule

The tool never tells you what to answer. Answering a questionnaire is a
contractual representation. It explains, translates and prices. The human
answers.

## Is it even a control?

The classifier's first job is deciding whether the pasted row is a security
question at all. Four classes; only the first gets a verdict.

| class | what it is | what happens |
|---|---|---|
| `control` | a security control | one of the six verdicts |
| `attestation` | a claim about a certificate or a contract | say what the claim commits you to |
| `admin` | headcount, contact email, number of data centres | say it is not a security question and move on |
| `disclosure` | "have you ever been breached?" | refuse to help word it, and say why |

That last row is the hard rule at its sharpest. A wrong answer to a breach
history question is not a failed control, it is a misrepresentation that can
void a cyber insurance policy. The tool says so and names who to call.

## The six verdicts

Every question of class `control` resolves to exactly one of six, and no others
exist:

| | |
|---|---|
| Not applicable | Here is how to say so without looking evasive. |
| Already solved | Go find the screenshot. |
| Write it down | Documentation control. An afternoon of work. |
| Cheap checkbox, expensive fix | Satisfy the question. Do not buy the product yet. |
| Do it properly | Real risk, real money, here is why. |
| Cannot tell yet | One question first. |

Alongside the verdict, four axes: does it apply to you, how much security value
the fix has, how much commercial value the checkbox has, and what it costs in
euro symbols. The gap between security value and checkbox value is the product.

### Which rung is enough

Sixty-five of the corpus rows are not statements at all, they are four-rung
maturity ladders: *not implemented / some systems / all systems / all systems,
risk-based, reviewed annually and aligned to emerging threats*.

Rung 4 is written by someone who sells rung 4. Every card that meets a ladder
has to say which rung is enough and what the last one actually buys - and that
answer is different for a packaging plant and a bank, so it is a judgement per
concept and per sector rather than a number read off a table.

## How it works

Three Strands agents. A **Classifier** normalises the pasted row, detects
statement-versus-question form, spots negation and translation damage, and maps
it to a concept. A **Researcher** owns six tools and only runs on a cache miss.
A **Skeptic** argues the control is not worth doing and produces the counter-case
that goes into the verdict.

The step that matters is detecting the single missing fact. An LLM wrapper
answers instantly and confidently. This agent works out that it cannot separate
"annoying" from "business stops", asks one question with buttons and no typing,
and the verdict visibly changes.

### Three tiers, and the UI says which one fired

```
resolved from cache  ·  1 model call  ·  0 searches  ·  0.9 s
new concept          ·  3 searches    ·  4 model calls  ·  11 s
```

- **Tier 0, exact match.** Normalise, hash, DynamoDB lookup. Questionnaire rows
  get copy-pasted between companies endlessly. Zero model calls.
- **Tier 1, semantic match.** Embed the question with Titan, cosine against the
  pre-embedded concept catalog held in Lambda memory, blended with a free
  lexical index over the same cards. Eighty concepts times a 1024-float vector
  is small enough for pure Python. No numpy, no vector database, no OpenSearch.
  Tier 1 hands the classifier a shortlist of 15 rather than an answer: measured
  against 364 real questionnaire rows, that shortlist contains the right
  concept 91% of the time. When the daily spend ceiling is hit, the embedding
  call is dropped and the lexical half carries on alone at 82%.
- **Tier 2, cold path.** Unknown concept, full research loop, result written back
  as a new evidence package. The system gets cheaper the more it is used.

### Anti-hallucination

Incident figures and framework references come only from the curated library,
referenced by id. The model cannot free-text a dollar figure or a control
number. Output is validated against the id set before rendering and unknown ids
are dropped. `tools/validate_cards.py` applies the same rule to the corpus at
build time, so a malformed card fails the build rather than a demo.

This is a security tool. If a judge fact-checks one number and it is wrong, the
submission is dead.

## What is in this repository, and what is not

The cards ship. The questionnaires they were built from do not.

Three real supplier questionnaires went into building this - 364 rows. Their
wording belongs to the companies that wrote them, one of them is a commercial
assessment product, and a fourth source was a confidential assessment of a named
company. None of that is here. It lives in a gitignored `private/` directory and
never leaves the machine it was built on.

What ships instead is `corpus/synthetic.tsv`: 223 questions written for this
repo from the concept catalog, covering every concept and every question form.
The repo builds, tests and runs from a clean checkout with nothing private
present. `python tools/check_publishable.py` scans every shipped file for wording taken from the
real sources and fails the build if it finds any.

Coverage statistics are reported against the real corpus when it is present,
because covering questions we wrote ourselves proves nothing. See
[corpus/README.md](corpus/README.md).

## Repository layout

```
corpus/               synthetic questions, ours, safe to publish
knowledge/            the product. everything else is plumbing.
  concepts/      80   one card per concept, covering every corpus row
  frameworks/     7   incl. all 106 CSF 2.0 subcategories and a 190-entry
                      crosswalk to NIS2, ISO 27001/27002 and IEC 62443
  incidents/     12   curated records, every figure sourced
  patterns/       5   questionnaire bullshit patterns
  already-have/  15   controls already satisfied by default M365 / Workspace config
  WRITING-CARDS.md    how to fill them in. read this first.
src/whyf/             strands agents, tools, cache tiers, spend caps
infra/                cdk stack and config.yaml
web/                  phone-width PWA
tools/                questionnaire parsers, corpus mapping, validation
docs/AWS-SETUP.md     the console work
private/              gitignored. the real questionnaires and everything
                      derived from them. absent from any checkout but one.
```

## Getting started

```bash
pip install -r requirements.txt
```

```bash
python tools/validate_cards.py
```

Deploying needs an AWS account with Bedrock model access. See
[docs/AWS-SETUP.md](docs/AWS-SETUP.md) - Bedrock model access blocks everything
else, so do it first.

```bash
python tools/check.py
```

Card validator, publication check and tests. Passes on a clean checkout with no
private data present. `make check` does the same thing if you have make; this
project is developed on Windows, where you usually do not.

## Status

The knowledge substrate is finished. 80 concept cards, 15 already-have cards, 5
patterns and 6 framework libraries, all at `done`, covering every one of the 364
rows across the three source questionnaires.

One gap, deliberately: the 12 incident records are blank. Every field in them is
a sourced figure, and a figure that came out of a language model is exactly the
thing that gets fact-checked. No card cites an incident, so nothing renders
empty, and the validator will reject a card that starts to.

Next is the agent itself and the AWS deployment. Bedrock model access blocks
everything, so it goes first: [docs/AWS-SETUP.md](docs/AWS-SETUP.md).

## License

MIT. See [LICENSE](LICENSE).
