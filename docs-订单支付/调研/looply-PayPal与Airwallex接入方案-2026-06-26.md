# looply PayPal + Airwallex 接入方案

> 调研日期：2026-06-26
> 调研方法：多源交叉验证（86条声明提取 → 25条深度验证 → 16条确认 / 9条推翻）

---

## 一、整体架构定位

| 角色 | PayPal | Airwallex（空中云汇）|
|------|--------|---------------------|
| **定位** | 面向买家的支付方式 | 底层跨境收单基础设施 + 资金通道 |
| **核心价值** | 美国用户信任度高、渗透率高；支持 Venmo、Pay Later | 多币种收单、跨境资金归集、全球打款 |
| **接入模式** | PayPal Multiparty（Commerce Platform）| Payments for Platforms（Marketplace 方案）|

### 架构组合方式

有两种可选方案：

#### 方案 A：PayPal 直连 + Airwallex 处理其他支付方式（推荐）

```
买家
 ├── PayPal/Venmo 支付 ──→ PayPal Multiparty API（直连）──→ PayPal 结算
 └── 信用卡/其他支付 ──→ Airwallex Payment Acceptance ──→ Airwallex 钱包
```

- PayPal 直连：平台以 Partner 身份接入，商家通过 Partner Referral API 入驻
- Airwallex 收单：处理信用卡、Apple Pay、Google Pay 等非 PayPal 支付方式
- 两套独立集成，资金分别在两个通道

**优势**：PayPal 功能完整（延迟打款、平台抽佣），无 beta 风险
**劣势**：需维护两套支付集成，资金分散在两个账户体系

#### 方案 B：PayPal 走 Airwallex Managed Path（统一入口）

```
买家
 ├── PayPal/Venmo 支付 ──→ Airwallex（PayPal Managed Path）──→ Airwallex 钱包
 └── 信用卡/其他支付 ──→ Airwallex Payment Acceptance ──→ Airwallex 钱包
```

- 所有支付方式统一走 Airwallex，PayPal 资金也归集到 Airwallex 钱包
- Airwallex 的 PayPal Managed Path **目前针对美国商户仍为 Beta 状态**
- 结算周期：T+1 工作日

**优势**：资金统一归集到 Airwallex 钱包，简化对账和资金管理
**劣势**：Managed Path 处于 Beta，功能/限额/SLA 可能变化；PayPal 分账能力受限于 Airwallex 透传程度

### 推荐决策

**Phase 1 推荐方案 A**，原因：
1. PayPal Managed Path 的 Beta 状态对生产环境有风险
2. PayPal Multiparty 的延迟打款、平台抽佣功能经过充分验证
3. Phase 2 做商家结算时，再评估 Managed Path 是否已转正，决定是否迁移

---

## 二、Phase 1：收单 + 退款

### 2.1 PayPal Multiparty 收单

#### API 能力（已验证）

| 能力 | API | 说明 |
|------|-----|------|
| **创建订单** | `POST /v2/checkout/orders` | 支持 PayPal、Venmo（仅美国）、Pay Later、信用卡/借记卡 |
| **延迟打款** | `disbursement_mode: DELAYED` | 平台先代收，资金暂扣；28天后自动释放给商家 |
| **手动释放** | `POST /v1/payments/referenced-payouts-items` | 用 capture transaction ID 手动触发打款 |
| **平台抽佣** | `PURCHASE_UNITS.PAYMENT_INSTRUCTION.PLATFORM_FEES` | 每笔交易抽取平台佣金，佣金币种必须与交易币种一致 |
| **退款** | `POST /v2/payments/captures/{capture_id}/refund` | 支持全额/部分退款 |

#### 集成层级

| 层级 | 适用场景 | 特点 |
|------|---------|------|
| **Standard Checkout** | 快速接入 | PayPal 托管支付页面，接入简单 |
| **Advanced Checkout** | 品牌定制 | 自定义卡片字段、品牌 UI，体验更原生 |

**建议 looply 选 Advanced Checkout**：二手电商需要原生支付体验提升信任度。

#### 商家入驻流程

```
平台 → Partner Referral API 生成入驻链接
 → 商家跳转 PayPal 完成入驻（身份验证、银行账户绑定）
 → 回调通知平台入驻完成
 → 平台查询商家集成状态（payments_receivable、primary_email_confirmed）
```

### 2.2 Airwallex 收单

#### API 能力（已验证）

| 能力 | API | 说明 |
|------|-----|------|
| **创建支付意图** | Payment Intent API | 支持信用卡、Apple Pay、Google Pay 等 |
| **多币种** | 支持 60+ 币种 | 前期 USD 为主，后续可扩展 |
| **退款** | Refund API | 全额/部分退款 |
| **3D Secure** | 内置风控 | 符合 PSD2/SCA 要求 |

#### 定价模式

| 模式 | 说明 | 适用场景 |
|------|------|---------|
| **Interchange++（IC++）** | 卡组织实际费率 + Airwallex 固定加价 | 交易量大、想优化成本 |
| **Blended（混合费率）** | 固定费率（如 2.9% + $0.30） | 起步阶段、费用可预测 |

费用构成三部分：
1. **Gateway fee**：路由/基础设施费
2. **Payment method fee**：支付方式费率（因卡种/支付方式不同）
3. **Fraud/3DS fee**：风控/认证费

**FX 汇兑费**：当交易币种 ≠ 结算币种时额外收取（主要币种约 0.5%，其他约 1%）

### 2.3 退款流程设计

```
买家申请退款
 → 平台审核通过
 → 判断原支付渠道
   ├── PayPal 支付 → 调用 PayPal Refund API → 退回买家 PayPal 账户
   └── 信用卡支付 → 调用 Airwallex Refund API → 退回原卡
 → 更新订单状态
```

---

## 三、Phase 2：商家结算 + 跨境资金归集（规划）

### 3.1 Airwallex 商家账户模型

| 账户类型 | Connected Account | Ledger Account |
|---------|-------------------|----------------|
| **KYC 深度** | 完整 KYC/KYB | 轻量审查 |
| **覆盖国家** | 50+ 国家 | 200+ 国家 |
| **资金归属** | 商家名下 | 平台代管 |
| **打款限制** | 灵活 | 仅限同名账户 |
| **适用场景** | 美国本土商家 | 国际轻量卖家 |

**looply 建议**：美国商家用 Connected Account（合规完整），国际商家用 Ledger Account（轻量入驻）。

### 3.2 全球打款能力

- **本地清算**：120+ 国家/地区
- **SWIFT**：150+ 国家/地区
- **支持币种**：60+ 种
- 批量打款 API 支持规模化结算

### 3.3 PSP-Agnostic 架构

Airwallex 支持 PSP 无关架构：平台可以用任意 PSP（如 PayPal）做收单，资金沉淀到 Airwallex Holding Account，再通过 Airwallex 做下游打款。

**重要限制**：Airwallex **不直接集成**第三方 PSP——平台必须自行维护与每个 PSP 的集成，然后通过 API 将外部 PSP 的资金信息同步到 Airwallex。

### 3.4 跨境资金归集

```
PayPal 结算资金 → PayPal 平台账户 → 提现到 Airwallex 钱包（或银行中转）
Airwallex 收单资金 → Airwallex 钱包
                          ↓
                    统一归集（多币种 → 人民币）
                          ↓
                    结汇入境（走 Airwallex 跨境通道）
```

---

## 四、接入前置条件

### 4.1 PayPal Multiparty

| 事项 | 说明 | 耗时预估 |
|------|------|---------|
| **Partner 审批** | 必须获得 PayPal 批准的 Partner 资格才能上线（未获批 API 返回 401） | 需与 PayPal 确认（公开文档未注明周期） |
| **PayPal 代表** | 批准后会分配专属 PayPal 代表 | - |
| **开发者账号** | PayPal Developer Dashboard 注册 | 即时 |
| **Sandbox 测试** | 批准前可用 Sandbox 开发测试 | - |
| **企业资质** | 美国注册公司 | - |

**关键提醒**：Partner 审批是硬性前置条件，建议尽早申请，不要等到开发完成再提交。

### 4.2 Airwallex

| 事项 | 说明 | 耗时预估 |
|------|------|---------|
| **企业注册** | 美国注册公司 | - |
| **受益所有人披露** | 持股 ≥25% 的受益人：全名、出生日期、国籍、持股比例 | - |
| **董事签署证明** | 公司信纸上的证明文件，由董事签署，日期在 6 个月内 | - |
| **KYC 审核** | 提交材料后等待审核 | 需与 Airwallex 确认 |
| **开发者账号** | Airwallex 后台注册 | 即时 |

### 4.3 前置行动清单

| 优先级 | 行动 | 负责方 | 备注 |
|--------|------|--------|------|
| P0 | 申请 PayPal Partner 资格 | 业务 | 审批周期不确定，越早越好 |
| P0 | 注册 Airwallex 企业账户 + 提交 KYC 材料 | 业务 | 需准备受益所有人信息和董事签署文件 |
| P1 | 申请 PayPal Developer 账号，开始 Sandbox 开发 | 开发 | 不依赖 Partner 审批 |
| P1 | 申请 Airwallex 测试环境 | 开发 | - |
| P2 | 确认 Airwallex PayPal Managed Path Beta 状态 | 业务 | 评估 Phase 2 是否迁移 |

---

## 五、费率对比

| 项目 | PayPal Multiparty | Airwallex |
|------|-------------------|-----------|
| **收单费率** | 需 Partner 谈判（公开费率约 2.99% + $0.49 标准交易） | IC++（按卡种浮动）或 Blended（约 2.9% + $0.30） |
| **平台抽佣** | platform_fees 字段，每日结算到 Partner 银行账户 | 平台侧自行管理 |
| **退款费用** | 退款手续费不退还 | 需确认 |
| **FX 汇兑** | PayPal 汇率 + markup | 主要币种 ~0.5%，其他 ~1% |
| **打款费用** | N/A（Phase 1 不涉及） | 本地清算 / SWIFT，费率因国家不同 |

**注意**：以上为公开参考费率，实际费率需与两家分别商务谈判，交易量越大议价空间越大。

---

## 六、待确认问题

| # | 问题 | 影响 | 建议行动 |
|---|------|------|---------|
| 1 | PayPal Partner 审批周期具体多长？ | 直接影响项目排期 | 尽早联系 PayPal 商务 |
| 2 | Airwallex PayPal Managed Path 何时转正？Beta 期间有无交易额限制？ | 影响 Phase 2 架构决策 | 联系 Airwallex 客户经理 |
| 3 | 两家的实际谈判费率？ | 影响成本测算 | 业务侧发起商务谈判 |
| 4 | PayPal 延迟打款 28 天自动释放是否可配置更长周期？ | 二手商品可能有较长确认期 | 与 PayPal 代表确认 |
| 5 | Airwallex Connected Account 的商家 KYC 流程是否支持 API 化（嵌入 looply 入驻流程）？ | 影响商家入驻体验 | 查阅 Airwallex 文档 / 确认 |

---

## 七、调研来源

核心信源（均为官方文档，经交叉验证）：
- PayPal Multiparty Docs: https://developer.paypal.com/docs/multiparty/
- PayPal Delayed Disbursement: https://developer.paypal.com/docs/multiparty/checkout/delayed-disbursement/
- Airwallex Pricing: https://www.airwallex.com/docs/payments/about-airwallex-payments/fees-and-pricing-models
- Airwallex PayPal Integration: https://www.airwallex.com/docs/payments/payment-methods/global/paypal
- Airwallex Marketplace: https://www.airwallex.com/docs/payments-for-platforms/use-cases/payments-for-marketplaces
- Airwallex US KYC Requirements: https://help.airwallex.com/hc/en-gb/articles/4419267227417
