# Looply GA4数据分析 PRD 修订记录

| 版本 | 日期 | 修改人 | 修改内容 |
|---|---|---|---|
| v1.3 | 2026-07-30 | Looply产品 | 独立GA4开发基线；地区门控、页面语言、金额、Purchase浏览器主路径与服务端兜底、Refund服务端路径。 |
| v1.4 | 2026-08-20 | Looply产品 | 纳入`search`、`view_search_results`、`view_item_list`、`view_cart`、`remove_from_cart`五个事件的目标规则、字段来源、传递链路、测试环境验收结果和修复后复验用例；冻结“事件与参数分离”规则，参数缺失不阻止事件发送且本期不新增诊断机制；明确`filter_ids`格式及PC Cart Drawer的`view_cart`规则；商品ID改为`listing_public_code`；取消`search_id`和`search_request_id`要求；明确增强型衡量仅关闭“网站搜索”；统一业务参数缺失时仍发送事件的全局校验规则；统一PC＋Mobile Wishlist／Recently Viewed展示位；明确`page_instance_id`由Web公共上下文生成并随适用GA4事件发送；增加新增参数的GA4报表、探索或原始数据用途；将PRD设为唯一规则位置，验收修复单精简为实测问题、修改目标和复测索引。 |
