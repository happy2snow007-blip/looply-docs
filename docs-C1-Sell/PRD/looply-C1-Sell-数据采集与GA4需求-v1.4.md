# Looply C1 Sell 数据采集与 GA4 需求

> 版本：v1.4  日期：2026-09-11  状态：待开发评审
> 本文定义 C1 一方与 GA4 的业务采集口径；配套《埋点开发清单 v1.2》和《C2 公共埋点规范引用入口 v1.1》。技术接入与平台配置由技术团队确定。

## 一、范围与指标

一方平台采集 C1 前台 PC Web / Mobile Web 的页面到达、首页各屏有效曝光、业务/导航/转化相关点击、表单、校验、异常、预约和 Contact Us。首期回答：需求规模、预约漏斗、售卖方式、服务区域。除 Sell 首页外，其他页面不做逐屏曝光，仅记录页面到达和纳入字典的业务交互。来源、IP/地域、设备、Session、语言和 Market 属于平台通用维度，由统一采集体系提供，C1 不新增或重复定义；C1 业务事件只需与这些公共维度关联分析。后台人工操作、邮件、Download、Internal note、供给质量、处理效率和预约后有效供给转化不在本期；后台预约记录创建仅作为独立业务事实统计。

## 二、一方平台公共规则

复用 C2 公共事件载荷、身份和 Session：`event_id`、`event_type`、`event_time`、`anonymous_id`、`domain_userid`、已登录 `user_id`、`session_id`、`page.page_type`、`page.page_id`、`page_instance_id`、`previous_page_type`、来源/UTM、设备、语言和 `market`。这些字段是平台通用维度，不属于 C1 新增字段；IP 仅按平台隐私规则用于地域/网络分析，不由 C1 事件传原始值。字段缺失时省略，不填空字符串或伪造 ID；C2→C1→C2 连续性必须用真实环境验证。C1 不新增第二套身份或 Session。PC 与 Mobile 共用同一事件名、参数和统计口径；仅在控件确实不同的情况下使用不同 `element_id`，不新增同义事件。

## 三、机器事件契约

公共字段按《C1 Sell：C2 公共埋点规范引用入口 v1.1》定位原始规范及待确认冲突，不将两份冲突原文拼接为新基线。C1 只复用公共采集层，不修改身份或 Session 生命周期。开发同时读取本 PRD v1.4 和 Excel 点位清单 v1.2；Excel“交互字典”维护每个 point_id + variant_id 的完整操作组合，本文第四章是同源生成的定位索引。point_id、variant_id 是文档定位键，不要求新增上报公共字段。

以下为产品层事件定义；具体传输结构与 C2 公共机器契约对齐。本文和 Excel 中 page_id 是 page.page_id 的简写，不新增顶层同义字段。

| event_type | 触发与不触发 | 事件唯一键 | 必带 C1 字段 |
|---|---|---|---|
| `page_view` | 页面实例真实到达；预加载不触发 | `event_id` | `page_id`、`page_instance_id` |
| `ui_interaction` | 按逐点字典记录操作、操作结果；默认推荐仅 C1-METHOD-02 允许系统触发，并标记 auto；纯焦点移动、逐字输入不触发 | `event_id` | `interaction_name`、`action`、`element_id`、`page.page_id`、`module_id` |
| `seller_flow_start` | 预约表单首次实际展示；重新渲染不触发 | `seller_flow_id` | `entry_source`、`flow_entry_event_id` |
| `seller_step_view` | Step 1–4 实际展示；后台重渲染不触发 | `event_id` | `seller_flow_id`、`flow_step`、`step_visit_seq` |
| `seller_content_view` | 内容前台可见连续 1 秒；同页面实例同内容只一次 | `page_instance_id+module_id+content_id` | `content_id`、`content_state` |
| `seller_view_result` | 内容加载或草稿保存/恢复出现明确终态 | `event_id` | `operation`、`result_state` |
| `seller_service_area_check` | ZIP 查询出现明确终态；Loading 不触发终态 | `coverage_check_id` | `query_context`、`result_state` |
| `seller_request_submit` | 一次提交请求收到明确接口终态 | `event_id` | `seller_flow_id`、`result_state` |
| `seller_request_created` | 后台预约记录创建成功的独立事实 | `request_id` | `request_id` |

## 四、页面与控件稳定字典

| point_id / variant_id | interaction_name | action | element_id | page_id 规则 | module_id | 端 |
|---|---|---|---|---|---|---|
| C1-NAV-02/default | header_sell_click | click | global_header.sell | current_page | global_header | PC/Mobile |
| C1-NAV-03/default | footer_link_click | click | footer.link | current_page | footer | PC/Mobile |
| C1-NAV-04/default | mobile_tab_sell_click | click | mobile_tab.sell | current_page | mobile_bottom_nav | Mobile |
| C1-HOME-02/default | hero_sell_now_click | click | hero.sell_now | c1_sell_home | hero | PC/Mobile |
| C1-HOME-03/default | hero_explore_options_click | click | hero.explore_options | c1_sell_home | hero | PC/Mobile |
| C1-HOME-05/default | sell_method_card_select | select | three_ways_to_sell.method_card | c1_sell_home | three_ways_to_sell | PC/Mobile |
| C1-HOME-06/default | sell_method_card_expand | expand | three_ways_to_sell.method_card | c1_sell_home | three_ways_to_sell | PC/Mobile |
| C1-HOME-07/default | sell_method_card_collapse | collapse | three_ways_to_sell.method_card | c1_sell_home | three_ways_to_sell | PC/Mobile |
| C1-HOME-08/default | faq_expand | expand | faq.item | c1_sell_home | faq | PC/Mobile |
| C1-HOME-09/default | faq_collapse | collapse | faq.item | c1_sell_home | faq | PC/Mobile |
| C1-HOME-10/default | content_link_click | click | content.link | c1_sell_home | content_navigation | PC/Mobile |
| C1-FLOW-06/default | step_continue | click | sell_flow.continue | c1_sell_flow | flow_step | PC/Mobile |
| C1-FLOW-07/default | step_back | click | sell_flow.back | c1_sell_flow | flow_step | PC/Mobile |
| C1-FLOW-08/default | flow_close | close | sell_flow.close | c1_sell_flow | flow_step | PC/Mobile |
| C1-FORM-01/default | field_fill_state | change | sell_flow.field | c1_sell_flow | form | PC/Mobile |
| C1-FORM-02/default | field_fill_state | change | sell_flow.field | c1_sell_flow | form | PC/Mobile |
| C1-FORM-03/default | contact_consent_change | select | sell_flow.contact_consent | c1_sell_flow | form | PC/Mobile |
| C1-FORM-04/default | field_validation_result | validate | sell_flow.field | c1_sell_flow | form | PC/Mobile |
| C1-FORM-05/default | category_select | select | sell_flow.category | c1_sell_flow | form | PC/Mobile |
| C1-FORM-06/default | configured_brand_select | select | sell_flow.configured_brand | c1_sell_flow | form | PC/Mobile |
| C1-FORM-07/suggestion | brand_suggest_select | select | sell_flow.brand_suggestion | c1_sell_flow | form | PC/Mobile |
| C1-FORM-07/manual | custom_brand_add | add | sell_flow.custom_brand | c1_sell_flow | form | PC/Mobile |
| C1-FORM-08/default | piece_count_select | select | sell_flow.piece_count | c1_sell_flow | form | PC/Mobile |
| C1-FORM-09/default | photo_select | select | sell_flow.photos | c1_sell_flow | form | PC/Mobile |
| C1-FORM-10/default | photo_upload_result | upload_result | sell_flow.photos | c1_sell_flow | form | PC/Mobile |
| C1-AREA-01/standalone | service_area_check_start | submit | service_area.zip_checker | c1_service_area | zip_checker | PC/Mobile |
| C1-AREA-01/step3 | service_area_check_start | submit | service_area.zip_checker | c1_sell_flow | form | PC/Mobile |
| C1-AREA-01/step4 | service_area_check_start | submit | service_area.zip_checker | c1_sell_flow | form | PC/Mobile |
| C1-AREA-06/standalone | service_area_retry | retry | service_area.retry | c1_service_area | zip_checker | PC/Mobile |
| C1-AREA-06/step3 | service_area_retry | retry | service_area.retry | c1_sell_flow | form | PC/Mobile |
| C1-AREA-06/step4 | service_area_retry | retry | service_area.retry | c1_sell_flow | form | PC/Mobile |
| C1-AREA-07/default | service_area_alternative_click | click | service_area.alternative_method | c1_service_area | zip_checker | PC/Mobile |
| C1-METHOD-02/default | method_default_select | select | sell_flow.selling_method | c1_sell_flow | form | PC/Mobile |
| C1-METHOD-03/default | selling_method_select | select | sell_flow.selling_method | c1_sell_flow | form | PC/Mobile |
| C1-METHOD-04/default | selling_method_blocked | blocked | sell_flow.selling_method | c1_sell_flow | form | PC/Mobile |
| C1-SUBMIT-03/default | submit_deduplicated | blocked | sell_flow.submit | c1_sell_flow | flow_step | PC/Mobile |
| C1-CONTACT-02/default | business_type_select | select | contact_us.business_type | contact_us | contact_form | PC/Mobile |
| C1-CONTACT-03/fill | field_fill_state | change | contact_us.field | contact_us | contact_form | PC/Mobile |
| C1-CONTACT-03/validation | field_validation_result | validate | contact_us.field | contact_us | contact_form | PC/Mobile |
| C1-CONTACT-04/default | contact_submit | submit | contact_us.form | contact_us | contact_form | PC/Mobile |
| C1-CONTACT-05/default | contact_retry | retry | contact_us.retry | contact_us | contact_form | PC/Mobile |
| C1-BRAND-01/default | category_filter_select | select | accepted_brands.category_filter | c1_accepted_brands | brand_filter | PC/Mobile |
| C1-BRAND-02/default | initial_filter_select | select | accepted_brands.initial_filter | c1_accepted_brands | brand_filter | PC/Mobile |
| C1-BRAND-03/default | brand_search_submit | submit | accepted_brands.search | c1_accepted_brands | brand_filter | PC/Mobile |
| C1-BRAND-04/default | brand_search_clear | click | accepted_brands.search_clear | c1_accepted_brands | brand_filter | PC/Mobile |

逐点触发条件、业务字段、不触发边界和平台去向由 Excel 的“详细点位”维护；交互字典中的组合逐行匹配。不得仅按 interaction_name 匹配或将不同组合的 action、element_id、页面、模块自由拼接。

`current_page` 是文档规则，不是上报枚举：Header、Footer 和 Mobile Tab 记录点击发生页面的真实 page.page_id，不将目标 Sell 首页冒充来源页面。其他行记录表中固定页面；各端仅在实际渲染对应控件时触发。原有点位 ID 保留；同点位多场景通过 variant_id 拆行，每次操作只匹配一个场景。未取得最新 UI 证据的页面不因字典补齐而视为覆盖验收通过。

### 4.1 最终 UI 对照（Figma 文件：`1.1-C1业务`）

全量 C1 UI 的产品事实源为 [Figma《1.1-C1业务》](https://www.figma.com/design/XIl3SfaIL8y2xy6yJnrrJE/1.1-C1%E4%B8%9A%E5%8A%A1?node-id=0-1&p=f&m=dev)；预约流程对应节点为 [`3:6738`](https://www.figma.com/design/XIl3SfaIL8y2xy6yJnrrJE/1.1-C1%E4%B8%9A%E5%8A%A1?node-id=3-6738&m=dev)。最终实现按该文件中实际呈现的页面、控件和状态对照本需求与 Excel，不以其他模块或旧 Demo 代替。

已核对的预约流程节点 `3:6738` 明确包含：PC 预约表单四步进度条、Step 1–4、Continue/Back、In-Home / Visit Looply / Ship To Us 分支、协议勾选、Preferred date、Referral code、ZIP 与地址字段、成功/错误状态。这些元素的已有需求按 `seller_step_view`、`ui_interaction`、`seller_service_area_check`、`seller_request_submit` 分类；姓名、电话、邮箱、地址、备注及照片只记录填写状态/结果，不记录原文。

UI 对照不是事件新增依据：若最终实现未出现某控件，该控件点位从实现覆盖率分母剔除；若出现本表未列出的稳定业务操作，开发需在联调前补充 `element_id` 与验收用例后再上线。

### 4.2 曝光与点击范围

- 仅 `c1_sell_home` 记录首页各屏 `seller_content_view` 有效曝光；有效曝光为屏幕进入视口并连续可见达到约定阈值，预加载、快速划过和后台不可见不触发。
- `c1_accepted_brands`、`c1_service_area`、`c1_sell_flow`、`contact_us` 等其他页面记录 `page_view` 和字典内业务交互，不发送通用逐屏曝光；预约流程 Step 到达仍按业务漏斗记录 `seller_step_view`，不等同于通用屏幕曝光。
- 可点击元素不做无差别全量采集，仅追踪会改变页面/流程、影响转化或回答业务问题的 CTA、导航、卡片、筛选、展开/收起、Retry、提交和替代方式入口。装饰性点击、无业务结果的容器点击、焦点移动和逐字输入不采集。

## 五、枚举与状态

| 参数 | 允许值 | 使用规则 |
|---|---|---|
| result_state | success / failed / cancelled | blocked使用c1_block_reason，不扩展公共结果 |
| selling_method | IH / VL / ST | 默认自动选择与用户主动选择分开 |
| query_context | standalone / flow_step3 / flow_step4 | Service Area查询上下文 |
| coverage_status | covered / uncovered（仅成功查询） | 失败不计为未覆盖 |
| c1_validation_code | required / format / length / unavailable / upload_limit / other | 表单校验失败 |
| c1_failure_code | network_error / service_unavailable / upload_failed / timeout / content_load_failed / unknown | 请求或内容失败 |
| business_type | sell / buy | Contact Us业务类型 |
| filter_type | all / category / initial | Accepted Brands筛选类型 |
| position | 正整数，从1开始 | 内容/卡片位置 |
| flow_step | step_1 / step_2 / step_3 / step_4 | 一方字段；GA4 step_id 由 flow_step 映射，不是第二个一方字段 |
| entry_source | hero / bottom_cta / sticky_cta / service_area / other_internal / direct / unknown | 按真实预约入口；不可识别用 unknown |
| selection_origin | auto / user | 配置品牌选择是 user；configured 不是此字段允许值 |
| brand_input_type | configured / suggestion / manual | 仅品牌选择使用，区分配置品牌/联想/手动；C1业务参数 |
| content_state | ready / empty | 内容可用/成功返回空内容 |
| c1_block_reason | duplicate_submit / method_unavailable | 重复提交/方式不可用拦截 |
| piece_count_bucket | 1_2 / 3_5 / 6_9 / 10_plus | 沿用 PRD 当前区间，最终 UI 取值尚需复核 |
| operation | content_load / draft_save / draft_restore | 内容加载/草稿保存/恢复终态 |
| action | click / select / expand / collapse / close / change / validate / add / upload_result / submit / retry / blocked | 只允许交互字典对应行的值，不跨行自由组合 |
| 布尔业务参数 | true / false | field_present、selected、retry_flag、recovery_flag、brand_input_present；无来源不猜测 |

配置品牌、联想与手动品牌都属于用户操作，selection_origin=user；具体输入方式由 C1 业务参数 brand_input_type 区分，不扩展公共字段。step_id 仅用于 GA4，一方统一用 flow_step。interaction_name、element_id、module_id 和 variant_id 的允许组合以第四章及同源 Excel 字典为准。

## 六、关键状态与幂等样例

1. Service Area：发起即生成 `coverage_check_id`；发起操作 ui_interaction 与 seller_service_area_check 成功/失败/取消终态使用同一 ID；自动网络重试不新增 ID；用户 Retry 新建 ID；并发查询各自独立。
2. 提交：`seller_request_submit` 只记录接口返回的明确终态；重复点击只记录 `submit_deduplicated` / `c1_block_reason=duplicate_submit`，不重复发起提交。
3. 后台预约创建：`seller_request_created` 是独立后台事实，按唯一 `request_id` 去重；本期不要求与前台提交事件建立关联。前台提交成功率与后台预约创建量分别统计。
4. Continue：只记录 `ui_interaction`，不携带业务 `result_state`；步骤变化由 `seller_step_view` 记录。
5. 首页方式卡片曝光统一使用 C1-HOME-04；C1-METHOD-01 仅是该场景说明，不重复发送。预约页方式展示依预约步骤业务事件分析，不新增通用屏幕曝光。
6. 内容：失败使用 `c1_failure_code=content_load_failed`；空结果为 `result_state=success + content_state=empty`；恢复为 `seller_view_result=success + recovery_flag=true`。

## 七、GA4 上报单元

### 7.1 上报范围

仅上报六类：Sell 页面到达、预约开始、Step 1–4 到达、售卖方式选择、Service Area 查询结果、预约成功。内容曝光、入口点击、Contact Us、字段校验、照片、草稿、邮件和后台操作只进一方平台。

### 7.2 GA4 产品口径

### 7.2.1 页面停留时长（一期方案）

一期采用 GA4 默认互动时长指标（`user_engagement`、`engagement_time_msec`）分析 C1 页面和预约流程的互动情况。本期不要求逐屏精确停留时长，也不以 C1 独立 Session 时长作为统计口径。

该方案可回答 C1 页面及预约流程的平均互动时长、不同来源用户的整体参与度；不能回答首页每一屏精确停留秒数。后续若需要逐屏时长，再单独评估。

### 7.3 C1 独立分析口径

GA4 仍使用全站 Session，不另建 C1 Session。为支持 C1 单独分析，所有 C1 `page_view`、预约流程事件和 GA4 关键漏斗事件必须带稳定的 `business_domain=c1`；页面事件同时带 `page_id`，预约事件带 `flow_scope=c1_sell`。通过这些参数可筛选 C1 页面和 C1 预约流程的平均互动时长、渠道质量和漏斗转化，并与 C2 对比。

“C1 平均互动时长”定义为 GA4 在 C1 页面/事件上下文归因的 `engagement_time_msec` 汇总或平均；“C1 独立 Session 时长”不在一期提供。跨 C2→C1→C2 的完整 Session 时长仍属于全站口径，不得直接标记为 C1 时长。

| 一方 event_type | GA4 event_name | 参数白名单 | 关键事件 |
|---|---|---|---:|
| `page_view`（Sell 页面） | `page_view` | `business_domain=c1`、`page_type`、`page_id`、`locale`、`market`、`device_type`、低基数 `entry_source` | 否 |
| `seller_flow_start` | `c1_sell_flow_start` | `business_domain=c1`、`flow_scope=c1_sell`、`entry_source`、`prefilled_zip_present`、`preselected_method`、`device_type`、`locale` | 否 |
| `seller_step_view` | `c1_sell_step_view` | `business_domain=c1`、`flow_scope=c1_sell`、`step_id`、`device_type`、`locale` | 否 |
| `seller_service_area_check` | `c1_service_area_check` | `business_domain=c1`、预约内查询才带 `flow_scope=c1_sell`、`query_context`、`result_state`、成功时 `coverage_status`、`in_home_available`、`default_method`、`retry_flag` | 否 |
| `ui_interaction / selling_method_select`（C1-METHOD-03，selection_origin=user） | `c1_selling_method_select` | `business_domain=c1`、`flow_scope=c1_sell`、`selling_method`、`selection_origin=user`、`step_id`、`device_type` | 否 |
| `seller_request_submit` 接口成功 | `c1_sell_request_submit` | `business_domain=c1`、`flow_scope=c1_sell`、`selling_method`、`piece_count_bucket`、`category_count`、`brand_count`、`photo_count`、`coverage_status`、`preferred_date_present`、`referral_present`、`result_state=success` | 是 |

GA4 step_id 由一方 flow_step 映射；ZIP 发起只进入一方，明确查询终态按上表映射，失败/取消不携带 coverage_status。默认推荐、首页卡片点击不映射为预约内主动选择事件。

GA4 不接收 `request_id`、`seller_flow_id`、身份标识、完整 ZIP、自由文本、照片和高基数品牌列表。同一实际 C1 页面实例在 GA4 中只计一条页面浏览。

### 7.4 GA4 产品验收与技术交付

产品侧验收以下业务结果：

- 在 GA4 中可按 `business_domain=c1` 区分 C1，并按来源、页面、预约步骤、售卖方式及服务区域结果分析已定义的六类事件；
- 仅 `c1_sell_request_submit` 的接口成功被标记为关键事件；
- 同一实际 C1 页面实例只计一条页面浏览，刷新、返回、Retry 按本 PRD 的业务边界统计；
- GA4 中不出现姓名、联系方式、地址、完整 ZIP、照片、业务主键或自由文本；
- GA4 不可用不影响 C1 业务提交和一方平台采集。

事件接入方式、GA4 资源配置、参数注册和调试工具由技术团队按现有全站方案确定。开发交付时提供实际可查询的验证结果，证明上述产品验收结果成立。

## 八、开发验收用例

| 用例 | 通过标准 |
|---|---|
| C2→C1→C2 | 共享配置时身份/Session 连续；不共享时不伪造 ID |
| 四步漏斗 | 每次实际展示一条 `seller_step_view`；返回、刷新、草稿恢复不重复伪造 |
| Service Area | covered/uncovered/非法/网络失败分别可区分；Retry 和并发不重复 |
| 售卖方式 | 默认、主动选择、切换、不可用拦截可区分 |
| 提交成功 | 接口返回 success 时产生 GA4 关键事件；刷新不重复 |
| 隐私 | GA4 实际可查询事件与参数中无姓名、联系方式、地址、完整 ZIP、照片、业务主键和自由文本 |
| 跨端 | PC/Mobile 事件名、参数和业务含义一致 |

## 九、运营取数与开发交付边界

本期不新增 Looply Operations 报表页面。埋点事件写入自建数据平台，产品和运营通过已提供的查询方式、查询字段说明和脱敏聚合结果自行取数。查询结果至少支持需求规模、预约漏斗、售卖方式、服务区域四类问题；不得暴露姓名、联系方式、地址、完整 ZIP、照片和自由文本。

### 9.1 四类核心指标口径

自建数据平台是一方业务分析的主数据源；GA4 用于低敏关键漏斗及渠道比较，不替代以下运营主口径。下表的核心结果指标按唯一业务对象去重；页面点击、内容浏览和用户偏好等行为分析按实际发生的原始事件量统计，两类口径并行使用，互不替代。

| 业务问题 | 主指标与统计对象 | 分子 / 分母 / 去重规则 |
|---|---|---|
| 需求规模 | Sell 页面访问量、C1 访问会话、C1 访问用户 | 页面访问量＝有 C1 `page_view` 的唯一 `page_instance_id` 数；访问会话＝至少含一条 C1 `page_view` 的唯一 `session_id` 数；访问用户＝唯一 `anonymous_id` 数（缺失时不补造）。页面访问量是主指标；会话和用户用于来源、端类型、语言、Market 等切分。C1 不新建独立 Session。 |
| 预约漏斗 | 预约开始、Step 1–4 到达、前台提交成功 | 预约开始＝唯一 `seller_flow_id` 的 `seller_flow_start` 数；某步骤到达＝至少一次到达该步骤的唯一 `seller_flow_id` 数；前台提交成功＝至少一次接口成功的唯一 `seller_flow_id` 数。转化率同时提供“相对预约开始”（本步骤或成功 / 预约开始）和“相对上一步”（本步骤 / 上一步到达）；返回、刷新、草稿恢复、重复点击和 Retry 不增加同一流程的主漏斗计数。后台预约创建量不进入此前台成功率。 |
| 售卖方式 | 最终提交方式分布、主动选择行为、默认推荐方式 | 最终提交方式分布＝前台接口成功的唯一 `seller_flow_id`，按成功时 `selling_method` 分组，三种方式互斥，分母为全部前台接口成功流程。主动选择行为量＝每次实际发生的用户主动方式选择，按所选方式计数；同一流程切换多次或多种方式均按实际发生次数保留，不能将其作为互斥占比。默认推荐方式＝发生自动默认选择的唯一流程，按默认方式分组，单独展示。 |
| 服务区域 | 查询结果、覆盖率、未覆盖后的替代方式选择 | 查询结果＝有明确终态的唯一 `coverage_check_id`，分别展示 covered、uncovered、非法与失败；覆盖率＝covered /（covered + uncovered），仅成功查询进入分母，非法和失败单列。预约流程内的“未覆盖后选择替代方式”＝出现 uncovered 后又主动选择或前台接口成功为 VL/ST 的唯一 `seller_flow_id` / 出现 uncovered 的唯一 `seller_flow_id`；仅限 `query_context` 为预约流程的查询。用户主动 Retry 产生新的查询 ID，计为一次新的查询尝试。 |

后台预约创建量作为补充业务事实：按唯一 `request_id` 的 `seller_request_created` 统计，独立展示，不与前台提交成功率拼接、相除或逐条对账。

### 9.2 页面与偏好行为指标口径

页面、内容和偏好行为用于理解用户如何浏览、点击和选择，不用于替代第 9.1 节的漏斗或最终转化率。其统计单位为每次实际成立的前台行为事件：

| 行为类别 | 统计方式 | 不计入的情况 |
|---|---|---|
| 页面与内容浏览 | 记录实际页面到达、Sell 首页有效内容曝光和字典内内容入口/筛选/展开等每次行为；可按页面、模块、端类型和来源分析。 | 预加载、纯焦点移动、同一页面实例内重复的同一有效内容曝光。 |
| 页面与业务点击 | Header、Footer、Mobile Tab、CTA、卡片、FAQ、筛选、Continue、Back、关闭、Retry 等按每次实际点击或操作统计。 | 被重复点击拦截而未成立的同一操作，不作为新的业务点击。 |
| 用户偏好与选择 | 用户主动选择售卖方式、品类、品牌、件数区间等按每次实际选择或切换统计；一次流程内多次切换应保留全部行为，用于分析偏好变化。 | 系统默认推荐、自动恢复和自动切换不计为用户主动偏好；如需分析，单独按其业务状态展示。 |

原始行为量可以与唯一流程数并列查看，例如“方式选择次数”与“最终提交方式分布”同时提供；不得用点击量、切换量或查询尝试量直接作为预约转化率的分子或分母。

开发交付时需提供自建数据平台的查询入口或固定查询方法、字段说明、默认时间范围与时区、数据更新时间、权限范围，以及按上述口径输出的一份四类示例查询结果。查询方法可以是现有平台查询页、固定 Explore、SQL 模板或等价的受控方式，但本期不新增 Looply Operations 页面；具体工具形态不改变本节业务口径。

前台提交结果以接口返回状态统计；后台预约创建以独立业务事实 `seller_request_created` 统计并按 `request_id` 去重。本期不要求二者关联。GA4 关键事件反映前台接口成功，不替代后台预约创建事实。

## 十、开发评审读取边界

产品侧开发输入为本 PRD v1.4、Excel《C1 Sell 埋点开发清单 v1.2》及本需求第 4.1 节的 Figma 链接。产品需求不新增第二套身份、Session、来源或 GA4 实现方案；C2 公共字段复用与采集平台接入按现有平台能力处理，不改变本 PRD 已定义的 C1 业务语义、统计口径和隐私边界。
