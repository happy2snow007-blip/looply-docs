# Looply 核心页面 SEO/GEO — 技术代码实现说明

| 项 | 内容 |
|---|---|
| 文档版本 | v2.1 |
| 创建日期 | 2026-06-08 |
| 最近更新 | **v2.1（2026-07-21）**：首页商家主体 schema 由宽泛的 `Organization` 改为 Google 推荐的电商子类型 `OnlineStore`；新增全站稳定实体 ID `https://looply.com/#store`，并由 `WebSite.publisher`、`Article.publisher`、`Person.worksFor`、`Product.offers.seller` 统一引用；移除已停止展示的 Sitelinks 搜索框及 `SearchAction`；新增 4 个 schema 自动化验收用例。 |
| 历史更新 | v2.0（2026-07-14）：新增统一 SEO 状态计算层；重构 robots/noindex/canonical 职责矩阵；PLP See more 强制使用可抓取分页 URL；Collection 自动索引门槛定为 3 件并支持受控人工覆盖；已售 PDP 采用 90 天观察期与价值信号分层，补齐撤回/合并/合规删除/不存在状态；sitemap 改为仅读取最终 SEO 状态，已售 index 页继续进入 sitemap；新增 AI Coding 自动化验收矩阵。<br>v1.9（2026-07-09）：§7 sitemap **移除 `priority` 设置**——`priority`/`changefreq` 已被 Google 与 Bing 明确忽略（Bing 2025-07 官方确认），Looply 相关引擎无一采纳，生成 sitemap 不再输出；§7.2 表格列头由"priority/lastmod"改为仅 `lastmod`（唯一有效字段，须诚实、只在内容真实变更时更新）、新增说明块；§7.6 示例片段删除全部 `<priority>` 标签；§7.3、§13 售出商品"降 priority 吃权重"改为"canonical 自指 + 内容降级"，并修正 §13 与 §7.3"售出即移出 sitemap"的口径矛盾。<br>v1.8（2026-07-09）：§9.2 改为**展示层/唤起层两分**，展示层**全站三端统一自建 banner、废弃 iOS 原生 `apple-itunes-app` meta**（避免 iOS Safari 原生+自建双条，且文案/样式/静默期/埋点全可控、可承载营销文案）；唤起层 Universal/App Links 照常保留；删原 D「iOS 非 Safari 盲区」（统一自建后无盲区）；新增 D「关闭与静默期」——关闭/唤起成功写 `localStorage` 时间戳静默 7 天、不做永久关闭、静默期按端隔离；节名改「App 引导 Banner + Deep Link 配置」。<br>v1.7（2026-07-09）：§9.2 App 引导 banner 三点补充——① 展示页面从"仅首页"扩到首页/PLP/PDP/内容页（`/shop`/`/favorites`/搜索/账户不出，范围对齐 §3.2 OG）；② A 点补「iOS 原生 banner 内容不可自定义」——App 名/图标/副标题/评分由 Safari 自动拉，开发者仅控 `app-id`/`app-argument`/`affiliate-data` 三参数；③ 新增 D 点「iOS 非 Safari 盲区」——原生 banner 仅 iOS Safari 生效，iOS Chrome/Firefox 不支持（Safari 应用层功能非 WebKit 引擎层），一期用前端自建 banner 兜底（与 Android 复用同一套，触发条件改为 Android+iOS 非 Safari）；原 D/E 顺延为 E/F。<br>v1.6（2026-07-08）：品牌页彻底对齐"普通 collection"——删 §3「品牌页字段降级读品牌管理 brand_*」行（与"无品牌管理模块"矛盾的旧残留）、删 §5 Brand schema 行 + JSON 示例、§13 品牌页去掉 Brand 专属 schema 增强（schema 同普通 collection：BreadcrumbList + ItemList）。<br>v1.5（2026-07-08）：新增 §3.2「OG / 社交卡片配置」——分页面 OG 输出清单（首页/PLP/PDP/内容页出，`/shop`/`/favorites`/搜索/账户不出）、字段取值（与 Meta 同源、og:url=canonical、og:locale 随 en/es）、og:image 分页面取图与 1200×630 处理、兜底链（全站默认 OG 图=品牌板非裸 logo）、Twitter 用 summary_large_image。<br>v1.4（2026-07-03）：① slug 唯一池去掉保留词黑名单（对齐类目 PRD v0.18，MVP 不设）；② §6 AI 爬虫放行清单补全为训练型+检索型两类（补 OAI-SearchBot/ChatGPT-User/Claude-User/Applebot/anthropic-ai/CCBot）；③ §5 补齐 BreadcrumbList/ItemList/FAQPage/Article/HowTo/Person/Brand/ImageObject 完整 JSON 示例。<br>v1.3（2026-07-03）：① 新增 §3.1 图片 alt 自动生成逻辑（复用商品显示名降级链）；② §4 PDP 面包屑中间级取值改为 collection 侧 `breadcrumb_role` 标记（品牌优先类目兜底），清除"来自 Navigation 模块"旧表述；③ 新增 §9.2 Smart App Banner + Deep Link 配置；④ §2 PDP slug 改为 slugify(商品显示名)-{id}，与 SEO Title 同源；⑤ 待决策项落定：S1=CSR、S2=302 跳转、C1=/guides/、D2/D3 去"决策/待定"措辞；⑥ 附表新增 alt/slug/显示名/活动 banner 跨模块依赖。<br>v1.2（2026-07-03）：§7 Sitemap 扩写、§13 D2 改 "See more + sitemap 兜底"、新增 §11 国际化，第二部分顺延 §12–16 |

---

## 〇、阅读说明

分两层：**第一部分 整体架构**（全站统一实现的技术机制）、**第二部分 分页面说明**（各页面独有的技术实现点）。代码层字段（canonical/robots/schema/og/sitemap/降级逻辑）几乎都在本文。

---

# 第一部分 · 整体架构（技术统一实现）

## 1. 渲染策略

| 页面 | 渲染方式 | 说明 |
|---|---|---|
| 首页 | SSG/ISR | 核心文案静态化；精选商品模块 ISR/动态 |
| PLP | SSR | schema 直出首屏 |
| PDP | SSR | schema 直出首屏 |
| 搜索页 | **CSR（已定 S1）** | 结果页 noindex 无需被爬，行业主流做法（Amazon/eBay 等搜索结果页均不 SSR）；省服务器成本 |
| 内容页 | SSR/SSG | 核心内容静态可读 |

- 核心页 SSR/SSG，保证 AI 爬虫与移动优先索引拿到完整首屏 HTML。
- 注意水合(hydration)坑：控制水合开销、避免过度水合（影响 INP）。

## 2. URL 与路由实现

**URL 模式**：

| 页面 | URL 模式 | 示例 |
|---|---|---|
| 首页 | `/` | `looply.com/` |
| 品类页 PLP | `/collections/{slug}` | `/collections/shoulder-bags` |
| 品牌页 PLP | `/collections/{brand-slug}` | `/collections/chanel` |
| 商品 PDP | `/products/{slug}-{id}/` | `/products/chanel-classic-flap-caviar-black-a1b2c3/` |
| 内容/指南页 | `/guides/{slug}/` | `/guides/how-to-authenticate-chanel-bags/` |
| 内容中心 Hub | `/guides/` | — |
| 分面筛选 | `/collections/{slug}?参数` | `/collections/chanel?color=black&price_max=3000` |
| 排序 | `/collections/{slug}?sort=` | `/collections/chanel?sort=newest` |
| 站内搜索 | `/search?q=` | `/search?q=chanel` |
| 购物车/结算/账户 | `/cart` `/checkout` `/account` | — |

**PDP URL 路由实现（关键，跨商品系统待对齐项）**：

```
规范 URL：  /products/{slug}-{id}/
  slug = slugify(商品显示名)（小写、空格转连字符、去特殊字符、过长可截断）
         商品显示名 = listing.listing_title → product.title（上架必非空）
  id   = 短唯一码（listing_id 或其 base62 短码）
解析规则：  路由仅用末尾 {id} 定位商品；slug 部分仅作展示
重定向：    访问 slug 与当前规范 slug 不符 → 301 到规范 URL
canonical： 自指规范 URL；带参数/旧 slug 的变体一律 canonical 到它
```

> slug 生成口径：slug 与 SEO Title 都基于商品标题自动生成，但走各自的格式化——SEO Title 面向阅读、slug 面向 URL（slugify）。不单独定义 `{brand}-{model}-{material}-{color}` 字段公式（商品显示名里已含这些，另拼会与标题口径分裂），而是对商品显示名做 slugify。slug 自动生成 + 可手改的最终规则由商品模块落地（生成来源对齐其 SEO Title，见附表）。

> 行业实证（The RealReal）确定用"描述性 slug + 末尾短唯一码"，兼顾关键词价值与链接稳定。**自建站需自行实现 canonical + 按 id 解析 + slug 不符 301**，否则商品改 slug 或跨多 collection 时重复收录。

> 方案对比（为何不用纯 id / 纯 slug）：纯 `{listing_id}`（纯数字）URL 无关键词、放弃二手超长尾价值、对 GEO 不利；纯 `{url_slug}`（纯文字）二手同款多导致 slug 唯一难保证、运营改 slug 即断链。`{slug}-{id}` 兼得关键词与唯一稳定。行业实证 The RealReal 真实 URL：`/products/.../the-row-suede-east-west-top-handle-pbq81`（描述性 slug + 短码 `pbq81`，内部 ID 放 utm 不进主路径）。

**Collection URL 路由实现（PLP 专属，与 PDP 不同）**：

Collection（品类页/品牌页）**不加末尾唯一码**，URL 就是纯 `/collections/{slug}`。原因：品类/品牌天然全站唯一（一个 `shoulder-bags`、一个 `chanel`），slug 唯一性池已保证不撞车，无需 `-{id}` 兜底；且 slug 极少变动。

但"改 slug 即断链"这半问题 PLP 同样存在，且 PLP 是长青资产、权重高于单个 PDP，断链损失更大。collection **有唯一主键 `id`**，只是**行业惯例不把 id 放进 collection URL**（纯 `/collections/{slug}`）——因此 PLP 的 URL 里不带 id，无法像 PDP 那样从请求直接解析出 id 定位，**只能靠历史 slug 映射表做 301**：

```
规范 URL：  /collections/{当前slug}
解析规则：  按当前 slug 命中当前 collection；未命中则查「历史 slug 映射表」
重定向：    访问命中历史 slug → 301 到 /collections/{当前slug}
canonical： 自指当前规范 URL
slug 变更： 运营改 slug 时，系统自动写一条 旧slug→collection_id 的 301 重定向记录；
            旧 slug 进入重定向表并指向新地址。若日后新建 collection 想复用该旧 slug，
            不永久禁用，而是冲突提示让运营确认（可覆盖/停用旧重定向后复用，同 Shopify URL Redirect）
```

**URL 通用规则（代码强制）**：

- 全小写、连字符分词、无下划线/大写/`.html` 后缀；
- 强制 HTTPS；统一带末尾斜杠（不一致的 301）；
- 统一 www 或非 www（另一个 301）；
- 多语言 URL：英语裸 URL、es 走 `/es/` 子目录前缀，配完整 hreflang（详见 §11 国际化）。

**slug 唯一性校验（后端，按命名空间划分）**：`/collections/` 下的品类页与品牌页共用一个 slug 唯一池，写入时校验冲突；PDP 靠末尾 id 保唯一、slug 不入池；内容页 `/guides/` 为独立命名空间，与 collections 互不冲突。**MVP 阶段不设保留词黑名单**（对齐类目管理 PRD v0.18）；后续若需可再补 all/new/search/shop 等系统路由保留词。

## 3. 字段自动生成与降级逻辑（meta title / meta description / alt / OG）

产品后台只填部分字段，其余由代码自动生成：

| 字段 | 自动生成/降级逻辑 |
|---|---|
| Meta Title / `<title>`（留空时） | 按降级链兜底（PLP：`Pre-Owned {Brand} {Category} \| Authenticated \| Looply`）。**指搜索结果里的标题标签，非页面可见 H1** |
| Meta Description（留空时） | 按降级链兜底 |
| OG/Twitter 卡 | 降级自 title/description/主图，取不到图回退全站默认 OG 图（完整配置见 §3.2） |
| 图片 alt（未人工填时） | 按结构化字段模板自动拼装（见 §3.1） |

### 3.1 图片 alt 自动生成逻辑

一期策略：**L1 模板拼装 + L2 人工覆盖**，不上 AI 视觉。alt 为空时用自动值，人工填了用人工值。

```
商品显示名 DN = listing.listing_title（最终上架标题，PDP 前台展示）
                空 → product.title（商品模块保证上架商品 product.title 必非空，故两级即兜底到底）
商品主图： {成色前缀} {DN}
           成色前缀 = grade 映射为 "Pre-owned"；若 DN 已含 pre-owned/used 则不加
商品细节图：{DN} — {部位}
           部位取 product_image 的"部位枚举"；无枚举时降级为 "detail {sort_order}"
collection图：Shop {collection_name} at Looply
活动 banner：无字段可拼 → 不自动生成，强制人工填（后台该图 alt 必填校验）
```

> **不逐字段拼品牌/款式/颜色/材质**：`spu_name` 大概率已含品牌+颜色+材质，逐字段拼会重复。改为复用商品模块已治理的显示名 DN（= title 口径），alt 只在其上加成色前缀/部位。避免在 alt 侧重造一遍字段去重、并与站内标题口径统一。

**护栏（代码强制）**：
- 长度 ≤ 125 字符，超长优先保留 DN、截断部位/成色；
- DN 两级均空时才跳过该段，不输出 "undefined"、不留空占位（product.title 上架必非空，实际极少触发，仅作代码防御）；
- 同一 product 下多图 alt 去重（部位/sort_order 保证不同）；
- 成色前缀与 DN 去重（DN 含 pre-owned/used 则不加前缀）；不写 "image of"；
- 细节图部位依赖商品模块新增 `product_image` 部位枚举字段（跨模块，见附表）；无该字段时走 `detail {n}` 降级。

### 3.2 OG / 社交卡片配置（Open Graph + Twitter Card）

分享到 Facebook/iMessage/WhatsApp/X/Slack 时的预览卡片。属**代码层自动产出**（产品不单独设计录入界面），字段大部分复用 SEO title/description/图片，本节定义**哪些页要、每页取值、兜底链**。

**A. 哪些页面输出 OG**

| 页面 | 输出 OG | og:type | 说明 |
|---|---|---|---|
| 首页 | ✅ | `website` | 品牌分享入口 |
| PLP（品类/品牌/升格组合） | ✅ | `website` | 品牌页同为普通 collection |
| PDP | ✅ | `product` | 分享价值最高，og:image 用商品主图 |
| 内容/指南页 + `/guides/` Hub | ✅ | `article` | 补 `article:published_time`/`modified_time`/`author` |
| `/shop`、`/favorites` | ❌ | — | 移动端 tab、noindex，不作分享入口，无需 OG |
| 搜索页 / 参数筛选/排序页 | ❌ | — | noindex，不分享 |
| 购物车/结算/`/account` | ❌ | — | noindex 交易/账户页 |

> 原则：**可索引页 + 有分享价值的页才输出 OG**。

**B. 分页面字段取值（每页 `<head>` SSR 直出）**

| 字段 | 取值规则 |
|---|---|
| `og:title` | = SEO Title（留空走 §3 title 降级链）；PDP=商品显示名、PLP=`Pre-Owned {Brand} {Category}...`、内容页=文章 H1 |
| `og:description` | = Meta Description（留空走 §3 description 降级链） |
| `og:image` | 见 C（分页面取图 + 兜底） |
| `og:url` | = 该页 **canonical URL**（与 §6 canonical 同源，绝不带 query 参数） |
| `og:type` | 见 A 表 |
| `og:site_name` | 固定 `Looply` |
| `og:locale` | 随 §11 语言：en 页 `en_US`、es 页 `es_ES`；并用 `og:locale:alternate` 列另一语言（与 hreflang 对齐） |
| Twitter Card | 统一 `twitter:card = summary_large_image`（大图卡）；`twitter:title`/`description`/`image` 复用同源 OG 值；`twitter:site = @looply` |

**C. og:image 分页面取图**

| 页面 | og:image 取值 | 尺寸处理 |
|---|---|---|
| PDP | 商品**主图**（同 PDP 首图 / ImageObject.contentUrl） | 生成/裁切为 1200×630 横版；商品图多为竖版，需居中裁切或加品牌底衬，不直接拉伸变形 |
| PLP / 品牌页 | 该 collection 的**封面图**（运营在 collection 后台配的入口图）；无则兜底图 | 同上 |
| 内容/指南页 | 文章**首图/封面图** | 同上 |
| 首页 | 指定的**品牌主视觉图**（非兜底图） | 预制 1200×630 |

**D. 兜底链（代码强制，防空白卡片）**

```
og:image 取值顺序：
  1. 页面指定图（PDP 主图 / collection 封面 / 文章封面 / 首页主视觉）
  2. 取不到或图 URL 不可达(非 200) → 回退【全站默认 OG 图】
og:title 空 → SEO Title → H1
og:description 空 → Meta Description → 全站默认品牌简介一句话
```

- **全站默认 OG 图（必须存在）**：一张**预制的 1200×630 品牌图** = Looply logo **居中于品牌色纯背景**（可含一句 slogan），**不是直接甩 logo.png**（透明底/近方形 logo 塞进横版框会大片留白或被拉伸模糊，业界共识）。此图放固定 CDN 地址、返回 200，作为任何页取不到图时的最后兜底——og:image 返回 404 会全站悄悄拉低社交点击率，故兜底图不可缺。

**E. 护栏（代码强制）**

- 尺寸统一 **1200×630（1.91:1）**，JPG/PNG，建议 <1MB；一张图覆盖 FB/LinkedIn/X/Slack，不做每平台变体；
- `og:url`、Twitter/OG 的目标图必须与 canonical 一致，**绝不用带参数 URL**（防分享变体与索引页不一致）；
- 竖版商品图**居中裁切或加底衬**到横版，禁止直接拉伸变形；
- OG 的 title/description 与页面 Meta **同源**（不另写一套，避免维护分叉）；
- 多语言 OG 随页面语言出对应 `og:locale`，与 §11 hreflang/canonical 保持一致。

## 4. 面包屑实现（BreadcrumbList）

- 全站统一 BreadcrumbList schema 模板，SSR 直出。
- **层级不来自 URL 路径**（扁平架构 URL 无层级）：PLP 为 `Home › {Collection}` 两级；PDP 中间级按下方规则取自 collection 侧 `breadcrumb_role` 标记。
- 显示文字保留层级感，但每级链接指向各自 `/collections/{slug}`，不拼层级路径。
- **schema 必须恒定**：同一 PDP 的 BreadcrumbList 不随用户来路变（广告直链/搜索/站内一致），否则产生多版本结构化数据，SEO 减分。

**PDP 面包屑中间级取值（已定，实现逻辑）**：

```
输入：当前商品的 brand_id、category_id
查询：collection 表中被标记为"规范面包屑页"(breadcrumb_role)且 seo_indexable=true 的记录
取值优先级：
  1. brand_id  → 命中"该品牌的规范页"      → 用它（品牌优先）
  2. category_id → 命中"该类目的规范页"     → 用它（类目兜底）
  3. 都未命中 → 无中间级
输出：
  命中 → [Home, {规范页(name,url)}, {商品名(无url)}]   三级
  未命中 → [Home, {商品名(无url)}]                        两级
约束：
  - 恒定：取值只依据商品自身 brand_id/category_id，与来路无关
  - 只输出有真实 URL 的级；绝不输出无 url 的中间 ListItem（Schema 会被判无效/不采纳）
  - 中间级 url 必须是 collection 的规范 canonical URL（可索引），不得用 noindex 的 query 筛选页
```

> 此逻辑不依赖商品侧 `primary_collection` 字段（商品数据模型无此字段），锚点由 Collection 管理模块在 collection 侧维护 `breadcrumb_role` 标记。跨模块落地见文末「跨模块依赖与待对齐项」附表与 Collection 管理 PRD。

## 5. 结构化数据 schema 模板库（代码实现，SSR 直出）

| schema | 用于页面 | 字段要点 |
|---|---|---|
| OnlineStore（Organization 子类型） | 首页 | `@id`/name/url/logo/description/sameAs/contactPoint |
| WebSite | 首页 | `@id`/name/url/publisher；用于网站实体识别，不再配置 Sitelinks 搜索框 |
| BreadcrumbList | PLP/PDP/内容页 | 同一模板，恒定（PDP 中间级取值见 §4） |
| ItemList | PLP | 商品列表 url/name/image/position |
| Product + Offer | PDP | 完整示例见 §14 |
| ImageObject | PDP | 实拍图 |
| FAQPage | 内容页 | 问答对（PLP 不做 FAQ） |
| Article / BlogPosting | 内容页 | 作者、发布/更新日期、标题 |
| HowTo | 内容页（步骤类） | 步骤化 |
| Person | 内容页作者 | E-E-A-T 作者实体 |

> OnlineStore / WebSite 完整示例见 §12 首页，Product+Offer 见 §14 PDP。以下补齐其余模板的完整 JSON 示例。

**BreadcrumbList（PLP/PDP/内容页，中间级取值见 §4）**：

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://looply.com/" },
    { "@type": "ListItem", "position": 2, "name": "Chanel", "item": "https://looply.com/collections/chanel" },
    { "@type": "ListItem", "position": 3, "name": "Chanel Classic Flap Medium Black Caviar" }
  ]
}
```
> 末项（当前页）不带 `item`；中间级取不到时只输出 Home + 当前页两项。

**ItemList（PLP 商品列表）**：

```json
{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1,
      "url": "https://looply.com/products/chanel-classic-flap-medium-black-caviar-a12345" },
    { "@type": "ListItem", "position": 2,
      "url": "https://looply.com/products/chanel-boy-bag-small-black-b67890" }
  ]
}
```

**FAQPage（内容页；PLP 不做 FAQ）**：

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "How can I tell if a Chanel bag is authentic?",
    "acceptedAnswer": { "@type": "Answer",
      "text": "Check the serial number, hologram sticker, stitching and hardware engraving..." }
  }]
}
```

**Article / BlogPosting（内容页，含作者 + 日期）**：

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "How to Authenticate a Chanel Classic Flap",
  "image": ["https://cdn.looply.com/guides/chanel-auth.jpg"],
  "datePublished": "2026-06-01T08:00:00-04:00",
  "dateModified": "2026-07-03T09:00:00-04:00",
  "author": { "@type": "Person", "name": "Jane Doe",
    "jobTitle": "Senior Authenticator", "description": "10+ yrs luxury authentication, ex-Sotheby's" },
  "publisher": { "@type": "OnlineStore", "@id": "https://looply.com/#store", "name": "Looply",
    "logo": { "@type": "ImageObject", "url": "https://looply.com/logo.png" } }
}
```

**HowTo（验真步骤类内容页）**：

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to Authenticate a Chanel Bag",
  "step": [
    { "@type": "HowToStep", "position": 1, "name": "Check the serial number",
      "text": "Locate the serial sticker inside the bag and verify the format..." },
    { "@type": "HowToStep", "position": 2, "name": "Inspect the hardware",
      "text": "Genuine hardware is engraved cleanly and weighs..." }
  ]
}
```

**Person（内容页作者，E-E-A-T 实体，可被 Article.author 引用或独立作者页用）**：

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Jane Doe",
  "jobTitle": "Senior Authenticator",
  "description": "10+ years luxury handbag authentication; former Sotheby's specialist",
  "worksFor": { "@type": "OnlineStore", "@id": "https://looply.com/#store", "name": "Looply" }
}
```

**ImageObject（PDP 实拍图，可内嵌进 Product.image 或独立输出）**：

```json
{
  "@context": "https://schema.org",
  "@type": "ImageObject",
  "contentUrl": "https://cdn.looply.com/products/a12345/main.jpg",
  "caption": "Pre-owned Chanel Classic Flap Medium in Black Caviar — front view"
}
```

## 6. robots / 索引控制（v2.0 统一规则）

### 6.1 robots.txt、页面 robots 与 canonical 的职责

| 机制 | 负责解决的问题 | 不用于 |
|---|---|---|
| robots.txt | 控制合规爬虫是否允许请求路径 | 不能可靠地把已知 URL 从索引中移除 |
| meta robots / `X-Robots-Tag` | 页面可访问，但明确不进入索引 | 不负责合并重复 URL |
| canonical | 在多个重复或近似 URL 中声明规范版本 | 不与 noindex 共同承担“删除页面”职责 |
| HTTP 状态码 | 表达正常、迁移、缺失或永久删除 | 不把删除页面统一返回 200 |

页面矩阵：

| 页面/URL 类型 | robots.txt | 页面 robots | canonical | 进 sitemap |
|---|---|---|---|---|
| 首页、最终可索引 PLP/PDP/内容页 | 允许抓取 | `index,follow` | 自指 | ✅ |
| PLP 合法分页页 | 允许抓取 | `index,follow` | 自指分页 URL | ❌ |
| 筛选/排序及其分页页 | 允许抓取 | `noindex,follow` | 不设置 | ❌ |
| 站内搜索页 | 允许抓取 | `noindex,follow`，初始 HTML 或响应头直出 | 不设置 | ❌ |
| `/shop`、`/favorites`、匿名账户落地页 | 允许抓取 | `noindex,follow` | 不设置 | ❌ |
| 购物车、结算、登录后个人数据页 | 以登录态和权限保护为主 | 可访问 HTML 仍输出 noindex | 不设置 | ❌ |
| UTM 等追踪参数变体 | 允许抓取 | `index,follow` | 指向无追踪参数的规范 URL | 仅规范 URL 进入 |

约束：

- `/search` 不在 robots.txt 中统一 Disallow；否则爬虫无法读取 noindex。
- 搜索页虽为 CSR，noindex 必须在服务器返回的初始 HTML 或 `X-Robots-Tag` 中存在，不能等待 JavaScript 注入。
- noindex URL 一律不进 sitemap；核心内链必须来自可索引页面，不能长期依赖 noindex 页传递。
- 已被索引且计划移除的 URL，先保持可抓取并输出 noindex；确认移除后再评估是否需要 robots 屏蔽。
- UTM/广告追踪参数与业务筛选参数分开：前者 canonical 清洗，后者 noindex。

### 6.2 Collection 索引质量门槛

Collection 统一使用下列字段：

| 字段 | 类型/枚举 | 说明 |
|---|---|---|
| `in_stock_count` | 非负整数 | 当前可购买商品数 |
| `seo_index_mode` | `AUTO` / `FORCE_INDEX` / `FORCE_NOINDEX` | 默认 AUTO |
| `min_indexable_stock` | 全局配置整数 | MVP 默认 3 |
| `seo_indexable` | 系统派生布尔值 | 页面最终是否 index，供页面、sitemap、面包屑共同读取 |
| `seo_index_reason` | 完整枚举 | 最终判断原因 |

`seo_index_reason` 枚举：

| 枚举值 | 触发条件 | 输出 |
|---|---|---|
| `AUTO_THRESHOLD_MET` | AUTO 且在售数 ≥3 | index |
| `AUTO_BELOW_THRESHOLD` | AUTO 且在售数 0–2 | noindex |
| `MANUAL_FORCE_INDEX` | FORCE_INDEX 且校验通过 | index |
| `MANUAL_FORCE_NOINDEX` | FORCE_NOINDEX | noindex |
| `UNPUBLISHED` | 草稿或未发布 | 公网路由 404 |

判断顺序：

```text
未发布 → seo_indexable=false，公网路由 404
FORCE_NOINDEX → seo_indexable=false
FORCE_INDEX → 仅当在售数≥1、H1非空、存在自定义描述时为 true；否则拒绝保存
AUTO → seo_indexable = (in_stock_count >= 3)
```

当 `seo_indexable` 变化时，必须同步刷新页面 robots、sitemap、缓存、hreflang 资格和 PDP 面包屑候选。`breadcrumb_role` 的候选条件统一读取 `seo_indexable=true`。

### 6.3 分面与高价值组合

筛选/排序 URL 使用 noindex,follow、不设置 canonical、不进 sitemap。若某个组合值得独立排名，运营将其升格为正式 collection；升格页具备独立 slug、内容和索引状态，不复用参数 URL。

**robots.txt — 放行 AI 爬虫（分两类，检索型对 GEO 更关键）**：

| 类型 | 作用 | user-agent |
|---|---|---|
| 检索型（**GEO 关键**） | AI 实时回答时抓取、决定能否被引用 | `OAI-SearchBot`、`ChatGPT-User`（OpenAI）；`Claude-User`（Anthropic）；`PerplexityBot`（Perplexity）；`Applebot`（Apple 智能） |
| 训练型 | 喂大模型训练语料 | `GPTBot`（OpenAI）；`ClaudeBot`、`anthropic-ai`（Anthropic）；`Google-Extended`（Google）；`CCBot`（Common Crawl） |

- 二者都放行：训练型帮模型"认识"Looply，检索型保证 ChatGPT/Perplexity 实时回答"哪买二手 Chanel"时能抓到并引用 Looply（缺检索型 = 实时问答里消失）。
- HTML 页面是否可抓取遵循 §6.1；不得用 robots.txt 代替 noindex。购物车、结算和个人数据以权限保护为主，站内搜索保持可抓取以读取 noindex。
- 爬虫清单需可维护（新 AI 爬虫层出不穷），不硬编码死。

## 7. Sitemap（代码动态生成）

### 7.1 定位与形态（先破除误解）

- **sitemap 不写进任何页面 HTML**，它是放在**网站根目录、各有独立 URL 的一批 `.xml` 文件**，读者是搜索引擎/AI 爬虫，不是浏览器渲染给人看的。
- 结构是**"总索引 + 分文件"两层**：`sitemap-index.xml` 只**列出各子 sitemap 的地址**（不含它们的内容），爬虫读索引 → 拿到子文件 URL → 再逐个请求。
- 全部 sitemap 由**后端动态生成**（现查数据库或读预生成缓存 → 拼 XML → 以 `Content-Type: application/xml` 返回），**不是前端静态资源、不可手写维护**。属后端/SEO 工程职责，与前端页面开发是两条线。
- Looply 可索引页均为扁平 slug，`<loc>` 正常不含参数；若 URL 含 `&` 必须转义为 `&amp;`。

### 7.2 文件结构（根目录）

```
https://looply.com/
├── sitemap-index.xml          ← 总索引，只列出下列文件的 URL
├── sitemap-static.xml         ← 核心静态页（首页/how-it-works/authentication…）
├── sitemap-collections.xml    ← 分类/集合/品牌页 PLP（品牌页即普通 collection）
├── sitemap-content.xml        ← 内容/指南页
├── sitemap-products-1.xml     ← 商品 PDP 分片 1（1–50,000）
├── sitemap-products-2.xml     ← 商品 PDP 分片 2（50,001–100,000）
└── ... sitemap-products-N.xml ← 按 5 万条/片切；100 万商品 = 20 片
```

| sitemap 文件 | 内容（穷举范围） | 更新节奏（内部口径） | `lastmod`（唯一有效字段） |
|---|---|---|---|
| `sitemap-static.xml` | 核心静态页 | 极少变动 | 仅内容真实变更时更新 |
| `sitemap-collections.xml` | `seo_indexable=true` 的分类/集合/**品牌** PLP（品牌页即普通 collection），每个集合只 1 条首页 URL | 低频 | 最终索引状态或集合内容真实变化时更新 |
| `sitemap-content.xml` | 内容/指南页 | 低频 | 文章发布/修订时更新 |
| `sitemap-products-N.xml` | **全部可索引 PDP，一品一条，穷举** | 高频 | **精确到时分**；上下架/售出即更新 |
| `sitemap-index.xml` | 索引以上全部子文件的 URL | 随分片数动态 | 子文件内容变化时更新 |

> **不设 `priority`，也不依赖 `changefreq`。** `<priority>` 与 `<changefreq>` 这两个可选标签**已被 Google 与 Bing 明确忽略**（Bing 2025-07 官方确认，Google 由 John Mueller 多次确认），不影响抓取与排名——历史上很多站把页面都标成高优先级，信号早已失效。Looply 面向美国市场，相关引擎（Google + Bing，含 Yahoo/DuckDuckGo 走 Bing 索引）**无一采纳 priority**，故**生成 sitemap 时不输出 `priority`**（输出也不违规、只是无效且易误导团队）。
>
> **唯一真正生效的是 `lastmod`**：帮爬虫判断"此页自上次抓取后是否变化、要不要重抓"，直接影响收录新鲜度（对 100 万级 PDP 尤为关键）。**前提是 `lastmod` 必须诚实**——只在内容真实变化时更新；若为催爬虫而每天刷成当前时间，Google/Bing 会识别其不可信，进而整体不再信任本站 `lastmod`。上表"更新节奏"仅作**内部 sitemap 重生成/lastmod 刷新的节奏参考**，不写入 `changefreq` 标签。

### 7.3 统一纳入条件与发现路径

任一 URL 只有同时满足以下条件才能进入 sitemap：

```text
HTTP = 200
AND robots = index
AND canonical = 当前 URL 自指
AND 页面已发布
AND 语言版本内容完整且可访问
AND sitemap_eligible = true
```

- 在售 PDP、`SOLD_RECENT` 和 `SOLD_RETAINED` 均满足条件，应进入商品 sitemap；
- `SOLD_NOINDEX`、WITHDRAWN、筛选、排序、搜索页不得进入；
- 301、404、410 URL 不得进入；
- Collection 只有 `seo_indexable=true` 时进入；AUTO 模式在售 3 件开放，0–2 件移出；
- Collection 分页页采用 index + 自指 canonical，但不进 sitemap；
- 西语 URL 只有在译文完整、robots=index 时进入，并与英语 URL 双向标注 hreflang。

**商品发现采用双通道**：

1. `sitemap-products-*.xml` 穷举所有最终可索引 PDP；
2. PLP See more 底层使用真实 `?page=N` 链接，爬虫和无 JavaScript 环境可以逐页发现 PDP。

sitemap 不能替代站内分页内链；分页页不进 sitemap 也不表示分页页不可抓取。

### 7.4 100 万级工程要点

- **协议硬限制**：单文件 ≤ 50,000 条 URL 且 ≤ 50MB（未压缩）→ 必须分片，由 `sitemap-index.xml` 统管。
- **预生成 + 缓存，禁止实时拼**：`products` 用定时/增量任务离线生成静态文件 + CDN 缓存；`collections/brands/static/content` 量小可实时或每日重建。
- **增量更新**：新品上架 / 商品售罄只更新**受影响的那个分片**，不必每次全量重刷 20 个文件。新品准实时进 sitemap，加速收录。
- **分片稳定**：按 `product_id` 段固定切片，避免全量重排导致所有分片 lastmod 齐变、爬虫误判全站更新。
- **lastmod 取真实值**：PDP 取商品最后更新时间（精确到时分）；集合取"该集合下最新商品上架时间 / 集合本身更新时间"。**禁止用生成时间戳糊弄**，会被 Google 忽略。
- **`sitemap-index.xml` 动态**：分片数随商品量增长（150 万→30 片），索引须反映当前实际分片数。
- **image 扩展（建议）**：PDP 加 `xmlns:image` + `<image:image>`，二手奢侈品强视觉，进 Google 图片搜索多一个流量入口。
- **`<loc>` 页面自身达标**：sitemap 只"告知存在"，被列页面须 SSR 直出 + canonical 自指 + robots index，才会被真正收录。

### 7.5 爬虫发现路径（robots.txt + GSC）

- **robots.txt**（根目录独立文件）只写**总索引**一行，子文件由索引串联、无需逐个列出：
  ```
  Sitemap: https://looply.com/sitemap-index.xml
  ```
  同时按 §6 放行 AI 爬虫。`/search` 必须保持可抓取以读取 noindex；购物车、结算和个人数据以权限保护为主，不用 robots.txt 替代访问控制或页面 noindex。
- **Google Search Console** 后台提交 `sitemap-index.xml` 一个地址即可，用于收录报告与错误排查。
- 发现链路：`robots.txt → sitemap-index.xml → 各子 sitemap → 页面`。全程与前端 HTML 无关。

### 7.6 示例片段

`sitemap-index.xml`（只列子文件地址）：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://looply.com/sitemap-collections.xml</loc>
    <lastmod>2026-07-02</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://looply.com/sitemap-products-1.xml</loc>
    <lastmod>2026-07-03T09:12:00-04:00</lastmod>
  </sitemap>
  <!-- ... products-2 到 products-20 ... -->
</sitemapindex>
```

`sitemap-collections.xml`（每个集合仅 1 条首页 URL，无分页）：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://looply.com/collections/chanel-bags</loc>
    <lastmod>2026-07-03</lastmod>
  </url>
  <!-- 升格组合（§6）同样是扁平 slug，非参数 URL；不输出 priority/changefreq -->
  <url>
    <loc>https://looply.com/collections/black-chanel-bags</loc>
    <lastmod>2026-07-01</lastmod>
  </url>
</urlset>
```

`sitemap-products-1.xml`（PDP 一品一条，含 image 扩展）：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
  <url>
    <loc>https://looply.com/products/chanel-classic-flap-medium-black-caviar-a12345</loc>
    <lastmod>2026-07-03T07:30:00-04:00</lastmod>
    <image:image>
      <image:loc>https://cdn.looply.com/products/a12345/main.jpg</image:loc>
    </image:image>
  </url>
  <!-- SOLD_RECENT 仍为 index 页面，因此继续进入 sitemap；90 天后按 §14 重新判断 -->
  <url>
    <loc>https://looply.com/products/lv-neverfull-mm-monogram-c11111</loc>
    <lastmod>2026-07-03T06:00:00-04:00</lastmod>
  </url>
</urlset>
```

- 搜索页、参数筛选页、排序页、购物车/结算/账户**不进 sitemap**。

### 7.7 sitemap 一致性对账（发布阻断）

- sitemap 生成任务必须读取统一 SEO 状态计算结果，不得另写一套库存或商品状态判断；
- 每次发布执行全量对账；生产环境至少每日检查一次；
- sitemap 中任一 URL 返回非 200、noindex、canonical 非自指、301/404/410，均视为失败；
- 应进 sitemap 的规范内容页遗漏、同一 canonical 重复出现、语言 alternate 不双向，均视为失败；
- 分页页为明确例外：可索引但不进 sitemap，不计为遗漏；
- 页面最终索引状态变化时，只更新受影响分片，并使用真实内容变化时间更新 lastmod。

## 8. 性能（Core Web Vitals，技术实现 + 验收）

移动端基线：

- **LCP < 2.5s**：hero/主图预加载、首屏图 priority、控制首屏 JS 体积。
- **INP < 200ms**：控制水合开销、避免过度水合。
- **CLS < 0.1**：图片/字体占位防抖动。
- 图片：WebP/AVIF、响应式 srcset、首屏外懒加载。
- 核心文案区块 SSG/ISR 静态化，保证 AI 爬虫稳定可读。

## 9. 三端技术实现

- **响应式同 URL**（不做 `m.` 独立站），避免双倍维护与重复内容。
- **移动版即被索引版本**：移动端 SSR 内容完整性 = 排名上限。
- **APP**：APP 与 Web 同期上线，靠 Universal/App Links 实现 Web 链接唤起 APP（Deep Link）；Web 为索引主体。首页/PLP/PDP/内容页配 App 引导 banner 引导下载/打开（展示页面清单见 §9.2）。

### 9.1 移动端 H5 设计与 SEO 的边界（重要）

Looply 的移动端定位：**H5 与 APP 共用移动端设计语言**，H5 不按 PC 等比缩小，而是按移动端购物体验重新设计。但这带来一条必须守住的技术红线——

**H5 可以"长得像 App"，但底层必须是标准、可索引的电商网页。** 无论交互观感多接近 App，以下网页基本结构一个都不能丢：

| 必守底层 | 具体要求 |
|---|---|
| 独立 URL | 每个商品/品类/内容有自己的可访问 URL（`/products/...`、`/collections/...`），不是单页 hash 路由 |
| 完整内容 SSR | 首屏内容服务端直出，不靠纯 JS 客户端渲染（否则爬虫/AI 抓不到） |
| 可抓取链接 | 用真实 `<a href>`，不是 `onclick`/`div` 模拟跳转 |
| 结构化数据 | schema 照常输出（见 §5） |
| 清晰 metadata | title/description/canonical/og 照常（见 §3、§6） |
| 性能 | 满足 §8 Core Web Vitals 基线 |

**反模式（禁止）**：把 H5 做成"网页里的 App 壳"——空 HTML + 全靠 JS 拉数据渲染、无独立 URL、链接用 JS 跳转。这种"伪 App"对 Google/AI 几乎不可索引，等于放弃移动端 SEO（而移动端是 Google 索引的主版本，见上）。

> 一句话：**H5 长得像 App，底层像一个干净、标准、可索引的电商网页**——既不伤 SEO，又更适合移动端转化。

### 9.2 App 引导 Banner + Deep Link 配置

APP 与 Web 同期上线，需实现两件事：① 移动端 Web 顶部展示 App 引导条；② 点 Web 链接能唤起 APP 对应页面（Deep Link）。二者是**两层、分开实现**：

- **展示层（banner UI）**：**全站三端统一用前端自建 banner**（iOS Safari / iOS 非 Safari / Android 同一套），**不使用 iOS 原生 `apple-itunes-app` meta**——原因见 A。文案、样式、静默期、埋点全部可控，三端体验一致，可承载营销文案（如"下载领 $20"）。
- **唤起层（deep link）**：iOS Universal Links + Android App Links **照常部署**（见 B、C）。这层是操作系统级的链接唤起机制，与 banner 长什么样无关，**不因改用自建 banner 而省略**。

**展示页面**：banner 不只放首页，凡是可被分享/搜索直达的落地页都放——用户从 Google 或分享链接直接落到某商品/品类页时，引导"用 App 看这件商品"转化最高，且 deep link 直接唤起对应页。范围与 §3.2 OG 输出页面基本一致：

| 页面 | 展示 | 理由 |
|---|---|---|
| 首页 | ✅ | 品牌入口 |
| PDP 商详 | ✅（最该放） | 分享/搜索直达占比高，deep link 唤起该商品页，转化最高 |
| PLP 品类/品牌页 | ✅ | deep link 到对应 collection |
| 内容/指南页 `/guides/` | ✅ | 引导下载 |
| `/shop`、`/favorites`、搜索、账户、购物车 | ❌ | 功能/工具页，不引导 |

每页的 deep link 目标取**当前页规范 URL**，各页链各页，不写死首页。

**A. 展示层 —— 全站统一自建 banner（三端一套）**

三端统一用前端自建 banner，**不用 iOS 原生 `apple-itunes-app` meta**。原因：

- **一致 + 可控**：文案、样式、静默期、埋点三端统一，可承载营销文案（如"下载领 $20"）与活动，原生 meta 做不到（App 名/图标/评分由 Safari 自动拉、不可改）；
- **避免双条**：iOS Safari 若同时保留原生 meta + 自建条，会**顶部并排出现两条 banner**（系统原生 + 自建），既伤体验又触发 E 的首屏/CLS 红线。故**全站不注入 `apple-itunes-app` meta**，只保留一套自建。

自建 banner 行为逻辑（三端一致）：

- **已装 APP**：点击 → 走唤起层（Universal/App Links，见 B/C）深链到当前页规范 URL；
- **未装 APP**：点击 → 跳应用商店（iOS→App Store，Android→Google Play，按 UA 判定）；
- **深链目标**：由 SSR 注入当前页规范 canonical URL，各页链各页，不写死首页。

**B. 唤起层（iOS）—— Universal Links**

在域名根部署 `apple-app-site-association`（AASA）文件，声明哪些路径由 APP 接管：

```
路径： https://looply.com/.well-known/apple-app-site-association
      （无扩展名、Content-Type: application/json、HTTPS、不可重定向）
```
```json
{
  "applinks": {
    "details": [{
      "appID": "TEAMID.com.looply.app",
      "paths": ["/products/*", "/collections/*", "/guides/*", "/"]
    }]
  }
}
```

**C. 唤起层（Android）—— App Links**

- 域名根部署 `assetlinks.json` 声明网站与 APP 的关联，配合 APP 端 intent-filter + `android:autoVerify="true"`：

  ```
  路径： https://looply.com/.well-known/assetlinks.json（HTTPS、application/json）
  ```
  ```json
  [{
    "relation": ["delegate_permission/common.handle_all_urls"],
    "target": {
      "namespace": "android_app",
      "package_name": "com.looply.app",
      "sha256_cert_fingerprints": ["APP 签名证书 SHA-256"]
    }
  }]
  ```

> 因全站统一自建 banner，**iOS 所有浏览器一视同仁**（Safari 与 Chrome/Firefox 走同一套自建条），不存在"iOS 非 Safari 盲区"，也无需按浏览器分叉逻辑。

**D. 关闭与静默期（自建 banner 可控）**

因展示层是自建的，关闭后的静默期由前端完全掌控（不像 iOS 原生 banner 那样由系统决定、不可配置）。规则：

- **关闭即静默 7 天**：用户点关闭 → 写 `localStorage` 时间戳 → **7 天内该端不再弹**，到期后可再次展示。（7 天：二手奢侈品复访周期不高频，既不打扰又保留再触达。）
- **唤起成功即停弹**：用户点 banner 成功唤起/跳商店，视为已触达，同样写入时间戳按 7 天静默（避免已转化用户反复被打扰）。
- **不做"永久关闭"**：用户清缓存会重置 `localStorage`，永久关闭既不可靠也无必要。
- **静默期按端隔离**：`localStorage` 按浏览器隔离，同一用户在 Safari 与 Chrome 的静默期各自独立——这是浏览器存储的天花板，接受即可，不强做跨端同步。

**E. SEO 红线（banner 不能伤索引）**

| 红线 | 要求 |
|---|---|
| 不占标题层级 | 引导条为独立 UI 层，**不使用 `<h1>`~`<h6>`**，不与页面唯一 H1 冲突 |
| 不遮首屏内容 | 不得盖住 LCP 主内容（Hero/H1/信任信号），自建条注意留出安全间距 |
| 不引入 CLS | banner 占位要预留高度或用 fixed 层，避免推动内容造成布局抖动（CLS<0.1，见 §8） |
| deep link = 规范 URL | `app-argument` 与 App/Universal Links 的目标必须是页面**规范 canonical URL**，与 SEO 一致，防深链页与索引页不一致 |
| 关联域一致 | AASA / assetlinks.json 的域名与 `sameAs`、canonical 主域保持一致 |

**F. 埋点**：banner 曝光 / 点击 / 唤起成功 / 跳商店，分平台上报，供 APP-ASO 与增长分析（口径与 §10 监测对齐）。

## 10. 接入与监测（上线前）

- 接入 GSC / Bing Webmaster / GMC / 分析工具。
- 搜索词埋点（见搜索页 §16）。

## 11. 国际化（i18n / 多语言 URL / hreflang）

> **本节前提**：一期即上线 **en + es 双语**（英语为源/默认语言，es 为通用西语，不限地区）。此前文档中"MVP 单语言 en-us、hreflang 仅预留"的表述**已作废**。多语言内容的存储/翻译/查询由《looply 多语言模块 PRD v3.1》负责，本节只定义**前台 SEO 层**：URL 结构、hreflang、canonical、sitemap 与红线。两份文档的接缝是 `language_code`。

### 11.1 URL 结构（子目录，英语裸 URL）

- **英语（源/默认）走裸 URL，es 走 `/es/` 子目录前缀**：
  ```
  looply.com/collections/chanel-bags        → en（默认，x-default）
  looply.com/es/collections/chanel-bags     → es（通用西语）
  ```
- 选子目录（非子域名/ccTLD）：新站权重宝贵，子目录让各语言**共享 looply.com 主域权重**，成本最低、不返工。
- `/es/` 前缀由前端路由解析出 `language_code=es`，据此向翻译服务查询 es 译文（对接多语言模块 §3.4 的 `resource_type+resource_id+field_name+language_code`）。
- **语言代码用通用 `en`/`es`**（对齐多语言模块 ISO 639-1），**不加地区后缀**（不用 `es-us`/`es-mx`）——一期定位通用西语，加地区反而限制展示范围。

### 11.2 hreflang（每个页面 `<head>` 输出，含自指 + x-default）

每个可索引页面输出**全量** hreflang 组（含自身），en/es 两页指向同一组：
```html
<link rel="alternate" hreflang="en" href="https://looply.com/collections/chanel-bags" />
<link rel="alternate" hreflang="es" href="https://looply.com/es/collections/chanel-bags" />
<link rel="alternate" hreflang="x-default" href="https://looply.com/collections/chanel-bags" />
```
- **x-default 指向英语裸 URL**（默认语言）。
- **hreflang 清单动态生成**：读 Market 模块已开通语言（对接多语言模块 §1.5），新增语言自动追加 hreflang 条目，**不硬编码**——将来上第三语言零返工。

### 11.3 canonical（各语言自指）

- 每个语言版本 canonical **指向自己**：`/es/...` 的 canonical = `/es/...`，英文页 canonical = 裸 URL。
- **禁止跨语言 canonical**（如 es 页 canonical 回英文页）——否则 es 页被判为英文页副本，不被收录，直接丢西语流量。

### 11.4 sitemap 多语言标注

- en/es 两个 URL **都进 sitemap**；每条 `<url>` 用 `xhtml:link` 标注各语言互为 alternate：
  ```xml
  <url>
    <loc>https://looply.com/collections/chanel-bags</loc>
    <xhtml:link rel="alternate" hreflang="en" href="https://looply.com/collections/chanel-bags"/>
    <xhtml:link rel="alternate" hreflang="es" href="https://looply.com/es/collections/chanel-bags"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://looply.com/collections/chanel-bags"/>
  </url>
  ```
- `urlset` 需声明 `xmlns:xhtml="http://www.w3.org/1999/xhtml"`（补充 §7 的 sitemap 命名空间）。

### 11.5 红线（易错，必须守住）

1. **每语言 SSR 直出**：es 译文必须服务端渲染进首屏 HTML，不能纯 JS 拉取——否则 Googlebot 抓不到 es 内容、不收录（呼应 §9.1 移动端红线）。
2. **fallback 页不打错语言标签**：多语言模块 §4.6 规定某语言无译文时前台回退英文。这种"实为英文的 es URL"**要么不生成该 es URL、要么不给它输出 es hreflang**，避免"声明 es 却给英文"的矛盾信号误导爬虫。
3. **币种不进 URL**：本模块只管语言，不管币种。USD 等币种显示靠 geo/用户选择，**不产生 `?currency=` 类 URL 变体、不进 sitemap、不生成新可索引页**（防重复页吃抓取预算）。
4. **canonical 各语言自指**（见 §11.3）。
5. **hreflang 与实际可访问 URL 一致**：声明的每个 hreflang URL 必须真实可独立访问、返回对应语言、robots index。
6. **PDP 多语言 = 同一件商品的翻译**：二手一品一件，各语言 PDP 是同一 SKU 的不同语言版，用 hreflang 互指、canonical 各自自指，不是不同商品。

### 11.6 反模式（禁止）——cookie/session 切语言而不改 URL

- **禁止**用 cookie/session 在同一 URL 下切换语言（部分大站如 SHEIN 在 SEO 页这么做）。原因：Googlebot 默认不带 cookie、不点语言切换，抓同一 URL **只会看到一个语言版本**，非默认语言内容无法被发现和收录。
- 大站靠体量/投放可承受非默认语言收录不全，**新站不能**——Looply 一期即吃西语自然流量，必须让 es 页有独立可抓取 URL。
- 注意区分：`/user/*`、`/cart`、`/checkout`、`/account` 等 **noindex 账户/交易页**切语言用 cookie 是正常的（本就不参与 SEO），本红线只约束**可索引的 SEO 页面**（首页/PLP/PDP/内容页）。

### 11.7 与多语言模块的接缝

| 层 | 归属 | 内容 |
|---|---|---|
| URL / hreflang / canonical / sitemap | 本文（SEO/前端） | `/es/` 路由、hreflang 输出、各语言自指 canonical、sitemap xhtml 标注 |
| 语言清单（有哪些语言） | Market 模块 | hreflang 动态读取来源 |
| 译文存储/翻译/查询 | 多语言模块 PRD v3.1 | 按 `language_code` 返回对应语言文本 |
| 源语言 = en | 多语言模块 §1.5/§3.8 | 印证英语为默认/x-default |

---

# 第二部分 · 分页面技术实现说明

## 12. 首页

**渲染**：区块 1-4、6、8-9 走 SSG；精选商品（区块 5）ISR/动态；社会证明可 SSG/ISR。

**技术实现点**：

- 首屏 SSR 直出 H1 + 信任信号（移动可见）；
- title/description/H1/H2/OG 按规范输出；
- **OnlineStore + WebSite schema** 在首页初始 HTML 中直出。`OnlineStore` 是 `Organization` 的更具体电商子类型，用作 Looply 商店主体实体；`WebSite` 用作网站实体。两者放入同一个 `@graph`，并通过稳定 `@id` 建立关系：

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "OnlineStore",
      "@id": "https://looply.com/#store",
      "name": "Looply",
      "url": "https://looply.com/",
      "logo": {
        "@type": "ImageObject",
        "url": "https://looply.com/logo.png",
        "contentUrl": "https://looply.com/logo.png"
      },
      "description": "Authenticated pre-owned luxury marketplace for bags, jewelry, and watches.",
      "sameAs": [
        "https://www.instagram.com/looply",
        "https://www.tiktok.com/@looply",
        "https://www.trustpilot.com/review/looply.com"
      ],
      "contactPoint": {
        "@type": "ContactPoint",
        "contactType": "Customer Service",
        "email": "{{customer_service_email}}"
      }
    },
    {
      "@type": "WebSite",
      "@id": "https://looply.com/#website",
      "url": "https://looply.com/",
      "name": "Looply",
      "publisher": {
        "@id": "https://looply.com/#store"
      }
    }
  ]
}
```

- 完整的 `OnlineStore` 主体档案原则上只需放在首页或单独的 About 页面。MVP 放首页；Article/PDP/作者页可按页面关系输出最小引用。如 About 页或 `/es/` 首页也输出完整档案，必须复用 `https://looply.com/#store`，不得生成第二个 Looply 商店实体；语言版本可本地化 `description`，但 `@id`、`name`、`url`、`logo` 必须一致。
- `sameAs` 只输出已上线且可公开访问的 Looply 官方资料页；`contactPoint` 只在真实客服渠道确认后输出，模板变量 `{{customer_service_email}}` 上线前必须替换，禁止原样部署或填虚假邮箱。
- Logo URL 必须返回 200、允许抓取和索引，图片至少 112×112 px，并确保在白色背景上可识别。
- Google 已于 2024-11-21 停止展示 Sitelinks 搜索框，因此本版本删除 `SearchAction`/`potentialAction`，但保留 `WebSite` 节点用于网站名称和网站实体识别。
- 全站引用统一：`Article.publisher`、`Person.worksFor`、`Product.offers.seller` 复用 `https://looply.com/#store`；页面需要独立验证的建议字段（如 Article publisher 的 name/logo）仍需在当前页面节点内保留。
- 官方依据：[Google Organization 结构化数据指南](https://developers.google.com/search/docs/appearance/structured-data/organization)、[Sitelinks 搜索框停止展示公告](https://developers.google.com/search/blog/2024/10/sitelinks-search-box)。

- 首页为根，不挂 BreadcrumbList；
- 内链分发（导航/卡片/Footer 指向 PLP 与内容页）；
- Smart App Banner + Universal/App Links（配置见 §9.2）。

## 13. 分类页 PLP

**渲染**：SSR，schema 直出首屏。

**技术实现点**：

- title/H1 按规范输出（title 留空走降级链 `Pre-Owned {Brand} {Category} | Authenticated | Looply`）；
- **分面索引规则**：参数筛选/排序页输出 noindex,follow、不设置 canonical、不进 sitemap（见 §6）；
- canonical 自指主集合页（无参数版）；
- **ItemList schema**：标注商品列表（url/name/image/position）；
- **分页与商品发现（v2.0 已定：See more + 真实分页 + sitemap 双通道）**：
  - See more 必须渲染为真实 `<a href="?page=N">`；JavaScript 可拦截并原地追加，但关闭 JS 仍可导航；
  - 每个合法分页 URL SSR 返回对应商品批次；主排序字段相同时用 `listing_id` 作为最终稳定排序键；
  - 第 2 页及以后 robots=index、canonical 自指、title 追加 `– Page {N}`，但不进 sitemap；
  - `?page=1` 单跳 301 到无 page 的规范 URL；0、负数、非整数、超范围页码返回 404；
  - 带筛选参数的分页 noindex、不设置 canonical、不进 sitemap；
  - sitemap 穷举最终可索引 PDP，真实分页提供站内发现和内链，两者不可互相替代。
- **索引质量门槛**：读取 §6.2 的统一结果。AUTO 模式在售数 ≥3 才 index；0–2 为 noindex。FORCE_INDEX 需至少 1 件在售、H1 非空且有自定义描述；FORCE_NOINDEX 始终关闭索引。

**品牌页**：品牌页就是**用 collection 建、以品牌名为 slug 的普通 PLP**（如 `/collections/chanel`），无独立数据源、无品牌管理模块关联——URL/canonical/robots/分页/索引质量门槛/进 sitemap 等全部同普通 collection。运营建 collection 时把名称填为品牌名、slug 用品牌名即可。

- **文案模板**：H1/title 建议 `Pre-Owned {Brand}` / `Pre-Owned {Brand} | Looply`（运营录入，无需特殊引擎）。schema 也同普通 collection（BreadcrumbList + ItemList），不单独输出品牌专属 schema。

## 14. 商详页 PDP

**渲染**：SSR，schema 直出首屏。

**技术实现点**：

- title：`{Brand} {Model} {Key-Attr} - Pre-Owned | Looply`；H1 商品全名；
- canonical 自指 `/products/{slug}-{id}/`（防任何参数/来源 URL 重复收录）；
- 图片：实拍图、`alt` 按 §3.1 模板自动生成（可人工覆盖）、文件名语义化、ImageObject schema；
- 面包屑见 §4。

**Product schema（二手关键差异，最易漏）**：

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Chanel Classic Flap Medium Caviar Black",
  "image": ["实拍图URL数组"],
  "description": "差异化成色描述...",
  "brand": { "@type": "Brand", "name": "Chanel" },
  "sku": "唯一商品ID",
  "itemCondition": "https://schema.org/UsedCondition",
  "offers": {
    "@type": "Offer",
    "price": "3200.00",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "itemCondition": "https://schema.org/UsedCondition",
    "url": "https://looply.com/products/...",
    "seller": { "@type": "OnlineStore", "@id": "https://looply.com/#store", "name": "Looply" }
  }
}
```

- `itemCondition: UsedCondition` 必填（非默认 NewCondition）；
- `availability` 随状态机变化：InStock → `https://schema.org/OutOfStock`；
- 价格币种固定 USD（MVP 单市场）；
- GMC feed price 复用 listing_price（与现有 GMC 定价策略一致）。

**商品退出在售生命周期（v2.0）**：

| SEO 页面状态 | 业务触发 | HTTP | robots | canonical | sitemap | 页面行为 |
|---|---|---:|---|---|---|---|
| `IN_STOCK` | 正常在售 | 200 | index | 自指 | 进入 | 正常购买 |
| `SOLD_RECENT` | 正常售出且未满 90 天 | 200 | index | 自指 | 进入 | Sold、CTA 置灰、推荐与回流 |
| `SOLD_RETAINED` | 售出满 90 天且满足保留价值条件 | 200 | index | 自指 | 进入 | Sold、CTA 置灰、推荐与回流 |
| `SOLD_NOINDEX` | 售出满 90 天且无保留价值 | 200 | noindex | 不设置 | 移出 | URL 仍可访问，继续回流 |
| `WITHDRAWN` | 未成交但撤回、质检失败或停止经营 | 200 | noindex | 不设置 | 移出 | 不得显示 Sold，展示不可购买与替代入口 |
| `MERGED` | 重复商品或 URL 合并 | 301 | — | 跳到保留 PDP | 移出 | 不渲染旧详情页 |
| `REMOVED` | 违规、法律或隐私要求永久删除 | 410 | — | 无 | 移出 | 不泄露原商品信息 |
| `NOT_FOUND` | 从未存在或 ID 无法识别 | 404 | — | 无 | 移出 | 通用 404 |

售出满 90 天后，满足下列任一条件进入 `SOLD_RETAINED`，否则进入 `SOLD_NOINDEX`：

1. `seo_retention_mode=KEEP_INDEX`；
2. 最近 90 天存在自然搜索访问；
3. 已识别到有效外部反向链接；
4. 当前至少有 3 件相似在售商品。

`seo_retention_mode` 完整枚举：`AUTO`（默认，按价值条件）、`KEEP_INDEX`（人工保留）、`FORCE_NOINDEX`（人工停止索引）。如果 MVP 尚未接入自然搜索或外链数据，AUTO 先使用人工模式与相似在售数，状态输出不变。

所有已售状态的 Product/Offer availability 输出 `https://schema.org/OutOfStock`，并与页面可见状态和商品主数据一致。相似商品降级顺序固定为：同品牌+同类目 → 同类目 → 规范 Collection 热门在售商品 → 规范 Collection CTA。

> **跨模块依赖**：商品系统需提供售出时间、退出原因、合并目标、合规删除标记、相似在售数和 SEO 保留模式；搜索与推荐不得返回 WITHDRAWN、REMOVED、NOT_FOUND 商品。

## 15. 搜索页

**渲染**：CSR（已定 S1）。结果内容不要求 SSR，但 noindex 必须由服务器初始 HTML 或 `X-Robots-Tag` 直出，使爬虫无需执行 JavaScript 即可读取。

**技术实现点**：

- 搜索结果页 **noindex,follow**、不设置 canonical、不进 sitemap；分页/排序参数同规则；robots.txt 不屏蔽 `/search`；
- 结果卡片 follow 链向 PDP（辅助爬虫发现商品）；
- 零结果页**仍 noindex**；
- 同义词/拼写容错（搜"purse"匹配"bag"、"chanle"→"chanel"）；
- autocomplete 搜索建议；
- 复用 PLP 分面筛选组件（这些筛选 URL 同样 noindex）；
- 品牌词智能跳转（已定 S2）：整串 query 恰为品牌/品类词且目标有货时，**302/前端路由跳转**（非 301——搜索页 noindex，目的是沉淀流量非传权重）到 `/collections/chanel`；带修饰长尾不跳。完整规则见产品文档 §9。

**搜索词埋点（核心，不能等）**：

- 采集字段：**query 词、结果数、是否零结果、是否点击、点击位次**；
- 数据回流供运营分析（看板 Phase 1）。

## 16. 内容/指南页

**渲染**：SSR/SSG，核心内容静态可读。

**技术实现点**：

- H1 含核心问题关键词；
- 答案前置 TL;DR（首段直接给答案，AI Overviews 优先抓）；
- 作者署名 + 资质 + 审核日期；
- H2/H3 问答式分节；
- URL `/guides/{slug}/`（已定 C1）；
- 内容中心 Hub `/guides/`（可索引，列出所有指南）；
- Topic Cluster 支柱+卫星互链结构；
- **schema 组合**：Article/BlogPosting + FAQPage + HowTo + BreadcrumbList + Person（验真指南用 HowTo + FAQPage 最佳）；
- 内链 CTA 指向 PLP/PDP；
- 更新日期输出（内容新鲜度信号）。

---

## 附一：统一 SEO 状态计算层

页面 head、HTTP 响应、sitemap、面包屑候选、hreflang 和后台状态展示必须读取同一计算结果，禁止在前端、sitemap 任务和后台分别复制判断条件。

| 统一输出 | 说明 |
|---|---|
| `http_status` | 200 / 301 / 404 / 410 |
| `robots_indexable` | index / noindex |
| `canonical_url` | 规范 URL；不适用时为空 |
| `sitemap_eligible` | 是否进入 sitemap |
| `seo_state_reason` | 得到当前状态的确定原因 |
| `breadcrumb_eligible` | 是否允许作为 PDP 面包屑中间级 |
| `hreflang_eligible` | 当前语言版本是否进入 hreflang 组 |

任何新增业务状态必须显式映射以上全部输出，不允许默认落入 index。

## 附二：AI Coding 自动化验收矩阵

以下用例为固定验收标准，不得根据实现结果反向生成预期值。

### A. 分页与无 JS 抓取

| 用例 ID | 场景 | 断言 |
|---|---|---|
| PAG-001 | Collection 第 1 页 | 200；canonical 无 page；存在指向 page=2 的真实链接 |
| PAG-002 | 无 JS 请求 page=2 | 200；返回第 2 批商品；index；canonical 自指 |
| PAG-003 | 遍历全部分页 | 同一排序快照下商品不重复、不遗漏 |
| PAG-004 | page=1 | 单跳 301 到无 page URL |
| PAG-005 | 非法或超范围页码 | 404，不返回最后一页，不形成 soft 404 |
| PAG-006 | 筛选分页 | 200；noindex；无 canonical；不进 sitemap |
| PAG-007 | 禁用 JS 点击 See more | 能导航并看到下一页商品 |

### B. robots/noindex/canonical

| 用例 ID | 场景 | 断言 |
|---|---|---|
| ROB-001 | 搜索页初始响应 | 200；无需执行 JS 即可读到 noindex；robots.txt 未屏蔽 `/search` |
| ROB-002 | 筛选页 | 200；noindex；无 canonical；不进 sitemap |
| ROB-003 | UTM 变体 | 200；index；canonical 指向无 UTM 规范 URL |
| ROB-004 | 应进 sitemap 的规范内容页 | 可抓取；index；canonical 自指；在对应 sitemap |
| ROB-005 | 遍历 sitemap | 不存在 noindex、301、404、410 URL |
| ROB-006 | 核心内链 | 无需经过搜索/筛选页即可到达核心 PLP/PDP |

### C. Collection 索引门槛

| 用例 ID | 场景 | 断言 |
|---|---|---|
| PLP-001 | AUTO 库存 0/1/2 | 200；noindex；不进 sitemap；不作面包屑中间级 |
| PLP-002 | AUTO 库存 3 | 200；index；canonical 自指；进入 sitemap |
| PLP-003 | 库存 3→2 | 切 noindex；移出 sitemap；缓存和面包屑候选失效 |
| PLP-004 | 库存 2→3 | 切 index；进入 sitemap；lastmod 更新 |
| PLP-005 | FORCE_INDEX，库存≥1且描述完整 | index；原因为 MANUAL_FORCE_INDEX |
| PLP-006 | FORCE_INDEX，库存 0或描述为空 | 拒绝保存，不开放索引 |
| PLP-007 | FORCE_NOINDEX，库存充足 | noindex；不进 sitemap；原因为 MANUAL_FORCE_NOINDEX |

### D. PDP 生命周期

| 用例 ID | 场景 | 断言 |
|---|---|---|
| PDP-001 | 在售商品售出 | SOLD_RECENT；200；index；OutOfStock；仍在 sitemap |
| PDP-002 | 售出满 90 天且相似在售数≥3 | SOLD_RETAINED；200；index；在 sitemap |
| PDP-003 | 售出满 90 天且无保留价值 | SOLD_NOINDEX；200；noindex；移出 sitemap |
| PDP-004 | KEEP_INDEX | 保留 index，除非进入 REMOVED/MERGED |
| PDP-005 | FORCE_NOINDEX | 200；noindex；移出 sitemap |
| PDP-006 | 重复记录合并 | 旧 URL 单跳 301 到保留 PDP |
| PDP-007 | 合规永久删除 | 410；不泄露原商品信息 |
| PDP-008 | 不存在 ID | 404；不返回 Sold 模板；无 canonical |
| PDP-009 | 已售页无相似商品 | 展示规范 Collection CTA，不显示空白模块 |
| PDP-010 | 状态对账 | 页面可见状态、Offer availability、后台状态一致 |

### E. sitemap 对账

| 用例 ID | 场景 | 断言 |
|---|---|---|
| SMP-001 | 遍历 sitemap URL | 全部 200、index、canonical 自指 |
| SMP-002 | 遍历应收录对象 | 全部且只出现在一个正确 sitemap |
| SMP-003 | index 切 noindex | URL 移出 sitemap，受影响分片 lastmod 更新 |
| SMP-004 | 301/404/410 页面 | 不进入 sitemap |
| SMP-005 | en/es 页面 | 只纳入内容完整版本，alternate 双向一致 |
| SMP-006 | 分页 URL | 不进 sitemap，但可由 Collection 链接发现 |

### F. 商店实体 Schema

| 用例 ID | 场景 | 断言 |
|---|---|---|
| SCH-001 | 抓取首页初始 HTML | JSON-LD 可解析；存在 `OnlineStore#store` 与 `WebSite#website`；`WebSite.publisher.@id` 精确指向 `https://looply.com/#store` |
| SCH-002 | 检查首页商店主体节点 | Looply 主体使用 `OnlineStore`，不再单独创建无 `@id` 的 `Organization`；不存在 `SearchAction`、`potentialAction` 或未替换的 `{{...}}` 模板变量 |
| SCH-003 | 抽查 Article、Person、Product 页面 | `publisher`/`worksFor`/`seller` 均复用 `https://looply.com/#store`；Article publisher 同页保留 name/logo |
| SCH-004 | 首页、About 页和多语言首页实体对账 | 如多处输出商店主体，全部复用同一 `#store`；核心 name/url/logo 一致；无第二个 Looply 商店实体 ID |

发布阻断条件：任一上述用例失败、任一 sitemap URL 为 noindex/非 200、任一删除页返回 200、任一搜索页缺 noindex、任一 PLP 分页无法无 JS 访问、首页 schema 无法解析或商店实体 ID 不一致。

## 附三：技术相关的跨模块依赖与待对齐项

| 依赖/待对齐 | 涉及 | 内容 | 对齐方 |
|---|---|---|---|
| PDP URL 形态 + 路由 | PDP | `{slug}-{id}`、按 id 解析、slug 不符 301、canonical 自指 | 商品系统 |
| 商品退出在售状态 | PDP、搜索、推荐、sitemap | 提供售出时间、退出原因、合并目标、合规删除、相似在售数、`seo_retention_mode` | 商品系统 |
| 相似商品召回能力 | PDP 已售回收、首页、内容页 | 按同品牌+同类目 → 同类目 → 规范 Collection 热门商品降级，至少返回 Collection CTA | 商品系统 |
| Collection SEO 状态 | PLP、sitemap、面包屑 | `in_stock_count`、`seo_index_mode`、门槛 3、`seo_indexable`、`seo_index_reason` 由统一规则计算 | Collection 管理/技术 |
| PDP 面包屑中间级锚点 | PDP、Collection 管理 | collection 侧维护 `breadcrumb_role` 标记并要求 `seo_indexable=true`；品牌优先类目兜底、取不到降两级 | Collection 管理/产品 |
| SEO 状态统一计算层 | 页面 head、HTTP、sitemap、面包屑、hreflang、后台 | 同一结果输出状态码、robots、canonical、sitemap 资格、原因和各类 eligibility | 技术 |
| sitemap 自动对账 | 所有可索引页面 | 发布时全量对账，生产每日检查 200/index/canonical 自指与遗漏 | 技术/运维 |
| 图片部位枚举 | PDP 图片 alt | `product_image` 新增"部位枚举"字段（正面/内部/五金/底部/瑕疵等），供细节图 alt 自动生成语义版；无则降级 `detail {n}`（见 §3.1） | 商品系统 |
| 商品显示名取数能力 | PDP alt/slug/title | 对外提供"取商品显示名"：`listing_title → product.title` 两级降级链（product.title 上架必非空作兜底），供 alt、slug、title 复用同一口径 | 商品系统 |
| URL Slug 自动生成 | PDP URL | 商品模块 URL Slug 目前为纯手填，需补成"自动 slugify(商品显示名)+可手改"（对齐其 SEO Title 的自动生成逻辑） | 商品系统 |
| 活动 banner alt 必填 | 活动/营销页 | 活动 banner 无结构化字段可拼，alt 设为必填 + placeholder 提示；落在 CMS/营销模块 | CMS/营销 |
| 搜索词埋点口径 | 搜索页 | query/结果数/零结果/点击/位次 | 数据/选品团队 |

*文档结束*
