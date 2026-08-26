"""Tier 1, the paid half: embed the question and cosine it against the cards.

The concept vectors are built once at build time by tools/build_embeddings.py
and shipped in knowledge/embeddings.json. At runtime only the pasted question
gets embedded, which is one small Bedrock call, and the cosine runs in pure
Python over eighty vectors. No numpy, no vector database, nothing to deploy
alongside the Lambda.

Whether this is worth the call over the free lexical index in match.py is a
measured question, not an assumed one. See tools/compare_tier1.py.
"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
VECTORS = ROOT / "knowledge" / "embeddings.json"

DEFAULT_MODEL = "amazon.titan-embed-text-v2:0"
DEFAULT_REGION = "eu-west-1"


def embed(texts, client=None, model_id=DEFAULT_MODEL, region=DEFAULT_REGION,
          dimensions=1024):
    """Embed one string or a list of them. Titan has no batch endpoint, so a
    list is a loop; that is fine for eighty cards at build time and irrelevant
    at runtime, where it is always one."""
    if client is None:
        import boto3
        client = boto3.client("bedrock-runtime", region_name=region)
    single = isinstance(texts, str)
    out = []
    for text in ([texts] if single else texts):
        body = json.dumps({"inputText": text, "dimensions": dimensions,
                           "normalize": True})
        response = client.invoke_model(modelId=model_id, body=body)
        out.append(json.loads(response["body"].read())["embedding"])
    return out[0] if single else out


def cosine(a, b):
    """Titan returns normalised vectors, so this is a dot product. The norms
    are computed anyway because a cached vector may have been rounded on the
    way into the JSON file."""
    dot = na = nb = 0.0
    for x, y in zip(a, b):
        dot += x * y
        na += x * x
        nb += y * y
    if not na or not nb:
        return 0.0
    return dot / math.sqrt(na * nb)


class EmbeddingMatcher:
    """Cosine against the pre-embedded concept catalog."""

    def __init__(self, vectors, client=None, model_id=DEFAULT_MODEL,
                 region=DEFAULT_REGION):
        self.vectors = vectors
        self.client = client
        self.model_id = model_id
        self.region = region

    @classmethod
    def load(cls, path=None, **kwargs):
        path = Path(path or VECTORS)
        if not path.exists():
            raise FileNotFoundError(
                "no embeddings at {}. Run tools/build_embeddings.py, or leave "
                "`embedding` empty in infra/config.yaml and let the lexical "
                "index handle tier 1.".format(path))
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls(data["vectors"], **kwargs)

    def match(self, text, limit=3, query_vector=None):
        from .match import Match
        q = query_vector if query_vector is not None else embed(
            text, client=self.client, model_id=self.model_id, region=self.region)
        scored = [Match(cid, cosine(q, v)) for cid, v in self.vectors.items()]
        scored.sort(key=lambda m: (-m.score, m.concept))
        return scored[:limit]


def hybrid(lexical, embedding_matcher, text, limit=3, query_vector=None,
           weight=0.5):
    """Both, blended. Lexical is free and catches exact vocabulary; embeddings
    catch the paraphrase. Where they agree the score compounds, which is what
    makes the confidence check upstream meaningful."""
    from .match import Match
    lex = {m.concept: m.score for m in lexical.match(text, limit=None or 999)}
    emb = {m.concept: m.score for m in embedding_matcher.match(
        text, limit=999, query_vector=query_vector)}

    def norm(scores):
        top = max(scores.values()) if scores else 0.0
        return {k: (v / top if top else 0.0) for k, v in scores.items()}

    lex, emb = norm(lex), norm(emb)
    blended = [
        Match(cid, weight * emb.get(cid, 0.0) + (1 - weight) * lex.get(cid, 0.0))
        for cid in set(lex) | set(emb)
    ]
    blended.sort(key=lambda m: (-m.score, m.concept))
    return blended[:limit]
