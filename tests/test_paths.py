"""The knowledge base has to be findable, and its absence has to be loud.

An empty cards directory is not an error anywhere downstream: the index builds,
the shortlist comes back empty, and the agent declines every question quickly
and politely. That shipped once. These tests are the tripwire.
"""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from whyf.match import CARDS, ConceptMatcher  # noqa: E402
from whyf.paths import find_knowledge  # noqa: E402


def test_cards_directory_resolves():
    assert CARDS.is_dir(), CARDS


def test_index_is_not_empty():
    # The specific failure: a deployed agent that declines everything because
    # it was looking one directory too high.
    matcher = ConceptMatcher.from_cards()
    assert len(matcher.documents) > 50


def test_missing_knowledge_raises_rather_than_returning_nothing(tmp_path):
    with pytest.raises(RuntimeError):
        find_knowledge(tmp_path / "nowhere" / "deep" / "file.py")


def test_env_override_wins(tmp_path, monkeypatch):
    monkeypatch.setenv("WHYF_KNOWLEDGE", str(tmp_path))
    assert find_knowledge(__file__) == tmp_path
