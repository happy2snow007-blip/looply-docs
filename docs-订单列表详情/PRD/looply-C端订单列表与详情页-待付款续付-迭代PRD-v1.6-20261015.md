# Looply C 端订单列表与详情页｜待付款续付 · 迭代 PRD v1.6

> 日期：2026-10-15  
> 基线：C 端订单列表与详情页 PRD v1.5  
> 关联：订单支付待付款续付迭代 PRD V1.7、响应式交互原型 v1

## 1. 变更目标

把 `pending_payment` 订单详情从单一“去支付/确认中”入口升级为完整续付承载页：展示剩余支付时间、上一次结果、当前可用支付方式，并允许在安全条件下重试原方式或切换方式。

## 2. My Orders 列表

- 继续只在 All 中展示 `pending_payment`，状态标签仍为 `Placed`。
- 可继续支付：卡片展示剩余时间与 `Continue payment`。
- `processing / unknown`：展示 `Payment is being confirmed`，按钮为 `View order`，不出现再次支付动作。
- 同时存在多笔待付款订单时按原列表排序；全站提醒的默认目标使用最早到期订单，不使用“最新一笔”。
- 倒计时到零后立即刷新该卡片；普通到期转 Cancelled，风控审核中保持 Placed 并展示确认中。

## 3. 订单详情待付款支付区

### 3.1 通用结构

1. 状态标签：`Placed`。
2. 顶部状态提示：剩余时间或付款确认中。
3. 商品与订单摘要：继续读取父订单冻结快照和冻结金额。
4. Payment 区：待付款状态不展示 `Paid with`，改为支付方式选择器或确认中面板。

### 3.2 可支付状态

- 文案：`Complete payment within MM:SS to keep these items reserved.`
- 明确失败/取消时追加一条买家可理解的结果，不展示渠道错误码。
- 默认选择上一次支付方式；不可用时选择当前列表第一项，并说明原方式当前不可用。
- 支付方式按 Market、币种、设备、浏览器、渠道路由实时过滤。
- 主按钮随方式变化：`Pay $X`、`Continue with PayPal`、`Continue with Klarna`、`Pay with Apple Pay`。
- 信用卡需重新填写卡号、有效期和 Security code，不回显敏感信息。
- 点击主按钮后立即禁用所有支付方式和按钮，等待服务端返回。

### 3.3 付款确认中

- 文案：`We’re confirming your payment. Please don’t pay again yet.`
- 隐藏方式选择器和支付按钮。
- 展示状态自动刷新，可提供不创建支付请求的 `Refresh status`。
- 用户可离开页面；再次进入仍按服务端状态渲染。

### 3.4 已到期

- 普通待付款订单切换为 Cancelled 变体。
- 文案说明支付窗口结束、商品预占已释放，并提供返回商品页检查库存的入口。
- 不允许恢复原订单支付，重新购买必须重新结算。

## 4. 各方式前端交互

| 方式 | 打开方式 | 明确取消/失败 | 结果未知 |
|---|---|---|---|
| Credit Card | 页面内嵌；必要时 3DS | 回详情可支付态 | 回详情确认中 |
| PayPal | 弹窗/跳转 | 回详情可支付态 | 回详情确认中 |
| Klarna | 跳转 | 回详情可支付态 | 先查单，确认中 |
| Apple Pay | 系统面板 | 回详情可支付态 | 回详情确认中 |

## 5. 全站待付款提醒

- 触发：用户从一笔仍有效的待付款订单详情主动离开。
- 首个后续站内页展示一次轻提示；随后 PC/APP 顶部展示紧凑横幅。
- 可支付文案：`Payment is still needed · MM:SS left`，动作 `Continue payment`。
- 确认中文案：`We’re confirming your payment`，动作 `View order`。
- 多笔时：`You have N orders waiting for payment`，主动作打开最早到期订单，并提供查看全部待付款订单入口。
- 用户可关闭；关闭后本会话不再主动出现。My Orders 待付款标识不受影响。
- 在另一笔 Checkout、支付验证页、支付结果页不展示竞争性的 `Continue payment`。
- 成功、取消或到期后立即撤下。

## 6. 游客访问

- Checkout 静默创建账户后，当前浏览器获得可访问该父订单的临时登录态。
- 快速失败或取消直接进入订单详情，不得先要求设置密码。
- 临时态失效或跨设备访问时，使用邮箱验证码或时效签名订单链接恢复。

## 7. 文案

| 场景 | 文案 |
|---|---|
| 卡被拒 | `Your card was declined. Try this card again or choose another payment method.` |
| PayPal 取消 | `PayPal payment was cancelled. You can try again or choose another payment method.` |
| Klarna 拒绝 | `Klarna couldn’t approve this payment. Choose another payment method or try again.` |
| Apple Pay 取消 | `Apple Pay was cancelled. You can try again or choose another payment method.` |
| 通用未知 | `We’re confirming your payment. Please don’t pay again yet.` |
| 已到期 | `This order is no longer available for payment. The reserved items were released.` |

语气使用陈述句，不用感叹号，不用 `Sorry / Oops`。

## 8. 验收标准

1. PC 与 APP 的状态、可用动作和文案一致。
2. 明确失败时原方式默认选中，切换方式后主按钮与输入区正确变化。
3. `processing / unknown` 时页面不存在任何可创建新支付的入口。
4. 刷新、返回、切换方式不重置倒计时。
5. 横幅倒计时和订单详情使用同一服务端截止时间，偏差不超过 1 秒刷新周期。
6. 横幅关闭频控、支付终态撤下、多订单最早到期跳转符合规则。
7. 键盘可操作支付方式；状态与错误不只依赖颜色表达；倒计时变化不频繁打断读屏。

