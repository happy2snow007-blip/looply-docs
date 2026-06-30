# Looply 支付渠道对接集成说明文档 V1.0

> PayPal + Airwallex (Credit Card / Klarna / Apple Pay) 全渠道支付 & 退款技术方案
>
> Version 1.0 · 2026-06-26 · 面向：前端 / 后端开发

## 1. 支付架构总览


### 1.1 支付渠道矩阵


Looply Checkout 页面提供 4 种支付方式，分别通过 PayPal 和 Airwallex 两个支付渠道完成：


| 支付方式 | 对接渠道 | 前端组件 | 用户体验 | 支持币种 |
| --- | --- | --- | --- | --- |
| **PayPal** | PayPal | PayPal JS SDK Button | 弹窗/跳转到 PayPal 登录并支付 | USD |
| **Credit Card** | Airwallex | Airwallex Drop-in Element | 页面内嵌卡号输入框，无跳转 | USD |
| **Klarna** | Airwallex | Airwallex Drop-in Element | 跳转到 Klarna 完成支付 | USD |
| **Apple Pay** | Airwallex | Airwallex Drop-in Element | 系统级 Apple Pay 弹窗（仅 Safari/iOS） | USD |


>
> **为什么 Credit Card 走 Airwallex 而不走 PayPal？**
>
> PayPal 的信用卡通道（ACDC）需要 PayPal 商家账号审核且费率较高。Airwallex 作为独立收单渠道，费率更优、支持 3DS 验证、且可同时接入 Klarna 和 Apple Pay，一个 Drop-in 组件覆盖三种支付方式。


### 1.2 系统架构图


### 1.3 核心设计原则

1. **以 Webhook 为准**：前端回调仅用于页面跳转提示，订单状态变更必须以 Webhook 通知为最终依据
2. **幂等处理**：所有 Webhook handler 和支付回调都必须支持幂等，防止重复处理
3. **统一抽象**：Looply 后端 Payment Service 统一封装 PayPal / Airwallex 的差异，Order Service 只关心 payment_order 的最终状态（succeeded / failed）
4. **支付成功即创建订单**：用户点击支付按钮时，Looply 先创建 payment_order（status = pending），支付成功后（payment_order.status = succeeded）才创建 parent_order + order（order_status = paid）


## 2. PayPal 支付集成


### 2.1 PayPal 支付时序图


用户选择 PayPal 支付后，点击 "Pay with PayPal" 按钮，完整流程如下：


>
> **异步补偿机制**：如果步骤 ⑨ Capture 返回 `status: "PENDING"`（如 eCheck），payment_order 保持 pending，不能创建订单。需等待 Webhook 最终确认（时序图中"异步补偿"部分）。


### 2.2 前端集成（PayPal JS SDK）


#### 加载 SDK


```
<!-- 在 Checkout 页面 head 或 body 末尾加载 -->
<script src="https://www.paypal.com/sdk/js?client-id={PAYPAL_CLIENT_ID}¤cy=USD"></script>
```


>
> `client-id` 从 PayPal Developer 后台的 REST APP 获取。Sandbox 和 Live 环境使用不同的 client-id。
>
> `currency=USD` 指定币种，与 Create Order 时传入的 currency 保持一致。


#### 渲染按钮 & 处理回调


```
// 当用户选择 PayPal 支付方式时，渲染 PayPal 按钮
paypal.Buttons({
  // 步骤 1-5：创建 PayPal 订单
  createOrder: async () => {
    const res = await fetch('/api/payment/paypal/create', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        cart_id: cartId,          // Looply 购物车 ID
        shipping_address: addr,   // 用户已填的收货地址
      }),
    });
    const data = await res.json();
    return data.paypal_order_id;  // 返回给 PayPal SDK
  },

  // 步骤 7-12：用户在 PayPal 确认支付后
  onApprove: async (data, actions) => {
    const res = await fetch('/api/payment/paypal/capture', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        paypal_order_id: data.orderID,
      }),
    });
    const result = await res.json();

    if (result.status === 'COMPLETED') {
      // 跳转到支付成功页
      window.location.href = `/order/${result.looply_order_id}/confirmation`;
    } else if (result.status === 'PENDING') {
      // eCheck 等异步支付，显示"支付处理中"
      window.location.href = `/order/${result.looply_order_id}/pending`;
    }
  },

  // 用户在 PayPal 弹窗中取消
  onCancel: () => {
    showToast('Payment cancelled. You can try again.');
  },

  // SDK 级错误（网络异常等）
  onError: (err) => {
    console.error('PayPal error:', err);
    showToast('Something went wrong. Please try again.');
  },
}).render('#paypal-button-container');
```


### 2.3 后端 API 对接


#### 2.3.1 获取 Access Token


所有 PayPal API 调用前需获取 Bearer Token（有效期约 9 小时，建议缓存复用）：


```
# Sandbox
POST https://api-m.sandbox.paypal.com/v1/oauth2/token
Authorization: Basic {Base64(CLIENT_ID:SECRET)}
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials

# Live
POST https://api-m.paypal.com/v1/oauth2/token
```


#### 2.3.2 创建 PayPal 订单


```
POST https://api-m.sandbox.paypal.com/v2/checkout/orders
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "intent": "CAPTURE",
  "purchase_units": [{
    "reference_id": "LOOPLY-ORD-20260626001",
    "amount": {
      "currency_code": "USD",
      "value": "129.99",
      "breakdown": {
        "item_total":    { "currency_code": "USD", "value": "109.99" },
        "shipping":      { "currency_code": "USD", "value": "15.00" },
        "tax_total":     { "currency_code": "USD", "value": "5.00" }
      }
    },
    "items": [{
      "name": "Pre-owned Gucci Bag",
      "quantity": "1",
      "unit_amount": { "currency_code": "USD", "value": "109.99" },
      "category": "PHYSICAL_GOODS"
    }],
    "shipping": {
      "name": { "full_name": "John Doe" },
      "address": {
        "address_line_1": "123 Main St",
        "admin_area_2": "San Francisco",
        "admin_area_1": "CA",
        "postal_code": "94105",
        "country_code": "US"
      }
    }
  }],
  "payment_source": {
    "paypal": {
      "experience_context": {
        "shipping_preference": "SET_PROVIDED_ADDRESS",
        "return_url": "https://looply.com/checkout/return",
        "cancel_url": "https://looply.com/checkout/cancel"
      }
    }
  }
}
```


>
> **Looply 二手商品均为实物**：`category` 固定传 `PHYSICAL_GOODS`，`shipping_preference` 传 `SET_PROVIDED_ADDRESS`（使用用户在 Looply 已填的地址，PayPal 页面不允许修改地址）。


#### 2.3.3 捕获支付（Capture）


```
POST https://api-m.sandbox.paypal.com/v2/checkout/orders/{paypal_order_id}/capture
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

// 请求体为空 {}
// 成功响应关键字段：
{
  "id": "PAY-xxx",
  "status": "COMPLETED",
  "purchase_units": [{
    "payments": {
      "captures": [{
        "id": "CAP-xxx",          // capture_id，退款时需要
        "status": "COMPLETED",
        "amount": { "currency_code": "USD", "value": "129.99" }
      }]
    }
  }]
}
```


| Capture 状态 | 含义 | Looply 处理 |
| --- | --- | --- |
| `COMPLETED` | 支付成功 | payment_order → succeeded，创建订单 (paid) |
| `PENDING` | 支付处理中（eCheck 等） | payment_order 保持 pending，等 Webhook 确认后再创建订单 |
| `DECLINED` | 支付被拒 | 提示用户更换支付方式 |


#### 2.3.4 错误处理：INSTRUMENT_DECLINED


```
// 在 onApprove 中，如果 Capture 返回 INSTRUMENT_DECLINED
if (result.error === 'INSTRUMENT_DECLINED') {
  // 调用 actions.restart() 让用户在 PayPal 中选择其他支付方式
  return actions.restart();
}
```


### 2.4 PayPal Webhook 处理


#### 需要监听的事件


| 事件名 | 触发时机 | Looply 处理 |
| --- | --- | --- |
| `PAYMENT.CAPTURE.COMPLETED` | Capture 成功（含异步成功） | payment_order.status → succeeded，创建订单（幂等：已 succeeded 则忽略） |
| `PAYMENT.CAPTURE.DENIED` | Capture 被拒（异步场景） | payment_order.status → failed，通知用户 |
| `PAYMENT.CAPTURE.PENDING` | Capture 进入待处理 | 记录日志，payment_order 保持 pending |
| `PAYMENT.CAPTURE.REFUNDED` | 退款完成 | refund_order.status → succeeded，更新 order_item.refund_status = refunded（见第 5 章退款流程） |


#### Webhook 端点实现


```
// POST /api/webhook/paypal
// 1. 验证 Webhook 签名（调用 PayPal Verify Webhook Signature API）
// 2. 解析事件

async function handlePayPalWebhook(event) {
  const eventType = event.event_type;
  const resource = event.resource;

  switch (eventType) {
    case 'PAYMENT.CAPTURE.COMPLETED':
      const captureId = resource.id;
      const paypalOrderId = resource.supplementary_data
        ?.related_ids?.order_id;
      // 通过 paypalOrderId 找到 Looply 订单，更新为 PAID
      await orderService.markAsPaid(paypalOrderId, {
        capture_id: captureId,
        channel: 'PAYPAL',
      });
      break;

    case 'PAYMENT.CAPTURE.DENIED':
      await orderService.markAsPaymentFailed(paypalOrderId);
      break;
  }
}
```


>
> **Webhook 签名验证必做**：使用 PayPal 的 `POST /v1/notifications/verify-webhook-signature` API 验证 Webhook 真实性，防止伪造通知。生产环境必须开启。


## 3. Airwallex 支付集成


Airwallex 使用 **PaymentIntent** 模型：后端创建 PaymentIntent，前端使用 Drop-in Element 收集支付信息并完成支付。Credit Card、Klarna、Apple Pay 共用同一个 Drop-in 组件。


### 3.1 Airwallex 支付时序图


>
> **Airwallex 与 PayPal 的关键差异**：Airwallex 的 Drop-in Element 自行处理支付确认（步骤 ⑦），不需要像 PayPal 那样由后端调用 Capture API。后端只需在收到 success 回调后，通过 Retrieve API 二次确认状态即可。


### 3.2 前端集成（Airwallex Drop-in Element）


#### 安装 SDK


```
# 方式一：npm 安装
npm install @airwallex/components-sdk

# 方式二：CDN 引入
<script src="https://static.airwallex.com/components/sdk/v1/index.js"></script>
```


#### 初始化 & 挂载 Drop-in


```
import { init, createElement } from '@airwallex/components-sdk';

// 用户点击 "Pay now" 后执行
async function handleAirwallexPayment(cartId, shippingAddr) {
  // 1. 请求后端创建 PaymentIntent
  const res = await fetch('/api/payment/airwallex/create', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ cart_id: cartId, shipping_address: shippingAddr }),
  });
  const { intent_id, client_secret, currency } = await res.json();

  // 2. 初始化 Airwallex SDK
  await init({
    env: 'demo',   // 生产环境改为 'prod'
    enabledElements: ['payments'],
  });

  // 3. 创建 Drop-in Element
  const element = await createElement('dropIn', {
    intent_id,
    client_secret,
    currency,
    // 可选：指定只展示特定支付方式
    // methods: ['card', 'klarna', 'applepay'],
  });

  // 4. 挂载到 DOM
  element.mount('airwallex-dropin-container');

  // 5. 事件监听
  element.on('ready', () => {
    // Drop-in 加载完成，隐藏 loading 态
    hideLoadingSpinner();
  });

  element.on('success', async () => {
    // 支付成功 - 通知后端确认并跳转
    const confirmRes = await fetch('/api/payment/airwallex/confirm', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ intent_id }),
    });
    const result = await confirmRes.json();
    window.location.href = `/order/${result.looply_order_id}/confirmation`;
  });

  element.on('error', (event) => {
    // 支付失败 - 展示错误信息，用户可重试
    showToast(event.detail?.message || 'Payment failed. Please try again.');
  });
}
```


#### HTML 容器


```
<!-- Checkout 页面中，当用户选择 Credit Card / Klarna / Apple Pay 时展示 -->
<div id="airwallex-dropin-container"></div>
```


### 3.3 后端 API 对接


#### 3.3.1 获取 Access Token


```
# Sandbox
POST https://api-demo.airwallex.com/api/v1/authentication/login
Content-Type: application/json
x-api-key: {YOUR_SANDBOX_API_KEY}
x-client-id: {YOUR_SANDBOX_CLIENT_ID}

# 响应
{
  "token": "eyJhbGciOi...",
  "expires_at": "2026-06-26T12:00:00Z"
}

# Live
POST https://api.airwallex.com/api/v1/authentication/login
```


>
> **安全要求**：`x-api-key` 和 `x-client-id` 仅在服务端使用，绝不能暴露到前端代码或客户端。


#### 3.3.2 创建 PaymentIntent


```
POST https://api-demo.airwallex.com/api/v1/pa/payment_intents/create
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "request_id": "looply-pay-20260626-001",    // 幂等键，建议用 UUID
  "amount": 129.99,                        // 注意：Airwallex 用实际金额，不是分
  "currency": "USD",
  "merchant_order_id": "LOOPLY-ORD-20260626001",
  "return_url": "https://looply.com/order/LOOPLY-ORD-20260626001/result",
  "metadata": {
    "looply_order_id": "LOOPLY-ORD-20260626001",
    "user_id": "USR-12345"
  }
}

// 响应
{
  "id": "int_hkdm1234567890",
  "request_id": "looply-pay-20260626-001",
  "amount": 129.99,
  "currency": "USD",
  "merchant_order_id": "LOOPLY-ORD-20260626001",
  "status": "REQUIRES_PAYMENT_METHOD",
  "client_secret": "int_hkdm1234567890_abcdefg",  // 传给前端
  "created_at": "2026-06-26T10:00:00+0000"
}
```


>
> **金额单位**：Airwallex 金额使用主货币单位（如 10.99 = $10.99），与 Stripe 的分单位（1099）不同。
>
> **return_url**：Klarna 等需要跳转的支付方式会在完成后重定向到此 URL。


#### 3.3.3 查询 PaymentIntent 状态


```
GET https://api-demo.airwallex.com/api/v1/pa/payment_intents/{intent_id}
Authorization: Bearer {ACCESS_TOKEN}

// 检查 status 字段
{
  "id": "int_hkdm1234567890",
  "status": "SUCCEEDED",         // 支付成功
  "latest_payment_attempt": {
    "payment_method": "card",    // 实际使用的支付方式
    "id": "att_xxx"               // payment_attempt_id，退款时可能需要
  }
}
```


| PaymentIntent 状态 | 含义 | Looply 处理 |
| --- | --- | --- |
| `REQUIRES_PAYMENT_METHOD` | 等待用户输入支付信息 | 前端展示 Drop-in |
| `REQUIRES_CUSTOMER_ACTION` | 需要 3DS 验证 / Klarna 跳转 | SDK 自动处理 |
| `SUCCEEDED` | 支付成功 | payment_order → succeeded，创建订单 (paid) |
| `REQUIRES_CAPTURE` | 预授权成功，待捕获 | Looply 当前不使用预授权 |
| `CANCELLED` | 已取消 | payment_order → closed |


### 3.4 Airwallex Webhook 处理


#### 需要监听的事件


| 事件名 | 触发时机 | Looply 处理 |
| --- | --- | --- |
| `payment_intent.succeeded` | PaymentIntent 支付成功 | payment_order.status → succeeded，创建订单（幂等） |
| `payment_attempt.authorized` | 支付授权成功 | 记录日志（Looply 用自动捕获模式，后续会收到 succeeded） |
| `payment_attempt.payment_failed` | 支付失败 | payment_order.status → failed |
| `refund.succeeded` | 退款成功 | refund_order.status → succeeded，更新 order_item.refund_status = refunded（见第 5 章） |
| `refund.failed` | 退款失败 | 退款单标记失败，通知运营人员 |


#### Webhook 签名验证


```
// POST /api/webhook/airwallex
// Airwallex Webhook 签名验证

function verifyAirwallexWebhook(req) {
  const timestamp = req.headers['x-timestamp'];   // Unix 毫秒时间戳
  const signature = req.headers['x-signature'];   // HMAC-SHA256 签名
  const rawBody = req.rawBody;                     // 原始请求体（未解析）

  // 拼接待签名字符串：timestamp + rawBody
  const valueToDigest = timestamp + rawBody;

  // 使用 Webhook Secret 计算 HMAC-SHA256
  const hmac = crypto.createHmac('sha256', AIRWALLEX_WEBHOOK_SECRET);
  const computedSignature = hmac.update(valueToDigest).digest('hex');

  return computedSignature === signature;
}

// 事件处理
async function handleAirwallexWebhook(event) {
  const { name, data } = event;

  switch (name) {
    case 'payment_intent.succeeded':
      const intentId = data.object.id;
      const merchantOrderId = data.object.merchant_order_id;
      await orderService.markAsPaid(merchantOrderId, {
        intent_id: intentId,
        channel: 'AIRWALLEX',
        payment_method: data.object.latest_payment_attempt?.payment_method,
      });
      break;

    case 'payment_attempt.payment_failed':
      await orderService.markAsPaymentFailed(merchantOrderId);
      break;

    case 'refund.succeeded':
      await refundService.markRefundSucceeded(data.object.id);
      break;
  }
}
```


>
> **关键**：验证签名时必须使用**原始请求体**（raw body），不能重新序列化 JSON。Express 中需配置 `express.raw()` 或 `bodyParser.raw()` 来获取 raw body。


### 3.5 Apple Pay 额外配置


Apple Pay 需要完成以下前置配置才能在 Drop-in 中展示：


| 步骤 | 说明 | 负责方 |
| --- | --- | --- |
| 1. 注册 Apple Developer | 需要 Apple Developer 账号（$99/年） | 运营 / 管理员 |
| 2. 创建 Merchant ID | 在 Apple Developer 后台创建 Merchant Identifier | 后端开发 |
| 3. 域名验证 | 在 Airwallex Dashboard 上传 Apple 域名验证文件到 `/.well-known/apple-developer-merchantid-domain-association` | 后端开发 / 运维 |
| 4. Airwallex 配置 | 在 Airwallex Dashboard → Payment Methods 中启用 Apple Pay 并配置证书 | 运营 / 后端开发 |


>
> **展示条件**：Apple Pay 按钮仅在支持 Apple Pay 的设备（Safari / iOS）上展示，Drop-in Element 会自动检测并隐藏不支持的支付方式。无需前端额外判断。


## 4. Checkout 页面前端组件


### 4.1 支付方式选择器


根据用户提供的 UI 设计稿，Checkout 页面的 Payment 区域展示 4 种支付方式（Radio 单选），选中后展示对应的支付组件：


| Radio 选项 | 选中后展示 | 按钮文案 | 组件来源 |
| --- | --- | --- | --- |
| Credit card (VISA / MC / AMEX + 5) | Airwallex Drop-in（Card 输入框：Card number / Expiration / Security code / Name on card） | **Pay now** | Airwallex Drop-in Element |
| PayPal PayPal | 提示文案："You'll be redirected to PayPal to complete your purchase" | **Pay with PayPal** | PayPal JS SDK Button |
| Klarna Klarna | Airwallex Drop-in（Klarna 支付区域） | **Pay now** | Airwallex Drop-in Element |
| Apple Pay  Pay | Airwallex Drop-in（Apple Pay 按钮） | **Pay now** | Airwallex Drop-in Element |


### 4.2 按钮状态 & 文案映射


| 选中的支付方式 | 按钮文案 | 按钮颜色 | 点击行为 |
| --- | --- | --- | --- |
| Credit Card | Pay now | 品牌紫 #6C5CE7 | 触发 Airwallex Drop-in 提交 |
| PayPal | Pay with PayPal | PayPal 蓝 #003087 | 触发 PayPal JS SDK createOrder |
| Klarna | Pay now | 品牌紫 #6C5CE7 | 触发 Airwallex Drop-in 提交 |
| Apple Pay | Pay now | 品牌紫 #6C5CE7 | 触发 Airwallex Drop-in 提交 |


### 4.3 组件挂载逻辑


```
// Checkout 页面支付方式切换逻辑

const PAYMENT_METHOD = {
  CREDIT_CARD: 'credit_card',
  PAYPAL: 'paypal',
  KLARNA: 'klarna',
  APPLE_PAY: 'apple_pay',
};

// Airwallex 类型的支付方式共用一个 Drop-in，PayPal 使用独立 SDK
const AIRWALLEX_METHODS = [
  PAYMENT_METHOD.CREDIT_CARD,
  PAYMENT_METHOD.KLARNA,
  PAYMENT_METHOD.APPLE_PAY,
];

let currentMethod = null;
let airwallexElement = null;
let paypalButtonRendered = false;

function onPaymentMethodChange(method) {
  currentMethod = method;

  // 切换 UI 显隐
  document.getElementById('paypal-button-container').style.display =
    method === PAYMENT_METHOD.PAYPAL ? 'block' : 'none';
  document.getElementById('airwallex-dropin-container').style.display =
    AIRWALLEX_METHODS.includes(method) ? 'block' : 'none';

  // 更新按钮文案
  const payBtn = document.getElementById('pay-button');
  if (method === PAYMENT_METHOD.PAYPAL) {
    payBtn.textContent = 'Pay with PayPal';
    payBtn.style.background = '#003087';
    payBtn.style.display = 'none'; // PayPal 用自己的按钮
  } else {
    payBtn.textContent = 'Pay now';
    payBtn.style.background = '#6C5CE7';
    payBtn.style.display = 'block';
  }

  // 延迟初始化 PayPal 按钮（只渲染一次）
  if (method === PAYMENT_METHOD.PAYPAL && !paypalButtonRendered) {
    renderPayPalButton();
    paypalButtonRendered = true;
  }
}

// 点击 "Pay now" 按钮
async function onPayNowClick() {
  if (AIRWALLEX_METHODS.includes(currentMethod)) {
    await handleAirwallexPayment(cartId, shippingAddr);
  }
  // PayPal 有自己的按钮，不走这里
}
```


## 5. 退款流程


### 5.1 退款系统流程


按照 v8.0 状态设计，退款分为两个阶段：**业务审批**（refund_request）和**资金退回**（refund_order），两者通过单号松耦合。


### 5.2 PayPal 退款 API


```
# 对已捕获的交易发起退款（capture_id 在 Capture 响应中获取）
POST https://api-m.sandbox.paypal.com/v2/payments/captures/{capture_id}/refund
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

// 全额退款：body 为空 {}

// 部分退款：
{
  "amount": {
    "value": "50.00",
    "currency_code": "USD"
  },
  "note_to_payer": "Refund for returned item"
}

// 响应
{
  "id": "REFUND-xxx",
  "status": "COMPLETED",     // 或 "PENDING"
  "amount": {
    "value": "50.00",
    "currency_code": "USD"
  }
}
```


| 退款状态 | 含义 | Looply 处理 |
| --- | --- | --- |
| `COMPLETED` | 退款即时成功 | refund_order.status → succeeded，更新 order_item.refund_status = refunded |
| `PENDING` | 退款处理中（eCheck 等） | refund_order 保持 pending，等待 Webhook `PAYMENT.CAPTURE.REFUNDED` |
| `CANCELLED` | 退款被取消 | 退款记录标记 FAILED，通知运营 |


### 5.3 Airwallex 退款 API


```
# 对 PaymentIntent 发起退款
POST https://api-demo.airwallex.com/api/v1/pa/refunds/create
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "request_id": "looply-refund-20260626-001",   // 幂等键
  "payment_intent_id": "int_hkdm1234567890",
  "amount": 50.00,                            // 部分退款金额
  "reason": "Buyer requested return",
  "metadata": {
    "looply_refund_id": "RFD-20260626001"
  }
}

// 全额退款：amount 不传或传原金额

// 响应
{
  "id": "ref_hkdm9876543210",
  "request_id": "looply-refund-20260626-001",
  "payment_intent_id": "int_hkdm1234567890",
  "amount": 50.00,
  "currency": "USD",
  "status": "SUCCEEDED"           // 或 "CREATED" / "PENDING"
}
```


| 退款状态 | 含义 | Looply 处理 |
| --- | --- | --- |
| `SUCCEEDED` | 退款即时成功 | 退款记录标记 SUCCESS |
| `CREATED` | 退款已创建，处理中 | 等待 Webhook `refund.succeeded` |
| `PENDING` | 退款处理中 | 等待 Webhook |
| `FAILED` | 退款失败 | 退款记录标记 FAILED，通知运营 |


### 5.4 退款 Webhook 事件


| 渠道 | 事件 | 触发时机 | Looply 处理 |
| --- | --- | --- | --- |
| PayPal | `PAYMENT.CAPTURE.REFUNDED` | 退款完成 | refund_order.status → succeeded，更新 order_item.refund_status = refunded |
| Airwallex | `refund.succeeded` | 退款成功 | refund_order.status → succeeded，更新 order_item.refund_status = refunded |
| Airwallex | `refund.failed` | 退款失败 | 更新退款记录为 FAILED，通知运营 |


>
> **退款到账时间参考**：PayPal 余额退款一般即时到账；信用卡退款 5-10 个工作日；Klarna 退款 5-7 个工作日。退款时间由支付渠道和用户银行共同决定，Looply 无法控制。


## 6. 订单状态映射


以下状态设计严格参照《looply 订单模块状态设计说明 v8.0》，采用分层状态模型。支付对接只涉及其中两层：**支付层**（payment_order / refund_order）和**订单核心层**（order 创建触发）。


### 6.1 Looply 分层状态模型（支付相关）


#### 支付层：payment_order.status（4 个值）


用户点击「去支付」时创建 payment_order，跳转支付网关。支付前的状态由 checkout_session 承载。


| 枚举值 | 中文 | 说明 |
| --- | --- | --- |
| `pending` | 待支付 | 已跳转支付网关，等待支付结果 |
| `succeeded` | 成功 | 支付回调确认成功，触发创建 parent_order + order |
| `failed` | 失败 | 支付网关返回失败（余额不足、风控拒绝等） |
| `closed` | 超时关闭 | 超过 expired_at 未完成支付 |


#### 订单层：order.order_status（4 个值）


订单在 payment_order succeeded 后才创建，起始状态即 `paid`，**无 pending_payment 状态**。


#### 退款层：refund_order.status（3 个值）


退款审批通过（refund_request.approval_status = approved）后，在支付域创建 refund_order 执行资金退回。


| 枚举值 | 中文 | 说明 |
| --- | --- | --- |
| `pending` | 退款中 | 已发起退款，等待渠道确认 |
| `succeeded` | 退款成功 | 渠道确认退款到账，累加 payment_order.refunded_amount |
| `failed` | 退款失败 | 渠道返回失败，需人工介入或重试 |


>
> **退款不改订单生命周期**：退款进度在商品级跟踪（order_item.refund_status: none → refunding → refunded），不影响 order.order_status。订单级无 REFUNDED / PARTIALLY_REFUNDED 状态，退款维度从 order_item 实时聚合。


### 6.2 支付渠道状态 → Looply 状态映射表


#### PayPal → payment_order.status


| PayPal 状态 / 事件 | payment_order.status | 后续动作 |
| --- | --- | --- |
| Order Created（createOrder 返回） | `pending` | 等待用户在 PayPal 弹窗中确认 |
| Capture: COMPLETED | `succeeded` | 创建 parent_order + order（order_status = paid） |
| Capture: PENDING | `pending` | 保持待支付，等 Webhook 最终确认 |
| Capture: DECLINED | `failed` | 提示用户支付失败，可重试（创建新 payment_order） |
| Webhook: PAYMENT.CAPTURE.COMPLETED | `succeeded` | 幂等：已 succeeded 则忽略，未处理则创建订单 |
| Webhook: PAYMENT.CAPTURE.DENIED | `failed` | 更新状态，通知用户 |


#### PayPal → refund_order.status


| PayPal 状态 / 事件 | refund_order.status | 后续动作 |
| --- | --- | --- |
| Refund API: COMPLETED | `succeeded` | 累加 payment_order.refunded_amount，更新 order_item.refund_status = refunded |
| Refund API: PENDING | `pending` | 等 Webhook 最终确认 |
| Webhook: PAYMENT.CAPTURE.REFUNDED | `succeeded` | 幂等确认退款到账 |


#### Airwallex → payment_order.status


| Airwallex 状态 / 事件 | payment_order.status | 后续动作 |
| --- | --- | --- |
| PaymentIntent 创建 | `pending` | 等待前端 Drop-in 组件完成支付 |
| PaymentIntent: REQUIRES_PAYMENT_METHOD | `pending` | 等待用户输入支付信息 |
| PaymentIntent: REQUIRES_CUSTOMER_ACTION | `pending` | 3DS 验证中 / Klarna 跳转中 |
| PaymentIntent: SUCCEEDED | `succeeded` | 创建 parent_order + order（order_status = paid） |
| PaymentIntent: CANCELLED | `closed` | 支付取消，checkout_session 保持 pending 可重试 |
| Webhook: payment_intent.succeeded | `succeeded` | 幂等：已 succeeded 则忽略，未处理则创建订单 |
| Webhook: payment_attempt.payment_failed | `failed` | 更新状态，通知用户 |


#### Airwallex → refund_order.status


| Airwallex 状态 / 事件 | refund_order.status | 后续动作 |
| --- | --- | --- |
| Refund API: RECEIVED / PENDING | `pending` | 退款已受理，等待渠道处理 |
| Refund API: SUCCEEDED | `succeeded` | 累加 payment_order.refunded_amount，更新 order_item.refund_status = refunded |
| Webhook: refund.succeeded | `succeeded` | 幂等确认退款到账 |
| Webhook: refund.failed | `failed` | 需人工介入或重试 |


>
> **支付成功 = 创建订单**：payment_order.status 变为 succeeded 时，同步完成：checkout_session.checkout_status → converted + 创建 parent_order + order（order_status = paid）。支付失败时 checkout_session 保持 pending，用户可重试（创建新的 payment_order）。
>
> **超额退款防护**：创建 refund_order 前校验 payment_order.refunded_amount + 本次退款 ≤ payment_order.amount。


## 7. 错误处理 & 异常场景


| 异常场景 | 触发条件 | 处理策略 |
| --- | --- | --- |
| **用户关闭支付弹窗** | PayPal 弹窗关闭 / 页面刷新 | payment_order 保持 pending，超时后自动关闭（payment_order.status → closed） |
| **支付成功但前端回调未执行** | 网络中断、用户关闭页面 | Webhook 兜底更新 payment_order 状态并创建订单，不依赖前端回调 |
| **重复支付** | 用户多次点击支付按钮 | 前端：点击后禁用按钮。后端：PayPal 同一 order_id 只能 Capture 一次；Airwallex 使用 request_id 幂等 |
| **3DS 验证失败** | 信用卡 3DS 挑战未通过 | Airwallex Drop-in 自动处理 3DS 流程，失败会触发 error 事件，提示用户重试 |
| **Webhook 重复投递** | 支付渠道重试 | 所有 handler 幂等处理：通过 event_id 或 capture_id/intent_id 去重 |
| **Webhook 签名验证失败** | 伪造请求 / Secret 配置错误 | 返回 400，记录告警日志，不处理 |
| **退款超出可退金额** | 运营输入退款金额 > 已付金额 - 已退金额 | 后端校验并拒绝，提示最大可退金额 |
| **PayPal INSTRUMENT_DECLINED** | 用户 PayPal 绑定的支付方式余额不足 / 被拒 | 前端调用 `actions.restart()` 让用户在 PayPal 中选择其他支付方式 |
| **Airwallex Token 过期** | Access Token 超过有效期 | 后端实现 Token 刷新机制，过期前自动重新获取 |
| **Klarna 跳转后未完成** | 用户在 Klarna 页面放弃 | Klarna 超时后自动取消，Webhook 通知 payment_failed |


## 8. 前置准备清单


### 8.1 PayPal


| 事项 | 说明 | 负责人 | 状态 |
| --- | --- | --- | --- |
| 注册 PayPal Business 账号 | 在 PayPal.cn 注册跨境收付款商家账号 | 运营 | 待完成 |
| 创建 REST APP | 在 PayPal Developer 后台创建 APP，获取 Client ID 和 Secret | 后端开发 | 待完成 |
| 创建 Sandbox 测试账号 | 创建 Business（商家）和 Personal（买家）测试账号 | 后端开发 | 待完成 |
| 配置 Webhook | 在 Developer 后台配置 Webhook URL 和事件订阅 | 后端开发 | 待完成 |


### 8.2 Airwallex


| 事项 | 说明 | 负责人 | 状态 |
| --- | --- | --- | --- |
| 注册 Airwallex 商家账号 | 在 airwallex.com 注册商家账号并完成 KYC 审核 | 运营 | 待完成 |
| 获取 API Key | 在 Airwallex Dashboard → API Keys 获取 Client ID 和 API Key | 后端开发 | 待完成 |
| 开通支付方式 | 在 Dashboard → Payment Methods 中启用 Card、Klarna、Apple Pay | 运营 | 待完成 |
| 配置 Webhook | 在 Dashboard → Webhooks 配置通知 URL 和事件订阅 | 后端开发 | 待完成 |
| Apple Pay 域名验证 | 上传 Apple 域名验证文件到网站根目录 | 后端 / 运维 | 待完成 |
| Apple Developer 账号 | 注册 Apple Developer Program（$99/年） | 运营 | 待完成 |


## 9. 环境配置 & 测试


### 9.1 环境变量


```
# === PayPal ===
PAYPAL_CLIENT_ID=<sandbox-client-id>
PAYPAL_SECRET=<sandbox-secret>
PAYPAL_API_BASE=https://api-m.sandbox.paypal.com   # 生产: https://api-m.paypal.com
PAYPAL_WEBHOOK_ID=<webhook-id>

# === Airwallex ===
AIRWALLEX_CLIENT_ID=<sandbox-client-id>
AIRWALLEX_API_KEY=<sandbox-api-key>
AIRWALLEX_API_BASE=https://api-demo.airwallex.com  # 生产: https://api.airwallex.com
AIRWALLEX_WEBHOOK_SECRET=<webhook-secret>
AIRWALLEX_ENV=demo                                  # 生产: prod
```


### 9.2 测试卡号


#### PayPal Sandbox


使用 PayPal Developer 后台创建的 Personal Sandbox 账号登录测试。


#### Airwallex Sandbox 测试卡


| 场景 | 卡号 | 有效期 | CVV |
| --- | --- | --- | --- |
| 支付成功 | `4242 4242 4242 4242` | 任意未来日期 | 任意 3 位 |
| 支付成功（需 3DS） | `4000 0000 0000 3220` | 任意未来日期 | 任意 3 位 |
| 支付拒绝 | `4000 0000 0000 0002` | 任意未来日期 | 任意 3 位 |


### 9.3 Webhook 本地调试


本地开发时无法接收外部 Webhook，推荐使用 ngrok 或 Airwallex CLI 进行调试：


```
# 使用 ngrok 暴露本地端口
ngrok http 3000

# 将 ngrok 生成的 URL 配置到 PayPal / Airwallex Webhook 设置中
# 例如: https://abc123.ngrok.io/api/webhook/paypal
```


### 9.4 Airwallex Webhook IP 白名单（生产环境）


生产环境建议在防火墙/网关层配置 Airwallex Webhook IP 白名单，仅允许以下 IP 发起请求：


```
# Airwallex Production IPs
35.240.218.67, 35.198.197.83, 35.197.128.86, 35.240.219.218,
35.198.239.51, 35.198.250.210, 35.197.165.40, 35.240.221.15,
35.198.227.200, 34.87.130.213, 34.87.175.82, 35.198.207.246,
34.87.67.183, 35.198.234.237, 35.198.197.137, 35.198.236.255,
34.87.7.233, 34.87.155.193, 34.87.38.65, 34.87.54.142,
35.197.135.105, 35.240.235.109, 34.87.141.165, 34.87.26.83,
34.85.218.163
```


## 附：后端服务接口清单


Looply 后端需要实现以下接口：


| 接口 | Method | 说明 | 调用方 |
| --- | --- | --- | --- |
| `/api/payment/paypal/create` | POST | 创建 Looply 订单 + 调用 PayPal Create Order API | 前端 |
| `/api/payment/paypal/capture` | POST | 调用 PayPal Capture API，支付成功后创建订单 | 前端 |
| `/api/payment/airwallex/create` | POST | 创建 Looply 订单 + 调用 Airwallex Create PaymentIntent | 前端 |
| `/api/payment/airwallex/confirm` | POST | 调用 Airwallex Retrieve PaymentIntent 确认状态 + 更新订单 | 前端 |
| `/api/webhook/paypal` | POST | 接收 PayPal Webhook 通知 | PayPal |
| `/api/webhook/airwallex` | POST | 接收 Airwallex Webhook 通知 | Airwallex |
| `/api/refund/create` | POST | 创建退款请求，调用对应渠道退款 API | 运营后台 |


## 附：数据库关键字段


支付相关信息需要存储在订单表和支付流水表中：


### 支付流水表 (payment_transaction)


| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | BIGINT PK | 主键 |
| `order_id` | VARCHAR | Looply 订单号 |
| `channel` | ENUM | PAYPAL / AIRWALLEX |
| `payment_method` | VARCHAR | paypal / card / klarna / applepay |
| `channel_order_id` | VARCHAR | PayPal Order ID / Airwallex Intent ID |
| `channel_capture_id` | VARCHAR | PayPal Capture ID（退款用） |
| `amount` | DECIMAL(10,2) | 支付金额 |
| `currency` | VARCHAR(3) | 币种（USD） |
| `status` | ENUM | PENDING / SUCCEEDED / FAILED |
| `channel_status` | VARCHAR | 渠道原始状态 |
| `created_at` | TIMESTAMP | 创建时间 |
| `updated_at` | TIMESTAMP | 最后更新时间 |


### 退款流水表 (refund_transaction)


| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | BIGINT PK | 主键 |
| `order_id` | VARCHAR | Looply 订单号 |
| `payment_transaction_id` | BIGINT | 关联支付流水 |
| `channel` | ENUM | PAYPAL / AIRWALLEX |
| `channel_refund_id` | VARCHAR | 渠道退款 ID |
| `amount` | DECIMAL(10,2) | 退款金额 |
| `currency` | VARCHAR(3) | 币种 |
| `reason` | VARCHAR | 退款原因 |
| `status` | ENUM | PROCESSING / SUCCEEDED / FAILED |
| `operator_id` | VARCHAR | 操作人 ID |
| `created_at` | TIMESTAMP | 创建时间 |
| `completed_at` | TIMESTAMP | 完成时间 |
