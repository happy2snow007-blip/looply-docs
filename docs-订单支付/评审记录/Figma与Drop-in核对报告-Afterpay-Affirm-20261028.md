# Afterpay／Affirm Figma 与 Airwallex Drop-in 核对报告

> 核对日期：2026-10-28  
> 结论：通过，可作为开发基线

## 一、核对范围

| 来源 | 对象 | 用途 |
| --- | --- | --- |
| Figma | Section `6660:22668` | 订单详情更改支付方式外层结构 |
| Figma | PC `6687:31637` | PC 支付容器、订单摘要和布局 |
| Figma | Mobile `6660:23386` | Mobile 支付方式底部弹层 |
| 线上 Checkout 截图 | Payment 区块 | Airwallex Drop-in 支付列表密度、选中态和重定向提示 |
| 交互原型 | `looply-afterpay-affirm-interactive-prototype-v1.html` | 新方式、金额边界、结果状态和 PC／Mobile 交互 |

## 二、双向核对结果

| 核对项 | 结果 | 说明 |
| --- | --- | --- |
| 方式顺序 | 通过 | `Payment Card → PayPal → Apple Pay → Klarna → Afterpay → Affirm` |
| 资格不满足隐藏 | 通过 | 隐藏后其余方式保持相对顺序 |
| Drop-in 文案 | 通过 | 保留 `Pay later`、`Pay in 4`、`Monthly payments` 及原始重定向句式，不替换为 Looply 自拟文案 |
| Checkout 区块 | 通过 | 与用户提供的线上样式对齐，选中方式下展开重定向提示 |
| PC 订单详情 | 通过 | 外层页面与 Figma 对齐，Payment 区域复用同一 Drop-in |
| Mobile 订单详情 | 通过 | 底部弹层与 Figma 对齐，内部复用同一 Drop-in |
| 卡表单与 Billing Address | 通过 | 标记为 Drop-in 责任区，不要求 Looply 重做表单 |
| 确认中 | 通过 | 隐藏支付列表与付款按钮，防止重复付款 |
| 成功／失败／取消 | 通过 | 成功关闭入口；失败和取消恢复可用方式 |

## 三、差异分类

| 分类 | 数量 | 结论 |
| --- | ---: | --- |
| 产品逻辑缺失 | 0 | 无 |
| 设计遗漏 | 0 | Figma 未覆盖的金额和结果状态已由交互原型补齐 |
| 原型偏差 | 0 | 定稿前已将订单详情自拟跳转文案改为 Drop-in 原始句式 |
| 交付边界不清 | 0 | Figma 负责外层布局，Airwallex 负责 Drop-in 内部，PRD 负责业务规则 |
| 阻塞问题 | 0 | 可进入开发 |

## 四、开发解读原则

1. 不将原型重画的 Drop-in 内部结构解读为需要 Looply 自研的支付列表。
2. 不将原型中的当前英文快照写入 Looply 语言包。
3. 生产页面的品牌、Logo、右侧说明、重定向提示、卡表单和组件内错误以 Airwallex Drop-in 运行时实际输出为准。
4. 业务资格、展示顺序、支付窗口、状态处理和退款／争议规则以 PRD V1.1 为准。
