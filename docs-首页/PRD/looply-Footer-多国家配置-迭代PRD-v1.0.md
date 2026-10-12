# Looply Footer 多国家配置迭代 PRD

版本：v1.0
日期：2026-10-12

## 一、迭代目标

在现有 Footer 与关联页面 PRD 基础上，补齐 Footer 按国家读取内容、C1 Sell 联动和 Contact Us 国家信息传递规则。本文件只描述本次新增或变化，未变化的 Footer、法律文件、FAQ 和 Contact Us 完整规则统一查询 [Footer 与关联页面 PRD v0.7](./looply-Footer-PRD-v0.7.md)。

## 二、后台国家范围

- Footer 后台以页面顶部选择的国家为配置范围；国家来自 C2 业务国家管理，允许提前维护未启用国家。
- 切换国家后，法律文件、FAQ、社媒账号和相关编辑状态全部切换到目标国家；未保存内容需先提示保存或放弃。
- 普通 Footer 入口不新增逐条名称、启停或排序配置，站内 URL 由当前国家和语言自动拼接 locale。

## 三、C1 Sell 联动

- Footer 的 `SELL` 栏、`Seller FAQ`、`Seller Agreement` 以及其他 C1 入口统一跟随当前国家的 Sell 生效条件：C2 国家已启用且 C1 Sell 已开放。
- 当前国家未生效时隐藏整个 `SELL` 栏、`Seller FAQ` 和 `Seller Agreement`，保留非 C1 Footer 内容。
- Contact Us 页面入口始终保留；仅动态隐藏或展示 `Selling to Looply` 和 Sell 联系信息。
- C1 入口不增加独立启停配置，具体 Sell 状态规则查询《C1 Sell 多国家支持迭代 PRD v1.1》。

## 四、法律文件、FAQ 与社媒账号

- 法律文件按“国家 + 文件类型 + 法务语言”维护；文件类型由开发预置，运营只能上传富文本新版本、下载当前版本和历史版本，不能在线编辑正文。
- FAQ 按国家维护英语富文本；上传后解析为问题和答案列表，支持覆盖或追加，并保留排序、启用和首页精选状态。
- 社媒平台固定为 Facebook、TikTok、Instagram、YouTube；每个平台按国家维护 URL。合法 URL 才展示，URL 为空则隐藏，不跨国家回退。
- 法律文件和 FAQ 中的外部 HTTPS 链接、站内相对路径和同页锚点按 v0.7 的安全清洗、校验和 locale 处理规则执行。

## 五、Contact Us 国家规则

- 邮箱地址不按国家变化；`BUY` 发送至 `service@looply.com`，`SELL` 发送至 `sell@looply.com`。
- 每次提交由服务端固定携带 `country_code`、页面 `language`、`inquiry_type`、UTC `submitted_at` 和唯一 `contact_request_id`。
- 邮件标题为 `Looply Contact Us | {submitted_at_utc} | {full_name} | {country_code}`，姓名中的换行符和 `|` 由服务端清理。
- 邮件正文展示国家、语言、咨询类型、Request ID、提交时间和用户原始输入。
- `SELL` 提交时服务端再次校验当前国家的 C2 和 C1 Sell 状态；校验失败时拒绝发送并保留用户输入，不自动改成普通咨询。
- 国家上下文缺失时阻止提交，不默认使用美国；发送失败时保留输入并允许使用同一 Request ID 重试。
- 仅保存最小发送记录，不在普通技术日志中保存姓名、邮箱和留言正文。

## 六、Demo 与验收

- 迭代 Demo 使用 CMS 统一配置入口 v80 的 Footer 页面作为交互基线，文档中心副本命名为 `Footer 多国家配置迭代 Demo v1.0`，打开后直接定位 `#/footer`。
- 验收覆盖国家切换、法律文件版本上传/下载、FAQ 解析与首页精选、社媒 URL 为空隐藏、Sell 关闭时 Footer 内容隐藏，以及 Contact Us 邮件标题追加国家代码。

## 七、关联文档

- 全量规则：[Footer 与关联页面 PRD v0.7](./looply-Footer-PRD-v0.7.md)
- C1 Sell 国家开关：[C1 Sell 多国家支持迭代 PRD v1.1](../../docs-C1-Sell/PRD/looply-C1-Sell-多国家支持-迭代PRD-v1.1.md)
- 后台原型基线：`looply-CMS统一配置入口-antd-原型-v80.html#/footer`
