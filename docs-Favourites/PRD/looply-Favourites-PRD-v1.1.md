# Looply Favourites PRD

**文档版本**：v1.1
**撰写时间**：2026年7月
**模块**：Favourites（收藏中心）
**子模块**：Wishlist / Recently Viewed / Recommended（本期 Feed 展示）
**端**：APP
**配套原型**：looply-favourites-prototype-v6.html
**参考文档**：looply-收藏与浏览历史-PRD-v1.0.md

---

## 一、概述

### 1.1 背景与目标

Favourites 是 Looply APP Tab Bar 的独立功能入口（第 3 个 Tab），将收藏、浏览历史、保存搜索、为你推荐四项买家高频能力聚合在同一页面下，以子 Tab 切换的方式组织，降低用户在不同收藏类内容间的导航成本。

**核心定位**：Favourites 是聚合容器，负责页面框架与子 Tab 路由。各子模块（Wishlist、Recently Viewed）的业务逻辑、后台数据获取、交互规则、前端页面与「收藏与浏览历史 PRD v1.0」完全一致，不另立业务规则。Recommended 模块本期以 Feed 形式实现，展示基于用户收藏与浏览历史的个性化推荐商品。

**与「收藏与浏览历史」模块的关系**：

| 维度 | 收藏与浏览历史（原模块） | Favourites（本 PRD） |
|---|---|---|
| 入口 | 我的页各自独立入口，独立页面含返回键 | Tab Bar 第 3 Tab，子 Tab 切换，无返回键 |
| 业务逻辑 | 完整定义方 | 复用方，100% 对齐，不重复定义 |
| 端 | APP + PC Web | 仅 APP 端 |
| 子模块范围 | Wishlist + Recently Viewed | 四个子 Tab（含两个本期占位） |

### 1.2 不做什么（明确边界）

| 不做项 | 说明 |
|---|---|
| Saved Searches | 本期不做，从 Favourites 模块移除，二期单独立项 |
| Recommended 算法/个性化召回 | 本期仅展示 Feed 框架，推荐算法依赖推荐系统，二期接入 |
| PC Web 端 Favourites 页 | 仅覆盖 APP 端；PC 端收藏/浏览历史沿用独立页方案 |
| 收藏分组 / 批量管理 / 排序 | 二期，与收藏与浏览历史 PRD v1.0 §1.3 一致 |
| 浏览历史容量上限 | 本期不限，与原 PRD 一致 |
| 降价推送提醒 | 事件源在商品/促销模块，本模块不产生对外事件 |
| 商详页「最近浏览」横条 | 数据能力由收藏与浏览历史模块提供，本模块不重复定义 |

### 1.3 用户角色

与「收藏与浏览历史 PRD v1.0」§1.4 完全一致：

| 角色 | 说明 |
|---|---|
| 登录用户 | 以 user_id 为主体，账户级持久化、跨设备同步 |
| 未登录访客 | 以设备级 anonymous_id 为主体记录，登录后复制关联到账户 |

### 1.4 核心场景

1. 用户点 Tab Bar「Favourites」→ 默认打开 Wishlist 子 Tab → 查看收藏商品、识别降价 → 点「Buy Now」直接结算。
2. 用户切换到「Recently Viewed」→ 找回最近浏览的商品 → 点卡片进商详。
3. 收藏/浏览的商品已售出 → 列表显示 Sold Out 失效态 → 点「Find Similar」看同类在售商品。
4. 未登录访客收藏/浏览 → 注册登录 → 设备级记录复制关联到账户，跨设备可见。
5. 用户在首页下滑查看 Recommended Feed → 看到基于收藏/浏览历史的推荐商品双列瀑布流。

### 1.5 全局页面流转



### 1.6 术语说明

| 术语 | 含义 |
|---|---|
| listing（渠道商品） | 用户前台可见、可下单的单件在售商品，收藏/浏览的锚定对象 |
| product（实物商品） | 一物一码的实物层，listing 的上游，本模块不直接锚定 |
| price_at_save | 收藏时记录的价格快照，降价判断基准 |
| anonymous_id | 设备级匿名标识，未登录记录的主体 |
| 失效态 | 商品已售出或已下架，不可购买的状态，前台统一展示为 Sold Out |
| 降价高亮 | 打开列表时实时比对现价与快照价，现价更低则标识 |
| 子 Tab | Favourites 页内的横向切换标签 |
| 占位页 | 本期功能未实现，显示空态 + Coming Soon 标签，仅保留结构 |

### 1.7 多语言 / 多国家策略

本模块文案需支持 i18n（多市场方向）。价格按商品系统返回的币种展示。收藏/浏览数据本身不含地域属性，无多国合规差异；隐私相关（浏览记录、未登录记录）的合规告知见 §2.4.2。


---

## 二、页面框架：Favourites 容器

### 2.1 整体布局

v1.1 将 Favourites 改为**概览页（Overview）+ 全屏面板（Full Panel）**双层结构，取代原来的子 Tab 切换模式。

| 区域 | 说明 |
|---|---|
| Status Bar | 系统状态栏，高度 50px |
| 概览页头部 | 「Favourites」大标题 + 搜索图标 + 购物车图标，position: sticky |
| 概览内容区 | 按模块分区展示：Wishlist 区块 / Recently Viewed 区块 / Recommended 区块（自上至下） |
| App Tab Bar | 固定底部，全局导航，高度 72px |

**全屏面板**：点击 Wishlist / Recently Viewed 区块的卡片或"See All"后，从底部滑入全屏面板，覆盖整个页面。面板内含顶部 back 按钮返回概览页。

### 2.2 子 Tab 栏规格

**位置**：Status Bar 正下方，position: sticky，top: 50px。

**Tab 顺序与状态**：

| 顺序 | Tab 标签 | 本期实现状态 |
|---|---|---|
| 1 | Wishlist | 完整实现 |
| 2 | Recently Viewed | 完整实现 |
| 3 | Recommended | 本期实现（Feed 展示，无独立全屏面板） |

**交互规则**：

| 规则 | 说明 |
|---|---|
| 默认激活 | 进入 Favourites 页时默认选中 Wishlist（Tab 1） |
| 切换 | 点任意 Tab → 内容区完整替换为对应页，页面回到顶部，Tab 高亮切换 |
| 切回 | 切回已浏览过的 Tab 时，恢复该 Tab 上次的滚动位置 |
| 横向滑动 | Tab 栏支持横向滑动，为二期增加更多 Tab 预留 |

**样式规格**：

| 状态 | 样式 |
|---|---|
| 激活态 | 文字颜色 #1A1A1A，font-weight 700，Tab 下沿紫色下划线（色值 #6432FC，高 2.5px，内缩左右各 14px） |
| 未激活态 | 文字颜色 #9CA3AF，font-weight 500，无下划线 |
| Tab 字号 | 13px |

### 2.3 全屏面板规格

全屏面板由 Wishlist 和 Recently Viewed 两个模块各有一个，覆盖整屏（position: fixed, inset: 0）。

| 元素 | 规格 |
|---|---|
| 顶部 Header | 左侧 back 箭头 + 中间标题（Wishlist / Recently Viewed），position: sticky |
| 三 Tab 切换栏 | All / In Stock / Price Drop（Wishlist）；All / In Stock / On Sale（Recently Viewed） |
| 内容区 | 单列商品卡片，与「收藏与浏览历史 PRD v1.0」规格完全一致 |
| 底部 | 无限滚动到底显示「✓ You've reached the end」 |

**三 Tab 筛选规则**：

| Tab | Wishlist 含义 | Recently Viewed 含义 |
|---|---|---|
| All | 全部商品（含在售、降价、Sold Out） | 全部浏览记录 |
| In Stock | 仅展示在售（含降价）商品，过滤 Sold Out | 仅展示在售商品 |
| Price Drop | 仅展示相比收藏时价格有降幅的商品 | 仅展示当前促销/降价中的商品 |

**Tab 深链接**：点击概览页降价强调条 → 进入对应全屏面板 → 自动激活 Price Drop / On Sale tab。

---

## 三、需求详细描述

### 3.1 Wishlist 子 Tab

#### 3.1.1 模块概述

收藏让用户把感兴趣的孤品加入个人清单，支持登录与未登录。核心价值是「蹲降价」——收藏时记录价格快照，后续打开列表实时比对现价，降价则高亮。一物一码下，被收藏商品随时可能售出/下架，列表需处理失效态。

本子 Tab 完整复用「收藏与浏览历史 PRD v1.0」§2.1 全部业务规则，以下各节列出规则要点及原文引用，不重复定义。

#### 3.1.2 收藏操作（机制型）

**功能描述**：在商品卡片或详情页点 ♡ 完成收藏/取消，无独立页面的轻交互。

**触发条件**：用户点击商品卡片、商品详情页上的 ♡ 图标。

**处理流程**：
- 添加收藏：♡ 空心 → 点击 → 写入主体 × listing 收藏关系 + 记录价格快照 price_at_save → ♡ 变实心。乐观更新（先变 UI，再确认服务端）。
- 取消收藏：♡ 实心 → 点击 → 软删除（is_active=false + 时间戳）→ ♡ 变空心。在 Wishlist 列表页取消收藏，该项即时从列表移除。
- 未登录收藏：以设备级 anonymous_id 为主体写入，不拦截、不强制登录。

**规则说明**：

| 规则 | 内容 |
|---|---|
| 收藏主体 | 登录用 user_id，未登录用 anonymous_id，二选一 |
| 价格快照 | 收藏成功即记录当时 listing 价格，后续不随商品改价变动 |
| 重复收藏 | (主体, listing_id) 唯一约束，同件不重复收藏 |
| 软删除 | 取消收藏不物理删除，置 is_active=false，保留追溯与合并幂等 |
| 收藏上限 | 不限上限 |

**异常处理**：

| 场景 | 处理方式 |
|---|---|
| 网络异常 | 乐观更新后服务端失败 → ♡ 回滚原状态 + 轻提示「操作失败，请重试」 |
| 商品已失效仍点收藏 | 允许收藏；失效商品的 ♡ 在列表中置灰不可点 |
| 并发重复点击 | 以最终状态为准，幂等处理 |

**UI 关联**：♡ 按钮属商品卡片/详情页组件。本模块负责收藏关系写入与状态回显。APP 端见原型 Wishlist 子 Tab 各卡片右上角。

> 完整规则引用：收藏与浏览历史 PRD v1.0 §2.1.2

#### 3.1.3 收藏状态回显（机制型）

**功能描述**：向商品卡片、详情页提供 ♡ 的收藏状态查询，使各页面正确显示实心/空心。

**触发条件**：商品卡片、详情页渲染时查询当前主体对某 listing（或一批 listing）的收藏状态。

**处理流程**：按主体 + listing_id（单个或批量）查询是否存在有效收藏（is_active=true），返回布尔状态供前端渲染 ♡。

**规则说明**：未登录态按 anonymous_id 查询；登录态按 user_id。状态回显是只读能力，供全站商品展示位复用。

> 完整规则引用：收藏与浏览历史 PRD v1.0 §2.1.3

#### 3.1.4 收藏列表页（页面型）

**功能描述**：展示当前用户的全部收藏，支持「仅看在售」筛选，处理四种商品状态，提供失效项「Find Similar」。

**前置条件**：用户进入 Favourites → Wishlist 子 Tab。无收藏时显示空态（见 §3.1.5）。

**页面布局**：

| 区域 | 说明 |
|---|---|
| 顶部标题区 | 大标题「Wishlist」，含 back 箭头返回概览页 |
| 三 Tab 筛选栏 | All（默认）/ In Stock / Price Drop，参见 §2.3 |
| 商品卡片列表 | 竖向单列卡片，图左信息右 |
| 列表底部提示 | 无限滚动到底显示「✓ You've reached the end」；加载中显示「⟳ Loading more...」 |

**页面元素**：

| 元素 | 说明 |
|---|---|
| 三 Tab 筛选 | 激活 tab 紫色下划线（#6432FC）+ 紫色文字；未激活灰色；切换即时过滤，无需刷新 |
| 商品卡片 | 复用 ProductCard：图 / 品牌（全大写）/ 名称 / 价格；失效态变体见 §3.3.2 |
| 排序 | 默认按收藏时间倒序，在售在前、失效下沉；本期不提供其他排序 |
| 加载策略 | 上滑无限滚动，分批加载（每批约 20 件），详见 §3.3.5 |

**页面状态变体**：

| 状态 | 触发条件 | 表现 |
|---|---|---|
| 默认（有收藏） | 存在至少一条收藏记录 | 卡片列表，在售在前、失效下沉 |
| In Stock tab | 点「In Stock」tab | 隐藏 Sold Out 卡片，只显在售（含降价）卡片 |
| Price Drop tab | 点「Price Drop」tab | 只显相比收藏时有降价的卡片 |
| 空态 | 无任何收藏，或全部取消后 | 见 §3.1.5 |
| 加载态 | 列表请求中 | 底部显示「⟳ Loading more...」 |

**操作流程**：
- 主流程：进入页 → 加载收藏列表（实时附带商品状态与现价）→ 在售卡片在前、失效下沉 → 点卡片进商详。
- 筛选：点「In Stock」tab → 只显在售；点「Price Drop」tab → 只显降价商品；点「All」tab → 显示全部（含失效）。默认进入时激活 All tab；从概览页降价强调条点击进入时激活 Price Drop tab。
- 取消收藏：点卡片 ♡ → 软删除 → 该项即时从列表移除。
- 失效项找相似：失效卡点「Find Similar」→ 跳同品牌/品类/价位的在售商品。
- 空态：全部移除或无收藏 → 显示空态（见 §3.1.5）。

**校验规则**：

| 字段/动作 | 规则 | 时机 |
|---|---|---|
| 列表数据 | 每项渲染时实时取商品系统状态与现价 | 列表加载 |
| 降价判断 | 实时比对 price_at_save 与现价，任意幅度降价即标 | 列表加载 |

**交互说明**：
- 降价高亮：现价低于 price_at_save → 绿色现价 + 原价划线 + 「↓$X since saved」绿色标签。任意幅度降价即标，非后台监控触发。
- 失效下沉：已售出/已下架项排到在售之后，不过滤。

**异常处理**：

| 场景 | 处理方式 |
|---|---|
| 商品系统接口超时/不可用 | 降级展示（按上次已知状态），不阻塞列表 |
| 收藏的 listing 已被删除 | 显示为失效态 + Find Similar |
| 空数据 | 显示空态 |

**UI 关联**：APP 端原型 `looply-favourites-prototype-v3.html` Wishlist 子 Tab（含在售 / 降价 / Sold Out / 空态四种状态）。

> 完整规则引用：收藏与浏览历史 PRD v1.0 §2.1.4

#### 3.1.5 收藏空态（页面型）

**功能描述**：用户无任何收藏时的引导页。

**页面元素**：♡ 图标（紫色圆形底，#EDE9FE 背景）+ 主文案「Your wishlist is empty」+ 副文案「Save pieces you love and we'll alert you when prices drop.」+ 主按钮「Explore Items」（紫色）。

**操作流程**：点「Explore Items」→ 跳 Shop All 页面（全部商品 collection，带默认排序）。

**UI 关联**：APP 端原型 Wishlist 子 Tab 空态。

> 完整规则引用：收藏与浏览历史 PRD v1.0 §2.1.5

#### 3.1.6 收藏数据计数

**规则说明**：

| 位置 | 本期 | 口径 |
|---|---|---|
| Tab Bar Favourites 入口 | 不显数字 | 只显图标，不算不存 |
| Wishlist 列表页头计数 | 不显示 | 前台精简，不在列表头显示计数 |
| 商详页「X 人收藏此商品」 | 不做 | 二期 |

> 完整规则引用：收藏与浏览历史 PRD v1.0 §2.1.6


### 3.2 Recently Viewed 子 Tab

#### 3.2.1 模块概述

隐式记录用户进入过的商品详情页，帮助找回。纯时间倒序展示，支持登录与未登录，支持单条删除与全量清除。

本子 Tab 完整复用「收藏与浏览历史 PRD v1.0」§2.2 全部业务规则。

#### 3.2.2 浏览记录写入（机制型）

**功能描述**：用户进入商品详情页即在服务端记录一次浏览，无独立页面。

**触发条件**：用户进入任一商品详情页。

**处理流程**：
- 进详情页 → 服务端记录：主体（user_id 或 anonymous_id）× listing_id × viewed_at。
- 去重：同一 listing 重复浏览不新增记录，只更新 viewed_at 为最近时间。
- 容量：本期不限制条数与留存时长。

**规则说明**：

| 规则 | 内容 |
|---|---|
| 记录主体 | 登录 user_id，未登录 anonymous_id |
| 去重 | (主体, listing_id) 唯一，再次浏览更新时间戳 |
| 容量 | 本期不限制（二期再评估上限/留存期） |
| 隐式记录 | 无需用户操作，进详情页即记录 |

**异常处理**：写入失败不阻塞用户浏览（异步、容错）。

> 完整规则引用：收藏与浏览历史 PRD v1.0 §2.2.2

#### 3.2.3 浏览历史列表查询（机制型）

**功能描述**：按主体查询浏览记录，返回时实时附带每件商品的最新状态与价格，供前端直接渲染失效态。

**处理流程**：按主体查询 → 时间倒序 → 分页 → 每项实时关联商品系统状态/价格。

**规则说明**：读写接口中立开放，供 C 端各页调用（列表页、商详页横条等），展示形态不约束。

> 完整规则引用：收藏与浏览历史 PRD v1.0 §2.2.3

#### 3.2.4 浏览历史列表页（页面型）

**功能描述**：展示当前用户的浏览记录，纯时间倒序，支持单条删除与全量清除，失效项处理同收藏。

**前置条件**：用户进入 Favourites → Recently Viewed 子 Tab。无记录显示空态（见 §3.2.5）。

**页面布局**：

| 区域 | 说明 |
|---|---|
| 顶部标题区 | 大标题「Recently Viewed」+ back 箭头返回概览页 + 右侧「🗑 Clear All」按钮 |
| 三 Tab 筛选栏 | All（默认）/ In Stock / On Sale，参见 §2.3 |
| 商品卡片列表 | 竖向单列卡片，每行右侧有单条删除「×」按钮 |
| 列表底部提示 | 到底显示「✓ You've reached the end」；加载中显示「⟳ Loading more...」 |

**页面元素**：

| 元素 | 说明 |
|---|---|
| Clear All | 右上角，trash 图标 + 文字「Clear All」，触发全量清除二次确认弹窗 |
| 商品卡片 | 复用 ProductCard，每行右侧有「×」单条删除按钮；失效态变体见 §3.3.2 |
| 排序 | 纯时间倒序，不做日期分组，不做失效下沉（浏览历史以找回为目的，纯倒序最直接） |
| 加载策略 | 上滑无限滚动，详见 §3.3.5 |

**为什么纯时间倒序、不做日期分组**：浏览历史采用纯时间倒序平铺，不做 Today / Earlier 等日期分组。用途是「快速找回刚看的」，纯倒序最直接；日期分组适用于浏览器式海量历史的按天回溯场景，价值低且增加复杂度。

**页面状态变体**：

| 状态 | 触发条件 | 表现 |
|---|---|---|
| 默认（有记录） | 存在至少一条浏览记录 | 纯倒序卡片列表 |
| 空态 | 无记录，或 Clear All / 单条全删后 | 见 §3.2.5 |
| 加载态 | 列表请求中 | 底部显示「⟳ Loading more...」 |

**操作流程**：
- 主流程：进入页 → 纯时间倒序加载（实时附带状态/价格）→ 点卡片进商详。
- 单条删除：点某条「×」→ 即时移除该条 → 若全部删完则显示空态。
- 全量清除：点「Clear All」→ 触发二次确认弹窗（见 §3.2.6）→ 确认 → 清空全部 → 显示空态。
- 失效项找相似：失效卡点「Find Similar」→ 跳相似在售品。
- 空态：全部删除或无记录 → 显示空态（见 §3.2.5）。

**校验规则**：

| 动作 | 规则 | 时机 |
|---|---|---|
| 列表数据 | 每项实时取商品状态/价格 | 列表加载 |
| Clear All | 需二次确认弹窗，防误删 | 点击 Clear All 时 |

**异常处理**：

| 场景 | 处理方式 |
|---|---|
| 商品状态接口异常 | 降级展示，不阻塞列表 |
| 已删除/失效的 listing | 显示失效态 + Find Similar |
| 空数据 | 显示空态 |

**UI 关联**：APP 端原型 `looply-favourites-prototype-v3.html` Recently Viewed 子 Tab（含在售 / 降价 / Sold Out / 单条删除 / Clear All 弹窗 / 空态）。

> 完整规则引用：收藏与浏览历史 PRD v1.0 §2.2.4

#### 3.2.5 浏览历史空态（页面型）

**功能描述**：无浏览记录时的引导页。

**页面元素**：时钟（history）图标（紫色圆形底，#EDE9FE 背景）+ 主文案「No browsing history yet」+ 副文案「Items you view will appear here so you can find them again.」+ 主按钮「Explore Items」（紫色）。

**操作流程**：点「Explore Items」→ 跳 Shop All 页面，与收藏空态一致。

**UI 关联**：APP 端原型 Recently Viewed 子 Tab 空态。

> 完整规则引用：收藏与浏览历史 PRD v1.0 §2.2.5

#### 3.2.6 Clear All 二次确认弹窗（页面型）

**功能描述**：点击「Clear All」后触发居中弹窗，要求用户二次确认，防止误删浏览历史。

**触发条件**：用户点击 Recently Viewed 页面右上角「Clear All」按钮。

**页面元素**：

| 元素 | 说明 |
|---|---|
| 弹窗类型 | 居中弹窗（非底部 sheet），背景半透明黑遮罩 |
| 图标 | 红色圆形底（#FEE2E2）+ trash 图标（#EF4444） |
| 标题 | 「Clear all history?」 |
| 副文案 | 「This will remove all items from your browsing history. This can't be undone.」 |
| 按钮 | 并排两个：「Cancel」（灰底 #F5F5F5 + 灰边）/ 「Clear All」（红底 #EF4444 白字） |

**操作流程**：
- 点「Cancel」或点遮罩区域 → 关闭弹窗，不执行清除。
- 点「Clear All」→ 清空全部浏览记录 → 关闭弹窗 → 列表替换为空态。

**UI 关联**：APP 端原型 Recently Viewed 子 Tab Clear All 弹窗。

#### 3.2.7 隐私控制

**规则说明**：

| 控制项 | 本期 | 说明 |
|---|---|---|
| 清除浏览历史 | ✅ | 全量清除 + 单条删除，本模块直接负责，本期合规主手段 |
| 隐私告知 | ✅ | 隐私政策中说明记录行为、未登录记录复制关联到账户 |
| 配合全局 DSAR | ✅ | 全局 DSAR 触发时删除本模块数据；DSAR 入口归用户中心，非本模块 |

> 完整规则引用：收藏与浏览历史 PRD v1.0 §2.2.6


### 3.3 公共组件：商品卡片与失效态

#### 3.3.1 组件概述

Wishlist 与 Recently Viewed 共用同一商品卡片组件（ProductCard），共用一套失效态规则。提取为公共组件，两个列表页引用。

#### 3.3.2 商品卡片字段

| 字段 | 说明 |
|---|---|
| 商品图 | listing 主图，96×96px，圆角 12px |
| 品牌 | 大写品牌名（如 CHANEL），10px font-weight 600，颜色 #9CA3AF |
| 名称 | 商品名称，14px font-weight 600 |
| 价格 | 现价；降价时附原价划线 + 降幅标签 |
| 操作按钮 | 在售卡：「Buy Now」紫色主按钮；失效卡：「Find Similar」链接 |
| 右侧操作 | Wishlist 卡：♡ 收藏/取消按钮；Recently Viewed 卡：「×」单条删除按钮 |

> 认证：前台收藏/浏览卡片不展示认证徽章，卡片保持精简。认证（Authenticated）信息在商品详情页呈现。

#### 3.3.3 失效态变体（完整枚举）

前台买家侧不区分「已售出」与「已下架」，统一展示为 Sold Out：

| 状态枚举 | 含义 | 进入条件 | 卡片表现 |
|---|---|---|---|
| 在售（active） | 商品可购买 | listing_status=在售 且 有库存 | 正常图 + 价格；♡ 可点（Wishlist）/ × 可点（Recently Viewed） |
| 已降价（active+discount） | 在售且现价低于快照价 | 在售 且 现价 < price_at_save | 正常展示 + 绿色现价 + 原价划线 + 绿色降幅标签（↓$X since saved） |
| 失效（sold / off_shelf） | 已售出或已下架，不可购买 | listing_status=已售出 或 已下架 | 保留商品图 + 半透明灰蒙层 + 蒙层居中白字「Sold Out」+ 品牌/名称置灰 + 「Find Similar」链接 + ♡ 置灰不可点 |

> 说明①：后台 listing_status 仍区分 sold 与 off_shelf，前台两者渲染完全一致（均为 Sold Out 蒙层），买家无需感知区别。
> 说明②：降价高亮是「在售」的子表现，不是独立状态；判定为实时比对，任意幅度降价即标。
> 说明③：失效态保留原商品图，仅叠加半透明灰蒙层 + 文案，不用纯灰色块（保留商品识别度）。

#### 3.3.4 失效项排序与找相似

| 规则 | Wishlist | Recently Viewed |
|---|---|---|
| 失效下沉 | 已售出/已下架项排到在售之后 | 不下沉，纯时间倒序 |
| Find Similar | 失效卡提供「Find Similar」→ 跳同品牌/品类/价位的在售商品 | 同左 |

#### 3.3.5 立即购买（Buy Now）

**功能描述**：在售商品卡片提供「Buy Now」立即购买按钮，点击直接进入结算流程，绕过购物车，缩短转化路径。

**为什么用 Buy Now**：一物一码下每件库存唯一随时被买走，Buy Now 直接进结算锁定该件；二奢单件决策、购物车凑单场景弱；收藏/浏览用户高购买意向，Buy Now 一步到位。

**展示规则**：

| 卡片状态 | 按钮 |
|---|---|
| 在售 / 已降价 | 展示「Buy Now」（紫色 #6432FC + 图标） |
| 失效（Sold Out） | 不展示，位置改为「Find Similar」 |

**交互**：点击「Buy Now」→ 跳转结算页（Checkout），不经过购物车 → 进入该 listing 的下单结算流程。

**库存锁定说明**：Buy Now 进入结算时需锁定该 listing，防止结算过程中被他人买走。锁定机制（锁定时长、超时释放、并发抢购处理）归属交易/结算模块定义，本模块负责「触发 Buy Now 跳转结算」。

**异常处理**：

| 场景 | 处理方式 |
|---|---|
| 点击 Buy Now 时商品已失效 | 拦截跳转 → 提示「商品已售出」+ 卡片刷新为失效态 |
| 结算后库存锁定失败 | 由结算流程提示「商品已售出」并中止，引导「Find Similar」 |
| 接口异常 | 提示「操作失败，请重试」，按钮状态回滚 |

> 完整规则引用：收藏与浏览历史 PRD v1.0 §2.3.6

#### 3.3.6 分页与加载策略

**规则**：APP 端上滑无限滚动（infinite scroll）+ 分批加载，每批约 20 件，上滑续接。

| 维度 | 规则 |
|---|---|
| 触发 | 滚动到当前内容底部时自动加载下一批 |
| 加载中 | 底部显示「⟳ Loading more...」（旋转 icon + 文字） |
| 到底 | 无更多数据时显示「✓ You've reached the end」（静态文案，不可点击） |
| 空态 | 空态不显示结束提示，有独立空态页 |
| 筛选联动 | 收藏页切换筛选 pill 时，重置滚动，基于筛选后结果集重新加载 |
| 加载失败 | 底部显示重试入口，不顶掉已加载内容 |

> 完整规则引用：收藏与浏览历史 PRD v1.0 §2.3.7

### 3.4 Saved Searches（本期不做）

Saved Searches 从本期 Favourites 模块移除，不在概览页展示入口，不设占位页。

**移除原因**：一期优先聚焦收藏与浏览历史的核心降价价值；Saved Searches 功能依赖搜索模块写入能力尚未就绪，二期单独立项。

**二期方向**（不属于本文档范围）：
- 搜索页保存条件、列表管理、新品匹配通知。

### 3.5 Recommended based on your favourites

#### 3.5.1 本期范围

在 Favourites 概览页底部以**双列瀑布流**形式展示推荐商品，风格与首页 Feed 一致。本期展示框架，召回数据使用首页推荐接口兜底，个性化算法二期接入。

**页面元素**：
- 区块标题：「Recommended based on your favourites」
- 布局：2 列等宽网格，商品卡片与首页 Feed 卡片规格保持一致
- 无"See All"入口，无独立全屏面板；概览页本身可无限下滑加载更多推荐商品（模拟）

**商品卡片字段**（与首页 Feed 一致）：

| 字段 | 说明 |
|---|---|
| 商品图 | 1:1 比例，圆角 14px |
| 品牌 | 大写品牌名，10px |
| 名称 | 商品名称，13px，最多 2 行 |
| 价格 | 现价；降价时展示绿色现价 + 划线原价 |
| Buy Now | 紫色主按钮 |
| ♡ 图标 | 右上角悬浮，点击收藏/取消 |

**UI 关联**：APP 端原型 `looply-favourites-prototype-v6.html` Recommended 区块。

#### 3.5.2 二期方向

- 接入推荐系统，基于收藏/浏览历史进行个性化召回。
- 召回策略：同品牌在售品、同品类近似价格、用户偏好标签。

---

## 四、跨模块横切：未登录记录与登录关联

完整复用「收藏与浏览历史 PRD v1.0」第四章，以下为规则要点。

### 4.1 双行分离模型

| 规则 | 说明 |
|---|---|
| 行主体 | favorite / browsing_history 每行主体二选一：user_id 与 anonymous_id 必须且只能一个非空 |
| 物理隔离 | 匿名行（anonymous_id 非空、user_id 为空）与用户行（user_id 非空、anonymous_id 为空）物理分离，互不污染 |
| 分域唯一约束 | UNIQUE(user_id, listing_id) WHERE user_id IS NOT NULL；UNIQUE(anonymous_id, listing_id) WHERE anonymous_id IS NOT NULL；唯一约束覆盖软删行 |

### 4.2 登录后复制上移

**触发条件**：登录 / 注册 / 第三方授权登录，任一拿到 user_id 即触发（注册不可遗漏）。

**处理流程**：
1. 取当前设备 anonymous_id 名下的活跃匿名记录（is_active=true）。
2. 复制到 user_id 名下（不删匿名原件）：INSERT ... ON CONFLICT DO NOTHING。
3. 防复活：ON CONFLICT DO NOTHING + 唯一约束覆盖软删行，防止「取消 → 再登录又复活」。
4. 快照/时间取舍：收藏保留较早的 price_at_save；浏览取较晚的 viewed_at。
5. 匿名原件保留不动，登出态仍可读。

**读写口径**：

| 状态 | 读取 | 写入 | 取消/删除 |
|---|---|---|---|
| 登录态 | WHERE user_id=?（跨设备一致） | 只写用户行 | 按 user_id + listing_id 软删用户行 |
| 登出态 | WHERE anonymous_id=?（本设备） | 只写匿名行 | 按 anonymous_id + listing_id 软删匿名行 |

> 完整规则引用：收藏与浏览历史 PRD v1.0 第四章

---

## 五、依赖与风险

### 5.1 上下游系统依赖

| 系统 | 依赖内容 |
|---|---|
| 商品系统 | listing 实时状态/价格（在售/降价/售出/下架判定）、商品基础信息（图/品牌/名/认证）；锚定主键 listing_id |
| 用户中心 | 用户主体 user_id；账户体系；全局 DSAR 删除编排 |
| 登录注册 | 登录/注册/授权触发复制关联；未登录引导 |
| 推荐/搜索 | 「Find Similar」找相似能力 |
| 交易/结算模块 | Buy Now 触发后的库存锁定（锁定机制由结算模块定义） |
| 商详页模块 | 消费「最近浏览」横条（本模块提供数据能力，界面归商详页） |
| Saved Searches（二期） | 搜索模块「保存搜索」写入能力 |
| 推荐系统（二期） | Recommended 个性化召回能力 |

### 5.2 外部服务依赖

无直接三方服务对接（收藏/浏览为平台内部能力）。

### 5.3 风险

| 风险 | 影响 | 应对 |
|---|---|---|
| 商品状态接口不可用 | 列表无法渲染实时状态 | 降级展示（上次已知状态），不阻塞 |
| anonymous_id 不稳定 | 未登录记录丢失/关联失败 | 方案待端上确认生成与有效期 |
| 失效项过多 | Wishlist 列表体验差 | 「仅看在售」筛选 + 失效下沉 + Find Similar |
| 浏览历史隐私投诉 | 合规风险 | 清除能力 + 隐私告知 + 配合 DSAR |
| Tab 切换白屏 | 用户体验差 | 懒加载：首次激活 Tab 时才发请求；切回已加载 Tab 直接渲染缓存 |
| Saved Searches / Recommended 占位期用户预期落差 | 用户困惑 | 明确展示「Coming Soon」标签，管理预期 |

---

## 六、版本规划

### 6.1 当前版本（MVP）范围

- Favourites 容器页框架（4 子 Tab + 切换逻辑 + App Tab Bar 第 3 Tab 入口）。
- Favourites 概览页：三区块聚合展示（Wishlist / Recently Viewed / Recommended）。
- Wishlist 全屏面板：三 Tab 筛选（All / In Stock / Price Drop）+ 降价深链接入口。
- Recently Viewed 全屏面板：三 Tab 筛选（All / In Stock / On Sale）+ 降价深链接入口。
- 降价强调条：两个区块各一条绿色提示，支持深链跳转对应 tab。
- Recommended 区块：双列 Feed 预览，无全屏面板，无限下拉加载。
- Saved Searches：本期移除，不做任何入口。
- 未登录记录与登录关联（双行分离 + 复制上移，与收藏与浏览历史模块共用数据能力）。

### 6.2 后续迭代方向（二期）

- Saved Searches：单独立项，完整功能（保存搜索条件 + 新品匹配通知）。
- Recommended：接入推荐系统个性化召回，替换首页兜底数据。
- Wishlist 排序（降价优先/价格）、批量管理、收藏分组文件夹。
- 社交化收藏（公开/分享）、关注品牌/卖家。
- 收藏变更事件输出（供降价推送提醒）。
- 商详页「X 人收藏此商品」计数。
- 浏览历史容量淘汰策略（条数/留存期上限）。
- 共享设备登出轮换 anonymous_id。

---

## 七、数据与埋点

### 7.1 关键埋点事件

| 事件 | 触发 | 用途 |
|---|---|---|
| favourites_tab_open | 点击 Tab Bar Favourites | 页面 PV / 模块活跃度 |
| favourites_subtab_switch | 切换子 Tab | 各子模块使用分布 |
| favourites_price_drop_banner_click | 点击概览页降价强调条 | 降价深链点击率 |
| favourites_recommended_scroll | 下滑加载更多推荐 | Recommended 区块参与度 |
| wishlist_open | 进 Wishlist 子 Tab | 收藏模块活跃度 |
| wishlist_item_add | 点 ♡ 添加收藏 | 收藏率 |
| wishlist_item_remove | 点 ♡ 取消收藏 | 流失率 |
| wishlist_price_drop_tab | 激活 Price Drop tab | tab 使用率 |
| wishlist_price_drop_click | 点降价卡片 | 降价转化率 |
| wishlist_find_similar_click | 点 Find Similar | 失效补救转化 |
| wishlist_buy_now_click | 点 Buy Now | 收藏页直接购买转化 |
| recently_viewed_open | 进 Recently Viewed 子 Tab | 浏览历史模块活跃度 |
| recently_viewed_item_delete | 点单条 × 删除 | 隐私行为监测 |
| recently_viewed_clear_all | 确认 Clear All | 隐私行为监测 |
| recently_viewed_find_similar_click | 点 Find Similar | 失效补救转化 |
| recently_viewed_buy_now_click | 点 Buy Now | 浏览历史直接购买转化 |

### 7.2 数据字段与来源

收藏/浏览数据见 ER 图 v1.0（favorite / browsing_history 表）。商品状态/价格来源商品系统，实时读取不落库。

---

## 八、附录

### 8.1 设计稿索引

| 页面 / 状态 | 原型文件 |
|---|---|
| Favourites 概览页（3 区块聚合） | looply-favourites-prototype-v6.html |
| Wishlist — 有内容态（在售卡） | looply-favourites-prototype-v6.html |
| Wishlist — 有内容态（降价卡） | looply-favourites-prototype-v6.html |
| Wishlist — 有内容态（Sold Out 卡） | looply-favourites-prototype-v6.html |
| Wishlist — 空态 | looply-favourites-prototype-v6.html |
| Recently Viewed — 有内容态（含单条删除 ×） | looply-favourites-prototype-v6.html |
| Recently Viewed — 有内容态（含降价卡） | looply-favourites-prototype-v6.html |
| Recently Viewed — Clear All 二次确认弹窗 | looply-favourites-prototype-v6.html |
| Recently Viewed — 空态 | looply-favourites-prototype-v6.html |
| Recommended — 双列 Feed 预览 | looply-favourites-prototype-v6.html |
| 参考设计稿（APP） | looply-收藏与浏览历史-APP-v1.pen |

> 注：API 接口属于技术文档范畴，PRD 不含接口清单。后台数据获取、接口设计完全沿用「收藏与浏览历史 PRD v1.0」定义。

---

## 九、变更日志

### v1.1 · 2026-07-07

**§1（概述）**

- 子模块范围变更：移除 Saved Searches（本期不做），Recommended 从"占位"升级为本期实现的 Feed 模块。
- 配套原型更新为 v6。

**§2（页面框架）**

- §2.1 整体布局：页面结构从「子 Tab 切换」改为「概览页 + 全屏面板」双层结构。
- §2.2 子 Tab 栏规格 → 改为概览页区块结构：Wishlist 区块 / Recently Viewed 区块 / Recommended 区块，各含横向缩略卡片条或双列预览网格；新增降价强调条规格（绿色提示条 + 深链点击逻辑）。
- §2.3 与原独立页差异 → 改为全屏面板规格：定义面板三 Tab 切换（All / In Stock / Price Drop·On Sale）及 Tab 深链接规则。

**§3（需求详细描述）**

- §3.1.4 Wishlist 列表页：筛选区从「In Stock Only / All」两个 pill 改为三 Tab（All / In Stock / Price Drop）；进入默认 All tab，从降价强调条点击进入时激活 Price Drop tab。
- §3.2.4 Recently Viewed 列表页：新增三 Tab 筛选（All / In Stock / On Sale）；从降价强调条点击进入时激活 On Sale tab。
- §3.4 Saved Searches：改为"本期不做"，移除占位页，二期单独立项。
- §3.5 Recommended：从占位页改为双列瀑布流 Feed 展示规格，含商品卡片字段定义。

**§6（版本规划）**

- §6.1 当前版本范围对齐上述结构变更。
- §6.2 后续迭代：Saved Searches 改为单独立项；Recommended 二期接入个性化召回算法。

**§7（埋点）**

- 新增 `favourites_price_drop_banner_click`、`favourites_recommended_scroll`、`wishlist_price_drop_tab` 三个埋点事件；移除 `favourites_coming_soon_view`。

**§8（附录）**

- 设计稿索引全部更新为 v6 原型；移除 Saved Searches 和 Recommended 占位页条目。

**其他**

- Header 右侧图标描述修正：搜索 + 购物车（原为搜索 + 用户）。
