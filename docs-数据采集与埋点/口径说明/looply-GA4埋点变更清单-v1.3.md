# Looply GA4 埋点变更清单

> 版本：v1.3  
> 日期：2026-08-19  
> 状态：开发评审稿  
> 适用范围：仅处理本清单列出的 GA4 事件；未列出的 GA4 事件、自动采集和现有标准字段保持当前方式。

本清单与《Looply GA4数据分析 PRD v1.3》共同构成 GA4 开发依据：v1.3 继续作为未调整内容的原始基线；本清单对列出的五个事件及 `items[].item_id=listing_public_code` 规则拥有更高优先级。两份文档存在冲突时，以本清单为准。

## 一、现有 GA4 事件调整

| 优先级 | GA4 事件 | 当前开发定位 | 当前情况 | 修改要求 | 必要信息 | 不处理的后果 | 验收标准 |
|---|---|---|---|---|---|---|---|
| P0 | `search` | dataLayer Custom Event：`looply_ga4_search` | 搜索接口成功或明确无结果时发送 | 改为用户通过搜索轮播词、手动输入后回车或搜索按钮、输入联想、搜索历史或热门搜索词正式提交时发送一次；`search_term`只取搜索模块正式输出；进入结果页时由URL携带搜索上下文参数 | `search_term`、`trigger_type`；联想触发时增加建议类型和位置，有稳定实体ID时可选传`suggestion_object_id` | 搜索意图受接口结果影响，失败搜索消失，搜索次数口径不稳定 | 每次正式提交恰好一条`search`；接口结果不反向决定是否产生提交事件；输入变化和建议仅展示不发送；热门品牌和热门Collection入口不发送`search` |
| P0 | `view_item_list` | dataLayer Custom Event：`looply_ga4_view_item_list` | 列表数据成功展示即形成曝光 | 改为单件商品达到50%可视且持续1秒时形成真实曝光；同一`page_instance_id`内按`placement_id + listing_public_code`去重 | `page_instance_id`、`placement_id`、商品位置及`items[]`；每个`items[].item_id=listing_public_code`；搜索结果页曝光增加从当前URL解析的`search_term`、`trigger_type`及已生效筛选／排序上下文 | 曝光虚高，点击率和推荐效果被低估 | 未达到阈值、后台或失焦不发送；同一页面实例同一展示位的同一商品只计一次；新页面实例可重新计数 |

## 二、新增 GA4 事件

| 优先级 | GA4 事件 | dataLayer Custom Event | 新增要求 | 必要信息 | 不新增的后果 | 验收标准 |
|---|---|---|---|---|---|---|
| P0 | `view_search_results` | `looply_ga4_view_search_results` | 搜索结果页初始加载或URL参数生效后的结果实际展示并形成终态时发送一次；直达URL、刷新或页面恢复允许独立产生本事件，但不得补造`search` | `event_id`、`page_instance_id`、从当前结果页URL解析的`search_term`和`trigger_type`、`result_status`、`duration_ms`；成功时记录`result_count`，失败时记录低基数`failure_type`；筛选／排序已生效时记录结构化上下文 | 无法准确计算搜索成功率、零结果率和失败率，也无法识别直达搜索结果页 | 每次初始加载或URL参数生效后的结果更新只有`success`、`no_results`、`failed`、`cancelled`之一；失败不记作零结果；筛选、排序或重置更新结果时不额外产生`search` |
| P1 | `view_cart` | `looply_ga4_view_cart` | 非空购物车中的可购商品成功展示时，每个`page_instance_id`发送一次 | `page_instance_id`、`currency`、`value`和`items[]`；`items[]`包含页面内全部可购商品，`value`为这些商品的金额合计；每个`items[].item_id=listing_public_code` | 无法区分已加购未查看购物车与查看后未结账 | 空购物车、只有不可购商品、加载失败和同页面重复渲染不发送；刷新或重新进入产生新页面实例后可再次发送；不受勾选状态影响 |
| P1 | `remove_from_cart` | `looply_ga4_remove_from_cart` | 当前一物一码商品成功删除后发送；本期不新增数量修改能力 | 实际减少数量1、币种、金额和`items[]`；每个`items[].item_id=listing_public_code` | 无法分析购物车减少行为和购物车流失 | 只有购物车内容真实减少才发送；失败、无变化和仅打开操作区不发送；删除结果可与购物车状态核对 |

## 三、统一约束

1. 本清单只修改以上五个 GA4 事件，未列出的现有 GA4 事件保持当前实现。
2. 同一业务事实只发送一次，不由浏览器、服务端或多个适配器重复产生同义 GA4 事件。
3. GA4 商品标识统一使用`items[].item_id=listing_public_code`；`listing_public_code`来源于`listings.public_code`。
4. GA4不得接收邮箱、电话、姓名、地址明文、支付卡信息、支付令牌或自由错误文本。
5. `search`和搜索结果相关事件分别从提交动作与结果页URL取得结构化搜索上下文；直达URL、刷新或页面恢复允许只有`view_search_results`，不得补造用户主动`search`。
6. `search_version`、`index_version`和`cart_id`不属于本期GA4必要字段，不为这些字段扩展搜推或购物车接口，也不得填充占位值。
7. GA4 Web数据流关闭增强型衡量中的“网站搜索”，其他增强型衡量选项保持当前设置，避免自动和主动`view_search_results`重复。

## 四、开发完成条件

- 五个事件分别在测试环境完成单事件验证。
- `search`验证六种正式提交方式；直达URL、刷新和页面恢复不得补造`search`。
- `view_search_results`验证主动提交进入结果页、无前序提交的结果展示，以及成功、零结果、失败和取消场景；搜索上下文与当前结果页URL一致。
- `view_item_list`完成可视阈值、持续时间、前后台和页面实例去重验证；搜索结果页曝光带当前URL解析出的结构化搜索上下文。
- `view_cart`只包含可购商品；`remove_from_cart`只在当前商品成功删除后产生。
- GA4后台关闭“网站搜索”后，带搜索参数的结果页不会额外产生第二条自动`view_search_results`。
- GA4 DebugView或等效测试证据能够显示事件名、触发次数和必要信息符合本清单。
