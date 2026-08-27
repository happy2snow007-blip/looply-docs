# Looply GA4 全量事件清单

| Looply事件 | dataLayer Custom Event | GA4事件 | 权威触发时机 | 应传业务信息 |
|---|---|---|---|---|
| page_view | looply_ga4_page_view | page_view | 首次页面主路由确认、有效SPA路由完成或硬刷新形成新页面生命周期 | page_instance_id、page_location、page_title、page_language |
| lead | looply_ga4_generate_lead | generate_lead | 联系线索接口成功 | lead_id、lead_type |
| sign_up | looply_ga4_sign_up | sign_up | 注册事务成功一次 | registration_id、method |
| login | looply_ga4_login | login | 用户真实登录成功 | login_id、method |
| view_item_list | looply_ga4_view_item_list | view_item_list | 单件商品达到50%可视且持续1秒 | page_instance_id、placement_id、商品位置、items；搜索结果页增加URL解析出的搜索上下文 |
| select_item | looply_ga4_select_item | select_item | 用户从列表主动点击商品 | page_instance_id、selection_id、item_list_id/name、items |
| search | looply_ga4_search | search | 用户通过六种正式入口提交搜索 | search_term、trigger_type；联想场景按条件增加建议位置与稳定对象ID |
| view_search_results | looply_ga4_view_search_results | view_search_results | 搜索结果请求形成唯一终态 | page_instance_id、search_term、result_status、duration_ms；站内提交且URL存在时增加trigger_type；成功时增加result_count，失败时增加failure_type |
| view_item | looply_ga4_view_item | view_item | 商详核心内容可见 | currency、value、单个item |
| add_to_wishlist | looply_ga4_add_to_wishlist | add_to_wishlist | 首次收藏事务成功 | wishlist_operation_id、currency、value、items |
| add_to_cart | looply_ga4_add_to_cart | add_to_cart | 加购事务成功 | cart_operation_id、currency、value、shangitems |
| view_cart | looply_ga4_view_cart | view_cart | Shopping Bag或PC Cart Drawer中的非空可购商品成功展示 | page_instance_id、currency、value、items |
| remove_from_cart | looply_ga4_remove_from_cart | remove_from_cart | 当前一物一码商品成功从购物车删除 | currency、value、实际减少数量为1的items |
| begin_checkout | looply_ga4_begin_checkout | begin_checkout | checkout session创建成功 | checkout_id、currency、value、items |
| add_shipping_info | looply_ga4_add_shipping_info | add_shipping_info | 地址和配送方式校验保存成功 | checkout_id、step_version、shipping_tier、金额、items |
| add_payment_info | looply_ga4_add_payment_info | add_payment_info | 支付方式token化保存成功 | checkout_id、step_version、payment_type、金额、items |
| purchase | looply_ga4_purchase | purchase | 后端确认paid且浏览器claim成功 | order_id、value、tax、shipping、currency、items |
| refund | — | refund | 支付渠道确认退款成功；仅服务端 | refund_id、order_id、value、currency、退款items |
