# Looply GA4 首版变更清单

> 版本：v1.0  
> 日期：2026-08-14  
> 状态：可交付 GA4 开发  
> 适用范围：仅处理本清单列出的 GA4 事件；未列出的 GA4 事件、自动采集和现有标准字段保持当前方式。

本清单与《Looply GA4数据分析 PRD v1.3》共同构成 GA4 开发依据：v1.3 继续作为未调整内容的原始基线；本清单对列出的六个事件及 `items[].item_id=listing_public_code` 规则拥有更高优先级。两份文档存在冲突时，以本清单为准。

## 一、现有 GA4 事件调整

| 优先级 | GA4 事件 | 当前开发定位 | 当前情况 | 修改要求 | 必要信息 | 不处理的后果 | 验收标准 |
|---|---|---|---|---|---|---|---|
| P0，最高 | `purchase` | dataLayer Custom Event：`looply_ga4_purchase` | 浏览器主发，服务端兜底 | 改为服务端确认订单首次支付成功后，通过唯一正式路径发送一次；浏览器成功页不再发送 | `transaction_id=order_id`；金额、币种、税费、运费和`items[]`取服务端成交事实；每个`items[].item_id=listing_public_code` | 用户未打开成功页可能漏报；浏览器与服务端并发可能重复记录成交和收入 | 同一`order_id`只产生一笔GA4成交；刷新、重复回调和再次打开成功页不增加成交或收入；GA4与服务端成交金额、币种和商品明细可对账 |
| P0 | `search` | dataLayer Custom Event：`looply_ga4_search` | 搜索接口成功或明确无结果时发送 | 改为用户通过建议、热门词、回车或搜索按钮正式提交时发送一次；使用本次提交的`search_id`；`search_term`只取搜索模块正式输出 | `search_id`、`search_term`、`trigger_type`；建议触发时增加建议类型、位置和稳定业务对象ID | 搜索意图受接口结果影响，失败搜索消失，搜索次数口径不稳定 | 每次正式提交恰好一条`search`；接口结果不反向决定是否产生提交事件；输入变化和建议仅展示不发送 |
| P0 | `view_item_list` | dataLayer Custom Event：`looply_ga4_view_item_list` | 列表数据成功展示即形成曝光 | 改为单件商品达到50%可视且连续1秒时形成真实曝光；同一`page_instance_id`内按`placement_id + listing_public_code`去重 | `page_instance_id`、`placement_id`、商品位置及`items[]`；每个`items[].item_id=listing_public_code` | 曝光虚高，点击率和推荐效果被低估 | 未达到阈值、后台或失焦不发送；同一页面实例同一展示位的同一商品只计一次；新页面实例可重新计数 |

## 二、新增 GA4 事件

| 优先级 | GA4 事件 | dataLayer Custom Event | 新增要求 | 必要信息 | 不新增的后果 | 验收标准 |
|---|---|---|---|---|---|---|
| P0 | `view_search_results` | `looply_ga4_view_search_results` | 每次搜索请求进入最终结果时发送一次，并通过`search_id`关联对应`search` | `search_id`、`result_status`、`duration_ms`、`search_version`、`index_version`；成功时记录`result_count`，失败时记录低基数`failure_type` | 无法准确计算搜索成功率、零结果率和失败率 | 同一`search_id`只有一个终态；`result_status`区分`success`、`no_results`、`failed`、`cancelled`；失败不记作零结果 |
| P1 | `view_cart` | `looply_ga4_view_cart` | 非空购物车成功展示时，每个`page_instance_id`发送一次 | `page_instance_id`、`cart_id`、`currency`、`value`和`items[]`；每个`items[].item_id=listing_public_code` | 无法区分已加购未查看购物车与查看后未结账 | 空购物车、加载失败和同页面重复渲染不发送；刷新或重新进入产生新页面实例后可再次发送 |
| P1 | `remove_from_cart` | `looply_ga4_remove_from_cart` | 商品成功删除或数量真实减少时发送 | `cart_id`、实际减少数量、币种、金额和`items[]`；每个`items[].item_id=listing_public_code` | 无法分析购物车减少行为和购物车流失 | 只有购物车内容或数量真实减少才发送；失败、无变化和仅打开操作区不发送；减少数量与购物车结果可核对 |

## 三、统一约束

1. 本清单只修改以上六个 GA4 事件，未列出的现有 GA4 事件保持当前实现。
2. 同一业务事实只发送一次，不由浏览器、服务端或多个适配器重复产生同义 GA4 事件。
3. GA4 商品标识统一使用`items[].item_id=listing_public_code`；`listing_public_code`来源于`listings.public_code`。
4. GA4不得接收邮箱、电话、姓名、地址明文、支付卡信息、支付令牌或自由错误文本。
5. `search_id`用于关联一次搜索提交与其最终结果；同一次搜索的`search`和`view_search_results`使用完全相同的值。

## 四、开发完成条件

- 六个事件分别在测试环境完成单事件验证。
- `purchase`完成同一订单重复回调、刷新和再次打开成功页的防重验证。
- `search`与`view_search_results`完成一对一关联、成功、零结果、失败和取消场景验证。
- `view_item_list`完成可视阈值、持续时间、前后台和页面实例去重验证。
- `view_cart`和`remove_from_cart`完成成立条件与不计入边界验证。
- GA4 DebugView或等效测试证据能够显示事件名、触发次数和必要信息符合本清单。
