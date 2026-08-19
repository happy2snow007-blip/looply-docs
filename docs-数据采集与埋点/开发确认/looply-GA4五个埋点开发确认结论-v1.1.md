# Looply GA4 五个埋点开发确认结论

> 版本：v1.1  
> 日期：2026-08-19  
> 状态：开发评审稿  
> 适用范围：回答《Looply GA4 五个埋点调整·需求分析报告》中的待确认项，不新增事件范围。

本文件用于回答开发分析报告中的问题；最终开发口径已合并进入《Looply GA4 埋点变更清单 v1.3》，实施时以v1.3为准。

## 一、开发确认结论

| 对应事件 | 开发提出的问题 | 确认结论 | 开发处理 |
|---|---|---|---|
| `view_search_results` | 是否保留主动上报，以及如何避免与 GA4 自动网站搜索重复 | 保留主动上报。GA4 后台关闭增强型衡量中的“网站搜索”，其他增强型衡量选项不变 | 继续发送 `looply_ga4_view_search_results`，最终进入 GA4 的事件名为 `view_search_results`；发布时同步关闭对应 Web 数据流的“网站搜索”自动采集 |
| `view_search_results` | `search_version`、`index_version` 从哪里取得 | 两个字段不属于本期 GA4 必要信息 | 从 GA4 必填字段和开发阻塞项中删除；不得使用前端常量或占位值 |
| `view_cart`、`remove_from_cart` | `cart_id` 是否需要由购物车接口新增返回 | `cart_id` 不属于本期 GA4 必要信息 | 从 GA4 必填字段和开发阻塞项中删除；不为 GA4 单独修改 CartView 或购物车后端契约 |
| `view_cart` | 非空、`items[]`和`value`统计哪些商品 | 只包含当前可购商品；不可购商品不进入事件 | `items[]`记录页面内全部可购商品，`value`为这些商品的金额合计；不受购物车勾选状态影响，实际勾选结算商品由`begin_checkout`记录；只有不可购商品时不发送`view_cart` |
| `search` | 输入联想是否必须提供稳定业务对象ID | 普通搜索词联想不要求稳定业务对象ID | 必填`search_term`、`trigger_type=suggestion_select`和建议位置；有稳定实体ID时可选传`suggestion_object_id`，没有时不得伪造 |
| `search` | 热门品牌、热门Collection是否作为搜索 | 不作为搜索 | 不发送`search`；按入口点击和目标Collection页面`page_view`处理 |
| `remove_from_cart` | 当前购物车商品数量固定为1，是否同时建设数量修改能力 | 本期只覆盖现有成功删除，不新增数量修改能力 | 成功删除后发送一次，实际减少数量为1；删除失败、无变化或只露出删除操作不发送 |

## 二、搜索提交与结果关联

### 2.1 需要取消的旧限制

取消“所有`view_search_results`都必须存在前序`search`”的限制。

调整后两个事件分别成立：

- `search`记录用户通过站内搜索入口主动提交搜索；
- `view_search_results`记录搜索结果实际展示及该次结果的终态。

站内主动提交和结果事件通过结果页URL中的结构化搜索上下文保持口径一致；直达搜索URL、刷新或页面恢复没有新的用户提交动作，因此允许只有`view_search_results`。

### 2.2 开发发送矩阵

| 场景 | 是否发送`search` | 是否发送`view_search_results` | 结果页URL与事件处理 |
|---|---:|---:|---|
| 点击搜索轮播词 | 是 | 结果实际展示后发送 | 结果页URL携带搜索词与`trigger_type=carousel_term_button`，两类事件读取相同结构化上下文 |
| 手动输入后按回车 | 是 | 结果实际展示后发送 | 结果页URL携带搜索词与`trigger_type=manual_enter` |
| 手动输入后点击搜索按钮 | 是 | 结果实际展示后发送 | 结果页URL携带搜索词与`trigger_type=manual_search_button` |
| 点击输入联想 | 是 | 结果实际展示后发送 | 结果页URL携带搜索词与`trigger_type=suggestion_select` |
| 点击搜索历史 | 是 | 结果实际展示后发送 | 结果页URL携带搜索词与`trigger_type=history_select` |
| 点击热门搜索词 | 是 | 结果实际展示后发送 | 结果页URL携带搜索词与`trigger_type=popular_term_select` |
| 首次直达带有效搜索词的结果URL | 否 | 结果实际展示后发送 | 直接读取当前URL中的搜索上下文 |
| 刷新搜索结果页 | 否 | 结果重新展示后发送 | 读取当前URL；新`page_instance_id`区分新的结果页实例 |
| 前进、后退或页面恢复后重新展示结果 | 否 | 结果重新展示后发送 | 读取当前URL；按实际页面实例记录 |
| Apply筛选、Apply排序或Reset | 否 | 更新后的结果形成终态后发送 | 更新URL中的筛选／排序参数；操作另记`ui_interaction`，不产生新的`search` |
| URL有搜索参数但未执行搜索或未形成结果终态 | 否 | 否 | 不发送 |

### 2.3 具体实现规则

1. 站内主动提交时发送`search`，同时进入携带搜索词、`trigger_type`及当前筛选／排序参数的结果页URL。
2. 结果进入最终状态时发送`view_search_results`；事件从当前结果页URL读取结构化搜索上下文，并携带当前`page_instance_id`。
3. 每次初始加载或URL参数生效后的结果更新只发送一条`view_search_results`，使用独立`event_id`，终态只能是`success`、`no_results`、`failed`或`cancelled`之一。
4. 直达、刷新、前进后退或页面恢复可以产生新的结果页实例，但不得反向补发`search`。
5. 筛选、排序和重置属于结果页操作，不产生新的`search`；结果更新完成后记录新的`view_search_results`及更新后的URL上下文。
6. 分析时，站内主动搜索次数按`search`事件计数；结果展示、成功、零结果和失败按`view_search_results`计数。商品曝光、点击及商详来源通过结果页`page_instance_id`、结构化搜索上下文、商品标识、Session和事件时间关联。

## 三、GA4后台设置与上线验收

### 3.1 设置调整

路径：GA4管理 → 数据收集和修改 → 数据流 → Looply Web数据流 → 增强型衡量功能 → 设置。

- 关闭“网站搜索”；
- 不关闭增强型衡量功能总开关；
- 网页浏览量、滚动次数、出站点击等其他选项保持当前设置。

### 3.2 验收要求

1. 在测试环境确认主动`view_search_results`已正常进入GA4后，再调整正式数据流设置。
2. 分别验证搜索成功、零结果、失败和取消场景。
3. 同一次站内正式提交只出现一条`search`；结果页按实际`page_instance_id`记录`view_search_results`。两类事件的搜索词和触发方式应与结果页URL上下文一致；直达URL、刷新和页面恢复允许只有`view_search_results`。
4. 关闭“网站搜索”后，确认带`keyword`等查询参数的结果页不会再额外生成第二条自动`view_search_results`。
5. 验证`view_cart`只包含可购商品；`remove_from_cart`只在购物车实际减少后产生。

## 四、不需要扩大的开发范围

- 不为GA4新增或改造搜推版本字段接口；
- 不为GA4新增购物车主体ID接口；
- 不为GA4新增购物车数量修改能力；
- 不要求普通搜索词联想新增稳定业务对象ID；
- 不修改本次五个事件以外的GA4事件。
