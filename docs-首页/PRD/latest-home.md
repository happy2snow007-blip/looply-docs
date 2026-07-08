# Looply · 首页 PRD v1.4

> 版本：v1.4 | 日期：2026-07-08 | 端：移动端（主）+ PC 端
> 状态：🔄 迭代中

---

## 目录

- [§1 概述](#1-概述)
- [§2 全局上下文 — Market & Language](#2-全局上下文--market--language)
- [§3 顶部导航 Header](#3-顶部导航-header)
- [§4 搜索功能](#4-搜索功能)
- [§5 首页 Banner（home_banner 资源位）](#5-首页-bannerhome_banner-资源位)
- [§6 信任板块 Trust Bar](#6-信任板块-trust-bar)
- [§7 精选合集 Collections（home_collection 资源位）](#7-精选合集-collectionshome_collection-资源位)
- [§8 Explore Finds Feed 流](#8-explore-finds-feed-流)
- [§9 底部导航 Tab Bar（移动端）](#9-底部导航-tab-bar移动端)
- [§10 页脚 Footer（PC 端）](#10-页脚-footerpc-端)
- [§11 登录态差异矩阵](#11-登录态差异矩阵)
- [§12 降级策略汇总](#12-降级策略汇总)
- [§13 性能要求](#13-性能要求)
- [§14 依赖与风险](#14-依赖与风险)
- [§15 版本规划](#15-版本规划)
- [§16 数据与埋点](#16-数据与埋点)
- [§17 附录 — 设计稿索引](#17-附录--设计稿索引)

---

## §1 概述

### §1.1 背景与目标

Looply 是面向美国市场的大牌二手电商平台。首页是用户进入 App 的第一个落点，承担三项核心任务：

1. **建立品牌信任**：通过 Trust Bar 传递鉴定能力和正品心智，降低用户对二手品的顾虑
2. **运营精选曝光**：通过 Banner + Collections 资源位传递活动和品类场景
3. **个性化留存**：通过 Feed 流持续为用户发现好货，加深浏览深度

### §1.2 不做什么（MVP 边界）

| 功能 | MVP 状态 | 说明 |
|------|----------|------|
| 搜索联想词 / 模糊匹配 | ❌ 不做 | 搜索输入态不展示候选词 |
| 搜索配置后台 | ❌ 不做 | 搜索占位词和热门趋势一期硬编码 |
| PC 端搜索框交互 | ⏳ 待做 | 搜索框当前为占位，交互设计优先级靠后；预置搜索内容待搜推确认后再实现 |
| Deals Tab | ❌ 隐藏 | 营销系统未上线，一期不展示 |
| Best Sellers Tab | ❌ 隐藏 | MVP 原型未实现，后续版本上线 |
| Trust Bar 运营配置 | ❌ 不做 | 前端硬编码，内容固定 |
| Feed Tab 顺序配置 | ❌ 不做 | Tab 前后顺序固定，暂未做配置化 |
| C1 回收/寄卖入口 | ❌ 不做 | 当前仅 C2 买家侧业务 |
| PC Navbar Heart/Cart 侧栏 | ❌ 不做 | MVP 暂不设计侧栏展开交互，后续迭代 |

### §1.3 用户角色

| 角色 | 状态 | 首页核心行为 |
|------|------|-------------|
| 访客（未登录） | 未登录 | 浏览 Feed、查看 Banner、搜索商品 |
| 普通买家（已登录） | 已登录 | 个性化推荐、收藏、购物车 |

### §1.4 核心场景

| 场景 | 用户状态 | 首页对应模块 |
|------|----------|-------------|
| Discover：第一次打开 Looply | 无行为数据 | Trust Bar → Feed (New Arrivals) |
| Browse：没有明确需求，随便逛 | 有/无行为数据 | Banner → Collections → Feed (For You / New Arrivals) |
| Intent：有明确品类或品牌需求 | 任意 | 搜索 → (跳转搜索结果页) |
| Consideration：回来看收藏/考虑下单 | 已登录 | Feed (For You) → (跳转商详) |

### §1.5 全局页面流转

```
首页
├── 搜索展开卡 ──→ 搜索结果页（点击搜索词 / 提交搜索）← 跳转暂不做，搜索结果页待设计
├── Banner CTA ──→ 活动落地页 / 品类页（landing_page 字段决定）← 跳转暂不做，结果页待设计
├── Collections 卡片 ──→ 合集落地页 ← 跳转暂不做，结果页待设计
├── Feed 商品卡 ──→ 商品详情页 ← 已有，参考商详 PRD
├── Header Market & Language ──→ 展开 Market & Language 面板（浮层，不跳页）
├── Header Account 图标（未登录）──→ 弹出登录引导浮层（Sign In / Create Account）
├── Header Account 图标（已登录）──→ 展开账户菜单浮层（My Orders / My Profile / Settings / Sign Out）
└── 底部 Tab Bar ──→ Shop / Favorites / Account

> ⚠️ 首页不关注以下 Header 展开态，本期不设计、不交付：
> - 🔍 Search bar 点击展开搜索卡（PC 端）
> - ♡ Favorites 侧栏滑出
> - 🛒 Cart 侧栏滑出 / 数量徽标
> 上述交互即便在原型文件中有示意，首页 PRD 本期也不覆盖，待对应页面设计完成后再补。
```

### §1.6 术语说明

| 术语 | 含义 |
|------|------|
| `market_id` | Looply 内部市场标识符（见 Market PRD v1.2） |
| `country_code` | ISO 3166-1 alpha-2 国家代码（如 `US`、`GB`） |
| `language_code` | BCP 47 语言代码（如 `en`、`zh-Hans`） |
| `currency_code` | ISO 4217 货币代码（如 `USD`、`GBP`） |
| `zone_key` | CMS 资源位唯一标识（如 `home_banner`、`home_collection`） |
| `listing_price` | 商品当前上架价格 |
| `grade` | 商品成色等级：NWT / Excellent / Good / Fair |
| Trust Bar | 首页信任板块，前端硬编码，不通过 CMS 配置 |
| 资源位 | CMS 系统中由运营人员配置的内容插槽 |

---

## §2 全局上下文 — Market & Language

首页加载时，系统需确定当前用户所在的 Market 以及使用的语言。此上下文影响资源位内容、货币显示。

### §2.1 市场（Market）自动识别机制

用户所在的 **country** 决定 **market**：每个 country 唯一隶属于一个 market（`market_country` 表），系统先确定 `country_code`，再映射至唯一的 `market_id`。

App 端和 Web 端可获取的信号不同，优先级分别如下：

**App 端**

| 优先级 | 来源 | 说明 |
|--------|------|------|
| 1 | 用户已保存的选择 | 持久化存储（见 §2.4）中的 `saved_country_code` → 映射 `market_id` |
| 2 | 设备位置 | 用户已授权时，系统 Location API（GPS + WiFi 融合）取经纬度 → 反解 `country_code` |
| 3 | IP 地理位置 | 服务端请求 IP → GeoIP 库 → `country_code`；VPN/代理场景可能偏差 |
| 4 | 语言推断 | 系统首选语言 → `market_language.default_language_code` 匹配的 market；多个匹配取 `market.priority` 最高的 |
| 5 | 默认兜底 | US 市场，货币 USD |

**Web 端**

| 优先级 | 来源 | 说明 |
|--------|------|------|
| 1 | 用户已保存的选择 | localStorage 中的 `saved_country_code` → 映射 `market_id` |
| 2 | IP 地理位置 | 服务端请求 IP → GeoIP 库 → `country_code`；VPN/代理场景可能偏差 |
| 3 | 语言推断 | `Accept-Language` / `navigator.language` 首项 → `market_language.default_language_code` 匹配的 market；多个匹配取 `market.priority` 最高的 |
| 4 | 默认兜底 | US 市场，货币 USD |

**country_code → market_id 映射规则**（来自 Market PRD v1.2）：
- 查 `market_country` 表，找 `country_code` 匹配且 `market.status = 'running'` 的记录
- 每个 country 唯一隶属于一个 market，无多映射情况

**时机**：首页 SSR/初始化请求时由服务端完成判断，结果通过 `market_id` + `currency_code` 随页面数据下发。客户端不重复检测。

### §2.2 语言（Language）自动识别机制

**App 端**

| 优先级 | 来源 | 说明 |
|--------|------|------|
| 1 | 用户已保存的选择 | 持久化存储（见 §2.4）中的 `saved_language_code` |
| 2 | 系统首选语言 | iOS: `preferredLanguages[0]`；Android: `Locale.getDefault()` |
| 3 | 默认兜底 | `en` |

**Web 端**

| 优先级 | 来源 | 说明 |
|--------|------|------|
| 1 | 用户已保存的选择 | localStorage 中的 `saved_language_code` |
| 2 | 浏览器语言 | `navigator.language` 或 `Accept-Language` 首项 |
| 3 | 默认兜底 | `en` |

### §2.3 Market & Language 切换面板

**入口**：
- 移动端：Header 右侧 Globe 图标（市场与语言设置）
- PC 端：Navbar 右侧 Globe 图标

> ⚠️ 当前方案：语言和市场设置入口在 Globe 图标。后续建议收口到 Account 页进行手动设置（Account 功能待设计）。

**面板形态**：
- 移动端：从 Header 下方向下展开（dropdown），背景遮罩
- PC 端：下拉浮层，出现在 Globe 图标正下方

**视觉设计**：见 Figma 设计稿
- 移动端：[移动端设计稿 · Market & Language 面板](https://www.figma.com/design/rLK7XCdVvYqEHQHd7WjOkk/Looply-v1.0?node-id=452-127&p=f&t=RlXBrpSFytzKCkEh-0)
- PC 端：[PC 端 Header & Footer](https://www.figma.com/design/rLK7XCdVvYqEHQHd7WjOkk/Looply-v1.0?node-id=1378-22993&p=f&t=RlXBrpSFytzKCkEh-0)

**面板结构（先语言，后国家）**：上部为 Language 单选列表，下部为 Country 单选列表（国旗 + 国家名 + 该国所属 market 货币代码），底部 Apply 按钮。

**交互规则**：
1. 语言变更后，Country 候选列表立即根据新语言重新渲染（国家名展示当前语言版本）
2. 两者均为单选
3. Country 候选项：国旗 emoji（由 `country_code` 映射）+ 国家名称 + 货币代码；仅展示 `market.status = 'running'` 的 market 下属的所有 country
4. 选择完成后点击 Apply 确认：系统通过 `market_country` 表将所选 `country_code` 映射至 `market_id`，浮层关闭，页面以新 `market_id` 刷新首页资源位内容
5. 关闭浮层未点击 Apply → 不保存，恢复原值

**字段映射**（来自 Market PRD v1.2）：

| 面板展示 | 字段来源 |
|----------|---------|
| Language 选项文本 | `language.local_name` |
| Country 国旗 | `country_code` → Unicode 国旗 emoji |
| Country 名称 | `country.country_name`（当前语言版本）|
| Country 货币 | `country` 所属 market 的 `default_currency_code` |

### §2.4 持久化策略

| 数据 | 存储位置 | 生命周期 |
|------|----------|---------|
| 已登录用户的语言和国家选择（`saved_language_code` + `saved_country_code`） | 用户账号 profile（服务端） | 永久，直至用户再次修改 |
| 未登录访客的语言和国家选择 | 客户端本地（App: UserDefaults/SharedPreferences；Web: localStorage） | 30 天 |

---

## §3 顶部导航 Header

### §3.1 移动端 Header

**视觉设计**：[移动端设计稿 · Header](https://www.figma.com/design/rLK7XCdVvYqEHQHd7WjOkk/Looply-v1.0?node-id=452-127&p=f&t=RlXBrpSFytzKCkEh-0)

**布局（从左到右）**：Logo（左对齐，点击返回首页）→ Search Pill（居中，内含搜索图标 + 预埋占位词，点击进入搜索展开态）→ Market & Language 图标（点击展开面板，见 §2.3）

**Search Pill 预埋占位词**：
- MVP 一期：前端硬编码轮播词列表：`["Chanel", "bags", "iPhone", "Gucci", "cameras", "Prada", "watches"]`
- 展示方式：每隔 3 秒切换到下一个词，淡入淡出动画；切换时显示为灰色占位文字（非实际输入内容）
- 后续迭代：词库由运营后台配置（搜索配置页）+ 算法策略动态生成

**Header 滚动行为**：sticky 吸顶，始终可见。

### §3.2 PC 端 Header

PC 端 Header 包含 Announcement Bar + Navbar，导航内容与结构详见[导航栏配置 PRD v1.2](looply-导航栏配置-PRD-v1.2.html)。样式见 [PC 端 Header & Footer 设计稿](https://www.figma.com/design/rLK7XCdVvYqEHQHd7WjOkk/Looply-v1.0?node-id=1378-22993&p=f&t=RlXBrpSFytzKCkEh-0)。

**首页相关的补充说明**：
- Announcement Bar：MVP 一期文案前端硬编码，正式文案由运营提供
- Navbar 右侧（navRight）：本期展示 Market & Language 入口（见 §2.3）+ Account 入口（已登录 → hover 展开账户菜单；未登录 → 点击跳转登录页）；搜索、收藏、购物车图标本期不在首页展示
- Navbar 滚动行为：向下滚动后 Navbar sticky 吸顶，Announcement Bar 可随页面滚动消失

---

## §4 搜索功能

> ⚠️ **本章节为搜索功能框架说明，搜索展开样式、内容策略（Hot Trends 词库、联想词逻辑）均由搜推团队负责设计与实现，首页 PRD 不定义具体搜索逻辑。**
> **开发阶段暂时只保留搜索 icon 占位，展开态留白，待搜推团队补充设计后统一接入。**

### §4.1 搜索栏状态机

**状态转换图**：[移动端设计稿 · 搜索展开态](https://www.figma.com/design/rLK7XCdVvYqEHQHd7WjOkk/Looply-v1.0?node-id=452-127&p=f&t=RlXBrpSFytzKCkEh-0)

状态说明：
|------|----------|------|
| 默认态（Idle） | 初始 / 搜索收起后 | Search Pill 显示占位词轮播，无展开卡片 |
| 展开态（Expanded） | 点击 Search Pill（未输入内容） | Search Pill 变为可输入文本框，下方展开搜索卡片（含热门词） |
| 输入态（Typing） | 在搜索框中键入字符 | 搜索卡片内容隐藏（无联想词），光标闪烁 |
| 提交 | 点击搜索按钮 / 按 Enter / 点击搜索词 | 导航至搜索结果页 |
| 关闭 | 点击卡片外部遮罩区域 / 点击"取消"按钮 | 回到 Idle 态，搜索框内容清空 |

### §4.2 搜索展开卡片（Expanded 态）

展开卡片从 Search Pill 正下方向下滑出，紧贴搜索框底部，宽度覆盖整个屏幕宽度（移动端为全宽下拉卡片，浮于内容上方；PC 端为下拉卡片，宽度与搜索框对齐）。

**视觉设计**：[移动端设计稿 · 搜索展开卡](https://www.figma.com/design/rLK7XCdVvYqEHQHd7WjOkk/Looply-v1.0?node-id=452-127&p=f&t=RlXBrpSFytzKCkEh-0)

展开卡结构（Expanded 态）：
- 顶部：Recent Searches 区块（条件渲染：有历史时展示，最多 5 条，时间倒序；每条可单独删除；点击词 → 提交搜索）
- 底部：Hot Trends 区块（始终展示，品类标签 + 品牌标签）
- 无历史记录时：直接从 Hot Trends 开始，不留空白

输入态（Typing）：展开卡内容完全隐藏，用户继续输入直到手动提交。MVP 不做 autocomplete。

**Recent Searches**：
- 仅当本地存在搜索历史（`≥ 1` 条）时，整个 Recent Searches 区块才渲染
- 无历史：直接从 Hot Trends 开始，不留空白
- 最多展示最近 5 条，按时间倒序
- 每条右侧有 ✕ 按钮，点击删除该条记录（不关闭卡片）
- 点击词：记录到搜索历史，跳转搜索结果页

**Hot Trends**：
- MVP 一期：前端硬编码，内容如下：
  - 品类标签（Row 1，5 个）：`Luxury Bags`、`Watches`、`Jewelry`、`Smartphones`、`Cameras`
  - 品牌标签（Row 2，5 个）：`Gucci`、`Prada`、`Fendi`、`Leica`、`Sony`
- 标签样式：浅色填充胶囊，可点击；品类与品牌标签可用不同填充色区分
- 点击标签：以标签文字为关键词提交搜索，记录到搜索历史，跳转搜索结果页
- 后续迭代：支持运营后台配置 + 算法策略动态生成

### §4.3 搜索输入态

- 用户开始在搜索框中输入字符后，展开卡片内所有内容（Recent Searches + Hot Trends）**立即隐藏**
- 搜索框保持可见和可输入状态，背景不遮罩
- MVP 不做搜索联想词（autocomplete / fuzzy match）
- 用户继续输入直到手动点击搜索图标 / 按 Enter 提交

### §4.4 搜索历史本地持久化

| 数据 | 存储位置 | 生命周期 |
|------|----------|---------|
| 搜索历史（最近 20 条） | 客户端本地（App: UserDefaults；Web: localStorage） | 30 天，超时自动清除；用户手动删除单条 / 全部 |

---

## §5 首页 Banner（home_banner 资源位）

Banner 是首页最顶部的视觉焦点，内容由 CMS 系统控制（见 CMS PRD v2.5.1）。Banner 内容由 CMS 系统控制，详见 CMS PRD v2.5.1。

### §5.1 CMS 资源位规格

| 字段 | 值 |
|------|----|
| `zone_key` | `home_banner` |
| 最大配置数 | 4 条（按 `start_time` 和 `market_id` 过滤后取 active 状态） |
| 支持模板 | `banner_image`（P0）、`banner_video`（P1） |
| Terminal 维度 | App / PC 各自独立配置 |

**CMS 配置字段（前端消费）**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `asset_image` | URL | Banner 图片地址（banner_image 模板使用） |
| `asset_video` | URL | Banner 视频地址（banner_video 模板使用） |
| `title` | 文本 | 主标题文案（可为空） |
| `subtitle` | 文本 | 副标题文案（可为空） |
| `cta_text` | 文本 | CTA 按钮文案（如 "Explore Finds →"） |
| `text_color` | HEX | 覆盖在图片上的文字颜色（默认白色） |
| `landing_page` | URL | 点击跳转地址，由 CMS 后台提供 |

### §5.2 移动端 Banner 展示规则

**视觉设计**：[移动端设计稿 · Banner](https://www.figma.com/design/rLK7XCdVvYqEHQHd7WjOkk/Looply-v1.0?node-id=452-127&p=f&t=RlXBrpSFytzKCkEh-0)

- **多条 Banner**：分页展示（Carousel / Swiper），底部居中分页圆点指示器
- **自动轮播**：默认间隔 4 秒（可配置），点击暂停
- **覆盖层**：图片下方从底部向上渐变遮罩（用于文字可读性）
- **文字排布**（从下到上）：`cta_text` 按钮 → `subtitle` → `title`；文字左对齐，文字颜色读取 `text_color`
- **点击**：点击 Banner 任意区域（含 CTA 按钮）→ 跳转 `landing_page`

### §5.3 PC 端 Banner 展示规则

- 其余规则同移动端（轮播、自动播放、点击跳转 `landing_page`）

### §5.4 降级策略

| 场景 | 处理 |
|------|------|
| 当前 market 无 active Banner 配置 | 隐藏 Banner 区域，页面从 Trust Bar 开始 |
| 图片加载失败 | 显示品牌色填充背景，文字和 CTA 按钮正常显示 |
| 视频加载失败 | 自动降级展示 `asset_image`；若 `asset_image` 也加载失败，处理方式同图片加载失败 |

---

## §6 信任板块 Trust Bar

Trust Bar 展示 Looply 平台的核心鉴定和服务能力，建立用户信任。**MVP 阶段内容固定，前端硬编码，不接入 CMS 配置。**

### §6.1 内容结构

**位置**：Banner 正下方，Collections 正上方。

**交互线框图**

移动端（2×2 网格）：

```
┌─────────────────────────────────────────┐
│  Confidence in Every Find               │  ← 版块标题（不可折叠，无交互）
├───────────────────┬─────────────────────┤
│  [img 60×60]      │  [img 60×60]        │
│  Authenticated    │  Reliable           │
│  Luxury           │  Electronics        │
│  Expert-reviewed  │  Tested, refurbished│
│  through a        │  and ready for...   │
│  rigorous...      │                     │
├───────────────────┼─────────────────────┤
│  [img 60×60]      │  [img 60×60]        │
│  True to          │  Tech-Driven        │
│  the Piece        │  Verification       │
│  Real product     │  Powered by...      │
│  photos, clear... │                     │
└───────────────────┴─────────────────────┘
Trust Bar 整体不可点击，无跳转行为
```

PC 端（4×1 横排）：

```
┌──────────┬──────────┬──────────┬──────────┐
│[img]     │[img]     │[img]     │[img]     │
│Authenti- │Reliable  │True to   │Tech-Driven│
│cated     │Electron- │the Piece │Verif...  │
│Luxury    │ics       │          │          │
│subtitle  │subtitle  │subtitle  │subtitle  │
└──────────┴──────────┴──────────┴──────────┘
4列横排，布局更宽松
```

**各条目字段（MVP 硬编码）**：

| 序号 | 标题 | 副文案 |
|------|------|--------|
| 1 | Authenticated Luxury | Expert-reviewed through a rigorous authentication process. |
| 2 | Reliable Electronics | Tested, refurbished, and ready for everyday performance. |
| 3 | True to the Piece | Real product photos, clear condition notes, and listed flaws. |
| 4 | Tech-Driven Verification | Powered by intelligent technologies and trusted partners. |

> ⚠️ **文案待最终确认**：以上文案来自设计稿占位内容，运营提供最终版本后直接替换硬编码值。

每个条目配有一张缩略图，图片资源由设计同步提供，前端静态引入。

### §6.2 展示规则

- **移动端**：2 列 × 2 行网格，每格显示图标 + 标题 + 副文案
- **PC 端**：4 列 × 1 行横排
- Trust Bar 区域不可点击（无跳转行为）
- Trust Bar 不受 market_id 影响，全市场统一内容

---

## §7 精选合集 Collections（home_collection 资源位）

Collections 展示运营精选的商品合集场景（如 Everyday Carry、Travel Ready、Quiet Luxury），引导用户进入特定品类场景。内容由 CMS 系统控制。

### §7.1 CMS 资源位规格

| 字段 | 值 |
|------|----|
| `zone_key` | `home_collection` |
| 最大配置数 | 8 条（同一 market + terminal 下 active 状态的） |
| 支持模板 | `collection_card_slide`（P0）、`collection_chip`（P1）、`collection_card_small`（P1） |
| Terminal 维度 | App / PC 各自独立配置 |

**CMS 配置字段（前端消费）**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `asset_image` | URL | 合集封面图 |
| `title` | 文本 | 合集名称（如 "Everyday Carry"） |
| `subtitle` | 文本 | 合集副标题（可为空） |
| `collection_id` | ID | 关联的商品合集 ID |
| `landing_page` | URL | 点击跳转地址（由 CMS 后台提供） |

### §7.2 移动端 Collections 展示规则

**交互线框图（移动端横向滚动）**：

```
Curated Collections
←──────────────── 横向单行滚动（swipe 左右）────────────────→
 ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
 │          │  │          │  │          │  │  ...     │
 │  封面图   │  │  封面图   │  │  封面图   │  │  (更多)  │
 │          │  │          │  │          │  │          │
 │  Title   │  │  Title   │  │  Title   │  │  Title   │
 └──────────┘  └──────────┘  └──────────┘  └──────────┘
  横向滚动，点击→ landing_page，最多8张
```

**Section 标题**：`Curated Collections`（前端固定文案）

- 布局：横向单行滚动（horizontal scroll），左右滑动浏览更多
- 最多展示 8 张（由 CMS 活跃配置数决定）
- 点击卡片：跳转 `landing_page`

### §7.3 PC 端 Collections 展示规则

**Section 标题**：`Curated Collections` 或 `Explore Our Collection`（跟随设计稿确定）

- 布局：多列网格，不横向滚动
- 悬停（hover）：封面图轻微缩放效果
- 其余规则同移动端

### §7.4 降级策略

| 场景 | 处理 |
|------|------|
| 当前 market 无 active Collections 配置 | 隐藏整个 Collections 区域 |
| 图片加载失败 | 单张卡片图片渲染失败 → 该卡片不展示；若所有卡片均渲染失败 → 隐藏整个 Collections 区域，直接接下一模块 |

---

## §8 Explore Finds Feed 流

Feed 流展示平台上的个性化推荐商品，位于 Collections 下方，是首页沉浸浏览的主体。

### §8.1 Tab 结构

**视觉设计**：[移动端设计稿 · Feed Tab](https://www.figma.com/design/rLK7XCdVvYqEHQHd7WjOkk/Looply-v1.0?node-id=452-127&p=f&t=RlXBrpSFytzKCkEh-0)

**Tab 吸顶行为**：
- 页面向下滚动，当 Feed Tab 行到达顶部（移动端为 Header 底部，PC 端为 Navbar 底部）时，Tab 行开始 sticky 吸顶
- 吸顶期间 Tab 始终可见，用户可随时切换 For You / New Arrivals，不需要回滚到顶部
- 移动端吸顶时 Tab 行叠加在 Header 正下方；PC 端叠加在 Navbar 正下方
- 滚动回到 Feed 区域顶部以上时，Tab 行恢复原始位置（不再吸顶）

**Tab 样式**：胶囊式（pill style）
- 激活 Tab：深色背景填充，白色文字
- 未激活 Tab：透明背景，深色文字，边框
- Tab 容器：横向排列，左对齐，可横向滚动（如 Tab 超出宽度）

**Tab 列表（MVP）**：

| Tab | 标识 | MVP 状态 | 说明 |
|-----|------|----------|------|
| For You | `for_you` | ✅ 展示 | 个性化推荐（A1/A2/B/C 通路混排） |
| New Arrivals | `new_arrivals` | ✅ 展示 | 最近 X 天新上架商品（X 为可配置参数，默认 30 天，B 通路） |
| Best Sellers | `best_sellers` | ❌ 隐藏 | MVP 原型中未实现，后续版本上线 |
| Deals | `deals` | ❌ 隐藏 | 营销系统未上线，MVP 不展示 |

**Tab 顺序**：固定为 For You → New Arrivals，后续版本配置化。

**默认 Tab**：
- 有行为数据（历史交互 ≥ 1 次）→ For You
- 无行为数据（全新访客）→ New Arrivals

**推荐规则**：完整规则见《Looply 首页 Feed PRD v2.3》（`/Users/zz/looply/home/feed-prd/Looply-首页Feed-PRD-v2.3.md`）。首页 PRD 仅定义展示层规格，不重复推荐逻辑。

### §8.2 商品卡片规格

**布局**：
- 移动端：2 列等宽网格
- PC 端：4 列等宽网格

**卡片字段**：

| 字段 | 数据来源 | 说明 |
|------|---------|------|
| 商品图 | `listing.og_image_url`，降级 `product_image.main_image_url` | 首张实拍图，无则降级品牌图 |
| 品牌名 | `brand.brand_name_en`（via listing → product → standard_sku → spu → brand） | 全大写展示，禁止翻译 |
| 商品标题 | `listing.listing_title`，降级 `product.title` | 走 i18n，最多 2 行省略 |
| 当前价格（高亮展示） | `listing.listing_price` | 挂牌价（渠道售价），需做币种换算 |
| 原价（划线，条件展示） | `standard_sku.market_price` | 参考价（官方原价）；仅当两价格均存在时展示 |
| Save 标签（条件展示） | 前端计算：`market_price - listing_price` | 仅当两价格均存在时展示差额 |
| 收藏按钮 | 收藏模块 | outline（未收藏）/ filled（已收藏） |
| Sold Out 状态 | `listing.listing_status` | ENUM: listed / unlisted / presale |

**价格展示规则**：
- `listing.listing_price` 始终展示（挂牌价，当前渠道售价）
- 当 `standard_sku.market_price` 存在且 `market_price > listing_price` 时：同时展示划线原价 + Save 标签
- Save 标签值由前端计算：`market_price - listing_price`，展示条件：两价格字段均存在且 `listing_price < market_price`

**Sold Out 商品**：样式以 Figma 设计稿为准（[Looply v1.0 · Figma](https://www.figma.com/design/rLK7XCdVvYqEHQHd7WjOkk/Looply-v1.0?node-id=1554-31868)）。

### §8.3 收藏交互

**视觉设计**：[移动端设计稿 · 商品卡收藏交互](https://www.figma.com/design/rLK7XCdVvYqEHQHd7WjOkk/Looply-v1.0?node-id=452-127&p=f&t=RlXBrpSFytzKCkEh-0)

- 商品主图右上角：心形图标，默认 outline（未收藏）
- 点击后：即时切换为 filled（已收藏），触发收藏 API；若失败则回滚
- 未登录用户点击：弹出登录引导弹窗（非强制跳转，可关闭弹窗继续浏览）
- 已收藏商品的 heart 始终显示 filled 状态

### §8.4 PC 端商品列表加载方式

**PC 端采用分页加载（非无限滚动）**：

- 首屏默认展示 **16 个商品**（4 列 × 4 行）
- 页面底部展示「View More」按钮
- 点击「View More」每次追加加载 **4 行（16 个）**商品，追加至当前列表末尾
- **无翻页 / 页码逻辑**，仅 View More 追加
- 加载中：View More 按钮显示 loading 状态
- 所有商品加载完毕：隐藏 View More 按钮，显示"You've seen it all"

**移动端**保持原有无限滚动逻辑：
- 首屏约 20 个商品，滚动至接近底部时触发加载下一页
- 加载失败：底部显示 Retry 按钮

**Section 标题**：`Explore Finds`（前端固定文案），紧贴 Tab 行上方。

---

## §9 底部导航 Tab Bar（移动端）

**视觉设计**：[移动端设计稿 · Tab Bar](https://www.figma.com/design/rLK7XCdVvYqEHQHd7WjOkk/Looply-v1.0?node-id=452-127&p=f&t=RlXBrpSFytzKCkEh-0)

**位置**：fixed 吸底，内容页面可滚动穿透 Tab Bar 下方。

**Tab 列表**：

| Tab | 激活状态 |
|-----|---------|
| Home | filled icon，品牌色 |
| Shop | filled icon |
| Favorites | filled icon |
| Account | filled icon |

- 激活 Tab：filled 图标 + 加粗文字 + 品牌色
- 非激活：outline 图标 + 灰色

**首页对应**：Tab Bar 中 Home 为激活态

---

## §10 页脚 Footer（PC 端）

PC 端首页最底部展示通用 Footer。移动端首页无 Footer（由 Tab Bar 替代导航）。

**视觉设计**：[PC 端设计稿 · 首页全页](https://www.figma.com/design/rLK7XCdVvYqEHQHd7WjOkk/Looply-v1.0?node-id=1474-30799&p=f&t=RlXBrpSFytzKCkEh-0)

**页面纵向结构**（从上到下）：Announcement Bar → Navbar（sticky）→ Banner → Trust Bar → Curated Collections → Explore Finds（View More 追加加载）→ Footer

**Footer 内容（MVP 版）**：

> ℹ️ MVP 阶段 Footer 内容与 Shopify 默认保持一致，内容不变。参考【Footer截图（shopify）】。Footer 内所有交互、跳转、二级页面暂不设计。如有余力可重新排版，优先级靠后，不强制。

- Footer 背景色：深色（见设计稿）
- 底部版权：`© 2026 Looply. All rights reserved.`

---

## §11 登录态差异矩阵

| 功能 | 未登录 | 已登录 |
|------|--------|--------|
| 浏览 Feed / Banner / Collections | ✅ 正常展示 | ✅ 正常展示 |
| Feed For You 推荐 | 基于 anonymous_user_id 的行为数据（若无历史→ New Arrivals 兜底） | 基于 user_id 的行为数据 |
| 商品卡片收藏（Heart） | 点击 → 登录引导弹窗 | 即时收藏，同步账户 |
| Header Cart 徽标 | — | — |
| Header Favourite 图标 | — | — |
| Market & Language 选择持久化 | 本地存储（30 天） | 账号 profile 永久保存 |

---

## §12 降级策略汇总

| 模块 | 场景 | 降级处理 |
|------|------|---------|
| Market 识别 | 所有来源均失败 | 默认 US 市场（market_id = US_MARKET_ID） |
| Banner（home_banner） | 无 active 配置 | 隐藏整个 Banner 区域 |
| Banner（home_banner） | 图片加载失败 | 显示品牌色背景块，文字和 CTA 按钮正常显示 |
| Trust Bar | 静态资源加载失败 | 显示文字条目，隐藏图标 |
| Collections（home_collection） | 无 active 配置 | 隐藏整个 Collections 区域 |
| Collections（home_collection） | 图片加载失败 | 单张卡片渲染失败 → 该卡片不展示；全部失败 → 隐藏整个区域 |
| Feed | 推荐服务异常 | For You 降级至 New Arrivals 商品池排序兜底 |
| Feed | 商品池为空 | 展示"No items available"空态插图 |
| Feed | 下一页加载失败 | 底部显示 Retry 按钮，不崩溃 |
| 搜索展开卡片 | 无搜索历史 | 隐藏 Recent Searches 区块，直接展示 Hot Trends |

---

## §13 性能要求

> ℹ️ 以下指标为产品侧参考建议，最终目标值由研发团队根据实际情况确认。

| 指标 | 目标值 | 说明 |
|------|--------|------|
| 首屏 LCP（Largest Contentful Paint） | ≤ 2.5s（P75） | Banner 图片为 LCP 候选元素，需优先加载 |
| Feed 首屏 TTI（Time to Interactive） | ≤ 3.5s（P75） | 首屏 20 张卡片渲染完成 |
| 图片格式 | WebP（AVIF 可选） | Banner 和商品主图使用 CDN 压缩版本 |
| Feed 分页加载 | ≤ 800ms（P90） | 下一页 20 条 API 响应时间 |
| Banner 图片预加载 | 首屏 Banner 图片 `<link rel="preload">` | 减少 LCP 时间 |

---

## §14 依赖与风险

### §14.1 上下游系统依赖

| 系统 | 依赖内容 | PRD 文档 |
|------|---------|---------|
| CMS 系统 | `home_banner` + `home_collection` 资源位配置和下发 API | CMS PRD v2.5.1 |
| Market 系统 | `market_id` 映射、country → market 关系、Market 列表枚举 | Market PRD v1.2 |
| 商品系统 | 商品列表（listing_id / grade / listing_price / main_image_url / listed_at） | 商品系统 PRD |
| Feed 推荐引擎 | For You / New Arrivals / Best Sellers 商品列表 API | Feed PRD v2.3 |
| GeoIP 服务 | IP → country_code 地理位置解析 | 外部服务（三方库或自建） |
| 用户系统 | 收藏状态、购物车数量、账号信息 | 用户/账号 PRD |
| Collections 合集系统 | collection_id 对应的合集数据 | Collections PRD v1.0 |
| 商品详情系统 | 商品详情页（Feed 商品卡点击跳转目标） | 商详 PRD（已有） |

### §14.2 关键依赖缺口

| 缺口 | 影响 | 状态 |
|------|------|------|
| `listed_at` 字段 | New Arrivals / B 通路排序依赖此字段，商品系统尚未添加 | 需向商品系统提需求（见 Feed PRD §25.2） |
| 营销系统 | Deals Tab、划线价均依赖营销系统，MVP 均不上线 | 后续迭代 |
| GeoIP 库选型 | IP → country_code 需选定服务商 | 待技术确认 |
| Trust Bar 最终文案 | 当前为设计稿占位文案，运营未提供最终版本 | 待运营提供 |

### §14.3 风险

| 风险 | 等级 | 缓解措施 |
|------|------|---------|
| Market 识别失败导致错误币种 | 高 | 兜底默认 US，前端显示"Price in USD"提示 |
| CMS 资源位请求超时 | 中 | 隐藏对应区域，不阻塞页面主体加载 |
| Feed 推荐服务不稳定 | 中 | 降级到 B 通路直接排序，用户体验可接受 |
| Banner 大图影响 LCP | 中 | 图片 preload + CDN + WebP 格式 |

---

## §15 版本规划

### §15.1 当前版本（v1.0 / MVP）

- 首页移动端 + PC 端全结构
- Market & Language 自动识别 + 手动切换面板
- Search 展开卡（Recent Searches + Hot Trends 硬编码，仅移动端）；PC 端搜索框为占位，展开态本期不设计
- home_banner + home_collection CMS 资源位
- Trust Bar 硬编码（待运营文案）
- PC 端 Navbar：NavLinks 内容与结构见[导航栏配置 PRD v1.2](looply-导航栏配置-PRD-v1.2.html)；navRight 本期展示 Market & Language + Account；搜索/收藏/购物车图标本期不在首页展示，其展开态不属于首页交付范围
- PC 端 Navbar Account 交互：未登录 → Sign In 引导浮层；已登录 → 账户菜单（My Orders / My Profile / Settings / Sign Out）；浮层外点击关闭
- PC 端 Navbar：含二级/三级导航展开面板（结构见导航栏配置 PRD，Brands Mega Menu MVP 采用版本 A）
- Feed 两 Tab（For You / New Arrivals），Best Sellers 和 Deals 隐藏
- 商品卡片（无促销价）
- PC 端 Feed 分页加载：默认 16 个，View More 追加 4 行，无页码

### §15.2 后续迭代方向（建议）

| 功能 | 预期版本 | 条件 |
|------|---------|------|
| Best Sellers Tab 上线 | v1.1 | Feed PRD 热卖榜通路就绪 |
| Deals Tab 上线 | v1.1 | 营销系统上线 |
| 促销价展示 | v1.1 | 营销系统上线 |
| 搜索配置后台（Hot Trends 运营化） | v1.1 | 搜索配置页开发完成 |
| PC 端搜索框展开态交互 | v1.1 | 搜推确认预置内容后实现 |
| PC Navbar Favorites / Cart 侧栏 | v1.1 | Favorites 页 / 购物车页完成后补 |
| Trust Bar CMS 化 | v1.2 | CMS 扩展支持 trust_bar 区块 |
| Feed Tab 顺序配置化 | v1.2 | Feed 配置后台扩展 |
| 搜索联想词 | v1.2 | 搜索引擎接入 |
| 匿名行为合并（anonymous → user_id） | v1.1（Feed PRD V1.1） | 见 Feed PRD v2.3 §12.2 |

---

## §16 数据与埋点

所有事件均携带 `market_id`、`user_id`（已登录）或 `anonymous_user_id`（未登录）、`session_id`、`terminal`（App/PC）。

### §16.1 关键埋点事件

| 事件名 | 触发时机 | 关键参数 |
|--------|---------|---------|
| `page_view_home` | 首页加载完成 | `market_id`, `detected_market_source`（ip/saved/default 等） |
| `search_pill_tap` | 点击搜索 Pill，进入展开态 | `has_recent_searches`（bool） |
| `search_submit` | 搜索提交（按 Enter / 点击词 / 点击标签） | `query`, `source`（recent/trend_category/trend_brand/input） |
| `search_recent_delete` | 删除某条搜索历史 | `deleted_query` |
| `banner_view` | Banner 进入视口 | `banner_config_id`, `position`（第几张） |
| `banner_click` | 点击 Banner | `banner_config_id`, `landing_page` |
| `collection_click` | 点击 Collections 卡片 | `collection_config_id`, `collection_id`, `position` |
| `feed_tab_switch` | 切换 Feed Tab | `to_tab`, `from_tab` |
| `product_card_view` | 商品卡片进入视口 | `listing_id`, `tab`, `position`, `rec_source`（A1/A2/B/C） |
| `product_card_click` | 点击商品卡片（跳商详） | `listing_id`, `tab`, `position`, `rec_source` |
| `product_favorite_toggle` | 点击收藏心形 | `listing_id`, `action`（add/remove）, `logged_in` |
| `market_language_panel_open` | 点击 Globe 图标 | — |
| `market_language_save` | 点击面板 Apply | `new_language_code`, `new_country_code`, `new_market_id` |

### §16.2 Feed 行为数据

Feed 相关埋点的详细定义见《Looply 首页 Feed PRD v2.3》§10 行为数据 + §19 埋点事件。首页 PRD 不重复定义。

---

## §17 附录 — 设计稿索引

| 页面 / 区域 | 端 | Figma 链接 |
|-------------|----|----|
| 首页 PC 端全页 | PC | [Looply v1.0 · PC 首页全页](https://www.figma.com/design/rLK7XCdVvYqEHQHd7WjOkk/Looply-v1.0?node-id=1474-30799&p=f&t=RlXBrpSFytzKCkEh-0) |
| PC 端 Header & Footer | PC | [Looply v1.0 · PC Header & Footer](https://www.figma.com/design/rLK7XCdVvYqEHQHd7WjOkk/Looply-v1.0?node-id=1378-22993&p=f&t=RlXBrpSFytzKCkEh-0) |
| 首页移动端全页 | App | [Looply v1.0 · 移动端首页](https://www.figma.com/design/rLK7XCdVvYqEHQHd7WjOkk/Looply-v1.0?node-id=452-127&p=f&t=RlXBrpSFytzKCkEh-0) |

---

*文档维护：Looply 产品团队 | 首页 PRD v1.4 | 2026-07-08*

---

## 变更日志

### v1.4 · 2026-07-08

| 编号 | 章节 | 变更内容 | 原因 |
|------|------|---------|------|
| C18 | §8.2 商品卡片规格 | 删除成色/评级标签（grade）字段及彩色标签颜色规范 | Figma 设计稿无成色标签，以 Figma 为准 |
| C19 | §8.2 商品卡片规格 | 删除线框图和视觉规范（字号、颜色、加粗等），改为字段表格 | 视觉规范由 Figma 承载，PRD 中重复定义反而会导致 AI 开发时混乱 |
| C20 | §8.2 商品卡片规格 | 价格逻辑从「MVP 仅展示 listing_price」升级为 V1 双价格逻辑：`listing.listing_price`（挂牌价高亮）+ `standard_sku.market_price`（参考原价划线，条件展示）+ Save 标签（前端计算差额，条件展示） | 对齐 Figma 交互稿及商品系统 ER 图确认的字段名，V1 正式行为 |
| C21 | §8.2 商品卡片规格 | Sold Out 展示由具体交互描述改为「样式以 Figma 设计稿为准」并附 Figma 链接 | 交互细节以设计稿为唯一基准，PRD 不重复描述 |
| C22 | §1.2 不做什么 | 「划线价 / 促销价」行改为「促销价」；说明更新为「V1 展示挂牌价 + 参考原价双价格逻辑」 | 对齐 C20 价格逻辑变更 |
| C23 | §15.2 后续迭代 | 「划线价 / 促销价展示」改为「促销价展示」 | 对齐 C20，划线参考价 V1 已实现，无需后续迭代 |
| C24 | §1.2 不做什么 | 删除「促销价」和「多语言 UI（i18n）」两行 | 促销价边界无需单独列出；多语言是要做的，不应列为不做项 |
| C25 | §2.2 语言识别机制 | 「用户已保存的选择」说明改为：在 Header Market & Language 面板手动选择并点击 Apply 后持久化的 `saved_language_code`；删除末尾「MVP 限制」说明 | 明确保存来源；移除多语言不做的错误描述 |
| C26 | §8.2 价格展示规则 | 删除「❌ 不展示促销价（营销系统未就绪）」一行 | 避免与已实现的双价格逻辑产生混淆 |
| C27 | §2.3 / §3.1 / §4.1 / §4.2 / §5.2 / §8.1 / §8.3 / §9 / §10 | 删除各章节 ASCII 线框图；替换为对应 Figma 链接（移动端全页 / PC 端全页 / PC 端 Header & Footer） | 线框图由手绘维护成本高且易与设计稿失同步，统一以 Figma 为唯一视觉基准 |
| C28 | §17 附录 — 设计稿索引 | 更新设计稿索引，全部替换为用户提供的 Figma 链接（PC 全页 / PC Header & Footer / 移动端全页） | 原索引指向已过期的 Untitled Figma 文件和本地 .pen 文件，对齐最新设计稿 |
| C29 | §3 顶部导航 Header | §3.2 PC 端 Header 大幅精简：删除 §3.2.1 Announcement Bar 详细规格、§3.2.2 Navbar 三栏尺寸布局描述、§3.2.3 导航下拉面板全部内容；改为「详见导航栏配置 PRD v1.2」链接，仅保留首页专有的补充说明（Announcement Bar 文案策略、navRight 本期展示范围、滚动行为） | 导航结构在导航栏配置 PRD 中已完整定义，首页 PRD 不重复 |
| C30 | 全文 | 删除所有像素值、尺寸数字、颜色色值、字号、边距等视觉规范描述（`52px`、`320px`、`#6432FC`、`14px`、`border-radius: 18px`、`$color-ink-primary` 等） | 视觉规范由 Figma 承载，PRD 负责功能逻辑，不应描述设计师职责范围内的内容 |
| C31 | §8.1 Feed Tab | 新增 Tab 吸顶行为：滚动至 Tab 行触顶时开始 sticky，移动端吸于 Header 下方，PC 端吸于 Navbar 下方，回滚至 Feed 区域上方后恢复 | 保证深度浏览时用户始终可切换 Tab，无需回滚顶部 |
| C32 | §4 搜索功能 | 在章节顶部新增免责说明：搜索展开样式及内容策略由搜推团队负责；开发阶段暂仅保留搜索 icon 占位，展开态留白待搜推补充 | 避免开发按 PRD 示例实现搜索展开 UI，造成后续搜推方案接入困难 |
| C33 | §2.1 市场识别机制 | 重写：明确用户选择 country（而非 market），每个 country 唯一隶属于一个 market；App/Web 优先级分列两表；App 侧设备位置调至 IP 之前；持久化字段改为 `saved_country_code`；删除"一国对应多个 market"兼容注释 | country → market 是一对一映射，原写法混淆了用户感知对象（country）和系统内部对象（market） |
| C34 | §2.2 语言识别机制 | 重写：App/Web 优先级分列两表，明确 App 读系统首选语言、Web 读 navigator.language；去掉混写的单表结构 | App 和 Web 语言信号来源不同，混表描述导致开发理解歧义 |
| C35 | §2.3 切换面板 | 面板下部从"Market 单选列表"改为"Country 单选列表"；候选项改为展示 running market 下属所有 country；Apply 动作说明改为 country_code → market_id 映射；字段映射表相应更新 | 用户实际选择的是国家，不是 market；market 由 country 唯一推导 |
| C36 | §2.4 持久化 / §16.1 埋点 | 持久化字段改为 `saved_country_code`；`market_language_save` 埋点增加 `new_country_code` 参数 | 对齐 C33/C35 变更 |
| C37 | §2.2 语言识别机制 | 删除"Market 默认语言"兜底档（App 第 3 档 / Web 第 3 档）；语言判断只依赖自身信号，不引入市场字段 | 语言和市场互相兜底是循环依赖，逻辑错误；语言信号（系统语言/浏览器语言）足以兜底，无需绕回市场 |

### v1.3 · 2026-07-02

| 编号 | 章节 | 变更内容 | 原因 |
|------|------|---------|------|
| C2 | §1.2 不做什么 | 新增 PC 端搜索框交互（⏳ 待做）、Best Sellers Tab（❌ 隐藏）、PC Navbar Heart/Cart 侧栏（❌ 不做）三行 | 对齐原型稿 MVP 边界 |
| C3 | §3.2 PC 端 Header | 删除 PC 端整体简笔画线框图；§3.2 改为"样式与交互见原型" | 线框图与原型重复且易失真，以原型为唯一视觉基准 |
| C4 | §3.2.2 NavLinks | 删除固定品类列表与顺序约束，改为「内容与顺序由 CMS 导航栏配置统一管理，详见导航栏配置 PRD」 | NavLinks 是全局可配置内容，非首页独有需求，不在此处硬编码 |
| C5 | §3.2.2 navRight | 删除逐图标交互说明；明确本期仅展示 Market & Language 入口 + Account 入口，搜索/收藏/购物车本期不在此处展示；图标样式与顺序以原型为准 | 与导航栏配置 PRD 对齐，避免首页 PRD 重复定义 |
| C6 | §3.2.3（新增） | 新增 PC 端导航下拉面板说明：一级（无面板）/ 二级（浮动小卡，2列）/ 三级（全宽面板，MVP 采用版本 A，版本 B 保留备选） | 原型稿新增交互设计 |
| C7 | §5.3 PC 端 Banner | 高度从 600px 改为 400px | 对齐原型稿实际定值 |
| C8 | §8.1 Feed Tab | Tab 从 3 个（For You / New Arrivals / Best Sellers）改为 2 个（For You / New Arrivals）；Best Sellers 改为 ❌ 隐藏 | 对齐原型稿 MVP 实现 |
| C9 | §8.4（重写） | PC 端由无限滚动改为分页加载：默认 16 个（4×4），点击 View More 追加 4 行，无页码；移动端保持无限滚动 | 对齐原型稿交互备注及 View More 按钮设计 |
| C10 | §10 Footer 线框图 | Banner 高度更正为 400px，Feed 描述从「无限滚动」改为「View More 追加加载」，Tab 更新为 2 个 | 对齐 C7/C8/C9 |
| C11 | §10 Footer 内容 | 改为「与 Shopify 默认保持一致，内容不变」，去掉硬编码列表，优先级靠后，不强制重排 | 对齐原型备注 |
| C12 | §15.1 当前版本 | 补全 PC Navbar 导航结构、搜索框状态、Feed Tab 变更、View More 分页信息 | 对齐原型实际范围 |
| C13 | §15.2 后续迭代 | 新增 Best Sellers Tab、PC 搜索框完整交互、PC Navbar Heart/Cart 侧栏三个迭代项 | 补全待做清单 |
| C14 | §1.5 全局页面流转 | 删除 Header 收藏/购物车图标跳转条目，改为 Account 浮层交互（未登录引导 / 已登录菜单）；新增说明：Search 展开卡、Favorites 侧栏、Cart 侧栏展开态本期不属于首页范围 | 明确首页 MVP 边界，避免开发对 Header 展开态产生误解 |
| C15 | §11 登录态差异矩阵 | Header Cart 徽标 / Header Favourite 图标两行改为「—」，本期首页不关注此两项 | 与 §1.5 边界对齐 |
| C16 | §15.1 当前版本 | 补充 PC 端 Account 浮层交互说明；明确搜索/收藏/购物车图标展开态不属于首页交付范围 | 与 §1.5 边界对齐，防止开发误交付 |
| C17 | §15.2 后续迭代 | 「PC 端搜索框完整交互」和「PC Navbar Heart/Cart 侧栏展开」描述对齐新边界说明 | 措辞清晰化 |

### v1.2 · 2026-06-18

| 编号 | 章节 | 变更内容 | 原因 |
|------|------|---------|------|
| C1 | §4.2 搜索展开卡片（Expanded 态） | 移动端展开卡片交互由 bottom sheet 改为全宽下拉卡片：紧贴搜索框底部向下滑出，宽度覆盖整个屏幕宽度，不从底部弹出 | 底部弹出与搜索入口位置脱节，用户视线从顶部搜索框跳到底部 sheet，体验断层；改为贴顶下拉后视觉连贯 |
