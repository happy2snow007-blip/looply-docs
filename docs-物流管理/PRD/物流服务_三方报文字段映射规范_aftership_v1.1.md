# Looply 物流信息服务 — 三方报文字段映射规范

> 版本：v1.1
> 日期：2026-06-29
> 负责人：产品架构组
> 范围：AfterShip / 快递100 Webhook 成功推送报文 → tracking_checkpoints 落库 → 后台详情 / 前台轨迹页的完整字段血缘
> 关联：PRD v1.5（2.4 状态映射、2.6 前台轨迹页、ETA 用 AI EDD）、ER v2.6（tracking_checkpoints / shipments）、《API 错误处理规范》AfterShip v1.0 + 快递100 v1.2

---

## 〇、本文档解决什么问题

现有文档已覆盖**状态码映射**（三方 tag/state → internal_status，见各 API 错误规范第四节），
但缺失**报文字段级的解析落库规则**：一条 Webhook 推送的 JSON，逐字段拆出来存进
`tracking_checkpoints` 哪一列、再渲染到后台详情 / 前台轨迹页的哪个元素。

本规范补齐这条血缘链，分三段：
1. **入站映射**：三方 Webhook 字段 → `tracking_checkpoints` / `shipments` 列
2. **加工规则**：时区转换、地点拼接、国家码处理、message fallback、去重键
3. **出站映射**：DB 列 → 后台详情字段 / 前台轨迹页元素

> **字段来源**：快递100 字段名依据官方 Apifox 文档确认；AfterShip 字段名依据 AfterShip Tracking API v4 / Webhook Specifications 官方文档整理。字段确认状态详见 §六，其中标「⚠️ 联调核验」的少数项需对接时以实际推送报文最终确认。

---

## 一、入站映射：Webhook 报文 → 数据库列

### 1.1 推送报文形态差异

> AfterShip 侧依据官方文档（AfterShip Tracking API v4 / Webhook Specifications）整理；标「★联调核验」者为基于 v4 标准 schema、需对接时最终确认的字段名。

| 维度 | AfterShip | 快递100 |
|------|-----------|---------|
| 推送格式 | JSON body | form-urlencoded（`param` 为 JSON 字符串） |
| 签名 | base64-encoded HMAC | MD5(param + salt) |
| Webhook 信封 | `{ ts, event, event_id, msg, is_tracking_first_tag }`；ts=UTC unix 时间戳，event_id=UUID v4，tracking 对象在 `msg` 内 | param(JSON) |
| 回调确认 | HTTP 响应码须落在 200–299，否则判为失败重试 | 必须返回 `{"result":true,"returnCode":"200","message":"成功"}` |
| 推送重试 | 失败按官方策略重试（次数未公开） | 30 分钟间隔，最多 3 次 |
| 轨迹节点载体 | `msg.checkpoints[]` 数组（已确认） | `data` 数组（已确认） |
| 一级状态字段 | `tag` | state |
| 二级状态字段 | `subtag` | statusCode |
| 承运商纠错 | 无 | autoCheck=1 + comOld/comNew |
| 预计送达（ETA） | `msg.aftership_estimated_delivery_date`（AI EDD 对象：min/max/confidence_code）；不再用承运商原生 `expected_delivery` | 不返回 |
| 承运商官网链接 | `msg.courier_tracking_link`（v4 字段名，部分版本为 courier_redirect_link）★联调核验 | 不返回（需用模板拼接） |
| 运单平台ID | `msg.id`（tracking id） | 订阅运单号+承运商反查 |

### 1.2 tracking_checkpoints 列 → 报文来源（逐列）

> 每收到一个新轨迹节点，落一行 tracking_checkpoints。列定义以 ER v2.6 为准。

| DB 列（ER v2.6） | AfterShip 来源（checkpoint 对象） | 快递100 来源 | 加工规则 |
|------------------|----------------|--------------|----------|
| `shipment_id`(FK) | 由 msg.id（tracking id）反查本地 shipment | 由订阅回调的运单号+承运商反查 | 见 1.3 运单归属 |
| `platform_tag` | `tag` | state | 直接存原始值（字符串） |
| `platform_subtag` | `subtag` | statusCode | 快递100 无 subtag 时存 NULL 或 state 占位（见 §2.5） |
| `message` | `message`（节点原始描述）→ `subtag_message` → `tag` | `context`（已确认） | fallback 见 §2.4 |
| `mapped_internal_status` | 查 status_mappings | 查 status_mappings | 接收即映射，见 §2.1 |
| `display_i18n_key` | 查 status_mappings（subtag 级） | NULL（国内段不用） | 见 §2.6 |
| `location` | `location`（已含完整地点串）；或由 `city` + `state` + `country_name` 拼接 | 无独立字段（已确认）→ 存 NULL | 见 §2.2 |
| `country_iso3` | `country_iso3`（AfterShip 已是 ISO3，如 USA） | 无字段 → 国内默认 CHN | 见 §2.3 |
| `checkpoint_time` | `checkpoint_time`（ISO8601，可能带承运商当地时区偏移） | `ftime`（已确认，北京时间 UTC+8） | 统一转 UTC，见 §2.7 |
| `raw_payload` | 整条节点原始 JSON | 整条节点原始 JSON | 全量存档，不加工 |
| `created_at` | 落库时间 | 落库时间 | 系统生成 |

> AfterShip checkpoint 对象其他可用字段（按需取用）：`created_at`（AfterShip 收录时间，GMT+0）、`slug`（承运商代码）、`raw_tag`（承运商原始状态码）、`zip`、`coordinates`。以上字段名依据 AfterShip Tracking API v4 标准 schema，最终以联调报文为准。

### 1.3 shipments 列的 Webhook 联动更新

> 部分 Webhook 不只落 checkpoint，还要回写 shipments 主记录。

| shipments 列 | 触发推送 | 更新规则 |
|--------------|----------|----------|
| `internal_status` | 每次轨迹推送 | 取本次 mapped_internal_status，但受终态保护（见 §3.1）；用 checkpoint_time 排序防乱序 |
| `platform_status` | 每次轨迹推送 | 存平台原始一级状态（tag/state），用于调试回溯 |
| `tracking_health` | 状态映射命中 abnormal 规则 / 快递100 abort | 见 §2.1 与各 API 规范 |
| `last_tracking_update` | 每次有效落库 | 取本次 checkpoint_time |
| `carrier_id` | 快递100 autoCheck=1 | comNew → 反查 Looply carrier_id 后更新（见 §4）。**tracking_platform_id 不变**：纠错不跨平台 |

> 运单归属（1.2 的 shipment_id 反查）：
> - AfterShip：推送含 platform_tracking_id（AfterShip tracking.id），用它在 shipments 精确匹配
> - 快递100：推送含运单号 + 承运商代码，组合反查 shipments 的 (tracking_no, carrier_id)
> - 反查不到 → 记 message_logs（inbound_webhook, status=failed），不落 checkpoint（见 §3.5）

## 二、加工规则

### 2.1 状态映射（接收即映射）

- 收到推送时**立即**查 `status_mappings` 完成映射，结果存 `tracking_checkpoints.mapped_internal_status`，不延后到查询时算。
- 查找顺序（ER v2.6 status_mapping_lookup 规则）：先精确匹配 `platform_status_code + platform_sub_code`，匹配不到则 fallback 到仅 `platform_status_code` 的行。
- 同时取该映射行的 `tracking_health`，决定是否回写 shipments.tracking_health 并触发追踪异常通知。
- 未命中任何映射行 → 记日志告警，由开发补 status_mappings（PRD 2.4 已约定），internal_status 暂不推进。
- 具体状态值口径以 **PRD 2.4 + 快递100规范 §4.1** 为准。注意：MVP internal_status 取值为 AfterShip 英文 8 值（不含 Expired，见评审决策），快递100 经映射后归入同一套值。

### 2.2 地点拼接（location）

- AfterShip：checkpoint 对象提供 `location`（已是拼好的完整地点串）以及分字段 `city` / `state` / `zip` / `country_name` / `country_iso3`。**优先直接取 `location`**；若 `location` 为空，则用 `city, state, country_name` 非空段以逗号连接兜底。
- 快递100：**已确认无独立地点字段**。data[] 节点只有 context / time / ftime 三个基础字段，地点信息内嵌在 `context` 描述文本中（如「上海分拨中心/装件入车扫描」）。→ `location` 列**存 NULL**，地点由 message（context 原文）承载，前台直接展示原文即可。
- 统一原则：location 为展示辅助字段，缺失允许 NULL，前台不强依赖。

### 2.3 国家码（country_iso3）

- 列名为 country_iso3（ISO 3166-1 alpha-3，如 USA/CHN）。
- AfterShip：直接取 checkpoint 的 `country_iso3` 字段（**AfterShip 已返回 ISO3，无需转换**，如 USA/CHN/GBR）。
- 快递100：**已确认无国家字段**，国内段统一默认 CHN（如后续出现跨境清关节点，仍以 CHN 入库，跨境段由 AfterShip 承载）。
- 缺失允许 NULL。

### 2.4 message fallback（轨迹描述）

PRD 1.7 与 2.4 已定 fallback 优先级，本规范明确字段落点：

```
AfterShip： checkpoint.message（承运商原始描述）→ checkpoint.subtag_message → checkpoint.tag
快递100：   context（已确认，承运商原始描述）→ （无 subtag_message）→ state 含义文案
```

- 取第一个非空值存入 `tracking_checkpoints.message`。
- 快递100：直接取 `context`（已确认字段）。
- AfterShip：依次取 `message` → `subtag_message` → `tag`（均为 v4 标准 checkpoint 字段）。
- MVP 阶段 message 直接存原文（英文/中文按承运商返回），前台直接展示，不做结构化翻译。

### 2.5 二级状态对齐（platform_subtag）

- AfterShip：subtag 始终存在（无具体 subtag 时平台 fallback 到 `_001` 变体），直接存。
- 快递100：**无 subtag 概念**。约定：
  - `platform_tag` 存 state
  - `platform_subtag` 存 statusCode（如 201/202）；state 无 statusCode 时存 NULL
- 这样 status_mappings 的 (platform_status_code, platform_sub_code) 双列对两平台统一适用。

### 2.6 i18n key（display_i18n_key）

- 仅国际平台（AfterShip）使用，对应 subtag 级别，从 status_mappings 取。
- 国内平台（快递100）该列恒为 NULL，前台轨迹文案直接用 message 原文。
- MVP 阶段：PRD 1.7 明确前台直接展示 AfterShip tag 英文原文，display_i18n_key 先存不用（为后续 i18n 体系预留）。前端取值口径见 §5。

### 2.7 时间转换（checkpoint_time）

- DB 统一存 **UTC**。
- AfterShip：取 checkpoint 的 `checkpoint_time`（ISO8601 格式）。该字段为**承运商扫描当地时间，可能带时区偏移，也可能不带**（取决于承运商是否提供时区）；带偏移按偏移转 UTC，不带偏移时回退用 checkpoint 的 `created_at`（AfterShip 收录时间，格式 `YYYY-MM-DDTHH:mm:ssZ`，已是 GMT+0）作为近似。★联调时核验各承运商 checkpoint_time 的时区携带情况。
- 快递100：**已确认用 `ftime`**（格式化时间，如 `2012-08-28 16:33:19`），为**北京时间（UTC+8）、无时区标识**，入库须 **-8h 转 UTC**。
  - 注：data[] 同时有 `time` 和 `ftime`，二者多数情况值相同；统一取 `ftime`（格式化后更稳定），两者均无时区后缀，按 UTC+8 处理。
- 前台展示时再由 UTC 转用户本地时区（PRD 1.7）。
- 排序与去重均以 checkpoint_time（事件时间）为准，非接收时间。

### 2.8 ETA（预计送达）取值与时区

- **数据源**：AfterShip AI EDD —— `aftership_estimated_delivery_date` 对象，取 `estimated_delivery_date_min` / `estimated_delivery_date_max` / `confidence_code`。**不再使用承运商原生 `expected_delivery`**（覆盖率低、缺失率高）。
- **落库**：写入 shipments.eta_min / eta_max / eta_confidence_code（ER 同步新增，见下）。单日期时 min=max。
- **时区（关键差异）**：AI EDD 日期的时区为**目的地当地时区**（AfterShip 官方定义）。**只取日期部分（YYYY-MM-DD），入库与展示均不做 UTC 转换、不做时区加减** —— 与 §2.7 的 checkpoint_time「统一转 UTC」逻辑相反，切勿套用，否则会把日期减成前一天。
- **快递100**：不参与 AI EDD（国内段无 ETA）。
- **展示**：min≠max → 日期范围；min=max → 单日期。confidence_code 可用于展示决策/置信提示，阈值联调确认。

## 三、落库与状态机规则

> 以下规则与 PRD 2.4「状态转移规则」一致，本节明确其在落库环节的落点。

### 3.1 终态保护
- Delivered 为唯一终态。已 Delivered 的运单，后续非终态推送（如 InTransit）仅落 checkpoint，**不回退** shipments.internal_status。

### 3.2 Exception 可恢复
- Exception 不是终态。后续收到 InTransit/OutForDelivery/Delivered 推送时，正常推进 internal_status。

### 3.3 乱序处理
- 用 checkpoint_time（事件时间）判断先后。late-arriving 的旧节点照常落 checkpoint，但不把 shipments.internal_status 往回拨。

### 3.4 去重
- 联合唯一键 `(shipment_id, checkpoint_time, platform_tag, message)`（ER v2.6 webhook_dedup）。
- 同一 shipment 连续收到相同四元组的节点视为重复推送，不重复落库。

### 3.5 cancelled 后推送
- record_status=cancelled 后，平台推送仍可能到达：记 message_logs（inbound_webhook），**不落 checkpoint、不更新 internal_status**。

### 3.6 反查不到运单的推送
- 见 §1.3：记 message_logs（status=failed），不落库。区别于 cancelled（cancelled 是有记录但已终止，此处是无记录）。

---

## 四、快递100 autoCheck 自动纠错的字段联动

收到 `autoCheck=1` 的推送时（快递100规范 §3.2.2）：

| 报文字段 | 含义 | Looply 处理 |
|----------|------|-------------|
| autoCheck | =1 标识本次为自动纠错 | 触发纠错流程 |
| comOld | 原始（错误）承运商代码 | 仅记录审计 |
| comNew | 修正后承运商代码 | 经 platform_carrier_mappings 反查 Looply carrier_id |

处理动作：
1. comNew → 查 platform_carrier_mappings（platform=快递100, platform_carrier_code=comNew）→ 得 Looply carrier_id
2. 更新 shipments.carrier_id。**tracking_platform_id 保持不变**——快递100 自动纠错只在国内段平台内部更换承运商（如圆通→中通，均由快递100 追踪），追踪平台未变，故 platform_id 不动
3. 发承运商变更通知给业务系统（原承运商、新承运商、原因="快递100自动识别"）
4. 全过程记 message_logs
5. 若 comNew 在 platform_carrier_mappings 无映射 → 告警，由运营补映射；本地 carrier_id 暂不变，仍正常落 checkpoint

> 边界说明：理论上若 comNew 对应的 Looply 承运商仅配置了「另一追踪平台」的映射（属配置异常），才会涉及换平台；此情形归入第 5 条告警处理，不在正常纠错流程内。正常路径下纠错恒不跨平台。

## 五、出站映射：DB 列 → UI 元素

### 5.1 后台运单详情页（PRD 2.1.7，原型 TrackingQueryDetailPage）

| 详情页字段 | 数据来源 | 加工 |
|------------|----------|------|
| 业务单号 | shipments.business_order_no | 直接 |
| 运单号 | shipments.tracking_no | 已取消加删除线 |
| 承运商 | carriers.name（由 carrier_id 关联） | 显示中文名，非 code |
| 追踪平台 | tracking_platforms.name（由 tracking_platform_id 关联） | — |
| 物流状态 | shipments.internal_status | 后台展示 AfterShip 英文 tag 原文 |
| 记录状态 | shipments.record_status | active/cancelled → 活跃/已取消 |
| 来源系统 | shipments.source | — |
| 创建时间 | shipments.created_at | UTC → 运营时区展示 |
| 最后更新 | shipments.last_tracking_update | UTC → 运营时区展示 |
| 取消原因/时间 | shipments.cancel_reason / cancelled_at | 仅已取消运单展示 |
| 轨迹时间线-时间 | tracking_checkpoints.checkpoint_time | UTC → 展示时区 |
| 轨迹时间线-地点 | tracking_checkpoints.location | NULL 时省略 |
| 轨迹时间线-描述 | tracking_checkpoints.message | 直接展示原文 |

### 5.2 前台物流轨迹页（PRD 2.6，物流轨迹.pen）

| 轨迹页元素 | 数据来源 | 加工 |
|------------|----------|------|
| 进度条节点高亮 | shipments.internal_status | 按 PRD 2.6「tag↔节点」表映射到 5 节点 |
| ETA | AfterShip AI EDD（shipments.eta_min/eta_max，目的地当地日历日，不转 UTC） | 快递100 无 → 隐藏 ETA 区（PRD 2.6 缺省处理）；min≠max 展示范围 |
| 承运商 logo | carriers.logo_url | NULL 时显示默认占位 |
| 承运商名称 | carriers.name | — |
| 运单号 + 复制 | shipments.tracking_no | — |
| 承运商官网跳转 | carriers.tracking_url_template + tracking_no | 拼接归属见下方说明 |
| 轨迹时间线-时间 | tracking_checkpoints.checkpoint_time | UTC → 用户本地时区 |
| 轨迹时间线-地点 | tracking_checkpoints.location | NULL 时省略 |
| 轨迹时间线-描述 | tracking_checkpoints.message | **MVP 直接展示 message 原文**（英文）；display_i18n_key 暂不消费 |
| 收货地址 | （非本服务字段，由订单系统提供） | 脱敏由订单系统处理 |

**两处取值口径明确（原评审遗留）：**
- **message vs display_i18n_key**：MVP 阶段前台**统一读 message 原文**，display_i18n_key 先存不读（PRD 1.7）。后续建 i18n 体系时切换为读 key。
- **承运商官网 URL 拼接归属**：由**后端**拼好成品 URL，在状态通知 / 查询响应中以统一字段 `courierRedirectLink` 返回，前端直接用、不感知来源差异。取值优先级：
  1. **AfterShip 段优先**用平台返回的 `courier_tracking_link`（v4 字段名，部分版本为 courier_redirect_link；直连承运商官方轨迹页，更准）
  2. 无该字段（或快递100 段）→ 用 `carriers.tracking_url_template` 替换 `{tracking_no}` 拼接（兜底，模板为承运商管理页必填项，PRD 2.2.2）
  3. 两者皆无（模板未配置且平台无 link）→ 不返回该字段，前端不展示跳转入口

---

## 六、字段确认状态清单

字段名已依据官方文档补实（AfterShip Tracking API v4 / Webhook Specifications；快递100 官方 Apifox 文档）。仅少数项需联调时最终核验：

| # | 项 | 平台 | 状态 | 来源/说明 |
|---|----|------|------|-----------|
| 1 | 轨迹节点数组 `msg.checkpoints[]` | AfterShip | ✅ 已确认 | v4 Webhook 信封 `{ts,event,event_id,msg}`，tracking 在 msg |
| 2 | message：`message`→`subtag_message`→`tag` | AfterShip | ✅ 已确认 | v4 checkpoint 字段 |
| 3 | 地点：`location`（完整串）/ `city`+`state`+`country_name` | AfterShip | ✅ 已确认 | v4 checkpoint 字段 |
| 4 | 国家码 `country_iso3` 已是 ISO3 | AfterShip | ✅ 已确认 | v4 直接给 ISO3，无需转换 |
| 5 | `checkpoint_time` ISO8601，时区偏移视承运商而定 | AfterShip | ⚠️ 联调核验 | 各承运商是否带时区偏移需联调确认；不带则回退 created_at(GMT+0) |
| 6 | 回调确认：HTTP 200–299 | AfterShip | ✅ 已确认 | 非 2xx 判失败重试 |
| 7 | ETA `msg.aftership_estimated_delivery_date`（AI EDD：min/max/confidence_code，目的地当地日历日不转 UTC） | AfterShip | ⚠️ 待销售确认 | v4 字段；改用 AI EDD 替代 expected_delivery；计费方式与是否需单独开通待 AfterShip 销售核实 |
| 8 | 官网链接 `msg.courier_tracking_link` | AfterShip | ⚠️ 联调核验 | v4 字段名；部分版本/文档为 courier_redirect_link，联调确认实际键名 |
| 9 | 运单平台ID `msg.id`（tracking id） | AfterShip | ✅ 已确认 | 用于运单归属反查 |

> **快递100 侧（来源：快递100 官方 Apifox 文档）**：data[] 轨迹节点仅含 `context`（轨迹描述）/ `time` / `ftime`（均为北京时间 UTC+8）三个基础字段，无独立 location / city / state / country。message 取 context，时间取 ftime 转 UTC，location 存 NULL，country_iso3 默认 CHN。
>
> **AfterShip 侧字段名依据 v4 标准 schema**；联调时以实际推送报文为准，如有出入按实际报文修订本规范并升版本。

---

## 七、关联文档

| 文档 | 路径 |
|------|------|
| 物流信息服务 PRD | PRD/looply-物流信息服务-PRD-v1.4.md |
| API 错误处理规范（AfterShip） | 需求分析/物流服务_API错误处理规范_v1.0.md |
| API 错误处理规范（快递100） | 需求分析/物流服务_API错误处理规范_快递100_v1.2.md |
| 实体关系图 | 实体关系图/looply-物流管理实体关系图-v2.6.svg |

**维护说明**：本规范与 PRD、ER 同源。status_mappings 口径变化、ER 列变更、新增追踪平台时，须同步评审本规范。
