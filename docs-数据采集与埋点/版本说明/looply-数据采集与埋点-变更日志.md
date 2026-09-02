# Looply 数据采集与埋点变更日志

## 基线版本（已交付开发）

**v1.4（2026-08-17）**

- PRD：`looply-数据采集与埋点产品需求-v1.4.md`
- 状态：已冻结版本，继续保留，不用本轮补充内容覆盖。

## v1.5（进行中）— 未交付

### 新增交付物

- 无。

### 变更内容

#### PRD调整

##### 🔄 全页面有意义操作补齐

- **PRD版本**：v1.4 → v1.5
- **PRD文件**：`looply-数据采集与埋点产品需求-v1.5.md`
- **来源**：`looply-PC-Mobile全页面有意义操作覆盖清单-v0.1.md`
- **变更内容**：
  - 补充Authentication、密码恢复、Header／Footer、商详辅助交互、订单搜索、Returns、Delivery、Shopping Bag、Checkout、Account、Contact Us及About Us页面映射与稳定操作名。
  - 补齐筛选／排序关闭、筛选分组展开收起、View all、取消全选、移除优惠等已有节点缺失动作。
  - 根据Figma状态页补齐Returns真实按钮、Shopping Bag失效商品Clear all，以及支付成功页复制订单号和Continue Shopping。
  - 保持业务成功事件、订单／支付／退款／售后权威事实和GA4既有边界不变；新增内容主要进入一方平台的`ui_interaction`或复用现有统一事件。

#### GA4埋点变更清单调整

- **文件版本**：v1.0 → v1.1
- **文件名称**：`looply-GA4首版变更清单-v1.0.md` → `looply-GA4埋点变更清单-v1.1.md`
- **变更内容**：
  - 根据开发确认的现有Browser Claim前后端互斥方案，从待修改清单删除`purchase`。
  - 当前清单只保留确实需要调整或新增的五个GA4事件。
  - 历史v1.0继续保留用于版本追溯。

#### GA4搜索与购物车开发确认收口

- **文件版本**：GA4埋点变更清单v1.1 → v1.2。
- **变更内容**：
  - `search`仅记录用户通过站内入口主动提交搜索；直达搜索URL、刷新和页面恢复不补造`search`。
  - 结果实际展示继续发送`view_search_results`；无前序提交时允许独立存在，有前序`search`时复用相同`search_id`。
  - 明确关闭GA4增强型衡量中的“网站搜索”，保留主动`view_search_results`，避免双发。
  - 删除`search_version`、`index_version`和`cart_id`的GA4必填要求，不为GA4扩大搜推或购物车接口范围。
  - `view_cart`只包含全部可购商品；`remove_from_cart`本期只覆盖一物一码商品成功删除。

#### PRD文档职责收口

- **PRD版本**：v1.5工作稿内持续更新
- **变更内容**：
  - 从《数据采集与埋点产品需求》移除GA4架构、平台口径、字段映射、事件验收和专项文档引用。
  - PRD只保留一方平台的采集要求及搜推存量埋点调整。
  - GA4现状与变更要求统一由独立《Looply GA4埋点变更清单》维护。

### 影响范围

- **PRD**：已形成v1.5补充稿，待产品确认后冻结。
- **UI**：无修改，以Figma Looply 1.1和测试站核对结果为输入。
- **GA4**：变更清单更新至v1.1；`purchase`不再列为本期改造项。
- **广告／搜推**：无新增平台改造要求；已存在统一业务事件继续复用。

### 待办事项

- [ ] 产品确认v1.5新增页面与操作清单。
- [ ] 确认后执行冻结前一致性检查并同步文档中心。

## v1.6（开发交付基线）

### 新增交付物

- `looply-数据采集与埋点-v1.5开发审查问题处理结论-v1.0.md`
- `looply-数据采集与埋点产品需求-v1.6.md`

### 变更内容

- 逐条闭合开发对v1.5提出的事件命名、搜索语义、身份与Session、字段可获得性、权威业务事实范围、不存在场景、枚举和分享事件迁移问题。
- 将原22项拆分为17个Web／SDK客户端统一事件和5类权威业务事实，订单、支付和退款事实不再列为Web埋点任务。
- 搜索现有两个`search`调用点分别迁移为统一`search`和`view_search_results`，使用同一`search_id`关联，不再新增第三条同义事件。
- 客户端商品事件只强制`listing_public_code`；内部`product_id`和内部`listing_id`由下游映射补充。
- 登出和切换账号不结束行为Session，只改变身份状态；Session继续执行首个有效事件建立、连续30分钟无有效事件结束的规则。
- 删除当前系统拿不到或业务尚不存在的首期必填字段与交互场景。
- 页面范围明确为PC没有独立Shop和Favorites，Mobile按现有Shop和Favorites页面实施，Tablet和App不在本期范围。
- `payment_type`直接沿用当前API的`credit_card/paypal/klarna`，不增加转换层。
- 增加存量12个Active事件及`share_*`事件族的复用和迁移要求。
- 补充`visitor_id → anonymous_id`术语映射、位置从1开始、取消收藏不删除历史触点，以及成交／退款商品行最小信息。
- 搜索结果页正式Apply筛选、Apply排序或Reset时生成新`search_id`，同步形成`search`和唯一`view_search_results`终态。
- 将第八章的两套页面操作命名收敛为一张权威映射表，补齐页面、模块、展示位、操作、控件和目标的稳定业务名。
- Delivery收口为订单页内的物流详情模块；Shopping Bag商品卡点击继续复用`select_item`；Checkout地址与Account地址管理动作分开定义。
- 补充`auth/change_password`页面标识，并将密码找回与修改密码分别映射到对应目标页面。
- 在客户端事件触发摘要中明确Shopping Bag商品卡点击复用`select_item`，与第八章操作映射保持一致。
- 明确六个存量`share_*`真实物理名称和调用点属于开发技术迁移盘点，不作为产品PRD冻结条件；产品侧迁移目标和禁止双计规则已经闭合。

### 影响范围

- **产品需求**：v1.6取代v1.5成为后续开发实施基线；v1.5继续作为历史版本保留。
- **Web／SDK**：按17个客户端统一事件、存量迁移表和页面操作唯一映射实施。
- **服务端／数据平台**：五类权威业务事实另建接入任务，不由Web重复上报。

### 待办事项

- [ ] 开发在技术迁移清单中登记六个现有`share_*`真实物理名称和调用点，并按v1.6统一迁移。
- [ ] 开发完成后按v1.6逐事件、逐页面操作验收。

### 版本关系

- v1.5继续保留为历史版本，不覆盖、不删除。
- v1.6已收口为开发交付基线；六个`share_*`真实物理名称和调用点由开发在技术迁移方案中登记，不再作为产品PRD阻塞项。

## v1.7（开发评审稿）

### 新增交付物

- `looply-数据采集与埋点-v1.7开发问题处理结论-v1.0.md`

### 变更内容

- 取消一方平台与GA4的搜索请求ID要求，不再生成、传递或验收该字段。
- 搜索结果合集页URL承载搜索词对应参数、`trigger_type`、已生效筛选和排序；各事件将这些参数解析为结构化搜索上下文。
- 搜索次数直接按去重`search`事件计数；结果状态按`view_search_results.event_id`计数。
- 搜索结果曝光、点击与商详来源使用结果页`page_instance_id`、结构化URL上下文、商品标识、Session和事件时间关联。
- 筛选、排序和Reset只记录结果页操作及更新后的`view_search_results`，不再产生新的`search`。
- 开发问题处理结论明确：`anonymous_id`由身份模块生成并作为稳定匿名主体ID上传，Snowplow `domain_userid`作为浏览器辅助标识同时上传但不参与身份合并；PC无Shop和Favorites聚合入口但覆盖PC Wishlist和Recently Viewed；支付枚举增加`apple_pay`；搜索结果请求使用四种唯一终态且不设置搜索请求关联ID；旧分享调用按打开、关闭、渠道选择、复制链接和系统分享迁移为`ui_interaction`，入口曝光、旧完成记录和短码记录停止进入一方平台；当前不存在的Account Privacy下载数据和删除账号操作不预埋。
- 授权技术团队决定字段类型、长度、空值、ID格式、Schema／SDK版本和兼容实现；业务事件语义、业务枚举、PII边界及防重复原则继续以产品文档为准。
- 明确五类服务端权威事实另建服务端／数据平台任务，不由Web SDK上报。

#### GA4 `trigger_type`验收与变更清单补齐

- **文件版本**：GA4埋点变更清单v1.3 → v1.4。
- **变更内容**：
  - 完整定义`carousel_term_button`、`manual_enter`、`manual_search_button`、`suggestion_select`、`history_select`和`popular_term_select`六种枚举及判定边界。
  - 明确同一枚举从搜索提交动作进入结果页URL，再由`search`、`view_search_results`和搜索结果`view_item_list`读取并进入GA4。
  - 明确筛选、排序和Reset保留原`trigger_type`且不新增`search`；直达URL无该参数时留空，不伪造。
  - 同步修正测试环境验收记录，移除已取消的搜索请求ID验收要求。
- 同步形成GA4变更清单v1.3、GA4开发确认结论v1.1、页面操作覆盖清单v0.2、数据分析报表PRD v0.2、指标来源对照表v0.2和采集影响评估v0.2。

### 影响范围

- **Web／SDK**：删除搜索请求ID生成和透传；确保结果页URL参数及其结构化事件字段一致。
- **GA4**：不再验收搜索请求ID；继续验收搜索提交、结果终态、曝光和购物车事件。
- **报表**：搜索提交规模与结果状态分别统计；不再建设单次搜索请求级严格漏斗。

### 待办事项

- [ ] 开发确认结果页URL参数与事件结构化字段映射。
- [ ] 按v1.7和GA4变更清单v1.3完成搜索链路验收。

## v1.8（开发实施基线）

### 新增交付物

- `looply-数据采集与埋点产品需求-v1.8.md`
- `looply-GA4数据分析-PRD-v1.5.md`
- `looply-GA4五事件新增与修改-PRD-v1.1.md`
- `looply-GA4埋点变更清单-v1.5.md`
- `looply-一方埋点公共实施规则-v1.7.md`
- `Looply-v1.4-详细埋点需求定稿-v1.2.xlsx`
- `looply-一方埋点公共实施规则-v1.8.md`
- `Looply-v1.4-详细埋点需求定稿-v1.3.xlsx`
- `looply-一方埋点三份开发基线-20260828版本差异-v1.0.md`

### 变更内容

#### 一方售后点位与无生产入口点位收口（2026-08-28）

- 详细埋点需求定稿v1.2升级为v1.3，公共实施规则v1.7升级为v1.8；公共基础字段表继续使用v1.1。
- 12个当前没有真实生产控件或可达入口的点位转入停止项，从Active覆盖率分母排除，原点位ID保留且不得复用。
- `pt-0192`统一覆盖d3页面内复制和d4物流弹窗复制，使用真实`shipment_id`并由`copy_source`区分入口。
- `pt-0196/0197/0199/0200/0202`统一按同一订单内多商品退货处理：一次操作一条事件，`target_id=order_id`，`order_item_ids`传订单商品行数组；单商品也使用单元素数组。
- 本次为一方埋点契约调整，不修改GA4事件、参数或报表口径。

- Search与Collection筛选上下文统一由后台稳定`dimension_code`和`option_code`形成，不再由前端固定维度白名单决定可上报范围。
- GA4把最终已Apply离散筛选集合序列化为逗号连接的`filter_ids`；一方埋点保留`filter_ids[]`数组，两者读取同一公共筛选事实。
- Search／Collection筛选组交互使用`dimension_code`，筛选项选择使用`dimension_code:option_code`，Apply携带最终集合；选择后取消、关闭或Reset不得残留旧值。
- Collection商品曝光与点击补充最终筛选和排序上下文。
- 后台／数据平台维护稳定Code到展示名称的可追溯映射，报表展示阶段关联名称。

### 影响范围

- **Web／SDK**：统一Search／Collection动态筛选事实及GA4、一方两个适配出口。
- **GA4**：更新`view_search_results`及Search／Collection筛选后商品曝光的`filter_ids`。
- **一方平台**：更新筛选Apply、Collection曝光／点击及筛选交互的稳定Code字段。
- **公共字段表**：无新增公共字段，继续使用v1.1。
- **数据平台**：补充筛选维度／选项Code到展示名称的可追溯映射。

### 待办事项

- [ ] 开发按新基线完成Search／Collection动态筛选上下文改造。
- [ ] 测试按PC／Mobile的单选、多选、动态`Series`、选择后取消、Reset和无筛选完成双平台复验。
