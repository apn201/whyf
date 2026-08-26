"""Run the corpus through the agent and report what happened.

This produces the demo statistic. Concept accuracy against the hand-mapped
ground truth, how many rows the agent declined rather than guessed, model calls
per row, and elapsed time.

It costs money, so it says how much before spending any:

    python tools/harness.py --profile whyf --estimate
    python tools/harness.py --profile whyf --limit 40
    python tools/harness.py --profile whyf --all
    python tools/harness.py --profile whyf --all --source q1

Declining is counted separately from getting it wrong, because they are not the
same failure and the second is much worse than the first.
"""
import argparse
import json
import os
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))

from corpus_map import build_map, load_rows  # noqa: E402

# Haiku 4.5, per million tokens. Only used for the estimate.
IN_PER_1M, OUT_PER_1M = 1.10, 5.50
TYPICAL_IN, TYPICAL_OUT = 750, 180


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", default=None)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--source", default=None, help="q1, q2, q3 or syn")
    ap.add_argument("--estimate", action="store_true")
    ap.add_argument("--out", default=None, help="write per-row results as JSON")
    args = ap.parse_args()

    rows = load_rows()
    truth, _ = build_map(rows)
    subset = {rid: r for rid, r in rows.items()
              if (args.source or "syn") != "syn" or args.source == "syn"
              or r["source"] != "syn"}
    if args.source:
        subset = {rid: r for rid, r in rows.items() if r["source"] == args.source}
    else:
        subset = {rid: r for rid, r in rows.items() if r["source"] != "syn"}
    if args.limit:
        subset = dict(sorted(subset.items())[: args.limit])
    elif not args.all and not args.estimate:
        sys.exit("pass --limit N for a sample or --all for the whole corpus. "
                 "--estimate prices it first.")

    cost = len(subset) * (TYPICAL_IN * IN_PER_1M + TYPICAL_OUT * OUT_PER_1M) / 1e6
    print("{} rows, roughly ${:.2f} at Haiku prices".format(len(subset), cost))
    if args.estimate:
        return 0

    if args.profile:
        os.environ["AWS_PROFILE"] = args.profile

    from whyf.pipeline import Pipeline
    pipeline = Pipeline()

    right = wrong = declined = 0
    calls = Counter()
    tiers = Counter()
    classes = Counter()
    verdicts = Counter()
    elapsed = []
    misses = []
    results = []

    started = time.time()
    for i, (rid, row) in enumerate(sorted(subset.items()), 1):
        v = pipeline.resolve(row["question"])
        want = truth[rid]
        t = v.telemetry
        tiers[t.tier] += 1
        calls[t.model_calls] += 1
        elapsed.append(t.elapsed_s)
        classes[v.question_class] += 1
        if v.verdict:
            verdicts[v.verdict] += 1

        if v.concept is None:
            declined += 1
        elif v.concept == want:
            right += 1
        else:
            wrong += 1
            misses.append((rid, row["question"][:70], want, v.concept))

        results.append({"id": rid, "want": want, "got": v.concept,
                        "verdict": v.verdict, "class": v.question_class,
                        "tier": t.tier, "calls": t.model_calls,
                        "seconds": round(t.elapsed_s, 2)})
        if i % 20 == 0:
            print("  {}/{}".format(i, len(subset)))

    total = len(subset)
    wall = time.time() - started
    print("\n" + "=" * 62)
    print("{} rows in {:.0f}s, {:.1f}s per row".format(total, wall, wall / total))
    print("=" * 62)
    print("  correct concept   {:>4}  {:>5.0f}%".format(right, 100 * right / total))
    print("  wrong concept     {:>4}  {:>5.0f}%   <- the one that matters".format(
        wrong, 100 * wrong / total))
    print("  declined          {:>4}  {:>5.0f}%   (said so rather than guessing)"
          .format(declined, 100 * declined / total))
    print("\n  tiers      " + "  ".join(
        "{}:{}".format(k, v) for k, v in tiers.most_common()))
    print("  model calls " + "  ".join(
        "{} calls:{}".format(k, v) for k, v in sorted(calls.items())))
    print("  classes    " + "  ".join(
        "{}:{}".format(k, v) for k, v in classes.most_common()))
    print("  verdicts   " + "  ".join(
        "{}:{}".format(k, v) for k, v in verdicts.most_common()))

    if misses:
        print("\n  wrong concept on {} rows:".format(len(misses)))
        for rid, q, want, got in misses[:15]:
            print("    {:<14} want {:<26} got {}".format(rid, want, got))
            print("      {}".format(q))

    if args.out:
        Path(args.out).write_text(json.dumps(results, indent=1), encoding="utf-8")
        print("\nwrote {}".format(args.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
