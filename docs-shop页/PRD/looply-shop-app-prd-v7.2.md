# Looply Shop 页 PRD v7.2

---

## 版本对照表

| PRD 版本 | 前端交互原型 | 后台配置原型 | 主要变更 |
|---|---|---|---|
| v1 | — | — | 初稿，含顶部横向 Tab |
| v2 | — | — | 简化结构，保留 Tab |
| v3 | — | `looply-shop导航-后台原型-v0.5-antd.html` | 去掉顶部 Tab，单层左侧导航 + 图文入口 + YMAL |
| v4 | `looply-shop-app-v0.3.html` | `looply-shop导航-后台原型-v1.0-antd.html` | 去掉 YMAL；命名体系对齐；引入全局维度 |
| v5 | `looply-shop-app-v0.3.html` | `looply-shop导航-后台原型-v1.0-antd.html` | 修正 Collection 归属为 CMS；去除"圆形"描述；image 改必填；字段枚举完整定义；Channel 枚举待确认备注；交互细节补全 |
| **v6** | **`looply-shop-app-v0.3.html`** | **`looply-shop页导航栏配置-后台原型-v0.1-antd.html`** | 后台原型更新；targetType 精简为 collection/external；引入 targetUrl；排序改为拖拽；删除前置条件改为"仅停用状态可删"；无数量上限；二级导航列表增加关联 Collection 和跳转链接列 |
| **v7** | **`looply-shop-app-v0.3.html`** | **`looply-shop页导航栏配置-后台原型-v0.1-antd.html`** | 引入两级/三级层级方案；正文仍保留旧分组模型，不能作为开发基线 |
| **v7.1** | **`looply-shop-app-v0.4.html`** | **`looply-shop页导航栏配置-后台原型-v0.2-antd.html`** | 正文、原型统一为 `levels / parentId` 模型；对齐全局 Tab 命名、Collection v0.22 依赖与多语言归属 |

---

## 一、概述

### 1.1 背景与目标

Shop 页是 Looply App 的核心商品入口页，承载二手奢侈品的分类导航功能。用户通过左侧导航选择品类，点击图文卡片直达对应 Collection 商品列表。

目标：提供清晰、快速的分类入口，让目标明确的买家以最少点击到达目标品类。

### 1.2 不做什么（明确边界）

- **不做商品推荐**：Shop 页定位是"分类入口"，不承载算法推荐或 Feed 流商品展示
- **不做搜索结果页**：搜索功能由 TopBar 触发，结果页独立
- **不做商品详情**：点击 Menu Item 跳转至目标落地页，商详页独立
- **不做 PC 端顶导**：PC 端 Navbar 配置独立管理，不在本文档范围内

### 1.3 用户角色

| 角色 | 说明 |
|---|---|
| 买家（前台） | 通过 Shop 页浏览分类、进入商品列表 |
| 运营（后台） | 通过 CMS > Shop页 > 导航配置管理 Navigation 和 Menu Items，控制前台展示内容 |

### 1.4 核心场景

1. 买家打开 App → 切换到 Shop Tab → 默认看到第一个 Navigation 下的所有 Menu Items → 点击某个图文卡片 → 进入对应落地页
2. 买家切换左侧导航 → 右侧 Menu Items 随之切换
3. 运营在 CMS 后台新增/调整 Navigation 和 Menu Items → 前台实时生效

### 1.5 全局页面流转

```
底部 TabBar（Shop 入口）
  └─→ Shop 页
        └─→ 点击图文卡片（Menu Item / L3 Item）→ 目标落地页（targetUrl）
```

### 1.6 术语说明

| 术语 | 含义 |
|---|---|
| Navigation | 左侧一级导航项（如"Bags"、"Jewelry"） |
| L2 Item | Navigation 下的二级导航项；两级模式下即图文卡片；三级模式下为纯文字分组标题 |
| L3 Item | 三级模式下 L2 分组标题之下的图文卡片，关联跳转目标 |
| Menu Item | 统称 L2 Item 和 L3 Item |
| targetType | 跳转目标类型：collection（关联合集）/ external（自定义链接）|
| targetUrl | 跳转目标路径，如 `/collections/bags` |
| Collection | CMS 后台定义的商品集合（对齐 Collection PRD v0.22）；Shop 仅保存 `collection_id`，并消费 Collection 返回的当前语言展示标题与 `url_slug`；targetType=collection 时系统根据 `url_slug` 自动填充 targetUrl |
| Market / Channel / Terminal | 全局配置维度，当前 Shop 页固定为 US / 美国官网商城（chn_us_001）/ app |
| levels | Navigation 的层级数；`2`=两级（L2 直接是图文卡片），`3`=三级（L2 为文字标题，L3 为图文卡片）；创建时选定，**不可修改** |

### 1.7 字段枚举完整定义

| 字段名 | 枚举值 | 说明 |
|---|---|---|
| `enabled` | `true`（启用）/ `false`（停用） | Navigation 和 Menu Item 统一使用布尔字段；区别于 Collection 的三态 `status`——导航项无草稿态，仅需启停 |
| `targetType` | `collection`（关联合集）/ `external`（自定义链接） | 跳转目标类型 |
| `market_id` | `US`（当前仅美国市场） | 对齐 Market 系统 `market_code` |
| `channel_id` | `chn_us_001`（美国官网商城） | 读商品中心渠道管理实体 |
| `terminal` | `app`（App 端） | 本文档固定值 |
| `order` | 正整数，升序 | 在当前维度下的排列顺序，由系统维护 |
| `levels` | `2`（两级）/ `3`（三级） | Navigation 层级数；创建时选定，**保存后不可修改** |
| `parentId` | 父级 Menu Item ID / `null` | L2 Item 的 parentId 为 null；L3 Item 的 parentId 为所属 L2 Item 的 ID |

### 1.8 多语言 / 多国家策略

当前版本以美国市场和英文源文为基线。Navigation 名称、L2 标题和叶子 Menu Item 名称属于动态业务内容，统一新建 Shop Navigation 翻译资源卡；固定页面、表单、校验、空态与反馈文案属于静态 UI 文案，进入对应 App/CMS message package；ID、排序、跳转地址和内部运营备注不翻译。

| 业务对象 | 业务字段 | 内容类别 | 卡片决策 | resourceType | 翻译中心路径 | fieldName | 展示面 | 语种/兜底 |
|---|---|---|---|---|---|---|---|---|
| Shop Navigation | 一级导航名称 | 动态业务内容 | 新建卡片 | `shop_navigation` | CMS 域 → Shop Navigation | `name` | App Shop 左侧导航、移动 Web Shop | 英文源文；目标语种缺失时回退英文源文 |
| Shop Menu Item | L2 标题、叶子卡片名称 | 动态业务内容 | 新建卡片 | `shop_menu_item` | CMS 域 → Shop Menu Item | `name` | App Shop 右侧内容区、移动 Web Shop | 英文源文；目标语种缺失时回退英文源文 |
| Shop UI | 固定 UI 文案 | 静态 UI 文案 | 不进业务资源卡 | — | App/CMS message package | `shop.*` / `cms.shop.*` | App、移动 Web、CMS | 按语言包规则 |

---

## 二、需求详细描述

### 2.1 页面整体布局

Shop 页由四个区域构成：

```
┌─────────────────────────────────┐
│           TopBar                │
├───────────┬─────────────────────┤
│           │                     │
│ 左侧       │   右侧内容区         │
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

**移动 Web**：移动 Web 复用 App Shop 的信息架构、内容层级、状态和交互；不采用传统 PC header/footer 作为页面结构。页面中的 Collection 跳转使用可抓取链接，Collection 的 canonical、分页、结构化数据、索引控制、sitemap 与面包屑由 Web/SEO 公共能力提供，Shop 不重复定义其实现。

### 2.2 TopBar

**元素（从左到右）**：
- Looply Logo
- 搜索框（居中，点击后展开为全宽输入态）
- 收藏图标（心形）
- 购物袋图标

TopBar 在 Shop 页的行为与 App 其他页面保持一致，本 PRD 不重复定义其交互。

### 2.3 左侧 Navigation

**展示规则**：
- 只展示 terminal=app、当前 market_id/channel_id 下 enabled=true 的 Navigation
- 按 order 字段升序排列
- 进入页面时默认选中第一个 enabled=true 的 Navigation

**激活态**：
- 当前选中项：左侧竖线高亮 + 背景色变化 + 文字颜色变化
- 激活态样式仅用于当前选中项

**交互**：
- 点击任意 Navigation 项 → 右侧内容区切换展示该 Navigation 下的 Menu Items
- App 端 Navigation 始终为分组（不支持直接跳转）

**空态**：所有 Navigation 均为 enabled=false 时，页面主体区域显示空态提示。

### 2.4 右侧内容区 — Menu Items 图文卡片列表

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

### 2.5 底部 TabBar

Tab 项：Home / Shop（当前激活）/ Favorites / Me。Shop Tab 保持激活态。TabBar 行为由全局规范定义，本 PRD 不重复定义。

---

## 三、依赖与风险

| 依赖方 | 依赖内容 | 关键要求 |
|---|---|---|
| CMS Collection 模块 | Menu Item 关联的 Collection 列表（collection_id / title / url_slug） | 需提供可搜索的 Collection 列表接口；Collection 删除时需通知导航模块标记关联失效 |
| 商品中心渠道管理 | channel_id 枚举来源（渠道实体列表） | Shop 导航配置的 channel_id 须读取商品中心渠道管理数据，不可硬编码 |
| Market 模块 | market_id 枚举来源（market_code 列表） | Shop 导航配置的 market_id 须与 Market 系统 market_code 保持一致 |
| 前端路由 | 点击 Menu Item 跳转到 targetUrl | targetUrl 所指路径需稳定；Collection url_slug 修改须同步更新关联 Menu Items |

**风险**：
- targetUrl 指向的目标页被删除或路由变更时，若前台未及时感知，用户点击会跳转失败；建议建立目标有效性检测机制
- channel_id 实际枚举依赖商品中心渠道管理数据，上线前需与商品系统团队确认渠道实体 ID

---

## 四、版本规划

### 当前版本（MVP）

- App 端 Shop 页：左侧 Navigation + 右侧 Menu Items 图文卡片列表
- 后台：Navigation 和 Menu Items 的 CRUD、拖拽排序、启停
- targetType：collection（关联合集，自动填充 URL）/ external（自定义链接）
- 全局维度：market_id / channel_id 单选筛选，terminal 固定 app

### 后续迭代方向

- Navigation 支持图标图片（当前纯文字）
- Menu Items 支持视频封面（当前仅图片）
- targetType 扩展：支持 brand 页、campaign 页
- 多市场扩展（当前仅 US）
- 配置预览增强：手机预览实时反映拖拽排序结果

---

## 五、附录

### A.1 设计稿索引

| 页面/功能 | 端 | 原型文件 |
|---|---|---|
| Shop 页（App 端整体） | App 前台 | `looply-shop-app-v0.3.html` |
| 后台导航配置（Navigation 管理） | CMS 后台 | `looply-shop页导航栏配置-后台原型-v0.1-antd.html` |
| 后台导航配置（Menu Items 管理） | CMS 后台 | `looply-shop页导航栏配置-后台原型-v0.1-antd.html` |

### A.2 UI 规范参考

> 具体数值以设计稿为准，此处为当前原型实现的参考值。

**左侧 Navigation**：

| 属性 | 参考值 |
|---|---|
| 宽度 | 70px |
| 背景色 | `#F5F5F5` |
| 右侧分隔线 | 1px solid `#EBEBEB` |
| 字号 | 9px |
| 激活态背景 | `#FFFFFF` |
| 激活态左侧竖线 | 3px，颜色 `#7C3AED` |
| 激活态文字色 | `#7C3AED`，font-weight: 600 |
| 未激活文字色 | `#6B7280` |

**右侧图文卡片网格**：

| 属性 | 参考值 |
|---|---|
| 列数 | 3 列 |
| 图片区高宽比 | 1:1 |
| 图片填充方式 | object-fit: contain |
| 文字标签字号 | 8px |
| 文字最大行数 | 2 行 |

---

## 六、版本变更记录

> 相对于上一版本：`looply-shop-app-prd-v5.md`

### v6 变更内容（2026-07-06）

**变更 1：后台原型文件更新**
- 变更类型：修改
- 变更内容：后台配置原型文件从 `looply-shop导航-后台原型-v1.0-antd.html` 更新为 `looply-shop页导航栏配置-后台原型-v0.1-antd.html`；该文件为 App 端 Shop 页专属后台原型，从 v0.3 拆分独立
- 变更原因：原型已拆分为 App 端和 PC 端两个独立文件，分别维护

**变更 2：targetType 精简为两种，引入 targetUrl**
- 变更类型：修改
- 变更内容：Menu Items 的跳转目标配置从 v5 的 `collectionId` 直接关联 Collection，改为 `targetType`（collection / external）+ `targetUrl` 两字段组合；collection 类型时系统自动填充 targetUrl（只读）；external 类型时运营手动填写 URL
- 变更原因：需要支持非 Collection 目标页的跳转（如品牌页、活动页临时链接）；targetType 枚举当前精简为 collection 和 external，后续按需扩展

**变更 3：排序方式从"上下箭头"改为"拖拽排序"**
- 变更类型：修改
- 变更内容：Navigation 和 Menu Items 的排序操作，从点击上/下箭头按钮改为行首拖拽手柄（drag handle）拖拽排序；手机预览区实时反映拖拽后的新顺序
- 变更原因：拖拽排序在数量多时操作效率更高，原型已实现

**变更 4：删除前置条件改为"仅停用状态可删"**
- 变更类型：修改
- 变更内容：Navigation 和 Menu Items 的删除操作，从"任何状态均可删除"改为"仅当 enabled=false（停用状态）时才能操作删除"；启用状态下删除按钮不展示
- 变更原因：防止运营误删线上展示中的导航项；必须先停用、确认前台不展示后，才允许执行删除

**变更 5：Navigation 和 Menu Items 数量无上限**
- 变更类型：修改
- 变更内容：明确 Navigation 和每个 Navigation 下的 Menu Items 均无数量上限；列表无分页，窗口内无限滚动
- 变更原因：业务无需限制数量，由运营自行管理

**变更 6：后台入口路径明确**
- 变更类型：新增
- 变更内容：后台模块入口路径明确为 CMS > Shop页 > 导航配置；Breadcrumb 路径与左侧菜单结构一致
- 变更原因：原 v5 未明确后台入口路径

**变更 7：二级导航列表新增"关联 Collection"和"跳转链接"列**
- 变更类型：新增
- 变更内容：Menu Items 管理页（下钻后的二级导航列表）新增两列：关联 Collection（展示合集名称标签）和跳转链接（展示 targetUrl，可点击）
- 变更原因：运营需要在列表页直接确认每条二级导航的跳转目标，无需逐条点击编辑查看

**变更 8：一级导航列表"二级导航数"改为展示已启用数量**
- 变更类型：修改
- 变更内容：一级导航列表中"二级导航数"列改为"二级导航数（已启用）"，只统计并展示 enabled=true 的 Menu Items 数量，纯数字显示，不可点击
- 变更原因：运营关心的是用户实际能看到的数量，停用的条目不应计入

**变更 9：不做什么边界补充**
- 变更类型：新增
- 变更内容：1.2 不做什么中新增"不做 PC 端顶导"，明确 PC 端 Navbar 配置独立管理，不在本文档范围
- 变更原因：PC 端顶导已由 `looply-导航栏-PRD-v1.0.md` 单独定义，避免与本文档范围混淆

---

### v7 变更内容（2026-07-06）

**变更 1：Navigation 新增分组功能（grouped 字段）**
- 变更类型：新增
- 变更内容：Navigation 新增 `grouped` 布尔字段（默认 false）；创建/编辑 Navigation 时增加"支持分组"单选（是/否）；一级导航列表新增"组数"列（grouped=false 显示"—"；grouped=true 显示分组数，存在未分组 Menu Item 时数字标橙附 ⚠）；名称列在有未分组 Menu Item 时显示 ⚠ 有未分组警示
- 变更原因：二级导航数量较多时需要分组展示，方便运营管理和用户浏览

**变更 2：Menu Item 新增 groupId 字段**
- 变更类型：新增
- 变更内容：Menu Item 新增 `groupId` 字段（条件必填：所属 Navigation grouped=true 时必填）；新建/编辑 Menu Item 时，若 Navigation 开启分组，表单新增"所属分组"必填字段，可选已有分组或内联新建；二级导航管理页新增"所属分组"列（grouped=true 时展示，groupId 为空则显示 ⚠ 未分配）
- 变更原因：配合 Navigation 分组功能，记录每个 Menu Item 的归属分组

**变更 3：Nav Group 实体定义**
- 变更类型：新增
- 变更内容：新增 2.6.4 Nav Group 管理章节；Nav Group 字段：id / navId / name / order；命名规则：最多 30 字符，同一 Navigation 下不可重名；创建入口：Menu Item 表单内联创建；随 Navigation 删除一同删除
- 变更原因：分组是独立实体，需明确字段定义和生命周期

**变更 4：全有或全无分组约束**
- 变更类型：新增
- 变更内容：一个 Navigation 下，要么所有 Menu Items 都有 groupId，要么全部没有；grouped=true 时若有 groupId 为空的 Menu Item，后台列表和导航概览页均显示 ⚠ 警示，但不阻止保存
- 变更原因：混合状态在前台渲染上无法预期，强约束保证展示一致性

**变更 5：grouped false→true 时弹窗警告**
- 变更类型：新增
- 变更内容：编辑 Navigation 将 grouped 从 false 改为 true 保存后，若该 Navigation 下已有 Menu Items，立即弹窗提示运营去分配分组；提供"去分配分组"（跳转至该导航二级导航管理页）和"稍后处理"两个操作
- 变更原因：防止运营开启分组后遗忘分配，导致警示长期存在

---

### v7.1 变更内容（2026-08-06）

**变更 1：层级模型正文收口**
- 变更类型：修正
- 变更内容：Navigation 以创建后锁定的 `levels` 表示两级或三级；Menu Item 以 `parentId` 表示 L2/L3 父子关系。删除 `grouped`、`groupId` 与 Nav Group 的字段、操作和管理章节。
- 变更原因：使正文与 v7 的目标层级方案及后台原型一致。

**变更 2：前台原型同步**
- 变更类型：修正
- 变更内容：前端原型升级为 v0.4，移除 `You May Also Like` 商品推荐区，底部 Tab 名称改为 `Favorites`、`Me`。
- 变更原因：Shop 仅承担分类入口，且需对齐已确认的全局 Tab 命名。

**变更 3：跨模块与多语言对齐**
- 变更类型：修正
- 变更内容：Collection 依赖更新为 v0.22；补充 Navigation/Menu Item 动态内容、静态 UI 文案和不翻译字段的归属规则；补充移动 Web 与 App 的一致体验及 SEO 公共依赖。
- 变更原因：消除旧版 v0.17 字段描述与全局多语言、移动 Web 基线的不一致。

---

## 七、下个版本修改需求

本节为基于 v7.1 的用户端增量修改；本节未涉及的规则保持不变。

### 7.1 新增横向大图展示样式

1. 现有图文卡片样式命名为「方形图卡」，展示规则保持不变。
2. Shop 右侧内容区新增「横向大图」样式，按单列纵向展示。
3. 每个一级导航下只展示后台为该导航配置的一种样式。
4. 两级导航展示二级导航入口；三级导航按二级分组展示三级导航入口。
5. 横向大图的末级导航名称显示在图片中央：两级读取二级导航名称，三级读取三级导航名称。
