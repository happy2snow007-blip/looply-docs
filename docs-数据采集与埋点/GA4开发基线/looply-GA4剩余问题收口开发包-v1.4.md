# Looply GA4 剩余问题收口开发包

> 版本：v1.4  
> 日期：2026-08-31  
> 状态：开发收口基线
> 说明：历史版本，不再作为当前开发依据；当前依据为 GA4 PRD v1.10。
> 适用环境：生产站 `https://www.looply.com/`  
> GA4：Property `531542304`，Measurement ID `G-Z2EKP8QGT7`  
> 文档中心正式需求基线：《looply-GA4数据分析-PRD-v1.8》《looply-数据采集与埋点产品需求-v1.9》  
> 本文件职责：记录本次生产验收发现的问题，并集中定义剩余问题的开发结果、可执行验收契约、提测证据和发布门禁；不重新定义完整 GA4 事件体系。

## 一、目标与范围

### 1.1 目标

本轮一次性关闭 2026-08-31 生产复验仍未通过的 GA4 问题，使开发、测试和产品可以使用同一组动作与断言完成自测、回归和验收。

### 1.2 当前基线

2026-08-26 修复单共 12 个 FIX。截至 2026-08-31：7 个通过，2 个部分通过，3 个未通过。本轮只处理下列 5 个剩余问题，并按共同根因合并为 4 个开发任务。

| 开发任务 | 收口问题 | 当前状态 |
|---|---|---|
| T1 当前页面与来源语义纠正 | FIX-09 `page_location/page_referrer` | 待按最终口径复验 |
| T2 主动事件来源标识全链路 | FIX-05 `page_view_source`；FIX-06 `view_search_results_source` | Web已具备，GTM／发布链路未通过 |
| T3 Wishlist 公共列表事件 | FIX-08 Wishlist 曝光与 PC 点击 | 部分通过 |
| T4 配送方式版本 | FIX-12 `add_shipping_info` tier版本 | 首次tier已通过；地址变化但tier不变不属于缺陷 |

## 二、本次生产验收发现的问题

### 2.1 问题明细

| 编号 | 问题 | 本次真实复现 | 当前影响 | 对应收口任务 |
|---|---|---|---|---|
| A01 | 主动 `page_view` 缺 `page_view_source` | PC Search、Collection、PDP，以及 Mobile Search、Favorites、PDP 的主动 `page_view` 已携带 `page_instance_id`，但均未携带 `page_view_source=looply_custom` | 主动与 GA 自动 `page_view` 无法使用稳定字段区分 | T2 |
| A02 | 主动 `view_search_results` 缺来源字段 | PC 搜索 `chanel`、`dior`，Mobile 搜索 `gucci`，以及筛选后的主动结果事件均未携带 `view_search_results_source=looply_custom`；Mobile `gucci` 已正常上报结果数 5963 和耗时 963 ms | 主动结果事件与 GA 自动网站搜索事件无法按稳定来源字段区分 | T2 |
| A03 | 当前页面URL与来源字段曾被混用 | 筛选后点击商品时，`select_item.page_referrer`仍为当前Search实例建立前的上一页面，这符合最终语义；需要验证`select_item.page_location`为筛选后的完整URL。从`dior`提交`prada`后，新页面实例的`page_referrer`仍为基础`/search`则不符合要求 | 如继续用`page_referrer`承载当前动作URL，会破坏标准来源语义并导致测试Oracle漂移 | T1 |
| A04 | Wishlist 曝光和 PC 点击漏发 | PC Favorites Drawer 展示商品并等待后没有 `view_item_list`，点击后只有 `view_item`、没有 `select_item`；Mobile Favorites 首屏等待约 6.5 秒也没有 `view_item_list`；Mobile 点击第 1 件已正确发送 `favorites_wishlist + index=1` | Wishlist 曝光缺失，PC 点击链路断开，PC 与 Mobile 不能统一计算列表表现 | T3 |
| A05 | 配送验收口径曾与既有确认冲突 | 首次有效配送方式已发送`step_version=1`、`shipping_tier=standard_fedex`。修改地址后没有新的保存请求，且有效tier未变化 | 按最终口径不应新增事件，也不要求`shipping_info_source`；原“modified/2”验收要求撤销 | T4 |

### 2.2 与上一轮修复单的对照

| 状态 | 数量 | 对应 FIX |
|---|---:|---|
| 已通过 | 7 | FIX-01、FIX-02、FIX-03、FIX-04、FIX-07、FIX-10、FIX-11 |
| 部分通过 | 2 | FIX-08、FIX-12 |
| 未通过 | 3 | FIX-05、FIX-06、FIX-09 |

本次严格按完整验收标准计算，通过 7/12。部分通过项仍进入本轮收口范围，不按已完成处理。

## 三、公共验收原则

### 3.1 事件成立证据

每个用例同时检查：业务动作真实成立、事件数量、事件参数、禁止参数、事件之间的上下文关系以及 GA4 请求结果。任一项不满足，该用例不通过。

### 3.2 页面实例与当前页面

- “当前页面 URL”指动作发生时地址栏中的完整 URL，包含已经生效的搜索词、排序和筛选参数。
- “上一页面”指当前页面实例建立前的真实页面 URL。
- 新页面实例建立后，该实例内的主动事件使用同一份页面上下文。
- 直达页面没有可确认来源时省略 `page_referrer`。

### 3.3 跨端覆盖

页面或组件同时存在 PC 与 Mobile 形态时，两端分别执行，不使用一端通过代替另一端。公共逻辑通过后仍需验证各端真实入口已接入该逻辑。

## 四、T1 当前页面与来源语义纠正

### 4.1 目标结果

适用事件的`page_location`读取事件发生时地址栏中的完整当前URL；`page_referrer`只读取当前页面实例建立前的真实上一页面URL。筛选、排序、Drawer开关、页面重渲染和同页接口刷新不建立新页面实例，也不更新`page_referrer`。

### 4.2 场景契约

| 场景 | 预期`page_location` | 预期`page_referrer` | 页面实例 |
|---|---|---|---|
| Search筛选结果点击 | 点击时完整筛选URL | 当前Search实例建立前的上一页面，筛选后保持不变 | `select_item`沿用当前Search实例 |
| Collection筛选结果点击 | 点击时完整Collection筛选URL | 当前Collection实例建立前的上一页面，筛选后保持不变 | `select_item`沿用当前Collection实例 |
| 从`dior`正式提交`prada` | `prada`完整结果URL | 提交前完整`dior` Search URL | `prada`建立新实例；其主动事件共用新ID |
| Search排序Apply | 排序生效后的当前完整URL | 当前Search实例原`page_referrer` | 沿用当前Search实例 |
| 直达页面 | 当前完整URL | 省略 | 建立一个新实例 |

### 4.3 异常与禁止结果

- 不使用基础`/search`替代事件发生时的完整`page_location`。
- 不把当前动作URL写入`page_referrer`，也不使用前两跳或更早页面作为来源。
- 页面内部接口刷新失败时保留当前实例与来源，不回退到旧页面上下文。
- 无法确认来源时省略，不生成猜测值。

### 4.4 T1 自动断言

1. 建立页面实例时记录其真实上一页面URL。
2. 筛选或排序后捕获浏览器当前完整URL，执行动作并取得对应事件。
3. 断言`page_location`等于事件发生时当前完整URL，`page_referrer`仍等于该页面实例建立前的上一页面。
4. 新搜索断言新旧`page_instance_id`不同，且新实例`page_referrer`等于提交前完整Search URL；筛选、排序断言实例不变。
5. 连续执行至少3次跨页面跳转，确认来源没有回到前两跳。

## 五、T2 主动事件来源标识

### 5.1 字段枚举

| 字段 | 枚举值 | 含义 | 触发时机 | 适用事件 |
|---|---|---|---|---|
| `page_view_source` | `looply_custom` | Looply 主动页面事件 | 主动 `page_view` 成立时固定写入 | 仅主动 `page_view` |
| `view_search_results_source` | `looply_custom` | Looply 主动搜索结果终态事件 | 主动搜索结果形成唯一终态时固定写入 | 仅主动 `view_search_results` |

上述两个字段当前版本只有表中一个合法值。字段不适用时省略。

### 5.2 事件契约

| 事件类型 | 必须字段 | 禁止结果 |
|---|---|---|
| Looply 主动 `page_view` | `page_view_source=looply_custom` | 字段缺失或使用其他值 |
| GA 自动 `page_view` | 无 `page_view_source` | 补写 `looply_custom` |
| Looply 主动 `view_search_results` | `view_search_results_source=looply_custom` | 字段缺失或使用其他值 |
| 其他业务事件 | 不携带上述两个来源字段 | 跨事件继承来源字段 |

### 5.3 覆盖入口

- PC：Search、Collection、PDP。
- Mobile：Search、Favorites、PDP。
- Search 结果：手输回车、Search 按钮、历史词、联想词、热门词和轮播词；线上没有真实入口的场景记录为未执行。
- Search 排序、筛选和 Reset 后形成的主动结果终态。

### 5.4 T2 自动断言

1. 对每个入口按事件名和 `page_instance_id` 定位主动事件。
2. 断言主动事件来源字段存在且值完全相等。
3. 同一窗口检查其他事件，断言没有携带不适用来源字段。
4. 若同时观察到 GA 自动 `page_view`，断言其没有 `page_view_source`。

### 5.5 全链路验收

A01、A02不得继续只通过Web字段构造或公共函数测试判定。每个字段必须逐层保留证据：Web事件对象 → dataLayer事件 → GTM Data Layer Variable → GA4 Event Tag参数映射 → 实际发布的生产容器版本 → 真实`g/collect`请求。任一层缺字段或版本未发布，该事件仍判未通过；HTTP 204只用于证明请求到达，不替代字段和值验收。

## 六、T3 Wishlist 公共列表事件

### 6.1 目标结果

PC Favorites Drawer 与 Mobile Favorites 页面使用同一 Wishlist 列表标识和同一曝光阈值。曝光与点击能够按列表标识、商品和真实位置直接关联。

PC Favorites Drawer不创建新页面实例、不发送新`page_view`，曝光与点击沿用打开Drawer前当前页面的`page_instance_id`。Mobile Favorites页面按实际路由形成自己的页面实例。

### 6.2 列表常量

| 使用位置 | `placement_id` | `item_list_id` | `item_list_name` |
|---|---|---|---|
| PC Favorites Drawer | `favorites_wishlist` | `favorites_wishlist` | `favorites_wishlist` |
| Mobile Favorites 页面 | `favorites_wishlist` | `favorites_wishlist` | `favorites_wishlist` |

### 6.3 曝光契约

- 商品卡片至少 50% 进入可视区域并持续 1 秒后，发送非空 `view_item_list`。
- `items[]`只包含本次达到曝光阈值的真实商品。
- `items[].index`使用用户当前看到的真实列表位置，从 1 开始。
- 同一 `page_instance_id + placement_id + listing_public_code` 只计一次；进入新页面实例后可重新计数。
- 页面失焦或进入后台期间不累计 1 秒曝光时长。

### 6.4 点击契约

- PC 与 Mobile 点击 Wishlist 商品均发送 1 条 `select_item`。
- `select_item`使用 `favorites_wishlist` 三个列表字段。
- `items[].index`等于点击时真实位置，从 1 开始。
- 点击后进入 PDP 的 `view_item`不能替代 `select_item`。

### 6.5 T3 用例矩阵

| 端 | 场景 | 预期事件 | 关键断言 |
|---|---|---|---|
| PC | Drawer 打开，第 1 件达标 | `view_item_list` 1 条 | 非空、位置 1、列表标识一致 |
| PC | 点击第 1 件 | `select_item` 1 条 | 位置 1；随后可有 PDP `view_item` |
| PC | 滚动后非首件达标并点击 | 曝光与点击各 1 条 | 位置等于实际顺序 |
| Mobile | 页面首屏第 1 件达标 | `view_item_list` 1 条 | 非空、位置 1、列表标识一致 |
| Mobile | 点击第 1 件 | `select_item` 1 条 | `favorites_wishlist + index=1` |
| Mobile | 滚动后非首件达标并点击 | 曝光与点击各 1 条 | 位置等于实际顺序 |
| PC＋Mobile | 同一商品重复渲染 | 不新增曝光 | 同一页面实例内去重 |

### 6.6 异常处理

- Wishlist 为空时不发送 `view_item_list` 或 `select_item`。
- 商品数据未加载完成时不发送空事件；数据完成并达到曝光阈值后再发送。
- 列表请求失败时只记录页面错误状态，不生成商品曝光。

## 七、T4 配送方式版本

### 7.1 成立条件

`add_shipping_info`只在同一`checkout_id`首次形成有效`shipping_tier`，或之后有效tier发生变化时成立。地址新建、复用、切换或修改但最终有效tier未变化时不成立；页面显示变化但没有真实保存事实时也不成立。

### 7.2 版本规则

- `step_version`在同一`checkout_id`首次有效tier时为1。
- 之后只有有效`shipping_tier`变化才递增并再次发送。
- 同一tier事实重复回调或重试沿用原版本。
- 地址变化但tier未变化、页面重渲染、仅离焦、离开Checkout或返回首页不形成新版本。
- 本版本不要求`shipping_info_source`；已有该字段不得参与事件成立或幂等判断。

### 7.3 T4 用例矩阵

| 场景 | 预期新增事件数 | `step_version` |
|---|---:|---:|
| 同一checkout首次形成有效tier | 1 | 1 |
| 修改、切换或复用地址，最终tier未变化 | 0 | — |
| 修改信息后有效tier发生变化 | 1 | 当前版本 + 1 |
| 修改后仍无有效tier | 0 | — |
| 同一tier事实重复回调 | 0 | 沿用原值 |
| 重复渲染、离开或返回首页 | 0 | — |

### 7.4 隐私边界

事件只记录版本、配送档位、金额和商品信息；不向GA4发送收件人、电话、详细地址、邮编或其他地址明文。

## 八、自动回归要求

### 8.1 回归层级

| 层级 | 必须验证的结果 |
|---|---|
| 单元／组件 | 条件字段隔离、曝光阈值、事件去重、tier版本递增 |
| 页面集成 | PC Drawer与Mobile页面真实入口均调用公共规则，不能只测helper |
| 浏览器端到端 | 按本文件用例执行动作并捕获真实 `g/collect` |
| 生产冒烟 | 上线后使用生产 Measurement ID 复测核心正反例 |

### 8.2 通用自动断言

- 事件名称与预期一致。
- 事件数量与预期一致。
- 必须字段存在且值正确。
- 禁止字段不存在。
- 商品数组非空且商品、列表和位置一致。
- 页面实例的新建与沿用符合场景。
- `page_location`与事件发生时当前完整URL一致；`page_referrer`与当前页面实例建立前的真实上一页面一致。
- 同一事实重复回调不会产生重复事件。

### 8.3 必跑回归

除 T1–T4 用例外，必须继续执行已经通过的 FIX-01、02、03、04、07、10、11 核心用例，防止公共上下文或事件构造修改造成回归。

## 九、开发提测材料

开发提测时一次性提供以下内容：

1. 根因说明：每个任务原实现为何产生当前结果，本次改动覆盖哪些公共场景。
2. 影响范围：PC、Mobile、页面、公共组件和事件清单。
3. 自动测试：测试名称、执行时间、通过数、失败数和失败详情。
4. 请求证据：每个任务至少一条正例和一条反例，列出事件名、事件数量和关键字段；敏感信息脱敏。
5. 回归结论：FIX-01 至 FIX-12 全表状态，不只报告本次新增用例。
6. 上线信息：构建版本、上线时间和生产复测窗口。

未提供上述材料时，状态保持“开发自测未完成”，不进入产品正式复验。

## 十、发布阻断标准

以下任一情况出现即阻断发布：

- 主动来源字段缺失或被带入不适用事件。
- `page_location`不是事件发生时当前完整URL，或`page_referrer`被写成当前动作URL、基础路由、前两跳及更早页面。
- PC 或 Mobile Wishlist 曝光／点击任一入口漏发。
- `view_item_list`商品为空或商品位置错误。
- `add_shipping_info`首次有效tier未发送version=1、有效tier变化后版本未递增，或地址变化但tier未变化时重复发送。
- 已通过的 FIX-01、02、03、04、07、10、11 出现回归。
- 只有 HTTP 204，没有动作、数量、字段和上下文证据。

## 十一、依赖与风险

| 依赖／风险 | 当前要求 |
|---|---|
| Web 公共页面上下文 | 必须提供当前页面实例、当前完整 URL 与实例建立前真实来源，供主动事件统一读取 |
| PC／Mobile Wishlist | 两端必须使用同一业务列表契约；端形态差异不能改变事件成立条件和列表标识 |
| Checkout 配送信息 | 必须以首次有效tier及后续tier变化驱动事件；页面或地址变化不能单独替代配送方式事实 |
| GTM／GA4 | 生产实际容器权限仍是完整 Tag／Trigger／Variable 验收依赖；缺权限时只能完成请求层验收 |
| 历史数据 | 新来源字段和修复后的事件不回填历史，验收只使用上线后的新事件 |

## 十二、验收通过定义

本轮只有同时满足以下条件才算收口：

1. T1–T4 全部用例通过，PC 与 Mobile 覆盖完整。
2. FIX-01 至 FIX-12 回归无新增失败。
3. 开发提测材料齐全。
4. 生产真实动作、事件数量、字段、上下文和请求结果一致。
5. 复验记录明确区分已通过、未执行和受权限阻塞的层级。

## 十三、输入源与权威关系

| 输入源 | 用途 | 权威关系 |
|---|---|---|
| 《looply-GA4数据分析-PRD-v1.8》 | GA4事件语义、字段与验收基线 | 当前GA4正式需求权威文档 |
| 《looply-数据采集与埋点产品需求-v1.9》 | 一方事件与跨平台业务事实基线 | `add_shipping_info`及Favorites页面实例规则的跨平台权威文档 |
| 《looply-GA4线上验收问题与开发修复单-v1.2-20260826》 | 12 个原始修复点和复测标准 | 历史修复基线 |
| 《looply-GA4线上修复复验-20260827》 | 上一轮真实生产复验状态 | 验收证据 |
| 《looply-GA4线上修复复验-20260831》 | 本轮剩余问题与真实复现 | 当前问题证据 |
| 本文件 | 剩余问题的集中执行与提测入口 | 只记录问题、执行动作和复验要求；与上述正式PRD冲突时必须先修正文档，不交由开发选边 |
