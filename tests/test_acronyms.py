"""Acronyms are a retrieval problem, so these test retrieval, not wording."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from whyf.acronyms import expand  # noqa: E402
from whyf.normalise import row_hash  # noqa: E402


def test_expansion_appends_and_never_replaces():
    out = expand("Do you have PAM?")
    assert "PAM" in out                       # original wording survives
    assert "privileged" in out


def test_unknown_text_is_untouched():
    assert expand("Are backups encrypted?") == "Are backups encrypted?"


def test_case_insensitive():
    assert "privileged" in expand("do you have pam?")


def test_only_whole_words():
    # "pam" inside another word must not fire, or "tampering" expands.
    assert expand("Is there hardware tampering detection?") == \
        "Is there hardware tampering detection?"


def test_soc_two_is_the_report_not_the_team():
    assert "operations centre" not in expand("Are you SOC 2 certified?")
    assert "operations centre" in expand("Do you have a SOC?")


def test_cache_key_is_unaffected():
    # Expansion is for matching only. If it reached the tier-0 hash, two
    # different rows could collide onto one cached verdict.
    assert row_hash("Do you have PAM?") != row_hash(expand("Do you have PAM?"))


def test_every_expansion_is_lowercase_words():
    from whyf.acronyms import GLOSSARY
    for acronym, expansion in GLOSSARY.items():
        assert acronym.islower(), acronym
        assert expansion == expansion.lower(), acronym
