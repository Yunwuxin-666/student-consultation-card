# 咨询文档归位到课程组知识库

归档目录无需逐次询问。生成前先核对目标 Wiki 节点的标题、父级、年份和权限；能唯一确认时沿用下方目录。节点不存在、年份不符、出现多个同名候选、权限不足或用户指定了不同位置时，再向用户询问准确归档地址。未确认前保留本地稿，不把文档移入猜测的目录。

目标：课程组知识库「00 9.9/99职业规划咨询课 → 2026」。目标节点链接：`https://he9za7tvkd.feishu.cn/wiki/LG9hwY3xdiPVuVkFQXqcEaZ0nt2`。执行时先用 `lark-cli wiki +node-get --node-token <目标链接> --as user` 回读其标题、`space_id`、`node_token` 和父节点；目标标题或层级不符时停止迁移，不能凭旧 token 猜位置。

新文档先完成 Markdown 导入和三图嵌入，再使用 `lark-cli wiki +move --obj-type docx --obj-token <文档 token> --target-space-id <目标 space_id> --target-parent-token <目标 node_token> --as user` 将原件迁入。已有 Wiki 节点用 `--node-token <原节点>` 移动。遇到异步任务按返回的 `next_command` 查询，不重复移动。

移动后用 `wiki +node-get` 核对 `obj_token` 与源文档一致、`parent_node_token` 等于目标 2026 节点、`space_id` 等于课程组空间，并回读节点标题为 `YYYYMMDD 真实姓名｜建弦转行咨询卡`。标题不一致时用 `drive +update-title --url <Wiki节点URL> --title <规范标题> --as user` 原地更名，再回读底层文档标题；不要复制或重建节点。随后重新读取并设置该文档公开权限：迁移可能将 `external_access_entity` 重置为 `closed`，`link_share_entity` 重置为 `tenant_readable`。只有迁移后最终回读为 `open` 与 `anyone_readable`，才可对外声明公开。学员表“职业画布归档”仍使用该文档的实际可访问链接，不用节点标题代替。
