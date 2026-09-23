# Agents for Humans: two days in AWS and I am not much smarter

AWS has always been a bit of a black box for me. I joined the hackathon to fix
that.

I registered and it was worse than I remembered. I used Claude to tell me
exactly where to find what. In the end she got frustrated and asked me to
install the CLI on my pc and let her drive. I activated IAM Identity Center and
got a sign saying my free account is now a paid one. Not ideal. Anyway, moved
on, created the keys, let Claude do something.

Now there is seemingly something in Lambda, S3, DynamoDB and Bedrock, and
seemingly it works. I still lack a dashboard showing me what I have where. So I
am not much smarter on AWS than before.

Two things I would have liked to know. The Frankfurt catalog carries no
Anthropic models, so Ireland. And an eu.* inference profile routes to six
regions, not four, so an IAM policy naming four fails intermittently instead of
failing properly.

Vibecoding is not as cool as it was a year ago. In a complex environment it
still gets you deployed quicker. You just need to remember that it is you who is
in charge of the cost and the security, not the AI helping you.

## What I built

NIS2 makes customers check that their vendors are secure, so they send
questionnaires. 50 to 300 rows of translated consultant-speak. I have answered
many. WhyF takes one row and explains what is actually being asked, whether it
applies to a company your size, what proof satisfies it, and whether the thing
is worth the money. It never tells you what to answer. That is a contractual
claim about your company and only you can make it.

Five stages, two of them Strands agents. The other three need no model. The
Reader hands over a card id and nothing else. Every word after that was written
by a person, so it cannot invent an answer.

The biggest accuracy win came from a failure. Asked which card this is, a model
always answers, confidently. A row about whistleblowing came back as
incident-reporting. Right family, wrong answer. Splitting it into two questions,
which card is closest and does that card actually answer the row, took a probe
set from 1 correct out of 9 to 8.

Spend caps are in the code, not in a billing alarm. Over the daily ceiling it
answers from the free matcher and says on screen that it is degraded.

Try it: why-f.com

Code, MIT: github.com/apn201/whyf
