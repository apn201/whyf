"""Check that nothing from private/ has leaked into the publishable tree.

The repo goes public and judges read it. Three things must never be in it:

1. Questionnaire wording from the three real sources. Whoever wrote those
   questions owns them, and the vendor instrument behind q2 is a commercial
   product.
2. The peer benchmark table, which is the assessor's proprietary data.
3. Anything identifying the company assessed in the source report.

This runs in `make check`. It is a shingle scan rather than an exact-file
comparison, because the way this leaks is not by committing private/ - that is
gitignored - it is by pasting one real question into a card while writing it.

    python tools/check_publishable.py
    python tools/check_publishable.py --verbose

Without private/ on the machine there is nothing to compare against, and the
script says so and passes. That is correct: a clean checkout cannot leak what
it does not have.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRIVATE = ROOT / "private"

# Everything that ships.
PUBLIC_GLOBS = [
    "knowledge/**/*.yaml", "knowledge/**/*.md", "corpus/**/*.tsv",
    "corpus/**/*.md", "src/**/*.py", "tools/**/*.py", "tests/**/*.py",
    "docs/**/*.md", "infra/**/*.yaml", "*.md", "Makefile",
    # The interface ships example rows and shows them to everybody who opens
    # the demo. It was outside this list while carrying four rows lifted
    # verbatim from a real questionnaire, which is the most public place any
    # of this could have leaked.
    "web/**/*.html", "web/**/*.js", "web/**/*.css",
]

# tools/*.py describe what they deliberately do not extract, and quote a few
# words of the source to explain why. Those quotes are the point.
ALLOW = {"tools/check_publishable.py", "tools/parse_annex.py",
         "tools/parse_q2.py", "tools/parse_benchmarks.py",
         "tools/gen_synthetic.py"}

SHINGLE = 6          # consecutive words that count as copied wording

# Strings from the assessment report that identify its subject or its
# commercial figures. None of these should ever appear anywhere.
IDENTIFIERS = [
    "luxembourg", "fefco", "printing and packaging", "23.028.285",
    "cyber advisory", "3936 peers", "risk, integrity and compliance",
]


def words(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def shingles(text, n=SHINGLE):
    w = words(text)
    return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}


def private_shingles():
    """Every n-word run from the real questionnaire rows."""
    out = {}
    if not PRIVATE.exists():
        return out
    # q3 is excluded: its question text is NIST CSF 2.0, a US government
    # publication in the public domain. What was private about that source was
    # the compiled relevance ratings and crosswalk, and those are handled by
    # keeping them out of the tree entirely.
    sources = [PRIVATE / "questions.txt", PRIVATE / "q2-vendor-cyber.tsv"]
    for path in sources:
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            for field in line.split("\t"):
                if len(words(field)) < SHINGLE:
                    continue
                for sh in shingles(field):
                    out.setdefault(sh, path.name)
    return out


def public_files():
    seen = []
    for pattern in PUBLIC_GLOBS:
        for path in ROOT.glob(pattern):
            if path.is_file() and PRIVATE not in path.parents:
                rel = path.relative_to(ROOT).as_posix()
                if rel not in ALLOW:
                    seen.append(path)
    return sorted(set(seen))


def history_blobs():
    """Every blob ever committed, as (path, text). Deleted files included.

    The working tree is what you look at; history is what you publish. Those
    stop being the same thing the moment you fix a leak, because the fix is a
    new commit and the leak is still one commit back.
    """
    listing = subprocess.run(["git", "rev-list", "--objects", "--all"],
                             cwd=ROOT, capture_output=True, text=True).stdout
    pairs = []
    for line in listing.splitlines():
        parts = line.split(" ", 1)
        if len(parts) != 2:
            continue                      # a commit or tree, not a blob
        sha, path = parts
        if path.startswith("private/"):
            continue                      # never committed; belt and braces
        if TEXTUAL.search(path) and path not in ALLOW:
            pairs.append((sha, path))

    if not pairs:
        return

    # One batch, walked by the size in each response header. Walking by
    # request order instead desynchronises the moment git returns anything
    # unexpected, and then every finding is attributed to the wrong file.
    proc = subprocess.run(["git", "cat-file", "--batch"], cwd=ROOT,
                          input="\n".join(s for s, _ in pairs).encode(),
                          capture_output=True)
    data, pos, idx = proc.stdout, 0, 0
    while pos < len(data) and idx < len(pairs):
        nl = data.find(b"\n", pos)
        if nl < 0:
            break
        header = data[pos:nl].decode("utf-8", "replace").split()
        if len(header) < 3:
            break
        size = int(header[2])
        try:
            yield pairs[idx][1], data[nl + 1:nl + 1 + size].decode("utf-8")
        except UnicodeDecodeError:
            pass
        pos = nl + 1 + size + 1
        idx += 1


TEXTUAL = re.compile(r"[.](html|md|py|yaml|yml|tsv|txt|json|js|css)$")


def main():
    verbose = "--verbose" in sys.argv
    problems = []

    # ---- 1. private/ must actually be ignored by git ------------------------
    if PRIVATE.exists():
        try:
            r = subprocess.run(["git", "check-ignore", "-q", "private"],
                               cwd=ROOT, capture_output=True)
            if r.returncode != 0:
                problems.append("private/ is NOT gitignored. Fix .gitignore "
                                "before committing anything.")
        except FileNotFoundError:
            pass

    # ---- 2. no real questionnaire wording in the public tree ----------------
    priv = private_shingles()
    files = public_files()
    if not priv:
        print("private/ not on this machine - nothing to compare against.")
        if "--history" in sys.argv:
            # Passing here would be worse than failing. Somebody runs this in
            # CI before making the repository public, sees a green tick, and
            # concludes the history is clean when nothing was compared at all.
            print("\n--history needs the real corpus. Run it where private/ "
                  "exists, or this check means nothing.")
            return 2
    else:
        print("{} distinct {}-word runs from the real corpus".format(len(priv), SHINGLE))
        for path in files:
            text = path.read_text(encoding="utf-8", errors="replace")
            hits = shingles(text) & set(priv)
            if hits:
                rel = path.relative_to(ROOT).as_posix()
                for h in sorted(hits)[:3]:
                    problems.append("{}: copied wording from {} - \"{}...\"".format(
                        rel, priv[h], h))
                if len(hits) > 3:
                    problems.append("{}: and {} more runs".format(rel, len(hits) - 3))

    # ---- 3. no identifiers from the assessment report -----------------------
    for path in files:
        low = path.read_text(encoding="utf-8", errors="replace").lower()
        for ident in IDENTIFIERS:
            if ident in low:
                problems.append("{}: contains {!r}, which identifies the "
                                "assessed company or its assessor".format(
                                    path.relative_to(ROOT).as_posix(), ident))

    # ---- 4. and the same, for everything ever committed --------------------
    # Only on request, because it reads every blob in the repository. Run it
    # before making the repository public: deleting a leak from the working
    # tree does not delete it from the commit that introduced it.
    if "--history" in sys.argv and priv:
        seen = {}
        for path, text in history_blobs():
            hits = shingles(text) & set(priv)
            if hits:
                seen.setdefault(path, set()).update(hits)
            # The company the assessment was about must not be identifiable
            # from any commit either, and that is a worse leak than wording.
            low = text.lower()
            for ident in IDENTIFIERS:
                if ident in low:
                    problems.append(
                        "{}: contains {!r} in git history, which identifies "
                        "the assessed company".format(path, ident))
        for path, hits in sorted(seen.items()):
            problems.append(
                "{}: {} copied runs survive in git history, e.g. \"{}...\""
                .format(path, len(hits), sorted(hits)[0][:46]))
        if not seen:
            print("git history is clean too")

    print("scanned {} publishable files".format(len(files)))
    if verbose:
        for path in files:
            print("  " + path.relative_to(ROOT).as_posix())

    if problems:
        print("\n{} PROBLEMS - do not publish".format(len(problems)))
        for p in problems:
            print("  x " + p)
        return 1

    print("nothing from private/ appears in the publishable tree")
    return 0


if __name__ == "__main__":
    sys.exit(main())
