# 提交与维护

## 参评者

1. 使用 `questions.json` 生成全部答案。不要将 Rubric 和参考答案作为 Student 输入。
2. 使用 `submission_template.json` 的结构，填写模型精确版本、生成日期、温度、输出上限和推理模式等配置。
3. 执行 `python3 validate.py --submission predictions.json`。
4. Fork 本仓库，把文件放入 `submissions/<model>-<date>.json`，通过 PR 提交。PR 说明接口模型名称、是否使用本地权重、是否接触过数据集或参考答案，以及特殊生成设置。不要提交密钥。

无法提交 PR 时可先创建 Issue 协调文件交付。外部 API 代跑目前通过维护者协调，不接受公开粘贴凭据。模型身份是提交者声明，不能据此证明输出一定来自该模型。

## 维护者：本机调用云端 Judge

审查 PR 数据文件后，把答案下载到受信任的仓库副本。不要在贡献者分支里直接运行其代码，也不要把 Judge Secrets 暴露给 fork PR。

```bash
cp judge_config.example.json judge_config.json
# 编辑确切模型 ID 和 OpenAI-compatible base URL；权重保持原值。
export JUDGE_GEMINI_API_KEY='在本机设置'
export JUDGE_CLAUDE_API_KEY='在本机设置'
export JUDGE_GPT_API_KEY='在本机设置'

python3 run_judges.py --submission predictions.json \
  --config judge_config.json --output evidence_model_date.json
```

配置文件只放环境变量的名称，不放 Key；`judge_config.json` 默认忽略。三路接口可以使用同一个兼容网关，但必须配置对应的三个不同模型。首次完整评测最多需要 420 个正常 Judge 请求，连接重试可能增加调用次数；API 费用由调用者承担。本次仓库构建没有调用付费模型。

失败时修复配置/接口后使用同一命令继续。输入答案、数据、Prompt 或配置变化后必须使用新输出文件，避免混合成绩。

## 审核与发布

确认真实调用来源、模型配置和逐题判分后，将完整证据归档到公开 GitHub Release 或不可变的 commit URL。使用：

```bash
python3 publish_score.py --evidence evidence_model_date.json \
  --evidence-url https://github.com/SatoSakula/MoveBench/releases/download/RELEASE/FILE.json
git add leaderboard.json
git commit -m "Add reviewed Release 1 evaluation"
git push
```

`RELEASE/FILE.json` 是示例占位符，必须替换为实际已公开的证据地址。发布工具重新计算细则分数，拒绝缺题或其他版本证据；它不能独立证明证据来自真实 Judge API。成绩更新经维护者推送后，GitHub Pages 读取同一份 `leaderboard.json`。

当前仓库不包含自动执行外部 API 配置的后台，不承诺提交后立即评分。后续若增加 Actions 评分队列，应限制手动触发权限、设置预算，并继续使用受信任主分支代码。
