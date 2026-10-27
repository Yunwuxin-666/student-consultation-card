# 归档到学员表格

目标 Base、咨询表与归档字段来自用户自己的 `config.json`。用户需已授权对该学员记录归档。

1. 从妙记和咨询学员表匹配学员，至少核对姓名、专业、学历、学校或咨询内容。重名或无法唯一确认时不写入。
2. 读取目标记录已有归档值。相同链接不重复写；已有不同链接时保留历史内容，必要时追加新链接。
3. 仅更新归档字段，写入发布后飞书 Docx 的 URL。
4. 再次读取该记录，核对姓名与 URL；只有回读成功才报告归档完成。

示例命令中所有占位符均需替换，不能把真实 Base ID 或学员记录 ID 提交到仓库：

```powershell
lark-cli base +record-upsert --base-token '<base-token>' --table-id '<consultation-table-id>' --record-id '<verified-record-id>' --json '{"职业画布归档":"https://example.feishu.cn/docx/<doc-token>"}' --as user
```
