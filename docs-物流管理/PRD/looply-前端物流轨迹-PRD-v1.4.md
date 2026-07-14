# Looply 前端物流轨迹 PRD

> 版本：v1.4  
> 日期：2026-07-14  
> 适用端：PC Web、移动端（APP、H5）  
> 需求状态：待产品、设计、前后端及测试评审

## 一、概述【必写】

### 1.1 背景与目标

用户需要在订单详情中查看某个包裹的承运商、运单号、预计送达信息和完整物流轨迹。现有物流信息服务已经具备运单、承运商、预计送达日期和轨迹节点等数据能力，本需求将这些能力以订单详情内的 `Tracking details` PC 弹窗或移动端 Bottom Sheet 提供给 PC Web、APP、H5 用户。

本期目标：

- 用户无需离开订单详情即可查看单个包裹的物流信息。
- 同一订单拆成多个包裹时，每个包裹独立查看，避免轨迹混合。
- 前端展示口径与物流 PRD v1.5、物流 ER 图 v2.7一致。
- 补齐设计稿未覆盖的加载、空数据、异常、取消及刷新场景。

### 1.2 不做什么

| 非本期范围 | 说明 |
|---|---|
| 订单级预计送达日期 | 由订单模块定义；本 PRD 只定义单个 shipment 的 ETA。 |
| 订单维度实际送达日期 | 由订单模块定义；本 PRD 只定义单个 shipment 的 Delivered 节点时间。 |
| 弹窗内切换包裹 | 每个包裹从订单详情中的独立入口打开，不在弹窗中增加包裹选择器。 |
| 修改运单或承运商 | 仅展示，不提供编辑、纠错或取消追踪能力。 |
| 承运商官网跳转 | Figma 未设计，本期不提供。 |
| 五段式物流进度条 | Figma 未设计，本期仅使用轨迹时间线。 |
| 商品、收货地址、客服及 FAQ | 继续由订单详情承载，不重复放入物流弹窗。 |
| 手动刷新按钮及自动轮询 | 进入订单详情时获取状态卡数据，打开轨迹弹窗/抽屉时再次获取；停留期间不轮询。 |
| 暴露追踪平台技术信息 | 不展示 AfterShip、快递100、tracking_health 或平台错误码。 |

### 1.3 用户角色

| 角色 | 权限与行为 |
|---|---|
| 已登录买家 | 仅可查看本人订单下有效包裹的物流轨迹。 |
| 游客或登录失效用户 | 不可查看；按账号体系规则引导登录。 |
| 客服及运营人员 | 不通过本弹窗操作，继续使用各自后台工具。 |

### 1.4 核心场景

1. 包裹运输中：查看承运商、运单号、预计送达日期范围和最新轨迹。
2. 包裹已送达：查看 `Delivered` 状态及签收轨迹。
3. 轨迹较多：在弹窗内容区滚动查看全部节点。
4. 拆包订单：从对应包裹卡片分别打开各自轨迹。
5. 数据暂不可用：获得明确、可恢复的页面反馈。

### 1.5 全局页面流转

`My Account → My Orders → Order details → 点击对应已发货包裹的物流状态卡 → Tracking details（PC 弹窗 / 移动端 APP、H5 底部抽屉）`

关闭弹窗后仍停留在原订单详情位置，不刷新订单详情页，不改变浏览器页面层级。

### 1.6 术语说明

| 术语 | 定义 |
|---|---|
| 订单 | 用户购买行为形成的业务订单。 |
| 包裹 | 一次独立发运单元，对应一条有效 shipment。一个订单可有多个包裹。 |
| 运单 | 物流服务中的追踪记录，由 `shipment_id` 唯一标识。 |
| 运单号 | 承运商提供的 `tracking_no`，用于识别包裹。 |
| 轨迹节点 | 承运商在某一时间产生的物流事件。 |
| ETA / Est. delivery | 预计送达日期。国际段使用 AfterShip AI EDD；国内段无该数据。 |
| 物流状态 | `internal_status`，描述包裹当前运输阶段。 |
| 追踪健康度 | `tracking_health`，仅供内部监控，不直接展示给用户。 |

### 1.7 多语言、多国家与时间策略

- 本 PRD 使用 Figma 英文文案作为默认 `en-US` 源文基线；PC、APP、H5 共用同一套业务 i18n key，不按端重复建设译文。
- 固定标题、字段标签、按钮、Toast、空态和错误态进入前端语言包，不进入翻译中心业务资源卡片。
- 物流状态及可枚举的轨迹事件文案由物流服务完成状态映射，并通过服务端 message package 提供本地化结果，不进入翻译中心业务资源卡片。
- 承运商原始 message 属于外部实时动态内容，MVP 不进入翻译中心、不按 checkpoint 生成翻译记录；仅在缺少映射文案时作为降级原文展示。
- 当前语言由订单前端传递给物流服务；服务端返回同一语言决策下的用户端状态文案和可读事件描述，前端不自行翻译平台状态。
- 译文缺失按“目标语言映射文案 → `en-US` 映射文案 → 可读的承运商原始 message → `en-US` 用户状态文案”降级，不得显示空文本、未解析 i18n key、平台 tag 或错误码。
- 轨迹时间以服务端返回的 UTC 时间为基准，展示时转换为用户当前选择/账号设置的时区；若账号无时区设置，使用浏览器时区。
- AfterShip AI EDD 已是目的地当地时区的日历日期；前端仅做语言与日期格式化，不做 UTC 换算或任何时区加减。
- 日期、时间和月份名称按当前语言及地区格式化，不在前端硬编码英文月份。
- 地名、承运商名称、运单号不翻译。

## 二、需求详细描述【必写】

### 2.1 订单详情入口（页面型）

#### 功能描述

订单详情按包裹展示物流入口。点击某个包裹的入口，只打开该包裹对应的 `Tracking details` 弹窗。

#### 前置条件

- 用户已登录，且订单属于当前用户。
- 包裹已关联一条 `record_status = active` 的 shipment。
- 订单服务能够提供 Fulfillment Group（已发货包裹组）与 `shipment_id` 的明确对应关系。

#### 页面元素与规则

| 场景 | 入口规则 |
|---|---|
| 单包裹订单 | 该已发货包裹组展示可点击的物流状态卡。 |
| 多包裹订单 | 每个 Fulfillment Group 分别展示物流状态卡，点击后使用该组关联的 `shipment_id`。 |
| 尚未发货或未注册运单 | 不展示可点击的物流状态卡。 |
| shipment 已取消且存在替代 active shipment | 入口绑定替代 shipment，不展示已取消记录。 |
| shipment 已取消且无替代记录 | 不打开正常轨迹弹窗；入口隐藏。订单已有已发货事实但追踪被终止时，可由订单模块显示自身状态提示。 |

#### 操作流程

1. 用户进入订单详情。
2. 订单模块获取并展示各 Fulfillment Group 的当前物流状态卡数据。
3. 用户点击目标已发货包裹组的物流状态卡。
4. 系统先校验订单归属及包裹与 shipment 的关系。
5. 校验通过后打开弹窗/抽屉并进入加载态，同时再次获取该 shipment 的最新物流数据。
6. 获取成功后展示该 shipment 的信息和轨迹。
7. 用户关闭弹窗/抽屉，返回原订单详情位置。

#### 异常处理

| 异常 | 处理 |
|---|---|
| 登录失效 | 关闭弹窗或不打开弹窗，按账号体系规则引导登录。 |
| 订单不属于当前用户 | 不返回物流内容，页面按无权限/资源不存在统一规则处理。 |
| 包裹未关联 shipment | 不打开空弹窗；订单详情提示 `Tracking information is not available yet.` |
| shipment 与当前订单不匹配 | 拒绝展示并记录异常，不使用前端传入的运单号绕过关系校验。 |
| 重复快速点击 | 同一入口在请求完成前防重复触发，仅保留一个弹窗和一次有效请求。 |

#### UI 关联

- PC：[Looply v1.0 — PC Tracking details](https://www.figma.com/design/rLK7XCdVvYqEHQHd7WjOkk/Looply-v1.0?node-id=2058-5798&p=f&t=m1Tl5y2Xfo9BOTzN-0)，节点 `2058:5798`。
- 移动端（APP、H5）：[Looply v1.0 — Mobile Tracking details](https://www.figma.com/design/rLK7XCdVvYqEHQHd7WjOkk/Looply-v1.0?node-id=2058-7950&p=f&t=m1Tl5y2Xfo9BOTzN-0)，节点 `2058:7950`。

### 2.2 Tracking details 弹窗（页面型）

#### 功能描述

以模态弹窗展示单个包裹的承运商、运单号、预计送达/送达状态，以及按时间倒序排列的完整轨迹。

#### 页面布局

- PC：在订单详情上方显示居中模态弹窗，背景增加遮罩。
- 移动端（APP、H5）：从屏幕底部打开全宽 Bottom Sheet，顶部为大圆角，覆盖在订单详情上方并显示遮罩。
- 弹窗/抽屉由固定标题区、运单摘要区和可滚动轨迹区组成。
- 标题 `Tracking details` 和右上角关闭按钮在滚动过程中保持可见。
- PC 内容未达到最大高度时弹窗随内容自然收缩；超过最大高度时仅内容区纵向滚动。
- 移动端 APP、H5 抽屉高度受可视区域限制，轨迹内容在抽屉内纵向滚动；滚动触底可查看最早节点，背景订单详情不可滚动。
- 弹窗打开后焦点进入弹窗；键盘焦点不得越过弹窗进入背景页面。
- 关闭后焦点返回触发查看物流的入口。

#### 页面元素

| 区域 | 元素 | 数据来源/展示规则 |
|---|---|---|
| 标题区 | `Tracking details` | 固定文案。 |
| 标题区 | 关闭按钮 | 点击关闭弹窗。 |
| 运单摘要 | `Carrier` | `carrier.name`；为空时显示 `—`。 |
| 运单摘要 | `Tracking No.` | `tracking_no`；保持原始字符，不自动插入或移除空格。 |
| 运单摘要 | 复制图标 | 仅 tracking_no 非空时展示。 |
| 运单摘要 | `Est. delivery` / `Status` | 条件字段：未签收显示 `Est. delivery + 日期/日期范围`；仅已签收时替换为 `Status + Delivered`，规则见 2.3。 |
| 轨迹区 | `Tracking History` | 固定标题。 |
| 轨迹节点 | 状态 | 直接展示物流服务返回的用户端统一状态文案。服务端负责状态映射；MVP 阶段允许映射后的文案沿用物流渠道信息。 |
| 轨迹节点 | 描述 | 直接展示物流服务返回的可读事件描述；前端不解析渠道原始字段。 |
| 轨迹节点 | 地点 | `location` 非空时展示地点图标和文本；为空时整行隐藏。 |
| 轨迹节点 | 时间 | `checkpoint_time` 转用户时区后展示；与地点位于同一辅助信息行。 |

#### 数据装配边界

| 数据 | 责任系统 | 说明 |
|---|---|---|
| 订单归属、包裹与 shipment 的对应关系 | 订单服务 | 决定当前用户是否能查看目标 shipment。 |
| shipment 当前状态、运单号、ETA | 物流信息服务 | 以前端可消费的统一物流口径返回。 |
| 承运商名称 | 物流信息服务 | 来自 carriers。 |
| 轨迹节点 | 物流信息服务 | 来自 tracking_checkpoints，返回完整可展示节点。 |
| 商品和地址 | 订单服务 | 本弹窗不请求、不展示。 |

前端不得直接依赖 AfterShip 或快递100的原始报文结构，也不得自行维护平台状态映射。

#### 打开与关闭交互

- 点击物流状态卡后立即打开弹窗/抽屉，并按 Figma 规范显示居中 loading spinner，避免用户误以为点击无效。
- 点击关闭按钮关闭弹窗。
- PC 支持按 `Esc` 关闭弹窗；移动端 APP、H5 不适用。
- PC 点击遮罩关闭弹窗；移动端 APP、H5 支持点击关闭按钮或下滑关闭 Bottom Sheet。
- 关闭后清理本次弹窗视图状态；再次打开时重新获取目标 shipment 的最新可用信息。
- 页面不得因打开或关闭弹窗新增历史记录，浏览器后退键仍按订单详情原有逻辑工作。

#### 复制运单号

1. 用户点击运单号旁复制图标。
2. 系统复制完整原始 tracking_no，不包含标签或多余空格。
3. 成功后显示轻提示 `Tracking number copied`。
4. 复制失败时显示 `Unable to copy. Please copy the tracking number manually.`，运单号仍保持可选择文本。

#### 滚动规则

- 初次打开定位在轨迹顶部，最新节点可见。
- 轨迹节点按时间倒序排列，用户向下滚动查看更早节点。
- PC、移动端 APP/H5 的标题与关闭按钮均保持固定；运单摘要随内容向上滚出视口，符合 Figma“送达—滑动/触底”状态。
- 滚动到底后展示最早节点，不增加无限加载或分页。
- 关闭后不记忆滚动位置；再次打开回到顶部。

#### 无障碍规则

- 弹窗使用可识别的对话框语义，并关联标题。
- 关闭和复制图标必须有可读的辅助标签，不能只依赖图形。
- 紫色不能作为“最新节点”的唯一识别方式；最新节点同时通过排序位置和状态内容体现。
- 正文、辅助文字、图标与背景的对比度符合现有前台设计规范。

#### UI 关联

- PC：[Looply v1.0 — PC Tracking details](https://www.figma.com/design/rLK7XCdVvYqEHQHd7WjOkk/Looply-v1.0?node-id=2058-5798&p=f&t=m1Tl5y2Xfo9BOTzN-0)，节点 `2058:5798`，覆盖在途、送达最高滑动、送达滑动到底。
- 移动端（APP、H5）：[Looply v1.0 — Mobile Tracking details](https://www.figma.com/design/rLK7XCdVvYqEHQHd7WjOkk/Looply-v1.0?node-id=2058-7950&p=f&t=m1Tl5y2Xfo9BOTzN-0)，节点 `2058:7950`，覆盖在途、送达最高滑动、送达触底。

### 2.3 预计送达信息（机制型）

#### 功能描述

摘要区第三行为条件字段：shipment 未签收时展示 `Est. delivery`；仅当 `internal_status = Delivered` 时，整行替换为 `Status`。

#### 处理规则

| 条件 | 展示 |
|---|---|
| `internal_status = Delivered` | 标签显示 `Status`，值显示紫色 `Delivered`；不再显示 `Est. delivery` 标签或原 ETA。 |
| 未送达且 eta_min、eta_max 均有值，二者不同 | 显示本地化日期范围，如 `May 22 – May 24, 2026`。 |
| 未送达且 eta_min = eta_max | 显示单日期，如 `May 22, 2026`。 |
| 未送达且仅一个 ETA 日期有效 | 显示该单日期。 |
| 未送达且无 ETA | 显示 `—`，保留该行以维持摘要结构。 |
| 快递100国内段 | 不参与 AI EDD，通常显示 `—`。 |

- ETA 使用物流服务落库的 `eta_min`、`eta_max`，不使用承运商原生 expected_delivery。
- AfterShip AI EDD 返回值本身就是目的地当地时区的日历日期。前端只做本地化格式展示，不将其视为 UTC 时间，不做时区转换或日期加减。
- `eta_confidence_code` 本期仅作为服务端内部数据，不向用户展示，也不由前端设置展示阈值。
- 日期范围同年时只展示一次年份；跨年时起止日期分别展示年份。
- eta_min 晚于 eta_max 属于异常数据：不展示错误范围，显示 `—` 并记录监控信息。

#### 异常处理

- ETA 已过但包裹未送达：继续展示服务端当前 ETA，不由前端自行改成 `Delayed`。
- ETA 后续被服务端修正：重新打开弹窗时展示最新值。
- Delivered 状态与 ETA 同时存在：第三行始终展示 `Status → Delivered`，忽略原 ETA。
- `Status` 行仅用于 Delivered。Pending、InfoReceived、InTransit、OutForDelivery、AvailableForPickup、AttemptFail、Exception 均继续使用 `Est. delivery` 行；无 ETA 时值显示 `—`。

#### 单 shipment 实际送达时间

- 当轨迹中存在 Delivered 节点时，该节点的 `checkpoint_time` 是该 shipment 的送达事件时间。
- `checkpoint_time` 按普通轨迹时间处理：服务端以 UTC 返回，前端转换为用户展示时区后呈现。
- 同一 shipment 存在多个 Delivered 节点时，取首次进入 Delivered 的有效节点作为实际送达时间；时间线仍按服务端返回的完整节点展示。
- 当前状态为 Delivered 但暂时没有 Delivered 节点时，摘要区只显示 `Delivered`，不生成或猜测送达日期。
- 订单维度的实际送达日期及多包裹聚合方式由订单模块定义，不在本 PRD 中规定。

### 2.4 物流状态展示（机制型）

#### 完整枚举

| internal_status | 用户端英文文案 | 含义 | 轨迹展示规则 |
|---|---|---|---|
| Pending | Pending | 已注册追踪，尚未获得有效承运信息 | 作为普通节点；若无节点则走等待扫描空态。 |
| InfoReceived | Info Received | 承运商已收到运单信息 | 普通节点。 |
| InTransit | In Transit | 包裹运输中 | 普通节点。 |
| OutForDelivery | Out for Delivery | 包裹派送中 | 普通节点。 |
| AvailableForPickup | Ready for Pickup | 包裹等待用户自取 | 普通节点，使用面向用户的文案。 |
| AttemptFail | Delivery Attempt Failed | 派送尝试失败 | 最新状态时使用异常强调色，并保留后续更新可能性。 |
| Delivered | Delivered | 包裹已送达 | 最新节点紫色高亮；摘要第三行替换为 `Status → Delivered`。 |
| Exception | Delivery Exception | 包裹运输存在异常或长期无更新 | 最新状态时使用异常强调色，不展示平台技术原因。 |

#### 节点状态与描述规则

- 节点状态展示物流服务返回的用户端统一状态文案。状态映射由服务端维护；MVP 阶段服务端映射结果可以直接填充物流渠道提供的信息，但前端不自行读取或映射 `platform_tag`、`platform_subtag`。
- 事件描述展示物流服务返回的可读事件描述。服务端负责按“映射后的展示文案 → 可读的承运商原始 message → 用户端状态文案”完成兜底，前端不重复实现 fallback。
- 不向用户展示空白描述；所有节点至少具有状态和时间。
- `tracking_health = abnormal` 不等于物流异常，不在弹窗中展示“系统追踪异常”标签。
- Expired_001 等长期无更新场景由后端映射为 Exception，本弹窗不新增 Expired 状态。

### 2.5 轨迹时间线（页面型）

#### 排序与高亮

- 以前端收到的有效节点按 `checkpoint_time` 倒序展示。
- 若多个节点时间相同，使用服务端提供的稳定顺序；前端不得随机重排。
- 第一条有效节点视为最新节点：圆点实心并使用当前主题紫色，状态文字同步高亮。
- 其余节点使用空心圆点和中性连接线。
- 不按状态阶段合并节点；同为 In Transit 的多个真实事件均保留。
- 不在前端去重。重复数据由物流服务依据既定唯一规则处理，前端按返回结果展示。

#### 节点字段规则

| 字段 | 必填 | 规则 |
|---|---|---|
| 状态 | 是 | 使用 2.4 的用户端状态。 |
| 描述 | 是 | 使用描述兜底规则。 |
| 地点 | 否 | 有值时展示；无值时不留空占位。 |
| 时间 | 是 | 转换为用户时区并按地区格式化。 |

若地点为空，时间单独显示；不得因地点为空而隐藏时间。Figma 最早节点即采用此形态。

#### 页面状态变体

| 状态 | 展示 |
|---|---|
| 正常且有轨迹 | 展示摘要和完整时间线。 |
| shipment 存在但无轨迹 | 摘要保留；轨迹区显示 `Waiting for the carrier to scan the package.` |
| 物流异常 | 摘要保留；最新异常节点使用异常色，其余节点正常展示。 |
| 数据加载中 | 按 Figma 显示弹窗/抽屉内 loading spinner，关闭按钮可用；不展示旧 shipment 数据。 |
| 网络异常或请求超时 | 弹窗内显示加载失败错误态和 `Retry`；保留关闭能力，不清空或刷新背景订单详情。 |
| 首次加载失败 | 弹窗内显示错误态和 `Retry`；不得伪装成无轨迹。 |
| 重试中 | 保留错误区位置并显示加载反馈，禁止重复点击。 |
| shipment 不存在/不可访问 | 显示 `Tracking information is not available.`，不展示任何运单信息。 |
| 关键数据不完整 | 能展示的内容继续展示；缺失字段按各字段规则降级，同时记录监控。 |

#### 错误恢复

- `Retry` 仅重新获取当前 shipment，不关闭弹窗、不刷新订单详情。
- 重试成功后替换为正常内容并回到轨迹顶部。
- 失败响应中不得暴露第三方平台错误码、内部主键、原始报文或调试信息。

### 2.6 数据一致性与安全机制（机制型）

#### 关联与权限

- 前端以订单内包裹对应的 `shipment_id` 发起查看行为，不以可修改的 tracking_no 作为资源身份。
- 服务端必须同时校验当前用户、订单、包裹和 shipment 的归属关系。
- 前端隐藏入口不能代替服务端鉴权。
- 返回已取消 shipment 时，订单服务应优先解析其替代 active shipment；无替代项则不返回历史取消记录给普通用户。

#### 一致性规则

- `shipment_id` 是稳定身份；tracking_no 被后台纠错后，用户再次打开弹窗应看到新运单号和新轨迹。
- 订单详情加载时，订单模块获取各 Fulfillment Group 的物流状态卡数据；用户点击状态卡打开弹窗/抽屉时，物流轨迹数据再次获取，以减少状态卡与详情轨迹之间的时间差。
- 同一 business_order_no 可对应多个 shipment；不同 shipment 的轨迹不得合并。
- 已 Delivered 的 shipment 即使收到更早或非终态节点，摘要状态仍不得从 Delivered 回退；轨迹节点可按服务端结果保留用于事实追溯。
- 当前状态与最新节点暂时不一致时，以物流服务返回的 current internal_status 决定摘要状态，以 checkpoints 决定时间线内容，前端不上推或改写状态。
- 每次打开弹窗获取同一时点的数据快照，避免摘要来自一次请求、轨迹来自另一次请求而产生瞬时冲突；具体技术实现由研发确定。

#### 隐私与日志

- 本弹窗不展示收件人、电话和收货地址，降低不必要的个人信息暴露。
- 客户端日志不得记录完整轨迹原始报文；运单号如进入分析或错误日志，应按公司日志规范处理。
- 页面错误文案不得确认其他用户的订单或 shipment 是否存在。

### 2.7 多语言内容处理（机制型）

#### 触发条件

- 用户打开订单详情时，状态卡按当前界面语言获取用户端物流文案。
- 用户打开 Tracking details 弹窗/抽屉时，再次按当前界面语言获取轨迹详情。
- 用户切换界面语言后重新打开轨迹详情，必须按新语言重新获取，不复用上一语言的状态或事件文案。

#### 服务端与前端职责

| 责任方 | 职责 |
|---|---|
| 物流服务 | 维护平台状态到 Looply 状态的映射、状态 i18n key、事件描述 i18n key及语言回退；返回可直接展示的用户端状态和事件描述。 |
| PC、APP、H5 前端 | 传递当前语言；通过前端语言包渲染固定 UI；直接展示服务端本地化后的状态和事件描述；负责日期时间地区格式化。 |
| 翻译中心 | 本期不接收物流 checkpoint、平台原始 message、固定 UI 文案或状态枚举记录。 |

#### 服务端语言回退

1. 目标语言的映射事件文案。
2. `en-US` 映射事件文案。
3. 可读的承运商原始 message。
4. `en-US` 用户状态文案。

状态文案与事件描述应使用同一次语言决策。只有降级到承运商原始 message 时允许事件描述保持渠道原文。

#### 日期与非翻译字段

- `checkpoint_time`：从 UTC 转换为用户展示时区，再按当前语言和地区格式化。
- `eta_min`、`eta_max`：保持目的地当地日历日期，仅按当前语言和地区格式化，不做时区转换。
- `carrier.name`、`tracking_no`、`location`：按原值展示，不进入语言包或翻译中心。

## 三、依赖与风险【必写】

### 3.1 上下游依赖

| 依赖 | 所需能力 | 责任方 |
|---|---|---|
| 订单服务 | 订单归属校验、包裹列表、包裹与 shipment_id 映射 | 订单后端 |
| 物流信息服务 | shipment 摘要、承运商、统一状态、ETA、完整轨迹 | 物流后端 |
| 账号与权限 | 登录态、用户身份及无权限处理 | 账号系统 |
| 国际化体系 | 前端固定文案语言包、物流服务 message package、语言回退和日期时间本地化 | 前端、物流后端、本地化 |
| 前台设计系统 | Modal、Skeleton、Toast、空态、错误态组件 | 前端 |

### 3.2 外部服务依赖

- 国际段物流轨迹和 AI EDD 依赖 AfterShip。
- 国内段轨迹依赖快递100，不提供 AfterShip AI EDD。
- 本前端不直接调用第三方服务；第三方不可用时由物流信息服务统一降级并返回用户可消费的结果。

### 3.3 风险与应对

| 风险 | 影响 | 应对 |
|---|---|---|
| 订单侧尚无包裹与 shipment_id 的稳定映射 | 多包裹可能打开错误轨迹 | 联调前明确映射字段和生命周期；不可使用 tracking_no 猜测关联。 |
| Figma 未覆盖异常态 | 前端实现可能不一致 | 本 PRD 已定义文案与行为，视觉沿用现有空态/错误态组件。 |
| 状态与轨迹异步更新 | 摘要和最新节点短暂不一致 | 使用同一数据快照；状态不由前端推导。 |
| 时区处理错误 | 轨迹日期偏移、ETA 日期变成前一天 | checkpoint 转用户时区；ETA 明确禁止时区换算。 |
| 第三方描述质量不稳定 | 出现空白或技术文案 | 使用物流服务映射与完整 fallback。 |
| 长轨迹性能 | 弹窗滚动卡顿 | 本期完整展示；研发根据真实节点规模选择合适渲染方式，但不得改变排序和完整性。 |

## 四、版本规划【必写】

### 4.1 当前版本 v1.4

- PC 订单详情按 Fulfillment Group 打开单运单 Tracking details 弹窗。
- 移动端 APP、H5 订单详情按 Fulfillment Group 打开单运单 Tracking Details Bottom Sheet。
- 展示承运商、可复制运单号、条件摘要字段（未签收为 ETA、已签收为 Status）和完整轨迹。
- 支持弹窗内部滚动、加载、空数据、失败重试及权限保护。
- 支持物流服务定义的 8 类 internal_status。
- 支持拆包订单，但不在弹窗内切换包裹。

### 4.2 后续迭代方向

| 方向 | 进入条件 |
|---|---|
| 订单级统一物流入口与弹窗内切包裹 | 完成新的多包裹交互设计后评估。 |
| 跳转承运商官网 | 明确业务价值、外链安全与 tracking_url_template 可用性后评估。 |
| 主动刷新或自动更新 | 有用户停留弹窗等待实时更新的明确需求后评估。 |

## 五、数据与埋点【按需】

### 5.1 埋点事件

| 事件 | 触发时机 | 关键字段 |
|---|---|---|
| `tracking_details_open` | 用户成功触发弹窗打开 | order_id、shipment_id、package_index、current_status |
| `tracking_details_load_result` | 首次加载或重试结束 | shipment_id、result、error_type、checkpoint_count、has_eta |
| `tracking_number_copy` | 用户点击复制后 | shipment_id、result |
| `tracking_details_retry` | 用户点击 Retry | shipment_id、previous_error_type |
| `tracking_details_close` | 用户关闭弹窗 | shipment_id、close_method、view_duration_ms、has_scrolled |

### 5.2 埋点约束

- `result`、`error_type`、`current_status` 使用受控枚举，不上传第三方原始错误信息。
- 不上传轨迹 message、location、完整 tracking_no 或收货信息。
- package_index 仅用于分析多包裹入口使用，不作为业务身份。

## 六、权限与角色矩阵【按需】

| 能力 | 当前订单买家 | 其他登录用户 | 游客 | 运营/客服后台角色 |
|---|---:|---:|---:|---:|
| 查看订单详情内入口 | 是 | 否 | 否 | 不适用 |
| 查看对应 shipment 轨迹 | 是 | 否 | 否 | 不通过本功能 |
| 复制运单号 | 是 | 否 | 否 | 不通过本功能 |
| 修改/取消物流追踪 | 否 | 否 | 否 | 通过其他系统按权限处理 |

## 七、验收标准【必写】

1. 单包裹订单点击已发货包裹组的物流状态卡，只打开该包裹的轨迹弹窗/抽屉。
2. 多包裹订单的不同 Fulfillment Group 状态卡分别展示对应 shipment，轨迹不串包。
3. 弹窗打开、关闭不离开订单详情，关闭后恢复原滚动位置及入口焦点。
4. 在途状态按 Figma 展示 Carrier、Tracking No.、日期范围和倒序轨迹。
5. 未签收时摘要第三行显示 `Est. delivery + 日期/日期范围`；仅 Delivered 时替换为 `Status + Delivered`，不得保留 `Est. delivery` 标签。
6. PC 弹窗或移动端 APP/H5 Bottom Sheet 的轨迹超过最大高度时，仅内容区滚动，标题与关闭按钮保持可用；可以触底查看最早节点。
7. 复制成功与失败均有明确反馈，复制内容为完整原始运单号。
8. 地点为空时仍展示节点时间，不出现多余空白占位。
9. 无轨迹、加载失败、无权限和资源不存在不会互相混淆。
10. checkpoint_time 转为用户展示时区；AfterShip AI EDD 直接按目的地当地日历日期格式化，不进行时区换算。
11. 页面不展示 tracking_health、第三方平台名、原始平台错误码或原始报文。
12. 非订单所有者即使获得 shipment_id 也无法查看其物流信息。
13. PC、APP、H5 在相同语言下展示一致的固定 UI、状态和映射事件文案。
14. 切换语言后重新打开轨迹详情，按新语言展示；目标语言缺失时回退 `en-US`，不显示空文本或未解析 i18n key。
15. 承运商原始 message、运单号、承运商名称和地点不生成翻译中心资源记录。
16. checkpoint_time 按用户时区和地区格式化；AI EDD 只做地区格式化，用户时区变化不得改变 ETA 日历日期。
17. 翻译中心不得产生 checkpoint 级批量翻译记录。

## 八、附录【必写】

### 8.1 输入源索引

| 输入源 | 版本/节点 | 用途 |
|---|---|---|
| 物流信息服务 PRD | v1.5，2026-06-29 | 业务规则、状态、ETA、时区及异常口径。 |
| 物流管理 ER 图 | v2.7，2026-06-29 | shipment、carrier、ETA、checkpoint 数据模型。 |
| 物流管理后台原型 | v5.11 antd，2026-06-11 | 后台字段及轨迹事实展示交叉检查。 |
| PC 前端 Figma | [Looply v1.0 — PC Tracking details](https://www.figma.com/design/rLK7XCdVvYqEHQHd7WjOkk/Looply-v1.0?node-id=2058-5798&p=f&t=m1Tl5y2Xfo9BOTzN-0)，node `2058:5798` | PC 订单详情弹窗布局与正常态交互。 |
| 移动端前端 Figma | [Looply v1.0 — Mobile Tracking details](https://www.figma.com/design/rLK7XCdVvYqEHQHd7WjOkk/Looply-v1.0?node-id=2058-7950&p=f&t=m1Tl5y2Xfo9BOTzN-0)，node `2058:7950` | APP、H5 订单详情 Bottom Sheet 布局、在途、送达及触底状态。 |
| 用户提供 Figma 截图 | 在途、送达最高滑动、送达滑动到底 | 当前 UI 验收基线。 |

### 8.2 输入源差异处理结论

| 差异 | 处理结论 |
|---|---|
| PC 与移动端采用不同容器 | PC 使用居中 Modal；移动端 APP、H5 使用底部 Bottom Sheet，业务字段与状态规则保持一致。 |
| 物流 PRD 包含商品、地址、客服、FAQ和五段进度条，Figma 无 | PC 弹窗不展示，这些内容由订单详情或后续需求承载。 |
| 本地 `物流轨迹.pen` 与线上 Figma 页面形态不同 | 本文不以该 `.pen` 作为 UI 验收依据。 |
| 物流服务支持一个订单多个 shipment，Figma 未设计弹窗内切换 | 采用方案 A：订单详情按 Fulfillment Group 展示独立物流状态卡并关联 `shipment_id`。 |
| 订单级 ETA 与订单维度送达日期 | 由订单模块定义；本 PRD 不制定聚合规则，仅定义单 shipment 的 ETA 与 Delivered 节点时间。 |
| Figma 仅展示正常在途和已送达 | 本文按现有设计系统补齐加载、空态、异常和权限场景。 |
| 移动端已送达稿为 `Status → Delivered`，PC 已送达稿为 `Est. delivery → Delivered` | 以订单 PRD 4.2.1 为统一业务口径：PC、APP、H5 均使用 `Status → Delivered`；PC Figma 待同步标签。 |

### 8.3 前后端字段映射

| 前端字段/行为 | 业务定义 | 物流/订单数据 | 差异结论 |
|---|---|---|---|
| 当前包裹入口 | 点击 Fulfillment Group 的物流状态卡打开单 shipment | 订单侧 fulfillment_group → shipment_id | 订单服务需提供稳定映射，前端不得用 tracking_no 猜测。 |
| Carrier | 承运商名称 | carriers.name | 一致。 |
| Tracking No. | 当前有效运单号 | shipments.tracking_no | 一致；允许后台纠错后变化。 |
| Est. delivery | 非 Delivered 展示 AI EDD；无 ETA 显示 `—` | eta_min、eta_max、internal_status | 仅非 Delivered 展示。 |
| Status | 仅 Delivered 时展示 `Delivered` | internal_status | 与 Est. delivery 在同一行条件替换，不同时展示。 |
| 当前物流状态 | 后端统一状态 | shipments.internal_status | 前端不自行映射平台状态。 |
| 节点状态 | 服务端返回的用户端统一状态文案 | mapped_internal_status / display_i18n_key | 服务端完成映射；MVP 可沿用物流渠道信息。 |
| 节点描述 | 服务端返回的可读事件描述 | message 及服务端 fallback | 服务端保证可读兜底，前端直接展示。 |
| 节点地点 | 可选地点 | tracking_checkpoints.location | 一致，空值隐藏。 |
| 节点时间 | 用户当地时间 | checkpoint_time（UTC） | 前端转换显示时区。 |
| 节点顺序 | 最新在前 | checkpoint_time 倒序 | 一致。 |
| 追踪健康度 | 不面向用户展示 | shipments.tracking_health | 明确隔离。 |

### 8.4 固定 UI i18n key 与英文基线

| 场景 | i18n key | `en-US` 基线 |
|---|---|---|
| 弹窗/抽屉标题 | `logistics.tracking.title` | Tracking Details |
| 承运商标签 | `logistics.tracking.carrier` | Carrier |
| 运单号标签 | `logistics.tracking.tracking_no` | Tracking No. |
| 预计送达标签 | `logistics.tracking.estimated_delivery` | Est. delivery |
| 物流状态标签 | `logistics.tracking.status` | Status |
| 轨迹标题 | `logistics.tracking.history` | Tracking History |
| 复制成功 | `logistics.tracking.copy_success` | Tracking number copied |
| 复制失败 | `logistics.tracking.copy_failed` | Unable to copy. Please copy the tracking number manually. |
| 无轨迹 | `logistics.tracking.waiting_scan` | Waiting for the carrier to scan the package. |
| 资源不可用 | `logistics.tracking.unavailable` | Tracking information is not available. |
| 加载失败 | `logistics.tracking.load_failed` | Unable to load tracking information. Please try again. |
| 重试按钮 | `common.retry` | Retry |
| 关闭按钮辅助文案 | `common.close` | Close |

### 8.5 翻译归属清单

| 业务对象 | 业务字段 | 内容类别 | 卡片决策 | resourceType | 翻译归属 | 展示面 | 语种及兜底 |
|---|---|---|---|---|---|---|---|
| Tracking details UI | 标题、标签、Toast、空态、错误态 | 静态 UI 文案 | 不进入业务卡片 | — | 前端语言包 | PC、APP、H5 | 当前语言缺失回退 `en-US` |
| 物流状态 | Pending、In Transit、Delivered 等 | 静态枚举文案 | 不进入业务卡片 | — | 物流服务 message package | 状态卡、摘要、轨迹节点 | 目标语言 → `en-US` |
| 物流事件映射 | 可枚举事件描述 | 静态映射文案 | 不进入业务卡片 | — | 物流服务 message package | Tracking History | 目标语言 → `en-US` → 原始 message |
| 承运商原始 message | 渠道实时事件原文 | 动态外部内容 | MVP 不翻译 | — | 保留渠道原文 | Tracking History 降级展示 | 映射缺失时展示可读原文 |
| 承运商 | `carrier.name` | 不翻译 | 不进入业务卡片 | — | 物流服务原值 | 摘要区 | 原值 |
| 运单号 | `tracking_no` | 不翻译 | 不进入业务卡片 | — | 物流服务原值 | 摘要区、复制 | 原值 |
| 地点 | `location` | 不翻译 | 不进入业务卡片 | — | 物流服务原值 | 轨迹节点 | 原值 |
| ETA | `eta_min`、`eta_max` | 日期格式化 | 不进入业务卡片 | — | 前端地区格式化 | 摘要区 | 目的地当地日期 |
| 轨迹时间 | `checkpoint_time` | 日期时间格式化 | 不进入业务卡片 | — | 前端地区格式化 | 轨迹节点 | 用户时区及当前地区格式 |

本期没有新增翻译中心业务资源卡片，因此无 `resourceType`、migration 或 `translation_record` 新增。若后续要求运营在翻译中心人工维护物流事件模板，应另行确认新建卡片，不得复用商品、CMS 或其他相似卡片。
