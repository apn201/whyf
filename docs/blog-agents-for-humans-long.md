# Agents for Humans: two days in AWS and I am not much smarter

AWS has always been a bit of a black box for me. I know what it is. We use it at
work, but I am not the admin there. I have had a workshop with AWS about the
services behind our intranet and extranet solutions and the controls around
them. Already in the workshop it was intimidating to look at all the dashboards,
menus, abbreviations and places where you do not really know what does what.

So I joined the [Agents for Humans](https://agentsforhumans.devpost.com/)
hackathon to fix that. AI and agents are a hot topic both at work and privately.
I use Openclaw at home to automate some stuff, but Strands Agents was completely
new territory.

I registered in AWS and it was even more overwhelming than I remembered. Just
creating a non-root user and adding a passkey felt difficult. I used Claude to
tell me exactly where to find what. In the end she got frustrated and asked me
to install the CLI on my pc and let her drive. That step was also scary. I
needed to activate IAM Identity Center and got a sign saying my free account is
now changed to a paid one. Crap. Anyway, moved on, created the keys, linked
them, let Claude do something.

Now there is seemingly something in Lambda, S3, DynamoDB and Bedrock, and
seemingly it works. I spent a long time googling what is what and I still lack a
dashboard showing me what I have where. So I am not much smarter on AWS than
before.

Vibecoding is not as cool as it was a year ago. In a complex environment like
AWS it still gets you deployed a lot quicker than reading your way in. You just
need to remember that it is you who is in charge of the cost and the security,
not the AI helping you.

A few things I would have liked to know before starting. Ireland, not Frankfurt:
the Frankfurt catalog carries no Anthropic models. The Bedrock console does not
list embedding models at all, which made me conclude for half a day that the EU
had none, and the API has them. An `eu.*` inference profile routes to six
regions, not four, so an IAM policy that names four of them fails intermittently
instead of failing properly.

## Why the f

The project is called WhyF. Why the f are they asking this.

It comes from real life frustration. NIS2 forces customers to make sure their
vendors are secure enough, so they send out questionnaires. 50 to 200 rows.
Sometimes 300. I have answered many of these. A lot of the rows say nothing to
the person who has to tick them.

Here is a real shape of a row, rewritten so it belongs to nobody:

> A formalised mapping of operational technology assets, together with their
> sensitivity tiering, is maintained on an ongoing basis.

A company with eleven employees now has to answer that. It has been translated
twice, pasted between four companies and renumbered by somebody who has never
seen the system it describes. There is no security team to ask and the deal is
waiting. So they tick yes to make it go away, which is a false statement in a
contract. Or they tick no on a control they probably already have. Or they pay a
consultant for two days to find out the row does not apply to them.

WhyF does not answer the questionnaire. That is the one thing nobody can do for
you, because the answer is a factual claim about your company. It tells you what
the row is actually asking, whether it applies to you, what proof would satisfy
it, and whether the underlying thing is worth spending money on. It is allowed
to conclude that it is not.

If your answer is no, it tells you how far from yes you are and what the trip
costs. In euros and in afternoons, from your business point of view, not just to
get the checkbox on the form.

## What the agents do

I curated the knowledge by hand. 112 concept cards, written from having answered
these forms, not scraped from anywhere. The agents are the plumbing that finds
the right card. This is what the interface shows while it works on the asset row
above:

```
✓ Recogniser   Normalised the row and looked for it in the cache. Not seen before.      4 ms
✓ Librarian    Expanded acronyms, searched 112 cards by wording and by meaning,       182 ms
               put the closest 15 in front of the next stage.            titan-embed-text
✓ Reader       Picked asset-inventory. Judged separately whether that card           3169 ms
               actually answers what was asked: it does.        claude-haiku-4-5-20251001
✓ Scribe       Assembled from the card. No model wrote any of this text.                0 ms
  route concept · model calls 2 · cards 15 shortlisted · total 3.4 s
```

Two of those five are Strands agents. The other three are plain code, because
they do not need a model to do their job.

The Scribe line is the point of the whole thing. The Reader hands over a concept
id and nothing else, and the id is checked against the shortlist before it is
used. Every word you then read was written by a person. The verdict, the counter
argument, the costs. A prompt injection can at absolute worst get you the wrong
card. It cannot make the tool say something that is not in the knowledge base.

There is a fifth agent, the Understudy, for rows no card covers. It writes one
under constraints, and everything it produces is labelled as generated, on
screen, with no option to hide it.

## Two things that came out of failures

The Reader used to make one judgement: which concept is this. A model always
answers that question, and answers it confidently. A row about paying a ransom
came back as incident-response. A row about whistleblowing came back as
incident-reporting. Right family, wrong answer, and well formatted, which is the
worst thing this tool can do to somebody using it to avoid lying in a
contract.

Splitting it into two questions fixed it. How sure are you that this is the
closest card, and does that card actually answer the row. A confident no on the
second is the useful answer, because then you get the nearest card plus a
precise description of what it does not cover. On a probe set of nine
deliberately adjacent questions it went from 1 correct to 8.

The second one was invisible until I tested it. Ask the deployed agent "do you
have PAM?" and it declines. The letters P, A, M appear nowhere in the knowledge
base, so neither the text index nor the embeddings can reach the privileged
accounts card. That looks like the model not understanding, when it is retrieval
failing. The fix was about sixty acronym expansions and a retrieval-only
vocabulary list on 33 cards, and neither one costs a model call.

Against 329 real questionnaire rows, none of which are in the repository, 310
get answered from a card and 19 get the nearest card with the gap named. Zero
bare declines. Rows about payment terms and parking spaces still decline, which
is the property that makes the first number mean anything.

## Cost and safety

A public demo URL that can call a model is a way to spend money by accident, so
the caps are in the code and not in a billing alarm. Six model calls per
request. A daily ceiling checked before the work, not after. Over the ceiling
the agent keeps answering from the free text matcher and says on screen that it
is degraded. I would rather hand a judge a slow demo than one that quietly
stopped working.

The model choice follows the same logic. The Reader picks one id out of fifteen,
so it runs on Haiku. Sonnet only runs on the cold path, which is about 1.4 cents
a time, and cache hits cost nothing.

The three real supplier questionnaires this was built from are not in the
repository. Their wording belongs to the companies that wrote them. There is a
check that scans every shipped file for six word runs taken from the real
sources and fails the build if it finds any, and another that walks all of git
history rather than just the working tree.

## Try it against a plain chatbot

Take a row from a form somebody sent you. Paste it into your favourite LLM, then
paste it into WhyF, and see which answer you would rather send to a customer.

Try it: [why-f.com](https://why-f.com/)

Code, MIT: [github.com/apn201/whyf](https://github.com/apn201/whyf)
