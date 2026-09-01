# Looply GA4 生产环境全量验收测试用例

> 版本：v0.3  
> 日期：2026-08-27  
> 状态：执行基线  
> 生产站：`https://www.looply.com/`  
> GA4：Property `531542304` / Measurement ID `G-Z2EKP8QGT7`  
> 线上实际 GTM：`GTM-PD3ZGT7L`  
> 用途：开发调整 GA4 逻辑后的全量生产回归；每个事件、实际入口、终端与用户状态分别取证。

## 一、文档中心基线

本版只依据文档中心提交 `a66ffcc21f0c3fb89f8b64aad6003c9ac6415337` 中以下当前文件编制：

1. 《Looply GA4数据分析 PRD》v1.9；
2. 《Looply GA4五事件新增与修改 PRD》v1.1；
3. 《Looply GA4全量事件清单》v1.0；
4. 《Looply GA4埋点变更清单》v1.5；
5. 《Looply GA4线上验收问题与开发修复单》v1.2。

合并后验收对象为基础 `page_view` 加17类业务事件，共18个事件。

### 1.1 已识别的基线冲突及本轮执行口径

| 主题 | 文档冲突 | 本轮执行口径 |
|---|---|---|
| GA自动 `page_view` | 当前临时方案暂停Looply主动事件 | 保留GA自动 `page_view`；验证无`looply_ga4_page_view`主动事件，页面实例上下文仍可供其他事件关联。 |
| GA自动网站搜索 | 当前数据流设置保持关闭 | 仅Looply主动 `view_search_results`；发布前后在GA4设置与`g/collect`复核无自动第二条同名事件。 |
| `view_item.item_brand` | GA4 PRD示例包含品牌；修复单v1.2 FIX-11明确本项不要求 | 不把 `item_brand`作为通过条件。 |

## 二、全链路通过标准

每个“事件 × 触发场景 × 终端 × 用户状态”独立记录以下证据：

| 层级 | 必须取得的证据 |
|---|---|
| 业务事实 | 页面状态、接口结果或业务对象真实发生预期变化 |
| dataLayer | 对应 `looply_ga4_*`、推送次数、载荷和事件先后顺序 |
| Tag Assistant / GTM | Custom Event只命中预期GA4 Event Tag一次；变量映射与dataLayer一致 |
| GA请求 | 请求发往 `G-Z2EKP8QGT7`；核对 `en`、页面参数、业务参数、`items[]`及HTTP结果 |
| GA4接收 | DebugView本会话事件及参数；Realtime只作聚合辅助，不替代单事件证据 |
| D+1 | 需注册或处理后才能查询的来源字段、原始参数和服务端事件对账 |

结论规则：

- 五层即时证据全部正确：运行态通过。
- 缺Tag Assistant、GTM或DebugView本会话证据：标记“证据未闭环”，不得写成通过。
- 业务事实成立但事件缺失、重复、时序错误或值错误：不通过。
- 文档允许省略的字段缺失：事件继续发送；不得因缺失停止事件，也不得伪造默认值。
- 需求明确不应发送且实际为0条：反向用例通过。
- 页面确实不存在对应入口：记录“线上无此入口”及页面证据，不判失败。
- 未实际执行：写“未执行”，不得写成失败或通过。

## 三、通用执行矩阵

| 维度 | 覆盖值 |
|---|---|
| 终端 | PC；Mobile 390×844 |
| 用户状态 | 游客；登录用户（适用场景） |
| 页面生命周期 | 首次进入；SPA进入；硬刷新；前进/后退；重复渲染 |
| 市场/语言 | US/EN；HK及其他已启用语言需具备可访问条件后执行 |
| 事件结果 | 成功；失败；取消；重复回调；无状态变化 |
| 商品位置 | 首件；非首件；滚动/加载后商品 |
| 安全边界 | 不创建真实付费订单；不输入真实支付卡；Refund不做浏览器伪造 |

## 四、公共规则用例

| 用例ID | 场景 | 预期 |
|---|---|---|
| GL-01 | 允许地区打开生产站 | dataLayer、共享GTM加载器和GA4适配器各初始化一次 |
| GL-02 | EEA、英国或瑞士禁止地区 | 不初始化dataLayer、不加载GTM/GA4、不push事件、零GA请求；仅在可控地区环境执行 |
| GL-03 | 浏览器事件Schema | 事件名、语言、页面、金额、商品ID和参数类型符合基线 |
| GL-04 | PII扫描 | 无邮箱、电话、姓名、完整地址、支付卡、Token、自由错误文本等原始PII |
| GL-05 | GTM Preview逐事件 | 每个 `looply_ga4_*`只触发一个对应GA4 Event Tag |
| GL-06 | 生产目标 | 所有GA4请求只发送到 `G-Z2EKP8QGT7`，不串测试属性 |
| GL-07 | 公共页面实例 | 同页适用事件读取同一 `page_instance_id`；新页面实例生成新值 |
| GL-08 | 参数缺失 | 业务事实已成立时继续发送；不可取参数省略，不填0、空字符串或猜测值 |
| GL-09 | 页面来源 | `page_referrer`等于动作发生前真实页面；直达允许为空，不使用前两跳旧值 |
| GL-10 | 跨事件参数隔离 | 每个事件独立组装参数；不得继承其他事件的操作ID、`event_id`或业务上下文 |
| GL-11 | 主动来源参数隔离 | `page_view_source`只出现在主动 `page_view`；`view_search_results_source`只出现在主动结果事件；其他事件不得携带 |

## 五、逐事件用例

### 5.1 `page_view`

| 用例ID | 场景 | 终端 | 预期 |
|---|---|---|---|
| PV-01 | 首次打开首页 | PC/Mobile | 1条GA自动`page_view`；0条Looply主动事件 |
| PV-02 | 直达Collection、Search、PDP、Wishlist、Shopping Bag、Checkout、登录/注册、Account等实际路由 | PC/Mobile | 按GA自动页面采集验证；0条Looply主动事件 |
| PV-03 | 首页→Collection→PDP等有效SPA路由 | PC/Mobile | 按现有GA自动history配置实测；不新增受控SPA Tag |
| PV-04 | 首页、列表、PDP硬刷新 | PC/Mobile | 有GA自动`page_view`；0条Looply主动事件 |
| PV-05 | 浏览器前进/后退重新进入 | PC/Mobile | 按现有GA自动history配置实测；0条Looply主动事件 |
| PV-06 | 骨架屏、预取、组件重渲染、重复监听 | PC/Mobile | 不新增主动事件 |
| PV-07 | 已在Search页连续提交三个新搜索词 | PC/Mobile | 结果事件按请求终态发送；不产生Looply主动`page_view` |
| PV-08 | 同一Search页Apply筛选、排序、Reset | PC/Mobile | 沿用当前页面实例，不生成第二套ID |
| PV-09 | PDP返回首页；Search、Wishlist及PDP SPA进入 | PC/Mobile | 按GA自动页面采集验证；不得出现Looply主动`page_view` |
| PV-10 | 主动页面事件暂停 | PC/Mobile | GA自动`page_view`存在；不存在Looply主动事件或`page_view_source`新值 |
| PV-11 | 页面连续跨首页、列表、Search、PDP、Cart、Checkout | PC/Mobile | 主动事件来源指向真实上一页，不指向旧页面或前两跳 |
| PV-12 | D+1来源核对 | 全日 | 可按 `page_view_source=looply_custom`识别生效后的主动事件；历史空值不反推来源 |

### 5.2 `generate_lead`

执行前盘点生产站全部联系线索入口，包括Contact Us及其他真实调用联系线索接口的页面。

| 用例ID | 场景 | 预期 |
|---|---|---|
| LEAD-01 | 每个实际入口提交成功 | 1条 `generate_lead`；`lead_id`、`lead_type`与成功事实一致 |
| LEAD-02 | 前端校验失败、接口失败或取消 | 0条 |
| LEAD-03 | 成功回调重复 | 同一线索只发送1条 |

### 5.3 `sign_up`

| 用例ID | 场景 | 终端 | 预期 |
|---|---|---|---|
| SU-01 | 邮箱注册成功 | PC/Mobile | 事务成功一次；`registration_id`、`method=email` |
| SU-02 | Google注册成功（如提供） | PC/Mobile | `method=google`，无账号原文 |
| SU-03 | Apple注册成功（如提供） | PC/Mobile | `method=apple`，无账号原文 |
| SU-04 | Facebook注册成功（如提供） | PC/Mobile | `method=facebook`，无账号原文 |
| SU-05 | 校验/验证码失败、OAuth取消或接口失败 | PC/Mobile | 0条 |
| SU-06 | 成功回调重复、刷新成功页 | PC/Mobile | 同一注册事务只发送1条 |

### 5.4 `login`

| 用例ID | 场景 | 终端 | 预期 |
|---|---|---|---|
| LI-01 | 邮箱登录成功 | PC/Mobile | 1条；`login_id`、`method=email` |
| LI-02 | Google登录成功（如提供） | PC/Mobile | `method=google` |
| LI-03 | Apple登录成功（如提供） | PC/Mobile | `method=apple` |
| LI-04 | Facebook登录成功（如提供） | PC/Mobile | `method=facebook` |
| LI-05 | 密码/验证码失败、OAuth取消或接口失败 | PC/Mobile | 0条 |
| LI-06 | 重复回调或刷新 | PC/Mobile | 同一真实登录成功只发送1条；不切断当前行为Session |

### 5.5 `search`

六种正式入口均在PC和Mobile实际寻找并执行；不存在时保留页面证据。

| 用例ID | 触发动作 | 预期 `trigger_type` | 其他预期 |
|---|---|---|---|
| SE-01 | 未改写轮播词，直接点击搜索按钮 | `carousel_term_button` | 1条 `search` |
| SE-02 | 手动输入后按回车 | `manual_enter` | 1条 |
| SE-03 | 手动输入后点击搜索按钮 | `manual_search_button` | 1条 |
| SE-04 | 点击第1条与非首条输入联想 | `suggestion_select` | `suggestion_position`从1开始；稳定对象ID存在时携带 |
| SE-05 | 点击搜索历史词 | `history_select` | 使用正式分析词 |
| SE-06 | 点击热门搜索词 | `popular_term_select` | 1条 |
| SE-07 | 点击热门品牌或热门Collection | 不适用 | 0条 `search`；仅按入口点击和目标页处理 |
| SE-08 | 只输入、只展示联想、筛选、排序、结果返回 | 不适用 | 0条新 `search` |
| SE-09 | 正式提交后接口失败或无结果 | 对应入口 | 提交事件仍发送1条 |
| SE-10 | 连续“联想→回车→按钮→历史→热门→轮播” | 各自枚举 | 只有联想事件携带本次 `suggestion_position`；其余不得继承旧位置 |
| SE-11 | 刷新或直达搜索URL | 不适用 | 不补造 `search` |

### 5.6 `view_search_results`

| 用例ID | 场景 | 预期 |
|---|---|---|
| VSR-01 | 六种正式入口分别形成有结果终态 | 每次1条 `success`；结果数大于0；上下文与URL一致 |
| VSR-02 | 正式提交无结果词 | 1条 `no_results`；`result_count=0` |
| VSR-03 | 直达有结果URL | 不补 `search`；1条 `success` |
| VSR-04 | 直达无结果URL | 不补 `search`；1条 `no_results` |
| VSR-05 | 刷新或页面恢复 | 不补 `search`；当前结果请求形成1个终态 |
| VSR-06 | Search单选、多选、动态Series并Apply | 新终态；沿用页面实例；`filter_ids`为稳定Code且排序去重 |
| VSR-07 | 选择后取消、关闭面板、未Apply | 不把未生效选择写入 `filter_ids` |
| VSR-08 | Reset | 新终态；沿用页面实例；省略 `filter_ids`，不残留旧值 |
| VSR-09 | 四种排序 | 分别携带 `recommended/newest/price_low_to_high/price_high_to_low` |
| VSR-10 | 非Abort错误且重试结束 | 1条 `failed`；`failure_type`使用封闭枚举，无错误原文 |
| VSR-11 | 被新请求替换、显式取消或离页 | 1条 `cancelled`；不伪造结果数或失败类型 |
| VSR-12 | 同一终态发送重试 | 保持同一 `event_id`；新终态生成新ID |
| VSR-13 | 主动结果事件来源 | 携带 `view_search_results_source=looply_custom`；其他事件不携带 |
| VSR-14 | GA增强型衡量网站搜索 | 带搜索参数URL不额外产生第二条自动同义事件 |

### 5.7 `view_item_list`

所有入口同时检查曝光阈值、单商品载荷、位置、页面实例、筛选上下文和去重。

| 用例ID | 商品展示位置 | `placement_id` | 终端 |
|---|---|---|---|
| VIL-01 | 首页For You | `home_feed_for_you` | PC/Mobile |
| VIL-02 | 首页New Arrivals | `home_feed_new_arrivals` | PC/Mobile |
| VIL-03 | Collection商品列表 | `collection_results` | PC/Mobile |
| VIL-04 | 搜索结果列表 | `search_results` | PC/Mobile |
| VIL-05 | 搜索无结果推荐 | `search_no_results_recommendations` | PC/Mobile |
| VIL-06 | PDP You May Also Like | `product_you_may_also_like` | PC/Mobile |
| VIL-07 | PDP Recently Viewed | `product_recently_viewed` | PC/Mobile |
| VIL-08 | Wishlist | `favorites_wishlist` | PC/Mobile |
| VIL-09 | Favorites Recently Viewed | `favorites_recently_viewed` | PC/Mobile |
| VIL-10 | Favorites推荐 | `favorites_recommendations` | Mobile |
| VIL-11 | Shopping Bag商品列表 | `shopping_bag_items` | PC/Mobile |

| 用例ID | 边界场景 | 预期 |
|---|---|---|
| VIL-B01 | 首次列表请求成功并展示初始商品 | 1条；`items[]`携带本次已加载商品并生成新的`list_instance_id` |
| VIL-B02 | 搜索／筛选／排序／首页Tab真实请求成功且结果集合变化 | 1条新的`view_item_list`；沿用页面实例并生成新的`list_instance_id` |
| VIL-B03 | 滚动或分页追加 | 0条`view_item_list`；卡片可视Hook不得触发GA4列表事件 |
| VIL-B04 | 失败、取消、未提交条件、重复条件或结果未变化 | 0条 |
| VIL-B05 | 重复回调、重渲染或缓存复用 | 0条重复事件 |
| VIL-B06 | 新列表结果的`items[]` | 只含该结果首次成功展示时已加载商品；位置从1开始，字段和上下文完整 |
| VIL-B07 | 后续商品点击 | `select_item`复用当前列表的`list_instance_id` |
| VIL-B08 | Search/Collection筛选、排序、Reset | 只携带最终已Apply的稳定Code；价格区间不进入 `filter_ids` |
| VIL-B09 | 收藏后继续滚动列表 | 不得继承 `wishlist_operation_id`或其他事件的 `event_id` |

### 5.8 `select_item`

对VIL-01～VIL-11所有实际可点击入口分别点击首件和非首件商品。

| 用例ID | 场景 | 预期 |
|---|---|---|
| SI-01～SI-11 | 分别点击VIL-01～VIL-11商品卡 | 1条；`selection_id`、`page_instance_id`、列表标识、商品及真实位置正确 |
| SI-12 | 每个入口点击首件和非首件 | `items[].index`从1开始并等于页面真实顺序 |
| SI-13 | Wishlist点击 | 曝光和点击均使用 `favorites_wishlist` |
| SI-14 | Search/Collection筛选后点击 | 携带最终已Apply `filter_ids`；页面实例不因筛选改变 |
| SI-15 | 首页、列表、Search、PDP、Cart连续跳转后点击 | `page_referrer`等于动作发生时真实页面 |
| SI-16 | 同一卡片再次真实点击 | 新点击可发送；使用不同 `selection_id` |
| SI-17 | 曝光、滚动、hover或点击收藏按钮 | 0条 `select_item` |

### 5.9 `view_item`

| 用例ID | 场景 | 终端 | 预期 |
|---|---|---|---|
| VI-01 | 直达PDP | PC/Mobile | 核心内容可见后1条；与PDP主动 `page_view`使用同一 `page_instance_id` |
| VI-02～VI-12 | 从VIL-01～VIL-11入口进入PDP | 适用端 | 每个新PDP实例1条；商品、币种、金额及当前PDP页面实例正确 |
| VI-13 | 硬刷新PDP | PC/Mobile | 新页面实例，可重新发送1条 |
| VI-14 | 重复渲染或接口重复回调 | PC/Mobile | 同一页面实例同一商品不重复 |
| VI-15 | Search/首页/New Arrivals/Collection/推荐/Recently Viewed/Wishlist连续进入 | PC/Mobile | 前序 `select_item`、PDP主动 `page_view`、`view_item`可按当前页面实例关联；不要求 `item_brand` |

### 5.10 `add_to_wishlist`

执行前盘点全部收藏入口，至少覆盖首页商品卡、Collection、Search、无结果推荐、PDP、PDP推荐和Favorites推荐等实际位置。

| 用例ID | 场景 | 预期 |
|---|---|---|
| WL-01 | 每个入口首次收藏成功 | 1条；`wishlist_operation_id`、币种、金额和商品正确 |
| WL-02 | 已收藏商品重复点击或关系无变化 | 0条新的成功事件 |
| WL-03 | 收藏接口失败 | 0条 |
| WL-04 | 游客点击仅触发登录引导，未建立关系 | 0条成功事件 |
| WL-05 | 收藏成功后继续浏览首页、Search、PDP推荐和Recently Viewed | 后续其他事件不得继承收藏操作ID |

### 5.11 `view_cart`

| 用例ID | 场景 | 终端 | 预期 |
|---|---|---|---|
| VC-01 | 非空Shopping Bag | PC/Mobile | 每个页面实例1条；全部可购商品、金额、币种正确 |
| VC-02 | 非空PC Cart Drawer | PC | 沿用当前页面实例；同一页面实例最多1条 |
| VC-03 | 同一实例重复打开/渲染Drawer | PC | 不重复 |
| VC-04 | 刷新或重新进入Shopping Bag | PC/Mobile | 新页面实例可再次发送 |
| VC-05 | 空购物车 | PC/Mobile | 0条 |
| VC-06 | 只有不可购商品或加载失败 | PC/Mobile | 0条 |

### 5.12 `add_to_cart`

| 用例ID | 场景 | 终端 | 预期 |
|---|---|---|---|
| AC-01 | 每个实际加购入口成功且购物车状态变化 | PC/Mobile | 1条；操作ID、币种、金额、商品、quantity=1正确 |
| AC-02 | 同一成功回调重复 | PC/Mobile | 同一操作不重复 |
| AC-03 | 商品已在购物车且无状态变化 | PC/Mobile | 0条新成功事件 |
| AC-04 | 加购接口失败 | PC/Mobile | 0条 |

### 5.13 `remove_from_cart`

| 用例ID | 场景 | 终端 | 预期 |
|---|---|---|---|
| RC-01 | Shopping Bag删除本轮测试商品 | PC/Mobile | 1条；删除商品、quantity=1、实际单价、减少金额、币种正确 |
| RC-02 | PC Drawer删除本轮测试商品 | PC | 同上 |
| RC-03 | 仅打开删除操作区 | PC/Mobile | 0条 |
| RC-04 | 删除失败或购物车无变化 | PC/Mobile | 0条 |
| RC-05 | 删除成功回调重复 | PC/Mobile | 同一真实减少只发送1条 |

### 5.14 `begin_checkout`

执行前盘点所有能创建checkout session的实际入口。

| 用例ID | 场景 | 终端 | 预期 |
|---|---|---|---|
| BC-01 | Shopping Bag开始结算 | PC/Mobile | session创建成功后1条；ID、币种、金额、商品正确 |
| BC-02 | PC Cart Drawer开始结算 | PC | 同上 |
| BC-03 | PDP Buy Now（如存在） | PC/Mobile | 同上，商品集合符合实际交接 |
| BC-04 | checkout创建失败或校验未通过 | PC/Mobile | 0条 |
| BC-05 | 重复点击或重复回调 | PC/Mobile | 同一 `checkout_id`只发送1条 |

### 5.15 `add_shipping_info`

| 用例ID | 场景 | 终端 | 预期 |
|---|---|---|---|
| SH-01 | 新地址及配送方式校验保存成功 | PC/Mobile | 1条；`checkout_id`、`step_version`、`shipping_tier`、金额和商品正确 |
| SH-02 | 使用已有地址并形成有效保存事实 | PC/Mobile | 新步骤版本1条 |
| SH-03 | 修改已完整地址后再次有效保存 | PC/Mobile | 新 `step_version`再发送1条，版本递增且稳定 |
| SH-04 | 校验失败、保存失败或仅填写未保存 | PC/Mobile | 0条 |
| SH-05 | 同一版本重复回调或页面重渲染 | PC/Mobile | 不重复 |
| SH-06 | 未修改离开Checkout、返回首页 | PC/Mobile | 0条；不得在首页补发旧配送事件 |
| SH-07 | 无变化再次点击或离焦 | PC/Mobile | 0条新事件 |

### 5.16 `add_payment_info`

| 用例ID | 场景 | 终端 | 预期 |
|---|---|---|---|
| PM-01 | 信用卡支付方式token化保存成功（仅官方测试通道） | PC/Mobile | 1条；类型、checkout、版本、金额、商品正确 |
| PM-02 | PayPal保存成功（如提供测试通道） | PC/Mobile | 稳定 `payment_type` |
| PM-03 | Klarna保存成功（如提供测试通道） | PC/Mobile | 稳定 `payment_type` |
| PM-04 | Apple Pay保存成功（如提供测试通道） | 适用端 | 稳定 `payment_type` |
| PM-05 | token化失败、用户取消或仅选择未保存 | PC/Mobile | 0条 |
| PM-06 | 同一步骤版本重复回调 | PC/Mobile | 不重复 |

生产环境不输入真实卡号、不保存真实支付方式；没有官方测试通道时标记“未执行”。

### 5.17 `purchase`

不创建真实付费订单，只读取既有订单、成功页或服务端运行证据：

| 用例ID | 场景 | 预期 |
|---|---|---|
| PU-01 | 支付状态processing | 0条 `purchase` |
| PU-02 | 首次paid且浏览器5分钟内claim成功 | 浏览器发送1条；服务端兜底被抑制 |
| PU-03 | 用户关闭成功页 | 5分钟后Measurement Protocol兜底1条 |
| PU-04 | claim与Worker并发 | 只有一方取得发送权 |
| PU-05 | 刷新成功页、多标签或重复支付回调 | 同一 `order_id`不重复 |
| PU-06 | 金额、税、运费、币种和商品 | `transaction_id=order_id`；与业务事实一致 |
| PU-07 | MP失败重试 | 同幂等键和transaction_id重试，不形成新交易 |
| PU-08 | 禁止地区订单 | 浏览器与服务端零请求；任务为 `suppressed_by_region` |

### 5.18 `refund`

只验收服务端真实运行证据，不做浏览器伪造：

| 用例ID | 场景 | 预期 |
|---|---|---|
| RF-01 | 部分退款成功 | 关联原transaction_id；只发送本次退款商品和金额 |
| RF-02 | 全额退款成功 | 发送完整退款明细 |
| RF-03 | 同订单多次部分退款 | 不同 `refund_id`分别1条 |
| RF-04 | 重复退款回调 | 同一 `refund_id`不重复 |
| RF-05 | 退款失败、处理中或取消 | 0条成功 `refund` |
| RF-06 | 禁止地区退款 | 零MP请求；任务为 `suppressed_by_region` |

## 六、开发本次修改专项回归

以下用例不能只由单入口正向测试替代：

| 修复项 | 必跑用例 |
|---|---|
| FIX-01 联想位置残留 | SE-10，PC/Mobile连续完整序列 |
| FIX-02 Search页面实例 | PV-07、PV-08及VSR/VIL/SI同ID核对 |
| FIX-03 动态筛选 | VSR-06～08、VIL-B08、SI-14，Search/Collection双端 |
| FIX-04 主动页面事件次数 | PV-01～09，覆盖首页、Search、Collection、PDP、Wishlist、Cart、Checkout |
| FIX-05 页面来源参数 | PV-10、PV-12 |
| FIX-06 搜索结果来源参数 | VSR-13、VSR-14 |
| FIX-07 空曝光 | VIL-B09 |
| FIX-08 点击位置/Wishlist标识 | SI-01～SI-13 |
| FIX-09 页面来源 | GL-09、PV-11、SI-15 |
| FIX-10 跨事件ID污染 | GL-10、VIL-B10、WL-05 |
| FIX-11 PDP页面实例 | VI-01～VI-15 |
| FIX-12 配送保存事实 | SH-01～SH-07 |

## 七、执行顺序

1. 访问生产站、生产GA4和线上实际GTM容器，确认权限与网络。
2. 建立Tag Assistant Preview、dataLayer监听、`g/collect`监听和DebugView本会话识别。
3. 盘点生产UI全部实际入口，先补充入口记录再执行；不能用一个入口代表同类全部入口。
4. 游客态完成页面、搜索、曝光、点击、PDP、收藏、购物车和结算前半段。
5. 创建或使用专用测试账号，执行注册、登录、Wishlist及已有地址场景。
6. 只在无真实资金影响且具备官方测试通道时执行配送和支付信息场景。
7. Purchase/Refund只读取既有运行证据。
8. D+1核对来源自定义维度、原始参数和需跨日处理的数据。

## 八、交付结果格式

正式验收报告逐用例记录：用例ID、端、用户状态、实际动作、业务事实、dataLayer次数与参数、Tag Assistant/GTM标签与次数、`g/collect`及HTTP、DebugView/GA4接收、结论、证据、修复建议。没有执行的用例必须写“未执行”及原因，不得合并成失败。
