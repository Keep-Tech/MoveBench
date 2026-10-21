# 提交与评测

1. 下载 `data/questions.json`，完成全部 80 题（50 道开放题 OQ + 30 道选择题 MCQ）。MCQ 请阅读选项后作答。
2. 按 `data/submission_template.json` 填写模型精确版本、生成设置和全部答案。请披露是否使用过本题库、历史评分材料或参考答案。
3. 运行 `python3 tools/validate.py --submission predictions.json` 校验格式。
4. 通过 PR 提交至 `submissions/<model>-<date>.json`。不要上传密钥、私有配置或自评 Judge 证据。
5. 维护者核对后使用私有维护端评分、审核并更新汇总榜单；参评者无需本地运行评分。

MCQ 采用 exact_match 判分，标准答案已随 `benchmark.json` / `test.jsonl` 公开，可自行自动判分。OQ 采用 rubric 逐项评分：rubric 评分细则已公开，但 Judge Prompt、评分配置和维护端执行流程私有保存，最终成绩以维护端复评为准。

当前采用本地维护端调用云端 API，并非全天候自动后端；提交后不会即时出分。API 代跑需先通过 Issue 协调安全交付，不接受公开粘贴 Key。

模型身份由参评者声明；维护者可能要求补充生成记录。本版本公开了 rubric 和参考答案，公开成绩可能受数据污染影响，不应宣传为从未曝光的隐藏测试。
