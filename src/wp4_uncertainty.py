"""WP4 - Per-curve bootstrap uncertainty of the published Charpy curves of the CP2-frozen primary cohort (analysis of published test data).

Reads the frozen cohorts (checked against data/FROZEN_COHORTS_CP2.csv before anything is fitted), refits every primary curve with the
final approved WP3 method and stops unless the refits reproduce outputs/wp3/fits_primary.csv, then:
  1. runs the PRIMARY nonparametric pairs bootstrap and the fixed-design wild bootstrap SENSITIVITY on all 170 curves (B = 2,000 each,
     deterministic per-replicate seeds; D-052 to D-055);
  2. summarises every target with failure-aware accounting and the 95 % finite-target reporting rule (D-056 to D-059);
  3. reruns a predeclared subset with B = 4,000 on an independent seed stream (Monte Carlo stability, D-055);
  4. characterizes the empirical published-data residual scatter of the WP3 point fits (D-061), relates uncertainty to pre-existing
     sampling properties (D-062), cross-checks against published uncertainty estimates (D-063), compares the two methods (D-064);
  5. draws the worked-example figure and a diagnostic figure for curve 33-153 (D-065) and writes wp4_summary.md.
Outputs (outputs/wp4/, besides the synthetic_* files of src/wp4_validation.py): listed in method_configuration.md and wp4_summary.md.

Run:  .venv/bin/python src/wp4_uncertainty.py      (after src/wp3_fit_curves.py and src/wp4_validation.py)
"""
from __future__ import annotations

import textwrap
import time

import numpy as np
import pandas as pd
from scipy import stats

import wp3_fit_curves as W3
import wp3_fitter as F
import wp4_bootstrap as B
import wp4_checkpoint as CK
from common import DATA, OUTPUTS, PRIMARY_DATASET, md_table, write_text

OUT = OUTPUTS / "wp4"
DATA_TYPE = "published measurements (analysis of published test data)"
WORKERS = B.worker_count()      # conservative default (3) for the 8 GB project machine; results do not depend on it (D-067)
METHODS = [B.PAIRS, B.WILD]
QUALITY = {F.OUTCOMES[0]: "optimizer failure", F.OUTCOMES[1]: "non-physical (inadmissible)", F.OUTCOMES[2]: "boundary-limited",
           F.OUTCOMES[3]: "weakly identified", F.OUTCOMES[4]: "usable", F.OUTCOMES[5]: "usable"}
CURVE_33_153 = W3.CURVE_THAT_EXPOSED_BRACKETING_GAP        # the one T41J not bracketed by its measured energies (D-044)
STABILITY_SEED_SUFFIX = "|stability-4000"

# D-061. Regions of the fitted curve for the residual characterization (x = (T - T0) / C; the four WP3 regions of
# residual_pattern_by_lower_shelf_outcome.csv plus the upper shelf), and three coarser zones for the strata.
REGIONS = [("lower shelf (x <= -1.5)", lambda x: x <= -1.5), ("lower transition (-1.5 < x <= -0.5)", lambda x: (x > -1.5) & (x <= -0.5)),
           ("central transition (-0.5 < x < 0.5)", lambda x: (x > -0.5) & (x < 0.5)),
           ("upper transition (0.5 <= x < 1.5)", lambda x: (x >= 0.5) & (x < 1.5)), ("upper shelf (x >= 1.5)", lambda x: x >= 1.5)]
ZONES = [("lower shelf (x <= -1.5)", lambda x: x <= -1.5), ("transition (-1.5 < x < 1.5)", lambda x: (x > -1.5) & (x < 1.5)),
         ("upper shelf (x >= 1.5)", lambda x: x >= 1.5)]
MIN_CURVES_STRATUM, MIN_RESIDUALS_STRATUM = 10, 30          # D-061: smaller strata are shown but marked "too few to interpret"

# D-063. Published values used in the cross-check, each read from the source named (DECISIONS.md WP4 sources).
MARINI_T41 = dict(a=3.1, b=1.2, c_best=12.5, c_upper=16.0, shift_min=-0.23, shift_max=1.33)   # Marini 2020 Table 13, Table 8 shifts
MARINI_RCCM = dict(n=18, sigma=3.52, accuracy=-0.13, uncertainty=3.52, use_sigma=4.44, shift=0.67)  # Table 6, Table 7, Table 14
MIURA_STANDARD = dict(lse=3.0, use=200.0, c=50.0, n_lse=2, n_use=4, n_tt=6, cv_lse=0.1, cv_use=0.1, cv_cve=0.49)   # preprint §4


# ---------------------------------------------------------------------------
# 1. Data, and the check that WP4 refits reproduce the approved WP3 point fits
# ---------------------------------------------------------------------------
def load_primary() -> tuple:
    membership = W3.check_frozen_cohorts()
    curves, rec = W3.load_curves(membership)
    primary = curves[curves["in_primary"]].reset_index(drop=True)
    frozen = pd.read_csv(DATA / "FROZEN_COHORTS_CP2.csv").set_index(["release", "cohort"]).loc[(PRIMARY_DATASET, "primary")]
    if len(primary) != frozen["curves"] or int(primary["n_points"].sum()) != frozen["records"]:
        raise AssertionError("primary cohort size differs from the CP2 freeze")
    wp3 = pd.read_csv(OUTPUTS / "wp3" / "fits_primary.csv", float_precision="round_trip").set_index("curve_id")
    by_id = rec.set_index("record_id")
    data = {}
    for c in primary.itertuples(index=False):
        s = by_id.loc[c.record_ids.split()].sort_values("source_row")
        t, e = s["test_temp_c"].to_numpy(float), s["energy_j"].to_numpy(float)
        category = W3.GEOMETRY_CATEGORY[c.geometry_class]
        data[c.curve_id] = dict(t=t, e=e, category=category, est=B.wp3_estimate(t, e, category), record_ids=list(s.index),
                                source_rows=s["source_row"].to_numpy(int))
    return primary, rec, wp3, data


def reproduction_check(wp3: pd.DataFrame, data: dict) -> pd.DataFrame:
    """Stop unless the WP4 refit of every original curve reproduces the approved WP3 fit table (same code, same record order)."""
    rows = []
    numeric = {"lse_j": "lse_j", "use_j": "use_j", "t0_c": "t0_c", "c_c": "c_c", "sse": "sse"}
    for cid, d in data.items():
        est, w = d["est"], wp3.loc[cid]
        diffs = {k: abs(est["fit"][k] - w[col]) for k, col in numeric.items()}
        diffs["index_temperature_c"] = (0.0 if (np.isnan(est["t41"]) and np.isnan(w["index_temperature_c"]))
                                        else abs(est["t41"] - w["index_temperature_c"]))
        same = dict(outcome=est["cls"]["outcome"] == w["outcome"], index_status=est["index_status"] == w["index_status"],
                    flag_index_near_fitted_shelf=bool(est["cls"]["flag_index_near_fitted_shelf"]) == bool(w["flag_index_near_fitted_shelf"]),
                    flag_index_not_bracketed=bool(est["bracketing"]["flag_index_not_bracketed_by_measured_energy"]) ==
                    bool(w["flag_index_not_bracketed_by_measured_energy"]))
        rows.append(dict(curve_id=cid, **{f"abs_difference_{k}": v for k, v in diffs.items()}, **{f"identical_{k}": v for k, v in same.items()}))
    t = pd.DataFrame(rows)
    worst = t[[c for c in t.columns if c.startswith("abs_difference")]].max()
    ok = bool((worst <= 1e-9).all() and t[[c for c in t.columns if c.startswith("identical")]].all().all())
    summary = pd.DataFrame([dict(data_type=DATA_TYPE, check="WP4 refit of every primary curve reproduces outputs/wp3/fits_primary.csv",
                                 curves=len(t), **{f"max_{k}": v for k, v in worst.items()},
                                 **{f"all_{c}": bool(t[c].all()) for c in t.columns if c.startswith("identical")}, passed=ok)])
    if not ok:
        raise AssertionError("WP4 refits do not reproduce the approved WP3 point fits:\n" + summary.T.to_string())
    return summary


# ---------------------------------------------------------------------------
# 2. Bootstrap runs
# ---------------------------------------------------------------------------
def bootstrap_task(payload) -> tuple:
    """Worker: one curve and one method; returns the replicate arrays (the parent saves them to a checkpoint at once)."""
    cid, method, t, e, category, n_replicates, seed_method = payload
    return cid, method, B.run_replicates(t, e, category, method, cid, range(n_replicates), seed_method)


class RunStore:
    """The replicate arrays of the bootstrap runs of the published curves, kept on disk as verified checkpoints (cache/wp4/published/, D-067)
    and loaded one run at a time: store[(curve_id, method)] returns that run's arrays. Only summaries are held in memory."""

    def __init__(self, data: dict, code_fp: str, n_replicates: int, seed_suffix: str = ""):
        self.data, self.code_fp, self.n, self.suffix = data, code_fp, n_replicates, seed_suffix
        self.root = CK.checkpoint_root() / "published" / f"B{n_replicates}{seed_suffix.replace('|', '_')}"

    def path(self, cid: str, method: str):
        return self.root / method / f"{cid}.npz"

    def fp(self, cid: str, method: str) -> str:
        d = self.data[cid]
        return CK.fingerprint(self.code_fp, arrays=[d["t"], d["e"]], curve_id=cid, method=method, seed_method=method + self.suffix,
                              replicates=self.n, category=d["category"], seed=B.WP4_SEED)

    def __getitem__(self, key) -> dict:
        cid, method = key
        arrays = CK.load_arrays(self.path(cid, method), self.fp(cid, method))
        if arrays is None:
            raise KeyError(f"no verified bootstrap checkpoint for {key}")
        arrays["errors"] = [str(x) for x in arrays.pop("errors")]
        return arrays

    def ensure(self, curve_ids) -> tuple:
        """Compute every run that has no verified checkpoint, saving each as it arrives. Returns (computed, resumed)."""
        keys = [(cid, m) for cid in curve_ids for m in METHODS]
        pending = sorted([k for k in keys if not CK.has_arrays(self.path(*k), self.fp(*k))], key=lambda k: (-len(self.data[k[0]]["t"]), k))
        print(f"bootstrap B = {self.n}{self.suffix}: {len(keys)} runs, {len(keys) - len(pending)} resumed from verified checkpoints, "
              f"{len(pending)} to compute with {WORKERS} worker processes", flush=True)
        payloads = ((cid, m, self.data[cid]["t"], self.data[cid]["e"], self.data[cid]["category"], self.n, m + self.suffix) for cid, m in pending)
        t_start = time.perf_counter()
        for k, (cid, m, r) in enumerate(B.stream_map(bootstrap_task, payloads, WORKERS), start=1):
            if len(r["outcome_code"]) != self.n:
                raise AssertionError(f"{cid} {m}: {len(r['outcome_code'])} replicates returned, {self.n} requested")
            CK.save_arrays(self.path(cid, m), {**{f: r[f] for f in B.REPLICATE_FIELDS + ["replicate"]},
                                               "errors": np.array(r["errors"], dtype=str)}, self.fp(cid, m))
            if k % 20 == 0 or k == len(pending):
                print(f"  {k}/{len(pending)} runs saved; {(time.perf_counter() - t_start) / 60:.1f} min", flush=True)
        return len(pending), len(keys) - len(pending)


def determinism_spot_check(data: dict, reps: dict) -> pd.DataFrame:
    """Published-data spot check: replicates 0-249 of two curves recomputed in this single process must equal the pooled run exactly."""
    rows = []
    ids = sorted(data, key=lambda c: (len(data[c]["t"]), c))
    for cid in [ids[0], ids[-1]]:
        d = data[cid]
        for method in METHODS:
            stored = reps[(cid, method)]
            n = min(250, len(stored["outcome_code"]))
            single = B.run_replicates(d["t"], d["e"], d["category"], method, cid, range(n), method)
            pooled = {k: v[:n] for k, v in stored.items() if k != "errors"}
            same = all(np.array_equal(single[k], pooled[k], equal_nan=single[k].dtype.kind == "f") for k in B.REPLICATE_FIELDS)
            rows.append(dict(data_type=DATA_TYPE, curve_id=cid, n_points=len(d["t"]), method=method, replicates_compared=n,
                             compared="single process, one chunk vs the pooled multi-process run", identical=same))
    out = pd.DataFrame(rows)
    if not out["identical"].all():
        raise AssertionError("published-data determinism spot check failed")
    return out


# ---------------------------------------------------------------------------
# 3. Summaries (long tables, accounting, wide per-geometry tables)
# ---------------------------------------------------------------------------
META = ["curve_id", "ref_id", "material_family", "product_form_group", "irradiated", "geometry", "geometry_category", "geometry_description",
        "flag_full_size_notch_dimensions_unreported", "reconstituted", "in_stricter", "n_points", "n_temperatures", "T_span_c", "outcome",
        "outcome_reason"]


def original_value(w: pd.Series, target: str) -> float:
    if target == "lse" and w["lse_mode"] != "fitted":
        return np.nan
    return float(w[B.ORIGINAL_COLUMN[target]])


def summarise_method(wp3: pd.DataFrame, data: dict, reps: dict, method: str) -> tuple:
    long_rows, acc_rows = [], []
    for cid, d in data.items():
        w = wp3.loc[cid]
        r = reps[(cid, method)]
        meta = {k: (cid if k == "curve_id" else w[k]) for k in META}
        acc = B.accounting(r, d["category"])
        acc_rows.append(dict(data_type=DATA_TYPE, **meta, method=method, errors="; ".join(sorted(set(r["errors"])))[:300], **acc))
        for target in B.TARGETS[d["category"]]:
            s = B.summarise_target(r, target, original_value(w, target), w["outcome"])
            if s["finite_target_values"] + s["target_unavailable"] != s["replicates_requested"]:
                raise AssertionError("finite + unavailable replicates do not equal the replicates requested")
            if target == "lse" and w["lse_mode"] != "fitted":
                continue
            rel = (lambda x: x / s["original_estimate"]) if target == "use" else (lambda x: np.nan)
            long_rows.append(dict(data_type=DATA_TYPE, **meta, method=method, method_label=B.METHOD_LABELS[method], target=target,
                                  target_label=B.TARGET_LABELS[target], target_role=B.TARGET_ROLE[(d["category"], target)], **s,
                                  relative_interval_width=rel(s["interval_width"]), relative_sd=rel(s["sd"])))
    return pd.DataFrame(long_rows), pd.DataFrame(acc_rows)


STAT_COLS = ["finite_target_fraction", "q025", "median", "q975", "mean", "sd", "interval_width", "bias_mean_minus_original",
             "robust_sd_q84_minus_q16_over_2", "interval_reportable", "interval_label"]


def wide(long: pd.DataFrame, target: str, extra_meta: list, wp3: pd.DataFrame) -> pd.DataFrame:
    parts = []
    for method in METHODS:
        s = long[(long["target"] == target) & (long["method"] == method)].set_index("curve_id")
        cols = STAT_COLS + (["relative_interval_width", "relative_sd"] if target == "use" else [])
        parts.append(s[cols].add_prefix(f"{method}_"))
    base = long[(long["target"] == target) & (long["method"] == B.PAIRS)].set_index("curve_id")[
        [c for c in META if c != "curve_id"] + ["original_estimate"]]
    t = base.join(wp3[extra_meta]).join(parts[0]).join(parts[1])
    t["ratio_sd_pairs_to_wild"] = t["pairs_sd"] / t["wild_sd"]
    t["ratio_width_pairs_to_wild"] = t["pairs_interval_width"] / t["wild_interval_width"]
    t.insert(0, "data_type", DATA_TYPE)
    return t.reset_index()


def interval_availability(long: pd.DataFrame) -> pd.DataFrame:
    g = (long.assign(quality=long["outcome"].map(QUALITY))
         .groupby(["method", "geometry_category", "target", "target_role", "quality", "outcome", "interval_label"]).size().rename("curves").reset_index())
    return g.sort_values(["method", "geometry_category", "target", "outcome", "interval_label"])


def curve_accounting(long: pd.DataFrame) -> pd.DataFrame:
    """For each method and each geometry's primary target (full-size T41J; miniature T0) and USE: curves with a primary CI, a diagnostic
    interval and no interval, by original WP3 outcome, with totals that must equal the curves of that geometry."""
    rows = []
    keys = [("full-size", "t41j"), ("full-size", "use"), ("full-size", "t0"), ("miniature", "t0"), ("miniature", "use")]
    for method in METHODS:
        for cat, target in keys:
            s = long[(long["method"] == method) & (long["geometry_category"] == cat) & (long["target"] == target)]
            for outcome in F.OUTCOMES + ["ALL"]:
                h = s if outcome == "ALL" else s[s["outcome"] == outcome]
                if outcome != "ALL" and len(h) == 0:
                    continue
                rows.append(dict(method=method, geometry_category=cat, target=target, original_wp3_outcome=outcome, curves=len(h),
                                 primary_bootstrap_ci=int((h["interval_label"] == B.INTERVAL_PRIMARY).sum()),
                                 diagnostic_bootstrap_interval=int((h["interval_label"] == B.INTERVAL_DIAGNOSTIC).sum()),
                                 interval_unavailable=int((h["interval_label"] == B.INTERVAL_UNAVAILABLE).sum())))
    t = pd.DataFrame(rows)
    chk = t[t["original_wp3_outcome"] == "ALL"]
    if not (chk["primary_bootstrap_ci"] + chk["diagnostic_bootstrap_interval"] + chk["interval_unavailable"] == chk["curves"]).all():
        raise AssertionError("interval labels do not account for every curve")
    return t


def failure_summary(acc: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (method, cat, outcome), h in acc.groupby(["method", "geometry_category", "outcome"]):
        req = h["replicates_requested"].sum()
        r = dict(method=method, geometry_category=cat, original_wp3_outcome=outcome, curves=len(h), replicates_requested=int(req),
                 replicates_accounted=int(h[[f"replicates_{o}" for o in F.OUTCOMES] + ["replicate_evaluation_errors"]].sum().sum()))
        for o in F.OUTCOMES:
            r[f"share_{o}"] = h[f"replicates_{o}"].sum() / req
        r["share_evaluation_errors"] = h["replicate_evaluation_errors"].sum() / req
        if cat == "full-size":
            for code, label in enumerate(B.INDEX_STATUS_LABELS):
                if code == 1:
                    continue
                r[f"share_t41j_{label}"] = h[f"t41j_status_{code}"].sum() / req
        r["share_replicates_lost_lowest_temperature"] = h["replicates_with_lost_lowest_temperature"].sum() / req
        r["share_replicates_lost_highest_temperature"] = h["replicates_with_lost_highest_temperature"].sum() / req
        rows.append(r)
    t = pd.DataFrame(rows)
    if not (t["replicates_accounted"] == t["replicates_requested"]).all():
        raise AssertionError("replicates were lost from the accounting")
    return t


def support_table(wp3: pd.DataFrame, acc: pd.DataFrame, long: pd.DataFrame) -> pd.DataFrame:
    fs = wp3[wp3["geometry_category"] == "full-size"]
    rows = []
    for cid, w in fs.iterrows():
        r = dict(data_type=DATA_TYPE, curve_id=cid, outcome=w["outcome"], index_temperature_c=w["index_temperature_c"],
                 criterion_bracketed_by_measured_energy=bool(w["criterion_bracketed_by_measured_energy"]),
                 n_points_below_criterion=int(w["n_points_below_criterion"]), n_points_above_criterion=int(w["n_points_above_criterion"]),
                 flag_index_not_bracketed_by_measured_energy=bool(w["flag_index_not_bracketed_by_measured_energy"]),
                 index_fraction_of_rise=w["index_fraction_of_rise"], flag_index_near_fitted_shelf=bool(w["flag_index_near_fitted_shelf"]),
                 flag_full_size_notch_dimensions_unreported=bool(w["flag_full_size_notch_dimensions_unreported"]))
        for method in METHODS:
            a = acc[(acc["curve_id"] == cid) & (acc["method"] == method)].iloc[0]
            s = long[(long["curve_id"] == cid) & (long["method"] == method) & (long["target"] == "t41j")].iloc[0]
            req, calc = a["replicates_requested"], a["t41j_status_0"]
            r.update({f"{method}_share_replicate_energies_bracket_41j": a["replicates_energies_bracket_41j"] / req,
                      f"{method}_t41j_finite_fraction": s["finite_target_fraction"],
                      f"{method}_share_of_finite_t41j_not_bracketed": a["t41j_calculated_not_bracketed"] / calc if calc else np.nan,
                      f"{method}_share_of_finite_t41j_with_index_position_warning": a["t41j_calculated_index_position_warning"] / calc if calc else np.nan,
                      f"{method}_share_of_finite_t41j_from_usable_replicate_fit": a["t41j_calculated_from_usable_replicate_fit"] / calc if calc else np.nan,
                      f"{method}_share_t41j_unsupported_below_lowest_temperature": a["t41j_status_4"] / req,
                      f"{method}_share_t41j_unsupported_above_highest_temperature": a["t41j_status_5"] / req,
                      f"{method}_share_t41j_undefined": a["t41j_status_3"] / req,
                      f"{method}_share_t41j_optimizer_failure": a["t41j_status_2"] / req,
                      f"{method}_interval_label": s["interval_label"]})
        rows.append(r)
    return pd.DataFrame(rows)


def distribution_rows(values: pd.Series, **labels) -> dict:
    v = values.dropna()
    q = v.quantile([0.1, 0.25, 0.5, 0.75, 0.9]) if len(v) else pd.Series([np.nan] * 5, index=[0.1, 0.25, 0.5, 0.75, 0.9])
    return dict(**labels, curves=len(v), minimum=v.min() if len(v) else np.nan, p10=q[0.1], p25=q[0.25], median=q[0.5], p75=q[0.75],
                p90=q[0.9], maximum=v.max() if len(v) else np.nan)


def t41j_group_distributions(t41: pd.DataFrame) -> pd.DataFrame:
    """Distributions of the full-size T41J bootstrap SD, 95 % width and finite fraction, by the groups the WP4 handoff separates."""
    groups = [("all full-size curves", pd.Series(True, index=t41.index)),
              ("original WP3 outcome: usable fit", t41["outcome"].isin(F.OUTCOMES[4:])),
              ("original WP3 outcome: weakly identified", t41["outcome"] == F.OUTCOMES[3]),
              ("original WP3 outcome: boundary-limited", t41["outcome"] == F.OUTCOMES[2]),
              ("notch dimensions reported", ~t41["flag_full_size_notch_dimensions_unreported"].astype(bool)),
              ("exact notch dimensions unreported", t41["flag_full_size_notch_dimensions_unreported"].astype(bool)),
              ("index-position warning (41 J outside 11.9-88.1 % of the fitted rise)", t41["flag_index_near_fitted_shelf"].astype(bool)),
              ("no index-position warning", ~t41["flag_index_near_fitted_shelf"].astype(bool)),
              (f"empirically unbracketed T41J ({CURVE_33_153})", t41["flag_index_not_bracketed_by_measured_energy"].astype(bool))]
    rows = []
    for method in METHODS:
        for name, mask in groups:
            h = t41[mask]
            for col, label, subset in [(f"{method}_sd", "bootstrap SD of T41J (°C), reportable intervals", h[f"{method}_interval_reportable"]),
                                       (f"{method}_interval_width", "95 % interval width of T41J (°C), reportable intervals", h[f"{method}_interval_reportable"]),
                                       (f"{method}_sd", "bootstrap SD of T41J (°C), all curves (conditional on finite values)", pd.Series(True, index=h.index)),
                                       (f"{method}_finite_target_fraction", "finite-T41J fraction of the 2,000 replicates", pd.Series(True, index=h.index))]:
                rows.append(distribution_rows(h.loc[subset.astype(bool), col], method=method, group=name, quantity=label,
                                              curves_in_group=len(h), curves_without_reportable_interval=int((~h[f"{method}_interval_reportable"].astype(bool)).sum())))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 4. Monte Carlo stability (predeclared subset, D-055)
# ---------------------------------------------------------------------------
def stability_subset(wp3: pd.DataFrame, long_pairs: pd.DataFrame) -> pd.DataFrame:
    picks = []
    fits = wp3.reset_index()
    fits["quality"] = np.where(fits["outcome"].isin(F.OUTCOMES[4:]), "usable fit", "weakly identified or boundary-limited fit")
    for (cat, quality), g in fits.groupby(["geometry_category", "quality"], sort=True):
        g = g.sort_values(["n_points", "curve_id"]).reset_index(drop=True)
        for label, i in [("fewest points", 0), ("median points", (len(g) - 1) // 2), ("most points", len(g) - 1)]:
            picks.append((g.loc[i, "curve_id"], f"{cat}, {quality}: {label} ({g.loc[i, 'n_points']} points)"))
    for cat, target in [("full-size", "t41j"), ("miniature", "t0")]:
        s = long_pairs[(long_pairs["geometry_category"] == cat) & (long_pairs["target"] == target) & long_pairs["interval_reportable"]]
        s = s.sort_values(["interval_width", "curve_id"])
        if len(s) == 0:
            continue
        picks.append((s.iloc[0]["curve_id"], f"{cat}: narrowest reportable pairs {target} interval ({s.iloc[0]['interval_width']:.3g})"))
        picks.append((s.iloc[-1]["curve_id"], f"{cat}: broadest reportable pairs {target} interval ({s.iloc[-1]['interval_width']:.3g})"))
    t = pd.DataFrame(picks, columns=["curve_id", "reason"]).groupby("curve_id", sort=False)["reason"].agg("; ".join).reset_index()
    return t


def stability_table(sub: pd.DataFrame, wp3: pd.DataFrame, data: dict, reps: dict, reps_4000: dict) -> pd.DataFrame:
    rows = []
    for cid, reason in zip(sub["curve_id"], sub["reason"]):
        w = wp3.loc[cid]
        for method in METHODS:
            for target in B.TARGETS[data[cid]["category"]]:
                if target in ("c", "lse"):
                    continue
                a = B.summarise_target(reps[(cid, method)], target, original_value(w, target), w["outcome"])
                b = B.summarise_target(reps_4000[(cid, method)], target, original_value(w, target), w["outcome"])
                row = dict(data_type=DATA_TYPE, curve_id=cid, selection_reason=reason, geometry_category=w["geometry_category"],
                           outcome=w["outcome"], n_points=int(w["n_points"]), method=method, target=target)
                for k in ["finite_target_fraction", "q025", "median", "q975", "sd", "interval_width"]:
                    row[f"b2000_{k}"], row[f"b4000_{k}"] = a[k], b[k]
                    if k != "finite_target_fraction":
                        row[f"change_{k}"] = b[k] - a[k]
                row["change_finite_target_fraction"] = b["finite_target_fraction"] - a["finite_target_fraction"]
                scale = a["interval_width"]
                changes = np.abs([row["change_q025"], row["change_median"], row["change_q975"]])
                row["max_abs_endpoint_or_median_change_as_share_of_b2000_width"] = (
                    float(np.max(changes)) / scale if np.isfinite(scale) and scale > 0 and np.all(np.isfinite(changes)) else np.nan)
                row["reportable_status_changes"] = bool(a["interval_reportable"] != b["interval_reportable"])
                rows.append(row)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 5. Empirical published-data residual scatter of the WP3 point fits (D-061)
# ---------------------------------------------------------------------------
def region_of(x: float) -> str:
    hits = [name for name, inside in REGIONS if inside(x)]
    if len(hits) != 1:
        raise ValueError(f"x = {x} falls in {len(hits)} regions")
    return hits[0]


def residual_dataset(wp3: pd.DataFrame, data: dict) -> pd.DataFrame:
    rows = []
    for cid, d in data.items():
        w, fit = wp3.loc[cid], d["est"]["fit"]
        adj = B.leverage_adjusted_residuals(d["t"], d["e"], fit)
        x = (d["t"] - fit["t0_c"]) / fit["c_c"]
        rise = fit["use_j"] - fit["lse_j"]
        slope = 0.5 * rise / fit["c_c"] * (1.0 - np.tanh(x) ** 2)
        for i in range(len(d["t"])):
            rows.append(dict(data_type=DATA_TYPE, record_id=d["record_ids"][i], source_row=int(d["source_rows"][i]), curve_id=cid,
                             ref_id=int(w["ref_id"]), geometry_category=w["geometry_category"], geometry=w["geometry"],
                             material_family=w["material_family"], product_form=w["product_form"], product_form_group=w["product_form_group"],
                             irradiated=bool(w["irradiated"]), wp3_outcome=w["outcome"], wp3_fit_usable=w["outcome"] in F.OUTCOMES[4:],
                             wp3_outcome_reason=w["outcome_reason"], lse_mode=w["lse_mode"],
                             test_temp_c=d["t"][i], measured_energy_j=d["e"][i], fitted_energy_j=adj["fitted"][i],
                             residual_j=adj["residual"][i], residual_over_fitted_use=adj["residual"][i] / fit["use_j"],
                             leverage=adj["leverage"][i], leverage_adjusted_residual_j=adj["adjusted"][i],
                             leverage_adjusted_residual_over_fitted_use=adj["adjusted"][i] / fit["use_j"],
                             x_normalized_temperature=x[i], fraction_of_fitted_rise=(adj["fitted"][i] - fit["lse_j"]) / rise if rise > 0 else np.nan,
                             region=region_of(x[i]), fitted_slope_j_per_c=slope[i], fitted_use_j=fit["use_j"], fitted_lse_j=fit["lse_j"],
                             fitted_t0_c=fit["t0_c"], fitted_c_c=fit["c_c"]))
    df = pd.DataFrame(rows)
    if len(df) != sum(len(d["t"]) for d in data.values()):
        raise AssertionError("residual dataset does not cover every record")
    return df


def scale_stats(v: pd.Series) -> dict:
    v = v.dropna()
    if len(v) == 0:
        return dict(mean=np.nan, sd=np.nan, median=np.nan, mad_scaled=np.nan, q05=np.nan, q25=np.nan, q75=np.nan, q95=np.nan)
    q = v.quantile([0.05, 0.25, 0.75, 0.95])
    return dict(mean=v.mean(), sd=v.std(ddof=1) if len(v) > 1 else np.nan, median=v.median(),
                mad_scaled=1.4826 * float(np.median(np.abs(v - v.median()))), q05=q[0.05], q25=q[0.25], q75=q[0.75], q95=q[0.95])


def residual_summaries(res: pd.DataFrame) -> tuple:
    rows = []
    for curve_set, sel in [("usable WP3 fits (primary summary)", res["wp3_fit_usable"]), ("all WP3 fits (sensitivity)", pd.Series(True, index=res.index))]:
        for cat in ["full-size", "miniature"]:
            for region, _ in REGIONS:
                h = res[sel & (res["geometry_category"] == cat) & (res["region"] == region)]
                for quantity, col in [("residual / fitted USE", "residual_over_fitted_use"),
                                      ("leverage-adjusted residual / fitted USE", "leverage_adjusted_residual_over_fitted_use"),
                                      ("residual (J)", "residual_j")]:
                    rows.append(dict(data_type=DATA_TYPE, curve_set=curve_set, geometry_category=cat, region=region, quantity=quantity,
                                     residuals=len(h), curves=h["curve_id"].nunique(), **scale_stats(h[col])))
    summary = pd.DataFrame(rows)
    strata = []
    usable_fs = res[res["wp3_fit_usable"] & (res["geometry_category"] == "full-size")]
    for dim in ["product_form_group", "irradiated"]:
        for value, g in usable_fs.groupby(dim):
            for zone, inside in ZONES:
                h = g[inside(g["x_normalized_temperature"])]
                n_curves = h["curve_id"].nunique()
                strata.append(dict(data_type=DATA_TYPE, curve_set="usable WP3 fits, full-size", dimension=dim, value=str(value), zone=zone,
                                   residuals=len(h), curves=n_curves,
                                   interpretable=bool(n_curves >= MIN_CURVES_STRATUM and len(h) >= MIN_RESIDUALS_STRATUM),
                                   **scale_stats(h["leverage_adjusted_residual_over_fitted_use"])))
    return summary, pd.DataFrame(strata)


# ---------------------------------------------------------------------------
# 6. Uncertainty against pre-existing sampling properties (D-062)
# ---------------------------------------------------------------------------
SAMPLING_PROPERTIES = [("n_points", "specimens (N)"), ("n_temperatures", "distinct test temperatures"), ("T_span_c", "tested temperature span (°C)"),
                       ("n_T_transition_fit", "distinct temperatures inside T0 ± C (WP3 fit)"),
                       ("n_points_transition_fit", "specimens inside T0 ± C (WP3 fit)"),
                       ("n_points_lower_shelf_fit", "specimens on the fitted lower shelf (x <= -1.5)"),
                       ("n_points_upper_shelf_fit", "specimens on the fitted upper shelf (x >= 1.5)"),
                       ("wp2_n_T_lower_band", "WP2 lower-band temperatures"), ("wp2_n_T_transition_band", "WP2 transition-band temperatures"),
                       ("wp2_n_T_upper_band", "WP2 upper-band temperatures"), ("span_over_c", "tested span / fitted C"),
                       ("c_c", "fitted transition half-width C (°C; curve shape, not sampling)"),
                       # Added after the published results were visible (D-067 step 7), to show the mechanism behind unavailable T41J
                       # intervals; a pre-existing WP3 audit count (D-044), full-size curves only.
                       ("n_points_below_criterion", "measured energies below 41 J (WP3 audit count; full-size only)")]


def sampling_table(wp3: pd.DataFrame, data: dict, long: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for cid, d in data.items():
        w, fit = wp3.loc[cid], d["est"]["fit"]
        x = (d["t"] - fit["t0_c"]) / fit["c_c"]
        r = dict(data_type=DATA_TYPE, curve_id=cid, geometry_category=w["geometry_category"], outcome=w["outcome"], quality=QUALITY[w["outcome"]],
                 in_stricter=bool(w["in_stricter"]), wp2_sampling_class=w["wp2_sampling_class"], n_points=int(w["n_points"]),
                 n_temperatures=int(w["n_temperatures"]), T_span_c=w["T_span_c"], n_T_transition_fit=int(w["n_T_transition_fit"]),
                 n_points_transition_fit=int(np.sum(np.abs(x) < F.X_TRANSITION)), n_points_lower_shelf_fit=int(w["n_points_lower_shelf_fit"]),
                 n_points_upper_shelf_fit=int(w["n_points_upper_shelf_fit"]), wp2_n_T_lower_band=int(w["wp2_n_T_lower_band"]),
                 wp2_n_T_transition_band=int(w["wp2_n_T_transition_band"]), wp2_n_T_upper_band=int(w["wp2_n_T_upper_band"]),
                 span_over_c=w["T_span_c"] / w["c_c"], c_c=w["c_c"], use_support=w["use_support"],
                 flag_index_near_fitted_shelf=bool(w["flag_index_near_fitted_shelf"]),
                 n_points_below_criterion=w["n_points_below_criterion"])
        for method in METHODS:
            s = long[(long["curve_id"] == cid) & (long["method"] == method)].set_index("target")
            key = "t41j" if w["geometry_category"] == "full-size" else "t0"
            r.update({f"{method}_key_target": key, f"{method}_key_sd": s.loc[key, "sd"], f"{method}_key_width": s.loc[key, "interval_width"],
                      f"{method}_key_finite_fraction": s.loc[key, "finite_target_fraction"],
                      f"{method}_key_reportable": bool(s.loc[key, "interval_reportable"]),
                      f"{method}_use_relative_width": s.loc["use", "relative_interval_width"], f"{method}_use_relative_sd": s.loc["use", "relative_sd"],
                      f"{method}_use_reportable": bool(s.loc["use", "interval_reportable"])})
        rows.append(r)
    return pd.DataFrame(rows)


def spearman_table(samp: pd.DataFrame) -> pd.DataFrame:
    rows = []
    metrics = [("pairs_key_sd", "bootstrap SD of the key target", "pairs_key_reportable"),
               ("pairs_key_width", "95 % interval width of the key target", "pairs_key_reportable"),
               ("pairs_key_finite_fraction", "finite key-target fraction", None),
               ("pairs_use_relative_width", "USE 95 % width / USE", "pairs_use_reportable")]
    for cat, key in [("full-size", "T41J"), ("miniature", "T0")]:
        g = samp[samp["geometry_category"] == cat]
        for col, label, gate in metrics:
            h = g[g[gate]] if gate else g
            for prop, plabel in SAMPLING_PROPERTIES:
                x, y = h[prop].astype(float), h[col].astype(float)
                ok = x.notna() & y.notna()
                if ok.sum() >= 5 and x[ok].nunique() > 1 and y[ok].nunique() > 1:
                    rho, p = stats.spearmanr(x[ok], y[ok])
                else:
                    rho, p = np.nan, np.nan
                rows.append(dict(geometry_category=cat, key_target=key, metric=label, curves_in_analysis=int(ok.sum()),
                                 curve_scope="reportable pairs intervals only" if gate else "all curves", sampling_property=plabel,
                                 spearman_rho=rho, p_value_descriptive=p))
    return pd.DataFrame(rows)


BINS = [("n_points", [0, 8, 11, 14, 19, 1000], ["6-8", "9-11", "12-14", "15-19", "20+"]),
        ("n_temperatures", [0, 5, 8, 11, 1000], ["<=5", "6-8", "9-11", "12+"]),
        ("T_span_c", [0, 150, 250, 350, 10000], ["<=150", "150-250", "250-350", ">350"]),
        ("n_points_transition_fit", [-1, 2, 4, 6, 1000], ["0-2", "3-4", "5-6", "7+"]),
        ("n_points_upper_shelf_fit", [-1, 1, 3, 1000], ["0-1", "2-3", "4+"]),
        ("n_points_lower_shelf_fit", [-1, 1, 3, 1000], ["0-1", "2-3", "4+"]),
        ("n_points_below_criterion", [-1, 0, 1, 2, 4, 1000], ["0", "1", "2", "3-4", "5+"])]    # added after results (D-067 step 7)


def binned_table(samp: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for cat in ["full-size", "miniature"]:
        g = samp[samp["geometry_category"] == cat]
        for prop, edges, labels in BINS:
            b = pd.cut(g[prop], edges, labels=labels)
            for label in labels:
                h = g[b == label]
                if prop == "n_points_below_criterion" and cat != "full-size":
                    continue
                rep = h[h["pairs_key_reportable"]]
                rows.append(dict(geometry_category=cat, key_target="T41J" if cat == "full-size" else "T0", sampling_property=prop, bin=label,
                                 curves=len(h), curves_with_reportable_pairs_interval=len(rep),
                                 median_pairs_sd=rep["pairs_key_sd"].median() if len(rep) else np.nan,
                                 p25_pairs_sd=rep["pairs_key_sd"].quantile(0.25) if len(rep) else np.nan,
                                 p75_pairs_sd=rep["pairs_key_sd"].quantile(0.75) if len(rep) else np.nan,
                                 median_pairs_width=rep["pairs_key_width"].median() if len(rep) else np.nan,
                                 median_pairs_finite_fraction=h["pairs_key_finite_fraction"].median() if len(h) else np.nan,
                                 median_wild_sd=h.loc[h["wild_key_reportable"], "wild_key_sd"].median() if h["wild_key_reportable"].any() else np.nan,
                                 median_pairs_use_relative_width=h.loc[h["pairs_use_reportable"], "pairs_use_relative_width"].median()
                                 if h["pairs_use_reportable"].any() else np.nan))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 7. Published cross-check (D-063) and the pairs / fixed-design comparison (D-064)
# ---------------------------------------------------------------------------
def marini_amplitude_range(c: float) -> tuple:
    """Range of Marini's (2020) Eq. 6 amplitude a S^2 + b S + c for T41 over the test-matrix shifts he studied (Table 8)."""
    s = np.linspace(MARINI_T41["shift_min"], MARINI_T41["shift_max"], 2001)
    amp = MARINI_T41["a"] * s ** 2 + MARINI_T41["b"] * s + c
    return float(amp.min()), float(amp.max())


def miura_sigma_t41j(p: dict) -> float:
    """Miura, Shinko & Nomoto (2024 preprint) Eq. 13: SD of T41J by propagation of uncertainty, with the Charpy-curve parameters known."""
    lse, use, crit = p["lse"], p["use"], F.FULL_SIZE_CRITERION_J
    inner = (p["cv_lse"] ** 2 * lse ** 2 / (p["n_lse"] * (crit - lse) ** 2) + p["cv_use"] ** 2 * use ** 2 / (p["n_use"] * (use - crit) ** 2)
             + p["cv_cve"] ** 2 * crit ** 2 * (use - lse) ** 2 / (p["n_tt"] * (crit - lse) ** 2 * (use - crit) ** 2))
    return 0.5 * p["c"] * np.sqrt(inner)


def literature_table() -> pd.DataFrame:
    best, upper = marini_amplitude_range(MARINI_T41["c_best"]), marini_amplitude_range(MARINI_T41["c_upper"])
    n = MARINI_RCCM["n"]
    rows = [
        dict(source="Marini 2020, EPJ Nucl. Sci. Technol. 6:57, Tables 6-7", quantity="precision sigma of T41 (SD of T41 over 10,000 Monte Carlo data sets)",
             value=MARINI_RCCM["sigma"], unit="°C", specimens=n,
             test_matrix="RCC-M MC1222 matrix: 3 specimens at each of -60, -40, -20, 0, +20 °C (transition) and +100 °C (upper shelf)",
             basis="one 16MND5 forging; per-temperature bimodal Weibull scatter fitted to 142 tests; tanh with LSE = 0; fixed test matrix",
             comparable_with="bootstrap SD of T41J (one standard deviation)"),
        dict(source="Marini 2020, Table 7", quantity="accuracy (mean - reference) of T41", value=MARINI_RCCM["accuracy"], unit="°C", specimens=n,
             test_matrix="RCC-M matrix", basis="reference values from a 600-specimen simulated matrix", comparable_with="bootstrap bias (loosely)"),
        dict(source="Marini 2020, Table 7, Eq. 3", quantity="uncertainty u = sqrt(sigma^2 + accuracy^2) of T41", value=MARINI_RCCM["uncertainty"],
             unit="°C", specimens=n, test_matrix="RCC-M matrix", basis="as above", comparable_with="bootstrap SD (the accuracy term is negligible here)"),
        dict(source="Marini 2020, Table 7", quantity="precision sigma of USE", value=MARINI_RCCM["use_sigma"], unit="J", specimens=n,
             test_matrix="RCC-M matrix", basis="as above (USE 163.6 J, Table 2)", comparable_with="bootstrap SD of USE"),
        dict(source="Marini 2020, Tables 8 and 13, Eq. 6", quantity="T41 uncertainty amplitude a S^2 + b S + c (best estimate, c = 12.5), over the shifts studied",
             value=f"{best[0]:.2f} to {best[1]:.2f}", unit="°C × sqrt(specimens)", specimens="15-25 (A matrices), 10-100 (B, C)",
             test_matrix=f"shift S from {MARINI_T41['shift_min']} to {MARINI_T41['shift_max']}", basis="u = amplitude / sqrt(N), fitted to his simulations",
             comparable_with="bootstrap SD × sqrt(N)"),
        dict(source="Marini 2020, Table 13, Eq. 6", quantity="T41 uncertainty amplitude, upper bound (c = 16.0), over the shifts studied",
             value=f"{upper[0]:.2f} to {upper[1]:.2f}", unit="°C × sqrt(specimens)", specimens="as above", test_matrix="as above",
             basis="upper envelope of his simulations", comparable_with="bootstrap SD × sqrt(N)"),
        dict(source="Marini 2020, Tables 10 and 12", quantity="exponent beta of u = a N^-beta for T41 (B and C matrices)", value="0.51 (B); 0.53 (C)",
             unit="-", specimens="10-100", test_matrix="5 or 6 temperatures, i specimens each", basis="power-law fit to his simulations",
             comparable_with="slope of log(bootstrap SD) against log(N)"),
        dict(source="Miura, Shinko & Nomoto, SSRN preprint 4917170 (2024), Eq. 13, §4 standard parameters", quantity="SD of T41J by uncertainty propagation (our evaluation of Eq. 13)",
             value=round(miura_sigma_t41j(MIURA_STANDARD), 2), unit="°C",
             specimens=f"{MIURA_STANDARD['n_lse']} lower shelf + {MIURA_STANDARD['n_tt']} transition + {MIURA_STANDARD['n_use']} upper shelf",
             test_matrix="transition specimens at T41J; C and D assumed known", basis=f"LSE {MIURA_STANDARD['lse']:g} J, USE {MIURA_STANDARD['use']:g} J, C {MIURA_STANDARD['c']:g} °C, CV at 41 J {MIURA_STANDARD['cv_cve']:g}",
             comparable_with="order of magnitude and 1/sqrt(transition specimens) scaling only"),
        dict(source="Switzner et al. 2023, Metals 13:877, §3.2", quantity="USE 95 % quantile half-range (four-parameter algorithm)", value=8.0, unit="J",
             specimens=12, test_matrix="API-5L X52 pipe, 4.5 mm sub-size bars; EUS 46 J", basis="Monte Carlo of an assumed measurement error (0.6 J + 2.6 % of the value), 1,000 sets",
             comparable_with="not T41J; USE only loosely (different scatter source, geometry and steel)"),
    ]
    return pd.DataFrame(rows)


def crosscheck_table(t41: pd.DataFrame) -> pd.DataFrame:
    best, upper = marini_amplitude_range(MARINI_T41["c_best"]), marini_amplitude_range(MARINI_T41["c_upper"])
    rows = []
    usable = t41["outcome"] == F.OUTCOMES[5]
    for method in METHODS:
        rep = t41[f"{method}_interval_label"] == B.INTERVAL_PRIMARY
        subsets = [("C1: usable full-size fits with a primary T41J CI", usable & rep),
                   ("C2: C1 with 15-25 specimens (Marini's A matrices; RCC-M 18)", usable & rep & t41["n_points"].between(15, 25)),
                   ("C3: C1 in the stricter (E185-count) cohort", usable & rep & t41["in_stricter"].astype(bool))]
        for name, mask in subsets:
            h = t41[mask]
            amp = h[f"{method}_sd"] * np.sqrt(h["n_points"])
            r = dict(method=method, subset=name, curves=len(h), median_specimens=h["n_points"].median(),
                     median_bootstrap_sd_c=h[f"{method}_sd"].median(), p25_bootstrap_sd_c=h[f"{method}_sd"].quantile(0.25),
                     p75_bootstrap_sd_c=h[f"{method}_sd"].quantile(0.75), median_interval_width_c=h[f"{method}_interval_width"].median(),
                     median_sd_times_sqrt_n=amp.median(), p25_sd_times_sqrt_n=amp.quantile(0.25), p75_sd_times_sqrt_n=amp.quantile(0.75),
                     share_amplitude_below_marini_best_range=float((amp < best[0]).mean()) if len(h) else np.nan,
                     share_amplitude_within_marini_best_range=float(amp.between(best[0], best[1]).mean()) if len(h) else np.nan,
                     share_amplitude_above_marini_upper_bound_max=float((amp > upper[1]).mean()) if len(h) else np.nan,
                     marini_best_amplitude_range=f"{best[0]:.2f}-{best[1]:.2f}", marini_upper_bound_amplitude_max=round(upper[1], 2),
                     marini_rccm_sigma_c=MARINI_RCCM["sigma"], ratio_median_sd_to_marini_rccm_sigma=h[f"{method}_sd"].median() / MARINI_RCCM["sigma"])
            if len(h) >= 5 and h["n_points"].nunique() > 1:
                ts = stats.theilslopes(np.log(h[f"{method}_sd"]), np.log(h["n_points"]), alpha=0.95)
                r.update(theil_sen_slope_log_sd_vs_log_n=ts[0], slope_ci_low=ts[2], slope_ci_high=ts[3],
                         spearman_rho_sd_vs_n=stats.spearmanr(h["n_points"], h[f"{method}_sd"])[0])
            rows.append(r)
    return pd.DataFrame(rows)


def comparison_tables(long: pd.DataFrame, samp: pd.DataFrame, data: dict) -> tuple:
    rows = []
    for (cid, target), g in long.groupby(["curve_id", "target"]):
        p, w = g[g["method"] == B.PAIRS].iloc[0], g[g["method"] == B.WILD].iloc[0]
        both = bool(p["interval_reportable"] and w["interval_reportable"])
        lev = B.leverage_adjusted_residuals(data[cid]["t"], data[cid]["e"], data[cid]["est"]["fit"])
        rows.append(dict(data_type=DATA_TYPE, curve_id=cid, geometry_category=p["geometry_category"], target=target, outcome=p["outcome"],
                         original_estimate=p["original_estimate"], n_points=int(p["n_points"]), n_temperatures=int(p["n_temperatures"]),
                         both_reportable=both,
                         pairs_interval_label=p["interval_label"], wild_interval_label=w["interval_label"],
                         pairs_finite_fraction=p["finite_target_fraction"], wild_finite_fraction=w["finite_target_fraction"],
                         pairs_sd=p["sd"], wild_sd=w["sd"], pairs_width=p["interval_width"], wild_width=w["interval_width"],
                         ratio_sd_pairs_to_wild=p["sd"] / w["sd"] if w["sd"] > 0 else np.nan,
                         ratio_width_pairs_to_wild=p["interval_width"] / w["interval_width"] if w["interval_width"] > 0 else np.nan,
                         max_leverage=float(lev["leverage"].max()), points_with_leverage_numerically_one=lev["n_leverage_one"],
                         n_points_transition_fit=int(samp.set_index("curve_id").loc[cid, "n_points_transition_fit"])))
    per = pd.DataFrame(rows)
    summary, extremes = [], []
    for (cat, target), g in per.groupby(["geometry_category", "target"]):
        for scope, h in [("both methods reportable", g[g["both_reportable"]]),
                         ("both reportable and original WP3 fit usable", g[g["both_reportable"] & g["outcome"].isin(F.OUTCOMES[4:])])]:
            for col in ["ratio_sd_pairs_to_wild", "ratio_width_pairs_to_wild"]:
                v = h[col].dropna()
                summary.append(dict(geometry_category=cat, target=target, scope=scope, ratio=col, curves=len(v),
                                    median=v.median() if len(v) else np.nan, p10=v.quantile(0.1) if len(v) else np.nan,
                                    p90=v.quantile(0.9) if len(v) else np.nan, minimum=v.min() if len(v) else np.nan,
                                    maximum=v.max() if len(v) else np.nan, share_pairs_wider=float((v > 1).mean()) if len(v) else np.nan,
                                    curve_min=h.loc[v.idxmin(), "curve_id"] if len(v) else "", curve_max=h.loc[v.idxmax(), "curve_id"] if len(v) else ""))
        if target in ("t41j", "t0") and (target == "t41j") == (cat == "full-size"):
            h = g[g["both_reportable"]].sort_values("ratio_sd_pairs_to_wild")
            for label, part in [("pairs much narrower than fixed design (lowest ratios)", h.head(3)), ("pairs much wider (highest ratios)", h.tail(3))]:
                extremes.append(part.assign(extreme=label))
    return per, pd.DataFrame(summary), (pd.concat(extremes, ignore_index=True) if extremes else pd.DataFrame())


# ---------------------------------------------------------------------------
# 8. Figures (published data; grayscale-legible)
# ---------------------------------------------------------------------------
INK, INK2, MUTED, GRID = W3.INK, W3.INK2, W3.MUTED, W3.GRID
NAVY, BLUE, LIGHT, ORANGE = "#0d366b", W3.BLUE, "#86b6ef", W3.ORANGE
BAND = "#c9c8c2"


def select_worked_example(t41: pd.DataFrame) -> tuple:
    """D-065, declared before any published bootstrap result existed: among usable full-size fits with a calculated T41J whose notch
    dimensions are reported, that are empirically bracketed, carry no index-position warning, have 10-20 specimens and obtain a primary
    pairs T41J CI, the curve whose pairs bootstrap SD is closest to the median SD of that pool (ties: fewer specimens, then curve ID)."""
    pool = t41[(t41["outcome"] == F.OUTCOMES[5]) & ~t41["flag_full_size_notch_dimensions_unreported"].astype(bool)
               & t41["criterion_bracketed_by_measured_energy"].astype(bool) & ~t41["flag_index_near_fitted_shelf"].astype(bool)
               & t41["n_points"].between(10, 20) & (t41["pairs_interval_label"] == B.INTERVAL_PRIMARY)].copy()
    pool["distance"] = (pool["pairs_sd"] - pool["pairs_sd"].median()).abs()
    return pool.sort_values(["distance", "n_points", "curve_id"]).iloc[0]["curve_id"], len(pool), float(pool["pairs_sd"].median())


def _curve_panel(ax, d, w, reps_by_method, methods, t41_rows, title):
    import matplotlib.patches as mpatches
    t, e = d["t"], d["e"]
    grid_t = np.linspace(t.min(), t.max(), 300)
    W3._style(ax)
    handles = []
    shades = {B.PAIRS: (BAND, 0.85, "pairs bootstrap (primary): pointwise 95 % band of the fitted mean curve"),
              B.WILD: ("#8f8e88", 0.35, "fixed-design wild bootstrap (sensitivity): pointwise 95 % band")}
    for method in methods:
        lo, hi, used = B.mean_curve_band(reps_by_method[method], grid_t)
        color, alpha, label = shades[method]
        ax.fill_between(grid_t, lo, hi, color=color, alpha=alpha, lw=0, zorder=1)
        handles.append(mpatches.Patch(color=color, alpha=alpha, label=f"{label} ({used} of {len(reps_by_method[method]['outcome_code'])} replicates)"))
    fit = d["est"]["fit"]
    line, = ax.plot(grid_t, F.tanh_energy(grid_t, fit["lse_j"], fit["use_j"], fit["t0_c"], fit["c_c"]), color=INK, lw=1.8, zorder=3,
                    label="approved WP3 fit (full-size LSE fixed at 2.7 J)")
    pts = ax.scatter(t, e, s=30, facecolor=INK, edgecolor="white", linewidth=0.7, zorder=4, label="published test data")
    handles = [pts, line] + handles
    ax.axhline(F.FULL_SIZE_CRITERION_J, color=MUTED, lw=0.8, zorder=2)
    ax.text(grid_t[-1], F.FULL_SIZE_CRITERION_J, "41 J ", color=INK2, fontsize=7.5, va="bottom", ha="right")
    if np.isfinite(d["est"]["t41"]):
        row = t41_rows[methods[0]]
        y = F.FULL_SIZE_CRITERION_J
        reportable = bool(row["interval_reportable"])
        if np.isfinite(row["q025"]):
            # A non-reportable interval (finite T41J in < 95 % of replicates, D-057) is drawn grey and thin and named a conditional range.
            ax.errorbar([d["est"]["t41"]], [y], xerr=[[max(d["est"]["t41"] - row["q025"], 0.0)], [max(row["q975"] - d["est"]["t41"], 0.0)]],
                        fmt="none", ecolor=INK if reportable else MUTED, elinewidth=2.2 if reportable else 1.2, capsize=5, capthick=1.6, zorder=5)
        mk, = ax.plot([d["est"]["t41"]], [y], marker="D", ms=8, color=ORANGE, mec=INK, mew=1.0, ls="none", zorder=6,
                      label=(f"T41J with its {methods[0]} bootstrap 95 % interval" if reportable else
                             f"T41J with the conditional 2.5-97.5 % range of its finite {methods[0]} replicates (interval not reportable)"))
        handles.append(mk)
    ax.set_xlabel("Test temperature (°C)", fontsize=9, color=INK)
    ax.set_ylabel("Absorbed energy (J)", fontsize=9, color=INK)
    ax.set_title(title, fontsize=9, color=INK)
    return handles


def worked_example_figure(cid: str, d: dict, w: pd.Series, reps: dict, t41: pd.DataFrame, pool_size: int, pool_median: float) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    row = t41.set_index("curve_id").loc[cid]
    r = reps[(cid, B.PAIRS)]
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 5.4), gridspec_kw=dict(width_ratios=[1.55, 1]))
    s = {B.PAIRS: pd.Series({k.replace("pairs_", ""): row[k] for k in row.index if k.startswith("pairs_")})}
    handles = _curve_panel(axes[0], d, w, {B.PAIRS: r}, [B.PAIRS], s,
                           f"curve {cid}: {w['material_family']} {w['product_form']}, {'irradiated' if w['irradiated'] else 'unirradiated'}, "
                           f"full-size V-notch, {int(w['n_points'])} specimens")
    fig.legend(handles=handles, loc="upper center", ncol=2, fontsize=7.4, frameon=False, bbox_to_anchor=(0.5, 0.935))
    ax = axes[1]
    W3._style(ax)
    vals = r["t41j"][B.target_available(r, "t41j")]
    ax.hist(vals, bins=40, color=LIGHT, edgecolor="white", linewidth=0.6, zorder=2)
    for x, lab, ls in [(row["pairs_q025"], "2.5th percentile", "-"), (row["pairs_q975"], "97.5th percentile", "-")]:
        ax.axvline(x, color=INK, lw=1.2, ls=ls, zorder=3)
    ax.axvline(d["est"]["t41"], color=ORANGE, lw=2.0, ls="--", zorder=4)
    ax.set_xlabel("T41J of the bootstrap replicate fits (°C)", fontsize=9, color=INK)
    ax.set_ylabel("Replicates", fontsize=9, color=INK)
    ax.set_title(f"pairs bootstrap distribution of T41J (B = {len(r['outcome_code']):,})", fontsize=9, color=INK)
    lines = [f"T41J {d['est']['t41']:.1f} °C (approved WP3 fit, outcome: {w['outcome']})",
             f"pairs bootstrap (primary): 95 % CI {row['pairs_q025']:.1f} to {row['pairs_q975']:.1f} °C, SD {row['pairs_sd']:.1f} °C; "
             f"finite T41J in {100 * row['pairs_finite_target_fraction']:.1f} % of {len(r['outcome_code']):,} replicates; label: {row['pairs_interval_label']}",
             f"fixed-design wild bootstrap (sensitivity): 95 % interval {row['wild_q025']:.1f} to {row['wild_q975']:.1f} °C, SD {row['wild_sd']:.1f} °C",
             f"empirical bracketing: 41 J bracketed by the measured energies ({int(w['n_points_below_criterion'])} below, "
             f"{int(w['n_points_above_criterion'])} above); 41 J at {100 * w['index_fraction_of_rise']:.0f} % of the fitted rise (no index-position warning)",
             "vertical lines: orange dashed = WP3 estimate; black = 2.5th and 97.5th percentiles. The band is a confidence band for the fitted mean curve, "
             "not a prediction interval for a new specimen.",
             f"Selection (declared before results, D-065): SD closest to the median ({pool_median:.1f} °C) of {pool_size} eligible curves."]
    fig.text(0.01, 0.02, "\n".join(textwrap.fill(x, 150) for x in lines), fontsize=7.4, color=INK2, va="bottom")
    fig.suptitle("WP4 worked example: published Charpy V-notch data, approved tanh fit and bootstrap uncertainty of T41J (analysis of published test data)",
                 fontsize=10, color=INK)
    fig.tight_layout(rect=(0, 0.2, 1, 0.86))
    fig.savefig(OUT / "worked_example_t41j_bootstrap.png", dpi=150, metadata={"Software": None})
    plt.close(fig)


def diagnostic_figure(cid: str, d: dict, w: pd.Series, reps: dict, t41: pd.DataFrame, support: pd.DataFrame) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    row = t41.set_index("curve_id").loc[cid]
    sup = support.set_index("curve_id").loc[cid]
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 5.4), gridspec_kw=dict(width_ratios=[1.55, 1]))
    s = {m: pd.Series({k.replace(f"{m}_", ""): row[k] for k in row.index if k.startswith(f"{m}_")}) for m in METHODS}
    handles = _curve_panel(axes[0], d, w, {m: reps[(cid, m)] for m in METHODS}, METHODS, s,
                           f"DIAGNOSTIC: curve {cid} ({w['material_family']} {w['product_form']}, {int(w['n_points'])} specimens) - "
                           "41 J not bracketed by the measured energies")
    fig.legend(handles=handles, loc="upper center", ncol=2, fontsize=7.4, frameon=False, bbox_to_anchor=(0.5, 0.935))
    ax = axes[1]
    W3._style(ax)
    edges = np.histogram_bin_edges(np.concatenate([reps[(cid, m)]["t41j"][B.target_available(reps[(cid, m)], "t41j")] for m in METHODS]), bins=40)
    for m, color, lw in [(B.PAIRS, NAVY, 1.8), (B.WILD, MUTED, 1.4)]:
        v = reps[(cid, m)]["t41j"][B.target_available(reps[(cid, m)], "t41j")]
        ax.hist(v, bins=edges, histtype="step", color=color, lw=lw, ls="-" if m == B.PAIRS else "--",
                label=f"{m}: finite T41J in {100 * len(v) / len(reps[(cid, m)]['outcome_code']):.1f} % of replicates")
    ax.axvline(d["t"].min(), color=INK, lw=1.0)
    ax.text(d["t"].min(), ax.get_ylim()[1] * 0.97, " lowest test\n temperature", fontsize=7, color=INK2, va="top")
    ax.axvline(d["est"]["t41"], color=ORANGE, lw=2.0, ls=":")
    ax.set_xlabel("T41J of the bootstrap replicate fits (°C)", fontsize=9, color=INK)
    ax.set_ylabel("Replicates", fontsize=9, color=INK)
    ax.legend(fontsize=7.2, frameon=False, loc="upper right")
    lines = [f"T41J {d['est']['t41']:.1f} °C from a usable WP3 fit; all {int(w['n_points'])} measured energies lie above 41 J (lowest "
             f"{w['measured_energy_min_j']:.1f} J at {d['t'][np.argmin(d['e'])]:.1f} °C): the crossing is placed by the tanh shape and the fixed 2.7 J lower shelf.",
             f"pairs (primary): label '{row['pairs_interval_label']}'; conditional 95 % range {row['pairs_q025']:.1f} to {row['pairs_q975']:.1f} °C; "
             f"T41J unsupported below the resample's lowest temperature in {100 * sup['pairs_share_t41j_unsupported_below_lowest_temperature']:.1f} % of replicates; "
             f"replicate energies bracket 41 J in {100 * sup['pairs_share_replicate_energies_bracket_41j']:.1f} %.",
             f"fixed-design wild (sensitivity): label '{row['wild_interval_label']}'; 95 % range {row['wild_q025']:.1f} to {row['wild_q975']:.1f} °C; synthetic "
             f"energies bracket 41 J in {100 * sup['wild_share_replicate_energies_bracket_41j']:.1f} % of replicates, because reflecting the residual about "
             "the fitted curve can place an energy below 41 J that was never measured.",
             "Mathematical bootstrap variability, empirical support for the index and the original WP3 fit quality are separate questions (D-059)."]
    fig.text(0.01, 0.02, "\n".join(textwrap.fill(x, 150) for x in lines), fontsize=7.4, color=INK2, va="bottom")
    fig.suptitle(f"WP4 diagnostic: bootstrap T41J of curve {cid}, the one full-size curve whose measured energies do not bracket 41 J "
                 "(analysis of published test data)", fontsize=10, color=INK)
    fig.tight_layout(rect=(0, 0.2, 1, 0.86))
    fig.savefig(OUT / f"diagnostic_{cid}_bootstrap.png", dpi=150, metadata={"Software": None})
    plt.close(fig)


def sampling_figure(samp: pd.DataFrame) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fs = samp[samp["geometry_category"] == "full-size"]
    rep = fs[fs["pairs_key_reportable"]]
    styles = {"usable": dict(marker="o", facecolor=NAVY, edgecolor="white", s=30),
              "weakly identified": dict(marker="s", facecolor="white", edgecolor=NAVY, s=30),
              "boundary-limited": dict(marker="^", facecolor=MUTED, edgecolor=INK, s=40)}
    panels = [("n_points", "Specimens per curve, N (log scale)", True), ("n_temperatures", "Distinct test temperatures", False),
              ("n_points_transition_fit", "Specimens inside T0 ± C of the WP3 fit", False), ("T_span_c", "Tested temperature span (°C)", False)]
    fig, axes = plt.subplots(1, 4, figsize=(15, 4.6), sharey=True)
    best, upper = marini_amplitude_range(MARINI_T41["c_best"]), marini_amplitude_range(MARINI_T41["c_upper"])
    for ax, (col, label, logx) in zip(axes, panels):
        W3._style(ax)
        if col == "n_points":
            n = np.linspace(max(5, rep[col].min() * 0.9), rep[col].max() * 1.1, 200)
            ax.fill_between(n, best[0] / np.sqrt(n), best[1] / np.sqrt(n), color=BAND, alpha=0.7, lw=0, zorder=1,
                            label="Marini 2020 Eq. 6 best estimate over his matrix shifts")
            ax.plot(n, upper[1] / np.sqrt(n), color=INK2, lw=1.2, ls="--", zorder=1, label="Marini 2020 upper bound at his largest shift")
            ax.plot([MARINI_RCCM["n"]], [MARINI_RCCM["sigma"]], marker="*", ms=13, color=ORANGE, mec=INK, ls="none", zorder=5,
                    label="Marini 2020 RCC-M matrix: sigma(T41) 3.52 °C, N = 18")
        for quality, st in styles.items():
            h = rep[rep["quality"] == quality]
            if len(h):
                ax.scatter(h[col], h["pairs_key_sd"], zorder=3, linewidth=0.9,
                           label=f"WP3 outcome {quality} ({len(h)} curve{'s' if len(h) != 1 else ''})", **st)
        ax.set_yscale("log")
        if logx:
            ax.set_xscale("log")
        ax.set_xlabel(label, fontsize=8.5, color=INK)
    axes[0].set_ylabel("Pairs bootstrap SD of T41J (°C, log scale)", fontsize=8.5, color=INK)
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="upper center", ncol=3, fontsize=7.5, frameon=False, bbox_to_anchor=(0.5, 1.0))
    fig.suptitle(f"Full-size curves with a reportable pairs T41J interval ({len(rep)} of {len(fs)}); "
                 f"{len(fs) - len(rep)} curves without a reportable interval are not plotted (analysis of published test data)",
                 fontsize=9, color=INK, y=0.86)
    fig.tight_layout(rect=(0, 0, 1, 0.82))
    fig.savefig(OUT / "t41j_uncertainty_vs_sampling.png", dpi=150, metadata={"Software": None})
    plt.close(fig)


def residual_figure(res: pd.DataFrame) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.6), sharey=True)
    bins = np.arange(-4.0, 4.01, 0.5)
    for ax, cat in zip(axes, ["full-size", "miniature"]):
        W3._style(ax)
        h = res[res["wp3_fit_usable"] & (res["geometry_category"] == cat)]
        x, y = h["x_normalized_temperature"].clip(-4, 4), h["leverage_adjusted_residual_over_fitted_use"]
        ax.scatter(x, y, s=8, color=MUTED, alpha=0.45, lw=0, zorder=2, label="leverage-adjusted residuals")
        b = pd.cut(x, bins)
        g = pd.DataFrame({"b": b, "y": y}).groupby("b", observed=True)["y"]
        centers = np.array([iv.mid for iv in g.size().index])
        sd = g.std().to_numpy()
        mad = g.apply(lambda v: 1.4826 * np.median(np.abs(v - v.median()))).to_numpy()
        cnt = g.size().to_numpy()
        keep = cnt >= 10
        ax.plot(centers[keep], sd[keep], color=NAVY, lw=2, marker="o", ms=5, zorder=4, label="SD in 0.5-wide bins of x (>= 10 residuals)")
        ax.plot(centers[keep], mad[keep], color=INK, lw=1.4, ls="--", marker="s", ms=4, zorder=4, label="robust scale 1.4826 MAD, same bins")
        ax.axhline(0, color=INK2, lw=0.8, zorder=1)
        ax.axvspan(-1, 1, color=GRID, alpha=0.5, lw=0, zorder=0)
        ax.set_ylim(-0.45, 0.45)
        ax.set_xlabel("Normalized temperature x = (T - T0) / C of the WP3 fit (clipped to ±4)", fontsize=8.5, color=INK)
        ax.set_title(f"{cat}: {len(h)} residuals from {h['curve_id'].nunique()} usable WP3 fits", fontsize=9, color=INK)
    axes[0].set_ylabel("Residual / fitted USE (axis clipped to ±0.45)", fontsize=8.5, color=INK)
    hl, ll = axes[0].get_legend_handles_labels()
    fig.legend(hl, ll, loc="upper center", ncol=3, fontsize=7.5, frameon=False, bbox_to_anchor=(0.5, 1.0))
    fig.suptitle("Empirical published-data residual scatter about the approved WP3 fits (not a pure material-scatter distribution; shaded: T0 ± C)",
                 fontsize=9.5, color=INK, y=0.9)
    fig.tight_layout(rect=(0, 0, 1, 0.86))
    fig.savefig(OUT / "published_residual_scatter.png", dpi=150, metadata={"Software": None})
    plt.close(fig)


def comparison_figure(per: pd.DataFrame) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 3, figsize=(15, 5.0))
    for ax, (cat, target, label) in zip(axes, [("full-size", "t41j", "full-size T41J (°C)"), ("miniature", "t0", "miniature T0 (°C)"),
                                              ("all", "use", "USE / fitted USE")]):
        W3._style(ax)
        h = per[(per["target"] == target) & per["both_reportable"]]
        if cat != "all":
            h = h[h["geometry_category"] == cat]
        h = h.copy()
        if target == "use":   # SD of USE relative to the fitted USE, so that full-size and miniature curves share one axis
            h["wild_sd"], h["pairs_sd"] = h["wild_sd"] / h["original_estimate"], h["pairs_sd"] / h["original_estimate"]
        usable = h["outcome"].isin(F.OUTCOMES[4:])
        for mask, st, lab in [(usable, dict(marker="o", facecolor=NAVY, edgecolor="white", s=30), "original WP3 fit usable"),
                              (~usable, dict(marker="s", facecolor="white", edgecolor=NAVY, s=30), "weakly identified or boundary-limited")]:
            ax.scatter(h.loc[mask, "wild_sd"], h.loc[mask, "pairs_sd"], zorder=3, linewidth=0.9, label=f"{lab} ({int(mask.sum())})", **st)
        lim = [np.nanmin([h["wild_sd"].min(), h["pairs_sd"].min()]) * 0.8, np.nanmax([h["wild_sd"].max(), h["pairs_sd"].max()]) * 1.25]
        if np.all(np.isfinite(lim)) and lim[0] > 0:
            ax.plot(lim, lim, color=INK2, lw=1.0, zorder=2)
            ax.set_xscale("log")
            ax.set_yscale("log")
        ax.set_xlabel(f"fixed-design wild bootstrap SD: {label}", fontsize=8.3, color=INK)
        ax.set_ylabel(f"pairs bootstrap SD: {label}", fontsize=8.3, color=INK)
        ax.set_title(f"{label}\n{len(h)} curves with both intervals reportable" + (" (both geometries)" if cat == "all" else ""),
                     fontsize=8.8, color=INK)
        ax.legend(fontsize=7, frameon=False, loc="lower right")
    fig.suptitle("Pairs (primary) against fixed-design wild (sensitivity) bootstrap SD; line: equal SD (analysis of published test data)",
                 fontsize=9.5, color=INK)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(OUT / "pairs_vs_fixed_design_sd.png", dpi=150, metadata={"Software": None})
    plt.close(fig)


# ---------------------------------------------------------------------------
# 9. Method configuration and summary document
# ---------------------------------------------------------------------------
def method_configuration() -> str:
    L = ["# WP4 method configuration (generated from src/wp4_bootstrap.py, src/wp4_validation.py, src/wp4_uncertainty.py)", "",
         "| item | setting | decision |", "| --- | --- | --- |",
         f"| primary resampling | {B.METHOD_LABELS[B.PAIRS]}: each replicate draws N complete specimen records (temperature and energy together) with replacement and refits them; it also resamples which test temperatures are present | D-052 |",
         f"| fixed-design sensitivity | {B.METHOD_LABELS[B.WILD]}: tested temperatures kept; replicate energy = approved WP3 fit + r_i / (1 - h_i)^(1/2) × (±1, probability 1/2 each); h_i from the Jacobian of the free parameters at the WP3 solution; energies below 0 J set to 0 J and counted; 1 - h_i <= {B.LEVERAGE_ONE_TOLERANCE:g} → transformed residual 0 (counted) | D-053 |",
         f"| fit inside every replicate | exact approved WP3 functions (lse_setting, fit_curve, index_temperature, index_fraction_of_rise, classify, criterion_bracketing); full-size LSE fixed at {F.FIXED_LSE_CONVENTION_J['full-size']:g} J (never varied); miniature LSE fitted >= 0 J; the tested-range rule uses each replicate's own temperatures | D-054 |",
         f"| replicates | B = {B.B_REPLICATES} per curve and method (published curves); Monte Carlo stability rerun of a predeclared subset with B = {B.B_STABILITY} on an independent seed stream | D-055 |",
         f"| seeds | numpy SeedSequence([{B.WP4_SEED}, sha256(curve ID or synthetic data-set key), sha256(method name, with a suffix for the stability stream), replicate index]); results independent of worker count, chunking and order | D-055 |",
         f"| interval | 95 % percentile bootstrap interval [2.5th, 97.5th percentile] (NumPy linear interpolation) of the finite target values; also median, mean, SD, width, bias = mean - original, 16th/84th percentiles; BCa not used | D-056 |",
         "| targets | full-size: T41J (primary), USE, T0; C diagnostic. Miniature: T0 (primary), USE; LSE and C diagnostic; no miniature index criterion | D-056 |",
         "| target available | T41J: index status 'calculated' in that replicate; T0, C, USE, LSE: optimizer converged and fit not non-physical (inadmissible) | D-057 |",
         f"| reporting rule | interval reportable only if finite target values >= {100 * B.REPORTABLE_FINITE_FRACTION:g} % of the replicates REQUESTED (a project rule, not an ASTM requirement); conditional quantiles always stored | D-057 |",
         f"| labels | reportable + original WP3 fit usable: '{B.INTERVAL_PRIMARY}'; reportable + original boundary-limited or weakly identified: '{B.INTERVAL_DIAGNOSTIC}'; otherwise '{B.INTERVAL_UNAVAILABLE}'; the bootstrap never changes a WP3 outcome | D-058 |",
         "| T41J support in replicates | share of replicates whose energies bracket 41 J; among finite T41J: share not bracketed and share with the index-position warning; T41J unavailable by reason | D-059 |",
         "| SYNTHETIC validation | zero scatter, determinism, failure accounting, coverage (WP3 scenarios; 200 data sets × 500 replicates) | D-060 |",
         f"| residual scatter | WP3 point-fit residuals of all 2,588 records; normalized by fitted USE; leverage-adjusted (HC2) version; five x-regions; primary summary on usable WP3 fits; strata shown only as interpretable with >= {MIN_CURVES_STRATUM} curves and >= {MIN_RESIDUALS_STRATUM} residuals | D-061 |",
         "| sampling analysis | Spearman rank correlations and binned medians against pre-existing sampling properties | D-062 |",
         "| published cross-check | Marini 2020 (sigma(T41) 3.52 °C at N = 18; Eq. 6 amplitudes); Miura et al. preprint Eq. 13 (magnitude, scaling); Switzner et al. 2023 (not T41J) | D-063 |",
         "| method comparison | ratios of pairs to wild SD and width where both are reportable | D-064 |",
         "| worked example | selection rule declared before results; pointwise band of the fitted mean curve | D-065 |"]
    return "\n".join(L)


def _pct(x) -> str:
    return "" if pd.isna(x) else f"{100 * x:.1f} %"


def headline_lines(ctx: dict) -> list:
    """Headline numbers, each read from a table generated in this run (no number is typed in by hand)."""
    ca, t41, long = ctx["curve_accounting"], ctx["t41"], ctx["long"]
    L = []
    for method in METHODS:
        for cat, target, name in [("full-size", "t41j", "full-size T41J"), ("full-size", "use", "full-size USE"), ("miniature", "t0", "miniature T0"),
                                  ("miniature", "use", "miniature USE")]:
            r = ca[(ca["method"] == method) & (ca["geometry_category"] == cat) & (ca["target"] == target) & (ca["original_wp3_outcome"] == "ALL")].iloc[0]
            L.append(f"- {method}, {name}: {r['curves']} curves = {r['primary_bootstrap_ci']} primary bootstrap CIs + {r['diagnostic_bootstrap_interval']} "
                     f"diagnostic intervals + {r['interval_unavailable']} unavailable.")
    usable = t41["outcome"] == F.OUTCOMES[5]
    for method in METHODS:
        prim = t41[usable & (t41[f"{method}_interval_label"] == B.INTERVAL_PRIMARY)]
        if len(prim):
            L.append(f"- {method}, full-size T41J, usable fits with a primary CI ({len(prim)}): SD median {prim[f'{method}_sd'].median():.1f} °C "
                     f"(10th-90th percentile {prim[f'{method}_sd'].quantile(0.1):.1f}-{prim[f'{method}_sd'].quantile(0.9):.1f} °C); 95 % width median "
                     f"{prim[f'{method}_interval_width'].median():.1f} °C (10th-90th {prim[f'{method}_interval_width'].quantile(0.1):.1f}-"
                     f"{prim[f'{method}_interval_width'].quantile(0.9):.1f} °C).")
    for method in METHODS:
        m = long[(long["method"] == method) & (long["geometry_category"] == "miniature") & (long["target"] == "t0") & long["interval_reportable"]]
        u = long[(long["method"] == method) & (long["target"] == "use") & long["interval_reportable"]]
        if len(m):
            L.append(f"- {method}, miniature T0, reportable intervals ({len(m)}): SD median {m['sd'].median():.1f} °C, width median {m['interval_width'].median():.1f} °C.")
        for cat in ["full-size", "miniature"]:
            h = u[u["geometry_category"] == cat]
            if len(h):
                L.append(f"- {method}, {cat} USE, reportable intervals ({len(h)}): 95 % width / USE median {100 * h['relative_interval_width'].median():.1f} % "
                         f"(10th-90th {100 * h['relative_interval_width'].quantile(0.1):.1f}-{100 * h['relative_interval_width'].quantile(0.9):.1f} %).")
    x = ctx["crosscheck"]
    for _, r in x[x["method"] == B.PAIRS].iterrows():
        slope = (f"; Theil-Sen slope of log SD on log N {r['theil_sen_slope_log_sd_vs_log_n']:.2f} (95 % CI {r['slope_ci_low']:.2f} to {r['slope_ci_high']:.2f})"
                 if pd.notna(r.get("theil_sen_slope_log_sd_vs_log_n", np.nan)) else "")
        L.append(f"- cross-check, pairs, {r['subset']}: {r['curves']} curves, median N {r['median_specimens']:.0f}, median SD {r['median_bootstrap_sd_c']:.2f} °C "
                 f"(Marini RCC-M sigma 3.52 °C at N = 18); median SD × sqrt(N) {r['median_sd_times_sqrt_n']:.1f} against Marini's {r['marini_best_amplitude_range']} "
                 f"(best estimate) and <= {r['marini_upper_bound_amplitude_max']} (upper bound); below / within / above: "
                 f"{_pct(r['share_amplitude_below_marini_best_range'])} / {_pct(r['share_amplitude_within_marini_best_range'])} / "
                 f"{_pct(r['share_amplitude_above_marini_upper_bound_max'])}{slope}.")
    cs = ctx["comparison_summary"]
    for cat, target in [("full-size", "t41j"), ("miniature", "t0"), ("full-size", "use"), ("miniature", "use")]:
        r = cs[(cs["geometry_category"] == cat) & (cs["target"] == target) & (cs["scope"] == "both methods reportable") & (cs["ratio"] == "ratio_sd_pairs_to_wild")]
        if len(r) and r.iloc[0]["curves"]:
            r = r.iloc[0]
            L.append(f"- pairs / fixed-design SD, {cat} {target} ({r['curves']} curves): median {r['median']:.2f}, 10th-90th {r['p10']:.2f}-{r['p90']:.2f}, "
                     f"pairs wider for {_pct(r['share_pairs_wider'])}.")
    bn = ctx["binned"]
    below = bn[(bn["geometry_category"] == "full-size") & (bn["sampling_property"] == "n_points_below_criterion")]
    if len(below):
        L.append("- full-size T41J, pairs: curves with a reportable interval / curves, by measured energies below 41 J: "
                 + "; ".join(f"{r['bin']}: {r['curves_with_reportable_pairs_interval']} / {r['curves']}" for _, r in below.iterrows())
                 + " (unavailable intervals arise when replicates lose every specimen below 41 J and the crossing falls below their tested range).")
    so = ctx["stability_overall"]
    if len(so):
        L.append(f"- Monte Carlo stability (B = 4,000 independent rerun): largest change of a 2.5th/50th/97.5th percentile = "
                 f"{100 * so['max_share_of_width'].max():.1f} % of the B = 2,000 interval width (median over curves and targets "
                 f"{100 * so['median_share_of_width'].median():.1f} %); reportability changed for {int(so['reportable_status_changes'].sum())} curve-target rows.")
    rs = ctx["residual_summary"]
    h = rs[(rs["curve_set"] == "usable WP3 fits (primary summary)") & (rs["geometry_category"] == "full-size")
           & (rs["quantity"] == "leverage-adjusted residual / fitted USE")]
    if len(h):
        L.append("- empirical published-data residual scatter, full-size usable fits, leverage-adjusted residual / fitted USE, SD (robust scale) by region: "
                 + "; ".join(f"{r['region']} {r['sd']:.3f} ({r['mad_scaled']:.3f}, n = {r['residuals']})" for _, r in h.iterrows()) + ".")
    return L


def summary_markdown(ctx: dict) -> str:
    long, acc, t41 = ctx["long"], ctx["acc"], ctx["t41"]
    val = ctx["validation"]
    cov = val["coverage"]
    fmt_cov = cov.drop(columns=["data_type", "wp3_scenario"]).copy()
    for c in ["share_datasets_with_original_estimate", "share_datasets_interval_reportable", "coverage_of_reportable_intervals",
              "share_truth_below_interval", "share_truth_above_interval", "coverage_all_intervals_with_values"]:
        fmt_cov[c] = fmt_cov[c].map(_pct)
    curve_acc = ctx["curve_accounting"]
    dist = ctx["t41_distributions"]
    fail = ctx["failures"]
    L = ["# WP4 summary: per-curve bootstrap uncertainty (q4x6v-dyt25)", "",
         "Analysis of published Charpy V-notch test data (Materials Cloud 2025.30), CP2-frozen primary cohort (170 curves, 2,588 records), "
         "final approved WP3 fits (CP3). Files named `synthetic_*` are SYNTHETIC bootstrap checks; every other file concerns the published "
         "measurements. Decisions: DECISIONS.md D-052 to D-067. **Status: WP4 complete - internal review awaiting the author; WP5 not started.**", "",
         "## Headline numbers (each read from a table below)", "", *headline_lines(ctx), "",
         "## 1. Method", "", method_configuration().split("\n", 2)[2], "",
         "## 2. SYNTHETIC checks of the bootstrap implementation (not published data)", "",
         "Zero scatter (data exactly on the approved model):", "",
         md_table(val["zero"][["scale", "method", "replicates", "replicates_admissible", "share_key_target_within_tolerance",
                               "max_abs_key_target_deviation_c", "median_abs_key_target_deviation_c", "passed"]].round(6)), "",
         "Determinism:", "", md_table(val["determinism"][["method", "run", "per_replicate_arrays_identical", "summaries_identical", "passed"]]), "",
         "Failure accounting (difficult WP3 data sets; T41J rows):", "",
         md_table(val["failure"][val["failure"]["target"] == "t41j"][["data_set", "method", "replicates_requested", "finite_target_values",
                                                                       "target_unavailable", "finite_target_fraction", "interval_label", "passed"]].round(3)), "",
         "Coverage of 95 % percentile intervals (SYNTHETIC; 200 data sets per WP3 scenario, 500 replicates each):", "",
         md_table(fmt_cov[["scenario", "method", "target", "truth", "share_datasets_interval_reportable", "coverage_of_reportable_intervals",
                           "coverage_monte_carlo_se", "share_truth_below_interval", "share_truth_above_interval", "median_bootstrap_sd",
                           "empirical_sd_of_original_estimates", "ratio_median_bootstrap_sd_to_empirical_sd"]].round(3)), "",
         "## 3. Reproduction of the approved WP3 point fits and determinism on published curves", "",
         md_table(ctx["reproduction"].drop(columns=["data_type"]).T.reset_index().rename(columns={"index": "item", 0: "value"})), "",
         md_table(ctx["determinism_spot"].drop(columns=["data_type"])), "",
         "## 4. Curve accounting: which curves received which interval", "",
         md_table(curve_acc), "",
         "## 5. Full-size T41J uncertainty", "",
         md_table(dist.round(3)), "",
         "## 6. Miniature T0 and USE uncertainty (no miniature index criterion)", "",
         md_table(ctx["mini_distributions"].round(4)), "",
         "## 7. USE uncertainty (both geometries)", "",
         md_table(ctx["use_distributions"].round(4)), "",
         "## 8. T41J support diagnostics in the bootstrap replicates", "",
         md_table(ctx["support_summary"].round(4)), "",
         f"Curve {CURVE_33_153}:", "", md_table(ctx["support"][ctx["support"]["curve_id"] == CURVE_33_153].drop(columns=["data_type"]).T.reset_index()
                                                 .rename(columns={"index": "item"})), "",
         "## 9. Bootstrap failures and target availability (every replicate counted)", "",
         md_table(fail.round(4)), "",
         md_table(ctx["denominator_check"]), "",
         "## 10. Uncertainty against pre-existing sampling properties", "",
         "Spearman rank correlations (descriptive; association, not causation; properties are correlated with one another):", "",
         md_table(ctx["spearman"].round(3)), "", "Binned medians:", "", md_table(ctx["binned"].round(3)), "",
         "## 11. Published uncertainty cross-check", "", "Values read from the sources (DECISIONS.md, WP4 sources):", "",
         md_table(ctx["literature"]), "", "This project's full-size T41J bootstrap distributions, compared like with like:", "",
         md_table(ctx["crosscheck"].round(3)), "",
         "## 12. Pairs (primary) against fixed-design wild (sensitivity)", "", md_table(ctx["comparison_summary"].round(3)), "",
         "Largest disagreements (key targets):", "",
         md_table(ctx["comparison_extremes"][["extreme", "curve_id", "geometry_category", "target", "outcome", "n_points", "n_temperatures",
                                               "n_points_transition_fit", "pairs_sd", "wild_sd", "ratio_sd_pairs_to_wild", "max_leverage",
                                               "points_with_leverage_numerically_one"]].round(3)
                  if len(ctx["comparison_extremes"]) else pd.DataFrame()), "",
         "## 13. Monte Carlo stability (B = 2,000 against an independent B = 4,000 run)", "",
         md_table(ctx["stability"][["curve_id", "method", "target", "b2000_q025", "b4000_q025", "b2000_median", "b4000_median", "b2000_q975",
                                    "b4000_q975", "b2000_sd", "b4000_sd", "max_abs_endpoint_or_median_change_as_share_of_b2000_width",
                                    "reportable_status_changes"]].round(3)), "",
         md_table(ctx["stability_overall"].round(4)), "",
         "## 14. Empirical published-data residual scatter (not a pure material-scatter distribution)", "",
         md_table(ctx["residual_summary"][ctx["residual_summary"]["quantity"] != "residual (J)"].drop(columns=["data_type"]).round(4)), "",
         "Strata (full-size usable fits, leverage-adjusted residual / fitted USE):", "",
         md_table(ctx["residual_strata"].drop(columns=["data_type"]).round(4)), "",
         "## 15. Figures", "",
         f"- `worked_example_t41j_bootstrap.png`: curve {ctx['worked_example']} (selection rule D-065; {ctx['worked_pool']} eligible curves).",
         f"- `diagnostic_{CURVE_33_153}_bootstrap.png`: the one full-size T41J not bracketed by measured energies.",
         "- `t41j_uncertainty_vs_sampling.png`: pairs bootstrap SD of T41J against sampling properties, with Marini (2020) for reference.",
         "- `published_residual_scatter.png`: residual scatter against the normalized temperature.",
         "- `pairs_vs_fixed_design_sd.png`: the two methods compared.", ""]
    return "\n".join(L)


# ---------------------------------------------------------------------------
# 10. Driver
# ---------------------------------------------------------------------------
def main():
    OUT.mkdir(parents=True, exist_ok=True)
    t_start = time.perf_counter()
    primary, rec, wp3, data = load_primary()
    reproduction = reproduction_check(wp3, data)
    print(f"WP3 point fits reproduced for {len(data)} curves")
    code_fp = CK.code_fingerprint()
    print(f"WP4 published-data bootstrap: {WORKERS} worker processes; checkpoints in {CK.checkpoint_root()} (code fingerprint {code_fp[:12]})")
    reps = RunStore(data, code_fp, B.B_REPLICATES)
    computed, resumed = reps.ensure(list(data))
    print(f"Bootstraps: {computed} runs computed, {resumed} resumed, {B.B_REPLICATES} replicates each; {(time.perf_counter() - t_start) / 60:.1f} min")
    determinism_spot = determinism_spot_check(data, reps)
    longs, accs = zip(*[summarise_method(wp3, data, reps, m) for m in METHODS])
    long, acc = pd.concat(longs, ignore_index=True), pd.concat(accs, ignore_index=True)
    long[long["method"] == B.PAIRS].to_csv(OUT / "bootstrap_summary_pairs.csv", index=False)
    long[long["method"] == B.WILD].to_csv(OUT / "bootstrap_summary_fixed_design.csv", index=False)
    acc.to_csv(OUT / "bootstrap_replicate_accounting.csv", index=False)
    outcome_columns = [f"replicates_{o}" for o in F.OUTCOMES] + ["replicate_evaluation_errors"]
    denominator = (acc.groupby("method").agg(curves=("curve_id", "size"), replicates_requested=("replicates_requested", "sum"))
                   .join(acc.groupby("method")[outcome_columns].sum().sum(axis=1).rename("replicates_in_outcome_categories"))
                   .reset_index())
    denominator["all_replicates_accounted"] = denominator["replicates_requested"] == denominator["replicates_in_outcome_categories"]
    t41 = wide(long, "t41j", ["index_fraction_of_rise", "flag_index_near_fitted_shelf", "criterion_bracketed_by_measured_energy",
                              "n_points_below_criterion", "n_points_above_criterion", "flag_index_not_bracketed_by_measured_energy",
                              "notch_reported"], wp3)
    t41.to_csv(OUT / "t41j_uncertainty_full_size.csv", index=False)
    mini = pd.concat([wide(long[long["geometry_category"] == "miniature"], tg, ["use_support", "lse_support", "flag_lse_at_lower_bound"], wp3)
                      .assign(target=tg) for tg in ["t0", "use", "lse", "c"]], ignore_index=True)
    mini.to_csv(OUT / "miniature_t0_use_uncertainty.csv", index=False)
    use = wide(long, "use", ["use_support", "use_plateau_mean_j", "flag_weak_upper_shelf", "flag_nonflat_upper_shelf"], wp3)
    use.to_csv(OUT / "use_uncertainty_all_geometries.csv", index=False)
    support = support_table(wp3, acc, long)
    support.to_csv(OUT / "t41j_support_bootstrap.csv", index=False)
    availability = interval_availability(long)
    availability.to_csv(OUT / "interval_availability_by_outcome.csv", index=False)
    curve_acc = curve_accounting(long)
    curve_acc.to_csv(OUT / "interval_curve_accounting.csv", index=False)
    fail = failure_summary(acc)
    fail.to_csv(OUT / "bootstrap_failure_summary.csv", index=False)
    dist = t41j_group_distributions(t41)
    dist.to_csv(OUT / "t41j_uncertainty_distributions.csv", index=False)
    mini_rows, use_rows = [], []
    for method in METHODS:
        for tg in ["t0", "use", "lse", "c"]:
            h = long[(long["geometry_category"] == "miniature") & (long["method"] == method) & (long["target"] == tg)]
            for group, mask in [("all miniature curves", pd.Series(True, index=h.index)), ("original WP3 fit usable", h["outcome"].isin(F.OUTCOMES[4:])),
                                ("original boundary-limited", h["outcome"] == F.OUTCOMES[2]), ("original weakly identified", h["outcome"] == F.OUTCOMES[3])]:
                g = h[mask]
                col = "relative_interval_width" if tg == "use" else "interval_width"
                mini_rows.append(distribution_rows(g.loc[g["interval_reportable"], "sd"], method=method, target=tg, group=group,
                                                   quantity="bootstrap SD, reportable intervals", curves_in_group=len(g),
                                                   curves_reportable=int(g["interval_reportable"].sum())))
                mini_rows.append(distribution_rows(g.loc[g["interval_reportable"], col], method=method, target=tg, group=group,
                                                   quantity="95 % width" + (" / USE" if tg == "use" else " (°C)" if tg in ("t0", "c") else " (J)") + ", reportable intervals",
                                                   curves_in_group=len(g), curves_reportable=int(g["interval_reportable"].sum())))
                mini_rows.append(distribution_rows(g["finite_target_fraction"], method=method, target=tg, group=group, quantity="finite-target fraction",
                                                   curves_in_group=len(g), curves_reportable=int(g["interval_reportable"].sum())))
        for cat in ["full-size", "miniature"]:
            h = long[(long["geometry_category"] == cat) & (long["method"] == method) & (long["target"] == "use")]
            for group, mask in [("all", pd.Series(True, index=h.index)), ("original WP3 fit usable", h["outcome"].isin(F.OUTCOMES[4:])),
                                ("original not usable", ~h["outcome"].isin(F.OUTCOMES[4:]))]:
                g = h[mask]
                for q, col, gate in [("relative 95 % width (width / USE), reportable", "relative_interval_width", True),
                                     ("relative SD (SD / USE), reportable", "relative_sd", True), ("finite-target fraction", "finite_target_fraction", False)]:
                    vals = g.loc[g["interval_reportable"], col] if gate else g[col]
                    use_rows.append(distribution_rows(vals, method=method, geometry_category=cat, group=group, quantity=q, curves_in_group=len(g),
                                                      curves_reportable=int(g["interval_reportable"].sum())))
    mini_dist, use_dist = pd.DataFrame(mini_rows), pd.DataFrame(use_rows)
    mini_dist.to_csv(OUT / "miniature_uncertainty_distributions.csv", index=False)
    use_dist.to_csv(OUT / "use_uncertainty_distributions.csv", index=False)
    support_summary = []
    for method in METHODS:
        for group, mask in [("all full-size curves", pd.Series(True, index=support.index)),
                            ("original T41J bracketed", support["criterion_bracketed_by_measured_energy"]),
                            (f"original T41J not bracketed ({CURVE_33_153})", ~support["criterion_bracketed_by_measured_energy"]),
                            ("original index-position warning", support["flag_index_near_fitted_shelf"]),
                            ("no original index-position warning", ~support["flag_index_near_fitted_shelf"])]:
            h = support[mask]
            for col in [f"{method}_share_replicate_energies_bracket_41j", f"{method}_share_of_finite_t41j_not_bracketed",
                        f"{method}_share_of_finite_t41j_with_index_position_warning", f"{method}_share_t41j_unsupported_below_lowest_temperature",
                        f"{method}_t41j_finite_fraction"]:
                support_summary.append(distribution_rows(h[col], method=method, group=group, quantity=col.replace(f"{method}_", "")))
    support_summary = pd.DataFrame(support_summary)
    support_summary.to_csv(OUT / "t41j_support_bootstrap_summary.csv", index=False)

    # Monte Carlo stability (predeclared subset rule; D-055).
    sub = stability_subset(wp3, long[long["method"] == B.PAIRS])
    reps_4000 = RunStore(data, code_fp, B.B_STABILITY, STABILITY_SEED_SUFFIX)
    reps_4000.ensure(list(sub["curve_id"]))
    stability = stability_table(sub, wp3, data, reps, reps_4000)
    stability.to_csv(OUT / "bootstrap_mc_stability.csv", index=False)
    stability_overall = (stability.groupby(["method", "target"])
                         .agg(curve_target_rows=("curve_id", "size"),
                              median_share_of_width=("max_abs_endpoint_or_median_change_as_share_of_b2000_width", "median"),
                              max_share_of_width=("max_abs_endpoint_or_median_change_as_share_of_b2000_width", "max"),
                              max_abs_change_q025=("change_q025", lambda v: v.abs().max()), max_abs_change_q975=("change_q975", lambda v: v.abs().max()),
                              max_abs_change_sd=("change_sd", lambda v: v.abs().max()), reportable_status_changes=("reportable_status_changes", "sum"))
                         .reset_index())
    stability_overall.to_csv(OUT / "bootstrap_mc_stability_summary.csv", index=False)

    # Residual scatter, sampling analysis, cross-check, comparison.
    res = residual_dataset(wp3, data)
    res.to_csv(OUT / "published_residual_scatter_dataset.csv", index=False)
    residual_summary, residual_strata = residual_summaries(res)
    residual_summary.to_csv(OUT / "published_residual_scatter_summary.csv", index=False)
    residual_strata.to_csv(OUT / "published_residual_scatter_strata.csv", index=False)
    samp = sampling_table(wp3, data, long)
    samp.to_csv(OUT / "uncertainty_vs_sampling_by_curve.csv", index=False)
    spearman = spearman_table(samp)
    spearman.to_csv(OUT / "uncertainty_vs_sampling_spearman.csv", index=False)
    binned = binned_table(samp)
    binned.to_csv(OUT / "uncertainty_vs_sampling_binned.csv", index=False)
    literature = literature_table()
    literature.to_csv(OUT / "published_uncertainty_literature_values.csv", index=False)
    crosscheck = crosscheck_table(t41)
    crosscheck.to_csv(OUT / "published_uncertainty_crosscheck.csv", index=False)
    comparison_per, comparison_summary, comparison_extremes = comparison_tables(long, samp, data)
    comparison_per.to_csv(OUT / "pairs_vs_fixed_design_by_curve.csv", index=False)
    comparison_summary.to_csv(OUT / "pairs_vs_fixed_design_summary.csv", index=False)
    comparison_extremes.to_csv(OUT / "pairs_vs_fixed_design_extremes.csv", index=False)

    # Figures and the audit subset of replicates.
    worked, pool_size, pool_median = select_worked_example(t41)
    worked_example_figure(worked, data[worked], wp3.loc[worked], reps, t41, pool_size, pool_median)
    diagnostic_figure(CURVE_33_153, data[CURVE_33_153], wp3.loc[CURVE_33_153], reps, t41, support)
    sampling_figure(samp)
    residual_figure(res)
    comparison_figure(comparison_per)
    audit_ids = list(dict.fromkeys(list(sub["curve_id"]) + [worked, CURVE_33_153]))
    audit = []
    status_label = dict(enumerate(B.INDEX_STATUS_LABELS))
    outcome_label = {**{v: k for k, v in B.OUTCOME_CODES.items()}, B.EVALUATION_ERROR: "replicate evaluation error"}
    for cid in audit_ids:
        for method in METHODS:
            r = reps[(cid, method)]
            frame = pd.DataFrame({k: r[k] for k in ["replicate"] + B.REPLICATE_FIELDS})
            frame["outcome"] = frame.pop("outcome_code").map(outcome_label)
            frame["index_status"] = frame.pop("index_status_code").map(status_label)
            frame.insert(0, "method", method)
            frame.insert(0, "curve_id", cid)
            audit.append(frame)
    audit = pd.concat(audit, ignore_index=True)
    audit.insert(0, "data_type", DATA_TYPE)
    audit.to_csv(OUT / "bootstrap_replicates_audit_subset.csv.gz", index=False, float_format="%.6g", compression={"method": "gzip", "mtime": 0})

    validation = dict(zero=pd.read_csv(OUT / "synthetic_bootstrap_zero_scatter_check.csv"),
                      determinism=pd.read_csv(OUT / "synthetic_bootstrap_determinism_check.csv"),
                      failure=pd.read_csv(OUT / "synthetic_bootstrap_failure_accounting_check.csv"),
                      coverage=pd.read_csv(OUT / "synthetic_bootstrap_coverage_summary.csv"))
    write_text(OUT / "method_configuration.md", method_configuration())
    ctx = dict(long=long, acc=acc, t41=t41, validation=validation, curve_accounting=curve_acc, t41_distributions=dist, failures=fail,
               mini_distributions=mini_dist, use_distributions=use_dist, support=support, support_summary=support_summary,
               denominator_check=denominator, spearman=spearman, binned=binned, literature=literature, crosscheck=crosscheck,
               comparison_summary=comparison_summary, comparison_extremes=comparison_extremes, stability=stability,
               stability_overall=stability_overall, residual_summary=residual_summary, residual_strata=residual_strata,
               reproduction=reproduction, determinism_spot=determinism_spot, worked_example=worked, worked_pool=pool_size)
    write_text(OUT / "wp4_summary.md", summary_markdown(ctx))
    print(curve_acc.to_string(index=False))
    import resource
    print(f"peak RSS: main process {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024 ** 2:.0f} MB, largest worker "
          f"{resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1024 ** 2:.0f} MB")
    print(f"WP4 complete in {(time.perf_counter() - t_start) / 60:.1f} min -> {OUT}")


if __name__ == "__main__":
    main()
