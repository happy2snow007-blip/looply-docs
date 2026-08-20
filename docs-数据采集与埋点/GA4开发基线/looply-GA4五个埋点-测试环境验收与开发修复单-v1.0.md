# Looply GA4 五个埋点测试环境验收与开发修复单

> 版本：v1.0  
> 日期：2026-08-20  
> 测试环境：`https://www.test.looply.com/`  
> GA4媒体资源：`Looply-test`  
> Measurement ID：`G-VFBQX6RSB7`  
> 目标读者：负责GA4 Web埋点修改的开发或开发AI  
> 当前结论：GA4接收链路已通过，但本单五个事件尚需按PRD修改并复测。

## 一、文档职责与任务边界

《Looply GA4数据分析 PRD v1.4》是事件语义、字段来源、缺失处理、枚举、去重和验收规则的唯一权威位置。本单只记录测试环境已观察问题、本次修改目标和待复测用例，不再维护第二套完整事件规则。

本次主业务口径只修改以下五个GA4事件：

- 调整：`search`、`view_item_list`。
- 新增或补齐：`view_search_results`、`view_cart`、`remove_from_cart`。

为闭合公共页面实例关联，同步为现有`page_view`和`select_item`补充`page_instance_id`参数，不改变两个事件的触发点和业务语义。除此之外，本次不修改`purchase`及其他现有GA4事件；不新增`search_id`或`search_request_id`要求。同一业务事实只保留一个触发点，不新旧同义双发。

## 二、开发查找入口

开始修改前，在Web仓库中搜索以下物理事件名及其全部调用点：

```text
looply_ga4_search
looply_ga4_view_search_results
looply_ga4_view_item_list
looply_ga4_view_cart
looply_ga4_remove_from_cart
```

## 三、当前问题与修改目标

| GA4事件 | 当前实测已通过 | 当前问题 | 开发修改目标 | PRD权威位置 |
|---|---|---|---|---|
| `search` | 请求到达GA4并返回HTTP 204；单次点击只观察到一条；已有`search_term=chanel` | 缺当前场景`trigger_type=manual_search_button` | 六种正式提交动作各自使用唯一枚举，并在提交、结果URL、结果事件和搜索结果曝光中保持一致 | 3.5.1、3.5.5、9.5 |
| `view_search_results` | 成功结果请求到达GA4；已有`result_status=success`、`duration_ms=4395`、`result_count=1590` | 成功结果缺`search_term`及与提交动作一致的`trigger_type`；直达无结果页未发送`no_results` | 每次结果更新只形成一个终态；结果事件从当前URL读取搜索上下文；直达URL不补造`search`但产生结果终态 | 3.5.1、3.5.4、3.5.5、9.5 |
| `view_item_list` | 请求到达GA4；`items[].item_id`已使用CP开头的`listing_public_code` | 首屏产生8条事件且每条重复携带全部40件商品；缺`page_instance_id`、`placement_id`、商品位置和搜索上下文 | 只有真实达到50%可视且持续1秒的新商品进入载荷；按页面实例＋展示位＋商品去重；展示位使用PRD封闭表，其中Wishlist和Recently Viewed覆盖PC＋Mobile | 3.5.2、3.5.4、3.5.5、9.5 |
| `view_cart` | 非空购物车成功发送；已有`page_instance_id`、`value`和正确商品；同页面未重复发送；空购物车未发送 | 缺`currency` | Shopping Bag和PC Cart Drawer中非空可购商品成功展示时发送，同时携带相互匹配的`currency`、`value`和全部可购商品 | 3.5.3、3.5.4、3.5.5、9.5 |
| `remove_from_cart` | 商品成功删除后发送；商品、实际减少数量1和`value`正确 | 缺`currency` | 删除成功后发送一次，携带被删除商品的币种、实际减少金额、价格和数量1 | 3.5.3、3.5.5、9.5 |

## 四、通用修改约束

1. 业务事实成立时发送事件；业务参数缺失不阻止事件发送。可取参数正常携带，不可取参数省略且不伪造默认值。具体执行PRD 3.1、3.5.5和4.3。
2. `page_instance_id`由Web公共页面上下文统一生成。`page_view`、`view_search_results`、`view_item_list`、`select_item`和`view_cart`在同一页面实例中读取同一值，具体执行PRD 3.4、3.5.4和3.5.5。
3. 新增GA4参数的报表、探索或原始数据用途执行PRD 3.5.6，本单不重复定义。
4. 本期不新增线上参数缺失诊断事件或诊断机制。

## 五、修复后复测索引

| 复测范围 | 执行PRD用例 | 当前状态 |
|---|---|---|
| 六种搜索提交和热门品牌／Collection边界 | G02–G07 | 待修复后复测 |
| 搜索成功、无结果、直达URL和筛选／排序／Reset | G08–G11 | 待修复后复测 |
| 商品曝光阈值、去重、展示位和搜索上下文 | G12–G13 | 待修复后复测 |
| Shopping Bag、PC Cart Drawer和删除商品 | G14–G16 | 待修复后复测 |
| 同一页面实例的GA4与一方事件关联 | G17 | 待修复后复测 |

每项复测保留Tag Assistant、DebugView或浏览器真实`g/collect`请求证据。事件名称、次数、参数和值全部符合PRD后，本批五个事件方可判定通过。
