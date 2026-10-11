# Study report

- [Full PDF](charpy_test_matrix_study.pdf) — the typeset report.
- [Filled Markdown](report_filled.md) — the same report content, with numbers
  substituted and figure links that resolve in GitHub.
- [Plain-language explanation](PLAIN_LANGUAGE.md) — question, result, and limits.
- [Numeric claim map](claim_source_map.csv) and [constant map](constant_source_map.csv)
  — provenance for reported values.

The analysis uses published measurements and labeled synthetic validation and
Monte Carlo data. No physical Charpy tests were performed for this project.
The miniature-versus-full-size result is conditional on the tested models,
material budget, geometry, temperature reachability, and correction assumptions.

The October 11, 2026 presentation update removes the title-page byline and fixes
relative figure links. It changes no input dataset, scientific calculation,
reported result, source-map value, or third-party attribution. The report builder
and delivery checks use the same presentation rules when the report is regenerated.

Run `./run_all.sh` from the repository root for complete reproduction. To rebuild
only the report from existing outputs, use the pinned environment with
`.venv/bin/python src/wp7_report.py` and `.venv/bin/python src/wp7_tests.py`.
