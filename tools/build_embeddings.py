"""Embed the concept cards once, so the Lambda never has to.

Writes knowledge/embeddings.json: eighty vectors of 1024 floats, rounded to
five decimal places because the sixth changes nothing about a cosine and
doubles the file size.

The text embedded is built from the shipped card content only - the same
fields the lexical index uses - so this is reproducible from a clean checkout
and contains nothing from private/.

    python tools/build_embeddings.py --profile whyf
    python tools/build_embeddings.py --profile whyf --dry-run   # cost only
"""
import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from whyf.embed import DEFAULT_MODEL, DEFAULT_REGION, embed  # noqa: E402

CARDS = ROOT / "knowledge" / "concepts"
OUT = ROOT / "knowledge" / "embeddings.json"

# Titan Text Embeddings V2, per million input tokens. Only used to print an
# estimate before spending anything.
PRICE_PER_1M = 0.02


def card_text(card):
    """What the concept is, in the words that ship. Deliberately the same
    material the lexical index reads, so the two are compared fairly."""
    parts = [
        card.get("title", ""),
        card.get("plain_english", ""),
        card.get("misunderstanding", ""),
    ]
    parts += (card.get("aka") or [])
    parts += (card.get("common_form") or [])
    dq = card.get("deciding_question")
    if isinstance(dq, dict) and dq.get("text"):
        parts.append(dq["text"])
    return " ".join(p for p in parts if p).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", default=None)
    ap.add_argument("--region", default=DEFAULT_REGION)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    import yaml
    texts = {}
    for path in sorted(CARDS.glob("*.yaml")):
        card = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        texts[card.get("id") or path.stem] = card_text(card)

    tokens = sum(len(t.split()) for t in texts.values()) * 1.4
    print("{} cards, roughly {:.0f} tokens, about ${:.4f}".format(
        len(texts), tokens, tokens / 1_000_000 * PRICE_PER_1M))
    if args.dry_run:
        return 0

    if args.profile:
        os.environ["AWS_PROFILE"] = args.profile
    import boto3
    client = boto3.client("bedrock-runtime", region_name=args.region)

    vectors = {}
    for i, (cid, text) in enumerate(sorted(texts.items()), 1):
        vec = embed(text, client=client, model_id=args.model, region=args.region)
        vectors[cid] = [round(x, 5) for x in vec]
        print("\r  {}/{}  {}".format(i, len(texts), cid.ljust(36)), end="")
    print()

    OUT.write_text(json.dumps({
        "model": args.model,
        "dimensions": len(next(iter(vectors.values()))),
        "source": "knowledge/concepts, public card content only",
        "vectors": vectors,
    }), encoding="utf-8")
    print("wrote {} ({:.1f} MB)".format(
        OUT.relative_to(ROOT), OUT.stat().st_size / 1e6))
    return 0


if __name__ == "__main__":
    sys.exit(main())
