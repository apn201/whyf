"""Fill in the framework files from tools/framework_content.py.

Reads the id set already in each file, which is whatever the Annex I crosswalk
reached plus anything the cards cite, and rewrites the file with a description
for each id. Ids with no description are kept and flagged rather than dropped,
because dropping one would silently invalidate a citation on a card.

nist-csf.yaml is not touched. It is generated straight from the source workbook
by tools/parse_annex.py, and CSF 2.0 is public domain, so its own text stands.

    python tools/render_frameworks.py
    python tools/render_frameworks.py --check   # report gaps, write nothing
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from framework_content import FRAMEWORKS  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
K = ROOT / "knowledge" / "frameworks"

ID_RE = re.compile(r"^  - id: (\S+)$", re.M)
CROSSWALK = ROOT / "private" / "crosswalk.tsv"


def crosswalk_ids():
    """Ids the Annex I crosswalk reaches, when the private data is present.
    Without it we still have whatever is already in the files, which is why a
    clean checkout renders the same framework library."""
    out = {}
    if not CROSSWALK.exists():
        return out
    import csv
    with CROSSWALK.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh, delimiter="	"):
            out.setdefault(r["framework"], set()).update(
                r["control_ids"].split(","))
    return out


def existing_ids(path):
    if not path.exists():
        return []
    return ID_RE.findall(path.read_text(encoding="utf-8"))


def wrap(text, indent):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > 72:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return "\n".join(indent + ln for ln in lines)


def main():
    check_only = "--check" in sys.argv
    gaps = []
    from_crosswalk = crosswalk_ids()

    for fid, (name, url, note, glosses) in FRAMEWORKS.items():
        path = K / "{}.yaml".format(fid)
        ids = existing_ids(path)
        ids.extend(from_crosswalk.get(fid, ()))
        # Anything described but not yet in the file still belongs in it.
        for cid in glosses:
            if cid not in ids:
                ids.append(cid)
        ids = sorted(set(ids), key=lambda s: [
            int(p) if p.isdigit() else p
            for p in re.split(r"[.\-]", s.split("-", 1)[-1])])

        out = [
            "id: {}".format(fid),
            "name: {}".format(name),
            'url: "{}"'.format(url),
            "status: done",
            "",
            "# The only ids a concept card may cite for this framework. The",
            "# validator drops anything else before it reaches a user.",
            "#",
        ]
        out.append(wrap(note, "# "))
        out.append("")
        out.append("controls:")
        for cid in ids:
            gloss = glosses.get(cid)
            if not gloss:
                gaps.append("{}: {}".format(fid, cid))
                gloss = "TODO no description written yet"
            out.append("  - id: {}".format(cid))
            out.append('    title: >-')
            out.append(wrap(gloss, "      "))

        if not check_only:
            path.write_text("\n".join(out) + "\n", encoding="utf-8")
        print("{:<10} {:>3} ids".format(fid, len(ids)))

    unused = K / "cis.yaml"
    if unused.exists() and not check_only:
        unused.unlink()
        print("removed cis.yaml - no card cites it")

    if gaps:
        print("\n{} ids with no description:".format(len(gaps)))
        for g in gaps:
            print("  " + g)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
