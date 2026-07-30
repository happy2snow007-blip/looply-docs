# Looply Contact Us PRD v0.2

> 文档状态：产品已确认
> 版本日期：2026-07-30
> 适用终端：PC Web、Mobile Web / App
> 页面参考：[Looply Contact Us](https://looply.com/pages/contact)
> UI 设计文件：[Looply v1.0](https://www.figma.com/design/rLK7XCdVvYqEHQHd7WjOkk/Looply-v1.0?t=VQDfvElDOm7kMhSj-0)
> Mobile 状态稿：[Looply v1.0 · node 6772:3636](https://www.figma.com/design/rLK7XCdVvYqEHQHd7WjOkk/Looply-v1.0?node-id=6772-3636&t=pVFMkiNnle3oB3B1-0)

## 一、概述

### 1.1 背景与目标

Contact Us 为用户提供统一的客服联系入口。用户可填写姓名、邮箱和留言并提交咨询，也可查看 Looply 客服邮箱和响应时效。

当前版本目标：

- PC Web 与 Mobile 提供一致的联系内容和提交规则；
- 用户无需登录即可提交咨询；
- 对提交中、成功和失败结果提供明确反馈。

### 1.2 当前版本边界

当前版本仅包含联系表单、客服联系信息及提交反馈，不接入 hCaptcha、Google reCAPTCHA 或其他 CAPTCHA。咨询记录以发往 `service@looply.com` 的邮件为唯一业务记录，不建立独立的 Contact Us 业务记录或用户侧历史咨询记录。咨询分类、订单号、附件上传和在线聊天不属于当前版本。

### 1.3 用户角色

游客与登录用户均可访问并使用 Contact Us，页面内容和提交能力一致。

### 1.4 核心场景

- 用户咨询订单、退货、商品或平台服务问题；
- 用户通过表单向 Looply 客服提交留言；
- 用户查看客服邮箱和响应时效。

### 1.5 全局页面流转

- PC Web：首页 Footer → Contact Us
- Mobile：个人中心（游客态 / 登录态）→ Contact Us
- Contact Us → 系统邮件应用（点击客服邮箱）

### 1.6 术语说明

| 术语 | 说明 |
|---|---|
| Email Response Time | 客服对用户咨询的预计邮件回复时效 |

### 1.7 多语言与多国家策略

当前版本页面文案使用英文。页面标题、字段标签、按钮、校验提示、提交结果和客服信息标签均属于静态 UI 文案，通过稳定的 message key 管理，不进入翻译中心业务资源卡片。用户填写的 Full Name、Email 和 Message 属于用户原始输入，不翻译。

法律文件和市场版本按市场配置选择，不在前端写死单一国家版本。每个 Looply 自有法律文件至少维护以下元数据：法律文件类型、适用市场 / 国家、语言、版本号、生效日期和审核状态。Contact Us 页面及公共 Footer 展示的法律链接必须指向当前市场已批准且处于生效状态的版本。

香港市场法律文件适配属于后续阶段，本期不新增香港市场的具体法律文本、语言版本或市场映射。后续阶段接入香港市场时，必须由法务确认适用范围、语言、版本号、生效日期和链接；在确认前，不将其他国家版本标记为香港适用版本。

当前版本不在 PRD 中写入具体法律条文、法定保存期限或跨境传输结论；这些内容以法务批准的市场版本为准。

## 二、需求详细描述

### 2.1 Contact Us 页面

#### 2.1.1 功能描述与前置条件

用户进入 Contact Us 后，可查看联系信息并填写表单。页面不要求登录。登录用户进入页面时，表单读取账户姓名和邮箱作为初始值；游客不读取账户信息。

#### 2.1.2 页面布局

| 终端 | 页面框架 | 内容顺序 |
|---|---|---|
| PC Web | 使用 PC Web 公共 Header 与 Footer；展示形式以 Figma《Looply v1.0》为准 | 页面标题与引导语 → 联系表单 → Email → Email Response Time |
| Mobile Web / App | 游客态和登录态的个人中心均展示 Contact Us 入口；页面使用 Mobile 公共页面框架，顶部提供返回操作；展示形式以 Figma 指定节点为准 | 页面标题与引导语 → 联系表单 → Email → Email Response Time |

Mobile 内容按单列纵向排列；PC 与 Mobile 使用相同字段、联系信息和提交规则。

#### 2.1.3 页面元素

Mobile 个人中心的 Contact Us 入口在游客态与登录态均展示。游客点击后直接进入页面，不触发登录或注册流程。

| 区域 | 元素 | 英文文案 / 内容 | 交互 |
|---|---|---|---|
| 页面标题 | 标题 | Contact us | 无 |
| 联系表单 | 姓名 | Full Name | 单行输入 |
| 联系表单 | 邮箱 | Email | 邮箱输入 |
| 联系表单 | 留言 | Message | 多行输入 |
| 联系表单 | 提交按钮 | Send | 提交表单 |
| 联系信息 | 引导语 | If you have any questions about your order, returns, products, or our services, please contact us using the information below. | 无 |
| 联系信息 | Email | service@looply.com | 点击后调用系统邮件应用 |
| 联系信息 | Email Response Time | We generally respond to customer inquiries within 1–2 business days. | 无 |

#### 2.1.4 表单字段与校验

| 字段 | 必填 | 长度 / 格式 | 校验时机 | 错误反馈 |
|---|---|---|---|---|
| Full Name | 是 | 去除首尾空格后 1–100 个字符 | 失焦、点击 Send | 为空提示 `Enter your full name.`；超长提示 `Full name must be 100 characters or fewer.` |
| Email | 是 | 去除首尾空格后符合基础邮箱格式，最多 254 个字符 | 失焦、点击 Send | 为空提示 `Enter your email.`；格式错误提示 `Incorrect email` |
| Message | 是 | 去除首尾空格后 1–2,000 个字符 | 失焦、点击 Send | 为空提示 `Enter your message.`；超长提示 `Message must be 2,000 characters or fewer.` |

规则：

- 登录用户进入页面时，Full Name 和 Email 自动带入账户中的姓名和邮箱；账户中任一字段为空时，对应输入框保持空白；
- 游客进入页面时，Full Name、Email 和 Message 均为空；
- 登录用户可修改自动带入的 Full Name 和 Email；修改值仅用于本次 Contact Us 提交和客服回复，不更新账户资料；
- 字段错误显示在对应字段附近；
- 任一字段未通过校验时，不提交表单；
- 用户修改错误字段后再次失焦或提交时重新校验；
- 不自动翻译或改写用户输入内容。

#### 2.1.5 页面状态

| 状态 | 触发条件 | 页面表现 | 可用操作 |
|---|---|---|---|
| 默认态 | 页面正常打开 | 游客三个字段为空；登录用户自动带入 Full Name 和 Email，Message 为空；同时展示完整联系信息 | 填写、提交、点击客服邮箱 |
| 字段错误态 | 输入未通过校验 | 对应字段显示错误提示，保留其他已填内容 | 修改后重新提交 |
| 提交中 | 字段校验通过，正在提交 | Send 置灰不可点击，全部字段保留并暂不可再次提交 | 等待提交结果 |
| 提交成功 | 邮件服务确认已受理发往 `service@looply.com` 的邮件 | 页面内显示成功提示；游客清空三个字段，登录用户清空 Message 并将 Full Name、Email 恢复为账户初始值 | 可重新填写新咨询 |
| 提交失败 | 网络、邮件服务或系统异常 | 页面内显示失败提示，保留三个字段内容 | 点击 Send 重试 |
| 离开确认 | 当前字段值与页面初始值不同，用户点击页面返回或发起站内跳转 | 显示离开确认弹窗 | 留在页面或确认离开 |

成功提示：`Thanks for contacting us. We’ll get back to you as soon as possible.`

提交失败提示：`Submit failed, please try again.`

离开确认弹窗：

- 标题：`Leave without sending?`
- 正文：`Your message hasn’t been sent. If you leave, your changes will be lost.`
- 次操作：`Stay`
- 主操作：`Leave`

#### 2.1.6 操作流程

1. 用户从对应终端入口进入 Contact Us。
2. 用户填写 Full Name、Email 和 Message。
3. 用户点击 Send，系统校验三个字段。
4. 校验失败时，系统显示字段错误且不提交。
5. 校验通过后，由 Looply 服务端将 Full Name、Email、Message 发送至 `service@looply.com`。
6. 邮件服务确认已受理发送请求后，显示成功提示并清空表单。
7. 提交失败时，保留用户输入并允许重试。

提交成功后，本流程以页面内成功提示结束。客服后续从 `service@looply.com` 人工回复用户填写的 Email。

Looply 服务端不将 Full Name、Email 或 Message 写入独立的 Contact Us 业务存储。邮件为本期唯一业务记录。

离开页面流程：

1. 页面以首次展示时的三个字段值作为初始值；游客初始值均为空，登录用户的 Full Name 和 Email 初始值为账户带入值。
2. 当前任一字段值与对应初始值不同时，页面进入“有未提交修改”状态。
3. 用户点击页面返回或发起站内跳转时，显示离开确认弹窗。
4. 点击 Stay，关闭弹窗并保留全部内容；点击 Leave，清空本次内容并继续原离开动作。
5. 提交成功并重置字段后，页面退出“有未提交修改”状态，再次离开时不提示。
6. 关闭浏览器、App 被系统终止或跨设备访问时不保存、不恢复草稿。

#### 2.1.7 异常处理

| 异常 | 处理规则 |
|---|---|
| 页面公共框架加载失败 | 使用公共页面错误规则处理 |
| 联系表单局部加载失败 | 联系信息继续展示；表单区域显示失败提示和 Retry |
| 联系信息局部加载失败 | 表单继续可用；Email 与 Email Response Time 区域显示失败提示和 Retry |
| 登录用户账户信息读取失败 | 页面继续展示；Full Name 和 Email 保持空白，由用户手动填写 |
| 网络中断 | 保留全部输入，显示提交失败提示 |
| 邮件服务拒绝或超时 | 不显示成功提示；保留输入并允许重试 |
| 重复点击 Send | 提交中按钮不可重复触发，不创建重复请求 |
| 用户主动返回或站内跳转 | 有未提交修改时显示离开确认；确认离开后不保存表单内容 |
| 浏览器关闭、App 被系统终止或跨设备访问 | 不保存、不恢复未提交表单内容 |

#### 2.1.8 UI 关联

| 页面 / 状态 | PC Web | Mobile Web / App |
|---|---|---|
| Contact Us 默认态 | Figma《Looply v1.0》 | Figma node 6772:3636 |
| 字段错误态 | Figma《Looply v1.0》 | Figma node 6772:3636 |
| 提交中 | Figma《Looply v1.0》；Send 置灰 | Figma node 6772:3636；Send 置灰 |
| 提交成功 | Figma《Looply v1.0》 | Figma node 6772:3636 |
| 提交失败 | Figma《Looply v1.0》 | Figma node 6772:3636 |
| 离开确认 | 按本 PRD 弹窗文案与触发规则补齐 | 按本 PRD 弹窗文案与触发规则补齐 |

## 三、依赖与风险

| 依赖 / 风险 | 关键要求 |
|---|---|
| 邮件服务 | Contact Us 邮件由 Looply 服务端发送至 `service@looply.com`；邮件为本期唯一业务记录；用户浏览器不得直接发送邮件；仅在邮件服务确认已受理发送请求后向用户显示成功提示；客服后续从该邮箱人工回复用户 |
| 用户账户信息 | 登录用户进入页面时提供账户姓名和邮箱作为表单初始值；读取失败时表单降级为空白输入，不阻塞提交 |
| 公共页面框架 | PC 使用网站公共 Header / Footer；Mobile 在游客态和登录态的个人中心均展示入口，并使用公共返回规则 |
| 外部邮件能力 | 调用失败不影响页面其他能力 |
| 客服信息准确性 | 客服邮箱和响应时效上线前由客服与运营复核 |
| 隐私与数据处理 | 表单包含个人信息和用户留言；不建立独立 Contact Us 业务记录；必要技术日志不得记录 Full Name、Email 或 Message 原文；邮件的访问、保存和删除规则需与 Looply Privacy Policy 及客服邮箱管理规则一致 |
| 法律文件版本与市场配置 | 后续多市场阶段由法务为各市场提供已批准且生效的 Privacy Policy、Terms of Service 及适用语言版本；系统按市场读取版本、语言、生效日期和审核状态，缺少有效映射时阻止该市场上线，不使用未经确认的回退版本 |
| 香港市场 | 属于后续阶段，本期不接入香港市场法律文件映射；后续阶段接入前完成法务确认，并与 Contact Us、公共 Footer 和其他入口共用同一市场配置 |

## 四、版本规划

### 4.1 当前版本 v0.2

- PC Footer 与 Mobile 个人中心入口；
- Full Name、Email、Message 三字段表单；
- 提交中、成功、失败和重试；
- 客服邮箱和响应时效。

### 4.2 后续迭代方向

后续是否增加咨询分类、订单号、附件、在线聊天或咨询记录，应基于客服量级与处理效率另行立项，不属于当前版本。

## 五、数据与埋点

当前版本记录以下产品事件，不在埋点中记录 Full Name、Email 或 Message 原文：

| 事件 | 触发时机 | 非敏感属性 |
|---|---|---|
| `contact_us_view` | Contact Us 页面成功展示 | terminal、entry_source、login_status |
| `contact_us_submit_click` | 用户点击 Send | terminal、login_status |
| `contact_us_validation_failed` | 字段校验失败 | terminal、invalid_field |
| `contact_us_submit_result` | 提交结束 | terminal、result、failure_type |
| `contact_us_contact_click` | 点击客服邮箱 | terminal、contact_type |

枚举定义：

| 枚举字段 | 枚举值 | 含义 | 触发时机 / 适用场景 |
|---|---|---|---|
| terminal | `pc_web` | PC Web | PC 页面事件 |
| terminal | `mobile_web` | Mobile Web | Mobile Web 页面事件 |
| terminal | `app` | App | App 页面事件 |
| entry_source | `footer` | PC Footer | PC 入口 |
| entry_source | `me` | 个人中心 | Mobile 入口 |
| login_status | `guest` | 游客 | 未登录访问 |
| login_status | `logged_in` | 登录用户 | 已登录访问 |
| invalid_field | `full_name` | 姓名字段错误 | 字段校验失败 |
| invalid_field | `email` | 邮箱字段错误 | 字段校验失败 |
| invalid_field | `message` | 留言字段错误 | 字段校验失败 |
| result | `success` | 提交成功 | 邮件服务确认已受理发送请求 |
| result | `failed` | 提交失败 | 未确认成功 |
| failure_type | `network` | 网络异常 | 网络不可用或中断 |
| failure_type | `receiver` | 邮件服务异常 | 邮件服务拒绝、失败或超时 |
| failure_type | `unknown` | 未分类异常 | 无法归入其他类型 |
| contact_type | `email` | 客服邮箱 | 点击邮箱 |

## 六、权限与角色矩阵

| 能力 | 游客 | 登录用户 |
|---|---|---|
| 查看页面 | 支持 | 支持 |
| 查看联系信息 | 支持 | 支持 |
| 提交联系表单 | 支持 | 支持 |

## 七、附录

### 7.1 输入源与覆盖差异

| 输入源 | 覆盖情况 | 本 PRD 处理 |
|---|---|---|
| Figma《Looply v1.0》 | 已提供设计文件及 Mobile Contact Us 状态节点 | 作为当前 UI 展示与状态文案基线 |
| Looply 现有 PC 页面 | 包含历史页面结构、字段及联系信息 | 仅作为早期输入，不覆盖当前 Figma 设计 |
| PC 页面入口 | 已确认 | 首页 Footer → Contact Us |
| Mobile 页面入口 | 已确认 | 游客态和登录态的个人中心均展示 Contact Us；进入时不要求登录 |
| Mobile 独立设计稿 | 已提供 | Figma node 6772:3636 覆盖默认、邮箱校验错误、填写完成、提交成功和提交失败 |
| ER 图 | 本页面无专项输入源 | 当前版本不建立独立 Contact Us 业务实体；服务端邮件发送方式由技术方案定义 |
| 系统流程图 | 本页面无专项输入源 | 操作流程已在 2.1.6 闭合 |

### 7.2 字段映射

| 字段 / 元素 | PRD 定义 | Figma《Looply v1.0》 | 差异 |
|---|---|---|---|
| Full Name | 单行必填；登录用户自动带入账户姓名且可修改 | 已展示 | PRD 补充初始值和校验规则 |
| Email | 邮箱必填；登录用户自动带入账户邮箱且可修改 | 已展示邮箱校验错误态 | PRD 补充初始值和账户数据隔离规则 |
| Message | 多行必填 | 已展示 | PRD 补充校验规则 |
| Send | 提交按钮；提交中置灰 | 已展示默认与置灰状态 | PRD 补充防重复提交规则 |
| 客服联系信息 | Email、Email Response Time | 已展示 | 一致 |
| 提交结果 | 成功与失败页面内提示 | 已展示 | 一致 |
| Looply 法律文件链接 | 按当前市场展示已批准生效版本 | 未在 Contact Us 节点展示 | 多市场版本映射属于后续阶段；本期不新增香港市场链接 |
