# Looply C1 Sell 数据采集与 GA4 需求

> 版本：v0.5  日期：2026-09-09  状态：开发评审稿
> 本文是 C1 埋点唯一开发阅读入口，整合一方平台与 GA4；v0.4 为上一版整合稿。本版按最终 Figma 文件《1.1-C1业务》可访问节点复核页面与控件。

## 一、范围与指标

一方平台完整采集 C1 前台 PC Web / Mobile Web 的页面、内容、点击、表单、校验、异常、预约和 Contact Us。首期回答：需求规模、预约漏斗、售卖方式、服务区域。来源、IP/地域、设备、Session、语言和 Market 属于平台通用维度，由统一采集体系提供，C1 不新增或重复定义；C1 业务事件只需与这些公共维度关联分析。后台操作、邮件、Download、Internal note、供给质量、处理效率和预约后有效供给转化不在本期。

## 二、一方平台公共规则

复用 C2 公共事件载荷、身份和 Session：`event_id`、`event_type`、`event_time`、`anonymous_id`、`domain_userid`、已登录 `user_id`、`session_id`、`page.page_type`、`page.page_id`、`page_instance_id`、`previous_page_type`、来源/UTM、设备、语言和 `market`。这些字段是平台通用维度，不属于 C1 新增字段；IP 仅按平台隐私规则用于地域/网络分析，不由 C1 事件传原始值。字段缺失时省略，不填空字符串或伪造 ID；C2→C1→C2 连续性必须用真实环境验证。C1 不新增第二套身份或 Session。PC 与 Mobile 共用同一事件名、参数和统计口径；仅在控件确实不同的情况下使用不同 `element_id`，不新增同义事件。

## 三、机器事件契约

以下为产品层最终字段契约；技术需按此生成 Schema，不得另造同义字段。

| event_type | 触发与不触发 | 事件唯一键 | 必带 C1 字段 |
|---|---|---|---|
| `page_view` | 页面实例真实到达；预加载不触发 | `event_id` | `page_id`、`page_instance_id` |
| `ui_interaction` | 用户完成一次稳定字典操作；焦点移动、逐字输入不触发 | `event_id` | `interaction_name`、`action`、`element_id` |
| `seller_flow_start` | 预约表单首次实际展示；重新渲染不触发 | `seller_flow_id` | `entry_source`、`flow_entry_event_id` |
| `seller_step_view` | Step 1–4 实际展示；后台重渲染不触发 | `event_id` | `seller_flow_id`、`flow_step`、`step_visit_seq` |
| `seller_content_view` | 内容前台可见连续 1 秒；同页面实例同内容只一次 | `page_instance_id+module_id+content_id` | `content_id`、`content_state` |
| `seller_view_result` | 内容加载或草稿保存/恢复出现明确终态 | `event_id` | `operation`、`result_state` |
| `seller_service_area_check` | ZIP 查询出现明确终态；Loading 不触发终态 | `coverage_check_id` | `query_context`、`result_state` |
| `seller_request_submit` | 一次提交尝试出现明确终态 | `submission_attempt_id` | `seller_flow_id`、`result_state` |
| `seller_request_created` | 后台预约权威记录创建成功 | `request_id` | `request_id`、`submission_attempt_id`、`session_link_status` |

## 四、页面与控件稳定字典

| page_id | module_id | element_id / interaction_name | 端 |
|---|---|---|---|
| `c1_sell_home` | `global_header` | `header_sell_click` | PC/Mobile |
| `c1_sell_home` | `hero` | `hero_sell_now_click`、`hero_explore_options_click` | PC/Mobile |
| `c1_sell_home` | `three_ways_to_sell` | `sell_method_card_view`、`sell_method_card_select`、`sell_method_card_expand` | PC/Mobile |
| `c1_sell_home` | `faq` | `faq_expand`、`faq_collapse` | PC/Mobile |
| `c1_accepted_brands` | `brand_filter` | `category_filter_select`、`initial_filter_select`、`brand_search_submit`、`brand_search_clear` | PC/Mobile |
| `c1_service_area` | `zip_checker` | `service_area_check_start`、`service_area_retry`、`service_area_alternative_click` | PC/Mobile |
| `c1_sell_flow` | `flow_step` | `step_continue`、`step_back`、`flow_close`、`submit_deduplicated` | PC/Mobile |
| `c1_sell_flow` | `form` | `category_select`、`configured_brand_select`、`custom_brand_add`、`piece_count_select`、`photo_upload_result`、`field_validation_result` | PC/Mobile |
| `contact_us` | `contact_form` | `business_type_select`、`contact_submit`、`contact_retry` | PC/Mobile |

不存在于最新 UI 的控件不进入覆盖率分母，不得自行扩展自由命名。

### 4.1 最终 UI 对照（Figma 文件：`1.1-C1业务`）

已核对的预约流程节点 `3:6738` 明确包含：PC 预约表单四步进度条、Step 1–4、Continue/Back、In-Home / Visit Looply / Ship To Us 分支、协议勾选、Preferred date、Referral code、ZIP 与地址字段、成功/错误状态。上述元素均已在详细点位中由 `seller_step_view`、`ui_interaction`、`seller_service_area_check`、`seller_request_submit` 覆盖。姓名、电话、邮箱、地址、备注及照片只记录填写状态/结果，不记录原文。

UI 对照不是事件新增依据：若最终实现未出现某控件，该控件点位从实现覆盖率分母剔除；若出现本表未列出的稳定业务操作，开发需在联调前补充 `element_id` 与验收用例后再上线。

## 五、枚举与状态

| 参数 | 允许值 |
|---|---|
| `flow_step` / `step_id` | `step_1`、`step_2`、`step_3`、`step_4` |
| `entry_source` | `hero`、`bottom_cta`、`sticky_cta`、`service_area`、`other_internal`、`direct`、`unknown` |
| `selling_method` | `IH`、`VL`、`ST` |
| `selection_origin` | `auto`、`user` |
| `query_context` | `standalone`、`flow_step3`、`flow_step4` |
| `result_state` | `success`、`failed`、`cancelled` |
| `coverage_status` | `covered`、`uncovered`（仅成功查询） |
| `content_state` | `ready`、`empty` |
| `c1_validation_code` | `required`、`format`、`length`、`unavailable`、`upload_limit`、`other` |
| `c1_failure_code` | `network_error`、`service_unavailable`、`upload_failed`、`timeout`、`content_load_failed`、`unknown` |
| `c1_block_reason` | `duplicate_submit`、`method_unavailable` |
| `piece_count_bucket` | `1_2`、`3_5`、`6_9`、`10_plus` |
| `operation` | `content_load`、`draft_save`、`draft_restore` |

## 六、关键状态与幂等样例

1. Service Area：发起即生成 `coverage_check_id`；发起、成功/失败/取消终态使用同一 ID；自动网络重试不新增 ID；用户 Retry 新建 ID；并发查询各自独立。
2. 提交：点击/Retry 为 `ui_interaction`；每次实际尝试新建 `submission_attempt_id`；重复点击只记 `duplicate_submit`，不新建 attempt 或预约。
3. 成功：`seller_request_submit=result_state=success` 只能在收到 `seller_request_created` 权威确认后成立；成功页加载、客户端暂态响应不触发成功；按 `request_id` 只保留一条权威预约。
4. Continue：只记录 `ui_interaction`，不携带业务 `result_state`；步骤变化由 `seller_step_view` 记录。
5. 内容：失败使用 `c1_failure_code=content_load_failed`；空结果为 `result_state=success + content_state=empty`；恢复为 `seller_view_result=success + recovery_flag=true`。

## 七、GA4 上报单元

### 7.1 上报范围

仅上报六类：Sell 页面到达、预约开始、Step 1–4 到达、售卖方式选择、Service Area 查询结果、预约成功。内容曝光、入口点击、Contact Us、字段校验、照片、草稿、邮件和后台操作只进一方平台。

### 7.2 dataLayer 映射

| 一方 event_type | GA4 event_name | 参数白名单 | 关键事件 |
|---|---|---|---:|
| `page_view`（Sell 页面） | `page_view` | `page_type`、`page_id`、`locale`、`market`、`device_type`、低基数 `entry_source` | 否 |
| `seller_flow_start` | `c1_sell_flow_start` | `entry_source`、`prefilled_zip_present`、`preselected_method`、`device_type`、`locale` | 否 |
| `seller_step_view` | `c1_sell_step_view` | `step_id`、`device_type`、`locale` | 否 |
| `seller_service_area_check` | `c1_service_area_check` | `query_context`、成功时 `coverage_status`、`in_home_available`、`default_method`、`retry_flag` | 否 |
| 用户主动售卖方式选择 | `c1_selling_method_select` | `selling_method`、`selection_origin=user`、`step_id`、`device_type` | 否 |
| 权威预约成功后的 `seller_request_submit` | `c1_sell_request_submit` | `selling_method`、`piece_count_bucket`、`category_count`、`brand_count`、`photo_count`、`coverage_status`、`preferred_date_present`、`referral_present`、`result_state=success` | 是 |

GA4 不接收 `request_id`、`seller_flow_id`、`submission_attempt_id`、身份标识、完整 ZIP、自由文本、照片和高基数品牌列表。自动 page_view 与主动 page_view 必须在容器配置中互斥。

## 八、开发验收用例

| 用例 | 通过标准 |
|---|---|
| C2→C1→C2 | 共享配置时身份/Session 连续；不共享时不伪造 ID |
| 四步漏斗 | 每次实际展示一条 `seller_step_view`；返回、刷新、草稿恢复不重复伪造 |
| Service Area | covered/uncovered/非法/网络失败分别可区分；Retry 和并发不重复 |
| 售卖方式 | 默认、主动选择、切换、不可用拦截可区分 |
| 提交成功 | 仅权威 `seller_request_created` 后产生 GA4 关键事件；刷新不重复 |
| 隐私 | GA4 DebugView 无姓名、联系方式、地址、完整 ZIP、照片、业务主键和自由文本 |
| 跨端 | PC/Mobile 事件名、参数和业务含义一致 |

## 九、开发评审前置确认

开发需要在评审会上确认：C2 公共 Schema 版本、C1 页面字典与 Figma 全量页面/状态的逐项对照（预约流程节点 `3:6738` 已核对）、GA4 容器自动 page_view 设置、dataLayer 实际字段路径、C2→C1→C2 运行验证环境，以及 PC/Mobile 控件差异是否仅通过 `element_id` 表达。以上为实施验证，不再改变本文业务口径。
