# Looply 汇率管理模块 PRD

**文档版本**：v1.0  
**创建日期**：2026-04-29  
**产品负责人**：产品团队  
**目标上线**：MVP 阶段

---

## 一、产品概述

### 1.1 模块定位

汇率管理模块是 Looply 跨境电商平台的**用户价格换算基础设施**，为商品展示、运费计算、支付页面等场景提供统一的汇率数据服务。

**核心职责**：
- 从外部数据源获取实时汇率
- 配置平台点差规则
- 发布生效汇率供业务系统调用
- 提供历史快照与变动追溯
- 监控汇率异常并告警

**明确边界**：
- ✅ 提供汇率数据查询服务
- ❌ 不负责金额换算计算逻辑
- ❌ 不负责金额格式化与展示
- ❌ 不负责报价锁定与心理价修正
- ❌ 不负责支付结算与财务对账

### 1.2 业务价值

- **用户侧**：看到准确、稳定的商品价格，支付金额与展示一致
- **运营侧**：通过点差配置平衡汇率波动风险与价格竞争力
- **技术侧**：统一汇率数据源，避免各业务系统重复接入

### 1.3 系统基准货币

**USD（美元）** 作为 Looply 平台的系统基准货币：
- 所有商品定价以 USD 为基准
- 汇率数据以 USD 为 base_currency
- 其他币种汇率均为 USD → 目标币种的换算率

---

## 二、核心功能

### 2.1 数据源管理

**功能描述**：接入外部汇率数据源，支持主备切换与定时拉取。

**核心字段**（表：`exchange_rate_source`）：

| 字段 | 类型 | 说明 |
|------|------|------|
| source_code | varchar(50) | 数据源标识（如 `fixer_io`） |
| source_name | varchar(100) | 数据源名称 |
| api_endpoint | varchar(500) | API 地址 |
| priority | int | 优先级（数字越小优先级越高） |
| status | enum | `active`/`inactive` |
| fetch_interval | int | 拉取间隔（分钟） |

**业务规则**：
- 系统按 `priority` 顺序调用数据源
- 主数据源失败时自动切换到备用源
- 支持手动禁用/启用数据源
- 记录每次拉取的成功/失败日志

---

### 2.2 原始汇率记录

**功能描述**：存储从数据源获取的原始汇率数据，作为审计基准。

**核心字段**（表：`exchange_rate_raw`）：

| 字段 | 类型 | 说明 |
|------|------|------|
| source_code | varchar(50) | 数据源标识 |
| base_currency | char(3) | 基准货币（固定 USD） |
| target_currency | char(3) | 目标货币 |
| rate | decimal(18,8) | 原始汇率 |
| fetched_at | datetime | 数据源返回时间 |
| created_at | datetime | 入库时间 |

**业务规则**：
- 每次拉取成功后写入原始记录
- 不可修改，仅供审计追溯
- 保留 90 天历史数据

---

### 2.3 点差配置

**功能描述**：运营人员配置平台点差规则，用于调整生效汇率。

**核心字段**（表：`exchange_rate_spread`）：

| 字段 | 类型 | 说明 |
|------|------|------|
| currency | char(3) | 目标货币 |
| spread_type | enum | `percentage`/`fixed` |
| spread_value | decimal(10,4) | 点差值 |
| effective_from | datetime | 生效开始时间 |
| effective_to | datetime | 生效结束时间（可为空） |
| status | enum | `active`/`inactive` |

**业务规则**：
- 同一币种同一时间只能有一条生效配置
- 支持提前配置未来生效的点差
- 点差计算公式：
  - 百分比型：`生效汇率 = 原始汇率 × (1 + spread_value)`
  - 固定值型：`生效汇率 = 原始汇率 + spread_value`

**操作界面**：
- 列表展示当前生效的点差配置
- 支持新增/编辑/停用点差规则
- 显示历史配置记录

---

### 2.4 生效汇率发布

**功能描述**：基于原始汇率 + 点差配置，计算并发布最终生效汇率。

**核心字段**（表：`exchange_rate_effective`）：

| 字段 | 类型 | 说明 |
|------|------|------|
| base_currency | char(3) | 基准货币（USD） |
| target_currency | char(3) | 目标货币 |
| raw_rate | decimal(18,8) | 原始汇率 |
| spread_value | decimal(10,4) | 应用的点差 |
| effective_rate | decimal(18,8) | 最终生效汇率 |
| effective_from | datetime | 生效开始时间 |
| effective_to | datetime | 生效结束时间（可为空） |
| status | enum | `active`/`expired` |

**业务规则**：
- 每次原始汇率更新或点差配置变更时，生成新的生效汇率记录
- 同一币种对同一时间只有一条 `active` 记录
- 旧记录自动标记为 `expired` 并记录 `effective_to`
- 生效汇率保留历史快照，支持时间点查询

**发布流程**：
1. 定时任务拉取原始汇率
2. 查询当前生效的点差配置
3. 计算生效汇率
4. 写入 `exchange_rate_effective` 表
5. 将旧记录标记为 `expired`

---

### 2.5 汇率查询 API

**功能描述**：为业务系统提供汇率查询接口。

**接口 1：查询当前生效汇率**

```http
GET /api/v1/exchange-rates/current
```

**请求参数**：
- `target_currency`（可选）：目标货币代码，不传则返回所有币种

**响应示例**：
```json
{
  "base_currency": "USD",
  "rates": [
    {
      "target_currency": "CNY",
      "effective_rate": 7.2500,
      "effective_from": "2026-04-29T10:00:00Z"
    },
    {
      "target_currency": "EUR",
      "effective_rate": 0.9200,
      "effective_from": "2026-04-29T10:00:00Z"
    }
  ]
}
```

**接口 2：查询历史汇率**

```http
GET /api/v1/exchange-rates/history
```

**请求参数**：
- `target_currency`（必填）：目标货币代码
- `date`（必填）：查询日期（YYYY-MM-DD）

**响应示例**：
```json
{
  "base_currency": "USD",
  "target_currency": "CNY",
  "effective_rate": 7.2300,
  "effective_from": "2026-04-28T10:00:00Z",
  "effective_to": "2026-04-29T10:00:00Z"
}
```

**业务规则**：
- 查询接口仅返回 `active` 状态的生效汇率
- 历史查询根据 `effective_from` 和 `effective_to` 时间范围匹配
- 接口响应时间 < 100ms（需加缓存）

---

### 2.6 汇率变动监控

**功能描述**：监控汇率异常波动并告警。

**监控规则**：
- **波动阈值告警**：单次汇率变动超过 ±5% 时触发告警
- **数据源失败告警**：连续 3 次拉取失败时触发告警
- **数据延迟告警**：超过预期拉取间隔 2 倍未更新时触发告警

**告警方式**：
- 发送邮件/企业微信通知给运营团队
- 记录告警日志到 `exchange_rate_alert` 表

**核心字段**（表：`exchange_rate_alert`）：

| 字段 | 类型 | 说明 |
|------|------|------|
| alert_type | enum | `volatility`/`source_failure`/`data_delay` |
| currency | char(3) | 相关货币 |
| old_rate | decimal(18,8) | 变动前汇率 |
| new_rate | decimal(18,8) | 变动后汇率 |
| change_percent | decimal(10,4) | 变动百分比 |
| alert_message | text | 告警详情 |
| created_at | datetime | 告警时间 |

---

## 三、数据模型

### 3.1 核心表结构

**表关系图**：

```
exchange_rate_source (数据源配置)
         ↓
exchange_rate_raw (原始汇率)
         ↓
exchange_rate_spread (点差配置)
         ↓
exchange_rate_effective (生效汇率) → 业务系统调用
         ↓
exchange_rate_alert (异常告警)
```

### 3.2 数据流转

1. **定时任务** 从 `exchange_rate_source` 读取配置
2. 调用外部 API 获取原始汇率，写入 `exchange_rate_raw`
3. 读取 `exchange_rate_spread` 当前生效的点差配置
4. 计算生效汇率，写入 `exchange_rate_effective`
5. 检查汇率变动，触发告警写入 `exchange_rate_alert`
6. 业务系统通过 API 查询 `exchange_rate_effective`

---

## 四、非功能需求

### 4.1 性能要求

- **API 响应时间**：P99 < 100ms
- **数据更新频率**：每 15 分钟拉取一次（可配置）
- **并发支持**：支持 1000 QPS 查询

### 4.2 可用性要求

- **服务可用性**：99.9%
- **数据源容灾**：主备自动切换，切换时间 < 1 分钟
- **缓存策略**：Redis 缓存生效汇率，TTL = 5 分钟

### 4.3 安全要求

- **API 鉴权**：内部服务调用需携带 API Key
- **数据加密**：敏感配置（API Key）加密存储
- **操作审计**：点差配置变更记录操作人和时间

### 4.4 监控与告警

- **关键指标**：
  - 汇率拉取成功率
  - API 调用量与响应时间
  - 汇率变动幅度
- **告警渠道**：企业微信 + 邮件
- **日志保留**：操作日志保留 180 天

---

## 五、实施计划

### 5.1 MVP 阶段（第一期）

**目标**：上线基础汇率查询服务

**功能范围**：
- ✅ 接入 1 个主数据源（如 Fixer.io）
- ✅ 支持 USD → CNY/EUR/GBP 三个币种
- ✅ 提供当前汇率查询 API
- ✅ 基础点差配置（百分比型）
- ✅ 汇率波动告警（±5% 阈值）

**技术实现**：
- 后端：Spring Boot + MySQL
- 缓存：Redis
- 定时任务：Spring Scheduler

**上线时间**：2 周

---

### 5.2 第二期优化

**功能增强**：
- 接入备用数据源，实现主备切换
- 支持更多币种（10+ 币种）
- 提供历史汇率查询 API
- 运营后台：点差配置管理界面
- 数据源健康度监控面板

**上线时间**：MVP 后 4 周

---

### 5.3 第三期扩展

**高级功能**：
- 支持固定值型点差
- 汇率变动趋势分析
- 自动化点差调整建议
- 与支付网关汇率对比

**上线时间**：待业务验证后评估

---

## 六、风险与依赖

### 6.1 外部依赖

- **汇率数据源**：依赖第三方 API 稳定性（需签订 SLA）
- **支付网关**：需与支付网关汇率保持一致性（误差 < 0.5%）

### 6.2 技术风险

- **数据源限流**：免费 API 可能有调用次数限制，需评估付费方案
- **汇率延迟**：外部 API 更新延迟可能导致价格不一致
- **缓存穿透**：高并发场景下需防止缓存失效导致数据库压力

### 6.3 业务风险

- **汇率剧烈波动**：极端行情下点差配置可能失效，需人工介入
- **用户投诉**：汇率与第三方平台差异过大可能引发用户质疑

---

## 七、附录

### 7.1 参考文档

- [Looply 汇率管理研究文档](looply-汇率管理-研究文档-v1.0.md)
- [Looply 架构设计图](looply-汇率管理-架构图-v1.0.png)
- [Looply ER 图](looply-汇率管理-ER图-v1.0.png)
- [Looply v3 原型](looply-汇率管理-v3原型.png)

### 7.2 术语表

| 术语 | 英文 | 说明 |
|------|------|------|
| 基准货币 | Base Currency | 汇率换算的基准，Looply 使用 USD |
| 目标货币 | Target Currency | 需要换算到的货币 |
| 原始汇率 | Raw Rate | 从数据源获取的未加工汇率 |
| 点差 | Spread | 平台在原始汇率基础上加减的调整值 |
| 生效汇率 | Effective Rate | 应用点差后实际使用的汇率 |

---

**文档结束**
