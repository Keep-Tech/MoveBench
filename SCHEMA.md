# 数据格式

完整 JSON/JSONL 每条记录包含：

| 字段 | 含义 |
|---|---|
| `problem_id` | 原始稳定 ID，领域前缀 PG/DA/QA |
| `problem.context` | 场景或用户上下文 |
| `problem.question` | 题目正文；可能与 context 相同，生成提示词时去重 |
| `problem.choices` | 本批均为开放题，保留原始结构 |
| `evaluation.type` | `rubric` |
| `evaluation.question_structure` | `openQa` |
| `evaluation.rubric[]` | `dimension`、`criterion`、`description`、`score`；score 是该项最大值 |
| `expect_answer` | 原始参考答案，供研究/评分参考，不发送给 Student |
| `metadata` | 原始结构化标签 |
| `release_metadata` | 原 Excel 发布筛选标签；不参与评分 |

`benchmark.json` 与 `test.jsonl` 完全等价。`questions.json` 仅含 `problem_id`、`problem`、`domain`、`question_format`，没有答案或评分细则。保留原题 ID，不重新编号。原文、参考答案和 Rubric 未在导出时改写。

原始发布清单的 140 个 ID 和题目文本均已逐条匹配。58 行 Excel 题型显示标签为空或与原标注不同，因此评分以结构化标注为准。首月分组和筛选理由是来源元数据，不应误读为能力领域或评分维度。

模板中的空答案用于填写，不是可直接评分的样例。正式提交必须包含完整题集，未知/重复 ID、空答案、版本或 hash 不一致都会被拒绝。
