# Looply 数据采集与埋点产品需求

> 版本：v1.6  
> 日期：2026-08-18  
> 状态：开发交付基线  
> 变更依据：《Looply 数据采集与埋点 v1.5 开发审查问题处理结论 v1.0》  
> 版本关系：v1.5保留为历史版本；后续开发实施以本稿为准。

身份规则输入依据：[《Looply 唯一用户身份识别 PRD v2.19》](https://zhuanspirit.feishu.cn/wiki/N5RLwnrxMi6FJCkVfWZcvJa8nee)。本稿已摘录本次数据采集实施所需规则，开发不需要依赖外部文档理解第四章。

## 一、目标与范围

本方案定义 Looply 一方数据平台需要记录的客户端业务行为、公共业务上下文、身份与 Session 业务口径、权威业务事实输入，以及存量埋点迁移目标。

本期覆盖当前 PC Web 和 Mobile Web 已存在的页面与有意义用户操作。PC没有独立Shop和Favorites页面；Mobile包含独立Shop和Favorites页面。Tablet和App不在本期范围。

本方案不定义 GA4、广告平台或搜推算法专项字段，不定义 SDK、网关、消息队列、存储表及发送重试机制。

## 二、一方数据组成

一方分析数据由两部分组成：

1. **客户端统一事件**：用户在页面中真实发生的页面访问、有意义操作及客户端业务结果，共17个事件，由Web／SDK采集。
2. **权威业务事实**：订单创建、支付尝试、支付成功及退款等事实，共5类，由订单、支付和退款业务系统或其权威数据表提供，不由Web重复上报。

同一个业务事实只允许在一方平台形成一条记录。旧调用与新契约可在技术适配层兼容，但不得双发双计。

## 三、统一事件的公共信息

### 3.1 基础识别信息

| 字段 | 业务含义 | 产品要求 |
|---|---|---|
| `event_id` | 一条统一业务事实的唯一标识 | 同一事实重试沿用同一值；不得把事件类型或旧物理名称写入该字段 |
| `event_name`／最终物理`event_type` | 一方平台事件类型 | 两者取相同值；客户端事件只取第五章17个名称，权威业务事实只取第六章5个名称。旧物理名称仅可在专项消费者兼容层存在，不得进入一方平台 |
| `occurred_at` | 事实实际发生时间 | 不以接收时间替代 |
| `schema_version` | 事件契约版本 | 本稿对应版本由技术方案登记 |

### 3.2 客户端行为的公共上下文

客户端事件按适用场景记录：

| 类别 | 业务信息 |
|---|---|
| 身份 | `anonymous_id`；已登录时增加`user_id`和`identity_state`；身份模块已返回时增加`canonical_person_id` |
| Session | `session_id` |
| 页面 | `page_type`、`page_id`、`page_instance_id`、清洗后的页面URL、上一页面类型 |
| 设备与市场 | 设备类别、浏览器、操作系统、Market、国家／地区；具体取得方式由技术方案确定 |
| 模块与入口 | `module_id`、`placement_id`、`source_type`；存在前序事实时增加`source_event_id` |
| 站外原始来源 | 首次到达时可取得的referrer、UTM、广告点击标识和落地页；保留原始触点，不在采集环节计算首次／末次归因结果 |
| 站内原始来源 | 引导当前事实发生的来源页面、模块、入口和前序事件；归因结果不得覆盖原始触点 |
| 结果 | 适用时记录`result_state`和低基数`failure_type` |

`page_instance_id`唯一识别用户实际进入的这一次页面实例，不是页面URL、`session_id`或用户ID。该ID由Web页面公共上下文在页面实例建立时统一生成并保存；适用的一方客户端事件均从同一公共上下文读取该值，用于页面实例关联和去重。业务页面、搜索、商品、收藏和购物车等模块不得各自生成另一套`page_instance_id`。

### 3.3 业务对象标识

| 对象 | 首期必填 | 有值时携带／下游补充 |
|---|---|---|
| 商品 | `listing_public_code` | 商品名称、价格、币种等业务快照；内部`product_id`和内部`listing_id`由下游商品映射补充 |
| 搜索 | `search_id` | 搜索模块正式输出的分析字段 |
| 推荐 | `module_id`、`placement_id` | 算法推荐模块将现有`placement.request_id`映射为`recommendation_request_id`；接口未提供时曝光／点击仍上报，并登记关联缺失，不伪造ID |
| 购物车 | 商品列表及金额快照 | 通过商品明细及页面上下文分析 |
| 收藏 | `listing_public_code` | 通过商品标识和身份上下文分析 |
| 订单商品行 | `order_item_id`、`listing_public_code` | 商品名称和内部商品标识可通过商品表关联 |

## 四、身份与 Session

### 4.1 身份

1. `anonymous_id`是统一匿名身份字段，直接使用现有业务`looply_anonymous_id`的值。Snowplow `domain_userid`、搜索指纹等是源系统标识，不得替代`anonymous_id`或参与身份合并。
2. 统一事件对外字段名使用`anonymous_id`，不得再生成另一套长期匿名ID。
3. 数据分析与报表文档中的`visitor_id`对应本方案的`anonymous_id`，不新增第二套访客标识。
4. 首次访问和页面初始化时，身份模块创建或解析匿名身份，并返回当前identity context。
5. 注册／登录成功后，身份模块建立`anonymous_id → user_id`确定性关系；底层分析可使用身份模块返回的`canonical_person_id`串联匿名、登录和下单路径。事件保留发生时身份，历史原始事件不回写。
6. 登出或账号切换时，身份模块必须为后续事件返回已经隔离的当前identity context和可用`anonymous_id`；原身份按身份模块规则失效。该身份变化不强制结束或新建行为Session。
7. 自动合并只能使用身份模块确认的强身份线索，例如同一`account_id`、`email_hash`、`phone_hash`、第三方登录稳定ID或`payment_customer_id`。IP、User-Agent、设备信息、浏览路径和广告来源不得触发自动合并。
8. 普通行为事件不自行生成、替换、合并或废弃`anonymous_id`，也不按`canonical_person_id`直接查询并展示跨账号历史。
9. 登录授权 Token 和`auth_session_id`不作为行为`session_id`。

### 4.2 Session

1. 首个有效事件创建行为 Session；连续30分钟没有新的有效事件，当前 Session 结束；之后的首个有效事件创建新 Session。
2. 有效事件指页面处于前台时已经满足本方案成立条件的客户端统一事件。技术心跳、接口重试、预加载、后台自动变化和服务端延迟事实不创建或延长 Session。
3. 登录、登出和切换账号不强制结束现有行为Session，也不因身份变化强制新建Session；如果当时没有有效Session，该操作仍按“首个有效事件”规则创建Session。相同`session_id`不能作为不同身份之间的合并依据，每条事件按发生时的identity context归属。
4. 不同设备或浏览器实例分别产生 Session，即使属于同一用户也不合并。
5. Session开始和结束时间由同一`session_id`内的有效事件派生，不另设`session_start`或`session_end`业务事件。

## 五、客户端统一事件

### 5.1 事件字典

| `event_name` | 业务事实 | 成立条件 | 关键业务信息 |
|---|---|---|---|
| `page_view` | 用户实际进入一个新的可访问页面 | 首次打开、刷新或有效路由切换到目标页面；页面公共上下文每次建立新的`page_instance_id`并记录一次 | 页面公共上下文 |
| `ui_interaction` | 用户完成一个没有专属业务事件的有意义操作 | 稳定动作实际发生；成功业务结果另有专属事件时不重复记录同义成功事件 | `interaction_name`、`action`、`element_id`、`target_id`、结果 |
| `search` | 用户正式提交一次站内搜索 | 轮播词＋搜索按钮、输入后回车／搜索按钮、输入联想、搜索历史、热门搜索词，或搜索结果页正式Apply筛选、Apply排序、Reset触发新请求 | `search_id`、`trigger_type`、搜索模块正式输出的分析字段 |
| `view_search_results` | 一次搜索上下文取得最终结果 | 成功有结果、成功无结果、失败或取消中的唯一终态 | `search_id`、`result_status`；成功时`result_count`，失败时`failure_type` |
| `view_item_list` | 一件商品在列表或推荐位形成有效曝光 | 商品在前台视口达到50%且持续1秒；同一`page_instance_id`内按`placement_id + listing_public_code`去重 | `listing_public_code`、`exposure_id`、模块、展示位、位置；搜索结果页必须携带`search_id` |
| `select_item` | 用户从列表或推荐位点击商品 | 点击真实发生 | `listing_public_code`、模块、展示位、位置；有前序曝光时增加`exposure_id` |
| `view_item` | 商品详情核心内容成功可分析 | 每个商详`page_instance_id`一次 | `listing_public_code`、价格、币种、来源 |
| `sign_up` | 注册事务成功 | 新账号真实建立一次 | `anonymous_id`、`user_id`、`sign_up_method`；不含PII |
| `login` | 登录事务成功 | 用户真实登录一次 | `anonymous_id`、`user_id`、`login_method`；不含PII |
| `add_to_wishlist` | 收藏关系真实新增 | 未收藏变为已收藏 | `listing_public_code`、发生页面和来源 |
| `remove_from_wishlist` | 收藏关系真实取消 | 已收藏变为未收藏 | `listing_public_code`、发生页面；取消只新增本事实，不回写或删除历史`add_to_wishlist` |
| `add_to_cart` | 商品真实加入购物车 | 购物车从不含该商品变为包含该商品 | `listing_public_code`、数量、价格、币种、来源；当前每件商品数量固定为1 |
| `view_cart` | 用户成功看到至少一件可购商品的购物车 | 每个符合条件的购物车`page_instance_id`一次；只有失效商品时不产生本事件 | `items[]`只含当前可购商品，每项含`listing_public_code`、数量和价格 |
| `remove_from_cart` | 商品真实移出购物车 | 购物车从包含该商品变为不包含该商品 | `listing_public_code`、移除前后状态；当前不定义减量场景 |
| `begin_checkout` | 用户开始进入结算流程 | 复用当前`checkout_start`真实触发点；购物车或Buy Now进入Checkout均可 | 当前`session_id`、来源和商品快照 |
| `add_shipping_info` | 配送信息和配送方式首次达到可继续结账状态 | 每个Checkout页面`page_instance_id`内，新填写、复用或修改配送信息后首次校验通过一次；重新进入Checkout形成新页面实例后可重新记录 | `page_instance_id`、`shipping_tier`、`shipping_info_source=new/existing/modified`、商品快照；不含地址明文 |
| `add_payment_info` | 支付方式和必要支付信息首次达到可提交状态 | 每个Checkout页面`page_instance_id`内，当前可用支付方式首次校验通过一次；重新进入Checkout形成新页面实例后可重新记录 | `page_instance_id`、`payment_type`、`payment_info_source=new`、商品快照；不含卡号、Token或网关原文 |

### 5.2 搜索关联规则

- 正式提交产生一个`search`并生成`search_id`。
- 同一次请求的`view_search_results`、搜索结果商品曝光和点击沿用同一`search_id`。
- 在搜索结果页正式Apply筛选、Apply排序或Reset时，产生新的`search`和新`search_id`，并由对应`view_search_results`记录该次请求的唯一终态。面板内尚未正式生效的选择只记操作，不生成新`search_id`。
- 直达搜索URL、刷新或页面恢复允许直接形成`view_search_results`；为当前搜索上下文生成`search_id`，但不补造`search`。
- 品牌和Collection入口不算搜索提交，记录入口`ui_interaction`及目标页面`page_view`。

所有Banner、Collection、搜索建议、搜索热词和商品列表的`position`从1开始。无法从当前页面或业务数据取得时留空，不使用0或猜测值。

### 5.3 推荐入口

当前统一识别以下推荐／商品发现入口：

| 入口 | 稳定业务标识要求 |
|---|---|
| 首页 Feed／For You | 稳定`module_id`、`placement_id`；接口提供`placement.request_id`时映射为`recommendation_request_id` |
| Collection商品列表 | Collection ID、稳定`module_id`和`placement_id` |
| 商详 You May Also Like | 稳定`module_id`、`placement_id`；接口提供`placement.request_id`时映射为`recommendation_request_id` |
| 搜索热词进入结果后的商品列表 | `trigger_type=popular_term_select`和`search_id`；热词本身不算商品曝光 |
| 搜索无结果页推荐 | 稳定无结果推荐模块标识和当前`search_id`；接口提供`placement.request_id`时映射为`recommendation_request_id` |
| Recently Viewed | 稳定`module_id`和`placement_id`；属于浏览历史商品模块，不冒充算法推荐 |

### 5.4 客户端事件与当前实际触发点

| 统一事件 | 当前页面／模块 | 实际触发点 | 实施类型 |
|---|---|---|---|
| `page_view` | 所有实际可访问页面 | 按5.1的页面到达规则 | 现有事件调整字段 |
| `ui_interaction` | 第8.2节页面／模块中由8.4映射的控件 | 用户完成没有专属事件的有意义操作 | 新增统一事件；复用或迁移旧通用操作 |
| `search` | Header或Mobile搜索面板、搜索页 | 用户通过回车、搜索按钮、输入联想、搜索历史、轮播词、热门搜索词，或正式Apply筛选、Apply排序、Reset提交搜索 | 调整现有提交点，并补充筛选／排序／重置的提交点 |
| `view_search_results` | 搜索结果页 | 搜索请求进入成功有结果、成功无结果、失败或取消的唯一终态 | 将结果位置的现有`search`改名并调整字段 |
| `view_item_list` | 首页Feed、Collection、搜索结果、无结果推荐、商详推荐、Mobile Favorites／Recently Viewed | 单件商品达到50%可视且持续1秒 | 将现有`item_impression`改名并调整字段 |
| `select_item` | 上述商品列表／推荐位及Shopping Bag商品卡 | 用户点击商品卡 | 将现有`item_click`改名并调整字段 |
| `view_item` | 商品详情 | 商品核心内容成功显示 | 现有事件调整字段 |
| `sign_up` | 注册流程 | 注册事务真实成功 | 现有事件调整字段 |
| `login` | 登录流程 | 登录事务真实成功 | 现有事件调整字段 |
| `add_to_wishlist` | 商品详情、Mobile Favorites及其他现有收藏入口 | 收藏关系真实新增 | 现有事件调整字段 |
| `remove_from_wishlist` | 商品详情、Mobile Favorites／Wishlist | 收藏关系真实删除 | 现有事件调整字段 |
| `add_to_cart` | 商品详情 | 加购成功且Shopping Bag状态真实变化 | 现有事件调整字段 |
| `view_cart` | Shopping Bag | 至少一件可购商品成功显示；全失效商品不产生 | 新增 |
| `remove_from_cart` | Shopping Bag | 商品成功从Shopping Bag删除 | 现有事件调整字段 |
| `begin_checkout` | Shopping Bag Check Out、商品Buy Now | 现有`checkout_start`触发 | 将现有`checkout_start`改名；不新增触发点 |
| `add_shipping_info` | Checkout配送区域 | 每个Checkout`page_instance_id`内，新填、复用或修改地址并选择配送方式后首次达到可继续状态 | 新增 |
| `add_payment_info` | Checkout支付区域 | 每个Checkout`page_instance_id`内，当前支付方式和必要信息首次校验通过并达到可提交状态 | 新增 |

## 六、权威业务事实

以下内容是一方分析所需的权威业务输入，不属于 Web 客户端埋点任务：

| `event_name`／事实名 | 权威来源 | 最小业务信息 |
|---|---|---|
| `order_created` | 订单系统／订单表 | `order_id`、创建时间、金额、币种、`items[]`（`order_item_id`、`listing_public_code`）；能够确定关联时增加`origin_session_id`，否则标记未关联且不得猜测 |
| `payment_started` | 支付系统／支付尝试表 | `payment_attempt_id`、`order_id`、支付方式、开始时间 |
| `payment_failed` | 支付系统／支付结果表 | `payment_attempt_id`、`order_id`、失败时间和低基数失败类型 |
| `purchase` | 支付成功与订单成交事实 | `order_id`、支付成功时间、成交金额、币种、`items[]`（每行至少含`order_item_id`、`listing_public_code`、该行成交金额）；整单金额不得替代商品行金额；同一订单只形成一次成交事实；能够确定关联时增加`origin_session_id`，否则标记未关联且不得猜测 |
| `refund` | 退款／售后权威表 | `refund_id`、`order_id`、退款金额、币种、退款时间、`items[]`（每行至少含`order_item_id`、`listing_public_code`、该行退款金额）；整单退款金额不得替代商品行退款金额 |

Web不得用点击、成功页、缓存或回调重复生成这些权威事实。真实交易时序和表字段由交易域方案确认；不影响第五章客户端事件实施。

服务端与数据平台需要另建接入任务，选择读取权威业务表或由业务系统推送其中一种实现方式。上线验收必须以唯一业务键对账：订单使用`order_id`，支付尝试使用`payment_attempt_id`，退款使用`refund_id`；一方平台的订单数、成交金额、退款金额及订单商品行必须与权威业务表一致。

## 七、存量埋点迁移

下表是本期唯一存量迁移表。一方平台最终物理`event_type`等于表中的目标统一事件名。旧物理事件只允许在搜推等现有专项消费者的兼容层继续存在；进入一方平台时必须只形成一条目标统一事件，不能同时进入新旧两种`event_type`。

| 当前物理事件／调用点 | 当前触发位置和语义 | 目标统一事件 | 处理方式 | 本期变化 |
|---|---|---|---|---|
| `page_view` | Web首次打开或路由变化后记录页面访问 | `page_view` | 沿用＋调整字段 | 补统一页面、身份、Session和`page_instance_id`上下文 |
| `sign_up` | 注册事务成功 | `sign_up` | 沿用＋调整字段 | 携带`anonymous_id`和`user_id`，不得包含账号原文 |
| `login` | 登录事务成功 | `login` | 沿用＋调整字段 | 携带`anonymous_id`和`user_id`；登录不切断行为Session |
| `view_item` | 商品详情核心内容成功显示 | `view_item` | 沿用＋调整字段 | 商品只强制`listing_public_code`，补来源和页面上下文 |
| `add_to_wishlist` | 收藏接口成功且收藏关系真实新增 | `add_to_wishlist` | 沿用＋调整字段 | 商品只强制`listing_public_code` |
| `remove_from_wishlist` | 取消收藏成功且关系真实删除 | `remove_from_wishlist` | 沿用＋调整字段 | 商品只强制`listing_public_code` |
| `add_to_cart` | 加购成功且购物袋状态真实变化 | `add_to_cart` | 沿用＋调整字段 | 当前数量固定为1，不实现数量增加场景 |
| `remove_from_cart` | 商品从购物袋成功删除 | `remove_from_cart` | 沿用＋调整字段 | 当前只表达整件删除，不实现数量减少场景 |
| `item_impression` | 首页、Collection、搜索结果、推荐或收藏列表中的商品曝光 | `view_item_list` | 改名＋调整字段 | 50%可视且持续1秒；按`page_instance_id + placement_id + listing_public_code`去重；搜索结果曝光必须携带`search_id` |
| `item_click` | 上述商品列表或推荐位中的商品卡点击 | `select_item` | 改名＋调整字段 | 补页面、模块、展示位、位置和可用的前序曝光／搜索关联 |
| `checkout_start` | 从Shopping Bag或Buy Now开始进入Checkout | `begin_checkout` | 改名 | 沿用现有触发点，不新增第二条开始结算事件 |
| 提交位置的现有`search` | 用户通过回车、搜索按钮、输入联想、搜索历史、轮播词或热门搜索词正式提交 | `search` | 沿用＋调整字段 | 生成`search_id`并增加`trigger_type` |
| 搜索结果页的筛选／排序／重置提交点 | 用户正式Apply筛选、Apply排序或Reset后发起新结果请求 | `search` | 新增提交事实 | 每次生成新`search_id`，`trigger_type`分别为`filter_apply`、`sort_apply`、`filter_reset` |
| 结果位置的现有`search` | 当前已确认在搜索结果返回位置发送`search`；现有代码是否覆盖失败／取消尚待开发按调用点核对 | `view_search_results` | 改名＋调整字段 | 复用同一`search_id`；目标必须补齐`success/no_results/failed/cancelled`唯一终态；直达URL可无前序`search` |
| 当前代码中的6个`share_*`物理事件 | 商品详情分享面板的打开、关闭、渠道选择、复制链接或系统分享 | `ui_interaction` | 改名并合并 | 统一`interaction_name=product_share`，使用`action`和`share_channel`区分；旧名不得继续形成一方记录。真实物理名称和调用点由开发扫描当前Web代码，并登记在技术迁移清单中 |
| 无 | 没有专属业务事件的页面有意义操作 | `ui_interaction` | 新增 | 按第8章操作表实施 |
| 无 | 非空Shopping Bag成功显示 | `view_cart` | 新增 | 每个`page_instance_id`一次，携带可购商品明细 |
| 无 | Checkout配送信息和配送方式首次达到可继续状态 | `add_shipping_info` | 新增 | 覆盖新填、复用已有和修改已有；不含地址明文 |
| 无 | Checkout支付方式和必要信息首次达到可提交状态 | `add_payment_info` | 新增 | 首期只覆盖当前新填写支付信息；不含支付敏感信息 |

## 八、页面与操作覆盖边界

### 8.1 本期原则

- 只记录有分析意义的用户操作，不采集每一次原始DOM点击、输入内容、自由文本或敏感信息。
- 每个当前可用页面应覆盖：页面访问、主要入口、Tab／筛选／排序、核心业务动作、明确失败结果及目标页面跳转。
- 已有专属业务事件时，成功结果不再重复发送同义`ui_interaction`。

### 8.2 页面、模块与展示位稳定字典

动态商品、Collection、订单或售后对象ID不写入`page_id`、`module_id`或`placement_id`，通过对应业务字段携带。

| 端别 | `page_type`／`page_id` | 本期稳定`module_id` |
|---|---|---|
| PC＋Mobile | `home/home` | `global_header`、`mobile_bottom_nav`、`home_banner`、`home_authentication`、`curated_collections`、`home_feed_tabs`、`home_product_feed`、`footer` |
| Mobile | `listing/shop` | `shop_navigation`、`search_panel` |
| PC＋Mobile | `listing/collection` | `collection_list_controls`、`collection_product_list` |
| PC＋Mobile | `listing/search_results` | `search_panel`、`search_suggestions`、`search_submit`、`search_list_controls`、`search_results_list`、`search_no_results_recommendations` |
| PC＋Mobile | `product/product_detail` | `product_header`、`product_gallery`、`product_information`、`product_actions`、`product_share`、`product_recommendations` |
| Mobile | `listing/favorites`、`listing/wishlist`、`listing/recently_viewed` | `saved_list_tabs`、`saved_product_list`、`saved_product_actions`、`saved_recommendations` |
| PC＋Mobile | `cart/cart` | `cart_items`、`cart_selection`、`cart_item_actions`、`cart_checkout`、`cart_empty_state`、`cart_unavailable_items`、`cart_authentication` |
| PC＋Mobile | `checkout/checkout` | `checkout_contact`、`checkout_shipping`、`checkout_payment`、`checkout_coupon`、`checkout_submit` |
| Mobile | `checkout/order_confirmation` | `order_confirmation` |
| PC＋Mobile | `auth/login`、`auth/sign_up`、`auth/verification`、`auth/password_recovery`、`auth/set_password`、`auth/change_password`、`auth/blocked` | `auth_form`、`auth_recovery`、`auth_legal`、`auth_consent_modal`、`auth_blocked_state` |
| PC＋Mobile | `order/orders`、`order/order_detail` | `order_list`、`order_search`、`order_detail`、`order_refund_modal`、`order_support`、`delivery_tracking` |
| PC＋Mobile | `returns/returns`、`returns/return_detail` | `returns_list`、`returns_application`、`returns_information`、`returns_status` |
| PC＋Mobile | `account/account`、`account/profile`、`account/address_list`、`account/address_edit`、`account/privacy` | `account_orders`、`account_navigation`、`account_profile`、`account_addresses`、`account_preferences`、`account_privacy`、`account_authentication` |
| PC＋Mobile | `content/contact_us`、`content/about`、`content/authentication`、`content/privacy_policy`、`content/terms_of_service`、`content/accessibility_statement`、`content/your_privacy_choices` | `contact_form`、`contact_information`、`content_navigation`、`footer` |

PC不定义`listing/shop`、`listing/favorites`、`listing/wishlist`或`listing/recently_viewed`页面。Delivery是订单页内的物流详情模块，不定义独立`page_id`。

商品曝光与点击使用下列封闭`placement_id`：

| 场景 | `placement_id` |
|---|---|
| 首页For You | `home_feed_for_you` |
| 首页New Arrivals | `home_feed_new_arrivals` |
| Collection商品列表 | `collection_results` |
| 搜索结果列表 | `search_results` |
| 搜索无结果推荐 | `search_no_results_recommendations` |
| 商详You May Also Like | `product_you_may_also_like` |
| 商详Recently Viewed | `product_recently_viewed` |
| Mobile Wishlist | `favorites_wishlist` |
| Mobile Recently Viewed | `favorites_recently_viewed` |
| Mobile Favorites推荐 | `favorites_recommendations` |
| Shopping Bag商品列表 | `shopping_bag_items` |

### 8.3 页面覆盖索引

本期需覆盖的页面组为：全站公共导航、首页、Mobile Shop、搜索、Collection、商品详情、Mobile Favorites／Wishlist／Recently Viewed、Shopping Bag、Checkout与订单确认页、登录注册与密码找回、Orders／Order Detail、Returns、Account／Profile／Address／Privacy、Contact Us、About、Authentication介绍页及政策页。每个实际可访问页面按5.1记录`page_view`；页面内操作的唯一命名以8.4为准。

普通滚动、输入过程、文字选择、组件渲染和无操作的状态展示不采集。

### 8.4 页面与操作唯一映射

下表是页面操作的唯一命名位置。每一行只定义一组可唯一匹配的操作；同行多个`action`时，必须按“`action` → `element_id` → `target_id`”的显式映射实施。成功结果已有专属事件时，不再发送同义`ui_interaction`。

商品列表和推荐位先按以下规则复用专属事件：

| 页面／展示位 | 曝光 | 点击进商详 | 收藏／取消 |
|---|---|---|---|
| 首页Feed、Collection、搜索结果、搜索无结果推荐、商详推荐、Mobile Wishlist／Recently Viewed／Favorites推荐 | `view_item_list` | `select_item` | `add_to_wishlist`／`remove_from_wishlist` |
| Shopping Bag商品列表 | `view_cart`承载列表展示 | `select_item` | 无 |

| 端别／页面 | `module_id` | `interaction_name` | 稳定操作映射 |
|---|---|---|---|
| PC＋Mobile／全站 | `global_header`／`mobile_bottom_nav` | `global_navigation` | `select` → `logo`／`header_nav_item`／`account_entry`／`favorites_entry`／`cart_entry`／`mobile_nav_item` → 目标`page_id` |
| PC／全站Header | `global_header` | `navigation_menu` | `open` → `more_navigation_button` → `more_navigation`；`close` → `more_navigation_close` → `more_navigation`；`select` → `more_nav_item` → 目标`page_id` |
| PC＋Mobile／Market & Language | `global_header` | `market_language` | `open` → `market_language_entry` → `market_language`；`close` → `market_language_close` → `market_language`；`select_market` → `market_option` → Market枚举；`select_language` → `language_option` → Language枚举；`select_currency` → `currency_option` → Currency枚举 |
| PC＋Mobile／通用失败态 | 当前失败模块 | `retry` | `submit` → `retry_button` → 原失败操作的稳定`element_id` |
| PC＋Mobile／首页 | `home_banner` | `home_banner` | `change` → `banner_dot`／`banner_swipe` → Banner配置ID；`select` → `banner_item`／`explore_button` → 目标`page_id` |
| PC＋Mobile／首页 | `home_authentication` | `authentication_entry` | `select` → `explore_details_button` → `content/authentication` |
| PC＋Mobile／首页 | `curated_collections` | `curated_collection` | `scroll` → `collection_rail` → `curated_collections`；`select` → `collection_card` → `collection_id` |
| PC＋Mobile／首页 | `home_feed_tabs` | `home_feed_tab` | `change` → `feed_tab` → `for_you`／`new_arrivals` |
| Mobile／首页 | `mobile_bottom_nav` | `page_navigation` | `back_to_top` → `back_to_top_button` → `page_top` |
| Mobile／Shop | `shop_navigation` | `shop_section` | `change` → `shop_section_item` → 类目、品牌或Tab稳定ID |
| PC＋Mobile／搜索入口 | `search_panel` | `search_panel` | `open` → `search_entry` → `search_panel`；`close` → `search_close` → `search_panel` |
| PC＋Mobile／搜索面板 | `search_suggestions` | `popular_navigation` | `select_popular_brand` → `popular_brand_item` → `collection_id`；`select_popular_collection` → `popular_collection_item` → `collection_id` |
| PC＋Mobile／Collection | `collection_list_controls` | `collection_filter` | `open` → `filter_control` → `collection_filter`；`close` → `filter_close` → `collection_filter`；`expand_group`／`collapse_group`／`view_all_options` → `filter_group` → 筛选组ID；`select` → `filter_option` → 筛选项稳定值；`reset` → `filter_reset` → `collection_id`；`apply` → `filter_apply` → `collection_id` |
| PC＋Mobile／Collection | `collection_list_controls` | `collection_sort` | `open` → `sort_control` → `collection_sort`；`close` → `sort_close` → `collection_sort`；`select` → `sort_option` → 排序枚举；`apply` → `sort_apply` → 排序枚举 |
| PC＋Mobile／搜索结果 | `search_list_controls` | `search_filter` | `open` → `filter_control` → `search_filter`；`close` → `filter_close` → `search_filter`；`expand_group`／`collapse_group`／`view_all_options` → `filter_group` → 筛选组ID；`select` → `filter_option` → 筛选项稳定值；`reset` → `filter_reset` → 新`search_id`；`apply` → `filter_apply` → 新`search_id` |
| PC＋Mobile／搜索结果 | `search_list_controls` | `search_sort` | `open` → `sort_control` → `search_sort`；`close` → `sort_close` → `search_sort`；`select` → `sort_option` → 排序枚举；`apply` → `sort_apply` → 新`search_id` |
| PC＋Mobile／商详 | `product_header` | `product_navigation` | `back` → `back_button` → 上一`page_id`；`select_cart` → `cart_entry` → `cart/cart` |
| PC＋Mobile／商详 | `product_gallery` | `product_gallery` | `change` → `image_item`／`gallery_previous`／`gallery_next` → 图片位置；`preview` → `main_image` → 图片位置；`close_preview` → `image_preview_close` → 图片位置；`zoom_in`／`zoom_out` → `image_zoom` → 图片位置 |
| PC＋Mobile／商详 | `product_information` | `product_information` | `expand`／`collapse` → `product_section` → `condition`／`description`／`shipping_returns` |
| PC＋Mobile／商详 | `product_information` | `product_info_modal` | `open`／`close` → `information_entry`／`information_close` → `certified_authentic`／`condition_guide`／`size_guide` |
| PC＋Mobile／商详 | `product_share` | `product_share` | `open` → `share_button` → `listing_public_code`；`close` → `share_close` → `listing_public_code`；`select_channel` → `share_channel_item` → `listing_public_code`（另带`share_channel`）；`copy_link` → `copy_link_button` → `listing_public_code`；`open_system_share` → `system_share_button` → `listing_public_code` |
| PC＋Mobile／商详 | `product_recommendations` | `recommendation_rail` | `scroll` → `recommendation_rail` → `placement_id`；`previous`／`next` → `recommendation_previous`／`recommendation_next` → `placement_id` |
| PC＋Mobile／商详 | `product_recommendations` | `product_recommendation_navigation` | `view_all` → `module_view_all` → `listing/recently_viewed`；`find_more` → `find_more_button` → 目标`page_id` |
| Mobile／Favorites | `saved_list_tabs` | `saved_list_tab` | `change` → `saved_list_tab` → `wishlist`／`recently_viewed` |
| Mobile／Favorites | `saved_product_actions` | `saved_list_entry` | `select` → `explore_items_button`／`add_more_card` → 目标`page_id` |
| PC＋Mobile／Shopping Bag | `cart_selection` | `cart_selection` | `select_item`／`unselect_item` → `cart_item_checkbox` → `listing_public_code`；`select_all`／`unselect_all` → `select_all_checkbox` → `all_items` |
| Mobile／Shopping Bag | `cart_item_actions` | `cart_action_panel` | `open` → `cart_item` → `listing_public_code`；`close` → `cart_action_panel` → `listing_public_code` |
| PC＋Mobile／Shopping Bag空态 | `cart_empty_state` | `cart_empty_navigation` | `select` → `continue_shopping_button` → 目标`page_id` |
| PC／Shopping Bag失效区 | `cart_unavailable_items` | `unavailable_items` | `clear_all` → `clear_all_button` → `unavailable_items` |
| PC＋Mobile／Shopping Bag游客态 | `cart_authentication` | `authentication_entry` | `select` → `login_entry`／`continue_entry` → 目标`page_id` |
| PC＋Mobile／Checkout | `checkout_contact` | `marketing_subscription` | `enable`／`disable` → `marketing_subscription_checkbox` → `marketing_subscription` |
| PC＋Mobile／Checkout | `checkout_shipping` | `shipping_address` | `add` → `add_address_button` → `new_address`；`edit` → `address_edit_button` → 地址内部对象ID；`select` → `address_item` → 地址内部对象ID；`save` → `address_save_button` → 地址内部对象ID或`new_address`；`back` → `address_back_button` → `checkout/checkout` |
| PC＋Mobile／Checkout | `checkout_shipping` | `shipping_tier` | `select` → `shipping_tier_option` → 配送方式枚举 |
| PC＋Mobile／Checkout | `checkout_payment` | `payment_method` | `select` → `payment_method_option` → `credit_card`／`paypal`／`klarna` |
| PC＋Mobile／Checkout | `checkout_contact` | `phone_information` | `open` → `phone_information_control` → `phone_information`；`close` → `phone_information_close` → `phone_information` |
| PC／Checkout | `checkout_payment` | `security_code_information` | `open` → `security_code_information_control` → `security_code_information`；`close` → `security_code_information_close` → `security_code_information` |
| PC＋Mobile／Checkout | `checkout_coupon` | `checkout_coupon` | `apply` → `coupon_apply_button` → `checkout_coupon`；`remove` → `coupon_remove_button` → `checkout_coupon`；不携带优惠码原文 |
| PC＋Mobile／Checkout | `checkout_submit` | `checkout_submit` | `submit` → `pay_now_button` → 当前Checkout`page_instance_id` |
| Mobile／订单确认页 | `order_confirmation` | `order_confirmation` | `copy_order_id` → `copy_order_id_button` → `order_id`；`continue_shopping` → `continue_shopping_button` → `listing/shop` |
| PC＋Mobile／登录注册 | `auth_form` | `authentication_tab` | `change` → `auth_tab` → `auth/login`／`auth/sign_up` |
| PC＋Mobile／登录注册 | `auth_form` | `authentication_form` | `submit` → `auth_submit_button` → `login`／`sign_up` |
| PC＋Mobile／已记忆账号 | `auth_form` | `remembered_login` | `continue` → `remembered_account` → `login`；`switch_account` → `other_account` → `auth/login` |
| PC＋Mobile／密码找回／修改 | `auth_recovery` | `password_recovery` | `start` → `forgot_password_link` → `auth/password_recovery`；`submit_password` → `password_submit_button` → `auth/set_password`或`auth/change_password` |
| PC＋Mobile／验证码 | `auth_recovery` | `verification_code` | `send`／`resend` → `verification_code_button` → `auth/verification`；`submit` → `verification_code_submit` → `auth/verification` |
| PC＋Mobile／认证流程 | `auth_recovery` | `authentication_navigation` | `back` → `auth_back_button` → 目标认证`page_id` |
| PC＋Mobile／登录受阻页 | `auth_blocked_state` | `authentication_blocked` | `retry` → `blocked_retry_button` → 原认证步骤ID；`back` → `blocked_back_button` → 目标认证`page_id`；`contact_support` → `blocked_support_button` → `content/contact_us` |
| PC＋Mobile／认证法律入口 | `auth_legal` | `legal_navigation` | `select` → `terms_link`／`privacy_link` → `content/terms_of_service`／`content/privacy_policy` |
| Mobile／同意更新弹窗 | `auth_consent_modal` | `consent_update` | `confirm` → `consent_confirm_button` → 同意类型ID；`close` → `consent_close_button` → 同意类型ID |
| PC＋Mobile／Orders | `order_list` | `order_status_tab` | `change` → `order_status_tab` → 订单状态枚举 |
| PC＋Mobile／Orders | `order_list` | `order_navigation` | `select_order` → `order_item` → `order_id` |
| PC＋Mobile／Orders | `order_search` | `order_search` | `open` → `order_search_entry` → `order_search`；`close` → `order_search_close` → `order_search`；`submit`／`auto_query` → `order_search_submit` → `order_search`；`select_result` → `order_search_result` → `order_id` |
| PC＋Mobile／Order Detail | `order_detail` | `order_action` | `copy_order_id` → `copy_order_id_button` → `order_id`；`select_tracking` → `tracking_entry` → `shipment_id`；`select_return` → `return_entry` → `returns/returns`；`back` → `order_back_button` → 上一`page_id` |
| PC＋Mobile／Order Detail | `order_refund_modal` | `refund_information` | `open` → `refund_information_entry` → `order_id`；`close` → `refund_information_close` → `order_id` |
| PC＋Mobile／Order Detail | `order_support` | `support_navigation` | `select` → `contact_button` → `content/contact_us` |
| PC＋Mobile／Order Detail | `delivery_tracking` | `tracking_details` | `open` → `tracking_details_entry` → `shipment_id`；`close` → `tracking_details_close` → `shipment_id` |
| PC＋Mobile／Returns | `returns_list` | `returns_filter` | `select_order` → `returns_filter_control` → `order_id`；`clear` → `returns_filter_clear` → `all_orders` |
| PC＋Mobile／Returns | `returns_list` | `return_case_navigation` | `select` → `return_case_item` → 售后对象ID |
| PC＋Mobile／Returns申请 | `returns_application` | `return_item` | `select` → `return_item` → `order_item_id`；`unselect` → `return_item` → `order_item_id` |
| PC＋Mobile／Returns申请 | `returns_application` | `return_reason` | `open` → `return_reason_control` → `order_item_id`；`close` → `return_reason_close` → `order_item_id`；`select` → `return_reason_option` → 退货原因枚举 |
| PC＋Mobile／Returns申请 | `returns_application` | `return_evidence` | `add` → `evidence_add_button` → `order_item_id`；`remove` → `evidence_remove_button` → `order_item_id`；`replace` → `evidence_replace_button` → `order_item_id` |
| PC＋Mobile／Returns申请 | `returns_application` | `return_application` | `submit` → `return_submit_button` → `order_item_id`；`edit` → `return_edit_button` → 售后对象ID；`resubmit` → `return_resubmit_button` → 售后对象ID；`open_cancel` → `return_cancel_button` → 售后对象ID；`confirm_cancel` → `cancel_confirm_button` → 售后对象ID；`cancel_cancel` → `cancel_back_button` → 售后对象ID |
| PC＋Mobile／Returns说明 | `returns_information` | `refund_fee_information` | `open`／`close` → `refund_fee_information_control`／`refund_fee_information_close` → 售后对象ID |
| PC＋Mobile／Returns说明 | `returns_information` | `return_shipping_information` | `open`／`close` → `return_shipping_information_control`／`return_shipping_information_close` → 售后对象ID |
| PC＋Mobile／Returns状态页 | `returns_status` | `return_status_action` | `back` → `return_status_back` → `returns/returns`；`contact_support` → `return_support_button` → `content/contact_us`；`update_request` → `update_request_button` → 售后对象ID；`open_cancel` → `cancel_request_button` → 售后对象ID |
| PC＋Mobile／Returns寄回物流 | `returns_status` | `return_tracking` | `copy` → `return_tracking_copy_button` → `shipment_id`；`open` → `return_tracking_entry` → `shipment_id` |
| PC＋Mobile／Account | `account_orders` | `order_status_entry` | `select` → `order_status_entry` → `processing`／`shipped`／`delivered`／`refunds` |
| PC＋Mobile／Account | `account_navigation` | `account_section` | `select` → `account_section_item` → `account/profile`／`account/address_list`／`account/privacy`或对应政策`page_id` |
| PC＋Mobile／Profile | `account_profile` | `profile` | `edit` → `profile_edit_control` → `nickname`／`gender`；`save` → `profile_save_button` → `profile`；`cancel` → `profile_cancel_button` → `profile` |
| PC＋Mobile／Address | `account_addresses` | `address` | `add` → `address_add_button` → `new_address`；`edit` → `address_edit_button` → 地址内部对象ID；`save` → `address_save_button` → 地址内部对象ID或`new_address`；`set_default` → `address_default_control` → 地址内部对象ID；`open_delete` → `address_delete_button` → 地址内部对象ID；`confirm_delete` → `address_delete_confirm` → 地址内部对象ID；`cancel_delete` → `address_delete_cancel` → 地址内部对象ID；`cancel`／`back` → `address_cancel_button`／`address_back_button` → `account/address_list` |
| PC＋Mobile／Account偏好 | `account_preferences` | `account_preference` | `open`／`close` → `preference_control`／`preference_close` → `country_region`／`language`／`currency`；`select` → `preference_option` → 选中稳定枚举 |
| PC＋Mobile／Account订阅 | `account_preferences` | `subscription` | `subscribe`／`unsubscribe` → `subscription_control` → 订阅类型ID |
| PC＋Mobile／Account隐私 | `account_privacy` | `account_privacy` | `change` → `privacy_preference_control` → 隐私选择类型ID；`download_data` → `download_data_button` → `current_account`；`open_delete_account` → `delete_account_button` → `current_account`；`confirm_delete_account` → `delete_account_confirm` → `current_account`；`cancel_delete_account` → `delete_account_cancel` → `current_account` |
| PC＋Mobile／Account | `account_authentication` | `account_logout` | `open` → `logout_entry` → `logout`；`confirm` → `logout_confirm_button` → `logout`；`cancel` → `logout_cancel_button` → `logout` |
| PC＋Mobile／Account游客态 | `account_authentication` | `authentication_entry` | `login` → `login_entry` → `auth/login`；`register` → `register_entry` → `auth/sign_up` |
| PC＋Mobile／Contact Us | `contact_form` | `contact_request` | `submit` → `contact_submit_button` → `contact_form` |
| PC＋Mobile／Contact Us | `contact_information` | `email_contact` | `select` → `contact_email_link` → `email_client` |
| PC＋Mobile／Contact Us | `content_navigation` | `policy_navigation` | `select` → `privacy_choices_entry` → `content/your_privacy_choices` |
| PC＋Mobile／Footer | `footer` | `newsletter` | `submit` → `newsletter_submit_button` → `newsletter`；不携带邮箱原文 |
| PC＋Mobile／Footer | `footer` | `footer_navigation` | `select` → `footer_link` → 目标`page_id` |
| PC＋Mobile／Footer | `footer` | `social_entry` | `select` → `social_link` → `facebook`／`tiktok`／`instagram`／`youtube` |
| PC＋Mobile／Authentication介绍页 | `content_navigation` | `guarantee_navigation` | `select` → `guarantee_details_link` → `returns/returns` |

所有`ui_interaction`携带本表定义的`interaction_name`、`action`、`element_id`和适用时的`target_id`。同一操作由图标、文字和容器共同组成时只记录一次，不因DOM层级重复。表单、地址、邮箱、电话、验证码、密码、优惠码、凭证文件和自由错误文本不进入普通分析事件。

### 8.5 当前不存在或暂不实施

以下能力不进入本期触发矩阵，未来功能上线时另行补充：

- 购物车商品数量增加／减少；当前商品数量固定为1。
- 购物车优惠码入口。
- Cart的Move to Wishlist；当前为Coming Soon。
- 已保存支付工具的复用或修改；当前`payment_info_source`只取`new`。
- Tablet和App页面交互。

PC没有独立Shop和Favorites页面，不实现这两个PC页面的埋点。Mobile现有Shop和Favorites按实际页面实施。

## 九、统一枚举

| 字段 | 允许值／映射 |
|---|---|
| `result_state` | `success`、`failed`、`cancelled` |
| `failure_type` | 低基数失败分类；表单校验失败使用`validation_failed` |
| `result_status` | `success`、`no_results`、`failed`、`cancelled` |
| `payment_type` | 直接沿用当前API：`credit_card`、`paypal`、`klarna`，不做额外转换 |
| `payment_info_source` | 首期仅`new` |
| `shipping_info_source` | `new`、`existing`、`modified` |
| `trigger_type` | `carousel_term_button`、`manual_enter`、`manual_search_button`、`suggestion_select`、`history_select`、`popular_term_select`、`filter_apply`、`sort_apply`、`filter_reset` |
