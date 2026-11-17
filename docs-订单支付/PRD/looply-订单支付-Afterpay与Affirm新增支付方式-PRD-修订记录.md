# Looply 订单支付｜Afterpay 与 Affirm 新增支付方式 PRD 修订记录

| 版本 | 日期 | 修改人 | 修改内容 |
| --- | --- | --- | --- |
| V1.0 草稿 | 2026-10-26 | 产品 | 创建新增 Afterpay、Affirm 的完整迭代 PRD，进入产品决策与原型阶段 |
| V1.0 定稿 | 2026-10-28 | 产品 | 合入产品决策审核和已确认原型：首期美国站且不依赖多 Market 路由；确认金额门槛隐藏规则、自动扣款、主动查单与 30 分钟／72 小时处理、退款与争议边界；固定支付方式顺序；补齐 PC／Mobile Figma 节点、页面状态与验收标准 |
| V1.1 定稿 | 2026-10-28 | 产品 | 明确 Checkout 与待付款订单详情均复用 Airwallex Drop-in Element；组件内支付方式名称、Logo、右侧说明、跳转提示、卡表单、错误提示及本地化由 Airwallex 输出，Looply 不另行硬编码或改写；原型统一为 Drop-in 原文快照；完成金额边界、支付结果状态和双入口复用验证，可进入开发 |
| V1.2 定稿 | 2026-10-28 | 产品 | 根据代码核实修正责任边界：Checkout 与待付款订单详情的支付方式列表、品牌图标、右侧短文案、顺序、显隐和多语言由 Looply 负责；用户选中方式后的支付表单、跳转提示、组件内校验与错误由 Airwallex Drop-in 输出；新增 Afterpay `Pay in 4` 和 Affirm `Monthly payments` 为 Looply 列表文案 |
| V1.3 定稿 | 2026-10-28 | 产品 | 根据线上页面核实支付方式现有顺序为 `Payment Card → PayPal → Klarna → Apple Pay`；本期不在新增方式之外调整存量方式的相对顺序，Afterpay 与 Affirm 追加在其后；最终顺序为 `Payment Card → PayPal → Klarna → Apple Pay → Afterpay → Affirm` |
| V1.4 定稿 | 2026-10-28 | 产品 | 以 Figma Section `10.28 checkout增加支付方式`（`7447:46168`）为最终 UI 依据；支付方式顺序调整为 `Payment Card → PayPal → Apple Pay → Afterpay → Affirm → Klarna`；Afterpay、Affirm 右侧短文案统一为 `Pay over time`，Klarna 保持 `Pay later`；交付范围收敛为 Figma 设计稿与 PRD，不再以交互原型作为开发依据 |
| V1.5 定稿 | 2026-10-28 | 产品 | 合入产品决策审核 D1–D10；按 D3 修正 Afterpay 金额资格：仅开通 Pay in 4 时展示范围为 1–2,000 USD，同时开通 Pay in 4 与 Monthly Installments 时为 1–4,000 USD；计划组合未知或配置不一致时隐藏并告警；Affirm 保持 35–30,000 USD；补齐配置变更、风险与验收用例 |

