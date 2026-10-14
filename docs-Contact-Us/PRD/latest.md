# Looply Contact Us PRD v0.4

> 文档状态：产品已确认
> 版本日期：2026-10-14
> 适用终端：PC Web、Mobile Web / App

## 一、范围与入口

Contact Us 为游客和登录用户提供咨询表单与联系邮箱。PC 从 Footer 进入，Mobile 从个人中心进入；访问和提交均无需登录。

页面不接入 CAPTCHA。咨询邮件为业务记录；不建立独立的 Contact Us 业务记录或用户侧咨询历史。必要技术日志和埋点不得记录姓名、邮箱或留言原文。

## 二、页面展示

PC 保留当前左右结构：左侧地址与邮箱卡片，右侧联系表单。邮箱卡片标题沿用现有 `Email`，按第三章顺序纵向展示，每项标题一行、邮箱一行；点击邮箱调用对应 `mailto:`。Mobile 使用单列布局，分类顺序和业务规则与 PC 一致。

页面标题为 `Contact Us`。顶部说明保持现状：`If you need any help, please contact us below. We usually respond within 1–2 business days.` 地址、地图及其他公共页面内容沿用现有配置，本次不调整。

## 三、联系原因与收件邮箱

下拉字段标签及占位文案均为 `What can we help you with?`。以下表格定义邮箱标题下的分类顺序、下拉选项和收件邮箱，是完整分发规则的唯一位置。

| 顺序 | 邮箱分类 / 下拉选项 | 收件邮箱 | 适用咨询 |
|---|---|---|---|
| 1 | Shopping Inquiries | service@looply.com | 购物、订单、退货及买家服务 |
| 2 | Selling Inquiries | sell@looply.com | 向 Looply 出售商品 |
| 3 | Social Collaborations | influencer@looply.com | 社媒达人、博主及内容合作 |
| 4 | Corporate Partnerships | partnerships@looply.com | 企业、品牌商务合作 |

`Selling Inquiries` 及对应邮箱仅在当前国家 `C2 已启用且 Sell 已开放` 时展示并允许提交；其他三类不受 Sell 开关影响。服务端提交时再次核验国家 Sell 状态。用户已选出售咨询后，若国家切换或 Sell 状态变化使其不可用，取消该选择，保留其他输入，要求重新选择可用原因；不得自动改投其他邮箱。

## 四、表单与校验

字段顺序为联系原因、Full Name、Email、Message、Send。

| 字段 | 必填 | 初始值及校验 | 错误反馈 |
|---|---|---|---|
| 联系原因 | 是 | 初始未选择；提交时必须属于当前国家可用选项 | `Please select a topic.` |
| Full Name | 是 | 去除首尾空格后 1–100 字符；游客为空，登录用户带入账户姓名 | 空值：`Enter your full name.`；超长：`Full name must be 100 characters or fewer.` |
| Email | 是 | 去除首尾空格后符合基础邮箱格式，最多 254 字符；游客为空，登录用户带入账户邮箱 | 空值：`Enter your email.`；格式错误：`Incorrect email` |
| Message | 是 | 初始为空；去除首尾空格后 1–2,000 字符 | 空值：`Enter your message.`；超长：`Message must be 2,000 characters or fewer.` |

姓名、邮箱、留言在失焦及点击 Send 时校验，错误显示在对应字段附近；任一字段未通过时阻止提交。登录用户修改姓名、邮箱仅用于本次咨询，不修改账户资料。账户资料读取失败时保持空白，允许手动输入。

输入框占位分别为 `Enter your name`、`Enter your email`、`Enter your message`。用户原始输入不自动翻译或改写。

## 五、提交与邮件规则

1. 用户选择联系原因并填写姓名、邮箱、留言，点击 `Send`。
2. 服务端校验分类及国家适用条件，根据第三章固定映射发送到对应邮箱；不得接收客户端自行指定的任意收件地址。
3. 邮件标题沿用 `Looply Contact Us - {submission time} - {Full Name}`；正文包含所选联系原因、Full Name、Email 和 Message。用户填写的 Email 作为回复地址。
4. 邮件服务确认已受理发送请求后，显示成功；接收团队后续回复用户邮箱。

| 状态 | 展示与操作 |
|---|---|
| 默认 | 展示当前国家可用分类和邮箱；联系原因未选择，姓名与邮箱按第四章带入 |
| 提交中 | Send 置灰，禁止重复提交；保留全部字段 |
| 成功 | 留在当前页面位置；清空联系原因、姓名、邮箱、留言；展示成功 Toast 4 秒 |
| 失败 | 网络、邮件服务拒绝、超时或系统异常均显示失败；保留分类与输入，允许重试；分类失效按第三章处理 |

成功文案：`Thanks for contacting us. We’ll get back to you as soon as possible.`

失败文案：`Submit failed, please try again.`

页面以首次显示的四个字段值作为初始值；任一字段变化后，用户返回或发起站内跳转时显示离开确认：标题 `Leave without sending?`，正文 `Your message hasn’t been sent. If you leave, your changes will be lost.`，操作 `Stay` / `Leave`。Stay 保留内容，Leave 放弃内容并继续离开。提交成功清空后，以空值作为新的初始值。关闭浏览器、App 被终止或跨设备访问不保存或恢复草稿。

## 六、异常与依赖

| 场景 / 依赖 | 处理要求 |
|---|---|
| 联系表单局部加载失败 | 联系信息继续展示，表单区域提示失败并提供 Retry |
| 联系信息局部加载失败 | 表单继续可用，联系信息区域提示失败并提供 Retry |
| 页面公共框架加载失败 | 使用公共页面错误规则 |
| 邮件服务 | 支持第三章四个收件邮箱及用户回复地址；未确认受理时不得显示成功 |
| 国家配置 | 提供当前国家 C2 与 Sell 状态；前台展示及提交校验使用一致条件 |
| 公共法律文件 | Contact Us 与 Footer 共用当前国家、语言对应的已批准生效法律文件映射 |

## 七、多语言与数据采集

页面标题、标签、分类名称、占位、按钮和提示属于静态 UI 文案，进入 message package；邮箱地址及用户输入不翻译。新增静态文案标识：`contact.topic.shopping`、`contact.topic.selling`、`contact.topic.social_collaborations`、`contact.topic.corporate_partnerships`、`contact.topic.required`，英文分别对应第二至四章文案。

数据采集沿用《数据采集与埋点产品需求》的 Contact Us 表单提交和邮箱点击规则，不新增另一套事件；分类扩展不改变成功、校验失败和提交失败的业务含义，不采集个人信息和留言原文。

## 八、UI 与关联文档

- 本次页面结构和联系原因输入以用户 2026-10-14 提供的 PC 页面、下拉截图及本次确认的四分类调整为输入。
- 历史 Figma：[Looply v1.0](https://www.figma.com/design/rLK7XCdVvYqEHQHd7WjOkk/Looply-v1.0)，Mobile 历史节点 `6772:3636`；历史稿不覆盖本次已确认变更。
- C1 Sell 国家状态由 C1 Sell 全量 PRD 定义；本文第三章定义该状态在 Contact Us 中的展示和提交结果。
