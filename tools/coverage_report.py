"""Run a file of questions through the agent and report where the gaps are.

Not the same job as tools/harness.py. That one measures accuracy against known
ground truth. This one takes questions nobody has mapped, and answers a
different question: which of these can the knowledge base actually answer, and
what is missing from it.

    python tools/coverage_report.py private/test-questions.txt --profile whyf

The output is a gap list, ordered by how often a topic came up. That list is
what tells you which cards to write next, rather than guessing.
"""
import argparse
import os
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("questions", help="a text file, one question per line")
    ap.add_argument("--profile", default=None)
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    lines = [l.strip() for l in
             Path(args.questions).read_text(encoding="utf-8").splitlines()
             if l.strip() and not l.startswith("#")]
    if args.limit:
        lines = lines[: args.limit]

    if args.profile:
        os.environ["AWS_PROFILE"] = args.profile

    from whyf.cache import MemoryCache
    from whyf.pipeline import Pipeline
    pipeline = Pipeline(cache=MemoryCache())

    covered, near, declined = [], [], []
    concepts = Counter()
    classes = Counter()

    for i, q in enumerate(lines, 1):
        v = pipeline.resolve(q)
        tier = v.telemetry.tier
        if tier == "declined":
            declined.append((q, ""))
        elif tier == "near-miss":
            gap = v.subtitle.replace("Does not cover ", "")
            near.append((q, "{} / missing: {}".format(v.concept, gap)))
        else:
            covered.append((q, v.concept))
            concepts[v.concept] += 1
            classes[v.question_class] += 1
        if i % 20 == 0:
            print("  {}/{}".format(i, len(lines)), file=sys.stderr)

    total = len(lines)
    print("\n" + "=" * 70)
    print("{} questions".format(total))
    print("=" * 70)
    print("  answered from a card   {:>3}  {:>4.0f}%".format(
        len(covered), 100 * len(covered) / total))
    print("  near miss, gap named   {:>3}  {:>4.0f}%".format(
        len(near), 100 * len(near) / total))
    print("  no card at all         {:>3}  {:>4.0f}%".format(
        len(declined), 100 * len(declined) / total))

    if near:
        print("\nNEAR MISSES  (a card exists nearby but does not answer it)")
        for q, why in near:
            print("  {:<66}".format(q[:66]))
            print("      {}".format(why))

    if declined:
        print("\nNO CARD  (these are the gaps worth writing)")
        for q, _ in declined:
            print("  {}".format(q[:74]))

    print("\nmost-used cards: " + ", ".join(
        "{} x{}".format(c, n) for c, n in concepts.most_common(8)))
    print("classes: " + ", ".join(
        "{}:{}".format(k, v) for k, v in classes.most_common()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
