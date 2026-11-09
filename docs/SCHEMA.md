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

## 覆盖范围 / Coverage

| 场景 / Domain | 开放题 / OQ | 选择题 / MCQ | 合计 / Total |
|---|---:|---:|---:|
| PG | 17 | 9 | 26 |
| DA | 15 | 14 | 29 |
| QA | 18 | 7 | 25 |
| 合计 / Total | 50 | 30 | 80 |

以上为当前公开版，不代表完整 809 题的分布。完整记录中 50 道开放题有 464 条评分细则；29 道开放题的参考答案非空，其余为空。公开材料曾包含评分标准与答案，本版本不是未曝光测试集。

## 示例：从题目到提交 / Example workflow

读取 `data/questions.json`：`problem_id` 用于对应答案，`domain` 标识场景，`question_format` 区分 `OQ` 与 `MCQ`。当 `problem.context` 与 `problem.question` 不同且非空时应都提供；相同时仅提供一次。MCQ 还需提供 `problem.choices`。

将模型生成的文本写入提交模板中对应题目的 `model_answer`；例如：

```json
{
  "problem_id": "DA_OQ262",
  "model_answer": "示例回答：此处填写模型对该题的完整回答。"
}
```

上面仅为单条格式示意，不是参考答案，不能单独作为完整提交。提交须使用模板包含全部 80 个 ID、模型与生成参数。MCQ 单选如 `A`，多选如 `A,C`，可在下一行附理由。运行 `python3 tools/validate.py --submission predictions.json` 校验；通过仅表示结构合格，不代表完成评测。

HF 数据集提供仅含题目的表格形式：`questions_test.jsonl` 的 `choices` 是 `{label,text}` 列表；GitHub 的 `questions.json` 使用选项字母到文本的映射。GitHub 的完整 `benchmark.json` 和 `test.jsonl` 当前还包含 rubric、参考答案和正确选项。

## 数据构建与局限 / Construction and limitations

公开版从 809 题研究集选取 80 题；公开材料描述题目基于运动健康用户画像构建，覆盖训练方案、运动数据和知识问答。当前公开材料尚未完整说明 80 题抽样标准、具体标注与去标识化流程，详细信息以论文和后续维护文档为准。题目为中文、仅 80 题，不保证覆盖全部人群和运动健康场景；评测分数不能视为医疗安全或实际训练效果认证。
