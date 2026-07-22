# Looply Favorites PRD

> 文档版本：v2.11
> 文档状态：产品确认稿，不代表已开发、上线或验收
> 日期：2026-07-22
> 适用范围：App / H5 Mobile · Favorites Overview 聚合展示页
> 原型：`prototypes/favorites/looply-favorites-prototype-v9.html`

## 一、概述

### 1.1 背景与目标

Favorites 面向处于购买考虑阶段的用户，聚合展示 Wishlist、Recently Viewed 和条件出现的 Recommended for You，帮助用户找回商品、感知可购买商品降价，并继续发现商品。

本期只负责 Favorites Overview 的展示、交互、异常降级、页面跳转和与公共能力的衔接；不重定义收藏、浏览历史、Price Drop 或推荐算法。

### 1.2 范围边界

本期仅支持 App 与 H5 Mobile。H5 Mobile 沿用 App 的移动端页面结构与交互体验；PC Web 不在本期范围。

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
| `favorites.recently_viewed.remove` | 删除单条浏览记录的无障碍名称 | Remove from recently viewed | Eliminar de vistos recientemente | 不显示可见文案 |
| `favorites.recently_viewed.remove_error` | 删除浏览记录失败 Toast | Couldn’t remove this item. Try again. | No se pudo eliminar este artículo. Inténtalo de nuevo. | 无 |
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

1. Wishlist、Recently Viewed、Recommended for You 并行请求，各模块成功后独立更新；
2. 有可用缓存时，刷新期间保留当前内容和位置；
3. 下拉刷新请求三个模块；模块级 `Retry` 仅重试对应模块；
4. 各模块的刷新失败、缓存保留和 Retry 规则见第四章。

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
| Sold Out | 未收藏 | 展示置灰空心，禁用点击。 |
| Sold Out | 已收藏 | 保留实心且可操作，可移出。 |

商品支持在售和 Sold Out 两种展示状态。Sold Out 卡整卡灰化；已收藏商品保留可操作的实心心形。商品从在售变为 Sold Out 后仍保留在 Wishlist。

Price Drop 完全使用 Wishlist 上游返回的“可购买 Price Drop 总数”，不得从预览数组、分页或当前卡片自行计算；上游负责排除 Sold Out。`N > 0` 显示提示条，`N = 0` 或数量失败时隐藏；文案使用 `1 item dropped in price` / `{N} items dropped in price` 的 i18n 复数规则。点击提示条进入 Wishlist 完整页并定位 Price Drop Tab。

`View all` 进入 Wishlist 完整页 All Tab。

### 3.2 Recently Viewed

Recently Viewed 直接展示浏览历史上游返回的顺序、真实总数、商品字段和本地化浏览时间，横向最多预览 30 件；浏览时间缺失时隐藏。

| 上游总数 | 标题 View all | 列表末尾 | 展示规则 |
|---|---|---|---|
| 0 | 隐藏 | `Explore` | 轻量空态，进入 Home · Explore Finds · For You。 |
| 1 | 展示 | `Explore more` | 展示 1 件商品和引导卡。 |
| 2–3 | 展示 | 隐藏 | 展示现有商品。 |
| 4–30 | 展示 | `View all` | 展示全部预览商品。 |
| 大于 30 | 展示 | 第 30 件后 `View all` | 只预览前 30 件。 |

商品卡展示商品图、品牌、名称、可选成色、价格、可选浏览时间、可选降价、删除入口与 Sold Out，不展示 Wishlist 心形。卡片主体进入商品详情；点击右上角删除入口只删除当前浏览记录，不得触发商品跳转。

单条删除与完整浏览记录页保持一致：操作后立即从当前预览移除卡片。删除成功后，使用浏览历史上游的最新结果同步更新 Recently Viewed 总数、Price Drop 数量及对应入口；若 Price Drop 数量变为 0，在卡片完成删除收起后，通过高度与透明度过渡平滑收起提示条，动效参数遵循 App 全局 UI 规范，减少动态效果开启时使用全局默认处理。删除失败时恢复原卡片、总数、Price Drop 数量及相关入口，并展示轻量 Toast：`Couldn’t remove this item. Try again.`。Sold Out 浏览记录同样允许删除。

Recently Viewed 与 Wishlist 的加载和异常反馈保持一致，具体按第四章的公共状态规则执行；Price Drop 上游数量和全售罄视觉层级同样保持一致。Price Drop 点击进入完整浏览历史页并定位 Price Drop Tab；`View all` 进入完整浏览历史 All Tab。

### 3.3 Recommended for You

Recommended for You 基于当前登录或匿名主体的 Wishlist、加购、购买和商品点击浏览行为生成个性化结果。推荐侧负责行为判断、召回和结果过滤；Favorites 前端不自行计算推荐资格。

当缺少 Wishlist、加购和购买行为，只有商品点击浏览行为时，由推荐侧通过分段函数判断是否返回推荐结果。分段函数及其阈值由推荐侧维护。

购买行为可作为偏好信号，但推荐侧识别为已购买的同一 `listing_id` 不进入推荐结果。哪些订单状态计入购买信号由推荐侧定义。

推荐结果只包含可购买商品，并排除当前页面 Wishlist 或 Recently Viewed 已展示的同 `listing_id` 商品。过滤后返回至少 1 件商品时展示模块；行为条件不满足、结果为空或首次请求失败时静默隐藏。

推荐使用双列商品 Feed。卡片主体进入商品详情；心形支持加入或移出 Wishlist，写入失败时恢复点击前状态，写入中不可重复点击，卡片位置不变化。加载更多失败时保留已有商品，并在 Feed 末尾提供轻量 Retry。

### 3.4 Heart 写入失败的统一规则

同一页面中，所有显示 Wishlist 心形的商品卡按 `listing_id` 共用收藏状态：任一商品卡发起收藏或取消收藏后，其他同商品心形乐观更新；写入中不可重复点击，写入失败时统一回滚。心形状态即时联动，商品卡、模块数量、排序和入口在权威刷新后更新。

回滚完成后展示轻量 Toast：`Couldn’t update Wishlist. Try again.`，Wishlist 与 Recommended for You 共用同一提示和 i18n key。普通写入失败保留当前登录状态；会话失效时使用登录注册模块的统一恢复规则。

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
| Wishlist / 收藏关系 | 当前主体的有序预览、真实总数、收藏状态、Wishlist 写入、可购买 Price Drop 总数和完整页定位。 |
| 浏览历史 | 当前主体的有序预览、真实总数、本地化浏览时间、单条删除、统一的删除成功与失败反馈、可购买 Price Drop 总数和完整页定位。 |
| 推荐 | 基于当前主体的 Wishlist、加购、购买和商品点击浏览行为生成个性化结果；仅有点击浏览行为时使用分段函数判断是否返回。结果只包含可购买商品，并排除已购买及当前页面 Wishlist / Recently Viewed 已展示的同 `listing_id` 商品。购买行为及订单状态口径由推荐侧定义。 |
| 订单 | 为推荐侧提供购买行为及对应 `listing_id`。 |
| 商品系统 | 最终本地化商品字段、价格与币种、成色、在售 / Sold Out 状态与商品详情目标。 |
| App 页面容器 | 统一刷新策略、缓存、位置恢复与整页错误组件。 |
| 统一身份 / 登录注册 | 当前主体、登录复制完成信号、会话恢复和退出结果。 |
| Home / Search / Cart / 商品详情 | 统一目标页、目标区域定位和返回恢复。 |

开发前需与 App 页面容器确认统一刷新触发时机、缓存有效期和回到前台规则；推荐侧需按本 PRD 过滤 Sold Out、已购买同 `listing_id` 及当前页面重复商品；与 Wishlist / 浏览历史确认模块 Retry 和权威刷新结果契约、Wishlist 写入结果，以及单条删除后的浏览历史总数与可购买 Price Drop 总数。

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
| Recently Viewed 删除结果 | `listing_id`、位置、结果。 |
| Retry 与恢复结果 | 错误层级、模块、重试结果、是否有缓存。 |

Favorites 不采集商品标题、浏览时间文案、完整商品列表、原始 `user_id` 或原始 `anonymous_id`。已有全局事件优先复用，并补充 `source_page=favorites`、`source_module` 和位置来源。

### 5.3 验收标准

1. 登录和未登录用户均可进入 Favorites，并只展示当前主体结果。
2. Wishlist、Recently Viewed、Recommend 的顺序、30 件预览上限、数量阈值与跳转入口符合本 PRD。
3. 商品卡进入商品详情；Wishlist 心形和 Recently Viewed 删除入口点击均不穿透到商品详情。
4. Wishlist 符合四种在售 / Sold Out 心形规则；Sold Out 未收藏展示置灰空心且禁用点击，已收藏仍可取消；Recently Viewed 的 Sold Out 记录可删除；Recommend 不展示 Sold Out 商品。
5. Price Drop 数量完全使用各自上游可购买总数，数量为 0 或失败时隐藏，单复数文案正确。
6. Wishlist 与 Recently Viewed 的 Loading、首次失败、缓存刷新失败、Retry 和全售罄状态保持一致。
7. 下拉刷新并行请求三个模块；部分失败不影响成功模块；全部无缓存且失败才进入整页错误。
8. Wishlist 与 Recently Viewed 有缓存的刷新失败保留旧内容，在当前模块标题下显示行内提示，并仅重试失败模块；Recommended 有缓存时刷新失败保留 Feed 并静默处理。
9. 同一页面所有显示 Wishlist 心形的卡片按 `listing_id` 实时联动；写入失败时所有同商品心形统一回滚、不改变卡片位置，并展示 `Couldn’t update Wishlist. Try again.`；写入中不可重复点击。
10. Wishlist 与 Recently Viewed 同时失败但 Recommend 可用时继续展示 Recommend；该场景不归入 Recently Viewed 单模块状态。
11. 静态 UI 文案使用本 PRD 定义的稳定 key、`en-US` / `es-US` 值及复数规则；动态商品内容和浏览时间直接消费上游本地化结果。
12. App 与 H5 Mobile 按同一移动端页面结构和交互方案验收；本期不包含 PC Web 适配。
13. 推荐侧使用当前主体的 Wishlist、加购、购买和商品点击浏览行为；仅有点击浏览行为时由推荐侧使用分段函数判断是否返回。返回非空结果时展示，行为条件不满足、结果为空或首次失败时静默隐藏；Favorites 前端不自行计算推荐资格。
14. Recommended for You 不展示与当前页面 Wishlist 或 Recently Viewed 相同 `listing_id` 的商品；去重后有 1 件商品仍展示，无剩余商品时静默隐藏模块。
15. 推荐侧识别为已购买的同一 `listing_id` 不出现在推荐结果中；购买行为仍可作为其他商品的偏好信号。哪些订单状态计入购买信号由推荐侧定义。
16. Recently Viewed 概览卡不显示 Wishlist 心形；点击删除入口后立即移除卡片。删除成功后同步更新上游返回的 Recently Viewed 总数、Price Drop 数量及对应入口；Price Drop 变为 0 时，在卡片删除收起后平滑收起提示条，不发生突兀跳变；失败时恢复卡片、两类数量与相关入口，并展示 `Couldn’t remove this item. Try again.`；Sold Out 记录同样可删除。

Recommended for You 验收用例：

| 用例 | 前置数据 | 预期结果 |
|---|---|---|
| 与 Wishlist 重复 | 推荐候选中包含 Wishlist 当前已展示的 `listing_id`，且还有其他商品。 | 重复商品不出现，其他商品正常展示。 |
| 与 Recently Viewed 重复 | 推荐候选中包含 Recently Viewed 当前已展示的 `listing_id`，且还有其他商品。 | 重复商品不出现，其他商品正常展示。 |
| 仅有点击浏览行为 | 当前主体无 Wishlist、加购和购买行为。 | 推荐侧按分段函数判断；返回非空结果时展示，返回空结果时静默隐藏。 |
| 已购买同一商品 | 推荐候选中包含推荐侧识别为已购买的 `listing_id`。 | 已购买商品不出现；该购买行为仍可用于其他商品的个性化。 |
| 去重后剩余 1 件 | 排除 Wishlist 和 Recently Viewed 重复商品后，只剩 1 件可展示商品。 | 模块正常展示该商品。 |
| 去重后为空 | 推荐候选全部与 Wishlist 或 Recently Viewed 当前已展示商品重复。 | Recommended for You 静默隐藏。 |
| 删除浏览记录后的当前 Feed | 页面已展示 Recommended for You，用户成功删除一条 Recently Viewed 记录。 | 当前推荐商品、顺序和位置不立即变化；下次页面统一刷新时，使用推荐侧基于最新行为与页面数据返回的新结果。 |

## 六、版本规划

当前 MVP 仅交付 Favorites Overview 的聚合展示与本 PRD 所列交互；完整页、收藏/浏览收录去重、身份复制、Price Drop 统计、推荐算法与数据平台最终口径由各自上游模块负责。后续迭代如新增独立入口、实体或跨角色流程，再评估是否补充架构图、ER 图或泳道图。

## 七、原型索引

| 场景 | V9 Demo 状态 |
|---|---|
| Wishlist / Recently Viewed 正常、少量、Loading、空、首次失败、Price Drop、全售罄 | 各模块对应状态选择器。 |
| 缓存刷新失败 | `Wishlist · Refresh failed (global UI)` / `Recently · Refresh failed (global UI)`；保留内容并在模块标题下显示提示。 |
| 心形写入失败 | Wishlist / Recommend 的 `Heart failed (global UI)`；任意可操作心形均乐观切换后回滚并显示轻量 Toast。 |
| 删除浏览记录失败 | `Recently · Remove failed`；卡片先移除后恢复，并显示轻量 Toast。 |
| 两个核心模块同时失败、Recommend 可用 | `Page · Wishlist + Recently failed`。 |
| 所有业务数据不可用 | `Page · All data failed`。 |
| Recommend 无数据、首次失败、加载更多失败 | Recommend 对应状态选择器。 |
