# MoveBench

**中文运动健康教练大模型评测集 · KeepaceAI Team**

[English](docs/README_EN.md) · [数据格式](docs/SCHEMA.md) · [参评流程](docs/SUBMISSION.md) · [评分说明](docs/SCORING.md) · [CC BY 4.0](LICENSE)

MoveBench 评估大模型在运动健康教练场景中的计划生成（PG）、数据分析（DA）和问答（QA）能力。首批公开 **140 道中文开放题、1,224 条逐题评分细则**，附参考答案、标准化 JSON/JSONL 和本地评测工具。

## 当前版本

| 范围 | 数量 |
|---|---:|
| PG · Plan Generation | 8 |
| DA · Data Analysis | 44 |
| QA · Question Answering | 88 |
| 合计 | **140** |

- 140 题全部采用原始结构化标注中的 `rubric / openQa`，没有 SS/MS 题。
- 论文完整评测包含 **809 题、5,012 条细则**。当前版本是其中按发布清单选择的子集，**不等同于完整论文数据**。
- 论文中的 15 模型成绩来自完整题库，不能填入本批 140 题的榜单。当前公开版榜单从空榜开始。
- Excel 中有 58 行题型标签为空或与结构化标注不同；原标签保存在 `release_metadata`，评分统一遵循结构化标注。

## 文档与目录

| 目录 | 内容 |
|---|---|
| [docs/](docs/) | 数据格式、评分方法、参评维护说明与英文文档 |
| [data/](data/) | JSON/JSONL 数据、模型输入、提交模板与版本校验 |
| [tools/](tools/) | 本地生成答案、三 Judge 评分、校验及发布工具 |

[在线数据集与榜单](https://satosakula.github.io/MoveBench/) · [固定版本下载](https://github.com/SatoSakula/MoveBench/releases/tag/release-1)

以下命令均在仓库根目录运行。

## 下载与加载

| 文件 | 用途 |
|---|---|
| [test.jsonl](data/test.jsonl) | 每行一题，包含问题、Rubric、参考答案和元数据 |
| [benchmark.json](data/benchmark.json) | 相同完整记录的 JSON 数组，兼容既有数据结构 |
| [questions.json](data/questions.json) | 仅问题、ID、领域、题型；不含参考答案和 Rubric，供 Student 使用 |
| [submission_template.json](data/submission_template.json) | 完整 140 题的提交模板；需要填写全部答案 |
| [manifest.json](data/manifest.json) | 数据量、来源、版本和 SHA-256 校验 |

```python
import json
from pathlib import Path

records = [json.loads(line) for line in Path('data/test.jsonl').read_text().splitlines()]
print(len(records))  # 140
```

也可以使用 Hugging Face `datasets` 库直接读取本地 JSONL，不需要 HF 账号：

```python
from datasets import load_dataset
dataset = load_dataset('json', data_files={'test': 'data/test.jsonl'}, split='test')
```

上述示例显式使用 `test` split。公开评测时请披露是否使用过本数据集或参考答案。

## 本地生成答案

运行需要 Python 3.10+，评测脚本只依赖标准库。

```bash
git clone https://github.com/SatoSakula/MoveBench.git
cd MoveBench
python3 tools/validate.py
python3 -m unittest discover -s tools -v

export STUDENT_API_KEY='在本机设置，不要提交到 GitHub'
python3 tools/run_student.py --model organization/exact-model-version \
  --base-url https://api.example.com/v1 --output predictions.json
python3 tools/validate.py --submission predictions.json
```

支持 OpenAI-compatible Chat Completions 接口。使用本地权重、自定义程序或其他厂商协议，也可自行生成相同格式的 `predictions.json`。Student 不需要 Judge 凭据。

## 提交与上榜

1. 完成全部 140 题，将答案文件通过 Pull Request 提交至 `submissions/<model>-<date>.json`。
2. 维护者核对数据版本、覆盖率和模型声明，在受信任本机使用云端三 Judge 重新评分。
3. 维护者审核逐题证据后，运行 `publish_score.py` 更新 `leaderboard.json` 并提交。启用 GitHub Pages 后，静态页面随仓库内容更新。

目前采用 **提交答案文件 → 维护者运行 Judge → 审核上榜**，不是全天候自动评分服务，也不在公开 Issue、PR 或配置文件中接收 API Key。需要代跑 API 时，先通过 Issue 联系维护者确定接口和安全交付方式。

三 Judge 固定权重为 Gemini 0.35、Claude 0.35、GPT 0.30；至少两名 Judge 判定明确红线时该题清零。具体公式、原始双 Judge 脚本与新协议的区别、失败处理见 [SCORING.md](docs/SCORING.md)。

## 适用范围

适合比较中文运动健康教练回答的 Rubric 满足程度。公开参考答案和评分细则可能造成数据污染；本地生成答案的模型身份由提交者声明。成绩不是医疗安全或真实训练效果认证。

此次发布保留原题、原 Rubric 和参考答案，不代表对每条运动医学陈述进行了独立复审。维护者欢迎通过 Issue 提交具体问题 ID、证据和修改建议。

## 引用与许可

使用时注明 ** MoveBench, Release 1**，链接至本仓库，说明是否修改。机器可读引用见 [CITATION.cff](CITATION.cff)。论文的正式发表信息确认后再补充；本仓库不预先声明已发表或编造 DOI。
