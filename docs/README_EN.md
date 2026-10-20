# MoveBench

[Paper](https://arxiv.org/abs/2610.26185) · [Leaderboard](https://satosakula.github.io/MoveBench/)

This release provides 140 Chinese open-ended questions: PG 8, DA 44, QA 88. Public files contain questions, stable IDs, domains, formats, a submission template and checksums. Rubrics, reference answers and evaluation implementation are retained privately by maintainers.

Generate answers from `data/questions.json` using `tools/run_student.py` or your own model runner. Validate using `python3 tools/validate.py --submission predictions.json`, then submit all 140 answers in a pull request under `submissions/`. Include the exact model version and generation settings. Never submit API keys.

Maintainers evaluate submissions using a private local workflow and cloud APIs, review results, and publish aggregate leaderboard scores. This is not an always-on automatic service. Earlier versions exposed evaluation materials; participants must disclose prior use. These are not previously unseen held-out questions. Paper-wide scores must not be reused for this subset.

Public questions: CC BY 4.0. Public code: MIT. Scores are not clinical or exercise-safety certifications.
