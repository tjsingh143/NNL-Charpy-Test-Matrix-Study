"""WP6 - On-disk checkpoints for the long Monte Carlo run, so an interrupted run resumes instead of restarting.

Same design as WP4's (DECISIONS.md D-067, D-111) and it reuses WP4's atomic-write and fingerprint helpers, but
it keeps its OWN source list and its own cache directory, so that adding or editing WP6 code never invalidates
the WP4 checkpoint cache and no WP4 file is touched.

A checkpoint is reused only when its fingerprint matches exactly: a SHA-256 over result-affecting source and
resolved input-file contents, the Python and package versions, and the cell's own parameters (D-111, D-127).
There is no automatic fallback to the weaker pre-D-127 fingerprint. Files are written to a temporary
name and renamed, so a checkpoint is either complete or absent. `cache/wp6/` is git-ignored: deleting it only
forces recomputation.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
from pathlib import Path

import numpy as np
import pandas as pd

from common import ROOT
from wp4_checkpoint import _atomic, has_arrays, load_arrays, load_table, save_arrays, save_table, slug  # noqa: F401

SOURCES = ["src/wp6_design.py", "src/wp6_scatter.py", "src/wp6_correction.py", "src/wp6_simulator.py",
           "src/wp6_experiment.py", "src/wp6_checkpoint.py", "src/wp6_stability.py",
           "src/common.py", "src/wp2_curves.py", "src/wp3_fitter.py", "src/wp5_normalization.py",
           "src/wp4_bootstrap.py", "src/wp4_checkpoint.py"]


def input_files() -> dict[str, Path]:
    """Actual paths resolved by the calibration readers, keyed without machine-specific paths.

    Hashing their bytes covers values, pool membership and cohort data, rather than merely
    recording filenames or symbolic scenario names. A relocated identical input is equivalent.
    """
    import common
    import wp6_correction as correction
    import wp6_scatter as scatter
    paths = {f"outputs/wp5/{name}": correction.WP5 / name for name in (
        "wp6_size_correction_handoff.csv", "size_correction_summary_overall.csv",
        "normalization_sensitivity_comparison.csv", "size_correction_residuals.csv")}
    paths.update({f"outputs/wp4/{name}": scatter.OUTPUTS / "wp4" / name for name in (
        "published_residual_scatter_summary.csv", "published_residual_scatter_dataset.csv")})
    paths.update({f"outputs/wp3/{name}": scatter.OUTPUTS / "wp3" / name for name in (
        "fits_primary.csv", "fits_looser_cohort_curves.csv")})
    for rel in ("data/processed/primary/charpy_records_with_curves.csv", "data/FROZEN_COHORTS_CP2.csv"):
        paths[rel] = common.ROOT / rel
    return paths


def dependency_manifest() -> dict:
    import scipy
    digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
    return dict(schema="WP6 input-sensitive checkpoints, D-127",
                sources={rel: digest(ROOT / rel) for rel in SOURCES},
                inputs={rel: digest(path) for rel, path in input_files().items()},
                runtime=dict(python=platform.python_version(), numpy=np.__version__,
                             scipy=scipy.__version__, pandas=pd.__version__))


def checkpoint_root() -> Path:
    env = os.environ.get("WP6_CHECKPOINT_DIR", "").strip()
    return Path(env) if env else ROOT / "cache" / "wp6"


def code_fingerprint() -> str:
    """Historical API name; now fingerprints both source and resolved upstream inputs."""
    encoded = json.dumps(dependency_manifest(), sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def fingerprint(code_fp: str, **fields) -> str:
    h = hashlib.sha256(code_fp.encode())
    h.update(json.dumps(fields, sort_keys=True, default=str).encode())
    return h.hexdigest()


def payload_digest(arrays: dict) -> str:
    """Bitwise digest excluding only the fingerprint metadata, for explicit approved migration."""
    h = hashlib.sha256()
    for key, value in sorted(arrays.items()):
        a = np.ascontiguousarray(value)
        h.update(json.dumps([key, a.dtype.str, a.shape]).encode())
        h.update(a.tobytes())
    return h.hexdigest()


def upgrade_approved_checkpoint(path: Path, old_fp: str, new_fp: str) -> str:
    """Explicit D-127 migration primitive; NEVER called by normal checkpoint loading.

    The caller must first establish approved-baseline code/input equivalence. Require the exact
    old task fingerprint and prove that re-keying leaves every result array bit-identical.
    """
    arrays = load_arrays(path, old_fp)
    if arrays is None:
        raise RuntimeError(f"Approved legacy checkpoint does not match its task: {path.name}")
    before = payload_digest(arrays)
    save_arrays(path, arrays, new_fp)
    after = load_arrays(path, new_fp)
    if after is None or payload_digest(after) != before:
        raise RuntimeError(f"Checkpoint payload changed during metadata upgrade: {path.name}")
    return before
