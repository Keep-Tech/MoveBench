# Dataset release notes

## Current public subset — release-1

- 80 Chinese questions: 50 open-ended, 11 single-select, 19 multi-select; PG 26 / DA 29 / QA 25.
- `data/questions.json` is question-only. `data/benchmark.json` and `data/test.jsonl` contain evaluation records, including rubrics and reference answers. The Hugging Face dataset is a separate questions-only distribution.
- `data/manifest.json` records checksums and the scoring dataset identity; the public 80-question subset is distinct from the 809-question paper evaluation.
- See [the current release](https://github.com/Keep-Tech/MoveBench/releases/latest) and [submission guide](docs/SUBMISSION_EN.md). Historical release files describe an earlier 140-question distribution and are not compatible with the current template.

This file records the present release scope; it is not a complete historical change log.
