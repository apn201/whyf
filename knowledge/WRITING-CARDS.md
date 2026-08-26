# Writing the cards

The cards are the product. Everything else is plumbing that can be rebuilt in a
weekend. Read `concepts/rpo.yaml` first - it is filled in end to end and is the
target shape, tone and length.

## Where the material is

Cards live in `knowledge/concepts/` and ship. The questionnaire rows they were
built from do not - they belong to the companies that wrote them. While writing
a card, open `private/context/<concept>.md` beside it: that file has how the
question is really asked across all three source questionnaires, its framework
references, its relevance rating, and its peer benchmark if one exists.

Read from the context file. Write into the card, in your own words. Nothing from
the context file may appear verbatim in a card, and `python tools/check.py` fails the
build if it does.

## Editing a card

The cards in `knowledge/concepts/` are generated. Do not edit them directly or
the next render overwrites you. The prose lives in `tools/content/*.py`, one
dict per concept, which is what keeps eighty cards the same shape.

```bash
python tools/render_cards.py
```

Same for the pattern and already-have libraries: content in
`tools/library_content.py`, rendered by `python tools/render_library.py`.

Then check it:

```bash
python tools/check.py
```

That runs the schema validator, the publication check and the tests. The
publication check is not optional. Writing a card while reading the real
questionnaire in `private/context/` is exactly how source wording ends up in a
public file, and it caught eight such phrases the first time these cards were
written.

`status` goes `skeleton` -> `draft` -> `done`. A card marked `done` that still
contains `TODO`, or that cites a pattern or incident which is itself
unfinished, fails the build. That second rule matters: the id would resolve, so
the agent would happily render an empty reference at a user.

## Two kinds of card

`class:` decides which template a card uses and what the agent is allowed to do
with it.

**`control`** - a security control. Gets one of the six verdicts. 76 of the 80.

**`disclosure`**, **`admin`**, **`attestation`** - not controls, and they must
never receive a verdict. The validator enforces this. They exist because the
second corpus asks whether the company has ever been breached, and how many
staff it has. Pretending either is a control would be dishonest in a way that
eventually hurts someone.

The disclosure cards matter most. Answering "no" to a breach-history question
when the answer is "yes" is not a failed control, it is a misrepresentation
that can void a cyber insurance policy. The card's `response` field must say
that the tool will not help word the answer, and `refer_to` must name who the
user should actually talk to. This is the hard rule from the project definition
at its sharpest: the tool explains, it does not answer.

## Order of work

`validate_cards.py` ranks the remaining cards by how many corpus rows each one
unlocks and shows the running coverage. That is the stopping rule: you can see
what "I have written 25 cards" is actually worth before you write them.

The three demo cards come first regardless, because presentation is a fifth of
the score:

1. `ics-inventory` - the "does not apply to you" beat (q1 line 11, cartography)
2. `dlp` - the cheap checkbox vs expensive fix beat (q1 line 31)
3. `rpo` - the tap question that flips the verdict (q1 line 8). Already drafted.

Then follow the ranking. Then the 15 `already-have` cards, which are short and
close out corpus rows on their own. Then `patterns`. Incidents last - they are
decoration next to the verdict and they are the slowest to verify.

## Field notes

**plain_english** - the first thing the user reads. Someone who runs a 30-person
company and has never heard the acronym. Two sentences maximum. If you write "in
order to ensure", start again.

**misunderstanding** - the "why the f" answer. RPO: "nightly backups mean you
already decided on 24 hours, you just did not decide it on purpose."

**skeptic_case** - the honest argument for not doing it, written as an argument
rather than a caveat. The Skeptic agent gets it verbatim. If you genuinely
cannot write one, say so in the field: "There isn't one. Do this." That reads as
strong precisely because it is rare.

**maturity_ladder** - the field the second corpus forced into existence, and the
most valuable one on the card.

A large share of the corpus is four-rung ladders: not implemented / some systems
/ all systems / all systems, risk-based, reviewed annually. Rung 4 is written by
somebody who sells rung 4.

There is a peer benchmark in `private/benchmarks.yaml` for 35 control areas, and
`private/context/*.md` will tell you when one exists for the concept you are
writing. Read it, but read the scope note with it: it comes from an industrial
manufacturer's assessment, regulated sectors score higher, and the source does
not even say whether the column is a sector average or a global one. It tells
you the shape - real companies cluster mid-ladder and the top rung is rare in
that segment - not a number to copy.

So `enough_rung` is a judgement per concept **and** per sector. A bank is not the
peer group of a packaging plant, and a card that assumes otherwise is wrong for
half its readers. Where the answer genuinely differs by sector, say so in
`why_not_4` rather than picking one and hoping.

`enough_rung` is which rung a sane company should answer and stop at.
`why_not_4` is what the last rung costs and what it buys. Each rung carries the
verdict it produces, so the UI can show the ladder with the answer highlighted
and the price of climbing next to it. If `question_forms` includes
`maturity_ladder`, a card cannot reach `done` without this block.

**how_to_say_no** - verbatim scope wording for the comment box. It states scope.
It never asserts a fact about the company. "Not applicable - this control
assumes X, we do not do X." Never "we have implemented".

**deciding_question** - one fact that moves the verdict. Symbols and buttons, no
typing, four options at most, each carrying its verdict and a one-line `why`. If
the verdict genuinely never moves, set it to `null` and say why in
`skeptic_case`.

**security_value / checkbox_value** - both 0-3. The gap is the entire product.
`dlp` should be roughly security 1, checkbox 3. `mfa` should be 3 and 3. If both
are equal and low, ask whether the concept earns a card at all.

**answer_risk** - `none`, `disclosure`, `warranty` or `certification`. Anything
other than `none` makes the UI put a warning above the verdict.

**frameworks / incidents / patterns / already_have** - ids only, and the id must
exist in the library or the validator rejects the card. Deliberate, and the same
rule the runtime applies to model output: an id the model invents is dropped
before rendering rather than shown to a user. It is the mitigation for the one
risk that can kill the submission.

The generated block at the bottom of each card now includes
`suggested_frameworks`, pulled from the Annex I crosswalk via whichever CSF 2.0
subcategories map to the concept. Those are real ids from a real mapping, not
model output. Copy the two or three that matter up into `frameworks:`. Do not
cite all nine - a verdict that lists nine control references reads as padding.

## What is left

Everything except the incidents. Those are the one thing that cannot be written
from the outside.

## Incidents

Twelve records in `incidents/`, all blank on purpose. No figure was prefilled,
because a figure that came out of a model is exactly the thing that gets
fact-checked and ends the submission. Fill `source_url` first, then the figure,
then `basis`. A cost figure without a basis is a validation error.

If you cannot source a number, delete the field. The card still works.

## Re-shaping the catalog

`tools/corpus_map.py` holds the concept catalog and maps every corpus row to
exactly one concept. `q1` is mapped by hand, line by line. `q2` and `q3` are
matched by each concept's `rules` list, first match in dict order, with
`OVERRIDES` for the stubborn ones. Those rules are not throwaway - they are the
deterministic first pass the tier-0 classifier uses before any model runs.

```bash
python tools/corpus_map.py
```

Reports coverage per source, duplicate rows across sources, and anything no
rule claimed. Then:

```bash
python tools/gen_skeletons.py
```

Creates missing cards and refreshes the generated block on existing ones.
`--migrate` additionally rewrites cards still at `status: skeleton` from the
current template, and never touches anything at `draft` or `done`.
