"""Shared helpers for the Charpy test-matrix study pipeline.

Deliberately small: project paths, raw-file checksum verification, a transparent
spreadsheet loader, and a Markdown table writer.

Why the loader does not use pandas.read_excel: see DECISIONS.md D-003. In short,
pandas silently turns the empty cells of the fluence column into the text '' and
leaves the column as generic objects, because fluence values such as 3e19 exceed
the 64-bit integer range after pandas converts whole-number floats to int.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import openpyxl
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RAW = DATA / "raw"
PROCESSED = DATA / "processed"
OUTPUTS = ROOT / "outputs"

# Two published releases of the dataset exist (DECISIONS.md D-001).
DATASETS = {
    "eny5v-www93": {
        "label": "Materials Cloud record eny5v-www93 (DOI 10.24435/materialscloud:gh-za, issued 2024-12-19)",
        "xlsx": RAW / "Charpy_Impact_Test_Dataset.xlsx",
        "record_json": RAW / "materialscloud_record_eny5v-www93.json",
    },
    "q4x6v-dyt25": {
        "label": "Materials Cloud record q4x6v-dyt25 (DOI 10.24435/materialscloud:p6-5y, issued 2025-02-26)",
        "xlsx": RAW / "alternate_record_q4x6v-dyt25" / "Charpy_Impact_Test_Dataset.xlsx",
        "record_json": RAW / "alternate_record_q4x6v-dyt25" / "materialscloud_record_q4x6v-dyt25.json",
    },
}
# The record named in PROJECT_BRIEF.md. Provisional until confirmed at CP1 (D-001).
PRIMARY_DATASET = "eny5v-www93"
COMPARISON_DATASET = "q4x6v-dyt25"

DATA_SHEET = "Charpy Data"


def file_digest(path: Path, algorithm: str) -> str:
    h = hashlib.new(algorithm)
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def verify_checksums() -> list[dict]:
    """Check every file listed in data/CHECKSUMS.sha256 and each workbook's MD5
    against the value published in its archive record. Raises on any mismatch."""
    results = []
    for line in (DATA / "CHECKSUMS.sha256").read_text().splitlines():
        expected, rel = line.split(maxsplit=1)
        actual = file_digest(DATA / rel, "sha256")
        results.append({"file": rel, "check": "SHA-256 vs data/CHECKSUMS.sha256",
                        "expected": expected, "actual": actual, "ok": actual == expected})
    for key, ds in DATASETS.items():
        entries = json.loads(ds["record_json"].read_text())["files"]["entries"]
        for name, entry in entries.items():
            path = ds["xlsx"].parent / name
            expected = entry["checksum"].split(":", 1)[1]
            actual = file_digest(path, "md5")
            results.append({"file": str(path.relative_to(DATA)), "check": f"MD5 vs archive record {key}",
                            "expected": expected, "actual": actual, "ok": actual == expected})
    bad = [r for r in results if not r["ok"]]
    if bad:
        raise RuntimeError(f"Checksum mismatch: {bad}")
    return results


def sheet_rows(xlsx: Path, sheet: str) -> list[tuple]:
    """All rows of a sheet as tuples of cached cell values (formulas -> their stored results)."""
    wb = openpyxl.load_workbook(xlsx, read_only=True, data_only=True)
    try:
        return [tuple(r) for r in wb[sheet].iter_rows(values_only=True)]
    finally:
        wb.close()


def load_charpy_data(xlsx: Path) -> pd.DataFrame:
    """Load the 'Charpy Data' sheet exactly as stored.

    Row 1 of the sheet holds merged group headings, row 2 the column names, data
    start on row 3. Column names are kept verbatim (including trailing spaces).
    A column becomes float64 (empty cell -> NaN) only if every non-empty cell is
    numeric; otherwise values stay as stored. `source_row` is the Excel row number,
    so every record can be traced back to the spreadsheet.
    """
    rows = sheet_rows(xlsx, DATA_SHEET)
    header = list(rows[1])
    df = pd.DataFrame([list(r) for r in rows[2:]], columns=header, dtype=object)
    for col in header:
        present = [v for v in df[col] if v is not None]
        if present and all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in present):
            df[col] = np.array([np.nan if v is None else float(v) for v in df[col]], dtype=float)
    df.insert(0, "source_row", np.arange(3, 3 + len(df)))
    return df


def load_references(xlsx: Path) -> pd.DataFrame:
    rows = sheet_rows(xlsx, "References")
    refs = pd.DataFrame(rows[1:], columns=["ref_id", "citation", "link"])
    refs["ref_id"] = refs["ref_id"].astype(int)
    refs["year"] = refs["citation"].str.extract(r"\((\d{4})\)", expand=False).astype(int)
    return refs


def md_escape(value) -> str:
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return ""
    return str(value).replace("|", "\\|").replace("\n", " ")


def md_table(df: pd.DataFrame, float_fmt: str = "{:.4g}") -> str:
    """Render a DataFrame as a GitHub-flavoured Markdown table (no extra dependency)."""
    def fmt(v):
        if isinstance(v, (float, np.floating)) and not np.isnan(v):
            return float_fmt.format(v)
        return md_escape(v)
    lines = ["| " + " | ".join(md_escape(c) for c in df.columns) + " |",
             "| " + " | ".join("---" for _ in df.columns) + " |"]
    for row in df.itertuples(index=False):
        lines.append("| " + " | ".join(fmt(v) for v in row) + " |")
    return "\n".join(lines)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n")
