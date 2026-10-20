# MoveBench

中文运动健康教练大模型评测集 · MoveBench Team

[论文](https://arxiv.org/abs/2610.26185) · [在线题库与榜单](https://satosakula.github.io/MoveBench/) · [参评指南](docs/SUBMISSION.md) · [数据格式](docs/SCHEMA.md) · [English](docs/README_EN.md) · [品牌素材](docs/BRAND.md)

公开提供 **140 道中文开放题**，覆盖计划生成 PG（8）、运动数据分析 DA（44）、专业知识问答 QA（88）。这是论文 809 题完整评测集的公开子集；论文成绩与本批题目成绩分别报告。

## 当前公开范围

- `data/questions.json`：题目、稳定 ID、领域和题型；不包含评分细则或参考答案。
- `data/submission_template.json`：全部 140 题的答案提交模板。
- `data/manifest.json`：版本、数量、校验值和提交所需数据集标识。
- `tools/`：学生模型作答和答案格式校验工具。

逐题评分项、参考答案、Judge Prompt、配置和执行流程由维护者私有保存，提交后在维护端评分。当前维护端运行于受信任本机并调用云端 API，没有全天候自动评分服务。历史版本曾包含评分材料，当前收紧公开范围不代表这些题目成为从未公开的隐藏测试。

## 下载与作答

```bash
git clone https://github.com/SatoSakula/MoveBench.git
cd MoveBench
python3 tools/validate.py
export STUDENT_API_KEY='在本机设置，不要提交到 GitHub'
python3 tools/run_student.py --model organization/exact-model-version \
  --base-url https://api.example.com/v1 --output predictions.json
python3 tools/validate.py --submission predictions.json
```

Python 3.10+，公开工具仅依赖标准库。也可使用本地权重或其他 API 自行生成相同格式的答案。题目输入与原 Release 1 保持一致；不需要参评者运行 Judge 或提供 Judge 凭据。

## 提交与上榜

1. 完成全部 140 题，填写精确模型版本、生成设置及是否曾接触历史参考答案／评分材料。
2. 通过 PR 将答案提交到 `submissions/<model>-<date>.json`。不要提交 API Key。
3. 维护者核对完整性，在私有维护端评分并审核，再发布汇总成绩到榜单。完整评分证据私有归档，不公开逐项标准。

尚不支持提交后即时自动评分。需要 API 代跑时先通过 Issue 联系维护者协调；不要公开粘贴凭据。模型身份由参评者声明。成绩不构成医疗安全或真实训练效果认证。

## 许可与引用

当前公开题目采用 [CC BY 4.0](LICENSE)，公开代码采用 [MIT](LICENSE-CODE)。引用 MoveBench, Release 1 并链接本仓库，说明修改情况；论文见 [arXiv](https://arxiv.org/abs/2610.26185)。
