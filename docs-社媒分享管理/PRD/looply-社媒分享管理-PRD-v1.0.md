# Looply 社媒分享管理 PRD

**模块名称**：社媒分享管理（Social Share Management）
**版本**：v1.0（MVP）
**文档日期**：2026-06-07
**目标市场**：美国二手奢侈品电商
**状态**：待评审

> 修订记录单独维护在同目录 `looply-社媒分享管理-PRD-修订记录.md`，正文不含修订历史。

---

## 目录

- [一、概述](#一概述)
  - [1.1 背景与目标](#11-背景与目标)
  - [1.2 不做什么（明确边界）](#12-不做什么明确边界)
  - [1.3 用户角色](#13-用户角色)
  - [1.4 核心场景](#14-核心场景)
  - [1.5 全局页面流转](#15-全局页面流转)
  - [1.6 术语说明](#16-术语说明)
  - [1.7 多语言 / 多国家策略](#17-多语言--多国家策略)
- [二、需求详细描述](#二需求详细描述)
  - [2.1 公共功能组件](#21-公共功能组件)
  - [2.2 C 端商品分享](#22-c-端商品分享)
  - [2.3 短链服务（系统机制）](#23-短链服务系统机制)
  - [2.4 渠道归因与数据采集](#24-渠道归因与数据采集)
  - [2.5 后台短链管理](#25-后台短链管理)
- [三、依赖与风险](#三依赖与风险)
- [四、版本规划](#四版本规划)
- [五、数据与埋点](#五数据与埋点)
- [六、附录](#六附录)

---

## 一、概述

### 1.1 背景与目标

**背景**

Looply 是转转国际业务面向美国市场的大牌二手电商平台，从二手奢侈品（包袋、首饰、配饰）切入。平台当前处于冷启动阶段，品牌认知度低、用户信任待建立，需要低成本、可量化的获客与曝光手段。

竞品调研结论：外部社媒分享是行业**基础配置**而非核心竞争力——Poshmark 有外部分享但增长来自站内社交，The RealReal 无外部分享靠重金推荐增长。因此 Looply 的策略是：**先以最小成本做好基础分享 + 可量化的短链归因能力**，验证分享意愿与转化，再决定是否投入推荐计划、站内社交等更重的增长杠杆。

**目标（MVP）**

1. 为商品详情页提供全端（PC Web / Mobile Web / iOS App / Android App）基础社媒分享能力，满足用户基本预期。
2. 建立统一短链服务，同时承载**用户分享**与**运营投放**两类链接，替代 Google Campaign URL Builder 的手工拼链方式。
3. 提供后台短链管理，让运营可创建投放短链、查看每条短链的点击与独立访客数据，沉淀渠道归因基础。
4. 技术方案从简：MVP 用原生深度链接（Universal Links + App Links）+ UTM 参数 + 自建短链，技术成本为零，不引入 Branch.io 等付费深链方案。

**衡量标准**（来自调研报告 §8.1）

- 商品详情页分享率 > 2%（行业基准 1–3%）
- 分享点击率 > 5%
- Copy Link 渠道占比 > 50%（最通用）

### 1.2 不做什么（明确边界）

本期（MVP）**明确不做**以下内容，避免范围蔓延：

| 不做项 | 原因 | 计划 |
|--------|------|------|
| 推荐拉新计划（邀请好友、奖励发放、反作弊） | 独立的较大模块，需单独立项 | 后续版本 |
| 站内社交（关注、信息流、社区达人） | 需用户基数支撑，重构信息流架构 | Phase 3 |
| 归因转化（点击 → 注册 / 下单链路打通） | 依赖订单侧回传 UTM + 用户身份识别，当前 user_id 常为空 | 后续规划（TBD-3） |
| 短链启用 / 停用 / 封禁 / 过期管理 | 运营止损场景已记录，但本期不做；DB `status` 字段保留 | 后续迭代 |
| WebView 中间页引导（Instagram/TikTok 内置浏览器） | Universal Links 在 WebView 不生效，需中间页 | Phase 2 |
| 动态合成 OG 分享卡片图（商品图 + 价格 + 水印） | MVP 的 OG 图直接用商品主图，不动态合成（注：Instagram Stories 所需的 9:16 合成图本期做，见 2.2.3） | Phase 2 |
| 卖家工具包（批量导出、店铺短链、竖屏素材） | Depop 路线，赋能卖家自运营 | Phase 2 |
| 分享激励（分享得优惠券） | 属于营销活动模块 | 后续评估 |
| 目标商品下架后的短链落地兜底页 | 需规划"商品已下架"提示页 / 推荐相似商品 | 后续规划（TBD-1） |
| 用户分享短链滥用管控（刷量、不当内容紧急关闭） | 优先级与触发条件待定 | 待评估（TBD-2） |

### 1.3 用户角色

| 角色 | 说明 | 在本模块的职责 |
|------|------|----------------|
| **C 端用户（分享人）** | 平台买家 / 浏览用户，可未登录 | 在商品详情页点击分享，将商品通过社媒渠道分享给他人 |
| **C 端用户（接收方）** | 收到分享链接的人 | 点击短链，被唤起 App 或跳转落地页 |
| **运营人员** | Looply 市场 / 增长运营 | 在后台创建运营投放短链、查看短链点击数据 |
| **系统** | 短链服务 / 归因服务 | 自动生成用户分享短链、解析点击、记录归因数据 |

> 本模块为 MVP，后台仅区分"运营人员"单一角色，不做差异化权限矩阵（故第六章权限矩阵省略）。

### 1.4 核心场景

| 场景 | 触发 | 主体 | 商业价值 |
|------|------|------|----------|
| **场景 1：买家推荐好货** | 浏览商品时发现好东西，分享给特定朋友（"这个包适合你"） | C 端用户 | 高意向流量 |
| **场景 2：买家晒单** | 购买 / 收货后展示品味（注：晒单入口在订单/收货页，本期仅做详情页分享，晒单场景见 Phase 2） | C 端用户 | 品牌曝光 |
| **场景 3：运营投放** | 在社媒平台投放广告 / 达人合作，需带 UTM 的可追踪链接 | 运营人员 | 拉新、可量化归因 |
| **场景 4：效果复盘** | 运营查看各短链 / 渠道的点击与独立访客表现 | 运营人员 | 投放决策依据 |

### 1.5 全局页面流转

**C 端（商品分享）**

```
商品详情页（PC/Mobile Web/iOS/Android）
    │ 点击「Share」按钮
    ▼
分享弹窗 / 分享面板（渠道列表）
    │ 选择渠道
    ├── Copy Link → 复制到剪贴板（本地操作，toast 提示）
    ├── 社媒渠道（Facebook/Pinterest/X/...）→ 唤起对应 App / 跳转 Web 分享页
    ├── IM 渠道（Message/WhatsApp/...）→ 唤起对应 App 预填文案
    └── More → 调起系统分享面板（系统级，渠道由 OS 决定）
```

**接收方（点击短链）**

```
点击 looply.com/s/{short_code}
    │
    ├── 已装 App（OS 拦截 Universal Links / App Links）→ 直接打开 App → 商品详情页
    ├── 社媒爬虫（UA 匹配）→ 返回 OG HTML 渲染预览卡片（不跳转）
    └── 未装 App 真人 → 服务端记录点击 + 写 Cookie → 302 → 商品页 H5
```

**后台（短链管理）**

```
短链管理（列表页）
    ├── 点击「创建运营短链」→ 创建运营短链页 → 提交 → 返回列表
    └── 点击「详情」→ 短链详情页（只读看板：KPI + 点击趋势 + 点击记录）→ 返回列表
    └── 点击「复制链接」→ 复制短链到剪贴板（toast 提示）
```

### 1.6 术语说明

| 术语 | 英文 / 字段 | 含义 |
|------|------------|------|
| 短链 | short link / `short_code` | 形如 `looply.com/s/sh_8f3k29` 的短地址，是全局唯一标识 |
| 长链 | `long_url` | 短链最终重定向到的、带完整 UTM 参数的目标 URL |
| 用户分享短链 | `sh_` 前缀 | 由系统在 C 端用户分享时自动生成 |
| 运营投放短链 | `oc_` 前缀 | 由运营在后台手动创建 |
| 渠道平台 | `utm_source` | 链接被创建 / 分发的渠道（如 facebook、whatsapp） |
| 营销类型 | `utm_medium` | 区分链接类型（`social_share` = 用户分享，其余 = 运营营销类型） |
| 活动 / 内容主题 | `utm_campaign` | 用户分享为 `product_share`，运营为自定义活动名 |
| 分享入口 / 账号 | `utm_content` | 用户分享为分享入口标识，运营为自营 / 达人账号 |
| 点击数 | `click_count` | 短链被点击总次数（含重复） |
| 独立访客 | `unique_visitor_count` | 按 `visitor_id` 去重后的访客数 |
| 访客 ID | `visitor_id` | Looply 第一方 Cookie 种下的匿名标识，用于独立访客去重 |
| Referer | `referer` | 本次点击浏览器从哪个页面跳来（HTTP Referer 头），按域名归一化为渠道名 |
| OG 卡片 | Open Graph | 社媒爬取页面 meta 标签生成的链接预览卡片 |
| Universal Links / App Links | — | iOS / Android 的域名验证深度链接，静默唤起 App |

### 1.7 多语言 / 多国家策略

- **市场范围**：MVP 仅聚焦美国本土社媒（Facebook、iMessage、Pinterest、WhatsApp、X、Instagram），不铺全球，规避跨境合规复杂度。
- **语言**：C 端分享 UI 文案为英文（如 "Share to"、"Copy Link"），OG 卡片描述为英文（如 "Authentic pre-owned, verified by Looply"）。后台管理为中文（运营内部使用）。
- **币种 / 时区**：OG 卡片价格按商品币种展示（USD）；后台点击时间按运营所在时区展示。
- **合规**：分享链接不在中国大陆社媒（微信等）分发；短链落地写 Cookie 需遵循目标市场 Cookie 同意要求（与平台统一 Cookie 同意机制对接，本模块不单独实现）。

---

## 二、需求详细描述

本章是 PRD 核心。公共功能组件放在最前，其后为 C 端商品分享、短链服务、渠道归因、后台短链管理四个模块，平级排列。

### 2.1 公共功能组件

#### 2.1.1 Copy Link（复制链接）

**功能描述**：在 C 端分享面板与后台短链列表 / 详情中复用的"复制链接到剪贴板"能力。

**处理流程**：
1. 用户点击「Copy Link」/「复制链接」。
2. 优先调用 `navigator.clipboard.writeText(url)` 写入剪贴板。
3. 成功 → 显示 toast 提示（C 端 "Link copied"，后台 "已复制：{短链}"）。
4. 失败（非 HTTPS / API 不可用）→ 降级用临时 `textarea` + `execCommand('copy')` 兜底。

**规则说明**：
- 必须 HTTPS 环境，HTTP 不可用。
- iOS Safari 要求在同步 click 事件回调内调用，不能在 async/await 之后调用（否则被拒）。
- 复制的内容：C 端为短链（`looply.com/s/sh_xxx`），后台列表 / 详情为对应短链。
- 用户粘贴到哪里不可追踪，仅记录"点击复制"行为（埋点见第五章）。

**异常处理**：剪贴板权限被拒或两种方式均失败 → toast 提示"复制失败，请手动复制"并选中链接文本。

#### 2.1.2 OG 预览卡片（Open Graph）

**功能描述**：社媒平台爬取被分享链接时，渲染的商品预览卡片（图 + 标题 + 价格 + 描述）。

**触发条件**：短链服务通过 User-Agent 识别为社媒爬虫（facebookexternalhit / Twitterbot / WhatsApp / Pinterest / LinkedInBot / TelegramBot / iMessageLinkPreview / Discordbot 等）。

**处理流程**：爬虫请求 `looply.com/s/{short_code}` → 服务端**不 302**，实时关联查询商品表 → 返回含 OG 标签的 HTML → 爬虫渲染预览卡片。

**OG 标签内容（MVP）**：

| 标签 | 内容 | 来源 |
|------|------|------|
| `og:title` | `{品牌} {商品名} - ${价格}` | 商品表 brand + title + price_cents |
| `og:image` | 商品主图 URL | 商品表 image_url |
| `og:description` | "Authentic pre-owned, verified by Looply" | 固定文案 |
| `og:type` | `product` | 固定 |
| `og:url` | `looply.com/s/{short_code}` | 短链自身 |
| `twitter:card` | `summary_large_image` | 固定 |

**OG 图片规格**：

| 平台 | 推荐尺寸 | 文件限制 |
|------|---------|---------|
| Facebook / iMessage / WhatsApp | 1200×630 (1.91:1) | < 8MB |
| X (Twitter) | 1200×628 | < 5MB |
| Pinterest | 1000×1500 (2:3) | < 20MB |

**规则说明**：
- MVP 直接用商品主图作 `og:image`，不动态合成（OG 卡片图的动态合成为 Phase 2；此处不含 Instagram Stories 的 9:16 竖图——后者本期做，见 2.2.3）。
- Facebook 对 OG 图片缓存约 30 天，商品图更新后需用 Facebook Sharing Debugger 手动刷新。

**异常处理**：商品不存在 / 已下架 → 返回通用品牌 OG 卡片（Looply logo + slogan），不报错（落地兜底页为 TBD-1）。

### 2.2 C 端商品分享

**模块概述**：在商品详情页提供分享入口，点击后按端形态展示渠道列表，用户选择渠道后由系统生成用户分享短链并调起对应渠道。本模块为**页面型 + 流程型混合**，按端拆分形态差异。

#### 2.2.1 分享入口（商品详情页）

**功能描述**：商品详情页的「Share」按钮，是所有分享的统一入口。

**前置条件**：用户处于商品详情页（PDP）。用户可未登录（未登录时分享人记为匿名）。

**页面布局（各端差异）**：

| 端 | 入口位置 | 触发方式 |
|----|---------|---------|
| PC Web | 商品图右上角浮动分享图标 | 点击 → 模态弹窗（半透明遮罩） |
| Mobile Web | 商品图右上角分享图标 | 点击 → 底部弹出分享面板 |
| iOS App | 商品图右上角分享图标 | 点击 → 底部弹出分享面板 |
| Android App | 商品图右上角分享图标 | 点击 → 底部弹出分享面板 |

**页面元素**：分享图标按钮（次要按钮样式，icon + 可选 "Share" 文字）。

**操作流程**：点击「Share」→ 打开分享弹窗 / 面板（见 2.2.2）。

**交互说明**：分享按钮在 PDP 常驻显示，不做悬停触发（保证移动端可复用）。

**UI 关联**：
- PC：`looply-share-prototype.pen` → Frame「PC Web - Product Detail + Share Modal」(`tFl2A`)
- Mobile Web：Frame「Mobile Web - Product Detail + Share Sheet」(`NPfew`)
- iOS：Frame「iOS App - Product Detail + Share Sheet」(`rMtyB`)
- Android：Frame「Android App - Product Detail + Share Sheet」(`9wWk7`)

#### 2.2.2 分享弹窗 / 面板（渠道列表）

**功能描述**：展示可用分享渠道，PC 为模态弹窗，移动端为底部面板。移动端面板顶部带商品摘要卡（商品主图 + 商品名 + 价格）。

**页面元素**：
- 标题："Share to"
- 商品摘要卡（仅移动端）：主图缩略 + 商品名（截断）+ 价格
- 渠道图标列表（圆形图标 + 渠道名）
- 关闭方式：× 按钮、点击遮罩、ESC（PC）

**各端渠道方案**

各端首屏渠道由"固定渠道 + 动态检测渠道"组成。**动态检测**仅 App 端做（通过 `canOpenURL` / `<queries>` 检测目标 App 是否安装），未安装则不显示该渠道；Web 端全部固定显示。

**① PC Web**（全固定显示，对标 SHEIN 点击弹窗）

| 渠道 | 说明 |
|------|------|
| Facebook | 跳 Facebook 分享对话框 |
| Pinterest | 跳 Pinterest pin 创建页 |
| X (Twitter) | 跳 X intent 分享页 |
| Email | 调起邮件客户端（`mailto:`，预填标题 + 链接） |
| Copy Link | 复制短链（见 2.1.1） |

> 说明：PC 端保留 Email 渠道（与前端原型一致）。不放 Message（Windows 不可用）、WhatsApp（桌面端非主流）。

**② Mobile Web**（全固定显示）

| 渠道 | 未安装降级 |
|------|----------|
| WhatsApp | 跳 `wa.me` / App Store |
| Message | 系统 SMS（`sms:&body=`），必有 |
| Facebook | 跳 Facebook 网页版分享 |
| Pinterest | 跳 Pinterest 网页版 |
| X (Twitter) | 跳 `twitter.com/intent/tweet` 分享页（预填链接 + 文案，必有 Web 降级） |
| Messenger | `facebook.com/dialog/send`（需登录 FB） |
| Copy Link | 复制短链 |
| More | `navigator.share()` 调系统面板 |

> Mobile Web 不做安装检测：用户已在浏览器内，每个渠道都有 Web 降级方案，跳转不突兀。

**③ iOS App**（固定 + 动态混合）

- 固定渠道（必显示）：Message (iMessage) / Facebook / Copy Link
- 动态渠道（`canOpenURL` 检测，按权重排序后取首屏前 2 个补位）：

| 渠道 | URL Scheme | 权重 |
|------|-----------|------|
| WhatsApp | `whatsapp://` | 100 |
| Pinterest | `pinterest://` | 90 |
| X | `twitter://` | 80 |
| Instagram | `instagram://` | 30（Stories 合成图方案，调起见 2.2.3） |
| Messenger | `fb-messenger://` | 20（收进 More） |

示例：已装 WhatsApp → `Message → FB → WhatsApp → Pinterest → Copy Link → More`；未装 WhatsApp → `Message → FB → Pinterest → Copy Link → More`。

**④ Android App**（固定 + 动态混合）

- 固定渠道（必显示）：Facebook / SMS（系统内置，100% 可用） / Copy Link
- 动态渠道（`<queries>` 声明包名后检测，按权重排序）：

| 渠道 | URL Scheme | 权重 |
|------|-----------|------|
| WhatsApp | `whatsapp://` | 100（检测到后插首屏，SMS 挤进 More） |
| X | `twitter://` | 90 |
| Pinterest | `pinterest://` | 80 |
| Instagram | `instagram://` | 30（Stories 合成图方案，调起见 2.2.3） |
| Messenger | `fb-messenger://` | 20（收进 More） |

示例：已装 WhatsApp → `FB → WhatsApp → X → Copy Link → More`（SMS 收进 More）；未装 → `FB → SMS → X → Copy Link → More`。

> **PRD 口径**：以上"固定 + 动态检测"规则为准；前端原型（`rMtyB` / `9wWk7`）展示的是"已安装全部 App"的最大视图，作渠道形态示例，不代表固定渲染列表。

**操作流程（主流程）**：
1. 用户在分享面板点击某渠道。
2. 前端调用短链创建接口，传入 `product_id`、`channel`（渠道）、`share_page`（入口，PDP 为 `pdp_share_button`）。
3. 服务端生成用户分享短链（见 2.3），返回短链 URL。
4. 前端用该短链调起对应渠道：
   - Copy Link → 写剪贴板 + toast
   - 社媒 / IM 渠道 → 按渠道 API 调起（见 2.2.3）
   - More → `navigator.share()` / 系统面板，`channel` 记为 `native_share`

**分支流程**：
- 点击 More（系统面板）→ 渠道由 OS 决定，前端无法获知最终渠道，`channel` 标记 `native_share`，接收方点击后由服务端从 Referer 反推真实渠道。
- 用户中途关闭弹窗 → 不生成分享动作，记录弹窗放弃埋点。

**校验规则**：

| 字段 | 规则 | 时机 |
|------|------|------|
| product_id | 必须为有效在售商品 ID | 创建短链时 |
| channel | 必须在渠道枚举内（见 2.4.1） | 创建短链时 |

**异常处理**：
- 短链创建接口失败 → toast "Failed to generate link, please retry"，不调起渠道。
- 目标渠道 App 未安装（App 端动态渠道）→ 该渠道不显示（不会出现"点了没反应"）。
- 网络异常 → toast 网络错误提示。

**交互说明**：分享面板打开 / 关闭动效遵循平台规范；遮罩半透明；移动端面板从底部滑入。

**UI 关联**：同 2.2.1（各端 Frame）。

#### 2.2.3 各渠道调起方式（技术说明）

> 本节为流程型功能的技术说明，供开发理解各渠道 API 与坑点。所有渠道分享的都是**短链**（`looply.com/s/{short_code}`），非原始长链。

| 渠道 | 调起方式 | 关键坑点 |
|------|---------|---------|
| Facebook | `facebook.com/dialog/share?app_id=X&href={短链}&hashtag=%23shoplooply` | 需注册 FB App；hashtag 仅一个；OG 图缓存 30 天 |
| Pinterest | `pinterest.com/pin/create/button/?url={短链}&media={图}&description=X` | media 防盗链会加载失败；Rich Pin 审核 2–5 工作日 |
| X (Twitter) | `twitter.com/intent/tweet?text=X&url={短链}&hashtags=shoplooply&via=LooplyApp` | text+url ≤ 280 字符（t.co 占 23）；hashtag 不与 text 重复 |
| WhatsApp | App：`whatsapp://send?text={编码文案}`；Web：`wa.me/?text=X` | iOS 需 Info.plist 注册 `whatsapp`；Android 11+ 需 `<queries>` 声明 `com.whatsapp` |
| iMessage / SMS | iOS：`sms:&body={编码文案}`；Android：`sms:?body=X` | iOS 8+ 用 `&body=`；用户是否真发送无法感知 |
| Messenger | App：`fb-messenger://share?link={短链}`；Web：`facebook.com/dialog/send?app_id=X&link={短链}` | Web 需登录 FB；只能发单个好友 |
| Email（PC） | `mailto:?subject={商品名}&body={短链}` | 依赖本地邮件客户端配置 |
| Copy Link | 见 2.1.1 | — |
| Instagram Stories | 服务端合成 9:16 图 → `instagram-stories://share?backgroundImage={本地URI}`（贴纸层可附带短链跳转） | 须先下载合成图到本地取文件 URI；分享无点击回调（归因靠落地页 Referer）；Android 需配 FileProvider 授予 IG 读取权限；iOS 需 Info.plist 注册 `instagram-stories` |

**Facebook 品牌 Hashtag**：所有端 Facebook 分享统一通过 `hashtag=%23shoplooply` 预填品牌标签，便于社媒搜索聚合与品牌曝光追踪。

### 2.3 短链服务（系统机制）

**模块概述**：一套统一短链服务，同时承载用户分享（API 自动生成）与运营投放（后台手动创建），统一入口 `looply.com/s/{short_code}`。本模块为**机制型**（无独立 C 端页面，后台创建页见 2.5）。

#### 2.3.1 短链生成

**触发条件**：
- 用户分享：C 端点击渠道时，前端调用短链创建接口。
- 运营投放：运营在后台「创建运营短链」页提交。

**处理流程（用户分享）**：
1. 前端传入 `product_id`、`channel`、`share_page`。
2. 服务端生成 `short_code = sh_ + 6位Base62`。
3. 按渠道与商品上下文拼接长链（`long_url`），写入 UTM 参数（取值规则见 2.4.1）。
4. 写入 `short_links` 表（含冗余的 4 个 UTM 字段、product_id、sharer_user_id / session_id）。
5. 返回短链 `looply.com/s/sh_xxx`。

**处理流程（运营投放）**：
1. 运营填写基础 URL + 备注名称 + 4 个 UTM 参数（见 2.5.2）。
2. 服务端生成 `short_code = oc_ + 6位Base62`。
3. **自动拼接长链**：`base_url` + 拼接符 + UTM 参数串 → `long_url`。
   - base_url 无参数：第一个 UTM 用 `?` 连接。
   - base_url 已含参数（如 `?ref=xxx`）：第一个 UTM 用 `&` 连接。
   - 各 UTM 参数间用 `&` 连接。
4. 写入 `short_links` 表（含 created_by 运营 ID、campaign_name 备注名）。**不存储 base_url**（ER 仅有 long_url + 4 个 UTM 字段）。
5. 返回短链，支持复制 + 生成二维码（二维码为后台能力）。

**short_code 生成规则**：

| 场景 | 格式 | 示例 |
|------|------|------|
| 用户分享（API） | `sh_` + 6 位 Base62 | `sh_8f3k29` |
| 运营创建 | `oc_` + 6 位 Base62 | `oc_x7Km9p` |

固定 6 位（62⁶ ≈ 568 亿组合），容量充足。前缀用于人工快速区分两类短链来源。

**规则说明（UTM 命名规范）**：
- 小写 + 下划线（如 `organic_social`、`summer_bags_2026`）。运营投放的 utm_source 枚举因沿用现有外链规范保留原始大小写（见 2.4.1）。
- 禁止空格和特殊字符（`& = # +` 等），避免破坏 URL 拼接。

**异常处理**：
- short_code 碰撞（极低概率）→ 重新生成。
- 基础 URL 格式非法 → 后台创建时校验拦截（见 2.5.2）。
- 商品不存在 → 用户分享创建失败，返回错误。

#### 2.3.2 短链点击解析

**功能描述**：接收方点击短链后的解析与跳转逻辑，是归因数据的采集起点。

**触发条件**：任意来源点击 `looply.com/s/{short_code}`。

**处理流程**：

```
GET /s/{short_code}
    ↓
① 已装 App（OS 层 Universal Links / App Links 拦截，请求不到服务器）
   → 直接打开 App → App 解析 long_url 路径 → 调 API 记录点击 → 跳商品详情页
    ↓（未被 OS 拦截，请求到达服务器）
② 判断 User-Agent：
   ├── 社媒爬虫 → 返回 OG HTML（200，不跳转，见 2.1.2）
   ├── WebView（Instagram/TikTok 内置浏览器）→ 返回中间页引导"在浏览器打开"（Phase 2，MVP 暂按真人处理）
   └── 普通真人 →
        1. 记录 share_clicks（visitor_id、user_id、clicked_at、ip、user_agent、referer）
        2. 写 Cookie `_looply_ref={short_code}`（30 天有效）
        3. click_count +1，按 visitor_id 去重更新 unique_visitor_count
        4. 302 重定向到 long_url（带完整 UTM 参数，GA4 可识别）
```

**规则说明**：
- **多次点击归因**：Last Click 归因（以最后一次点击为准）。
- **Cookie**：`_looply_ref`，30 天有效，供后续注册 / 下单时反查归因（归因转化为 TBD-3，本期仅写 Cookie 不打通转化）。
- **App 唤起**：Universal Links (iOS) + App Links (Android)，部署 `/.well-known/apple-app-site-association` 与 `/.well-known/assetlinks.json` 声明 `/s/*` 与 `/product/*` 路径。App 内部据 long_url 路径决定跳转页面，无需额外 Deep Link ID 字段。

**异常处理**：
- short_code 不存在 → 返回 404 或通用首页（落地兜底为 TBD-1）。
- 目标商品已下架 → MVP 仍 302 到商品页（由商品页自行处理下架展示）；规范化兜底页为 TBD-1。

**技术说明（已知限制）**：
- Instagram / TikTok 内置 WebView 中 Universal Links 不生效 → Phase 2 用中间页引导。
- Safari 地址栏直接输入 URL 不触发唤起（符合预期）。
- 从同域名页面跳转不触发唤起（iOS 限制）。
- iOS 26 系统级剥离 `utm_*` / `fbclid` / `gclid` 参数 → **短链路径方案（`/s/{short_code}`）天然免疫**，因 URL 路径永不被剥离，归因上下文存在服务端而非 URL 参数。

### 2.4 渠道归因与数据采集

**模块概述**：定义 UTM 参数取值规范、Referer 归一化规则、访客去重口径。本模块为**机制型**，是后台报表与渠道分析的数据口径基础。

#### 2.4.1 UTM 参数取值规范

短链服务用 4 个 UTM 字段承载归因信息，**用户分享**与**运营投放**两类取值不同：

| 字段 | 用户分享取值 | 运营投放取值 | 含义 |
|------|------------|------------|------|
| `utm_source` | 见下方【用户分享 source 枚举】 | 见下方【运营投放 source 枚举】 | 渠道平台 |
| `utm_medium` | `social_share`（固定） | `organic_social` / `paid_social` / `influencer` / `paid_search` / `paid_shopping` | 营销类型 |
| `utm_campaign` | `product_share`（固定） | 自定义活动名（小写 + 下划线） | 活动 / 内容主题 |
| `utm_content` | 分享入口标识（见下方【入口枚举】） | 自营账号 / 达人账号 | 分享入口 / 账号 |

> **核心过滤器**：`utm_medium=social_share` 即可在 GA4 / 报表中分离"用户分享"与"运营投放"流量。`utm_medium` 同时替代了早期设计中 `link_type` 字段的区分职责——故 ER 不单设 link_type。

**【用户分享 source 枚举】**（系统按用户选择的渠道自动写入）

| 枚举值 | 含义 | 触发时机 |
|--------|------|---------|
| `whatsapp` | WhatsApp 分享 | 用户在面板选 WhatsApp |
| `imessage` | iMessage 分享 | iOS 选 Message |
| `sms` | 短信分享 | Android 选 SMS |
| `facebook` | Facebook 分享 | 用户选 Facebook |
| `messenger` | Messenger 分享 | 用户选 Messenger |
| `pinterest` | Pinterest 分享 | 用户选 Pinterest |
| `twitter` | X (Twitter) 分享 | 用户选 X |
| `instagram` | Instagram Stories 分享 | App 端选 Instagram（合成 9:16 图调起 Stories） |
| `email` | 邮件分享 | PC 选 Email |
| `copy_link` | 复制链接 | 用户选 Copy Link |
| `native_share` | 系统分享面板 | 用户选 More，渠道由 OS 决定 |

**【运营投放 source 枚举】**（后台创建时下拉选择，支持自定义输入；沿用现有外链规范，保留原始大小写）

| 枚举值 | 含义 |
|--------|------|
| `tiktok` | TikTok |
| `Instagram` | Instagram |
| `Youtube` | YouTube |
| `Facebook` | Facebook |
| `google` | Google |
| `email` | 邮件营销 |

> 运营 source 为下拉 + 可自定义输入（应对列表外平台）。

**【运营投放 medium 枚举】**（后台创建时下拉选择，支持自定义输入）

| 枚举值 | 含义 |
|--------|------|
| `organic_social` | 非付费社媒内容 |
| `paid_social` | 付费社交广告 |
| `influencer` | 达人带货 / 种草 / 测评 |
| `paid_search` | 付费搜索广告 |
| `paid_shopping` | Google Performance Max 广告 |

> 运营创建表单仅给以上 5 个营销类型（不含 `social_share`——运营不创建用户分享链接）。

**【utm_content 用户分享入口枚举】**

| 枚举值 | 含义 |
|--------|------|
| `pdp_share_button` | 商品详情页分享按钮（MVP 唯一入口） |
| `product_card_share` | 商品卡片分享（Phase 2） |
| `wishlist_share_button` | 心愿单分享（Phase 2） |
| `collection_share_button` | 合集页分享（Phase 2） |
| `order_share_button` | 订单完成页分享（Phase 2） |
| `app_product_share` | App 内商品分享（Phase 2） |

**【utm_content 运营账号枚举（参考值，可自定义输入）】**：`looply_luxury` / `looplybags` / `looply.rebirth` / `looplyfinds` / `Archive Edit` / `inspoetry` / `sarah` / `relovemybag` / `FshnLuxeClub` / `BreeLuxeFinds`，以及其他达人账号（直接输入，不限于列表）。

#### 2.4.2 Referer 归一化与渠道口径

**功能描述**：点击记录中的 Referer 字段，记录本次点击浏览器从哪个页面跳来，归一化为友好渠道名。

**核心口径：utm_source ≠ Referer，互补不替代**

| 维度 | utm_source | Referer |
|------|-----------|---------|
| 含义 | 链接被创建 / 分发的渠道 | 本次点击从哪个页面跳来 |
| 时机 | 建链时写死（静态） | 每次点击动态采集 |
| 归属 | 短链记录（`short_links`） | 每条点击日志（`share_clicks`） |
| 可靠性 | 高（一定在 URL 里） | 低（社媒 / 原生 App 常丢失） |
| 回答 | "链接推到了哪个渠道" | "这次点击真实来自哪里" |

链接发出后会二次传播（转发到别的渠道、复制粘贴），一条 `utm_source=imessage` 的链接完全可能最终从 Twitter 点进来。**两者不一致是有效信号（链接破圈），不是数据错误**。

- 看**分发渠道 / 投放效果** → 以 `utm_source` 为准（权威）。
- 看**本次点击真实来源** → 看 Referer。

**Referer 归一化规则**：取 host → 查"域名 → 渠道"映射表 → 输出友好渠道名。

| 来源域名（host / 通配） | 归一化渠道名 |
|------------------------|-------------|
| `*.instagram.com` / `l.instagram.com` | Instagram |
| `*.facebook.com` / `l.facebook.com` / `m.facebook.com` | Facebook |
| `t.co` / `x.com` / `*.twitter.com` | Twitter/X |
| `*.tiktok.com` | TikTok |
| `*.pinterest.com` | Pinterest |
| `*.youtube.com` / `youtu.be` | YouTube |
| `*.whatsapp.com` / `wa.me` | WhatsApp |
| `*.google.*` | Google |
| `*.bing.com` | Bing |
| 命中不了的其它合法域名 | 直接显示原始 host（不归入"其它"） |
| referer 为空 / 取不到 | 显示 `—`（见下方规则） |

**实现要点**：
- 匹配维度是 host，不是整段 URL；先剥协议和路径再比对。
- 子域用后缀通配（`endsWith`），避免漏掉 `l.` / `m.` 等跳转域。
- 未命中映射表的合法域名保留原始 host，不归到"其它/Direct"，避免丢失长尾渠道。
- 映射表是可配置项，新渠道上线只加表项，不改代码。

**空 Referer 规则（硬性）**：
- 取不到 referer → 统一显示 `—`，语义是"未采集到来源"。
- **禁止**使用 "Direct" 标签——社媒场景中空 referer 99% 是被剥离 / 丢失（App 抹掉、HTTPS→HTTP 降级、Referrer-Policy），标 "Direct" 会让丢失流量伪装成直接流量，造成归因误判。
- 渠道占比统计中，空 referer 单列为"未知来源"，不计入任何具体渠道，也不计入"直接访问"。

**重要局限（避免误读数据）**：
- 原生 App（iMessage、WhatsApp、Instagram / Facebook 内置浏览器）点击大概率空 referer。
- 因此"靠 referer 识别出 iMessage"现实中基本做不到——要区分是否 iMessage 仍需依赖 utm_source。
- **结论**：渠道分析主依据是 utm_source，Referer 仅作辅助交叉验证。

#### 2.4.3 访客去重（visitor_id）

**功能描述**：独立访客统计的标识口径。

**规则说明**：
- `visitor_id` 不是请求带来的，是 Looply 第一方生成的匿名标识。
- 首次访问跳转服务 / 落地页时种第一方 Cookie，值为随机 ID（如 `vis_a1b2`）；同浏览器再次访问读回同一 Cookie → 同一 visitor_id。
- `unique_visitor_count` 按 visitor_id 去重计算。
- 访客已登录时，可将 visitor_id 关联到 `user_id`（点击记录"登录用户 ID"列，未登录为空）。
- Cookie 不可用时降级用 IP + User-Agent 指纹兜底，主路径是第一方 Cookie。

### 2.5 后台短链管理

**模块概述**：运营在后台管理短链的入口，含列表页、创建运营短链页、短链详情页三个页面。MVP 定位为"创建运营短链 + 只读数据看板"，不含启用 / 停用 / 编辑等写操作（详见各页面）。一级菜单「短链管理」点击直接进入列表页。

#### 2.5.1 短链列表页

**功能类型**：页面型。

**功能描述**：展示系统内所有短链（用户分享 + 运营投放），支持筛选、查看详情、复制链接、创建运营短链。

**前置条件**：运营登录后台。

**页面布局**：标题区（标题 + 描述 + 右上「创建运营短链」按钮）→ 筛选区 → 表格 → 分页。

**页面元素**

> 说明：列表页**不设 KPI 卡片区**。短链整体数据（总点击 / 独立访客等）按单条短链在「详情页」呈现；列表页定位为"查询 + 列表"，避免与详情页数据重复。早期版本曾设计 3 个列表级 KPI（总短链数 / 总点击数 / 独立访客），本期移除。

筛选区：

| 筛选项 | 类型 | 选项 |
|--------|------|------|
| 渠道（utm_source） | 下拉单选，可清除 | 全部渠道 + 各渠道值（imessage / facebook / instagram / pinterest / tiktok / copy_link / email / twitter / whatsapp 等） |
| 营销类型（utm_medium） | 下拉单选，可清除 | 全部营销类型 + 6 个值：`social_share`（用户分享）/ `organic_social` / `paid_social` / `influencer` / `paid_search` / `paid_shopping` |
| 创建时间 | 日期范围（RangePicker） | 创建开始 ~ 创建结束 |
| 查询 / 重置 | 按钮 | — |

> 筛选区**不含**「全部状态」（MVP 不做启用 / 停用）。营销类型筛选含 `social_share`，用于筛出用户分享的短链。

表格列：

| 列 | 字段 | 渲染规则 |
|----|------|---------|
| 短码 | `short_code` | 代码样式（如 `sh_8f3k29`） |
| 渠道 | `utm_source` | 标签展示 |
| utm_medium | `utm_medium` | 代码样式；表头带 tooltip：`social_share = 用户主动分享`，其它 = 运营手动选择的营销类型 |
| 备注 | `campaign_name` / `product_name` | 渲染优先级：`campaign_name` → `product_name` → `—`（规则见下） |
| 点击 | `click_count` | 数字，可排序；表头 tooltip："短链被点击总次数（含重复）" |
| 独立访客 | `unique_visitor_count` | 数字，可排序；表头 tooltip："去重后的独立访客数" |
| 创建时间 | `created_at` | 时间 |
| 操作 | — | 「详情」+「复制链接」两个平铺按钮 |

**「备注」列渲染规则**：

| 短链类型 | utm_medium | 来源字段 | 示例 |
|---------|-----------|---------|------|
| 用户分享 PDP | `social_share` | `product_name`（系统生成短链时从商品数据带入） | Chanel Classic Flap |
| 运营投放 | `organic_social` / `paid_social` 等 | `campaign_name`（运营填写的备注名） | Summer Bags 推广 |
| 非单品页分享（Wishlist / 合集等） | `social_share` | 两字段均为空 | `—` |

> 非单品页分享场景，两字段均空时列显示 `—`，不从 utm_content 反推入口类型。

**列表无「状态」列**：MVP 不做启用 / 停用，列表不展示状态列。数据库 `status` 字段保留（默认 active），留待后续启用。

**操作列规则**：
- 固定展示「详情」「复制链接」两个平铺按钮（不使用「···」下拉菜单）。
- 所有短链（用户分享 / 运营投放）均可查看详情、复制链接。
- 不含「编辑备注」「停用」等写操作。

**页面状态变体**：

| 状态 | 表现 |
|------|------|
| 正常数据 | 显示表格 + 分页 |
| 零数据 | 隐藏筛选区，居中引导 + CTA「创建运营短链」 |
| 筛选无匹配 | 保留筛选区，表格替换为提示 + 「清除筛选」 |
| 网络异常 | 保留筛选区，表格替换为错误提示 + 「重试」 |
| 加载态 | 表格 loading |

**操作流程**：
- 点击「创建运营短链」→ 进入创建页（2.5.2）。
- 点击「详情」→ 进入详情页（2.5.3）。
- 点击「复制链接」→ 复制该短链到剪贴板（2.1.1），toast "已复制：lply.link/{short_code}"。
- 筛选 + 查询 → 刷新表格；重置 → 清空筛选。

**校验规则**：筛选项均非必填；日期范围结束不得早于开始。

**异常处理**：列表加载失败 → 网络异常态 + 重试；筛选无结果 → 无匹配态。

**交互说明**：列表默认按创建时间倒序；分页用紧凑分页器。

**UI 关联**：
- PC：`looply-社媒分享管理-antd-原型-v1.2.html` → `ShortLinkListPage`
- APP 端：后台管理为 PC Web 应用，无 APP 端设计稿（运营后台不提供移动端，下同）。

#### 2.5.2 创建运营短链页

**功能类型**：页面型。

**功能描述**：运营填写基础 URL + 备注 + UTM 参数，系统自动拼接生成运营投放短链。

**前置条件**：运营从列表页点击「创建运营短链」进入。

**页面布局**：标题区（标题 +「返回列表」）→「链接信息」分区 →「UTM 参数（用于自动拼接）」分区 → 底部操作栏（取消 + 创建短链）。

**页面元素 / 表单字段**：

| 字段 | 必填 | 控件 | 说明 |
|------|------|------|------|
| 基础 URL | 是 | 输入框 | 填不含参数的目标页面 URL（如 `https://looply.com/product/1001`），系统自动拼接 UTM 生成长链 |
| 备注名称 | 否 | 输入框 | 内部管理用，不对外展示（如 "Summer Bags 推广 — BreeLuxeFinds"），存入 `campaign_name` |
| utm_source | 是 | 下拉 + 可自定义输入（单值） | 平台，6 个枚举（见 2.4.1），支持输入列表外值 |
| utm_medium | 是 | 下拉 + 可自定义输入（单值） | 营销类型，5 个枚举（见 2.4.1），支持输入列表外值 |
| utm_campaign | 否 | 输入框 | 活动 / 内容主题，自定义内容名称（小写字母），如 `summer_bags_2026` |
| utm_content | 否 | 下拉 + 可自定义输入（单值） | 自营 / 达人账号，参考枚举见 2.4.1，其他达人账号可直接输入 |

> 三个 UTM 下拉均为"可输入列表外值的单值选择"（保留自定义能力但限制单值，一条链接的每个 UTM 只能有一个值）。

**自动拼接逻辑**：`base_url` + 拼接符（无参数用 `?`，已有参数用 `&`）+ `utm_source=X&utm_medium=X&utm_campaign=X&utm_content=X` → 存入 `long_url`。4 个 UTM 同时单独存储（冗余，用于筛选）。**不存储 base_url**。

**操作流程（主流程）**：
1. 填写基础 URL（必填）。
2. 填写备注名称（可选）。
3. 选择 / 输入 utm_source、utm_medium（必填），utm_campaign、utm_content（可选）。
4. 点击「创建短链」→ 校验通过 → 系统生成 `oc_` 短链 → toast "短链已创建" → 返回列表页。

**分支流程**：点击「取消」/「返回列表」→ 不保存，返回列表页。

**校验规则**：

| 字段 | 规则 | 校验时机 |
|------|------|---------|
| 基础 URL | 必填；须为合法 URL（http/https 开头） | 提交时 |
| utm_source | 必填 | 提交时 |
| utm_medium | 必填 | 提交时 |
| 各 UTM 值 | 小写 + 下划线；禁止空格和 `& = # +` 等特殊字符（utm_source 运营枚举保留原始大小写除外） | 提交时 |

**异常处理**：
- 必填项为空 → 字段下方红色提示，不提交。
- URL 格式非法 → 提示"请输入合法的 URL"。
- 提交接口失败 → toast 错误提示，停留在当前页保留已填内容。

**交互说明**：本页为纯新建表单，无操作记录区（短链创建后不可编辑，无编辑历史）。

**UI 关联**：PC `ShortLinkCreatePage`（`looply-社媒分享管理-antd-原型-v1.2.html`）；无 APP 端。

#### 2.5.3 短链详情页

**功能类型**：页面型。

**功能描述**：只读数据看板，展示单条短链的基本信息、点击趋势、点击记录。所有短链（用户分享 / 运营投放）均可查看。

**前置条件**：运营从列表页点击「详情」进入。

**页面布局**：标题区（标题 +「返回列表」）→ KPI 卡片（2 个）→「基本信息」→「点击趋势」→「点击记录」表。

**页面元素**

KPI 卡片（2 个）：总点击数、独立访客。

> 早期设计的「归因转化 / 归因订单」KPI 为占位假数据，本期移除（依赖点击→下单链路打通，归入 TBD-3）。

基本信息（只读）：

| 字段 | 说明 |
|------|------|
| 短码 | `short_code` |
| 短链地址 | `lply.link/{short_code}` |
| 目标 URL | `long_url`（完整长链，含 UTM） |
| 分享人 / 创建人 | 用户分享（`social_share`）显示分享人 `sharer_user_id`（未登录显示"未登录（匿名分享）"）；运营投放显示创建人 `created_by` |
| 备注 | `campaign_name` / `product_name`，均空显示 `—` |
| 创建时间 | `created_at` |

> 说明：基本信息**不单独展示 `utm_source` / `utm_medium` / `utm_campaign` / `utm_content` 四个原始 UTM 字段**——完整含 UTM 的长链已在「目标 URL」行可见，运营可直接从中读出渠道，无需重复罗列。

点击趋势：
- 折线图（点击数 + 独立访客双线）。
- 时间范围切换：近 7 日 / 近 30 日 / 全部，默认近 7 日。
- 趋势区高度固定，长周期下横向加密点位，不纵向撑长页面。

点击记录表：

| 列 | 字段 | 说明 |
|----|------|------|
| 点击时间 | `clicked_at` | — |
| 访客 ID | `visitor_id` | 表头 tooltip：系统首次访问种下的第一方 Cookie 标识，用于独立访客去重，未登录也可识别同一浏览器 |
| 登录用户 ID | `user_id` | 未登录显示 `—` |
| IP | `ip` | — |
| User Agent | `user_agent` | — |
| Referer | `referer` | 表头 tooltip：HTTP Referer 头按域名归一化为渠道名；原生 App 常不发送、取不到显示 `—`；描述"本次点击从哪来"，与 utm_source 不同、可能不一致。有值显示渠道名，空值显示 `—` |

**页面状态变体**：正常（有数据）/ 点击记录为空（表格空提示）/ 加载态 / 网络异常。

**操作流程**：仅查看 + 「返回列表」。本页为只读，无写操作。

**异常处理**：短链不存在 → 提示并返回列表；数据加载失败 → 错误态 + 重试。

**交互说明**：详情页为只读看板，不计入「操作」，不含启用 / 停用 / 编辑入口。本页无操作记录区（短链不可编辑，无变更历史可记录）。

**UI 关联**：PC `ShortLinkDetailPage`（`looply-社媒分享管理-antd-原型-v1.2.html`）；无 APP 端。

---

## 三、依赖与风险

### 3.1 上下游系统依赖

| 依赖系统 | 依赖内容 | 本模块用途 | 关系 |
|---------|---------|-----------|------|
| 商品模块 | `products`（product_id / title / brand / price_cents / image_url） | 拼接 OG 卡片、列表「商品名」、长链商品路径 | 只读 |
| 用户模块 | `users`（user_id / username） | 分享人、点击者、登录用户识别 | 只读 |
| 订单模块 | `orders`（order_id / user_id / total_cents） | 归因订单（TBD-3，本期不打通） | 只读 |
| 平台 Cookie 同意机制 | Cookie 合规授权 | 落地写 `_looply_ref` / `visitor_id` Cookie | 依赖 |
| 埋点平台 | 统一埋点规则 | 分享漏斗事件上报（见第五章） | 依赖（规则待定） |

### 3.2 外部服务依赖

| 外部服务 | 用途 | 前置准备 | 审核周期 |
|---------|------|---------|---------|
| Facebook App（Meta） | Facebook / Messenger 分享对话框需 `app_id` | 注册 Facebook App、配置 redirect_uri 白名单、准备隐私政策 | 基础 Share Dialog 无需审核 |
| Pinterest Rich Pin | 商品 Rich Pin 自动抓价格 / 库存 | 申请 Rich Pin（全站一次性） | 2–5 工作日 |
| X (Twitter) intent | X 分享 | 无需注册（intent 公开） | 无 |
| 域名 / SSL | 短链 `looply.com/s/*` 需 HTTPS | 配置 AASA / assetlinks.json，部署 `.well-known/` | — |
| iOS / Android 应用 | Universal Links / App Links 唤起 | App 端集成深链解析、声明 URL Scheme（whatsapp / Info.plist、Android `<queries>`） | 随 App 发版 |

> **外部服务对接提醒**：Facebook App 注册需准备隐私政策 / 服务条款链接；Pinterest Rich Pin 有审核周期，需提前申请。建议在开发排期前确认上述账号注册与合规材料就绪。

### 3.3 关键风险

| 风险 | 影响 | 规避 |
|------|------|------|
| WebView 深链失效（Instagram/TikTok 内置浏览器） | 30–40% 社媒流量唤起 App 失败 | MVP 降级为正常网页落地；Phase 2 加中间页引导"在浏览器打开" |
| iOS 26 剥离 UTM 参数 | URL 参数归因丢失 | 短链路径方案（`/s/{short_code}`）天然免疫，归因上下文存服务端 |
| Referer 大量为空 | 点击真实来源识别率低 | 渠道分析主用 utm_source，Referer 仅辅助；空值显示 `—` 不标 Direct |
| 归因不准（跨设备 / 无 IDFA） | 概率匹配 70–85% | 接受模糊度，本期不承诺精确归因；归因转化打通为 TBD-3 |
| 平台外链政策变动 | 单一渠道失效 | 不重度依赖单一渠道；MVP 多渠道并行 |
| 用户分享短链滥用（刷量 / 不当内容） | 数据污染 / 品牌风险 | 已记录为 TBD-2，本期无紧急关闭手段，待评估 |

---

## 四、版本规划

### 4.1 当前版本（v1.0 MVP）范围

- C 端商品详情页分享（PC / Mobile Web / iOS / Android 四端）。
- 统一短链服务：用户分享 API 自动生成 + 运营投放后台手动创建；点击解析 302 + Cookie 写入。
- 社媒爬虫 OG 卡片返回（实时查商品表）。
- Universal Links / App Links App 唤起。
- 后台短链管理：列表（筛选 / 复制 / 创建入口）、创建运营短链、短链详情（只读看板）。
- 渠道归因数据采集口径：UTM 规范、Referer 归一化、visitor_id 去重。

### 4.2 后续迭代方向

| 阶段 | 功能 | 说明 |
|------|------|------|
| Phase 2 | WebView 中间页引导 | Instagram/TikTok 内置浏览器降级 |
| Phase 2 | 动态合成 OG 分享卡片图 | 商品图 + 价格 + 品牌 + Looply 水印（OG 1200×630；Instagram Stories 的 9:16 合成图已在 MVP 实现） |
| Phase 2 | 分享入口扩展 | 订单完成页 / 收货确认页 / 心愿单 / 合集页 / 卖家店铺页 |
| Phase 2 | 卖家工具包 | 批量导出 CSV、店铺短链、竖屏素材 |
| Phase 2 | 短链状态管理 | 启用 / 停用 / 封禁 / 过期（DB status 已预留） |
| Phase 2 | 分享报表完整版 | 渠道 / 入口 / 热门商品多维度 |
| 后续规划 | 归因转化打通（TBD-3） | 点击→注册 / 下单链路，依赖订单回传 UTM + 身份识别 |
| 后续规划 | 目标下架短链落地兜底（TBD-1） | "商品已下架"提示页 / 推荐相似 / 引导首页 |
| 待评估 | 用户分享短链滥用管控（TBD-2） | 刷量 / 不当内容紧急关闭 |
| 后续立项 | 推荐拉新计划 | 邀请奖励 + 反作弊，独立模块 |
| Phase 3 | 站内社交 | 关注 / 信息流 / 社区达人 |

### 4.3 待规划事项（TBD）

| 编号 | 事项 | 说明 | 状态 |
|------|------|------|------|
| TBD-1 | 用户分享短链目标下架后的落地处理 | 目标商品 / 页面已下架但链接仍被点击，需兜底页而非 404 | 后续规划 |
| TBD-2 | 用户分享短链滥用管控 | 刷量 / 不当内容的紧急关闭手段，优先级与触发条件待定 | 待评估 |
| TBD-3 | 归因转化 / 归因订单 | 点击→下单 / 注册链路打通，依赖订单回传 UTM/click_id + 用户身份识别 | 后续规划 |

---

## 五、数据与埋点

> ⚠ 以下为事件框架设计。具体埋点字段规范待埋点平台模块设计统一规则后补充，再进入开发。

### 5.1 分享漏斗与核心事件

**核心漏斗**：分享入口曝光 → 弹窗打开 → 渠道点击 → 分享完成 → 链接被点击 → 安装 / 注册 / 首单。

| 事件名 | 触发时机 | 关键字段 |
|--------|---------|---------|
| `share_entry_view` | 分享按钮曝光 | page, product_id, platform |
| `share_sheet_open` | 弹窗 / 面板打开 | channels_shown（用户看到的渠道列表） |
| `share_channel_click` | 选择某渠道 | channel, channel_position, is_dynamic, short_code |
| `share_complete` | 分享动作完成 | channel, short_code |
| `share_sheet_dismiss` | 弹窗关闭（放弃） | dismiss_action, time_open_ms, any_channel_clicked |
| `share_more_click` | 点击 More | channels_shown_before_more |
| `share_link_click`（服务端） | 接收方点击短链 | short_code, channel（UTM/Referer 反推）, is_new_visitor |

### 5.2 关键指标

| 指标 | 计算 |
|------|------|
| 分享按钮 CTR | `share_sheet_open` / `share_entry_view` |
| 渠道选择率 | `share_channel_click(channel=X)` / `share_sheet_open` |
| 弹窗放弃率 | `share_sheet_dismiss(any_channel_clicked=false)` / `share_sheet_open` |
| More 使用率 | `share_more_click` / `share_sheet_open`（高则首屏渠道不够） |
| 渠道位置效应 | 按 channel_position 分组的点击率 |
| 分享点击率 | 链接被点击次数 / 分享次数 |

### 5.3 用户 ID 处理（未登录场景）

- 所有事件同时携带 `user_id`（登录时有值）和 `anonymous_id`（始终有值），登录后通过 ID Merge 关联历史行为。
- Web 端 anonymous_id：localStorage 持久化 + 服务端 Cookie 双存备份。
- App 端 anonymous_id：iOS Keychain / Android EncryptedSharedPreferences。

### 5.4 系统弹窗 vs 自定义弹窗追踪差异

| 追踪能力 | 系统弹窗（More） | 自定义弹窗 |
|---------|----------------|----------|
| 链接被点击（UTM/short_code） | ✅ | ✅ |
| 用户点了分享按钮 | ✅ | ✅ |
| 用户选了哪个渠道 | ❌ 拿不到 | ✅ |
| 弹窗放弃 | ✅ | ✅ |

核心差距：系统弹窗（More）拿不到用户最终选的渠道，`channel` 记为 `native_share`，接收方点击后由服务端从 Referer 反推。因页面内有明显自定义分享入口，大部分用户走自定义路径，可追踪率 80%+。

---

## 六、附录

### 6.1 设计稿索引

| 模块 | 子页面 | PC 设计稿 | APP 设计稿 |
|------|--------|----------|-----------|
| C 端商品分享 | 商品详情 + 分享弹窗 | `looply-share-prototype.pen` → `tFl2A`（PC Web） | `rMtyB`（iOS）/ `9wWk7`（Android）/ `NPfew`（Mobile Web） |
| C 端商品分享 | iOS 系统分享面板（示意） | — | `vYyqr` |
| 后台短链管理 | 短链列表 | `looply-社媒分享管理-antd-原型-v1.2.html` → `ShortLinkListPage` | 后台无 APP 端 |
| 后台短链管理 | 创建运营短链 | 同上 → `ShortLinkCreatePage` | 后台无 APP 端 |
| 后台短链管理 | 短链详情 | 同上 → `ShortLinkDetailPage` | 后台无 APP 端 |

### 6.2 数据模型参考（ER v1.1）

本模块涉及 3 张自有表 + 3 张外部只读表，详见 `实体关系图/looply-社媒分享实体关系图-v1.1`。

| 表 | 类型 | 关键字段 | 本期使用情况 |
|----|------|---------|------------|
| `short_links` | 自有（核心） | short_code(PK) / long_url / utm_source / utm_medium / utm_campaign / utm_content / product_id / sharer_user_id / session_id / created_by / campaign_name / click_count / unique_visitor_count / status / created_at | 全字段使用；`status` 字段保留但 MVP 不操作 |
| `share_clicks` | 自有（追踪） | id(PK) / short_code(FK) / visitor_id / user_id / clicked_at / ip / user_agent / referer | 全字段使用（详情页点击记录） |
| `share_attributions` | 自有（归因） | id(PK) / short_code(FK) / user_id / event_type / order_id / gmv_cents / attributed_at | **本期不写入**（归因转化为 TBD-3，预留表结构） |
| `products` | 外部只读 | product_id / title / brand / price_cents / image_url | OG 卡片 + 列表商品名 |
| `users` | 外部只读 | user_id / username | 分享人 / 点击者识别 |
| `orders` | 外部只读 | order_id / user_id / total_cents | 归因订单（TBD-3，本期不用） |

> 接口清单属技术文档范畴，本 PRD 不含。

### 6.3 给 ER 图的反馈（待产品确认后回写 ER）

PRD 撰写过程中发现的 ER 优化点，供后续回写 ER 图：

| # | 项 | 说明 |
|---|---|---|
| 1 | `short_links.status` 枚举定义 | 当前 ER 仅标"状态"，建议补枚举：`active`（启用）/ `disabled`（停用）/ `expired`（过期）。MVP 默认 active，启停为后续迭代 |
| 2 | `share_attributions.event_type` 枚举定义 | 建议补枚举：`signup`（注册）/ `first_order`（首单）/ `repeat_order`（复购）。本期不写入，预留 |
| 3 | 早期 `link_type` 字段已废弃 | 用 `utm_medium`（social_share vs 运营值）区分用户 / 运营，无需单设 link_type，ER 当前已无此字段，确认保持 |

