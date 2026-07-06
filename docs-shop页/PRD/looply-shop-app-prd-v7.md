# Looply Shop 页 PRD v7

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
| **v7** | **`looply-shop-app-v0.3.html`** | **`looply-shop页导航栏配置-后台原型-v0.1-antd.html`** | 用原生两级/三级层级替代分组概念；Navigation 新增 `levels` 字段（两级/三级，创建后锁定）；三级模式下 L2 为纯文字分组标题、L3 为图文卡片；一级导航列表新增"层级"列；移除 grouped/groupId/Nav Group 相关内容 |

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
| Collection | CMS 后台定义的商品集合（对齐 Collection PRD v0.17）；字段：`collection_id`（唯一标识）/ `title`（EN 名称）/ `url_slug`（URL 路径段）；targetType=collection 时系统根据 `url_slug` 自动填充 targetUrl |
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
| `parentId` | L2 Item 所在组的 ID / `null` | L2 Item 的 parentId 为 null；L3 Item 的 parentId 为所属 L2 Item 的 ID |

### 1.8 多语言 / 多国家策略

当前阶段仅支持美国市场（market_id = US）、英文界面。Navigation 和 Menu Item 的名称由运营在后台直接填写英文，不做多语言翻译处理。

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

Tab 项：Home / Shop（当前激活）/ Favourites / Account。Shop Tab 保持激活态。TabBar 行为由全局规范定义，本 PRD 不重复定义。

---

### 2.6 后台配置能力（CMS > Shop页 > 导航配置）

**后台原型参考**：`looply-shop页导航栏配置-后台原型-v0.1-antd.html`

#### 2.6.1 全局维度（最顶层筛选）

Market / Channel / Terminal 是后台的最顶层配置维度，三者组合确定一个独立的配置空间。Shop 页导航配置固定 terminal=app，后台界面中 Terminal 显示为只读的"📱 App"标签，不可切换。

| 维度 | 字段名 | 当前值 | 说明 |
|---|---|---|---|
| 市场 | `market_id` | `US` | 对齐 Market 系统 `market_code`；当前仅美国市场，枚举来自 Market 模块 |
| 渠道 | `channel_id` | `chn_us_001`（美国官网商城）| 枚举来自商品中心渠道管理实体，非硬编码字符串；实际 ID 以商品系统渠道管理数据为准 |
| 终端 | `terminal` | `app` | 固定，不可切换 |

- market_id 和 channel_id 单选，无"全部"选项
- 切换 market_id/channel_id 后，Navigation 和 Menu Items 列表同步切换

#### 2.6.2 Navigation 管理

**功能描述**：运营管理 Shop 页左侧一级导航列表。

**后台入口路径**：CMS > Shop页 > 导航配置（点击一级导航名称可下钻进入该导航的二级导航管理页）

**字段定义**：

| 字段名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `name` | 文本 | 是 | 前台左侧展示的导航名称；最大字符数以设计规范为准，输入框实时显示剩余字符数，超出上限不允许继续输入 |
| `enabled` | 布尔 | 是 | true（启用）/ false（停用）；默认 true |
| `grouped` | 布尔 | 是 | true（开启分组）/ false（不分组）；默认 false；开启后该 Navigation 下所有 Menu Item 必须归属一个分组 |
| `order` | 整数 | 自动 | 在当前 market_id/channel_id/terminal 下的排列顺序，由系统维护 |
| `market_id` | 字符串 | 自动 | 继承自全局 market_id，创建后不可修改 |
| `channel_id` | 字符串 | 自动 | 继承自全局 channel_id，创建后不可修改 |
| `terminal` | 字符串 | 自动 | 固定为 app，创建后不可修改 |

**操作能力**：

| 操作 | 规则 |
|---|---|
| 新增 | 名称必填；market_id/channel_id/terminal 自动继承全局维度，不可手动修改；grouped 默认 false |
| 编辑 | 可修改名称、enabled、grouped；market_id/channel_id/terminal 不可修改 |
| 排序 | 拖拽排序（拖拽手柄在行首），决定前台左侧导航展示顺序 |
| 启停 | 切换 enabled；停用后前台不展示该 Navigation，其下 Menu Items 不受影响，重新启用后恢复显示 |
| 删除 | **仅当 enabled=false（停用状态）时可操作删除**；删除前弹窗确认"将同时删除该导航下所有二级导航，不可恢复"；点击确认后，该 Navigation 及其下所有 Menu Items 和 Nav Groups 一并删除 |

**grouped 切换规则**：
- **false → true**：若该 Navigation 下已有 Menu Items，立即弹窗提示运营前往分配分组（提示：该导航下存在尚未分配分组的二级导航；操作者可选择"去分配分组"直接跳转至该导航的二级导航管理页，或"稍后处理"关闭弹窗）；在所有 Menu Items 完成分组前，导航概览页该行名称列显示 ⚠ 有未分组，组数列显示数字并标橙。
- **true → false**：允许直接切换，已有 groupId 的数据保留（不清空），前台不再分组展示；若再次切换回 true，已有 groupId 数据仍有效。

**去重规则**：同一 market_id/channel_id/terminal 下，Navigation name 不可重复；字母大小写不同视为同一名称（如"Bags"与"bags"判定为重复）；提交时校验，重复则提示错误，不关闭表单。

**数量**：无上限，支持无限创建；列表无分页，窗口内无限滚动。

**列表字段展示**：

| 列名 | 说明 |
|---|---|
| 排序手柄 | 拖拽图标，用于调整顺序 |
| 名称 (Name) | 点击可下钻进入该导航的导航项管理页 |
| 层级 | 显示该 Navigation 的 levels 值：两级 / 三级 |
| 已启用导航数 | 两级模式：统计该 Navigation 下 enabled=true 的 L2 Items 数量；三级模式：统计 enabled=true 的 L3 Items 数量；纯数字，不可点击 |
| 状态 | 启用/停用开关 |
| 操作 | 编辑按钮（常驻）；删除按钮（仅 enabled=false 时展示） |

#### 2.6.3 Menu Items（二级导航）管理

**功能描述**：运营管理每个 Navigation 下的图文卡片入口列表。

**后台入口路径**：CMS > Shop页 > 导航配置 > 点击一级导航名称（下钻进入）

**字段定义**：

| 字段名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `navId` | 关联 | 是 | 归属的 Navigation；新建时选择，编辑时不可修改 |
| `name` | 文本 | 是 | 前台图片下方展示文字；最大字符数以设计规范为准，输入框实时显示剩余字符数，超出上限不允许继续输入 |
| `image` | 图片 | 是 | 1:1 比例图片；必须上传后才可保存，未上传不允许提交 |
| `targetType` | 枚举 | 是 | `collection`（关联合集）/ `external`（自定义链接） |
| `collectionId` | 关联 | 条件必填 | targetType=collection 时必填；从 CMS Collection 列表中选择；存储 `collection_id`（对齐 Collection PRD v0.17） |
| `targetUrl` | 字符串 | 是 | 点击跳转目标路径；targetType=collection 时由系统根据所选 Collection `url_slug` 自动填充为 `/collections/{url_slug}`（只读）；targetType=external 时由运营手动填写 |
| `groupId` | 关联 | 条件必填 | 归属的 Nav Group ID；**仅当所属 Navigation 的 grouped=true 时必填**；grouped=false 时此字段忽略（存 null）；新建时可选择该 Navigation 下已有分组或新建分组 |
| `enabled` | 布尔 | 是 | true（启用）/ false（停用）；默认 true |
| `order` | 整数 | 自动 | 在所属 Navigation 内的排列顺序，由系统维护 |

**targetType 行为说明**：

| targetType | 后台表单行为 | targetUrl 来源 |
|---|---|---|
| collection（关联合集） | 显示合集搜索下拉框；选中后展示合集名称和链接预览（链接可点击跳转验证） | 系统自动填充 `/collections/{url_slug}`，只读不可修改 |
| external（自定义链接） | 显示 URL 输入框，运营手动填写 | 运营手动输入，如 `https://...` 或 `/path/...` |

**操作能力**：

| 操作 | 规则 |
|---|---|
| 新增 | 选择 Navigation、填写名称、上传图片（必填）、选择 targetType、填写关联信息；若所属 Navigation grouped=true，groupId 必填——可选已有分组或在表单内新建分组；所有必填项完整后方可提交 |
| 编辑 | market_id/channel_id/terminal/Navigation 不可修改；名称、图片、targetType、collectionId、targetUrl、groupId、enabled 可改 |
| 排序 | 拖拽排序（拖拽手柄在行首）；仅在同一 Navigation 内有效，不可跨 Navigation 排序 |
| 启停 | 切换 enabled；停用后前台不展示该图文卡片 |
| 删除 | **仅当 enabled=false（停用状态）时可操作删除**；删除前弹窗确认"停用状态下删除，不可恢复"；仅删除该 Menu Item，不影响其他 |

**去重规则**：
- **Menu Item name**：同一 Navigation 下不可重复；字母大小写不同视为同一名称；不同 Navigation 之间允许同名。提交时校验，重复则提示错误，不关闭表单。
- **Nav Group name**：同一 Navigation 下不可重复；字母大小写不同视为同一名称；最多 30 个字符；输入框实时显示剩余字符数；提交/确认时校验重复，重复则提示错误。

**全有或全无约束**：一个 Navigation 下，要么所有 Menu Items 都有 groupId（grouped=true 时保证），要么全部没有（grouped=false）；不存在部分有分组、部分无分组的混合状态。grouped=true 时，若有 Menu Item 的 groupId 为空，视为分组未完成，后台列表和导航概览页均显示 ⚠ 警示，但不阻止保存。

**数量**：每个 Navigation 下 Menu Items 无数量上限；列表无分页，窗口内无限滚动。

**列表字段展示（二级导航管理页）**：

| 列名 | 说明 |
|---|---|
| 排序手柄 | 拖拽图标，用于调整顺序 |
| 名称 | Menu Item 展示名称；若所属 Navigation grouped=true 且该项 groupId 为空，名称右侧显示橙色 ⚠ 未分组 |
| 所属分组 | 所属 Navigation grouped=true 时展示（列存在）；显示该 Menu Item 所属 Nav Group 名称标签；groupId 为空则显示橙色 ⚠ 未分配；grouped=false 时此列不展示 |
| 关联 Collection | targetType=collection 时展示合集名称标签；targetType=external 时显示"—" |
| 跳转链接 | targetUrl 值，显示为可点击链接，点击在新标签页打开 |
| 状态 | 启用/停用开关 |
| 操作 | 编辑按钮（常驻）；删除按钮（仅 enabled=false 时展示） |

**Collection 关联说明**：选择 Collection 后，后台展示该 Collection 的 `title`（EN 名称）和落地页链接（`/collections/{url_slug}`）；链接可点击在新标签页打开，供运营确认关联是否正确。字段对齐 Collection PRD v0.17：`collection_id`（唯一标识）、`title`（名称）、`url_slug`（URL 路径段）。

**逆向链路（Collection 被删除）**：targetType=collection 且关联的 Collection 在 CMS 后台被删除时，后台 Menu Items 列表提示"⚠️ 关联合集已失效"；前台该图文卡片点击跳转会 404；运营需手动修正 targetUrl 或停用该 Menu Item。

#### 2.6.4 Nav Group 管理

**功能描述**：运营管理某个 Navigation 下的分组列表；Nav Group 是 Menu Item 的分类容器，仅在 Navigation grouped=true 时生效。

**字段定义**：

| 字段名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `id` | 字符串 | 自动 | 系统生成唯一 ID |
| `navId` | 关联 | 是 | 归属的 Navigation ID |
| `name` | 文本 | 是 | 分组名称；最多 30 个字符；同一 Navigation 下不可重复（大小写不区分） |
| `order` | 整数 | 自动 | 在所属 Navigation 内的排列顺序，由系统维护 |

**创建入口**：在新增/编辑 Menu Item 的表单中，"所属分组"下拉框内选择"＋ 新建分组…"后内联创建；后续迭代可在二级导航管理页提供独立的分组管理入口。

**操作能力**：

| 操作 | 规则 |
|---|---|
| 新建 | 在 Menu Item 表单内创建；名称必填，校验唯一性（同一 Navigation 下不可重名），超出 30 字符不允许输入；确认后立即生效，可在当前表单中直接选中 |
| 重命名 | 暂不支持（后续迭代） |
| 删除 | 暂不支持（后续迭代）；Nav Group 与 Navigation 一同删除 |

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
