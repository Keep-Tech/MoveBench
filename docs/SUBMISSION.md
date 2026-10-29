# 提交与评测

当前版本：**80 题（50 OQ + 11 单选 + 19 多选）**。请使用 main 分支的 [questions.json](../data/questions.json) 和 [submission_template.json](../data/submission_template.json)，不要混用旧版 140 题 Release。

## 准备与校验

填写 `model_id`（精确模型版本）、`generation.date`（YYYY-MM-DD）、`temperature`（非负数）、`max_tokens`（正整数）及全部 80 条 `predictions`。注明模型推理设置，并在 PR 中披露是否接触过题库、评分细则或参考答案。

MCQ 答案第一行仅填写选项字母：单选 `A`，多选 `A,C`（英文逗号，不得重复）；可从第二行起写理由。校验仅检查格式与完整性，不判断答案是否正确。

```bash
python3 tools/validate.py --submission predictions.json
```

## 网页提交（无需命令行）

1. 登录 GitHub，打开 [公司仓库](https://github.com/Keep-Tech/MoveBench)，点击右上角 **Fork**，创建到自己的账号。已有 Fork 请先 **Sync fork → Update branch**。
2. 在自己的 Fork 中新建一个提交分支。在 `submissions/` 目录点击 **Add file → Upload files**，上传校验后的 JSON，命名为 `<model>-<YYYY-MM-DD>.json`，然后提交到自己的分支。没有写入公司仓库权限是正常的，不需要申请组织成员资格。
3. 点击 **Contribute → Open pull request**。确认 base repository 是 `Keep-Tech/MoveBench`，base 是 `main`，head 是你的 Fork 和提交分支。
4. 按 PR 模板填写模型版本、生成设置、数据曝光声明，点击 **Create pull request**。保留 PR 链接作为提交回执。文件将公开，请勿上传密钥、私有配置或 Judge 证据。
5. 在 PR 的 **Checks** 查看 `Validate submissions`：失败时按错误提示更新同一分支；通过仅表示格式合格。维护者随后核对、私有评分、审核，发布结果后会在 PR 告知；不会即时自动出分。

## 命令行提交

```bash
# 先 Fork 到自己的账号，克隆自己的 Fork，再执行：
git switch -c submission/my-model-20261029
cp /path/to/predictions.json submissions/my-model-20261029.json
python3 tools/validate.py --submission submissions/my-model-20261029.json
git add submissions/my-model-20261029.json
git commit -m "Submit model answers"
git push -u origin HEAD
# 到自己的 Fork 页面点击 Compare & pull request，目标选择 Keep-Tech/MoveBench:main。
```

## 审核与状态

- **已提交**：PR 已创建；**格式校验通过**：Checks 成功；**待评分／待审核**：维护者处理；**已发布**：维护者更新榜单并回复 PR。以 PR 实际进展为准，无固定出分时限。
- MCQ 采用 exact_match，OQ 采用 rubric 逐项评分。Judge Prompt、配置和维护端执行流程私有保存，最终成绩以维护端复评为准。
- 当前本地维护端调用云端 API，并非全天候自动后端。API 代跑需先通过 Issue 协调安全交付，禁止公开粘贴 Key。
- 模型身份由提交者声明，维护者可能要求生成记录。公开版题库、rubric 和参考答案存在曝光，不应宣传为未曝光的隐藏测试。
- 联调测试请在标题注明 **TEST ONLY — DO NOT MERGE**。测试 PR 不合并、不评分、不上榜。
