# 导航栏配置 PRD v1.0

---

## 一、概述

### 1.1 背景与目标

Looply 的商品分类导航在 App 端和 PC 端结构本质相同：均是通过若干导航入口（一级分类），引导用户找到目标商品。原"Shop页PRD"仅覆盖 App 端，现将两端统一抽象为**导航栏配置**，由 CMS 后台统一管理，按 terminal（终端）区分 App 和 PC 两套展示逻辑。

**目标**：通过统一的导航栏配置，让运营在一个后台模块内分别管理 App 端分类导航（Shop页）和 PC 端顶部导航（Navbar），实现前台实时生效。

**前台对应关系**：
- `terminal = app`：App 端 Shop 页（底部 TabBar 第二项 Shop 入口）
- `terminal = web`：PC 端顶部 Navbar 的导航区域

### 1.2 不做什么（明确边界）

- **不做商品推荐**：导航配置定位是"分类入口"，不承载算法推荐或 Feed 流
- **不做搜索**：搜索功能由独立模块管理，导航栏中的搜索框入口不在本 PRD 范围内
- **不做 Navbar 右侧图标区**：Market/Language 切换、购物袋、收藏、账户图标的交互逻辑由各自独立模块定义
- **不做商品详情和商品列表页**：点击导航项跳转后的目标页面不在本 PRD 范围内
- **不做 Announcement Bar 内容配置**：公告栏内容由独立 Banner/公告模块管理

### 1.3 用户角色

| 角色 | 说明 |
|---|---|
| 买家（前台 App 端） | 通过 Shop 页左侧导航找到目标品类，点击图文卡片进入商品列表 |
| 访客/买家（前台 PC 端） | 通过顶部 Navbar 一级导航 hover/点击进入目标分类 |
| 运营（后台） | 通过 CMS → 导航栏配置管理两端的 Navigation 和 Menu Items |

### 1.4 核心场景

**App 端（Shop 页）**：
1. 买家切换到 Shop Tab → 默认看到第一个 Navigation 下的所有 Menu Items 图文卡片
2. 买家点击左侧 Navigation 项 → 右侧切换为该导航下的图文卡片列表
3. 买家点击图文卡片 → 跳转到对应目标页（商品列表 / 品牌页 / 活动页）

**PC 端（顶导 Navbar）**：
1. 访客/买家 hover 顶部导航项（isLeaf=false） → 展开下拉子菜单面板
2. 访客/买家点击顶部导航项（isLeaf=true） → 直接跳转目标页，无子菜单
3. 访客/买家点击子菜单链接 → 跳转到对应目标页

**后台**：
1. 运营切换 terminal（App/Web）→ 独立管理各端 Navigation 和 Menu Items
2. 运营新增/调整 Navigation 和 Menu Items → 前台实时生效

### 1.5 全局页面流转

**App 端**：
```
底部 TabBar（Shop 入口）
  └─→ Shop 页（左侧Navigation + 右侧Menu Items图文卡片）
        └─→ 点击图文卡片 → 目标落地页（targetUrl）
```

**PC 端**：
```
PC 顶部 Navbar（导航区域）
  ├─→ Navigation（isLeaf=true）→ 点击直接跳转目标落地页
  └─→ Navigation（isLeaf=false）→ hover展开子菜单
        ├─→ Menu Items L1（全叶子）→ 2列文字下拉，点击跳转
        └─→ Menu Items L1（含分组）→ 全宽 Mega Panel，按分组标题 + L2 链接列表，点击L2跳转
```

### 1.6 术语说明

| 术语 | 含义 |
|---|---|
| Navigation | 一级导航项。App端：左侧垂直列表；PC端：顶部水平 Navbar 链接 |
| Menu Items | Navigation 下的子导航项。App端：图文卡片（L1，单层）；PC端：L1（下拉列表或分组标题）+ L2（Mega Panel链接，可选）|
| L1 | Menu Items 的第一层（parentId = null） |
| L2 | Menu Items 的第二层（parentId = L1的id），仅 PC 端支持 |
| isLeaf | 是否为叶子节点。true = 有目标URL、点击跳转；false = 无URL、触发展开子菜单 |
| targetUrl | 点击跳转的目标路径，如 `/collections/bags` |
| targetType | 目标页类型：collection / brand / campaign / external |
| terminal | 终端类型：app（App端）/ web（PC端） |
| Market / Channel | 全局配置维度，与 terminal 组合确定独立配置空间 |

### 1.7 字段枚举完整定义

| 字段名 | 枚举值 | 说明 |
|---|---|---|
| `terminal` | `app`（App端）/ `web`（PC端） | 区分两套配置空间 |
| `enabled` | `true`（启用）/ `false`（停用） | 前台是否展示 |
| `isLeaf` | `true`（叶子，有URL）/ `false`（分组，无URL） | 是否直接跳转 |
| `targetType` | `collection` / `brand` / `campaign` / `external` | 目标页类型 |
| `market` | `US`（United States） | ⚠️ 完整枚举待市场模块 PRD 确认 |
| `channel` | `official`（官方站） | ⚠️ 完整枚举待市场模块 PRD 确认 |
| `order` | 正整数，升序 | 在当前维度下的排列顺序 |

> ⚠️ market / channel 的完整枚举须以市场模块 PRD 和数据表设计为准，上线前需交叉核对。

### 1.8 多语言 / 多国家策略

当前阶段仅支持美国市场（market = US）、英文界面。Navigation 和 Menu Item 的名称由运营在后台直接填写英文，不做多语言翻译处理。

---

## 二、需求详细描述

### 2.1 App 端前台展示（Shop 页）

**原型参考**：`looply-shop-app-v0.3.html`

#### 2.1.1 页面整体布局

Shop 页由四个区域构成：

```
┌─────────────────────────────────┐
│           TopBar                │
├───────────┬─────────────────────┤
│           │                     │
│  左侧      │   右侧内容区         │
│Navigation │   Menu Items 卡片列表 │
│           │                     │
├───────────┴─────────────────────┤
│           底部 TabBar            │
└─────────────────────────────────┘
```

- TopBar：固定在顶部，不随页面滚动
- 左侧 Navigation：固定宽度，内容超出时可独立滚动，不影响右侧
- 右侧内容区：宽度自适应（占剩余空间），内容超出时可独立滚动
- 底部 TabBar：固定在底部，不随页面滚动

#### 2.1.2 TopBar

**元素（从左到右）**：
- Looply Logo
- 搜索框（居中，点击后展开为全宽输入态）
- 收藏图标（心形）
- 购物袋图标

TopBar 在 Shop 页的行为与 App 其他页面保持一致，本 PRD 不重复定义其交互。

#### 2.1.3 左侧 Navigation

**展示规则**：
- 只展示 terminal=app、当前 Market/Channel 下 enabled=true 的 Navigation
- 按 order 字段升序排列
- 进入页面时默认选中第一个 enabled=true 的 Navigation

**激活态**：
- 当前选中项：左侧竖线高亮 + 背景色变化 + 文字颜色变化
- 激活态样式仅用于当前选中项

**交互**：
- 点击任意 Navigation 项 → 右侧内容区切换展示该 Navigation 下的 Menu Items
- App 端 Navigation 始终为分组（isLeaf 固定 false），不支持直接跳转

**空态**：所有 Navigation 均为 enabled=false 时，页面主体区域显示空态提示。

#### 2.1.4 右侧内容区 — Menu Items 图文卡片列表

**标题行**：展示当前激活 Navigation 的名称，位于卡片列表上方。

**图文卡片网格**：
- 固定 3 列布局
- 只展示 enabled=true 的 Menu Items
- 按 order 字段升序排列（排序仅在同一 Navigation 内有效）

**图文卡片单项元素**：
- 图片区域：1:1 比例，contain 填充
- 图片下方：Menu Item 名称（最多 2 行，超出截断）

**点击交互**：
- 点击图文卡片 → 跳转到该 Menu Item 的 `targetUrl`

**空态**：当前激活 Navigation 下没有 enabled=true 的 Menu Item 时，右侧显示空态提示"暂无分类入口"。

#### 2.1.5 底部 TabBar

Tab 项：Home / Shop（当前激活）/ Favourites / Account。Shop Tab 保持激活态。TabBar 行为由全局规范定义，本 PRD 不重复定义。

---

### 2.2 PC 端前台展示（顶导 Navbar）

**原型参考**：`首页PC端原型v1.0.pen`（NavbarRow 及顶导交互示意区域）

#### 2.2.1 整体结构

PC 端顶导由上下两行固定吸顶组成：

```
┌─────────────────────────────────────────────────────────┐
│  AnnouncementBar（40px，公告栏）                           │
├─────────────────────────────────────────────────────────┤
│  Navbar（72px）                                          │
│  NavLeft: Logo + 导航项列表（水平）                        │
│  NavCenter: 搜索框                                       │
│  NavRight: Market/Language / 收藏 / 购物袋 / 账户          │
└─────────────────────────────────────────────────────────┘
```

页面向下滚动后：AnnouncementBar 消失，Navbar sticky 吸顶。

本 PRD 仅定义 **NavLeft 中的导航项列表**（Navigation + 子菜单展开）。AnnouncementBar、搜索框、NavRight 各图标由独立模块定义。

#### 2.2.2 Navigation 展示规则（水平导航项列表）

- 只展示 terminal=web、当前 Market/Channel 下 enabled=true 的 Navigation
- 按 order 字段升序排列，在 NavLeft 中水平排列
- 不设默认激活状态（与 App 端不同，PC 端没有"选中某个一级导航"的持久态）

**文字样式**：字号 13px，normal weight，letter-spacing 0.2px；hover/active 态变色（主色 `#6432FC`）

#### 2.2.3 Navigation 点击/hover 交互

根据 Navigation 的 `isLeaf` 值，行为分为三种：

**情况一：Navigation isLeaf = true（叶子节点）**
- 点击直接跳转到 `targetUrl`
- hover 无下拉面板，仅文字高亮

**情况二：Navigation isLeaf = false，其下 L1 Menu Items 全部为 isLeaf=true（叶子）**
- hover Navigation 项 → 展开文字下拉卡片（小面板）
- 面板内 2 列平铺所有 L1 Menu Items 的文字链接
- 点击任意 L1 项 → 跳转到该项的 `targetUrl`
- 鼠标移出 Navigation 项及面板区域 → 面板收起

**情况三：Navigation isLeaf = false，其下 L1 Menu Items 中包含 isLeaf=false 的分组**
- hover Navigation 项 → 展开全宽 Mega Panel（覆盖 Navbar 下方区域）
- Mega Panel 中按 L1 分组标题排列：
  - L1 isLeaf=false：显示为分组标题（不可点击，或点击无效）
  - L1 isLeaf=true：显示为独立链接行（可点击跳转）
  - 每个 isLeaf=false 的 L1 下方，列出其所有 L2 Menu Items 的文字链接（4列布局）
- 点击任意 L2 项 → 跳转到该 L2 的 `targetUrl`
- 鼠标移出 Navigation 项及 Mega Panel 区域 → 面板收起

**面板背景与遮罩**：下拉面板弹出时，页面正文区域有半透明遮罩（`rgba(0,0,0,0.15)`），遮罩点击收起面板。

**空态**：Navigation 下没有 enabled=true 的 L1 Menu Items 时，hover 无子菜单弹出（与 isLeaf=true 行为相同，直接处理为不展开）。

---

### 2.3 后台配置能力（CMS → 导航栏配置）

**后台原型参考**：`looply-导航栏配置-后台原型-v0.3-antd.html`

#### 2.3.1 全局维度（最顶层筛选）

Market / Channel / Terminal 是后台的最顶层配置维度，三者组合确定一个独立的配置空间。切换维度后，Navigation 和 Menu Items 列表同步切换展示。

| 维度 | 当前已知枚举值 | 备注 |
|---|---|---|
| market（市场） | US（United States） | ⚠️ 完整枚举待市场模块 PRD 确认 |
| channel（渠道） | official（官方站） | ⚠️ 完整枚举待市场模块 PRD 确认 |
| terminal（终端） | app（📱 App）/ web（🖥 Web） | 本模块核心区分维度 |

- 每个维度单选，无"全部"选项
- terminal 切换决定后台展示的字段和规则差异（见 2.3.2 和 2.3.3）

#### 2.3.2 Navigation 管理

**功能描述**：运营管理当前 terminal 下的一级导航列表。

**字段定义**：

| 字段名 | 类型 | 必填 | App端 | PC端 | 说明 |
|---|---|---|---|---|---|
| `name` | 文本 | 是 | ✓ | ✓ | 前台展示名称；最大字符数以设计规范为准，输入框实时显示剩余字符数，超出不允许继续输入 |
| `enabled` | 枚举 | 是 | ✓ | ✓ | `true`（启用）/`false`（停用）；默认 true |
| `order` | 整数 | 自动 | ✓ | ✓ | 在当前维度下的排列顺序，由系统维护 |
| `market` | 字符串 | 自动 | ✓ | ✓ | 继承自全局 market，创建后不可修改 |
| `channel` | 字符串 | 自动 | ✓ | ✓ | 继承自全局 channel，创建后不可修改 |
| `terminal` | 字符串 | 自动 | `app` | `web` | 继承自全局 terminal，创建后不可修改 |
| `isLeaf` | 布尔 | 是 | 固定 false | 是/否 | App端始终false（Navigation不支持直接跳转）；PC端运营选择 |
| `targetUrl` | 字符串 | 条件必填 | 无此字段 | isLeaf=true时必填 | 点击跳转目标路径 |
| `targetType` | 枚举 | 条件必填 | 无此字段 | isLeaf=true时必填 | `collection` / `brand` / `campaign` / `external` |

**操作能力**：

| 操作 | 规则 |
|---|---|
| 新增 | 名称必填；market/channel/terminal 自动继承全局维度；PC端需选择 isLeaf，isLeaf=true时需填 targetUrl 和 targetType |
| 编辑 | 可修改名称、enabled、isLeaf（PC端）、targetUrl、targetType；market/channel/terminal 不可修改 |
| 删除 | 同时删除其下所有 Menu Items；删除前弹窗提示："将同时删除该 Navigation 下的 N 个 Menu Items，此操作不可恢复"，展示受影响 Menu Items 数量，点击确认后执行 |
| 排序 | 上下箭头调整顺序，决定前台展示顺序 |
| 启停 | 切换 enabled；停用后前台不展示该 Navigation |

**去重规则**：同一 market/channel/terminal 下，Navigation name 不可重复；字母大小写不同视为同一名称（如"Bags"与"bags"判定为重复）；提交时校验，重复则提示错误，不关闭表单。

**逆向链路（删除）**：删除 Navigation 时，其下所有 Menu Items（含L1和L2）一并删除，不可恢复；删除弹窗需展示将被删除的 Menu Items 总数量。

**逆向链路（停用）**：停用 Navigation 后，前台不展示该项；其下 Menu Items 不受影响，重新启用后恢复显示。PC端停用一级导航后，hover 不触发子菜单。

#### 2.3.3 Menu Items 管理

**功能描述**：运营管理 Navigation 下的子导航项列表。App端和PC端字段有差异，后台切换 terminal 后展示对应字段集。

**字段定义（App端，terminal=app）**：

| 字段名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `navId` | 关联 | 是 | 归属的 Navigation；新建时手动选择，编辑时不可修改 |
| `name` | 文本 | 是 | 图片下方展示文字；最大字符数以设计规范为准，输入框实时显示剩余字符数 |
| `image` | 图片 | 是 | 1:1 比例图片；未上传不允许提交 |
| `targetType` | 枚举 | 是 | `collection` / `brand` / `campaign` / `external` |
| `targetUrl` | 字符串 | 是 | 点击跳转目标路径，如 `/collections/bags` |
| `enabled` | 枚举 | 是 | `true`（启用）/`false`（停用）；默认 true |
| `order` | 整数 | 自动 | 在所属 Navigation 内的排列顺序，由系统维护 |

> App端 Menu Items 始终为叶子节点（isLeaf 固定 true），不支持 parentId（无 L2），无需运营填写。

**字段定义（PC端，terminal=web）**：

| 字段名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `navId` | 关联 | 是 | 归属的 Navigation（L1）或间接归属（L2）；创建时选择，编辑时不可修改 |
| `parentId` | 关联 | 条件 | L1 时为 null；L2 时必填，选择所属 L1 |
| `name` | 文本 | 是 | 前台展示的链接文字或分组标题 |
| `isLeaf` | 布尔 | 是 | true = 叶子（有URL，可点击跳转）；false = 分组标题（无URL，不可跳转） |
| `targetType` | 枚举 | 条件必填 | isLeaf=true时必填；`collection` / `brand` / `campaign` / `external` |
| `targetUrl` | 字符串 | 条件必填 | isLeaf=true时必填；点击跳转目标路径 |
| `enabled` | 枚举 | 是 | `true`（启用）/`false`（停用）；默认 true |
| `order` | 整数 | 自动 | 在所属 Navigation/L1 下的排列顺序，由系统维护 |

> PC端无 `image` 字段。L2 Menu Items 的 isLeaf 固定为 true（L2 不可再分组）。

**两端字段对比**：

| 字段 | App端（terminal=app） | PC端（terminal=web） |
|---|---|---|
| `image` | 必填（图文卡片） | 无此字段 |
| `parentId` | 固定 null（单层，无L2） | L1为null，L2填L1的id |
| `isLeaf` | 固定 true | 运营选择（L2固定true） |
| `targetUrl` | 必填 | isLeaf=true时必填 |
| `targetType` | 必填 | isLeaf=true时必填 |

**操作能力**：

| 操作 | App端 | PC端 |
|---|---|---|
| 新增 | 选Navigation，填名称、上传图片（必填）、选targetType、填targetUrl；全部填写后可提交 | 选Navigation，选层级（L1/L2），填名称，选isLeaf；isLeaf=true时填targetType、targetUrl |
| 编辑 | market/channel/terminal/Navigation 不可修改；名称、图片、targetType、targetUrl、enabled 可改 | market/channel/terminal/Navigation/parentId 不可修改；名称、isLeaf、targetType、targetUrl、enabled 可改 |
| 删除 | 仅删除该 Menu Item，不影响其他；弹窗确认"删除后不可恢复" | L1删除时同时删除其下所有L2；弹窗提示"将同时删除 N 个子菜单项，此操作不可恢复"；L2仅删除自身 |
| 排序 | 上下箭头；仅在同一 Navigation 内有效 | 上下箭头；L1在Navigation内有效，L2在L1内有效；不可跨层级排序 |
| 启停 | 切换 enabled；停用后前台不展示该图文卡片 | 切换 enabled；L1停用后前台不展示该项及其所有L2；L2停用后仅隐藏自身 |

**搜索与筛选**：
- 按 Navigation 筛选：下拉选择，范围为当前 terminal 下的 Navigation 列表；可清空（清空后展示全部）
- 按状态筛选：启用 / 停用 / 全部
- PC端额外：按层级筛选（L1 / L2 / 全部）
- 搜索：Menu Item name 模糊匹配

**去重规则**：同一 Navigation 下（L1之间、同一L1下的L2之间），name 不可重复；字母大小写不同视为同一名称；不同 Navigation 之间允许同名。提交时校验，重复则提示错误，不关闭表单。

**逆向链路（L1删除/停用）**：
- L1被删除 → 其下所有 L2 一并删除，不可恢复；弹窗展示将被删除的 L2 数量
- L1被停用 → 前台 Mega Panel 中不展示该分组及其 L2；L2 不受影响，重新启用后恢复

**逆向链路（Collection/目标页删除）**：targetUrl 指向的 Collection/页面在系统内被删除时：
- 后台 Menu Items 列表提示"⚠️ 目标页已失效（targetUrl 已不存在）"
- 前台：App端 该图文卡片仍展示但点击跳转会404；PC端 该链接项仍展示但跳转会404
- 运营需手动修正 targetUrl 或停用该 Menu Item

---

## 三、依赖与风险

| 依赖方 | 依赖内容 | 关键要求 |
|---|---|---|
| CMS Collection 模块 | App端 Menu Items 关联的 Collection（id / name / slug） | 需提供可搜索的 Collection 列表接口；Collection 删除时通知导航栏模块标记关联失效 |
| 品牌模块 | PC端 targetType=brand 时的品牌页路径 | 品牌 slug 需稳定；品牌下线时需通知导航栏标记目标失效 |
| 市场模块 | market / channel 完整枚举定义 | 导航栏配置的维度枚举必须与市场模块 PRD 和数据表保持一致，上线前需交叉核对 |
| 前端路由 | 点击后跳转到 targetUrl | targetUrl 所指路径需稳定；修改路由结构须同步更新所有相关 Menu Items |
| PC端 Navbar 布局 | Navigation 项数量影响 Navbar 水平空间 | 运营配置的 Navigation 数量过多时，前端需有截断/省略方案（待设计确认） |

**风险**：
- targetUrl 指向的目标页被删除或路由变更时，若前台未及时感知，用户点击会跳转失败；建议建立目标有效性检测机制
- market/channel 枚举尚未由市场模块 PRD 最终确认，开发前需对齐
- PC端 Navigation 项目数量过多时，Navbar 水平空间不足，展示逻辑（截断/折叠）需设计确认

---

## 四、版本规划

### 当前版本（MVP）

- App端（terminal=app）：Navigation 竖排 + Menu Items 图文卡片，CRUD、排序、启停
- PC端（terminal=web）：Navigation 水平排列 + 最多2层 Menu Items（L1 + L2），CRUD、排序、启停
- 后台统一配置界面，按 terminal 分组管理
- targetType 支持：collection / brand / campaign / external
- 全局维度：Market / Channel / Terminal 单选筛选

### 后续迭代方向

- Navigation 支持图标图片（当前纯文字）
- App端 Menu Items 支持视频封面（当前仅图片）
- 多市场扩展（当前仅 US）
- 配置预览增强：PC端实时预览子菜单展开效果
- targetType 扩展：支持搜索词直达（`search://{keyword}`）

---

## 五、附录

### A.1 设计稿索引

| 页面/功能 | 端 | 原型文件 |
|---|---|---|
| Shop 页（App端整体） | App | `looply-shop-app-v0.3.html` |
| Navbar 默认态 | PC | `首页PC端原型v1.0.pen` → 帧「PC 首页原型稿 v1.0」→ NavbarRow |
| Navbar 一级导航激活态 | PC | `首页PC端原型v1.0.pen` → 帧「顶导交互示意（左侧导航）」→ Nav-L1 |
| Navbar 二级导航展开（小卡片） | PC | `首页PC端原型v1.0.pen` → 帧「顶导交互示意（左侧导航）」→ Nav-L2 |
| Navbar 三级导航展开（Mega Panel）| PC | `首页PC端原型v1.0.pen` → 帧「顶导交互示意（左侧导航）」→ Nav-L3 |
| 后台导航栏配置（Navigation管理） | 后台 | `looply-导航栏配置-后台原型-v0.3-antd.html` |
| 后台导航栏配置（Menu Items管理）| 后台 | `looply-导航栏配置-后台原型-v0.3-antd.html` |

---

## 六、版本变更记录

> 相对于上一版本：`looply-shop-app-prd-v5.md`

### v1.0 变更内容（2026-07-03）

**变更 1：文档重命名与范围扩大**
- 变更类型：大版本重写
- 变更内容：文档由「Looply Shop 页 PRD」改为「导航栏配置 PRD」；覆盖范围从 App 端单端扩展至 App端 + PC端双端
- 变更原因：App端 Shop 页导航与 PC 端顶导结构本质相同，均为"多级导航入口"，统一由 CMS 后台管理，抽象为通用导航栏配置

**变更 2：引入 terminal 维度**
- 变更类型：新增
- 变更内容：新增 terminal 字段（app / web）作为 Navigation 和 Menu Items 的区分维度；后台配置界面按 terminal 切换
- 变更原因：两端数据独立管理，terminal 是唯一区分键

**变更 3：PC端前台展示规则（全新章节 2.2）**
- 变更类型：新增
- 变更内容：新增 PC 端 Navbar 展示逻辑，包含三种 Navigation 交互情况（直接跳转 / 二级文字下拉 / 全宽 Mega Panel）；定义 L1+L2 两层子菜单规则
- 变更原因：PC 端顶导需求全新接入

**变更 4：引入 isLeaf 字段**
- 变更类型：新增
- 变更内容：Navigation 和 PC端 Menu Items 新增 isLeaf 字段（true=叶子可跳转 / false=分组展开）；App端 Navigation 固定 false，App端 Menu Items 固定 true
- 变更原因：区分"直接链接"和"展开子菜单"两种行为

**变更 5：targetType / targetUrl 替换 collectionId + slug**
- 变更类型：修改
- 变更内容：原 App端字段 `collectionId` 和 Collection 的 slug 跳转逻辑，统一改为 `targetType`（collection/brand/campaign/external）+ `targetUrl`（完整路径）；适用于两端
- 变更原因：PC端需支持多种目标页类型（不仅限于 Collection），统一字段设计减少两套逻辑

**变更 6：PC端 Menu Items 支持L2（两层子菜单）**
- 变更类型：新增
- 变更内容：PC端 Menu Items 新增 `parentId` 字段，支持 L1 → L2 两层结构；App端 parentId 固定 null（不支持 L2）
- 变更原因：PC端 Mega Panel 需要按分组展示，需要 L2 层级

**变更 7：Menu Items 无 image 字段（PC端）**
- 变更类型：修改
- 变更内容：PC端 Menu Items 不含 image 字段；image 字段仅 App端 Menu Items 保留且必填
- 变更原因：PC端导航为纯文字链接，不使用图片
