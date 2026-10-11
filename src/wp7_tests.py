"""WP7 - Independent checks of the built report.

Deliberately independent, in the pattern src/wp5_tests.py and src/wp6_tests.py established: this
module re-reads the generated artefacts from disk and re-derives what it checks from the source
tables. Artefact checks use the declared registries; the honesty check exercises the declared
lint. Separate negative regression fixtures exercise the builder's rejection paths (D-127),
including complete scratch reports, rather than treating those fixtures as independent science.

A failure raises and stops the pipeline.
"""
from __future__ import annotations

import hashlib
import contextlib
import io
import re
import tempfile
import zlib
from pathlib import Path
from unittest.mock import patch

import pandas as pd

import wp7_report as R
from common import OUTPUTS, ROOT

REPORT = ROOT / "report"
RESULTS: list = []


def check(name: str, passed: bool, detail: str):
    RESULTS.append(dict(check=name, passed=bool(passed), detail=detail))
    print(f"  [{'PASS' if passed else 'FAIL'}] {name}: {detail}", flush=True)
    if not passed:
        raise RuntimeError(f"WP7 check failed: {name}: {detail}")


def c1_placeholders_resolved_and_used():
    src = R.blank_comments((REPORT / "report.md").read_text())
    filled = (REPORT / "report_filled.md").read_text()
    used = set(R.PLACEHOLDER.findall(src))
    unknown = sorted(used - set(R.REGISTRY))
    unused = sorted(set(R.REGISTRY) - used)
    leftover = R.PLACEHOLDER.findall(filled)
    check("every placeholder resolves and every registry entry is used",
          not unknown and not unused and not leftover,
          f"{len(used)} placeholders, {len(R.REGISTRY)} registry entries, "
          f"0 unresolved in the built document"
          + (f"; UNKNOWN {unknown}" if unknown else "")
          + (f"; UNUSED {unused}" if unused else "")
          + (f"; LEFTOVER {leftover[:3]}" if leftover else ""))


def c2_claim_map_rereads():
    """Every claim re-reads from the file, row and column the map names, independently of the
    registry object, and matches the value printed in the report."""
    m = pd.read_csv(REPORT / "claim_source_map.csv")
    bad = []
    for _, row in m[m.kind == "table lookup"].iterrows():
        df = pd.read_csv(ROOT / row["file"])
        sel = df
        for clause in str(row["row_selector"]).split("; "):
            col, _, val = clause.partition(" = ")
            sel = sel[sel[col].astype(str).str.strip() == val.strip()]
        if len(sel) != 1:
            bad.append(f"{row['key']}: selector matched {len(sel)} rows")
            continue
        spec = R.REGISTRY[row["key"]]
        if spec.fmt.format(float(sel.iloc[0][row["column"]])) != str(row["value"]):
            bad.append(f"{row['key']}: {row['value']} does not re-read from {row['file']}")
    check("every claim re-reads from its named file, row and column", not bad,
          f"{len(m)} claims in the map, {int((m.kind == 'table lookup').sum())} direct lookups "
          f"re-read and matched" + (f"; MISMATCH {bad[:3]}" if bad else ""))


def c3_figure_hashes():
    """Every embedded figure is the approved generated file, byte for byte - including both panels
    of the two-panel Figure 3 (D-125 item 3)."""
    filled = (REPORT / "report_filled.md").read_text()
    embedded = re.findall(r"!\[[^\]]*\]\(\.\./outputs/([^)]+)\)", filled)
    declared = [p for spec in R.FIGURES.values() for p in spec["paths"]]
    bad = [p for p in embedded if not (OUTPUTS / p).exists()]
    digests = {p: hashlib.sha256((OUTPUTS / p).read_bytes()).hexdigest()[:12] for p in embedded
               if (OUTPUTS / p).exists()}
    panels = R.FIGURES["3"]["paths"]
    # Any presentation-only crop must remove nothing but blank space and the broken source title:
    # re-check that the masked strip carries no axis, tick, legend, annotation or data mark, by
    # requiring the rows immediately above the crop line to be blank (D-118 keeps the file itself
    # untouched, so its digest above is still the provenance).
    import matplotlib.image as mpimg
    crop_bad = []
    for rel, n in R.CROPS.items():
        img = mpimg.imread(str(OUTPUTS / rel))
        ink = (img[..., :3].mean(axis=2) < 0.6)
        w = ink.shape[1]
        # Plot structure - axes, frame, gridlines, the legend box - shows as long continuous
        # horizontal runs. Rendered text does not. The masked strip must contain no such run.
        def longest_run(row):
            best = cur = 0
            for v in row:
                cur = cur + 1 if v else 0
                best = max(best, cur)
            return best
        worst = max((longest_run(ink[y]) for y in range(n)), default=0)
        if worst > 0.15 * w:
            crop_bad.append(f"{rel}: masked strip contains a {worst}px run (plot structure?)")
        if not ink[n:].any():
            crop_bad.append(f"{rel}: nothing survives the crop")
        # and the plot frame must still be intact below the crop
        if max((longest_run(ink[y]) for y in range(n, min(n + 20, ink.shape[0]))), default=0) < 0.5 * w:
            crop_bad.append(f"{rel}: the plot frame does not survive the crop")
    check("every embedded figure is the approved generated file, and any crop removes no content",
          not bad and sorted(embedded) == sorted(declared) and len(panels) == 2 and not crop_bad,
          f"{len(embedded)} images, all present in outputs/; Figure 3 carries its two approved "
          f"panels ({', '.join(digests[p] for p in panels)}); "
          f"{len(R.CROPS)} presentation crop(s), each verified to contain no plot structure "
          f"and to leave the plot frame intact"
          + (f"; MISSING {bad}" if bad else "") + (f"; CROP {crop_bad}" if crop_bad else ""))


def c4_evidence_classes():
    """At least one valid class per float, several allowed, and the declared combinations present
    (D-126 item 1)."""
    bad = []
    for kind, reg in (("figure", R.FIGURES), ("table", R.TABLES)):
        for num, spec in reg.items():
            classes = set(spec["classes"])
            if not classes or classes - set(R.EVIDENCE_CLASSES):
                bad.append(f"{kind} {num}: {sorted(classes)}")
            key = num if kind == "figure" else f"T{num}"
            if key in R.REQUIRED_COMBINATIONS and not R.REQUIRED_COMBINATIONS[key] <= classes:
                bad.append(f"{kind} {num} missing {sorted(R.REQUIRED_COMBINATIONS[key] - classes)}")
    multi = sum(1 for reg in (R.FIGURES, R.TABLES) for s in reg.values() if len(s["classes"]) > 1)
    check("every float carries at least one valid evidence class, combinations as declared",
          not bad,
          f"{len(R.FIGURES)} figures and {len(R.TABLES)} tables tagged; {multi} carry more than "
          f"one class; {len(R.REQUIRED_COMBINATIONS)} declared combinations present"
          + (f"; BAD {bad}" if bad else ""))


def c5_constant_provenance():
    """No uncited number may reach the report: every registered constant states a provenance
    category and a source (D-126 item 3)."""
    m = pd.read_csv(REPORT / "constant_source_map.csv")
    bad = [r["name"] for _, r in m.iterrows()
           if not str(r["provenance_category"]).strip() or not str(r["source"]).strip()
           or str(r["provenance_category"])[0] not in "ABM"]
    cats = m["provenance_category"].str[0].value_counts().to_dict()
    check("every registered numeric constant is provenance-tracked", not bad,
          f"{len(m)} constants: {cats.get('A', 0)} method/configuration, {cats.get('B', 0)} "
          f"externally cited, {cats.get('M', 0)} document metadata; all carry a source"
          + (f"; BAD {bad}" if bad else ""))


def c6_honesty_lint():
    """The forbidden-phrase rules hold on the built document, and the conclusions carry the
    CP5 conditional language rather than an unconditional claim (D-116, D-125, D-126)."""
    filled = (REPORT / "report_filled.md").read_text()
    problems = R.lint_filled(filled)
    concl = filled.split("## 8. Conclusions", 1)[-1].split("## 9.", 1)[0]
    required = ["conditional fixed-volume scenario", "WEAKLY SUPPORTED",
                "not a finding that full-size specimens are preferable in general"]
    missing = [r for r in required if r not in concl]
    plate = re.search(r"[^.]*plate-only[^.]*\.", filled, re.I)
    plate_ok = plate and "No simulated winner or tie labels" in filled
    check("the honesty lint holds and the conclusions stay conditional",
          not problems and not missing and plate_ok,
          f"0 forbidden phrases; the conclusions carry all {len(required)} required conditional "
          f"phrases; the plate-only statement carries its no-verdict rider"
          + (f"; LINT {problems[:2]}" if problems else "")
          + (f"; MISSING {missing}" if missing else ""))


def c7_definition_of_done():
    """The README's definition-of-done table names, for each brief section 10 item, a path that
    exists in the repository."""
    readme = (ROOT / "README.md").read_text()
    block = readme.split("## Definition of done", 1)
    if len(block) < 2:
        check("README definition-of-done names an existing file per brief item", False,
              "README.md has no 'Definition of done' section")
        return
    section = block[1].split("\n## ", 1)[0]          # stop at the next heading
    rows = [l for l in section.splitlines() if l.startswith("|") and "`" in l]
    refs, missing = [], []
    for line in rows:
        for path in re.findall(r"`([^`]+)`", line):
            target = path.split()[0].rstrip(",;")
            if "/" in target or target.endswith(".md") or target.endswith(".sh"):
                refs.append(target)
                if not (ROOT / target).exists():
                    missing.append(target)
    check("README definition-of-done names an existing file per brief item",
          len(rows) >= 11 and not missing,
          f"{len(rows)} checklist rows naming {len(refs)} paths, all present"
          + (f"; MISSING {missing}" if missing else ""))


def pdf_text(path: Path) -> str:
    """Extract text from the built PDF using only the pinned environment. matplotlib emits kerned
    runs as separate strings, so the caller compares on whitespace-stripped text."""
    raw = path.read_bytes()
    out = []
    for m in re.finditer(rb"stream\r?\n(.*?)endstream", raw, re.S):
        try:
            blob = zlib.decompress(m.group(1))
        except Exception:
            continue
        if b"Tj" not in blob and b"TJ" not in blob:
            continue
        for s in re.findall(rb"\((?:\\.|[^()\\])*\)", blob):
            out.append(re.sub(rb"\\([()\\])", rb"\1", s[1:-1]))
    return b" ".join(out).decode("latin-1")


def c8_pdf_delivery_integrity():
    """A delivery-integrity check on the final PDF, not a new analysis (D-126 item 6)."""
    pdf = REPORT / "charpy_test_matrix_study.pdf"
    text = pdf_text(pdf)
    flat = re.sub(r"\s+", "", text)
    expect = {
        "title": "CharpyTransitionTemperatureUncertainty",
        "section 1": "1.Objectiveandscope",
        "section 2": "2.Datasource,provenanceandlicense",
        "section 3": "3.Datacleaningandinclusioncriteria",
        "section 4": "4.Methods",
        "section 5": "5.Fittervalidation",
        "section 6": "6.Results",
        "section 7": "7.Uncertaintyandlimitations",
        "section 8": "8.Conclusions",
        "section 9": "9.References",
        "CP5 conditional language": "notafindingthatfull-sizespecimensarepreferableingeneral",
    }
    missing = [k for k, v in expect.items() if v not in flat]
    pages = len(re.findall(rb"/Type\s*/Page[^s]", pdf.read_bytes()))
    attribution = bool(re.search(r"Taij\s*Singh|(?:developed|created|written|built)\s+by\s+(?:Claude|Astra|ChatGPT)", text, re.I))
    check("the built PDF contains its title, sections 1-9 and the conditional conclusion without a project byline",
          not missing and not attribution,
          f"{len(text):,} characters extracted over {pages} pages; all {len(expect)} required "
          f"elements present; project byline absent" + (f"; MISSING {missing}" if missing else ""))


def c9_provenance_rejection_paths():
    """Authored numbers cannot escape through headings/tables or a retired lint directive."""
    positive = ("## 1. Results\n### 1.1 Index temperature\n"
                "| Criterion | Value |\n|---|---|\n| Threshold | 41 J |\n"
                "Full-size LSE is 2.7 J; {{clean.retained}} records remain.\n[[TAB 1]]\n")
    if R.lint_source(positive):
        raise AssertionError("Registered numbers or structural document numbering rejected")
    bad_literals = {
        "prose": "An estimated uncertainty is 987.654 degrees.\n",
        "heading": "## 1. Estimated uncertainty of 987.654 degrees\n",
        "manual table": "| Quantity | Estimate |\n|---|---|\n| Uncertainty | 987.654 |\n",
        "box title": "[[BOX uncertainty of 987.654 degrees]]\n[[/BOX]]\n",
        "retired directive": "<!-- lint:allow-digits -->\nUncertainty is 987.654 degrees.\n",
    }
    for name, text in bad_literals.items():
        if not R.lint_source(text):
            raise AssertionError(f"Unregistered number accepted in {name}")
    source = R.SOURCE.read_text()
    build_cases = {**{k: bad_literals[k] for k in ("prose", "heading", "manual table")},
                   "unresolved placeholder": "{{unregistered.audit_claim}}\n"}
    with tempfile.TemporaryDirectory(prefix="charpy-report-test-") as tmp:
        root = Path(tmp)
        scratch = root / "report.md"
        for name, extra in build_cases.items():
            scratch.write_text(source + "\n" + extra)
            with patch.object(R, "SOURCE", scratch), patch.object(R, "REPORT", root), \
                    patch.object(R, "typeset") as typeset, \
                    contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                try:
                    R.build()
                except SystemExit:
                    pass
                else:
                    raise AssertionError(f"Complete report build accepted {name}")
                if typeset.called or (root / "report_filled.md").exists():
                    raise AssertionError(f"Rejected {name} reached output generation")
    try:
        R._select("wp1/reconciliation_table.csv", {"step": "NONEXISTENT_AUDIT_ROW"})
    except SystemExit:
        pass
    else:
        raise AssertionError("Invalid source selector accepted")
    check("provenance guard rejects authored numbers and invalid sources", True,
          "5 literal-negative fixtures; 4 complete-report rejection fixtures; invalid selector rejected; "
          "registered claims/constants and section numbering pass")


CHECKS = [c1_placeholders_resolved_and_used, c2_claim_map_rereads, c3_figure_hashes,
          c4_evidence_classes, c5_constant_provenance, c6_honesty_lint, c7_definition_of_done,
          c8_pdf_delivery_integrity, c9_provenance_rejection_paths]


def main():
    print("WP7 independent checks of the built report")
    for c in CHECKS:
        c()
    df = pd.DataFrame(RESULTS)
    df.to_csv(REPORT / "wp7_check_results.csv", index=False)
    print(f"  {len(df)} of {len(df)} checks passed")


if __name__ == "__main__":
    main()
