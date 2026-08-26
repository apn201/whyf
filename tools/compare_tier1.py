"""Measure tier 1 three ways against the real corpus, then decide.

Lexical is free and instant. Embeddings cost one Bedrock call per request.
Hybrid costs the same call and adds nothing at runtime. Which one to ship is a
measured question, and this is the measurement.

Ground truth is the concept map. Note that only q1 is hand-mapped; q2 and q3
labels come from the regex rules in private/rules.py, so treat the q1 column as
the trustworthy one and the rest as indicative.

    python tools/compare_tier1.py --profile whyf
    python tools/compare_tier1.py --profile whyf --limit 120   # cheaper sample
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))

from corpus_map import build_map, load_rows  # noqa: E402
from whyf.embed import EmbeddingMatcher, embed, hybrid  # noqa: E402
from whyf.match import ConceptMatcher  # noqa: E402

CACHE = Path(ROOT / "private" / "question-vectors.json")


def recall_at(results, want, k):
    return want in [m.concept for m in results[:k]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", default=None)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--weight", type=float, default=0.5)
    args = ap.parse_args()

    if args.profile:
        os.environ["AWS_PROFILE"] = args.profile

    rows = load_rows()
    truth, _ = build_map(rows)
    real = {rid: r for rid, r in rows.items() if r["source"] != "syn"}
    if args.limit:
        real = dict(sorted(real.items())[: args.limit])

    lex = ConceptMatcher.from_cards()
    emb = EmbeddingMatcher.load()

    # Embedding every question is the only cost here, so cache it. Questions
    # come from private/, so the cache lives there too.
    cache = {}
    if CACHE.exists():
        cache = json.loads(CACHE.read_text(encoding="utf-8"))
    todo = [rid for rid in real if rid not in cache]
    if todo:
        import boto3
        client = boto3.client("bedrock-runtime", region_name="eu-west-1")
        print("embedding {} questions...".format(len(todo)))
        for i, rid in enumerate(todo, 1):
            cache[rid] = [round(x, 5) for x in
                          embed(real[rid]["question"], client=client)]
            if i % 25 == 0:
                print("  {}/{}".format(i, len(todo)))
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        CACHE.write_text(json.dumps(cache), encoding="utf-8")

    methods = {
        "lexical (free)": lambda r, v: lex.match(r["question"], limit=20),
        "embedding": lambda r, v: emb.match(r["question"], limit=20,
                                            query_vector=v),
        "hybrid {:.0%}".format(args.weight):
            lambda r, v: hybrid(lex, emb, r["question"], limit=20,
                                query_vector=v, weight=args.weight),
    }

    sources = ["all"] + sorted({r["source"] for r in real.values()})
    print("\n{} real rows. q1 is hand-mapped ground truth; q2 and q3 labels "
          "come from\nthe regex rules, so read those as indicative.\n"
          .format(len(real)))

    for name, fn in methods.items():
        t0 = time.time()
        got = {rid: fn(real[rid], cache.get(rid)) for rid in real}
        ms = (time.time() - t0) / len(real) * 1000
        print("{}  ({:.1f} ms/row)".format(name, ms))
        for src in sources:
            subset = [rid for rid in real
                      if src == "all" or real[rid]["source"] == src]
            if not subset:
                continue
            row = "    {:<5}".format(src)
            for k in (1, 3, 8, 15):
                hits = sum(1 for rid in subset
                           if recall_at(got[rid], truth[rid], k))
                row += "  top{:<3}{:>4.0f}%".format(k, 100 * hits / len(subset))
            print(row)
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
