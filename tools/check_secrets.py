"""Scan every commit for secrets and for anything from private/.

check_publishable.py looks at the working tree. That is not enough before a
repo goes public, because git history is permanent: a key committed today and
deleted tomorrow is still in the history when the repo flips to public, and
so is every file that was ever tracked.

This scans all commits, all files, all the way back.

    python tools/check_secrets.py
    python tools/check_secrets.py --verbose

Exit 1 means do not push, or do not make it public, depending on what it
found. Read what it says: some findings mean rewrite history, some just mean
rotate a credential.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Patterns worth stopping a push for. Deliberately narrow: a scanner that
# cries wolf gets ignored, and this one has to be trusted the day it fires.
SECRETS = [
    ("AWS access key id", re.compile(r"\b(AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("AWS secret access key", re.compile(
        r"aws_secret_access_key\s*=\s*\S{20,}", re.I)),
    ("private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("bearer or api token assignment", re.compile(
        r"(api[_-]?key|secret[_-]?key|access[_-]?token|auth[_-]?token)"
        r"\s*[:=]\s*['\"][A-Za-z0-9_\-]{20,}['\"]", re.I)),
    ("Tavily or Brave key", re.compile(r"\btvly-[A-Za-z0-9]{16,}\b")),
    ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b")),
]

# Not secrets, but they identify the account or its people, and a public repo
# is free reconnaissance. Warned about rather than blocked.
IDENTIFYING = [
    ("AWS account id", re.compile(r"\b\d{12}\b")),
    ("SSO portal url", re.compile(r"https://d-[0-9a-z]{10}\.awsapps\.com")),
    ("Identity Center instance", re.compile(r"\bssoins-[0-9a-f]{16}\b")),
]

# Paths that must never appear in any commit.
FORBIDDEN_PATHS = [
    re.compile(r"^private/"),
    re.compile(r"(^|/)\.aws/"),
    re.compile(r"(^|/)\.env$"),
    re.compile(r"\.pem$"),
    re.compile(r"(^|/)credentials$"),
]

# Files where a 12-digit number is a coincidence rather than an account id.
NUMERIC_NOISE = re.compile(
    r"(embeddings\.json|\.lock$|package-lock|poetry\.lock|\.svg$)")


def git(*args):
    r = subprocess.run(["git"] + list(args), cwd=ROOT,
                       capture_output=True, text=True, errors="replace")
    return r.stdout if r.returncode == 0 else ""


def all_commits():
    out = git("rev-list", "--all")
    return [c for c in out.split() if c]


def main():
    verbose = "--verbose" in sys.argv
    commits = all_commits()
    if not commits:
        print("no commits yet, nothing to scan")
        return 0

    blocking, warnings = [], []

    # ---- 1. paths that were ever tracked ---------------------------------
    tracked = set()
    for line in git("log", "--all", "--pretty=format:", "--name-only").splitlines():
        line = line.strip()
        if line:
            tracked.add(line)
    for path in sorted(tracked):
        for pattern in FORBIDDEN_PATHS:
            if pattern.search(path):
                blocking.append(
                    "{} was committed at some point. It is in history even if "
                    "it is gone now.".format(path))

    # ---- 2. content of every blob in every commit -------------------------
    scanned = 0
    for commit in commits:
        listing = git("ls-tree", "-r", "--name-only", commit)
        for path in listing.splitlines():
            path = path.strip()
            if not path:
                continue
            blob = git("show", "{}:{}".format(commit, path))
            if not blob:
                continue
            scanned += 1
            for label, pattern in SECRETS:
                m = pattern.search(blob)
                if m:
                    blocking.append("{} in {} (commit {}): {}".format(
                        label, path, commit[:8], m.group(0)[:24] + "..."))
            if NUMERIC_NOISE.search(path):
                continue
            for label, pattern in IDENTIFYING:
                m = pattern.search(blob)
                if m:
                    warnings.append("{} in {}: {}".format(
                        label, path, m.group(0)))

    print("scanned {} commits".format(len(commits)))
    if verbose:
        print("  {} tracked paths, {} blob reads".format(len(tracked), scanned))

    # ---- 3. is private/ actually ignored, right now -----------------------
    if (ROOT / "private").exists():
        r = subprocess.run(["git", "check-ignore", "-q", "private"],
                           cwd=ROOT, capture_output=True)
        if r.returncode != 0:
            blocking.append("private/ exists and is NOT gitignored")

    seen = set()
    warnings = [w for w in warnings if not (w in seen or seen.add(w))]

    if warnings:
        print("\n{} identifying values (not secrets, but a public repo is "
              "free reconnaissance):".format(len(warnings)))
        for w in warnings[:12]:
            print("  ? " + w)
        if len(warnings) > 12:
            print("  ... and {} more".format(len(warnings) - 12))

    if blocking:
        print("\n{} BLOCKING".format(len(blocking)))
        for b in blocking:
            print("  x " + b)
        print("\nA secret already committed is compromised whether or not you "
              "rewrite history.\nRotate it first, then clean the history.")
        return 1

    print("no secrets found in history")
    if warnings:
        print("Safe to push private. Clear the warnings above before making "
              "the repo public.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
