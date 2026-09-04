# Looply C1 Sell 运营后台 PRD

版本：v1.2
日期：2026-09-04
状态：开发评审候选版

## 一、范围与入口

C1 Sell 运营后台位于 `https://ops.looply.com/`，与 C2 运营模块独立登录。当前版本包含三个一级入口：`ZIP Coverage`、`Categories & Brands`、`Appointments`。预约提交后发送确认邮件，邮件结果在 Appointments 中查看和处理。

当前使用角色为 C1 运营人员。预约原始提交信息只读；运营人员可以维护覆盖配置、品类和品牌配置、预约内部备注，并下载当前筛选结果。

页面流转：

`ZIP Coverage 列表 → Add ZIP code / 列表内切换状态`

`Categories 列表 → Category 下的 Brands 列表 → Add brand / Edit brand`

`Appointments 列表 → 行内展开预约详情 → 新增或编辑内部备注`

## 二、ZIP Coverage

### 2.1 列表

列表展示 `ZIP code`、`City`、`State`、`Status`、`Updated at`。支持按 ZIP、City 或 State 搜索。

每个 ZIP 使用一个独立配置项，状态枚举如下：

| 枚举值 | 含义 | 触发时机 | 前台结果 |
|---|---|---|---|
| `Active` | 当前 ZIP 支持 In-Home Service | 新增时默认使用 Active，或在列表中切换为 Active | 参与前台 Service Area 查询和预约方式推荐 |
| `Inactive` | 当前 ZIP 不支持 In-Home Service | 在列表中切换为 Inactive | 不参与前台覆盖判断 |

列表包含正常数据、加载、无数据、无匹配和加载失败状态。无匹配时保留搜索条件并显示 `No results`；加载失败时显示 `Something went wrong. Please try again.` 和 `Retry`。

### 2.2 新增与状态切换

| 字段 | 必填 | 规则 |
|---|---:|---|
| ZIP code | 是 | 5 位数字；同一 ZIP 不可重复；保存后不可修改 |
| City | 系统回填 | 输入有效 ZIP 后复用现有 `Postal/addressconfig` 回填，只读 |
| State | 系统回填 | 输入有效 ZIP 后复用现有 `Postal/addressconfig` 回填，只读 |
| Status | 是 | `Active` 或 `Inactive`；新增时默认为 `Active` |

输入满足 5 位格式后开始查询 City 和 State。查询中显示 Loading；查询失败时保留 ZIP，允许 Retry；无法匹配时提示 `We couldn't find a city and state for this ZIP code.`。City、State 回填成功且所有必填项有效后方可保存。

保存成功后关闭表单、刷新列表并更新 `Updated at`；保存失败时保留已填内容并提示重试。运营人员在列表中通过状态开关直接切换 Active / Inactive；切换成功后更新 `Updated at`，失败时恢复原状态并提示重试。

## 三、Categories & Brands

Category 与 Brand 按两级关系维护，一个 Brand 归属于一个 Category。前台 Accepted Brands 和预约品牌联想读取当前生效配置，并使用后台保存顺序展示。

### 3.1 Categories

列表展示拖拽手柄、`Category`、`Active brand count`、`Status`、`Updated at`。`Active brand count` 统计该 Category 下 Status 为 `Active` 的 Brand 数量，与 Category 自身 Status 无关。支持按 Category name 搜索；点击 Category 名称进入该 Category 的 Brands 列表。

| 字段 | 必填 | 规则 |
|---|---:|---|
| Category name | 是 | 在 C1 Sell 范围内大小写不敏感且不可重复 |
| Status | 是 | `Active` 或 `Inactive` |

运营人员可以新增、编辑名称、启用或停用品类，并通过拖拽调整顺序。存在搜索词时禁用拖拽并提示清空搜索后排序。拖拽成功后保存新顺序并更新受影响记录的 `Updated at`；保存失败时恢复操作前顺序并提示重试。

`Active` Category 在前台展示并可供用户选择；`Inactive` Category 不进入前台配置读取结果。停用品类不修改其下 Brand 的状态；重新启用品类后，仅其下 `Active` Brand 恢复前台可见。

Category name 属于动态业务内容：business object 为 `Seller Category`，`resourceType=seller_category`，`fieldName=name`；覆盖 Accepted Brands 和预约 Step 2，源语言为英语、目标语言为西语，西语译文缺失时回退英语。翻译配置复用现有翻译能力，本后台不新增翻译入口。后台内部字段和内部备注不翻译。

### 3.2 Brands

Brands 列表展示拖拽手柄、`Brand`、`Status`、`Updated at`，支持按 Brand name 搜索。

| 字段 | 必填 | 规则 |
|---|---:|---|
| Brand name | 是 | 同一 Category 下大小写不敏感且不可重复 |
| Status | 是 | `Active` 或 `Inactive` |

运营人员可以新增、编辑名称、启用或停用品牌，并通过拖拽调整该 Category 下的品牌顺序。存在搜索词时禁用拖拽并提示清空搜索后排序。拖拽成功后保存新顺序并更新受影响记录的 `Updated at`；保存失败时恢复操作前顺序并提示重试。

只有所属 Category 和 Brand 均为 `Active` 时，该品牌才进入前台 Accepted Brands 和预约品牌联想。未配置或未生效品牌不出现在联想结果中，但不限制用户在预约表单中自由输入品牌。

同名 Brand 可分别配置在不同 Category 下。前台 `All` 视图或用户同时选择多个 Category 时，按 Brand name 大小写不敏感去重，并按“Category 后台顺序 → Category 内 Brand 后台顺序”取首次出现项。Brand name 作为专有名称不翻译。

Categories 和 Brands 列表均包含正常数据、加载、无数据、无匹配和加载失败状态；新增、编辑或状态保存失败时保留当前输入并提示重试。

## 四、Appointments

### 4.1 列表、查询与下载

用户成功提交 Seller Request 后，后台立即新增一条预约记录。Appointment 不设置业务状态。

列表展示：

| 列 | 说明 |
|---|---|
| Request ID | 系统生成的唯一申请编号；点击后展开当前行详情 |
| Full name | `First name + Last name` |
| Email | 用户提交的 Email |
| Selling method | `In-Home Appointment`、`Visit Looply` 或 `Ship To Us` |
| Categories | 用户多选结果 |
| Brands | 用户多选或自由输入结果 |
| Total pieces | `1–2`、`3–5`、`6–9` 或 `10+` |
| ZIP / State | 最终履约地址的 ZIP 和 State；Visit Looply 固定展示 `90048 / CA` |
| Preferred date | 用户未填写时展示 `—` |
| Submitted at | 用户正式提交时间 |
| Confirmation email status | `Pending`、`Sent` 或 `Failed` |
| View | 展开或收起当前行详情 |

关键词搜索仅匹配 `Request ID`、`Full name`、`Email`。Submitted at 支持起止日期筛选，默认最近 7 天并包含起止日；起始日期晚于结束日期时阻止查询并提示 `Start date cannot be later than end date.`。日期筛选按美东时区 `America/New_York` 的自然日边界计算，并自动适配夏令时。

`Download` 导出当前关键词和日期筛选共同命中的全部记录，不只导出当前分页。无匹配记录时按钮置灰。文件每行对应一条预约；CSV 不包含图片文件、照片链接或 Attachment ID。CSV 字段按以下顺序固定：

| 分组 | CSV 字段 |
|---|---|
| Request | Request ID、Submitted at、Selling method |
| Personal information | First name、Last name、Phone、Email、Contact authorization result、Contact authorization accepted at |
| Item information | Categories、Brands、Total pieces、Additional notes |
| ZIP recommendation | Step 3 submitted ZIP、In-Home coverage result |
| Method information | Street address、Apartment、City、State、ZIP code、Looply address、Preferred date、Referral code、Seller Agreement acceptance result、Seller Agreement version、Seller Agreement accepted at；不适用字段留空 |
| Confirmation email | Confirmation email status、Last attempted at、Failure reason；非 Failed 时 Failure reason 留空 |
| Internal note | Internal note、Internal note created at、Internal note updated at、Internal note operator |

每次成功触发 Download 后记录以下信息：

| 字段 | 记录内容 |
|---|---|
| Operator account | 当前登录账号 |
| Downloaded at | 实际触发下载的时间 |
| Search keyword | 当前关键词；未填写时记为空 |
| Submitted at range | 当前起止日期 |
| Exported record count | 本次导出的预约记录数 |

下载记录由系统保存，本版本不新增下载记录查看页面。下载生成失败时不产生成功下载记录，并提示用户重试。

### 4.2 行内详情

点击 `View` 后在当前行下方展开详情；再次点击 `Hide` 收起。详情中的用户提交信息只读，按以下分区展示。

**公共信息**

| 分区 | 字段 |
|---|---|
| Request | Request ID、Submitted at、Selling method |
| Personal information | First name、Last name、Phone、Email、Contact authorization result、Contact authorization accepted at |
| Item information | Categories、Brands、Total pieces、Additional notes、Photos |
| ZIP recommendation | Step 3 submitted ZIP、In-Home coverage result |
| Confirmation email | Confirmation email status、Last attempted at；失败时同时展示失败原因和 `Resend email` |

照片按用户上传顺序展示，最多 10 张；无照片时展示 `—`。Additional notes 未填写时展示 `—`。

**按 Selling method 展示的信息**

| Selling method | 字段 |
|---|---|
| In-Home Appointment | Street address、Apartment、City、State、ZIP code、Preferred date、Referral code、Seller Agreement version、Seller Agreement accepted at |
| Visit Looply | 固定 Looply address、Preferred date、Referral code |
| Ship To Us | Street address、Apartment、City、State、ZIP code、Seller Agreement acceptance result、Seller Agreement version、Seller Agreement accepted at |

`Apartment`、`Preferred date`、`Referral code` 等选填字段未填写时展示 `—`。In-Home 的 Seller Agreement acceptance 以用户点击 `Submit Request` 作为同意动作；Ship To Us 同时展示用户勾选结果。协议版本和同意时间均以正式提交时记录为准。

Request ID 使用 `[METHOD]-[YYMMDD]-[LOCATION]-[RANDOM]`：`METHOD` 为 `IH`、`VL` 或 `ST`；`YYMMDD` 为正式提交日期；Visit Looply 的 `LOCATION` 固定为 `LA`，In-Home 和 Ship To Us 使用客户地址 State 缩写；`RANDOM` 为后台生成并校验唯一性的 6 位大写字母和数字。

### 4.3 确认邮件

预约记录成功创建后，由 `sell@looply.com` 自动向用户提交的 Email 发送确认邮件。预约记录创建成功不因邮件发送失败而回滚。

| 枚举值 | 含义 | 触发时机 | 可执行操作 |
|---|---|---|---|
| `Pending` | 等待发送或正在发送 | 预约创建后、人工重发开始后 | 等待发送结果 |
| `Sent` | 邮件服务已返回发送成功 | 自动发送或人工重发成功后 | 无 |
| `Failed` | 邮件服务返回发送失败 | 自动发送或人工重发失败后 | `Resend email` |

状态为 `Failed` 时，业务人员可在预约详情点击 `Resend email`。点击后状态变为 `Pending`；成功后变为 `Sent`，再次失败则回到 `Failed` 并更新失败原因和 Last attempted at。人工重发复用原预约和 Request ID，不创建新预约。

邮件主题为 `We received your Looply sell request — {Request ID}`。正文包含 Request ID、Submitted at、Selling method、Total pieces、用户填写的地址摘要、Categories / Brands 摘要、Preferred date（未填写时不展示）以及客户代表后续联系说明。邮件语言使用用户提交时的页面语言；人工重发沿用该预约首次发送时的主题、正文模板、语言和收件邮箱，不读取运营人员当前后台语言。

### 4.4 内部备注

运营人员可在预约详情中新增或编辑一条内部备注。内部备注不修改用户原始提交信息，也不回传前台。

| 字段 | 规则 |
|---|---|
| Internal note | 可为空；保存空内容视为清空备注 |
| Created at | 第一次保存非空备注时生成；后续编辑保持不变 |
| Updated at | 每次成功保存或清空时更新 |
| Operator | 记录最近一次成功保存或清空备注的登录账号 |

保存成功后在当前详情更新备注及元信息；保存失败时保留编辑内容并提示 `Couldn't save the note. Please try again.`。

Appointments 列表包含正常数据、加载、无数据、无匹配和加载失败状态。详情加载失败时仅详情区域显示错误和 Retry，不影响列表；预约记录不存在时收起详情并刷新列表。

## 五、权限与数据边界

C1 运营人员通过独立登录进入本后台。当前版本使用同一 C1 运营角色，不新增管理员角色或细分权限。

用户提交的个人信息和地址在 Appointments 详情与 Download 中提供给已登录的 C1 运营人员；照片仅在 Appointments 详情中在线查看，不进入 Download。用户原始业务字段保持只读；运营人员仅可编辑 Internal note，并可对 `Failed` 的确认邮件执行 `Resend email`。当前版本仅对 Download 实施 4.1 定义的专项记录。

## 六、依赖与风险

| 依赖 | 当前版本要求 |
|---|---|
| Seller Request 用户端 | 成功提交后提供本 PRD 4.2 定义的完整数据，并保持 Request ID 唯一 |
| `Postal/addressconfig` | 为 5 位 ZIP 返回 City 和 State；不可用时阻止新增 ZIP 配置 |
| 配置读取能力 | 前台仅读取 `Active` ZIP、Category 和 Brand，并保持后台保存顺序 |
| 翻译能力 | `seller_category` 支持英语源内容和西语展示；缺译时回退英语 |
| 文件能力 | 预约照片仅在详情中向已登录的 C1 运营人员提供受控访问，不进入 Download |
| 邮件服务 | 使用 `sell@looply.com` 发送预约确认邮件，并向后台返回可判断 `Sent` 或 `Failed` 的发送结果 |

Appointments 涉及姓名、电话、邮箱、地址和照片。开发需沿用 ops.looply.com 现有登录与访问控制；Download 专项记录必须与文件生成结果一致。

所有时间字段按洛杉矶时区 `America/Los_Angeles` 存储，接口传输时保留明确的时区偏移，避免夏令时切换产生歧义。后台时间展示、Submitted at 日期筛选以及 Request ID 中的 `YYMMDD` 与 C2 保持一致，统一按美东时区 `America/New_York` 计算并自动适配夏令时。Preferred date 按用户选择的日期值保存，不进行跨时区换日。

## 七、版本规划

### 7.1 当前版本

- ZIP Coverage：单 ZIP 新增、City/State 回填、搜索、列表内启用/停用及异常状态。
- Categories & Brands：两级新增、编辑、搜索、启用/停用、排序及前台读取规则。
- Appointments：列表、关键词与日期筛选、行内只读详情、确认邮件状态与失败重发、内部备注、Download 和下载专项记录。

### 7.2 后续规划

- 预约后的其他指引邮件。
- Appointments 字段脱敏、细分权限、通用操作审计和数据保留策略。

## 八、验收标准

1. 后台独立登录后仅展示 `ZIP Coverage`、`Categories & Brands`、`Appointments` 三个业务入口。
2. ZIP 仅在格式、唯一性及 City/State 回填均通过后保存；Active 状态正确影响前台 In-Home 判断。
3. Category 和 Brand 分层维护，名称去重、状态和排序规则符合本 PRD；前台仅读取同时生效的配置。
4. Appointment 列表搜索仅匹配 Request ID、Full name、Email；日期筛选、空态和失败重试符合本 PRD。
5. 行内详情完整展示对应用户提交字段，原始信息只读，仅 Internal note 可编辑。
6. Download 导出当前全部筛选结果及规定字段，不包含图片文件、照片链接或 Attachment ID，并记录账号、时间、筛选条件和导出记录数。
7. 预约创建后由 `sell@looply.com` 自动发送确认邮件；后台准确展示 `Pending`、`Sent`、`Failed`，Failed 支持人工重发且不重复创建预约。

## 九、设计与资料索引

- 当前运营后台原型：`prototypes/c1-sell/outputs/looply-c1-sell-ops-local.html`。该本地文件用于核心正常路径的可点击演示；异常状态、接口结果及验收边界以本 PRD 的完整规则为准。
- 用户端数据字段基线：`docs/product/looply-C1-Sell-PRD-v0.8.md`
- 第三轮开发反馈回复：`docs/reviews/c1-sell/looply-C1-Sell-第三轮开发反馈回复-20260904.md`
- 第二轮开发反馈：`/Users/zz/Downloads/requirement-analysis(1).html`

运营后台仅提供 PC Web 页面，本模块没有 Mobile 运营端页面。
