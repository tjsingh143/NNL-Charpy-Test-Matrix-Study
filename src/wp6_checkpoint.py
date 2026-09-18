"""WP6 - On-disk checkpoints for the long Monte Carlo run, so an interrupted run resumes instead of restarting.

Same design as WP4's (DECISIONS.md D-067, D-111) and it reuses WP4's atomic-write and fingerprint helpers, but
it keeps its OWN source list and its own cache directory, so that adding or editing WP6 code never invalidates
the WP4 checkpoint cache and no WP4 file is touched.

A checkpoint is reused only when its fingerprint matches exactly: a SHA-256 over every module that can change a
WP6 result, the Python and package versions, and the cell's own parameters. Files are written to a temporary
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
           "src/wp3_fitter.py", "src/wp5_normalization.py", "src/wp4_bootstrap.py"]


def checkpoint_root() -> Path:
    env = os.environ.get("WP6_CHECKPOINT_DIR", "").strip()
    return Path(env) if env else ROOT / "cache" / "wp6"


def code_fingerprint() -> str:
    import scipy
    h = hashlib.sha256()
    for rel in SOURCES:
        h.update(rel.encode())
        h.update((ROOT / rel).read_bytes())
    h.update(json.dumps(dict(python=platform.python_version(), numpy=np.__version__,
                             scipy=scipy.__version__, pandas=pd.__version__)).encode())
    return h.hexdigest()


def fingerprint(code_fp: str, **fields) -> str:
    h = hashlib.sha256(code_fp.encode())
    h.update(json.dumps(fields, sort_keys=True, default=str).encode())
    return h.hexdigest()
