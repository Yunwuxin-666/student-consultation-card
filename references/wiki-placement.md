# 咨询文档归位到知识库

在本地配置中指定目标知识库年份节点的 Wiki URL。移动前用 `lark-cli wiki +node-get --node-token <目标 URL> --as user` 回读标题、`space_id`、`node_token` 和父节点；路径不符时停止，不能凭旧 token 猜位置。

完成导入及三图嵌入后，使用 `lark-cli wiki +move --obj-type docx --obj-token <文档 token> --target-space-id <space_id> --target-parent-token <年份 node_token> --as user` 将原件迁入。已有 Wiki 节点使用 `--node-token` 移动。异步任务按返回的 `next_command` 查询，不重复移动。

迁移后回读 `obj_token`、`parent_node_token`、`space_id` 和标题。标题须为 `YYYYMMDD 真实姓名｜建弦转行咨询卡`；不一致时用 `drive +update-title --url <Wiki节点URL> --title <规范标题> --as user` 原地更名，不能复制或重建节点。再读取及设置文档公开权限；迁移可能把原先的互联网可读重置为组织内可读。只有最终回读为 `external_access_entity=open` 且 `link_share_entity=anyone_readable`，才可对外声明公开。学员表归档字段存放实际可访问的文档链接。
