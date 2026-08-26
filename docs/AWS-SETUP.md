# AWS setup

The console work only you can do, in the order it has to happen. About ninety
minutes including waiting.

Nothing in `src/` can be tested against real Bedrock until step 4 is green, so
steps 1 to 4 belong in one sitting.

---

## Already settled

Do not redo these.

**Region: `eu-west-1` (Ireland).** Decided 26 August, written into
`infra/config.yaml`. Reasoning in the decision record at the bottom.

**Models, all three verified by invoking them on 26 August:**

| job | model id | called |
|---|---|---|
| synthesiser | `eu.anthropic.claude-sonnet-4-6` | once per cold verdict |
| classifier | `eu.anthropic.claude-haiku-4-5-20251001-v1:0` | once per cache miss |
| embedding | `amazon.titan-embed-text-v2:0` | optional, tier 1 |

A cold verdict is roughly 3k in and 800 out, so about 1.4 cents. Cache hits cost
nothing. $50 of credits is thousands of verdicts.

Sonnet 5 and Opus 4.8 are listed in the region but return `AccessDenied` even
after the use case form. They are gated beyond it on a normal account. Sonnet
4.6 does the job and the codebase names no model anywhere except
`infra/config.yaml`, so swapping later is one line.

**Embeddings: `amazon.titan-embed-text-v2:0`, and it works today.** The console
catalog does not list embedding models, which led to an early wrong conclusion
that the EU had none. The API has them.

Tier 1 does not depend on it either way. `src/whyf/match.py` is a lexical index
over the concept cards that needs no model at all, and it is what runs when
`embedding` is empty in the config. Embeddings are the accuracy upgrade on top,
not the thing that makes tier 1 exist.

---

## Blocking. Do first.

### 1. Install the AWS CLI

Not installed on this machine. Everything below needs it.

```bash
winget install --id Amazon.AWSCLI -e
```

Close and reopen the shell afterwards so it lands on `PATH`.

### 2. Root account hygiene, once, manually

- [ ] MFA on the root user. TOTP or hardware key.
- [ ] Alternate contacts set: billing, security, operations.
- [ ] Billing console: turn on "IAM user and role access to Billing Information".
- [ ] Close the root session and do not use it again.

### 3. Build identity

IAM Identity Center. Ten minutes, and no long-lived keys sitting in a Dropbox
folder.

Console half first. The CLI cannot do this part, and `aws configure sso` will
ask for a URL that does not exist until it is done.

- [ ] IAM Identity Center console, **region set to `eu-west-1`**, Enable.
      Identity Center has one home region per account and this is the choice.
      Choose an **account instance**, not an organization instance. An account
      instance is all a single-account project needs. The organization instance
      pulls in AWS Organizations, and on a recently opened account that can flip
      the billing plan from Free Plan to Pay-As-You-Go. Neither service costs
      anything, and the flip is not a charge, but it removes the hard spending
      stop, so do step 5 the same evening if it happens.
- [ ] **Users** -> Add user. Username `juha`, a real email address, first and
      last name. Skip the group step. Create.
- [ ] **Check that email and accept the invitation.** Set a password, register
      MFA when it asks. SSO login fails with a confusing error until the user
      has actually been activated, and this is the step people skip.
- [ ] **Permission sets** -> Create. Predefined permission set ->
      `AdministratorAccess` -> Next. Name it `HackathonAdmin`, session duration
      8 hours. Create.
- [ ] **AWS accounts** -> tick your account -> Assign users or groups. Users
      tab, pick `juha`, Next. Pick `HackathonAdmin`, Next, Submit. Takes a
      moment to provision.
- [ ] **Copy the AWS access portal URL from the Identity Center dashboard.**
      It looks like `https://d-1234567890.awsapps.com/start`, or
      `https://something.awsapps.com/start` if you set a custom alias. Older
      console versions call it the user portal URL.

Not to be confused with the IAM sign-in URL,
`https://<account-id>.signin.aws.amazon.com/console`, which is a different
thing entirely and is what the console shows you on the IAM dashboard. Feeding
that one to `aws configure sso` gives you `Invalid start url provided`. If the
only URL you can find has `signin.aws.amazon.com` in it, Identity Center is not
enabled yet.

Now the CLI half:

```bash
aws configure sso --profile whyf
```

It asks five things in this order:

| prompt | answer |
|---|---|
| SSO session name | `whyf` |
| SSO start URL | the portal URL you just copied |
| SSO region | `eu-west-1` - where Identity Center is enabled, not where your resources are |
| SSO registration scopes | accept the default `sso:account:access` |
| then, after the browser | account, role `HackathonAdmin`, region `eu-west-1`, output `json`, profile `whyf` |

A browser opens partway through and asks you to authorise the request. If it
does not open, the CLI prints a URL and a code to paste.

```bash
aws sso login --profile whyf
```

Set `AWS_PROFILE=whyf` in the shell you hand to Claude Code, and confirm it
worked:

```bash
aws sts get-caller-identity --profile whyf
```

### Fallback: IAM user with a key

Take this the moment Identity Center costs you more than ten minutes. It is
the right call under time pressure and this project has nineteen days left. IAM console, Users, Create user
`whyf-builder`, no console access. Attach `AdministratorAccess` directly.
Security credentials, Create access key, choose "Command Line Interface". Then:

```bash
aws configure --profile whyf
```

Access key, secret, `eu-west-1`, `json`. Done in three minutes.

The cost is a long-lived key pair on disk in a Dropbox folder, which is exactly
the thing this project tells other people not to do. If you take this path,
delete the key the moment judging ends on 8 October, and do not put the repo's
own AWS credentials anywhere near `private/`.

### 4. Bedrock model access - the hard blocker

**The Model access page is retired.** Serverless models now enable themselves
on first invocation, so there is nothing to request for most of them. Anthropic
is the exception, and the form that gates it moved with the page.

- [ ] Bedrock console, **`eu-west-1`**, **Model catalog**. Pick a Claude model,
      open its page, and use **Open in Playground**. The Anthropic use case
      details form appears there. Company name, website, industry, who the
      users are, what you are building.
- [ ] Submit it, then **wait 15 minutes**. The error message says so
      explicitly, and the propagation is genuinely that slow.
- [ ] Everything else enables itself the first time you call it. No requests to
      raise.

Until the form is in, every Anthropic model returns `ResourceNotFoundException:
Model use case details have not been submitted for this account`, which reads
like the model does not exist rather than like a form is missing. One form
unblocks all of them.

Some of the newest models return `AccessDeniedException: not available for
this account` even after the form. Those need enabling individually, and a few
are gated harder than that. Do not fight one particular model; the probe will
tell you which ones actually answer.

Then find out what actually answers. Listing a model is not the same as being
allowed to call it, so the probe invokes each pick rather than trusting the
catalog:

```bash
python tools/probe_bedrock.py --region eu-west-1 --profile whyf --test
```

Add `--write` once the picks come back OK and it puts them into
`infra/config.yaml`. Add `--all` to see every model id in the region.

The console catalog and the API disagree. The catalog page in Ireland shows
about 35 models and no Amazon ones; the API returns 62 foundation models and 41
inference profiles, including the Titan and Cohere embedding models the catalog
page does not list. Trust the probe.

Two reasons not to copy ids by hand. In the EU, Anthropic models are usually
only callable through a cross-region inference profile, and the profile id is
not what the catalog page shows. And the model catalog differs by region: this
same catalog in Frankfurt has no Anthropic models at all, which is why the
region moved.

If the picks come back on an inference profile (`eu.anthropic...`), the runtime
IAM policy has to allow both the profile ARN and the underlying foundation model
ARNs in **every** region the profile can route to. This is the one that costs
everybody an afternoon. The policy in `infra/` already lists the four EU regions.

### 5. Money guardrails

Do these the same evening as step 3, not later, particularly if the account has
moved off the Free Plan. Nothing here is running yet, so there is nothing to
panic about, but a public demo URL and no ceiling is a bad combination and the
in-code caps only exist once the Lambda is deployed.

- [ ] AWS Budgets: monthly budget 20 USD, alerts at 50 / 80 / 100 percent to
      your email.
- [ ] Cost Anomaly Detection enabled on the account, immediate alerts.
- [ ] **Request the $50 promotional credits.** Form closes **11 September 12:00
      PT** and the credits expire 31 October. Independent of everything else on
      this page, so do it tonight rather than in week three.

Budgets tell you after the money is gone. The caps in `src/whyf/limits.py` are
what actually stop it.

If a console message ever claims something changed about billing, check rather
than assume: Billing and Cost Management, then Bills for the current month, then
Free tier, then Credits. Free services that are commonly mistaken for chargeable
ones: IAM, IAM Identity Center, AWS Organizations, CloudFormation, Budgets
itself. What actually costs money on this project is Bedrock tokens, and nothing
else comes close.

---

## This week, not tonight

### 6. Registration paperwork

- [ ] Devpost account and hackathon registration.
- [ ] AWS Builder ID created. The submission form asks for it.
- [ ] Track selected: Professional Agents.

### 7. Search API key

Only the cold path uses it, so this is not urgent, but it has to exist before
tier 2 works end to end.

- [ ] Sign up for Tavily or Brave, get a key.
- [ ] Store it as a SecureString:

```bash
aws ssm put-parameter --name /whyf/search-api-key --type SecureString --value "PASTE_KEY" --region eu-west-1 --profile whyf
```

Nothing in the repo, nothing in `.env`, no literal in the CDK stack. The repo is
public and judges will read it.

### 8. Bootstrap for the first deploy

Claude Code does the deploy, but the account has to be bootstrapped once by you:

```bash
npx cdk bootstrap aws://ACCOUNT_ID/eu-west-1 --profile whyf
```

---

## Later, only if ahead

### 9. AgentCore

- [ ] Check whether Bedrock AgentCore is available in `eu-west-1` at all.

If it is not, the choice is: agent runtime in `us-east-1` with the site and data
staying in EU, or drop AgentCore. It helps the Technical Implementation score
and it is not required. Plain Lambda first, and never let this block week 2.

### 10. Before judging opens

- [ ] Demo URL public, free, unauthenticated, and up until 8 October.
- [ ] Daily spend ceiling in DynamoDB (`SPEND#`) set to something that survives
      a bad weekend without draining the credits.
- [ ] CloudWatch log retention set to 7 days so logs are not a line item.
- [ ] `private/` still gitignored. `python tools/check_publishable.py` before the
      repo goes public.

---

## Order of blocking

```
CLI  ->  build identity  ->  bedrock model access  ->  probe  ->  everything in src/
                         \->  cdk bootstrap  ->  first deploy

credits form                 independent, deadline 11 September
registration paperwork       independent
search API key               only blocks tier 2
```

Model access is the only true blocker for the code.

---

## Decision record: why Ireland

Three regions checked on 26 August, by catalog.

**`eu-central-1` Frankfurt.** No Anthropic models. Third-party only. First
choice, and it does not work.

**`eu-west-1` Ireland.** Claude Opus 5, Sonnet 5, Opus 4.8, Opus 4.7, Haiku 4.5,
plus the same third-party set. This is the one.

**`us-east-1` N. Virginia.** A much longer catalog - GPT-5.x, Grok, DeepSeek,
Kimi, GLM 5, Mistral Large 3 - but the **same five Anthropic models at the same
prices**, and the agent calls two of them. Third-party models run 10 to 15
percent cheaper there, which at these volumes is worth cents. Not a reason to
move processing out of the EU for a tool aimed at NIS2-adjacent companies.

No embedding model appeared in any of the three. Tier 1 does not need one.

The only thing that would reopen this is AgentCore landing in `us-east-1` and
not in Ireland. That is a week-3 decision and a one-line region change, not
something to pre-empt.
