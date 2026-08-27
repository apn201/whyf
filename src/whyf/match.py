"""Tier 1: match a pasted row to a concept, without calling a model.

The original plan was to embed the question with Titan and cosine it against a
pre-embedded concept catalog. That plan had a dependency nobody needed: an
embedding model, in the right region, with an API call and a bill on every
cache miss.

Eighty concepts is small. Small enough that a TF-IDF index over the cards, with
cosine in pure Python, does the same job in under a millisecond for nothing. No
embedding model, no vector database, no numpy, no container image. Tier 1 now
costs zero model calls instead of one.

The index is built from the card content that ships - title, plain English,
synthetic examples, the concept id itself. It never reads the real
questionnaires, so a clean checkout builds exactly the same index.

    from whyf.match import ConceptMatcher
    m = ConceptMatcher.from_cards()
    m.match("Are laptop drives encrypted?")
    # [Match(concept='full-disk-encryption', score=0.71), ...]
"""
import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from .normalise import clean_text

from .paths import find_knowledge

CARDS = find_knowledge(__file__) / "concepts"

# Words that appear in nearly every questionnaire row and carry no signal.
# Left deliberately short: idf already handles most of it, and an aggressive
# stoplist throws away the difference between "is encrypted" and "encrypt".
NOISE = frozenset("""
a an the is are was were be been being do does did has have had of to in on at
for from with by and or that this these those your our their its it as not no
you we they i organisation organization organization's company companies
security information please describe following all any each such
""".split())

TOKEN = re.compile(r"[a-z0-9]+")


def tokens(text):
    """Words, lowercased, with a crude suffix trim so plural and participle
    forms collide. Not a real stemmer; a real one is a dependency and this is
    a matcher over eighty short documents."""
    out = []
    for w in TOKEN.findall(clean_text(text).lower()):
        if w in NOISE or len(w) < 2:
            continue
        for suffix in ("ations", "ation", "ing", "ies", "ed", "es", "s"):
            if len(w) > len(suffix) + 3 and w.endswith(suffix):
                w = w[: -len(suffix)]
                break
        out.append(w)
    return out


@dataclass(frozen=True)
class Match:
    concept: str
    score: float

    def __repr__(self):
        return "Match({!r}, {:.2f})".format(self.concept, self.score)


class ConceptMatcher:
    """TF-IDF over the concept cards, cosine at query time."""

    def __init__(self, documents):
        #: concept id -> raw term counts
        self.documents = documents
        n = len(documents) or 1
        df = Counter()
        for terms in documents.values():
            df.update(set(terms))
        self.idf = {
            t: math.log((n + 1) / (c + 1)) + 1.0 for t, c in df.items()
        }
        self.vectors = {cid: self._vector(terms)
                        for cid, terms in documents.items()}

    def _vector(self, terms):
        counts = Counter(terms)
        vec = {t: (1 + math.log(c)) * self.idf.get(t, 1.0)
               for t, c in counts.items()}
        norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
        return {t: v / norm for t, v in vec.items()}

    def match(self, text, limit=3):
        """Best concepts for a pasted row, most likely first."""
        query = self._vector(tokens(text))
        scored = []
        for cid, vec in self.vectors.items():
            if len(query) > len(vec):
                small, large = vec, query
            else:
                small, large = query, vec
            score = sum(w * large.get(t, 0.0) for t, w in small.items())
            if score > 0:
                scored.append(Match(cid, score))
        scored.sort(key=lambda m: (-m.score, m.concept))
        return scored[:limit]

    def confident(self, text, floor=0.20, margin=1.25):
        """The concept, or None when tier 1 should give up and let tier 2 run.

        Two ways to be unsure: nothing scored well, or the top two scored too
        close together. Both mean the same thing to the agent - do not guess,
        it costs more to be wrong here than to spend a model call."""
        top = self.match(text, limit=2)
        if not top or top[0].score < floor:
            return None
        if len(top) > 1 and top[1].score > 0 and \
                top[0].score / top[1].score < margin:
            return None
        return top[0]

    # ---- building -------------------------------------------------------

    @classmethod
    def from_cards(cls, path=None):
        """Build from the shipped cards. Field weights are repetition: the
        title is worth more than an example sentence, so it goes in more than
        once."""
        try:
            import yaml
        except ImportError:
            raise RuntimeError("pyyaml is needed to build the index from cards")

        path = Path(path or CARDS)
        documents = {}
        for card_file in sorted(path.glob("*.yaml")):
            card = yaml.safe_load(card_file.read_text(encoding="utf-8")) or {}
            cid = card.get("id") or card_file.stem
            parts = []
            parts += tokens(cid.replace("-", " ")) * 4
            parts += tokens(card.get("title", "")) * 4
            parts += tokens(card.get("plain_english", "")) * 2
            for phrase in (card.get("aka") or []):
                parts += tokens(phrase) * 3
            for example in (card.get("common_form") or []):
                parts += tokens(example) * 2
            parts += tokens(card.get("misunderstanding", ""))
            dq = card.get("deciding_question") or {}
            parts += tokens(dq.get("text", "") if isinstance(dq, dict) else "")
            documents[cid] = parts
        return cls(documents)
