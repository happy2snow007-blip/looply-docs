# Looply GA4数据分析 PRD 修订记录

| 版本 | 日期 | 修改人 | 修改内容 |
|---|---|---|---|
| v1.3 | 2026-07-30 | Looply产品 | 独立GA4开发基线；地区门控、页面语言、金额、Purchase浏览器主路径与服务端兜底、Refund服务端路径。 |
| v1.4 | 2026-08-20 | Looply产品 | 纳入`search`、`view_search_results`、`view_item_list`、`view_cart`、`remove_from_cart`五个事件的目标规则、字段来源、传递链路、测试环境验收结果和修复后复验用例；冻结“事件与参数分离”规则，参数缺失不阻止事件发送且本期不新增诊断机制；明确`filter_ids`格式及PC Cart Drawer的`view_cart`规则；商品ID改为`listing_public_code`；取消`search_id`和`search_request_id`要求；明确增强型衡量仅关闭“网站搜索”；统一业务参数缺失时仍发送事件的全局校验规则；统一PC＋Mobile Wishlist／Recently Viewed展示位；明确`page_instance_id`由Web公共上下文生成并随适用GA4事件发送；增加新增参数的GA4报表、探索或原始数据用途；将PRD设为唯一规则位置，验收修复单精简为实测问题、修改目标和复测索引。 |
| v1.5 | 2026-08-26 | Looply产品 | Search／Collection动态筛选改为后台稳定`dimension_code + option_code`驱动；删除前端固定筛选维度白名单；GA4 `filter_ids`按`dimension_code:option_code`序列化；补齐Apply、取消、Reset、动态`Series`维度及Code到展示名称映射边界；同步五事件PRD、GA4变更清单、一方埋点规则与详细点位表。 |
| v1.6 | 2026-08-28 | Looply产品 | 将线上验收确认的目标规则回写为正式开发基线：搜索入口临时字段隔离、正式新搜索生成新页面实例、保留GA自动`page_view`并以`page_view_source`区分主动事件、主动`view_search_results`增加来源标识、禁止空商品曝光、点击携带真实位置并统一列表标识、`page_referrer`读取真实上一页面、事件ID跨类型隔离、`view_item`携带PDP页面实例、`add_shipping_info`按新建／复用／修改后的有效保存事实发送并递增`step_version`；删除旧验收状态，改为最终验收要求。 |
| v1.7 | 2026-08-31 | Looply产品 | 按已发布《数据采集与埋点产品需求 v1.8》统一Purchase为服务端权威事实与唯一投递路径：订单／支付服务端首次确认父订单进入最终`paid`即成立，由唯一服务端发送者通过Measurement Protocol投递，`transaction_id=order_id`；浏览器不发送、不claim、不确认、不补发；删除5分钟兜底、浏览器确认表、相关状态、示例与验收用例，并补充关联上下文缺失不阻断成交事实、服务端幂等和订单对账要求。规则确认不代表生产已经实现。 |
| v1.8 | 2026-08-31 | Looply产品 | 收口A01–A05最终口径：区分事件发生时`page_location`与页面实例上一来源`page_referrer`；`add_shipping_info`改为同一checkout首次有效tier及后续tier变化，撤销地址变化即递增和`shipping_info_source`必填；明确PC Favorites Drawer沿用当前页面实例；主动来源字段增加Web、dataLayer、GTM、生产容器和真实请求全链路验收。同步五事件PRD v1.2、采集PRD v1.9与收口开发包v1.4。 |
| v1.9 | 2026-09-01 | Looply产品 | 临时收口数据污染：`view_item_list`改为新列表结果成功展示时每次一条，滚动／分页不再发送并新增`list_instance_id`；暂停Looply主动`page_view`、保留GA自动`page_view`；继续由Looply按搜索请求唯一终态发送`view_search_results`，网站搜索自动衡量保持关闭。同步全量验收用例与三项变更专项用例。 |

| v1.10 | 2026-09-02 | Looply产品 | 产品逐项确认并统一收口：Search滚动／分页追加不发送`view_search_results`；PC Wishlist Drawer保留列表展示与商品点击记录，滚动追加和相同结果重开不重复；暂停Looply主动`page_view`并保留GA4自动页面浏览；不以独立“干净日”重建历史基线。 |
