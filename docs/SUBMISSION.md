# 提交与评测

1. 下载 data/questions.json，完成全部 140 道开放题。
2. 按 data/submission_template.json 填写模型精确版本、生成设置和全部答案。请披露是否使用过本题库、历史评分材料或参考答案。
3. 运行 `python3 tools/validate.py --submission predictions.json` 校验格式。
4. 通过 PR 提交至 `submissions/<model>-<date>.json`。不要上传密钥、私有配置或自评 Judge 证据。
5. 维护者核对后使用私有维护端评分、审核并更新汇总榜单；参评者无需本地运行评分。

评分材料和完整证据只在维护端保存。当前采用本地维护端调用云端 API，并非全天候自动后端；提交后不会即时出分。API 代跑需先通过 Issue 协调安全交付，不接受公开粘贴 Key。

模型身份由参评者声明；维护者可能要求补充生成记录。历史版本曾公开评分材料，因此当前题库不应宣传为从未曝光的隐藏测试。
