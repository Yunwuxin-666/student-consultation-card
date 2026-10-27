# 发布为飞书云文档并设置互联网可读

本流程面向已定稿的本地 `.md`。公开权限是高风险写操作，必须确认用户已针对当前任务明确要求互联网公开可见；仅有“分享一下”“开放给大家”不够。用户在本次咨询流程或同一会话中明确授权后，不重复询问。

1. **导入。** 按已安装的 `lark-drive` 技能与 `lark-shared` 安全规则，使用 `drive +import --type docx`。`--name` 必须与正文一级标题同为 `YYYYMMDD 真实姓名｜建弦转行咨询卡`，日期取咨询日，不能沿用源文件名或脱敏称呼。保留返回的唯一 `token`、`type=docx`、`url`。如返回 `ticket` 且 `ready=false`，用 `drive +task_result` 等待，不再次导入。

```powershell
& $cli drive +import --file '.\诊断卡.md' --type docx --name '20261023 王益｜建弦转行咨询卡' --as user
```

2. **回查正文并嵌入三图。** `docs +fetch --doc '<返回的URL>' --scope outline --max-depth 2 --as user`，核对七模块标题；按 [三图设计与嵌入](cards.md) 在第1节咨询信息后、第5节行动正文后、第7节案例正文后依次插入职业规划画布、学习行动卡与案例卡。逐节回读确认图片位置与正文完整性。导入局部失败时对已创建文档修复，不能用重导入创建第二份。
3. **读当前权限。** `drive +permission-get-setting --token <token> --type docx --as user`。如果已有 `link_share_entity=anyone_readable` 且 `external_access_entity=open`，直接进入最终回读。
4. **确认有权管理。** `drive permission.members auth --token <token> --type docx --action manage_public --as user`，需 `auth_result=true`。
5. **设置互联网可读。** 先按运行时 `lark-cli schema drive.permission.public.patch` 核对枚举和参数。已获用户对具体文档及“互联网获得链接者可阅读”的明确授权时，传 `external_access=true` 与 `link_share_entity=anyone_readable`，并按 CLI 的高风险门禁传 `--yes`。只赋予阅读权限，不设置任何人可编辑。不要一并扩大评论、复制或协作者管理权限。

```powershell
& $cli drive permission.public patch --token <token> --type docx --data '{"external_access":true,"link_share_entity":"anyone_readable"}' --as user --yes
```

6. **回读核验。** 再运行 `drive +permission-get-setting`。仅当 `external_access_entity=open` 且 `link_share_entity=anyone_readable` 时报告“互联网上获得链接的任何人可阅读”。权限错误如租户策略或密级限制时，保留文档、给出链接与实际权限状态，不能声称公开成功。遇到不确定结果先回读，不重复导入。

优先使用 `--as user`，不切到 bot 绕过权限。命令与权限枚举以当前安装的 `lark-cli` 帮助和 schema 为准。
