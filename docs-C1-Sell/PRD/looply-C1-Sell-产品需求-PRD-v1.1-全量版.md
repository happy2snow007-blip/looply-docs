# Looply C1 Sell 产品需求 PRD

版本：v1.1（全量版）
日期：2026-10-12
范围：C1 Sell 用户端、运营后台及相关跨模块联动

## 一、文档职责与基线

本文件维护截至当前已确认的 C1 Sell 全量产品规则，是长期查询和后续迭代合并入口。开发实施本次多国家改造时，先阅读《C1 Sell 多国家支持迭代 PRD v1.1》识别增量，再使用本文件查询完整业务规则。

当前交互基线：

- C1 用户端展示与交互以当前最新 Figma《1.1-C1业务》为准；PRD补充数据来源、状态条件、异常和业务边界。
- C1 运营后台展示与交互以 [运营后台 Demo v1.14](../原型/looply-C1-Sell-运营后台原型-v1.14.html) 为准。
- 多国家增量来源：[多国家支持迭代 PRD v1.1](./looply-C1-Sell-多国家支持-迭代PRD-v1.1.md)。
- 本文件已吸收用户端 PRD v0.9、运营后台 PRD v1.13、批量导入与删除 PRD v1.2 和多国家支持迭代 PRD v1.1 中仍然有效的规则；这些文件保留用于追溯。

## 二、产品范围与角色

C1 Sell 面向游客和登录用户提供三种出售方式：`In-Home Appointment`、`Visit Looply`、`Ship To Us`。用户无需登录即可浏览 Sell 内容和提交 Seller Request，提交后以系统生成的 Request ID 标识申请。

用户端范围包括 PC Header、Mobile 底部导航、Sell 首页、Accepted Brands、Condition Guidelines、Service Area、Seller FAQ、预约流程、成功页、Footer、Contact Us 和个人中心 Seller Agreement 入口。运营后台范围包括服务国家、ZIP Coverage、Categories & Brands、Appointments、批量导入、导出和删除。

PC 与 Mobile 的业务流程、字段、校验、状态和结果一致，布局及交互触发方式分别以对应 UI 为准，Mobile 不按 PC 页面缩放实现。

## 三、国家与 Sell 状态

### 3.1 国家来源

- C1 不创建国家，读取「C2 业务国家管理」中全部有效、未删除国家。
- 国家选择范围不受 C2 启用状态限制，允许提前加入尚未启用的国家并维护 C1 配置。
- 已加入服务国家列表的国家不再出现在新增国家下拉选项中。
- 国家名称、国家代码和 C2 启用状态在 C1 只读展示，并随 C2 更新。

### 3.2 生效条件

前台 C1 业务生效条件固定为：

```text
C2 国家状态 = 已启用
且 C1 Sell 业务状态 = 开放
```

| C2 状态 | Sell 状态 | 可维护配置 | 前台生效 | 接收新预约 |
|---|---|---:|---:|---:|
| 未启用 | 未开放 | 是 | 否 | 否 |
| 未启用 | 开放 | 不允许出现 | 否 | 否 |
| 已启用 | 未开放 | 是 | 否 | 否 |
| 已启用 | 开放 | 是 | 是 | 是 |

- 新增服务国家默认保存为未开放；C2 未启用时开放操作置灰。
- C2 启用国家后 Sell 不自动开放，由运营手动开放。
- 第一版不执行自动业务适配检查；产品、开发和运营在开放前人工确认地址、表单、法律文件及前后台能力已具备。
- 停用 Sell 需要二次确认。停用后立即隐藏入口并拒绝新预约，配置和历史预约保留。
- C2 停用或删除已开放 Sell 的国家时，Sell 同步改为未开放；删除或不再提供后停止新的配置写入和预约，已有配置与历史 Appointment 仍可按原国家查询。重新启用后仍需运营再次开放。
- 对已经打开页面或预约流程的用户不强制关闭页面，但继续下一步和提交时必须重新校验状态。

### 3.3 当前站点国家

C1 使用全站当前实际生效的站点国家，不自行重新判断。带国家子目录 URL 的访问以 URL 国家为准，不被 IP 覆盖；裸域沿用 C2 全站国家识别规则。不得使用运营后台最近选择国家、其他国家配置或美国默认配置替代当前站点国家。

## 四、C1 用户端

### 4.1 入口和直接访问

以下位置统一跟随当前国家的 C1 生效条件，不再增加入口级启停条件：

| 位置 | 生效时 | 未生效时 |
|---|---|---|
| PC Header | 展示 Sell | 隐藏 Sell |
| Mobile 底部导航 | 展示 Sell | 隐藏 Sell |
| PC Footer | 展示 `SELL` 栏及 C1 入口 | 隐藏整个 `SELL` 栏 |
| Footer Support | 展示 `Seller FAQ` | 隐藏 `Seller FAQ` |
| Footer Legal | 展示 `Seller Agreement` | 隐藏 `Seller Agreement` |
| Contact Us | 展示 `Selling to Looply` 和 Sell 联系邮箱 | 隐藏 Sell 专属内容，保留普通购物咨询 |
| 个人中心 | 展示 `Seller Agreement` | 隐藏 `Seller Agreement` |

用户直接访问 Sell URL 时仍校验当前国家。未生效时展示服务不可用状态和返回首页入口，不允许开始或提交预约；服务端必须再次校验。

### 4.2 Sell 首页及内容页

- Sell 首页 Hero 的 `Sell Now` 进入预约，`Explore your options` 定位 Three Ways to Sell。
- Three Ways to Sell 展示 In-Home、Visit Looply、Ship To Us；PC 使用 UI 定义的 Hover 交互，Mobile 使用独立移动端交互。
- What We Buy 首页滚动品牌为固定内容；`View All Brands & Categories` 进入 Accepted Brands。
- Selling Tips 与 How to Get Paid 展示说明内容，不增加额外跳转。
- FAQ 摘要支持展开收起，`View All FAQs` 进入 Seller FAQ。
- 底部 CTA 与 PC 吸底 CTA 的 `Sell Now` 均进入预约流程。
- Accepted Brands 按当前国家读取 Active Category 和 Brand，并保持后台顺序；支持品类筛选、品牌首字符实时过滤和品牌联想。
- Accepted Brands 的 `All` 视图或多品类结果先按当前国家与 Active 状态过滤，再按 Brand name 大小写不敏感去重，并按标准品牌名首字母分组；同组内按“Category 后台顺序 → Category 内 Brand 后台顺序”保留首次出现项。
- 搜索从输入第一个字符起实时生效，匹配品牌名称且保留首字母分组；无匹配时展示 `No brands found.` 和 `Clear search`，清空后恢复当前品类列表。当前国家无 Active Brand 时展示空状态，不回退其他国家。
- Condition Guidelines 展示 UI 定义的 9 个成色模块；前 8 个按 Accepted / Not Accepted 展示，Jewelry and Watches 按 UI 合并说明。

### 4.3 ZIP Coverage 与 Service Area

- Service Area 和预约流程只读取当前国家 Active ZIP 配置，不回退其他国家。
- 当前版本仅定义美国 ZIP：用户可输入 5 位 ZIP 或 ZIP+4，查询覆盖范围时统一取前 5 位。
- 覆盖结果只决定 In-Home 是否可用，不控制国家级 Sell 入口。
- 无 Active ZIP 时按没有可用 In-Home 服务区域处理，其他可用出售方式不受影响。
- Service Area 查询成功且覆盖时展示 In-Home 可用状态；点击预约后从 Step 1 开始，预填本次 ZIP 并预选 In-Home 意向，进入 Step 3 后仍可切换方式。未覆盖时展示其他出售方式入口；查询失败时保留 ZIP 并提供 Retry。
- 非美国国家的地址字段、服务区域标识和格式校验在正式开放该国家 C1 前另行定义。

### 4.4 预约流程

预约固定四步：个人信息 → 物品信息 → ZIP 与出售方式 → 对应方式信息。进度条始终显示四段。

**Step 1 个人信息**

- `First name`、`Last name`、`Phone`、`Email` 必填。
- 联系授权必须勾选，文案链接复用 C2 Privacy Policy 和 Terms of Service。

**Step 2 物品信息**

- Category 读取当前国家全部 Active 配置，至少选择一项，可多选。
- Brand 至少填写一项，可多选；选择 Category 后按其 Active Brand 联想，未配置品牌允许手动输入。
- Total pieces 必填，选项为 `1–2`、`3–5`、`6–9`、`10+`。
- Additional notes 选填，最多 300 字符；Photos 选填，最多 10 张。

**Step 3 ZIP 与出售方式**

- ZIP 必填。覆盖时默认选择 In-Home；未覆盖时 In-Home 置灰并默认选择 Ship To Us；Visit Looply 始终可选。
- 用户可切换任何可用方式；系统保留已填写的个人信息、物品信息和 ZIP。
- Step 4 修改 ZIP 后重新查询；若新 ZIP 不支持 In-Home，则阻止以 In-Home 提交并要求重新选择。

**Step 4 方式信息**

| 方式 | 必填 | 选填 | 协议规则 |
|---|---|---|---|
| In-Home | Street address、City、State、ZIP | Apartment、Preferred date、Referral code | 点击 Submit Request 即表示同意 Seller Agreement，记录协议版本和时间 |
| Visit Looply | 固定 Looply 地址 | Preferred date、Referral code | 无额外勾选 |
| Ship To Us | Street address、City、State、ZIP、Seller Agreement 勾选 | Apartment | 勾选后才能提交 |

提交时记录不可变 `country_code`、页面语言、配置项稳定 ID、Seller Agreement 版本和同意时间。Sell 已停用、C2 已停用、配置无效、字段校验失败或重复提交时阻止创建。失败后停留 Step 4，保留输入并提供 Retry。

预约草稿仅在同一国家恢复；切换国家后不带入原国家 ZIP、Category、Brand、地址或方式选择。切回原国家时可恢复原国家草稿。普通表单字段在同一设备、同一浏览器保存 30 天，主动关闭流程不清除草稿，提交成功后立即清除；不支持跨浏览器或跨设备恢复。照片不跨次恢复，临时上传但未提交的照片在 24 小时后自动清除。

### 4.5 成功页与 Request ID

成功页展示 `Request received`、Selling method、Total pieces，以及已填写的 Preferred date。Request ID 为 `[METHOD]-[YYMMDD]-[LOCATION]-[RANDOM]`：METHOD 使用 `IH`、`VL`、`ST`；Visit Looply 的 LOCATION 为 `LA`，其他方式使用地址 State 缩写；RANDOM 为后台生成并保证唯一的 6 位大写字母和数字。

### 4.6 Contact Us

Contact Us 页面保留普通购物咨询。当前国家 C1 生效时才展示 `Selling to Looply` 和 Sell 邮箱；未生效时隐藏两者。Sell 咨询提交至 `sell@looply.com`，普通购物咨询提交至 `service@looply.com`。Contact Us 的完整页面、字段和异常规则由 Footer 与关联页面 PRD 定义。

### 4.7 确认邮件与法律文件

- 预约记录创建成功后由 `sell@looply.com` 自动发送与 Selling method 匹配的确认邮件；邮件失败不回滚预约。
- 邮件语言使用提交时页面语言；人工重发沿用首次发送的主题、正文模板、语言和收件邮箱。
- 主题为 `We received your Looply sell request — {Request ID}`。
- 选填字段为空时隐藏对应整行；邮件分别展示请求、物品、联系方式和方式对应地址/地点。
- Seller Agreement 按国家和法务语言读取法律文件当前版本，不使用自动翻译；提交时保存实际同意的版本。
- `Brands and details` 合并展示 Brands 和 Additional notes；`Photos uploaded` 展示照片数量或 none。

**In-Home Appointment 模板**

```text
Hi {{first_name}},

Thanks for choosing Looply.

We’ve received your selling request, and a Looply team member will contact you by phone, text, or email within 24 hours to confirm the next steps.

Here’s a summary of the information you submitted:

YOUR REQUEST
Request ID: {{request_id}}
Selling method: {{selling_method}}
Preferred date: {{preferred_date_or_not_provided}}
Referral code: {{referral_code_or_not_provided}}

YOUR PIECES
Categories: {{categories}}
Brands and details: {{brands_and_details}}
Photos uploaded: {{photo_count_or_none}}

YOUR CONTACT INFORMATION
Name: {{full_name}}
Phone: {{phone}}
Email: {{email}}

APPOINTMENT ADDRESS
{{street_address}}
{{apartment_suite_if_provided}}
{{city}}, {{state}} {{zip_code}}

Your preferred date is not yet confirmed. A Looply team member will contact you to confirm availability.

At your appointment, we’ll evaluate your pieces, make an offer, and—if you accept—pay you on the spot.

Need to make a change? Simply reply to this email and let us know.

Warmly,
The Looply Team
```

**Visit Looply 模板**

```text
Hi {{first_name}},

Thanks for choosing Looply.

We’ve received your selling request, and a Looply team member will contact you by phone, text, or email within 24 hours to confirm the next steps.

Here’s a summary of the information you submitted:

YOUR REQUEST
Request ID: {{request_id}}
Selling method: {{selling_method}}
Preferred date: {{preferred_date_or_not_provided}}
Referral code: {{referral_code_or_not_provided}}

YOUR PIECES
Categories: {{categories}}
Brands and details: {{brands_and_details}}
Photos uploaded: {{photo_count_or_none}}

YOUR CONTACT INFORMATION
Name: {{full_name}}
Phone: {{phone}}
Email: {{email}}

APPOINTMENT LOCATION
Looply Suit 1720, 6300 Wilshire Blvd
Los Angeles, CA 90048

Your preferred date is not yet confirmed. Please wait for a Looply team member to confirm your appointment before visiting.

Need to make a change? Simply reply to this email and let us know.

Warmly,
The Looply Team
```

**Ship To Us 模板**

```text
Hi {{first_name}},

Thanks for choosing Looply.

We’ve received your selling request, and a Looply team member will contact you by phone, text, or email within 24 hours to confirm the next steps.

Here’s a summary of the information you submitted:

YOUR REQUEST
Request ID: {{request_id}}
Selling method: {{selling_method}}
Preferred date: {{preferred_date_or_not_provided}}
Referral code: {{referral_code_or_not_provided}}

YOUR PIECES
Categories: {{categories}}
Brands and details: {{brands_and_details}}
Photos uploaded: {{photo_count_or_none}}

YOUR CONTACT INFORMATION
Name: {{full_name}}
Phone: {{phone}}
Email: {{email}}

SHIPPING ADDRESS
{{street_address}}
{{apartment_suite_if_provided}}
{{city}}, {{state}} {{zip_code}}

A Looply team member will review your request and send you the applicable complimentary shipping instructions.

Need to make a change? Simply reply to this email and let us know.

Warmly,
The Looply Team
```

## 五、C1 运营后台

### 5.1 信息架构与国家上下文

后台包含 `Appointments` 和 `Configuration`。Configuration 下包含 `Service Countries`、`ZIP Coverage`、`Categories & Brands`。ZIP、Category、Brand 和 Appointment 均按国家隔离；国家切换后清空搜索词、勾选记录和展开状态并重新读取目标国家。存在未保存表单或抽屉内容时，切换前提示内容将丢失；确认后关闭编辑并切换，取消则保留当前国家和输入。

### 5.2 服务国家

列表展示 Country、Country code、C2 country status、Sell status 和操作。新增国家只能从 C2 全部有效且尚未加入 C1 的国家中选择，支持保存为未开放。开放与停用遵循第三章状态规则。

### 5.3 ZIP Coverage

- 列表按当前国家展示 ZIP code、Region、Status、Created at、Updated at 和操作，支持关键词与状态筛选。
- 美国 ZIP 固定为 5 位数字；同一国家内标准化后唯一，不允许重复新增或导入。
- 支持单条新增、编辑、启停、导出、CSV 导入和批量删除。
- 停用保留记录并立即不参与覆盖判断；编辑或启用时重新校验唯一性。
- Add ZIP code 成功后新记录插入列表顶部。

### 5.4 Categories & Brands

- Category 按国家维护 Name、Status 和 Sort order，支持新增、编辑、搜索、启停、拖拽排序和单条删除。
- Brand 隶属于当前国家下的 Category，支持新增、编辑、搜索、启停、排序、CSV 导入和批量删除。
- 同一国家同一层级内 Category name 唯一；同一国家同一 Category 下 Brand name 唯一，比较时忽略首尾空格和大小写。
- Category 或 Brand 停用后不出现在用户端选择器和联想结果中；存量 Appointment 保留提交时快照。
- 删除 Category 时连同当前国家下关联 Brand 一并删除，必须展示影响数量并二次确认。
- 新增 Category 或 Brand 成功后插入对应列表顶部。

### 5.5 批量导入、导出和删除

- ZIP 和 Brand 提供 CSV 模板下载与导入；Category 不提供批量导入和批量删除。
- 导入文件固定为 UTF-8 CSV，首行为表头，单个文件最大 10 MB、5,000 行；空行忽略。文件格式、编码或文件级超限时阻止解析，字段错误只使对应行失败。
- 导入先完成字段、格式、国家归属、重复和冲突校验，再展示总行数、可导入行数、失败行数及逐行原因。文件内重复记录保留首次出现行，其余失败；已存在配置失败且不覆盖。
- 确认后只写入校验通过的行，允许部分成功；完成后展示成功数、失败数并提供包含原始行号、关键字段和失败原因的明细下载。
- 导入任务必须防重复提交；关闭弹窗不取消已开始任务。网络异常保留文件与校验结果；超时或服务异常允许 Retry，且不得重复写入已经成功的行。
- ZIP 模板包含必填 `ZIP code` 和选填 `Status`；Status 仅接受 `Active`、`Inactive`，为空默认 `Active`。系统根据 ZIP 回填只读 City、State；无法匹配或地址服务失败的行失败。
- Brand 模板包含必填 `Brand name` 和选填 `Status`；从当前国家、当前 Category 的 Brands 列表进入，CSV 不重复填写国家和 Category。
- ZIP 和 Brand 列表支持复选与批量删除；只删除当前国家当前筛选结果中明确选中的记录。
- 跨页全选最多 500 条；匹配结果超过 500 条时阻止全选并提示缩小范围，不静默截断。
- 批量删除确认信息展示国家、数量和状态构成；成功后清空选择并刷新列表，失败项保留并显示原因。
- ZIP 批量删除在确认层直接使用 `Cancel` / `Delete`；Brand 批量删除需要输入 `DELETE` 后才能确认。
- 手工新增 ZIP、Category 或 Brand 成功后插入列表顶部；CSV 导入的新 Brand 按文件顺序追加，不倒序插入。
- ZIP 导出当前国家筛选后的全部匹配记录，不只导出当前页；无匹配时按钮置灰。
- 导入、导出和删除记录操作人、时间、国家、筛选条件、成功/失败数量和逐行结果。
- 导入、批量删除及失败后的 Retry 在任务启动时锁定目标国家；页面随后切换国家不改变任务归属和结果写入范围。

### 5.6 Appointments

- 默认展示全部国家，可切换单一国家；支持 Request ID、Full name、Email 关键词和 Submitted at 日期筛选。日期默认最近 7 天并包含起止日，按 `America/New_York` 自然日边界计算并适配夏令时；起始日期晚于结束日期时阻止查询。
- 列表展示 Request ID、Country、Submitted at、Selling method、Name、Email、Phone、Categories、Brands、Total pieces、Confirmation email status 和操作。
- Download 导出当前国家、关键词和日期共同命中的全部记录，每行一条预约；无匹配时置灰。
- CSV 包含 Request、Personal information、Item information、ZIP recommendation、Method information、Confirmation email 和 Internal note 字段，不包含照片文件、照片链接或 Attachment ID。
- CSV 字段顺序固定：Request 为 Request ID、Country、Submitted at、Selling method；Personal information 为 First name、Last name、Phone、Email、Contact authorization result、Contact authorization accepted at；Item information 为 Categories、Brands、Total pieces、Additional notes；ZIP recommendation 为 Step 3 submitted ZIP、In-Home coverage result；Method information 为 Street address、Apartment、City、State、ZIP code、Looply address、Preferred date、Referral code、Seller Agreement acceptance result、Seller Agreement version、Seller Agreement accepted at；Confirmation email 为 status、Last attempted at、Failure reason；Internal note 为正文、created at、updated at、operator。不适用字段留空。
- 每次成功触发 Download 后记录操作账号、下载时间、关键词、国家筛选、日期范围和导出数量；生成失败时不记录成功下载。
- 点击 View 在当前行下方展开只读详情；照片最多 10 张，无值显示 `—`。
- 用户提交业务字段只读，运营仅可编辑 Internal note，并可对 Failed 邮件执行 `Resend email`。
- Confirmation email 状态为 Pending、Sent、Failed。重发开始后进入 Pending，成功变为 Sent，失败回到 Failed 并更新原因和 Last attempted at。
- 内部备注记录 Created at、Updated at 和最近操作人；保存失败时保留编辑内容。

## 六、数据、多语言与权限

- 服务国家、ZIP、Category、Brand、Appointment 和相关任务均保存稳定 `country_code`；列表、查询、写入、导入、导出和前台读取使用同一维度。
- Appointment 保存提交时国家以及 Category、Brand、ZIP、Seller Agreement 版本与同意结果的快照；后续改名、停用或删除配置不改写历史预约。
- 国家之间不回退 ZIP、Category、Brand、预约或入口配置。
- Category name 属于动态业务内容，使用 `seller_category` 翻译资源，`fieldName=name`，覆盖 Accepted Brands 与预约 Step 2；译文缺失时回退英语。Brand name 属于专有名称，不翻译；普通 UI 文案使用统一 message package。
- Seller Agreement 使用法务提供的对应语言正文，不进入自动翻译。
- 后台当前使用同一 C1 运营角色；无编辑权限时只读，隐藏或禁用保存、导入、删除、启停和邮件重发操作。
- Appointments 中的姓名、电话、邮箱、地址和照片仅向已登录且有权限的运营人员提供；照片只在详情受控访问，不进入 CSV。
- 上线前缺少 `country_code` 的 ZIP、Category、Brand 和 Appointment 统一归属美国；美国 Sell 初始状态为开放，并保留存量配置的启停、排序和历史 Appointment。
- 时间以 UTC 保存；用户端与后台按对应页面约定时区展示。Appointments 日期筛选固定按 `America/New_York` 自然日边界换算查询，避免夏令时造成漏数或重复。

## 七、异常与一致性

- 网络或保存失败时保留用户输入，不将失败操作显示为成功。
- 同一记录被他人修改或删除时，阻止旧数据覆盖，提示刷新后重试。
- 当前国家失效时终止新的配置写入和预约创建，历史数据仍可按权限查询。
- 前台入口状态、直接访问校验和预约提交接口必须消费同一 Sell 生效结果。
- 国家切换后列表、详情、编辑表单、批量选择、导出条件和预约草稿不得残留上一国家数据。

## 八、验收标准

1. C2 未启用国家可以加入 C1 并提前配置，但不能开放 Sell。
2. C1 未生效国家不展示任何 Sell 入口、Seller FAQ、Seller Agreement、Selling to Looply 或 Sell 邮箱，并拒绝新预约。
3. C1 生效国家的 PC、Mobile、Footer、Contact Us 和个人中心入口状态一致。
4. 用户端 ZIP+4 可输入，覆盖判断只使用前 5 位；后台美国 ZIP 只维护 5 位。
5. 当前国家只读取本国 Active ZIP、Category 和 Brand，不回退其他国家。
6. 预约保存提交国家；切换国家后草稿、配置、列表、详情和导出均正确隔离。
7. 同一国家重复 ZIP、Category 或 Brand 无法保存；批量导入能够报告重复和失败行。
8. 启用项停用后立即不参与前台读取，历史预约仍展示提交时快照。
9. 批量删除只影响明确选中项，超过 500 条时阻止全选；确认、结果和操作日志可核对。
10. Appointments 能按全部国家或单一国家查询和下载，Country 与完整既有 CSV 字段均正确。
11. 确认邮件失败不回滚预约，人工重发不创建新预约。
12. 保存、上传、下载或查询失败时保留当前可恢复状态，并提供明确重试入口。

## 九、关联制品

- 本次增量：[C1 Sell 多国家支持迭代 PRD v1.1](./looply-C1-Sell-多国家支持-迭代PRD-v1.1.md)
- 运营后台 Demo：[v1.14](../原型/looply-C1-Sell-运营后台原型-v1.14.html)
- 用户端历史基线：C1 Sell 用户端 PRD v0.9
- 运营后台历史基线：C1 Sell 运营后台 PRD v1.13
- 批量规则历史基线：C1 Sell 运营后台批量导入与删除 PRD v1.2
- Footer 与 Contact Us 完整页面规则：Looply Footer 与关联页面 PRD
