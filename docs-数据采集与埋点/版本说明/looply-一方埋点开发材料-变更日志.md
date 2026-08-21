# Looply 一方埋点开发材料变更日志

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
