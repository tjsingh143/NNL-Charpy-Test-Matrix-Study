# PROJECT BRIEF: Charpy Transition Temperature Uncertainty and Test Matrix Study

**Read this whole file before writing any code.**

This is a requirements document, not an implementation guide. It specifies *what* must be
produced and *what questions must be answered*. All implementation choices (libraries,
structure, algorithms, fitting strategy) are yours to make and to justify. Where this brief
names a method, treat it as the accepted approach in the field, not as an instruction to
avoid thinking about it. If you believe a different approach is better, say so and explain
why before proceeding.

---

## 1. Who this is for and why it exists

The author is a first-year Materials Science and Engineering student at UC Irvine applying
to the Naval Nuclear Laboratory's Materials Engineering Internship at Bettis Atomic Power
Laboratory. The posting's first two responsibilities are:

1. "design, coordination, & documentation of material test programs"
2. "analysis and modeling of test program data"

and its stated areas of interest include mechanical properties, forging, and specifications
of core and plant components.

This project exists to produce genuine evidence of competency in those two areas, on real
reactor pressure vessel materials data. **It will be read by professional materials
engineers who do this work for a living.** Credibility matters more than sophistication. A
modest, correct, honestly-caveated result beats an ambitious one with hidden assumptions.

### 1.1 The author must be able to defend every part of this

This is a hard requirement, not a preference. The author will be questioned on this work in
technical interviews. Therefore:

- **Do not make silent judgment calls.** Every choice that could reasonably have gone
  another way gets written down, with reasoning, in `DECISIONS.md`.
- **Stop at the checkpoints in Section 9.** At each one, explain your reasoning in plain
  language, present what you found, and wait. Do not proceed past a checkpoint on your own.
- **No black boxes.** If a step cannot be explained to someone with one year of college
  physics and math, either explain it better or choose a simpler approach.
- Prefer a transparent method the author can defend over an opaque method that scores better.

---

## 2. The research question

> A reactor pressure vessel surveillance capsule contains a fixed, small volume of irradiated
> material. That volume can be spent on a few full-size Charpy specimens or on many
> miniature ones. **Which choice yields a better-determined ductile-to-brittle transition
> temperature, once both curve-fitting uncertainty and sub-size-to-full-size correction
> uncertainty are accounted for?**

Supporting questions that must also be answered:

- **Q1.** For a given transition curve, how well-determined is the index temperature, and
  what property of the sampling drives that (number of specimens, temperature span, how many
  points land in the transition rather than on the shelves)?
- **Q2.** How does index-temperature uncertainty depend on specimen count and on where the
  test temperatures are placed?
- **Q3.** How much additional uncertainty does the sub-size to full-size correction introduce,
  and does it differ by product form (plate, forging, weld)?
- **Q4.** Under what conditions does the answer to the main question flip?

### 2.1 Relationship to published work

There is a 2026 paper in *Scientific Reports* ("Machine Learning-based Correlation of Charpy
Impact Properties Between Sub-sized and Standard-sized Specimens for Nuclear Structural
Materials", arXiv 2607.10412) that uses machine learning to **predict** standard-size
properties from sub-size ones.

**This project is not that, and must not become that.** That is a prediction problem. This is
a test-program *design* problem: given the uncertainty stack, which test matrix should you
choose. Read that paper, cite it, and state explicitly in the report how this work differs.
If at any point the project starts drifting toward "train a model to predict full-size
properties," stop and flag it.

---

## 3. Data

**Source:** Materials Cloud Archive, record `eny5v-www93`
https://archive.materialscloud.org/records/eny5v-www93

**File:** `Charpy_Impact_Test_Dataset.xlsx`, approximately 760 KB
**License:** CC-BY-4.0. Redistribution is permitted with attribution. Attribution is mandatory
and must appear in the README, the report, and the data directory.

**Data descriptor paper (cite this):** "Comprehensive Toughness Dataset of Nuclear Reactor
Structural Materials using Charpy V-Notch Impact Testing", *Scientific Data*, 2025.
https://www.nature.com/articles/s41597-025-04823-1

**What it contains** (per the descriptor, verify against the actual file):
- ~4,775 records, 55 parameters, compiled from 109 peer-reviewed publications
- Materials: SA533B / A533B (RPV plate), SA508 (pressure vessel forgings), 20MnMoNi55,
  A302B, SS316
- Base metal and weld joints; product forms include plate, forging, and weld
- Irradiated and unirradiated conditions, with fluence where applicable
- Specimen geometries: full-size, sub-size, and miniature
- Per-record fields include test temperature, absorbed energy, lateral expansion, shear
  fracture appearance percentage, composition, manufacturing history, heat treatment, and
  specimen dimensions

**The dataset is compiled from 109 different studies.** This is the single most important
fact about it. Different laboratories, machines, calibration practices, and reporting
conventions are mixed together. Between-study variability is baked into any scatter estimate
derived from it and cannot be cleanly separated from real material scatter. This must be
stated in the report's limitations and must not be quietly ignored in the analysis.

---

## 4. Scope

### In scope
- Ferritic RPV steels and their welds (the SA533B / A533B / SA508 / 20MnMoNi55 / A302B family)
- Absorbed energy versus temperature transition behavior
- Index temperature and upper shelf energy as the extracted properties
- Statistical uncertainty in those extracted properties
- The specimen size effect as it bears on the above

### Out of scope
- SS316 (austenitic, no ductile-to-brittle transition in the same sense). Exclude it, and say
  in the report why.
- Fracture mechanics (K, J, master curve, RT_NDT determination per ASME). The report may
  reference why the index temperature matters, but must not attempt fracture toughness work.
- Predicting embrittlement from composition and fluence (ASTM E900 territory). Interesting,
  different project.
- Any machine learning model. See 2.1.

---

## 5. Work packages

Each work package lists what must be produced and how it will be judged. Order matters;
later packages depend on earlier ones.

### WP0 — Acquisition and data dictionary

**Produce:**
- The dataset vendored into the repo with a recorded checksum, plus attribution and license
  files alongside it
- A **data dictionary** covering every column: name, meaning, units, fill rate, value range
  for numerics, full set of distinct values for categoricals

**Judged by:** someone who has never opened the file can read the data dictionary and know
what is in it, including which fields are sparse enough to be unusable.

**Flag anything surprising.** If a column's meaning is not obvious from its name and the
descriptor paper, say so rather than guessing.

### WP1 — Cleaning and normalization

**Produce:**
- Unit harmonization across temperature, energy, fluence, and specimen dimensions. Records
  compiled from 109 papers will not share units.
- Naming harmonization for materials and product forms (expect variants like A533B, SA533B,
  SA-533 Gr. B Cl. 1 referring to the same thing). Do not merge things you are not confident
  are the same; when unsure, keep them separate and flag it.
- Detection and explicit handling of: missing values, duplicate records, and physically
  impossible values (negative energy, energy far above any plausible upper shelf, test
  temperatures outside any plausible range)
- A **reconciliation table**: starting record count, count removed at each step with the
  reason, ending count. The arithmetic must close.

**Judged by:** nothing is silently dropped or silently altered. Every record that leaves the
dataset leaves for a stated reason.

### WP2 — Curve grouping and inclusion criteria

A "transition curve" is a set of records that can legitimately be fitted together.

**Produce:**
- A definition of what makes one curve. At minimum this involves material, product form,
  heat or lot identifier where available, irradiation condition, and specimen geometry.
  Decide how to treat fluence: exact match, or binned. Justify.
- A **curve inventory**: how many curves the grouping yields, points per curve, temperature
  span per curve, and whether the points actually bracket the transition or sit only on the
  shelves.
- **Inclusion criteria** for which curves are fittable. This is a judgment call with real
  consequences. State the rule, justify it, and run a **sensitivity check** showing how the
  headline results change if the rule is loosened and tightened.

**Judged by:** the inclusion rule is defensible to someone who wants to argue with it, and its
influence on the conclusions is quantified rather than assumed away.

### WP3 — Transition curve fitting

The accepted empirical model is the hyperbolic tangent form, in which absorbed energy varies
between a lower shelf and an upper shelf through a mid-transition temperature with a
characteristic transition width. The index temperature is the temperature at which the fitted
curve crosses a criterion energy (41 J is the standard criterion for full-size RPV steel
specimens; the criterion for sub-size geometries is not simply the same number, and you must
determine and justify the convention you use from the references in Section 11).

**Produce:**
- A fitter that extracts upper shelf energy, mid-transition temperature, transition width,
  and index temperature per curve
- A documented decision on whether the lower shelf is fixed or fitted, with reasoning
- **Fitter validation before any real data is trusted:** demonstrate that the fitter recovers
  known parameters from synthetic curves with known truth, across a range of sampling
  densities and noise levels. Report where it stops working.
- Explicit accounting of fit failures: how many curves failed to converge or produced
  non-physical parameters, and the pattern in those failures

**Judged by:** the validation is convincing, and failures are reported rather than dropped.

**Note:** this fit is known to be ill-conditioned when few points fall in the transition
region. That is not a bug to be worked around; it is the phenomenon the whole project is
about. Characterize it.

### WP4 — Per-curve uncertainty

**Produce:**
- A confidence interval on the index temperature and on upper shelf energy for each fitted
  curve, obtained by resampling
- An analysis relating that uncertainty to the sampling properties: point count, temperature
  span, and the number of points falling inside the transition region rather than on a shelf
- A **cross-check against published uncertainty estimates** for RPV steel transition
  temperatures (see Section 11). Report agreement or disagreement honestly. If your intervals
  are much tighter than the literature's, that is evidence of a problem in your method, not a
  triumph.

**Judged by:** the magnitudes are sane relative to published values, and the discrepancies are
discussed rather than buried.

### WP5 — Specimen size effect

**Produce:**
- Identification of material and condition pairs measured at more than one specimen geometry
- Application of the classical normalization approach, in which absorbed energy is scaled by
  a measure of the specimen ligament volume and a temperature normalization is applied, to
  test whether curves at different geometries collapse onto one another
- **Quantification of the residual disagreement in index temperature after normalization**,
  broken out by product form. This residual is the size-correction uncertainty and it is a
  required input to WP6.
- Explicit statement of why a volume ratio cannot fully correct the size effect: a thinner
  specimen has less through-thickness constraint, so the stress triaxiality at the notch root
  differs, and no scalar volume scaling captures that.

**Judged by:** the size-correction uncertainty is a real number with a stated basis, and its
limitations are named.

**If there are too few paired records to do this well, say so immediately rather than
producing a weak number.** That finding would itself change the shape of WP6 and the report.

### WP6 — Monte Carlo test matrix study (the headline)

**Produce:**
- A simulator that, given a true transition curve and a scatter model calibrated from WP4,
  draws a specified number of specimens at specified test temperatures, refits, and records
  the error in the recovered index temperature
- Sweeps over: **specimen count**, **test-temperature placement strategy** (at minimum:
  uniform across a wide span, clustered near the expected transition, and an adaptive or
  staircase approach that places later specimens based on earlier results), and **specimen
  geometry**
- The **fixed-material-volume comparison**: given a material volume budget, compute how many
  specimens of each geometry fit, and the resulting index-temperature uncertainty, with the
  WP5 size-correction penalty applied to the sub-size cases
- A clear statement of **where the answer flips** and what it depends on. The prior
  expectation is that it depends heavily on how well the transition location is known before
  testing begins, but do not assume this; determine it.

**Judged by:** the main research question in Section 2 gets a direct, quantitative answer with
its conditions attached.

**The scatter model is the weak link and must be treated as such.** State exactly where it
came from, test how sensitive the conclusions are to it, and report that sensitivity.

### WP7 — Report and repository

See Sections 6 and 7.

---

## 6. Deliverables

### 6.1 Technical report

A PDF of roughly 10 to 15 pages, structured as an engineering analysis report, not a lab
writeup or a blog post. Required sections:

1. Objective and scope
2. Data source, provenance, and license
3. Data cleaning and inclusion criteria, with the reconciliation table
4. Methods
5. Fitter validation
6. Results
7. **Uncertainty and limitations**
8. Conclusions
9. References

**Section 7 is the most important section in the document** and should be written with more
care than any other. At minimum it must address:

- Between-study heterogeneity: 109 source publications, different machines, calibrations, and
  reporting conventions, and the resulting inability to separate that variance from material
  scatter
- That Charpy absorbed energy is an empirical index, not a fracture-mechanics material
  property, and that the index temperature is a correlation parameter
- That the hyperbolic tangent model is empirical with no physical derivation
- That ligament-volume normalization does not capture constraint and triaxiality differences
  between geometries
- Sensitivity of the conclusions to the WP2 inclusion criteria and the WP6 scatter model
- Anything the analysis could not determine

Every numeric claim in the report must be traceable to code in the repository. No number
appears in the report that the repository cannot regenerate.

### 6.2 Required figures

Four figures carry the report. Each must be regenerable from the repo.

1. **A worked example**: one fitted transition curve with its data points, the fit, the
   resampling confidence band, and the index temperature marked
2. **Index-temperature uncertainty versus specimen count**, with a separate series per
   test-temperature placement strategy
3. **The size normalization**: curves before and after normalization, faceted by product form,
   with the residual disagreement quantified on the figure
4. **The fixed-volume comparison**: index-temperature uncertainty for full-size versus
   sub-size versus miniature at equal material volume, showing the crossover if one exists

Figures must be legible in grayscale and readable at print size. Axis labels carry units.

### 6.3 Repository

- Source for the full pipeline
- The vendored dataset with checksum, license, and attribution
- Generated figures
- The report and its source
- `DECISIONS.md`
- `README.md` with the research question, the data attribution and citation, how to reproduce
  every figure, and a plain-language summary of the finding

**One command regenerates every figure and every number in the report from the raw dataset.**
If that is not true, the project is not finished.

### 6.4 DECISIONS.md

A running log. One entry per judgment call, each stating: what was decided, what the
alternatives were, why this one, and what would change if the other had been chosen.

Non-exhaustive list of decisions that must appear:
- Whether the lower shelf is fixed or fitted, and at what value
- The criterion energy used for each specimen geometry, and its basis
- How fluence is treated in curve grouping (exact or binned, and bin edges)
- Which material name variants were merged and which were kept separate
- The curve inclusion rule and its thresholds
- The resampling scheme
- The scatter model for WP6 and its calibration
- The ligament-volume normalization convention adopted, and from which reference
- Every record exclusion category

---

## 7. Honesty constraints

These are absolute.

- **Never state or imply that the author performed Charpy tests, operated test equipment, or
  handled irradiated material.** The report and README must describe this as analysis of
  published test data. Use that phrasing.
- **No fabricated, imputed, or filled-in measurement data.** If a field is missing, it is
  missing and the record is excluded or handled explicitly. Synthetic data is permitted only
  for fitter validation (WP3) and the Monte Carlo (WP6), and both must be labelled as
  synthetic everywhere they appear.
- **Report negative and null results.** If the normalization does not collapse the curves, if
  the size effect cannot be resolved, if miniature specimens turn out to be strictly worse,
  those are the findings. Write them.
- **Do not tune the analysis toward a more interesting conclusion.** If you find yourself
  adjusting inclusion criteria or the scatter model after seeing how it moves the headline,
  stop and log it in `DECISIONS.md` as exactly that.
- Cite every external method, convention, and number that did not come from the dataset.

---

## 8. Non-goals

- Do not build a web app, dashboard, or interactive visualization.
- Do not build a general-purpose materials data library.
- Do not train a machine learning model.
- Do not optimize for lines of code, file count, or apparent sophistication. A short, clear
  pipeline is the goal.

---

## 9. Checkpoints

**Stop at each of these. Present what you found, explain the reasoning in plain language,
answer questions, and wait for explicit approval before continuing.**

- **CP1, after WP1.** Present the data dictionary and the cleaning reconciliation table. Walk
  through what the dataset actually contains, what had to be harmonized, and what was
  excluded and why.
- **CP2, after WP2.** Present the curve inventory and the proposed inclusion rule. Explain
  what the rule costs in curves and what it buys in fit quality.
- **CP3, after WP3.** Present the fitter validation. Explain where the fit breaks down and
  why, in physical and statistical terms.
- **CP4, after WP5.** Present the size-correction result. Explain what the normalization is
  trying to do and why it is imperfect.
- **CP5, after WP6, before writing the report.** Present the headline answer and its
  conditions. Explain the scatter model and how much the conclusion depends on it.

At each checkpoint, if the author cannot restate the reasoning back in their own words, that
is a signal to slow down and explain differently, not to move on.

---

## 10. Definition of done

- [ ] Every figure and every number in the report regenerates from raw data with one command
- [ ] The main research question has a direct, quantitative, conditioned answer
- [ ] Q1 through Q4 are each answered
- [ ] Fitter validation demonstrates the method recovers known truth, and names where it fails
- [ ] Per-curve uncertainties are cross-checked against published values
- [ ] The limitations section addresses every item in 6.1
- [ ] `DECISIONS.md` covers every item in 6.4
- [ ] Attribution and license for the dataset appear in the README, the report, and the data
      directory
- [ ] The relationship to the 2026 sub-size ML paper is stated explicitly
- [ ] Nothing in the repository implies the author ran physical tests
- [ ] All five checkpoints were reached, presented, and approved

---

## 11. Reference reading

The author should read these; the agent should use them to pin conventions rather than
inventing them.

**Dataset**
- Comprehensive Toughness Dataset of Nuclear Reactor Structural Materials using Charpy V-Notch
  Impact Testing, *Scientific Data* (2025). https://www.nature.com/articles/s41597-025-04823-1
- Dataset record: https://archive.materialscloud.org/records/eny5v-www93

**Method and uncertainty**
- Algorithms to Estimate the Ductile to Brittle Transition Temperature, Upper Shelf Energy,
  and Their Uncertainties for Steel Using Charpy V-Notch Shear Area and Absorbed Energy Data,
  *Metals* 13(5):877. https://www.mdpi.com/2075-4701/13/5/877
- Empirical estimation of uncertainties of Charpy impact testing transition temperatures for
  an RPV steel, *EPJ Nuclear Sciences & Technologies*.
  https://www.epj-n.org/articles/epjn/full_html/2020/01/epjn200012/epjn200012.html
- Variation of ductile-brittle transition temperature for Charpy curve provided by hyperbolic
  tangent function. https://www.sciencedirect.com/science/article/abs/pii/S0308016125000651
- Evaluation of Charpy-V transition curve fitting based on distribution-free statistical
  assessment. https://www.sciencedirect.com/science/article/abs/pii/S0308016123001965

**Specimen size effect and the work this project must differentiate itself from**
- Machine Learning-based Correlation of Charpy Impact Properties Between Sub-sized and
  Standard-sized Specimens for Nuclear Structural Materials, *Scientific Reports* (2026).
  https://arxiv.org/abs/2607.10412

**Background the author needs in order to defend the work**
- Why BCC ferritic steels exhibit a ductile-to-brittle transition, and why austenitic steels
  largely do not
- What the Charpy V-notch test physically measures, and why absorbed energy is an index rather
  than a transferable material property
- Why 41 J is the conventional criterion for RPV steels, and what RT_NDT is used for
- Why reactor surveillance capsules exist and why irradiated test material is scarce
