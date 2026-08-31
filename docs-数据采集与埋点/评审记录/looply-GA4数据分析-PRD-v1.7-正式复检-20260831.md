# Looply GA4数据分析 PRD v1.7 正式复检

> 复检日期：2026-08-31  
> 评审标准：Looply 开发交付文档 Review 标准 v0.1  
> 使用规范：prd-writing、prd-review-simulation  
> 正式审查模型：gpt-5.6-sol / high  
> 复检对象：`looply-GA4数据分析-PRD-v1.7.md`

## 结论

v1.6 原稿不能直接发布：Purchase 同时存在“首次确认 paid 即成立”“后端 paid 且浏览器 claim 才触发”“浏览器主发＋5分钟服务端兜底”三套口径，并与已发布《Looply 数据采集与埋点产品需求 v1.8》的服务端权威事实规则冲突。

v1.7 已完成该 P0 修复，可作为本次发布版本。Purchase 的权威事实、生产端、幂等键、交易号、关联上下文、浏览器边界、失败重试和验收用例已统一为服务端单路径。该规则是开发目标，不代表生产已经实现。

## Purchase 复检证据

| 检查项 | v1.7 结论 |
|---|---|
| 权威事实 | 订单／支付服务端首次确认父订单 `order_id` 进入最终 `paid` |
| GA4 生产端 | 唯一服务端发送者，通过 Measurement Protocol 投递 |
| 浏览器职责 | 只展示订单状态，不发送、claim、确认或补发 Purchase |
| 交易关联 | `transaction_id = parent order_id` |
| 归因关联 | 使用支付前冻结的 `client_id`、`session_id` 与合法来源上下文；缺失不阻断成交事实或投递 |
| 幂等 | `order_id + purchase + measurement_id` 唯一；重试复用同一键和 transaction_id |
| 验收 | 覆盖重复回调、并发消费、成功页关闭／晚到、上下文缺失、网络重试和订单对账 |

## 四项专项检查

- 准确性：Purchase 事实成立条件与发送条件已分离；未再把浏览器执行状态作为成交事实前提。
- 冲突：Purchase 在概述、范围、事件矩阵、第五章、数据模型、监控、验收和示例中的口径一致，并与采集 PRD v1.8 对齐。
- 重复：删除浏览器主路径、claim、`tag_invoked`、5分钟兜底及 `suppressed_by_browser` 的重复定义。
- 冗余：删除浏览器 Purchase 示例和确认数据表；保留服务端业务结果、幂等和验收所需的最少技术边界。

## 非本次决策项

高阶复检另识别出三个既有口径风险：GA 自动与主动 `page_view` 并存、`page_location` 与 `page_referrer` 的跨材料使用、`add_shipping_info` 与采集 PRD v1.8 的粒度差异。本次用户明确授权以 v1.8 统一 Purchase，未授权改变上述三项已写入 v1.6 的产品口径，因此未静默修改；后续应单独确认并跨文档收口。

## 发布门禁

- 本次可发布对象为 v1.7，不覆盖 v1.6。
- 文档中心索引必须指向 v1.7，并保留修订记录。
- 发布提交不得包含文档中心仓库内其他模块的未提交改动。
