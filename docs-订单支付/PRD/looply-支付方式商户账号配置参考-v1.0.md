# 已废弃｜Looply 支付方式商户账号配置参考 v1.0

> 2026-09-23 已废弃：产品后台不维护商户账号。请以 `looply-支付渠道技术配置参考-v1.0.md` 为准。

## 一、后台怎么配置

“商户账号”不让运营填写 API 密钥，而是从支付接入服务已经登记、验证通过的账号中选择。支付方式主数据只保存 `payment_account_ref`，指向内部账号记录；Client Secret、API Key、证书私钥等敏感信息由密钥服务保存。

推荐的内部账号记录至少包含：账号别名、支付通道、运行环境、渠道侧账号标识、凭证引用、收款主体、支付能力状态和启停状态。生产与沙箱账号必须分开。

## 二、三种支付方式参考

| 支付方式主数据 | 支付通道 | 商户账号示例 | 账号记录重点 | 额外条件 |
|---|---|---|---|---|
| PayPal 香港 | PayPal | `PayPal-HK-main` | PayPal Merchant ID／payer_id、Live REST App Client ID、Client Secret 的密钥引用、Webhook 配置、账号状态 | 使用已验证的 PayPal Business 账号；后台不保存邮箱作为唯一账号标识 |
| Credit Card US | Airwallex | `Airwallex-US-main` | Airwallex 账号或内部连接 ID、API 凭证引用、收款主体、Payments 激活状态 | 卡支付方式必须已在该 Airwallex 账号启用；同一账号可被多个支付方式引用 |
| Apple Pay US | Airwallex | `Airwallex-US-main` | 与银行卡收单共用 Airwallex 商户账号 | 另校验 Apple Pay 已启用；网页集成按模式完成域名登记，使用自有证书时另维护 Apple Merchant ID 与证书状态 |

PayPal REST API 使用 Client ID 和 Client Secret 换取访问令牌；PayPal 建议使用稳定的 Merchant ID／payer_id 标识商户，不使用可能变更的邮箱。参考：[PayPal REST API 入门](https://developer.paypal.com/api/get-started/)、[PayPal API 请求与商户标识](https://developer.paypal.com/api/make-api-requests)、[PayPal JavaScript SDK 配置](https://developer.paypal.com/sdk/js/configuration/)。

Airwallex Connected Account 的账号 ID 使用 `acct_` 前缀；只有平台替其他商户收款时才需要 Connected Account。Looply 为自身收款时，可直接登记自己的 Airwallex 主账号连接，不需要额外创建 Connected Account。参考：[Airwallex Connected Accounts](https://www.airwallex.com/docs/connected-accounts/get-started/get-started-with-connected-accounts)、[查看账号与支付激活状态](https://www.airwallex.com/docs/connected-accounts/manage-accounts/view-connected-accounts)。

Apple Pay 通过 Airwallex 时，商户账号仍是 Airwallex 账号，不把 Apple Merchant ID 当作收单账号。Airwallex 托管结账与自有网页／原生接入的域名、证书要求不同。参考：[Airwallex Apple Pay Web 接入](https://www.airwallex.com/docs/payments/payment-methods/global/apple-pay/native-api)、[使用自有 Apple Pay 证书](https://www.airwallex.com/docs/payments/payment-methods/global/apple-pay/use-your-own-certificate)。

## 三、页面规则

1. 先选支付通道，再加载该通道下已启用、环境一致的商户账号。
2. 保存支付方式时只保存商户账号引用，不复制渠道密钥。
3. 支付方式启用前，账号必须处于可收款状态；Apple Pay 还需通过能力与域名／证书检查。
4. 修改商户账号只影响新支付；支付单继续保存原支付方式、通道、账号和币种快照。
5. Credit Card 与 Apple Pay 可以绑定同一个 Airwallex 账号，因为它们是同一收单账号下的不同支付能力。
