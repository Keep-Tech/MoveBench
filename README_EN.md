# MoveBench — Release 1

[中文说明](README.md)

MoveBench evaluates large language models for sports and health coaching. This release contains **140 Chinese open-ended questions with 1,224 rubric criteria**, reference answers and metadata. Attribution: **KeepaceAI Team**. Maintained by [SatoSakula](https://github.com/SatoSakula).

| Domain | Items |
|---|---:|
| Plan Generation (PG) | 8 |
| Data Analysis (DA) | 44 |
| Question Answering (QA) | 88 |

This public subset is distinct from the paper's 809-question, 5,012-criterion benchmark. **Paper leaderboard scores are not Release 1 scores.** All items in this release are open-ended; source spreadsheet labels do not override the canonical structured annotations.

## Files and usage

- `test.jsonl`: one complete record per line.
- `benchmark.json`: equivalent JSON array.
- `questions.json`: Student inputs only, excluding references and rubrics.
- `submission_template.json`: fill every answer and specify the exact model configuration.
- `manifest.json`: dataset version, provenance, counts and SHA-256 hashes.

```bash
python3 validate.py
python3 -m unittest -v
export STUDENT_API_KEY='set locally'
python3 run_student.py --model organization/exact-version \
  --base-url https://api.example.com/v1 --output predictions.json
python3 validate.py --submission predictions.json
```

Python 3.10+ is required. Runtime tools use the standard library and an OpenAI-compatible Chat Completions API; other inference implementations may produce the same submission schema directly.

Submit all 140 answers through a PR at `submissions/<model>-<date>.json`. Maintainers run three cloud judges on trusted code, inspect the evidence, and publish a version-specific leaderboard. There is currently no continuously running evaluation backend. Never put API keys in PRs, Issues or tracked configuration files.

Judges have weights .35/.35/.30. At least two explicit redline votes override the item score to zero. Format scores pool earned/maximum points; Overall weights format scores by scored item counts. Since Release 1 contains only OQ, its Overall equals its OQ pooled ratio. Domain scores are diagnostic item-normalized macro means. See [SCORING.md](SCORING.md) and [SUBMISSION.md](SUBMISSION.md).

Dataset, reference answers, rubrics and documentation: **CC BY 4.0**. Python/workflow code: **MIT**. Cite **KeepaceAI Team, MoveBench, Release 1**, link this repository and indicate modifications. See `CITATION.cff`.

These are open-reference evaluations and cannot establish absence of training contamination or verify self-reported model identity. References and rubrics are versioned evaluation conventions, not clinical safety certification. The release process did not independently re-review every scientific claim.
