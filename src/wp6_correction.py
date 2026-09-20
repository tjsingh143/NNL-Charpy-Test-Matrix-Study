"""WP6 - The size-correction scenarios: what displaces the simulated truth, at what level, and from what
distribution.

Everything here is read at full precision from the approved WP5 outputs at run time (DECISIONS.md D-083, D-099);
nothing is typed from prose. The residual is drawn ONCE PER SIMULATED PROGRAMME and shared by the whole test
matrix (D-098): WP5 measured disagreement between whole matched curves, not independent specimen noise, and a
specimen-level draw would make the correction exact as the specimen count rises. Specimen-level redrawing exists
only as the clearly labelled illustrative sensitivity.

Two distributional forms, and the rule that keeps them apart (D-099):

    parametric normal   Delta = bias + SD * z          (no truncation; an extreme draw simply produces a
                                                        programme that misses the transition, counted honestly)
    empirical family    Delta = sample(family values)  DIRECTLY - the pool already contains its own mean, so
                                                        adding a bias would count it twice

The sign convention is D-078's and is never reversed: DT_size = T41J(normalized smaller-specimen estimate)
minus T41J(matched full-size curve); positive means the correction places the transition warmer.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from common import OUTPUTS

WP5 = OUTPUTS / "wp5"
SIGN_CONVENTION = ("DT_size = T41J(normalized smaller-specimen estimate) - T41J(matched full-size curve); "
                   "positive = the correction places the transition warmer (D-078). Never reversed.")
EVIDENCE_CAVEAT = ("WEAKLY SUPPORTED pooled distribution (D-083): 7 independent matched families from 5 studies, "
                   "0 of 9 geometries DIRECTLY SUPPORTED. Not a geometry-specific law, not pure material "
                   "scatter, not an ASTM uncertainty. Contains WP4 fit noise and between-study variation; no "
                   "deconvolution is attempted (D-082).")
POOL_TOLERANCE = 1e-9


# ---------------------------------------------------------------------------
# 1. The approved values, read from the regenerated WP5 outputs
# ---------------------------------------------------------------------------
def central_scenario_values() -> dict:
    """The CENTRAL pooled family-weighted bias and SD (D-083 handoff, POOLED row)."""
    t = pd.read_csv(WP5 / "wp6_size_correction_handoff.csv", float_precision="round_trip")
    row = t[t["smaller_geometry"].str.startswith("POOLED")].iloc[0]
    return dict(bias_c=float(row["central_bias_c"]), sd_c=float(row["residual_scale_sd_c"]),
                robust_scale_c=float(row["residual_scale_robust_c"]), n_families=int(row["n_families"]),
                n_studies=int(row["n_studies"]), evidence_status=str(row["evidence_status"]))


def conservative_scenario_values() -> dict:
    """The CONSERVATIVE all-STRICT family-weighted bias and SD (D-083, required sensitivity)."""
    t = pd.read_csv(WP5 / "size_correction_summary_overall.csv", float_precision="round_trip")
    row = t[(t["subset"].str.startswith("all STRICT")) & (t["weighting"].str.startswith("family-weighted"))].iloc[0]
    return dict(bias_c=float(row["mean_c"]), sd_c=float(row["sd_c"]),
                robust_scale_c=float(row["robust_scale_1p4826_mad_c"]), n_families=int(row["n_families"]),
                n_studies=int(row["n_studies"]), evidence_status="all-STRICT matched set")


def normalization_scenario_values() -> pd.DataFrame:
    """Every pre-declared published normalization with ITS OWN (bias, SD) measured on the same comparisons.

    D-100 resolves the open D-089 this way: each method is a complete, self-consistent scenario. Nothing is
    added in quadrature and which method is 'true' is never randomly sampled. S2 (pure fracture area) is not a
    scenario and is returned marked so, for illustration only.
    """
    t = pd.read_csv(WP5 / "normalization_sensitivity_comparison.csv", float_precision="round_trip")
    t = t[["case", "label", "family_weighted_mean_c", "family_weighted_sd_c", "n_comparisons", "n_families"]].copy()
    t["is_scenario"] = ~t["case"].str.startswith("S2")
    t["scenario_note"] = np.where(t["is_scenario"], "complete scenario: its own bias and its own residual SD",
                                  "NOT a WP6 scenario (D-089): shown once as an illustration only")
    return t


# ---------------------------------------------------------------------------
# 2. The family-level pools, reconstructed and verified before use (D-099)
# ---------------------------------------------------------------------------
def family_pool(subset: str) -> dict:
    """The independent family-level DT_size values behind an approved summary.

    subset 'primary'   -> the 7 families of the PRIMARY analysis set (pooled handoff)
    subset 'all_strict'-> the 10 families of the all-STRICT set (conservative sensitivity)

    The pool is rebuilt from outputs/wp5/size_correction_residuals.csv and CHECKED against the approved
    family-weighted mean and SD; a mismatch beyond 1e-9 raises and stops the run.
    """
    t = pd.read_csv(WP5 / "size_correction_residuals.csv", float_precision="round_trip")
    t = t[t["delta_t_size_c"].notna()]
    if subset == "primary":
        t = t[t["in_primary_analysis_set"].astype(str).str.lower() == "true"]
        approved = central_scenario_values()
    elif subset == "all_strict":
        t = t[t["match_class"].str.startswith("STRICT")]
        approved = conservative_scenario_values()
    else:
        raise ValueError(f"unknown family pool {subset!r}")
    means = t.groupby("family_id")["delta_t_size_c"].mean().sort_index()
    values = means.to_numpy(float)
    got_mean, got_sd = float(values.mean()), float(values.std(ddof=1))
    if abs(got_mean - approved["bias_c"]) > POOL_TOLERANCE or abs(got_sd - approved["sd_c"]) > POOL_TOLERANCE:
        raise RuntimeError(
            f"reconstructed {subset} family pool does not reproduce the approved WP5 summary: "
            f"mean {got_mean!r} vs {approved['bias_c']!r}, SD {got_sd!r} vs {approved['sd_c']!r}")
    return dict(subset=subset, values=values, family_ids=list(means.index),
                mean_c=got_mean, sd_c=got_sd, n_families=len(values),
                n_comparisons=int(len(t)), n_studies=int(t["study_ref_id"].nunique()))


# ---------------------------------------------------------------------------
# 3. Scenario objects
# ---------------------------------------------------------------------------
class CorrectionScenario:
    """A complete size-correction scenario: how Delta is drawn for one simulated programme.

    kind 'none'      : Delta = 0 exactly (full-size programmes, and the zero-penalty validation case)
    kind 'normal'    : Delta = bias + SD * z, no truncation (D-099)
    kind 'empirical' : Delta = a family-level value drawn with replacement, DIRECTLY. The pool already carries
                       its own mean, so `bias_already_included` is True and the sampler refuses a separate bias.
    """

    def __init__(self, name: str, kind: str, bias_c: float = 0.0, sd_c: float = 0.0, pool=None,
                 label: str = "", per_specimen: bool = False, injection: str = "temperature"):
        if kind not in ("none", "normal", "empirical"):
            raise ValueError(f"unknown correction kind {kind!r}")
        if injection not in ("temperature", "energy_scale"):
            raise ValueError(f"unknown injection form {injection!r}")
        if kind == "empirical" and pool is None:
            raise ValueError("an empirical scenario needs its family-level pool")
        self.name = name
        self.kind = kind
        self.bias_c = float(bias_c)
        self.sd_c = float(sd_c)
        self.pool = None if pool is None else np.asarray(pool, float)
        self.label = label or name
        self.per_specimen = bool(per_specimen)   # D-098: True only for the labelled illustrative sensitivity
        self.injection = injection               # D-097: 'temperature' centrally; 'energy_scale' is the optional V20
        self.bias_already_included = kind == "empirical"

    def draw(self, rng, size=None, bias_c=None):
        """Draw Delta. Passing `bias_c` to an empirical scenario is refused, because the pool already contains
        its own mean and adding a bias would count it twice (D-099)."""
        if bias_c is not None:
            if self.bias_already_included:
                raise ValueError(
                    "refusing a separate bias for an empirical family scenario: the pool already contains its "
                    "own empirical mean, so bias + sampled_value would count the bias twice (D-099)")
            bias = float(bias_c)
        else:
            bias = self.bias_c
        if self.kind == "none":
            return np.zeros(() if size is None else size)
        if self.kind == "normal":
            return bias + self.sd_c * rng.standard_normal(() if size is None else size)
        return rng.choice(self.pool, size=size, replace=True)

    def describe(self) -> dict:
        return dict(scenario=self.name, kind=self.kind, label=self.label, bias_c=self.bias_c, sd_c=self.sd_c,
                    pool_size=0 if self.pool is None else int(self.pool.size),
                    bias_already_included=self.bias_already_included, per_specimen_draw=self.per_specimen,
                    injection=self.injection, sign_convention=SIGN_CONVENTION, evidence=EVIDENCE_CAVEAT)


def scenario_none() -> CorrectionScenario:
    return CorrectionScenario("NONE", "none", label="no size correction (full-size programme, or zero-penalty check)")


def scenario_central() -> CorrectionScenario:
    v = central_scenario_values()
    return CorrectionScenario("CENTRAL", "normal", v["bias_c"], v["sd_c"],
                              label=f"CENTRAL pooled family-weighted, WEAKLY SUPPORTED ({v['n_families']} families, "
                                    f"{v['n_studies']} studies)")


def scenario_conservative() -> CorrectionScenario:
    v = conservative_scenario_values()
    return CorrectionScenario("CONSERVATIVE", "normal", v["bias_c"], v["sd_c"],
                              label=f"CONSERVATIVE all-STRICT family-weighted ({v['n_families']} families) - "
                                    f"required by D-083")


def scenario_empirical(subset: str) -> CorrectionScenario:
    p = family_pool(subset)
    name = "EMPIRICAL-7" if subset == "primary" else "EMPIRICAL-10"
    return CorrectionScenario(name, "empirical", p["mean_c"], p["sd_c"], pool=p["values"],
                              label=f"empirical resampling of the {p['n_families']} family-level DT_size values "
                                    f"({subset}); no normality assumed, no bias added")


def scenario_fixed_sd(sd_c: float, bias_c: float) -> CorrectionScenario:
    return CorrectionScenario(f"SD={sd_c:g}", "normal", bias_c, sd_c,
                              label=f"correction-SD sweep point: bias {bias_c:.6f} deg C, SD {sd_c:g} deg C")


def scenario_normalization(case: str) -> CorrectionScenario:
    t = normalization_scenario_values()
    row = t[t["case"] == case].iloc[0]
    if not bool(row["is_scenario"]):
        raise ValueError(f"{case!r} is not a WP6 scenario (D-089); it is shown as an illustration only")
    return CorrectionScenario(f"NORM:{case}", "normal", float(row["family_weighted_mean_c"]),
                              float(row["family_weighted_sd_c"]),
                              label=f"normalization scenario {case}: {row['label']}")


def scenario_specimen_level() -> CorrectionScenario:
    """The clearly labelled ILLUSTRATIVE sensitivity of D-098. Never a central or headline case."""
    v = central_scenario_values()
    return CorrectionScenario("SPECIMEN-LEVEL", "normal", v["bias_c"], v["sd_c"], per_specimen=True,
                              label="ILLUSTRATIVE ONLY (D-098): the correction residual redrawn independently per "
                                    "specimen, which makes the penalty average away as 1/sqrt(N). Not a central case.")


def scenario_energy_scale() -> CorrectionScenario:
    """OPTIONAL sensitivity (D-097, T4 variant V20): the same calibrated discrepancy injected as an ENERGY-SCALE
    error instead of a temperature displacement.

    The magnitude is matched exactly, not added to: for a programme whose drawn Delta is d, the simulator uses
    the energy factor f = 41 J / E_true(T41J_true + d), which is precisely the factor that moves the 41 J
    crossing of the true curve by d. Nothing is double-counted; only the FORM of the discrepancy changes.
    """
    v = central_scenario_values()
    return CorrectionScenario("ENERGY-SCALE", "normal", v["bias_c"], v["sd_c"], injection="energy_scale",
                              label="OPTIONAL (D-097): the same calibrated discrepancy injected as an energy-scale "
                                    "error, magnitude-matched to the temperature form, not added to it")
