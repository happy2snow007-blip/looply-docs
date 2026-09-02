# Looply 一方埋点开发材料变更日志

## 2026-08-28｜v1.8 售后多商品与无生产入口点位收口

- 开发实施基线更新为《Looply-v1.4-详细埋点需求定稿-v1.3》《Looply-v1.4-公共基础字段需求定稿-v1.1》和《Looply一方埋点公共实施规则v1.8》；公共字段表没有新增字段。
- 12个当前没有真实生产控件或可达入口的点位转入“停止项”，Active点位由250调整为238，客户端Active点位由245调整为233；5个权威业务表事实不变。
- `pt-0018/0037/0038/0128/0157/0159/0170/0171/0189/0190/0201/0239`标记为当前版本不适用，从埋点覆盖率分母中排除；原点位ID保留且不得复用。
- `pt-0192`统一覆盖d3页面内复制和d4物流弹窗复制，使用`target_id=shipment_id`及`copy_source=d3_inline/d4_modal`；d3数据链路需提供真实`shipment_id`，不得用物流单号代替。
- `pt-0196/0197/0199/0200/0202`按同一订单内多商品退货收口：一次操作只发送一条事件，`target_id=order_id`，`order_item_ids`传本次涉及的订单商品行数组；单商品也传单元素数组，不按商品行拆分发送。
- `pt-0202`继续保留成功、请求失败和校验失败的`result_state/failure_type`口径。
- 新增《Looply 一方埋点三份开发基线 2026-08-28 版本差异 v1.0》，供开发对照机器契约、接收存储和测试用例完成修改。
- 本轮只调整一方埋点，不修改GA4文档、GA4事件或GA4报表口径。
- 保留v1.7公共规则和详细点位v1.2为历史版本，新建v1.8公共规则及详细点位v1.3。

## 2026-08-26｜v1.7 动态筛选上下文

- 开发实施基线更新为《Looply-v1.4-详细埋点需求定稿-v1.2》《Looply-v1.4-公共基础字段需求定稿-v1.1》和《Looply一方埋点公共实施规则v1.7》；公共字段表没有新增字段。
- Search与Collection统一使用后台稳定`dimension_code`和`option_code`形成最终已Apply筛选事实，前端不维护固定筛选维度白名单。
- 一方`filter_ids[]`每项使用`dimension_code:option_code`；筛选组交互使用`dimension_code`，筛选项交互使用对应Code对。
- Search／Collection的Apply携带最终`filter_ids[]`；选择后取消、关闭或未Apply的值不进入，Reset后集合为空。
- Collection商品曝光与点击增加最终`filter_ids[] / sort_type`上下文。
- 后台／数据平台负责维护Code到展示名称的可追溯映射；事件不上传展示名称代替ID。
- 保留v1.6公共规则和详细点位v1.1为历史版本，新建v1.7公共规则及详细点位v1.2。公共基础字段仍为v1.1，公共字段总表无变化，仅更新交易事实的权威文档引用和兼容边界。
- 新增《Looply 一方埋点三份开发基线 2026-08-26 版本差异 v1.0》，基于今日以前实际文件与当前文件生成，供开发先行阅读。

## 2026-08-26｜订单归因关联与交易事实唯一权威位置收口

- `origin_session_id`由“可确定时携带”改为正常Web Checkout下单必传必存；Web／埋点SDK传入当时Snowplow `session_id`，订单服务随订单或归因上下文保存，支付和成交数据按`order_id`沿用。仅明确不经过Web Checkout且能由订单来源识别的例外允许为空。
- 订单、支付、成交、退款、订单商品行和售后过程的完整定义统一迁入《Looply 订单与交易数据接入需求 v1.0》；一方埋点公共规则及两份执行表只保留Web边界、事实名与精确引用，不再平行维护字段定义。

## 2026-08-22｜v1.6 冻结前口径修正

- 详细埋点工作簿明确区分17个客户端`event_type`与5个权威业务表事实名；仅客户端行由Web／SDK上报，权威业务表事实由数据平台读取业务表形成。
- 公共实施规则删除对事件工作簿中已不存在“公共字段”Sheet的引用。

## v1.6（2026-08-22，开发实施基线工作稿）

- 新增《Looply 一方埋点最终执行问题与结论 v1.0》，用于记录本轮Review问题和产品答复；确定性结论同步回三份实施基线后，该文档不作为开发实施规则或阶段状态依据。
- 登录结果只发送一条`login`、注册结果只发送一条`sign_up`，并用`result_state=success/failed`区分；如请求已发起后形成取消终态，可使用`cancelled`，不额外发送`ui_interaction`。
- 明确`order_created / payment_started / payment_failed / purchase / refund`均不由Web／SDK或业务服务新增埋点事件；由数据平台读取订单、支付、退款权威业务表形成一方分析事实。
- 明确`payment_failed`不进入Web／SDK YAML Schema，也不使用客户端公共`failure_type`；失败原因字段名、业务表来源、封闭枚举、映射和DataWorks质量规则在独立数据平台接入任务中定义，不阻塞前端埋点实施。
- 明确一方真实`purchase`只取订单／支付权威成交事实；Flink历史`checkout_start→purchase`代理可继续服务存量下游，但不得进入一方成交事实表或成交指标，落地和统计必须隔离。
- 搜索结果商品曝光／点击统一使用`module_id=search_results_list`；`view_search_results`作为结果请求终态，能明确属于结果列表时使用该模块，否则省略`module_id`，不得新增`search_results_data`。
- 明确`/favorites`聚合页及其推荐、Tab和列表点位仅适用于Mobile／H5；PC只覆盖真实存在的Wishlist和Recently Viewed页面，不为PC补不存在的Favorites聚合页点位。
- 开发确认Web／SDK及一方平台均直接沿用`item_impression`、`item_click`、`checkout_start`，三者不改名、不做平台前映射，也不双发`view_item_list`、`select_item`、`begin_checkout`。
- 将商品曝光、商品点击、Checkout开始及其`exposure_id`、`source_event_id`关联规则统一改为上述最终事件名。
- 开发实施基线改为《Looply-v1.4-详细埋点需求定稿-v1.1》《Looply-v1.4-公共基础字段需求定稿-v1.1》和《Looply一方埋点公共实施规则v1.6》三份材料；不再依赖“9条补充结论”或历史PRD。
- 订单确认页Continue Shopping的稳定目标统一为`home`，到达首页后由`home/home`的`page_view`记录页面访问。
- 认证`method`只约束`login/sign_up`携带本次实际认证方式；跨OAuth跳转如何取得该值由技术方案确定，产品材料不再指定暂存、回调读取或清理步骤。
- 删除Flink、DWD和DataWorks“零改动／零DDL”的产品承诺；是否改动、字段如何落地及下游如何读取由技术负责人验证确定，产品只冻结语义、可用性、防重复和历史代理隔离边界。
- 修正公共规则对已不存在“结果字段映射”Sheet的引用；`result_state`和`failure_type`改为直接以详细执行表“详细点位”Sheet对应行的成立时机和专属参数为唯一依据。
- 统一`failure_type`适用范围：首期仅为`validation_failed`，可用于详细执行表明确要求记录校验失败的客户端结果事件，包括适用的`ui_interaction`、`login`和`sign_up`；不适用于数据平台从权威业务表形成的`payment_failed`。
- 删除详细执行表K列和公共字段表L列逐行重复的技术方案占位；表头统一说明具体实现由技术负责人验证，避免产品材料重复维护技术方案。
- 删除事件处理矩阵G／H列逐事件重复的技术验证文案，仅在表头统一保留技术验证与数据可用性边界，不改变任何事件语义或责任端。
- 保留v1.5公共实施规则和两份v1.0最终执行表不变，新建v1.6规则及两份v1.1执行表。

## v1.5（2026-08-21，开发实施基线）

- 三份v1.5材料共同构成开发实施基线；旧全量PRD v1.7仅保留为历史来源，不再作为开发必须读取的第四份依赖。
- `anonymous_id`固定取身份模块已有的HttpOnly `looply_anonymous_id`；由服务端／BFF／采集网关或接收层读取并补入事件，Web JavaScript和SDK不读取Cookie，也不使用Snowplow DUID代填；`domain_userid`继续同时上传。
- 注册／登录`method`枚举扩展为`email / google / apple / facebook`，明确只记录本次实际成功方式及缺失处理，不在产品材料指定跨页面保存技术。
- 订单确认页PC＋Mobile的Continue Shopping统一目标为`home/home`。
- 商详推荐区导航：PC的`previous/next`分别使用`element_id=recommendation_previous/recommendation_next`；Mobile／H5仅在列表实际移动时记录，左滑且列表向后为`action=next`、右滑且列表向前为`action=previous`，统一使用`element_id=recommendation_rail`、`target_id=placement_id`；回弹或未移动不发送。商品曝光规则保持不变。
- 推荐请求ID只使用现有`placement.request_id`，不新增顶层`recommendation_request_id`；分析层需要时映射展开。
- 按真实代码调用名修正四个Share存量物理事件；`short_code`明确为`share_complete`参数而非独立事件，Web不双发新旧事件。
- 恢复并冻结既有`share_channel`稳定枚举：`whatsapp / message / facebook / pinterest / x / messenger`；未知渠道省略，`copy_link`不写该字段。
- `market`改为读取当前市场接口／上下文返回的稳定Market Code，支持多市场且不硬编码US；缺失时省略且事件继续发送。
- 同一搜索结果页仅修改筛选、价格区间、排序或重置条件时，沿用当前`page_instance_id`，不新增`page_view`；结果请求完成后形成新的`view_search_results`。
- 将PC按钮和Mobile手势分别改写为可直接解析的`interaction_name：action → element_id → target_id`映射；删除事件行与公共规则之间的重复完整定义，保留唯一权威引用。
- 修复事件工作簿“公共字段”索引Sheet的不可见格式，不改变字段或事件规则。
- 正式评审及最终冻结复检已通过：P0、P1、P2、P3均为0，准确性、冲突、重复和冗余检查全部通过；三份v1.5材料冻结为开发实施基线。
- 保留v1.4三份材料不变，新建v1.5开发实施基线。

## v1.4（2026-08-21，开发实施基线）

- 明确`anonymous_id`由身份模块通过可读取身份上下文提供，且不得与Snowplow `domain_userid`相同；不得读取HttpOnly能力Cookie或直接复用返回DUID的旧Helper。
- `session_id`改为直接复用现有Snowplow `domain_sessionid`，接受Snowplow客户端事件续期及30分钟超时口径，不再建设第二套一方Session ID；一方报表仅统计至少包含一个一方有效事件的sid，并补充多标签页、跨设备和`origin_session_id`关联边界。
- 保留逐商品`view_item_list`语义，新增`exposure_id`生成与`select_item`继承规则。
- 搜索事件适配现有URL结构：`keyword → query`、离散筛选及价格区间统一进入`filter_ids[]`、`sort → sort_type`；补齐筛选去重、稳定排序，以及完整／单边价格区间的稳定编码。
- PC订单确认页纳入范围；`global_header / footer / mobile_bottom_nav`明确为实际渲染页面均可使用的全局模块。
- 删除当前不存在或无独立分析增量的`zoom_in / zoom_out / auto_query / scroll`操作，补齐`cancelled`适用边界。
- PC Shop仍不纳入当前产品范围；代码中无用户入口的桌面组件不反向扩展埋点范围。
- 保留v1.3文件不变，新建v1.4开发实施基线。

## v1.3（2026-08-21，开发实施基线）

- 新增`click_id_type`，与`click_id`成对记录广告点击标识的类型和值。
- 固定广告点击标识白名单：`gclid / gbraid / wbraid / fbclid / msclkid / ttclid`；不接收未知参数，不使用`other`。
- 同一落地URL同时出现多个白名单参数时，只保留一个，优先级为`gclid > gbraid > wbraid > fbclid > msclkid > ttclid`。
- 无白名单参数时省略`click_id`和`click_id_type`，字段缺失不阻止触点`page_view`上报。
- 新增公共字段由20个调整为21个；其余事件、字段、触发和平台规则不变。
- 保留v1.2文件不变，新建v1.3开发实施基线。

## v1.2（2026-08-21，开发实施基线）

- 删除首期`canonical_person_id`字段及携带规则，不使用`user_id`重复填充该字段。
- 身份串联继续使用身份模块生成的`anonymous_id`与登录后`user_id`；`domain_userid`仍作为Snowplow浏览器辅助标识同时上传。
- 新增公共字段由21个调整为20个；其余事件、字段、触发和平台规则不变。
- 保留v1.1文件不变，新建v1.2开发实施基线。

## v1.1（2026-08-20，开发评审工作稿）

基线：

- 《Looply 一方埋点新增与修改清单 v1.0》
- 《Looply 一方埋点新增公共字段清单 v1.0》
- 《Looply 一方埋点公共实施规则 v1.0》

本次变更：

- 将三份材料的职责调整为事件表、公共字段表、公共规则三个唯一权威位置，删除重复维护。
- 补入完整页面、模块、展示位字典以及搜索结构化字段。
- 补全五类权威业务表事实和商品行级金额规则。
- 补全分享事件迁移、收藏页面范围、合法页面示例和通用失败结果边界。
- 明确参数缺失不抑制已经成立的业务事件，且不得伪造默认值。
- 删除新增公共字段`identity_state`；登录态统一根据事件发生时是否携带`user_id`判断。
- 保留并冻结`source_type`首期枚举：`direct / search / recommendation / collection / wishlist / cart / buy_now / other_internal`。
- 补齐`source_type`八个值与搜索、推荐、Collection、Wishlist、Shopping Bag、Buy Now、直达和其他站内入口的唯一映射；公共字段表只引用该权威映射，不再重复维护枚举。
- 补齐`source_event_id`封闭链路：`select_item → view_item → 商详收藏／加购／Buy Now`；Shopping Bag结算不引用单一商品事件，且禁止跨商品或按最近事件误关联。
- 修正`source_module_id`示例为合法`module_id=search_results_list`；通用Retry沿用原失败操作的合法`module_id`，无法识别时省略。
- 收口`failure_type`首期协议：仅表单校验失败使用`validation_failed`，其他失败只记录`result_state=failed`，不建立开放失败分类。
- 增加非站外触点公共字段与现有字段的逐项语义边界，明确复用、并存和不得互相替代的关系。
- 将`ui_interaction`通用字段及防重复规则集中到公共实施规则3.4；事件表页面操作行只保留稳定动作映射、额外字段和例外。
- 将`result_state`、`failure_type`等枚举收敛到公共实施规则唯一位置，公共字段表和事件表改为引用。
- 将事件表中的“商品快照、发生页面、来源、移除前后状态、价格／币种”等概念占位替换为可实施字段：复用现有`product / page / cart / placement`实体以及`method / query / quantity`字段；只有现有契约不存在的来源关联等信息才使用新增字段。
- 明确结果页URL的`search_term`在一方事件中映射为现有`query`，下游继续使用既有`search_query`；不新增平行搜索词字段。
- 明确复用现有`page`实体，同时将目标`page.page_type`枚举升级为`home / listing / product / cart / checkout / auth / order / returns / account / content`；不继续以旧`plp / pdp / other`作为本期目标值。
- 收口站外来源触点：仅由新Session首个`page_view`或新站外来源触点的`page_view`承载；后续事件不重复携带。
- 保留`landing_page_clean`，固定取落地URL的`pathname`；原始UTM、`referrer_url`和`click_id`按实际可取值携带。
- 删除新增字段`touchpoint_at`，触点时间直接复用承载触点的`page_view.event_time`。
- 收敛重复定义：站外来源字段的取值、来源和缺失处理只在《新增公共字段清单》中维护；公共规则仅保留触点成立、承载和不继承规则。
- 收敛事件表通用时机与`payment_type`枚举的重复维护，不改变任何事件触发或字段口径。
- 明确`landing_page_clean`由Web页面公共层读取`location.pathname`生成，统一埋点SDK负责随触点`page_view`发送；字段缺失不阻止事件上报。
- 新增工作簿“结果字段映射”Sheet，逐项冻结`interaction_name + action`是否携带`result_state/failure_type`、专属成功事件替代规则及Pay Now与权威业务表事实边界。
- 最终收敛唯一权威位置：结果映射Sheet只维护逐动作适用关系，枚举与未列动作默认规则引用公共实施规则；`landing_page_clean`生产方、取值与缺失处理只在新增公共字段清单维护。
- 保留 v1.0 文件不变，新建 v1.1 工作稿。

正式预评审及最终冻结复检已完成；P0、P1、P2、P3均为0，准确性、冲突、重复和冗余检查全部通过。v1.1现冻结为开发实施基线；运行态代码、Schema、SDK、网关、数据仓和真实事件样本仍需在开发与测试阶段另行验收。
