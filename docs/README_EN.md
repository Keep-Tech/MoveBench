# MoveBench

[Paper](https://arxiv.org/abs/2610.26185) · [Leaderboard](https://satosakula.github.io/MoveBench/)

This release provides 80 Chinese questions across three scenarios (PG / DA / QA): 50 open-ended questions (OQ) and 30 multiple-choice questions (MCQ, 11 single-select and 19 multi-select). Domain split: DA 29, PG 26, QA 25. Open-ended questions include 464 rubric criteria.

Public files include:
- `data/questions.json` — questions only (empty choices for OQ, choices included for MCQ), stable IDs, domains and formats; no rubrics or answers. Use this to generate answers.
- `data/benchmark.json` / `data/test.jsonl` — full records. OQ records carry rubric criteria and reference answers; MCQ records carry choices and gold answers. For scoring and research.
- `data/submission_template.json` and `data/manifest.json` — submission template and checksums.

This release makes rubrics and reference answers public. MCQ is graded by exact_match with public gold answers; OQ is graded by rubric, with Judge prompts, scoring configs and the maintainer workflow kept private.

Generate answers from `data/questions.json` using `tools/run_student.py` (it appends choices and asks for option letters on MCQ) or your own model runner. Validate with `python3 tools/validate.py --submission predictions.json`, then submit all 80 answers in a pull request under `submissions/`. Include the exact model version and generation settings. Never submit API keys.

Maintainers evaluate submissions using a private local workflow and cloud APIs, review results, and publish aggregate leaderboard scores. This is not an always-on automatic service. Because rubrics and answers are public, scores may be affected by data contamination; participants must disclose prior use, and these are not previously unseen held-out questions. Paper-wide scores must not be reused for this subset.

Public questions: CC BY 4.0. Public code: MIT. Scores are not clinical or exercise-safety certifications.
