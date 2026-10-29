# 飞书读取与案例数据

案例查询时用内部真实姓名和其他身份字段关联营课表、评价表及重复记录，仅用于核实与去重；同一人多次报名、回访或多个 Offer 只产生一个对外案例。对外写入前将真实姓名统一改为“姓氏＋同学”（如张思思→张同学，复姓欧阳某→欧阳同学）。同姓不同人并列时采用“张同学（案例一／案例二）”或只保留一例，绝不通过展示名字消歧。原名只留在内部核查材料，不得流入正文、卡片数据、图片或云文档。发布前以本次选用案例的全部原名逐一搜索本地稿和导入后的云文档，并人工查看图片；出现一次即修正。

## CLI和会议

优先 `Get-Command lark-cli`。本机可用：`C:\Users\Administrator\AppData\Local\Programs\lark-cli\lark-cli.exe`。显式沿用 `--as user`；鉴权失败时参考已安装的 lark-shared，不切换身份绕过权限。相关技能根目录为 `C:\Users\Administrator\.agents\skills`，会议走 lark-meeting，Wiki走 lark-doc，表格走 lark-base；只读取当前操作需要的参考。

从 `https://域名/minutes/<token>?...` 提取token：

```powershell
& $cli minutes +detail --minute-tokens '<token>' --transcript --as user
```

返回 `data.minutes[].artifacts.transcript_file`，按实际路径以UTF-8读取全文。已存在文件且需要更新时添加 `--overwrite`。日期取会议资料，不用今天替代。文件通常位于 `minutes/<token>/transcript.txt`。仅有消息链接时不能把消息token当妙记token；需先解析关联会议，不能读取则请用户提供妙记链接。

Wiki读取（先目录后相关章节，避免一次拉取多年课表）：

```powershell
& $cli docs +fetch --doc '<wiki-url>' --scope outline --max-depth 2 --as user
& $cli docs +fetch --doc '<wiki-url>' --scope section --start-block-id '<返回的标题ID>' --as user
```

保留完整JSON作为内部依据，正文位于 `data.document.content`。内嵌表格、PDF等只有影响本次方案时才按对应技能继续读取，不从图片描述或附件名推断权益。无权限时不自动发起授权申请。

## 学员Base

Base：`OSbNbeavAabLTws6xkPcGz3ln0Y`。

- `01 咨询学员汇总`：`tblq5GuU7YDAXA02`，匹配当前学员。
- `02 营课学员汇总`：`tblzt9Szm9LcTMU9`，背景、报名课程及转行进度。
- `学员评价（总）`：`tblOuObjSqtk2vEp`，岗位、去向、薪资及评价。

字段变化时先 `base +field-list --base-token ... --table-id ... --as user`，字段列表是 `data.fields`，不是 `data.items`。

营课表常用字段：`真实姓名`、`专业`、`学历`、`年龄`、`学校`、`工作年限`、`商品名称（内部下单）`、`求职招聘类型`、`预期求职地域`、`转行进度`、`找到实习/正职Offer赛道`、`你找到实习/正职Offer的公司名称（可多填）`。

评价表常用字段：`真实姓名`、`您的专业`（文本）、`您的学历`、`您的年龄`、`您的学校`、`转行前工作年限`、`您报名的课程（可多选）`、`求职招聘类型`、`你找到实习/正职Offer的岗位名称（可多选）`、`转行后最终去向实习/正职Offer的公司`、`你找到的全部实习/正职Offer的公司名称及情况（需多填）`、`转行前薪酬水平（月薪base，年薪/月份）：`、`转行后拿到的Offer薪酬水平（月薪base，年薪/月份，可多选）：`、`转行拿到的Offer最大薪酬涨幅`、`您对建弦培训的整体满意度如何？`。

案例还应读取评价表的 `转行后最终实习/正职Offer的公司的工作强度`、`最终去向实习/正职Offer的工作城市`、`最终去向实习/正职Offer的具体城市`、`转行后最终去向实习/正职Offer的公司规模`，以及确有需要时的 `转行后的实习/正职Offer对工作的满意度`。先按当前字段列表核对名称和类型。正文优先补充最终去向的工作城市、公司规模、工作强度，与岗位、薪资同列为事实；字段为空就省略，不写“未知”。“期望求职城市”不能冒充最终工作城市；多份 Offer 的公司、城市、薪资和强度只有明确对应时才放在同一案例结果中。工作强度照原始选项写，不改写成主观的“轻松”“稳定”。公司规模照原始区间写，不推断公司级别。

## 查询方式

当前学员用姓名搜索，重复 `--field-id` 仅投影必要字段：

```powershell
& $cli base +record-search --base-token 'OSbNbeavAabLTws6xkPcGz3ln0Y' --table-id 'tblq5GuU7YDAXA02' --keyword '<姓名>' --search-field '真实姓名' --field-id '真实姓名' --field-id '专业' --field-id '学历' --field-id '学校' --format json --as user
```

上例只用于定位身份，不能据此写完个人画像。定位后按 `base +field-list` 找到当前表中对应的求职阶段、毕业时间、工作状态与年限、当前工作内容、项目或作品、已掌握工具、意向岗位与城市、学习时间、预算及顾虑字段，再只投影本次有用的字段。表中没有的细节回逐字稿核对；表格与会议冲突时记录来源，不能把旧表值混成咨询当天现状。外发文档只写与判断方向、行动和方案相关的信息，不带联系方式或内部备注。

往期案例优先云端过滤。UTF-8保存过滤文件并通过 `@文件路径` 传入：

```json
{"logic":"and","conditions":[["专业","intersects",["环境环艺"]],["学历","intersects",["本科"]]]}
```

```powershell
& $cli base +record-list --base-token 'OSbNbeavAabLTws6xkPcGz3ln0Y' --table-id 'tblzt9Szm9LcTMU9' --filter-json '@./work/case-filter.json' --field-id '真实姓名' --field-id '专业' --field-id '学历' --field-id '工作年限' --field-id '商品名称（内部下单）' --field-id '转行进度' --format ndjson --output './work/cases.ndjson' --as user
```

按候选姓名搜索评价表，交叉核对背景以排除同名。JSON模式 `data.fields` 与 `data.data` 矩阵按列对应；ndjson逐行读取。检查 `has_more` 和分页/manifest，首屏不能代表完整结果。找到足够符合条件且证据完整的案例即可结束，不做未经全量验证的“只有这些”等结论。重复报名或重复回访按同一人去重，优先较新且明确的结果。

匹配先设阶段门槛：从当前学员的 `求职招聘类型`、年级、工作年限判断校招或社招；评价表的 `求职招聘类型` 与 `处于转行的什么阶段` 必须共同核对。在校求职学员优先选校招案例，并在有证据时同时呈现实习Offer与校招正职Offer；再比较同专业及学历、年龄、目标岗位、学校类型和证据完整性。找不到同阶段案例时才扩到邻近阶段，并在内部说明原因；不得以社招正式Offer案例充当校招结果。当前场景仅输出2—3例文字，不沿用咨询.skill的5—8例图片报告要求。学校层次无资料时不猜测。

## 薪资与结果口径

- 使用记录中原始范围，区分税前/税后、月薪/年包、几薪、实习/正式、全部Offer/最终去向。每份薪资与公司/岗位没有明确对应关系时不可自行绑定。
- 优先评价表的直接填写字段。汇总表引用值和评价表不一致时查看提交时间、具体说明并记录冲突；无法消解则仅用无歧义事实，不自行挑更高的数字。
- 有前后薪资和涨幅字段时一起写。原字段为“最大涨幅”则保留“最高薪资涨幅”，不得改成最终入职涨幅。
- 实习案例优先写实习日薪及实习Offer状态；无可比的转行前收入时不展示月薪涨幅，也不把实习日薪折算为月薪。
- 区间不能取中值或端点计算精确涨幅；零收入不能计算百分比。明确同口径的精确数值才可按用户需要计算并标明计算值。没有涨幅数据就省略，不编造。
- 姓名用“林同学”等脱敏，外发正文不含联系方式、微信、内部ID或私有表格链接。不得为了增加说服力虚构培训与录用之间的因果。

Windows Python输出中文时可设置 `$env:PYTHONIOENCODING='utf-8'`；优先明确UTF-8文件读写，避免控制台编码损坏。不要为读取资料打印认证配置或密钥。
