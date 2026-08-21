# Looply Web 全局搜索 PRD

> 版本：v0.4  
> V1 范围：PC Web、Mobile Web  
> 参考材料：`looply-全局搜索-核心逻辑-Checklist-v0.1.md`  
> 当前正式 UI：[Looply 1.1](https://www.figma.com/design/sAOLkw0gIl1bwQRYCDqKuW/Looply-1.1)
> UI 评审说明：`prototypes/search/looply-global-search-ui-review-v0.1.html`  
> 开发评审版：`prototypes/search/looply-global-search-dev-review-v0.1.html`  
> 统一逻辑 Demo：`prototypes/search/looply-global-search-web-demo-v0.1.html`  
> PC Web 原型：`prototypes/search/looply-global-search-pc-web-demo-v0.1.html`  
> Mobile Web 原型：`prototypes/search/looply-global-search-mobile-web-demo-v0.1.html`

> 本 PRD 是 Web V1 产品逻辑与测试基线；展示与交互以上述当前正式 UI 源稿为准。Checklist 保留决策过程和待确认项，Demo 仅用于逻辑和状态演示。

## 1. 产品范围与共用原则

### 1.1 V1 范围

- 全局搜索是 Web 端公共能力，由 Home、Shop、Collection 和 Favorites 接入。
- V1 覆盖 PC Web 和 Mobile Web；App 搜索不属于本次范围。
- PC Web 与 Mobile Web 共用搜索业务逻辑、数据来源和服务能力，分别定义页面布局与终端交互。

### 1.2 登录状态与数据归属

- 搜索不要求登录。游客与登录用户使用相同的搜索执行、召回、结果处理、Popular content、排序和筛选规则。
- 登录状态只影响搜索相关用户数据的归属：Recent searches 和 Search event 记录到当前 `anonymous_id` 或 `user_id`；Recent searches 的登录合并、跨设备同步和主体切换按第 4.5 节执行。

### 1.3 搜推能力边界

- 本 PRD 定义用户可见的功能、交互、市场和 locale 等业务约束。
- 可检索字段、业务对象、输入预处理、分词、纠错、改写、同义词、联想匹配、召回及相关性由搜推方案定义。
- 页面按搜推服务返回的结果及顺序展示。

### 1.4 多语言内容归属

- Web 搜索的 locale 范围继承当前 Web 全局 locale 范围。
- 本模块的静态 UI 文案统一接入 Web i18n 能力。
- 用户输入的关键词、Recent searches 中的普通关键词及 Popular searches 不自动翻译；Popular searches 的数据维度按第 5.2 节执行。
- 品牌、品类和商品名称不由搜索模块单独维护翻译；页面通过业务对象 ID 读取品牌域、品类域和商品域在当前 locale 下的名称，并复用各业务域统一的缺失翻译兜底。

## 2. 搜索入口与搜索发现

### 2.1 搜索入口共用规则

- Home、Shop、Collection 和 Favorites 复用同一 Sug、有效输入提交、搜索结果、Recent searches 和结果异常处理能力；入口打开方式与空输入初始状态按来源页分别执行。退出未提交的搜索状态时恢复来源页及原状态；结果页返回复用 Web 全局导航规则。
- PC Web 通过 Header 搜索图标进入搜索态；Header 切换为搜索输入框、`Search` 和 `Cancel`，下方展示搜索发现内容。
- Mobile Web 的 Home、Shop 和 Favorites 使用入口型搜索框，轮播词按第 5 章执行。点击入口后进入全屏搜索发现页；有效轮播词作为当前 placeholder，否则使用 `Search by brand or item...`。Favorites 入口搜索全站商品，不限定当前 Wishlist 或 Recently Viewed。
- Home 右侧同时展示搜索图标：存在有效轮播词时直接提交该词；展示固定 placeholder 时进入全屏搜索页，不发起搜索或展示 Toast。
- Home、Shop 和 Favorites 有轮播词缓存时首屏直接展示；无缓存加载中、空数据、失败或词条不可用时展示固定 placeholder。加载成功后切换为第一条有效词并开始轮播。
- Mobile Web 点击 Collection Header 的搜索入口后，当前 Header 切换为内联搜索态，自动聚焦并唤起键盘，使用固定 placeholder `Search by brand or item...`。空输入时保留原商品列表、筛选、排序和滚动位置，不展示搜索发现内容。

### 2.2 搜索发现页面形态

- PC Web 点击 Header 搜索入口后，Header 切换为搜索态，并在其下方展示搜索发现层；未输入时按单列纵向顺序展示 Recent searches 和 Popular searches。
- PC Web 搜索层固定吸附在全局导航栏下方；搜索层内容超出可视高度时，输入框保持可见，Recent searches 和 Popular searches 在搜索层内部滚动。
- Mobile Web 的 Home、Shop 和 Favorites 使用全屏搜索发现页；未输入时按顺序展示 Recent searches、Popular searches、Popular brands 和 Popular categories。
- 当前没有 Recent searches 时隐藏整个模块，后续内容自动上移；PC Web 中 Popular searches 直接承接搜索框下方的内容位置。

### 2.3 搜索输入状态

- PC Web 输入框使用固定 placeholder `Search by brand or item`；Mobile Web 全屏搜索页的初始 placeholder 按第 2.1 节的入口规则执行，Collection 内联搜索使用 `Search by brand or item...`。各入口的输入框初始保持空值。
- 用户开始输入有效真实内容后，隐藏搜索发现内容，并以当前输入请求 Sug；输入变化时只展示与最新输入对应的 Sug 状态和结果。
- 用户清空输入后隐藏 Sug，并按来源页恢复第 2.1 节定义的空输入状态；Collection 继续保留原页内容和位置，不转为搜索发现页。迟到的 Sug 结果不得覆盖当前状态。
- Mobile Web 全屏搜索页和 Collection 内联搜索态在输入非空时展示清除按钮；点击后清空输入并恢复对应空输入状态，焦点保留在输入框。
- PC Web 搜索层、Mobile Web 全屏搜索页和 Collection 内联搜索先对输入执行 Unicode 规范化、去除首尾空格并将连续空格归一。处理后的内容必须至少包含一个 Unicode 字母或数字；为空、纯空格、纯标点或仅包含其他非字母数字字符时，不请求 Sug、不发起搜索，展示轻量 Toast `Please enter a brand or item.`，并保留当前搜索状态。包含字母或数字的词可以同时包含标点，例如 `A.P.C.`、`M&M`。该 Toast 不用于 Mobile Web 首页固定 placeholder 状态。

### 2.4 打开与退出

- 打开 PC Web 搜索层、Mobile Web 全屏搜索页或 Collection 内联搜索态后，自动聚焦搜索输入框；Mobile Web 同时唤起系统键盘。
- Mobile Web 中，历史和 Popular content 保留为键盘上方的可滚动内容；用户收起键盘后可完整浏览。
- PC Web 支持按键盘 `Enter` 或点击 Header 中的 `Search` 提交当前输入。
- Mobile Web 全屏搜索页顶部由返回按钮、搜索框和搜索图标组成；Collection 内联搜索的搜索图标放在输入框内右侧。两处点击搜索图标或系统键盘 `Search` 时使用相同提交规则：有有效输入时提交当前输入，无有效输入时按第 2.3 节展示 Toast。
- PC Web 点击 Header 中的 `Cancel` 或按 `Esc` 退出搜索态。
- Mobile Web 点击顶部返回按钮或触发浏览器返回时，关闭全屏搜索页并恢复进入搜索前的页面及状态。
- Collection 内联搜索态点击返回时，恢复 Collection 原 Header，并保留原商品列表、筛选、排序和滚动位置。
- 退出时清空未提交输入，不弹出确认；下次打开时按来源页进入第 2.1 节定义的初始状态。

### 2.5 搜索发现模块状态

- Recent searches 与 Popular searches 分别独立加载和降级；Popular brands 与 Popular categories 使用 UI 1.1 定义的固定内容，不发起热门数据请求。
- 存在可用缓存时立即展示缓存内容；后台刷新失败时保留已展示的缓存内容。
- 没有可用缓存且请求尚未完成时，对应动态模块展示符合内容形态的轻量骨架屏：搜索词模块使用词条骨架。
- 没有可用缓存且服务返回空数据或请求失败时，隐藏对应模块，后续模块自动上移。
- Recent searches 缓存按游客域或登录账号隔离；Popular searches 缓存按 `market_id + locale` 隔离。登录、退出或切换账号后切换 Recent searches 缓存；切换市场或 locale 后重新读取 Popular searches。
- 单个或多个搜索发现模块不可用时，搜索框、手动输入、输入联想及其他成功模块继续正常使用。
- 只有搜索页公共框架、关键公共依赖或页面全部内容不可用时，才展示整页错误状态。

## 3. 输入联想

- Sug 候选来源、数量、匹配和相关性排序由现有搜推方案维护。Web 按服务返回顺序展示单列候选，不分组或重排。

| 状态 | 触发条件 | 用户可见处理 |
|---|---|---|
| 请求中 | 当前输入对应的 Sug 尚未返回 | 保留当前输入，隐藏搜索发现内容；联想区域展示 3 行轻量骨架。用户仍可直接提交当前输入。 |
| 正常返回 | Sug 返回一个或多个结果 | 不展示分组标题，按服务返回的相关性顺序从上到下展示一列联想结果。 |
| 空结果 | Sug 成功返回但没有可展示结果 | 保留当前输入，静默收起联想区域，搜索发现内容继续隐藏；用户仍可直接提交当前输入。 |
| 请求失败 | Sug 请求失败或服务不可用 | 保留当前输入，静默收起联想区域，搜索发现内容继续隐藏；不展示错误或重试入口，用户可继续输入或直接提交当前输入。 |

- 用户点击 Sug 后，提交对应搜索。
- Sug 视觉遵循当前正式 UI：候选以纯文本单列展示；Mobile Web 候选行不展示左侧图标或右侧 `Search`，PC Web 候选行右侧展示箭头。
- Collection 有效输入后在当前页面 Header 下展示同一 Sug；提交当前输入或 Sug 后进入全局搜索结果页。

## 4. Recent searches 与 Search event

### 4.1 展示与交互

- 按最近搜索时间倒序读取当前身份下的记录。
- 点击记录时按其搜索类型、完整文案和目标 ID 重新发起搜索。
- PC Web 默认完整展示 2 行；记录超出 2 行时，在第二行末尾展示 `More`，点击后在当前搜索发现层内展开全部记录并在末尾切换为 `Less`；点击 `Less` 后恢复 2 行。
- Mobile Web 默认完整展示 2 行；记录超出 2 行时，在第二行末尾展示向下箭头，点击后展开全部记录并在全部词条末尾切换为向上箭头；点击向上箭头后恢复 2 行。
- 各端实际展示数量由词条宽度和当前语言决定。单个词条使用单行展示，最大宽度不超过当前内容区可用宽度的 75%；超出时显示省略号，点击时使用完整词条搜索。
- V1 的 Recent searches 只提供查看、展开或收起及点击搜索，不提供单条删除或清空全部入口。

### 4.2 记录生成

以下行为真正发起搜索后，生成或更新 Recent searches：

- 手动输入并提交关键词。
- 点击 Mobile Web 首页搜索图标并成功提交当前有效轮播词；固定 placeholder 状态下进入全屏搜索页不生成记录。
- 点击输入联想。
- 点击 Popular searches 或 Popular brands。
- 点击已有 Recent searches；对应记录更新时间并移动到第一位。
- 点击搜推返回的纠错词或推荐词。

搜索结果为 0 或搜索请求失败时仍记录。仅打开搜索、输入但未提交或直接退出时不记录。

### 4.3 记录内容

| 内容 | 说明 |
|---|---|
| 搜索类型 | `keyword`、`brand`、`category` |
| 原始展示文案 | 用户实际输入或点击入口时的完整文案 |
| 规范化文案 | 用于去重，不替换用户可见文案 |
| 目标 ID | 品牌和品类保存对应 ID；关键词为空 |
| 搜索语言 | 本次搜索使用的语言 |
| 最近搜索时间 | 用于倒序、置顶及超限淘汰 |

### 4.4 去重与数量

- 搜索文案进行 Unicode 规范化、首尾及连续空白归一，并对有大小写区分的文字忽略大小写。
- 不翻译搜索词，不进行跨语言或语义合并；规范化后完全相同才视为同一文案。
- 去重标识由搜索类型、规范化文案和品牌/品类 ID 共同确定。
- 重复搜索更新最近搜索时间并移动到第一位，不新增记录。
- 游客域最多保留 20 条；登录账号全局最多保留 20 条。

### 4.5 存储与同步

- 未登录记录保存在当前浏览器本地，并归属于当前 `anonymous_id`。
- 用户登录、退出、切换账号或 `anonymous_id` 变化后，立即切换至当前主体的 Recent searches 数据源；切换前发出的请求只可写回原主体缓存，页面仅展示当前主体的记录。
- 用户登录成功时，将登录前当前 `anonymous_id` 下的 Recent searches 复制并合并到当前 `user_id`；匿名侧原记录保留，登录后只展示账号合并结果。
- 登录合并沿用第 4.4 节的去重标识，相同记录保留较新的最近搜索时间；合并后按最近搜索时间倒序保留最新 20 条。
- 登录用户提交搜索后，先在当前设备本地更新当前 `user_id` 的记录，再异步同步至账号云端；账号云端记录是同一账号跨设备读取和合并的最终数据源。
- 云端同步失败时，当前设备仍展示已经写入本地的记录；登录复制及后续搜索产生的待同步记录均绑定当前 `user_id`，不得在游客状态或其他账号下展示。
- 网络恢复、Web 页面重新可见或同一账号再次登录时重试同步；补同步沿用第 4.4 节的去重规则，并以最近搜索时间合并。
- 多设备合并后仍执行第 4.4 节的账号数量上限，各设备本地缓存以云端合并结果为准。

### 4.6 Search event

每次实际提交搜索时单独生成 Search event；该事件与 Recent searches 分别记录，不受其数量上限、去重或覆盖影响。

- 搜索结果为 0 或搜索请求失败时仍生成 Search event，并记录本次结果状态。
- 登录用户的 Search event 同步失败时进入绑定原 `user_id` 的待同步队列；网络恢复、页面重新可见或同一账号再次登录时重试，不转为游客或其他账号的事件。
- 刷新结果页、打开分享链接及浏览器前进或后退触发的状态恢复不属于新的搜索提交，不重复生成 Recent searches 或 Search event。
- 点击 Popular categories 后仅打开该品类配置的链接，不生成 Recent searches 或 Search event。

## 5. Popular content

### 5.1 展示与交互

**Popular searches**

- 按服务返回顺序展示，不在浏览器端重新排序。
- Mobile Web 的 Home、Shop、Favorites 入口轮播词与搜索发现页 Popular searches 共用同一份最终列表和顺序。
- PC Web 完整展示服务返回的前 10 条；服务返回不足 10 条时展示全部返回内容，不限制行数，不提供展开入口。
- Mobile Web 最多完整展示 3 行，实际展示数量由词条宽度和当前语言决定；放不进第三行的词条不展示，不提供 `See all`。
- 单个词条使用单行展示，最大宽度不超过当前内容区可用宽度的 75%；超出时显示省略号，点击时使用完整词条搜索。

**Popular Designers（业务对象：Popular brands）**

- 仅在 Mobile Web 搜索发现页展示。
- 固定品牌清单、展示顺序和品牌图片由 UI 1.1 提供，不根据用户行为、市场或终端动态生成或排序。
- 每项固定配置包含稳定 `brand_id`；展示当前 locale 下的品牌名称，不展示商品数量。
- 横向滑动浏览，不提供 `See all`；点击后以 `brand_id` 作为精确约束发起品牌搜索，品牌名称仅用于展示。

**Popular categories**

- 仅在 Mobile Web 搜索发现页展示。
- V1 由前端代码固定维护品类 ID 名单和展示顺序，并据此渲染；不请求动态 Popular categories 数据，不按市场热度重新排序。
- 品类卡复用品类模块已有图片，并读取当前 locale 对应的品类名称；搜索模块不单独配置图片或名称。
- 横向滑动浏览，不提供 `See all`；点击后打开该品类配置的链接，不发起品类搜索。

### 5.2 市场与多语言

- Popular searches 按当前 `market_id + locale` 请求。
- 用户切换 locale 后，重新读取新 `market_id + locale` 对应的 Popular searches。
- 不使用其他 locale 的 Popular searches 替代当前列表，也不对热门词进行机器翻译。
- Popular brands 的固定清单、展示顺序和图片不随 `market_id`、locale 或终端变化；品牌名称读取当前 locale 对应名称。
- Popular categories 的固定 ID 名单和顺序不随 `market_id` 或 locale 改变；品类名称读取当前 locale 对应名称，图片复用品类已有图片。
- Popular searches 的榜单生成、数据源切换、异常回退、内容治理及人工干预规则复用[搜推既有定义](https://zhuanspirit.feishu.cn/wiki/MRYIwf8SSiqSJskYtF8clxh5nud?from=auth_notice&hash=5732394c17444be5044ec05256c9e51d)；Web 仅消费最终有序结果。Popular brands 不参与动态榜单。

## 6. 搜索执行与结果

### 6.1 市场与 locale

- 每次搜索使用当前 `market_id`、渠道、locale 和展示货币作为上下文。
- 搜索结果仅包含当前市场可见、渠道 listing 为 `active` 且可售的商品；Sold Out、下架及其他不可公开状态直接排除，不进入结果数量、排序、筛选候选数量或分页。
- locale 控制搜索词处理、输入联想及品牌、品类和商品名称的展示语言。
- 展示货币不影响召回；价格展示、价格排序和价格筛选统一使用同一币种下的到手价快照，切换展示货币只做等值换算，不改变商品的原始价格关系。

### 6.2 结果页公共信息

- 从统一搜索输入层提交搜索后，关闭当前搜索层并进入搜索结果页。
- PC Web 搜索结果页常态保留全局 Header、导航栏和搜索图标；点击 Header 搜索图标后复用第 2 章的 Header 搜索态，提交新词后替换当前结果。
- Mobile Web 结果页顶部提供返回按钮、当前搜索词入口框和搜索图标。点击入口框或搜索图标后，打开统一全屏搜索层并带入当前搜索词；结果页本身不直接编辑搜索词或展示 Sug。
- 全屏搜索层打开后自动聚焦输入框，用户修改内容时按第 3 章展示 Sug；关闭或返回时保留原搜索结果、排序、筛选和滚动位置，不生成新的 Recent searches 或 Search event。
- 用户在全屏搜索层提交新搜索后，关闭搜索层并用新结果替换当前结果；新搜索使用默认排序和未筛选状态，并按普通搜索提交规则生成 Recent searches 与 Search event。
- Mobile Web 点击结果页返回按钮时，复用 Web 全局导航规则。
- 结果信息按 `Results for “{搜索词}”, {结果数量} items` 展示，并提供排序、筛选入口。
- PC Web 与 Mobile Web 分别复用 Collection 对应终端的商品卡、字段、到手价、优惠和收藏规则；Mobile Web 使用双列布局。商品卡主价格必须为价格服务返回的 `final_price`，定义和降级规则与首页 Explore Finds 一致。搜索模块向价格服务传递 `user_id / anonymous_id`、`market_id`、渠道、`listing_id`、当前货币和请求时间，不由前端或搜索服务自行推测优惠。
- 仅当搜推服务返回纠错词或推荐词时展示轻量提示；服务未返回时不占位。
- 系统不自动替换当前搜索词或重新搜索；用户点击纠错词或推荐词后才提交新搜索。

### 6.3 排序与筛选

**排序项**

- `Newest`：默认选中，按商品上架时间倒序。
- `Price: Low to High`：按当前请求同一价格快照的 `final_price` 升序；同价时按稳定 `listing_id` 排序。
- `Price: High to Low`：按当前请求同一价格快照的 `final_price` 降序；同价时按稳定 `listing_id` 排序。
- `Sort By` 是搜索结果页固定排序入口，不属于搜索接口动态返回的筛选维度。PC Web 在结果区顶部展示；Mobile Web 固定展示在横向筛选栏中，位于 `Filter` 之后。
- `Sort By` 仅允许单选，不参与筛选维度的 AND / OR、候选值数量、非收缩或 0 结果置灰规则；不得因搜索接口未返回某个筛选维度而隐藏、禁用或重置。
- 用户选择排序项后，将排序条件提交给搜索服务，并按服务返回的最终顺序更新商品列表；切换排序不改变筛选维度及候选项。
- 用户调整筛选时保留当前排序；提交新搜索词时重置为 `Newest`。

**筛选**

- Price 筛选的区间判断、候选数量和结果数量统一基于当前请求同一价格快照的 `final_price`，不得按 `listing_price` 过滤后再展示到手价。
- 用户身份、Market、Channel、优惠资格或价格有效期变化导致 `final_price` 变化时，服务端重新计算结果、价格排序及 Price 筛选数量；当前已选价格区间保留，列表按新到手价重新判断。
- 价格服务失败或返回无效到手价时，该商品允许按挂牌价降级展示并记录 `price_display_status = fallback_listing_price`；同一次结果请求中的排序和筛选也必须使用该降级展示价，避免所见价格与排序、筛选不一致。不得展示未经确认的优惠。

- 搜索接口返回有序的筛选维度、候选值及对应数量。PC Web 与 Mobile Web 展示接口返回的全部有效维度，并按返回顺序排列；前端不自行统计、补充、删除或重排。筛选维度的视觉样式、默认展开收起、组内搜索及查看更多等交互复用 Collection 对应端组件规则。
- 筛选采用非收缩候选项模型：本次搜索内候选集合保持稳定，只更新数量；数量为 0 的未选项保留但置灰，已选项保留供取消。提交新搜索词或切换 `market_id`、渠道、locale 后，按新响应重建候选集合。
- 维度间使用 AND，同一维度多值使用 OR。
- 应用筛选后，使用最新响应刷新商品、结果总数及候选值数量。
- 切换排序或应用筛选时，只有商品区域进入加载或刷新态；结果总数和筛选候选项保留在原位置，并在最新响应返回后更新。
- PC Web 直接复用 Collection 的 240px 左侧筛选栏、维度展示样式、展开收起、内部滚动和即时筛选规则；按接口顺序展示全部有效筛选维度，结果数量和 `Sort By` 保留在搜索结果区顶部。
- Mobile Web 直接复用 Collection 的移动端横向筛选栏和完整 Filter 抽屉组件：横向栏固定展示 `Filter`、`Sort By`，其后按接口顺序展示全部有效筛选维度，超出屏幕时横向滑动；Filter 抽屉按同一顺序展示同一套完整维度，用户点击 `Apply` 后应用。
- Mobile Web Filter 抽屉复用 Collection 的宽度、Reset、`Apply · N items`、点击右侧露出区关闭及状态联动规则。
- Mobile Web 筛选后的预估结果数为 0 时，`Apply` 按钮置灰并展示 `No items match`；用户需调整或重置筛选后再应用。
- 已应用的筛选条件在刷新、分享 URL 恢复、结果数据变化或服务端实际返回 0 时，进入筛选后无结果状态并提供 `Clear filters`。
- 搜索结果页不复用 Collection 的图文筛、Collection 运营配置的快筛、Banner 及其专属滚动交互。
- 切换排序或应用筛选后，商品列表回到顶部。

### 6.4 终端加载差异

- PC Web 使用 `View More`，每次追加 40 个商品；全部加载完成后按钮消失。
- Mobile Web 使用上滑无限滚动，每页最多加载 40 个商品。
- Mobile Web 无更多数据时使用系统原生 overscroll 回弹。

### 6.5 结果状态

| 状态 | 页面处理 |
|---|---|
| 首次加载 | 结果信息区展示 `Results for “{query}”`；商品区域展示统一商品列表骨架屏；保留当前终端的结果页顶部和页面框架。 |
| 首次请求失败 | 结果信息区展示 `Results for “{query}”`；结果区域展示 `We couldn’t load results`、`Check your connection and try again.` 和 `Try again`；保留当前搜索词、排序与筛选条件。点击 `Try again` 后按原条件重新请求，成功后进入正常结果状态。 |
| 下一批加载失败 | 保留已加载商品；在列表底部或 `View More` 区域展示 `More items couldn’t be loaded` 和 `Try again`，点击后按当前条件继续加载。 |
| 搜索词无结果 | 展示 `Results for “{query}”, 0 items`、空态插图、标题 `We couldn’t find any matches`、说明 `Try searching for a different brand or item.`，以及标题为 `You May Also Like` 的首页 `For You` 模块；用户通过结果页现有搜索入口重新搜索。 |
| 筛选后无结果 | 展示 `Results for “{query}”, 0 items`、当前筛选条件与筛选入口、标题 `No matches for these filters`、说明 `Try removing one or more filters.` 和 `Clear filters`。点击后清除全部筛选并重新加载当前搜索词结果。 |

- 搜索词无结果页直接挂载首页 `For You` 模块，并将模块标题展示为 `You May Also Like`；推荐数据、顺序、商品卡、加载及状态处理均执行首页 `For You` 规则。
- 搜索结果数量、排序和筛选作用于搜索结果；`For You` 模块按首页自身规则独立渲染。
- 从商品详情返回搜索结果页时，恢复搜索词、排序、筛选和列表位置。

### 6.6 Web 结果 URL 与浏览器行为

- 每次成功提交搜索后进入可分享的搜索结果 URL。
- URL 保存搜索目标（关键词，或品牌/品类目标 ID）、已生效的筛选条件和排序状态。
- 用户应用筛选或切换排序后，同步更新当前搜索结果 URL。
- 用户刷新页面、打开分享链接或使用浏览器前进与后退时，根据 URL 恢复搜索目标、筛选条件和排序状态。
- 通过刷新或分享链接进入结果页时，从页面顶部加载首批搜索结果。

## 7. 依赖与风险

| 依赖 | 本模块要求 |
|---|---|
| 搜推服务 | 提供 Sug、最终有序搜索结果、结果总数、可用筛选维度、候选值与数量及分页信息；价格排序和 Price 筛选消费价格服务的同一到手价快照。 |
| 统一身份与账号数据 | 提供当前 `anonymous_id` / `user_id`，并支持 Recent searches 的登录复制、账号归属、跨设备读取与合并、主体切换和待同步队列隔离。 |
| 数据埋点与行为平台 | 逐条接收 Search event，并支持账号归属、上报及待同步队列隔离；各事件保持独立。 |
| Market、商品与 listing | 提供当前 `market_id`、渠道可见性、listing 状态及统一商品卡所需字段。 |
| 价格 / 营销服务 | 按用户、Market、Channel、listing、币种和请求时间批量返回 `listing_price`、`final_price`、`eligible_discount_amount`、优惠明细、`price_valid_until` 和计算状态。 |
| 品牌、品类与商品域 | 通过稳定 ID 提供当前 locale 下的名称、品类已有图片及统一缺译兜底，并提供品类卡配置链接。 |
| Collection 与公共商品列表 | 提供统一筛选维度池、PC/Mobile 筛选交互、商品卡和列表加载规则。 |
| Popular searches 数据 | 按第 5.2 节维度返回最终有序内容；榜单策略复用搜推既有定义。 |
| 首页 `For You` | 在搜索词无结果页提供可直接挂载的 `For You` 模块，包括推荐数据、顺序、商品卡、加载及状态处理。 |

- Recent searches 的登录复制、保存边界与清除方式需纳入 Privacy Policy / Notice at Collection；数据保留、注销及 DSAR 删除复用全局隐私规则。
- SEO 收录、canonical 和 Sitemap 由 SEO 产品统一定义；搜索结果 URL 按第 6.6 节提供可恢复的页面状态。

## 8. 版本规划

- 当前版本为 Web V1，覆盖 PC Web 和 Mobile Web；App 搜索在后续 App 项目中单独定义。

## 9. 原型索引

| 模块 | PC Web | Mobile Web |
|---|---|---|
| 当前正式 UI 源稿 | [Looply 1.1](https://www.figma.com/design/sAOLkw0gIl1bwQRYCDqKuW/Looply-1.1) | [Looply 1.1](https://www.figma.com/design/sAOLkw0gIl1bwQRYCDqKuW/Looply-1.1) |
| 统一开发评审入口 | `looply-global-search-dev-review-v0.1.html`，可筛选 PC Web | `looply-global-search-dev-review-v0.1.html`，可筛选 Mobile Web |
| UI 评审说明（非 UI 源稿） | `looply-global-search-ui-review-v0.1.html`，切换至 PC Web | `looply-global-search-ui-review-v0.1.html`，切换至 Mobile Web |
| 功能逻辑与状态演示 | `looply-global-search-web-demo-v0.1.html`，PC 视口 | `looply-global-search-web-demo-v0.1.html`，Mobile 视口 |
| 独立终端原型 | `looply-global-search-pc-web-demo-v0.1.html` | `looply-global-search-mobile-web-demo-v0.1.html` |
| Sug 及 Loading / 空结果 / 失败 | `Demo states · review only` 中的 Sug 状态 | `Demo states · review only` 中的 Sug 状态 |
| Recent searches 与 Popular content | 搜索发现层 | 全屏搜索发现页 |
| 搜索结果、排序、筛选与状态 | 搜索结果页与状态控件 | 搜索结果页、抽屉与状态控件 |

## 10. 下个版本修改需求

本节为基于 v0.3 的增量修改；本节未涉及的规则保持不变。

### 10.1 筛选值显示商品数量

搜索结果页继续复用 Collection 筛选组件，并执行《Collection 落地页 PRD v1.6》§9.1：PC 筛选栏、Mobile 快筛二级面板及 Filter 抽屉中的每个筛选值后显示对应商品数量。
