# 公开数据格式

`data/questions.json` 是 JSON 数组，每题包含 `problem_id`、`problem`、`domain`、`question_format`。`problem` 仅有 `context`、`question`、`choices`；140 题全部为开放题（OQ）。context 与 question 相同时只发送一遍。公开文件不包含 evaluation、rubric 或 expect_answer。

`submission_template.json` 保留原 Release 1 版本和 dataset_sha256 标识，填写 model_id、generation 与每题 model_answer 后提交。manifest.files 校验当前公开文件；dataset_sha256 是与维护端匹配的固定版本标识，不要求参评者持有私有评分文件。

题目文本、ID、顺序和学生 Prompt 未改变。公开问题输入仅用于生成答案，评分在维护端执行。
