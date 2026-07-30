# Looply 个人中心 PRD

**文档版本**：v1.1  
**日期**：2026-07-27  
**模块**：个人中心（Account / Me）  
**覆盖端**：PC Web、Mobile Web、APP、运营后台  
**状态**：评审稿  

**输入基线**：

| 类型 | 文件 | 采用口径 |
|---|---|---|
| 功能范围 | `looply-个人中心-功能清单-v1.7.md` | 复用账户、匿名记录及平台差异；市场相关旧口径由本 PRD 覆盖 |
| 数据模型 | `looply-个人中心实体关系图-v1.5.svg` | `market_id`、Market 外部配置关系、`anonymous_merge_log` |
| C 端原型 | `looply-个人中心-APP-v5.pen` | 页面、字段、平台差异、登录态与多市场设置以此为准 |
| 运营后台 | `looply-客户咨询-antd-原型-v2.html` | 客户咨询列表、详情、状态与操作以此为准 |
| 子模块 PRD | `looply-收藏与浏览历史-PRD-v1.4.md` | 收藏、浏览、匿名合并与 listing 规则以最新版为准 |
| 翻译规则 | `prd-translation-card-placement-product-sync.md` | 静态 UI 与动态业务资源分流；明确资源卡片归属 |

> 冲突优先级：本 PRD 已确认决策 > V5 原型（前端页面、字段、文案、交互、平台差异与登录态）> ER v1.5（实体、字段、关系与数据规则）> 收藏与浏览历史 PRD v1.4 > 客户咨询后台原型 v2 > 功能清单 v1.7 > 旧资料。前端范围按 V5；旧资料中的“仅美国、Region 无入口、USD/EUR 固定选项”、独立 Settings 壳、匿名合并后清空等口径不再沿用。

---

## 一、概述

### 1.1 背景与目标

个人中心是买家查看账户信息、订单进度、偏好、隐私选择和支持信息的统一入口，也是收藏与浏览历史等个人化数据能力的导航与聚合层。

本期目标：

1. 用统一的信息架构承载移动端与 PC 账户入口，减少重复 Settings 层级。
2. 聚合订单、收藏和浏览历史信息，但不复制外部模块业务数据。
3. 提供 Profile、Country/Region、Language、Currency、Email 订阅和隐私选择等基础账户配置。
4. 提供 Contact Us 表单及运营后台客户咨询查看能力。
5. 支持未登录设备级收藏/浏览，并在登录时复制到用户域且保留匿名原件。
6. 首期支持 United States 与 Hong Kong 市场，并根据用户选择的市场加载可售 listing、可用币种和适用政策内容。
7. 合规能力按市场适用性执行；美国市场覆盖 CAN-SPAM、CCPA/CPRA、GPC 和 Cookie 分类控制，Hong Kong 市场规则由政策/合规模块提供。

### 1.2 本期范围

- 移动端个人中心首页、PC Account Home 与左侧导航。
- 订单状态入口：Processing、Shipped、Delivered、Returns、View All。
- Profile：Email、Nickname、Gender、Change Password、Log Out。
- Country/Region、Language、Currency；可选项分别读取 Market 模块和多语言系统配置。
- Subscriptions 登录态开关与游客邮箱订阅 Case。
- Privacy & Data 三模块平铺。
- Contact Us C 端提交与客户咨询运营后台。
- Policies、About Looply、APP 版本号。
- Wishlist / Recently Viewed 入口、当前市场数量聚合及与专项模块的衔接。
- anonymous_id、匿名记录复制合并和合并日志。

### 1.3 不做什么

- 不做独立 Settings 页面或右上角齿轮入口。
- 不做待付款入口；支付前状态属于结算/弃单，不属于订单。
- Returns 仅查看进度，不提供买家自助申请退货/退款。
- 不做头像、生日、个人简介、邮箱认证状态或邮箱换绑。
- 不做 Recommended for You、站内消息、支付方式管理、Push/SMS 订阅。
- 不做用户端自助导出数据或自助注销；本期邮件申请、运营处理。
- 不在个人中心拥有订单、地址、订阅、客户咨询、商品和政策正文的数据表。
- 不将 Google reCAPTCHA token、限流计数器写入客户咨询业务表。
- 不在 favorite / browsing_history 重复保存 `market_id`；市场由关联 listing 的 `market_id` 唯一确定。
- 本版不确定订单、付款、收藏、浏览等时间在 C 端采用设备时区还是事件时区；不新增事件时区字段。

### 1.4 用户角色

| 角色 | 说明 |
|---|---|
| 已登录买家 | 使用完整个人中心、账户级订单/偏好/隐私与咨询功能 |
| 未登录访客 | 看到 Signed Out / Sign In 引导；可通过独立 Subscriptions 游客页订阅邮箱；设备级收藏/浏览由专项入口承载 |
| 客服/运营 | 在客户咨询后台查询、查看、标记状态并通过邮件客户端回复 |
| 合规人员 | 依赖隐私同意审计、GPC、Do Not Sell/Share 与 DSAR 规则，不直接使用本期客户咨询后台角色能力 |

### 1.5 核心场景

1. 买家进入个人中心，快速查看订单各状态数量。
2. PC 买家查看 Wishlist / Recently Viewed 数量并进入对应能力。
3. 买家修改 Nickname、Gender、Country/Region、Language 或 Currency。
4. 登录用户开启/关闭 Email 营销订阅；访客直接填写邮箱订阅。
5. 用户查看和修改 Cookie Preferences、Do Not Sell/Share 选择。
6. 用户通过 Contact Us 提交咨询，运营在后台查看并邮件回复。
7. 未登录用户产生收藏/浏览，登录后系统复制到用户域，同时保留匿名原件并记录合并日志。
8. 用户从 United States 切换至 Hong Kong 后，仅看到 Hong Kong listing 对应的收藏和浏览历史；切回后原市场数据仍在。

### 1.6 全局页面流转

```text
个人中心首页
├─ 订单状态 / View All → 订单模块列表或详情
├─ Profile → Nickname Sheet / Gender Sheet / Change Password
├─ Addresses → 地址库模块
├─ Country/Region → 市场选择
├─ Language → 语言选择
├─ Currency → 币种选择
├─ Subscriptions → 登录态开关页
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
| market / market_id | Market 模块配置的经营市场及内部唯一标识；用户端统一显示为 Country/Region |
| listing | 用户前台可见、可下单的渠道商品单元；每条 listing 归属一个 market_id，收藏与浏览均锚定 listing_id |
| anonymous_id / looply_aid | 设备/浏览器级假名标识，承载未登录收藏、浏览和设备偏好 |
| 用户域 | 以 user_id 为主体的账户级数据 |
| 匿名域 | 以 anonymous_id 为主体的设备级数据 |
| 复制上移 | 登录时将匿名域记录复制到用户域，匿名原件保留 |
| customer_inquiry | 客服模块拥有的客户咨询记录 |
| Email Subscription | 营销邮件订阅，不影响订单、支付和账户安全等事务邮件 |

### 1.8 多语言、多国家与翻译归属

首期启用 United States 与 Hong Kong。Country/Region 选项读取 Market 模块中已启用市场，用户端展示市场名称，内部保存 `market_id`；不得在个人中心写死仅美国。Language 选项由多语言系统统一提供，语言不与市场一一绑定；V5 示例为 English、Español、繁體中文，译文缺失统一回退 English。Currency 选项读取当前市场配置，切换市场后若原币种不受支持，自动改为目标市场默认币种并明确提示。

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
| 政策正文 | 标题、正文、富文本 | 外部动态业务内容 | 本模块不注册卡片 | 外部政策/CMS 模块定义 | 外部模块定义 | 外部模块定义 | 政策正文页 | 同一政策版本可含 Global/US/Hong Kong 适用章节；返回当前市场适用内容与本地化 URL |
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
| 配置入口 | Profile、Addresses、Country/Region、Language、Currency、Subscriptions | 左侧栏 ACCOUNT SETTINGS 同顺序分组 |
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
| Wishlist | 当前市场收藏数量和说明 | 数量实时调收藏服务并按 listing.market_id 过滤；可显示 24 等真实数量 |
| Recently Viewed | 当前市场最近浏览数量和说明 | 调浏览历史服务并按 listing.market_id 过滤；点击进入专项页面 |

**状态变体**：已登录默认态、订单计数加载态、部分数据读取失败、Signed Out、退出确认。

**UI 关联**：`V5-移动端-个人中心-响应式统一版`、`V5-PC-个人中心-响应式统一版`、`V5-移动端-退出登录后`、`V5-PC-退出登录后`。

### 2.2 Profile

**功能描述**：展示基础账户资料并支持编辑 Nickname、Gender；密码修改跳用户中心。

**页面字段**：

| 字段/操作 | 控件 | 必填 | 规则 |
|---|---|:---:|---|
| Email | 只读文本 | — | 展示账户邮箱；本期无认证徽章、无换绑 |
| Nickname | 输入框 | 是 | 1–24 字位簇；规则见下表 |
| Gender | 单选 | 否 | Female / Male / Prefer not to say |
| Change Password | 跳转行 | — | 跳用户中心密码流程 |
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

**操作流程**：移动端点击 Nickname/Gender 打开底部 Sheet，Save 后回写；PC 点击 Edit 进入对应编辑态。保存失败保留输入并显示错误，不能静默回滚成旧值。

**本期不做**：头像、生日、Bio、邮箱认证状态。

**UI 关联**：`V5-移动端-Profile`、`V5-PC-Profile`、`V5-移动端-编辑昵称`、`V5-移动端-选择性别`。

### 2.3 Country/Region、Language 与 Currency

**功能描述**：管理用户当前市场、界面语言与展示/结算币种。用户端标签固定为 `Country/Region`，内部字段固定为 `market_id`，不得继续使用含义模糊的 `region` 作为市场主键。

| 偏好 | 选项来源 / V5 示例 | 默认 | 页面行为 |
|---|---|---|---|
| Country/Region | Market 模块已启用市场；示例 United States、Hong Kong | 已保存 market_id；无值时使用 Market 模块默认市场 | 单选后 Save；切换站点市场上下文并刷新市场相关数据 |
| Language | 多语言系统已启用语言；示例 English、Español、繁體中文 | 已保存语言；无值时 Accept-Language 协商，无法匹配回退 English | 单选后 Save；刷新静态 UI 和外部本地化内容 |
| Currency | 当前市场支持币种；示例 USD $、HKD HK$ | 已保存且受当前市场支持则沿用，否则使用该市场默认币种 | 单选后 Save；刷新金额展示 |

**市场切换规则**：

1. Country/Region 列表只展示 Market 模块中 `enabled=true` 的市场；市场名称由 Market 模块返回，个人中心不维护国家枚举。
2. 切换后更新用户/设备当前 `market_id`，商品列表、Wishlist、Recently Viewed 及其 PC 数量均按 `listing.market_id = 当前 market_id` 查询。
3. 其他市场的收藏和浏览记录只隐藏、不删除；用户切回原市场后恢复展示。
4. 若当前 Currency 不在目标市场支持列表中，自动切换为目标市场默认币种，并提示 `Country/region updated. Currency changed to {currency}.`；若仍受支持则保持原币种。
5. Language 与市场解耦；切换 Country/Region 不自动修改 Language。
6. 地址选择、格式和可配送范围由地址模块控制；个人中心不根据 market_id 改写地址数据。

登录用户以 `user_preference` 为跨端权威值；设备偏好用于首次体验和缓存。登录时账户无偏好则设备值 seed；账户已有值则账户优先并回写设备。

保存或市场上下文切换失败时保留原生效值并提示重试；不允许 UI 已切换但服务端保存失败后长期不一致。Market 模块返回空列表、目标市场停用或币种配置异常时，不切换当前市场并记录配置告警。

**UI 关联**：`V5-移动端-选择国家地区`、`V5-PC-CountryRegion`、`V5-移动端-选择语言`、`V5-PC-Language`、`V5-移动端-选择币种`、`V5-PC-Currency`、`V5-移动端-切换市场-币种回退Case`。

### 2.4 Subscriptions

**功能描述**：管理一个 Email 营销订阅总状态。状态和同意凭证归订阅管理模块，个人中心只提供前端入口。

**登录态**：

| 元素 | 规则 |
|---|---|
| Subscription email | 只读显示账户邮箱 |
| Email Subscription | subscribed 时 ON，unsubscribed 时 OFF |
| 说明 | 关闭只影响营销邮件，事务邮件不受影响 |

开关切换采用即时反馈；写入失败时回滚原状态并提示 `Update failed, please retry`。进入页面拉取失败时显示重试，不渲染一个可能错误的开关值。

**游客态**：

| 字段 | 必填 | 校验 |
|---|:---:|---|
| Email | 是 | trim；标准邮箱格式；长度上限由订阅模块统一约束 |
| Subscribe | — | 提交中 loading；重复订阅幂等成功 |

游客提交来源记为 preference。成功后显示订阅成功反馈；失败保留 Email。个人中心不存游客订阅状态。

**订阅状态枚举**：

| 枚举值 | 含义 | 触发时机 | 适用场景 |
|---|---|---|---|
| subscribed | 已同意接收营销邮件 | 游客 Subscribe 或登录用户开启开关 | 可发送营销邮件 |
| unsubscribed | 已退订营销邮件 | 登录用户关闭开关或邮件退订 | 仅保留事务邮件 |

**UI 关联**：`V5-移动端-Subscriptions`、`V5-PC-Subscriptions`、`V5-移动端-Subscriptions-未登录Case`、`V5-PC-Subscriptions-未登录Case`。

### 2.5 Privacy & Data

**功能描述**：在一个页面按固定顺序平铺 Manage Your Data、Cookie Preferences、Do Not Sell or Share My Personal Information。

**模块一：Manage Your Data**：

| 区块 | 展示与处理 |
|---|---|
| Request a Copy of Your Data | 纯文案，引导从注册邮箱联系 `privacy@looply.com`；人工核验并在 45 天内响应 |
| Delete Account | 纯文案，引导邮件申请；运营后台执行；本期无自助按钮 |

账号注销执行后立即匿名化 PII，无冷静期、不可恢复；交易记录按法律要求脱敏保留。账户删除不自动清空设备匿名域，除非全局隐私流程同时提供 anonymous_id。

**模块二：Cookie Preferences**：

| UI 分类 | 数据字段 | 默认 | 是否可关闭 | 说明 |
|---|---|---|:---:|---|
| Strictly Necessary | 不作为可选字段 | ON | 否 | 登录、结算、安全和 looply_aid 所需 |
| Performance | cookie_analytics | true | 是 | 性能和体验分析 |
| Functional | cookie_functional | true | 是 | 偏好记忆与非广告个性化 |
| Targeting | cookie_marketing | true | 是 | 广告和营销定向 |

选择作用于当前浏览器/设备；登录时设备与账户同意取更保护用户的一侧，任一侧关闭则账户侧关闭，并回写当前设备。

**模块三：Do Not Sell or Share**：`dns_opt_out=false` 表示未退出；用户开启后写 true，停止出售或用于跨情境行为广告共享。该选择独立于 Cookie 开关；即使 Targeting 仍为 ON，也不得继续执行被用户退出的共享行为。

**GPC**：检测到浏览器 GPC 信号时自动视为 opt-out，写入 `gpc_detected=true`、`dns_opt_out=true`、`consent_source=GPC`。前端无独立 GPC 开关。

同意读取失败时不得把用户已有的退出选择重置为默认值；保存失败时回滚 UI 并提示。审计历史由全局合规能力保存，个人中心 ER 只表示当前态。

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

**功能描述**：不分 POLICIES/LEGAL 组，平铺五项固定入口。

| 顺序 | 文件 | 说明 |
|---:|---|---|
| 1 | Privacy Policy | 数据收集和使用 |
| 2 | Terms of Service | Marketplace 条款与账户规则 |
| 3 | Shipping & Delivery | 配送方式、时效和履约 |
| 4 | Returns & Refunds | 退货窗口和退款处理 |
| 5 | Accessibility Statement | 无障碍浏览与购物支持 |

个人中心只维护入口名称、摘要和目标 URL，不拥有正文。五项政策各自只维护一个当前版本，不因市场拆成多份平行文件；同一版本可包含 Global、United States、Hong Kong 等适用章节，由政策/CMS 模块根据当前 `market_id` 返回适用内容、锚点或 URL。目标 URL 缺失时不得渲染可点击空链接；读取失败显示重试。Cookie Policy 不在该五项列表中。

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

详细列表、卡片、筛选、清理和空态沿用专项 PRD v1.4；本节只定义个人中心与 ER v1.5 必须一致的多市场衔接规则。

**Wishlist**：

- 收藏主体为 user_id 或 anonymous_id，二选一。
- 收藏锚定 listing_id，保存 price_at_save、is_active、created_at。
- 取消收藏使用 is_active=false 软删除。
- 列表读取 listing 当前价格和状态；已售出/下架展示失效态。
- 查询和 PC 数量只返回 `listing.market_id = 当前 market_id` 的记录；favorite 不重复保存 market_id。
- 切换市场只改变过滤条件，不删除、不迁移、不修改其他市场收藏记录。
- PC Account Home 可显示当前市场真实收藏数量；移动端个人中心首页不展示 Wishlist 入口。

**Recently Viewed**：

- 进入商品详情记录 user_id/anonymous_id + listing_id + viewed_at。
- 同一主体同一 listing 只保留一条，再次浏览更新时间。
- 容量、留存、单条删除、Clear All 和防回灌规则按专项 PRD v1.4 执行，本 PRD 不重复定义。
- 查询和 PC 数量只返回 `listing.market_id = 当前 market_id` 的记录；browsing_history 不重复保存 market_id。
- 切换市场只改变过滤条件，不删除其他市场浏览记录；切回原市场后继续按原记录时间排序。
- PC Account Home 可显示当前市场数量；移动端个人中心首页不展示入口。

个人中心只调服务，不在聚合页重复存商品快照或计数。

### 2.12 匿名记录复制合并

**触发条件**：未登录设备存在 anonymous_id，用户通过 login/register/oauth 首次取得 user_id。

**处理流程**：

1. 读取当前 anonymous_id 域的有效收藏和浏览记录。
2. 向 user_id 域复制；匿名原件不删除、不清空。
3. 用户域撞同 listing 时按专项 PRD v1.4 幂等去重；市场由 listing_id 隐式确定，不另按 market_id 建合并分支。
4. 写一条 anonymous_merge_log。
5. 登录完成后只按 user_id 读取；登出后按当前 anonymous_id 读取；两种主体查询均叠加当前 listing.market_id 过滤。

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
| 用户中心 | 账户资料、密码、session、账号注销 | 用户中心 |
| 订单/售后 | 状态计数、订单列表、Returns 进度 | 订单模块 |
| 地址库 | 地址列表与编辑 | 地址模块 |
| Market 模块 | 已启用市场、市场名称、默认币种和支持币种列表 | Market 模块 |
| 商品系统 | listing 当前价格、状态、本地化商品信息及 listing.market_id | 商品模块 |
| 订阅管理 | Email 订阅状态、同意凭证、游客订阅 | 订阅模块 |
| 客服模块 | customer_inquiry 创建、查询和状态 | 客服模块 |
| 隐私合规 | GPC、同意审计、DSAR 编排 | 合规/用户中心 |
| Google reCAPTCHA | Contact Us 人机验证 | Google 外部服务 |
| 邮件客户端/服务 | 客服回复与 DSAR 联系 | 外部/通信能力 |
| 翻译中心/message package | UI 文案与外部动态内容本地化 | 翻译平台及各数据 Owner |

### 3.2 兼容性与约束

- PC 与 Mobile Web 使用响应式页面；APP 复用移动端信息结构，但 About 额外显示 App Version。
- English、Español、繁體中文及后续启用语言的文案长度变化不得导致按钮、侧栏、政策名称和错误提示截断；必须支持文本换行。
- 当前 UI 采用从左到右布局；未来引入 RTL 语种时另做布局适配，本期不在范围。
- Google reCAPTCHA Web 与 APP 使用对应官方接入方式，但后端统一校验业务 action 和来源。
- GPC 仅适用于支持该信号的浏览器；不支持时不展示错误，仍允许用户手动 Do Not Sell/Share。
- 浏览器禁用可选 Cookie 时不得影响登录、订单、结算和安全所需的 Strictly Necessary 能力。
- 数据库时间字段统一保存 UTC；C 端采用设备当前时区还是事件发生时区展示仍待定，本版不得自行写死展示时区规则或新增事件时区字段。
- 键盘操作、焦点顺序、表单标签、错误提示和颜色对比应满足基础 WCAG 2.1 AA 要求。

### 3.3 主要风险

| 风险 | 影响 | 应对 |
|---|---|---|
| 订单状态映射不一致 | 数量与订单列表不一致 | 订单模块提供稳定聚合口径；个人中心不自行计算 |
| Contact Us 被刷 | 垃圾咨询、通知轰炸 | reCAPTCHA + 5次/24h + 重复内容拦截 |
| reCAPTCHA 不可用 | 用户无法提交 | 服务异常 fail-open，保留服务端限流 |
| Cookie 同意被登录覆盖 | 合规选择被削弱 | 登录合并取更保护一侧 |
| 匿名原件共享设备可见 | 隐私预期偏差 | 明确设备级语义；二期评估登出轮换 ID |
| 合并日志写失败 | 审计/排障缺口 | 不阻断登录，告警并补偿 |
| 外部模块故障 | 个人中心部分空白 | 分模块降级，不阻断其他功能 |
| Market 配置异常 | 无法切换市场或币种不合法 | 切换前校验 enabled 市场和支持币种；异常保留原市场并告警 |
| 跨市场数据串显 | 用户在 Hong Kong 看到 United States listing 收藏/浏览 | 所有列表和 count 在服务端按 listing.market_id 过滤并做回归测试 |
| 币种与市场不兼容 | 金额展示或结算币种错误 | 切换市场时校验，必要时回退目标市场默认币种并提示 |
| 翻译缺失 | 页面夹杂空白或错误语言 | 缺失统一回退 en；静态 key 上线前全量校验 |

---

## 四、版本规划

### 4.1 MVP / v1.1

- V5 全部正式页面与状态。
- Processing/Shipped/Delivered/Returns/View All 订单入口。
- Profile V5 字段。
- Country/Region、Language/Currency、市场币种回退、Email Subscriptions、Privacy & Data。
- Contact Us C 端与客户咨询后台查看/状态操作。
- Policies、About、APP Version、Log Out。
- Wishlist/Recently Viewed 按 listing.market_id 随当前市场过滤。
- 匿名记录复制上移、匿名原件保留、anonymous_merge_log。
- United States 与 Hong Kong 首发市场；语言由多语言系统提供，缺失回退 en。

### 4.2 后续迭代

- 头像、生日、邮箱认证状态。
- Contact Us 未登录个人中心表单 Case。
- Recommended for You。
- Push/SMS、站内消息。
- 客户咨询后台内直接回复、邮件正文留痕、附件、负责人和 SLA。
- 自助 DSAR、数据导出和自助注销。
- 更多市场、币种和语种配置扩展。
- C 端时间采用设备当前时区或事件发生时区的最终展示方案。
- 共享设备匿名 ID 轮换治理。

---

## 五、数据与埋点

### 5.1 关键埋点

| 事件 | 触发 | 关键维度 |
|---|---|---|
| account_home_view | 打开个人中心 | platform、login_state、market_id |
| account_entry_click | 点击功能入口 | entry_name、platform |
| order_status_click | 点击订单状态 | status_label |
| profile_edit_submit | 保存 Nickname/Gender | field、result |
| preference_change | 修改 Country/Region、Language、Currency | field、from、to、result |
| market_change | 保存 Country/Region | from_market_id、to_market_id、currency_fallback、result |
| subscription_toggle | 登录态切换订阅 | from_status、to_status、result |
| guest_subscribe_submit | 游客提交邮箱订阅 | platform、result |
| privacy_preference_change | Cookie/Do Not Sell 变更 | preference、from、to、source |
| contact_submit | 提交咨询 | platform、result、blocked_reason |
| contact_admin_view | 后台打开咨询 | status_before |
| contact_status_change | 后台修改状态 | from、to |
| logout_confirm | 确认退出 | platform、result |
| anonymous_merge | 匿名复制合并完成 | trigger_type、favorite_count、history_count、result |

埋点不得包含完整 Message、完整 IP、密码、reCAPTCHA token 或其他不必要 PII。

### 5.2 数据所有权

| 实体 | 个人中心是否拥有 | 说明 |
|---|:---:|---|
| favorite / browsing_history | 是 | 个人化关系与行为记录 |
| user_preference | 是 | 登录态 market_id/language/currency |
| device_pref_store | 逻辑实体 | 客户端设备偏好，不是 DB 表 |
| privacy_consent | 是 | 当前账户隐私选择；审计历史由全局合规能力拥有 |
| device_consent_store | 逻辑实体 | 当前设备隐私选择，不是 DB 表 |
| anonymous_merge_log | 是 | 匿名复制事件日志 |
| user / listing / market / market_currency / address | 否 | 外部引用；市场与币种配置归 Market 模块 |
| customer_inquiry | 否 | 客服模块拥有 |
| email_subscription | 否 | 订阅管理模块拥有 |

---

## 六、权限与角色矩阵

| 功能 | 未登录访客 | 已登录买家 | 客服/运营 |
|---|:---:|:---:|:---:|
| 完整个人中心首页 | 登录引导 | 可用 | 非后台职责 |
| Wishlist/Recently Viewed 设备能力 | 可通过专项入口使用 | 可用并跨端同步 | — |
| Profile / Orders / Addresses | 不可用 | 可用 | — |
| 登录态 Subscriptions 开关 | 不可用 | 可用 | 订阅后台另管 |
| 游客邮箱订阅页 | 可用 | 可用但优先登录态页 | — |
| Privacy & Data 个人中心页 | 本期不可用 | 可用 | 合规后台另管 |
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
| Currency | V5-移动端-选择币种 / 切换市场-币种回退Case | V5-PC-Currency |
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
| Profile | Email/Nickname/Gender/Change Password/Log Out | 一致 | 一致 |
| Subscriptions 登录态 | Subscription email + Email Subscription switch | 一致 | 一致 |
| Subscriptions 游客态 | Email + Subscribe + consent note | Mobile/PC 均已设计 | 一致 |
| Privacy & Data | Manage Data/Cookie Preferences/Do Not Sell | 固定顺序平铺 | 一致 |
| Contact Us | Full Name/Email*/Message*/Send Message/reCAPTCHA | 一致 | 一致 |
| Policies | 五项固定政策 | 一致 | 一致 |
| About | 品牌文案；仅 APP Version | 已拆 Mobile Web/APP/PC | 一致 |
| Account Home | V5 订单标签；Country/Region 入口；PC Wishlist/Recently Viewed | 一致 | 一致 |
| Country/Region | United States / Hong Kong + Cancel/Save | 移动端 Sheet、PC 页面均覆盖 | 一致 |
| Language | English / Español / 繁體中文单选 + Cancel/Save | 移动端 Sheet、PC 页面均覆盖 | 一致 |
| Currency | USD $ / HKD HK$ 单选 + Cancel/Save | 移动端 Sheet、PC 页面均覆盖 | 一致 |
| 市场切换币种回退 | Hong Kong + HKD HK$ + 回退提示 | 移动端 Case 已覆盖 | 一致 |
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

- 功能清单：`~/Desktop/个人中心/需求分析/looply-个人中心-功能清单-v1.7.md`
- ER：`~/Desktop/个人中心/实体关系图/looply-个人中心实体关系图-v1.5.svg`
- C 端原型：`~/Desktop/个人中心/原型/looply-个人中心-APP-v5.pen`
- 后台原型：`~/Desktop/个人中心/原型/looply-客户咨询-antd-原型-v2.html`
- 收藏与浏览历史专项 PRD：`~/Desktop/个人中心/PRD/looply-收藏与浏览历史-PRD-v1.4.md`

> 本 PRD 不包含 API 路径、HTTP 方法或参数清单；接口设计由技术方案另行定义。
