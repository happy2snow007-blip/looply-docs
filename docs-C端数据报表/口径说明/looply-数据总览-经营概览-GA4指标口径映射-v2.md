# Looply｜数据总览 / 经营概览 GA4 指标口径映射 v2

**版本日期**：2026-08-03  
**查询配置**：`tools/ga4-sync/queries.json` schema `2.3`  
**页面**：`outputs/looply-数据总览-经营概览-GA4自动同步副本-v1.html`

## 1. 核心经营指标

| 页面指标 | 计算 | 退款影响 | 状态 |
|---|---|---|---|
| 访问访客数 | `page_view` 的 `totalUsers`，周期去重 | 不影响 | GA4 已接入 |
| 首次访问访客数 | `first_visit` 的 `totalUsers`，周期去重 | 不影响 | GA4 已接入 |
| 购买访客数 | `purchase` 的 `totalUsers`，周期去重 | 后续退款不移除购买身份 | GA4 已接入 |
| 购买转化率 | 周期购买访客数 ÷ 周期访问访客数 | 后续退款不回退 | 已计算 |
| GA4 Purchase 数 | `ecommercePurchases` | 退款不冲减 | GA4 已接入，待订单对账 |
| GA4 成交客单价 | `grossPurchaseRevenue ÷ ecommercePurchases` | 退款不回算 | GA4 已接入 |
| GA4 成交收入 | `grossPurchaseRevenue` | 退款前成交金额 | GA4 已接入，不等同财务 GMV |

禁止替代：

- 不使用 `totalRevenue` 作为 GA4 成交收入。
- 不使用退款后的 `purchaseRevenue` 作为 GA4 成交收入或成交客单价分子。
- 不使用 `purchase eventCount` 冒充 `ecommercePurchases`；仅在临时兼容时可单独标注，当前正式查询不使用该兼容值。

## 2. 售后影响：成交订单 Cohort

### 2.1 页面指标

| 页面指标 | 订单选择 | 截止条件 | 聚合 | 当前状态 |
|---|---|---|---|---|
| 成交订单退款数 | 支付成功时间落入所选周期 | 退款在查询完成时间前已完成 | `count(distinct order_id/transaction_id)`；同一订单多次/部分退款只计 1 | 订单级关联未接入，显示 `—` |
| 成交订单退款金额 | 与退款订单数相同的成交订单 Cohort | 退款在查询完成时间前已完成 | 累计实际已完成退款金额；多次/部分退款金额相加 | 订单级关联未接入，显示 `—` |

- 观察截止时间使用本次报表查询完成时间，并在页面展示。
- 后续退款会回补对应历史成交订单 Cohort，因此历史周期值可能随时间增加。
- 不同 Cohort 的退款成熟度不同；没有统一固定观察窗口前，不展示直接上一周期对比或简单退款率。
- 售后结果不反向修改七个核心经营指标。

### 2.2 GA4 辅助诊断，不用于售后卡片

| 信号 | 查询 | 用途 | 不得用于 |
|---|---|---|---|
| 按退款日退款金额 | `after_sales_daily.refundAmount` | 核验 GA4 是否观察到退款金额 | 不得替代成交订单 Cohort 退款金额 |
| refund 事件数 | `refund_event_daily.eventCount` | 核验 refund 事件上报 | 不得称为去重退款订单数 |
| 退款后净购买收入 | `after_sales_daily.purchaseRevenue` | 售后净收入诊断 | 不得改写 GA4 成交收入 |

当前查询返回 0 行或 0 值只能说明 GA4 查询未观察到相应信号；在订单级链路未接入前，不能证明成交订单 Cohort 的真实退款为 0。

## 3. 购买意向与关键行为覆盖

| 指标 | 计算 | 状态规则 |
|---|---|---|
| 商详访客 | `view_item.totalUsers` | GA4 已接入 |
| 收藏访客 | 收藏事件的 `totalUsers` | 收藏事件未真实接入时显示 `—` |
| 加购访客 | `add_to_cart.totalUsers` | GA4 已接入 |
| 购买意向访客 | `add_to_wishlist OR add_to_cart` 后按访客联合去重 | 收藏未接入时显示 `— / 数据不完整` |
| 购买意向覆盖率 | 购买意向访客 ÷ 访问访客 | 联合人数缺失时不计算 |
| Checkout 访客 | `begin_checkout.totalUsers` | GA4 已接入 |

收藏与加购并列；购买访客不加入购买意向集合。各节点为独立事件覆盖，不是同一批访客的严格有序漏斗。

## 4. 访问与购买转化趋势

| 图形 | 坐标轴 | 值 |
|---|---|---|
| 每日访问访客柱状 | 左轴，从 0 开始 | `page_view_daily.totalUsers` |
| 每日购买转化率折线 | 右轴，从 0 开始 | 同日 `overview_daily.totalPurchasers ÷ page_view_daily.totalUsers` |

- 两个系列共用日期横轴和 Tooltip。
- 不展示每日购买访客折线。
- 周期购买转化率必须用周期内去重购买访客 ÷ 周期内去重访问访客，不得取每日转化率平均值。

## 5. 查询与缺失状态

- 默认周期：最近 7 个完整自然日；默认对比上一等长 7 日。
- 国家/地区与设备筛选由服务端白名单控制。
- 查询成功且字段已接入时，真实 0 可展示为 0。
- 事件或订单字段未接入、无法证明业务值为 0 时，显示“— / 待接入”。
- 所有 GA4 查询成功后才更新完整结果；失败时不发布半套数据。

