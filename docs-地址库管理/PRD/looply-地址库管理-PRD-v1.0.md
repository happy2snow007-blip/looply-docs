# Looply 地址库管理模块 PRD

**文档版本**：v1.1
**创建日期**：2026-05-09
**更新日期**：2026-05-11
**产品负责人**：产品团队
**目标上线**：MVP 阶段
**原型版本**：地址库管理后台原型 v3
**变更说明**：v1.1 新增后端校验规则设计

---

## 一、概述

### 1.1 背景与目标

Looply 是面向美国市场的跨境二手奢侈品电商平台。地址库管理是平台的**轻基础服务**，核心职责：

- 为美国用户提供流畅的地址填写体验（Google Autocomplete）
- 存储结构化地址数据，供订单和物流消费
- 基础格式校验，降低无效地址率

地址模块在业务链路中的角色：
- 不是核心竞争力，但是下单闭环的必要环节
- 地址错误直接导致退件（行业退件率 5-8%）
- 复杂地址表单导致弃单（行业弃单率 15-25%）

**设计原则**：

| 原则 | 说明 |
|------|------|
| 先跑通再优化 | MVP 只做美国，验证闭环后再扩展 |
| 依赖成熟服务 | 重度依赖 Google Places，不自建 |
| 最小字段集 | 只收集下单必要字段，不过度收集 |
| 预留钩子不预建系统 | 存 place_id、verified 等为后续预留，但不提前建去重/风控系统 |
| 国家数据统一管理 | 国家可用性引用 market 模块，地址库不独立维护国家列表 |

### 1.2 不做什么

| 明确不做 | 原因 |
|----------|------|
| ES 搜索 | PostgreSQL 足够，用户地址簿不超过 10 条 |
| 地址相似度检测 | 后期优化项，MVP 用户量小 |
| Address Validation API | 成本高、复杂、ROI 不确定（verified 字段已预留） |
| 后台校验规则引擎 | MVP 前端写死即可，美国地址格式固定 |
| GDPR 导出 / 审计日志平台 | 数据量小、美国优先、CCPA 只需支持删除 |
| 风控联动 | 还没到风控阶段 |
| 启用非美国国家配置 | 数据模型已支持多国，但 MVP 只启用美国 |
| 地址数据多语言存储 | 美国地址不需要多语言存储（前端 i18n 界面多语言 MVP 会做） |
| 地址标准化建议 | V1.1 再做 |
| 邮编反查城市/州 | V1.1 再做 |
| 邮编映射管理 | V1.1 再做 |
| 后台用户地址列表 | 地址模块后台定位为配置中心，不管理用户数据 |

### 1.3 用户角色

| 角色 | MVP 场景 |
|------|----------|
| C端买家 | 填写收货地址、管理地址簿、设置默认地址 |
| 物流系统 | 消费地址数据生成面单 |
| 运营人员 | 通过后台配置国家地址字段规则、管理行政区划数据 |

### 1.4 核心场景

1. **地址填写**：用户在下单流程中填写收货地址，通过 Autocomplete 快速补全
2. **地址管理**：用户在个人中心管理地址簿，增删改查、设置默认地址
3. **下单快照**：订单创建时冻结地址数据，后续修改不影响已有订单
4. **后台配置**：运营配置美国地址字段的展示名称、必填规则、显示顺序
5. **区划维护**：运营通过批量导入维护美国州级行政区划数据

### 1.5 全局页面流转

**C端**：
```
地址列表页 ──「新增地址」──→ 地址表单页（Autocomplete 触发）
地址列表页 ──「编辑」──→ 地址表单页（回填已有数据）
下单流程 ──「选择地址」──→ 地址选择弹窗 ──「新增」──→ 地址表单页
```

**后台**：
```
国家地址配置列表 ──「编辑」──→ 国家配置编辑子页面（基本配置 + 前端展示字段 + 操作记录）
行政区划管理 ──「导入区划数据」──→ 文件上传（CSV/Excel）
行政区划管理 ──「启用/停用」──→ 切换状态
```

### 1.6 术语说明

| 术语 | 说明 |
|------|------|
| 超集字段 | 数据库包含所有国家可能用到的字段，通过国家配置控制展示 |
| 前端展示字段 | 合并了 field_config + field_order + field_labels 的统一配置 |
| place_id | Google Places 返回的地点唯一标识，预留用于去重和标准化 |
| Address Snapshot | 订单创建时冻结的地址副本，由订单模块管理 |
| name_format | 姓名拼接顺序配置（first_last / last_first） |
| market 模块 | 平台国家/市场管理模块，地址库引用其国家启用状态 |

---

## 二、需求详细描述

### 2.1 C端地址模块

#### 模块概述

为美国用户提供完整的地址填写和管理能力，集成 Google Places Autocomplete 提升填写效率，支持 shipping 和 billing 两种地址类型。

#### 2.1.1 地址表单（页面型）

**页面入口**：
- 地址列表页点击「新增地址」
- 下单流程中点击「新增收货地址」
- 地址列表页点击「编辑」（回填模式）

**页面布局**（美国）：

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
│  [____________________________________] ← Autocomplete
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

**字段说明**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| first_name | text | 是 | 收件人名，1-50 字符 |
| last_name | text | 是 | 收件人姓，1-50 字符 |
| phone | tel | 是 | 美国手机号，10 位数字，前缀 +1 固定 |
| address_line1 | text | 是 | 街道地址，5-200 字符，触发 Autocomplete |
| address_line2 | text | 否 | 公寓/套房号，0-200 字符 |
| city | text | 是 | 城市，2-100 字符 |
| state | select | 是 | 美国 50 州 + DC 下拉选择 |
| postal_code | text | 是 | ZIP Code，格式 `^\d{5}(-\d{4})?$` |
| is_default | checkbox | 否 | 是否设为默认地址 |

**交互逻辑**：
- 字段顺序和展示名称由后台 country_address_config 配置驱动
- State 字段为下拉选择，数据来源于 administrative_division 表
- 表单提交时前后端双重校验
- 编辑模式下回填已有数据，address_line1 不再触发 Autocomplete（除非用户清空重新输入）

**接口需求**：
- `POST /api/v1/addresses` — 创建地址
- `PUT /api/v1/addresses/{id}` — 更新地址

#### 2.1.2 地址列表（页面型）

**页面入口**：
- 个人中心 → 我的地址
- 下单流程 → 选择收货地址

**页面布局**：

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

**交互逻辑**：
- 默认地址置顶显示，带 ★ 标记
- 每个用户最多 20 个地址，达到上限后隐藏「新增」按钮
- 默认地址不可删除（需先取消默认）
- 删除操作需二次确认弹窗
- 下单流程中选择地址后自动返回订单页

**接口需求**：
- `GET /api/v1/users/{user_id}/addresses` — 获取用户地址列表

#### 2.1.3 地址 CRUD（机制型）

| 操作 | 说明 | 业务规则 |
|------|------|----------|
| 新增 | 用户手动填写或通过 Autocomplete 填充后保存 | 每用户上限 20 条 |
| 编辑 | 修改已有地址任意字段 | 已被订单 snapshot 引用的地址可正常修改 |
| 删除 | 软删除 | 默认地址不可删除；已被 snapshot 引用不受影响 |
| 设为默认 | 同一用户同类型只有一个默认地址 | shipping 和 billing 各一个默认 |

**接口需求**：
- `DELETE /api/v1/addresses/{id}` — 删除地址（软删除）
- `POST /api/v1/addresses/{id}/set-default` — 设为默认

#### 2.1.4 基础格式校验（机制型）

**前后端双重校验策略**

| 层级 | 职责 | 实现方式 | 原因 |
|------|------|----------|------|
| 前端校验 | 用户体验优化，即时反馈 | 实时格式校验（输入/失焦） | 减少无效提交，提升体验 |
| 后端校验 | 数据安全防线，不可绕过 | 提交时再次校验（不信任前端） | 防止恶意数据注入，保证数据质量 |

**为什么后端必须再次校验？**

1. **前端可以被完全绕过**
   - 浏览器开发者工具可以禁用 JS 校验
   - 攻击者可以直接调用 API，绕过前端
   - 移动端、第三方集成等多渠道输入

2. **数据安全防线**
   - 防止 XSS 攻击（`<script>alert(1)</script>`）
   - 防止 SQL 注入（`'; DROP TABLE users; --`）
   - 防止路径遍历（`../../etc/passwd`）

**字段校验规则详细说明**

| 字段 | 必填 | 长度 | 正则表达式 | 错误提示 | 前端时机 | 后端时机 |
|------|------|------|------------|----------|----------|----------|
| first_name | ✅ | 1-50 | `^[a-zA-ZÀ-ÿ\s'-]{1,50}$` | First name contains invalid characters | 失焦 | 提交 |
| last_name | ✅ | 1-50 | `^[a-zA-ZÀ-ÿ\s'-]{1,50}$` | Last name contains invalid characters | 失焦 | 提交 |
| phone | ✅ | 10-20 | `^\+?1?\s?\(?[2-9]\d{2}\)?[\s\-]?\d{3}[\s\-]?\d{4}$` | Invalid US phone format | 失焦 | 提交 |
| address_line1 | ✅ | 1-100 | `^[a-zA-Z0-9À-ÿ\s,.'#\-/]{1,100}$` | Address contains invalid characters | 提交 | 提交 |
| address_line2 | ❌ | 0-100 | `^[a-zA-Z0-9À-ÿ\s,.'#\-/]{0,100}$` | Address contains invalid characters | 提交 | 提交 |
| city | ✅ | 1-50 | `^[a-zA-ZÀ-ÿ\s'-]{1,50}$` | City name contains invalid characters | 提交 | 提交 |
| state_province | ✅ | 2 | `^[A-Z]{2}$` | Invalid state code | 提交 | 提交 |
| postal_code | ✅ | 5-10 | `^\d{5}(-\d{4})?$` | Invalid ZIP Code format | 失焦 | 提交 |

**正则表达式说明**

- `a-zA-Z` - 基础英文字母
- `À-ÿ` - 扩展拉丁字符（支持法语、西班牙语等带重音符号的名字，如 José、François）
- `\s` - 空格（支持复合名如 "Mary Jane"）
- `'-` - 连字符和撇号（支持 "O'Connor"、"Jean-Pierre"）
- `0-9` - 数字
- `,.'#\-/` - 地址常用标点符号

**测试用例示例**

```
✅ 合法输入：
- first_name: "John", "Mary Jane", "O'Connor", "Jean-Pierre", "José"
- phone: "(415) 555-1234", "415-555-1234", "+1 415 555 1234"
- address_line1: "123 Main Street", "456 Oak Ave, Apt 2B", "Building #5"
- postal_code: "94102", "94102-1234"

❌ 非法输入：
- first_name: "John123" (包含数字), "John@Smith" (特殊符号)
- phone: "123-456-7890" (区号不能以0或1开头)
- address_line1: "123 Main St <script>alert(1)</script>" (XSS攻击)
- postal_code: "9410" (长度不足), "941023" (长度过长)
```

**安全性考虑**

1. **防止 XSS 攻击**
   - 正则限制字符集，不允许 `<>` 等 HTML 标签字符
   - 后端使用 HTML 转义库（OWASP Java HTML Sanitizer）
   - 前端框架自动转义（React JSX）

2. **防止 SQL 注入**
   - 使用参数化查询（PreparedStatement）
   - ORM 框架（JPA/Hibernate）自动处理
   - 正则限制特殊字符，不允许 `;'"`

3. **防止路径遍历**
   - 正则不允许 `../` 模式
   - 后端不直接使用地址字段拼接文件路径

**国家特定校验规则**

后端通过 `address_field_validation_rules` 表动态加载各国家的校验规则：

| 国家 | phone 正则 | postal_code 正则 | state_province 正则 |
|------|-----------|-----------------|-------------------|
| US | `^\+?1?\s?\(?[2-9]\d{2}\)?[\s\-]?\d{3}[\s\-]?\d{4}$` | `^\d{5}(-\d{4})?$` | `^[A-Z]{2}$` |
| GB | `^\+?44\s?[1-9]\d{9,10}$` | `^[A-Z]{1,2}\d{1,2}[A-Z]?\s?\d[A-Z]{2}$` | `^[a-zA-Z\s'-]{0,50}$` |
| CA | `^\+?1?\s?\(?[2-9]\d{2}\)?[\s\-]?\d{3}[\s\-]?\d{4}$` | `^[A-Z]\d[A-Z]\s?\d[A-Z]\d$` | `^[A-Z]{2}$` |
| JP | `^\+?81\s?\d{1,4}[\s\-]?\d{1,4}[\s\-]?\d{4}$` | `^\d{3}-?\d{4}$` | `^[一-龥]{2,4}[都道府県]$` |

**校验失败响应示例**

```json
{
  "error": "VALIDATION_ERROR",
  "message": "Address validation failed",
  "details": [
    {
      "field": "phone",
      "error": "Invalid US phone format",
      "pattern": "^\\+?1?\\s?\\(?[2-9]\\d{2}\\)?[\\s\\-]?\\d{3}[\\s\\-]?\\d{4}$",
      "value": "123-456-7890"
    },
    {
      "field": "postal_code",
      "error": "Invalid ZIP Code format",
      "pattern": "^\\d{5}(-\\d{4})?$",
      "value": "9410"
    }
  ]
}
```

**MVP 不做**：
- 邮编-城市-州匹配校验（V1.1）
- Address Validation API（V1.1）
- 地址相似度检测（V1.1）

#### 2.1.5 Google Places Autocomplete（机制型）

**交互流程**：

```
用户在 address_line1 输入框键入 3+ 字符
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
自动填充 address_line1, city, state, postal_code
（address_line2 留空让用户补充 Apt/Suite）
        ↓
用户确认/修改 → 保存
```

**字段映射**：

| Google address_component | 映射到 | 说明 |
|--------------------------|--------|------|
| street_number + route | address_line1 | 拼接为完整街道地址 |
| subpremise | address_line2 | 如有则预填 |
| locality | city | 城市 |
| administrative_area_level_1 (short_name) | state | 州缩写 |
| postal_code | postal_code | 邮编 |

**关键实现要点**：
- Session Token：将多次 Autocomplete + 1 次 Details 合并计费（$7/session vs 分开 $10+）
- 国家限制：`componentRestrictions: { country: 'us' }`
- 降级策略：Google API 不可用时，退化为纯手动输入，不阻断下单

#### 2.1.6 Address Snapshot（机制型）

**职责边界**：
- ✅ **地址库职责**：提供地址数据读取接口（`GET /api/v1/addresses/{id}`）
- ✅ **订单模块职责**：创建和管理 order_address_snapshot 表
- ❌ **地址库不负责**：快照的创建、存储、管理

**机制说明**：
- 订单创建时，订单模块调用地址库 API 读取地址数据
- 订单模块在自己的数据库中创建快照（snapshot）
- 快照与订单绑定，不受原地址后续修改/删除影响
- 物流系统读取快照数据，不读取实时地址

---

### 2.2 后台配置模块

#### 模块概述

地址库后台定位为**配置中心**，管理各国家的地址字段展示规则和行政区划数据。MVP 阶段不包含用户地址数据的查看和管理功能。

#### 2.2.1 国家地址配置列表（页面型）

**页面入口**：后台侧边栏 → 地址配置 → 国家地址配置

**页面布局**：
- KPI 统计卡片：配置国家数、已启用、未启用、姓名格式数
- 筛选工具栏：启用状态筛选 + 查询按钮 + 新增国家配置按钮
- 数据表格

**字段说明**：

| 列名 | 说明 |
|------|------|
| 国家代码 | ISO 3166-1 alpha-2（如 US、GB） |
| 国家名称 | 中文名称 |
| 启用状态 | 启用/未启用 tag |
| 姓名格式 | first_last / last_first |
| 字段配置 | 已配置字段数量（如"8个字段"） |
| 操作 | 编辑按钮 → 跳转编辑子页面 |

**交互逻辑**：
- 点击「编辑」进入国家配置编辑子页面（showSubPage）
- 点击「新增国家配置」进入空白编辑子页面
- 国家代码下拉列表数据来源于 market 模块已启用的国家

#### 2.2.2 国家地址配置编辑（页面型）

**页面入口**：国家地址配置列表 → 点击「编辑」

**页面布局**：

1. **基本配置区**
   - 国家代码（只读）
   - 国家名称（只读）
   - 启用状态（下拉：启用/停用）
   - 姓名格式（下拉：first_last / last_first）

2. **前端展示字段区**（核心配置）

   统一表格，合并了字段可见性、必填规则、展示名称和顺序：

   | 顺序 | 字段名 | 展示名称 | 必填规则 | 状态 | 操作 |
   |------|--------|---------|---------|------|------|
   | 1 | first_name | First Name（可编辑） | 必填/选填/隐藏 | 显示 | ↑ ↓ |
   | 2 | last_name | Last Name（可编辑） | 必填/选填/隐藏 | 显示 | ↑ ↓ |
   | 3 | phone | Phone（可编辑） | 必填/选填/隐藏 | 显示 | ↑ ↓ |
   | 4 | address_line1 | Street Address（可编辑） | 必填/选填/隐藏 | 显示 | ↑ ↓ |
   | 5 | address_line2 | Apt / Suite（可编辑） | 必填/选填/隐藏 | 显示 | ↑ ↓ |
   | 6 | city | City（可编辑） | 必填/选填/隐藏 | 显示 | ↑ ↓ |
   | 7 | state_province | State（可编辑） | 必填/选填/隐藏 | 显示 | ↑ ↓ |
   | 8 | postal_code | ZIP Code（可编辑） | 必填/选填/隐藏 | 显示 | ↑ ↓ |

3. **操作按钮**：取消 + 保存

4. **操作记录**（页面底部）
   - 筛选：操作类型 + 操作人 + 日期范围 + 查询/重置
   - 表格列：操作时间、操作人、操作类型、操作内容
   - 分页

**交互逻辑**：
- 展示名称为可编辑 input，修改后保存时写入 country_address_config.field_labels
- 必填规则下拉选择"隐藏"时，状态列自动变为"隐藏"tag
- ↑↓ 按钮调整字段顺序，保存时写入 field_order
- 展示名称修改后需同步更新前端翻译文件（MVP 阶段后台直接存最终展示文本）
- 返回列表按钮：`navigateTo('country-config','国家地址配置')`

**接口需求**：
- `GET /api/v1/admin/country-address-configs` — 配置列表
- `GET /api/v1/admin/country-address-configs/{country_code}` — 单个配置详情
- `PUT /api/v1/admin/country-address-configs/{country_code}` — 更新配置

#### 2.2.3 行政区划管理（页面型）

**页面入口**：后台侧边栏 → 地址配置 → 行政区划管理

**页面布局**：
- KPI 统计卡片：区划总数、一级(州/省)、二级(城市)、覆盖国家
- 筛选工具栏：国家筛选 + 层级筛选 + 搜索代码/名称 + 查询按钮 + 导入区划数据按钮
- 数据表格

**字段说明**：

| 列名 | 说明 |
|------|------|
| 国家 | 国家代码 |
| 层级 | L1 州/省、L2 城市、L3 区/县 |
| 代码 | 行政区划代码（如 NY、CA） |
| 名称 | 英文名称 |
| 本地名称 | 中文名称（运营参考） |
| 父级 | 父级代码（L1 为 -） |
| 状态 | 启用/停用 |
| 排序 | 排序权重 |
| 操作 | 启用/停用切换按钮 |

**交互逻辑**：
- 数据为只读列表，不支持单条编辑（通过批量导入维护）
- 「导入区划数据」按钮触发文件上传（支持 CSV/Excel）
- 导入逻辑：全量覆盖指定国家的区划数据，或增量追加
- 操作列仅有启用/停用切换按钮
- MVP 只导入美国 50 州 + DC 的 L1 数据

**接口需求**：
- `GET /api/v1/admin/administrative-divisions` — 区划列表（支持筛选）
- `POST /api/v1/admin/administrative-divisions/import` — 批量导入
- `PUT /api/v1/admin/administrative-divisions/{id}/toggle` — 启用/停用切换
- `GET /api/v1/administrative-divisions?country_code=US&level=1` — C端获取州列表

---

## 三、数据模型

### 3.1 address 表（超集字段设计）

虽然 MVP 只支持美国，但数据模型采用超集字段设计，避免后续扩展时改表结构。

| 字段 | 类型 | 必填 | MVP 状态 | 说明 |
|------|------|------|----------|------|
| id | UUID | 是 | 使用 | 主键 |
| user_id | UUID | 是 | 使用 | 关联用户（FK） |
| country_code | String(2) | 是 | 使用 | ISO 3166-1 国家代码，MVP 固定 "US" |
| address_type | String(20) | 是 | 使用 | shipping / billing |
| recipient_first_name | String(50) | 是 | 使用 | 收件人名 |
| recipient_last_name | String(50) | 是 | 使用 | 收件人姓 |
| recipient_name | String(100) | 是 | 使用 | 完整姓名（冗余拼接，用于展示） |
| phone_country | String(5) | 是 | 使用 | 电话区号，MVP 固定 "+1" |
| phone_number | String(20) | 是 | 使用 | 电话号码（E.164 格式） |
| alternate_phone_country | String(5) | 否 | 预留 | 备用电话区号（中东扩展） |
| alternate_phone_number | String(20) | 否 | 预留 | 备用电话号码（中东扩展） |
| address_line1 | String(200) | 是 | 使用 | 地址行1（街道门牌号） |
| address_line2 | String(200) | 否 | 使用 | 地址行2（Apt/Suite/Unit） |
| city | String(100) | 是 | 使用 | 城市 |
| state_province | String(100) | 是 | 使用 | 州/省（MVP 存美国州缩写） |
| postal_code | String(20) | 是 | 使用 | 邮编 |
| district | String(100) | 否 | 预留 | 区/町（日本等亚洲地址） |
| building_name | String(100) | 否 | 预留 | 建筑名称（日本地址） |
| is_default | Boolean | 是 | 使用 | 是否默认地址 |
| place_id | String(300) | 否 | 使用 | Google Place ID |
| latitude | Decimal | 否 | 使用 | 纬度 |
| longitude | Decimal | 否 | 使用 | 经度 |
| verified | Boolean | 否 | 预留 | 是否经过三方验证（默认 false） |
| verified_at | Timestamp | 否 | 预留 | 验证时间 |
| verified_source | String(50) | 否 | 预留 | 验证来源（google/usps/loqate） |
| created_at | Timestamp | 是 | 使用 | 创建时间 |
| updated_at | Timestamp | 是 | 使用 | 更新时间 |

**姓名字段设计说明**：
- `recipient_first_name` + `recipient_last_name`：拆分存储，支持支付网关 AVS 校验和物流 API
- `recipient_name`：冗余存储拼接结果，拼接顺序由 `country_address_config.name_format` 控制

### 3.2 country_address_config 表

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | UUID | 是 | 主键 |
| country_code | String(2) | 是 | 国家代码（引用 market.countries，唯一） |
| enabled | Boolean | 是 | 是否启用 |
| name_format | String(20) | 是 | 姓名拼接顺序（first_last / last_first） |
| field_config | JSON | 是 | 各字段的必填/选填/隐藏规则 |
| field_order | JSON | 是 | 前端表单字段顺序 |
| field_labels | JSON | 是 | 字段展示名称 |
| created_at | Timestamp | 是 | 创建时间 |
| updated_at | Timestamp | 是 | 更新时间 |

**MVP 美国配置示例**：

```json
{
  "country_code": "US",
  "enabled": true,
  "name_format": "first_last",
  "field_config": {
    "first_name": { "required": true, "visible": true },
    "last_name": { "required": true, "visible": true },
    "phone": { "required": true, "visible": true },
    "address_line1": { "required": true, "visible": true },
    "address_line2": { "required": false, "visible": true },
    "city": { "required": true, "visible": true },
    "state_province": { "required": true, "visible": true },
    "postal_code": { "required": true, "visible": true }
  },
  "field_order": ["first_name", "last_name", "phone", "address_line1", "address_line2", "city", "state_province", "postal_code"],
  "field_labels": {
    "first_name": "First Name",
    "last_name": "Last Name",
    "phone": "Phone",
    "address_line1": "Street Address",
    "address_line2": "Apt / Suite",
    "city": "City",
    "state_province": "State",
    "postal_code": "ZIP Code"
  }
}
```

**说明**：MVP 阶段 field_labels 直接存储最终展示文本（Path A 方案），不存 i18n key。后续多语言扩展时再改为 i18n key + 翻译文件模式。

### 3.3 administrative_division 表

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | UUID | 是 | 主键 |
| country_code | String(2) | 是 | 国家代码（FK） |
| level | Int | 是 | 层级（1=州/省，2=城市，3=区/县） |
| code | String(20) | 是 | 行政区划代码（唯一） |
| name | String(100) | 是 | 名称 |
| name_local | String(100) | 否 | 本地语言名称 |
| parent_id | UUID | 否 | 父级ID（自引用） |
| enabled | Boolean | 是 | 是否启用 |
| sort_order | Int | 是 | 排序权重 |
| created_at | Timestamp | 是 | 创建时间 |
| updated_at | Timestamp | 是 | 更新时间 |

**MVP 数据范围**：只录入美国 50 州 + DC 的 level=1 数据。

### 3.4 address_field_validation_rules 表（新增）

用于存储各国家地址字段的后端校验规则，支持动态配置和多国扩展。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | UUID | 是 | 主键 |
| country_code | String(2) | 是 | 国家代码（FK → country_address_config） |
| field_name | String(50) | 是 | 字段名（first_name/last_name/phone等） |
| pattern | String(500) | 是 | 正则表达式 |
| error_message | String(200) | 是 | 校验失败提示（英文） |
| error_message_i18n_key | String(100) | 否 | 多语言错误提示 key（预留） |
| max_length | Int | 是 | 最大长度 |
| min_length | Int | 是 | 最小长度 |
| is_required | Boolean | 是 | 是否必填 |
| created_at | Timestamp | 是 | 创建时间 |
| updated_at | Timestamp | 是 | 更新时间 |

**唯一约束**：`(country_code, field_name)`

**MVP 美国配置示例**：

```sql
INSERT INTO address_field_validation_rules 
(country_code, field_name, pattern, error_message, max_length, min_length, is_required)
VALUES 
('US', 'first_name', '^[a-zA-ZÀ-ÿ\\s''-]{1,50}$', 'First name contains invalid characters', 50, 1, TRUE),
('US', 'last_name', '^[a-zA-ZÀ-ÿ\\s''-]{1,50}$', 'Last name contains invalid characters', 50, 1, TRUE),
('US', 'phone', '^\\+?1?\\s?\\(?[2-9]\\d{2}\\)?[\\s\\-]?\\d{3}[\\s\\-]?\\d{4}$', 'Invalid US phone format', 20, 10, TRUE),
('US', 'address_line1', '^[a-zA-Z0-9À-ÿ\\s,.''#\\-/]{1,100}$', 'Address contains invalid characters', 100, 1, TRUE),
('US', 'address_line2', '^[a-zA-Z0-9À-ÿ\\s,.''#\\-/]{0,100}$', 'Address contains invalid characters', 100, 0, FALSE),
('US', 'city', '^[a-zA-ZÀ-ÿ\\s''-]{1,50}$', 'City name contains invalid characters', 50, 1, TRUE),
('US', 'state_province', '^[A-Z]{2}$', 'Invalid state code', 2, 2, TRUE),
('US', 'postal_code', '^\\d{5}(-\\d{4})?$', 'Invalid ZIP Code format', 10, 5, TRUE);
```

**设计说明**：

1. **与 country_address_config 的关系**
   - `country_address_config.field_config` 控制字段的可见性和必填规则（前端展示层）
   - `address_field_validation_rules` 控制字段的格式校验规则（后端安全层）
   - 两者配合使用，前者决定"要不要显示"，后者决定"怎么校验"

2. **正则表达式存储**
   - 数据库中存储的正则需要转义（如 `\\d` 而不是 `\d`）
   - 后端读取后直接用于 Pattern.compile()
   - 前端通过 API 获取后转换为 JavaScript RegExp

3. **多语言支持**
   - MVP 阶段 error_message 直接存英文文本
   - error_message_i18n_key 预留，V1.1 支持多语言时使用

4. **性能优化**
   - 校验规则在应用启动时加载到内存缓存
   - 按国家代码索引，查询时间复杂度 O(1)
   - 配置更新后自动刷新缓存

---

## 四、接口设计

### 4.1 C端接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/users/{user_id}/addresses` | 获取用户地址列表 |
| GET | `/api/v1/addresses/{id}` | 获取单个地址 |
| POST | `/api/v1/addresses` | 创建地址（含后端校验） |
| PUT | `/api/v1/addresses/{id}` | 更新地址（含后端校验） |
| DELETE | `/api/v1/addresses/{id}` | 删除地址（软删除） |
| POST | `/api/v1/addresses/{id}/set-default` | 设为默认 |
| GET | `/api/v1/administrative-divisions` | 获取行政区划（C端下拉用） |
| GET | `/api/v1/country-address-configs/{code}` | 获取国家字段配置（C端表单渲染用） |
| GET | `/api/v1/validation-rules/{country_code}` | 获取国家字段校验规则（前端动态加载，新增） |

### 4.2 后台接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/admin/country-address-configs` | 配置列表 |
| GET | `/api/v1/admin/country-address-configs/{code}` | 单个配置详情 |
| PUT | `/api/v1/admin/country-address-configs/{code}` | 更新配置 |
| POST | `/api/v1/admin/country-address-configs` | 新增配置 |
| GET | `/api/v1/admin/administrative-divisions` | 区划列表（支持筛选分页） |
| POST | `/api/v1/admin/administrative-divisions/import` | 批量导入 |
| PUT | `/api/v1/admin/administrative-divisions/{id}/toggle` | 启用/停用 |
| GET | `/api/v1/admin/validation-rules` | 校验规则列表（新增） |
| GET | `/api/v1/admin/validation-rules/{country_code}` | 单个国家的校验规则（新增） |
| PUT | `/api/v1/admin/validation-rules/{country_code}/{field_name}` | 更新单个字段校验规则（新增） |
| POST | `/api/v1/admin/validation-rules/batch` | 批量创建校验规则（新增） |

### 4.3 关键接口详情

**POST /api/v1/addresses**

请求体：
```json
{
  "country_code": "US",
  "address_type": "shipping",
  "recipient_first_name": "John",
  "recipient_last_name": "Smith",
  "phone_country": "+1",
  "phone_number": "2125550147",
  "address_line1": "350 Fifth Avenue",
  "address_line2": "Suite 200",
  "city": "New York",
  "state_province": "NY",
  "postal_code": "10118",
  "is_default": true,
  "place_id": "ChIJtcaxrqlZwokR...",
  "latitude": 40.7484,
  "longitude": -73.9857
}
```

响应：201 Created，返回完整地址对象（含 id、recipient_name、created_at）。

**校验失败响应**：400 Bad Request
```json
{
  "error": "VALIDATION_ERROR",
  "message": "Address validation failed",
  "details": [
    {
      "field": "phone_number",
      "error": "Invalid US phone format",
      "pattern": "^\\+?1?\\s?\\(?[2-9]\\d{2}\\)?[\\s\\-]?\\d{3}[\\s\\-]?\\d{4}$",
      "value": "123-456-7890"
    }
  ]
}
```

**GET /api/v1/validation-rules/{country_code}**（新增）

获取指定国家的字段校验规则，供前端动态加载使用。

请求：`GET /api/v1/validation-rules/US`

响应：200 OK
```json
{
  "country_code": "US",
  "rules": {
    "first_name": {
      "pattern": "^[a-zA-ZÀ-ÿ\\s'-]{1,50}$",
      "error_message": "First name contains invalid characters",
      "max_length": 50,
      "min_length": 1,
      "is_required": true
    },
    "last_name": {
      "pattern": "^[a-zA-ZÀ-ÿ\\s'-]{1,50}$",
      "error_message": "Last name contains invalid characters",
      "max_length": 50,
      "min_length": 1,
      "is_required": true
    },
    "phone": {
      "pattern": "^\\+?1?\\s?\\(?[2-9]\\d{2}\\)?[\\s\\-]?\\d{3}[\\s\\-]?\\d{4}$",
      "error_message": "Invalid US phone format",
      "max_length": 20,
      "min_length": 10,
      "is_required": true
    },
    "postal_code": {
      "pattern": "^\\d{5}(-\\d{4})?$",
      "error_message": "Invalid ZIP Code format",
      "max_length": 10,
      "min_length": 5,
      "is_required": true
    }
  }
}
```

**PUT /api/v1/admin/validation-rules/{country_code}/{field_name}**（新增）

更新单个字段的校验规则。

请求：`PUT /api/v1/admin/validation-rules/US/phone`
```json
{
  "pattern": "^\\+?1?\\s?\\(?[2-9]\\d{2}\\)?[\\s\\-]?\\d{3}[\\s\\-]?\\d{4}$",
  "error_message": "Invalid US phone format",
  "max_length": 20,
  "min_length": 10,
  "is_required": true
}
```

响应：200 OK，返回更新后的规则对象。

---

## 五、依赖与风险

### 5.1 外部依赖

| 依赖 | 用途 | 风险 | 缓解 |
|------|------|------|------|
| Google Places API | Autocomplete + Details | API 故障/限流 | 降级为手动输入，不阻断下单 |

MVP 阶段不依赖：Address Validation API、USPS 邮编数据库、Loqate。

### 5.2 内部依赖

| 依赖模块 | 提供内容 | 说明 |
|----------|----------|------|
| 用户模块 | user_id | 地址归属 |
| 订单模块 | 触发 snapshot | 下单时冻结地址 |
| market 模块 | country_code 启用状态 | 国家可用性联动 |

**国家可用性联动规则**：
- `market.countries.enabled = false` → 该国家完全不可用
- `market.countries.enabled = true` + `country_address_config.enabled = true` → 地址功能可用
- 前端国家下拉列表：读取 `market.countries WHERE enabled = true`

### 5.3 风险评估

| 风险 | 影响 | 应对 |
|------|------|------|
| Google API 故障 | 无法自动填充 | 降级手动输入，不阻断下单 |
| 用户填错地址 | 物流退件 | MVP 接受一定退件率，V1.1 加 Validation |
| 地址格式不规范 | 面单打印异常 | 基础校验兜底 |

---

## 六、非功能需求

### 6.1 安全与合规

| 要求 | MVP 做法 |
|------|----------|
| 数据传输加密 | 全链路 HTTPS |
| 敏感字段存储 | phone_number、recipient_first_name、recipient_last_name AES-256 加密存储 |
| 用户数据删除 | 支持用户请求删除地址（CCPA 基本要求） |
| 日志脱敏 | 日志中地址信息做掩码 |

### 6.2 性能

| 指标 | 要求 |
|------|------|
| 地址簿上限 | 每用户最多 20 条 |
| Autocomplete 防抖 | 300ms |
| 地址列表加载 | < 500ms |
| 表单提交响应 | < 1s |

### 6.3 成本估算

按 MVP 阶段月活 1 万用户、平均每人 2 次地址操作估算：

| API | 单价 | 预估月调用量 | 月费用 |
|-----|------|-------------|--------|
| Places Autocomplete (Session) | $7/session | 2 万次 | $140 |
| **合计** | | | **~$140/月** |

---

## 七、版本规划

### 7.1 MVP 范围总结

- C端：美国地址表单 + Google Autocomplete + 地址簿 CRUD + 基础校验 + 前端 i18n（en-US / es-US）
- 后台：国家地址配置（前端展示字段统一管理）+ 行政区划管理（只读 + 批量导入）
- 数据：超集字段设计 + place_id 存储预留 + verified 字段预留

### 7.2 后续版本展望

| 版本 | 一句话概括 |
|------|-----------|
| V1.1 | ZIP-city-state 匹配校验 + Address Validation（高风险订单）+ 地址去重 + 邮编映射管理 |
| V2 | 欧洲/中东地址结构扩展 + 多国字段动态配置 + 地址数据多语言存储 |
| V3 | 后台配置中心完善 + 审计日志 + 风控联动 + 地址智能 |

---

## 八、附录

### 8.1 设计稿索引

| 文档 | 路径 |
|------|------|
| 后台原型 v2 | `原型/looply-地址库管理后台原型-v2.html` |
| 实体关系图 v1.1 | `实体关系图/looply-地址库管理实体关系图-v1.1.svg` |

### 8.2 参考文档

| 文档 | 说明 |
|------|------|
| 需求分析报告 v2.0 | 完整技术调研与版本分层设计 |
| admin-prototype-skill-pack | 后台原型 UI 规范 |
| Google Places API 文档 | Autocomplete + Place Details 接口 |

