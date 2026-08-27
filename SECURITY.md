# Security policy

This project has a card in its own knowledge base about publishing a way for
strangers to report flaws, and what that page ought to say. It would be a poor
look not to have one.

## What this is

A hackathon demo, and worth being plain about that. There is no product, no
paying customer and no support contract. There is a public endpoint at
`whyf.apn201.com`, a Lambda function behind it, and a knowledge base of security
concept cards.

**Supported versions: `main`, and only `main`.** There are no releases, no
version numbers and no branches receiving backported fixes. If a problem is real
it gets fixed on `main`, and the deployed endpoint is redeployed from it.

## Reporting a vulnerability

Use GitHub's private vulnerability reporting: the **Security** tab of this
repository, then **Report a vulnerability**. It opens a private thread visible
only to the maintainer, which is better than an issue because an issue is
public the moment you file it.

Please include enough to reproduce it. A URL, a request, and what you expected
instead is usually plenty.

**What to expect.** This is one person working on it around a day job, so an
honest commitment rather than a flattering one:

| | |
|---|---|
| Acknowledgement | within 5 working days |
| First assessment | within 14 days |
| Fix, if the report is accepted | no committed date, but you will be told what the plan is |
| If declined | you will be told why, not ignored |

If you have not heard anything in two weeks, assume the notification was missed
rather than that you are being stonewalled, and nudge the thread.

**Safe harbour.** Test against `whyf.apn201.com` and the code in this repository
in good faith and no legal action will be taken. Good faith means: do not run
denial-of-service or load tests, do not attempt to reach data belonging to
anyone else, do not pivot to other apn201 systems, and give a reasonable chance
to fix before publishing. Stay within that and you are welcome here.

There is no bug bounty and no payment. Credit in the release notes if you want
it, and honest thanks either way.

## In scope

- The deployed endpoint and the Lambda behind it
- This repository: the agent, the CDK stack, the build and validation tooling
- The knowledge cards, including a card that is materially wrong in a way that
  would mislead somebody answering a questionnaire

That last one is a real report and is welcome. Bad security advice is the
failure mode this project cares most about.

## Not in scope, and why

Some of these look like findings and are deliberate design decisions. Reporting
them is fine, but the answer will be this section.

**The demo endpoint is public and unauthenticated.** On purpose. It holds
nothing about anybody and needs no session. Spend is bounded by a daily
model-call ceiling enforced in code, checked before the work rather than after.
Over the ceiling the agent keeps answering from the free lexical matcher and
says on screen that it is degraded.

**A prompt injection can cause the wrong card to be selected.** Known and
accepted. On the warm path the model's entire output is a concept id validated
against a fixed shortlist, so the worst outcome is a card that does not fit the
question. Every word displayed comes from a card a human wrote. There is no path
from model output to displayed prose.

**The cold path writes prose.** Also known, and the reason it is the most
constrained component in the codebase: it runs only when a security concept was
already judged nearest, the pasted row is fenced as data, the output is a schema
with no free-text channel, and citations are validated against the library.
Every generated answer is labelled as generated, on screen.

If you find a way past *those* constraints — an injection that makes the tool
emit attacker-chosen text, or that makes it draft an answer to a questionnaire
on the user's behalf — that is very much in scope and I would like to know.

**No rate limiting per IP.** The daily ceiling is the control. A demo URL that
silently stops working is worse than a slow one.

## What the service stores

Questions are normalised, hashed, and cached with their verdict in DynamoDB so
that a repeated row costs nothing. No accounts, no cookies, no analytics, no IP
logging beyond what AWS records by default.

The agent never asks anything about your company and never learns anything about
it. It does not need to: it explains what a question means, and you answer it.

Do not paste anything confidential into the demo. It is one row from a
questionnaire, and questionnaire rows are not secrets — but the box will accept
whatever you put in it, and it is a hackathon demo rather than a system with a
data-processing agreement behind it.

## What is not in this repository

The three real supplier questionnaires this was built from are not published.
They belong to the companies that wrote them and one is a commercial assessment
product. They live in a gitignored directory that never leaves one machine.

Two checks enforce that, and both are in the repository:

- `python tools/check_publishable.py --history` scans every shipped file **and
  every blob ever committed** for copied wording. History is what gets
  published; the working tree is only what you happen to be looking at.
- `python tools/check_secrets.py` walks all of git history for credentials,
  keys, and identifiers of the assessed company.

If you find something private that got through either of them, that is a report
worth making, and it is the one I would most want to receive.
