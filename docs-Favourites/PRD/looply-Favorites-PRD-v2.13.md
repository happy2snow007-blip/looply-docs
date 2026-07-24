# Looply Favorites PRD

> 文档版本：v2.13
> 文档状态：模拟评审问题收口中，不代表已开发、上线或验收
> 日期：2026-07-24
> 适用范围：H5 Mobile · Favorites Overview 聚合展示页
> 原型：`prototypes/favorites/looply-favorites-prototype-v9.html`

## 一、概述

### 1.1 背景与目标

Favorites 面向处于购买考虑阶段的用户，聚合展示 Wishlist、Recently Viewed 和条件出现的 Recommended for You，帮助用户找回商品、感知可购买商品降价，并继续发现商品。

本期只负责 Favorites Overview 的展示、交互、异常降级、页面跳转和与公共能力的衔接；不重定义收藏、浏览历史、Price Drop 或推荐算法。

### 1.2 范围边界

本期仅支持 H5 Mobile；App 与 PC Web 不在本期范围。

本期不负责 Wishlist 完整页、完整浏览历史页、收藏与浏览记录的收录与去重、匿名标识生命周期、Price Drop 识别与统计、推荐算法、Home / Search / Cart / 商品详情的内部逻辑，以及数据平台最终事件实现。

### 1.3 用户与身份

| 用户 | 页面规则 |
|---|---|
| 未登录买家 | 可直接进入，展示当前 `anonymous_id` 对应的 Wishlist、Recently Viewed 和推荐结果；可基于当前 `anonymous_id` 执行 Wishlist 操作，不触发登录硬拦截。 |
| 已登录买家 | 可直接进入，展示当前 `user_id` 对应数据并执行商品查看和 Wishlist 操作。 |

Favorites 不做必须登录硬拦截，也不自行判断、合并或迁移匿名数据。登录、注册、退出或匿名主体变化后，按统一身份模块返回的当前主体重新获取结果；旧主体或迟到请求不得覆盖当前页面。

缓存、写入结果和页面位置按主体隔离。统一身份模块确认主体变化时，立即停止展示上一主体内容，废弃上一主体未完成请求、写入回调、缓存和位置；新主体只读取自身缓存，无自身缓存时进入首次 Loading。普通刷新中的缓存保留规则仅适用于主体未变化的场景。

### 1.4 页面流转

```text
Favorites → 全局搜索 → 返回 Favorites
Favorites → Cart
Favorites → Wishlist 完整页（All / Price Drop）
Favorites → 完整浏览历史（All / Price Drop）
Favorites → Home · Explore Finds · For You
Favorites → 商品详情 → 返回 Favorites
```

从可改变 Wishlist 或浏览历史的页面返回 Favorites 时，受影响模块展示当前主体的最新数据，并恢复离开前的页面及模块位置。该规则覆盖 Search、Wishlist 完整页、完整浏览历史页和商品详情。

### 1.5 多语言与市场策略

- 当前美国范围支持英语 `en-US` 与西班牙语 `es-US`；所有固定 UI 文案使用 i18n message package。
- 商品标题、品牌、成色、浏览时间和价格使用上游返回的最终本地化展示值；Favorites 不自行翻译、拼接或换算。
- Price Drop 使用稳定 i18n key 和复数规则，不通过字符串拼接 `item/items`。
- 价格、币种和金额不翻译；使用全局商品卡价格组件。
- 美国 MVP 的最近浏览记录、匿名身份用途和隐私披露复用《收藏与浏览历史》及隐私模块规则；Favorites 不扩大 `anonymous_id` 的用途。
- 进入美国以外市场前，需重新评估终端存储、同意、留存和浏览记录默认开启规则，不能直接沿用美国方案。

静态 UI 文案使用以下稳定 key。下表为产品交付基线；正式上线前仍需按统一多语言流程完成语言审校。

| i18n key | 使用位置 | `en-US` | `es-US` | 变量 / 规则 |
|---|---|---|---|---|
| `favorites.wishlist.title` | Wishlist 模块标题 | Wishlist | Lista de deseos | 无 |
| `favorites.recently_viewed.title` | Recently Viewed 模块标题 | Recently Viewed | Vistos recientemente | 无 |
| `favorites.recommended.title` | 推荐模块标题 | Recommended for You | Recomendado para ti | 无 |
| `favorites.item_count` | Wishlist / Recently Viewed 正常态数量 | 1 item / {count} items | 1 artículo / {count} artículos | 使用 ICU 复数规则；空态不显示 |
| `common.view_all` | 标题及末尾入口 | View all | Ver todo | 优先复用公共 key |
| `common.view` | Price Drop 提示条右侧入口 | View | Ver | 优先复用公共 key |
| `common.retry` | 模块与加载更多重试 | Retry | Reintentar | 优先复用公共 key |
| `common.loading` | 首次 Loading 的读屏文案 | Loading | Cargando | 不显示可见文案；优先复用公共 key |
| `favorites.explore` | 空态入口 | Explore | Explorar | 无 |
| `favorites.add_more` | Wishlist 少量商品引导 | Add more | Añadir más | 无 |
| `favorites.add_more.subtitle` | Wishlist 引导副文案 | Explore more finds | Explora más opciones | 无 |
| `favorites.explore_more` | Recently Viewed 单商品引导 | Explore more | Explorar más | 无 |
| `favorites.explore_more.subtitle` | Recently Viewed 引导副文案 | Discover more finds | Descubre más opciones | 无 |
| `favorites.wishlist.empty` | Wishlist 空态 | Your wishlist is empty | Tu lista de deseos está vacía | 无 |
| `favorites.recently_viewed.empty` | Recently Viewed 空态 | No recently viewed items yet | Aún no has visto ningún artículo | 无 |
| `favorites.core.empty` | Wishlist 与 Recently Viewed 同时为空 | Nothing saved or viewed yet | Aún no has guardado ni visto ningún artículo | 无 |
| `favorites.core.empty_description` | 两个核心模块合并空态说明 | Save items or browse products to see them here. | Guarda artículos o explora productos para verlos aquí. | 无 |
| `favorites.explore_items` | 合并空态与整页空态入口 | Explore items | Explorar artículos | 无 |
| `favorites.wishlist.load_error` | Wishlist 首次失败 | Couldn't load your wishlist | No se pudo cargar tu lista de deseos | 无 |
| `favorites.recently_viewed.load_error` | Recently Viewed 首次失败 | Couldn't load recently viewed items | No se pudieron cargar los artículos vistos recientemente | 无 |
| `favorites.core.load_error` | 两个核心模块同时首次失败且页面仍有推荐内容 | Couldn't load your wishlist and recently viewed items | No se pudieron cargar tu lista de deseos ni los artículos vistos recientemente | 与 `common.retry` 同时使用 |
| `favorites.wishlist.refresh_error` | Wishlist 缓存刷新失败 | Couldn’t refresh your wishlist | No se pudo actualizar tu lista de deseos | 无 |
| `favorites.recently_viewed.refresh_error` | Recently Viewed 缓存刷新失败 | Couldn’t refresh recently viewed items | No se pudieron actualizar los artículos vistos recientemente | 无 |
| `favorites.recently_viewed.remove` | 删除单条浏览记录的无障碍名称 | Remove from recently viewed | Eliminar de vistos recientemente | 不显示可见文案 |
| `favorites.recently_viewed.remove_error` | 删除浏览记录失败 Toast | Couldn’t remove this item. Try again. | No se pudo eliminar este artículo. Inténtalo de nuevo. | 无 |
| `favorites.wishlist.update_error` | 心形写入失败 Toast | Couldn’t update Wishlist. Try again. | No se pudo actualizar la lista de deseos. Inténtalo de nuevo. | 无 |
| `favorites.price_drop` | Price Drop 提示条 | 1 item dropped in price / {count} items dropped in price | 1 artículo bajó de precio / {count} artículos bajaron de precio | 使用 ICU 复数规则；`count > 0` |
| `favorites.recommended.loading_more` | 推荐加载更多 | Loading more… | Cargando más… | 无 |
| `favorites.recommended.load_more_error` | 推荐加载更多失败 | Couldn’t load more | No se pudieron cargar más artículos | 与 `common.retry` 同时使用 |

固定 UI 的可见文案与无障碍文案均随当前语言切换；商品卡、Wishlist 心形和 Loading 复用全局组件规则。

动态展示内容与不翻译字段按下表消费上游结果，Favorites 不新建资源卡片：

| 业务对象 | 业务字段 | 内容类别 | 卡片决策 | `resourceType` | 翻译中心路径 | `fieldName` | 展示面 | `en-US` / `es-US` 与兜底 |
|---|---|---|---|---|---|---|---|---|
| 商品 Listing | 商品名称 | 动态业务内容 | 复用商品既有卡片；实际资源待技术校验 | `listing`（候选） | 商品域 → Listing（待校验） | `listing_title`（候选） | 三个商品模块的商品卡 | 使用商品系统最终本地化标题；缺失兜底由商品 / 多语言模块负责 |
| 商品 Product | 商品名称兜底 | 动态业务内容 | 复用商品既有卡片；实际资源待技术校验 | `product`（候选） | 商品域 → Product（待校验） | `title`（候选） | Listing 标题缺失时的商品卡 | 使用商品系统既有标题优先级；Favorites 不组合标题 |
| 品牌 | 品牌名称 | 动态业务内容 | 复用品牌既有卡片；实际资源待技术校验 | `brand`（候选） | 商品域 → Brand（待校验） | `brand_name`（候选） | 三个商品模块的商品卡 | 遵循品牌术语表和商品系统兜底规则 |
| 商品质检 | 成色等级展示值 | 动态业务内容 | 复用商品域现有资源；卡片归属待确认 | 待确认 | 待商品 / 多语言模块确认 | 待确认 | Wishlist 与 Recently Viewed 商品卡 | 直接使用商品系统最终本地化值；缺失时隐藏 |
| 浏览历史 | 浏览时间文案 | 静态 message + 动态时间变量 | 复用浏览历史 message package / locale formatter，不进业务资源卡片 | — | 浏览历史 UI message package | 稳定 key 由浏览历史上游维护 | Recently Viewed 商品卡 | 直接展示上游本地化值；缺失时隐藏 |
| 商品价格 | 当前价、原价、降价金额、币种 | 不翻译 | 不进翻译中心 | — | 全局价格组件 | — | 三个商品模块的商品卡 | 使用商品系统最终展示值 |

开发前由商品与多语言模块校验 `listing`、`product`、`brand` 和成色等级在实际 `translation_resource` 中的稳定标识，并确认浏览历史时间文案的稳定 message key。未完成校验前，不得由 Favorites 自行选择名称相近的资源卡片。


## 二、页面框架与刷新

### 2.1 页面框架

| 元素 | 规则 |
|---|---|
| Search | 页面顶部展示全局搜索入口框；点击后进入统一全屏搜索页，并将 Favorites 作为来源页。搜索全站商品，不筛选当前 Wishlist 或 Recently Viewed；从搜索发现页或结果页返回时回到 Favorites。 |
| Cart | 进入 Cart。 |
| 模块顺序 | Wishlist → Recently Viewed → Recommended for You（条件出现）。 |
| 底部导航 | `Home / Shop / Favorites / Me`，Favorites 为选中态。 |

### 2.2 刷新与缓存

Favorites 的首次进入、重新进入、从子页面返回、页面可见性恢复和缓存有效期，遵循 H5 Mobile 页面容器的统一刷新与恢复策略；Favorites 不单独设置轮询、刷新频率或过期阈值。

当页面容器策略触发刷新，或用户在 Favorites 主动下拉刷新时：

1. Wishlist、Recently Viewed、Recommended for You 并行请求，各模块成功后独立更新；
2. 有可用缓存时，刷新期间保留当前内容和位置；
3. 下拉刷新请求三个模块；单模块 `Retry` 仅重试对应模块，组合状态的 Retry 范围见第四章；
4. 各模块的刷新失败、缓存保留和 Retry 规则见第四章；
5. 第 2 条仅适用于主体未变化；主体变化时按 1.3 节立即隔离旧主体数据。

## 三、模块详细规则

### 3.1 Wishlist

Wishlist 使用上游提供的真实总数、有序列表和收藏状态。预览按最近收藏优先横向展示，最多 10 件；Sold Out 仍计入 Wishlist 总数并保留上游顺序。

当预览商品不少于 3 件时，首屏完整展示 2 张商品卡并露出部分第 3 张商品卡，用于提示列表支持横向滑动；不足 3 件时按实际数量展示。

| 上游总数 | 标题 View all | 列表末尾 | 展示规则 |
|---|---|---|---|
| 0 | 隐藏 | `Explore` | 轻量空态，进入 Home · Explore Finds · For You。 |
| 1 | 隐藏 | `Add more` | 展示 1 件商品；`Add more` 进入 Home · Explore Finds · For You。 |
| 2 | 隐藏 | 隐藏 | 仅展示 2 件商品。 |
| 3–10 | 展示 | `View all` | 展示全部预览商品。 |
| 大于 10 | 展示 | 第 10 件后 `View all` | 只预览最近 10 件。 |

商品卡展示商品图、品牌、名称、可选成色、价格、可选原价 / 降价、Wishlist 心形和 Sold Out 状态。卡片主体进入商品详情；心形只执行 Wishlist 操作，不得触发商品跳转。

取消收藏发起时，实心心形乐观变为空心，写入失败时按 3.4 节回滚。写入成功后，当前卡片、顺序、Wishlist 总数、入口阈值、Price Drop 数量和提示条均不立即变化；上一次写入完成后，在售商品可在刷新前再次加入 Wishlist，Sold Out 商品则变为置灰空心并不可再加入。下次权威刷新、重新进入或取得新 Wishlist 结果后，未收藏商品才移除。

| 商品状态 | 当前 Wishlist 状态 | 心形规则 |
|---|---|---|
| 在售 | 未收藏 | 空心，可加入。 |
| 在售 | 已收藏 | 实心，可移出。 |
| Sold Out | 未收藏 | 展示置灰空心，禁用点击。 |
| Sold Out | 已收藏 | 保留实心且可操作，可移出。 |

Sold Out 卡整卡灰化，仍计入 Wishlist 总数并保留上游顺序。

Price Drop 完全使用 Wishlist 上游返回的“可购买 Price Drop 总数”，不从预览数组、分页或当前卡片自行计算；上游负责排除 Sold Out。`N > 0` 显示包含降价文案和右侧 `View` 入口的提示条，`N = 0` 时隐藏；文案使用 `1 item dropped in price` / `{N} items dropped in price` 的 i18n 复数规则。无可用缓存且数量请求失败时隐藏提示条；有缓存刷新失败时保留上次成功的数量和提示条，并按第四章展示模块刷新失败提示。

| 入口 | 目标页面 | 初始 Tab |
|---|---|---|
| Price Drop 提示条任意区域（含右侧 `View`） | Wishlist 完整页 | Price Drop |
| 标题或列表末尾 `View all` | Wishlist 完整页 | All |

### 3.2 Recently Viewed

Recently Viewed 直接展示浏览历史上游返回的顺序、真实总数、商品字段和本地化浏览时间，横向最多预览 10 件；浏览时间缺失时隐藏。

当预览商品不少于 3 件时，首屏完整展示 2 张商品卡并露出部分第 3 张商品卡，用于提示列表支持横向滑动；不足 3 件时按实际数量展示。

| 上游总数 | 标题 View all | 列表末尾 | 展示规则 |
|---|---|---|---|
| 0 | 隐藏 | `Explore` | 轻量空态，进入 Home · Explore Finds · For You。 |
| 1 | 展示 | `Explore more` | 展示 1 件商品和引导卡。 |
| 2–3 | 展示 | 隐藏 | 展示现有商品。 |
| 4–10 | 展示 | `View all` | 展示全部预览商品。 |
| 大于 10 | 展示 | 第 10 件后 `View all` | 只预览前 10 件。 |

Recently Viewed 概览卡复用完整浏览记录页的商品信息、状态及删除规则；概览页采用横向预览卡样式，不显示 Wishlist 心形。卡片主体进入商品详情；点击右上角删除入口只删除当前浏览记录，不得触发商品跳转。

单条删除与完整浏览记录页保持一致：操作后立即从当前预览移除卡片，删除请求中禁用该卡片删除入口。删除成功后，以当前主体最新有序预览替换现有预览，并同步真实总数、Price Drop 数量及对应入口；总数仍大于 10 时由下一件商品补足 10 件预览。若 Price Drop 数量变为 0，在卡片完成删除收起后，通过高度与透明度过渡平滑收起提示条，动效参数遵循 H5 Mobile 全局 UI 规范，减少动态效果开启时使用全局默认处理。

删除成功但最新预览或数量同步失败时，不恢复已删除记录；保留删除后的预览，按当前卡片已知信息乐观更新总数和 Price Drop 数量，并显示本模块刷新失败提示与 Retry。删除失败时恢复原卡片、总数、Price Drop 数量及相关入口，并展示轻量 Toast：`Couldn’t remove this item. Try again.`。同一主体较早的刷新结果不得复活已成功删除的记录；主体变化后，旧主体删除结果不得写入新主体页面。Sold Out 浏览记录同样允许删除。

Recently Viewed 与 Wishlist 的加载和异常反馈保持一致，具体按第四章的公共状态规则执行。Price Drop 使用浏览历史上游返回的可购买总数，不在 Favorites 自行计算；展示、缓存与失败规则与 Wishlist 一致。Price Drop 提示条右侧展示 `View`，点击提示条任意区域进入完整浏览历史页的 Price Drop Tab；`View all` 进入完整浏览历史页的 All Tab。

### 3.3 Recommended for You

Recommended for You 基于当前登录或匿名主体的 Wishlist、加购、购买和商品点击浏览行为生成个性化结果。推荐侧负责行为判断、召回和结果过滤；Favorites 前端不自行计算推荐资格。

当缺少 Wishlist、加购和购买行为，只有商品点击浏览行为时，由推荐侧通过分段函数判断是否返回推荐结果。分段函数及其阈值由推荐侧维护。

购买行为可作为偏好信号，但推荐侧识别为已购买的同一 `listing_id` 不进入推荐结果。

推荐结果只包含可购买商品，并排除 Favorites Overview 当前主体 Wishlist 与 Recently Viewed 最终预览集合（各最多 10 件）中的同 `listing_id` 商品。首屏及每次加载更多还需排除当前 Feed 已加载的 `listing_id`，同一推荐会话不得返回重复商品。

三个模块仍可并行请求，但 Recommended for You 只有在推荐上游或聚合层完成同主体预览集合去重校验后才展示，不依赖 Wishlist / Recently Viewed 组件是否成功渲染；无法确认去重结果时不展示未校验结果。过滤后返回至少 1 件商品时展示模块；行为条件不满足、隐私或同意状态不允许个性化、结果为空或首次请求失败时静默隐藏。

Recommended for You 首次请求未完成时不展示模块，也不将该状态视为正常隐藏；其结果会影响整页空态与错误态时，按第四章的组合状态规则处理。

Recommended for You 复用全局双列商品 Feed 卡片。卡片主体进入商品详情；心形支持加入或移出 Wishlist，写入失败时恢复点击前状态，写入中不可重复点击，卡片位置不变化。加载更多复用 H5 Mobile 公共商品 Feed 规则：接近 Feed 底部时自动请求，请求中不重复发起；每批结果完成同主体、跨页去重校验后再追加；无更多结果时静默隐藏加载区；请求失败或本批结果无法完成校验时保留已有商品并在 Feed 末尾提供轻量 Retry，重试成功后追加结果并继续按同一规则加载。

### 3.4 Heart 写入失败的统一规则

同一页面中，所有显示 Wishlist 心形的商品卡按 `listing_id` 共用收藏状态：任一商品卡发起收藏或取消收藏后，其他同商品心形乐观更新；写入中不可重复点击，写入失败时统一回滚。心形状态即时联动，商品卡、模块数量、排序和入口在权威刷新后更新。

回滚完成后展示轻量 Toast：`Couldn’t update Wishlist. Try again.`，Wishlist 与 Recommended for You 共用同一提示和 i18n key。普通写入失败保留当前登录状态；会话失效时使用登录注册模块的统一恢复规则。

## 四、兼容性、状态与异常

Wishlist 与 Recently Viewed 的同类状态使用一致的视觉层级：

| 状态 | 展示规则 |
|---|---|
| 首次 Loading | 保留模块标题，隐藏数量、View all 和 Price Drop；展示 3 张同结构商品卡骨架，仅保留读屏可识别的隐藏 Loading 文案。 |
| 正常 | 展示上游真实数量、商品与入口。 |
| 空态 | 轻量空态与对应 Home 引导；隐藏数量占位、View all 和 Price Drop。 |
| 首次失败 | 轻量行内错误与模块 Retry；不伪装为空态。 |
| 刷新中 | 保留当前可用内容和位置。 |
| 有缓存的刷新失败 | 保留当前可用内容和位置；已确认成功的操作结果不回滚；在当前模块标题下显示轻量提示与 Retry，仅重试当前模块。 |
| 全部售罄 | 上游通过完整集合可购买数量或等价结果确认全部商品均为 Sold Out；商品卡整卡灰化，View all 与 Home 引导仍按 3.1 / 3.2 的总数阈值展示，可购买 Price Drop 数量为 0 并隐藏提示条。不得从最多 10 件预览自行判断。 |

| 页面场景 | 页面表现 | Retry 范围 |
|---|---|---|
| Wishlist 单独失败 | Wishlist 模块级错误，其他内容保持。 | 仅 Wishlist。 |
| Recently Viewed 单独失败 | Recently Viewed 模块级错误，其他内容保持。 | 仅 Recently Viewed。 |
| Wishlist 与 Recently Viewed 同时为空、Recommend 可用 | 隐藏两个核心模块标题及各自空态，合并显示轻量空态引导；Recommend 正常展示。 | 无 Retry；`Explore items` 进入 Home · Explore Finds · For You。 |
| Wishlist 与 Recently Viewed 同时为空、Recommend 首次请求中 | 隐藏两个核心模块标题及各自空态，先显示合并轻量空态；Recommend 暂不展示，不进入整页空态。 | 无 Retry；Recommend 首次请求完成后重新判断页面组合状态。 |
| Wishlist 与 Recently Viewed 同时为空、Recommend 隐藏 | 隐藏三个模块，内容区域显示统一整页空态。Recommend 因行为不足、不允许个性化、空结果或首次失败均按既有规则静默隐藏。 | 无 Retry；`Explore items` 进入 Home · Explore Finds · For You。 |
| Wishlist 与 Recently Viewed 同时首次失败、Recommend 可用 | 隐藏两个核心模块标题及各自错误态，合并显示轻量错误与一个 Retry；Recommend 已完成同主体去重校验时正常展示，否则隐藏。 | 同时重试 Wishlist 与 Recently Viewed；重试后仅一个模块仍失败时恢复为该模块独立错误。 |
| Wishlist 与 Recently Viewed 同时首次失败、Recommend 首次请求中 | 隐藏两个核心模块标题及各自错误态，先显示合并轻量错误与一个 Retry；Recommend 暂不展示，不进入整页错误。 | Retry 只同时重试 Wishlist 与 Recently Viewed；Recommend 首次请求完成后重新判断页面组合状态。 |
| 一个核心模块为空、另一个首次失败 | 两个模块分别显示空态与错误态，不升级为合并状态或整页状态。 | 仅重试失败模块。 |
| Recommend 首次失败 | 静默隐藏 Recommend。 | 无首屏 Retry。 |
| Recommend 有缓存时刷新失败 | 保留当前 Feed 并静默处理，不显示错误、Toast 或 Retry。 | 等待下次页面统一刷新。 |
| Wishlist 与 Recently Viewed 均首次失败且无缓存，Recommend 正常隐藏或首次失败，页面无任何可用业务内容 | 内容区域使用 H5 Mobile 统一整页错误组件；Recommend 的正常隐藏不计为请求失败，但页面已无可用内容。 | 重新请求本页业务数据。 |
| 页面容器或关键公共依赖不可用 | 使用 H5 Mobile 全局整页错误规则。 | 由全局组件负责。 |

空态只表示请求成功且返回 0 条；首次失败只表示无缓存且请求失败。有缓存的刷新失败继续保留原内容并使用模块标题下的刷新失败提示，不进入以上空态或首次失败组合。只要任一模块仍有可用内容，不得使用整页错误覆盖。Wishlist、Recently Viewed 或 Recommended for You 在首次加载、Retry、刷新或删除后结果变化时，均按最新结果重新判断以上组合状态。

## 五、依赖、数据与验收

### 5.1 依赖与风险

| 依赖 | Favorites 的关键要求 |
|---|---|
| Wishlist / 收藏关系 | 当前主体的有序预览、真实总数、收藏状态、Wishlist 写入、可购买 Price Drop 总数、完整集合可购买数量或等价全售罄结果，以及完整页定位。 |
| 浏览历史 | 当前主体的有序预览、真实总数、本地化浏览时间、单条删除后的最新有序预览与数量、可购买 Price Drop 总数、完整集合可购买数量或等价全售罄结果，以及完整页定位。 |
| 推荐 | 基于当前主体的 Wishlist、加购、购买和商品点击浏览行为生成个性化结果；仅有点击浏览行为时使用分段函数判断是否返回。结果只包含可购买商品，排除已购买、当前概览预览集合及当前 Feed 已加载的同 `listing_id` 商品，并在首屏和每次加载更多展示前完成同主体去重校验；隐私或同意状态不可用时返回不可展示结果。 |
| 商品 / 多语言 | 最终本地化商品字段、价格与币种、成色、在售 / Sold Out 状态与商品详情目标；校验动态字段的稳定 `resourceType` / `fieldName` 及译文缺失兜底。 |
| H5 Mobile 页面容器 | 统一刷新策略、缓存、浏览器返回与页面可见性恢复、位置恢复、迟到请求隔离和整页错误组件。 |
| 统一身份 / 登录注册 | 当前主体、主体变化信号、登录复制完成信号、会话恢复和退出结果；缓存、位置和请求按主体隔离。 |
| 隐私 / 同意 | 向推荐侧提供当前主体是否允许个性化的统一结果；Favorites 不自行解释同意状态。 |
| Home / Search / Cart / 商品详情 | 统一目标页、目标区域定位和返回恢复。 |

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

1. 登录和未登录用户均可进入 Favorites，并只展示当前主体结果；未登录用户可基于当前 `anonymous_id` 执行 Wishlist 操作，不触发登录硬拦截。登录、退出、换账号或匿名主体变化时立即停止展示旧主体内容，旧请求、缓存和位置不得进入新主体页面。
2. Wishlist、Recently Viewed、Recommended for You 的顺序、10 件预览上限与数量阈值符合本 PRD；Wishlist 为 2 件时仅展示 2 张商品卡，不出现 `Add more` 或 `View all`；Wishlist 与 Recently Viewed 在预览商品不少于 3 件时，首屏均完整展示 2 张商品卡并露出部分第 3 张卡，两模块的卡宽、间距和横向滑动提示方式保持一致。
3. Wishlist 与 Recently Viewed 的 Price Drop 提示条右侧均显示 `View`；点击提示条任意区域进入对应完整页的 Price Drop Tab，`View all` 进入对应完整页的 All Tab。
4. 商品卡进入商品详情；Wishlist 心形和 Recently Viewed 删除入口点击均不穿透到商品详情。
5. Wishlist 取消收藏成功后，心形立即变空，卡片、顺序、Wishlist 总数、入口阈值和 Price Drop 提示条均保留至下次权威刷新；写入完成前不可重复点击。
6. Wishlist 符合四种在售 / Sold Out 心形规则；Sold Out 未收藏展示置灰空心且禁用点击，已收藏仍可取消；Recently Viewed 的 Sold Out 记录可删除；Recommended for You 不展示 Sold Out 商品。
7. Price Drop 数量使用各自上游的可购买总数，`N = 0` 时隐藏，单复数文案正确；无缓存请求失败时隐藏，有缓存刷新失败时保留上次成功的数量和提示条。
8. Wishlist 与 Recently Viewed 的 Loading、空态、首次失败、缓存刷新失败、Retry 和完整集合全售罄状态保持一致；单模块空态或首次失败保留对应模块标题并隐藏数量、View all、Price Drop 和商品卡；空态进入 Home，首次失败仅重试当前模块；全售罄使用上游完整集合可购买数量或等价结果判定，不改变各模块原有入口阈值。
9. Recently Viewed 单条删除请求中禁用当前删除入口；成功后用最新有序预览、总数和 Price Drop 数量更新模块，总数仍大于 10 时补足 10 件；Price Drop 归零时在卡片收起后平滑收起提示条。删除成功后的同步失败不得复活记录，应保留删除结果、显示模块刷新失败并可 Retry；删除请求失败才恢复原状态并显示删除失败 Toast。
10. 下拉刷新并行请求三个模块，部分失败不影响成功模块；Wishlist 与 Recently Viewed 同时为空且 Recommend 可用时合并显示轻量空态，Recommend 隐藏时进入统一整页空态；两个核心模块均首次失败、无缓存且页面无任何可用业务内容时进入统一整页错误。Recommend 仍在首次请求中时先展示与两个核心模块结果对应的合并轻量状态，不进入整页空态或整页错误；首次请求完成后重新判断页面组合状态。Recommend 首次失败静默隐藏，不得把两个核心模块的成功空结果升级为整页错误。
11. Wishlist 与 Recently Viewed 有缓存的刷新失败保留当前可用内容和 Price Drop 入口，已确认成功的操作结果不回滚；在当前模块标题下显示行内提示，并仅重试失败模块。Recommended for You 有缓存时刷新失败保留 Feed 并静默处理。
12. 同一页面所有显示 Wishlist 心形的卡片按 `listing_id` 实时联动；写入失败时所有同商品心形统一回滚、不改变卡片位置，并展示 `Couldn’t update Wishlist. Try again.`。
13. Wishlist 与 Recently Viewed 同时首次失败但 Recommended for You 可用时，隐藏两个核心模块标题和各自错误态，合并显示轻量错误与一个 Retry；Retry 只同时重试两个核心模块，不刷新仍可用的 Recommended for You。重试后一个成功、一个仍失败时，成功模块正常展示，失败模块恢复为独立错误态。加载、Retry、刷新或删除使任一模块结果变化后，页面按最新结果重新判断组合状态。
14. 固定 UI 的可见文案与无障碍文案均支持 `en-US` / `es-US`；切换语言后，屏幕阅读器读出的操作名称与页面语言一致。动态商品内容和浏览时间按翻译归属表消费上游本地化结果，开发前完成稳定 `resourceType` / `fieldName` 校验；价格与币种不翻译。
15. 仅在 H5 Mobile 验收本 PRD 定义的页面结构、交互、浏览器返回、页面可见性恢复与刷新规则；App 与 PC Web 不在本期验收范围。
16. 推荐侧使用当前主体的 Wishlist、加购、购买和商品点击浏览行为；仅有点击浏览行为时由推荐侧使用分段函数判断是否返回。行为条件不满足、不允许个性化、结果为空或首次失败时静默隐藏；Favorites 前端不自行计算推荐资格。
17. Recommended for You 在展示前排除 Sold Out、已购买的同 `listing_id` 及当前概览 Wishlist / Recently Viewed 最终预览集合中的同 `listing_id` 商品；无法确认去重结果时不展示，去重后有 1 件仍展示，无剩余商品时静默隐藏。
18. Recommended for You 加载更多在接近 Feed 底部时触发，请求中不重复发起；每批结果不得与当前 Feed 重复，无更多结果时静默结束，失败或去重校验不可用时保留已有结果并可 Retry。
19. 从 Search、Wishlist 完整页、完整浏览历史页、商品详情或其他可改变 Wishlist / 浏览历史的页面返回 Favorites 时，受影响模块展示当前主体的最新数据，并恢复离开前的页面及模块位置。

Recommended for You 验收用例：

| 用例 | 前置数据 | 预期结果 |
|---|---|---|
| 与 Wishlist 重复 | 推荐候选中包含 Wishlist 当前已展示的 `listing_id`，且还有其他商品。 | 重复商品不出现，其他商品正常展示。 |
| 与 Recently Viewed 重复 | 推荐候选中包含 Recently Viewed 当前已展示的 `listing_id`，且还有其他商品。 | 重复商品不出现，其他商品正常展示。 |
| 仅有点击浏览行为 | 当前主体无 Wishlist、加购和购买行为。 | 推荐侧按分段函数判断；返回非空结果时展示，返回空结果时静默隐藏。 |
| 已购买同一商品 | 推荐候选中包含推荐侧识别为已购买的 `listing_id`。 | 已购买商品不出现；该购买行为仍可用于其他商品的个性化。 |
| 去重后剩余 1 件 | 排除 Wishlist 和 Recently Viewed 重复商品后，只剩 1 件可展示商品。 | 模块正常展示该商品。 |
| 去重后为空 | 推荐候选全部与 Wishlist 或 Recently Viewed 当前已展示商品重复。 | Recommended for You 静默隐藏。 |
| 加载更多跨页重复 | 新一页包含当前 Feed 已加载的 `listing_id`。 | 重复商品不追加；其余已校验商品按原顺序追加。 |
| 去重校验不可用 | 首屏或加载更多结果无法确认已按当前主体去重。 | 首屏静默隐藏；加载更多保留已有商品并提供 Retry。 |
| 不允许个性化 | 隐私 / 同意上游返回当前主体不可使用个性化。 | Recommended for You 静默隐藏。 |
| 双核心模块为空、推荐首次请求中 | Wishlist 与 Recently Viewed 均已成功返回空，Recommended for You 尚未完成首次请求。 | 先显示合并轻量空态，不进入整页空态；推荐请求完成后按最终结果重新判断组合状态。 |
| 双核心模块失败、推荐首次请求中 | Wishlist 与 Recently Viewed 均首次失败且无缓存，Recommended for You 尚未完成首次请求。 | 先显示合并轻量错误和核心模块 Retry，不进入整页错误；推荐请求完成后按最终结果重新判断组合状态。 |
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
| 两个核心模块同时为空、Recommend 可用 | `Page · Wishlist + Recently empty`；合并空态后继续展示 Recommend。 |
| 两个核心模块同时为空、Recommend 首次请求中 | `Page · Core empty + Recommend loading`；先展示合并轻量空态，不进入整页空态。 |
| 两个核心模块同时为空、Recommend 隐藏 | `Page · All content empty`；展示统一整页空态。 |
| 两个核心模块同时首次失败、Recommend 可用 | `Page · Wishlist + Recently failed`；隐藏两个模块标题，合并轻量错误并继续展示 Recommend。 |
| 两个核心模块同时首次失败、Recommend 首次请求中 | `Page · Core failed + Recommend loading`；先展示合并轻量错误，不进入整页错误。 |
| 所有业务数据不可用 | `Page · All data failed`；展示统一整页错误。 |
| Recommend 无数据、首次失败、加载更多失败 | Recommend 对应状态选择器。 |
