# Looply GA4 线上验收问题与开发修复单

> 版本：v1.2  
> 日期：2026-08-26  
> 状态：待开发修复后复验  
> 生产站：`https://www.looply.com/`  
> GA4：Property `531542304`，Measurement ID `G-Z2EKP8QGT7`  
> 线上实际加载 GTM：`GTM-PD3ZGT7L`  
> 目标读者：Web、GTM、GA4、测试与数据负责人  
> 替代版本：v1.1；开发仅使用本文件  
> 需求基线：《looply-GA4数据分析-PRD-v1.5》《looply-GA4五事件新增与修改-PRD-v1.1》《looply-一方埋点公共实施规则-v1.7》《Looply-v1.4-详细埋点需求定稿-v1.2》

## 一、开发修复点总览

| 编号 | 事件／范围 | 已确认问题 | 修改结果 |
|---|---|---|---|
| FIX-01 | `search` | 点击联想词后，后续非联想入口继续携带旧`suggestion_position` | 每次正式搜索提交使用本次动作独立上下文；仅`suggestion_select`可携带该字段 |
| FIX-02 | Search页面实例 | 同一结果页提交新搜索词后，结果、曝光继续复用旧`page_instance_id`，主动`page_view`缺失 | 新搜索上下文生成新页面实例；相关事件读取同一个新ID |
| FIX-03 | 动态筛选上下文（GA4＋一方埋点） | Search／Collection筛选由后台动态配置；GA4运行态缺最终筛选参数，一方现有动作事件不能稳定还原最终生效组合 | 前端统一生成基于后台稳定Code的已Apply筛选事实；GA4与一方适配器分别按各自格式发送 |
| FIX-04 | 主动`page_view` | Mobile PDP返回首页出现两条主动事件；Search、Wishlist及部分PDP存在主动事件漏发或时序异常 | 每个真实页面实例恰好一条主动事件；保留当前允许的GA自动事件 |
| FIX-05 | 主动`page_view`来源 | 主动与GA自动事件同名，现有事件无法长期稳定地区分来源 | 仅主动事件显式增加`page_view_source=looply_custom` |
| FIX-06 | 主动`view_search_results`来源 | 主动与GA自动事件同名，开启自动网站搜索后无法直接按事件名区分 | 仅主动事件显式增加`view_search_results_source=looply_custom` |
| FIX-07 | `view_item_list` | Search排序Apply时出现一条不含商品的空曝光事件 | 无商品达到曝光条件时不发送；只发送本次真实达标商品 |
| FIX-08 | `select_item` | 多数非PDP入口缺商品位置；Wishlist曝光与点击列表命名不一致 | 点击携带真实列表位置；同一列表曝光与点击使用一致标识 |
| FIX-09 | 页面来源 | 部分`select_item`和排序结果事件的`page_referrer`指向旧页面或前两跳 | 读取动作发生时真实上一页面，不复用过期页面上下文 |
| FIX-10 | `event_id` | 收藏成功后的`view_item_list`继承`wishlist_operation_id` | 清理共享参数；不同事件不得跨类型继承业务操作ID |
| FIX-11 | `view_item` | 已测商详事件缺当前PDP的`page_instance_id` | 从公共页面上下文读取当前PDP实例ID；本项不要求`item_brand` |
| FIX-12 | `add_shipping_info` | 未修改地址离开Checkout时重复发送；修改已完整地址后反而不发送新版本 | 只在新建／复用／修改后的有效配送信息形成新保存事实时发送并递增版本 |
| BLOCK-01 | GTM验收权限 | 线上加载`GTM-PD3ZGT7L`，当前账号只能访问`GTM-T3849GJP` | 确认生产唯一容器并提供线上容器至少只读权限，完成Tag／Trigger／Variable闭环验收 |

## 二、逐项修改与复测标准

### FIX-01 清理搜索入口间的联想位置状态

**运行证据**

- PC与Mobile均复现：先点击一次联想词后，再执行回车、Search按钮、历史词、热门词或轮播词，后续`search`仍携带`suggestion_position=1`。
- 新会话先执行手输或按钮时没有该字段，证明问题来自联想状态未清理。

**开发修改目标**

- 每次正式搜索提交按本次动作重新组装参数。
- `suggestion_position`仅在`trigger_type=suggestion_select`时读取本次被点击建议的真实位置。
- 其他入口省略该字段，不使用上一次搜索的残留值。

**复测标准**

- PC和Mobile均按“联想词→回车→按钮→历史词→热门词→轮播词”连续执行。
- 只有联想词事件携带从1开始的位置，其余事件均不携带。

### FIX-02 修复Search新上下文的页面实例生命周期

**运行证据**

- 同一Search结果页提交新搜索词后，`view_search_results`和`view_item_list`继续使用首个搜索结果页的`page_instance_id`。
- 同一次正式新搜索只观察到GA自动`page_view`，未观察到带新页面实例的Looply主动`page_view`。

**开发修改目标**

- 已在结果页正式提交新搜索词并形成新页面上下文时，生成新的`page_instance_id`。
- 新上下文中的主动`page_view`、`view_search_results`、`view_item_list`和`select_item`读取同一个新ID。
- 仅Apply筛选、Apply排序或Reset时沿用当前页面实例，不生成新ID。

**复测标准**

- 连续三次正式新搜索产生三个不同页面实例；每次搜索链内部ID一致。
- 排序、筛选和Reset不改变当前页面实例。

### FIX-03 统一Search／Collection动态筛选上下文

**运行证据**

- PC选择Condition=`Excellent`并Apply、Mobile选择`Excellent`＋`Very Good`并Apply后，URL已包含实际筛选条件，但主动`view_search_results`完全缺少`filter_ids`。
- 生产Search实际URL已出现后台动态筛选维度及选项Code，例如`filter_Category=CA5GYR4GDRH2K`、`filter_Series=SEB7TNVEXWVF7`；现有固定维度清单不能覆盖后续后台新增维度。
- 当前一方埋点已记录筛选项`select`、`reset`和`apply`动作，但`select`只记录单个选项稳定值，`apply`只记录目标页面／集合，无法区分“选中后取消”与“最终Apply生效”，也无法稳定还原完整的维度与选项组合。

**公共修改目标**

- Search与Collection共用一份标准化“最终已Apply筛选事实”，由后台配置中的稳定`dimension_code`和`option_code`生成；前端不得维护固定筛选维度白名单，也不得用展示名称作为ID。
- 只记录本次Apply后真正生效的组合；选择后取消、关闭面板或未Apply的值不进入最终筛选事实。
- 多选项去重并稳定排序；Reset后结果为空。价格区间继续单独处理，本期不并入离散筛选集合。
- 如果后台没有提供稳定的维度Code或选项Code，前端省略该项并记录错误，不得根据展示文案猜测或临时造Code。

**GA4适配**

- `view_search_results`以及现有需求中需要搜索／集合筛选上下文的`view_item_list`等事件，从上述公共事实生成`filter_ids`。
- GA4按`dimension_code:option_code`序列化，去重、稳定排序后用逗号连接。例如上述URL发送：`category:CA5GYR4GDRH2K,series:SEB7TNVEXWVF7`。
- 不再只按旧固定清单识别`brand／condition／category／color／size／material`；后台新增可筛选维度后无需再次修改前端枚举。

**一方埋点适配**

- 保留现有筛选`select／reset／apply`交互事件，同时在Apply成功及对应结果上下文中发送结构化的最终筛选集合，每项至少包含`dimension_code`和`option_code`。
- 一方数据使用`filter_ids[]`数组，每项为`dimension_code:option_code`，不直接复用GA4的逗号字符串；GA4与一方数据必须来自同一份公共筛选事实。
- 一方字段规则已同步到《Looply-v1.4-详细埋点需求定稿-v1.2》和《Looply一方埋点公共实施规则v1.7》。

**数据侧依赖**

- 后台／数据平台维护可按版本追溯的`dimension_code／option_code → 展示名称`映射；事件保留稳定Code，报表展示阶段再关联名称。

**复测标准**

- PC与Mobile分别覆盖Search、Collection的单选、多选、动态`Series`维度、Reset、无筛选、选择后取消六类场景。
- 页面最终状态、URL、公共筛选事实、GA4 `filter_ids`及一方`filter_ids[]`一致；两种适配格式不同，但维度Code和选项Code逐项相同。
- Reset后GA4省略`filter_ids`、一方最终筛选集合为空；不得残留上一次值。

### FIX-04 主动`page_view`每个页面实例恰好一次

**运行证据**

- Mobile从PDP返回首页时，18ms内发送两条Looply主动`page_view`，两个`page_instance_id`不同；随后另有一条GA自动事件。
- Search新搜索、Wishlist和部分PDP路由只观察到GA自动事件，但后续业务事件已经取得新页面实例。

**开发修改目标**

- 公共页面上下文是主动`page_view`唯一生产点。
- 首次打开、刷新、有效路由进入或前进／后退重新进入时，每个真实页面实例只发送一条主动事件。
- 组件挂载、重复监听、接口回调和同一实例重渲染不生成第二条主动事件。
- 保留当前确认的GA自动`page_view`；本批不关闭自动页面事件。

**复测标准**

- PC与Mobile覆盖首页、Search、Collection、PDP、Wishlist、Cart和Checkout。
- 每个页面实例主动事件数为1；允许另有GA自动事件，但不得出现两条主动事件。

### FIX-05 为主动`page_view`增加明确来源参数

**当前问题与修改原因**

- Looply主动事件与GA自动历史路由事件的事件名均为`page_view`，GA4默认汇总会把两类事件合并计数。
- 仅依赖部分主动事件当前已有的其他业务字段进行推断，无法形成长期稳定、可统一维护的来源口径。
- 因此需要由主动上报逻辑显式声明来源，避免后续报表、探索和数据核对只能靠间接条件猜测。

**开发修改目标**

- 仅Looply主动`page_view`增加事件参数`page_view_source=looply_custom`。
- GA自动`page_view`不补该参数；其他GA4事件也不携带该参数。
- 参数名和值使用上述固定小写常量，不随页面、端或触发入口变化。
- 本项不要求关闭GA自动`page_view`，也不改变当前主动＋自动双来源设计。

**GA4配置配合**

- 开发上线并取得真实请求证据后，在GA4管理后台注册事件范围自定义维度：维度名称`Page View Source`、事件参数`page_view_source`、范围`事件`。
- 注册用于GA4标准探索和报表按来源拆分；BigQuery原始事件可直接读取参数，不依赖该注册。
- 自定义维度只对注册后新处理的数据生效，不回填历史事件。

**复测标准**

- PC与Mobile各选择至少一个SPA路由，确认同次路由的Looply主动`page_view`携带`page_view_source=looply_custom`。
- 同次路由的GA自动`page_view`不携带`page_view_source`；其他业务事件也不携带。
- `dataLayer`、GTM变量／Tag、`g/collect`请求和GA4 DebugView四层的参数值一致。
- GA4自定义维度开始处理新数据后，可按`Page View Source=looply_custom`识别主动事件；仅对上线生效时间之后且已通过复测的新数据，才可将参数为空的同名事件按GA自动来源统计。
- 上线前的历史空值不可反推为GA自动事件，也不可据此重算主动／自动历史数量。

### FIX-06 为主动`view_search_results`增加明确来源参数

**修改原因**

- Looply主动事件与GA自动网站搜索事件的事件名均为`view_search_results`；自动网站搜索开启后，GA4默认事件总数会合并两类来源。
- 增加稳定来源参数后，可以在限定时间窗口同时采集两类事件，并对比URL识别与真实搜索结果请求终态之间的数量及场景差异。

**开发修改目标**

- 仅Looply主动`view_search_results`增加事件参数`view_search_results_source=looply_custom`。
- 参数名和值使用上述固定小写常量，不随PC／Mobile、搜索入口、结果状态或页面变化。
- GA自动网站搜索事件不携带该参数；其他GA4事件也不携带该参数。
- 本项只增加来源标识，不改变主动`view_search_results`原有成立条件、次数和业务参数。

**GA4配置配合**

- 开发上线并取得真实请求证据后，在GA4管理后台注册事件范围自定义维度：维度名称`View Search Results Source`、事件参数`view_search_results_source`、范围`事件`。
- 自定义维度开始处理新数据后，由GA4管理员记录实验开始时间，临时开启增强型衡量中的“网站搜索”；建议对比窗口为24～48小时。
- 对比结束后关闭GA自动“网站搜索”，长期保留Looply主动`view_search_results`。
- 自定义维度与本次来源参数均不回填历史数据；实验开始时间之前的参数空值不可用于判断事件来源。

**复测与对比标准**

- PC与Mobile覆盖手输回车、Search按钮、历史词、联想词、热门词和轮播词六种入口；没有真实入口的场景记录为“未执行”。
- Looply主动事件携带`view_search_results_source=looply_custom`，并继续按需求携带结果终态和搜索上下文；GA自动事件不携带该参数。
- `dataLayer`、线上GTM、`g/collect`和GA4 DebugView中的主动事件参数值一致。
- 仅统计实验开始时间之后的新数据：`View Search Results Source=looply_custom`为主动事件；参数为空为GA自动事件。两类事件分别统计，不直接使用合并后的`view_search_results`总数。
- 对比结果按入口、`search_term`、页面URL、终端和结果状态拆分；GA自动事件没有的业务参数标记为“不提供”，不得补造或按默认值归类。

### FIX-07 禁止空`view_item_list`

**运行证据**

- Search排序Apply后，在正常结果更新之外多出一条没有商品参数的空`view_item_list`。

**开发修改目标**

- 只有至少一件商品满足50%可视且持续1秒时才形成曝光事件。
- 每条事件只携带本次实际达到阈值的商品；结果刷新、空数组回调或排序状态更新本身不发送。

**复测标准**

- 排序、筛选和Reset完成但商品尚未满足曝光阈值时，事件数为0。
- 商品达标后按真实商品和位置发送，不出现空`items[]`。

### FIX-08 补齐点击位置并统一Wishlist列表标识

**运行证据**

- PC／Mobile的首页For You、New Arrivals、Collection、Search、搜索无结果推荐和Wishlist点击已发送`select_item`，但缺少商品位置。
- Wishlist曝光使用`favorites_wishlist`，点击使用`item_list_id=favorites`、`item_list_name=wishlist`。

**开发修改目标**

- 能取得业务列表位置时，`select_item.items[].index`使用筛选、排序和插入完成后的真实位置，从1开始。
- Wishlist的曝光和点击使用同一稳定列表／展示位标识，统一为现有需求常量`favorites_wishlist`；不得靠展示文案关联。

**复测标准**

- 上述入口分别点击第1件和非首件商品，位置与页面实际顺序一致。
- Wishlist曝光与点击可直接按稳定列表标识关联。

### FIX-09 修复过期`page_referrer`

**运行证据**

- 首页For You点击的`page_referrer`曾指向Checkout；New Arrivals点击曾指向上一商详。
- 部分Search排序结果事件指向前两跳页面，而同一动作的GA自动页面事件来源正确。

**开发修改目标**

- 主动事件从当前页面实例上下文读取真实上一页面。
- 新页面实例建立后同步更新来源；不得继续复用两次以前的路由上下文。

**复测标准**

- 首页、列表、Search、PDP、Cart、Checkout连续跳转后，业务事件来源均等于动作发生前的真实页面。
- 直达页面允许来源为空，不猜测、不补造。

### FIX-10 清理`event_id`跨事件污染

**运行证据**

- PC与Mobile多次复现：`add_to_wishlist`成功后，后续同批或下一批`view_item_list`的GA参数`evnid`继承刚才的`wishlist_operation_id`。
- 首页、搜索无结果推荐、PDP推荐和Recently Viewed均出现过该问题。

**开发修改目标**

- 每次组装GA4事件使用独立参数对象，发送完成后不在共享上下文保留业务操作ID。
- `view_search_results.event_id`只用于该结果终态及其重试；`view_item_list`不得继承`wishlist_operation_id`或其他事件ID。

**复测标准**

- 收藏后继续滚动多个列表，后续曝光均不携带收藏操作ID。
- 同一`view_search_results`重试保持自身ID；新的结果终态生成新ID。

### FIX-11 `view_item`关联当前商详页面实例

**运行证据**

- 从Search、首页、New Arrivals、Collection、推荐和Recently Viewed进入商详后，`view_item`均已成功发送，但未携带当前PDP的`page_instance_id`。

**开发修改目标**

- `view_item`从Web公共页面上下文读取当前PDP的`page_instance_id`，用于同一商详实例关联和去重。
- 本项不增加`item_brand`要求；现有商品ID、名称、价格和币种逻辑保持不变。

**复测标准**

- 每个入口的`select_item`、PDP主动`page_view`和`view_item`能够按当前页面实例正确关联。
- 刷新或重新进入PDP生成新页面实例；同一实例重复渲染不重复发送`view_item`。

### FIX-12 修复配送信息事件的保存事实与版本

**运行证据**

- Mobile从Checkout返回首页、未再次编辑地址时又发送`add_shipping_info`，且`page_location`已经是首页。
- PC修改已完整地址并离焦后没有发送新的`add_shipping_info`，也没有形成新的`step_version`。

**开发修改目标**

- 只有新填写、复用或修改配送信息后，地址及配送方式形成新的有效保存事实时发送。
- 同一Checkout中每个新保存版本使用递增且稳定的`step_version`。
- 离页、返回首页、仅重新渲染或没有信息变化时不发送。

**复测标准**

- 首次有效保存发送1次；修改并再次有效保存发送1次新版本。
- 未修改离开Checkout、返回首页或重复渲染均为0次。

### BLOCK-01 统一线上GTM容器身份与验收权限

**运行证据**

- `looply.com`实际加载`https://www.googletagmanager.com/gtm.js?id=GTM-PD3ZGT7L`。
- 当前账号可访问的`Looply-online`容器是`GTM-T3849GJP`，该工作区显示“最近无数据”；访问`GTM-PD3ZGT7L`会退回GTM首页。

**开发／管理员处理目标**

- 确认生产唯一正确容器。
- 若`GTM-PD3ZGT7L`正确，为验收账号提供至少只读权限，并说明`GTM-T3849GJP`的用途或废弃状态。
- 若`GTM-T3849GJP`才是计划生产容器，先解释并修正线上仍加载另一容器的问题，再重新验收。

**闭环标准**

- 从线上实际容器启动Preview，逐事件取得`Tags Fired / Tags Not Fired`、触发次数、变量值和GA4 Event Tag证据。
