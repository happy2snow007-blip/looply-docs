# G3｜Afterpay 与 Affirm C 端原型设计方案

> 日期：2026-10-27  
> 当前关卡：G3 原型与 UI  
> 适用范围：美国站、USD、一次性订单  
> 设计基线：现有 PC／移动端 Checkout、V1.7 待付款订单详情  
> 明确范围决定：**本期不修改订单支付系统流程图，继续引用 V3.1。**

## 1. 设计目标

面向美国站买家，在不改变现有下单与订单状态模型的前提下，将 Afterpay、Affirm 加入现有支付方式选择，并把外部支付的成功、明确失败／取消、结果未知三类结果清楚落回 Looply。

用户的核心任务只有三个：

1. 在符合基础条件时看见并选择 Afterpay 或 Affirm。
2. 明白点击 Pay Now 后会前往支付服务商完成资格确认和付款。
3. 返回 Looply 后明确知道支付成功、可以重试，还是仍在确认中且不可重复付款。

## 2. 设计方向与方案取舍

### 方案 A｜增量扩展现有支付组件（采用）

- 在现有 Credit Card、PayPal、Klarna 列表中新增 Afterpay、Affirm。
- 复用现有单选、选中态、跳转提示、Billing Address 和 Pay Now 交互。
- 复用 V1.7 订单详情的 Placed、Payment confirming、Paid 页面结构，只补充新支付方式名称、Logo 和专属提示。
- 不因新增渠道改变 Checkout 信息架构。

采用原因：本期是支付方式扩展，不是 Checkout 改版；该方案与“复用现有支付流程”“不修改系统流程图”的范围决定一致，也最利于降低开发和审核成本。

### 方案 B｜新增独立 BNPL 选择页（不采用）

会增加一次页面跳转，割裂现有支付方式列表，并产生新的返回、超时与埋点路径。

### 方案 C｜重做 Checkout 支付区（不采用）

能同时优化全部支付方式，但会把本期扩大为结算页改版，无法把风险限定在 Afterpay／Affirm 接入。

## 3. 视觉与内容原则

- 延续现有 Looply Checkout：浅色、克制、可信，主操作继续使用现有紫色品牌色。
- 支付方式自身只使用官方名称与官方 Logo，不用 Looply 自制图标替代正式上线资产。
- 不在 Looply 页面承诺固定期数、利率、每期金额或“必定获批”；最终资格和计划以渠道页面为准。
- 美国站固定文案使用英文；原型中的金额、商品和用户信息仅为示例。
- 不增加大面积营销信息，本期只提供完成选择所需的简短说明。

## 4. 页面矩阵

| 端 | 页面 | 必须覆盖的原型状态 | 本期变化 |
| --- | --- | --- | --- |
| PC | Checkout | 默认可选、Afterpay 选中、Affirm 选中、提交失败 | 支付列表新增两项；选中后展示跳转说明 |
| 移动端 | Checkout | 默认可选、Afterpay 选中、Affirm 选中、提交失败 | 与 PC 同规则，沿用移动端纵向列表与底部 Pay Now |
| PC | 待付款订单详情 | Placed 可重试、Payment confirming、Paid | 可用列表增加两项；确认中隐藏支付入口；成功后显示实际方式 |
| 移动端 | 待付款订单详情 | Placed 可重试、Payment confirming、Paid | 与 PC 同业务状态，按移动端现有布局适配 |

说明：金额、Market、币种或渠道能力不满足时，支付方式直接隐藏，不单独设计“不可用但置灰”状态。

## 5. Checkout 元素与交互

### 5.1 支付方式列表

现有支付方式相对顺序保持不变；Afterpay 排在 Affirm 之前，具体位置最终读取收单路由展示顺序。

每一项包含：

- Radio 单选；
- 官方 Logo；
- 官方名称；
- 简短类型说明，建议统一为 `Buy now, pay later`。

选中后，在该支付方式下方展示跳转说明：

- Afterpay：`You’ll be redirected to Afterpay to check your options and complete payment.`
- Affirm：`You’ll be redirected to Affirm to check your options and complete payment.`

说明中不用 `approved`、`guaranteed`、固定期数或固定分期金额。

### 5.2 展示与隐藏

- Afterpay：最终应付金额在 1–4,000 USD 且其他基础条件满足时展示。
- Affirm：最终应付金额在 35–30,000 USD 且其他基础条件满足时展示。
- 任何基础条件不满足：对应方式隐藏，不保留占位。
- 地址、优惠、运费或税费变化导致金额越过门槛：立即重新判断；若当前选中方式被隐藏，则清除选择，并提示 `Your order total changed. Please choose another payment method.`
- 点击 Pay Now 前服务端再次校验；校验失败时停留 Checkout，刷新可选方式并要求重新选择。

### 5.3 提交与跳转

- 点击 Pay Now 后按钮进入 Processing，阻止重复点击。
- 成功创建渠道会话后跳转外部页面。
- 会话创建失败或无法跳转：恢复 Pay Now，可继续选择其他方式；展示 `We couldn’t start this payment. Please try again or choose another payment method.`
- 已向渠道提交但结果不明确：不得按普通失败处理，不在 Checkout 开放第二次支付；进入订单详情 Payment confirming。

## 6. 订单详情状态

### 6.1 Placed｜可继续付款

- 显示支付剩余时间。
- 若上一尝试明确失败／取消，展示可理解的结果说明，不展示渠道内部错误码。
- 原支付方式仍可用时默认选中；也可切换到其他当前可用方式。
- Afterpay／Affirm 重新提交时，用户需重新完成渠道资格判断与付款确认。

建议文案：

- 明确失败：`Your payment wasn’t completed. Try again or choose another payment method.`
- 用户取消：`Payment was canceled. You can try again before the payment window closes.`

### 6.2 Payment confirming｜结果未知或处理中

- 页面主状态：`Payment confirming`。
- 隐藏所有支付方式与 Pay Now，不允许切换方式或再次付款。
- 显示原支付方式名称，以及“系统正在向支付服务商确认结果”的说明。
- 提供刷新结果入口；刷新不创建新支付尝试。
- 不展示“支付失败”或“请重新支付”。

建议文案：`We’re confirming your payment with {Afterpay/Affirm}. Please don’t try to pay again. This page will update when the result is available.`

### 6.3 Paid｜支付成功

- 沿用现有订单成功／订单详情结构。
- Payment method 显示实际支付方式：Afterpay 或 Affirm。
- 不在 Looply 推断或展示用户的具体分期计划；仅在渠道明确返回且现有数据模型已承载时显示。

## 7. 不在本期原型范围

- 产品详情页或购物车的分期营销信息；
- Afterpay／Affirm 外部页面；
- 多 Market 支付方式配置后台；
- Airwallex 密钥、商户账号或能力开关后台；
- 争议处理后台；
- 系统流程图修改；
- Checkout 整体信息架构或视觉改版。

## 8. 原型制作与评审门槛

原型按“同一可交互 HTML 内切换 PC／移动端和关键状态”制作，便于一次检查规则，不要求为所有金额组合复制静态页面。

出图前置：

- 官方 Logo 可先用清晰占位标识完成交互原型，但进入设计交付前必须替换为已核验的官方资产。
- 视觉完全沿用现有 Checkout 组件，不引入新的品牌风格。

G3 出关需要用户确认：

1. 支付方式在 Checkout 的位置和信息密度；
2. 选中后的跳转说明；
3. 金额变化导致方式隐藏并清空选择；
4. Placed 可重试与切换；
5. Payment confirming 禁止重复付款；
6. Paid 仅展示实际支付方式，不自行解释分期计划。

确认后进入 G3 原型制作；原型通过后再进入 G3.5 对齐，之后才定稿完整 PRD。
