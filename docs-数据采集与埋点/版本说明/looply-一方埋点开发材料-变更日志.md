# Looply 一方埋点开发材料变更日志

## v1.5（2026-08-21，开发实施基线）

- 三份v1.5材料共同构成开发实施基线；旧全量PRD v1.7仅保留为历史来源，不再作为开发必须读取的第四份依赖。
- `anonymous_id`固定取身份模块已有的HttpOnly `looply_anonymous_id`；由服务端／BFF／采集网关或接收层读取并补入事件，Web JavaScript和SDK不读取Cookie，也不使用Snowplow DUID代填；`domain_userid`继续同时上传。
- 注册／登录`method`枚举扩展为`email / google / apple / facebook`，明确只记录本次实际成功方式及缺失处理，不在产品材料指定跨页面保存技术。
- 订单确认页PC＋Mobile的Continue Shopping统一目标为`home/home`。
- 商详推荐区导航统一为`recommendation_rail`：PC记录左右按钮，Mobile在实际发生列表位移后将左滑／右滑记录为`next / previous`；商品曝光规则保持不变。
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
- 补全服务端五类权威事实和商品行级金额规则。
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
- 新增工作簿“结果字段映射”Sheet，逐项冻结`interaction_name + action`是否携带`result_state/failure_type`、专属成功事件替代规则及Pay Now服务端事实边界。
- 最终收敛唯一权威位置：结果映射Sheet只维护逐动作适用关系，枚举与未列动作默认规则引用公共实施规则；`landing_page_clean`生产方、取值与缺失处理只在新增公共字段清单维护。
- 保留 v1.0 文件不变，新建 v1.1 工作稿。

正式预评审及最终冻结复检已完成；P0、P1、P2、P3均为0，准确性、冲突、重复和冗余检查全部通过。v1.1现冻结为开发实施基线；运行态代码、Schema、SDK、网关、数据仓和真实事件样本仍需在开发与测试阶段另行验收。
