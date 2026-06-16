# Looply 地址库管理 — 需求分析报告 v2.1

> 版本：v2.1 | 日期：2026-05-13 | 作者：产品架构组

---

## 版本更新说明

### v2.0 主要变更（2026-05-08）

1. **引入版本分层**：将原 v1.0 的全量设计拆分为 MVP → V1.1 → V2 → V3 四个阶段
2. **MVP 聚焦美国单国**：砍掉多国家、多语言、ES 搜索、规则引擎、审计平台等非必要设计
3. **明确"不做什么"**：列出 MVP 阶段明确不做的能力，避免过度设计
4. **简化技术方案**：移除 Redis/ES 等中间件依赖描述，技术选型由开发团队决定
5. **调整成本估算**：按 MVP 实际调用量重新估算

### v2.1 主要变更（2026-05-13）

1. **校验架构重构**：必填性（required/optional/hidden）归 country_address_config.field_config 统一管理，address_field_validation_rules 只负责格式/长度校验
2. **多规则校验模型**：同一字段支持多条校验规则，新增 rule_type（pattern/length/custom）和 priority 字段
3. **field_config 结构显式化**：JSON 中使用 required_level 替代原 required boolean，支持三态（required/optional/hidden）

---

## 一、模块概述

### 1.1 模块定位

地址库管理是 Looply 平台的**轻基础服务**，核心职责：

- 为美国用户提供流畅的地址填写体验（Google Autocomplete）
- 存储结构化地址数据，供订单和物流消费
- 基础格式校验，降低无效地址率

### 1.2 业务背景

Looply 面向美国市场的跨境二手奢侈品电商，当前阶段核心目标是：

> **美国用户顺利完成「浏览 → 下单 → 发货 → 收货」闭环**

地址模块在整个链路中的角色：
- 不是核心竞争力，但是下单闭环的必要环节
- 地址错误直接导致退件（行业退件率 5-8%）
- 复杂地址表单导致弃单（行业弃单率 15-25%）

### 1.3 设计原则

| 原则 | 说明 |
|------|------|
| 先跑通再优化 | MVP 只做美国，验证闭环后再扩展 |
| 依赖成熟服务 | 重度依赖 Google Places，不自建 |
| 最小字段集 | 只收集下单必要字段，不过度收集 |
| 预留钩子不预建系统 | 存 place_id、verified 等为后续预留，但不提前建去重/风控系统 |
| 国家数据统一管理 | 国家可用性引用 market 模块，地址库不独立维护国家列表 |

### 1.4 目标用户

| 角色 | MVP 场景 |
|------|----------|
| C端买家 | 填写收货地址、管理地址簿、设置默认地址 |
| 物流系统 | 消费地址数据生成面单 |

MVP 不涉及：卖家地址、运营后台地址管理、风控系统。

---

## 二、版本规划（核心变更）

### 总览

| 版本 | 目标 | 核心能力 | 不做 |
|------|------|----------|------|
| **MVP** | 美国用户顺利下单 | 美国地址结构（超集字段）+ Google Autocomplete + CRUD + 基础校验 + snapshot + place_id + billing address + 前端 i18n | 多国家启用、Address Validation、规则引擎、ES、风控、审计 |
| **V1.1** | 降低物流失败率 | ZIP-city-state 匹配 + Address Validation（仅高风险订单）+ 地址去重 | 多国家、后台配置中心 |
| **V2** | 欧洲/中东扩展 | UK/EU/中东地址结构 + 多国字段配置 + 地址数据多语言 | 日本、地址画像 |
| **V3** | 平台化 | 后台配置中心 + 审计日志 + 风控联动 + 地址智能 | — |

### MVP 明确不做

| 不做的事 | 原因 |
|----------|------|
| ES 搜索 | PostgreSQL 足够，用户地址簿不超过 10 条 |
| 地址相似度检测 | 后期优化项，MVP 用户量小 |
| Address Validation API | 成本高、复杂、ROI 不确定（verified 字段已预留） |
| 后台正则规则引擎 | 写死即可，美国地址格式固定 |
| GDPR 导出 / 审计日志平台 | 数据量小、美国优先、CCPA 只需支持删除 |
| 风控联动 | 还没到风控阶段 |
| 启用非美国国家配置 | 数据模型已支持多国，但 MVP 只启用美国 |
| 地址数据多语言存储 | 美国地址不需要多语言存储（前端 i18n 界面多语言 MVP 会做） |
| 地址标准化建议 | V1.1 再做 |
| 邮编反查城市/州 | V1.1 再做 |

---

## 三、MVP 详细设计

### 3.1 数据模型设计原则

**核心原则：超集字段 + 国家配置**

虽然 MVP 只支持美国，但数据模型从一开始就采用**超集字段设计**，避免后续扩展时改表结构。通过**国家配置**控制哪些字段在前端展示、哪些必填。

| 设计层 | MVP 做法 | 扩展时 |
|--------|----------|--------|
| 数据库表结构 | 包含所有国家可能用到的字段（超集） | 不改表 |
| 国家配置表 | 只配置美国的字段规则 | 新增国家配置记录 |
| 前端表单 | 根据 country_code 动态渲染字段 | 读取新国家配置 |

### 3.2 地址数据模型（超集设计）

```
address {
  id              UUID        主键
  user_id         UUID        关联用户
  country_code    String(2)   ISO 3166-1 alpha-2 国家代码（MVP 固定 "US"）
  address_type    String(20)  地址类型：shipping / billing（支付 AVS 校验需要 billing）
  
  -- 收件人信息
  recipient_first_name     String(50)  收件人名
  recipient_last_name      String(50)  收件人姓
  recipient_name           String(100) 完整姓名（冗余拼接，用于展示）
  phone_country            String(5)   电话国家区号（MVP 固定 "+1"）
  phone_number             String(20)  电话号码（E.164 格式）
  alternate_phone_country  String(5)   备用电话区号（中东等地区需要，MVP 不用）
  alternate_phone_number   String(20)  备用电话号码（MVP 不用）
  
  -- 地址行（通用）
  address_line1   String(200) 地址行1（街道门牌号）
  address_line2   String(200) 地址行2（Apt/Suite/Unit 等）
  
  -- 行政区划（超集字段）
  city            String(100) 城市/Town
  state_province  String(100) 州/省/县（MVP 存美国州缩写，如 NY）
  postal_code     String(20)  邮编/ZIP/Postcode
  district        String(100) 区/町（日本等亚洲地址，MVP 不用）
  building_name   String(100) 建筑名称（日本地址，MVP 不用）
  
  -- 元数据
  is_default      Boolean     是否默认地址
  place_id        String(300) Google Place ID（预留去重/标准化）
  latitude        Decimal     纬度（Autocomplete 自动获取）
  longitude       Decimal     经度（Autocomplete 自动获取）
  
  -- 验证状态（预留）
  verified        Boolean     是否经过三方验证（默认 false，V1.1 启用）
  verified_at     Timestamp   验证时间
  verified_source String(50)  验证来源（google/usps/loqate）
  
  created_at      Timestamp
  updated_at      Timestamp
}
```

**MVP 阶段字段使用情况**：
- ✅ **使用**：country_code, address_type, recipient_first_name, recipient_last_name, recipient_name, phone_country, phone_number, address_line1, address_line2, city, state_province, postal_code, is_default, place_id, latitude, longitude
- ⏸️ **预留不用**：alternate_phone_*（中东扩展）、district, building_name（日本扩展）、verified_*（V1.1 Address Validation 启用）

**姓名字段设计说明**：
- `recipient_first_name` + `recipient_last_name`：拆分存储，支持支付网关 AVS 校验和物流 API
- `recipient_name`：冗余存储拼接结果，用于前端展示
- 拼接顺序由 `country_address_config.name_format` 控制（美国 first_last，日本 last_first）

**MVP 地址类型说明**：
- `shipping`：收货地址，用户地址簿管理
- `billing`：账单地址，支付网关 AVS 校验需要。前端提供"Same as shipping"选项，用户可复用收货地址

**与 v1.0 对比砍掉的字段**：
- `label`（地址标签）— MVP 不需要
- `raw_input` — 不做审计

### 3.3 地址字段注册表（v1.5 新增）

`address_field_registry` 是地址字段的**单一事实来源**，解决"后台配置国家地址时，怎么知道有哪些字段可以启用"的问题。

**设计动机**：
- `country_address_config.field_config` 的 JSON key 必须是注册表中已有的 `field_name`
- `address_field_validation_rules.field_name` 也引用注册表，形成闭环
- 后台"国家地址配置"编辑页面的字段列表从此表读取，运营不需要手写 field_name
- 通过 `admin_division_level` 字段声明与行政区划的映射关系，数据驱动，不硬编码

```
address_field_registry {
  id                    UUID        主键
  field_name            String(50)  字段标识（= address 表列名）  唯一约束
  field_type            String(20)  字段类型（text / select / phone）
  category              String(20)  分类（recipient / address / geo）
  display_name          String(100) 后台展示名（给运营看）
  admin_division_level  Int NULL    关联行政区划层级（NULL=不关联，1=州/省，2=市，3=区）
  max_length            Int         数据库列最大长度
  description           String(200) 后台说明
  created_at            Timestamp
}
```

**完整字段注册数据（含预留字段）**：

| field_name | field_type | category | display_name | admin_division_level | max_length | 备注 |
|---|---|---|---|---|---|---|
| recipient_first_name | text | recipient | First Name | NULL | 50 | MVP 使用 |
| recipient_last_name | text | recipient | Last Name | NULL | 50 | MVP 使用 |
| phone_number | phone | recipient | Phone | NULL | 20 | MVP 使用 |
| alternate_phone_country | text | recipient | Alt Phone Country | NULL | 5 | 中东预留 |
| alternate_phone_number | phone | recipient | Alt Phone | NULL | 20 | 中东预留 |
| address_line1 | text | address | Street Address | NULL | 200 | MVP 使用 |
| address_line2 | text | address | Apt / Suite / Unit | NULL | 200 | MVP 使用 |
| city | text | address | City | 2 | 100 | MVP 使用，关联 L2 行政区划 |
| state_province | select | address | State / Province | 1 | 100 | MVP 使用，关联 L1 行政区划 |
| postal_code | text | address | ZIP / Postal Code | NULL | 20 | MVP 使用 |
| district | text | address | District | 3 | 100 | 亚洲地址预留，关联 L3 |
| building_name | text | address | Building Name | NULL | 100 | 日本地址预留 |

**行政区划映射说明**：
- `admin_division_level` 不为 NULL 时，前端渲染该字段为下拉选择（`field_type=select`）
- 前端查询：`GET /api/v1/administrative-divisions?country_code=US&level={admin_division_level}`
- 例如：`state_province` 的 `admin_division_level=1`，前端查 level=1 的行政区划填充 State 下拉
- 不同国家可灵活配置：美国不用 district（hidden），日本启用 district 并关联 L3

**关系链**：
```
address_field_registry (字段有哪些)
       ↓ 引用
country_address_config.field_config (某国家启用哪些字段、是否可见)
       ↓ 引用
address_field_validation_rules (某国家某字段的格式校验规则)
       ↓ 对应
address 表列 (实际存储)
```

### 3.4 国家配置模型

控制各国地址字段的展示规则、校验规则、表单布局。

**与 market 模块的关系**：`country_code` 引用 market 系统的国家主数据（`market.countries`），地址库不独立维护国家列表。前端国家下拉选项读取 market 已启用的国家，地址库只负责该国家的地址字段配置。

```
country_address_config {
  id              UUID        主键
  country_code    String(2)   国家代码（引用 market.countries.country_code）
  enabled         Boolean     该国家地址功能是否启用（MVP 只有 US 为 true）
  
  -- 姓名配置
  name_format     String(20)  姓名拼接顺序（first_last / last_first）
  
  -- 字段配置（JSON）
  field_config    JSON        各字段的必填性规则（required_level: required/optional/hidden）
  field_order     JSON        前端表单字段顺序
  field_labels    JSON        字段 i18n key 映射（国家特定业务概念）
  
  -- 校验规则（格式/长度校验已移至 address_field_validation_rules 表）
  postal_regex    String      邮编正则（已废弃，保留兼容，实际校验走 validation_rules）
  phone_format    String      电话格式说明（展示用）
  
  created_at      Timestamp
  updated_at      Timestamp
}
```

**MVP 美国配置示例**：

```json
{
  "country_code": "US",
  "enabled": true,
  "name_format": "first_last",
  "field_config": {
    "recipient_first_name": { "required_level": "required", "visible": true },
    "recipient_last_name": { "required_level": "required", "visible": true },
    "phone_number": { "required_level": "required", "visible": true },
    "alternate_phone_number": { "required_level": "hidden", "visible": false },
    "address_line1": { "required_level": "required", "visible": true },
    "address_line2": { "required_level": "optional", "visible": true },
    "city": { "required_level": "required", "visible": true },
    "state_province": { "required_level": "required", "visible": true },
    "postal_code": { "required_level": "required", "visible": true },
    "district": { "required_level": "hidden", "visible": false },
    "building_name": { "required_level": "hidden", "visible": false }
  },
  "field_order": ["recipient_first_name", "recipient_last_name", "phone_number", "address_line1", "address_line2", "city", "state_province", "postal_code"],
  "field_labels": {
    "state_province": "address.field.state",
    "postal_code": "address.field.zipCode"
  },
  "postal_regex": "^\\d{5}(-\\d{4})?$",
  "phone_format": "+1 (XXX) XXX-XXXX"
}
```

**field_labels 说明**：
- 存储的是 i18n key，不是直接的文案
- 解决"不同国家业务概念不同"的问题（美国叫 State，英国叫 County）
- 前端根据用户选择的语言，查询对应的翻译文件
- 示例：`"state_province": "address.field.state"` → 前端查 `en-US.json` 得到 "State"，查 `es-US.json` 得到 "Estado"

**国家可用性联动规则**：
- `market.countries.enabled = false` → 该国家完全不可用，地址库也不可用
- `market.countries.enabled = true` + `country_address_config.enabled = true` → 地址功能可用
- 前端国家下拉列表：读取 `market.countries WHERE enabled = true`
- 地址表单渲染：读取 `country_address_config WHERE country_code = ? AND enabled = true`

### 3.5 行政区划数据模型

支持州/省下拉选择、邮编-城市映射等功能。

```
administrative_division {
  id              UUID        主键
  country_code    String(2)   国家代码
  level           Int         层级（1=州/省，2=城市，3=区/县）
  code            String(20)  行政区划代码（如美国州缩写 NY/CA）
  name            String(100) 名称
  name_local      String(100) 本地语言名称
  parent_id       UUID        父级ID（城市的父级是州）
  enabled         Boolean     是否启用
  sort_order      Int         排序
  
  created_at      Timestamp
  updated_at      Timestamp
}
```

**MVP 美国数据示例**：

| level | code | name | parent_id |
|-------|------|------|-----------|
| 1 | NY | New York | NULL |
| 1 | CA | California | NULL |
| 1 | TX | Texas | NULL |
| ... | ... | ... | ... |

**扩展时（UK）**：

| level | code | name | parent_id |
|-------|------|------|-----------|
| 1 | ENG | England | NULL |
| 2 | LDN | London | {England_id} |
| 2 | MAN | Manchester | {England_id} |

**MVP 阶段数据范围**：
- 只录入美国 50 州 + DC 的 level=1 数据
- 不录入城市级数据（V1.1 做邮编-城市映射时再补充）

### 3.6 邮编-城市映射表（V1.1 预留）

```
postal_code_mapping {
  id              UUID        主键
  country_code    String(2)   国家代码
  postal_code     String(20)  邮编
  city            String(100) 对应城市
  state_code      String(20)  州/省代码
  latitude        Decimal     中心点纬度
  longitude       Decimal     中心点经度
  
  created_at      Timestamp
  updated_at      Timestamp
}
```

**MVP 不做**，V1.1 加入后支持"输入邮编自动填充城市/州"功能。

### 3.7 地址 CRUD

| 操作 | 说明 |
|------|------|
| 新增 | 用户手动填写或通过 Autocomplete 填充后保存 |
| 编辑 | 修改已有地址任意字段 |
| 删除 | 软删除（已被订单 snapshot 引用的地址不受影响） |
| 列表 | 展示用户所有地址，默认地址置顶 |
| 设为默认 | 同一用户只有一个默认地址 |

**限制**：
- 每个用户最多 20 个地址
- 默认地址不可删除（需先取消默认）

### 3.8 Google Places Autocomplete

**为什么 MVP 必须做**：直接提升下单转化率，用户体验差异巨大。

**交互流程**：

```
用户在 address_line1 输入框键入
        ↓ 防抖 300ms
调用 Google Places Autocomplete API
（限定 country: "us", types: "address"）
        ↓
展示候选地址列表（最多 5 条）
        ↓
用户点击选择
        ↓
调用 Place Details API 获取结构化地址
        ↓
自动填充 address_line1, city, state, zip_code
（address_line2 留空让用户补充 Apt/Suite）
        ↓
用户确认/修改 → 保存
```

**关键实现要点**：
- 防抖 300ms，减少无效 API 调用
- Session Token：将多次 Autocomplete + 1 次 Details 合并计费（$7/session vs 分开 $10+）
- 国家限制：`componentRestrictions: { country: 'us' }`
- 降级策略：Google API 不可用时，退化为纯手动输入，不阻断下单

**字段映射**：

| Google address_component | 映射到 | 说明 |
|--------------------------|--------|------|
| street_number + route | address_line1 | 拼接为完整街道地址 |
| subpremise | address_line2 | 如有则预填 |
| locality | city | 城市 |
| administrative_area_level_1 (short_name) | state | 州缩写 |
| postal_code | zip_code | 邮编 |

### 3.9 基础格式校验

MVP 只做硬校验，不做智能建议。

**校验架构**：
- **必填性**：由 `country_address_config.field_config.required_level` 统一管理（required/optional/hidden）
- **格式/长度校验**：由 `address_field_validation_rules` 管理，rule_type 为 pattern/length/custom，按 priority 顺序执行
- **执行端区分（v1.5 新增）**：`execute_on` 字段标识规则在哪端执行（client/server/both）
- **严重程度（v1.5 新增）**：`severity` 字段区分硬拦截（error）和软提示（warning）

```
address_field_validation_rules {
  id                      UUID        主键
  country_code            String(2)   国家代码
  field_name              String(50)  字段名（引用 address_field_registry.field_name）
  rule_type               String(20)  规则类型（pattern / length / custom）
  priority                Int         执行优先级（值小先执行）
  pattern                 String      正则表达式（pattern/custom 时使用）
  min_length              Int         最小长度（length 时使用）
  max_length              Int         最大长度（length 时使用）
  execute_on              String(10)  执行端（client=前端实时 / server=后端提交 / both=前后端都执行）
  severity                String(10)  严重程度（error=硬拦截 / warning=软提示）
  error_message           String(200) 错误提示文案
  error_message_i18n_key  String(100) 多语言 key
  enabled                 Boolean     是否启用
  created_at              Timestamp
  updated_at              Timestamp
}
```

**前端校验规则 API**：后端提供 `GET /api/v1/address-config/{country_code}/validation-rules?execute_on=client` 接口，前端启动时加载，按 priority 顺序执行，命中首个失败即显示对应 error_message。

| 字段 | 必填性(field_config) | 格式校验(validation_rules) | 前端时机 |
|------|---------------------|--------------------------|----------|
| recipient_first_name | required | length: 1-50 字符 | 提交时 |
| recipient_last_name | required | length: 1-50 字符 | 提交时 |
| phone_number | required | pattern: 美国手机号 10 位数字 | 失焦时 |
| address_line1 | required | length: 5-200 字符 | 提交时 |
| address_line2 | optional | length: 0-200 字符 | — |
| city | required | length: 2-100 字符 | 提交时 |
| state | required | pattern: 美国 50 州 + DC 有效缩写 | 提交时 |
| zip_code | required | pattern: `^\d{5}(-\d{4})?$` | 失焦时 |

**校验策略**：
- 前端：实时格式校验（输入/失焦）
- 后端：先判必填性（读 field_config），再按 priority 执行格式/长度规则（读 validation_rules）
- 不做：邮编-城市-州匹配校验（V1.1）、Address Validation（V1.1）

### 3.10 Address Snapshot（关键）

**为什么 MVP 必须做**：订单创建后用户可能修改/删除地址，物流面单必须使用下单时的地址。

**机制**：
- 订单创建时，订单模块调用地址库 API 读取地址数据
- 订单模块在自己的数据库中创建快照（snapshot）
- 快照与订单绑定，不受原地址后续修改/删除影响
- 物流系统读取快照数据，不读取实时地址

**职责边界**：
- ✅ **地址库职责**：提供地址数据读取接口（GET /api/v1/addresses/{id}）
- ✅ **订单模块职责**：创建和管理 order_address_snapshot 表
- ❌ **地址库不负责**：快照的创建、存储、管理

**数据模型**（订单模块管理）：

```
order_address_snapshot {
  id              UUID        主键
  order_id        UUID        关联订单
  address_id      UUID        来源地址ID（可追溯）
  address_type    String(20)  shipping / billing
  recipient_first_name  String  收件人名
  recipient_last_name   String  收件人姓
  phone_number    String
  address_line1   String
  address_line2   String
  city            String
  state           String
  zip_code        String
  place_id        String      快照时的 place_id
  snapshot_at     Timestamp   快照时间
}
```

**说明**：此表由订单模块管理，不在地址库 ER 图中体现。

### 3.11 place_id 存储（预留钩子）

**为什么 MVP 要存**：
- 后续地址去重：同一个 place_id = 同一个物理地址
- 后续地址标准化：通过 place_id 可随时获取 Google 最新标准化结果
- 后续风控：多账户使用同一 place_id 是风险信号
- 成本为零：Autocomplete 流程中自然获得，只需存储

**MVP 阶段不基于 place_id 做任何逻辑**，纯存储预留。

### 3.12 前端多语言（i18n）

**为什么 MVP 要做**：美国约 18% 人口为西班牙语用户，前端界面多语言直接影响用户体验和转化率。

**范围界定**：
- ✅ **MVP 做**：前端界面多语言（表单标签、按钮文案、错误提示、placeholder）
- ❌ **MVP 不做**：地址数据多语言存储（如日文地址需要存罗马音 + 日文两种形式，V2 再做）

**实现方式**：前端 i18n（国际化），不涉及数据库改动。

| 层面 | 说明 |
|------|------|
| 翻译文件 | 前端维护 `en-US.json`、`es-US.json` 等语言包 |
| 代码调用 | 所有界面文案通过 `t('key')` 函数渲染，不硬编码 |
| 语言切换 | 根据浏览器语言自动匹配，或用户手动切换 |
| 数据库 | 无需改动，用户输入的地址数据与界面语言无关 |

**MVP 支持语言**：
- `en-US`（英文，默认）
- `es-US`（美国西班牙语）

---

## 四、前端交互设计

### 4.1 地址表单布局（美国）

```
┌─────────────────────────────────────────────┐
│  First Name                                  │
│  [____________________________________]      │
│                                              │
│  Last Name                                   │
│  [____________________________________]      │
│                                              │
│  Phone Number                                │
│  [+1] [____________________________________] │
│                                              │
│  Address Line 1 (Street address)             │
│  [____________________________________] ← Autocomplete 触发点
│                                              │
│  Address Line 2 (Apt, Suite, Unit, etc.)     │
│  [____________________________________]      │
│                                              │
│  City              State ▼      ZIP Code     │
│  [____________]    [__]         [_________]  │
│                                              │
│  ☐ Set as default address                    │
│                                              │
│  [Cancel]                    [Save Address]  │
└─────────────────────────────────────────────┘
```

### 4.2 Autocomplete 下拉交互

- 用户在 Address Line 1 输入 3+ 字符后触发
- 下拉列表最多 5 条候选
- 候选项格式：`街道地址, 城市, 州 邮编`
- 选中后自动填充 city/state/zip_code，光标跳到 address_line2
- 用户可修改任何自动填充的字段

### 4.3 地址列表页

```
┌─────────────────────────────────────────────┐
│  My Addresses                    [+ Add New] │
│─────────────────────────────────────────────│
│  ★ Default                                   │
│  John Smith                                  │
│  123 Main St, Apt 4B                         │
│  New York, NY 10001                          │
│  +1 (212) 555-0123                           │
│  [Edit]  [Delete]  [Set as Default]          │
│─────────────────────────────────────────────│
│  Jane Smith                                  │
│  456 Oak Ave                                 │
│  Los Angeles, CA 90001                       │
│  +1 (310) 555-0456                           │
│  [Edit]  [Delete]  [Set as Default]          │
└─────────────────────────────────────────────┘
```

---

## 五、与下游模块的关系

### 5.1 职责边界

| 模块 | 职责 | MVP 是否涉及 |
|------|------|-------------|
| 地址库 | 地址存储、格式校验、Autocomplete、提供地址读取接口 | ✅ |
| 订单模块 | 读取地址数据、创建和管理 order_address_snapshot | ✅ |
| 物流模块 | 消费 snapshot 数据、PO Box 检测、Zone 映射、运费计算 | ✅（物流模块自己负责） |
| 风控模块 | 地址黑名单、异常检测 | ❌ MVP 不涉及 |

### 5.2 数据流向（MVP）

```
用户填写/选择地址 → 地址库（校验 & 存储）
                          ↓
                    返回 address_id
                          ↓
用户下单 → 订单模块读取地址数据 → 订单模块创建 snapshot → 物流模块消费 snapshot
```

**说明**：
- 地址库只负责提供地址数据的读取接口（GET /api/v1/addresses/{id}）
- snapshot 的创建和管理由订单模块负责
- 地址库不感知 snapshot 的存在

### 5.3 接口预留（MVP 最小集）

```
GET    /api/v1/users/{user_id}/addresses          获取用户地址列表
GET    /api/v1/addresses/{id}                     获取单个地址
POST   /api/v1/addresses                          创建地址
PUT    /api/v1/addresses/{id}                     更新地址
DELETE /api/v1/addresses/{id}                     删除地址（软删除）
POST   /api/v1/addresses/{id}/set-default         设为默认
POST   /api/v1/orders/{order_id}/address-snapshot  创建订单地址快照
```

---

## 六、依赖与风险

### 6.1 外部依赖

| 依赖 | 用途 | 风险 | 缓解 |
|------|------|------|------|
| Google Places API | Autocomplete + Details | API 故障/限流 | 降级为手动输入 |

MVP 阶段**不依赖**：Address Validation API、USPS 邮编数据库、Loqate。

### 6.2 内部依赖

| 依赖模块 | 提供内容 | 说明 |
|----------|----------|------|
| 用户模块 | user_id | 地址归属 |
| 订单模块 | 触发 snapshot | 下单时冻结地址 |

### 6.3 风险评估

| 风险 | 影响 | 应对 |
|------|------|------|
| Google API 故障 | 无法自动填充 | 降级手动输入，不阻断下单 |
| 用户填错地址 | 物流退件 | MVP 接受一定退件率，V1.1 加 Validation |
| 地址格式不规范 | 面单打印异常 | 基础校验兜底 |

---

## 七、成本估算（MVP）

### Google Maps Platform 费用

按 MVP 阶段月活 1 万用户、平均每人 2 次地址操作估算：

| API | 单价 | 预估月调用量 | 月费用 |
|-----|------|-------------|--------|
| Places Autocomplete (Session) | $7/session | 2 万次 | $140 |
| **合计** | | | **~$140/月** |

说明：使用 Session Token 模式，Autocomplete + Details 合并为一次 session 计费。

对比 v1.0 报告的 $2,165/月，MVP 成本降低 93%。

---

## 八、后续版本能力预览

以下能力已在 v1.0 调研报告中完成分析，确认可行，按业务节奏分批落地：

### V1.1（订单稳定后）
- ZIP-city-state 匹配校验
- Google Address Validation（仅高风险订单）
- 基于 place_id 的地址去重提示
- 地址标准化建议（缩写规范化）

### V2（欧洲/中东扩展）
- UK/EU/中东地址结构（Postcode、County、alternate_phone 等）
- 多国字段动态配置（启用更多国家的 country_address_config）
- 地址数据多语言存储（日文罗马音 + 本地语言）
- Loqate 备选数据源

### V3（平台化）
- 后台校验规则配置中心
- 审计日志与数据导出
- 风控联动（地址黑名单、异常检测）
- 地址使用历史与画像
- 地址相似度检测

---

## 九、安全与合规（MVP 最小集）

| 要求 | MVP 做法 |
|------|----------|
| 数据传输加密 | 全链路 HTTPS |
| 敏感字段存储 | phone_number 加密存储 |
| 用户数据删除 | 支持用户请求删除地址（CCPA 基本要求） |
| 日志脱敏 | 日志中地址信息做掩码 |

MVP 不做：GDPR 合规（不涉及欧洲用户）、完整审计日志平台、数据导出功能。

---

## 附录

### A. 参考竞品

| 平台 | 地址方案 | 启示 |
|------|----------|------|
| Shopify（初期） | Google Places + 基础校验 | **MVP 对标**：薄、简单、强依赖 Google |
| The RealReal | Google Places | 同为奢侈品电商，地址流程简洁 |
| Amazon | 自建 + USPS | 亿级订单后演化的结果，不是起步方案 |

### B. v1.0 调研报告保留说明

v1.0 调研报告（`looply-地址库管理-需求分析报告-v1.0.md`）作为完整技术调研存档保留，其中的多国地址字段设计、三方服务对比、校验规则详情等内容在后续版本落地时仍有参考价值。

### C. Google Maps API 接入清单（MVP）

1. 创建 Google Cloud 项目
2. 启用 Places API（含 Autocomplete + Details）
3. 创建 API Key，配置域名白名单
4. 设置月度预算告警（$200 阈值）
5. 前端集成 Places JS SDK（Autocomplete widget）
