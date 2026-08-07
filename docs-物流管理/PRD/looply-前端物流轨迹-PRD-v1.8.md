# Looply 前端物流轨迹 PRD

> 版本：v1.8  
> 日期：2026-08-07  
> 适用端：PC Web、移动端（APP、H5）  
> 需求状态：待产品、设计、前后端及测试评审

## 一、概述【必写】

### 1.1 背景与目标

用户需要在订单详情中查看某个包裹的承运商、运单号、预计送达信息和完整物流轨迹。现有物流信息服务已经具备运单、承运商、预计送达日期和轨迹节点等数据能力，本需求将这些能力以订单详情内的 `Tracking details` PC 弹窗或移动端 Bottom Sheet 提供给 PC Web、APP、H5 用户。

本期目标：

- 用户无需离开订单详情即可查看单个包裹的物流信息。
- 同一订单拆成多个包裹时，每个包裹独立查看，避免轨迹混合。
- 前端展示口径与物流信息服务 PRD v1.9、物流 ER 图 v2.7 一致。
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
- 翻译中心“前端页面”域新增“物流轨迹”卡片，稳定标识为 `page_logistics_tracking`。
- 卡片本期只维护两类内容：固定 UI 文案、Looply 8 个统一物流状态文案；PC、APP、H5 共用。
- 固定 UI 译文同步至前端语言包，前端仍通过稳定 i18n key 获取，不直接在组件中写文案。
- 物流状态由物流服务完成平台状态映射，并读取同一卡片中的状态译文；前端直接展示服务端返回的 statusLabel。
- 轨迹事件描述和承运商原始 message 本期不进入该卡片、不按 checkpoint 生成翻译记录；优先展示渠道可读原文，原文不可读时回退本地化状态文案。
- 当前语言由订单前端传递给物流服务；状态译文缺失时按“目标语言状态文案 → `en-US` 状态文案”降级。
- 轨迹时间以服务端返回的 UTC 时间为基准，展示时转换为用户当前选择/账号设置的时区；若账号无时区设置，使用浏览器时区。
- AfterShip AI EDD 表示该 shipment 目的地所在地的预计送达日历日期，不是时间戳；前端仅做语言与日期格式化，不做 UTC 换算或任何时区加减。
- 美国等多时区国家按该票 shipment 的目的地地址解释 AI EDD 日期；同一 shipment 的 EDD 不随查询用户所在地、账号时区、浏览器时区或请求 locale 改变。
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
| 包裹未关联 shipment | 不打开空弹窗；订单详情使用 `logistics.tracking.unavailable`：`Tracking information is currently unavailable.` |
| shipment 与当前订单不匹配 | 拒绝展示并记录异常，不使用前端传入的运单号绕过关系校验。 |
| 重复快速点击 | 同一入口在请求完成前防重复触发，仅保留一个弹窗和一次有效请求。 |

#### UI 关联

- PC：[Looply 1.1 — PC Tracking details](https://www.figma.com/design/sAOLkw0gIl1bwQRYCDqKuW/Looply-1.1?node-id=32-296&p=f&m=dev)，节点 `32:296`。
- 移动端（APP、H5）：[Looply 1.1 — Mobile Tracking details](https://www.figma.com/design/sAOLkw0gIl1bwQRYCDqKuW/Looply-1.1?node-id=9-11674&p=f&m=dev)，节点 `9:11674`。

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

| 区域 | 元素 | 数据来源/展示规则 | 多语言归属与实现 |
|---|---|---|---|
| 标题区 | `Tracking Details` | 固定文案。 | 前端语言包：`t('logistics.tracking.title')`。 |
| 标题区 | 关闭按钮 | 点击关闭弹窗/抽屉。 | 图标无可见文案；辅助名称使用 `t('common.close')`。 |
| 运单摘要 | `Carrier` 标签 | 固定标签。 | 前端语言包：`t('logistics.tracking.carrier')`。 |
| 运单摘要 | 承运商名称 | `carrier.name`；为空时显示 `—`。 | 服务端原值，不翻译。 |
| 运单摘要 | `Tracking No.` 标签 | 固定标签。 | 前端语言包：`t('logistics.tracking.tracking_no')`。 |
| 运单摘要 | 运单号 | `tracking_no`；保持原始字符，不自动插入或移除空格。 | 服务端原值，不翻译。 |
| 运单摘要 | 复制图标 | 仅 tracking_no 非空时展示。 | 辅助名称使用 `t('logistics.tracking.copy_tracking_no')`；成功/失败 Toast 分别使用 `copy_success`、`copy_failed`。 |
| 运单摘要 | `Est. delivery` 标签 | 非 Delivered 时展示。 | 前端语言包：`t('logistics.tracking.estimated_delivery')`。 |
| 运单摘要 | ETA 值 | 日期/日期范围；无 ETA 显示 `—`。 | 使用 locale 日期格式化；AI EDD 不做时区转换，不走语言包。 |
| 运单摘要 | `Status` 标签 | 仅 Delivered 时替换 Est. delivery 标签。 | 前端语言包：`t('logistics.tracking.status')`。 |
| 运单摘要 | Delivered 状态值 | 展示物流服务返回的已本地化状态。 | 服务端本地化结果，前端直接展示，不使用前端 `Delivered` 常量。 |
| 轨迹区 | `Tracking History` | 固定标题。 | 前端语言包：`t('logistics.tracking.history')`。 |
| 轨迹节点 | 状态 | 物流服务返回的用户端统一状态文案。 | 服务端本地化结果，前端直接展示。 |
| 轨迹节点 | 描述 | 物流服务返回的可读渠道事件描述。 | 渠道原文，不进入翻译中心；不可读或为空时回退该节点的本地化状态文案。 |
| 轨迹节点 | 地点 | `location` 非空时展示地点图标和文本；为空时整行隐藏。 | 服务端原值，不翻译。 |
| 轨迹节点 | 时间 | `checkpoint_time` 转用户时区后展示；与地点位于同一辅助信息行。 | 使用 locale 日期时间格式化，不走语言包。 |
| 加载态 | loading spinner | 获取轨迹数据期间展示。 | 无可见固定文案；辅助名称使用 `t('common.loading')`。 |
| 错误/空态 | 提示文案及 Retry | 按页面状态变体展示。 | 分别使用 `waiting_scan`、`unavailable`、`load_failed`、`common.retry`，禁止写死英文。 |

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

- PC：[Looply 1.1 — PC Tracking details](https://www.figma.com/design/sAOLkw0gIl1bwQRYCDqKuW/Looply-1.1?node-id=32-296&p=f&m=dev)，节点 `32:296`，覆盖在途、送达最高滑动、送达滑动到底。
- 移动端（APP、H5）：[Looply 1.1 — Mobile Tracking details](https://www.figma.com/design/sAOLkw0gIl1bwQRYCDqKuW/Looply-1.1?node-id=9-11674&p=f&m=dev)，节点 `9:11674`，覆盖在途、送达最高滑动、送达触底。

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
- AfterShip AI EDD 返回值是该 shipment 目的地所在地的日历日期。美国等多时区国家按目的地地址解释日期语义；它不是 UTC 时间戳，前端不得做时区转换或日期加减。
- 同一 shipment 无论由哪个国家或时区的用户查询，`eta_min`、`eta_max` 的日期事实保持不变；locale 只改变日期格式和月份名称，不改变日期值。
- 前端不得从目的地州、城市或邮编自行推导时区，也不得在目的地信息不足时修正、补算或猜测 EDD；仅展示物流服务返回的日期事实。
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
| shipment 存在但无轨迹 | 摘要保留；轨迹区使用 `logistics.tracking.waiting_scan`：`Tracking updates will appear after the carrier scans your package.` |
| 物流异常 | 摘要保留；最新异常节点使用异常色，其余节点正常展示。 |
| 数据加载中 | 按 Figma 显示弹窗/抽屉内 loading spinner，关闭按钮可用；不展示旧 shipment 数据。 |
| 网络异常或请求超时 | 弹窗内显示加载失败错误态和 `Retry`；保留关闭能力，不清空或刷新背景订单详情。 |
| 首次加载失败 | 弹窗内显示错误态和 `Retry`；不得伪装成无轨迹。 |
| 重试中 | 保留错误区位置并显示加载反馈，禁止重复点击。 |
| shipment 不存在/不可访问 | 使用 `logistics.tracking.unavailable`：`Tracking information is currently unavailable.`，不展示任何运单信息。 |
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
| 物流服务 | 维护平台状态到 Looply 8 状态的映射；按 locale 读取 `page_logistics_tracking` 中的状态译文；返回 statusLabel 和可读渠道事件描述。 |
| PC、APP、H5 前端 | 传递当前语言；使用从 `page_logistics_tracking` 同步的前端语言包渲染固定 UI；展示服务端 statusLabel 和事件原文；负责日期时间地区格式化。 |
| 翻译中心 | 在“前端页面 → 物流轨迹”卡片维护固定 UI 和 8 个状态译文；不接收 checkpoint 实例或平台原始 message。 |

#### 文案回退

- 固定 UI：目标语言前端语言包 → `en-US` 前端语言包；不得显示未解析 key。
- 状态文案：目标语言状态译文 → `en-US` 状态译文；不得回退平台 tag/state。
- 事件描述：可读渠道原始 message → 当前节点本地化 statusLabel。事件原文允许与界面语言不同。

#### 日期与非翻译字段

- `checkpoint_time`：从 UTC 转换为用户展示时区，再按当前语言和地区格式化。
- `eta_min`、`eta_max`：保持 shipment 目的地当地日历日期；美国等多时区国家按该票目的地地址解释，仅按当前语言和地区格式化，不做时区转换。
- `carrier.name`、`tracking_no`、`location`：按原值展示，不进入语言包或翻译中心。

#### AI Coding 与前端实现硬性规则

1. 前端组件、模板、状态配置和 Toast 调用中，禁止直接写入用户可见的固定英文或中文字符串。
2. 标记为“前端语言包”的内容必须通过本 PRD 指定的稳定 i18n key 获取；不得根据英文源文临时生成 key。
3. 物流状态直接展示服务端本地化 statusLabel；事件描述展示服务端返回的渠道原文或状态兜底。禁止前端维护 `internal_status → 文案` 映射，禁止对平台 tag、subtag、message 自行翻译。
4. 日期、时间和日期范围必须使用项目统一 locale formatter；禁止拼接月份、星期、`Delivered on` 等字符串。
5. 带变量的固定文案必须使用语言包占位符插值，不得通过字符串相加组装；本期暂无必须展示的带变量固定文案。
6. `carrier.name`、`tracking_no`、`location` 和承运商原始 message 按规定原值展示，不得调用前端机器翻译或语言包。
7. 前端语言切换后，组件不得继续复用上一语言的服务端状态/事件缓存；重新打开轨迹详情时按当前语言获取。
8. 代码评审和 AI Coding 验收必须扫描新增用户可见硬编码文案；除 `—` 等无语言语义符号外，出现未登记字符串视为不通过。

## 三、依赖与风险【必写】

### 3.1 上下游依赖

| 依赖 | 所需能力 | 责任方 |
|---|---|---|
| 订单服务 | 订单归属校验、包裹列表、包裹与 shipment_id 映射 | 订单后端 |
| 物流信息服务 | shipment 摘要、承运商、统一状态、ETA、完整轨迹 | 物流后端 |
| 账号与权限 | 登录态、用户身份及无权限处理 | 账号系统 |
| 翻译中心与国际化体系 | 注册 `page_logistics_tracking`，维护固定 UI 和 8 个状态译文，同步前端语言包并供物流服务读取状态译文 | 翻译平台、前端、物流后端、本地化 |
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
| 时区处理错误 | 轨迹日期偏移、ETA 日期变成前一天 | checkpoint 转用户时区；ETA 明确禁止时区换算。美国等多时区国家以 shipment 目的地解释 EDD，不随查看者时区改变。 |
| 目的地信息不足 | AfterShip 无法准确识别多时区国家内的目的地区域，EDD 缺失或准确性下降 | 由创建/更新 shipment 的上游系统向物流服务提供足够的目的地国家、州/省、城市或邮编；前端不猜测、不补算。 |
| 第三方描述质量不稳定 | 出现空白或技术文案 | 使用物流服务映射与完整 fallback。 |
| 长轨迹性能 | 弹窗滚动卡顿 | 本期完整展示；研发根据真实节点规模选择合适渲染方式，但不得改变排序和完整性。 |

## 四、版本规划【必写】

### 4.1 当前版本 v1.8

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
10. checkpoint_time 转为用户展示时区；AfterShip AI EDD 直接按 shipment 目的地当地日历日期格式化，不进行时区换算。
11. 页面不展示 tracking_health、第三方平台名、原始平台错误码或原始报文。
12. 非订单所有者即使获得 shipment_id 也无法查看其物流信息。
13. PC、APP、H5 在相同语言下展示一致的固定 UI 和状态文案；渠道事件原文允许保持原语言。
14. 切换语言后重新打开轨迹详情，固定 UI 和状态按新语言展示；目标语言缺失时回退 `en-US`，不显示空文本或未解析 i18n key。
15. 承运商原始 message、运单号、承运商名称和地点不生成翻译中心资源记录。
16. checkpoint_time 按用户时区和地区格式化；AI EDD 只做地区格式化，用户时区变化不得改变 ETA 日历日期。
17. 对美国等多时区国家，同一 shipment 在不同时区、不同 locale 下查询，`eta_min`、`eta_max` 日期事实保持一致；前端不得根据查看者时区或目的地地址自行换算。
18. 翻译中心不得产生 checkpoint 级批量翻译记录。
19. 前端代码中没有写死本 PRD 所列固定用户文案；所有固定文案均通过对应 i18n key 获取。
20. 状态和事件描述不在前端二次映射或翻译，日期时间不通过字符串拼接生成。
21. 复制、关闭和 loading spinner 均具有通过语言包生成的可访问辅助名称。
22. 翻译中心“前端页面”域可查看“物流轨迹”卡片，resourceType 为 `page_logistics_tracking`，基础记录为15条固定 UI + 8条状态。
23. 无轨迹、不可用、加载失败分别命中 `waiting_scan`、`unavailable`、`load_failed`，加载失败提供 Retry；三种状态不得共用文案。

## 八、附录【必写】

### 8.1 输入源索引

| 输入源 | 版本/节点 | 用途 |
|---|---|---|
| 物流信息服务 PRD | v1.9，2026-08-07 | 业务规则、状态、ETA、多时区国家日期语义及异常口径。 |
| 物流管理 ER 图 | v2.7，2026-06-29 | shipment、carrier、ETA、checkpoint 数据模型。 |
| 物流管理后台原型 | v5.11 antd，2026-06-11 | 后台字段及轨迹事实展示交叉检查。 |
| PC 前端 Figma | [Looply 1.1 — PC Tracking details](https://www.figma.com/design/sAOLkw0gIl1bwQRYCDqKuW/Looply-1.1?node-id=32-296&p=f&m=dev)，node `32:296` | PC 订单详情弹窗布局与正常态交互。 |
| 移动端前端 Figma | [Looply 1.1 — Mobile Tracking details](https://www.figma.com/design/sAOLkw0gIl1bwQRYCDqKuW/Looply-1.1?node-id=9-11674&p=f&m=dev)，node `9:11674` | APP、H5 订单详情 Bottom Sheet 布局、在途、送达及触底状态。 |
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
| 复制图标辅助文案 | `logistics.tracking.copy_tracking_no` | Copy tracking number |
| 复制成功 | `logistics.tracking.copy_success` | Tracking number copied |
| 复制失败 | `logistics.tracking.copy_failed` | Unable to copy. Please copy the tracking number manually. |
| 无轨迹 | `logistics.tracking.waiting_scan` | Tracking updates will appear after the carrier scans your package. |
| 资源不可用 | `logistics.tracking.unavailable` | Tracking information is currently unavailable. |
| 加载失败 | `logistics.tracking.load_failed` | Unable to load tracking information. Please try again. |
| 重试按钮 | `common.retry` | Retry |
| 关闭按钮辅助文案 | `common.close` | Close |
| 加载状态辅助文案 | `common.loading` | Loading |

### 8.5 翻译归属清单

| 业务对象 | 业务字段 | 内容类别 | 卡片决策 | resourceType | 翻译中心路径 | 展示面 | 语种及兜底 |
|---|---|---|---|---|---|---|---|
| Tracking details UI | 标题、标签、Toast、空态、错误态、辅助文案 | 静态 UI 文案 | 新增并写入物流轨迹卡片 | `page_logistics_tracking` | 前端页面 → 物流轨迹 | PC、APP、H5 | 目标语言 → `en-US` |
| 物流状态 | 8 个 Looply 统一状态 label | 静态枚举文案 | 写入同一物流轨迹卡片 | `page_logistics_tracking` | 前端页面 → 物流轨迹 | 状态卡、摘要、轨迹节点 | 目标语言 → `en-US` |
| 轨迹事件描述 | 渠道实时事件原文 | 动态外部内容 | 本期不写入卡片 | — | — | Tracking History | 可读原文 → 本地化状态文案 |
| checkpoint 实例 | 单个包裹轨迹记录 | 动态业务数据 | 不写入卡片 | — | — | Tracking History | 不翻译 |
| 承运商、运单号、地点 | 原值字段 | 不翻译 | 不写入卡片 | — | — | 摘要、轨迹节点 | 原值 |
| ETA、轨迹时间 | 日期时间事实 | 日期格式化 | 不写入卡片 | — | — | 摘要、轨迹节点 | locale formatter |

### 8.6 物流轨迹翻译卡片注册规则

| 配置项 | 定义 |
|---|---|
| domain / domainName | 前端页面 / 前端页面 |
| 卡片名称 | 物流轨迹 |
| resourceType | `page_logistics_tracking` |
| 源语言 | `en-US` |
| 目标语种 | 跟随平台已启用语种 |
| 运营路径 | 多语言管理 → Translation → 前端页面 → 物流轨迹 |
| 记录范围 | 固定 UI key + 8 个统一状态 key |
| 明确排除 | checkpoint、平台原始 message、承运商、运单号、地点、ETA和时间事实 |

状态资源记录：

| internal_status | resourceId / i18n key | `en-US` 源文 |
|---|---|---|
| Pending | `logistics.status.pending` | Pending |
| InfoReceived | `logistics.status.info_received` | Info Received |
| InTransit | `logistics.status.in_transit` | In Transit |
| OutForDelivery | `logistics.status.out_for_delivery` | Out for Delivery |
| AvailableForPickup | `logistics.status.ready_for_pickup` | Ready for Pickup |
| AttemptFail | `logistics.status.delivery_attempt_failed` | Delivery Attempt Failed |
| Delivered | `logistics.status.delivered` | Delivered |
| Exception | `logistics.status.delivery_exception` | Delivery Exception |

卡片使用“一条 i18n key 对应一条翻译资源记录”的方式：`resourceId = i18n key`，`fieldName = text`。前端固定 UI 译文同步进入前端语言包；物流服务使用同一卡片中的 8 个状态 key 获取 statusLabel。两端不得创建同义但不同 key 的重复记录。

本期卡片预计包含 23 条基础记录：15 条固定 UI key + 8 条状态 key。后续新增固定 UI 文案时继续写入该卡片；新增渠道事件 message 不自动增加翻译记录。
