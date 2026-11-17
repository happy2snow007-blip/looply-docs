# Looply 支付渠道对接集成说明 v1.1｜待付款续付增量

> 本文仅定义 v1.0 的续付增量；退款与商户配置沿用 v1.0。  
> ER 不修改；同一 `payment_order` 通过多条 `payment_transaction` 承载多次尝试。

## 1. 接口职责

新增/调整三个支付服务能力：

1. 查询订单当前是否允许创建新尝试；
2. 在同一支付单下创建一次支付尝试并返回渠道启动参数；
3. 统一查单，将渠道状态归一为 `succeeded / explicit_failed / explicit_closed / processing / unknown`。

## 2. 创建尝试的原子校验

服务端在订单维度串行执行：校验父订单待付款 → 校验未到 `payment_deadline` → 查询并收敛上一活跃尝试 → 校验无活跃尝试 → 重校验方式路由与金额 → 创建 `payment_transaction` → 创建渠道单。

渠道单创建失败时，本次流水标记失败并保留原因，不得留下可被误认为活跃的空尝试。

## 3. 渠道映射

| 渠道结果 | 归一结果 | 是否开放新尝试 |
|---|---|---|
| PayPal capture COMPLETED | succeeded | 否 |
| PayPal buyer cancel / capture DECLINED | explicit_closed / explicit_failed | 是 |
| PayPal PENDING / 无可靠回跳结果 | processing / unknown | 否，先查单 |
| Airwallex SUCCEEDED | succeeded | 否 |
| Airwallex FAILED | explicit_failed | 是 |
| Airwallex CANCELLED，且渠道确认不可继续 | explicit_closed | 是 |
| REQUIRES_CUSTOMER_ACTION / 渠道处理中 | processing | 否 |
| 网络异常且未取得终态 | unknown | 否，先查单 |

## 4. 方式专项

- PayPal `INSTRUMENT_DECLINED` 优先在同一 PayPal Order 中执行 `actions.restart()`；退出 PayPal 后再次选择才创建新 Looply 流水与新 PayPal Order。
- Credit Card 3DS 明确失败/取消可结束尝试；授权后超时必须查 Airwallex PaymentIntent。
- Klarna 未回跳不等于失败；必须 Retrieve 后才能开放切换。
- Apple Pay 面板未授权即取消可关闭；已授权后网络异常按 unknown 处理。

## 5. 幂等与冲突

- 创建尝试：`parent_order_id + client_request_id` 幂等。
- Webhook：沿用渠道 event/capture/intent ID 去重。
- 成功优先：任一交易成功后，支付单和父订单只允许完成一次；其他渠道单按能力关闭或仅拒绝后续确认。
- 同时到达“创建新尝试”和“上一笔成功回调”时，以数据库事务内重新读取订单状态为准；已支付则创建请求失败。

## 6. 到期处理

- 普通 pending/failed/closed/unknown：到期停止新尝试，关闭支付单并通知订单取消。
- 只有渠道明确返回风控审核中的 processing 可保留超过 30 分钟；72 小时后主动查单，仍无终态则保留 processing、写入备注并通知运营。
- 不得把普通网络错误、回跳丢失或前端超时升级为 72 小时占用库存。

