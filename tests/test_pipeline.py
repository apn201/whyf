"""The agent, without touching Bedrock.

Everything here runs offline. The parts that need a model are the classifier
and the embedding call, and both are supposed to degrade rather than fail, so
the offline path is a real path and worth testing rather than mocking around.
"""
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from whyf import render  # noqa: E402
from whyf.cache import UNAVAILABLE, MemoryCache  # noqa: E402
from whyf.knowledge.library import load as load_library  # noqa: E402
from whyf.schema import Telemetry, Verdict  # noqa: E402


@pytest.fixture(scope="module")
def library():
    return load_library()


# ---- the anti-hallucination layer -----------------------------------------

def test_an_invented_reference_is_dropped(library):
    kept, dropped = library.validate_references({
        "frameworks": ["nis2-art21", "nis2-art9999"],
        "patterns": ["documentation-only", "made-up-pattern"],
    })
    assert kept["frameworks"] == ["nis2-art21"]
    assert dropped["frameworks"] == ["nis2-art9999"]
    assert kept["patterns"] == ["documentation-only"]


def test_unfinished_library_entries_are_treated_as_absent(library):
    """An incident card still at skeleton has no sourced figures in it. Citing
    one would render an empty reference at a user, which is the exact failure
    the id scheme exists to prevent."""
    kept, dropped = library.validate_references(
        {"incidents": ["maersk-notpetya"]})
    finished = library.incidents.get("maersk-notpetya")
    if finished is None:
        assert kept["incidents"] == []
        assert dropped["incidents"] == ["maersk-notpetya"]


def test_every_shipped_card_renders(library):
    """Rendering is deterministic and must not depend on a card's contents
    being convenient."""
    for cid, card in library.concepts.items():
        v = render.from_card("does this render", card, library)
        assert isinstance(v, Verdict)
        assert v.concept == cid
        if card.get("class") == "control":
            assert v.verdict, cid
            assert v.headline, cid
        else:
            assert v.verdict is None, "{} is not a control".format(cid)


# ---- the tap question ------------------------------------------------------

def test_tapping_an_option_changes_the_verdict(library):
    card = library.concept("rpo")
    options = {o["id"]: o for o in card["deciding_question"]["options"]}
    before = render.from_card("q", card, library).verdict

    after_bad = render.answered("q", card, library, options["no_way"])
    after_fine = render.answered("q", card, library, options["yes_fine"])

    assert after_bad.verdict == "do-it-properly"
    assert after_fine.verdict == "write-it-down"
    assert after_bad.verdict != before
    assert after_bad.deciding_question is None, "asked and answered"
    assert "Changed from" in after_bad.notes[0]


def test_every_deciding_option_names_a_real_verdict(library):
    from whyf.verdicts import resolve
    for cid, card in library.concepts.items():
        dq = card.get("deciding_question") or {}
        for opt in (dq.get("options") or []):
            resolve(opt["verdict"])          # raises if invented


# ---- the cache and the ceiling ---------------------------------------------

def test_the_cache_collapses_a_renumbered_row():
    from whyf.normalise import row_hash
    cache = MemoryCache()
    v = Verdict(question="Backups are encrypted.", verdict="already-solved")
    cache.put(row_hash("Backups are encrypted."), v)
    assert cache.get(row_hash("32. BACKUPS ARE ENCRYPTED. *")) is not None
    assert cache.hits == 1


def test_an_unreachable_counter_is_not_a_spent_one():
    """Conflating them is how a transient DynamoDB error turns into an agent
    that quietly stops thinking."""
    assert UNAVAILABLE is not None
    assert UNAVAILABLE != 0


# ---- the handler -----------------------------------------------------------

def test_handler_rejects_an_empty_question():
    from whyf.handler import handler
    r = handler({"rawPath": "/", "requestContext": {"http": {"method": "POST"}},
                 "body": json.dumps({"question": "   "})})
    assert r["statusCode"] == 400


def test_handler_rejects_a_whole_column():
    from whyf.handler import handler
    r = handler({"rawPath": "/", "requestContext": {"http": {"method": "POST"}},
                 "body": json.dumps({"question": "x " * 1500})})
    assert r["statusCode"] == 413


def test_handler_answers_a_tap_without_a_model(library):
    from whyf.handler import handler
    r = handler({
        "rawPath": "/answer",
        "requestContext": {"http": {"method": "POST"}},
        "body": json.dumps({"question": "q", "concept": "rpo",
                            "option": "no_way"}),
    })
    assert r["statusCode"] == 200
    body = json.loads(r["body"])
    assert body["verdict"] == "do-it-properly"
    assert body["telemetry"]["model_calls"] == 0


def test_handler_never_leaks_a_stack_trace():
    from whyf.handler import handler
    r = handler({"rawPath": "/", "requestContext": {"http": {"method": "POST"}},
                 "body": "not json at all"})
    assert r["statusCode"] == 400
    assert "Traceback" not in r["body"]
