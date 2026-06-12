# Looply 首页 Explore Finds Feed PRD

## 1. 模块概述

Explore Finds Feed 是首页中的商品流模块，位于 Hero Banner、Trust 模块、Curated Collections 之后，用于持续展示当前 Market + Channel 下的可售商品，并通过 Tab 区分不同商品发现场景。

Feed 的核心目标不是单纯展示商品，而是让用户在首页持续发现商品，并在用户发生点击、收藏、购买等行为后，为 For You 推荐提供行为数据基础。

本版本重点更新 For You 推荐逻辑：

```text
For You =
A1 当前 Session 兴趣相似召回
+
A2 24h 近期兴趣相似召回
+
B New Arrivals 召回
+
C Best Sellers 召回
```

其中：

- A1 和 A2 使用同一套相似召回算法，只是基准商品来源不同。
- A1 基准来自当前推荐 Session 的点击和收藏。
- A2 基准来自最近 24h 的点击和收藏，但必须先剔除当前 Session 已发生点击 / 收藏行为的 listing。
- B 复用 New Arrivals Tab 的商品池。
- C 复用 Best Sellers Tab 的商品池。
- For You 复用 B / C 的商品池，但不复用 B / C 的展示顺序。
- For You 是无限流，不展示“已全部看完”的结束状态。

---

## 2. 功能目标

| 目标 | 说明 |
|---|---|
| 商品发现 | 用户可以在首页持续浏览可售商品 |
| 多场景切换 | 通过 For You / New Arrivals / Best Sellers / Deals 区分浏览场景 |
| 支持未登录浏览 | 未登录用户也可以浏览商品流 |
| 支持会话级推荐 | 未登录和已登录用户均可通过推荐 Session 产生会话级推荐 |
| 支持 24h 近期兴趣推荐 | 根据用户最近 24h 点击、收藏、购买行为判断用户兴趣强度 |
| 支持当前 Session 兴趣推荐 | 当前 Session 内点击 / 收藏会影响 A1 通路 |
| 支持跨 Session 近期兴趣推荐 | 最近 24h 但不属于当前 Session 的点击 / 收藏会影响 A2 通路 |
| 支持商品去重 | 同一 Session 已展示商品不重复展示 |
| 支持曝光频控 | 同一 listing 在 24h 内对同一用户最多展示指定次数 |
| 支持间隔去重 | 同一 listing 在间隔 X 个商品内不得重复出现 |
| 支持多通路混排 | A1 / A2 / B / C 进入统一候选池后混排 |
| 支持多样性控制 | 控制同品牌、同系列、同类目、同价格带连续出现 |
| 支持无限流 | 每次加载默认返回 20 个 listing，不主动展示结束态 |
| 支持后续推荐演进 | 为长期画像、向量召回、精排模型积累行为数据 |
| 支持多 Market | 推荐数据按 Market + Channel 隔离 |

---

## 3. 不做什么

| 不做事项 | 原因 |
|---|---|
| 不在 Feed 侧管理商品主数据 | 商品主数据由商品系统维护 |
| 不在 Feed 侧重复计算库存数量 | 可售性由商品 / 库存域通过 listing_status / product_status 表达 |
| 不使用 available_quantity | Feed 只消费上游可售状态结果 |
| 不主动推荐不可售商品 | 首页 Feed 以转化为目标，不主动推荐不可购买商品 |
| 不在 MVP 做长期用户画像 | 先做 24h 行为分层和基础召回 |
| 不在 MVP 做向量召回 | 向量能力放到后续版本 |
| 不在 MVP 做深度学习排序 | 当前阶段使用规则召回 + 配额混排 |
| 不在 MVP 强依赖 Deals | 促销价、降价记录等营销能力未完整定义 |
| 不在 MVP 直接按 listing 购买数做 Best Sellers | Looply 一物一码，单个 listing 通常只能售出一次，listing 级购买数区分度不足 |
| 不把 wishlist_click 当作收藏兴趣 | wishlist_click 只是点击收藏按钮，只有 wishlist_add 成功才代表收藏成立 |
| 不把曝光 / 滚动作为兴趣分 | 曝光和滚动不能稳定代表用户兴趣，MVP 不参与用户状态判断 |

---

## 4. 术语说明

| 术语 | 说明 | 定义来源 |
|---|---|---|
| Explore Finds Feed | 首页商品流模块 | 本次 PRD 新定义 |
| Tab | Feed 内的场景切换入口，如 For You、New Arrivals | 本次 PRD 新定义 |
| 商品卡 | Feed 中每个 listing 的展示卡片 | 本次 PRD 新定义 |
| listing | 渠道商品，一件实物商品在某个销售渠道的上架记录，是 Feed 的展示对象 | 已有，商品系统 listing |
| product | 实物商品，一物一码，独立成色、质检和鉴定信息 | 已有，商品系统 product |
| standard_sku | 标品 SKU，SPU 下按销售属性组合拆分的标准规格 | 已有，商品系统 standard_sku |
| spu | 标准产品单元，代表标准商品 | 已有，商品系统 spu |
| backend_category | 后台类目，商品主数据分类维度 | 已有，商品系统 backend_category |
| brand | 品牌主数据 | 已有，商品系统 brand |
| series | 品牌系列 | 已有，商品系统 series |
| grade | 成色等级 | 已有，product / product_inspection |
| wishlist | 用户收藏关系 | 收藏模块 |
| Market | 市场维度，决定语言、货币、渠道和商品池 | Market 系统 |
| Channel | 销售渠道维度 | Channel 配置 |
| 可售 | listing 处于在售状态且商品处于可售状态 | 本次 PRD 定义业务规则 |
| 推荐 Session | 推荐侧浏览会话，不等于登录注册系统 user_session | 本次 PRD 新定义 |
| anonymous_user_id | 未登录用户的匿名访问标识，由推荐 / 埋点侧生成，不属于登录注册系统表 | 本次 PRD 新定义 |
| user_key | 推荐侧用户识别键，已登录用 user_id，未登录用 anonymous_user_id | 本次 PRD 新定义 |
| A1 通路 | 当前 Session 兴趣相似召回 | 本次 PRD 新定义 |
| A2 通路 | 24h 近期兴趣相似召回，排除当前 Session 行为商品后取基准 | 本次 PRD 新定义 |
| B 通路 | New Arrivals 商品池召回 | 本次 PRD 新定义 |
| C 通路 | Best Sellers 商品池召回 | 本次 PRD 新定义 |
| interest_score_24h | 最近 24h 用户兴趣分 | 本次 PRD 新定义 |
| 曝光频控 | 控制同一 listing 在一定时间内重复展示次数 | 本次 PRD 新定义 |
| 间隔去重 | 控制同一 listing 在最近 X 个已展示商品内不重复出现 | 本次 PRD 新定义 |
| 打散 | 控制同品牌、同类目、同系列商品不要连续出现 | 本次 PRD 新定义 |
| 降级 | 当推荐依赖不可用时，使用稳定规则替代 | 本次 PRD 定义业务规则 |

说明：

登录注册系统已有 user_account、user_session 等概念，但 user_session 是登录态会话，不等于推荐 Session。未登录用户的 anonymous_user_id 不属于登录注册模块原有表，本 PRD 只定义推荐 / 埋点侧需要具备匿名用户识别能力，具体命名和实现由研发确定。

---

## 5. 多 Market 与多 Channel 策略

说明：Market 检测与来源优先级（用户选择 > 账户默认 > IP/浏览器推断 > 系统默认）属于页面层/会话层职责，不属于 Feed 模块。Feed 只消费当前已确定的 market_id + channel_id，不做 Market 推断。详见 Market 系统 PRD v1.2。Channel 归属于 Market，不可跨 Market 切换，详见商品系统 PRD v1.7。

| 项目 | 规则 |
|---|---|
| 商品池 | Feed 仅读取当前 market_id + channel_id 下的可售 listing |
| 行为数据维度 | 所有点击、收藏、购买、曝光行为记录时必须携带 market_id + channel_id |
| 推荐召回范围 | A1/A2 相似召回、B 新上架、C Best Sellers 均只返回当前 market_id + channel_id 下的商品 |
| 用户相似性范围 | 用户兴趣基准商品和候选商品匹配均限定在当前 market_id + channel_id 内，不跨 Market 或 Channel |
| 推荐配置 | 配置项支持按 Market / Channel 覆盖，未配置时使用系统默认值 |

### 5.1 Feed 数据隔离规则

| 项目 | 规则 |
|---|---|
| 商品曝光 | 按 market_id + channel_id 隔离，独立统计 |
| 点击数据 | 按 market_id + channel_id 隔离，独立统计 |
| 收藏数据 | 按 market_id + channel_id 隔离，独立统计 |
| 购买数据 | 按 market_id + channel_id 隔离，独立统计 |
| 热门统计 | 按 market_id + channel_id 隔离，独立统计 |
| 用户兴趣分 | interest_score_24h 按 user_key + market_id + channel_id 计算 |
| 推荐训练 | 按 market_id 隔离，不跨 Market 共享训练数据 |

---

## 6. Explore Finds Feed 模块总览

### 6.1 功能描述

Explore Finds Feed 在首页中展示商品卡片流，由模块标题、Tab 区、商品卡片网格、加载更多状态和异常状态组成。

该模块独立于首页 Banner、Trust、Collections，不受这些模块的展示状态影响。

### 6.2 页面布局

| 区域 | 内容 | 说明 |
|---|---|---|
| 模块标题 | Explore Finds | 固定展示 |
| Tab 区 | For You / New Arrivals / Best Sellers / Deals | 横向排列，移动端可横向滑动 |
| 商品网格 | 商品卡片 | PC 4 列，Mobile 2 列 |
| 异常状态 | 加载失败、重试 | 仅影响 Feed 模块，不影响首页其他模块 |
| 无限流 | 下滑持续加载 | 不展示“已全部看完”的结束态 |

说明：

本版本不设计结束状态。Feed 是无限流，每次加载默认返回 20 个 listing。若当前请求无法生成足够新候选，则进入兜底逻辑，不直接展示 “You’ve seen it all”。

---

## 7. 前置依赖

| 依赖模块 | 依赖内容 | 当前状态 | 是否阻塞 MVP | 当前处理 |
|---|---|---|---|---|
| 商品系统 | listing、product、standard_sku、spu、brand、series、backend_category | 已有 PRD + 已有实体关系设计 / 字段定义 | 是 | Feed 展示对象必须是 listing_id |
| 商品系统（字段待新增） | listed_at（listing 首次变为 active 的时间戳） | 字段缺失，需提需求。商品系统 v1.7 明确"上架时间通过操作日志查看，不作为独立字段"，即当前无可查询字段 | 是，阻塞 New Arrivals 和 B 通路 | 需向商品系统侧提字段新增需求，建议命名 listed_at 或 on_shelf_at |
| 商品系统（字段名待确认） | 成色等级字段名（枚举值 NWT / Excellent / Good / Fair） | 商品系统 v1.7 有成色录入和枚举，但字段名（如 grade、condition 等）未在 PRD 中显式写出 | 是 | 快照表 grade 字段同步时需确认源字段名 |
| Market 系统 | market_id、language_code、currency_code、channel_id | 已有 PRD | 是 | 决定当前用户应该看到哪个市场、哪个渠道的商品 |
| 登录注册 | user_id、登录态识别 | 已有 PRD | 否 | 已登录时记录 user_id；推荐不按是否登录判断状态 |
| 匿名用户识别 | anonymous_user_id | 待新增 | 是 | 未登录用户也需要记录 24h 点击、收藏、曝光等行为 |
| 收藏模块 | 收藏状态读取、收藏成功写入 | 待确认 | 是 | 商品卡收藏入口依赖；收藏成功后记录 wishlist_add |
| 推荐系统 | A1/A2/B/C 召回、用户状态分层、混排、去重、频控 | 缺失 | 是 | 本 PRD 新增 |
| 用户行为数据 | 曝光、点击、收藏成功、取消收藏、购买、Tab 切换、加载更多 | 部分缺失 | 是 | 用于推荐、去重、频控、分析 |
| 订单系统 | listing / product / spu 的购买完成记录 | 待确认 | 是 | 用于 Best Sellers 中的购买热度，以及用户 24h 购买行为统计 |
| 营销系统 | promotion_price、price_drop、折扣 | 缺失 | 否 | Deals MVP 可隐藏或延后 |
| 埋点系统 | Feed 曝光、点击、收藏、加载更多 | 已有框架，事件需新增 | 是 | MVP 必须接入 |
| CMS / 运营配置 | Tab 开关、推荐配置默认值 | 缺失 | 否 | MVP 可先通过配置表维护 |
| 翻译模块 | 商品标题、品牌、类目、属性翻译 | 已有 PRD | 是 | 无翻译时 fallback 默认语言 |
| 图片服务 | 图片裁剪、CDN、WebP、兜底图 | 已有能力 | 是 | 商品卡必须稳定展示图片 |

---

## 8. Feed 展示对象

Feed 的展示对象必须是：

```text
listing_id
```

原因：

| 原因 | 说明 |
|---|---|
| 一物一码 | Looply 商品是二手实物商品，每件 product 独立成色、图片、质检、鉴定 |
| 多渠道 | 同一 product 可以在不同 channel 下有不同 listing |
| 前台售卖 | 用户实际点击、收藏、购买的对象是 listing |
| 价格独立 | listing_price / currency_code / listing_status 都在 listing 侧表达 |
| 推荐去重 | Feed 需要按 listing_id 做曝光去重和返回去重 |
| 购买特殊性 | 单个 listing 通常只能售出一次，购买热度需从 SPU 维度继承 |

Feed 不直接以 spu_id、standard_sku_id 或 product_id 作为前台展示对象。

---

## 9. 通用基础商品池

Feed 所有 Tab 和推荐通路均从基础商品池开始过滤。

```text
base_pool =
当前 market_id
+ 当前 channel_id
+ listing_status = 可售
+ product_status = 可售
+ listing_price > 0
+ main_image_url 不为空
+ grade 不为空
```

说明：

| 规则 | 说明 |
|---|---|
| 不使用 available_quantity | Feed 不重复计算库存 |
| 不使用库存数量字段 | 不读取 quantity_on_hand / quantity_reserved / quantity_locked |
| 可售性来源 | 由商品 / 库存域在 listing_status / product_status 中统一表达 |
| 图片有效 | 无主图商品不进入首页 Feed |
| 价格有效 | listing_price <= 0 的商品不进入 Feed |
| 成色有效 | grade 为空的商品不进入 Feed |
| Market 隔离 | 不同 Market 使用不同 Channel 下的 listing 池 |

注意：

已展示过滤、24h 曝光频控、间隔去重、跨通路去重不属于基础商品池规则，而属于推荐混排阶段规则。

---

## 10. 推荐 Session

Feed 推荐使用推荐侧 session_id，不是登录注册系统的 user_session。

| 项目 | 规则 |
|---|---|
| session_id | 推荐侧浏览会话 ID |
| 作用 | 串联曝光、点击、收藏、加载更多、Tab 切换等行为 |
| 是否要求登录 | 否，未登录用户也必须有 |
| 与 user_id 关系 | 已登录时同时记录 session_id + user_id；未登录时 user_id 为空 |
| 与 anonymous_user_id 关系 | 未登录或未识别用户用 anonymous_user_id 做行为归因 |
| 是否等于一屏商品 | 否，session 是一次连续浏览会话 |
| 下一屏请求是否更新 | 不更新 session_id，只更新行为数据 |
| 失效规则 | 连续 30 分钟无首页 Feed 行为后失效 |

### 10.1 首页 Feed 行为定义

首页 Feed 行为是用户在商品流中产生的操作或系统可记录的展示事件。行为需要写入行为日志，供推荐、统计、频控和分析使用。

| 行为事件 | 中文意思 | 是否需要记录 | 用途 |
|---|---|---:|---|
| product_card_impression | 商品卡曝光，即商品卡进入可视区域 | 是 | 用于曝光统计、CTR 分母、Session 去重、24h 曝光频控 |
| product_card_click | 用户点击商品卡进入商详 | 是 | 用于 A1/A2 基准、用户状态分、CTR 分子 |
| wishlist_click | 用户点击收藏按钮 | 是 | 用于收藏漏斗分析，不等于收藏成功 |
| wishlist_add | 收藏成功 | 是 | 用于 A1/A2 基准、用户状态分、Best Sellers 热度分 |
| wishlist_remove | 取消收藏 | 是 | 用于负反馈分析，MVP 不进入用户状态分 |
| feed_tab_switch | 用户切换 Feed Tab | 是 | 用于分析用户偏好哪个 Tab |
| feed_load_more | 用户触发下一屏加载 | 是 | 用于浏览深度分析和请求日志 |
| scroll_depth | 用户滚动深度 | 是 | 用于 Feed 吸引力分析，MVP 不进入用户状态分 |
| purchase_complete | 购买完成 | 是 | 用于用户状态分、Best Sellers 购买热度。注意：该事件由订单系统/支付完成后触发，触发点在商详页/结账页，不在首页 Feed；Feed 侧消费该事件数据，不负责触发埋点 |

---

## 11. Feed Tabs

### 11.1 Tab 列表

| Tab | 中文说明 | MVP 状态 | 说明 |
|---|---|---|---|
| For You | 个性化推荐 | 启用 | 基于 A1/A2/B/C 召回进入统一候选池 |
| New Arrivals | 新上架 | 启用 | 基于 listed_at 倒序 |
| Best Sellers | 热卖 / 热门 | 启用 | 使用 C 通路热门逻辑，不直接按 listing 销量排序 |
| Deals | 折扣 | 一期暂时留空 | 依赖促销价、降价记录、营销活动 |

### 11.2 默认 Tab

| 行为数据情况 | 默认 Tab | 说明 |
|---|---|---|
| 有行为数据（24h 内有点击或收藏） | For You | 已登录或匿名用户均可；已登录用 user_id 查询行为，未登录用跨 session 持久的 anonymous_user_id |
| 无行为数据（24h 内无点击或收藏） | For You，使用 B/C 冷启动 | A1/A2 无基准，由 B New Arrivals + C Best Sellers 承载 |
| 推荐服务异常（A1/A2/B/C 全部不可用） | New Arrivals 商品池直接排序兜底 | 降级到 B 通路排序逻辑，不依赖推荐算法 |

说明：

"有行为数据" = 当前 24h 内有 product_card_click 或 wishlist_add，与是否登录无关。anonymous_user_id 跨 session 持久（生命周期 ≥30 天），支持匿名用户跨多个 session 积累 24h 行为，不因关闭浏览器而重置。

---

## 12. For You 规则

### 12.1 功能描述

For You 是首页 Feed 的核心 Tab，目标是根据用户当前 Session 行为、最近 24h 行为、新上架商品和热门商品，返回更符合用户兴趣的商品流。

MVP 阶段 For You 不做长期画像、不做向量召回、不做深度学习排序。

采用：

```text
用户状态分层
+ A1/A2/B/C 多通路召回
+ 统一候选池
+ 配额混排
+ 去重与曝光频控
+ 多样性打散
+ 无限流兜底
```

### 12.2 用户识别

推荐系统不以“是否登录”判断推荐状态。

推荐系统使用 user_key 识别用户行为：

| 场景 | user_key | 说明 |
|---|---|---|
| 已登录 | user_id | 来自登录注册系统 |
| 未登录 | anonymous_user_id | 推荐 / 埋点侧生成的匿名访问标识 |
| 登录前后合并 | 后续支持 | MVP 可先不强制做历史合并 |

说明：

anonymous_user_id 不是登录注册模块已有字段，本 PRD 只定义推荐系统需要一个匿名用户识别键。实际字段名和存储方式由研发确认。

持久化要求：anonymous_user_id 需跨 session 持久，生命周期建议 ≥30 天（覆盖用户常规回访周期）。MVP 不强制合并匿名行为到登录后的 user_id，V1.1 支持历史合并。

### 12.3 用户状态分层

用户状态由最近 24h 兴趣行为决定。

24h 行为定义：

```text
当前 user_key
+ 当前 market_id
+ 当前 channel_id
+ 当前请求时间往前 24 小时内
已经成功上报的行为
```

24h 行为包含当前 Session 内已经发生并成功上报的行为。

兴趣分公式：

```text
interest_score_24h =
click_count_24h × click_weight
+ wishlist_add_count_24h × wishlist_weight
+ purchase_count_24h × purchase_weight
```

MVP 默认：

| 行为 | 默认权重 | 是否进入用户状态 | 是否进入 A1/A2 基准 | 是否支持配置 |
|---|---:|---:|---:|---:|
| product_card_click | 1 | 是 | 是 | 是 |
| wishlist_add | 3 | 是 | 是 | 是 |
| purchase_complete | 10 | 是 | 否 | 是 |
| product_card_impression | 0 | 否 | 否 | 是 |
| wishlist_click | 0 | 否 | 否 | 是 |
| wishlist_remove | 0 | 否 | 否 | 是 |
| scroll_depth | 0 | 否 | 否 | 是 |

说明：

- 点击和收藏都可表达兴趣，收藏优先级高于点击。
- 购买只用于判断用户活跃和兴趣强度，不作为 A1/A2 相似召回基准。
- 曝光和滚动默认不作为兴趣分，避免用户快速划过导致误判。
- 行为权重必须配置化。
- 架构说明：24h 行为来源包含用户在**所有页面**的行为（不只是首页 Feed），支持后续其他页面行为纳入兴趣分计算。MVP 阶段仅首页 Feed 接入埋点，因此实际行为来源为首页 Feed；架构设计上不限制来源页面，后续可扩展。

### 12.4 用户状态枚举

| 状态 | 默认条件 | 说明 | 是否支持配置 |
|---|---|---|---:|
| S0 冷启动 | interest_score_24h = 0 | 最近 24h 无有效兴趣行为 | 是 |
| S1 轻兴趣 | 1 ≤ interest_score_24h < 5 | 有少量点击或收藏 | 是 |
| S2 中兴趣 | 5 ≤ interest_score_24h < 15 | 有较明确兴趣 | 是 |
| S3 强兴趣 | interest_score_24h ≥ 15 | 高频点击、收藏或购买 | 是 |

所有阈值均支持配置。

### 12.5 MVP 召回来源

| 通路 | 说明 | 是否启用 | 复用关系 |
|---|---|---:|---|
| A1 当前 Session 兴趣相似召回 | 基于当前 Session 的点击 + 收藏商品召回相似 listing | 是 | For You 专属 |
| A2 24h 近期兴趣相似召回 | 基于最近 24h 的点击 + 收藏商品召回相似 listing，但剔除当前 Session 行为商品 | 是 | For You 专属 |
| B 新上架召回 | 当前 Market + Channel 下最新上架商品 | 是 | 复用 New Arrivals 商品池 |
| C Best Sellers 召回 | 近期浏览、点击、收藏、购买表现较好的商品 | 是 | 复用 Best Sellers 商品池 |

说明：A1/A2 的行为基准来源于用户在**所有页面**产生的行为（架构预留），MVP 阶段仅首页 Feed 接入埋点，实际行为来源为首页 Feed。

### 12.6 A1/A2 基准商品规则

A1 和 A2 使用完全相同的相似召回算法，区别只在基准商品来源。

| 通路 | 基准来源 | 时间范围 | 是否排除当前 Session 行为商品 |
|---|---|---|---|
| A1 | 当前 Session 内 wishlist_add + product_card_click | 当前推荐 Session | 否 |
| A2 | 最近 24h wishlist_add + product_card_click | 当前请求时间往前 24 小时 | 是 |

#### 12.6.1 A1 基准商品生成

A1 基准商品来自当前推荐 Session 内已经成功上报的兴趣行为。

兴趣行为包括：

```text
wishlist_add
product_card_click
```

生成规则：

```text
先取当前 Session 内 wishlist_add 商品
不足 seed_count 时
再用当前 Session 内 product_card_click 商品补齐
```

#### 12.6.2 A2 基准商品生成

A2 基准商品来自最近 24h 兴趣行为，但必须先排除当前 Session 已发生兴趣行为的商品。

生成流程：

```text
读取当前 user_key 最近 24h wishlist_add + product_card_click 行为
↓
读取当前 Session 已发生 wishlist_add + product_card_click 的 listing_id
↓
从 24h 行为列表中剔除这些 listing_id
↓
先取剩余 wishlist_add 商品
↓
不足 seed_count 时
再用剩余 product_card_click 商品补齐
```

说明：

- 24h 行为天然包含当前 Session 行为。
- A2 的定位是补充“当前 Session 之外的近期兴趣”。
- 当前 Session 内的点击和收藏只由 A1 消费，避免 A1/A2 使用同一批基准商品重复召回。

#### 12.6.3 基准商品去重规则

| 场景 | 处理方式 |
|---|---|
| 同一 listing 在同一通路内既被点击又被收藏 | 按收藏基准处理 |
| 同一 listing 在同一通路内多次点击 | 只保留最近一次点击 |
| 同一 listing 在同一通路内多次收藏 | 只保留最近一次收藏 |
| 同一 listing 同时出现在 A1 和 A2 原始基准中 | A2 生成基准时剔除，优先由 A1 消费 |
| A2 剔除当前 Session 行为商品后不足 seed_count | 有多少用多少 |
| A2 剔除后为空 | A2 不触发，配额释放给 A1/B/C |

#### 12.6.4 A1/A2 基准案例

当前请求时间为 6 月 11 日 20:00。

最近 24h 行为：

| 时间 | 行为 | listing |
|---|---|---|
| 6 月 11 日 19:50 | wishlist_add | LV Neverfull |
| 6 月 11 日 19:40 | product_card_click | Rolex Datejust |
| 6 月 11 日 10:00 | wishlist_add | Chanel CF |
| 6 月 10 日 23:00 | product_card_click | Omega Speedmaster |

当前 Session 行为：

| 行为 | listing |
|---|---|
| wishlist_add | LV Neverfull |
| product_card_click | Rolex Datejust |

A1 基准：

```text
LV Neverfull
Rolex Datejust
```

A2 先剔除当前 Session 已发生行为的：

```text
LV Neverfull
Rolex Datejust
```

A2 剩余 24h 基准：

```text
Chanel CF
Omega Speedmaster
```

### 12.7 A1/A2 相似召回规则

对每个基准 listing 单独执行一次相似召回。

系统从 recommend_listing_feature_snapshot（本次新增，见§20.2）读取基准商品特征：

```text
brand_id
series_id
backend_category_id
grade
price_band
listing_price
```

候选商品必须至少命中以下任一条件：

| 匹配条件 | 是否进入候选 |
|---|---:|
| 同 series_id | 是 |
| 同 brand_id | 是 |
| 同 backend_category_id | 是 |
| 同 grade | 是 |
| 同 price_band | 是 |
| 相邻 price_band | 是 |
| 以上均不命中 | 否 |

单个基准商品相似分：

| 子分项 | 计算规则 | 默认分值 | 是否支持配置 |
|---|---|---:|---:|
| series_match_score | candidate.series_id = seed.series_id，且 seed.series_id 不为空 | 3.0 | 是 |
| brand_match_score | candidate.brand_id = seed.brand_id | 2.5 | 是 |
| category_match_score | candidate.backend_category_id = seed.backend_category_id | 2.0 | 是 |
| grade_match_score | candidate.grade = seed.grade | 1.0 | 是 |
| same_price_band_score | candidate.price_band = seed.price_band | 1.5 | 是 |
| adjacent_price_band_score | candidate.price_band 与 seed.price_band 相邻 | 0.8 | 是 |

A1 和 A2 的基准数量、匹配条件、相似分配置分别独立配置，即使 MVP 初始值一致，也不共用同一套配置。

A1/A2 内部聚合规则：

| 项目 | 规则 |
|---|---|
| 去重字段 | listing_id |
| 同一 listing 被多个基准召回 | 只保留一条 |
| 分数保留 | 保留最高 single_similar_score |
| 命中次数 | 记录 recall_hit_count |
| 是否分数累加 | 否 |
| 排序辅助 | similar_score desc、recall_hit_count desc、listed_at desc、listing_id asc |

### 12.8 B 通路规则

B 通路复用 New Arrivals 商品池。

召回规则：

从基础商品池（base_pool）中，筛选出 listed_at 不为空、且上架时间在最近 b_freshness_days 天内（默认 30 天）的商品，按以下顺序排序后作为 B 通路候选池：

1. 上架时间从新到旧（listed_at 降序）
2. 成色从高到低（grade 降序：NWT > Excellent > Good > Fair）
3. listing_id 升序（分页稳定性兜底）

排序说明：
- 第一排序键确保最新上架的商品优先进入 Feed，体现"New Arrivals"的核心价值
- 第二排序键在同一时间上架的商品中，优先展示成色更好的商品，提升 Feed 整体品质感
- 第三排序键保证分页时结果顺序稳定，避免翻页时商品乱跳

B 通路在 New Arrivals Tab 中按上述规则展示。

B 通路在 For You 中仅作为候选来源，不直接复用 New Arrivals 的最终展示顺序。

### 12.9 C 通路规则

C 通路复用 Best Sellers 商品池。

C 通路不是直接对全量商品计算热门分，而是先用曝光量过滤，再计算 hot_score。

召回源流程：

```text
当前 Market + Channel 基础商品池
↓
关联 recommend_listing_stats（本次新增，见§20.3）
↓
按 impression_session_count_7d 倒序
↓
取曝光 session Top K 商品
↓
计算 hot_score
↓
按 hot_score 倒序
↓
进入 C 通路候选池
```

默认：

```text
impression_top_k = 2000
```

#### 12.9.1 C 通路统计口径

| 指标 | 中文定义 | 字段 |
|---|---|---|
| 7天曝光 session 数 | 近 7 天看过该 listing 的去重 session 数 | impression_session_count_7d |
| 7天点击 session 数 | 近 7 天点击过该 listing 的去重 session 数 | click_session_count_7d |
| 7天 CTR | 7天点击 session 数 / 7天曝光 session 数 | ctr_7d |
| 7天收藏数 | 近 7 天该 listing 被收藏成功的次数 | wishlist_add_count_7d |
| 30天 SPU 购买数 | 当前 listing 对应 spu_id 在近 30 天内的购买次数 | spu_purchase_count_30d |

说明：

Looply 是一物一码业务，单个 listing 通常只能卖出一次，因此购买热度不直接用 listing 购买数，而是从 SPU 维度继承。

#### 12.9.2 C 通路归一化规则

C 通路 hot_score 满分 10 分。CTR、收藏数、购买数需要先归一化到 0–1，再按权重计算。

归一化只在 C 通路浏览量 Top K 候选池内计算。

```text
hot_source_pool =
base_pool
+ impression_session_count_7d Top K
```

默认：

```text
impression_top_k = 2000
```

CTR 归一化：

```text
ctr_norm_score =
ctr_7d / max_ctr_7d_in_hot_source_pool
```

处理规则：

| 场景 | 处理 |
|---|---|
| 候选池最高 CTR > 0 | 正常计算 |
| 候选池最高 CTR = 0 | 所有商品 ctr_norm_score = 0 |
| 计算结果超过 1 | 按 1 处理 |

收藏数归一化：

```text
wishlist_norm_score =
log(1 + wishlist_add_count_7d)
/
max(log(1 + wishlist_add_count_7d) in hot_source_pool)
```

购买数归一化：

```text
purchase_norm_score =
log(1 + spu_purchase_count_30d)
/
max(log(1 + spu_purchase_count_30d) in hot_source_pool)
```

说明：

- 收藏数和购买数是次数型指标，头部商品可能明显高于其他商品，因此先用 log(1 + 次数) 做平滑，再归一化。
- CTR 本身已经是比例，不做 log 处理。

#### 12.9.3 C 通路热门分

中文公式：

```text
热门分 =
CTR归一化分 × CTR权重
+ 收藏归一化分 × 收藏权重
+ 购买归一化分 × 购买权重
```

英文字段公式：

```text
hot_score =
ctr_norm_score × ctr_weight
+ wishlist_norm_score × wishlist_weight
+ purchase_norm_score × purchase_weight
```

默认权重：

| 因子 | 权重 | 是否支持配置 |
|---|---:|---:|
| CTR | 2 | 是 |
| 收藏 | 4 | 是 |
| SPU 购买 | 4 | 是 |

说明：

- 三个权重默认合计为 10，因此 hot_score 为 10 分制。
- 收藏和购买权重大于点击。
- 权重支持配置。
- C 通路在 Best Sellers Tab 中按 hot_score 展示。
- C 通路在 For You 中仅作为候选来源，不直接复用 Best Sellers 的最终展示顺序。

### 12.10 用户状态对应配额

For You 每页默认返回 20 个 listing。

各状态默认目标配额：

| 状态 | A1 当前 Session 兴趣 | A2 24h 近期兴趣 | B 新上架 | C Best Sellers |
|---|---:|---:|---:|---:|
| S0 | 0% | 0% | 60% | 40% |
| S1 | 10% | 20% | 35% | 35% |
| S2 | 25% | 25% | 25% | 25% |
| S3 | 40% | 30% | 15% | 15% |

说明：

- S1 中 A2 可高于 A1，因为轻兴趣用户当前 Session 行为可能很少，24h 近期兴趣更稳定。
- 所有配额均支持配置化。
- 配额用于控制最终返回结果，不代表召回数量。

### 12.11 For You 召回阶段规则

```text
用户请求 For You
↓
读取 session_id、user_key、market_id、channel_id
↓
读取 / 计算 recommend_user_interest_24h（本次新增，见§20.4）
↓
判断 user_state = S0 / S1 / S2 / S3
↓
读取 user_state 对应 A1/A2/B/C 目标配额
↓
构建 base_pool
↓
A1：当前 Session 点击 + 收藏基准，相似召回 Top 200
↓
A2：24h 点击 + 收藏基准，剔除当前 Session 行为商品后，相似召回 Top 300
↓
B：New Arrivals 商品池召回 Top 500
↓
C：Best Sellers 商品池召回 Top 500
↓
合并 A1/A2/B/C 候选
↓
按 listing_id 跨通路去重
↓
执行过滤：当前 Session 已展示、24h 曝光频控、间隔去重、不可售等
↓
混排位置分配（加权轮询，含内联打散检查，见下方 mix-ranking 设计和 §12.14）
↓
通路不足时执行配额释放
↓
返回 20 个 listing
```

召回数量默认值：

| 通路 | 默认召回数量 | 说明 |
|---|---:|---|
| A1 | Top 200 | 当前 Session 兴趣，候选损耗较大 |
| A2 | Top 300 | 24h 近期兴趣，覆盖更宽 |
| B | Top 500 | 新上架商品池 |
| C | Top 500 | Best Sellers 商品池 |

召回数量故意放大，用于覆盖以下损耗：

1. A1/A2/B/C 跨通路去重；
2. 当前 Session 已展示 listing 过滤；
3. 同一 listing 24h 曝光频控；
4. 间隔 X 个商品内不重复推荐同一 listing；
5. 同品牌、同系列、同类目、同价格带打散；
6. 不可售、无图、价格无效商品过滤；
7. 某通路基准不足或候选不足。

#### 12.11.1 mix-ranking 位置分配设计

在过滤完成后，使用加权轮询（weighted round-robin）分配最终展示位置，同时内联执行打散检查（见 §12.14），两步合并为单次遍历，不额外增加遍历开销。

**分配原则：**

- 按各通路配额比例，将 20 个位置均匀分配给各通路，避免同通路候选连续堆积
- A1/A2 具有高于 B/C 的位置优先权，优先填充靠前位置
- B/C 候选分散填充中后段槽位，形成"兴趣推荐为主、发现为辅"的位置结构

**参考位置模式（以 S3 状态 A1:A2:B:C = 8:6:3:3 为例）：**

```text
位置:  1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20
通路: A1  A2  A1  A2  A1  A2  B   A1  C   A2  A1  A2  B   C   A1  A2  B   C   A1  —
```

实际分配使用加权轮询算法，各通路获得位置数与配额比例一致，上述仅为示意。

**打散检查内联在混排过程中执行（§12.14）**，每选一个候选商品时同步检查打散约束，不满足则跳过取该通路下一个候选，不另起独立的打散遍历。

### 12.12 过滤与去重规则

| 规则 | 默认值 | 说明 | 是否支持配置 |
|---|---:|---|---:|
| 当前 Session 已展示过滤 | 开启 | 当前推荐 Session 已展示 listing 不再返回 | 是 |
| 24h 曝光频控 | 3 次 | 同一 user_key 下，同一 listing 24h 内 For You 曝光次数达到 3 次后不再返回 | 是 |
| 间隔去重 | 100 个商品 | 同一 listing 在最近 100 个已展示商品内不得重复返回 | 是 |
| 跨通路去重 | 开启 | A1/A2/B/C 按 listing_id 去重 | 是 |
| 不可售过滤 | 开启 | listing_status / product_status 不可售不返回 | 是 |
| 无图过滤 | 开启 | main_image_url 为空不返回 | 是 |
| 价格过滤 | 开启 | listing_price <= 0 不返回 | 是 |
| 成色过滤 | 开启 | grade 为空不返回 | 是 |

说明：

- “当前 Session 已展示过滤”优先级高于间隔去重。
- 间隔去重用于兜底处理超长浏览场景，避免用户刷很久后短时间内又看到同一 listing。
- 如果当前 Session 已展示过滤开启，则同一 Session 内理论上不会重复；间隔去重主要用于跨 Session 或使用历史候选池兜底时控制重复。

### 12.13 配额释放机制

任一通路出现以下情况，视为该通路可用候选不足：

- 无基准商品；
- 召回结果为空；
- 召回结果被过滤后不足目标数量；
- 召回结果被打散规则消耗后不足目标数量。

释放规则：

```text
缺失配额
由其他仍有可用候选的通路
按原目标配额比例吸收
```

示例：

S3 原始配额：

| 通路 | 目标 |
|---|---:|
| A1 | 40% |
| A2 | 30% |
| B | 15% |
| C | 15% |

返回 20 个商品，对应：

| 通路 | 目标数量 |
|---|---:|
| A1 | 8 |
| A2 | 6 |
| B | 3 |
| C | 3 |

如果 A1 只能返回 5 个，缺 3 个。

剩余通路按 A2:B:C = 30:15:15 = 2:1:1 吸收。

调整后尽量返回：

| 通路 | 调整后数量 |
|---|---:|
| A1 | 5 |
| A2 | 8 |
| B | 4 |
| C | 3 |

若 A1、A2 均无可用候选，则缺口由 B 和 C 按原比例吸收。

### 12.14 打散规则

打散与混排位置分配（§12.11.1）合并为单次遍历，内联执行，不额外增加遍历开销。

**执行方式：**

每个槽位通过加权轮询确定应从哪个通路取商品后，取出该通路队首候选，立即检查以下配置的打散约束：

- 若满足所有约束 → 放入该槽位，推进该通路队列指针
- 若不满足某项约束 → 跳过该候选，取该通路下一个候选继续检查
- 若该通路候选全部检查后均不满足 → 降级到下一优先级通路补位
- 全部通路均无法满足约束时 → 放宽约束，将最近跳过的候选补入该槽位（不因打散返回不可售或已展示商品）

**打散维度与默认值（均可配置，见 §24.9）：**

| 维度 | 配置项 | 默认最大连续数 | 说明 |
|---|---|---:|---|
| 品牌 | max_consecutive_same_brand | 2 | 同 brand_id 连续最多 2 个 |
| 系列 | max_consecutive_same_series | 1 | 同 series_id 连续最多 1 个；series_id 为空不参与限制 |
| 后台类目 | max_consecutive_same_category | 3 | 同 backend_category_id 连续最多 3 个 |
| 价格带 | max_consecutive_same_price_band | 4 | 保持价格层次多样性 |

维度是否启用及各维度的最大连续数均通过 §24.9 配置项控制，不需修改代码。

### 12.15 无限流与兜底规则

For You 不展示结束状态。

每次加载默认返回 20 个 listing。

当本次召回 + 混排无法得到 20 个新商品时，按以下顺序兜底：

| 顺序 | 兜底方式 | 说明 |
|---:|---|---|
| 1 | 使用本次 A1/A2/B/C 剩余候选继续补足 | 排除已展示、超频、不可售商品 |
| 2 | 使用上一推荐请求未展示候选池 | 剔除已经展示的 20 个及之后已展示商品 |
| 3 | 对上一候选池中用户点击 / 收藏过的商品重新做相似召回 | 仍按 A1/A2 相似逻辑执行 |
| 4 | 使用 B New Arrivals 扩大候选池 | 从更靠后的新上架商品中补 |
| 5 | 使用 C Best Sellers 扩大候选池 | 从更靠后的热门商品中补 |
| 6 | 使用基础商品池稳定排序兜底 | 按 listed_at desc + listing_id asc 补足 |

说明：

- 兜底仍必须遵守可售、无图、价格有效、成色有效规则。
- 兜底仍尽量遵守当前 Session 已展示过滤、曝光频控和间隔去重。
- 若极端情况下仍不足 20 个，可返回实际数量，但前端不展示结束态，下次加载继续请求。
- New Arrivals Tab 同样不展示结束态，可使用更深分页的新上架商品或基础商品池排序兜底。

### 12.16 For You 返回规则

| 项目 | 规则 |
|---|---|
| 每页目标数量 | 20 个 listing |
| A1 召回数量 | 默认 Top 200 |
| A2 召回数量 | 默认 Top 300 |
| B 召回数量 | 默认 Top 500 |
| C 召回数量 | 默认 Top 500 |
| 候选池数量 ≥ 20 | 混排后返回 20 个 |
| 候选池数量 < 20 | 进入无限流兜底逻辑 |
| 是否允许重复 listing | 默认不允许 |
| 是否允许当前 Session 已展示 listing 再次返回 | 默认不允许 |
| 是否允许 24h 曝光超频 listing 返回 | 默认不允许 |
| 是否保存推荐结果 | 保存逻辑结果用于排查与分析；具体物理存储由研发决定 |

### 12.17 推荐案例

用户最近 24h 行为：

| 行为 | 商品 | 数量 |
|---|---|---:|
| 点击 | Rolex Datejust、Omega Speedmaster | 2 |
| 收藏 | LV Neverfull | 1 |
| 购买 | Chanel CF | 1 |

兴趣分：

```text
interest_score_24h =
点击 2 × 1
+ 收藏 1 × 3
+ 购买 1 × 10
= 15
```

用户状态：

```text
S3 强兴趣用户
```

S3 配额：

| 通路 | 配额 | 20 个商品目标数量 |
|---|---:|---:|
| A1 | 40% | 8 |
| A2 | 30% | 6 |
| B | 15% | 3 |
| C | 15% | 3 |

当前 Session 行为：

| 行为 | 商品 |
|---|---|
| 收藏 | LV Neverfull |
| 点击 | Rolex Datejust |

A1 基准：

```text
LV Neverfull
Rolex Datejust
```

最近 24h 行为：

| 行为 | 商品 |
|---|---|
| 收藏 | LV Neverfull |
| 点击 | Rolex Datejust、Omega Speedmaster |

A2 先剔除当前 Session 已发生行为：

```text
LV Neverfull
Rolex Datejust
```

A2 剩余基准：

```text
Omega Speedmaster
```

召回结果：

| 通路 | 召回数量 | 过滤后可用 |
|---|---:|---:|
| A1 | 200 | 5 |
| A2 | 300 | 80 |
| B | 500 | 300 |
| C | 500 | 260 |

A1 目标 8，但只有 5，缺 3。

缺口由 A2、B、C 按原配额 30:15:15 吸收。

最终返回示例：

| 通路 | 最终数量 |
|---|---:|
| A1 | 5 |
| A2 | 8 |
| B | 4 |
| C | 3 |
| 合计 | 20 |

最终 20 个商品还需执行打散：

- 同品牌连续不超过 2 个；
- 同系列连续不超过 1 个；
- 同后台类目连续不超过 3 个；
- 同价格带连续不超过 4 个；
- 同一 listing 在最近 100 个已展示商品内不得重复出现。

---

## 13. New Arrivals 规则

### 13.1 功能描述

New Arrivals 用于展示当前 Market + Channel 下最新上架的可售商品。

### 13.2 排序规则

中文规则：

```text
新上架商品 =
基础商品池
+ listed_at 不为空
+ listed_at 在近 b_freshness_days 天内（默认 30 天）
按 listed_at 倒序
同 listed_at 时按 listing_price 倒序
再同时按 listing_id 正序
```

英文字段规则：

```text
new_arrivals =
base_pool
where listed_at is not null
  and listed_at >= now() - interval b_freshness_days day
order by listed_at desc, listing_price desc, listing_id asc
```

### 13.3 字段来源

| 字段 | 来源 | 说明 |
|---|---|---|
| listing_id | listing | 推荐对象 |
| listed_at | 推荐快照 | listing 首次上架成功时间 / 首次变为 active 的时间 |
| listing_status | listing | 可售过滤 |
| product_status | product | 可售过滤 |
| listing_price | listing | 价格有效过滤 |
| main_image_url | product_image / listing.og_image_url | 图片有效过滤 |
| grade | 商品系统成色等级（字段名待确认），枚举：NWT / Excellent / Good / Fair | 成色有效过滤 |

### 13.4 与 For You 的关系

New Arrivals Tab 使用 B 通路商品池。

For You 中的 B 通路复用 New Arrivals 商品池，但不复用 New Arrivals 的最终展示顺序。

### 13.5 New Arrivals 无限流兜底

New Arrivals 不展示结束状态。

当最新上架商品不足 20 个时：

1. 继续向更早 listed_at 的商品分页（超出 b_freshness_days 窗口后继续分页历史商品）；
2. 过滤已展示商品；
3. 若全部新上架商品已在当前 Session 内展示完毕，从 listed_at 最新的商品重新循环，跳过当前 Session 已展示的（即回到第一页重新过一遍，已展示的自动跳过）；
4. 极端情况下返回实际数量，但前端不展示结束态。

---

## 14. Best Sellers 规则

### 14.1 当前判断

Best Sellers 不建议在 MVP 直接按 listing 购买数上线。

原因：

Looply 是一物一码业务，单个 listing 通常只能售出一次；如果直接按 listing 购买数排序，会导致绝大多数商品购买数为 0 或 1，区分度不足。

### 14.2 推荐口径

Best Sellers 使用 C 通路逻辑。

Best Sellers 的商品排序不是简单销量榜，而是综合：

```text
CTR
+ 收藏数
+ SPU 购买数
```

计算 10 分制 hot_score。

### 14.3 与 For You 的关系

Best Sellers Tab 使用 C 通路商品池。

For You 中的 C 通路复用该商品池，但不复用 Best Sellers 的最终展示顺序。

### 14.4 Best Sellers 无限流兜底

Best Sellers 不展示结束状态。

当当前候选池（默认 impression_top_k = 2000）展示完毕时：

1. 扩展候选池至下一批 2000（按 impression_session_count_7d 排序的第 2001–4000 名），使用相同 hot_score 计算逻辑；
2. 若下一批 2000 也已展示完毕，继续扩展至再下一批，依此类推；
3. 若商品池真正耗尽（全部可售商品均已展示），从 hot_score 最高商品重新循环，跳过当前 Session 已展示的；
4. 极端情况下返回实际数量，但前端不展示结束态。

---

## 15. Deals 规则

### 15.1 当前判断

Deals 依赖促销价、降价记录、营销活动配置等能力。当前商品系统不应由 Feed 自行创造折扣字段。

### 15.2 依赖字段

| 字段 | 来源 | 当前状态 |
|---|---|---|
| promotion_price | 营销系统 | 待建设 |
| price_drop | 营销 / 价格记录 | 待建设 |
| promotion_start_at | 营销系统 | 待建设 |
| promotion_end_at | 营销系统 | 待建设 |
| listing_price | listing | 已有 |

### 15.3 推荐口径

MVP 可隐藏 Deals Tab。

若展示 Deals，必须确保营销系统已经提供明确促销价或降价记录，Feed 只消费结果，不自行计算营销状态。

---

## 16. 商品卡字段

### 16.1 商品卡展示字段

| 页面展示 | 字段 | 来源 | 是否已有 / 处理方式 |
|---|---|---|---|
| 商品图片 | main_image_url | product_image / listing.og_image_url | 推荐侧快照派生 |
| 品牌名 | brand_id / brand name | listing → product → standard_sku → spu → brand | 链路可取 |
| 商品标题 | listing_title | listing | 商品系统已有展示标题概念 |
| 当前价格 | listing_price | listing | 已有 |
| 货币 | currency_code | listing / Market | 已有 |
| 成色 | grade | 商品系统成色等级，枚举：NWT / Excellent / Good / Fair | 快照表同步，源字段名待确认 |
| 收藏状态 | wishlist relation | 收藏模块 | 待确认 |
| 鉴定标识 | is_authenticated | product_inspection | 可用于 V1.1 展示 |
| Sold Out | listing_status / product_status | 商品系统 | MVP 不主动展示不可售商品 |

### 16.2 商品卡点击

| 行为 | 规则 |
|---|---|
| 点击商品卡 | 跳转商品详情页 |
| 跳转参数 | listing_id |
| 埋点事件 | product_card_click |
| 推荐作用 | 进入用户状态统计；作为 A1/A2 相似召回基准 |

---

## 17. 收藏规则

| 场景 | 规则 |
|---|---|
| 已登录用户点击收藏 | 调用收藏模块写入 wishlist |
| 未登录用户点击收藏 | 触发登录 / 注册引导 |
| 收藏成功 | 记录 wishlist_add |
| 取消收藏 | 记录 wishlist_remove |
| 推荐使用 | wishlist_add 进入用户状态统计、A1/A2 基准、C 通路热门分 |
| 不使用项 | 不把 wishlist_click 当成收藏关系 |

说明：

收藏关系只以 wishlist_add 成功结果为准。

wishlist_click 仅作为行为埋点，用于分析未登录收藏意图、登录弹窗转化和收藏漏斗，不进入 A1/A2 基准。

---

## 18. 分页与加载更多

| 项目 | 规则 |
|---|---|
| 每页数量 | 默认 20 个 listing |
| 加载方式 | 下滑加载更多 |
| 请求参数 | session_id、anonymous_user_id、tab、page_index、page_size、market_id、channel_id |
| 去重规则 | 当前 Session 已展示 listing 不再返回 |
| 曝光频控 | 同一 user_key 下同一 listing 24h 内 For You 曝光次数达到配置阈值后不再返回 |
| 间隔去重 | 同一 listing 在最近 X 个已展示商品内不得重复返回 |
| 空态 | 当前 Tab 首屏无任何商品时展示空态 |
| 结束态 | 不展示结束态，按无限流兜底规则继续加载 |

---

## 19. 埋点事件

| 事件 | 中文意思 | 触发时机 | 关键字段 | 用途 |
|---|---|---|---|---|
| product_card_impression | 商品卡曝光 | 商品卡进入可视区域 | session_id、anonymous_user_id、user_id、listing_id、tab、page_index、position | 曝光统计、CTR 分母、去重、频控 |
| product_card_click | 商品卡点击 | 点击商品卡进入商详 | session_id、anonymous_user_id、user_id、listing_id、tab、page_index、position | A1/A2 基准、CTR 分子、24h 用户状态 |
| wishlist_click | 点击收藏按钮 | 用户点击商品卡上的收藏按钮 | session_id、anonymous_user_id、user_id、listing_id、tab | 收藏漏斗 |
| wishlist_add | 收藏成功 | 收藏模块确认收藏写入成功 | session_id、anonymous_user_id、user_id、listing_id、tab | A1/A2 基准、收藏热度、24h 用户状态 |
| wishlist_remove | 取消收藏 | 用户取消收藏成功 | session_id、anonymous_user_id、user_id、listing_id、tab | 负反馈分析，MVP 先不进入状态分 |
| feed_tab_switch | Tab 切换 | 用户切换 Feed Tab | session_id、anonymous_user_id、user_id、from_tab、to_tab | 分析用户偏好哪个 Tab |
| feed_load_more | 加载更多 | 用户请求下一屏 | session_id、anonymous_user_id、tab、page_index | 浏览深度、请求日志 |
| scroll_depth | 页面滚动深度 | 用户滚动页面 | session_id、anonymous_user_id、tab、depth | Feed 吸引力分析 |
| purchase_complete | 购买完成 | 订单完成支付后触发（触发点在商详/结账页，不在首页 Feed；Feed 侧消费此事件数据） | user_id、anonymous_user_id、listing_id、product_id、spu_id、order_id | 用户状态分、Best Sellers 购买热度 |

---

## 20. 推荐侧新增数据对象

### 20.0 说明

以下为推荐逻辑所需的数据结构设计，用于表达产品规则、字段来源和数据关系。

PRD 不强制要求研发必须按以下名称创建物理数据库表。

实际研发实现可根据数据量、成本和架构选择：

```text
MySQL
Redis
ClickHouse
Elasticsearch
数据仓库
日志系统
缓存
```

本 PRD 中的表名和字段名作为逻辑参考。

### 20.1 recommend_behavior_event_log（本次新增）

作用：

记录 Feed 行为原始日志，是推荐召回、24h 用户状态、曝光频控、CTR、Best Sellers 统计的基础。

| 字段 | 说明 |
|---|---|
| event_id | 行为事件 ID |
| session_id | 推荐侧浏览会话 ID |
| user_id | 已登录用户 ID，未登录为空 |
| anonymous_user_id | 未登录匿名访问标识 |
| user_key | 推荐侧用户识别键，已登录用 user_id，未登录用 anonymous_user_id |
| market_id | 行为发生 Market |
| channel_id | 行为发生 Channel |
| event_type | 行为类型 |
| listing_id | 行为关联 listing |
| product_id | 可从 listing 关联 product，允许异步补齐 |
| spu_id | 可从 product → standard_sku → spu 关联，购买统计使用 |
| tab | 行为发生的 Feed Tab |
| page_index | 当前第几屏 |
| position | 商品在当前屏位置 |
| event_time | 行为发生时间 |

event_type 枚举：

| 枚举值 | 含义 | 是否进入用户状态 | 是否进入 A1/A2 基准 |
|---|---|---:|---:|
| product_card_impression | 商品曝光 | 否 | 否 |
| product_card_click | 商品点击 | 是 | 是 |
| wishlist_click | 点击收藏按钮 | 否 | 否 |
| wishlist_add | 收藏成功 | 是 | 是 |
| wishlist_remove | 取消收藏 | 否 | 否 |
| feed_tab_switch | Tab 切换 | 否 | 否 |
| feed_load_more | 加载更多 | 否 | 否 |
| scroll_depth | 滚动深度 | 否 | 否 |
| purchase_complete | 购买完成 | 是 | 否 |

### 20.2 recommend_listing_feature_snapshot（本次新增）

作用：

推荐侧商品特征快照表，供 A1/A2/B/C 快速查询，不直接实时 join 商品系统多张表。

| 字段 | 说明 |
|---|---|
| listing_id | 推荐对象 |
| product_id | 关联实物商品 |
| standard_sku_id | 关联标品 SKU |
| spu_id | 关联 SPU |
| brand_id | 品牌 |
| series_id | 系列，允许为空 |
| backend_category_id | 后台类目 |
| listing_price | 挂牌价 |
| currency_code | 货币 |
| price_band | 推荐侧派生价格带 |
| grade | 成色等级，来源：商品系统成色等级字段（源字段名待确认）；枚举：NWT / Excellent / Good / Fair |
| listing_status | listing 状态 |
| product_status | product 状态 |
| main_image_url | 主图 |
| listed_at | 首次上架成功时间 |
| snapshot_updated_at | 快照更新时间 |

### 20.3 recommend_listing_stats（本次新增）

作用：

推荐侧 listing 热门统计表，支撑 C 通路和 Best Sellers。

| 字段 | 说明 |
|---|---|
| listing_id | 统计对象 |
| spu_id | 购买热度继承维度 |
| market_id | 市场 |
| channel_id | 渠道 |
| impression_session_count_7d | 近 7 天曝光 session 数 |
| click_session_count_7d | 近 7 天点击 session 数 |
| wishlist_add_count_7d | 近 7 天收藏成功数 |
| spu_purchase_count_30d | 近 30 天 SPU 购买数 |
| ctr_7d | 点击率 |
| ctr_norm_score | CTR 归一化分 |
| wishlist_norm_score | 收藏归一化分 |
| purchase_norm_score | 购买归一化分 |
| hot_score | Best Sellers 热门分 |
| stats_updated_at | 统计更新时间 |

说明：

购买热度按 SPU 维度统计，再回填到同 SPU 下可售 listing。

### 20.4 recommend_user_interest_24h（本次新增）

作用：

存储 user_key 最近 24h 兴趣聚合，用于快速判断 S0/S1/S2/S3，并为 A2 生成基准商品。

| 字段 | 说明 |
|---|---|
| user_key | 推荐侧用户识别键 |
| user_key_type | user / anonymous |
| market_id | 市场 |
| channel_id | 渠道 |
| click_count_24h | 最近 24h 点击数 |
| wishlist_add_count_24h | 最近 24h 收藏成功数 |
| purchase_count_24h | 最近 24h 购买数 |
| interest_score_24h | 最近 24h 兴趣分 |
| user_state | S0 / S1 / S2 / S3 |
| recent_click_listing_ids | 最近 24h 点击 listing 列表，按时间倒序，原始包含当前 Session |
| recent_wishlist_listing_ids | 最近 24h 收藏 listing 列表，按时间倒序，原始包含当前 Session |
| updated_at | 更新时间 |

说明：

A2 使用 recent_click_listing_ids / recent_wishlist_listing_ids 时，必须结合当前 Session 行为集合，先剔除当前 Session 已点击 / 收藏的 listing。

### 20.5 recommend_request_log（本次新增）

作用：

记录每次推荐请求，用于排查、分析和实验。

| 字段 | 说明 |
|---|---|
| request_id | 推荐请求 ID |
| session_id | 推荐侧 Session |
| user_key | 推荐侧用户识别键 |
| user_key_type | user / anonymous |
| market_id | 市场 |
| channel_id | 渠道 |
| tab | 当前 Tab |
| user_state | S0 / S1 / S2 / S3 |
| page_index | 第几屏 |
| page_size | 请求数量 |
| a1_target_ratio | A1 目标配额 |
| a2_target_ratio | A2 目标配额 |
| b_target_ratio | B 目标配额 |
| c_target_ratio | C 目标配额 |
| request_time | 请求时间 |

### 20.6 recommend_result_log（本次新增）

作用：

记录推荐返回结果，用于排查、曝光分析、CTR 计算、AB 实验和频控。

| 字段 | 说明 |
|---|---|
| request_id | 推荐请求 ID |
| listing_id | 返回 listing |
| position | 最终位置 |
| recall_path_codes | 命中的召回通路，可能包含 A1/A2/B/C |
| primary_recall_path_code | 最终占用配额的通路 |
| final_score | 混排后分数或排序分 |
| is_exposed | 前端是否实际曝光 |
| exposed_at | 曝光时间 |
| created_at | 结果生成时间 |

说明：

结果明细数据量较大，具体是否逐行落库、压缩为 JSON、采样或进入日志系统，由研发决定。

### 20.7 recommend_exposure_control（本次新增）

作用：

记录或支撑曝光频控，避免同一 listing 在 24h 内反复展示给同一 user_key。

| 字段 | 说明 |
|---|---|
| user_key | 推荐侧用户识别键 |
| user_key_type | user / anonymous |
| listing_id | listing |
| market_id | 市场 |
| channel_id | 渠道 |
| exposure_count_24h | 最近 24h For You 曝光次数 |
| last_exposed_at | 最近一次曝光时间 |
| updated_at | 更新时间 |

说明：

该对象也可通过 recommend_result_log 或行为日志聚合实现。PRD 只定义需要具备“同一 listing 24h 曝光次数判断能力”。

---

## 21. 异常与降级

| 场景 | 处理方式 |
|---|---|
| For You 推荐失败 | 降级 New Arrivals 或基础商品池 |
| user_state 计算失败 | 默认 S0，使用 B/C |
| A1 无基准商品 | A1 不触发，配额释放给 A2/B/C |
| A2 剔除当前 Session 行为商品后无基准 | A2 不触发，配额释放给 A1/B/C |
| A1/A2 均无基准 | 使用 B/C |
| B 无新上架候选 | 使用 A1/A2/C |
| C 无 Best Sellers 候选 | 使用 A1/A2/B |
| 任一通路候选不足 | 缺口由其他可用通路按比例补齐 |
| 四通路候选不足 20 | 进入无限流兜底逻辑 |
| 商品无图 | 不进入基础商品池 |
| 商品价格无效 | 不进入基础商品池 |
| 商品状态不可售 | 不进入基础商品池 |
| 当前 Session 已展示 | 不重复返回 |
| 24h 曝光达到配置阈值 | 不再返回 |
| 间隔 X 个商品内已出现过 | 不再返回 |
| 收藏接口失败 | Toast 提示失败，不记录 wishlist_add，不进入 A1/A2 基准 |
| 埋点失败 | 不阻塞用户浏览，客户端重试或降级丢弃 |
| 推荐配置读取失败 | 使用系统默认配置 |
| 结果日志写入失败 | 不阻塞推荐返回 |

---

## 22. MVP 范围

| 项目 | MVP 是否包含 |
|---|---:|
| For You Tab | 是 |
| New Arrivals Tab | 是 |
| Best Sellers Tab | 是 |
| Deals Tab | 一期暂时留空 |
| 商品卡基础展示 | 是 |
| 收藏入口 | 是 |
| Feed 曝光 / 点击 / 收藏埋点 | 是 |
| 推荐 Session | 是 |
| anonymous_user_id 匿名识别 | 是 |
| 24h 用户状态分层 | 是 |
| A1 当前 Session 兴趣相似召回 | 是 |
| A2 24h 近期兴趣相似召回 | 是 |
| B New Arrivals 召回 | 是 |
| C Best Sellers 召回 | 是 |
| 统一混排 | 是 |
| 配额释放 | 是 |
| 当前 Session 去重 | 是 |
| 24h 单商品曝光频控 | 是 |
| 间隔 X 个商品内不重复推荐 | 是 |
| 品牌 / 系列 / 类目 / 价格带打散 | 是 |
| 无限流兜底 | 是 |
| 长期用户画像 | 否 |
| 向量召回 | 否 |
| 深度学习精排 | 否 |
| 运营后台配置界面 | 否，先配置表维护 |

---

## 23. 后续迭代方向

| 版本 | 能力 |
|---|---|
| V1.1 | 增加运营配置后台、Tab 开关、推荐权重配置 |
| V1.2 | 增加用户长期兴趣画像 |
| V1.3 | 增加搜索意图召回 |
| V1.4 | 增加 A/B 实验与推荐效果看板 |
| V2.0 | 增加 embedding / 向量召回 |
| V2.1 | 增加更精细的多样性控制和探索流量策略 |
| V2.2 | 增加 Deals / 营销活动召回 |

---

## 24. 配置项总表

### 24.1 配置项必备维度

所有推荐配置至少需要支持以下维度：

| 维度 | 是否必备 | 说明 |
|---|---:|---|
| config_key | 是 | 配置项名称 |
| config_value | 是 | 配置项值 |
| value_type | 是 | number / string / boolean / json |
| market_id | 是 | 支持按 Market 配置；为空时表示系统默认值 |
| channel_id | 是 | 支持按 Channel 配置；为空时表示 Market 默认值 |
| status | 是 | active / inactive |
| effective_at | 是 | 生效时间 |
| updated_by | 是 | 修改人 |
| updated_at | 是 | 修改时间 |
| remark | 否 | 备注 |

配置读取优先级：

```text
Market + Channel 专属配置
>
Market 默认配置
>
系统默认配置
```

### 24.2 用户状态配置

| 模块 | 配置项 | 默认值 | 说明 |
|---|---|---:|---|
| 用户状态 | click_weight | 1 | 点击行为权重 |
| 用户状态 | wishlist_add_weight | 3 | 收藏成功权重 |
| 用户状态 | purchase_weight | 10 | 购买权重 |
| 用户状态 | s1_min_score | 1 | S1 起始分 |
| 用户状态 | s2_min_score | 5 | S2 起始分 |
| 用户状态 | s3_min_score | 15 | S3 起始分 |

### 24.3 用户状态配额配置

| 模块 | 配置项 | 默认值 | 说明 |
|---|---|---:|---|
| S0 配额 | s0_a1_ratio | 0 | S0 A1 配额 |
| S0 配额 | s0_a2_ratio | 0 | S0 A2 配额 |
| S0 配额 | s0_b_ratio | 60 | S0 B 配额 |
| S0 配额 | s0_c_ratio | 40 | S0 C 配额 |
| S1 配额 | s1_a1_ratio | 10 | S1 A1 配额 |
| S1 配额 | s1_a2_ratio | 20 | S1 A2 配额 |
| S1 配额 | s1_b_ratio | 35 | S1 B 配额 |
| S1 配额 | s1_c_ratio | 35 | S1 C 配额 |
| S2 配额 | s2_a1_ratio | 25 | S2 A1 配额 |
| S2 配额 | s2_a2_ratio | 25 | S2 A2 配额 |
| S2 配额 | s2_b_ratio | 25 | S2 B 配额 |
| S2 配额 | s2_c_ratio | 25 | S2 C 配额 |
| S3 配额 | s3_a1_ratio | 40 | S3 A1 配额 |
| S3 配额 | s3_a2_ratio | 30 | S3 A2 配额 |
| S3 配额 | s3_b_ratio | 15 | S3 B 配额 |
| S3 配额 | s3_c_ratio | 15 | S3 C 配额 |

### 24.4 A1 通路配置

| 模块 | 配置项 | 默认值 | 说明 |
|---|---|---:|---|
| A1 基准 | a1_interest_seed_count | 5 | A1 基准商品数量 |
| A1 召回 | a1_recall_top_k | 200 | A1 召回截断 |
| A1 相似分 | a1_series_match_score | 3.0 | 系列相似分 |
| A1 相似分 | a1_brand_match_score | 2.5 | 品牌相似分 |
| A1 相似分 | a1_category_match_score | 2.0 | 类目相似分 |
| A1 相似分 | a1_grade_match_score | 1.0 | 成色相似分 |
| A1 相似分 | a1_same_price_band_score | 1.5 | 同价格带分 |
| A1 相似分 | a1_adjacent_price_band_score | 0.8 | 相邻价格带分 |

### 24.5 A2 通路配置

| 模块 | 配置项 | 默认值 | 说明 |
|---|---|---:|---|
| A2 基准 | a2_interest_seed_count | 5 | A2 基准商品数量 |
| A2 召回 | a2_recall_top_k | 300 | A2 召回截断 |
| A2 相似分 | a2_series_match_score | 3.0 | 系列相似分 |
| A2 相似分 | a2_brand_match_score | 2.5 | 品牌相似分 |
| A2 相似分 | a2_category_match_score | 2.0 | 类目相似分 |
| A2 相似分 | a2_grade_match_score | 1.0 | 成色相似分 |
| A2 相似分 | a2_same_price_band_score | 1.5 | 同价格带分 |
| A2 相似分 | a2_adjacent_price_band_score | 0.8 | 相邻价格带分 |

### 24.6 B 通路配置

| 模块 | 配置项 | 默认值 | 说明 |
|---|---|---:|---|
| B 召回 | b_recall_top_k | 500 | New Arrivals 候选池召回数量 |
| B 排序 | b_sort_by | listed_at_desc | 默认按 listed_at 倒序 |
| B 新鲜度 | b_freshness_days | 30 | 商品上架有效天数窗口，超出此天数的商品不进入 B 通路候选池 |

### 24.7 C 通路配置

| 模块 | 配置项 | 默认值 | 说明 |
|---|---|---:|---|
| C 召回 | c_recall_top_k | 500 | Best Sellers 候选池召回数量 |
| C 曝光候选池 | c_impression_top_k | 2000 | 先按曝光 session 数取 Top K |
| C 权重 | c_ctr_weight | 2 | CTR 权重 |
| C 权重 | c_wishlist_weight | 4 | 收藏权重 |
| C 权重 | c_purchase_weight | 4 | SPU 购买权重 |
| C 归一化 | c_wishlist_log_smooth | true | 收藏数是否使用 log(1+x) 平滑 |
| C 归一化 | c_purchase_log_smooth | true | 购买数是否使用 log(1+x) 平滑 |

### 24.8 过滤与频控配置

| 模块 | 配置项 | 默认值 | 说明 |
|---|---|---:|---|
| Session 去重 | filter_session_exposed | true | 当前 Session 已展示商品不再返回 |
| 24h 曝光频控 | max_listing_exposure_24h | 3 | 同一 listing 24h 内最多展示次数 |
| 间隔去重 | listing_repeat_gap_count | 100 | 同一 listing 在最近 X 个已展示商品内不得重复返回 |
| 跨通路去重 | dedupe_by_listing_id | true | A1/A2/B/C 按 listing_id 去重 |
| 可售过滤 | filter_unavailable_listing | true | 不可售商品不返回 |
| 图片过滤 | filter_empty_main_image | true | 无主图商品不返回 |
| 价格过滤 | filter_invalid_price | true | listing_price <= 0 不返回 |
| 成色过滤 | filter_empty_grade | true | grade 为空不返回 |

### 24.9 打散配置

| 模块 | 配置项 | 默认值 | 说明 |
|---|---|---|---|
| 打散维度开关 | scatter_enabled_dimensions | brand,series,category,price_band | 启用的打散维度列表，逗号分隔；可按需增减或置空（置空则关闭打散） |
| 品牌打散 | max_consecutive_same_brand | 2 | 同品牌连续最多 2 个 |
| 系列打散 | max_consecutive_same_series | 1 | 同系列连续最多 1 个 |
| 类目打散 | max_consecutive_same_category | 3 | 同后台类目连续最多 3 个 |
| 价格带打散 | max_consecutive_same_price_band | 4 | 同价格带连续最多 4 个 |

### 24.10 无限流兜底配置

| 模块 | 配置项 | 默认值 | 说明 |
|---|---|---:|---|
| 无限流 | page_size | 20 | 每次默认返回 20 个 listing |
| 无限流 | enable_previous_candidate_pool_fallback | true | 是否允许使用上一请求未展示候选池 |
| 无限流 | enable_previous_interest_similar_fallback | true | 是否允许对上一候选池中用户点击 / 收藏过的商品重新做相似召回 |
| 无限流 | enable_base_pool_fallback | true | 是否允许使用基础商品池稳定排序兜底 |
| 无限流 | base_pool_fallback_sort | listed_at_desc_listing_id_asc | 基础商品池兜底排序 |

---
