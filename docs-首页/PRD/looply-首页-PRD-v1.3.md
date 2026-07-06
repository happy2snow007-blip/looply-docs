# Looply · 首页 PRD v1.3

> 版本：v1.3 | 日期：2026-07-02 | 端：移动端（主）+ PC 端
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
| 划线价 / 促销价 | ❌ 不做 | 营销系统未就绪，商品卡片仅展示 listing_price |
| Trust Bar 运营配置 | ❌ 不做 | 前端硬编码，内容固定 |
| Feed Tab 顺序配置 | ❌ 不做 | Tab 前后顺序固定，暂未做配置化 |
| C1 回收/寄卖入口 | ❌ 不做 | 当前仅 C2 买家侧业务 |
| 多语言 UI（i18n） | ❌ 不做 | MVP 仅英文界面，语言选项仅影响 Market 关联的货币 / 配置，不影响页面文案翻译 |
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
├── Header 收藏图标 ──→ Favorites 页 ← 暂无
├── Header 购物车图标 ──→ 购物车页 ← 暂无
├── Header Market & Language ──→ 展开 Market & Language 面板（浮层，不跳页）
└── 底部 Tab Bar ──→ Shop / Favorites / Account
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

系统按以下优先级逐级判断，取第一个成功匹配的结果：

| 优先级 | 来源 | 说明 |
|--------|------|------|
| 1 | 用户已保存的选择 | 从本地持久化存储（见 §2.4）读取 `saved_market_id` |
| 2 | IP 地理位置 | 服务端通过请求 IP → GeoIP 库 → `country_code` → Market 系统映射 `market_id`；仅取"running"状态的 market |
| 3 | 设备 WiFi / 位置权限 | App 侧：若用户已授予位置权限，取设备 GPS/WiFi 所在国家 `country_code` → 同上映射；Web 侧不适用 |
| 4 | 浏览器语言首选项 | 从 `Accept-Language` 或 `navigator.language` 提取 `language_code` → Market 系统中首选语言为该语言的 market；多个 market 匹配时取 priority 最高的 |
| 5 | 默认兜底 | 使用 US 市场（`market_id` 对应美国），货币 USD |

**country_code → market_id 映射规则**（来自 Market PRD v1.2）：
- 查 `market_countries` 表，找 `country_code` 匹配且 `market.status = 'running'` 的记录
- 若一个国家对应多个 market（通常不会），取 `market.priority` 最高的

**时机**：首页 SSR/初始化请求时由服务端完成判断，结果通过 `market_id` + `currency_code` 随页面数据下发。客户端不重复检测。

### §2.2 语言（Language）自动识别机制

| 优先级 | 来源 | 说明 |
|--------|------|------|
| 1 | 用户已保存的选择 | 从本地持久化存储读取 `saved_language_code` |
| 2 | 设备系统输入法语言 | App 侧：读取系统首选语言（iOS: `preferredLanguages[0]`；Android: `Locale.getDefault()`） |
| 3 | 浏览器语言 | Web 侧：`navigator.language` 或 `Accept-Language` 第一项 |
| 4 | 当前 Market 的默认语言 | Market PRD 中 market 对应的 `default_language_code` |
| 5 | 默认兜底 | `en`（英文） |

**MVP 限制**：MVP 阶段 UI 界面固定为英文，语言识别结果不影响页面文案。多语言版本上线后，语言选择的影响包括：在 Market & Language 面板中回显用户当前语言、确定 Market 候选列表的展示语言、整体页面的文案展示。

### §2.3 Market & Language 切换面板

**入口**：
- 移动端：Header 右侧 Globe 图标（市场与语言设置）
- PC 端：Navbar 右侧 Globe 图标

> ⚠️ 当前方案：语言和市场设置入口在 Globe 图标。后续建议收口到 Account 页进行手动设置（Account 功能待设计）。

**面板形态**：
- 移动端：从 Header 下方向下展开（dropdown），背景遮罩
- PC 端：下拉浮层，宽 320px，出现在 Globe 图标正下方

**交互线框图**

移动端从 Header 下方向下展开的下拉面板：

```
┌────────────────────────────────┐
│                                │  ← 背景半透明遮罩（点击关闭）
│  ┌──────────────────────────┐  │
│  │                          │  │  ← 从 Header 下方向下展开
│  │  Language                │  │
│  │  ● English          ✓    │  │  ← 单选，已选中高亮
│  │  ○ 简体中文              │  │
│  │                          │  │
│  │  Market                  │  │  ← 语言改变后列表联动刷新
│  │  ● 🇺🇸 United States (USD)│  │
│  │  ○ 🇬🇧 United Kingdom (GBP)│  │
│  │  ○ ...                   │  │
│  │                          │  │
│  │  [        Apply         ]│  │  ← 点击确认并刷新页面
│  └──────────────────────────┘  │
└────────────────────────────────┘
点击遮罩 / 未点 Apply → 不保存，恢复原值
```

PC 端下拉浮层（Globe 图标正下方，宽 320px）：

```
                     ┌──────────────────┐
                     │ Language          │
                     │ ● English    ✓   │
                     │ ○ 简体中文       │
                     │                  │
                     │ Market           │
                     │ ● 🇺🇸 US (USD)  ✓│
                     │ ○ 🇬🇧 UK (GBP)   │
                     │                  │
                     │ [ Apply ]        │
                     └──────────────────┘
                          ↑ Globe 图标正下方，320px 宽
```

**面板结构（先语言，后市场）**：

```
┌─────────────────────────────┐
│  Language                   │  ← 区块标题
│  ○ English                  │  ← 单选，当前已选中高亮
│  ○ 简体中文                 │
│  ○ ...（仅展示 running 语言）│
│                             │
│  Market                     │  ← 区块标题（随语言更新）
│  ○ 🇺🇸 United States (USD)  │  ← 单选，含国旗 emoji + 货币代码
│  ○ 🇬🇧 United Kingdom (GBP) │
│  ○ ...（仅展示 running market）│
└─────────────────────────────┘
```

**交互规则**：
1. 语言变更后，Market 候选列表立即根据新语言过滤并重新渲染（展示语言本地化名称）
2. 两者均为单选
3. 市场候选项包含：国旗 emoji（由 `country_code` 映射）+ 国家名称 + 货币代码；仅展示 `market.status = 'running'` 的 market
4. 选择完成后点击"Apply"/"Save"按钮确认，浮层关闭，页面以新 `market_id` 刷新首页资源位内容
5. 关闭浮层未点击 Apply → 不保存，恢复原值

**字段映射**（来自 Market PRD v1.2）：

| 面板展示 | 字段来源 |
|----------|---------|
| Language 选项文本 | `language.local_name` |
| Market 国旗 | 由 `market.primary_country_code` → Unicode 国旗 emoji 计算得出 |
| Market 国家名称 | `country.country_name`（当前语言版本） |
| Market 货币 | `market.default_currency_code` |

### §2.4 持久化策略

| 数据 | 存储位置 | 生命周期 |
|------|----------|---------|
| 已登录用户的语言和市场选择 | 用户账号 profile（服务端） | 永久，直至用户再次修改 |
| 未登录访客的语言和市场选择 | 客户端本地（App: UserDefaults/SharedPreferences；Web: localStorage） | 30 天 |

---

## §3 顶部导航 Header

### §3.1 移动端 Header

**尺寸**：高度 52px，横向 full-width，背景色白色，底部无分割线（与 Banner 无缝连接）。

**交互线框图**

```
┌──────────────────────────────────────────────┐  h: 52px
│ LOOPLY  [ 🔍  Chanel...           ]  🌐      │
└──────────────────────────────────────────────┘
  ↑Logo      ↑Search Pill (flex 1)     ↑图标组
  18px       h:36px 圆角18px 灰色背景   24×24px
  Playfair   占位词每3s淡入淡出轮播     
  Italic
  点击→首页   点击→搜索展开态          🌐→Market面板
```

**布局（从左到右）**：

| 元素 | 规格 | 说明 |
|------|------|------|
| Logo | Playfair Display Italic，约 18px，`LOOPLY` | 左对齐，点击返回首页 |
| Search Pill | 胶囊形（border-radius: 18px），高度 36px，fill: 背景灰（`$color-surface-secondary`），占据大部分中间空间 | 内含搜索图标 + 预埋占位词；点击进入搜索展开态 |
| Market & Language 图标（🌐） | 24×24px，globe 形 | 点击展开 Market & Language 面板（见 §2.3） |

**Search Pill 预埋占位词**：
- MVP 一期：前端硬编码轮播词列表：`["Chanel", "bags", "iPhone", "Gucci", "cameras", "Prada", "watches"]`
- 展示方式：每隔 3 秒切换到下一个词，淡入淡出动画；切换时显示为灰色占位文字（非实际输入内容）
- 后续迭代：词库由运营后台配置（搜索配置页）+ 算法策略动态生成

**Header 滚动行为**：
- 向下滚动时：Header 保持 sticky（吸顶），始终可见
- 向上滚动时：Header 无额外动画，始终可见

### §3.2 PC 端 Header

**PC 端分为两层**：Announcement Bar + Navbar。样式与交互见原型「PC 首页原型稿 v1.0」。

#### §3.2.1 Announcement Bar（公告条）

- **高度**：40px
- **背景色**：`#6432FC`（品牌紫）
- **内容**：文字公告，MVP 一期前端硬编码文案（正式文案由运营提供）
- **文字**：14px，白色，居中
- **可关闭**：MVP 不做关闭按钮，始终展示

#### §3.2.2 Navbar

- **高度**：72px，背景色白色，底部 `1px solid #e5e7eb`
- **三栏布局**：navLeft（Logo + NavLinks）/ searchBar（320px 居中）/ navRight（图标组）

**navLeft（左栏）**：
- Logo：Playfair Display Italic，`LOOPLY`，点击返回首页
- NavLinks：一级导航入口列表，**内容与顺序由 CMS 导航栏配置统一管理**，非首页独有需求，详见「导航栏配置 PRD」（`/Users/zz/looply/cms/导航栏配置`）；字号 14px，Regular；hover 下划线；active 态文字加粗 + 品牌紫下划线

**searchBar（中栏）**：
- 宽度 320px，胶囊形，背景灰，内含搜索图标 + 占位词
- MVP 阶段搜索框为占位，交互设计优先级靠后；预置搜索内容待搜推确认后再做
- 点击后交互逻辑见 §4

**navRight（右栏）**：
- 图标样式与顺序以原型为准
- 本期展示：**Market & Language 入口**（点击展开下拉浮层，见 §2.3）、**我的（Account）**（已登录 → hover 展开个人中心菜单；未登录 → 点击跳转登录页）
- 搜索、收藏、购物车等其他图标**本期不在此处展示**

**Navbar 滚动行为**：向下滚动后 Navbar sticky 吸顶（Announcement Bar 可滚动消失）。

#### §3.2.3 PC 端导航下拉面板

PC 端 Navbar 各 NavLink hover 时触发对应级别的下拉面板，浮于页面内容上方。

**一级导航（无子分类，如 New Arrivals）**：
- 点击高亮（文字加粗 + 品牌紫下划线）
- 无下拉面板，直接跳转对应页面

**二级导航（有子分类，如 Handbags）**：
- hover 触发浮动白卡，从 Navbar 底部向下展开
- 内容：2 列平铺子分类链接，无分组标题
- 宽度约 460px，8px 圆角，阴影
- 示例链接：Shop All Bags / Bucket Bag / Tote Bag / Crossbody Bag / Shoulder Bag / Clutch / Top Handle Bag / Belt Bag / Backpack / Luggage

**三级导航（有品牌分组，如 Brands）—— MVP 采用版本 A**：
- hover 触发全宽白色面板（full-width），紧贴 Navbar 底部向下展开，覆盖页面内容
- 按二级目录分组，每组：组标题（粗体）+ 水平分割线 + 三级品牌名多列平铺（每组 4 列）
- 组间有间距分割，品牌数量多的组自动增加行高
- 待定：二级目录标题是否支持点击跳转，需产品确认

> 📌 原型中保留了版本 B 方案（左侧二级分类竖向 Tab，hover 切换，右侧显示对应品牌列表）作为备选，MVP 阶段采用版本 A。

---

## §4 搜索功能

### §4.1 搜索栏状态机

**状态转换图**：

```
                    ┌──────────────────────────────────────────────┐
                    │                                              │
              ┌─────▼──────┐   点击 Search Pill   ┌──────────────┐│
              │   Idle     │──────────────────────►│  Expanded   ││
              │  占位词轮播  │                       │  展开搜索卡  ││
              └────────────┘◄──────────────────────└──────┬───────┘│
                    ▲        点击遮罩 / Cancel              │       │
                    │                             键入字符 │       │
                    │                                      ▼       │
                    │                             ┌──────────────┐ │
                    │       点击遮罩 / Cancel      │   Typing    │ │
                    │◄────────────────────────────│  搜索卡隐藏  │ │
                    │                             └──────┬───────┘ │
                    │                                    │         │
                    │               点击搜索词/标签/Enter/🔍        │
                    └────────────────────────────────────┘         │
                              搜索结果页（新页面）                    │
                                                                    │
                    点击遮罩 / Cancel ───────────────────────────────┘
```

| 状态 | 触发条件 | 表现 |
|------|----------|------|
| 默认态（Idle） | 初始 / 搜索收起后 | Search Pill 显示占位词轮播，无展开卡片 |
| 展开态（Expanded） | 点击 Search Pill（未输入内容） | Search Pill 变为可输入文本框，下方展开搜索卡片（含热门词） |
| 输入态（Typing） | 在搜索框中键入字符 | 搜索卡片内容隐藏（无联想词），光标闪烁 |
| 提交 | 点击搜索按钮 / 按 Enter / 点击搜索词 | 导航至搜索结果页 |
| 关闭 | 点击卡片外部遮罩区域 / 点击"取消"按钮 | 回到 Idle 态，搜索框内容清空 |

### §4.2 搜索展开卡片（Expanded 态）

展开卡片从 Search Pill 正下方向下滑出，紧贴搜索框底部，宽度覆盖整个屏幕宽度（移动端为全宽下拉卡片，浮于内容上方；PC 端为下拉卡片，宽度与搜索框对齐）。

**交互线框图（Expanded 态）**：

```
[ 🔍  _________________________________ ] [Cancel]  ← 搜索框激活，可输入
┌────────────────────────────────────────┐
│  Recent Searches          清除全部 >   │  ← 条件渲染：本地有历史时才展示
│  ↻ iPhone 12 Pro                  [✕] │  ← 点击词 → 提交搜索；✕ → 删除该条
│  ↻ Chanel classic flap            [✕] │
│  ↻ Gucci belt                     [✕] │  最多5条，时间倒序
├────────────────────────────────────────┤
│  Hot Trends                            │  ← 始终展示
│  [Luxury Bags] [Watches] [Jewelry]     │  ← 品类标签 Row1（5个）
│  [Smartphones] [Cameras]               │
│  [Gucci] [Prada] [Fendi] [Leica]       │  ← 品牌标签 Row2（5个）
│  [Sony]                                │
└────────────────────────────────────────┘

无历史记录时（不渲染 Recent Searches 区块）：
[ 🔍  _________________________________ ] [Cancel]
┌────────────────────────────────────────┐
│  Hot Trends                            │
│  [Luxury Bags] [Watches] [Jewelry]     │
│  [Smartphones] [Cameras]               │
│  [Gucci] [Prada] [Fendi] [Leica] [Sony]│
└────────────────────────────────────────┘
```

**输入态（Typing）时搜索卡内容变化**：

```
[ 🔍  Chan_  ] [Cancel]
                           ← 搜索卡内容完全隐藏（无联想词）
                           ← MVP 不做 autocomplete
                           ← 用户继续输入，直到手动提交
```

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
- 标签样式：浅色填充胶囊，14px，可点击；品类与品牌标签可用不同填充色区分
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

**交互线框图（移动端 Banner 轮播）**：

```
┌────────────────────────────────┐  h: 320px，full-width
│                                │
│   （Banner 图片 / 视频内容）     │
│                                │
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│  ← 底部渐变黑色遮罩（从底向上）
│  Title Text                    │  ← 文字颜色读取 text_color
│  Subtitle Text                 │
│  [ Explore Finds →  ]          │  ← CTA 按钮
└────────────────────────────────┘
              ●  ○  ○  ○           ← 分页圆点指示器，居中，当前 Banner 实心
              
点击 Banner 任意区域（含 CTA）→ 跳转 landing_page
自动轮播：默认间隔4s（可配置），点击 Banner 后暂停
多 Banner 时：左右滑动切换，圆点跟随更新
```

- **尺寸**：full-width，高度 320px
- **多条 Banner**：分页展示（Carousel / Swiper），底部居中分页圆点指示器
- **自动轮播**：默认间隔 4 秒（可配置），点击暂停
- **覆盖层**：图片下方从底部向上渐变黑色遮罩（用于文字可读性）
- **文字排布**（从下到上）：`cta_text` 按钮 → `subtitle` → `title`；文字左对齐，文字颜色读取 `text_color`
- **点击**：点击 Banner 任意区域（含 CTA 按钮）→ 跳转 `landing_page`

### §5.3 PC 端 Banner 展示规则

- **尺寸**：full-width，高度 400px（原型稿定值）
- CTA 按钮 padding 比移动端更宽
- 其余规则同移动端（轮播、自动播放、点击跳转 `landing_page`）

### §5.4 降级策略

| 场景 | 处理 |
|------|------|
| 当前 market 无 active Banner 配置 | 隐藏 Banner 区域，页面从 Trust Bar 开始 |
| 图片加载失败 | 显示品牌色填充背景（`#6432FC`），文字和 CTA 按钮正常显示 |
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

每个条目配有一张缩略图（约 60×60px），图片资源由设计同步提供，前端静态引入。

### §6.2 展示规则

- **移动端**：2 列 × 2 行网格，每格显示图标 + 标题 + 副文案
- **PC 端**：4 列 × 1 行网格，布局更宽松
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
 │  180px   │  │  180px   │  │  180px   │  │          │
 │          │  │          │  │          │  │          │
 │  Title   │  │  Title   │  │  Title   │  │  Title   │
 └──────────┘  └──────────┘  └──────────┘  └──────────┘
  180×220px，圆角12px，点击→ landing_page，最多8张
```

**Section 标题**：`Curated Collections`（前端固定文案）

- 布局：横向单行滚动（horizontal scroll），左右滑动浏览更多
- 每张卡片：宽度 180px，高度约 220px，图片 + 标题
- 卡片圆角：12px
- 最多展示 8 张（由 CMS 活跃配置数决定）
- 点击卡片：跳转 `landing_page`

### §7.3 PC 端 Collections 展示规则

**Section 标题**：`Curated Collections` 或 `Explore Our Collection`（跟随设计稿确定）

- 布局：多列网格（3-4 列），不横向滚动
- 卡片尺寸比移动端大，图片 aspect-ratio 16:9 或 4:3
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

**交互线框图（Feed Tab 切换）**：

```
Explore Finds
┌────────────────────────────────────────┐
│  [■ For You ■]  [New Arrivals]         │  ← 胶囊式 Tab（MVP 仅 2 个）
│   激活：深色背景   未激活：透明+边框    │
└────────────────────────────────────────┘
点击 Tab → 切换商品列表内容（Tab 内容独立加载）
默认 Tab：有行为数据 → For You；无行为数据 → New Arrivals

Tab 内容区域切换示意：
For You  ───────► 个性化推荐 (A1/A2/B/C 混排)
New Arrivals ────► 最近X天新上架（可配置，B通路）
```

**Tab 样式**：胶囊式（pill style）
- 激活 Tab：深色背景填充（`$color-ink-primary`），白色文字
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

**交互线框图（商品卡片 + 双列网格布局）**：

```
移动端（2列网格，列间距8px，行间距12px）：

 ┌──────────┐  ┌──────────┐
 │          │  │          │
 │  商品图   │  │  商品图   │  ← 1:1 正方形，object-fit: cover
 │          │  │     ♡    │  ← 心形收藏按钮（右上角）
 │          │  │          │    outline（未收藏）/ filled（已收藏）
 ├──────────┤  ├──────────┤
 │ Brand    │  │ Brand    │  ← 12px，灰色
 │ Title..  │  │ Title..  │  ← 14px，深色，最多2行省略
 │ [Good]   │  │ [NWT]    │  ← 成色彩色标签（绿/蓝绿/蓝/橙）
 │ $299.00  │  │ $189.00  │  ← listing_price，16px 加粗
 └──────────┘  └──────────┘

已售出商品：
 ┌──────────┐
 │░░SOLD░░░ │  ← 灰色遮罩 + SOLD 标签，不可点击
 │░░░░░░░░░ │
 └──────────┘

PC端（4列网格，列间距12px，行间距16px）：同结构，宽度更大
```

**布局**：
- 移动端：2 列等宽网格，列间距 8px，行间距 12px
- PC 端：4 列等宽网格，列间距 12px，行间距 16px

**卡片结构（从上到下）**：

```
┌─────────────────┐
│   商品主图       │  ← 1:1 正方形，object-fit: cover；右上角心形收藏按钮
│                 │
│                 │
├─────────────────┤
│ 品牌名           │  ← 12px，灰色
│ 商品标题         │  ← 14px，深色，最多 2 行省略
│ 成色             │  ← grade 枚举：NWT / Excellent / Good / Fair；12px 彩色标签
│ $XXX.XX         │  ← listing_price，16px，加粗
└─────────────────┘
```

**价格展示规则**：
- MVP 仅展示 `listing_price`（当前上架价）
- ❌ 不展示划线价（原价）/ 促销价（营销系统未就绪）
- 后续迭代：营销系统上线后，有促销的商品展示 `~~原价~~` + 促销价 + 折扣标签

**成色标签颜色**（参考规范）：

| grade | 标签文字 | 颜色建议 |
|-------|---------|----------|
| NWT | New With Tags | 绿色 |
| Excellent | Excellent | 蓝绿色 |
| Good | Good | 蓝色 |
| Fair | Fair | 橙色 |

**Sold Out 商品**：
- 图片加灰色遮罩 + "SOLD" 标签
- 仍展示在列表中（不过滤），但不可点击进入商详
- Feed PRD 控制是否向前端下发已售出商品

### §8.3 收藏交互

**交互线框图（心形收藏按钮状态）**：

```
未收藏：  ♡（outline）  ──点击──►  ♡（filled，即时切换）  ──API失败──►  ♡（回滚到 outline）
已收藏：  ♡（filled）   ──点击──►  ♡（outline，即时切换）  ──API失败──►  ♡（回滚到 filled）

未登录用户点击 ♡ ：
          ♡（outline）  ──点击──►  [ 登录引导弹窗（可关闭，继续浏览）]
```

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

**移动端**保持原有无限滚动逻辑（见原 §8.4）：
- 首屏约 20 个商品，滚动至距底部约 200px 触发加载下一页
- 加载失败：底部显示 Retry 按钮

**Section 标题**：`Explore Finds`（前端固定文案），紧贴 Tab 行上方。

---

## §9 底部导航 Tab Bar（移动端）

**交互线框图**：

```
┌────────────────────────────────────────────┐  h: 60px（含底部安全区域）
│   🏠        🛍️        ♡         👤          │
│  Home      Shop    Favorites   Account     │
│ (激活：      (未激活:   (未激活：   (未激活：  │
│  filled    outline   outline    outline    │
│  品牌色)    灰色)      灰色)       灰色)     │
└────────────────────────────────────────────┘
  fixed 吸底，毛玻璃效果（backdrop-filter: blur）
  内容页可滚动穿透 Tab Bar 下方
```

**高度**：60px（含安全区域底部 inset 自适应）
**背景**：毛玻璃效果（backdrop-filter: blur），半透明白色
**位置**：fixed 吸底，内容页面可滚动穿透 Tab Bar 下方

**Tab 列表**：

| Tab | 图标 | 激活状态 |
|-----|------|---------|
| Home | house 形 | filled icon，标签文字加粗 |
| Shop | grid / search 形 | filled icon，标签文字加粗 |
| Favorites | heart 形 | filled icon，标签文字加粗 |
| Account | person 形 | filled icon，标签文字加粗 |

- 图标 24×24px，标签文字 10px
- 激活 Tab：filled 图标 + 加粗文字 + 品牌色（`$color-brand-primary`）
- 非激活：outline 图标 + 灰色

**首页对应**：Tab Bar 中 Home 为激活态

---

## §10 页脚 Footer（PC 端）

PC 端首页最底部展示通用 Footer。移动端首页无 Footer（由 Tab Bar 替代导航）。

**交互线框图（PC 端页面整体纵向结构）**：

```
┌───────────────────────────────────────────────────────────┐
│  [ Announcement Bar 40px - 品牌紫 ]                        │  sticky-scrollable
├───────────────────────────────────────────────────────────┤
│  [ Navbar 72px - 白底 sticky ]                             │  sticky
│   LOOPLY  NavLinks  [  Search  ]  ♡  🛒  🌐  👤           │
├───────────────────────────────────────────────────────────┤
│  [ Banner 400px - full-width ]                             │
├───────────────────────────────────────────────────────────┤
│  [ Trust Bar - 4列横排 ]                                   │
├───────────────────────────────────────────────────────────┤
│  Curated Collections                                       │
│  [ 卡片1 ][ 卡片2 ][ 卡片3 ][ 卡片4 ]  (3-4列网格)          │
├───────────────────────────────────────────────────────────┤
│  Explore Finds                                             │
│  [■ For You ■] [New Arrivals]                              │
│  ┌──────┐┌──────┐┌──────┐┌──────┐  (4列网格)               │
│  │      ││      ││      ││      │                          │
│  └──────┘└──────┘└──────┘└──────┘                         │
│  ... (默认16个，点击 View More 追加加载)                     │
│  [ View More ]                                             │
├───────────────────────────────────────────────────────────┤
│  [ Footer - 深色背景 ]                                      │
│  About | Support | Social                 © 2026 Looply   │
└───────────────────────────────────────────────────────────┘
```

**Footer 内容（MVP 版）**：

> ℹ️ MVP 阶段 Footer 内容与 Shopify 默认保持一致，内容不变。参考【Footer截图（shopify）】。Footer 内所有交互、跳转、二级页面暂不设计。如有余力可重新排版，优先级靠后，不强制。

- Footer 背景色：深色（`#1a1a2e` 或设计稿定义值）
- 文字颜色：白色
- 底部版权：`© 2026 Looply. All rights reserved.`

---

## §11 登录态差异矩阵

| 功能 | 未登录 | 已登录 |
|------|--------|--------|
| 浏览 Feed / Banner / Collections | ✅ 正常展示 | ✅ 正常展示 |
| Feed For You 推荐 | 基于 anonymous_user_id 的行为数据（若无历史→ New Arrivals 兜底） | 基于 user_id 的行为数据 |
| 商品卡片收藏（Heart） | 点击 → 登录引导弹窗 | 即时收藏，同步账户 |
| Header Cart 徽标 | 本地临时购物车（无账号同步） | 账户购物车（多端同步） |
| Header Favourite 图标 | 跳转 Favorites 页（可查看本地收藏） | 跳转 Favorites 页（账户数据） |
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
- Search 展开卡（Recent Searches + Hot Trends 硬编码）；PC 端搜索框当前为占位，交互待后续补全
- home_banner + home_collection CMS 资源位
- Trust Bar 硬编码（待运营文案）
- PC 端 Navbar：Handbags / Shoes / Jewelry / Watches / Accessories / Brands 6 个一级 NavLink，含二级/三级导航展开面板（三级 Brands 面板采用版本 A：多组横排，4列，组间分割线）
- Feed 两 Tab（For You / New Arrivals），Best Sellers 和 Deals 隐藏
- 商品卡片（无促销价）
- PC 端 Feed 分页加载：默认 16 个，View More 追加 4 行，无页码

### §15.2 后续迭代方向（建议）

| 功能 | 预期版本 | 条件 |
|------|---------|------|
| Best Sellers Tab 上线 | v1.1 | Feed PRD 热卖榜通路就绪 |
| Deals Tab 上线 | v1.1 | 营销系统上线 |
| 划线价 / 促销价展示 | v1.1 | 营销系统上线 |
| 搜索配置后台（Hot Trends 运营化） | v1.1 | 搜索配置页开发完成 |
| PC 端搜索框完整交互 | v1.1 | 搜推确认预置内容后实现 |
| PC Navbar Heart/Cart 侧栏展开 | v1.1 | Favorites 页 / 购物车页完成 |
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
| `market_language_save` | 点击面板 Apply | `new_language_code`, `new_market_id` |

### §16.2 Feed 行为数据

Feed 相关埋点的详细定义见《Looply 首页 Feed PRD v2.3》§10 行为数据 + §19 埋点事件。首页 PRD 不重复定义。

---

## §17 附录 — 设计稿索引

| 页面 / 区域 | 端 | 设计稿文件 | 关键 Frame / Node |
|-------------|----|-----------|--------------------|
| 首页移动端全页 | App | [首页 APP 端（Figma）](https://www.figma.com/design/hwPpMTL2rFF8fcWD8mHmLE/Untitled?node-id=280-2&t=n8yG97WUo5EQiBJF-1) | Node 280-2 |
| 首页 PC 端全页 | PC | `looply-home-PC.pen` | Frame `kSmej` |
| 移动端 Header + Search Pill | App | [首页 APP 端（Figma）](https://www.figma.com/design/hwPpMTL2rFF8fcWD8mHmLE/Untitled?node-id=280-2&t=n8yG97WUo5EQiBJF-1) | — |
| PC Navbar（含搜索 + navRight） | PC | `looply-home-PC.pen` | Node `PP8Uk` |
| PC Announcement Bar | PC | `looply-home-PC.pen` | Node `EhX1v` |
| Trust Bar | App / PC | `looply-home-PC.pen` | Trust Bar 区域 |
| Collections（横向卡片） | App / PC | `looply-home-PC.pen` | Collections 区域 |
| Feed 区域（Tab + 商品网格） | App / PC | `looply-home-PC.pen` | Feed 区域 |
| 底部 Tab Bar | App | `looply-home-PC.pen` | Node `o4oh3V` |

设计稿路径：
- 移动端：[首页 APP 端（Figma）](https://www.figma.com/design/hwPpMTL2rFF8fcWD8mHmLE/Untitled?node-id=280-2&t=n8yG97WUo5EQiBJF-1)
- PC 端：`/Users/zz/looply/cms/looply-home-PC.pen`

---

*文档维护：Looply 产品团队 | 首页 PRD v1.3 | 2026-07-02*

---

## 变更日志

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

### v1.2 · 2026-06-18

| 编号 | 章节 | 变更内容 | 原因 |
|------|------|---------|------|
| C1 | §4.2 搜索展开卡片（Expanded 态） | 移动端展开卡片交互由 bottom sheet 改为全宽下拉卡片：紧贴搜索框底部向下滑出，宽度覆盖整个屏幕宽度，不从底部弹出 | 底部弹出与搜索入口位置脱节，用户视线从顶部搜索框跳到底部 sheet，体验断层；改为贴顶下拉后视觉连贯 |
