"""Package the Lambda without Docker.

CDK's PythonFunction bundles dependencies inside a Docker container. Docker is
not installed on this machine and installing it to build one Lambda is a poor
trade, so this does the same job with pip's cross-platform download flags.

    python tools/build_lambda.py
    python tools/build_lambda.py --check    # report size, build nothing

boto3 is deliberately not installed: the Lambda runtime already has it, and
shipping a second copy adds about 15 MB for nothing.
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build" / "lambda"

# Everything the handler imports that is not already in the runtime.
RUNTIME_DEPS = ["strands-agents", "pydantic", "pyyaml"]

# Python version and architecture of the Lambda, not of this machine.
TARGET_PYTHON = "3.12"
TARGET_PLATFORM = "manylinux2014_x86_64"

# Things that are large, or that only exist for the build, and that the Lambda
# never imports.
PRUNE = [
    "**/__pycache__", "**/*.pyc", "**/*.pyi",
    "**/tests", "**/test", "**/*.dist-info/RECORD",
    "botocore", "boto3", "s3transfer",       # present in the runtime already
    "**/examples", "**/docs",
]


def sh(*args):
    result = subprocess.run(list(args), capture_output=True, text=True,
                            errors="replace")
    if result.returncode != 0:
        print(result.stdout[-2000:])
        print(result.stderr[-2000:])
        sys.exit("failed: {}".format(" ".join(args[:4])))
    return result.stdout


def tree_size(path):
    return sum(f.stat().st_size for f in path.rglob("*") if f.is_file())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    if args.check:
        if not BUILD.exists():
            sys.exit("nothing built yet")
        print("{:.1f} MB unpacked in {}".format(
            tree_size(BUILD) / 1e6, BUILD.relative_to(ROOT)))
        return 0

    if BUILD.exists():
        shutil.rmtree(BUILD)
    BUILD.mkdir(parents=True)

    print("installing {} for python {} on {}".format(
        ", ".join(RUNTIME_DEPS), TARGET_PYTHON, TARGET_PLATFORM))
    sh(sys.executable, "-m", "pip", "install",
       "--target", str(BUILD),
       "--platform", TARGET_PLATFORM,
       "--python-version", TARGET_PYTHON,
       "--only-binary=:all:",
       "--upgrade", "--quiet", "--disable-pip-version-check",
       *RUNTIME_DEPS)

    print("copying the agent and the knowledge")
    shutil.copytree(ROOT / "src" / "whyf", BUILD / "whyf",
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    # The cards are read at cold start. They are the product, so they ship
    # inside the bundle rather than being fetched from S3 at runtime: one
    # fewer thing that can be missing when a judge clicks the demo link.
    shutil.copytree(ROOT / "knowledge", BUILD / "knowledge",
                    ignore=shutil.ignore_patterns("__pycache__", "*.md"))

    removed = 0
    for pattern in PRUNE:
        for path in BUILD.glob(pattern):
            if path.is_dir():
                shutil.rmtree(path, ignore_errors=True)
            else:
                path.unlink(missing_ok=True)
            removed += 1

    size = tree_size(BUILD)
    print("\n{:.1f} MB unpacked, {} paths pruned".format(size / 1e6, removed))
    biggest = sorted(
        ((tree_size(d), d.name) for d in BUILD.iterdir() if d.is_dir()),
        reverse=True)[:6]
    for n, name in biggest:
        print("  {:>7.1f} MB  {}".format(n / 1e6, name))

    if size > 240e6:
        sys.exit("over the 250 MB unzipped Lambda limit")
    print("\nready. `cd infra && npx cdk deploy`")
    return 0


if __name__ == "__main__":
    sys.exit(main())
