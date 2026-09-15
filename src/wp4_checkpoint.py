"""WP4 - On-disk checkpoints for the long bootstrap runs, so that an interrupted run resumes instead of restarting.

A checkpoint is reused only if its fingerprint matches exactly: a SHA-256 over the source of every module that determines a result
(src/wp4_bootstrap.py, src/wp3_fitter.py, src/wp2_curves.py, src/wp3_validation.py), the Python and package versions, the run's parameters
(stream, seed method, replicates, targets) and the bytes of its input data. A reused checkpoint therefore holds exactly what recomputation
would produce (per-replicate seeds make every run deterministic, D-055). Files are written to a temporary name and renamed, so a
checkpoint is either complete or absent. The directory (default: cache/wp4/ in the repository, git-ignored; override with
WP4_CHECKPOINT_DIR) is a cache, not an output: deleting it only forces recomputation. Systems choice recorded in DECISIONS.md D-067.
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

SOURCES = ["src/wp4_bootstrap.py", "src/wp3_fitter.py", "src/wp2_curves.py", "src/wp3_validation.py"]


def checkpoint_root() -> Path:
    env = os.environ.get("WP4_CHECKPOINT_DIR", "").strip()
    return Path(env) if env else ROOT / "cache" / "wp4"


def code_fingerprint() -> str:
    import scipy
    h = hashlib.sha256()
    for rel in SOURCES:
        h.update(rel.encode())
        h.update((ROOT / rel).read_bytes())
    h.update(json.dumps(dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__, pandas=pd.__version__)).encode())
    return h.hexdigest()


def fingerprint(code_fp: str, arrays=(), **fields) -> str:
    h = hashlib.sha256(code_fp.encode())
    h.update(json.dumps(fields, sort_keys=True, default=str).encode())
    for a in arrays:
        h.update(np.ascontiguousarray(np.asarray(a, float)).tobytes())
    return h.hexdigest()


def _atomic(path: Path, write) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    write(tmp)
    os.replace(tmp, path)


def save_table(path: Path, table: pd.DataFrame, fp: str) -> None:
    _atomic(path, lambda tmp: table.assign(checkpoint_fingerprint=fp).to_csv(tmp, index=False))


def load_table(path: Path, fp: str):
    """The checkpointed table, or None if it is missing or was written for different code, parameters or data."""
    if not path.exists():
        return None
    t = pd.read_csv(path, float_precision="round_trip", keep_default_na=True)
    if len(t) == 0 or "checkpoint_fingerprint" not in t or not (t["checkpoint_fingerprint"] == fp).all():
        return None
    return t.drop(columns=["checkpoint_fingerprint"])


def save_arrays(path: Path, arrays: dict, fp: str) -> None:
    def write(tmp):
        with open(tmp, "wb") as fh:
            np.savez_compressed(fh, checkpoint_fingerprint=np.array(fp), **arrays)
    _atomic(path, write)


def load_arrays(path: Path, fp: str):
    if not path.exists():
        return None
    with np.load(path, allow_pickle=False) as z:
        if str(z["checkpoint_fingerprint"]) != fp:
            return None
        return {k: z[k] for k in z.files if k != "checkpoint_fingerprint"}


def has_arrays(path: Path, fp: str) -> bool:
    """True if a complete array checkpoint with this fingerprint exists (reads only the fingerprint member)."""
    if not path.exists():
        return False
    try:
        with np.load(path, allow_pickle=False) as z:
            return str(z["checkpoint_fingerprint"]) == fp
    except (OSError, ValueError, KeyError):
        return False


def slug(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]
