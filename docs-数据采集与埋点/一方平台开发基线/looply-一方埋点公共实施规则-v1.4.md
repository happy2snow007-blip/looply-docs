# Looply 一方埋点公共实施规则

> 版本：v1.4  
> 日期：2026-08-21  
> 状态：开发实施基线  
> 来源：从《Looply 数据采集与埋点产品需求 v1.7》中抽取两张开发表无法逐行表达的公共规则。

## 一、文档用途与唯一权威位置

一方埋点开发交付由以下三份材料共同组成：

1. 《Looply 一方埋点新增与修改清单 v1.4》：事件、页面、模块、动作、触发时机、业务参数及存量迁移的唯一权威表。
2. 《Looply 一方埋点新增公共字段清单 v1.4》：相对现有埋点服务需要新增的公共字段及字段来源的唯一权威表。
3. 本文档：跨事件规则、稳定页面／模块／展示位字典和服务端权威事实的唯一权威位置。

事件工作簿中的“公共字段”Sheet仅作为索引，不重复定义字段。现有公共字段继续沿用埋点服务当前基线；本次只按独立公共字段表增加尚未存在的字段。

## 二、本期范围

- 覆盖当前 PC Web 和 Mobile Web 已存在的页面及有意义用户操作。
- PC没有独立Shop和Favorites聚合页面；覆盖PC现有Wishlist和Recently Viewed页面。
- Mobile覆盖现有Shop和Favorites页面。
- Tablet和App不在本期范围。
- 本期一方埋点不定义GA4、广告平台或搜推算法专项字段。
- SDK、网关、消息队列、存储表、重试机制和字段技术类型由技术方案确定。

## 三、事件成立与防重复

1. 只有真实发生的用户行为或业务结果才形成事件；DOM点击、组件渲染、预加载、技术心跳和接口重试本身不形成业务事件。
2. 同一个业务事实在一方平台只形成一条记录。旧事件与新事件可在适配层兼容，但不能同时进入一方平台造成双发双计。
3. `event_name`／最终物理`event_type`表示事件类型；`event_id`表示一条已经发生的业务事实，两者不得混用。
4. 同一事实重试时沿用同一`event_id`，不得因重试生成新的业务事实。
5. 事件是否成立只取决于业务事实是否发生，不因参数缺失停止发送。适用且能够取得的参数正常携带；暂时无法取得时省略，不伪造默认值。文档中的“业务必需”表示数据质量要求，不表示缺少该参数时抑制整条事件；本期不为参数缺失新增远程诊断事件。
6. 有专属业务事件的成功结果不再重复发送同义`ui_interaction`。例如加购成功只记录`add_to_cart`。
7. 普通滚动、输入过程、文字选择、无操作的状态展示和没有分析意义的点击不采集。

### 3.1 页面实例

- 用户首次打开、刷新或有效路由切换到新的可访问页面时，建立新的`page_instance_id`并记录一次`page_view`。
- `page_instance_id`由Web页面公共层统一生成并保存；适用的一方客户端事件读取同一个值。
- 业务模块不得分别生成自己的`page_instance_id`。
- `page_instance_id`不是页面URL、用户ID或`session_id`。

### 3.2 商品曝光

- 单件商品在前台视口达到50%且持续1秒，形成一次有效曝光。
- 同一`page_instance_id`内，同一`placement_id + listing_public_code`只记录一次。
- 页面处于后台、失焦或未达到阈值时不记录曝光。
- 新的页面实例可重新记录曝光；刷新或重新进入页面会产生新的`page_instance_id`。
- 每次有效单商品曝光由Web生成唯一`exposure_id`并随`view_item_list`发送；同一卡片随后产生`select_item`时沿用该值。没有同一卡片前序有效曝光时省略，不补造。

### 3.3 通用操作的结果字段

- `result_state`和`failure_type`的逐动作适用范围，以《Looply 一方埋点新增与修改清单 v1.4》工作簿中的“结果字段映射”Sheet为唯一依据。
- 未列入“结果字段映射”的`interaction_name + action`默认不携带这两个字段。
- 字段允许值以第六章为准；自由错误文本不得上传。
- `cancelled`只用于请求已经发起后，被用户明确取消、被新请求替换，或因离开页面而中断且未形成成功／失败终态的场景。提交前关闭弹窗或返回只记录对应`close`／`back`操作，不写`cancelled`。

### 3.4 `ui_interaction`页面操作字段

事件清单“动作”列按`interaction_name：action → element_id → target_id`表达稳定业务映射：

- `interaction_name`、`action`和`element_id`按本行已列出的稳定值发送；
- 操作存在明确目标时发送本行箭头末端的`target_id`；没有明确目标时省略；
- 商品、订单、售后等对象使用本行动作中列出的稳定业务对象标识；
- 事件清单“参数”列只列本行额外需要的业务字段；为空表示没有额外业务字段，不表示省略适用的公共字段；
- 成功事件替代及失败事件规则以工作簿“结果字段映射”Sheet为准，不由各业务页面自行判断。

## 四、身份与Session

### 4.1 身份

1. `anonymous_id`由身份模块生成，是用于串联登录前后行为的稳定匿名主体ID；身份模块必须通过可供埋点读取的身份上下文提供该值，埋点模块不得另建第二套长期匿名ID。
2. `domain_userid`由Snowplow生成，作为浏览器侧辅助标识与`anonymous_id`同时上传，但不替代`anonymous_id`，也不用于跨设备自动合并。
3. 当前代码中的`getAnonymousId()`如果返回Snowplow DUID，不得直接用于`anonymous_id`；HttpOnly匿名能力Cookie也不得由Web读取或作为分析ID上传。
4. 已登录事件同时携带当前`user_id`。本期身份串联使用`anonymous_id → user_id`，不新增或上传`canonical_person_id`。
5. 登录态直接根据事件发生时是否携带`user_id`判断；公共字段表和事件协议均不新增`identity_state`。
6. 注册或登录成功后，由身份模块建立`anonymous_id → user_id`确定性关系。历史原始事件保留发生时身份，不回写。
7. 登出或切换账号后，后续事件使用身份模块返回的、已经隔离的当前身份上下文。
8. IP、User-Agent、设备信息、浏览路径或广告来源不得触发自动合并。
9. 登录Token和`auth_session_id`不得作为行为`session_id`。
10. 数据分析文档中的`visitor_id`对应本方案的`anonymous_id`，不新增第二套访客标识。

### 4.2 Session

1. `session_id`直接复用现有Snowplow `domain_sessionid`（sid），不再建设第二套一方Session ID。
2. 连续30分钟没有新的Snowplow客户端事件后，由Snowplow在后续事件发生时生成新的sid；任何实际发送给Snowplow的客户端事件都会续期当前Session。登录、登出和账号切换不强制切断当前Session。
3. 同一浏览器配置中的多个标签页共享当前sid；不同浏览器配置或设备分别产生Session，即使属于同一用户也不合并。
4. 一方报表只统计至少包含一个一方有效事件的`session_id`。报表中的Session开始和结束时间根据该`session_id`内第一条和最后一条一方有效事件派生，不新增`session_start`或`session_end`业务事件；技术心跳、接口重试、预加载、后台自动变化和服务端延迟事实即使可能续期Snowplow Session，也不作为一方有效事件或独立Session统计。
5. `begin_checkout`携带当前`session_id`。订单、支付和成交事实能够通过Checkout／订单链路确定来源Session时记录为`origin_session_id`；无法确定时省略，不猜测。具体贯通方式由服务端与数据平台接入任务确定。

## 五、业务对象与关联规则

### 5.1 商品与交易对象

- 商品对外稳定标识统一使用`listing_public_code`，来源为`listings.public_code`。
- 内部`listing_id`、实物商品编码、SKU或SEO slug不得替代`listing_public_code`。
- 内部`product_id`和内部`listing_id`可由下游商品映射补充，不要求Web为取得内部ID阻塞事件发送。
- 订单商品行使用`order_item_id + listing_public_code`，用于关联同一订单中的具体商品行。
- `position`从1开始；无法取得时省略，不使用0或猜测值。
- `source_type`记录业务事实发生前的原始站内来源粗分类；完整允许值和入口映射见本节下方权威表。能够识别真实入口时携带；无法确定时留空，不得根据后续结果反推。

事件参数优先复用现有埋点契约，不再使用“商品快照”“发生页面”“来源”“移除前后状态”等概念占位，也不为同一信息新建一套平行字段：

| 产品需要的信息 | 本期事件字段／实体 | 规则 |
|---|---|---|
| 商品标识、价格和币种 | `product.listing_public_code`、`product.price`、`product.currency` | 复用现有`product`实体；`listing_public_code`必带，价格和币种可取得时携带。多商品事件的`product`使用数组，不再另建`items[]`。 |
| 事件发生页面 | `page.page_type`、`page.page_id` | 复用现有`page`实体；`page_instance_id`作为公共上下文单独携带。 |
| 商品所在展示位 | 现有`placement`实体＋稳定`module_id`、`placement_id` | `placement`保留当前展示位置上下文；稳定业务模块和展示位使用5.3字典。 |
| 购物袋当前汇总 | `cart.item_count`、`cart.amount`、`cart.currency` | 复用现有`cart`实体；仅表达事件成功后的当前汇总，不新建“移除前后状态”。 |
| 注册／登录方式 | `method` | 复用现有事件字段，不新增`sign_up_method`或`login_method`。 |
| 搜索分析词 | `query` | 复用现有`search.query`；下游现有展开字段为`search_query`。结果页URL中的`keyword`在事件上报时映射为`query`。 |
| 原始站内来源 | `source_type`、`source_page_id`、`source_module_id`、`source_event_id` | 仅在真实可识别时携带，不使用笼统的“来源”字段，不得根据后续结果反推或补造。 |
| 加购／移除数量 | `quantity` | 复用现有事件字段；当前商品数量固定为1，整件加入或删除均记`quantity=1`。 |

`source_type`按用户实际进入当前业务事实前的直接入口取值：

| `source_type` | 唯一业务含义 | 对应入口／展示位 |
|---|---|---|
| `search` | 从正式搜索结果列表进入 | `search_results` |
| `recommendation` | 从推荐或商品发现模块进入 | `home_feed_for_you`、`home_feed_new_arrivals`、`search_no_results_recommendations`、`product_you_may_also_like`、`favorites_recommendations` |
| `collection` | 从Collection商品列表进入 | `collection_results` |
| `wishlist` | 从收藏商品列表进入 | `favorites_wishlist` |
| `cart` | 从Shopping Bag商品列表进入，或从Shopping Bag开始Checkout | `shopping_bag_items`及Shopping Bag的Check Out入口 |
| `buy_now` | 从商品详情页Buy Now直接开始Checkout | 商品详情页Buy Now入口 |
| `direct` | 直接打开商品详情，且没有可识别的站内前序入口 | 直达商品详情URL、书签或其他无站内前序事实的进入方式 |
| `other_internal` | 有明确站内入口，但不属于前述七类 | `product_recently_viewed`、`favorites_recently_viewed`及其他已识别的普通站内入口 |

同一入口不得由开发在多个值之间自行选择。页面刷新、恢复或后续操作不得把已经记录的原始来源改写为新的分类；无法确认直接来源时留空，不用`direct`代替未知来源。

`source_event_id`只建立以下同商品、同一真实操作链：

1. 用户点击商品列表形成`select_item`并进入同一商品商详时，`view_item.source_event_id = select_item.event_id`。
2. 用户在商详收藏、加购或通过Buy Now开始Checkout时，对应`add_to_wishlist`、`add_to_cart`或`begin_checkout`的`source_event_id`引用当前页面同一商品的`view_item.event_id`。
3. 从Shopping Bag进入Checkout时不强行引用某一商品事件，只使用`source_type=cart`以及来源页面、模块。
4. 没有同商品真实前序事件时省略；不得引用最近任意事件、跨商品引用或补造ID。

现有公共字段继续按当前语义使用。本期非站外触点新增字段与现有字段的边界如下；同一行中的字段不得互相替代：

| 本期字段 | 相关现有字段 | 唯一语义与处理结论 |
|---|---|---|
| `anonymous_id` | `domain_userid` | 两者同时上传。`anonymous_id`是身份模块生成的稳定匿名主体ID；`domain_userid`是Snowplow浏览器辅助标识。 |
| `session_id` | Snowplow `domain_sessionid` | 直接复用现有sid作为一方行为Session标识；Snowplow客户端事件按30分钟超时规则续期，不再生成第二套Session ID，登录Session和GA4 Session不得替代。 |
| `page_instance_id` | `page_type`、`page_id`、`page_url` | 新增一次页面访问实例标识；现有字段继续描述页面类型、页面ID和URL。 |
| `previous_page_type` | `referrer_url` | 新增稳定的上一页面业务类型；`referrer_url`继续保留原始来源URL，两者不互相推导。 |
| `market` | `geo_country` | 新增当前业务市场；`geo_country`继续表示地理定位结果。 |
| `module_id` | `placement_module_name` | 新增封闭字典中的稳定业务模块ID；现有字段不改名，也不得用展示名称替代`module_id`。 |
| `placement_id` | 现有`placement_*`字段 | 新增封闭字典中的稳定业务展示位ID；现有`placement_scene/module_name/list_id/position/page/page_size/impression_id/source`继续描述当前展示上下文。 |
| `source_type`、`source_page_id`、`source_module_id`、`source_event_id` | 当前事件的`page`、`placement`和`event_id` | 新增前序真实来源关系；现有字段继续描述当前事件本身，不能用当前上下文冒充前序来源。 |
| `result_state` | `result_status` | `result_state`描述通用用户操作结果；`result_status`只描述搜索结果请求终态，两者按适用事件分别使用。 |
| `failure_type` | 无同义现有字段 | 新增表单校验失败分类，允许值以第六章为准。 |

### 5.2 搜索

1. 正式搜索提交包括：轮播词搜索按钮、手动输入后回车、手动输入后点击搜索按钮、点击输入联想、点击搜索历史和点击热门搜索词。
2. 品牌和Collection入口不属于搜索提交，记录入口操作及目标页面访问。
3. 搜索提交使用搜索模块当前实际用于发起请求的分析词，不新增独立清洗服务；当前URL字段名继续沿用现有实现，由事件适配层完成字段映射。
4. `search`、`view_search_results`、搜索结果商品曝光和商品点击使用同一组结构化搜索信息。事件适配按下表把现有URL状态映射到一方事件字段：

| URL业务信息 | 结果页URL字段 | 一方事件字段 |
|---|---|---|
| 搜索模块实际请求词 | `keyword` | `query`；下游展开为现有`search_query` |
| 搜索触发方式 | `trigger_type` | `trigger_type` |
| 已生效筛选条件 | `filter_*`重复参数及价格区间参数 | `filter_ids[]`：离散筛选项使用`维度:稳定值`；价格区间使用`price:{币种}:{最低价或*}-{最高价或*}`；全部去重后按维度和值稳定排序 |
| 已生效排序 | `sort` | `sort_type`：直接使用当前API稳定`sort_key` |

价格区间使用当前Market结算币种的大写ISO 4217代码；同时存在最低价和最高价时例如`price:USD:100-900`，仅最低价时为`price:USD:100-*`，仅最高价时为`price:USD:*-900`。金额使用无千分位的标准数字文本；未选择价格筛选时不生成`price`项。

5. `view_search_results`、搜索结果商品曝光和商品点击从当前结果页URL解析上述信息，不使用`search_id`。直达URL不存在可识别`trigger_type`时省略，不补造。
6. 筛选、排序或重置只记录对应操作；结果更新后形成新的`view_search_results`，不新增`search`。
7. 直达搜索URL、刷新或页面恢复允许直接形成`view_search_results`，不得补造用户主动搜索。
8. 搜索词使用搜索模块现有请求链路已经采用的分析值；数据采集不额外定义或新增搜索词清洗、标准化服务。

`trigger_type`只取以下值：

| 值 | 含义 |
|---|---|
| `carousel_term_button` | 点击轮播词对应的搜索按钮 |
| `manual_enter` | 手动输入后按回车 |
| `manual_search_button` | 手动输入后点击搜索按钮 |
| `suggestion_select` | 点击输入联想 |
| `history_select` | 点击搜索历史 |
| `popular_term_select` | 点击热门搜索词 |

### 5.3 页面、模块与展示位稳定字典

动态商品、Collection、订单或售后对象ID不写入`page_id`、`module_id`或`placement_id`，通过对应业务字段携带。

复用现有`page`实体，但目标契约的`page.page_type`统一升级为：`home / listing / product / cart / checkout / auth / order / returns / account / content`。现有技术契约中的`plp / pdp / other`不再作为本期目标业务枚举；开发需按下表使用新的`page_type / page_id`组合更新机器契约，不自行建立第二套页面字段。

| 端别 | `page_type`／`page_id` | 稳定`module_id` |
|---|---|---|
| PC＋Mobile | `home/home` | `global_header`、`mobile_bottom_nav`、`home_banner`、`home_authentication`、`curated_collections`、`home_feed_tabs`、`home_product_feed`、`footer` |
| Mobile | `listing/shop` | `shop_navigation`、`search_panel` |
| PC＋Mobile | `listing/collection` | `collection_list_controls`、`collection_product_list` |
| PC＋Mobile | `listing/search_results` | `search_panel`、`search_suggestions`、`search_submit`、`search_list_controls`、`search_results_list`、`search_no_results_recommendations` |
| PC＋Mobile | `product/product_detail` | `product_header`、`product_gallery`、`product_information`、`product_actions`、`product_share`、`product_recommendations` |
| Mobile | `listing/favorites` | `saved_list_tabs`、`saved_product_list`、`saved_product_actions`、`saved_recommendations` |
| PC＋Mobile | `listing/wishlist`、`listing/recently_viewed` | `saved_list_tabs`、`saved_product_list`、`saved_product_actions` |
| PC＋Mobile | `cart/cart` | `cart_items`、`cart_selection`、`cart_item_actions`、`cart_checkout`、`cart_empty_state`、`cart_unavailable_items`、`cart_authentication` |
| PC＋Mobile | `checkout/checkout` | `checkout_contact`、`checkout_shipping`、`checkout_payment`、`checkout_coupon`、`checkout_submit` |
| PC＋Mobile | `checkout/order_confirmation` | `order_confirmation` |
| PC＋Mobile | `auth/login`、`auth/sign_up`、`auth/verification`、`auth/password_recovery`、`auth/set_password`、`auth/change_password`、`auth/blocked` | `auth_form`、`auth_recovery`、`auth_legal`、`auth_consent_modal`、`auth_blocked_state` |
| PC＋Mobile | `order/orders`、`order/order_detail` | `order_list`、`order_search`、`order_detail`、`order_refund_modal`、`order_support`、`delivery_tracking` |
| PC＋Mobile | `returns/returns`、`returns/return_detail` | `returns_list`、`returns_application`、`returns_information`、`returns_status` |
| PC＋Mobile | `account/account`、`account/profile`、`account/address_list`、`account/address_edit`、`account/privacy` | `account_orders`、`account_navigation`、`account_profile`、`account_addresses`、`account_preferences`、`account_privacy`、`account_authentication` |
| PC＋Mobile | `content/contact_us`、`content/about`、`content/authentication`、`content/privacy_policy`、`content/terms_of_service`、`content/accessibility_statement`、`content/your_privacy_choices` | `contact_form`、`contact_information`、`content_navigation`、`footer` |

`global_header`、`footer`和`mobile_bottom_nav`属于跨页面公共模块：分别在所有实际渲染PC Header、Footer或Mobile底部导航的页面上合法，不受`home/home`行限制。页面未渲染对应公共组件时不得补造该`module_id`。

PC不定义`listing/shop`或`listing/favorites`聚合页面；PC现有`listing/wishlist`和`listing/recently_viewed`纳入本期。代码中存在但没有当前用户入口的PC Shop组件不扩展本期产品范围。Delivery是订单页内物流详情模块，不定义独立`page_id`。

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
| PC＋Mobile Wishlist | `favorites_wishlist` |
| PC＋Mobile Recently Viewed | `favorites_recently_viewed` |
| Mobile Favorites推荐 | `favorites_recommendations` |
| Shopping Bag商品列表 | `shopping_bag_items` |

### 5.4 站外来源触点

1. 站外来源触点不新增独立业务事件，统一由符合条件的`page_view`承载。
2. 以下`page_view`记录一次站外来源触点：
   - 新Session的首个`page_view`；
   - 同一Session内，当前落地URL出现新的UTM、新的广告点击标识，或者当前页面由Looply站外referrer引导进入时。
3. 站外来源字段的生产方、取值来源和缺失处理，以《Looply 一方埋点新增公共字段清单 v1.4》为唯一依据；本节不重复定义单字段规则。
4. 触点时间直接使用承载该触点的`page_view.event_time`，不新增独立触点时间字段。
5. 普通站内路由、点击、收藏、加购等后续事件不重复携带这组站外触点字段。首次来源、Session来源和末次非Direct来源由分析层根据触点`page_view`、身份关系和Session顺序派生。
6. 广告点击标识只接收以下白名单参数：`gclid`、`gbraid`、`wbraid`、`fbclid`、`msclkid`、`ttclid`。Web页面公共层从本次落地URL读取，统一埋点SDK随符合条件的触点`page_view`发送。
7. `click_id`保存被选中参数的原始值；`click_id_type`保存对应参数名。两个字段必须成对出现，不得只发送其中一个，也不得使用`other`代替未知类型。
8. 同一落地URL同时出现多个白名单参数时，只保留一个，固定优先级为：`gclid > gbraid > wbraid > fbclid > msclkid > ttclid`。
9. 未出现白名单参数时省略`click_id`和`click_id_type`；未知广告点击参数不上传。字段缺失不阻止承载它们的`page_view`上报。

### 5.5 推荐与商品发现入口

当前识别以下入口：

- 首页Feed／For You；
- Collection商品列表；
- 商详You May Also Like；
- 热门搜索词进入结果页后的商品列表；
- 搜索无结果页推荐；
- Recently Viewed。

各入口使用5.3中的稳定`module_id`和`placement_id`。接口提供`placement.request_id`时映射为`recommendation_request_id`；接口未提供时曝光和点击仍正常上报，不伪造请求ID。

## 六、统一业务枚举

| 字段 | 允许值／规则 |
|---|---|
| `result_state` | `success`、`failed`、`cancelled` |
| `failure_type` | 首期仅`validation_failed`，只用于表单校验失败；其他失败不携带本字段 |
| `result_status` | `success`、`no_results`、`failed`、`cancelled` |
| `payment_type` | 直接沿用API：`credit_card`、`paypal`、`klarna`、`apple_pay` |
| `payment_info_source` | 本期仅`new` |
| `shipping_info_source` | `new`、`existing`、`modified` |
| `trigger_type` | 以5.2的六个值为准；筛选、排序和重置不写入本字段 |
| `click_id_type` | `gclid`、`gbraid`、`wbraid`、`fbclid`、`msclkid`、`ttclid`；多值选择顺序以5.4为准 |

## 七、服务端权威事实与Web边界

以下事实是一方分析所需数据，但不由Web埋点生成：

| 统一事实名 | 权威来源 | 唯一业务键 | 最小业务信息 |
|---|---|---|---|
| `order_created` | 订单系统／订单表 | `order_id` | `order_id`、创建时间、金额、币种、`items[]`（`order_item_id`、`listing_public_code`）；能够确定关联时增加`origin_session_id`，否则标记未关联且不得猜测 |
| `payment_started` | 支付系统／支付尝试表 | `payment_attempt_id` | `payment_attempt_id`、`order_id`、支付方式、开始时间 |
| `payment_failed` | 支付系统／支付结果表 | `payment_attempt_id` | `payment_attempt_id`、`order_id`、失败时间和低基数失败类型 |
| `purchase` | 支付成功与订单成交事实 | `order_id` | `order_id`、支付成功时间、成交金额、币种、`items[]`（每行至少含`order_item_id`、`listing_public_code`、该行成交金额）；整单金额不得替代商品行金额；同一订单只形成一次成交事实；能够确定关联时增加`origin_session_id`，否则标记未关联且不得猜测 |
| `refund` | 退款／售后权威表 | `refund_id` | `refund_id`、`order_id`、退款金额、币种、退款时间、`items[]`（每行至少含`order_item_id`、`listing_public_code`、该行退款金额）；整单退款金额不得替代商品行退款金额 |

服务端与数据平台需要另建接入任务，技术团队选择读取权威业务表或由业务系统在事实成立后推送。Web不得根据按钮点击、成功页、缓存或回调重复生成上述事实。

上线时必须按唯一业务键核对一方平台与权威业务表的订单数、成交金额、退款金额及订单商品行。

## 八、数据内容边界

普通分析事件不得携带：

- 邮箱、电话、姓名、详细地址；
- 密码、验证码、登录Token；
- 卡号、支付Token、支付网关原文；
- 优惠码原文；
- 退货凭证文件和自由文本；
- 未经搜索模块处理的搜索输入原文；
- 自由错误文本。

表单提交、订阅、联系邮箱、配送地址、优惠码和售后凭证等操作只记录动作类型、稳定业务对象及低基数结果，不上传用户填写的原文。

## 九、本期不实施的场景

- 购物车商品数量增加／减少；当前每件商品数量固定为1。
- 购物车优惠码入口。
- Cart Move to Wishlist；当前为Coming Soon。
- 已保存支付工具的复用或修改；本期`payment_info_source`仅取`new`。
- Account Privacy中的下载数据和删除账号操作；当前页面没有对应可用入口。
- Tablet和App页面交互。

上述能力真正上线时，再补充对应埋点，不为尚不存在的业务入口预埋事件。

## 十、技术实施边界

产品材料负责确定事件语义、成立条件、业务字段含义、业务枚举、敏感数据边界和防重复原则。技术团队可在不改变产品语义的前提下，在`tracking-plan.yaml`中确定：

- 字段技术类型、长度和空值表达；
- ID格式与生成方式；
- Schema／SDK版本；
- 新旧协议兼容方式；
- 网关、存储、重试和监控实现。

API已有枚举直接引用API。未形成稳定字段名和业务含义的开放对象不进入首期协议。
