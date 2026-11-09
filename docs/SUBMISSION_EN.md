# Submit model answers to MoveBench

The current public set contains 80 Chinese questions (50 open-ended, 11 single-select, 19 multi-select). It is a subset of the 809-question research benchmark. Read [the data schema](SCHEMA.md) and use the current [questions](../data/questions.json) and [submission template](../data/submission_template.json). The Hugging Face distribution is questions-only; GitHub also publishes full records with rubrics and reference answers. These materials have been exposed and the public set is not an unseen test set.

1. Generate an answer for each of the 80 question IDs. For MCQ, put the option letters on the first line, for example `A` or `A,C`; an explanation may follow on later lines.
2. Fill the template with the exact model ID, `generation.date` (YYYY-MM-DD), numeric nonnegative `temperature`, positive integer `max_tokens`, and all answers. Document the inference provider and thinking/reasoning settings in the PR; disclose prior exposure to questions, rubrics or reference answers. Do not include API keys or private credentials.
3. Run `python3 tools/validate.py --submission predictions.json`. Passing checks confirms structure and completeness, not the correctness of answers or an evaluation score.
4. Sign in to GitHub, fork [Keep-Tech/MoveBench](https://github.com/Keep-Tech/MoveBench), create a branch, and upload the JSON file to `submissions/<model>-<date>.json` in your fork. Open a pull request targeting `Keep-Tech/MoveBench:main`. The PR and its contents are public.
5. Check the PR's **Validate submissions** status and correct any errors on the same branch. Maintainers review and score the answers using their workflow; submission is not scored automatically or immediately. Keep the PR link as your receipt.

For evaluation on the full 809-question benchmark, the current project page provides **benchmarkcontact@keep.com**. Do not post API keys in issues or pull requests; contact maintainers to coordinate any API-based run. See the [Chinese submission guide](SUBMISSION.md) for details.
