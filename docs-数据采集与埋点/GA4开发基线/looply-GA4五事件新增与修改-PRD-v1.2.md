# Looply GA4 五事件新增与修改 PRD

> 版本：v1.2  
> 日期：2026-08-31  
> 状态：五事件专项实施细则  
> 测试环境：`https://www.test.looply.com/`  
> GA4媒体资源：`Looply-test`  
> Measurement ID：`G-VFBQX6RSB7`

## 一、目标与范围

本文件只定义五事件专项细则，与《looply-GA4数据分析-PRD-v1.8》和《looply-GA4剩余问题收口开发包-v1.4》共同执行。完整事件语义和字段以GA4 PRD v1.8为准；本轮问题、真实入口用例、GTM生产链路证据及发布门禁以收口包v1.4为准。历史GA4 PRD、旧变更清单和旧验收修复单不再作为当前实施依据。

本轮同时适用以下公共要求：事件发生时当前完整URL使用`page_location`，`page_referrer`只表示当前页面实例建立前的真实上一页面；Looply主动`page_view`固定携带`page_view_source=looply_custom`，主动`view_search_results`固定携带`view_search_results_source=looply_custom`。来源字段必须完成Web事件对象、dataLayer、GTM变量、GA4 Event Tag、实际生产容器版本和真实`g/collect`请求的全链路验收，仅验证Web代码或公共函数不能判通过。

本批只处理五个GA4事件：

| 处理类型 | GA4事件 | dataLayer物理事件 |
|---|---|---|
| 调整 | `search` | `looply_ga4_search` |
| 调整 | `view_item_list` | `looply_ga4_view_item_list` |
| 新增或补齐 | `view_search_results` | `looply_ga4_view_search_results` |
| 新增或补齐 | `view_cart` | `looply_ga4_view_cart` |
| 新增或补齐 | `remove_from_cart` | `looply_ga4_remove_from_cart` |

为保证同一页面行为能够关联，现有`page_view`和`select_item`同时补充`page_instance_id`参数，但不改变它们的触发点和业务语义。`purchase`及其他现有GA4事件不属于本批修改范围。

## 二、现状与开发改动

当前已确认浏览器能够向GA4发出请求，但这不代表字段映射和生产容器发布已经闭环。开发按下表定位现有事件并完成对应修改，再按收口包v1.4提供全链路证据。

| GA4事件 | 当前已确认 | 当前问题 | 开发修改目标 |
|---|---|---|---|
| `search` | 请求到达GA4并返回HTTP 204；单次点击只观察到一条；`search_term=chanel`正确 | 缺当前场景`trigger_type=manual_search_button` | 六种正式搜索提交动作各自产生一条`search`，携带唯一`trigger_type`；接口结果不决定是否产生提交事件 |
| `view_search_results` | 成功结果请求到达GA4；已有`result_status=success`、`duration_ms=4395`、`result_count=1590` | 成功结果缺`search_term`和`trigger_type`；直达无结果页未发送`no_results` | 每次结果更新形成一个唯一终态；从当前URL读取搜索上下文；直达URL不补造`search`，但正常产生结果终态 |
| `view_item_list` | 请求到达GA4；`items[].item_id`已使用CP开头的`listing_public_code` | 首屏产生8条事件且每条重复携带全部40件商品；缺页面实例、展示位、商品位置和搜索上下文 | 只上报达到曝光阈值的新商品；按页面实例、展示位和商品去重；每条事件只携带本次实际达标商品 |
| `view_cart` | 非空购物车成功发送；已有`page_instance_id`、`value`和正确商品；同页面未重复发送；空购物车未发送 | 缺`currency` | Shopping Bag和PC Cart Drawer中真实展示非空可购商品时发送，并携带匹配的币种、金额及全部可购商品 |
| `remove_from_cart` | 商品成功删除后发送；商品、实际减少数量1和`value`正确 | 缺`currency` | 商品真实删除成功后发送一次，并携带币种、实际减少金额、价格和数量1 |

## 三、五个事件的最终规则

### 3.1 `search`

用户正式提交一次搜索时发送一条`search`。输入内容变化、仅展示联想、筛选、排序和结果返回均不产生新的`search`。

| `trigger_type` | 用户动作 | 判定边界 |
|---|---|---|
| `carousel_term_button` | 搜索框展示轮播词且用户未改写，直接点击搜索按钮 | 用户改写内容后点击按钮使用`manual_search_button` |
| `manual_enter` | 用户手动输入搜索内容后按回车 | 仅输入未提交不发送 |
| `manual_search_button` | 用户手动输入搜索内容后点击搜索按钮 | 搜索框仍是未改写轮播词时使用`carousel_term_button` |
| `suggestion_select` | 用户点击输入联想中的搜索词建议 | 携带从1开始的`suggestion_position`；有稳定实体ID时可带`suggestion_object_id` |
| `history_select` | 用户点击搜索历史中的搜索词 | 使用该历史词对应的搜索模块正式分析词 |
| `popular_term_select` | 用户点击搜索页热门搜索词 | 热门品牌和热门Collection属于目标页面入口，不发送`search` |

事件参数：

- `search_term`：搜索模块正式输出的清洗后搜索词。
- `trigger_type`：按上表确定。
- `suggestion_position`：仅联想点击场景适用，从1开始。
- `suggestion_object_id`：仅在搜索模块已有稳定实体ID时携带。

### 3.2 `view_search_results`

搜索结果页初始加载或结果URL参数生效后，结果请求形成唯一终态时发送一次。

| `result_status` | 成立条件 | 附加信息 |
|---|---|---|
| `success` | 请求正常完成且结果数大于0 | 携带`result_count` |
| `no_results` | 请求正常完成且结果数为0 | 携带`result_count=0` |
| `failed` | 非Abort错误且重试结束 | 能取得时携带`failure_type` |
| `cancelled` | 被新搜索替换、显式取消或离开页面导致请求中止 | 不伪造结果数或失败类型 |

同一次结果请求只产生一个终态。筛选、排序或Reset实际更新结果后，产生新的结果终态，但不新增`search`。

每条`view_search_results`终态事件生成一个`event_id`；同一终态因发送重试而再次组装时保持同一个值。其他四个事件不要求携带`event_id`，分别按各自的成立与去重规则处理。`event_id`无法取得时省略，事件仍发送。

直达搜索URL、刷新和页面恢复允许直接产生`view_search_results`；没有前序用户提交时不补造`search`。结果事件从当前URL读取可用的`search_term`、`trigger_type`、`filter_ids`和`sort_type`。

`failure_type`使用以下封闭值：

| 枚举值 | 含义 |
|---|---|
| `network_error` | 网络连接错误 |
| `timeout` | 请求超时 |
| `http_error` | HTTP响应错误 |
| `invalid_response` | 响应格式或内容无效 |
| `unknown` | 无法归入以上类型的安全兜底 |

### 3.3 `view_item_list`

单件商品达到50%可视且持续1秒时形成有效曝光：

- 后台、页面失焦或未达到阈值不发送。
- 同一`page_instance_id`内，按`placement_id + listing_public_code`去重。
- 每条事件只携带本次实际达到曝光阈值的商品，不重复携带整页商品数组。
- `items[].index`取筛选、排序和插入完成后的业务列表位置，从1开始。
- 搜索结果页的曝光从当前URL读取可用的搜索词、触发方式、筛选和排序上下文。

`placement_id`使用以下封闭值：

| 商品展示位置 | `placement_id` |
|---|---|
| 首页For You | `home_feed_for_you` |
| 首页New Arrivals | `home_feed_new_arrivals` |
| Collection商品列表 | `collection_results` |
| 搜索结果列表 | `search_results` |
| 搜索无结果推荐 | `search_no_results_recommendations` |
| 商详You May Also Like | `product_you_may_also_like` |
| 商详Recently Viewed | `product_recently_viewed` |
| PC＋Mobile Wishlist | `favorites_wishlist` |
| PC＋Mobile Recently Viewed | `favorites_recently_viewed` |
| Mobile Favorites推荐 | `favorites_recommendations` |
| Shopping Bag商品列表 | `shopping_bag_items` |

### 3.4 `view_cart`

同时覆盖Shopping Bag页面和PC Cart Drawer：

- 非空购物车中至少一件可购商品成功展示时发送。
- Shopping Bag使用该页面新生成的`page_instance_id`。
- PC Cart Drawer沿用当前所在页面的`page_instance_id`。
- 同一页面实例内，Shopping Bag和PC Cart Drawer各自最多发送一次。
- `items[]`包含当前展示的全部可购商品，`value`为这些商品的金额合计，`currency`与金额同源。
- 刷新或重新进入Shopping Bag形成新的页面实例后可以再次发送。
- 空购物车、只有不可购商品、加载失败或同一展示面重复渲染不发送。

### 3.5 `remove_from_cart`

当前一物一码商品从购物车真实删除成功后发送一次：

- `items[]`只包含本次删除的商品。
- `items[].quantity=1`。
- `items[].price`取当前实际单价。
- `value`取本次真实减少金额。
- `currency`与商品价格同源。
- 删除失败、购物车没有变化或仅打开操作区不发送。

## 四、公共页面实例规则

`page_instance_id`标识用户实际进入并停留的这一次页面，由Web公共页面上下文生成一次。GA4适配器和一方平台适配器读取同一个值，业务模块不得各自生成第二套页面实例ID。

| 页面动作 | 处理 |
|---|---|
| 首次到达、整页刷新、进入另一个有效路由、前进或后退重新进入页面 | 生成新的`page_instance_id` |
| 从其他页面提交搜索并进入搜索结果页 | 结果页生成新的`page_instance_id` |
| 已在搜索结果页正式提交新搜索词并形成新的页面上下文 | 生成新的`page_instance_id` |
| 同一搜索结果页Apply筛选、Apply排序或Reset | 沿用当前`page_instance_id` |
| 列表加载更多、模块重渲染、接口重复回调或同一路由重复监听 | 沿用当前`page_instance_id` |
| 打开或关闭PC Favorites Drawer | Drawer不形成新页面实例；曝光和点击沿用打开前当前页面的`page_instance_id`，不新增`page_view` |

同一页面实例中的`page_view`、`view_search_results`、`view_item_list`、`select_item`和`view_cart`携带相同的`page_instance_id`。本批只为现有`page_view`和`select_item`补充该参数，不改变其原触发逻辑。

## 五、字段来源与传递规则

### 5.1 统一传递链路

```text
业务页面、搜索模块或公共页面上下文形成真实值
→ Web GA4适配器组装looply_ga4_* dataLayer事件
→ GTM Custom Event Trigger命中对应GA4 Event Tag
→ Data Layer Variable读取同名字段
→ GA4 Event Tag映射事件参数与items[]
→ 浏览器发送g/collect
```

### 5.2 字段契约

| 字段 | 适用事件 | 谁提供或生成 | 取值来源 | 无法取得时的处理 |
|---|---|---|---|---|
| `event_id` | 仅`view_search_results` | Web公共事件上下文 | 终态事件成立时生成；同一终态发送重试保持同值 | 省略，事件继续发送 |
| `page_instance_id` | `page_view`、`view_search_results`、`view_item_list`、`select_item`、`view_cart` | Web公共页面上下文 | 按第四章生成并由适用事件共同读取 | 省略，事件继续发送，不生成替代值 |
| `search_term` | `search`、有搜索词的结果和搜索结果曝光 | 搜索模块 | 搜索模块用于构造结果URL的正式分析词 | 省略，事件继续发送，不回退为未经处理的输入原文 |
| `trigger_type` | `search`；站内提交形成的结果和曝光 | 搜索交互点及结果URL | 按3.1确定并写入结果URL，结果和曝光再从URL读取 | 省略，事件继续发送，不猜测 |
| `suggestion_position` | 联想点击形成的`search` | 搜索联想组件 | 被点击建议在当前列表中的位置，从1开始 | 省略，事件继续发送 |
| `suggestion_object_id` | 有稳定建议实体的联想点击 | 搜索模块 | 已有稳定建议实体ID | 省略，不生成临时ID |
| `result_status` | `view_search_results` | 搜索结果状态控制器 | 按3.2的唯一终态 | 省略，事件继续发送，不伪造终态 |
| `result_count` | 成功或零结果 | 搜索接口 | 响应总结果数，不使用已渲染卡片数 | 省略，事件继续发送 |
| `duration_ms` | `view_search_results` | 搜索请求控制器 | 从请求发起到唯一终态的毫秒数 | 省略，事件继续发送，不填固定值 |
| `failure_type` | `failed`结果 | 搜索请求控制器 | 按3.2的低基数枚举映射 | 省略，事件继续发送，不发送错误原文 |
| `filter_ids` | `view_search_results`及Search／Collection筛选后的`view_item_list` | Search／Collection公共筛选上下文 | 最终已Apply的动态离散筛选条件；使用后台稳定`dimension_code`和`option_code` | 无筛选时省略；单项缺稳定Code时仅省略该项，事件继续发送 |
| `sort_type` | 结果和搜索结果曝光 | 搜索模块或结果URL | 当前实际生效的稳定排序枚举，包括默认排序 | 省略，事件继续发送，不根据UI文案猜测 |
| `placement_id` | `view_item_list` | 当前商品模块 | 按3.3封闭表取稳定常量 | 省略，事件继续发送，不伪造展示位 |
| `items[].item_id` | `view_item_list`、`view_cart`、`remove_from_cart` | 商品或购物车数据 | API中的`listing_public_code`，来源为`listings.public_code` | 省略，事件继续发送；不使用内部ID、SKU或SEO slug替代 |
| `items[].index` | `view_item_list` | 商品列表组件 | 当前业务列表位置，从1开始 | 省略，事件继续发送，不填0或猜测值 |
| `currency` | `view_cart`、`remove_from_cart` | 购物车或商品价格上下文 | 与价格同源的实际展示和结算币种 | 省略，事件继续发送，不写死`USD` |
| `value` | `view_cart`、`remove_from_cart` | 购物车状态 | 全部可购商品金额合计或本次真实减少金额 | 省略，事件继续发送，不填0占位 |
| `items[].price`、`items[].quantity` | `view_cart`、`remove_from_cart` | 商品或购物车数据 | 当前实际单价和数量 | 省略，事件继续发送，不按点击动作猜测 |

业务事实成立时发送事件。参数能够取得时正常携带；无法取得时省略，不伪造默认值，也不因参数缺失停止事件上报。本期不新增线上参数缺失诊断事件或诊断机制。

`filter_ids`采用`dimension_code:option_code`格式。同一维度多选分别记录，去重并按Code稳定排序后用逗号连接，例如`category:CA5GYR4GDRH2K,series:SEB7TNVEXWVF7`。维度与选项来自后台动态筛选配置，前端不维护固定维度清单，也不使用展示名称作为ID。选择后取消、关闭面板或未Apply的值不进入该字段；Reset后省略。价格区间本期不进入`filter_ids`。

后台新增筛选维度时必须同时提供稳定`dimension_code`和`option_code`。单项缺少任一稳定Code时只省略该项，事件继续发送且不得临时造Code。后台／数据平台维护Code到展示名称的可追溯映射，GA4事件只保留稳定Code。

`sort_type`仅使用以下值：

| 枚举值 | 含义 |
|---|---|
| `recommended` | 推荐排序，包括默认排序 |
| `newest` | 最新上架优先 |
| `price_low_to_high` | 价格从低到高 |
| `price_high_to_low` | 价格从高到低 |

## 六、搜索上下文URL规则

用户正式提交搜索时，结果页URL携带：

- `keyword={编码后的搜索模块正式分析词}`；
- `trigger_type={本次搜索提交方式}`。

筛选、排序和Reset更新URL时保留原`trigger_type`，并将实际生效的筛选和排序条件写入当前URL。Search与Collection共用后台Code驱动的已Apply筛选事实；`view_search_results`及Search／Collection的`view_item_list`从该公共事实组装各自事件参数。

直达搜索URL、刷新或页面恢复时，不补造`search`。URL没有`trigger_type`时，结果与曝光事件省略该参数。

## 七、GA4参数用途

| 用途 | 参数 | 处理要求 |
|---|---|---|
| GA4标准参数 | `search_term`、`currency`、`value`、`items[]`、`items[].index` | 使用GA4标准字段，不重复注册同义自定义字段 |
| GA4报表或探索维度 | `trigger_type`、`result_status`、`failure_type`、`placement_id`、`sort_type` | 支持按搜索入口、结果状态、失败类型、商品展示位和排序方式分析 |
| GA4报表或探索指标 | `result_count`、`duration_ms`、`suggestion_position` | 支持结果数、结果返回耗时和联想点击位置分析 |
| 仅原始事件关联与验收 | `event_id`、`page_instance_id`、`suggestion_object_id`、`filter_ids` | 随适用事件发送，但不注册为GA4自定义维度或指标 |

GA4 Web数据流保持增强型衡量开启，但关闭其中的“网站搜索”，避免GA4按URL参数自动生成第二条`view_search_results`。

## 八、开发完成检查

开发完成后按下表自查是否遗漏本批改动。正式运行验收另行执行，不在本文件扩展测试过程。

| 改动对象 | 完成条件 |
|---|---|
| `search` | 六种正式提交入口分别映射唯一`trigger_type`；每次正式提交只发送一次；输入变化、联想展示、筛选、排序和结果返回不产生`search` |
| `view_search_results` | 初始加载及结果URL参数生效后产生唯一终态；支持`success`、`no_results`、`failed`、`cancelled`；直达URL不补造`search`；仅本事件使用`event_id` |
| `view_item_list` | 单件商品达到50%可视且持续1秒后发送；同一页面实例按展示位和商品去重；只携带本次达标商品及可取得的列表位置、展示位和搜索上下文 |
| `view_cart` | Shopping Bag和PC Cart Drawer均保留；Drawer沿用当前页面实例，Shopping Bag使用新页面实例；携带可取得的`currency`、`value`及全部可购商品 |
| `remove_from_cart` | 商品真实删除成功后发送一次；携带可取得的`currency`、实际减少金额及数量为1的被删除商品；失败或无变化不发送 |
| 公共页面实例 | `page_view`、`view_search_results`、`view_item_list`、`select_item`和`view_cart`统一读取Web公共页面上下文中的`page_instance_id` |
| 字段缺失 | 业务事实成立时事件继续发送；无法取得的参数省略，不伪造默认值；不新增线上参数缺失诊断事件或诊断机制 |
| GA4配置 | 增强型衡量保持开启，仅关闭“网站搜索”，避免自动生成第二条`view_search_results` |
