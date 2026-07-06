# Looply Shop 页 PRD v5

---

## 版本对照表

| PRD 版本 | 前端交互原型 | 后台配置原型 | 主要变更 |
|---|---|---|---|
| v1 | — | — | 初稿，含顶部横向 Tab |
| v2 | — | — | 简化结构，保留 Tab |
| v3 | — | `looply-shop导航-后台原型-v0.5-antd.html` | 去掉顶部 Tab，单层左侧导航 + 图文入口 + YMAL |
| v4 | `looply-shop-app-v0.3.html` | `looply-shop导航-后台原型-v1.0-antd.html` | 去掉 YMAL；命名体系对齐；引入全局维度 |
| **v5** | **`looply-shop-app-v0.3.html`** | **`looply-shop导航-后台原型-v1.0-antd.html`** | 修正 Collection 归属为 CMS；去除"圆形"描述；image 改必填；字段枚举完整定义；Channel 枚举待确认备注；交互细节补全 |

---

## 一、概述

### 1.1 背景与目标

Shop 页是 Looply App 的核心商品入口页，承载二手奢侈品的分类导航功能。用户通过左侧导航选择品类，点击图文卡片直达对应 Collection 商品列表。

目标：提供清晰、快速的分类入口，让目标明确的买家以最少点击到达目标品类。

### 1.2 不做什么（明确边界）

- **不做商品推荐**：Shop 页定位是"分类入口"，不承载算法推荐、Feed 流商品展示（You May Also Like 已从本页移除，属于独立 Feed 模块范畴）
- **不做搜索结果页**：搜索功能由 TopBar 触发，结果页独立
- **不做商品详情**：点击 Menu Item 跳转至 Collection 商品列表，商详页独立

### 1.3 用户角色

| 角色 | 说明 |
|---|---|
| 买家（前台） | 通过 Shop 页浏览分类、进入商品列表 |
| 运营（后台） | 通过 CMS 后台配置 Navigation 和 Menu Items，控制前台展示内容 |

### 1.4 核心场景

1. 买家打开 App → 切换到 Shop Tab → 默认看到第一个 Navigation 下的所有 Menu Items → 点击某个图文卡片 → 进入对应 Collection 商品列表
2. 买家切换左侧导航 → 右侧 Menu Items 随之切换
3. 运营在 CMS 后台新增/调整 Navigation 和 Menu Items → 前台实时生效

### 1.5 全局页面流转

```
底部 TabBar（Shop 入口）
  └─→ Shop 页
        └─→ 点击 Menu Item 图文卡片 → Collection 商品列表页（/collection/:slug）
```

### 1.6 术语说明

| 术语 | 含义 |
|---|---|
| Navigation | 左侧一级导航项，对应一个分类入口（如"Bags"、"Jewelry"） |
| Menu Item | Navigation 下的图文卡片入口，每个关联一个 Collection |
| Collection | CMS 后台定义的商品集合，有唯一 slug，Menu Item 通过 collectionId 与之关联 |
| Market / Channel / Terminal | 全局配置维度，决定当前配置空间（当前 Shop 页固定为 US / Looply App / APP） |

### 1.7 字段名与前台展示名对照

| 字段名（后台/接口） | 前台展示名 | 枚举值 |
|---|---|---|
| `status` | 状态 | `enabled`（启用）/ `disabled`（停用） |
| `market` | 市场 | 见 2.6.1，待市场模块 PRD 确认 |
| `channel` | 渠道 | 见 2.6.1，待市场模块 PRD 确认 |
| `terminal` | 终端 | 见 2.6.1，待市场模块 PRD 确认 |
| `order` | 排序 | 整数，升序展示 |

> ⚠️ `status` 字段枚举值（enabled/disabled）及 market/channel/terminal 的完整枚举，须以市场模块 PRD 和数据表设计为准，本文档使用当前已知值，上线前需交叉核对。

### 1.8 多语言 / 多国家策略

当前阶段仅支持美国市场（market = US）、英文界面。Navigation 和 Menu Item 的名称由运营在后台直接填写英文，不做多语言翻译处理。

---

## 二、需求详细描述

### 2.1 页面整体布局

Shop 页由四个区域纵向排列：

```
┌─────────────────────────────────┐
│           TopBar                │
├───────────┬─────────────────────┤
│           │                     │
│ 左侧       │   右侧内容区         │
│Navigation │   Menu Items 列表    │
│           │                     │
├───────────┴─────────────────────┤
│           底部 TabBar            │
└─────────────────────────────────┘
```

- TopBar：固定在顶部，不随页面滚动
- 左侧 Navigation：固定宽度，内容超出时可独立滚动，不影响右侧
- 右侧内容区：宽度自适应（占剩余空间），内容超出时可独立滚动
- 底部 TabBar：固定在底部，不随页面滚动

### 2.2 TopBar

**元素（从左到右）**：
- Looply Logo
- 搜索框（居中，点击后展开为全宽输入态）
- 收藏图标（心形）
- 购物袋图标

TopBar 在 Shop 页的行为与 App 其他页面保持一致，本 PRD 不重复定义其交互。

### 2.3 左侧 Navigation

**展示规则**：
- 只展示当前 Market/Channel/Terminal 下 status = enabled 的 Navigation
- 按后台配置的 order 字段升序排列
- 进入页面时默认选中第一个 status = enabled 的 Navigation

**激活态**：
- 当前选中项有视觉高亮标识（左侧竖线 + 背景色变化 + 文字颜色变化），与未选中项有明显区分
- 激活态样式仅用于当前选中项，其他项保持未选中样式

**交互**：
- 点击任意 Navigation 项 → 右侧内容区切换展示该 Navigation 下的 Menu Items
- 左侧导航区域独立滚动，Navigation 数量较多时可上下滚动，不影响右侧

**空态**：所有 Navigation 均为 status = disabled 时，页面主体区域显示空态提示。

### 2.4 右侧内容区 — Menu Items 列表

右侧仅展示当前激活 Navigation 下的 Menu Items，无其他内容模块。

**标题行**：
- 展示当前激活 Navigation 的名称
- 位于 Menu Items 列表上方

**图文卡片网格**：
- 固定 3 列布局
- 只展示 status = enabled 的 Menu Items
- 展示顺序按后台配置的 order 字段升序排列（排序在同一 Navigation 内有效）

**图文卡片单项**：
- 图片区域展示图片（1:1 比例，contain 填充）
- 图片下方展示 Menu Item 名称（最多 2 行，超出截断）

**交互**：
- 点击图文卡片 → 跳转至该 Menu Item 关联的 Collection 商品列表页（路由：`/collection/:slug`）
- slug 取自关联 Collection 的 slug 字段

**空态**：当前激活 Navigation 下没有 status = enabled 的 Menu Item 时，右侧显示空态提示"暂无分类入口"。

### 2.5 底部 TabBar

Tab 项：Home / Shop（当前激活）/ Favourites / Account

Shop Tab 保持激活态。TabBar 行为在全局规范中定义，本 PRD 不重复定义。

### 2.6 后台配置能力

后台原型参考：`looply-shop导航-后台原型-v1.0-antd.html`

#### 2.6.1 全局维度（最顶层筛选）

Market / Channel / Terminal 是后台的最顶层配置维度，高于所有页面级操作。三者的组合确定一个独立的配置空间，Navigation 和 Menu Items 均在此空间下管理。

| 维度 | 当前已知枚举值 | 当前 Shop 页对应值 | 备注 |
|---|---|---|---|
| market（市场） | US（United States） | US | ⚠️ 完整枚举待市场模块 PRD 确认 |
| channel（渠道） | looply_app（Looply App）/ shopify（Shopify） | looply_app | ⚠️ 完整枚举待市场模块 PRD 确认 |
| terminal（终端） | app（APP） | app | ⚠️ 完整枚举待市场模块 PRD 确认 |

- 每个维度单选，无"全部"选项
- 切换全局维度后，Navigation 页和 Menu 页展示内容同步切换

#### 2.6.2 Navigation 管理

**功能描述**：运营管理 Shop 页左侧导航列表。

**字段定义**：

| 字段名 | 前台展示名 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| name | 名称 | 文本 | 是 | 前台展示的导航名称；最大字符数由设计规范确定后写入，输入框需实时显示剩余字符数，超出上限时不允许继续输入 |
| status | 状态 | 枚举 | 是 | enabled（启用）/ disabled（停用）；默认 enabled |
| order | 排序 | 整数 | 自动 | 在当前维度下的排列顺序，由系统维护 |
| market | 市场 | 字符串 | 自动 | 继承自全局 market 维度，创建后不可修改 |
| channel | 渠道 | 字符串 | 自动 | 继承自全局 channel 维度，创建后不可修改 |
| terminal | 终端 | 字符串 | 自动 | 继承自全局 terminal 维度，创建后不可修改 |

**操作能力**：

| 操作 | 规则 |
|---|---|
| 新增 | 名称必填；market/channel/terminal 自动继承全局维度，创建后不可修改 |
| 编辑 | 只可修改名称和状态；market/channel/terminal 不可修改 |
| 删除 | 同时删除其下所有 Menu Items；删除前弹窗交互：提示"将同时删除该 Navigation 下的 N 个 Menu Items，此操作不可恢复"，展示受影响 Menu Items 数量，需用户点击确认按钮后执行 |
| 排序 | 上下箭头调整顺序，决定前台左侧导航的展示顺序 |
| 启停 | 切换 status；停用后前台不展示该 Navigation |

**去重规则**：同一 market/channel/terminal 下，Navigation name 不可重复；字母大小写不同视为同一名称（如"Bags"与"bags"判定为重复）；提交时校验，重复则提示错误，不关闭表单。

**逆向链路**：删除 Navigation 时，其下所有 Menu Items 一并删除，不可恢复；删除弹窗中需展示将被删除的 Menu Items 数量供运营确认。

#### 2.6.3 Menu Items 管理

**功能描述**：运营管理每个 Navigation 下的图文卡片入口列表。

**字段定义**：

| 字段名 | 前台展示名 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| navId | 归属导航 | 关联 | 是 | 归属的 Navigation；新建时手动选择，编辑时不可修改 |
| name | 名称 | 文本 | 是 | 前台图片下方展示的文字；最大字符数由设计规范确定后写入，输入框需实时显示剩余字符数，超出上限时不允许继续输入 |
| image | 图片 | 图片 | 是 | 1:1 比例图片，必须上传后才可保存；未上传图片不允许提交 |
| collectionId | 关联 Collection | 关联 | 是 | 关联的 Collection；决定点击跳转目标 |
| status | 状态 | 枚举 | 是 | enabled（启用）/ disabled（停用）；默认 enabled |
| order | 排序 | 整数 | 自动 | 在所属 Navigation 内的排列顺序，由系统维护 |

**操作能力**：

| 操作 | 规则 |
|---|---|
| 新增 | 先选 Navigation，再填写名称、上传图片（必填）、关联 Collection；所有必填项均填写后才可提交 |
| 编辑 | market/channel/terminal/Navigation 不可修改；名称、图片、Collection、状态可改 |
| 删除 | 仅删除该 Menu Item，不影响其他；删除前弹窗交互：提示"删除后此操作不可恢复"，需用户点击确认按钮后执行 |
| 排序 | 上下箭头调整顺序；排序仅在同一 Navigation 内有效，不可跨 Navigation 排序 |
| 启停 | 切换 status；停用后前台不展示该 Menu Item |

**搜索与筛选**：
- 搜索：支持 Menu Item name 模糊匹配、关联 Collection name 模糊匹配、关联 Collection ID 精确匹配
- 按 Navigation 筛选：下拉选择，选项范围为当前全局维度下的 Navigation 列表；可清空（清空后展示全部）
- 按状态筛选：启用 / 停用 / 全部

**去重规则**：同一 Navigation 下，Menu Item name 不可重复；字母大小写不同视为同一名称（如"Shoulder"与"shoulder"判定为重复）；不同 Navigation 之间允许同名。提交时校验，重复则提示错误，不关闭表单。

**Collection 关联说明**：选择 Collection 后，后台显示该 Collection 的名称、落地页链接（`/collections/{slug}`）、商品数量（基于最近一次同步的近似值），辅助运营确认关联是否正确。

**逆向链路**：关联的 Collection 在 CMS 后台被删除时，后台 Menu Item 列表提示"关联已断开"；前台该图文卡片隐藏（不展示）。

---

## 三、依赖与风险

| 依赖方 | 依赖内容 | 关键要求 |
|---|---|---|
| CMS Collection 模块 | Menu Item 关联的 Collection 列表（id / name / slug） | 需提供可搜索的 Collection 列表接口，支持按名称模糊查询和按 ID 精确查询；Collection 删除时需通知 Shop 模块标记关联断开 |
| 市场模块 | market / channel / terminal 完整枚举定义 | Shop 导航配置的维度枚举必须与市场模块 PRD 和数据表保持一致，上线前需交叉核对 |
| 前端路由 | 点击 Menu Item 跳转 `/collection/:slug` | Collection slug 需稳定，不可随意修改；修改 slug 会导致 Menu Item 点击跳转 404 |

**风险**：
- Collection 被删除或 slug 变更时，若前台未及时感知，用户点击会跳转失败；需有后台预警机制
- market/channel/terminal 枚举尚未由市场模块 PRD 最终确认，开发前需对齐

---

## 四、版本规划

### 当前版本（MVP）

- Shop 页左侧 Navigation + 右侧 Menu Items 图文卡片列表
- 后台：Navigation 和 Menu Items 的 CRUD、排序、启停
- 全局维度：Market / Channel / Terminal 单选筛选
- 关联 Collection，点击跳转商品列表

### 后续迭代方向

- Menu Item 支持关联多个 Collection（当前一对一）
- Navigation 支持图标图片（当前纯文字）
- 多市场扩展（当前仅 US）
- 多渠道独立配置预览（Shopify 渠道独立前台预览）

---

## 五、版本变更记录

> 相对于上一版本：`looply-shop-app-prd-v4.md`

### v5 变更内容（2026-06-29）

**变更 1：Collection 归属修正**
- 变更类型：修改
- 变更内容：Collection 由"商品后台定义"改为"CMS 后台定义"；依赖方表述从"商品后台 Collection 模块"改为"CMS Collection 模块"
- 变更原因：Collection 实际归属 CMS 后台，非商品后台

**变更 2：全文去除"圆形"描述**
- 变更类型：修改
- 变更内容：所有"圆形"描述统一改为"图文卡片"；章节标题"圆形列表"改为"列表"；"圆形网格"改为"图文卡片网格"；相关交互描述同步更新
- 变更原因：形状是 UI 实现细节，不属于产品逻辑；命名应基于业务含义

**变更 3：字段名与枚举完整定义**
- 变更类型：新增
- 变更内容：新增 1.7 字段名与前台展示名对照表；`enabled` 字段重命名为 `status`，枚举值明确为 `enabled`（启用）/ `disabled`（停用）；全文统一使用 status 字段名和对应枚举值
- 变更原因：前后台字段名不一致导致理解歧义；枚举值需完整定义

**变更 4：Channel 枚举加待确认备注**
- 变更类型：修改
- 变更内容：market/channel/terminal 枚举值表格增加"备注"列，标注"⚠️ 完整枚举待市场模块 PRD 确认"；1.7 字段说明同步补充
- 变更原因：枚举合法值须由市场模块 PRD 和数据表设计最终确认，不能在 Shop PRD 中单独定死

**变更 5：Navigation name 和 Menu Item name 增加字符数限制交互说明**
- 变更类型：修改
- 变更内容：字段定义表中 name 字段说明补充"最大字符数由设计规范确定后写入；输入框需实时显示剩余字符数，超出上限时不允许继续输入"
- 变更原因：有字符限制的输入框需要明确交互形式，避免开发自行决定

**变更 6：删除操作补充弹窗交互细节**
- 变更类型：修改
- 变更内容：Navigation 删除操作规则补充弹窗交互描述（提示文案、受影响数量展示、确认按钮）；Menu Item 删除操作同步补充弹窗交互描述
- 变更原因：删除是不可逆操作，弹窗交互需在 PRD 中明确定义

**变更 7：大小写重复判断规则明确**
- 变更类型：修改
- 变更内容：Navigation 和 Menu Item 去重规则中，"大小写不敏感"改为明确表述"字母大小写不同视为同一名称（如'Bags'与'bags'判定为重复）"
- 变更原因：原表述"大小写不敏感"含义不够直接，需明确开发实现预期

**变更 8：Menu Item image 改为必填**
- 变更类型：修改
- 变更内容：image 字段必填由"否"改为"是"；操作说明中"上传图片"改为"上传图片（必填）"，并补充"所有必填项均填写后才可提交"；删除 v4 中"未上传图片时前台不展示"的逻辑；同步删除依赖与风险中"运营未上传图片即启用"的风险项
- 变更原因：图片是图文卡片的核心展示元素，不应允许无图片保存；强制必填从源头避免数据残缺

---

## 附录：UI 规范参考

> 本附录供设计师和前端实现参考，不属于产品需求定义范畴。具体数值以设计稿为准，此处为当前原型实现的参考值。

### A.1 左侧 Navigation

| 属性 | 参考值 |
|---|---|
| 宽度 | 108px |
| 背景色 | `#FAFAFA` |
| 右侧分隔线 | 1px solid `#E5E7EB` |
| 字号 | 13px |
| 每项 padding | `13px 10px 13px 14px` |
| 激活态背景 | `#FFFFFF` |
| 激活态左侧竖线 | 3px，颜色 `#7C3AED` |
| 激活态文字色 | `#7C3AED`，font-weight: 600 |
| 未激活文字色 | `#374151` |

### A.2 右侧图文卡片网格

| 属性 | 参考值 |
|---|---|
| 列数 | 3 列 |
| 网格 gap | 8px |
| 网格 padding | `0 10px 12px` |
| 图片区高宽比 | 1:1（aspect-ratio: 1） |
| 图片填充方式 | object-fit: contain |
| 文字标签字号 | 11px |
| 文字标签颜色 | `#374151` |
| 文字最大行数 | 2 行 |

### A.3 标题行

| 属性 | 参考值 |
|---|---|
| 字号 | 15px，font-weight: 600 |
| padding | `14px 12px 8px` |

### A.4 品牌色

| 用途 | 色值 |
|---|---|
| 主色（激活态、强调） | `#7C3AED` |
| 分隔线 | `#E5E7EB` |
| 次要文字 | `#374151` |
| 辅助文字 | `#6B7280` |
