"""Typed shapes for everything a model is allowed to return.

The model never writes a verdict string, a control number or a cost figure. It
selects: a concept id from a shortlist, a class, a form, and which of the six
verdicts applies. Everything rendered to the user comes from the card.

That is the whole anti-hallucination design, and it lives in these types.
"""
from typing import List, Literal, Optional

from pydantic import BaseModel, Field

VerdictId = Literal[
    "not-applicable", "already-solved", "write-it-down",
    "cheap-checkbox", "do-it-properly", "cannot-tell-yet",
]

QuestionClass = Literal["control", "disclosure", "admin", "attestation"]

QuestionForm = Literal[
    "binary_statement",   # "Backups are encrypted."
    "binary_question",    # "Are backups encrypted?"
    "maturity_ladder",    # four rungs, pick one
    "check_all",          # a list of sub-controls
    "admin_field",        # name, headcount, email
    "disclosure",         # have you ever been breached
]


class Classification(BaseModel):
    """What the classifier returns. Ids only, chosen from what it was given."""

    concept: str = Field(
        description="Concept id, chosen from the shortlist provided. Use the "
                    "literal string 'none' if none of them fit.")
    confidence: Literal["high", "medium", "low"]
    question_class: QuestionClass = Field(
        description="control for a security control. disclosure for a "
                    "statement of past fact such as breach history. admin for "
                    "company details like headcount. attestation for a claim "
                    "about holding a certificate or insurance.")
    form: QuestionForm
    negated: bool = Field(
        description="True when agreeing with the row means the opposite of "
                    "what it first appears. Rows carrying a double negative "
                    "about an exemption or an exclusion are the usual case.")
    translation_damage: bool = Field(
        description="True when the row reads as a bad translation or is so "
                    "mangled that its meaning is uncertain.")
    reasoning: str = Field(
        description="One sentence. Why this concept and not the others.",
        max_length=300)


class LadderPlacement(BaseModel):
    """Only asked for when the row arrived as a maturity ladder."""

    enough_rung: int = Field(ge=1, le=4)
    rung_asked_for: int = Field(
        ge=1, le=4,
        description="The rung this particular row is asking you to claim.")


class Reference(BaseModel):
    """A pointer into the curated library. Validated before rendering; unknown
    ids are dropped rather than shown."""

    kind: Literal["frameworks", "incidents", "patterns", "already_have"]
    id: str


class ColdVerdict(BaseModel):
    """The cold path, where there is no card. The model may write prose here,
    but it still may not invent a reference or a figure: `references` is
    validated against the library and anything unknown disappears.
    """

    verdict: VerdictId
    plain_english: str = Field(max_length=600)
    misunderstanding: str = Field(max_length=600)
    skeptic_case: str = Field(
        max_length=800,
        description="The honest argument for not doing this. Required. If "
                    "there genuinely is not one, say so in a sentence.")
    how_to_say_no: str = Field(
        max_length=600,
        description="Wording for the questionnaire's comment box if it does "
                    "not apply. States scope. Never asserts a fact about the "
                    "company.")
    security_value: int = Field(ge=0, le=3)
    checkbox_value: int = Field(ge=0, le=3)
    references: List[Reference] = Field(default_factory=list)
    unknown_territory: bool = Field(
        description="True when you are not confident. The tool says it does "
                    "not know rather than guessing, and that is a correct "
                    "answer.")


class Telemetry(BaseModel):
    tier: Literal["cache", "concept", "cold", "declined"]
    model_calls: int = 0
    searches: int = 0
    elapsed_s: float = 0.0
    degraded: bool = False
    degraded_reason: str = ""
    shortlist_size: int = 0
    dropped_references: dict = Field(default_factory=dict)


class Verdict(BaseModel):
    """What the UI renders. Assembled from a card wherever one exists."""

    question: str
    verdict: Optional[VerdictId] = None
    question_class: QuestionClass = "control"
    concept: Optional[str] = None
    concept_title: Optional[str] = None

    headline: str = ""
    subtitle: str = ""
    plain_english: str = ""
    misunderstanding: str = ""
    skeptic_case: str = ""
    how_to_say_no: str = ""
    response: str = ""            # non-control classes answer here instead
    refer_to: str = ""

    security_value: int = 0
    checkbox_value: int = 0
    cost_bands: dict = Field(default_factory=dict)
    evidence: dict = Field(default_factory=dict)
    maturity_ladder: dict = Field(default_factory=dict)
    deciding_question: Optional[dict] = None

    answer_risk: str = "none"
    references: dict = Field(default_factory=dict)
    reference_text: dict = Field(default_factory=dict)

    notes: List[str] = Field(default_factory=list)
    telemetry: Optional[Telemetry] = None
