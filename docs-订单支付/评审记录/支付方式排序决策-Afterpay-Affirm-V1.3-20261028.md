# Afterpay／Affirm V1.3 支付方式排序决策

> 日期：2026-10-28  
> 结论：沿用线上前四项顺序，新方式追加在后

## 一、方案比较

| 方案 | 顺序 | 优点 | 代价 | 结论 |
| --- | --- | --- | --- | --- |
| A. 沿用线上 | Payment Card → PayPal → Klarna → Apple Pay → Afterpay → Affirm | 本期范围可控；不改变老用户已熟悉的前四项位置；便于观察新方式增量 | 支付类型不完全按“卡／钱包／分期”分组 | 采用 |
| B. Apple Pay 前置 | Payment Card → PayPal → Apple Pay → Klarna → Afterpay → Affirm | 快捷支付优先；三个可延后／分期品牌更集中 | 本期同时改变存量方式顺序；没有 Looply 数据证明调整会提升转化 | 不采用 |

## 二、决策理由

1. 线上顺序已经是用户当前使用基线，不存在无法完成支付或明显误导。
2. Klarna 同时可覆盖 pay now、pay later 和 financing，不能仅因其包含分期能力就认定必须排在 Apple Pay 之后。
3. Apple Pay 具有低操作成本优势，但是否前置应由 Looply 设备支持率、选择率和成功率数据验证，不在本期无数据调整。
4. 保持存量顺序能让上线前后的变化集中在 Afterpay 和 Affirm，更容易归因新方式对转化的影响。

## 三、展示规则

- 固定顺序：`Payment Card → PayPal → Klarna → Apple Pay → Afterpay → Affirm`。
- Apple Pay 在不支持的设备或浏览器中隐藏。
- Afterpay、Affirm 不满足资格时隐藏。
- 任一方式隐藏后，其余方式保持相对顺序。
- 不根据历史选择、金额或当前选中项动态重排。
