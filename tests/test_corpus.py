"""Guard the corpus. These run in `make check` and must never be skipped.

The point is not coverage. It is that the things which can kill the submission
fail loudly at build time: an unmapped question, a fabricated reference id, a
non-control question that got handed a verdict it has no business having, and
a corpus that quietly counts the same questionnaire twice.
"""
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))

from corpus_map import (CONCEPTS, build_map, check_q1, duplicates,  # noqa: E402
                        has_private, load_rows)
from whyf.normalise import canonical, looks_like_statement, row_hash  # noqa: E402
from whyf.verdicts import VERDICTS, resolve  # noqa: E402


@pytest.fixture(scope="module")
def rows():
    return load_rows()


@pytest.fixture(scope="module")
def cards():
    return {p.stem: yaml.safe_load(p.read_text(encoding="utf-8"))
            for p in (ROOT / "knowledge" / "concepts").glob("*.yaml")}


# ---- the corpus -----------------------------------------------------------

def test_q1_is_hand_mapped_completely_and_disjointly(rows):
    missing, unknown, dupes = check_q1(rows)
    assert not missing, "unmapped questions.txt lines: {}".format(missing)
    assert not unknown, "mapped lines that do not exist: {}".format(unknown)
    assert not dupes, "lines mapped to two concepts: {}".format(dupes)


def test_every_corpus_row_reaches_a_concept(rows):
    assigned, unmapped = build_map(rows)
    assert not unmapped, "{} rows no rule claimed: {}".format(
        len(unmapped), unmapped[:10])
    assert len(assigned) == len(rows)


def test_the_synthetic_corpus_always_loads(rows):
    """The public corpus. It has to be there on any checkout, because it is the
    only one a judge gets."""
    assert {r["source"] for r in rows.values()} >= {"syn"}


def test_the_real_sources_load_when_present(rows):
    if not has_private():
        pytest.skip("private/ not on this machine")
    assert {r["source"] for r in rows.values()} >= {"q1", "q2", "q3"}


def test_the_repo_works_without_private():
    """A clean checkout has no private/. Everything must still map, or the
    setup instructions in the README do not actually work from clean."""
    rows = load_rows(private=False)
    assert rows, "no synthetic corpus"
    assigned, unmapped = build_map(rows)
    assert not unmapped
    assert {CONCEPTS[c]["class"] for c in assigned.values()} == {
        "control", "disclosure", "admin", "attestation"}, (
        "the synthetic corpus must exercise all four question classes")


def test_every_concept_has_a_synthetic_row():
    rows = load_rows(private=False)
    assigned, _ = build_map(rows)
    gaps = sorted(set(CONCEPTS) - set(assigned.values()))
    assert not gaps, "concepts a clean checkout cannot demonstrate: {}".format(gaps)


def test_corpus_has_no_duplicate_rows(rows):
    dupes = duplicates(rows)
    assert not dupes, (
        "the same question arrives from two sources, which would inflate every "
        "coverage number: {}".format(list(dupes.values())[:5]))


def test_every_concept_has_a_card(cards):
    assert set(CONCEPTS) == set(cards), (
        "run `python tools/gen_skeletons.py`. missing: {} orphaned: {}".format(
            set(CONCEPTS) - set(cards), set(cards) - set(CONCEPTS)))


# ---- normalisation, which is also the tier-0 cache key --------------------

def test_numbering_and_asterisks_do_not_change_the_hash():
    bare = "Laptop and phone storage is encrypted."
    decorated = "40. Laptop and phone storage is encrypted. *"
    assert row_hash(bare) == row_hash(decorated)


def test_statement_and_question_forms_collide():
    assert row_hash("Laptop and phone storage is encrypted.") == \
           row_hash("Is laptop and phone storage encrypted?")


def test_pdf_hyphenation_damage_is_repaired():
    assert canonical("across the organiza- tion") == canonical("across the organization")


def test_statement_form_is_detected():
    assert looks_like_statement("Backups are encrypted.")
    assert not looks_like_statement("Are backups encrypted?")


# ---- the verdict vocabulary -----------------------------------------------

def test_there_are_exactly_six_verdicts():
    assert len(VERDICTS) == 6


def test_an_invented_verdict_raises():
    with pytest.raises(ValueError):
        resolve("probably-fine")


def test_need_one_fact_is_an_alias_not_a_seventh_verdict():
    assert resolve("need-one-fact") is resolve("cannot-tell-yet")


def test_only_control_cards_carry_a_verdict(cards):
    offenders = [cid for cid, c in cards.items()
                 if c.get("class") != "control" and c.get("default_verdict")]
    assert not offenders, (
        "these are not security controls and must not be given one of the six "
        "verdicts: {}".format(offenders))


def test_disclosure_cards_declare_their_answer_risk(cards):
    for cid, c in cards.items():
        if c.get("class") == "disclosure":
            assert c.get("answer_risk") == "disclosure", (
                "{} is a disclosure question; answering it wrong is a "
                "misrepresentation, and the card must say so".format(cid))


# ---- the whole corpus ------------------------------------------------------

def test_corpus_validator_passes():
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "validate_cards.py")],
        capture_output=True, text=True, cwd=ROOT,
    )
    assert result.returncode == 0, result.stdout + result.stderr


# ---- the peer benchmark ----------------------------------------------------

BENCHMARKS = ROOT / "private" / "benchmarks.yaml"


@pytest.mark.skipif(not BENCHMARKS.exists(),
                    reason="benchmarks.yaml is optional; it may have been "
                           "removed for publication")
def test_benchmark_areas_all_point_at_real_concepts():
    data = yaml.safe_load(BENCHMARKS.read_text(encoding="utf-8"))
    unknown = [e["area"] for e in data["control_areas"]
               if e["concept"] not in CONCEPTS]
    assert not unknown, "benchmark areas with no concept: {}".format(unknown)


@pytest.mark.skipif(not BENCHMARKS.exists(), reason="benchmarks.yaml is optional")
def test_benchmark_carries_no_assessed_company_data():
    """The benchmark came out of one named company's confidential report. Only
    the peer column may cross over - never that company's own scores, and never
    anything that identifies it."""
    text = BENCHMARKS.read_text(encoding="utf-8").lower()
    # The identifiers themselves live in tools/check_publishable.py, which is
    # the one file allowed to name them. Reuse that list rather than repeating
    # it here and turning the test suite into its own leak.
    sys.path.insert(0, str(ROOT / "tools"))
    from check_publishable import IDENTIFIERS
    for leak in list(IDENTIFIERS) + ["your_score", "your score"]:
        assert leak not in text, "possible leak from the source report: {!r}".format(leak)


@pytest.mark.skipif(not BENCHMARKS.exists(), reason="benchmarks.yaml is optional")
def test_the_benchmark_states_its_scope():
    """It is one segment's benchmark, not a statement about companies in
    general - a bank is not the peer group of a packaging plant. Anything read
    off it has to carry that, so the file has to say it."""
    data = yaml.safe_load(BENCHMARKS.read_text(encoding="utf-8"))
    assert data.get("segment"), "benchmark with no stated segment is unusable"
    assert data.get("pool_unclear") is True


# ---- publication safety ----------------------------------------------------

def test_nothing_private_has_leaked_into_the_publishable_tree():
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "check_publishable.py")],
        capture_output=True, text=True, cwd=ROOT,
    )
    assert result.returncode == 0, result.stdout + result.stderr


# ---- tier 1: the lexical matcher -------------------------------------------

def test_the_index_builds_from_public_cards_only():
    """A clean checkout must produce the same index. If this ever needs
    private/ the deployment breaks in a way that only shows up in the cloud."""
    from whyf.match import ConceptMatcher
    m = ConceptMatcher.from_cards()
    assert set(m.documents) == set(CONCEPTS)


def test_the_matcher_shortlists_the_right_concept(rows):
    """Tier 1 hands the classifier a shortlist rather than an answer. What
    matters is recall at the shortlist width, not top-1 accuracy."""
    if not has_private():
        pytest.skip("recall is only meaningful against the real questionnaires")
    from whyf.match import ConceptMatcher
    m = ConceptMatcher.from_cards()
    truth, _ = build_map(rows)
    real = {r: v for r, v in rows.items() if v["source"] != "syn"}
    hit = sum(1 for rid, r in real.items()
              if truth[rid] in [g.concept for g in m.match(r["question"], limit=15)])
    recall = hit / len(real)
    assert recall > 0.75, (
        "shortlist recall dropped to {:.0%}. Either the cards changed or the "
        "index weights need looking at.".format(recall))


def test_the_matcher_declines_when_it_is_unsure():
    from whyf.match import ConceptMatcher
    m = ConceptMatcher.from_cards()
    assert m.confident("what is the weather like in helsinki today") is None
