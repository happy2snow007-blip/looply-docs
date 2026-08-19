# Looply 数据采集与埋点产品需求修订记录

## V1.0｜2026-08-13

- 首次形成可交付开发的冻结基线。
- 统一定义 22 个业务事件、48 个页面与业务操作节点、18 个跨页面业务节点。
- 明确身份与一方 Session、商品与订单标识、事件成立条件、平台去向和存量埋点处理。
- 明确 GA4 自动采集与主动适配互斥，同一业务事实不得重复上报或重复统计。
- 商品真实曝光采用 50% 可视且连续 1 秒；每件商品形成一条逻辑曝光事实。
- 归因仅采集原始触点与关联事实，归因模型、窗口和分类由成交归因及报表需求定义。
- 冻结前 Review：P0=0、P1=0；准确性、冲突、重复、冗余全部通过。

冻结来源：`looply-数据采集与埋点产品需求-v0.1.md`，冻结前 SHA-256：`ba4f7ac25da406dab95f8514b6ac3ee6d0ce33b74aa60cd5a2a63e15f173b66c`。

## V1.1｜2026-08-14

- 一方平台直接沿用搜推现有 `checkout_start` 作为 `begin_checkout`，不新增第二条开始结算事件。
- 删除对独立 `checkout_session_id` 的产品要求；Checkout 后续行为改为关联现有 `checkout_start` 的事件 ID。
- `add_shipping_info`、`add_payment_info` 分别覆盖新填写、复用已有信息和修改已有信息，并与同一条 `checkout_start` 关联。
- 订单能够回指时保留 `origin_checkout_start_event_id` 与对应的 `origin_session_id`；无法回指时保持未知，不影响权威订单事实成立。
- 明确搜推现有搜索结果记录新增字段 `search_id`，并与对应搜索提交使用同一个值。
- 删除第五章重复的存量摘要表；统一事件规则以5.1—5.3为准，搜推存量调整集中在5.4说明。
- 从主文档删除GA4首版变更明细，改为引用独立《Looply GA4首版变更清单》；搜推存量调整顺延为5.4。
- 明确搜推新增搜索提交事件 ID 为 `search_submit`，并补充现有搜索结果事件 `search` 的 SDK 方法、Schema 和当前字段，供开发直接定位。
- 搜索提交事件记录提交动作实际发生页面；只有真实到达搜索结果页后，才由页面访问事件记录`listing/search_results`。
- 补齐九种`trigger_type`，并记录结构化`filters[]`与`sort_type`；热门品牌和热门Collection改为入口点击加目标Collection页访问，不计入搜索。
- 明确《Looply GA4首版变更清单 v1.0》与旧 GA4 PRD v1.3 的适用关系：未调整内容沿用旧基线，六个变更事件及商品标识冲突以新清单为准。
- 第七章改为一方平台数据引用索引；防重复规则只以第2.2节为权威来源；第九章删除事件级重复验收并修正数据最小化引用。

## V1.2｜2026-08-14

- 明确搜索结果页产生的商品曝光`view_item_list`必须携带本次搜索的`search_id`，用于关联搜索提交与后续商品曝光。
- 同步更新搜索结果节点P16的触发与验收要求；不新增统一事件，不改变GA4首版变更范围。

## V1.3｜2026-08-14

- 新增站内找货入口映射，统一定义首页Feed、Collection、商详You May Also Like和搜索热词四类首期报表入口。
- 明确`entry_type`由分析环节根据原始事件上下文派生，客户端不新增上报该字段。
- 明确搜索热词入口必须通过同一`search_id`关联搜索提交与结果页商品曝光；仅点击热词不计商品曝光。
- 区分首期报表入口与其他已采集场景，Recently Viewed、无结果推荐、普通搜索结果、收藏列表和Shop入口不强行归入四类。

## V1.4｜2026-08-17

- 当前终端范围调整为PC Web和Mobile Web；PC无独立Shop／Favorites页面，Tablet Web尚未适配，不纳入本期页面与交互验收。
- 新增Mobile首页Back to Top、商品详情Share、Mobile Favorites Add More Card、Contact Us提交四类有意义操作的稳定映射。
- Favorites Retry继续复用通用P03，并区分Wishlist、Recently Viewed及两模块组合加载失败对象；Explore Items继续复用P28。
- 明确Price Drop、Loading、空态和分模块／组合失败属于展示状态，不自动新增点击事件。
- 未在最新Figma 1.1确认Recently Viewed删除或View All控件，本期不增加对应埋点。
- Share与Contact Us提交补充数据最小化要求，不采集分享内容、联系人、外部账号、姓名、邮箱、消息正文或自由错误文本。

## V1.7｜2026-08-19

- 取消搜索请求ID要求，搜索提交、结果、曝光、点击和商详来源改用结果页URL结构化搜索上下文。
- 搜索次数按`search.event_id`去重；结果状态按`view_search_results.event_id`去重。
- 筛选、排序和Reset不产生新的`search`，只记录操作及更新后的结果终态。
- 重复打开相同URL由`page_instance_id`区分页面实例；同一页面内多次结果更新由各自`event_id`区分。
- 同步调整GA4开发清单、全页面操作覆盖清单及数据分析报表相关文档。
