# Looply · 首页 PRD v1.7

> 版本：v1.7 | 更新日期：2026-08-11 | 端：Mobile Web + PC Web
> 状态：🔄 迭代中

## 1. 概述

### 1.1 目标

首页承担三项核心任务：

1. 通过品牌表达、鉴定说明和服务承诺建立购买信任。
2. 通过 Banner 与 Curated Collections 承接运营内容和购物场景。
3. 通过 Explore Finds 持续提供商品发现与浏览入口。

### 1.2 当前范围与模块边界

- 当前 PRD 覆盖 Mobile Web 与 PC Web 首页。
- 首页负责搜索入口的展示和触发方式；《Looply Web 全局搜索 PRD v0.3》是搜索发现、Sug、Recent searches、Popular content、输入校验、搜索执行和结果页规则的唯一产品规则来源。
- 导航栏、Banner、Collections 等后台配置规则由各自配置模块负责；首页消费已生效内容并按返回顺序展示。
- 页面展示、组件样式、间距、响应式布局和文案排版以当前最新 UI 稿为准；本 PRD 补充数据来源、状态、跳转和跨页面行为。

### 1.3 用户与核心场景

| 场景 | 首页能力 |
|---|---|
| Discover | Banner、信任内容、服务承诺 |
| Browse | Curated Collections、Explore Finds |
| Intent | 首页搜索入口进入全局搜索 |
| Consideration | 收藏入口、商品收藏、返回后恢复浏览状态 |

### 1.4 页面流转

```text
首页
├── 搜索入口 → Web 全局搜索
├── Banner → CMS 配置的目标页
├── Curated Collections → 对应 Collection 页
├── Explore Finds 商品卡 → 商品详情页
├── Favorites 入口 → Favorites 页
├── Account 入口 → Account Home
└── Mobile Web 底部导航 → Home / Shop / Favorites / Account
```

## 2. 市场、多语言与 UI 基线

### 2.1 市场与语言

- Web V1 使用美国市场，`market_id` 固定为美国市场标识。
- 页面支持英语和西班牙语，按照用户当前选择的 locale 展示静态 UI 文案和动态业务内容。
- 语言入口及页面内容始终与当前已生效 locale 一致。
- 英语界面的语言入口标题使用 `Language`，仅首字母大写。
- 未登录用户的语言选择保存在当前浏览器；已登录用户按账号保存。页面重新加载后恢复已保存语言。
- 静态 UI 文案使用 Web 统一 i18n message package；动态业务内容读取当前 locale 对应的内容。

### 2.2 已确认关键文案

| 位置 | English | Español |
|---|---|---|
| 首页 Slogan | `Designer pieces deserve another chapter.` | 读取当前 UI / i18n 配置 |
| 信任模块标题 | `Confidence in Every Find` | `Confianza en cada compra` |
| 商品推荐模块标题 | `Explore Finds` | `Selecciones para ti` |
| Easy Returns 说明 | `Returns made simple and stress-free.` | `Devoluciones fáciles y sin complicaciones.` |
| Free Shipping 说明 | `Fast, free shipping within the contiguous U.S.` | `Envío rápido y gratuito a los 48 estados contiguos de EE. UU.` |
| Customer Support 说明 | `Friendly support whenever you need it.` | `Estamos aquí para ayudarte cuando lo necesites.` |
| Footer About | `About` | `Sobre nosotros` |
| Footer Stay in the Loop | `Stay in the Loop` | `Mantente al tanto` |
| Footer Shop | `SHOP` | `COMPRAR` |
| Footer Support | `SUPPORT` | `AYUDA` |
| Mobile 底部 Shop | `Shop` | `Comprar` |
| Account | `Account` | `Cuenta` |

## 3. 顶部导航 Header

### 3.1 Mobile Web

- Header 展示 Logo、入口型搜索框和右侧搜索图标，样式与位置以最新 UI 为准。
- 搜索框内容和入口交互见第 4 章。
- Header 固定在页面顶部；在不同宽度和语言下，导航元素完整显示并保持可操作。

### 3.2 PC Web

- Header 展示 Logo、导航链接和右侧功能入口；结构与配置规则执行《导航栏配置 PRD v1.3》，元素、顺序和视觉以最新 UI 为准。
- 搜索入口以搜索图标展示，入口交互见第 4 章。
- Favorites 入口点击后进入 Favorites 页。
- Account 入口点击后统一进入 Account Home，由 Account Home 根据登录状态展示登录或账户内容。
- 语言入口展示当前语言，点击后切换 Web 支持的 locale。
- 导航链接展示后台已生效内容，最多 8 个并按配置顺序排列；品类链接进入对应品类的 Collection 页。
- Header 在小屏 PC 宽度下执行最新 UI 的响应式规则，所有核心入口保持可见和可操作。

## 4. 首页搜索入口

首页只定义来源为 Home 时的入口行为：

- Mobile Web 搜索框的轮播词与全局搜索的 Popular searches 共用同一份最终列表和顺序。
- 有可用缓存时首屏直接展示轮播词；无缓存、加载中、空数据、失败或当前词不可用时展示固定 placeholder：`Search by brand or item`。加载成功后从第一条有效词开始轮播。

| 端 | 当前状态 | 用户操作 | 结果 |
|---|---|---|---|
| Mobile Web | 有有效轮播词 | 点击搜索图标 | 直接提交当前轮播词 |
| Mobile Web | 固定 placeholder | 点击搜索图标 | 进入全屏搜索发现页 |
| Mobile Web | 任意入口词状态 | 点击搜索框 | 进入全屏搜索发现页 |
| PC Web | 默认 Header | 点击搜索图标 | Header 切换为搜索态并展示搜索发现层 |

搜索入口产生的查询、Recent searches 和 Search event 按 Web 全局搜索 PRD 统一处理。

## 5. 首页 Banner

### 5.1 数据与展示

- Banner 读取 CMS `home_banner` 资源位，按当前 Web 端和 locale 展示已生效内容，最多 4 条。
- Mobile Web 与 PC Web 使用各自配置的图片、文案和落地目标。
- 多条内容以轮播方式展示，分页指示器、切换控件、自动轮播和文本排版以最新 UI 为准。
- Banner 图片在当前断点内完整适配容器并限制在页面宽度内；具体裁切比例和文本安全区执行最新 UI。

### 5.2 交互

- Banner 整张图片区域均可点击，点击后进入 CMS 配置的目标页；CTA 与图片使用同一跳转目标。
- 轮播切换控件使用最新 UI 规定的点击热区，用户无需精确点击图标笔画。

### 5.3 状态

| 状态 | 展示 |
|---|---|
| 加载中 | 使用与 Banner 容器一致的占位状态 |
| 无生效配置 | 页面后续模块上移 |
| 图片失败 | 展示 CMS 文案和 CTA 的可读兜底背景 |
| 视频失败 | 使用对应封面图；封面图失败时使用图片失败状态 |

## 6. 信任内容与服务承诺

### 6.1 信任模块

- 模块标题和条目内容按当前 locale 展示，模块结构与响应式布局以最新 UI 为准。
- 图片、标题和说明在 PC 小屏及 Mobile Web 下保持在各自容器内，文本按 UI 规则换行。

### 6.2 服务承诺

首页展示 Easy Returns、Free Shipping 和 Customer Support 三项服务承诺，文案使用第 2.2 节定义的当前 locale 版本。图标与文案作为整体在各端完整显示并对齐。

## 7. Curated Collections

### 7.1 数据

- 读取 CMS `home_collection` 资源位中当前端、当前 locale 的已生效内容，按返回顺序展示，最多 8 个。
- 每项包含 Collection ID、封面图、标题、副标题及可选 CTA 文案。
- PC 配置图片尺寸为 616 × 816；Mobile Web 配置图片尺寸为 450 × 596。
- CTA 文案有值时展示按钮；CTA 文案为空时卡片按无按钮样式展示。

### 7.2 展示与交互

- PC Web 首屏展示 4 个；超过 4 个时展示左右切换箭头，点击箭头切换后续内容。
- Mobile Web 以横向滑动作为内容切换方式。
- 点击卡片进入对应 Collection 页。

### 7.3 状态

| 状态 | 展示 |
|---|---|
| 无生效内容 | 后续模块上移 |
| 单张图片失败 | 该卡片使用图片兜底样式，其他卡片继续展示 |
| 模块请求失败 | 仅该模块进入失败降级，其他首页模块继续展示 |

## 8. Explore Finds

### 8.1 Feed Tab

- 按固定顺序展示 `For You`、`New Arrivals`、`Best Sellers`、`Deals` 四个 Tab；本地化名称使用当前 locale。
- 每个 Tab 使用稳定的 `tab_key` 标识，不以翻译文案或显示位置识别 Tab。
- 点击 Tab 后切换到目标 Tab 的加载或缓存状态，并仅渲染目标 Tab 对应的数据。
- 切换 locale 或 PC / Mobile Web 断点时，通过 `tab_key` 保留当前 Tab。例如西班牙语 `Novedades` 对应 `new_arrivals`，切换端后仍保持 New Arrivals。
- Feed Tab 行滚动至 Header 下方时固定在 Header 下方；滚动回 Feed 区域上方后恢复原位置。
- 各 Tab 的召回、排序和空态数据来源执行首页 Feed 规则；首页 PRD 只定义展示与交互。
- `For You` 支持被其他页面复用；搜索关键词无结果页以 `You May Also Like` 为模块标题，复用相同的推荐数据、顺序、商品卡、加载和状态规则。

### 8.2 商品卡与收藏

- 商品卡展示主图、品牌、商品标题、当前销售价和收藏入口；字段、图片比例、网格列数和视觉样式以最新 UI 及全站商品卡规范为准。
- 商品主图读取 `listing.og_image_url`，缺失时读取 `product_image.main_image_url`；商品标题读取 `listing.listing_title`，缺失时读取 `product.title`。
- 当前销售价读取 `listing.listing_price`。当有效 `standard_sku.market_price` 高于 `listing.listing_price` 时，同时展示划线参考价和 Save 差额，差额为两者之差；货币转换与格式化执行全站商品价格规则。
- 商品图片始终限制在卡片和页面内容区域内；调整窗口宽度或切换端时重新排版并保留已返回商品。
- 收藏按钮位于商品图片容器内，完整点击热区包含在商品卡内。
- 点击收藏按钮执行全站 Wishlist 规则并即时更新状态，请求失败时恢复操作前状态；点击商品卡其他区域进入商品详情页。

### 8.3 加载、追加与空态

| 状态 | 展示与处理 |
|---|---|
| 首次加载 | 展示与商品卡布局一致的骨架屏 |
| 成功有数据 | 用真实商品卡替换骨架屏 |
| 成功无数据 | 展示当前 Tab 的空态 |
| 请求失败 | 展示当前 Tab 的失败状态和重试入口 |
| PC 点击 View More | 在列表末尾连续追加下一批商品，并按网格顺序从左到右紧密排列 |
| Mobile Web 触底 | 继续加载下一批商品；加载期间在列表底部展示加载状态 |
| 全部加载完成 | 结束追加加载并展示完成状态 |

- 切换 Tab 后，当前列表、Loading、空态和失败状态与当前 `tab_key` 对应。

### 8.4 返回与状态恢复

- 首页下游页面返回行为见第 11 章。
- Mobile Web 在 Explore Finds 列表底部展示回到顶部入口，点击后返回首页顶部。

## 9. Mobile Web 底部导航

- 展示 Home、Shop、Favorites、Account 四个入口，首页中 Home 为激活态。
- 图标、标签和激活样式以最新 UI 为准；标签读取当前 locale。
- 从 Mobile Web 切换为 PC Web 时：当前位于 Shop 则进入 PC 首页；当前位于 Favorites 则进入 Account Home。

## 10. PC Footer

### 10.1 全站 Footer

- PC Web 首页挂载全站 Footer；栏目、链接目标和登录态行为执行《Footer PRD v0.3》，视觉以最新 UI 为准。

### 10.2 Stay in the Loop

- 用户提交有效邮箱并订阅成功后，在当前区域展示成功图标和 `You’re in the loop!`。
- 邮件订阅服务返回校验、重复订阅、成功或失败结果，首页按当前 UI 展示对应状态。

## 11. 跨端、响应式与浏览器行为

- PC 页面缩放或窗口宽度变化后，商品网格按当前断点重新排版；已经返回的商品完整保留。
- Header、Banner、Collections、商品卡、服务承诺和 Footer 在支持的 PC 宽度及 Mobile Web 下均限制在页面内容宽度内。
- locale 切换、端切换及从下游页面返回均使用稳定业务标识恢复状态。
- 从 Banner 目标页、Collection 页或商品详情页返回首页时，恢复离开前的滚动位置、Feed Tab、已加载商品、分页位置和 Collection 位置。
- 恢复完成后展示已保存内容或当前请求的明确终态，页面保持可操作。
- PC Web 文档标题使用 `Authenticated Luxury Resale｜Looply`；站点地址展示为 `looply.com`。

## 12. 登录状态差异

| 功能 | 未登录 | 已登录 |
|---|---|---|
| 浏览首页内容 | 正常展示 | 正常展示 |
| 商品收藏 | 执行全站 Wishlist 未登录规则 | 更新账户 Wishlist |
| Account 入口 | 进入 Account Home 并展示登录内容 | 进入 Account Home 并展示账户内容 |
| 语言选择 | 浏览器保存 | 账号保存 |
| Shipping / Returns | 登录后继续目标路径 | 直接进入目标模块 |

## 13. 数据与依赖

| 依赖 | 首页使用内容 |
|---|---|
| CMS 首页配置 v1.3 | Banner、Curated Collections 及 locale 文案 |
| 导航栏配置 v1.3 | PC Header 导航结构、顺序和目标 |
| Web 全局搜索 v0.3 | 首页搜索轮播词、入口提交和完整搜索能力 |
| Feed / 推荐 v2.3 | 四个 Feed Tab 的商品列表与分页状态 |
| 商品与 Wishlist | 商品卡数据、收藏状态和收藏操作 |
| 用户系统 | Account 登录状态、语言选择 |
| Collection | Collection 落地页及返回恢复 |
| Footer v0.3 | PC Footer 栏目、链接目标和登录态行为 |
| 邮件订阅服务 | Stay in the Loop 的邮箱校验、订阅结果和错误状态 |

## 14. 关键埋点

| 事件 | 关键参数 |
|---|---|
| 首页访问 | `market_id`, `locale`, `terminal` |
| 首页搜索入口点击 | `terminal`, `entry_action`, `placeholder_type`, `query` |
| Banner 曝光 / 点击 | `banner_id`, `position`, `target` |
| Collection 点击 | `collection_id`, `position` |
| Feed Tab 切换 | `from_tab_key`, `to_tab_key` |
| View More / 触底加载 | `tab_key`, `page`, `result_count` |
| 商品点击 | `listing_id`, `tab_key`, `position` |
| 收藏操作 | `listing_id`, `action`, `logged_in` |
| 语言切换 | `from_locale`, `to_locale` |

Feed 和搜索事件分别以对应模块 PRD 为唯一事件规则来源。

## 15. 版本规划

- v1.7 当前范围为本 PRD 已定义的 Mobile Web 与 PC Web 首页能力。
- 后续新增能力在明确版本范围后进入新版本 PRD，不在当前正文预留候选方案。

## 16. 设计与关联文档

| 范围 | 端 | 当前基线 |
|---|---|---|
| 首页全页 | Mobile Web | [Looply v1.0 · Mobile 首页](https://www.figma.com/design/rLK7XCdVvYqEHQHd7WjOkk/Looply-v1.0?node-id=341-885)；画布标记 2026-07-13 样式更新 |
| 首页全页 | PC Web | [Looply v1.0 · PC 首页](https://www.figma.com/design/rLK7XCdVvYqEHQHd7WjOkk/Looply-v1.0?node-id=1474-30799)；画布标记 2026-07-16 样式更新、Ready for dev |
| 搜索 | Mobile Web | [Looply v1.0 · Mobile 搜索](https://www.figma.com/design/rLK7XCdVvYqEHQHd7WjOkk/Looply-v1.0?node-id=5477-27518&m=dev) |
| 搜索 | PC Web | [Looply v1.0 · PC 搜索](https://www.figma.com/design/rLK7XCdVvYqEHQHd7WjOkk/Looply-v1.0?node-id=5477-28904&m=dev) |
| 搜索产品规则 | Mobile Web + PC Web | `looply-Web全局搜索-PRD-v0.3.md` |
| 验收问题来源 | 首页 Tab | [looply 验收问题汇总](https://zhuanspirit.feishu.cn/wiki/ERFRwynp2ik67nkRXqzcrepqn8D?from=from_copylink&sheet=keROil)，仅采用提出人为“柏雪”的有效产品结论 |

---

*文档维护：Looply 产品团队 | 首页 PRD v1.7 | 2026-08-11*
