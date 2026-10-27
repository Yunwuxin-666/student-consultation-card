# Student Consultation Card

根据飞书妙记咨询逐字稿、学员 Base、产品页面及可核实的往期案例，生成七模块咨询诊断文档和三张黄白黑瑞士网格 PNG 卡片。

## 使用

1. 安装并登录 `lark-cli`，准备 Python 3 与 Chrome 或 Edge。
2. 复制 `config.example.json` 为 `config.json`，填写自己的飞书 Base、表 ID、归档字段和产品资料链接。`config.json` 已被 Git 忽略。
3. 将本目录安装为 Codex skill，提供飞书妙记链接并调用 `$student-consultation-card`。
4. 公开飞书云文档须由用户明确授权。skill 会按第 1、5、7 节插入三图，回读权限及归档结果。

## 输出

文档七节依次为咨询信息、核心结论、当前卡点、方向建议、学习与行动路径、解决方案、往期学员适配案例。三张图为职业规划画布、学习行动卡和往期案例卡。

案例先按校招或社招阶段筛选，再按专业、学历、年龄和岗位匹配。在校求职可同时选实习与校招正职案例。实习日薪、正式月薪、最高涨幅分别保持原始口径。

渲染器可单独运行：

```bash
python scripts/render_canvas.py --input path/to/data.json --output-dir outputs --slug demo
python scripts/render_cards.py --input path/to/data.json --output-dir outputs --slug demo
```

输入 JSON 顶层包含 `canvas`、`action`、`cases`。字段说明见 [卡片规范](references/cards.md)。生成的数据与逐字稿可能含个人信息，请仅保存在本地或有权限的飞书空间，不要提交到公开仓库。

## 仓库内容

- `SKILL.md`：完整工作流程与文案约定
- `references/`：读取、产品匹配、案例口径、发布与归档规则
- `scripts/`：HTML 与 PNG 渲染器
- `assets/`：职业规划画布 HTML 底稿

本仓库不包含真实学员资料、私有 Base ID 或身份凭证。
