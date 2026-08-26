"""Everything `make check` does, without needing make.

Windows does not ship make, and neither does a plain Python install, so a judge
following the README on Windows would hit "make: command not found" as the
first thing they ever see from this project. This is the fallback.

    python tools/check.py            # validate, publication check, tests
    python tools/check.py --quick    # skip the tests
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

STEPS = [
    ("corpus mapping", [sys.executable, "tools/corpus_map.py"]),
    ("card schema and coverage", [sys.executable, "tools/validate_cards.py"]),
    ("publication safety", [sys.executable, "tools/check_publishable.py"]),
    ("secrets in history", [sys.executable, "tools/check_secrets.py"]),
    ("tests", [sys.executable, "-m", "pytest", "-q"]),
]


def main():
    quick = "--quick" in sys.argv
    steps = STEPS[:-1] if quick else STEPS
    failed = []

    for name, cmd in steps:
        print("\n" + "=" * 68)
        print(name)
        print("=" * 68)
        sys.stdout.flush()
        result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        print(result.stdout.rstrip())
        if result.stderr.strip():
            print(result.stderr.rstrip())
        if result.returncode != 0:
            failed.append(name)

    print("\n" + "=" * 68)
    if failed:
        print("FAILED: " + ", ".join(failed))
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
