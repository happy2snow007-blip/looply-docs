# Looply 订单与交易数据接入：后端事件契约 v1.1

> 本文只定义一方订单、支付、成交、退款数据的后端事件和字段。搜索、商详、收藏、加购等前端事件不在本文重复定义。

## 1. 后端事件定义表

| 模块 | 动作 | 业务事实事件 | 触发时机 | 业务唯一键 | 事件专属参数 |
|---|---|---|---|---|---|
| 订单 | 创建订单 | `order_created` | 订单创建成功并落库后 | `order_id` | `created_at`、订单金额、`currency`、订单状态、`items[]`（含 `order_item_id`、`listing_public_code`、数量、商品行成交金额） |
| 支付 | 开始支付尝试 | `payment_started` | 每次支付尝试真正发起前 | `payment_attempt_id` | `order_id`、支付方式、`started_at` |
| 支付 | 支付失败 | `payment_failed` | 一次支付尝试被确认失败后 | `payment_attempt_id` | `order_id`、`failed_at`、稳定失败分类 |
| 订单 | 首次支付成功 | `purchase` | 订单首次支付成功并完成成交状态落库后 | `order_id` | `paid_at`、成交金额、`currency` |
| 退款/售后 | 退款完成 | `refund` | 退款实际完成并落库后 | `refund_id` | `order_id`、`refunded_at`、退款金额、`currency`、退款明细（含 `order_item_id`、退款数量、行退款金额） |

规则：成交以订单系统首次支付成功为准；退款以退款完成为准；同一订单可有多次支付尝试和多次/部分退款。

## 2. 公共参数（所有后端事件统一携带）

事件没有对应值时传空值，不填充虚假默认值。

| 参数 | 含义 | 填写规则 |
|---|---|---|
| `event_id` | 本次事件记录的唯一 ID | 后端生成 UUID（推荐 UUIDv7；不支持时使用 UUIDv4）；创建后不可变。重试、补发、重新消费沿用原 ID，不重新生成 |
| `event_time` | 事件实际发生时间 | 使用服务端记录的业务时间，统一时区 |
| `user_id` | 已登录用户 ID | 登录用户填写；游客为空 |
| `anonymous_id` | 游客设备/浏览器 ID | 按接收到的原值保存；缺失为空 |
| `domain_userid` | Web 端埋点域用户 ID | 按接收到的原值保存，不自行生成或合并 |
| `origin_session_id` | 产生订单链路的访问会话 ID | 正常 Web Checkout 不得缺失；非 Web 场景可为空，但必须能识别该例外 |
| `market_id` / `market_code` | 业务所属市场 | 使用订单或业务系统确认的市场值 |
| `promotions[]` | 订单实际生效的全部优惠/营销码 | 手动输入、推广链接自动应用、用户组自动优惠，只要最终生效都记录；没有时为空数组或省略。每项包含 `promotion_id`（有则记录）、`promotion_code`、`discount_amount`、`currency` |
| `order_id` | 订单 ID | 订单相关事件必须填写；无订单事件为空 |

商品名称、图片等展示信息通过 `listing_public_code` 关联商品/Listing 维表，不要求事件重复携带。

`anonymous_id` 必须从当前 HttpOnly `looply_anonymous_id` 取得；缺失时保持为空，不得用 `domain_userid` 复制填充。`domain_userid` 和 `anonymous_id` 必须按实际值分别保存，不自动合并不同 `user_id`。

优惠字段规则：订单使用多个优惠/营销码时，`promotions[]` 全部记录；当前不判断是社媒码、普通优惠码还是用户组优惠，也不判断是手动输入还是自动应用。优惠码只作为订单归因辅助信息，不能单独认定渠道来源。

## 3. 字段使用原则

- `event_id` 用于事件记录幂等和去重；`order_id`、`payment_attempt_id`、`refund_id` 用于识别业务对象。
- 后端事件必须来自订单、支付、退款/售后业务事实，不用分析平台聚合数据代替。
- 支付失败只保存稳定的业务失败分类，不保存支付机构原始错误文本。
- 客户端不自行确认成交、不计算成交或退款金额；前端如何把上下文传给后端由开发决定。
- 售后过程（不等同于退款事件）需保留售后单 ID、`order_id`、涉及的 `order_item_id`、当前状态、处理结果，以及申请、受理、取消、结案时间或状态变更记录。
- 无法取得的字段保持为空，不补造默认值；订单归因上下文可以放在订单表，也可以放在以 `order_id` 为唯一键的关联表。
