"""Normalising a pasted questionnaire row, and hashing it for the tier-0 cache.

Questionnaire rows get copy-pasted between companies endlessly, then mangled by
Word, by PDF extraction, by translation, and by whoever renumbered the sheet.
Two rows that mean the same thing arrive looking different:

    "Laptop and phone storage is encrypted."
    "40. Laptop and phone storage is encrypted. *"
    "Is laptop and phone storage encrypted?"

The first two must hash the same, because that is a free cache hit and zero
model calls. The third is a different surface form of the same concept and is
tier 1's problem, not tier 0's.

This module is also what stops the corpus from double-counting. The same vendor
questionnaire turned up twice in the source files, and a corpus that counts it
twice reports a coverage number that is a lie.
"""
import hashlib
import re
import unicodedata

# Question numbering, section prefixes and the required-field asterisk. All
# noise; none of it changes what is being asked.
LEADING_NUMBER = re.compile(r"^\s*\(?\d{1,3}[a-z]?[.):]\s*")
TRAILING_MARKS = re.compile(r"[\s*·•]+$")
BULLETS = re.compile(r"^[\s•□☐*\-]+")

# Filler that survives translation but carries no meaning for matching.
STOPWORDS = frozenset("""
a an the is are was were be been being do does did has have had
of to in on at for from with by and or that this these those your our their its
""".split())


def clean_text(text: str) -> str:
    """Human-readable normalisation. Keeps words, drops formatting damage."""
    text = unicodedata.normalize("NFKC", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Cf")
    text = text.replace(" ", " ")
    # "organiza- tion" -> "organization", from PDF line breaks
    text = re.sub(r"(\w)-\s+(\w)", r"\1\2", text)
    text = BULLETS.sub("", text)
    text = LEADING_NUMBER.sub("", text)
    text = TRAILING_MARKS.sub("", text)
    return re.sub(r"\s+", " ", text).strip()


def canonical(text: str) -> str:
    """Aggressive form used only for hashing and duplicate detection.

    Lowercased, punctuation stripped, stopwords dropped, words sorted. Sorting
    is what makes "Is a DLP solution implemented?" and "A DLP solution is
    implemented." collide, which is the whole point - the statement form and
    the question form of one row are the same row.
    """
    text = clean_text(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    words = [w for w in text.split() if w not in STOPWORDS and len(w) > 1]
    return " ".join(sorted(words))


def row_hash(text: str) -> str:
    """Tier-0 cache key. Stable across releases - changing it empties the cache."""
    return hashlib.sha256(canonical(text).encode("utf-8")).hexdigest()


def looks_like_statement(text: str) -> bool:
    """Statement form ("Backups are encrypted.") vs question form ("Are backups
    encrypted?"). The classifier needs to know, because a statement is an
    assertion the user is being asked to agree with, and agreeing is the
    contractual act the tool refuses to perform on their behalf."""
    t = clean_text(text)
    return not t.endswith("?")
