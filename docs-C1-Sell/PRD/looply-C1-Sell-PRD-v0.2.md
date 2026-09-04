# Looply C1 Sell PRD（详细讨论稿）

版本：v0.2  日期：2026-09-02  状态：评审基线（基于 v2.6.4 Demo 与 Figma UI）

## 一、概述

### 1.1 目标与范围

C1 Sell 让用户通过 In-Home Appointment、Visit Looply、Ship to Us 三种方式出售符合条件的品牌商品。本版本覆盖 C 端 PC / Mobile 入口与交互、Service Area 初步查询、上门预约提交、确认邮件，以及 C1 独立运营后台的业务边界。

Buy 与 Sell 共用账户、公共法律入口和 Contact Us；Sell 交易数据、服务配置与预约运营模块独立管理。

### 1.2 端差异原则

| 端 | 入口 | 主要交互 |
|---|---|---|
| PC Web | 顶部主导航 Sell、Footer Sell 组中的 `Sell with Looply` | 页面级导航；预约表单在页面主体或弹层中展开。Footer `Contact Us` 属于公共 Support 入口，不计入 C1 Sell 入口 |
| Mobile Web / App | 底部 Tab Sell、Me 中的 Sell / Support 入口 | 单列页面、顶部返回、底部固定导航；表单按步骤或纵向展开 |

具体视觉以 Figma《LOOPLY 草稿》对应页面为准；点击与跳转以 `LOOPLY_SELL_PAGE_INTEGRATION_DEMO_v2.6.4_2026-08-31` 为准。

### 1.3 PC 全局导航（新版 UI 基线）

PC Header 按新版 Figma UI 组织为上下两排：第一排展示 LOOPLY、外露搜索框、语言 / 国家入口、Sell 入口及账户相关操作；第二排展示 `New Arrivals / Designers / Bags / Jewelry / Accessories / Watches / Sale` 等商品 / 品牌导航。语言 / 国家入口按 Figma 调整位置，点击后展开可用语言和市场选项；点击 `Sell` 进入 C1 Sell 首页。Footer `Contact Us` 属于公共 Support 入口，不计入 C1 Sell 入口。

Search、Account、Favorites、Bag 保持全站公共交互，Sell 页面不重新定义其业务行为。

### 1.4 角色

- C 端访客 / 登录用户：浏览、查询、提交预约或联系咨询。
- C1 运营人员（角色名称与权限待确认）：维护服务覆盖配置、查看和处理预约。

## 二、服务覆盖与配置维护

### 2.1 配置对象

运营后台分别维护 In-Home Service 支持的 ZIP Code 配置，以及可回收品类与品类-品牌映射配置。ZIP 配置由运营新增、编辑、启用或停用，前台 Service Area 和预约流程只读取当前生效的 ZIP 配置判断用户所在区域是否支持上门；品牌与品类配置仅用于决定可提交回收的商品范围。两者独立判断，不要求 ZIP、品牌、品类三者组合命中。首页 `What We Buy` 横向滚动区使用固定的精选品牌文案，不读取后台；完整 Accepted Brands 页面读取后台生效配置。

### 2.2 配置状态枚举

| 枚举值 | 含义 | 触发时机 | 记录内容 |
|---|---|---|---|
| `active` | 生效 | 运营发布或重新启用配置 | 生效人、时间 |
| `inactive` | 停用 | 运营主动停用配置 | 停用人、时间、原因 |

后台编辑中的未保存内容不进入 C 端生效配置；如设置有效期，到期后按停用处理并保留历史记录。配置变更保留历史版本；已有预约使用提交时的配置快照，不因后续停用而改变。

## 三、确认邮件与运营后台

### 3.1 确认邮件

预约创建成功后由服务端发送确认邮件。邮件至少包含预约编号、提交时间、服务方式、用户填写的地址摘要、品牌 / 品类摘要、后续由客户代表确认的说明和 Contact Us 入口。邮件发送失败不回滚预约，后台标记发送失败并允许运营重发；用户页面显示预约已提交但邮件可能延迟的提示。

发件地址、模板、语言、重发权限、邮件服务商和数据保留规则待确认。

### 3.2 C1 运营后台

入口：`https://ops.looply.com/`。C1 Sell 作为独立模块展示，使用独立登录会话；未通过 C1 登录不得查看预约信息。C2 菜单和 C2 权限不自动继承。

预约列表字段：预约编号、提交时间、状态、用户姓名、邮箱、电话、服务地址、ZIP、品牌、品类、服务方式、预约时间、邮件状态、负责人、更新时间。

预约状态枚举：`submitted`（已提交）、`email_pending`（邮件待发送）、`email_failed`（邮件失败）、`reviewing`（运营审核中）、`confirmed`（已确认）、`scheduled`（已安排）、`completed`（已完成）、`cancelled`（已取消）。每次状态变更记录操作人、时间和原因。

后台能力：筛选、查看详情、分配负责人、更新状态、重发确认邮件、记录备注。导出、批量操作和删除需单独授权，默认不开放。

## 四、法律文件与用户中心

公共法律文件由公共 Footer 与 Me 的 Legal 区统一入口：Terms of Service、Privacy Policy、Your Privacy Choices。

Sell 专属文件从 Sell 首页、预约流程和 Me / Sell 区进入：Seller Terms、Sales Agreement、Condition Guide、Seller FAQ、服务方式与邮寄规则。Buy 专属文件保留订单、退货、退款和物流政策。法律文件按市场、语言、版本、生效日期和审核状态配置；前端只展示有效版本。

用户中心 Me：Profile；Buy 区的 Orders、Favorites、Returns；Sell 区的 Selling Activity、Appointments / Shipments、Offers / Payments；Support 区的 Contact Us、FAQ；Legal 区的统一法律入口。具体字段和 UI 以 Figma 用户中心稿为准。

## 五、依赖、异常与埋点

依赖包括账户服务、服务配置、预约服务、邮件服务和 C1 独立登录。网络异常、非法输入、配置不存在、重复提交、邮件失败和并发状态更新均需保留用户输入或当前数据，并给出可恢复操作。权限分级、字段脱敏、审计和数据保留不在本版本实现范围内。

### 5.1 多语言规划

- 本版本所有新增静态 UI 文案（页面标题、按钮、表单标签、校验提示、结果状态、邮件提示）必须使用统一 message key，不在页面代码中散落硬编码。
- 当前 UI 基线为 `en-US`；语言切换入口沿用全站公共能力。新增 Sell 文案需预留翻译资源及缺失译文回退到英文的规则。
- 动态业务内容（品牌、品类、城市、FAQ、法律文件标题和正文）按翻译中心资源卡片管理；具体 `resourceType`、字段清单、支持语种和翻译负责人在开发前确认，不将其当作静态 UI 文案处理。
- 邮件语言跟随用户提交时的语言 / 市场；若暂不支持该语言，回退 `en-US`，并在预约记录中保存语言标识。

### 5.2 埋点规划

关键事件：`sell_view`、`sell_cta_click`、`service_area_check`、`service_area_result`、`appointment_start`、`appointment_step_view`、`appointment_submit`、`appointment_submit_result`、`confirmation_email_result`、`contact_us_submit`、`ops_appointment_view`、`ops_appointment_status_change`。

每个事件至少记录：事件时间、端（PC / Mobile）、页面路径、登录态、语言 / 市场、来源模块、结果状态和匿名 request / session ID。业务事件补充方式（In-Home / Visit / Ship）、ZIP 查询结果、品类 / 品牌是否已选、失败原因码等枚举字段。埋点不得记录姓名、邮箱、电话、完整地址、Message 原文、照片或其他可直接识别个人的信息；ZIP 仅记录脱敏或区间值。

## 六、版本规划与待确认

### 当前讨论稿 v0.2

完成 PC / Mobile 入口差异、Demo 交互基线、Figma UI 基线、ZIP 与品牌 / 品类配置方向、预约邮件、C1 独立运营后台、用户中心和法律文件整合框架。

### 待确认

- Figma 中未覆盖的预约字段和页面状态。
- ZIP 覆盖配置与品牌 / 品类配置的维护权限及发布流程。
- 邮件服务商、发件地址、模板和失败重发策略。
- C1 后台角色、MFA、字段脱敏、导出和保留期限。
- 用户中心 Sell 模块的具体页面与登录态差异。
- 各法律文件正式文本、适用市场和生效版本。
- 支持语种、翻译资源卡片标识、邮件语言回退规则及埋点数据字典 / 看板归属。

## 七、评审验收基线

- PC 与 Mobile 均可从对应入口进入 Sell；端内导航保持各自公共导航规则。
- Service Area 对有效 ZIP 返回覆盖或未覆盖结果；非法 ZIP、配置加载失败可恢复。
- 覆盖结果进入 In-Home Appointment；未覆盖结果进入 `Three Ways to Sell` 或 Contact Us。
- 预约成功后生成唯一预约记录，并向用户发送确认邮件；邮件失败不重复创建预约。
- C1 运营人员通过独立登录查看预约；无权限用户无法看到预约个人信息。
- ZIP、品牌、品类配置发布、停用和历史版本可追溯。
- 法律入口、Contact Us 和用户中心按 Buy / Sell 共用与专属边界展示。

## 八、逐页交互清单（PC）

本章以已确认的 PC Figma UI 页面为唯一展示与交互基线，按页面浏览顺序定义模块、文案、可点击元素及跳转结果。Demo 仅作为交互走查辅助，不作为页面设计或文案来源。

Figma 页面基线（文件 `LOOPLY 草稿`，C1 区域）：`PC-C1-3`（Sell 首页）、`PC-Accepted Brands`（收起 / 展开）、`PC-Condition Guidelines`、`PC-service-area-page`（默认）、`PC-service-area-page-输入`、`PC-service-area-page-错误提示`、`PC-Looply Seller Terms`、`PC-Looply Sales Agreement`、`PC-Contact Us -2`，以及预约流程的 `PC-sell-request-form-*` 各步骤和 `PC-sell-request-form-Request received` 成功页。以下页面、状态和按钮均以这些 Frame 的实际设计为准。

### 8.1 首页模块与文案

| 模块 | 展示文案 / 内容 | 可点击元素 | 点击结果 |
|---|---|---|---|
| 全局 Header（两排） | 第一排：LOOPLY、外露搜索框、语言 / 国家入口、Sell、Account、Favorites、Bag；第二排：New Arrivals、Designers、Bags、Jewelry、Accessories、Watches、Sale | 搜索框、语言 / 国家入口、Sell、Account、Favorites、Bag 及商品 / 品牌导航 | 点击 Sell 进入 C1 Sell 首页；语言 / 国家入口展开选项；其他操作沿用全站行为 |
| 游客 Hero | Sell 页面主标题、说明、`Sell Now`、`Explore your options` | Sell Now | 打开预约弹窗第 1 步 |
| 游客 Hero | 同上 | Explore your options | 滚动至 `Three Ways to Sell` |
| 登录态 Hero | `Welcome back, Julia` 及三种方式推荐卡 | 各方式 CTA | 打开预约弹窗并锁定对应方式 |
| Three Ways to Sell | `In-Home Appointment` / `Visit Looply` / `Ship to Us` 三个 Tab | Tab | 切换当前方式详情，不跳页 |
| 方式详情 | 方式标题、说明、`How It Works`、步骤、地点 / 服务区域 | `In-Home Service Area` | 打开 Service Area 弹窗 |
| 方式详情 | 方式步骤和说明 | 当前方式 CTA | 打开对应预约弹窗 |
| Advantages | Why sell with Looply、鉴定 / 透明 / 便捷等优势卡片 | 卡片 | 按 Figma 设计展示；无跳转时保持当前页面 |
| Brands | Accepted Brands / Categories 说明 | `View accepted brands` | 进入 `brands-and-categories.html` |
| FAQ | `More questions?` | `Read our FAQs` | 进入 `faq.html` |
| 底部吸底条 | `Ready when you are.`、`Sell Now` | Sell Now | 打开预约弹窗 |
| Footer | Sell、Accepted Brands、Service Area、Seller FAQ、Contact Us、法律链接 | 各链接 | 进入对应页面 |

### 8.2 预约弹窗：公共步骤

1. 用户点击 Sell Now 或方式 CTA，打开全屏 / 居中预约弹窗；背景页面不可操作。
2. 第 1 步填写用户信息：First Name、Last Name、Phone、Email，并显示登录用户自动带入值。
3. 第 2 步填写商品信息：Category、Brand、Item details / condition、Photos 或相关说明；品牌输入支持下拉搜索和多品牌 Chip 删除。
4. 第 3 步根据方式展示分支表单，并提供 Back / Continue / Submit。
5. 关闭按钮、遮罩点击和 Escape 关闭弹窗；有已填写内容时按本 PRD 的草稿保存与恢复规则处理。

### 8.3 第 3 步分支

| 方式 | 展示内容 | 交互 |
|---|---|---|
| In-Home Appointment | ZIP 输入 `Enter your ZIP code`、`Check Availability`；覆盖后展示 Street address、Apartment、City、ZIP、Preferred date；Seller Terms 说明 | ZIP 未通过前地址字段不可用；覆盖后解锁地址字段；提交进入成功页 |
| In-Home 未覆盖 | `Recommended Options for Your Area`、Ship to Us、Visit Looply、`Still prefer an In-Home Appointment? Contact us.` | 选择其他方式后切换分支并保留已填信息；Contact us → `contact-us.html` |
| Visit Looply | 办公地点、预约时间 / 说明 | 选择时间并提交 |
| Ship to Us | Street address、Apartment、City、State、ZIP、Mail-in Terms / Brands & Categories / Condition Guide 勾选说明 | 所有必填项和协议勾选通过后提交 |

### 8.4 查询与提交状态

| 操作 | 状态 / 文案 | 结果 |
|---|---|---|
| ZIP 查询 | `In-Home service is available in your area.` | 展示地址字段并允许继续 |
| ZIP 查询 | `In-Home service is not currently available for {ZIP}.` | 展示 Ship to Us / Visit Looply 推荐 |
| ZIP 非法 | 沿用现有地址页 ZIP 校验错误提示 | 保留输入，阻止继续；C1 不新增独立 ZIP 格式校验 |
| 表单提交 | 提交中 | 按钮置灰，防止重复提交 |
| 提交成功 | 成功标记、预约摘要、后续联系说明 | 发送确认邮件并生成运营后台预约记录 |
| 提交失败 | 页面错误提示 | 保留输入，允许重试 |

### 8.5 次级页面

#### Figma Frame 逐页交互基线

| Figma Frame | 页面 / 状态 | 页面核心内容 | 可点击交互与结果 |
|---|---|---|---|
| `PC-C1-3` | Sell 首页 | Header、Hero、Why Looply、What We Buy、Accepted Brands、Selling Tips、吸底 CTA、Footer | `Sell Now` 进入预约；`Explore your options` 定位 Three Ways；品牌、FAQ、Service Area 等链接进入对应页面；Header 公共图标沿用全站行为 |
| `PC-Accepted Brands` | 品牌页默认 | 品类分组、品牌列表、搜索 / 筛选 | 品类切换、品牌搜索、展开 / 收起；`Sell Now` 进入预约；返回回到来源页 |
| `PC-Accepted Brands-展开` | 品牌页展开 | 展开指定品类下的品牌明细 | 点击品类标题收起；点击 `Sell Now` 进入预约 |
| `PC-Accepted Brands-收起` | 品牌页收起 | 仅显示品类标题 / 摘要 | 点击品类标题展开 |
| `PC-Condition Guidelines` | 成色指南 | 可接受 / 不接受条件、附件和披露说明 | FAQ、Brands、Seller Terms 为内链；`Sell Now` 进入预约 |
| `PC-service-area-page` | Service Area 默认 | Greater Los Angeles 服务说明、ZIP 输入、城市列表 | 输入 ZIP 并点击 `Check Availability`；`Sell Now` 进入预约；`Contact Us` 进入联系页 |
| `PC-service-area-page-输入` | Service Area 输入 / 查询中 | ZIP 已输入，查询按钮和加载状态 | 查询完成后进入覆盖或未覆盖结果；非法输入在当前字段提示 |
| `PC-service-area-page-错误提示` | Service Area 查询错误 | 错误提示、重试入口 | `Retry` 重新查询；`Contact Us` 进入联系页 |
| `PC-Looply Seller Terms` | 卖家条款 | 条款正文和相关说明 | 返回来源页；Sales Agreement / Contact Us 为内链；`Sell Now` 进入预约 |
| `PC-Looply Sales Agreement` | 销售协议 | 协议正文和签署前说明 | 返回 Seller Terms；Contact Us 为内链 |
| `PC-Contact Us -2` | 联系我们 | Business Type（Sell / Buy）、Name、Email、Subject、Message | 切换业务类型；`Send Message` 复用公共校验并显示成功 / 失败状态 |
| `PC-sell-request-form-*` | 预约表单各步骤 | 进度条、用户信息、商品信息、服务方式分支、协议 | `Back` 返回上一步；`Continue` 校验后进入下一步；关闭按草稿规则处理 |
| `PC-sell-request-form-Request received` | 提交成功 | 成功标记、Request ID、Selling method、Total pieces、Preferred date、Location | 关闭返回来源页；确认邮件和后台记录由服务端异步处理 |

| 页面 | 页面文案 / 模块 | 可点击元素 | 结果 |
|---|---|---|---|
| Service Area | `In-Home Service Across Greater Los Angeles`、ZIP 查询、城市列表、免责声明、`Sell Now` | Check Availability、Sell Now、Contact Us | 查询状态；进入预约或 Contact Us |
| Accepted Brands | 品牌 / 品类列表、说明 | 返回、Sell Now、Contact Us、Footer 链接 | 返回来源或进入对应页面 |
| FAQ | Selling FAQ、折叠问答、法律提示 | 问题折叠、Brands & Categories、Condition Guide、Contact Us | 展开答案或页面跳转 |
| Condition Guide | 成色说明、可接受 / 不接受条件 | 返回、Brands、FAQ、Sell Now | 页面跳转 |
| Seller Terms | 卖家条款正文及适用说明 | 返回、Contact Us、Sell Now | 页面跳转 |
| Sales Agreement | 协议章节和非正式合同提示 | 返回、Seller Terms、Contact Us | 页面跳转 |
| Contact Us | 标题、Business Type（Sell / Buy）、Full Name、Email、Message、Send | 选择业务类型、提交 | Sell 提交至 `sell@looply.com`；Buy 提交至 `service@looply.com`；邮件标题为 `Looply Contact Us - {submission time} - {Full Name}` |

### 8.6 Mobile 端差异记录

- Header 主导航收缩，底部固定 `Home / Shop / Sell / Favorites / Me`。
- 首页三种方式采用横向滑动 Tab / 卡片；预约表单单列纵向排列。
- 预约弹窗占满视口，顶部提供关闭 / 返回；吸底 CTA 避让底部 Tab。
- Me 是 Mobile 的 Sell、Support、Legal 入口；PC 对应入口主要在 Header / Footer。

### 8.7 预约表单字段级定义

#### 公共表单校验复用原则

C1 Sell 预约和 Contact Us 表单复用 Looply 现有公共表单组件的校验、错误展示、提交中和防重复提交规则。C1 PRD 不重复定义公共组件已有的通用样式和提示机制；本 PRD 只补充 C1 特有的业务校验：ZIP Code 服务覆盖判断、品牌 / 品类联动、售卖方式分支必填项和协议确认。

公共规则基线：必填字段为空时阻止继续；Email 使用公共邮箱格式校验；Phone 使用美国 `+1` 后 10 位数字校验；ZIP Code 复用现有地址页校验；协议 Checkbox 未勾选时阻止提交；提交中按钮置灰并阻止重复提交；失败保留已填内容并允许重试。

#### Step 1 — Let’s start with you

| 字段 | 控件 | 必填 | 规则 / 交互 |
|---|---|---:|---|
| First name | 单行输入 | 是 | `given-name`；登录态预填 `Julia` |
| Last name | 单行输入 | 是 | `family-name`；登录态预填 `Seller` |
| Phone | 电话输入 + 固定 `+1` | 是 | 10 位数字；示例 `3105550123` |
| Email | 邮箱输入 | 是 | 基础邮箱格式；示例 `you@example.com` |
| Contact consent | Checkbox | 是 | 同意接收与卖出请求相关的电话、邮件和短信；展示资费、STOP 退订、非成交条件，并链接复用 C2 的 `Privacy Policy` 与 `Terms of Service` |

点击 `Continue`：校验失败时在当前步显示 `Please complete the required contact information and consent.` 并聚焦首个错误字段；成功后保存草稿并进入 Step 2。`Sign in.` 进入全站登录流程。

#### Step 2 — Tell us about your pieces

| 字段 | 控件 | 必填 | 规则 / 交互 |
|---|---|---:|---|
| Category | Handbags / Jewelry / Watches Checkbox | 是 | 支持多选，至少选择一项 |
| Brand | 搜索输入 + Add Brand | 是 | 支持多选；选择品类后按后台生效配置实时联想；未选择品类不联想；允许手动输入后台未配置品牌 |
| Quantity | 1–2 / 3–5 / 6–9 / 10+ Radio | 否 | 单选 |
| Notes | 多行输入 | 否 | Models、condition、repairs 或其他详情 |
| Photos | 多文件图片上传 | 否 | `image/*`；最多 10 张；展示文件名并在提交时上传 |

点击 `Back` 返回 Step 1 并保留已填值；点击 `Continue` 时校验品类和品牌，缺少任一必填项则显示 Toast `Please select at least one category and enter at least one brand to continue.`；校验通过后保存商品信息并进入 Step 3。照片最多上传 10 张，超出时提示 `You can upload up to 10 photos.`。

#### Step 3 — Find the Best Way to Sell

**In-Home Appointment**

| 字段 | 控件 | 必填 | 规则 / 交互 |
|---|---|---:|---|
| ZIP code | 数字输入 | 是 | 五位数字；点击 `Check Availability` 或 Enter 查询 |
| Street address | 单行输入 | 是 | ZIP 覆盖后解锁 |
| Apartment, suite, etc. | 单行输入 | 否 | ZIP 覆盖后解锁 |
| City | 单行输入 | 是 | ZIP 覆盖后解锁 |
| ZIP code（地址） | 只读输入 | 是 | 自动带入查询 ZIP |
| Preferred date | 日期输入 | 否 | ZIP 覆盖后解锁 |

ZIP 覆盖后展示 `Recommended for your area / In-Home Appointment / We come to your home at no cost.`，并以按钮展示 Visit Looply 和 Ship to Us 替代方式；点击替代方式可切换 Step 3 分支。ZIP 未覆盖后展示 `Recommended Options for Your Area`，推荐 Ship to Us 和 Visit Looply，并保留 `Still prefer an In-Home Appointment? Contact us.`。

**Visit Looply**

展示固定地点 `6300 Wilshire Blvd, Los Angeles, CA 90048`、`Appointment only.`、Preferred date（可选）和客户代表确认说明。

**Ship to Us**

| 字段 | 控件 | 必填 | 规则 / 交互 |
|---|---|---:|---|
| Street address | 单行输入 | 是 | 收件地址 |
| Apartment, suite, etc. | 单行输入 | 否 | 地址补充 |
| City | 单行输入 | 是 | 城市 |
| State | 下拉 | 是 | 美国州完整枚举 |
| ZIP code | 数字输入 | 是 | 五位邮编 |
| Terms acknowledgement | Checkbox | 是 | 同意 Mail-in Terms，确认商品属于 Brands & Categories，并确认 Condition Guide |

提交前校验当前分支必填项；失败显示 `Please complete the required details for this selling method.`，保留全部输入。成功后生成 Request ID、展示 Selling method / Total pieces / Preferred date / Location 摘要，提供 `Done` 关闭弹窗。

### 8.8 表单状态与恢复

- 弹窗打开时锁定背景滚动；关闭按钮、遮罩和 Escape 可关闭。
- 用户填写表单但未提交时，系统保存当前阶段草稿；用户下次在同一设备、同一浏览器打开 Sell 表单时，自动恢复已保存的联系人信息、商品信息、已选品牌 / 品类、售卖方式和已填写的分支字段，无需重复输入。
- 恢复草稿时，页面回到上次离开前的步骤；用户可以继续编辑、返回前一步或清空后重新填写。
- 提交成功后清除该草稿；关闭浏览器、清理站点数据或更换设备 / 浏览器时不保证恢复。
- 草稿只用于用户侧继续填写，不进入运营后台，不触发确认邮件，也不算正式预约记录。
- Step 3 返回时保留 ZIP 查询结果和已选方式；从未覆盖分支切换到替代方式后，可返回 Home 分支。
- 提交中按钮不可重复触发；成功页不再显示进度条。
- 成功页展示真实预约提交结果、Request ID 和后续联系说明。Request ID 按 `[METHOD]-[YYMMDD]-[LOCATION]-[RANDOM]` 生成：`IH` / `VL` / `ST` 分别对应三种方式；日期为正式提交日期；Location 为履约州缩写（Visit Looply 固定 `LA`，其余使用客户地址州缩写）；Random 为后台生成并校验唯一性的 4 位大写字母和数字。成功页的 Selling method、Total pieces 使用用户最终选择 / 填写的信息；Preferred date 未填写时隐藏该行。

## 九、评审前必须确认的产品决策

以下内容会改变实现或验收，需在评审会上明确结论后冻结：预约字段清单、ZIP 覆盖配置与品牌 / 品类配置的维护权限及发布流程、确认邮件模板与发件地址、C1 后台角色与脱敏范围、用户中心 Sell 页面、法律文件正式版本及适用市场。

## 十、业务整理文档对照补充

### 10.1 全站融入规则

- C1 Sell 是新版 looply.com 的第二条核心业务线，与 C2 共用账号体系和 Address；Sell 业务数据和运营模块独立。
- PC 顶部导航新增带底色的一级 `Sell`；Sell 页面沿用全站 Header / Footer。
- Mobile 底部 Tab 顺序为 `Home / Shop / Favorites / Sell / Me`；Mobile Header 不重复展示 Sell。
- Footer 新增 `Sell` 分组：`Sell with Looply / Accepted Brands / Service Area / Seller FAQ`。Seller Terms、Sales Agreement 归入 Policies。

### 10.2 Policies 信息架构

Policies 页面按以下分组展示，买家与卖家政策分开：

| 分组 | 页面 |
|---|---|
| Shopping Policies | Terms of Service、Shipping & Delivery、Returns & Refunds、Authenticity Guarantee、Accessibility Statement |
| Selling Policies | Seller Terms、Sales Agreement、Mail-in Terms、Payment Terms、In-Home Appointment Terms（页面清单待运营 / 法务确认） |
| Privacy & Data | Privacy Policy、Your Privacy Choices、Communication Consent、Identity and ownership verification notice |

Policies 页面只负责分组和跳转；各法律页面正文由法务批准版本提供。缺少有效市场版本时不展示为已生效文件。

### 10.3 Accepted Brands 页面

页面路径：`/en-US/sell/brands`（Demo 对应 `brands-and-categories.html`）。

- 分类：Handbags、Jewelry、Watches。
- 支持品牌名称和常见别名搜索。
- 结果显示品牌与可接受品类映射；无匹配时显示无结果提示并提供清空搜索。
- 支持回收的品类及各品类对应品牌均由运营后台配置；C 端只读取生效配置，不在页面或 PRD 内维护第二份品牌清单。
- 完整 FAQ、品类和品牌清单以业务整理文档为准：[Looply C1 Sell 业务融入新版 looply.com 需求文档](https://zhuanspirit.feishu.cn/docx/FhCvdYCxgoFRtCxekE6cdRFdnfg)。

### 10.4 Condition Guide 页面

页面路径：`/en-US/sell/condition-guide`（Demo 对应 `condition-guide.html`）。按 Handbags、Jewelry、Watches 说明成色标准、附件影响、维修 / 改动披露要求及清洁注意事项。该页从 Sell 首页、Seller FAQ 和商品条件说明内链进入，不作为 Footer 一级入口。

### 10.5 Service Area 页面

页面路径：`/en-US/sell/service-area`。展示 Greater Los Angeles（`Beverly Hills, Santa Monica, West Hollywood, Malibu, Culver City, Pasadena, Glendale, Burbank, Manhattan Beach, Long Beach, and surrounding communities.`）和 Orange County（`Irvine, Newport Beach, Laguna, Costa Mesa, Huntington Beach, Laguna Beach, Laguna Niguel, San Clemente and surrounding communities.`）的服务说明、ZIP Code 初步查询、覆盖结果、未覆盖时的替代售卖方式和 Contact Us。当前配置含 870 个候选 ZIP，是否可直接对客使用待确认。

Seller Agreement 正文以[业务提供的 Seller Agreement 文档](https://zhuanspirit.feishu.cn/docx/X2vjdYalQopAskxavSTcB4pAnR2?from=from_copylink)为准；PRD 仅定义入口、展示和跳转。

### 10.6 Seller FAQ 页面

页面路径：`/en-US/sell/faq`（Demo 对应 `faq.html`）。FAQ 按售卖方式、附件、报价依据、付款开始、邮寄流程、上门预约、品牌 / 品类、服务区域、身份与所有权检查组织；问答采用折叠交互，相关答案可内链至 Brands、Condition Guide、Service Area、Seller Terms 和 Contact Us。完整问题、答案和业务口径以[业务整理文档](https://zhuanspirit.feishu.cn/docx/FhCvdYCxgoFRtCxekE6cdRFdnfg)为准，PRD 不复制全文。

### 10.7 业务文档与 Demo 的差异

| 项目 | 业务整理文档 | Figma UI / PRD 处理 |
|---|---|---|
| Mobile Tab 顺序 | Home / Shop / Favorites / Sell / Me | Demo 当前顺序需按业务文档修正并在 UI 评审确认 |
| Policies 分组 | Shopping / Selling / Privacy & Data | PRD 已纳入信息架构；具体法律页待法务确认 |
| Accepted Brands | 支持分类与别名搜索 | Demo 已有品牌配置；页面搜索交互需在后续 Demo 走查中补全 |
| ZIP 数据 | 870 个候选 ZIP、246 段压缩范围 | Demo 使用 `service-zip-ranges.json` 初步判断 |
| 预约确认 | 生成 request state 并提示后续联系 / 邮件确认 | PRD 增加确认邮件与后台记录要求 |

## 十一、按页面顺序的 PC 评审稿

以下内容以用户从页面顶部向下浏览的顺序描述，展示和点击行为以已确认的 PC Figma UI 为准；Demo 仅用于交互演示参考。

### 11.1 Sell 首页首屏：Header + Hero + Why Looply

**页面定义**：用户进入 Sell 首页后首先看到的这一屏，对应 Figma 中的 PC-C1-3 首屏画面。该屏由全局 Header、Hero 主视觉和紧接其后的 Why Looply 四项优势组成。

**展示内容**：全局 Header、语言入口、商品导航、操作图标；Hero 主视觉和 Sell 价值主张；Why Looply 四项优势。

**文案**：`Sell with Looply`；`Sell from Home. Get Paid on the Spot.`；`We authenticate your pieces, make you an offer, and pay you in one visit. Fast and simple, so you have time for everything else.`；`Free In-Home Appointments · Visit Us · Ship to Us`。

**可点击与结果**：

| 元素 | 结果 |
|---|---|
| Logo | 返回 C2 首页 / 全站首页 |
| 语言 `🇺🇸 EN ▾` | 展开语言 / 市场选项；当前 Demo 仅展示外观 |
| Shop 导航 | 进入对应 C2 商品页面；具体页面由 C2 定义 |
| Search / Account / Favorites / Bag | 进入全站公共功能；Sell PRD 不重新定义 |
| `Sell Now` | 打开 Sell Request 弹窗 Step 1 |
| `Explore your options` | 滚动到 `Three Ways to Sell` |

首屏结束位置为 Why Looply 四项优势卡片底部；卡片当前为静态展示，不产生页面跳转。

### 11.2 Sell 首页第二屏：Three Ways to Sell

**标题文案**：`Three Ways to Sell`；`Choose how you’d like to sell.`

| Tab | 辅助文案 | 点击结果 |
|---|---|---|
| In-Home Appointment | `We come to you.`、`Most popular` | 切换本屏详情；显示服务区域入口 |
| Visit Looply | `Meet us at our office.` | 切换本屏详情；显示地点与流程 |
| Ship to Us | `Complimentary shipping across the U.S.` | 切换本屏详情；显示邮寄流程 |

详情区展示 `How It Works` 和步骤。In-Home 详情中的 `In-Home Service Area` 打开服务区域弹窗；方式 CTA 打开预约弹窗并预选对应方式。

### 11.3 Sell 首页第三屏：What We Buy

**文案**：`What We Buy`；`From icons to modern classics.`；`Explore accepted brands across handbags, jewelry and watches.`；`View All Brands & Categories`。

品牌横向展示 Hermès、Chanel、Cartier、Louis Vuitton、Van Cleef & Arpels、Christian Dior、Goyard、Tiffany & Co.。点击 `View All Brands & Categories` 进入 `brands-and-categories.html`；品牌展示条当前无单项点击。

### 11.4 Sell 首页第四屏：Selling Tips

**文案**：`Selling Tips`；`A little preparation makes selling easier.`；`Gather Original Accessories`、`Share the Condition`、`Check What We Buy` 及各自说明。

三条 Tip 当前为静态信息，无点击行为；`Check What We Buy` 的页面内文案不替代 Brands / Condition Guide 链接。

### 11.5 Sell 首页第五屏：How to Get Paid

**文案**：`How to Get Paid`；`Get paid without waiting for your item to sell.`；`Review Your Offer`；`Complete the Checks`；`Receive Your Payment`。

该屏为流程说明，无按钮和页面跳转。支付实际开始条件由预约 / 交易后续规则决定。

### 11.6 Sell 首页第六屏：FAQ

**文案**：`FAQ`；`More questions?`；`View All FAQs`。

首页折叠问题包括：`What pieces does Looply buy?`、`What conditions do you accept?`、`Is the In-Home Appointment complimentary?`、`How is my offer determined?`、`How does Looply review my item?`、`What happens if I do not accept the offer?`、`What if I live outside Los Angeles?`。

点击问题展开 / 收起答案；答案内链 `Brands & Categories` → `brands-and-categories.html`、`Condition Guide` → `condition-guide.html`。点击 `View All FAQs` → `faq.html`。

### 11.7 Sell 首页第七屏：底部 CTA + Footer

**CTA 文案**：`A refined, personal way to sell luxury.`；`Ready when you are.`；`Share a few details, and a client representative will take it from there.`；`Sell Now`。点击 `Sell Now` 打开预约弹窗 Step 1。

**Footer Sell 分组**：`Sell with Looply`、`Accepted Brands`、`Service Area`、`Seller FAQ`。分别进入首页、Brands、Service Area、FAQ。`Contact Us` 位于公共 Support 分组，不属于 Sell 入口。

**Footer 法律链接**：`Privacy Policy`、`Your Privacy Choices`、`Terms of Service` 等进入公共 Policies / 法律页面；Sell 专属 Seller Terms、Sales Agreement 由预约流程或 Selling Policies 进入。

### 11.8 首页吸底 CTA

用户向下滚动至 `Three Ways to Sell` 区域后，游客态显示浮动 `Ready when you are. / Sell Now`；点击 `Sell Now` 打开预约弹窗。登录态或页面回到顶部时隐藏；浮动条不遮挡 Mobile 底部 Tab。

### 11.9 次级页面进入后的统一行为

次级页面均保留全站 Header / Footer。页面内部链接按以下规则处理：Sell Now → 预约弹窗；Contact Us → `contact-us.html`；相关内容链接回 Brands、Service Area、FAQ、Condition Guide；浏览器返回回到来源页面并保持来源页面滚动位置（正式实现需按公共导航规则确认）。
