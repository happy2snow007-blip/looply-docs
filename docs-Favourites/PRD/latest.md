# Looply Favorites PRD

> 文档版本：v2.9  
> 文档状态：产品确认稿，不代表已开发、上线或验收  
> 日期：2026-07-20  
> 适用范围：Favorites Overview 聚合展示页  
> 原型：`prototypes/favorites/looply-favorites-prototype-v9.html`

## 一、概述

### 1.1 背景与目标

Favorites 面向处于购买考虑阶段的用户，聚合展示 Wishlist、Recently Viewed 和条件出现的 Recommended for You，帮助用户找回商品、感知可购买商品降价，并继续发现商品。

本期只负责 Favorites Overview 的展示、交互、异常降级、页面跳转和与公共能力的衔接；不重定义收藏、浏览历史、Price Drop 或推荐算法。

### 1.2 范围边界

本期不负责 Wishlist 完整页、完整浏览历史页、收藏与浏览记录的收录与去重、匿名标识生命周期、Price Drop 识别与统计、推荐算法、Home / Search / Cart / 商品详情的内部逻辑，以及数据平台最终事件实现。

### 1.3 用户与身份

| 用户 | 页面规则 |
|---|---|
| 未登录买家 | 可直接进入，展示当前 `anonymous_id` 对应的 Wishlist、Recently Viewed 和推荐结果。 |
| 已登录买家 | 可直接进入，展示当前 `user_id` 对应数据并执行商品查看和 Wishlist 操作。 |

Favorites 不做必须登录硬拦截，也不自行判断、合并或迁移匿名数据。登录、注册、退出或匿名主体变化后，按统一身份模块返回的当前主体重新获取结果；旧主体或迟到请求不得覆盖当前页面。

### 1.4 页面流转

```text
Favorites → Search
Favorites → Cart
Favorites → Wishlist 完整页（All / Price Drop）
Favorites → 完整浏览历史（All / Price Drop）
Favorites → Home · Explore Finds · For You
Favorites → 商品详情 → 返回 Favorites
```

从商品详情等子页面返回时，恢复页面纵向位置、Wishlist 与 Recently Viewed 横向位置，以及 Recommend 已加载内容和位置；若发生刷新，不得无故清空可用内容或跳回顶部。

### 1.5 多语言与市场策略

- 当前美国范围支持英语 `en-US` 与西班牙语 `es-US`；所有固定 UI 文案使用 i18n message package。
- 商品标题、品牌、成色、浏览时间和价格使用上游返回的最终本地化展示值；Favorites 不自行翻译、拼接或换算。
- Price Drop 使用稳定 i18n key 和复数规则，不通过字符串拼接 `item/items`。
- 价格、币种和金额不翻译；使用全局商品卡价格组件。
- 商品动态字段复用商品域既有翻译资源；稳定 `resourceType`、字段名和译文缺失兜底由商品与多语言模块在开发前确认。Favorites 不新建近似资源卡片。

静态 UI 文案使用以下稳定 key。下表为产品交付基线；正式上线前仍需按统一多语言流程完成语言审校。

| i18n key | 使用位置 | `en-US` | `es-US` | 变量 / 规则 |
|---|---|---|---|---|
| `favorites.title` | 页面标题 | Favorites | Favoritos | 无 |
| `favorites.wishlist.title` | Wishlist 模块标题 | Wishlist | Lista de deseos | 无 |
| `favorites.recently_viewed.title` | Recently Viewed 模块标题 | Recently Viewed | Vistos recientemente | 无 |
| `favorites.recommended.title` | 推荐模块标题 | Recommended for You | Recomendado para ti | 无 |
| `common.view_all` | 标题及末尾入口 | View all | Ver todo | 优先复用公共 key |
| `common.retry` | 模块与加载更多重试 | Retry | Reintentar | 优先复用公共 key |
| `favorites.explore` | 空态入口 | Explore | Explorar | 无 |
| `favorites.add_more` | Wishlist 少量商品引导 | Add more | Añadir más | 无 |
| `favorites.add_more.subtitle` | Wishlist 引导副文案 | Explore more finds | Explora más opciones | 无 |
| `favorites.explore_more` | Recently Viewed 单商品引导 | Explore more | Explorar más | 无 |
| `favorites.explore_more.subtitle` | Recently Viewed 引导副文案 | Discover more finds | Descubre más opciones | 无 |
| `favorites.wishlist.empty` | Wishlist 空态 | Your wishlist is empty | Tu lista de deseos está vacía | 无 |
| `favorites.recently_viewed.empty` | Recently Viewed 空态 | No recently viewed items yet | Aún no has visto ningún artículo | 无 |
| `favorites.wishlist.load_error` | Wishlist 首次失败 | Couldn't load your wishlist | No se pudo cargar tu lista de deseos | 无 |
| `favorites.recently_viewed.load_error` | Recently Viewed 首次失败 | Couldn't load recently viewed items | No se pudieron cargar los artículos vistos recientemente | 无 |
| `favorites.wishlist.refresh_error` | Wishlist 缓存刷新失败 | Couldn’t refresh your wishlist | No se pudo actualizar tu lista de deseos | 无 |
| `favorites.recently_viewed.refresh_error` | Recently Viewed 缓存刷新失败 | Couldn’t refresh recently viewed items | No se pudieron actualizar los artículos vistos recientemente | 无 |
| `favorites.wishlist.update_error` | 心形写入失败 Toast | Couldn’t update Wishlist. Try again. | No se pudo actualizar la lista de deseos. Inténtalo de nuevo. | 无 |
| `favorites.price_drop` | Price Drop 提示条 | 1 item dropped in price / {count} items dropped in price | 1 artículo bajó de precio / {count} artículos bajaron de precio | 使用 ICU 复数规则；`count > 0` |


## 二、页面框架与刷新

### 2.1 页面框架

| 元素 | 规则 |
|---|---|
| 标题 | `Favorites` |
| Search | 进入平台统一 Search，不搜索当前 Wishlist 或浏览记录。 |
| Cart | 进入 Cart。 |
| 模块顺序 | Wishlist → Recently Viewed → Recommended for You（条件出现）。 |
| 底部导航 | `Home / Shop / Favorites / Me`，Favorites 为选中态。 |

### 2.2 刷新与缓存

Favorites 的首次进入、重新进入、从子页面返回、回到前台和缓存有效期，遵循 App 统一页面刷新策略；Favorites 不单独设置轮询、刷新频率或过期阈值。

当 App 策略触发刷新，或用户在 Favorites 主动下拉刷新时：

1. Wishlist、Recently Viewed、Recommended for You 并行请求，彼此不阻塞；
2. 每个模块成功后独立更新，不等待其他模块；
3. 有可用缓存时，保留当前内容和位置，不用 Loading、空白或骨架覆盖；
4. Recommended for You 空结果或不满足展示条件时静默隐藏，不视为页面加载失败；
5. Recommended for You 已有缓存 Feed 时刷新失败，保留当前 Feed 并静默处理，不显示模块错误、Toast 或末尾 Retry；等待下次页面统一刷新再尝试更新；
6. Wishlist 或 Recently Viewed 刷新失败且有缓存时，保留该模块的商品卡、数量、Price Drop 和横向位置；在**对应模块标题下方**显示轻量行内提示与 `Retry`，不使用页面顶部浮层；
7. Wishlist 提示为 `Couldn’t refresh your wishlist`，Recently Viewed 提示为 `Couldn’t refresh recently viewed items`；点击 `Retry` 只重新请求当前失败模块，不影响其他模块；
8. 三个模块均刷新失败但仍有任一缓存内容时，保留旧内容；只有三者均无可用内容时才进入 App 统一整页错误态；
9. 下拉刷新属于页面级刷新，默认并行请求三个模块；模块级 Retry 仅重试对应失败模块。

两个模块的刷新失败提示使用相同结构、信息密度、错误层级与 Retry 交互；固定文案进入 `en-US` / `es-US` 的 UI message package。App 页面容器仍负责刷新触发、缓存有效期和回到前台策略；Favorites 负责模块内可见降级与模块级 Retry。

### 2.3 关联完整列表页加载基线

本节仅统一从 Favorites Overview 跳转到 Wishlist 完整页和完整浏览历史页后的公共列表加载规则，不扩展 Favorites Overview 的其他职责：

- 移动端完整列表页使用上滑无限滚动，每页最多加载 40 个商品。
- 移动端无更多数据时使用系统原生 overscroll 回弹。
- PC 端完整列表页使用 `View More` 加载，每次追加 40 个商品；全部数据加载完成后，`View More` 按钮消失。

## 三、模块详细规则

### 3.1 Wishlist

Wishlist 使用上游提供的真实总数、有序列表和收藏状态。预览按最近收藏优先横向展示，最多 30 件；Sold Out 仍计入 Wishlist 总数并保留上游顺序。

| 上游总数 | 标题 View all | 列表末尾 | 展示规则 |
|---|---|---|---|
| 0 | 隐藏 | `Explore` | 轻量空态，进入 Home · Explore Finds · For You。 |
| 1–2 | 隐藏 | `Add more` | 展示现有商品，进入 Home · Explore Finds · For You。 |
| 3–30 | 展示 | `View all` | 展示全部预览商品。 |
| 大于 30 | 展示 | 第 30 件后 `View all` | 只预览最近 30 件。 |

商品卡展示商品图、品牌、名称、可选成色、价格、可选原价 / 降价、Wishlist 心形和 Sold Out 状态。卡片主体进入商品详情；心形只执行 Wishlist 操作，不得触发商品跳转。

取消收藏时，实心心形立即变空心，但当前卡片、顺序、数量与入口阈值不立即变化；刷新前再次点击可恢复收藏。下次权威刷新、重新进入或取得新 Wishlist 结果后，未收藏商品才移除。

| 商品状态 | 当前 Wishlist 状态 | 心形规则 |
|---|---|---|
| 在售 | 未收藏 | 空心，可加入。 |
| 在售 | 已收藏 | 实心，可移出。 |
| Sold Out | 未收藏 | 展示置灰空心，禁用点击，不允许新加入。 |
| Sold Out | 已收藏 | 保留实心且可操作，可移出。 |

本期只消费商品系统返回的在售或 Sold Out 状态，不新增“已失效”商品状态。Sold Out 卡使用整卡灰色蒙版，但不得阻断已收藏商品的移出操作；商品从在售变为 Sold Out 后不自动移出 Wishlist。

Price Drop 完全使用 Wishlist 上游返回的“可购买 Price Drop 总数”，不得从预览数组、分页或当前卡片自行计算；上游负责排除 Sold Out。`N > 0` 显示提示条，`N = 0` 或数量失败时隐藏；文案使用 `1 item dropped in price` / `{N} items dropped in price` 的 i18n 复数规则。点击提示条进入 Wishlist 完整页并定位 Price Drop Tab。

`View all` 进入 Wishlist 完整页 All Tab，不属于 Favorites 内加载更多；目标页加载失败由 Wishlist 完整页处理。

### 3.2 Recently Viewed

Recently Viewed 使用浏览历史上游返回的顺序、真实总数、商品字段和本地化浏览时间；不二次排序或去重，横向最多预览 30 件。浏览时间未返回时隐藏，不由 Favorites 计算或格式化。

| 上游总数 | 标题 View all | 列表末尾 | 展示规则 |
|---|---|---|---|
| 0 | 隐藏 | `Explore` | 轻量空态，进入 Home · Explore Finds · For You。 |
| 1 | 展示 | `Explore more` | 展示 1 件商品和引导卡。 |
| 2–3 | 展示 | 隐藏 | 展示现有商品。 |
| 4–30 | 展示 | `View all` | 展示全部预览商品。 |
| 大于 30 | 展示 | 第 30 件后 `View all` | 只预览前 30 件。 |

商品卡展示商品图、品牌、名称、可选成色、价格、可选浏览时间、可选降价、Wishlist 心形与 Sold Out；不展示无操作含义的时钟图标。卡片主体进入商品详情；心形仅切换 Wishlist，不得触发商品跳转。加入或移出 Wishlist 后，浏览记录卡保持原位置，不从 Recently Viewed 移除；Wishlist 概览在下一次权威刷新中再更新。

Recently Viewed 的 Sold Out 心形规则、Price Drop 上游数量规则、Loading、首次失败、缓存刷新失败和全售罄视觉层级与 Wishlist 一致。Price Drop 点击进入完整浏览历史页并定位 Price Drop Tab；`View all` 进入完整浏览历史 All Tab，不属于 Favorites 内加载更多。

### 3.3 Recommended for You

Recommended for You 仅在推荐上游基于当前登录或匿名主体返回非空个性化结果时出现。行为数据不足、空结果或首次请求失败时静默隐藏；不使用 Home 通用推荐流补足，也不展示 `Based on your activity` 等副标题。

推荐上游必须只返回可购买商品，Sold Out 在上游过滤。Favorites 不为 Recommend 定义 Sold Out 卡片、蒙版或 Sold Out 心形分支。

推荐使用双列商品 Feed。卡片主体进入商品详情；心形支持加入或移出 Wishlist，写入失败时恢复点击前状态，写入中不可重复点击，卡片位置不变化。加载更多失败时保留已有商品，并在 Feed 末尾提供轻量 Retry。

### 3.4 Heart 写入失败的统一规则

Wishlist、Recently Viewed 与 Recommended for You 的心形均采用同一业务规则。同一页面中，相同 `listing_id` 共用 Wishlist 状态：任一商品卡发起收藏或取消收藏后，所有同商品心形先乐观切换；同一商品写入中不可重复点击；写入失败时所有同商品心形统一恢复点击前状态。心形状态实时联动，但商品卡增删、模块数量、排序、Price Drop 入口及其他模块结构只在权威刷新后更新。

回滚完成后，展示轻量 Toast：`Couldn’t update Wishlist. Try again.`。该 Toast 仅用于失败；不展示取消收藏成功 Toast。三个模块共用同一提示和 i18n key。普通写入失败不得误触发登录流程；会话失效才遵循登录注册模块的统一恢复规则。

## 四、状态、异常与组合场景

Wishlist 与 Recently Viewed 的同类状态使用一致的视觉层级：

| 状态 | 展示规则 |
|---|---|
| 首次 Loading | 保留图标与静态标题，隐藏数量、View all 和 Price Drop；展示 3 张同结构商品卡骨架，仅保留读屏可识别的隐藏 Loading 文案。 |
| 正常 | 展示上游真实数量、商品与入口。 |
| 空态 | 轻量空态与对应 Home 引导；隐藏数量占位、View all 和 Price Drop。 |
| 首次失败 | 轻量行内错误与模块 Retry；不伪装为空态。 |
| 刷新中 | 保留当前可用内容和位置。 |
| 有缓存的刷新失败 | 保留旧内容和位置；在当前模块标题下显示轻量提示与 Retry；仅重试当前模块。 |
| 全部售罄 | 商品卡整卡灰化；按真实总数保留 View all；Price Drop 由上游可购买数量决定，通常为 0。 |

| 页面场景 | 页面表现 | Retry 范围 |
|---|---|---|
| Wishlist 单独失败 | Wishlist 模块级错误，其他内容保持。 | 仅 Wishlist。 |
| Recently Viewed 单独失败 | Recently Viewed 模块级错误，其他内容保持。 | 仅 Recently Viewed。 |
| Wishlist 与 Recently Viewed 同时失败、Recommend 可用 | 两个核心模块分别显示模块级错误，Recommend 正常展示。 | 各失败模块独立重试。 |
| Recommend 首次失败 | 静默隐藏 Recommend。 | 无首屏 Retry。 |
| Recommend 有缓存时刷新失败 | 保留当前 Feed 并静默处理，不显示错误、Toast 或 Retry。 | 等待下次页面统一刷新。 |
| 三个模块均无可用内容且失败 | 内容区域使用 App 统一整页错误组件。 | 重新请求本页业务数据。 |
| 页面容器或关键公共依赖不可用 | 使用 App 全局整页错误规则。 | 由全局组件负责。 |

“Wishlist 与 Recently Viewed 同时失败”与“全部数据失败”是页面组合场景，不属于 Recently Viewed 的单模块状态。只要任一模块仍有可用内容，不得使用整页错误覆盖。

## 五、依赖、数据与验收

### 5.1 依赖与风险

| 依赖 | Favorites 的关键要求 |
|---|---|
| Wishlist / 收藏与浏览历史 | 当前主体的有序预览、真实总数、收藏状态、Wishlist 写入、可购买 Price Drop 总数和完整页定位。 |
| 浏览历史 | 当前主体的有序预览、真实总数、本地化浏览时间、收藏状态、可购买 Price Drop 总数和完整页定位。 |
| 推荐 | 当前主体的非空个性化结果；只返回可购买商品。 |
| 商品系统 | 最终本地化商品字段、价格与币种、成色、在售 / Sold Out 状态与商品详情目标。 |
| App 页面容器 | 统一刷新策略、缓存、位置恢复与整页错误组件。 |
| 统一身份 / 登录注册 | 当前主体、登录复制完成信号、会话恢复和退出结果。 |
| Home / Search / Cart / 商品详情 | 统一目标页、目标区域定位和返回恢复。 |

开发前需与 App 页面容器确认统一刷新触发时机、缓存有效期和回到前台规则；与推荐上游确认 Sold Out 已过滤；与 Wishlist / 浏览历史确认模块 Retry 和权威刷新结果契约，以及 Wishlist 写入结果契约。

### 5.2 数据与埋点

数据平台仍在建设中，本期仅明确业务分析需求，不锁定最终事件名、公共属性、曝光判定与去重实现。

| 采集内容 | 主要业务属性 |
|---|---|
| Favorites 页面访问与加载结果 | 入口来源、结果、耗时、是否使用缓存。 |
| 模块加载与有效曝光 | 模块、结果、数量区间、耗时。 |
| 商品有效曝光与点击 | 模块、`listing_id`、位置、是否 Price Drop。 |
| 入口点击 | 模块、动作、入口位置、目标页。 |
| Price Drop 提示条曝光与点击 | 模块、上游数量区间。 |
| Wishlist 操作结果 | 模块、`listing_id`、目标状态、结果。 |
| Retry 与恢复结果 | 错误层级、模块、重试结果、是否有缓存。 |

Favorites 不采集商品标题、浏览时间文案、完整商品列表、原始 `user_id` 或原始 `anonymous_id`。已有全局事件优先复用，并补充 `source_page=favorites`、`source_module` 和位置来源。

### 5.3 验收标准

1. 登录和未登录用户均可进入 Favorites，并只展示当前主体结果。
2. Wishlist、Recently Viewed、Recommend 的顺序、30 件预览上限、数量阈值与跳转入口符合本 PRD。
3. 商品卡进入商品详情；心形点击不穿透到商品详情。
4. Wishlist 与 Recently Viewed 符合四种在售 / Sold Out 心形规则；Sold Out 未收藏展示置灰空心且禁用点击，已收藏仍可取消；Recommend 不展示 Sold Out 商品。
5. Price Drop 数量完全使用各自上游可购买总数，数量为 0 或失败时隐藏，单复数文案正确。
6. Wishlist 与 Recently Viewed 的 Loading、首次失败、缓存刷新失败、Retry 和全售罄状态保持一致。
7. 下拉刷新并行请求三个模块；部分失败不影响成功模块；全部无缓存且失败才进入整页错误。
8. Wishlist 与 Recently Viewed 有缓存的刷新失败保留旧内容，在当前模块标题下显示行内提示，并仅重试失败模块；Recommended 有缓存时刷新失败保留 Feed 并静默处理。
9. 同一页面相同 `listing_id` 的心形实时联动；写入失败时所有同商品心形统一回滚、不改变卡片位置，并展示 `Couldn’t update Wishlist. Try again.`；写入中不可重复点击。
10. Wishlist 与 Recently Viewed 同时失败但 Recommend 可用时继续展示 Recommend；该场景不归入 Recently Viewed 单模块状态。
11. 静态 UI 文案使用本 PRD 定义的稳定 key、`en-US` / `es-US` 值及复数规则；动态商品内容和浏览时间直接消费上游本地化结果。

## 六、版本规划

当前 MVP 仅交付 Favorites Overview 的聚合展示与本 PRD 所列交互；完整页、收藏/浏览收录去重、身份复制、Price Drop 统计、推荐算法与数据平台最终口径由各自上游模块负责。后续迭代如新增独立入口、实体或跨角色流程，再评估是否补充架构图、ER 图或泳道图。

## 七、原型索引

| 场景 | V9 Demo 状态 |
|---|---|
| Wishlist / Recently Viewed 正常、少量、Loading、空、首次失败、Price Drop、全售罄 | 各模块对应状态选择器。 |
| 缓存刷新失败 | `Wishlist · Refresh failed (global UI)` / `Recently · Refresh failed (global UI)`；保留内容并在模块标题下显示提示。 |
| 心形写入失败 | 三个模块的 `Heart failed (global UI)`；任意可操作心形均乐观切换后回滚并显示轻量 Toast。 |
| 两个核心模块同时失败、Recommend 可用 | `Page · Wishlist + Recently failed`。 |
| 所有业务数据不可用 | `Page · All data failed`。 |
| Recommend 无数据、首次失败、加载更多失败 | Recommend 对应状态选择器。 |

本版不新增接口清单、实体关系图、产品架构图或泳道图；本页面仅聚合既有上游结果。
