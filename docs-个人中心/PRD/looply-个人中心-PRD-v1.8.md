# Looply 个人中心 PRD

**文档版本**：v1.8  
**日期**：2026-07-28  
**模块**：个人中心（Account / Me）  
**覆盖端**：PC Web、Mobile Web、APP、运营后台  
**状态**：评审稿  

**输入基线**：

| 类型 | 文件 | 采用口径 |
|---|---|---|
| 功能范围 | `looply-个人中心-功能清单-v1.8.md` | 账户、匿名记录、平台差异及 Market + 国家站双地域口径 |
| 数据模型 | `looply-个人中心实体关系图-v1.6.svg` | `market_id + country_code`、Market—国家关系、`anonymous_merge_log` |
| C 端原型 | `looply-个人中心-APP-v5.pen` | 页面、字段、平台差异、登录态与多市场设置以此为准 |
| 运营后台 | `looply-客户咨询-antd-原型-v2.html` | 客户咨询列表、详情、状态与操作以此为准 |
| 子模块 PRD | `looply-收藏与浏览历史-PRD-v1.6.md` | 收藏、浏览、地域隔离、匿名合并与 listing 规则以最新版为准 |
| 翻译规则 | `prd-translation-card-placement-product-sync.md` | 静态 UI 与动态业务资源分流；明确资源卡片归属 |

> 冲突优先级：本 PRD 已确认决策 > V5 原型（前端页面、字段、文案、交互、平台差异与登录态）> ER v1.6（实体、字段、关系与数据规则）> 收藏与浏览历史 PRD v1.6 > 客户咨询后台原型 v2 > 功能清单 v1.8 > 旧资料。前端范围按 V5；旧资料中的“Market 等同国家、收藏/浏览仅靠 listing 推导地域、仅美国、Region 无入口、USD/EUR 固定选项”、独立 Settings 壳、匿名合并后清空等口径不再沿用。

> **v1.8 变更**：Privacy & Data 中 Cookie Preferences 与 Do Not Sell or Share 改为可操作开关；每次切换均真实持久化用户偏好，但本期不触发 Cookie、广告、数据出售/共享或其他合规执行动作。用户每次切换均显示 `Preference updated.`，不显示失败 Toast。登录态 Email Subscription 的开启、取消订阅与异常提示分别改为“订阅成功”“已取消订阅”“系统异常，请稍后重试”；游客订阅成功/重复订阅成功与异常提示分别改为“订阅成功”“系统异常，请稍后重试”。

> **v1.7 历史变更**：Change Password 明确跳转并引用登录注册模块的已登录改密流程，个人中心不处理密码字段或校验；My Orders、Profile、Addresses 统一采用携带精确 `returnUrl` 的登录路由守卫，登录成功后自动进入原目标页；Subscriptions 按登录状态分流，访客直接使用 Email + Subscribe，不跳登录。Privacy & Data “仅展示且不可操作”的规则已由 v1.8 取代。

> **v1.6 历史变更**：曾统一 Email Subscription、Performance、Functional、Targeting、Do Not Sell or Share 的服务端开关反馈；其中 Privacy & Data 控制项的实时保存、回滚与 Toast 规则已由 v1.7 取代，不再适用本期。

> **v1.5 历史变更**：曾补充游客邮箱订阅提交反馈；其中 `You're subscribed!`、`Subscription failed. Please try again.` 文案已由 v1.8 的“订阅成功”“系统异常，请稍后重试”取代。邮箱格式错误继续使用输入框内联提示、不显示 Toast。

> **v1.4 历史变更**：Policies 页面按 V5 UI 效果实现 PC/Mobile 响应式展示，全部页面文案支持多语言；五类政策按 `market_id + country_code` 获取，国家之间允许使用不同政策正文、版本、生效时间和 URL。游客订阅 Email 基础格式校验，以及 Gender 未设置时的 `null` 展示与保存规则仍有效。v1.8 恢复“切换国家时读取对应 Cookie Preferences、Do Not Sell or Share 偏好”的地域隔离规则，但偏好仍不触发实际合规动作。

> **v1.3 补充**：个人中心根据 Market 模块返回的 C 端有效国家数量决定是否展示 Country/Region 入口。去重后仅 1 个国家时隐藏入口；大于 1 个时展示；0 个按配置异常处理。入口隐藏不影响国家站上下文及默认语言/币种初始化。

> **数据模型同步说明**：政策、Email 订阅偏好与登录用户隐私偏好均按 `market_id + country_code` 隔离。个人中心本期读写 `privacy_consent` 当前偏好；Cookie、Do Not Sell、GPC 和其他实际合规执行留待后续隐私合规模块消费该记录后实现。

---

## 一、概述

### 1.1 背景与目标

个人中心是买家查看账户信息、订单进度、偏好、Privacy & Data 信息和支持信息的统一入口，也是收藏与浏览历史等个人化数据能力的导航与聚合层。

本期目标：

1. 用统一的信息架构承载移动端与 PC 账户入口，减少重复 Settings 层级。
2. 聚合订单、收藏和浏览历史信息，但不复制外部模块业务数据。
3. 提供 Profile、Country/Region、Language、Currency、Email 订阅等基础账户配置，并展示 Privacy & Data 信息入口。
4. 提供 Contact Us 表单及运营后台客户咨询查看能力。
5. 支持未登录设备级收藏/浏览，并在登录时复制到用户域且保留匿名原件。
6. 首期支持 United States 与 Hong Kong 国家站，并根据当前 `market_id + country_code` 加载可售 listing、可用币种、适用政策与订阅偏好。
7. Cookie 分类控制、Do Not Sell/Share、GPC 和其他实际合规执行不属于本期个人中心；后续由隐私合规模块按适用国家实现。

### 1.2 本期范围

- 移动端个人中心首页、PC Account Home 与左侧导航。
- 订单状态入口：Processing、Shipped、Delivered、Returns、View All。
- Profile：Email、Nickname、Gender、Change Password、Log Out。
- Country/Region、Language、Currency；可选项分别读取 Market 模块和多语言系统配置。
- Subscriptions 登录态开关与游客邮箱订阅 Case。
- Privacy & Data 三模块平铺。
- Contact Us C 端提交与客户咨询运营后台。
- Policies、About Looply、APP 版本号。
- Wishlist / Recently Viewed 入口、当前国家站数量聚合及与专项模块的衔接。
- anonymous_id、匿名记录复制合并和合并日志。

### 1.3 不做什么

- 不做独立 Settings 页面或右上角齿轮入口。
- 不做待付款入口；支付前状态属于结算/弃单，不属于订单。
- Returns 仅查看进度，不提供买家自助申请退货/退款。
- 不做头像、生日、个人简介、邮箱认证状态或邮箱换绑。
- 不做 Recommended for You、站内消息、支付方式管理、Push/SMS 订阅。
- 不做用户端自助导出数据或自助注销；本期邮件申请、运营处理。
- 不在个人中心拥有订单、地址、订阅、客户咨询、商品、政策正文或隐私同意的数据表。
- 不将 Google reCAPTCHA token、限流计数器写入客户咨询业务表。
- `favorite`、`browsing_history` 与浏览删除标记必须保存 `market_id + country_code`；一个 Market 可包含多个国家，不能仅靠 listing 推导国家站。
- 本版不确定订单、付款、收藏、浏览等时间在 C 端采用设备时区还是事件时区；不新增事件时区字段。

### 1.4 用户角色

| 角色 | 说明 |
|---|---|
| 已登录买家 | 使用完整个人中心、账户级订单/偏好/订阅与咨询功能；可修改并保存 Privacy & Data 偏好，但本期不触发实际合规动作 |
| 未登录访客 | 看到 Signed Out / Sign In 引导；可通过独立 Subscriptions 游客页订阅邮箱；设备级收藏/浏览由专项入口承载 |
| 客服/运营 | 在客户咨询后台查询、查看、标记状态并通过邮件客户端回复 |
| 合规人员 | 后续隐私合规模块的 Cookie、Do Not Sell/Share、GPC 与 DSAR 规则 Owner，不直接使用本期客户咨询后台角色能力 |

### 1.5 核心场景

1. 买家进入个人中心，快速查看订单各状态数量。
2. PC 买家查看 Wishlist / Recently Viewed 数量并进入对应能力。
3. 买家修改 Nickname、Gender、Country/Region、Language 或 Currency。
4. 登录用户开启/关闭 Email 营销订阅；访客直接填写邮箱订阅。
5. 用户切换并保存 Cookie Preferences、Do Not Sell/Share 偏好；本期仅记录偏好和显示成功反馈，不触发实际合规动作。
6. 用户通过 Contact Us 提交咨询，运营在后台查看并邮件回复。
7. 未登录用户产生收藏/浏览，登录后系统复制到用户域，同时保留匿名原件并记录合并日志。
8. 用户切换 Country/Region 后，系统同时保存该国家的 `country_code` 与归属 `market_id`，仅看到当前国家站收藏和浏览历史；切回后原国家数据仍在。

### 1.6 全局页面流转

```text
个人中心首页
├─ 订单状态 / View All → 订单模块列表或详情
├─ Profile（需登录）→ Nickname Sheet / Gender Sheet / Change Password
├─ Addresses（需登录）→ 地址库模块
├─ Country/Region → 国家/地区选择（服务端同步确定归属 Market）
├─ Language → 语言选择
├─ Currency → 币种选择
├─ Subscriptions → 登录态开关页 / 游客 Email + Subscribe 页
├─ Privacy & Data → 三模块平铺页
├─ Contact Us → 咨询提交页
├─ Policies → 五项政策列表 → 外部政策正文
├─ About Looply → About 页面
└─ Log Out → 二次确认 → Signed Out / Sign In

游客订阅入口 → Subscriptions 游客页 → Email + Subscribe
Contact Us 提交 → 客服模块 customer_inquiry → 客户咨询后台详情 → 邮件客户端回复
```

### 1.7 术语说明

| 术语 | 定义 |
|---|---|
| market / market_id | Market 模块配置的商业运营市场及内部唯一标识；一个 Market 可包含多个国家 |
| country / country_code | 用户当前选择的具体经营国家/地区，使用 ISO 3166-1 alpha-2；Country/Region UI 实际选择此维度 |
| listing | 用户前台可见、可下单的渠道商品单元；收藏与浏览锚定 listing_id，同时独立保存发生时 Market 与国家 |
| anonymous_id / looply_aid | 设备/浏览器级假名标识，承载未登录收藏、浏览和设备偏好 |
| 用户域 | 以 user_id 为主体的账户级数据 |
| 匿名域 | 以 anonymous_id 为主体的设备级数据 |
| 复制上移 | 登录时将匿名域记录复制到用户域，匿名原件保留 |
| customer_inquiry | 客服模块拥有的客户咨询记录 |
| Email Subscription | 营销邮件订阅，不影响订单、支付和账户安全等事务邮件；订阅状态按 `market_id + country_code` 隔离 |
| 区域上下文 | 当前生效的 `market_id + country_code + language + currency` 组合，以及依赖该组合加载的政策与订阅偏好 |

### 1.8 多语言、多国家与翻译归属

首期启用 United States 与 Hong Kong 国家站。一个 Market 可包含多个国家；Country/Region 选项读取 Market 模块中允许 C 端使用的国家列表，用户选择具体国家，服务端同时确定并保存 `country_code + market_id`，不得把 Market 与国家视为同一层。语言资源仍由多语言系统提供，但 Market 模块须为每个国家配置 `default_language_code` 与 `default_currency_code`。每次切换国家都强制采用目标国家默认语言和默认币种，不保留原值，也不恢复该国家上次手动选择；切换后用户仍可分别修改 Language 与 Currency。

数据库时间字段统一保存 UTC。本版不确定 C 端最终按设备当前时区、事件发生时区或其他业务时区展示，原型和 ER 暂不新增 `event_timezone` 等字段；展示规则须在开发方案冻结前另行确认。

**翻译归属清单**

| 业务对象 | 业务字段 | 内容类别 | 卡片决策 | resourceType | 翻译中心路径 | fieldName / i18n key | 展示面 | 语种/兜底 |
|---|---|---|---|---|---|---|---|---|
| 个人中心 UI | 菜单、标题、按钮、状态标签、提示、校验错误、空态 | 静态 UI 文案 | 不进资源卡片 | — | UI message package | `account.*`、`common.*` | PC/Mobile/APP | 按用户选择语言；缺失回退 en |
| 订单入口 | Processing/Shipped/Delivered/Returns/View All 标签 | 静态 UI 文案 | 不进资源卡片 | — | UI message package | `account.orders.*` | 个人中心首页 | 按用户选择语言；缺失回退 en |
| Contact Us | 表单标签、说明、回复时限、非退货地址提示 | 静态 UI 文案 | 不进资源卡片 | — | UI message package | `account.contact.*` | Contact Us | 按用户选择语言；缺失回退 en |
| 公司联系方式 | Email、Phone | 不翻译 | 不进资源卡片 | — | — | — | Contact Us | 原值展示 |
| 公司地址 | 地址值 | 不翻译；周边标签需翻译 | 不进资源卡片 | — | UI message package | `account.contact.address_label` | Contact Us | 地址原值；标签回退 en |
| Policies 列表 | 五项政策名称和摘要 | 静态 UI 文案 | 不进资源卡片 | — | UI message package | `account.policies.*` | Policies 列表 | 按用户选择语言；缺失回退 en |
| 政策正文 | 标题、正文、富文本 | 外部动态业务内容 | 本模块不注册卡片 | 外部政策/CMS 模块定义 | 外部模块定义 | 外部模块定义 | 政策正文页 | 先按 `market_id + country_code` 确定适用政策及版本，再按用户语言取译文；目标语种缺失时仅可回退同一区域、同一版本的 English，不得跨国家回退 |
| About Looply | 品牌介绍文案 | 静态 UI 文案 | 不进资源卡片 | — | UI message package | `account.about.*` | About | 按用户选择语言；缺失回退 en |
| 客户咨询内容 | 用户 Full Name、Email、Message | 用户原始内容，不翻译 | 不进资源卡片 | — | — | — | 客户咨询后台 | 保留用户原文 |
| 客户咨询后台 | 菜单、筛选、状态、操作文案 | 内部中文运营 UI | 不翻译 | — | — | — | 运营后台 | 中文固定展示 |
| 商品/品牌信息 | listing 名称、品牌、商品描述 | 外部动态业务内容 | 本模块不注册卡片 | 商品模块既有卡片 | 商品域 | 商品模块定义 | Wishlist/History | 由商品模块返回本地化内容 |

结论：个人中心本期**不新建 translation_resource 卡片**。本模块产生的可翻译内容均为静态 UI 文案，进入 message package；政策正文和商品内容由数据 Owner 的 PRD 定义稳定 `resourceType`。用户提交的咨询内容不进入翻译中心。

---

## 二、需求详细描述

### 2.1 个人中心首页与导航

**功能描述**：为登录用户聚合账户信息、订单状态和功能入口。个人中心只读取外部模块汇总结果，不复制订单、地址或商品数据。

**前置条件**：用户已登录。未登录访问个人中心时进入 Signed Out / Sign In 页面，不展示完整目录。

**平台布局**：

| 区域 | Mobile Web / APP | PC Web |
|---|---|---|
| 用户标识 | My Account + Nickname + Email | Account Home；用户信息由全局账户上下文提供 |
| 订单 | 横向五入口 | 由 My Orders 入口进入订单模块；Account Home 可展示概览 |
| 配置入口 | Profile、Addresses、Language、Currency、Subscriptions；Country/Region 仅在有效国家数 > 1 时插入 | 左侧栏 ACCOUNT SETTINGS 同规则；Country/Region 仅在有效国家数 > 1 时显示 |
| Wishlist / Recently Viewed | 个人中心首页不展示 | Account Home 显示卡片与数量 |
| Support | Contact Us / Policies / About 平铺 | 左侧栏 SUPPORT & POLICIES 分组 |
| Log Out | 页面底部 | 左侧栏底部 |

**订单入口**：

| UI 标签 | 业务含义 | 数量来源 | 点击结果 |
|---|---|---|---|
| Processing | 已支付、待处理或备货中的订单聚合 | 订单模块 | 对应筛选的订单列表 |
| Shipped | 已发货且未完成送达 | 订单/物流模块 | 对应订单列表或物流详情 |
| Delivered | 已送达订单 | 订单模块 | Delivered 订单列表 |
| Returns | 退货/退款处理中或已有结果 | 售后/订单模块 | 仅查看进度，不显示申请入口 |
| View All | 全部订单 | — | 全部订单列表 |

订单状态到 UI 标签的具体枚举映射由订单模块提供；个人中心不得自行根据订单明细猜测或缓存计数。读取失败时对应角标不显示，并提供页面级轻提示，不展示 0 冒充真实结果。

**PC 资产卡片**：

| 卡片 | 展示 | 规则 |
|---|---|---|
| Wishlist | 当前国家站收藏数量和说明 | 数量实时调收藏服务并按实体 `market_id + country_code` 过滤；可显示 24 等真实数量 |
| Recently Viewed | 当前国家站最近浏览数量和说明 | 调浏览历史服务并按实体 `market_id + country_code` 过滤；点击进入专项页面 |

**状态变体**：已登录默认态、订单计数加载态、部分数据读取失败、Signed Out、退出确认。

**登录路由守卫**：以下入口的页面内点击和直接深链必须使用同一守卫；未登录时不得展示中间确认页，而是立即跳转登录注册模块，并附带精确目标的 `returnUrl`。登录注册模块登录成功后按 `returnUrl` 自动回到原目标页；`returnUrl` 必须为本站已登记的内部路由，非法、过期或跨站地址回退个人中心首页。

| 入口 / 目标路由 | 未登录行为 | 登录成功后 |
|---|---|---|
| My Orders、Processing、Shipped、Delivered、Returns、View All | 跳登录页，携带对应订单列表或状态筛选的 `returnUrl` | 自动进入对应订单列表或状态页；Returns 仅查看进度 |
| Profile | 跳登录页，携带 Profile 的 `returnUrl` | 自动进入 Profile |
| Addresses | 跳登录页，携带 Addresses 的 `returnUrl` | 自动进入地址库模块的 Addresses 页面 |
| Subscriptions | 不跳登录，直接进入游客 Email + Subscribe 页 | 已登录用户直接进入账户邮箱的订阅开关页 |

**UI 关联**：`V5-移动端-个人中心-响应式统一版`、`V5-PC-个人中心-响应式统一版`、`V5-移动端-退出登录后`、`V5-PC-退出登录后`。

### 2.2 Profile

**功能描述**：展示基础账户资料并支持编辑 Nickname、Gender；密码修改跳转登录注册模块的已登录改密流程。

**页面字段**：

| 字段/操作 | 控件 | 必填 | 规则 |
|---|---|:---:|---|
| Email | 只读文本 | — | 展示账户邮箱；本期无认证徽章、无换绑 |
| Nickname | 输入框 | 是 | 1–24 字位簇；规则见下表 |
| Gender | 单选 | 否 | `female` / `male` / `prefer_not_to_say`；未设置为 `null`，Profile 显示本地化 `Not set` |
| Change Password | 跳转行 | — | 跳转登录注册模块 `ChangePassword`；个人中心仅提供导航 |
| Log Out | 操作行 | — | 进入二次确认 |

**Nickname 校验**：

| 维度 | 规则 | 校验时机 |
|---|---|---|
| 长度 | 1–24 个 grapheme cluster | 输入时、提交时 |
| 字符 | Unicode 字母、数字、空格、`.` `_` `-` `'` | 输入时、提交时 |
| 组成 | 至少一个字母或数字；不允许纯符号 | 提交时 |
| 空格 | trim 首尾；连续空格折叠为一个 | 提交前规范化 |
| Emoji | 本期不允许 | 输入时、提交时 |
| 安全字符 | 拒绝控制字符、零宽字符、双向控制符、换行和制表符 | 后端最终校验 |
| 唯一性 | 不要求唯一 | — |
| 敏感词 | 禁止脏话及冒充 Looply Official/Customer Service | 后端提交时 |

**Gender 空值与保存规则**：用户从未设置 Gender 时，服务端返回并保存为 `null`；Profile 显示本地化 `Not set`，打开编辑面板后 Female、Male、Prefer not to say 三项均不选中。`Prefer not to say` 是用户主动选择的有效枚举值，不等于 `null`，不得作为默认选项。用户未选择直接 Save 时保持 `null`；只有明确选择并保存成功后才写入对应枚举值。

| Gender 枚举值 | 含义 | 触发时机 | 展示 |
|---|---|---|---|
| `female` | 用户选择 Female | 用户明确选择并保存成功 | Female 的本地化文案 |
| `male` | 用户选择 Male | 用户明确选择并保存成功 | Male 的本地化文案 |
| `prefer_not_to_say` | 用户主动表示不愿说明 | 用户明确选择并保存成功 | Prefer not to say 的本地化文案 |

`null` 表示用户未设置，不属于 Gender 枚举值。

**操作流程**：移动端点击 Nickname/Gender 打开底部 Sheet，Save 后回写；PC 点击 Edit 进入对应编辑态。保存失败保留输入并显示错误，不能静默回滚成旧值。

**Change Password 外部流程**：已登录用户点击 Change Password 后，跳转登录注册模块的 `ChangePassword`。该模块先要求并校验当前/旧密码，校验通过后才允许输入新密码；密码强度、新旧密码规则、密码写入、其他会话失效和成功反馈均由登录注册模块负责。个人中心不得承载密码输入框、旧密码校验、重置密码验证码或密码写入逻辑。忘记密码场景同样由登录注册模块的“邮箱验证码 → 重置密码”流程处理，不从个人中心复制实现。

**本期不做**：头像、生日、Bio、邮箱认证状态。

**UI 关联**：`V5-移动端-Profile`、`V5-PC-Profile`、`V5-移动端-编辑昵称`、`V5-移动端-选择性别`。

### 2.3 Country/Region、Language 与 Currency

**功能描述**：管理用户当前国家站、界面语言与展示/结算币种。用户端标签固定为 `Country/Region`，实际选择具体国家；内部同时保存 `country_code + market_id`，Market 表示商业运营市场、国家表示具体站点，二者不得混用。

| 偏好 | 选项来源 / V5 示例 | 默认 | 页面行为 |
|---|---|---|---|
| Country/Region | Market 模块允许 C 端使用的国家/地区；示例 United States、Hong Kong | 已保存 country_code；无值时使用默认国家，market_id 由服务端归属关系确定 | 单选后 Save；原子更新区域上下文，并刷新目标国家政策与订阅偏好 |
| Language | 多语言系统已启用语言；示例 English、Español、繁體中文 | 平时显示已保存语言；首次进入取默认国家的 default_language_code | 可单独修改；每次切换国家时强制覆盖为目标国家 default_language_code |
| Currency | 目标国家配置的默认币种须属于其 Market 支持币种；示例 USD $、HKD HK$ | 平时显示已保存币种；首次进入取默认国家的 default_currency_code | 可单独修改；每次切换国家时强制覆盖为目标国家 default_currency_code |

**市场切换规则**：

1. Country/Region 列表只展示 Market 模块中允许 C 端使用的国家；国家名称与 `country_code → market_id` 归属由 Market 模块返回，个人中心不维护国家枚举。
2. 入口展示数量只统计 Market 模块返回且 `is_c_end_enabled=true`、Market—国家关联有效的记录，并按 `country_code` 去重；不能把停用、重复或仅后台可用的国家计入。
3. 有效国家数 = 1：Mobile Web、APP 的 Account Settings 列表和 PC 左侧栏均隐藏 Country/Region 入口，不保留空白占位；系统仍用该唯一国家初始化/校验 `country_code + market_id + language + currency`。用户直接访问 Country/Region 深链时返回个人中心首页，不展示无意义的单选页面。
4. 有效国家数 > 1：三端显示 Country/Region 入口，当前值展示已生效国家名称；点击后进入国家单选页面。
5. 有效国家数 = 0：视为 Market 配置异常，不展示切换入口；已有有效国家站上下文时暂时保留并告警，无有效上下文时不得猜测国家或跨站兜底，由全局站点框架展示配置异常/重试状态。
6. 国家数量不是前端写死值；每次加载个人中心或刷新 Market 配置后重新计算。数量从 1 变为大于 1 时显示入口，从大于 1 变为 1 时隐藏入口并按唯一国家重新初始化默认偏好。
7. 保存时服务端校验国家归属 Market 且关联可用，读取目标国家在 Market 模块配置的 `default_language_code + default_currency_code`，再原子更新用户/设备当前 `country_code + market_id + language + currency`；默认语言必须是多语言系统启用值，默认币种必须是归属 Market 支持值。前端不得自由提交这四项组合，IP 仅可推荐国家。
8. 商品列表、Wishlist、Recently Viewed 及其 PC 数量均按当前 `market_id + country_code` 查询；收藏/浏览实体自身保存两字段，不再仅通过 listing 过滤。其他 Market/国家记录只隐藏、不删除，用户切回后恢复展示。
9. 每次切换 Country/Region 都强制覆盖为目标国家默认 Language 与 Currency，即使原值仍可用或在同一 Market 内切换也不保留；不按国家记忆历史手动选择。切换成功提示 `Country/region updated. Language changed to {language}; currency changed to {currency}.`，并按新语言/币种刷新展示。
10. 国家切换必须同时加载目标 `market_id + country_code` 下的五类政策、Email 订阅偏好、Cookie Preferences 与 Do Not Sell or Share 已保存偏好；这些数据不得沿用切换前国家的缓存或默认值。用户切回原国家时重新读取该国家已保存状态，不复制其他国家的选择。
11. 区域切换采用整体提交：只有目标国家的 `market_id + country_code + language + currency`、政策目录、订阅偏好和隐私偏好均返回有效结果后，前端才一次性展示新国家状态。缺少配置或请求失败不属于有效结果；任一关键项失败则保持切换前完整状态并提示重试，不得出现政策已切换但订阅或隐私偏好仍属于旧国家等混合状态。
12. 所有区域相关请求和客户端缓存键必须包含 `market_id + country_code`。语言仅控制 UI 与当前国家内容译文，不可替代国家维度；服务端仍须校验当前国家上下文，不能只信任前端缓存。
13. 地址选择、格式和可配送范围由地址模块控制；个人中心不根据 market_id/country_code 改写地址数据。国家未来调整所属 Market 时，历史收藏/浏览的地域快照不静默改写；迁移须走显式方案。

登录用户以 `user_preference` 为跨端权威值；设备偏好用于首次体验和缓存。登录时账户无偏好则设备值 seed；账户已有值则账户优先并回写设备。

保存或国家站上下文切换失败时保留原生效的区域上下文、政策、订阅偏好和隐私偏好并提示重试；不允许只更新其中一部分。Market 模块返回 0 个有效国家、归属不匹配、目标关联停用、缺少国家默认语言/币种、默认语言未在多语言系统启用、默认币种不受归属 Market 支持或目标国家区域配置不完整时，不切换当前国家站并记录配置告警。

**UI 关联**：`V5-移动端-选择国家地区`、`V5-PC-CountryRegion`、`V5-移动端-选择语言`、`V5-PC-Language`、`V5-移动端-选择币种`、`V5-PC-Currency`、`V5-移动端-切换市场-币种回退Case`。Country/Region 行与 PC 导航项采用条件渲染，不新增页面；原型中已展示的入口代表“有效国家数 > 1”Case。

### 2.4 Subscriptions

**功能描述**：管理当前 `market_id + country_code` 下的 Email 营销订阅状态。状态和同意凭证归订阅管理模块，个人中心只提供前端入口；切换国家后重新读取目标国家状态，不沿用旧国家开关值。

**入口分流**：已登录用户从个人中心入口或直达 Subscriptions 路由时，均展示注册邮箱和 Email Subscription 开关；未登录用户从同一入口或直达路由时，均直接展示 Email 输入框与 Subscribe，不跳转登录，也不携带登录 `returnUrl`。订阅成功不会自动创建登录态或跳转个人中心首页。

**登录态**：

| 元素 | 规则 |
|---|---|
| Subscription email | 只读显示账户邮箱 |
| Email Subscription | subscribed 时 ON，unsubscribed 时 OFF |
| 说明 | 关闭只影响营销邮件，事务邮件不受影响 |

开关切换采用即时反馈。中文基准文案及多语言资源规则见“订阅反馈”；进入页面拉取失败时显示重试，不渲染一个可能错误的开关值。

**游客态**：

| 字段 | 必填 | 校验 |
|---|:---:|---|
| Email | 是 | trim 首尾空格；仅允许一个 `@`；`@` 前后均非空；地址内不允许空格；域名至少包含一个 `.` 且不能以 `.` 开头或结尾；长度上限由订阅模块统一约束 |
| Subscribe | — | 提交中 loading；重复订阅幂等成功 |

游客提交前由前端执行基础格式校验，失败时不得发送订阅请求，并在输入框附近显示本地化提示 `Please enter a valid email address`；该校验只判断基本格式，不代表邮箱真实存在。校验通过后，后端仍执行长度、重复订阅幂等、频率限制及订阅模块既有风控规则，本 PRD 不新增人机验证要求。游客提交须携带当前 `market_id + country_code`，来源记为 preference。成功后显示订阅成功反馈；失败保留 Email。个人中心不存游客订阅状态。

**游客提交反馈**：

| 结果 | 触发条件 | 中文基准 Toast | i18n key | 页面行为 |
|---|---|---|---|---|
| 订阅成功 | 首次订阅成功；或重复订阅按幂等成功返回 | `订阅成功` | `account.subscriptions.toast.success` | 显示成功 Toast，约 3 秒后自动消失；停留当前页，不重复提交 |
| 系统异常 | 网络异常、请求超时或服务端返回失败 | `系统异常，请稍后重试` | `account.subscriptions.toast.system_error` | 显示失败 Toast，约 3 秒后自动消失；保留已输入 Email，Subscribe 恢复可点击 |
| 格式错误 | 前端 Email 基础格式校验未通过 | 不显示 Toast | `account.subscriptions.email.invalid` | 在输入框附近显示内联错误，阻止请求 |

Toast 使用全局 Toast 组件；表中中文为基准文案，C 端必须按当前语言显示对应 i18n 译文，不得把完整 Email 放入 Toast 或埋点。若全局 Toast 规范对位置、动效或无障碍停留时间有统一要求，以全局规范为准，本 PRD 固定触发条件、语义和反馈类型。

**登录态切换反馈**：

| 操作结果 | 中文基准 Toast | i18n key | 页面行为 |
|---|---|---|---|
| 从 unsubscribed 切换为 subscribed 且订阅管理模块保存成功 | `订阅成功` | `account.subscriptions.toggle.subscribe_success` | 保持 ON，显示 Toast 约 3 秒 |
| 从 subscribed 切换为 unsubscribed 且订阅管理模块保存成功 | `已取消订阅` | `account.subscriptions.toggle.unsubscribe_success` | 保持 OFF，显示 Toast 约 3 秒 |
| 网络异常、超时或订阅管理模块返回失败 | `系统异常，请稍后重试` | `account.subscriptions.toast.system_error` | 回滚到切换前状态，显示 Toast 约 3 秒 |

连续操作只展示最后一条 Toast；失败 Toast 不得被成功 Toast 覆盖。中文基准文案必须进入 UI message package，由多语言系统提供译文。

**订阅状态枚举**：

| 枚举值 | 含义 | 触发时机 | 适用场景 |
|---|---|---|---|
| subscribed | 已同意接收营销邮件 | 游客 Subscribe 或登录用户开启开关 | 可发送营销邮件 |
| unsubscribed | 已退订营销邮件 | 登录用户关闭开关或邮件退订 | 仅保留事务邮件 |

**UI 关联**：`V5-移动端-Subscriptions`、`V5-PC-Subscriptions`、`V5-移动端-Subscriptions-未登录Case`、`V5-PC-Subscriptions-未登录Case`。

### 2.5 Privacy & Data

**功能描述**：在一个页面按固定顺序平铺 Manage Your Data、Cookie Preferences、Do Not Sell or Share My Personal Information。页面结构和可见文案按 V5 与多语言系统渲染；Cookie Preferences 与 Do Not Sell or Share 均为可操作开关，切换后记录当前登录用户在当前国家站的偏好。

**本期边界**：本期只保存和读取用户偏好，不触发 Cookie 写入/删除、统计或广告 SDK 启停、个性化、出售/共享数据拦截、GPC 识别、同意审计或其他合规动作。用户每次切换后，前端立即显示新状态并显示 `Preference updated.`；不得因本期没有下游执行动作显示失败 Toast 或回滚。后端必须真实持久化偏好；若持久化链路出现技术故障，服务端必须记录告警并异步重试至成功，前端仍保持本次选择和 `Preference updated.` 反馈。

**模块一：Manage Your Data**：

| 区块 | 展示与处理 |
|---|---|
| Request a Copy of Your Data | 纯文案，引导从注册邮箱联系 `privacy@looply.com`；人工核验并在 45 天内响应 |
| Delete Account | 纯文案，引导邮件申请；运营后台执行；本期无自助按钮 |

账号注销执行后立即匿名化 PII，无冷静期、不可恢复；交易记录按法律要求脱敏保留。账户删除不自动清空设备匿名域，除非全局隐私流程同时提供 anonymous_id。

**模块二：Cookie Preferences**：按 V5 展示 Strictly Necessary、Performance、Functional、Targeting 及其说明。Strictly Necessary 固定 ON 且不可关闭，不产生偏好记录；其余三项均可切换、按当前已保存值展示，并分别记录如下偏好键。页面可翻译的标题、分类名称、说明与 Toast 使用 UI message package。

| UI 分类 | preference_key | 默认 | 是否可切换 | 本期效果 |
|---|---|---|:---:|---|
| Strictly Necessary | — | ON | 否 | 仅静态展示；不生成记录 |
| Performance | `cookie_analytics` | OFF | 是 | 保存偏好，不启停任何 SDK 或 Cookie |
| Functional | `cookie_functional` | OFF | 是 | 保存偏好，不改变偏好记忆或个性化行为 |
| Targeting | `cookie_marketing` | OFF | 是 | 保存偏好，不改变广告或营销定向行为 |

**模块三：Do Not Sell or Share**：按 V5 展示标题、说明与可操作开关。`dns_opt_out=false` 表示未选择退出，开启后保存为 `true`。该模块本期固定展示，不根据国家适用性隐藏；只记录偏好，不停止出售/共享数据或跨情境行为广告。实际展示条件和合规执行由后续隐私合规模块定义。

**偏好持久化与反馈规则**：

| 项目 | 规则 |
|---|---|
| 适用用户 | 仅登录用户；Privacy & Data 本期不向游客展示 |
| 地域维度 | 每条记录必须包含 `user_id + market_id + country_code`；切换国家后读取目标国家记录，切回后恢复原国家记录 |
| 偏好维度 | `cookie_analytics`、`cookie_functional`、`cookie_marketing`、`dns_opt_out`；每个键保存布尔值 |
| 更新语义 | 同一 `user_id + market_id + country_code + preference_key` 保留当前值，重复切换覆盖更新；最后一次用户操作生效 |
| 审计字段 | 保存 `updated_at`、`source=account_center`；不得保存密码、完整 Email 或浏览器指纹 |
| Toast | 用户每次可操作开关切换后均显示 `Preference updated.`，约 3 秒后自动消失；使用 `account.preference.toast.success` 并按当前语言翻译 |
| 下游动作 | 本期禁止基于该记录执行 Cookie、广告、数据出售/共享、GPC 或其他合规动作 |

连续切换仅显示最后一条 `Preference updated.` Toast，不叠加多个相同提示。隐私偏好写入失败的重试、告警和补偿仅作为服务端可靠性处理，不向用户展示失败 Toast，也不影响当前界面开关状态。

**UI 关联**：`V5-移动端-PrivacyData`、`V5-PC-PrivacyData`。

### 2.6 Contact Us C 端

**功能描述**：登录用户在个人中心填写咨询并提交给客服模块，同时可查看静态联系方式。

**表单字段**：

| 字段 | 控件 | 必填 | 默认/校验 |
|---|---|:---:|---|
| Full Name | 单行输入 | 否 | 默认账户 Nickname；允许修改 |
| Email | Email 输入 | 是 | 默认账户邮箱；允许修改本次回复邮箱；格式校验 |
| Message | 多行文本 | 是 | trim 后不能为空；仅保存用户原文，不进入翻译中心 |
| reCAPTCHA token | 隐式 | 是 | 后端校验 Google reCAPTCHA、站点/应用来源及 action=`contact_submit` |

**提交顺序**：字段校验 → reCAPTCHA 后端校验 → 频率/重复判断 → 创建 customer_inquiry → 返回成功反馈。任何拦截都发生在写咨询和触发通知之前。

**防滥用规则**：

| 规则 | 处理 |
|---|---|
| 登录用户频率 | 按 user_id 固定窗口 5 次/24h |
| 重复内容 | 同一 user_id 10 分钟内规范化后相同 Message 拦截 |
| 超限 | 返回 429 + Retry-After；提示 `Too many requests. Please try again later.` |
| reCAPTCHA 失败 | 不创建咨询；提示验证失败后重试 |
| Google 服务异常 | fail-open，但仍执行频率和重复判断 |
| 安全日志 | 记录时间、原因、user_id、脱敏 IP；不记录完整 Message |

**静态联系方式**：

- Email：`service@looply.com`
- Phone：`+852 4619 1323`
- Registered Office / Business Mailing Address：`ALEXANDRA HOUSE, 18 CHATER ROAD, CENTRAL, HONG KONG`
- Email Response Time：一般 1–2 个工作日。
- 注册地址仅供公司联系，不是退货地址；退货获批后由邮件提供正确地址与说明。

**异常处理**：网络失败保留字段；重复点击时按钮 loading 且禁止并发提交；创建成功但通知失败不回滚咨询记录，由客服模块补偿。

**UI 关联**：`V5-移动端-ContactUs`、`V5-PC-ContactUs`。

### 2.7 客户咨询运营后台

**模块定位**：后台只保留“客户咨询”模块，用于查看 Contact Us 及其他客服入口产生的 customer_inquiry。个人中心本期只产生登录用户咨询，但后台可同时展示其他来源产生的访客咨询。

**列表字段**：

| 列 | 数据字段 | 说明 |
|---|---|---|
| 咨询编号 | inquiry_id | 可点击打开详情 |
| 提交时间 | created_at | 列表显示相对/短日期，详情显示完整时间 |
| 姓名 | full_name | 可为空 |
| 回复邮箱 | reply_email | 超长省略，悬停显示完整值 |
| 咨询内容 | message | 列表省略，详情显示全文 |
| 状态 | status | 新咨询/已读/已解决 |
| 操作 | — | 查看 |

**筛选**：关键词搜索咨询编号、姓名、邮箱、咨询内容；状态筛选 all/new/read/resolved；支持查询与重置。无结果显示筛选空态，数据源为空显示零数据空态，读取异常显示重试。

**详情抽屉**：展示姓名、回复邮箱、用户类型、来源、Message、咨询编号、提交时间、最后更新；提供“通过邮件回复”“标记已解决”或“重新打开”。用户类型由 `user_id` 是否为空计算：非空=登录用户，空=访客，不要求另存一份可冲突的类型字段。

**状态枚举与流转**：

| 枚举值 | UI | 进入条件 | 退出条件 |
|---|---|---|---|
| new | 新咨询 | C 端创建成功 | 首次打开详情后进入 read；或直接解决 |
| read | 已读 | 运营首次查看，或 resolved 重新打开 | 标记已解决进入 resolved |
| resolved | 已解决 | 运营点击标记已解决 | 重新打开进入 read |

**来源枚举**：

| 枚举值 | 含义 | 记录场景 |
|---|---|---|
| pc_web | PC Web Contact Us | PC 用户提交 |
| mobile_web | Mobile Web Contact Us | 移动网页提交 |
| app | 原生 APP Contact Us | APP 提交 |

**回复方式**：点击“通过邮件回复”打开默认邮件客户端，收件人为 reply_email，主题包含咨询编号。MVP 不在后台内编辑和发送邮件，也不保存邮件正文；邮件回复留痕能力为后续项。

**分页**：列表分页，不使用无限滚动；具体每页数量由后台统一表格规范控制。

**UI 关联**：`looply-客户咨询-antd-原型-v2.html`。

### 2.8 Policies

**功能描述**：不分 POLICIES/LEGAL 组，按 V5 UI 效果平铺五类固定入口；PC Web、Mobile Web 和 APP 使用一致的信息结构并按屏幕宽度适配。政策列表标题、摘要、状态和错误提示均须接入多语言，不得在前端写死 English。

| 顺序 | 文件 | 说明 |
|---:|---|---|
| 1 | Privacy Policy | 数据收集和使用 |
| 2 | Terms of Service | Marketplace 条款与账户规则 |
| 3 | Shipping & Delivery | 配送方式、时效和履约 |
| 4 | Returns & Refunds | 退货窗口和退款处理 |
| 5 | Accessibility Statement | 无障碍浏览与购物支持 |

个人中心不拥有正式政策正文。政策/CMS 模块按 `policy_key + market_id + country_code` 返回当前适用政策，至少包含政策版本号、生效时间、可用状态和真实 URL；政策正文使用的本地化标题、摘要及内容也由该模块返回。不同国家允许返回不同正文、版本、生效时间和 URL，不要求多个国家共用一个政策文件。个人中心列表中的五类入口名称和通用摘要仍属于 UI message package。

读取顺序固定为：先用当前 `market_id + country_code` 确定适用政策和版本，再按当前 `language_code` 读取译文。目标语种缺失时，仅可回退同一 `market_id + country_code`、同一政策版本的 English；不得回退其他国家政策。若目标国家缺少某项有效政策或真实 URL，该项显示本地化不可用状态且不可点击，不得生成空 URL，也不得用其他国家政策兜底；首发国家上线前五项均须配置完成。

切换 Country/Region 成功后，Policies 页面必须重新请求目标国家目录并清除旧国家缓存；页面处于切换加载态时不得暂时显示旧国家正文。政策列表与政策正文可由单页路由、多页面或 CMS 页面实现，具体开发页面数量不属于产品约束，只需保证五类入口、返回路径、多语言、响应式展示和区域隔离满足本节规则。Cookie Policy 不在该五项列表中。

**UI 关联**：`V5-移动端-Policies`、`V5-PC-Policies`。

### 2.9 About Looply

**页面内容**：品牌标识、`Curated luxury marketplace`、Looply 品牌介绍。

| 端 | App Version |
|---|---|
| APP | 显示，从构建信息动态读取；原型示例 1.0.0 |
| Mobile Web | 不显示 |
| PC Web | 不显示 |

**UI 关联**：`V5-Mobile Web-About`、`V5-APP-About`、`V5-PC-About`。

### 2.10 Log Out 与 Signed Out

**操作流程**：点击 Log Out → 打开二次确认 → Cancel 留在当前页；确认后清理前端 access/refresh token，并请求用户中心终止 session → 跳站点首页或 Signed Out 页面。

退出接口失败时前端仍清理本地 token，避免用户误以为仍安全退出失败；同时记录异常。账户级订单/地址不可见，但设备匿名域收藏和浏览原件保留。

Signed Out 页面显示登录提示与 Sign In Again。成功登录后回个人中心首页。

**UI 关联**：`V5-移动端-退出登录-确认`、`V5-PC-退出登录-确认`、`V5-移动端-退出登录后`、`V5-PC-退出登录后`。

### 2.11 Wishlist 与 Recently Viewed 衔接

详细列表、卡片、筛选、清理和空态沿用专项 PRD v1.6；本节只定义个人中心与 ER v1.6 必须一致的 Market + 国家衔接规则。

**Wishlist**：

- 收藏主体为 user_id 或 anonymous_id，二选一。
- 收藏锚定 listing_id，并保存必填 `market_id + country_code`、price_at_save、is_active、created_at。
- 取消收藏使用 is_active=false 软删除。
- 列表读取 listing 当前国家站价格和状态；已售出展示 Sold Out，下架展示 Unavailable 且不返回商详 URL。
- 唯一粒度为主体 + market_id + country_code + listing_id；不同国家站同一 listing 状态互不覆盖。
- 查询、PC 数量和公开收藏人数按实体 `market_id + country_code` 返回；收藏人数再叠加 listing_id。
- 切换国家只改变过滤条件，不删除、不迁移、不修改其他 Market/国家收藏记录。
- PC Account Home 可显示当前国家站真实收藏数量；移动端个人中心首页不展示 Wishlist 入口。

**Recently Viewed**：

- 进入商品详情记录 user_id/anonymous_id + market_id + country_code + listing_id + viewed_at。
- 同一主体在同一 Market/国家下同一 listing 只保留一条，再次浏览更新时间；不同国家互不覆盖。
- 容量、留存、单条删除、Clear All 和防回灌规则按专项 PRD v1.6 执行，本 PRD 不重复定义。
- browsing_history 与 browsing_history_delete_marker 均保存必填 `market_id + country_code`；查询、PC 数量、Clear All 和防回灌按两级地域隔离。
- 切换国家只改变过滤条件，不删除其他 Market/国家浏览记录；切回原国家后继续按原记录时间排序。
- PC Account Home 可显示当前国家站数量；移动端个人中心首页不展示入口。

个人中心只调服务，不在聚合页重复存商品快照或计数。

### 2.12 匿名记录复制合并

**触发条件**：未登录设备存在 anonymous_id，用户通过 login/register/oauth 首次取得 user_id。

**处理流程**：

1. 读取当前 anonymous_id 域的有效收藏和浏览记录。
2. 向 user_id 域复制；匿名原件不删除、不清空。
3. 用户域按 `market_id + country_code + listing_id` 判断冲突并按专项 PRD v1.6 幂等去重；不同地域绝不互相覆盖。
4. 写一条 anonymous_merge_log。
5. 登录完成后按 `user_id + 当前 market_id + country_code` 读取；登出后按 `anonymous_id + 当前 market_id + country_code` 读取。

**合并日志字段**：

| 字段 | 说明 |
|---|---|
| merge_id | 日志主键 |
| anonymous_id | 来源设备匿名 ID |
| user_id | 目标账户 |
| trigger_type | login / register / oauth |
| favorite_merged_count | 本次实际新增收藏数，冲突跳过不计 |
| history_merged_count | 本次实际新增浏览数，冲突跳过不计 |
| merged_at | 合并时间 |

日志 append-only，不参与业务查询。同一 anonymous_id 与 user_id 可多次产生日志，以 merged_at 区分。日志失败不回滚复制、不阻断登录，但必须告警并重试/补偿。

**共享设备边界**：匿名原件保留，因此同设备登出态可能看到此前设备级匿名收藏/浏览，本期接受该语义；不把 anonymous_id 永久绑定到任何账户，不读取其他设备匿名域。

**DSAR**：删除 user_id 时处理用户域数据及相关 merge log；匿名原件不随账户自动删除，除非全局隐私流程明确提供 anonymous_id。

---

## 三、依赖与风险

### 3.1 上下游依赖

| 依赖 | 用途 | 所有权 |
|---|---|---|
| 登录注册模块 | 账户资料、已登录改密、session、账号注销；ChangePassword 负责旧密码校验、新密码规则与写入 | 登录注册模块 |
| 订单/售后 | 状态计数、订单列表、Returns 进度 | 订单模块 |
| 地址库 | 地址列表与编辑 | 地址模块 |
| Market 模块 | 已启用 Market、国家列表、country_code→market_id 归属、关联状态、每个国家的默认语言/默认币种、Market 支持币种 | Market 模块 |
| 站点上下文/网关 | 服务端确定当前 market_id + country_code；IP 仅可推荐国家 | C 端基础框架/网关 |
| 商品系统 | listing 当前国家站价格、状态、本地化商品信息及 Market/国家可见性 | 商品模块 |
| 订阅管理 | Email 订阅状态、同意凭证、游客订阅 | 订阅模块 |
| 客服模块 | customer_inquiry 创建、查询和状态 | 客服模块 |
| 政策/CMS | 按 policy_key + market_id + country_code 返回政策版本、生效时间、本地化内容和真实 URL | 政策/CMS 模块 |
| 隐私偏好存储 | 读取、持久化和重试 `privacy_consent` 当前偏好；不触发任何实际合规动作 | 个人中心 / 用户偏好服务 |
| 隐私合规 | 后续消费已保存偏好，负责 Cookie/Do Not Sell、GPC、同意审计与 DSAR 的实际执行 | 后续隐私合规模块 |
| Google reCAPTCHA | Contact Us 人机验证 | Google 外部服务 |
| 邮件客户端/服务 | 客服回复与 DSAR 联系 | 外部/通信能力 |
| 翻译中心/message package | UI 文案与外部动态内容本地化 | 翻译平台及各数据 Owner |

### 3.2 兼容性与约束

- PC 与 Mobile Web 使用响应式页面；APP 复用移动端信息结构，但 About 额外显示 App Version。
- English、Español、繁體中文及后续启用语言的文案长度变化不得导致按钮、侧栏、政策名称和错误提示截断；必须支持文本换行。
- Policies 页面按 V5 信息结构实现 PC/Mobile 响应式展示；PRD 不约束单页、多页面或 CMS 路由，但各实现均须支持五类入口、多语言、区域隔离、加载/失败状态与返回路径。
- 当前 UI 采用从左到右布局；未来引入 RTL 语种时另做布局适配，本期不在范围。
- Google reCAPTCHA Web 与 APP 使用对应官方接入方式，但后端统一校验业务 action 和来源。
- Cookie Preferences 与 Do Not Sell/Share 必须支持鼠标、触控、键盘和辅助功能操作；本期仅保存用户偏好并显示成功反馈，不接入 GPC、Cookie 分类控制、同意审计或相关浏览器存储。
- 数据库时间字段统一保存 UTC；C 端采用设备当前时区还是事件发生时区展示仍待定，本版不得自行写死展示时区规则或新增事件时区字段。
- 键盘操作、焦点顺序、表单标签、错误提示和颜色对比应满足基础 WCAG 2.1 AA 要求。

### 3.3 主要风险

| 风险 | 影响 | 应对 |
|---|---|---|
| 订单状态映射不一致 | 数量与订单列表不一致 | 订单模块提供稳定聚合口径；个人中心不自行计算 |
| Contact Us 被刷 | 垃圾咨询、通知轰炸 | reCAPTCHA + 5次/24h + 重复内容拦截 |
| reCAPTCHA 不可用 | 用户无法提交 | 服务异常 fail-open，保留服务端限流 |
| 隐私偏好被误当作实际合规控制 | 用户以为 Cookie、广告或数据共享已被实时改变 | UI 明确仅保存偏好；代码评审禁止根据该记录启停 Cookie/SDK、改变广告共享或接入 GPC，真实动作由后续隐私合规模块交付 |
| 隐私偏好持久化重试失败 | 当前页面显示与最终记录不一致 | 记录告警并异步重试；按 `user_id + market_id + country_code + preference_key` 最后写入值幂等覆盖 |
| 匿名原件共享设备可见 | 隐私预期偏差 | 明确设备级语义；二期评估登出轮换 ID |
| 合并日志写失败 | 审计/排障缺口 | 不阻断登录，告警并补偿 |
| 外部模块故障 | 个人中心部分空白 | 分模块降级，不阻断其他功能 |
| Market/国家配置异常 | 入口显隐错误、无法确定国家站或默认偏好不合法 | 按 C 端有效国家去重计数；0 个国家不猜测、不跨站兜底并告警；切换前校验国家归属、默认语言和默认币种 |
| 跨地域数据串显 | 用户看到其他 Market/国家的收藏/浏览 | 所有列表、count 和收藏人数在服务端按实体 market_id + country_code 过滤并做回归测试 |
| 国家归属被错误改写 | 历史收藏/浏览迁到错误 Market | 地域作为发生时快照；Market 关系变更不得静默更新，必须走显式迁移评审 |
| 目标国家默认偏好配置错误 | 切换后语言或金额展示错误 | 切换前校验默认语言已启用、默认币种受归属 Market 支持；任一失败则四项均不更新并告警 |
| 翻译缺失 | 页面夹杂空白或错误语言 | 缺失统一回退 en；静态 key 上线前全量校验 |
| 政策跨国家回退 | 用户看到不适用于当前国家的条款 | 先锁定 market_id + country_code 和政策版本，再做同区域 English 回退；禁止跨国家兜底 |
| 国家切换部分成功 | 政策、订阅偏好或隐私偏好混用两个国家 | 目标区域关键数据全部成功后一次性替换；任一失败保留旧区域完整状态 |
| 旧国家缓存污染 | 切换后短暂或持续展示旧政策、订阅或隐私选择 | 所有请求与缓存键包含 market_id + country_code；切换时清理页面旧状态并显示加载态 |
| 目标国家政策配置缺失 | 入口无效或用户无法查看适用条款 | 首发门禁校验五项政策均有有效版本和真实 URL；运行时显示不可用且不可跨国兜底 |

---

## 四、版本规划

### 4.1 MVP / v1.8

- V5 全部正式页面与状态。
- Processing/Shipped/Delivered/Returns/View All 订单入口。
- Profile V5 字段；Gender 未设置为 null，不默认选中 Prefer not to say。
- Country/Region 按 C 端有效国家数量条件显示（1 个隐藏，>1 个显示）、Language/Currency、切换国家强制重置默认语言与默认币种，并同步切换政策、Email Subscriptions 与隐私偏好。
- Contact Us C 端与客户咨询后台查看/状态操作。
- Policies 五类入口、多语言、PC/Mobile 响应式展示、按 market_id + country_code 读取不同政策；About、APP Version、Log Out。
- Subscriptions 游客 Email 基础格式校验。
- Subscriptions 游客提交成功/失败 Toast：成功或重复订阅成功提示“订阅成功”，系统异常提示“系统异常，请稍后重试”，格式错误仍使用内联提示。
- 登录态 Email Subscription：开启成功提示“订阅成功”，取消成功提示“已取消订阅”，系统异常提示“系统异常，请稍后重试”并回滚。
- Cookie Preferences、Do Not Sell or Share 可操作并按用户/国家站持久化；每次切换提示 `Preference updated.`，但本期不触发实际合规动作。
- Change Password 引用登录注册模块的已登录改密流程；个人中心不承载密码字段、校验或写入。
- My Orders、Profile、Addresses 未登录访问统一跳登录并携带 `returnUrl`；Subscriptions 未登录直接展示 Email + Subscribe。
- Wishlist/Recently Viewed 及删除标记保存 market_id + country_code，并随当前国家站过滤。
- 匿名记录复制上移、匿名原件保留、anonymous_merge_log。
- United States 与 Hong Kong 首发市场；语言由多语言系统提供，缺失回退 en。

### 4.2 后续迭代

- 头像、生日、邮箱认证状态。
- Contact Us 未登录个人中心表单 Case。
- Recommended for You。
- Push/SMS、站内消息。
- 客户咨询后台内直接回复、邮件正文留痕、附件、负责人和 SLA。
- 自助 DSAR、数据导出和自助注销。
- 更多 Market、国家、币种和语种配置扩展。
- C 端时间采用设备当前时区或事件发生时区的最终展示方案。
- 共享设备匿名 ID 轮换治理。
- Cookie 同意、Do Not Sell/Share、GPC、同意审计与已保存隐私偏好的实际执行。

---

## 五、数据与埋点

### 5.1 关键埋点

| 事件 | 触发 | 关键维度 |
|---|---|---|
| account_home_view | 打开个人中心 | platform、login_state、market_id、country_code |
| account_entry_click | 点击功能入口 | entry_name、platform |
| order_status_click | 点击订单状态 | status_label |
| profile_edit_submit | 保存 Nickname/Gender | field、result |
| preference_change | 修改 Country/Region、Language、Currency | field、from、to、result |
| country_change | 保存 Country/Region | from/to market_id、from/to country_code、from/to language、from/to currency、default_reset=true、policy_refresh_result、subscription_refresh_result、privacy_refresh_result、result |
| subscription_toggle | 登录态切换订阅 | market_id、country_code、from_status、to_status、result |
| guest_subscribe_submit | 游客提交邮箱订阅 | platform、market_id、country_code、result；格式失败记录 result=invalid_email_format，不记录完整 Email |
| privacy_preference_change | 切换 Cookie/Do Not Sell 偏好 | market_id、country_code、preference_key、from、to、write_result；不记录实际合规动作 |
| policy_entry_click | 点击政策入口 | policy_key、market_id、country_code、language_code、policy_version、result |
| contact_submit | 提交咨询 | platform、result、blocked_reason |
| contact_admin_view | 后台打开咨询 | status_before |
| contact_status_change | 后台修改状态 | from、to |
| logout_confirm | 确认退出 | platform、result |
| anonymous_merge | 匿名复制合并完成 | trigger_type、favorite_count、history_count、result |

埋点不得包含完整 Message、完整 IP、密码、reCAPTCHA token 或其他不必要 PII。

### 5.2 数据所有权

| 实体 | 个人中心是否拥有 | 说明 |
|---|:---:|---|
| favorite / browsing_history / browsing_history_delete_marker | 是 | 个人化关系、行为记录与删除抑制；均保存 market_id + country_code |
| user_preference | 是 | 登录态当前 market_id/country_code/language/currency；国家切换使用目标国家默认语言/币种，不恢复历史手动值 |
| device_pref_store | 逻辑实体 | 客户端当前区域与显示偏好，不是 DB 表；缓存键包含 market_id + country_code |
| privacy_consent | 是 | 登录用户当前隐私偏好；按 user_id + market_id + country_code + preference_key 保存布尔值、updated_at、source；本期只记录，不触发实际合规动作 |
| device_consent_store | 否 | 本期 Privacy & Data 不支持游客或设备级隐私设置；后续由隐私合规模块定义 |
| anonymous_merge_log | 是 | 匿名复制事件日志 |
| user / listing / market / country / market_currency / address | 否 | 外部引用；Market、国家与币种配置归 Market 模块 |
| customer_inquiry | 否 | 客服模块拥有 |
| email_subscription | 否 | 订阅管理模块拥有；状态与同意凭证须按 subject + market_id + country_code 隔离 |
| policy_document / policy_assignment | 否 | 政策/CMS 模块拥有；按 policy_key + market_id + country_code 返回适用版本与本地化 URL |

---

## 六、权限与角色矩阵

| 功能 | 未登录访客 | 已登录买家 | 客服/运营 |
|---|:---:|:---:|:---:|
| 完整个人中心首页 | 登录引导 | 可用 | 非后台职责 |
| Wishlist/Recently Viewed 设备能力 | 可通过专项入口使用 | 可用并跨端同步 | — |
| Profile / Orders / Addresses | 跳登录注册模块并携带精确 `returnUrl` | 可用 | — |
| Subscriptions | 直接进入游客 Email + Subscribe 页，不跳登录 | 进入账户邮箱订阅开关页 | 订阅后台另管 |
| Privacy & Data 个人中心页 | 本期不可用 | 可用；Cookie/Do Not Sell 可操作并记录偏好，不触发实际合规动作 | 后续合规后台另管 |
| Contact Us 个人中心表单 | 本期不可用 | 可用 | 查看 customer_inquiry |
| Policies / About 个人中心入口 | 本期不展示 | 可用 | — |
| 客户咨询后台 | 不可用 | 不可用 | 可查询、查看、改状态、唤起邮件 |

---

## 七、附录

### 7.1 设计稿索引

| 功能 | Mobile Web / APP | PC Web / 后台 |
|---|---|---|
| 个人中心首页 | V5-移动端-个人中心-响应式统一版 | V5-PC-个人中心-响应式统一版 |
| 退出确认/退出后 | V5-移动端-退出登录-确认 / 退出登录后 | V5-PC-退出登录-确认 / 退出登录后 |
| Profile | V5-移动端-Profile / 编辑昵称 / 选择性别 | V5-PC-Profile |
| Country/Region | V5-移动端-选择国家地区 | V5-PC-CountryRegion |
| Language | V5-移动端-选择语言 | V5-PC-Language |
| Currency | V5-移动端-选择币种 / 切换市场-币种回退Case（语义升级为语言+币种默认重置） | V5-PC-Currency |
| Addresses | 跳地址库模块，移动端页面不在本文件 | V5-PC-Addresses |
| Subscriptions 登录态 | V5-移动端-Subscriptions | V5-PC-Subscriptions |
| Subscriptions 游客态 | V5-移动端-Subscriptions-未登录Case | V5-PC-Subscriptions-未登录Case |
| Privacy & Data | V5-移动端-PrivacyData | V5-PC-PrivacyData |
| Contact Us | V5-移动端-ContactUs | V5-PC-ContactUs |
| Policies | V5-移动端-Policies | V5-PC-Policies |
| About | V5-Mobile Web-About / V5-APP-About | V5-PC-About |
| 客户咨询后台 | — | looply-客户咨询-antd-原型-v2.html |

### 7.2 C 端字段映射自检

| 页面 | PRD 字段 | 原型实际 | 结果 |
|---|---|---|---|
| Profile | Email/Nickname/Gender/Change Password/Log Out；Gender null 显示 Not set；Change Password 跳登录注册模块 | V5 覆盖字段与已设置 Case | UI 一致；未设置 Case 与外部改密边界由 PRD 补充 |
| Subscriptions 登录态 | Subscription email + Email Subscription switch | 一致 | 一致 |
| Subscriptions 游客态 | Email + Subscribe + consent note | Mobile/PC 均已设计 | 一致 |
| Privacy & Data | Manage Data/Cookie Preferences/Do Not Sell；后两者可操作、按当前国家站读取和保存偏好，切换后提示 Preference updated | V5 固定顺序平铺，表示三模块展示 Case | UI 一致；偏好持久化与不触发实际合规动作由 PRD 补充 |
| Contact Us | Full Name/Email*/Message*/Send Message/reCAPTCHA | 一致 | 一致 |
| Policies | 五类固定入口；政策版本与 URL 按 market_id + country_code 返回 | V5 覆盖 PC/Mobile 五项列表 | UI 一致；动态地域规则由 PRD 补充 |
| About | 品牌文案；仅 APP Version | 已拆 Mobile Web/APP/PC | 一致 |
| Account Home | V5 订单标签；Country/Region 条件入口；PC Wishlist/Recently Viewed | 原型展示 >1 个有效国家 Case；1 个国家时隐藏该行/导航项 | 规则已覆盖 |
| Country/Region | United States / Hong Kong + Cancel/Save | 移动端 Sheet、PC 页面覆盖 >1 个有效国家 Case；1 个国家不进入页面 | 规则已覆盖 |
| Language | English / Español / 繁體中文单选 + Cancel/Save | 移动端 Sheet、PC 页面均覆盖 | 一致 |
| Currency | USD $ / HKD HK$ 单选 + Cancel/Save | 移动端 Sheet、PC 页面均覆盖 | 一致 |
| 国家切换默认偏好重置 | Hong Kong + 默认语言 + 默认币种 + 重置提示 | 复用移动端 Case 页面结构，文案按 2.3 更新 | 规则已覆盖 |
| Log Out | 确认、取消、退出后 Sign In | Mobile/PC 确认与退出后 Case | 一致 |

### 7.3 客户咨询后台字段映射自检

| 区域 | PRD 定义 | 原型实际 | 结果 |
|---|---|---|---|
| 列表 | 编号、时间、姓名、邮箱、内容、状态、操作 | columns 完整对应 | 一致 |
| 搜索 | 编号/姓名/邮箱/内容关键词 | 输入框 placeholder 对应 | 一致 |
| 状态筛选 | all/new/read/resolved | Select 四项 | 一致 |
| 详情 | 用户信息、来源、Message、编号、时间、最后更新 | Drawer 对应 | 一致 |
| 操作 | 查看、邮件回复、解决、重新打开 | 原型对应 | 一致 |
| 状态流转 | new→read→resolved；resolved→read | 原型对应 | 一致 |
| 页面状态 | 数据、零数据、无匹配、错误 | 原型状态切换器均覆盖 | 一致 |

### 7.4 关联文档

- 功能清单：`~/Desktop/个人中心/需求分析/looply-个人中心-功能清单-v1.8.md`
- ER：`~/Desktop/个人中心/实体关系图/looply-个人中心实体关系图-v1.6.svg`
- C 端原型：`~/Desktop/个人中心/原型/looply-个人中心-APP-v5.pen`
- 后台原型：`~/Desktop/个人中心/原型/looply-客户咨询-antd-原型-v2.html`
- 收藏与浏览历史专项 PRD：`~/Desktop/个人中心/PRD/looply-收藏与浏览历史-PRD-v1.6.md`

> 本 PRD 不包含 API 路径、HTTP 方法或参数清单；接口设计由技术方案另行定义。

### 7.5 v1.8 验收口径

1. Policies 在 PC Web、Mobile Web、APP 均按 V5 信息结构展示，长译文可换行且无横向溢出；页面数量和路由形态不作为验收项。
2. 五类政策入口顺序固定；United States 与 Hong Kong 可返回不同政策版本、生效时间和真实 URL，不要求共用政策文件。
3. 同一国家缺少当前语言译文时，只能回退该国家同一版本 English；不得显示其他国家政策。
4. 目标国家某政策缺少有效版本或真实 URL 时，该项不可点击并显示本地化不可用状态；不得生成空链接。
5. 切换国家成功后，语言、币种、政策、Email 订阅偏好、Cookie Preferences 与 Do Not Sell 偏好一次性切到目标国家；切回后恢复该国家已保存的区域数据。
6. 区域切换任一关键配置失败时，页面继续展示切换前完整状态并提示重试，不出现两个国家的混合数据。
7. Privacy & Data 固定平铺 Manage Your Data、Cookie Preferences、Do Not Sell or Share；Performance、Functional、Targeting 和 Do Not Sell 均可操作，Strictly Necessary 固定 ON 且不可关闭。每次操作按 `user_id + market_id + country_code + preference_key` 持久化，并显示 `Preference updated.`；不触发 Cookie、广告、出售/共享、GPC 或其他实际合规动作。
8. 未登录订阅 Email 为空、包含多个 `@`、`@` 前后为空、含空格、域名无点或域名以点开头/结尾时，前端阻止提交并显示本地化格式错误。
9. Gender 为 `null` 时 Profile 显示本地化 `Not set`，进入编辑态后三项均未选中；`Prefer not to say` 只在用户主动选择并保存后展示。
10. 所有政策、订阅偏好和隐私偏好请求及缓存均按 `market_id + country_code` 隔离，服务端不接受只依赖语言或前端缓存推断国家的结果。
11. 游客首次订阅成功或重复订阅幂等成功时，均显示 Toast “订阅成功”，停留当前页且不重复发送请求。
12. 游客订阅因网络异常、超时或服务端失败时，显示 Toast “系统异常，请稍后重试”，保留 Email 并恢复 Subscribe 可点击；格式错误只显示输入框内联提示，不显示 Toast。
13. 登录态 Email Subscription 从关闭切换为开启时提示“订阅成功”，从开启切换为关闭时提示“已取消订阅”；网络异常、超时或服务端失败时回滚并提示“系统异常，请稍后重试”。
14. Privacy & Data 每次可操作开关切换均显示 `Preference updated.`，不显示失败 Toast 或回滚；持久化异常由服务端告警、异步重试及幂等补偿处理。
15. 已登录用户点击 Change Password 后跳转登录注册模块 `ChangePassword`，必须先验证旧密码；个人中心不得出现密码输入、验证码或密码写入逻辑。
16. 未登录用户从页面点击或直接访问 My Orders、任一订单状态、Profile、Addresses 时，均跳转登录注册模块并保留精确内部 `returnUrl`；登录成功后自动进入原目标页。未登录进入 Subscriptions 时不跳登录，直接展示 Email + Subscribe；登录态进入时展示账户邮箱和 Email Subscription 开关。
