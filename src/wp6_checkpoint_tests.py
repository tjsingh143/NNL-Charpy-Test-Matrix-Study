"""D-127 regression tests for dependency invalidation and explicit cache adoption."""
from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import tempfile
from unittest.mock import patch

import numpy as np
import pandas as pd

from common import OUTPUTS
import wp6_checkpoint as C
import wp6_correction as K
import wp6_scatter as S


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures-only", action="store_true", help="before the explicit approved-cache upgrade")
    args = parser.parse_args()
    results = []

    def check(name, passed, detail):
        results.append(dict(check=name, passed=bool(passed), detail=detail))
        if not passed:
            raise AssertionError(f"{name}: {detail}")

    base = C.code_fingerprint()
    task = dict(correction={"kind": "central"}, scatter="C1", replicates=3)
    old_fp = C.fingerprint(base, **task)
    with tempfile.TemporaryDirectory(prefix="charpy-checkpoint-test-") as tmp:
        root = Path(tmp)
        sample = root / "sample.npz"
        payload = {"errors": np.array([1., np.nan, -2.], np.float32), "status": np.array(["ok", "missing"])}
        C.save_arrays(sample, payload, old_fp)
        check("unchanged dependencies preserve fingerprint", C.code_fingerprint() == base,
              "repeated source/input/runtime hashing is identical")
        wp5 = root / "wp5"
        wp5.mkdir()
        for rel, path in C.input_files().items():
            if rel.startswith("outputs/wp5/"):
                shutil.copyfile(path, wp5 / path.name)
        original_bias = K.central_scenario_values()["bias_c"]
        with patch.object(K, "WP5", wp5):
            same = C.code_fingerprint() == base
            path = wp5 / "wp6_size_correction_handoff.csv"
            t = pd.read_csv(path, float_precision="round_trip")
            t.loc[t.smaller_geometry.str.startswith("POOLED"), "central_bias_c"] += 1.
            t.to_csv(path, index=False)
            changed = C.code_fingerprint()
            check("resolved WP5 calibration change rejects old checkpoint",
                  same and K.central_scenario_values()["bias_c"] != original_bias and changed != base
                  and C.load_arrays(sample, C.fingerprint(changed, **task)) is None,
                  "an identical relocated input is equivalent; adding 1 deg C to the actual pooled bias invalidates")
        check("restored WP5 inputs restore fingerprint", C.code_fingerprint() == base,
              "scratch mutation never changes repository inputs")

        scatter_outputs = root / "scatter_outputs"
        for rel, path in C.input_files().items():
            if rel.startswith(("outputs/wp3/", "outputs/wp4/")):
                target = scatter_outputs / Path(rel).relative_to("outputs")
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(path, target)
        original_scale = S.wp4_profile()["sd"].to_numpy()
        with patch.object(S, "OUTPUTS", scatter_outputs):
            same = C.code_fingerprint() == base
            path = scatter_outputs / "wp4" / "published_residual_scatter_summary.csv"
            t = pd.read_csv(path, float_precision="round_trip")
            mask = (t.geometry_category.eq("full-size") & t.curve_set.str.startswith("usable")
                    & t.quantity.eq(S.RESIDUAL_QUANTITY))
            t.loc[mask, "sd"] += .001
            t.to_csv(path, index=False)
            changed = C.code_fingerprint()
            check("resolved scatter change rejects old checkpoint",
                  same and not np.array_equal(S.wp4_profile()["sd"].to_numpy(), original_scale)
                  and changed != base and C.load_arrays(sample, C.fingerprint(changed, **task)) is None,
                  "changing the WP4 C1 SD values invalidates without changing symbolic scatter='C1'")

        source_root = root / "source_root"
        for rel in C.SOURCES:
            target = source_root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(C.ROOT / rel, target)
        with patch.object(C, "ROOT", source_root):
            same = C.code_fingerprint() == base
            path = source_root / "src" / "wp6_experiment.py"
            original = path.read_text()
            changed_source = original.replace("np.percentile(vals, [2.5, 97.5])", "np.percentile(vals, [5., 95.])")
            if changed_source == original:
                raise AssertionError("T6 code-change fixture no longer matches coverage_task")
            path.write_text(changed_source)
            changed = C.code_fingerprint()
            check("result-affecting T6 code rejects old checkpoint",
                  same and changed != base and C.load_arrays(sample, C.fingerprint(changed, **task)) is None,
                  "changing coverage_task percentile limits in a source fixture invalidates")

        new_fp = C.fingerprint(base, **dict(task, replicates=4))
        before = C.payload_digest(payload)
        adopted = C.upgrade_approved_checkpoint(sample, old_fp, new_fp)
        check("explicit metadata upgrade preserves payload and rejects legacy key",
              adopted == before and C.payload_digest(C.load_arrays(sample, new_fp)) == before
              and C.load_arrays(sample, old_fp) is None,
              "all array bytes/dtypes/shapes preserved; normal loading has no legacy fallback")

    if not args.fixtures_only:
        import wp6_experiment as E
        grid = pd.read_csv(OUTPUTS / "wp6" / "experiment_grid.csv", float_precision="round_trip")
        selected = pd.read_csv(OUTPUTS / "wp6" / "monte_carlo_stability_selection.csv", float_precision="round_trip")
        code_fp, checked = C.code_fingerprint(), 0
        for frame, stability in [(grid, False), (selected, True)]:
            for row in frame.to_dict("records"):
                task = E._task_from_row(row)
                if stability:
                    task["replicates"] = 4000
                    task["crn_stream"] += "|stability-4000"
                if row["tier"] == "T6":
                    task["bootstrap_replicates"] = E.B_T6
                    fp = C.fingerprint(code_fp, kind="coverage", **{k: v for k, v in task.items() if k != "cell_id"})
                else:
                    fp = E._cell_fingerprint(code_fp, task)
                path = C.checkpoint_root() / ("stability" if stability else row["tier"]) / (C.slug(row["cell_id"]) + ".npz")
                if not C.has_arrays(path, fp):
                    raise AssertionError(f"Current checkpoint missing/invalid: {row['cell_id']}")
                checked += 1
        check("all current checkpoints use complete dependency fingerprints", checked == 6251,
              f"{checked} valid checkpoints: accepted 6188 cells and 63 bounded verification arms")
    pd.DataFrame(results).to_csv(OUTPUTS / "wp6" / "checkpoint_check_results.csv", index=False)
    print(f"WP6 checkpoint regression checks: {len(results)} passed")


if __name__ == "__main__":
    main()
