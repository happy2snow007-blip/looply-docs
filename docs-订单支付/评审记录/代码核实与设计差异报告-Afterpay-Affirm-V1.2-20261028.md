# Afterpay／Affirm V1.2 代码核实与设计差异报告

> 日期：2026-10-28  
> 模式：迭代核对  
> 结论：V1.1 对支付方式列表的归属判断错误，V1.2 已修正

## 一、新增证据

| 证据 | 已核实结论 | 影响 |
| --- | --- | --- |
| 现有 Klarna 代码 | Klarna 品牌图标由 Looply 渲染 | 新增 Afterpay、Affirm 的列表品牌图标也应由 Looply 提供 |
| 现有 Klarna 代码 | 右侧 `Pay later` 由 Looply 编写 | Afterpay `Pay in 4`、Affirm `Monthly payments` 应定义为 Looply 列表文案 |
| Klarna 点击后效果 | 由 Airwallex 返回 | 跳转提示、表单、组件内校验和错误仍归 Airwallex |

## 二、双向差异

| 对象 | V1.1 口径 | 代码／页面实际 | V1.2 处置 | 分类 |
| --- | --- | --- | --- | --- |
| 支付方式列表 | 整体归 Airwallex Drop-in | Looply 渲染 | 改为 Looply 责任区 | 交付边界修正 |
| 品牌图标 | 归 Airwallex | Klarna 图标由 Looply 提供 | Afterpay、Affirm 使用 Looply 管理的官方品牌资源 | 交付边界修正 |
| 右侧短文案 | 归 Airwallex | `Pay later` 由 Looply 编写 | 三种 BNPL 右侧文案均归 Looply 语言包 | 交付边界修正 |
| 选中后内容 | 归 Airwallex | 归 Airwallex | 保持不变 | 一致 |
| 顺序与金额显隐 | Looply 业务规则 | Looply 判定 | 保持不变 | 一致 |

## 三、帧级核对

| 端 | 页面／帧 | nodeId | 列表层 | 选中后层 | 结论 |
| --- | --- | --- | --- | --- | --- |
| PC | Checkout Payment | 线上页面截图 | Looply | Airwallex | V1.2 已分层 |
| PC | 订单详情更改支付方式 | `6687:31637` | Looply | Airwallex | V1.2 已分层 |
| Mobile | 订单详情底部弹层 | `6660:23386` | Looply | Airwallex | V1.2 已分层 |

Figma Section 继续为 `6660:22668`。本次没有视觉顺序或布局变更，只修正开发责任边界，因此不需要设计返工。

## 四、最终分工

| 层级 | 负责方 | 内容 |
| --- | --- | --- |
| 列表层 | Looply | 方式名称、品牌图标、右侧短文案、顺序、显隐、选中态和多语言 |
| 选中后组件层 | Airwallex | 支付表单、跳转提示、组件内校验、错误提示和对应本地化 |
| 业务层 | Looply | 资格、金额门槛、固定顺序、支付窗口、状态、退款、对账和争议规则 |
