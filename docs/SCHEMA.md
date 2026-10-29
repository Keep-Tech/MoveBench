# 公开数据格式

本版本公开 80 题：50 道开放题（OQ）与 30 道选择题（MCQ），分 DA / PG / QA 三个领域。

## data/questions.json（仅题目，供学生作答）

JSON 数组，每题包含 `problem_id`、`problem`、`domain`、`question_format`。

- `problem` 含 `context`、`question`、`choices`。OQ 的 `choices` 为空对象；MCQ 的 `choices` 为 `{"A": "...", "B": "...", ...}`。context 与 question 相同时只发送一遍。
- `question_format` 为 `OQ` 或 `MCQ`。
- 本文件**不含** `evaluation`、`rubric` 或 `expect_answer`，供生成答案使用。

## data/benchmark.json / data/test.jsonl（完整记录，供评分与研究）

相同的 80 条完整记录，benchmark.json 为 JSON 数组，test.jsonl 为每行一条。每条含 `problem_id`、`problem`、`evaluation`、`metadata`、`expect_answer`。

- OQ：`evaluation.type = rubric`、`evaluation.question_structure = openQa`、`evaluation.rubric` 为逐项评分细则（dimension / criterion / description / score）；`expect_answer` 为参考答案，部分题目原始标注为空（null）。
- MCQ：`evaluation.type = exact_match`、`question_structure = singleSelect` 或 `multiSelect`；`expect_answer` 为标准答案，单选是字母字符串（如 `"A"`），多选是字母数组（如 `["A","B","D"]`）。

## data/submission_template.json

保留 Release 1 版本号。`dataset_sha256` 与 benchmark.json 的 SHA-256 一致，是与维护端匹配的固定版本标识。填写 `model_id`、`generation` 与每题 `model_answer` 后提交。`manifest.files` 记录各公开文件的 SHA-256 校验值。

MCQ 的 `model_answer` 建议直接给出选项字母（单选 `A`，多选 `A,C`），便于 exact_match 自动判分。

题目文本、ID 沿用原始题库。公开问题输入仅用于生成答案；OQ 的 rubric 评分在维护端按私有 Judge 流程执行，MCQ 可按公开答案自动判分。

## 提交生成设置

`generation.date` 使用 YYYY-MM-DD；`temperature` 为有限非负数；`max_tokens` 为正整数。MCQ 第一行仅填写有效选项字母，以英文逗号分隔，多选不得重复，单选仅一个字母；理由从第二行起填写。
