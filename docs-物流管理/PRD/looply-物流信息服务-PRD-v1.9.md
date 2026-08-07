# Looply 物流信息服务 — PRD

> **版本**：v1.9  
> **日期**：2026-08-07  
> **负责人**：产品架构组  
> **模块**：物流信息服务（Logistics Tracking Service）

> **v1.9 变更（前端物流轨迹设计依赖升级）**：
> 1. 前端物流轨迹页面职责引用升级至《looply-前端物流轨迹-PRD-v1.8》
> 2. PC Tracking details 设计依赖升级至 Figma《Looply 1.1》节点 `32:296`
> 3. 移动端 APP/H5 Tracking details 设计依赖升级至 Figma《Looply 1.1》节点 `9:11674`
> 4. 关联三方文档更新为 AfterShip 字段映射规范 v1.1 和快递100 API 错误处理规范 v1.2

> **v1.8 变更（AI EDD 多时区国家日期语义）**：
> 1. 明确 AI EDD 是 shipment 目的地所在地的日历日期，不是时间戳
> 2. 美国等多时区国家按该票 shipment 的目的地地址解释 EDD 日期，同一 shipment 不随查询用户时区或 locale 改变
> 3. 注册 AfterShip tracking 时向平台传递上游可提供的目的地国家、州/省、城市和邮编；信息不足不阻断轨迹注册，但可能导致 EDD 缺失或准确性下降
> 4. 服务端按 DATE 保存并原值返回 eta_min、eta_max；消费端不得自行推导目的地时区或换算日期

> **v1.7 变更（翻译中心物流轨迹卡片）**：
> 1. 翻译中心“前端页面”域新增“物流轨迹”卡片，`resourceType = page_logistics_tracking`
> 2. 卡片本期只维护固定 UI 文案和 8 个统一物流状态文案
> 3. 物流服务按 locale 从该卡片读取状态译文；前端固定 UI 译文由同一卡片同步至语言包
> 4. 轨迹事件描述不进入翻译中心，使用可读渠道原文；原文不可读时回退本地化状态文案
> 5. checkpoint 实例和平台原始 message 不生成翻译记录

> **v1.6 变更（前端职责拆分与服务端多语言）**：
> 1. 前端物流轨迹页面已拆分至《looply-前端物流轨迹-PRD-v1.5》，本 PRD 删除重复的页面布局、UI、交互和异常态定义
> 2. 原 2.6 调整为“C 端消费与多语言输出”，仅定义物流服务的数据职责、locale 处理、本地化输出和回退规则
> 3. 物流状态与可枚举轨迹事件由服务端 message package 本地化；固定 UI 文案继续由前端语言包管理（该规则已在 v1.7 收敛为统一翻译中心卡片）
> 4. 异步通知保持语言无关，传递状态码和 i18n key；按用户 locale 的本地化文案在查询消费时生成
> 5. 快递100与 AfterShip 统一使用 `display_i18n_key`，不再限定“仅国际段”
> 6. 本期不新增翻译中心物流资源卡片，不为 checkpoint 或平台原始 message 生成翻译记录（该结论已由 v1.7 替代）

> **v1.5 变更（ETA 数据源切换）**：
> 1. 前台 ETA 数据源由承运商原生 `expected_delivery` 切换为 AfterShip AI EDD（`aftership_estimated_delivery_date`），覆盖率更高、支持单日期/区间，并带置信度（见 2.6、附录）
> 2. 明确 AI EDD 时区为**目的地当地时区日历日**，入库与展示均不做 UTC 转换（与 checkpoint_time 处理不同）
> 3. shipments 表新增 EDD 落库字段（eta_min / eta_max / eta_confidence_code）
> 4. 关联文档升级《三方报文字段映射规范 v1.1》
> 5. 遗留待办：AI EDD 计费方式与是否需单独开通该产品，待向 AfterShip 销售核实（见 4.x 外部依赖）
>
> **v1.4 变更（评审一致性修订）**：
> 1. 状态空间收敛：internal_status 取值为 AfterShip 英文 8 值，移除消费端 Expired（Expired_001 经映射归入 Exception，详见 2.4）。后台筛选下拉、前台进度条、KPI 异常口径同步调整
> 2. PATCH 冲突判定明确为 effective 组合规则（见 2.1.3）
> 3. 异步退订任务承载方式归技术侧实现，不在数据模型范围（见 2.1.3）
> 4. 附录字段名对齐 ER v2.6（tracking_checkpoints / platform_tag / checkpoint_time / platform_carrier_mappings）
> 5. 确认拆包支持：1 business_order_no = N shipment（对齐 ER v2.6）
> 6. 关联文档新增《三方报文字段映射规范 v1.0》

---

## 一、概述

### 1.1 背景与目标

Looply 是面向美国市场的大牌二手电商平台，业务链路涉及国内转仓（卖家→国内仓）和国际配送（国内仓→美国买家）两段物流。平台需要为买家、卖家、客服、运营等多个业务系统提供统一的物流追踪能力。

**目标**：建设物流信息服务中台，对内屏蔽追踪平台差异，对外提供标准化的运单注册、轨迹查询、状态通知能力。

**核心价值**：
- 业务系统通过统一 API 注册运单，无需关心底层对接的是 AfterShip 还是快递100
- 物流状态变更时主动通知业务系统，业务系统无需轮询
- 后台运营可管理承运商、追踪平台配置，无需开发介入

### 1.2 不做什么（明确边界）

| 不做的事 | 归属 |
|----------|------|
| 配送限制（地址规则、关键词匹配、订单拦截） | 地址管理模块 |
| 物流渠道管理（渠道配置、时效设置、费用配置） | 不在本期范围 |
| 前台订单列表中的物流状态展示 | 订单列表模块 |
| 前台推送通知样式 | 订单列表模块 |
| PC、APP、H5 物流轨迹页面布局、交互、固定 UI 文案和异常态 | 《looply-前端物流轨迹-PRD-v1.8》 |
| 运费计算与收取 | 订单/支付模块 |
| 退货物流 | 售后模块 |
| 面单生成与打印 | 不在本期范围 |
| 合单发货（多订单共用一个运单号） | 不支持，1:1 模型 |

### 1.3 用户角色

| 角色 | 说明 | 使用方式 |
|------|------|----------|
| 业务系统（调用方） | 卖家系统、买家系统、客服系统等 | 通过 API 注册运单、查询状态、接收通知 |
| 运营人员 | 物流运营 | 通过后台管理承运商、追踪平台、查看运单 |
| 买家（C端用户） | 海外消费者 | 通过订单前端间接消费物流服务返回的本地化轨迹数据 |

### 1.4 核心场景

1. **注册运单追踪**：业务系统下单后，调用 API 注册运单号，系统自动路由到对应追踪平台开始追踪
2. **接收物流轨迹**：追踪平台通过 Webhook 推送轨迹更新，系统存储并通知业务系统
3. **查询物流状态**：订单等业务系统按用户 locale 查询运单当前状态、ETA 和完整轨迹
4. **纠错修正**：运单号或承运商填错时，通过 PATCH 修正，系统内部处理平台切换
5. **取消追踪**：业务方取消订单时，终止物流追踪服务
6. **后台管理**：运营人员管理承运商档案、追踪平台承运商映射

### 1.5 全局页面流转

```
后台：
  运单管理（列表） → 运单详情
  承运商管理（列表） → 编辑承运商 / 新增承运商
  追踪平台管理（列表） → 编辑追踪平台（含承运商映射管理）

C 端页面：
  页面流转、PC Modal 与移动端 Bottom Sheet 由《looply-前端物流轨迹-PRD-v1.8》定义；本服务仅提供数据
```

### 1.6 术语说明

| 术语 | 说明 |
|------|------|
| 运单（Shipment） | 一次物流追踪记录，由 tracking_no + business_order_no 唯一确定 |
| 承运商（Carrier） | 实际承运的物流公司，如 UPS、FedEx、顺丰国内 |
| 追踪平台（Tracking Platform） | 提供物流轨迹聚合服务的第三方平台，如 AfterShip、快递100 |
| 物流状态（Tracking Status） | 运单当前运输状态。统一为 Looply 8 值：Pending、InfoReceived、InTransit、OutForDelivery、AvailableForPickup、AttemptFail、Delivered、Exception |
| locale | 调用方传入的语言及地区标识，用于生成状态和事件描述的本地化文案；缺省为 `en-US` |
| 记录状态（Record Status） | 运单记录的生命周期状态：活跃(active) / 已取消(cancelled) |
| 追踪健康度（Tracking Health） | 追踪系统本身是否正常工作：normal / abnormal |
| 平台承运商映射 | 追踪平台的承运商代码与 Looply 内部承运商的对应关系 |

### 1.7 多语言 / 多国家策略

- 后台界面固定文案：中文，供内部运营使用；不进入翻译中心业务资源卡片。
- 翻译中心“前端页面”域新增“物流轨迹”卡片，稳定标识为 `page_logistics_tracking`。
- 卡片只维护两类内容：前端固定 UI 文案、Looply 8 个统一状态文案；不维护轨迹事件描述。
- 固定 UI 译文由该卡片同步至前端语言包；物流服务不返回固定 UI 文案。
- 物流服务按 locale 读取同一卡片中的状态译文，生成 statusLabel。
- 平台原始 message 属于第三方实时动态内容，不按 checkpoint 生成翻译记录；作为事件 description 原文，原文不可读时回退本地化 statusLabel。
- 地点、承运商名称、运单号：按原值返回，不翻译。
- 轨迹时间：服务端以 UTC 存储和返回，由消费端转换为用户时区并按 locale 格式化。
- AfterShip AI EDD：表示 shipment 目的地所在地的日历日期，不是时间戳；美国等多时区国家按该票目的地地址解释，存储及输出均不做 UTC 转换，消费端只按 locale 格式化日期。
- 同一 shipment 的 AI EDD 不随查询用户所在地、账号时区、浏览器时区或请求 locale 改变。
- 卡片需在业务首次推送源文前通过 migration 注册 `translation_resource` 和可翻译字段；运行时使用 `resourceType = page_logistics_tracking`。

---

## 二、需求详细描述

### 2.1 运单管理

#### 2.1.1 模块概述

运单管理是物流信息服务的核心模块，统一管理所有业务系统注册的运单及其物流状态。国内段（快递100）和国际段（AfterShip）运单在同一列表中管理，通过承运商和追踪平台区分。

---

#### 2.1.2 运单注册（机制型）

**功能描述**

业务系统通过 API 注册运单追踪。系统根据承运商自动路由到对应追踪平台，注册成功后开始追踪物流轨迹。

**触发条件**

业务系统调用注册接口，传入运单号、承运商、业务单号、来源系统标识。国际段调用方同时传入其可获得的目的地国家、州/省、城市和邮编，供 AfterShip 计算 AI EDD。

**处理流程**

1. Looply 基础校验（本地，毫秒级）：
   - tracking_no：非空，自动 trim 前后空格
   - carrier_id：非空、必须存在且启用、必须有追踪平台映射
   - business_order_no：非空
   - source：非空、必须在已注册系统标识白名单中（白名单由开发在系统配置中维护，不提供管理 UI）
   - 顺丰承运商：phone 字段条件必填（后4位即可）

2. 路由追踪平台：根据承运商的平台映射关系，确定使用 AfterShip 还是快递100

3. 调用追踪平台注册（远程，秒级）：
   - AfterShip 国际段：将调用方提供的目的地国家、州/省、城市和邮编透传给 AfterShip；物流服务不根据地址自行推导时区
   - 成功 → 创建 shipment 记录，返回运单信息
   - 失败 → 不创建记录，直接返回错误给调用方

**规则说明**

| 规则 | 说明 |
|------|------|
| 运单号唯一 | 同一 (tracking_no, carrier_id) 组合在 active 状态下唯一，不同承运商可有相同运单号 |
| 拆包支持 | 同一 business_order_no 可注册多条 shipment（一个订单拆多个包裹） |
| 注册失败不建记录 | shipments 表只有"真正可追踪"的运单 |
| 幂等处理 | 同一 (tracking_no, carrier_id) 重复注册返回已有记录；tracking_no 相同但 carrier_id 不同视为独立运单 |
| business_order_no 不可修改 | 注册后禁止修改，填错则 DELETE + 重新 POST |
| 格式校验交给平台 | Looply 不做运单号格式校验，由追踪平台判断 |
| 顺丰手机号 | 快递100对接顺丰时必须传入寄/收件人手机号（后4位即可） |
| 目的地信息与 AI EDD | 国际段应尽量提供目的地国家、州/省、城市和邮编。字段缺失不阻断运单注册和轨迹追踪，但 AfterShip AI EDD 可能为空或准确性下降；物流服务不得猜测缺失地址或时区。 |

**异常处理**

| 异常场景 | 处理方式 |
|----------|----------|
| 承运商不存在或已停用 | 返回 `CARRIER_NOT_FOUND` / `CARRIER_DISABLED`，提示确认承运商ID |
| 承运商无平台映射 | 返回 `CARRIER_NO_PLATFORM`，提示联系管理员配置 |
| 追踪平台返回运单号无效（AfterShip 4005/4017） | 返回 `TRACKING_NO_REJECTED`，提示核对运单号与承运商是否匹配 |
| 追踪平台返回承运商代码无效（AfterShip 4010） | 返回 `CARRIER_SLUG_INVALID`，提示联系管理员检查配置 |
| AfterShip 4012 — 承运商不在白名单 | 返回 `CARRIER_NOT_APPROVED`，提示联系管理员在追踪平台后台添加该承运商 |
| AfterShip 4012 — 无法从运单号识别承运商 | 返回 `CARRIER_UNRECOGNIZED`，提示明确指定 carrier_id |
| AfterShip 4012 — 运单号格式无效 | 返回 `TRACKING_NO_REJECTED`，提示核对运单号 |
| AfterShip 4012 — 承运商已下线 | 返回 `CARRIER_DEPRECATED`，提示联系管理员确认替代方案 |
| AfterShip 4012 — 运单号不属于该承运商 | 返回 `CARRIER_MISMATCH`，提示确认运单号与承运商对应关系 |
| 追踪平台认证失败 | 返回 `PLATFORM_AUTH_FAILED`，提示联系管理员检查 API Key |
| 追踪平台限流 | 返回 `RATE_LIMITED`，建议等待 10 秒后重试 |
| 追踪平台不可用 | 返回 `PLATFORM_UNAVAILABLE`，建议稍后重试 |
| 网络超时 | 返回 `PLATFORM_TIMEOUT`，系统将自动恢复 |
| 快递100重复订阅（每月4次限制） | 返回 `TRACKING_EXISTS`，提示无需重复注册 |
| AfterShip 4003 但本地无记录 | 从 AfterShip 同步该运单数据后创建本地 shipment 记录（兼容跨系统迁移、历史数据补录场景） |

**技术说明**

- 校验分两层：Looply 基础校验（本地毫秒级）→ 追踪平台校验（远程秒级）
- 每个错误响应必须包含：错误码（程序判断）、错误描述（人类可读）、操作指引（下一步怎么做）、追踪ID（定位问题）
- 详细错误码映射见《API 错误处理规范》（AfterShip 版 + 快递100 版）
- 注册失败的请求记入 message_logs（shipment_id=NULL），用于审计排查但不写入 shipments 表，保持 shipments 表只含「真正可追踪」的运单

**设计说明**

注册失败时不创建 shipment 记录的原因：
1. 所有追踪平台错误都是同步返回的（HTTP 4xx/5xx），不是异步的
2. 这些错误都是输入校验失败，说明追踪根本没有开始
3. 业务系统应该立即修正输入，而不是让 Looply 保留错误记录
4. 保持数据干净，shipments 表只有「真正可追踪」的运单

**source 白名单（MVP 阶段）**

| source 值 | 来源系统 | 用途 |
|----------|---------|------|
| seller-system | 卖家系统 | 卖家发货后注册转仓段运单 |
| ops-system | 运营/仓配系统 | 国内仓向美国发货后注册国际段运单 |
| cs-system | 客服系统 | 客服补录运单 |

新增 source 由开发在系统配置中追加，不提供管理 UI。

---

#### 2.1.3 运单信息修正（机制型）

**功能描述**

业务系统发现运单号或承运商填错时，通过 PATCH 修正。系统内部处理追踪平台的订阅切换，对调用方透明。

**触发条件**

业务系统调用修改接口，传入需要变更的字段（tracking_no / carrier_id / phone，至少一个）。

**接口定义**

```
PATCH /trackings/{shipment_id}
{
  "tracking_no": "新运单号",    // 可选
  "carrier_id": "CR005",        // 可选
  "phone": "8000"               // 可选，顺丰场景
}
```

至少传一个变更字段。`shipment_id` 为注册时返回的不可变 UUID。

**处理流程（先创建再取消）**

1. 校验：仅 record_status = active 的运单可修改
2. 用新信息在追踪平台注册新订阅
3. 新订阅成功 → 取消旧订阅 → 更新本地记录
4. 新订阅失败 → 旧订阅不动，返回错误给调用方（可再次 PATCH）
5. 旧订阅取消失败 → 不影响主流程，异步重试

**异步清理机制**

- 旧订阅取消由系统异步完成，不阻塞 PATCH 响应
- 取消所需的旧值（原 tracking_no、原 carrier slug、原 platform_tracking_id）在请求处理过程中以内存变量持有
- 若同步取消失败需异步重试，旧值随重试任务持久化（含平台、运单号、订阅ID等）
- 最终兜底：即使重试全部失败，平台侧旧订阅在签收或 abort 后自动停止，无业务影响

> **异步退订任务的承载方式**（消息队列 / 定时任务表 / 其他）由技术侧根据系统实现决定，不在本服务数据模型（ER）范围内。ER 仅定义业务实体；重试任务属技术实现细节。开发无需在 ER 中寻找该任务表。

**审计痕迹**

PATCH 操作的完整链路记录在该 shipment 的消息日志中，包括：
- 调用方发起 PATCH 请求（含变更前后字段值）
- 新订阅创建结果（平台响应）
- 本地记录更新完成
- 旧订阅取消请求及结果（含重试记录）

**规则说明**

| 规则 | 说明 |
|------|------|
| 不限修改次数 | 无次数限制（快递100场景除外） |
| 原地更新 | 同一条 shipment 记录，字段直接改为新值，不产生新记录 |
| 清除旧轨迹 | 修改成功后清除旧轨迹节点，internal_status 重置为 Pending（待揽收） |
| 快递100额度消耗 | 每次修改消耗 1 次订阅额度（每月上限 4 次），剩余不足时提前告知 |
| 先创建再取消 | 避免"旧的取消了、新的没建起来"的半失败中间态 |

**异常处理**

| 异常场景 | 处理方式 |
|----------|----------|
| 运单已取消 | 返回错误，已取消运单不可修改 |
| 新订阅注册失败 | 旧订阅保持不变，返回错误 |
| 旧订阅取消失败 | 不阻塞响应，异步重试；最终兜底：平台侧签收/abort 后自动停止 |
| 快递100月度额度用尽 | 返回 `QUOTA_EXHAUSTED`，提示需等次月重置（含 reset_at 时间） |
| 快递100剩余额度 ≤ 1 | 操作正常执行，响应附加 `LOW_QUOTA_WARNING` 预警，提示调用方谨慎使用 |
| 新 tracking_no 与已有 active 运单冲突 | 返回 `TRACKING_NO_CONFLICT`，提示该运单号已被占用（冲突判定见下方 effective 组合规则） |

**冲突判定规则（effective 组合）**

PATCH 可只改 tracking_no、只改 carrier_id、或两者都改。唯一约束作用于记录的最终值，故冲突判定基于「变更后的有效组合」：

```
effective_tracking_no = 请求带了 tracking_no 则用新值，否则用记录现值
effective_carrier_id  = 请求带了 carrier_id 则用新值，否则用记录现值

若存在另一条 active 记录，其 (tracking_no, carrier_id) == (effective_tracking_no, effective_carrier_id)
且其 shipment_id ≠ 当前记录 → 返回 TRACKING_NO_CONFLICT
```

- 必须排除当前记录自身（shipment_id 不同才算冲突），否则改成与自身相同的值会误报。
- 与 shipments 的 (tracking_no, carrier_id) active 唯一约束完全对齐，三种 PATCH 走同一判定。

---

#### 2.1.4 取消运单追踪（机制型）

**功能描述**

业务方取消订单时，终止物流追踪服务。语义为"停止追踪"，非删除数据，记录仍可查询。

**触发条件**

业务系统调用取消接口，传入取消原因。

**处理流程**

1. 标记 record_status = cancelled
2. 记录 cancel_reason 和 cancelled_at
3. 同步通知追踪平台停止追踪
4. 已取消的运单不可恢复，需重新注册
5. checkpoints 数据保留，不删除（供审计、客服查询、纠纷举证）

**规则说明**

| 规则 | 说明 |
|------|------|
| cancel_reason 枚举 | business_cancelled（业务方主动取消） |
| 不可恢复 | 取消后如需继续追踪，需重新注册新运单 |
| 运单号/承运商填错 | 使用 PATCH 修正，不再需要 DELETE + POST |

**设计说明**

cancel_reason 只有 `business_cancelled` 一个枚举值的原因：
- 运单号/承运商填错场景已改用 PATCH 修正（见 2.1.3），因此不再需要 `tracking_no_error` 枚举值
- DELETE 接口语义收窄为「业务方主动终止追踪」（如订单取消、用户退款等）

---

#### 2.1.5 轨迹更新通知（机制型）

**功能描述**

追踪平台每收到一个新轨迹节点，Looply 即主动通知调用方业务系统。调用方根据 `is_status_changed` 标志自行判断是否需要触达终端用户（避免每个轨迹节点都打扰用户）。

> 章节命名澄清：本接口实际为「轨迹更新通知」，每次轨迹更新均推送，不仅在状态变化时触发。命名上保留「状态变更通知」作为产品别称（业务方更熟悉），但开发实现以本节为准。

**触发条件**

每次收到新轨迹节点时推送（不仅是状态变更，状态是否变化由 `is_status_changed` 字段标记）。

**处理流程**

1. 追踪平台 Webhook 推送新轨迹
2. Looply 解析、存储轨迹节点
3. 通知调用方业务系统

**规则说明**

通知内容：
- shipment_id（不可变主键，调用方做精确关联）
- business_order_no、tracking_no、carrier
- 当前状态码（status）+ 状态稳定标识（statusI18nKey）
- 最新轨迹事件（mappedStatus、statusI18nKey、originalDescription、location、occurredAt）
- 承运商轨迹跳转链接（courierRedirectLink）
- is_status_changed 标志：true 表示本次轨迹导致 internal_status 发生变化；调用方据此决定是否向终端用户推送通知
- previous_status：上一个 internal_status，仅 is_status_changed=true 时有意义；用于调用方展示状态变更历史

异步通知为语言无关事件，不根据某个终端用户 locale 固化翻译结果。`defaultDescription` 使用 `en-US` 兼容文案；业务系统面向具体用户展示时，应按用户 locale 重新查询本地化轨迹或使用 i18n key 完成本系统通知文案。

> 拆包场景说明：同一 business_order_no 可能关联多条 shipment，调用方收到通知后用 shipment_id 或 tracking_no 区分具体是哪个包裹。

可靠性要求：
- 通知失败自动重试，最多 3 次，间隔递增（30s / 60s / 120s）
- 调用方可通过查询接口兜底

通知通道：具体实现方式（HTTP 回调 / 消息队列 / 其他）由技术侧根据系统对接方式决定，产品层面不约束。

---

#### 2.1.6 追踪异常通知（机制型）

**功能描述**

当追踪系统本身出现异常（无法正常获取轨迹信息）时，通知调用方。

**触发条件**

tracking_health 从 normal 变为 abnormal 时。

**规则说明**

追踪异常 ≠ 物流异常：
- **物流异常**（internal_status）：包裹运输本身出了问题（派送失败、损坏、丢失等）
- **追踪异常**（tracking_health）：追踪系统获取不到信息，需要排查配置或确认承运商

触发 abnormal 的场景：

| 来源 | 场景 | 通知内容 | 操作建议 |
|------|------|---------|---------|
| AfterShip | Pending_002 无活跃承运商连接 | 追踪信息暂时无法获取 | 检查 AfterShip 后台对应承运商账号的连接状态及凭证有效性（账号专属承运商需绑定 API Key/凭证，可能未配置或已过期） |
| AfterShip | Pending_004 承运商分配错误 | 追踪信息暂时无法获取 | 建议确认运单号与承运商是否匹配 |
| AfterShip | Pending_005 120天无更新 | 该运单长时间无物流更新 | 建议联系承运商确认包裹状态，必要时申请理赔 |
| AfterShip | Pending_006 无法识别承运商 | 追踪信息暂时无法获取 | 建议确认运单号与承运商是否匹配 |
| AfterShip | Expired_001 30天无信息 | 该运单长时间无物流更新 | 建议联系承运商确认包裹状态，必要时申请理赔 |
| 快递100 | abort 3天无记录 | 追踪信息暂时无法获取 | 建议确认运单号与承运商是否匹配 |
| 快递100 | abort 60天无变化 | 该运单长时间无物流更新 | 建议联系承运商确认包裹状态，必要时申请理赔 |

**恢复通知**

tracking_health 从 abnormal 恢复为 normal 时（例如 Pending_002 配置修复后承运商连接恢复），系统同样向调用方发送一次「追踪恢复」通知，包含：
- business_order_no、tracking_no、carrier
- 恢复前异常类型（previous_abnormal_subtag）
- 恢复时间（recovered_at）

调用方收到恢复通知后可清除前端的异常提示。

**告警升级**

- abnormal 持续超过 24 小时，后台告警升级到运营值班
- 具体 subtag 为 Pending_005 / Expired_001 时为高优先级，提示可能需要申请理赔

---

#### 2.1.7 运单管理后台（页面型）

**功能描述**

运营人员查看所有业务系统注册的运单及其状态轨迹。

**前置条件**

运营人员已登录后台系统。

**页面布局**

PC 端后台页面，左侧导航 + 右侧内容区。

**页面元素 — 列表页**

KPI 卡片区（仅统计 record_status=active 的运单）：

| 卡片 | 统计口径 |
|------|---------|
| 运单总数 | 全部活跃运单 |
| 运输中 | internal_status ∈ { InfoReceived, InTransit, OutForDelivery, AvailableForPickup } |
| 已送达 | internal_status = Delivered |
| 异常 | internal_status ∈ { AttemptFail, Exception } 或 tracking_health = abnormal |

筛选工具栏：
- 搜索框（业务单号/运单号）
- 物流状态下拉（全部 + 8 个 AfterShip tag：Pending / InfoReceived / InTransit / OutForDelivery / AvailableForPickup / AttemptFail / Delivered / Exception）
- 记录状态下拉（全部 / 活跃 / 已取消）
- 承运商下拉
- 追踪平台下拉
- 追踪健康度下拉（全部 / 正常 / 异常）

列表字段：

| 列名 | 说明 |
|------|------|
| 运单号 | 运单号文本 |
| 业务单号 | 调用方传入的关联标识 |
| 承运商 | Looply 承运商名称 |
| 物流状态 | AfterShip tag（如 InTransit、Delivered） |
| 记录状态 | 活跃 / 已取消 |
| 最后更新 | 最后轨迹更新时间 |
| 追踪平台 | AfterShip / 快递100 |
| 追踪健康度 | 正常 / 异常（abnormal 时用警告图标标识） |
| 创建时间 | 运单注册时间 |
| 操作 | 详情按钮 |

已取消运单样式：运单号带删除线，整行降低透明度，物流状态列显示 `—`（不显示取消前的最后状态）。

**页面元素 — 详情页**

基本信息区：
- 业务单号、运单号、承运商、追踪平台、物流状态、记录状态、来源系统、创建时间、最后更新

物流轨迹区（时间线样式）：
- 每个节点含：地点、时间、事件描述
- 最新节点高亮

已取消运单详情：
- 额外显示：取消原因、取消时间
- 轨迹区显示警告提示："追踪已终止，该运单已被取消，物流追踪服务已停止"

**操作流程**

- 列表页 → 点击"详情" → 进入运单详情页
- 详情页 → 点击"返回列表" → 回到列表页

**UI 关联**

- PC 端：后台原型 v5.11 — 运单管理列表页、运单详情页、已取消运单详情页

---

#### 2.1.8 查询能力（机制型）

**功能描述**

物流信息服务提供运单和承运商的查询能力，供调用方按需获取物流数据。

**触发条件**

调用方通过 API 发起查询请求。

**处理流程**

提供以下 4 个查询能力：

1. **查询单个运单**（GET /trackings/{shipment_id}）
   - 返回运单事实字段及按 locale 生成的 statusLabel（含 tracking_no、carrier、status、statusI18nKey、record_status、tracking_health、source、created_at 等）
   - 如运单不存在，返回 404 错误

2. **查询运单轨迹**（GET /trackings/{shipment_id}/checkpoints）
   - 返回该运单的完整轨迹节点列表（时间倒序）
   - 每个节点包含：时间、地点、可读渠道 description、原始 description、对应的 Looply 展示状态及状态 i18n key
   - 如运单不存在，返回 404 错误

3. **批量查询运单**（GET /trackings）
   - 支持筛选条件：status（物流状态）、carrier_id（承运商）、source（来源系统）、date_range（注册时间范围）、business_order_no（业务单号，返回列表）
   - 支持分页：page、per_page（默认 20，最大 100）
   - 返回运单列表 + 分页信息

4. **获取承运商列表**（GET /carriers）
   - 返回所有启用状态的承运商列表
   - 每个承运商包含：carrier_id、name、code、tracking_url_template、required_fields
   - required_fields 说明该承运商注册运单时的额外必填字段（如顺丰需要 phone 字段）

**规则说明**

| 规则 | 说明 |
|------|------|
| 权限控制 | 所有查询接口需验证调用方 source 身份 |
| 数据隔离 | 调用方只能查询自己注册的运单（按 source 过滤） |
| 频率限制 | 单个 source 每分钟最多 600 次查询请求 |
| locale | 单运单和轨迹查询接受当前界面 locale；缺失、非法或不支持时降级 `en-US` |
| 缓存策略 | 承运商列表可缓存 5 分钟；运单事实状态实时查询不缓存；若缓存本地化结果，缓存键必须包含 locale |

**异常处理**

| 异常场景 | 处理方式 |
|----------|----------|
| 运单号不存在 | 返回 404，message: "Tracking not found" |
| 参数格式错误 | 返回 400，message 说明具体字段问题 |
| source 未授权 | 返回 403，message: "Unauthorized source" |
| 频率超限 | 返回 429，message: "Rate limit exceeded"，Header 返回重试时间 |

**技术说明**

- 批量查询使用 offset 分页（非游标），适用于数据量可控的中台内部调用场景
- 承运商列表接口响应可被调用方本地缓存，建议 TTL 5 分钟
- 所有查询接口通过 source 参数实现数据隔离
- 鉴权不在物流服务范围内，由基础设施层保障（网关 mTLS / 内网 IP 白名单）；source 字段仅用于数据隔离标识，不做应用层鉴权

---

### 2.2 承运商管理

#### 2.2.1 模块概述

统一管理所有承运商基础信息。同一物流公司如同时提供国内外服务则分别定义（如顺丰国内、顺丰国际）。承运商是运单路由到追踪平台的关键枢纽。

---

#### 2.2.2 承运商管理后台（页面型）

**功能描述**

运营人员管理承运商档案，包括新增、编辑、启停。

**前置条件**

运营人员已登录后台系统。

**页面元素 — 列表页**

KPI 卡片区：
- 承运商总数
- 已启用
- 已停用
- 已配置平台映射

筛选工具栏：
- 搜索框（承运商名称/编码）
- 状态下拉（全部 / 启用 / 停用）

列表字段：

| 列名 | 说明 |
|------|------|
| ID | 承运商ID |
| Looply 承运商名称 | 内部统一名称 |
| Looply 承运商编码 | 唯一编码（如 ups、sf-domestic） |
| 已配置追踪平台 | 该承运商在哪些追踪平台有映射 |
| 状态 | 启用 / 停用 |
| 更新时间 | 最后修改时间 |
| 操作 | 编辑按钮 |

**页面元素 — 编辑页**

基本信息区：
- 承运商名称（必填）
- 承运商编码（必填，唯一）
- 轨迹查询URL模板（必填）：如 `https://www.ups.com/track?tracknum={tracking_no}`，用于生成承运商官网轨迹跳转链接
- Logo 图片地址（选填）：URL 格式，供 C 端物流状态卡或轨迹详情按需使用
- 状态开关（启用/停用）

已配置追踪平台区（只读展示）：
- 展示该承运商在各追踪平台的代码映射
- 提示："承运商与追踪平台的映射关系在「追踪平台管理 → 承运商映射管理」中维护"

**数据来源说明**

该区域数据来自 platform_carrier_mappings 表，展示该承运商在各追踪平台的代码映射：
- 展示格式：`平台名称: 平台承运商代码`（如 AfterShip: ups, 快递100: UPS）
- 如承运商在多个平台都有映射，按平台名称排序展示
- 同名物流公司（如顺丰国内 vs 顺丰国际）通过不同的 carrier code 区分（sf-domestic / sf-international），各自维护独立的平台映射

操作记录区：
- 操作时间、操作人、操作类型、操作内容

**页面元素 — 新增页**

与编辑页相同的表单字段，保存后提示到追踪平台管理配置映射。

**校验规则**

| 字段 | 规则 | 校验时机 |
|------|------|----------|
| 承运商名称 | 非空 | 提交时 |
| 承运商编码 | 非空、唯一 | 提交时 |
| 轨迹查询URL模板 | 必填；需包含 `{tracking_no}` 占位符 | 提交时 |

**操作流程**

- 列表页 → 点击"新增承运商" → 新增页 → 保存 → 回到列表
- 列表页 → 点击"编辑" → 编辑页 → 保存 → 回到列表

**异常处理**

| 异常场景 | 处理方式 |
|----------|----------|
| 编码重复 | 提示"该编码已存在" |
| 停用承运商时有活跃运单 | 允许停用，但提示"该承运商下有 N 条活跃运单" |
| 停用后的影响 | 不再参与新运单注册的路由，已有运单追踪不受影响 |

**UI 关联**

- PC 端：后台原型 v5.11 — 承运商管理列表页、编辑承运商页、新增承运商页

---

### 2.3 追踪平台管理

#### 2.3.1 模块概述

管理物流追踪平台（AfterShip、快递100）的承运商映射配置。系统根据承运商的平台映射自动路由到对应平台获取轨迹。

---

#### 2.3.2 追踪平台管理后台（页面型）

**功能描述**

运营人员管理追踪平台的承运商映射关系。API 密钥及 Webhook 配置由开发维护。

**前置条件**

运营人员已登录后台系统。

**页面元素 — 列表页**

列表字段：

| 列名 | 说明 |
|------|------|
| ID | 平台ID |
| 平台名称 | AfterShip / 快递100 |
| 连接状态 | 正常 / 异常 + 最后检测时间 |
| 操作 | 编辑按钮 |

**页面元素 — 编辑页**

基本信息区（只读）：
- 平台名称
- 连接状态 + 最后检测时间

承运商映射管理区：
- 说明文案："配置该平台返回的承运商代码与 Looply 内部承运商的映射关系。创建运单时，系统通过此映射表将平台识别结果转换为内部承运商。"
- 新增映射按钮
- 映射列表：

| 列名 | 说明 |
|------|------|
| 追踪平台承运商代码 | 平台返回的 slug/code |
| Looply 承运商名称 | 映射到的内部承运商 |
| 状态 | 启用 / 停用 |
| 操作 | 编辑 / 删除 |

安全提示区：
- "API 密钥及 Webhook 配置由开发维护，如需变更请联系开发团队"

操作记录区：
- 操作时间、操作人、操作类型、操作内容

**校验规则**

| 字段 | 规则 | 校验时机 |
|------|------|----------|
| 追踪平台承运商代码 | 非空、同一平台内唯一 | 提交时 |
| Looply 承运商 | 必选，从承运商列表中选择 | 提交时 |

**操作流程**

- 列表页 → 点击"编辑" → 编辑页
- 编辑页 → 点击"新增映射" → 弹窗填写 → 保存
- 编辑页 → 点击映射行"编辑" → 弹窗修改 → 保存
- 编辑页 → 点击映射行"删除" → 确认后删除

**异常处理**

| 异常场景 | 处理方式 |
|----------|----------|
| 删除映射时有活跃运单使用该映射 | 允许删除，但提示"该映射下有 N 条活跃运单" |
| 平台承运商代码重复 | 提示"该代码已存在" |

**UI 关联**

- PC 端：后台原型 v5.11 — 追踪平台管理列表页、编辑追踪平台页（AfterShip）、编辑追踪平台页（快递100）

---

### 2.4 物流状态映射机制

#### 2.4.1 模块概述（机制型）

定义追踪平台原始状态到 Looply 8 个统一状态及用户端文案 key 的映射规则。平台原始 tag/state 只用于接入和排查，不直接作为 C 端展示文案。

**功能描述**

将 AfterShip 和快递100 的原始状态统一映射为 Looply 物流状态，同时通过 tracking_health 字段标记追踪系统健康度。

**规则说明**

AfterShip 状态映射：

| AfterShip Tag | 物流状态展示 | tracking_health |
|---------------|-------------|-----------------|
| Pending（001/003） | Pending | normal |
| Pending（002/004/006） | Pending | abnormal |
| Pending（005，120天无更新） | Exception | abnormal |
| InfoReceived | InfoReceived | normal |
| InTransit | InTransit | normal |
| OutForDelivery | OutForDelivery | normal |
| AvailableForPickup | AvailableForPickup | normal |
| AttemptFail | AttemptFail | normal |
| Delivered | Delivered | normal |
| Exception | Exception | normal |
| Expired（001） | Exception | abnormal |

快递100 状态映射：

| 快递100 state | 物流状态展示 | tracking_health |
|--------------|-------------|-----------------|
| 1 揽收 | InTransit | normal |
| 0 在途 | InTransit | normal |
| 5 派件 | OutForDelivery | normal |
| 3 签收 | Delivered | normal |
| 7 转投 / 8 清关 / 10 待清关 / 11 清关中 / 12 已清关 | InTransit | normal |
| 2 疑难 / 4 退签 / 6 退回 / 13 清关异常 / 14 拒签 | Exception | normal |
| abort（3天无记录/60天无变化） | — | abnormal |

> 说明：快递100首次推送即为已揽收节点（state=1 揽收），无独立的「待揽收」状态。注册成功但尚未收到推送时，shipment 的 internal_status 默认为 Pending（与 AfterShip 一致），收到首个推送后立即转为 InTransit。

轨迹事件入库时保留平台可读原始 message，并记录 mapped_internal_status 及其状态 `display_i18n_key`。本期不维护事件描述译文，面向 C 端生成 description 时按以下顺序处理：

1. 可读的承运商/平台原始 message。
2. 当前节点 mapped_internal_status 对应的目标 locale 状态文案。
3. 当前节点 mapped_internal_status 对应的 `en-US` 状态文案。

不得将未解析的 tag、subtag、state、statusCode 或 i18n key 直接作为 C 端文案。

**技术说明**

- tracking_health 标记的是"追踪系统本身是否正常工作"，不是"物流运输是否正常"
- 物流异常（AttemptFail/Exception）时 tracking_health = normal，因为追踪系统能正常获取到异常信息
- 后台监控 tracking_health，abnormal 持续超过 24 小时告警升级

**status_mappings 预填说明**

status_mappings 表由开发预填，初期不提供管理 UI。预填内容包括：

1. AfterShip 映射规则：tag + subtag → Looply 统一状态 + 状态 `display_i18n_key`
2. 快递100 映射规则：state + statusCode → Looply 统一状态 + 状态 `display_i18n_key`

映射表覆盖所有已知的 tag/subtag 和 state/statusCode 组合，新增承运商或追踪平台出现未知状态码时，系统记录日志并告警，由开发补充映射规则。

**统一状态文案 key**

| internal_status | `page_logistics_tracking` 状态 key | `en-US` 基线 |
|---|---|---|
| Pending | `logistics.status.pending` | Pending |
| InfoReceived | `logistics.status.info_received` | Info Received |
| InTransit | `logistics.status.in_transit` | In Transit |
| OutForDelivery | `logistics.status.out_for_delivery` | Out for Delivery |
| AvailableForPickup | `logistics.status.ready_for_pickup` | Ready for Pickup |
| AttemptFail | `logistics.status.delivery_attempt_failed` | Delivery Attempt Failed |
| Delivered | `logistics.status.delivered` | Delivered |
| Exception | `logistics.status.delivery_exception` | Delivery Exception |

同一 internal_status 在所有平台复用同一个状态 key。平台事件 message 不生成 i18n key，不由前端或物流服务根据原文动态创建翻译记录。

**状态转移规则**

| 规则 | 说明 |
|------|------|
| 终态集合 | Delivered 为唯一终态 |
| 终态保护 | 已 Delivered 的运单，后续非终态推送（如 InTransit）仅落库到 checkpoints，不回退 internal_status |
| Exception 可恢复 | Exception 不是终态；后续收到 InTransit/OutForDelivery/Delivered 推送时，正常推进 internal_status |
| 时间戳排序 | 用事件时间（checkpoint_time）而非接收时间判断先后，解决乱序推送 |
| cancelled 后处理 | record_status=cancelled 后，平台推送仍可能到达；系统记入 message_logs 但不落库到 checkpoints、不更新 internal_status |
| 同状态去重 | 同一 shipment 连续收到相同 (checkpoint_time, platform_tag, message) 的节点，视为重复推送，不重复落库 |

---

### 2.5 快递100 特有机制

#### 2.5.1 模块概述（机制型）

快递100 与 AfterShip 存在若干差异化机制，需要 Looply 统一抽象层正确处理。

**规则说明**

| 机制 | 说明 |
|------|------|
| 每月订阅次数限制 | 同一运单号+承运商组合每月最多订阅 4 次（快递100平台限制；DELETE 后再 POST 也会消耗额度） |
| 自动承运商纠错 | 快递100 3天无结果时自动识别正确承运商并重新订阅（autoCheck=1） |
| abort 自动停止 | 3天无记录或60天无变化后自动停止监控 |
| 顺丰手机号验证 | 顺丰速运/顺丰快运必须提供寄/收件人手机号（后4位即可） |
| 推送格式差异 | form-urlencoded（param 为 JSON 字符串），签名为 MD5(param + salt) |
| 回调确认格式 | 必须返回 `{"result":true,"returnCode":"200","message":"成功"}` |

**订阅额度告知策略**

- GET /carriers 返回的快递100承运商，附加 `subscription_quota` 字段：`{used: 2, limit: 4, reset_at: '2026-06-01'}`
- POST /trackings 注册成功后，响应体附加 `quota_remaining` 字段提示当月剩余次数
- 当月剩余次数 ≤ 1 时，PATCH 接口返回 `LOW_QUOTA_WARNING`，提示调用方谨慎使用
- 额度耗尽时返回 `QUOTA_EXHAUSTED`（对应快递100 returnCode 702），message 含 `reset_at` 时间

> 说明：`LOW_QUOTA_WARNING` 和 `QUOTA_EXHAUSTED` 为 Looply 自定义错误码，非快递100平台返回。快递100仅在额度耗尽时返回 returnCode 702，Looply 在此基础上增加了"剩余 ≤ 1 时预警"的产品逻辑。待快递100错误处理规范升级 v1.1 时补入。

**自动纠错处理流程**

1. 识别自动纠错场景：快递100 Webhook 推送中 `autoCheck=1` 且包含 `comOld`/`comNew` 字段
2. 更新本地记录：将 shipment 的 carrier_id 更新为 `comNew` 对应的 Looply 承运商
3. 通知调用方：发送承运商变更通知，包含原承运商、新承运商、变更原因（「快递100自动识别」）
4. 记录审计日志：在 message_logs 中记录完整的自动纠错过程

abort 处理：
- 标记 tracking_health = abnormal
- 通知调用方（附操作建议）
- 如需继续追踪需重新订阅（受每月4次限制）

---

### 2.6 C 端消费与多语言输出（机制型）

**功能描述**

物流服务向订单等业务系统提供单 shipment 的统一状态、承运商、运单号、AI EDD 和完整轨迹，并根据调用方传入的 locale 生成可直接面向用户展示的状态文案。PC、APP、H5 的页面结构、交互、固定 UI 文案和异常态统一由《looply-前端物流轨迹-PRD-v1.8》定义。

**触发条件**

- 订单详情加载状态卡数据。
- 用户打开 Tracking details 时再次查询最新轨迹。
- 用户切换界面语言后重新打开轨迹详情。
- 客服等有权限的业务系统按需查询物流信息。

**语言上下文规则**

1. 调用方传入当前界面 locale；服务端按 BCP 47 形式标准化，如 `en-US`、`es-US`。
2. locale 缺失、格式非法或当前不支持时，统一降级为 `en-US`，不得因语言参数导致整单轨迹查询失败。
3. 同一响应中的 statusLabel 和所有 checkpoint description 使用同一次语言决策，避免混合语言。
4. 本地化响应缓存必须包含 locale 维度；不同语言不得共用已渲染文案缓存。
5. 状态码、i18n key、原始 message 和事实数据不随 locale 改变。

**查询输出规则**

| 数据 | 服务端输出职责 | 多语言处理 |
|---|---|---|
| shipment_id、business_order_no、tracking_no | 返回稳定身份和业务关联 | 原值，不翻译 |
| carrier | 返回统一承运商信息 | 名称原值，不翻译 |
| internal_status | 返回 Looply 8 值状态码 | 语言无关 |
| statusI18nKey | 返回稳定状态 key | 语言无关；见 2.4 |
| statusLabel | 返回目标 locale 的用户端状态文案 | 从 `page_logistics_tracking` 读取；缺失回退 `en-US` |
| eta_min、eta_max、eta_confidence_code | 返回 AI EDD 日期事实 | shipment 目的地当地日历日期；美国等多时区国家按该票目的地地址解释。不做时区转换，不随查询用户时区或 locale 改变，不返回拼接后的日期文案 |
| checkpoint mappedStatus | 返回节点映射状态 | 语言无关 |
| checkpoint statusI18nKey | 返回 mapped_internal_status 对应的状态 key | 与当前节点状态一致，来自 `page_logistics_tracking` 的8个状态记录 |
| checkpoint description | 返回可读渠道事件原文；不可读时返回本地化状态文案 | 事件原文不翻译、不进翻译中心 |
| checkpoint originalDescription | 返回平台可读原文供排查和展示使用 | 原值 |
| location、country_iso3 | 返回地点事实 | 原值，不翻译 |
| checkpoint_time | 返回 UTC 事件时间 | 消费端转换用户时区并按 locale 格式化 |

**状态和事件描述回退**

- statusLabel：目标 locale 状态文案 → `en-US` 状态文案。不得回退到平台 tag/state。
- checkpoint description：可读平台原始 message → 目标 locale 状态文案 → `en-US` 状态文案。
- 任一级结果为空、仅含代码或不可读时继续进入下一层。
- 最终不得返回空 description、未解析 i18n key、平台错误码或纯 tag/subtag 作为用户端文案。

**异步通知与查询的差异**

- 查询响应面向具体用户语言，可返回 statusLabel 和本地化 description。
- 轨迹更新异步通知面向业务系统，保持语言无关，核心传递状态码、i18n key、原始事实及 `en-US` 兼容文案。
- 业务系统向具体用户发送通知或展示页面时，使用用户 locale 重新获取本地化结果；不得把某一默认语言通知文案视为所有用户的最终展示文案。

**翻译归属清单**

| 业务内容 | 内容类别 | 翻译归属 | 翻译中心卡片决策 | resourceType |
|---|---|---|---|---|
| C 端标题、标签、按钮、Toast、空态、错误态 | 静态 UI 文案 | `page_logistics_tracking` → 前端语言包 | 写入物流轨迹卡片 | `page_logistics_tracking` |
| 物流状态文案 | 8 个静态枚举文案 | `page_logistics_tracking` → 物流服务 | 写入同一物流轨迹卡片 | `page_logistics_tracking` |
| 平台事件 message | 动态第三方内容 | 保留可读原文 | 不写入卡片、不按 checkpoint 建记录 | — |
| 地点、承运商、运单号 | 不翻译 | 原值 | 不进入业务卡片 | — |
| ETA、轨迹时间 | 日期时间格式化 | 消费端 locale formatter | 不进入业务卡片 | — |

**物流轨迹卡片注册**

| 配置项 | 定义 |
|---|---|
| domain / domainName | 前端页面 / 前端页面 |
| 卡片名称 | 物流轨迹 |
| resourceType | `page_logistics_tracking` |
| 源语言 | `en-US` |
| 目标语种 | 跟随平台启用语种 |
| 运营路径 | 多语言管理 → Translation → 前端页面 → 物流轨迹 |
| 记录范围 | 15 条固定 UI key + 8 条统一状态 key，共 23 条基础记录 |
| fieldName | `text` |
| resourceId | 对应稳定 i18n key |

新卡片必须先通过 migration 写入 `translation_resource` 并注册 `text` 字段，再推送23条源文。checkpoint、平台原始 message、承运商、运单号、地点、ETA和时间事实均不写入该卡片。

**源文同步与译文消费**

1. 前端团队维护15条固定 UI key 及 `en-US` 源文，物流服务维护8条状态 key 及 `en-US` 源文；双方使用同一 resourceType，禁止创建重复 key。
2. 源文以 `(page_logistics_tracking, i18nKey, text)` 定位，其中 `resourceId = i18nKey`、`fieldName = text`。
3. 前端固定 UI 译文由翻译平台同步至前端语言包；物流服务在生成 statusLabel 时按 locale 读取8个状态 key 的译文并缓存。
4. 源文变更后更新同一 resourceId，不新增另一条记录；已有译文按翻译中心源文变更规则标记重新确认。
5. 翻译中心不可用时不阻断物流事实查询：优先使用已缓存译文，其次使用本地 `en-US` 状态基线。

**异常与监控**

| 场景 | 处理 |
|---|---|
| locale 非法或不支持 | 降级 `en-US`，记录标准化结果，不中断查询 |
| 目标语言译文缺失 | 按回退链处理，并记录缺失 key、locale、平台和状态码 |
| i18n key 未注册 | 不返回 key 字符串给 C 端；继续回退并触发配置告警 |
| 平台 message 不可读 | 跳过原文层，回退目标 locale 状态文案；缺失时再回退 `en-US` 状态文案 |
| 翻译中心查询暂不可用 | 使用已缓存译文；缓存缺失时使用本地 `en-US` 状态基线，核心事实查询仍可用 |

**验收标准**

1. 同一 shipment 使用不同受支持 locale 查询时，状态码、i18n key、ETA、轨迹事实和可读渠道 description 一致，仅 statusLabel 及由状态兜底的 description 随语言变化。
2. locale 缺失、非法或不支持时返回 `en-US` 文案，查询不失败。
3. 渠道事件原文可读时原样返回；不可读时回退本地化状态文案，不返回空 description、未解析 key 或平台纯代码。
4. AfterShip 与快递100映射到相同 Looply 状态时，返回相同 statusI18nKey。
5. 异步通知不固化具体用户语言，包含状态码和稳定 i18n key。
6. 本地化缓存按 locale 隔离，切换语言后不会复用上一语言文案。
7. 固定 UI 和8个状态 key 写入 `page_logistics_tracking`；checkpoint 实例和平台原始 message 不生成翻译记录。
8. AI EDD 日期不因请求 locale 或用户时区发生日期加减；checkpoint_time 始终保持 UTC 事实值。
9. 美国等多时区国家使用不同用户时区和 locale 查询同一 shipment 时，eta_min、eta_max 日期事实完全一致；服务端和消费端均不得根据查看者时区重新换算。
10. 国际段目的地信息不足时，轨迹注册仍可成功；AI EDD 允许为空，并记录目的地信息完整度用于联调和监控，不生成猜测日期。
11. 翻译中心“前端页面”域可查看“物流轨迹”卡片，卡片包含23条基础记录且无 checkpoint 记录。

**前端需求引用**

- 页面与交互：《looply-前端物流轨迹-PRD-v1.8》
- PC Figma：[Looply 1.1 — PC Tracking details](https://www.figma.com/design/sAOLkw0gIl1bwQRYCDqKuW/Looply-1.1?node-id=32-296&p=f&m=dev)，node `32:296`
- 移动端 APP/H5 Figma：[Looply 1.1 — Mobile Tracking details](https://www.figma.com/design/sAOLkw0gIl1bwQRYCDqKuW/Looply-1.1?node-id=9-11674&p=f&m=dev)，node `9:11674`

---

### 2.7 接口能力汇总

#### 2.7.1 接口清单

物流信息服务对外提供 9 个接口能力，分为三类：

**一、运单生命周期管理（5个）**

| # | 接口 | 方法 | 说明 |
|---|------|------|------|
| 1 | 注册运单追踪 | POST /trackings | 调用方注册运单，成功后返回 shipment_id（UUID），后续操作统一使用该 ID（详见 2.1.2） |
| 2 | 查询运单状态 | GET /trackings/{shipment_id} | 查询单个运单的当前状态和最新轨迹（详见 2.1.8） |
| 3 | 查询运单轨迹 | GET /trackings/{shipment_id}/checkpoints | 查询运单的完整轨迹节点列表（详见 2.1.8） |
| 4 | 修改运单信息 | PATCH /trackings/{shipment_id} | 承运商或运单号填错时修正，触发平台切换（详见 2.1.3） |
| 5 | 取消运单追踪 | DELETE /trackings/{shipment_id} | 业务取消时，标记 cancelled 并停止追踪（详见 2.1.4） |

**二、批量与查询（2个）**

| # | 接口 | 方法 | 说明 |
|---|------|------|------|
| 6 | 批量查询运单状态 | GET /trackings | 支持按业务单号、状态、承运商等条件筛选（详见 2.1.8） |
| 7 | 获取承运商列表 | GET /carriers | 返回可用承运商枚举，供调用方下拉选择（详见 2.1.8） |

**三、状态通知（推送）（2个）**

| # | 接口 | 方法 | 说明 |
|---|------|------|------|
| 8 | 轨迹更新通知 | — | 每次轨迹更新主动通知调用方，含 is_status_changed 标志（详见 2.1.5；通道由技术侧决定） |
| 9 | 追踪异常/恢复通知 | — | tracking_health 在 normal/abnormal 间切换时通知调用方（详见 2.1.6） |

#### 2.7.2 接口路径参数统一约定

| 路径参数 | 含义 | 适用接口 |
|----------|------|---------|
| `{shipment_id}` | 运单 UUID（注册时生成，不可变） | 全部对外接口统一使用（GET/PATCH/DELETE） |
| `tracking_no` | 运单号（业务可读，可被 PATCH 修改） | 作为查询参数或请求体字段，不作为路径参数 |

注册接口（POST /trackings）成功后响应体返回 `shipment_id`，调用方后续所有操作（查询/修改/取消）统一使用该 ID。

#### 2.7.3 设计原则

1. **注册失败不建记录**：所有追踪平台错误同步返回，shipments 表只有「真正可追踪」的运单
2. **运单号唯一**：1 tracking_no = 1 shipment（同一 active 运单号不可重复）；1 business_order_no = N shipment（拆包场景下同一订单可有多个包裹）
3. **接口路径使用不可变 ID**：shipment_id（UUID）注册时生成，不可变；tracking_no 可被 PATCH 修改，因此不作为路径参数
4. **幂等键 = (tracking_no, carrier_id)**：同一组合重复注册返回已有记录；tracking_no 相同但 carrier_id 不同视为独立运单
5. **business_order_no 不可修改**：注册后禁止修改，填错则 DELETE + 重新 POST
6. **状态通知通道不限**：产品只定义业务要求，具体通道（HTTP/MQ）由技术侧决定
7. **追踪异常与物流异常分离**：tracking_health 标记追踪系统问题，internal_status 标记物流运输问题
8. **校验分层**：Looply 基础校验（本地毫秒级）→ 追踪平台校验（远程秒级）
9. **错误响应可操作**：每个错误必须包含 action 字段告诉调用方下一步怎么做

---

## 三、依赖与风险

### 上下游系统依赖

| 依赖方 | 依赖内容 | 影响 |
|--------|----------|------|
| 卖家系统 | 调用注册运单 API | 运单数据来源 |
| 订单/买家系统 | 传入用户 locale，消费本地化状态、ETA 和轨迹数据 | C 端数据消费 |
| 客服系统 | 调用查询 API | 客服查看物流状态 |
| 订单系统 | 接收状态变更通知 | 更新订单物流状态 |

### 外部服务依赖

| 服务 | 用途 | 风险 |
|------|------|------|
| AfterShip | 国际段物流追踪 | API 限流（429）、服务不可用（5xx） |
| 快递100 | 国内段物流追踪 | 每月订阅次数限制、abort 自动停止 |

### 风险项

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| AfterShip 服务不可用 | 国际段运单无法注册/无轨迹更新 | 错误码映射 + 自动重试 + 查询接口兜底 |
| 快递100 月度额度用尽 | 国内段运单无法修改/重新订阅 | 提前告知调用方剩余次数 |
| 承运商映射缺失 | 新承运商无法路由 | 注册时校验映射存在性，缺失时返回明确错误 |
| Webhook 推送延迟 | 轨迹更新不及时 | 调用方可通过查询接口主动获取 |
| 物流轨迹卡片缺状态 key 或目标语种译文 | C 端出现英文降级 | 注册时校验23条基础记录；运行时按状态回退链处理并告警 |
| 本地化缓存未隔离 locale | 用户看到其他语言文案 | 所有渲染后文案缓存键包含 locale |

---

## 四、版本规划

### 当前实现范围（v1.7）

- 运单注册、查询、修改、取消全生命周期管理
- AfterShip + 快递100 双平台对接
- 承运商管理 + 追踪平台承运商映射管理
- 物流状态通知 + 追踪异常通知
- 后台运单管理页面
- C 端统一物流数据消费与服务端多语言输出
- 统一错误处理规范

### 后续迭代方向

| 方向 | 说明 |
|------|------|
| 状态映射管理 UI | 接入第二个追踪平台时开发后台管理界面 |
| 轨迹事件译文 | 仅当未来需要翻译渠道事件原文时，在现有物流轨迹卡片扩展或另立事件模板方案；本期不维护 |
| 消息日志查看 | 后台可视化查看运单的完整消息链路 |
| 批量导入 | 支持批量运单号导入注册 |
| 识别准确率统计 | 记录自动识别 vs 手动修正比例，持续优化 |
| 多平台冗余 | 主平台失败时自动切换备用平台 |

---

## 五、附录

### 数据模型字段清单

#### shipments 表（运单表）

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | BIGINT | 主键，内部使用 |
| shipment_id | UUID | 对外主键（注册时生成，不可变），所有对外接口使用此字段 |
| tracking_no | VARCHAR(100) | 运单号（可被 PATCH 修改；联合 carrier_id 在 active 状态下唯一） |
| business_order_no | VARCHAR(64) | 业务单号（普通索引，非唯一；同一订单拆包时多条 shipment 共享） |
| carrier_id | BIGINT | 承运商ID（外键） |
| tracking_platform_id | BIGINT | 追踪平台ID（外键） |
| platform_tracking_id | VARCHAR(100) | 追踪平台内部ID（AfterShip tracking.id / 快递100订阅ID） |
| platform_status | VARCHAR(50) | 平台原始状态（用于调试和映射回溯） |
| internal_status | VARCHAR(50) | 物流状态（Pending/InfoReceived/InTransit/OutForDelivery/AttemptFail/AvailableForPickup/Delivered/Exception，共 8 值；不含 Expired，详见 2.4） |
| record_status | VARCHAR(20) | 记录状态（active/cancelled） |
| tracking_health | VARCHAR(20) | 追踪健康度（normal/abnormal） |
| source | VARCHAR(50) | 来源系统标识（seller-system/ops-system/cs-system 等） |
| phone | VARCHAR(20) | 承运商附加字段（如顺丰手机号后4位） |
| cancel_reason | VARCHAR(50) | 取消原因（仅 business_cancelled 一个枚举） |
| cancelled_at | TIMESTAMP | 取消时间 |
| eta_min | DATE | AI EDD 预计送达起始日（aftership_estimated_delivery_date.estimated_delivery_date_min，shipment 目的地当地日历日；美国等多时区国家按该票目的地地址解释，不转 UTC；无则 NULL） |
| eta_max | DATE | AI EDD 预计送达结束日（estimated_delivery_date_max；日期语义与 eta_min 一致；单日期时与 eta_min 相等；无则 NULL） |
| eta_confidence_code | VARCHAR(20) | AI EDD 置信度码（confidence_code；用于展示决策，无则 NULL） |
| last_tracking_update | TIMESTAMP | 最后轨迹更新时间（后台列表"最后更新"列数据源） |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

**命名说明**：`internal_status` 是历史命名，对应 1.6 术语表中的「物流状态（Tracking Status）」，与「记录状态（record_status）」语义独立。后续如建立 Looply 内部状态体系，会评估是否将 internal_status 改名为 tracking_status。

#### carriers 表（承运商表）

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | BIGINT | 主键 |
| name | VARCHAR(100) | 承运商名称（如「顺丰速运（国内）」） |
| code | VARCHAR(50) | 承运商编码（唯一，区分国内国际，如 sf-domestic / sf-international） |
| tracking_url_template | VARCHAR(500) | 轨迹查询URL模板（含 {tracking_no} 占位符） |
| logo_url | VARCHAR(500) | 承运商 Logo 图片地址（选填，供 C 端按需使用） |
| status | VARCHAR(20) | 状态（enabled/disabled） |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

#### tracking_platforms 表（追踪平台表）

> 列名以 ER v2.7 为准。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | BIGINT | 主键 |
| name | VARCHAR(50) | 平台名称（AfterShip/快递100） |
| platform_type | VARCHAR(20) | 平台类型（国际聚合/国内聚合） |
| connection_status | VARCHAR(20) | 连接状态（normal/abnormal） |
| last_checked_at | TIMESTAMP | 最后检测时间 |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

> API Key / Webhook 等加密配置字段见 ER v2.7，由开发维护，不在运营管理范围。

#### platform_carrier_mappings 表（平台承运商映射表）

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | BIGINT | 主键 |
| tracking_platform_id | BIGINT | 追踪平台ID（外键） |
| platform_carrier_code | VARCHAR(50) | 平台承运商代码（AfterShip slug / 快递100 code） |
| carrier_id | BIGINT | Looply 承运商ID（外键） |
| status | VARCHAR(20) | 状态（enabled/disabled） |

#### tracking_checkpoints 表（轨迹节点表）

> 列名以 ER v2.7 为准。去重联合唯一索引：(shipment_id, checkpoint_time, platform_tag, message)。
> v1.7 未新增字段；既有 `display_i18n_key` 统一保存 mapped_internal_status 对应的状态 key，适用于全部平台。ER v2.7 字段注释需同步，数据库无需新增列。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | BIGINT | 主键 |
| shipment_id | BIGINT | 运单ID（外键） |
| platform_tag | VARCHAR(50) | 平台一级状态（AfterShip tag / 快递100 state，存原始值） |
| platform_subtag | VARCHAR(50) | 平台二级状态（AfterShip subtag / 快递100 statusCode） |
| message | TEXT | 平台返回的可读事件原文（AfterShip message / subtag_message，快递100 context）；用于审计与本地化回退，不作为固定 C 端文案 |
| mapped_internal_status | VARCHAR(50) | 映射后 Looply 物流状态（接收即映射） |
| display_i18n_key | VARCHAR(100) | mapped_internal_status 对应的状态 i18n key；AfterShip、快递100均使用 |
| location | VARCHAR(200) | 地点（快递100 无独立字段，存 NULL） |
| country_iso3 | VARCHAR(3) | 国家代码（ISO3；国内段默认 CHN） |
| checkpoint_time | TIMESTAMP | 事件时间（UTC，前台展示时转用户本地时区） |
| raw_payload | JSON | 原始报文（排查用） |
| created_at | TIMESTAMP | 落库时间 |

#### status_mappings 表（状态映射表）

> 由开发预填，初期不提供管理 UI。
> v1.7 未新增字段；ER v2.7 中“仅国际平台使用”的旧注释需同步为“全部追踪平台使用状态 key”。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | BIGINT | 主键 |
| tracking_platform_id | BIGINT | 追踪平台ID（外键） |
| platform_status_code | VARCHAR(50) | 平台一级状态（AfterShip tag / 快递100 state） |
| platform_sub_code | VARCHAR(50) | 平台二级状态（AfterShip subtag / 快递100 statusCode） |
| internal_status | VARCHAR(50) | 映射后的 Looply 物流状态 |
| tracking_health | VARCHAR(20) | 映射后的追踪健康度（normal/abnormal） |
| display_i18n_key | VARCHAR(100) | internal_status 对应的状态 i18n key；所有追踪平台复用同一组8个 key |
| sort_order | INT | 排序 |

#### message_logs 表（消息记录表）

> 核心字段如下，详细字段定义由开发根据实际需求扩展。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | BIGINT | 主键 |
| shipment_id | BIGINT | 关联运单（注册失败时为 NULL） |
| direction | VARCHAR(30) | 数据流向（inbound_api / outbound_platform / inbound_webhook / outbound_push） |
| event | VARCHAR(50) | 事件名（registerTracking / createTracking / tracking_update / statusNotify） |
| status | VARCHAR(20) | 处理状态（success / failed） |
| created_at | TIMESTAMP | 创建时间 |

### 设计稿索引

> C 端物流轨迹页面已拆分至《looply-前端物流轨迹-PRD-v1.5》，本表仅保留物流服务后台页面。

| 页面 | PC 端 | APP/H5 端 |
|------|-------|------------|
| 运单管理 — 列表 | 后台原型 v5.11 | — |
| 运单管理 — 详情 | 后台原型 v5.11 | — |
| 运单管理 — 已取消详情 | 后台原型 v5.11 | — |
| 承运商管理 — 列表 | 后台原型 v5.11 | — |
| 承运商管理 — 编辑 | 后台原型 v5.11 | — |
| 承运商管理 — 新增 | 后台原型 v5.11 | — |
| 追踪平台管理 — 列表 | 后台原型 v5.11 | — |
| 追踪平台管理 — 编辑（AfterShip） | 后台原型 v5.11 | — |
| 追踪平台管理 — 编辑（快递100） | 后台原型 v5.11 | — |

### 关联文档

| 文档 | 路径 |
|------|------|
| 三方报文字段映射规范（AfterShip）v1.1 | 需求分析/物流服务_三方报文字段映射规范_aftership_v1.1.md |
| API 错误处理规范（快递100） | 需求分析/物流服务_API错误处理规范_快递100_v1.2.md |
| 设计讨论归档 v5.7 | 需求分析/物流服务_设计讨论归档_v5.7.md |
| 设计讨论归档 v5.8 | 需求分析/物流服务_设计讨论归档_v5.8.md |
| 实体关系图 v2.7 | 实体关系图/looply-物流管理实体关系图-v2.7.svg |
| 产品架构图 | 产品架构图/looply-物流管理产品架构图.svg |
| 竞品调研报告 | 需求分析/looply-物流管理-竞品调研报告-v1.0.md |
| 前端物流轨迹 PRD v1.8 | PRD/looply-前端物流轨迹-PRD-v1.8.md |
| 多语言对接与翻译卡片归属说明 | 需求分析/prd-translation-card-placement-product-sync.md |
| PC 物流轨迹 Figma | [Looply 1.1 — PC Tracking details](https://www.figma.com/design/sAOLkw0gIl1bwQRYCDqKuW/Looply-1.1?node-id=32-296&p=f&m=dev)，node 32:296 |
| 移动端 APP/H5 物流轨迹 Figma | [Looply 1.1 — Mobile Tracking details](https://www.figma.com/design/sAOLkw0gIl1bwQRYCDqKuW/Looply-1.1?node-id=9-11674&p=f&m=dev)，node 9:11674 |
| ~~承运商识别机制设计文档 v1.0~~（已废弃归档） | 该方案基于"运营录入+自动识别+17track"，与本 PRD"业务系统 API 注册"架构不符，已废弃，不作为开发依据 |

**版本管理说明**

- 三方报文字段映射规范、API 错误处理规范与 PRD 独立维护
- 规范文档更新时，PRD 中引用该规范的章节（2.1.2、2.1.3、2.4 等）需同步评审是否需要调整
- 如规范文档新增错误码或修改映射规则，PRD 维护者需确认是否影响产品规则
- internal_status 状态空间（8 值，不含 Expired）、字段命名（以 ER v2.7 为准）变更时，须同步评审本 PRD 附录、各 API 规范及三方报文字段映射规范
