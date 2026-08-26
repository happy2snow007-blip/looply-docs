# Looply 订单与交易数据接入需求 v1.0

> 目标：让订单、支付、退款和售后数据能够进入报表数仓，并与用户行为数据完成成交归因。

## 一、订单需要保存的归因信息

下单时随订单保存以下信息。可以放在订单表，也可以放在以`order_id`为唯一键的订单归因上下文表。

| 字段 | 谁提供 | 要求 |
|---|---|---|
| `order_id` | 订单服务 | 订单唯一键 |
| `user_id` | 登录／订单服务 | 登录订单保存；游客订单为空 |
| `domain_userid` | Web／埋点SDK | Snowplow浏览器ID，按实际值单独保存 |
| `anonymous_id` | 服务端／接收侧 | 从当前HttpOnly `looply_anonymous_id`取得并单独保存；缺失为空，不得用`domain_userid`复制填充 |
| `origin_session_id` | Web／埋点SDK、订单服务 | 正常Web Checkout下单时，Web／埋点SDK传入当时的Snowplow `session_id`，订单服务随订单或订单归因上下文保存；后续支付和成交数据按`order_id`沿用。正常Web下单不得缺失；明确不经过Web Checkout的订单可以为空，但必须能通过订单现有来源类型识别该例外 |
| `market_id`或`market_code` | 订单服务 | 订单所属Market；已有`market_id`时可由报表数仓关联Market表 |
| `promotion_code` | 订单服务 | 订单实际使用的社媒口令码／推广码；没有时为空 |

报表数仓同时保存`domain_userid`和`anonymous_id`，不根据任一ID自动合并不同`user_id`。后续比较两类ID的覆盖率和关联差异；需要更强的登录前后或跨设备身份串联时，再另行建设身份模块。

## 二、需要接入的权威业务数据

以下数据不由Web埋点生成，由报表数据接入／数仓任务直接读取权威业务表。本章是这些交易事实来源、字段与接入要求的唯一权威位置。

| 业务事实 | 报表逻辑事实名 | 唯一键 | 最少需要的数据 |
|---|---|---|---|
| 订单创建 | `order_created` | `order_id` | 创建时间、用户与归因信息、订单金额、币种、订单状态、`items[]` |
| 支付开始 | `payment_started` | `payment_attempt_id` | `order_id`、支付方式、开始时间 |
| 支付失败 | `payment_failed` | `payment_attempt_id` | `order_id`、失败时间、支付业务表已有的稳定失败分类 |
| 成交 | `purchase` | `order_id` | 首次支付成功时间、成交金额、币种 |
| 订单商品行 | — | `order_item_id` | `order_id`、`listing_public_code`、数量、退款前商品行成交金额 |
| 退款完成 | `refund` | `refund_id` | `order_id`、退款完成时间、金额、币种、退款商品行及行退款金额 |
| 售后过程 | — | 售后单ID | `order_id`、涉及的`order_item_id`、当前状态、处理结果，以及业务表已有的申请、受理、取消、结案时间或状态变更记录 |

支付失败原因按支付业务表已有的稳定分类读取；没有稳定分类时只统计支付失败，不上传支付机构原文或自由错误文本。

现有Flink `checkout_start→purchase`只属于历史代理链路，不作为本文件定义的权威成交事实，也不得进入报表成交事实表或成交指标。客户端公共`failure_type`不用于支付失败分类。

商品名称通过`listing_public_code`关联商品／Listing维表，不要求客户端重复上报。

为支持后续订单渠道报表，订单系统保存订单实际使用的`promotion_code`；推广码配置保存稳定的推广码与渠道／Campaign映射。报表数据接入／数仓任务同步GA4 `purchase`的原始`transaction_id`、Session渠道组、source、medium和Campaign，并按`transaction_id = order_id`保留订单关联关系。无法取得的字段保持为空，不补造默认值。本文件只规定原始数据的上报、记录和存储，不定义最终渠道归类优先级。
