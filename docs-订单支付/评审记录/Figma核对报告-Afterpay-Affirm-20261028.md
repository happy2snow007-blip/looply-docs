# Figma 核对报告｜Afterpay 与 Affirm｜2026-10-28

## 一、核对范围

- Figma 文件：`Looply-1.1`
- 本期 Section：`10.28 checkout增加支付方式`（`7447:46168`）
- 核对模式：迭代模式 B
- 对照 PRD：V1.3 → V1.4
- 最终交付范围：Figma 设计稿 + PRD V1.4；交互原型不作为开发依据

## 二、画布与帧清单

| 端 | 页面 | 本期 Section | 本期 Frame | 状态 |
| --- | --- | --- | --- | --- |
| Mobile | Checkout | `7447:46168` | `checkout增加支付方式`（`7447:45675`） | 已核对 |
| Mobile | 待付款订单详情 | `7447:46168` | `order details-切换付款`（`7447:46169`） | 已核对 |
| PC | 待付款订单详情 | `7447:46168` | `order details-切换付款`（`7447:46586`） | 已核对 |
| PC | Checkout | `7447:46168` | `chekout加协议随屏`（`7447:47191`） | 已核对，帧名沿用设计稿原拼写 |

## 三、关键元素核对

| # | 元素 | Figma 定稿 | PRD V1.4 落点 | 结论 |
| --- | --- | --- | --- | --- |
| 1 | 支付方式顺序 | Payment Card → PayPal → Apple Pay → Afterpay → Affirm → Klarna | §2.2、§3.1、§7.1、§8.1 | 一致 |
| 2 | Afterpay 右侧文案 | Pay over time | §2.2、§3.1、§8.1 | 一致 |
| 3 | Affirm 右侧文案 | Pay over time | §2.2、§3.1、§8.1 | 一致 |
| 4 | Klarna 右侧文案 | Pay later | §2.2、§8.1 | 一致 |
| 5 | Apple Pay 条件展示 | 支持时位于 PayPal 与 Afterpay 之间 | §2.2、§3.1、§8.1 | 一致 |
| 6 | 选中后支付内容 | 设计仅定义 Looply 列表层；实际内容由 Drop-in 返回 | §1.7、§2.2、§3.1、§3.4 | 一致 |

## 四、V1.3 → V1.4 差异判定

| 差异 | 分类 | 处理 |
| --- | --- | --- |
| 支付方式顺序由 Payment Card → PayPal → Klarna → Apple Pay → Afterpay → Affirm 调整为设计稿顺序 | 本期新增决策 | PRD 全文及验收标准统一更新 |
| Afterpay `Pay in 4` 改为 `Pay over time` | 本期新增决策 | PRD 列表文案统一更新；实际分期计划仍由渠道决定 |
| Affirm `Monthly payments` 改为 `Pay over time` | 本期新增决策 | PRD 列表文案统一更新；实际分期计划仍由渠道决定 |
| 原型不再作为交付依据 | 交付范围调整 | PRD 输入源、UI 关联、依赖与附录删除原型引用 |

## 五、结论

Figma Section `7447:46168` 与 PRD V1.4 的支付方式顺序、右侧文案、双端入口和 Looply／Airwallex 责任边界已对齐。未发现需要设计返工的差异。
