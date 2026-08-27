"""Extract the Annex I workbook into corpus rows and framework reference data.

The workbook is a FEFCO NIST CSF 2.0 checklist. It carries three things we
want, and one thing we deliberately leave behind.

Want:
  * the full CSF 2.0 subcategory catalog, 106 of them, which replaces the
    hand-typed category list in knowledge/frameworks/nist-csf.yaml;
  * per-subcategory relevance classes for IT and for OT - mandatory,
    recommended, point of improvement. That is real "does this apply to you"
    data rather than a guess;
  * a crosswalk from every subcategory to NIS2 articles, ISO 27001 clauses,
    ISO 27002 control numbers and IEC 62443 references. This is exactly what
    the framework_map tool needs and it is far better than anything a model
    would produce.

Leave behind:
  * the "Supplier Impact Comment" and "Note" columns. Those are commentary
    authored by a third party, and this repo is public. We keep the fact that
    a row is supplier-scoped, which is a fact, and drop the prose, which is
    someone else's writing.
  * ISO 27001 / 27002 / IEC 62443 control *text*. Numbers are facts, the
    standards are copyrighted. Only the identifiers cross over.

    python tools/parse_annex.py
"""
import os
import re
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

try:
    import openpyxl
except ImportError:
    sys.exit("openpyxl is not installed. Run: pip install -r requirements.txt")

ROOT = Path(__file__).resolve().parent.parent
# The source is not published. Point WHYF_SOURCE at it, or drop it in
# private/ under this name. This was a hardcoded path to one machine, which
# put a Windows username into a file that ships.
SRC = Path(os.environ.get("WHYF_SOURCE")
           or ROOT / "private" / "Annex I_Checklist of control points.xlsx")
PRIVATE = ROOT / "private"
CORPUS_OUT = PRIVATE / "q3-nist-checklist.tsv"
CROSSWALK_OUT = PRIVATE / "crosswalk.tsv"
RELEVANCE_OUT = PRIVATE / "nist-csf-relevance.tsv"

SUBCAT_RE = re.compile(r"^([A-Z]{2}\.[A-Z]{2}-\d{2}):\s*(.*)$", re.S)
CAT_RE = re.compile(r"\(([A-Z]{2}\.[A-Z]{2})\)")
FUNC_RE = re.compile(r"^([A-Z]+)\s*\(([A-Z]{2})\)")

CLASS_MAP = {
    "mandatory": "mandatory",
    "recommended": "recommended",
    "point of improvement": "optional",
    "point of improvment": "optional",
}


def txt(cell):
    if cell is None:
        return ""
    # The workbook came through a latin-1 round trip; the replacement char
    # stands in for apostrophes and dashes.
    s = str(cell).replace("\ufffd", "'").replace("\u00a0", " ")
    return re.sub(r"\s+", " ", s).strip()


def walk(ws, header_row, cols):
    """Yield one dict per subcategory, forward-filling the merged Function and
    Category cells and folding the Ex1/Ex2/Ex3 rows into the row above."""
    function = category = None
    current = None
    for row in ws.iter_rows(min_row=header_row + 1, values_only=True):
        cells = [txt(c) for c in row]
        while len(cells) < max(cols.values()) + 1:
            cells.append("")

        if cells[0]:
            m = FUNC_RE.match(cells[0])
            function = m.group(2) if m else cells[0][:2]
        if cells[1]:
            m = CAT_RE.search(cells[1])
            category = m.group(1) if m else None

        sub = cells[2]
        if sub:
            m = SUBCAT_RE.match(sub)
            if not m:
                continue
            if current:
                yield current
            current = {
                "id": m.group(1),
                "function": function,
                "category": category,
                "text": m.group(2).strip(),
                "examples": [],
            }
            for key, idx in cols.items():
                current[key] = cells[idx]

        if current and cells[3].startswith("Ex"):
            current["examples"].append(re.sub(r"^Ex\d+:\s*", "", cells[3]))
            # continuation rows carry crosswalk values too
            for key, idx in cols.items():
                if cells[idx] and cells[idx] not in current.get(key, ""):
                    current[key] = (current.get(key, "") + " ; " + cells[idx]).strip(" ;")

    if current:
        yield current


def main():
    if not SRC.exists():
        sys.exit("cannot find {}".format(SRC))
    wb = openpyxl.load_workbook(SRC, data_only=True)

    # ---- 1. the checklist: subcategory + IT/OT relevance class -------------
    checklist = {
        r["id"]: r for r in walk(
            wb["NIST 2.0 Checklist"], header_row=4,
            cols={"class_it": 4, "class_ot": 5},
        )
    }

    # ---- 2. the crosswalk to the other frameworks --------------------------
    cross = {
        r["id"]: r for r in walk(
            wb["NIST 2.0 vs other frameworks"], header_row=2,
            cols={"nis2": 4, "iso27001": 5, "iso27002": 6, "iec62443": 7},
        )
    }

    # ---- 3. which subcategories a supplier actually gets asked about -------
    supplier_scoped = set()
    for r in walk(wb["NIST2 Checklist supplier Ass.  "], header_row=2,
                  cols={"comment": 4}):
        if r.get("comment"):
            supplier_scoped.add(r["id"])

    print("checklist subcategories : {}".format(len(checklist)))
    print("crosswalk rows          : {}".format(len(cross)))
    print("supplier-scoped         : {}".format(len(supplier_scoped)))

    # ---- corpus source q3 --------------------------------------------------
    CORPUS_OUT.parent.mkdir(parents=True, exist_ok=True)
    cols = ["id", "function", "category", "form", "class_it", "class_ot",
            "supplier_scoped", "question", "examples"]
    with CORPUS_OUT.open("w", encoding="utf-8", newline="") as fh:
        fh.write("\t".join(cols) + "\n")
        for sid, r in checklist.items():
            out = {
                "id": "q3." + sid,
                "function": r["function"] or "",
                "category": r["category"] or "",
                "form": "maturity_ladder",   # every row is scored 1-4 on four axes
                "class_it": CLASS_MAP.get(r.get("class_it", "").lower(), ""),
                "class_ot": CLASS_MAP.get(r.get("class_ot", "").lower(), ""),
                "supplier_scoped": "yes" if sid in supplier_scoped else "no",
                "question": r["text"],
                "examples": " | ".join(r["examples"]),
            }
            fh.write("\t".join(str(out[c]).replace("\t", " ") for c in cols) + "\n")
    print("\nwrote {}".format(CORPUS_OUT.relative_to(ROOT)))

    # ---- framework crosswalk ----------------------------------------------
    def ids_from(field, value):
        """Pull identifiers out of the prose. Numbers only - the standards are
        copyrighted and this repo is public."""
        if not value:
            return []
        if field == "nis2":
            arts = re.findall(r"[Aa]rt\.?\s*(\d+)", value)
            return sorted({"nis2-art" + a for a in arts})
        if field == "iso27001":
            return sorted({"iso27001-clause" + c
                           for c in re.findall(r"[Cc]lause\s*(\d+(?:\.\d+)*)", value)})
        if field == "iso27002":
            return sorted({"iso27002-" + c
                           for c in re.findall(r"\b(\d+\.\d+)\b", value)})
        if field == "iec62443":
            # the source writes "62443-2-1:2009"; the part number is the id
            return sorted({"iec62443-" + c.replace(" ", "")
                           for c in re.findall(r"62443-(\d+-\d+(?::\d{4})?)", value)})
        return []

    # Controls the cards cite that the Annex I crosswalk happens not to reach.
    # These are published control numbers, which are facts; no control text is
    # reproduced. Without them the validator would drop a legitimate citation.
    EXTRA = {
        "iso27002": ["iso27002-5.23", "iso27002-5.24", "iso27002-5.30",
                     "iso27002-7.7", "iso27002-8.9", "iso27002-8.12",
                     "iso27002-8.31"],
    }

    seen = {f: set() for f in ("nis2", "iso27001", "iso27002", "iec62443")}
    for field, ids in EXTRA.items():
        seen[field].update(ids)
    with CROSSWALK_OUT.open("w", encoding="utf-8", newline="") as fh:
        fh.write("csf_subcategory\tframework\tcontrol_ids\n")
        rows = 0
        for sid, r in sorted(cross.items()):
            for field in seen:
                found = ids_from(field, r.get(field, ""))
                if found:
                    seen[field].update(found)
                    fh.write("{}\t{}\t{}\n".format(
                        "nist-csf-" + sid.lower(), field, ",".join(found)))
                    rows += 1
    print("wrote {} ({} mappings)".format(CROSSWALK_OUT.relative_to(ROOT), rows))

    # The other framework files are written by tools/render_frameworks.py,
    # which reads the crosswalk for ids and supplies a description for each.
    # Writing them here too would overwrite those descriptions with TODO.
    for field in sorted(seen):
        print("  {:<10} {:>3} ids -> render_frameworks.py".format(
            field, len(seen[field])))

    # ---- regenerate nist-csf.yaml from the real subcategory list -----------
    out = [
        "id: nist-csf",
        "name: NIST Cybersecurity Framework 2.0",
        'url: "https://www.nist.gov/cyberframework"',
        "status: done",
        "",
        "# Generated by tools/parse_annex.py from the Annex I workbook. CSF 2.0 is",
        "# a US government publication and is public domain, so the subcategory",
        "# text is reproduced here in full.",
        "#",
        "# The relevance ratings that came with the source workbook are a trade",
        "# federation's compiled editorial judgement, not part of CSF, so they are",
        "# not republished here. They are in private/nist-csf-relevance.tsv and",
        "# reach the cards through private/context/*.md while you write them.",
        "",
        "controls:",
    ]
    for sid, r in checklist.items():
        out.append("  - id: nist-csf-{}".format(sid.lower()))
        out.append('    title: "{}"'.format(r["text"].replace('"', "'")))
        out.append("    function: {}".format(r["function"]))
        out.append("    category: {}".format(r["category"]))

    (ROOT / "knowledge" / "frameworks" / "nist-csf.yaml").write_text(
        "\n".join(out) + "\n", encoding="utf-8")
    print("wrote knowledge/frameworks/nist-csf.yaml ({} subcategories, "
          "public domain)".format(len(checklist)))

    with RELEVANCE_OUT.open("w", encoding="utf-8", newline="") as fh:
        fh.write("subcategory\tclass_it\tclass_ot\tsupplier_scoped\n")
        for sid, r in checklist.items():
            fh.write("{}\t{}\t{}\t{}\n".format(
                "nist-csf-" + sid.lower(),
                CLASS_MAP.get(r.get("class_it", "").lower(), ""),
                CLASS_MAP.get(r.get("class_ot", "").lower(), ""),
                "yes" if sid in supplier_scoped else "no"))
    print("wrote {} (private)".format(RELEVANCE_OUT.relative_to(ROOT)))


if __name__ == "__main__":
    main()
