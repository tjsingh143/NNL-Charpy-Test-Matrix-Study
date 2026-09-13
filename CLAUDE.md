# CLAUDE.md — persistent rules for this repository

Charpy transition-temperature uncertainty and test-matrix study: an analysis of published Charpy V-notch test data for
reactor pressure vessel steels. This project uses fresh context windows at checkpoints; rebuild state from the repository.

## Authority and state
- `PROJECT_BRIEF.md` defines the requirements, except where an explicitly approved amendment (listed at its top, and logged in
  `DECISIONS.md`) changes them.
- Before beginning any new work package, read `DECISIONS.md` and `PROGRESS.md` in full.
- Treat claims in existing files as evidence to inspect, not facts to repeat.

## Scope of work
- Complete only the work package the author has explicitly authorized.
- Stop at every checkpoint in `PROJECT_BRIEF.md` §9 and wait for explicit approval before continuing.
- At checkpoints, explain the engineering and statistics in plain English that a first-year engineering student could defend in an interview.
- No machine-learning drift: this is a test-programme design study, not prediction of full-size properties.
- Do not use or spawn agents or subagents.

## Scientific integrity
- Never fabricate, impute or fill in experimental measurements. Missing means missing.
- Always describe the work as analysis of published test data. Never state or imply that anyone here performed Charpy tests,
  operated test equipment or handled irradiated material.
- Synthetic data only for fitter validation (WP3) and the Monte Carlo (WP6), labelled synthetic everywhere.
- Every meaningful scientific judgement call goes in `DECISIONS.md` (what, alternatives, why, consequence of the alternative).
- Do not tune inclusion rules, duplicate handling or scatter models on downstream results; if that happens, log it as exactly that.
- Prefer transparent, defensible methods over sophistication. Cite every external convention or number.

## Reproducibility
- Every reported number must be regenerable from code. `./run_all.sh` regenerates all outputs from `data/raw/`
  (pinned environment in `.venv/`, see `requirements.txt`; the script refuses other package versions).
- Raw files in `data/raw/` are never modified; `data/CHECKSUMS.sha256` is verified on every run.
- WP2 cohorts are frozen at CP2 (`data/FROZEN_COHORTS_CP2.csv`, verified on every run). Later work packages read them from
  `outputs/wp2*/cohort_membership.csv`; changing one requires an approved decision in `DECISIONS.md` (D-039).
- Scratch work belongs outside the repository.

## Git
- `main` holds checkpoint-approved states only. Work awaiting checkpoint approval is committed on a branch named for the work
  package; merge only after the author approves. Commit at meaningful boundaries. Never push or add a remote unless asked.
