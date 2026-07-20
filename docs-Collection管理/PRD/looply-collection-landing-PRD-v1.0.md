# Looply · Collection 落地页 — 产品需求文档

**版本** v1.0 | **日期** 2026-06-17 | **受众** UI 设计师 · 前端开发
**依赖** CMS PRD v2.4 · 商品系统 PRD v1.7 · 首页 PRD v1.0
**范围** Collection 落地页 · Mobile 端（PC 端 V2）

---

## 一、概述

### 1.1 背景与目标

Collection 落地页是 Looply 的「主题货架」页，承接首页 home_collections 坑位、Shop 页 shop_collections 坑位以及所有 `landing=collection_page` 跳转入口。

**目标**：
1. 通过运营配置的视觉素材传递合集氛围，建立品牌信任
2. 提供完整筛选链路（搜索 + 快筛 + 抽屉筛），帮用户快速锁定目标商品
3. 「零空结果」体验——交集为 0 的属性值物理隐藏，用户不会走进死胡同
4. 复用首页 Feed ProductCard 组件，保持全站视觉一致性

### 1.2 不做什么

| 不做 | 说明 |
|------|------|
| PC 端 | V1 仅 Mobile，PC 端独立规划（V2）|
| Collection 内分享 | Share 按钮 UI 预留，逻辑 V2 |
| 底部相关 Collection 推荐 | V2 |
| 筛选条件 URL 参数化 | V2 |
| C1 回收入口 | 本页无 C1 业务入口 |

### 1.3 用户角色

| 角色 | 说明 |
|------|------|
| 买家（C 端 Mobile 用户）| 浏览合集商品、筛选选品、跳转 PDP |

### 1.4 核心场景

| 场景 | 用户动作 | 关键模块 |
|------|------|------|
| 氛围浏览 | 进入页面后滑动浏览海报和商品 | 头部氛围区、商品网格 |
| 主题切入 | 点击图文 Label 切换子主题 | 图文 Label 行 |
| 关键词搜索 | 在集内搜索栏输入品牌名 / 品类 | 集内搜索 |
| 快速筛选 | 点击 Condition / Price / Brand Chip，弹出 Action Sheet 多选 | 快筛工具栏 |
| 精细筛选 | 打开抽屉筛，多维度组合 | 抽屉筛选器 |
| 逐项移除条件 | 面包屑区点 ✕ 拆除单条件 | 面包屑区 |
| 保存筛选组合 | 点 Save，后续一键复原 | 筛选保存 |
| 点击商品 | 跳转 PDP | 商品网格 |

### 1.5 全局页面流转

```
首页 home_collections 坑位 ──→ Collection 落地页
Shop 页 shop_collections 坑位 ──→ Collection 落地页
CMS 实例 landing=collection_page ──→ Collection 落地页
Collection 落地页 ──→ PDP（点击商品卡）
Collection 落地页 ──→ 登录页（未登录触发保存筛选）
登录成功 ──→ 回跳 Collection 落地页（自动执行保存）
```

### 1.6 术语说明

| 术语 | 定义 |
|------|------|
| Collection | CMS 合集实体，对应 URL `/collections/{slug}` |
| Label | Collection 内运营配置的二级分区入口 |
| Quick Filter（快筛）| 吸顶栏内的属性 Chip，点击弹出 Action Sheet |
| Drawer Filter（抽屉筛）| 屏幕左侧 66.6% 宽无遮罩抽屉，全量属性维度 |
| 面包屑（Breadcrumb）| 已选条件 Chip 展示区，在商品网格正上方 |
| Auto-Scroll | 筛选动作触发时页面自动平滑滚至搜索栏贴顶 |
| lock point | Auto-Scroll 目标：搜索栏贴紧顶导栏底部 |
| 物理隐藏 | 交集为 0 的属性值从 DOM 移除，不占位、不置灰 |

---

## 二、需求详细描述

### 2.1 数据源与字段映射

#### 2.1.1 现有 CMS 字段

| CMS 字段 | 前端用途 | 备注 |
|---------|------|------|
| `title` | 顶导栏标题 + 头部大标题 | |
| `tagline` | 头部副标题 | ≤60 字符 |
| `landing_page_template` | 头部渲染模式 | editorial / standard / compact |
| `landing_page_asset` | 头部背景图 | 空时见 §2.4.2 兜底 |
| `product_sets[]` | 商品数据来源（多集合并去重）| 后端排序后下发 |
| `pinned_listings[]` | 置顶商品 | 后端排序，前端直接渲染最前 |
| `status` | active 才可访问，否则 404 | |
| `display_start_time` / `display_end_time` | 超出范围返回 404 | |

#### 2.1.2 本文档新增字段

详见附录 §7.1，需同步至 CMS PRD v2.4 §三 合集管理。

---

### 2.2 页面整体布局与吸顶规则

#### 2.2.1 纵向模块列表

```
┌─────────────────────────────┐
│  M1. 顶导栏（44px）          │  ★ 始终固定
├─────────────────────────────┤
│  M2. 头部氛围区（按模板可变）  │  随流滚动
├─────────────────────────────┤
│  M3. 图文 Label 行（48px）   │  随流滚动
╠═════════════════════════════╣
│  M4. 集内搜索栏（44px）       │  ★ 吸顶层 1（z-index 100）
├─────────────────────────────┤
│  M5. 快筛与工具栏（44px）     │  ★ 吸顶层 2（z-index 100）
╠═════════════════════════════╣
│  M6. 结果数量通栏（32px）     │  随流滚动（禁止吸顶）
├─────────────────────────────┤
│  M7. 已选条件面包屑区（fit）  │  随流滚动（禁止吸顶）
├─────────────────────────────┤
│  M8. 商品网格（动态高度）     │  随流滚动
└─────────────────────────────┘
```

#### 2.2.2 吸顶触发条件

- M4 + M5 在页面向上滚动越过 M3 底部时锁定吸顶
- 吸顶样式：背景 white，底部 1px solid `$color-border`，z-index 100
- compact 模式无 M2，M3 紧接 M1；M4 越过 M3 底部即吸顶

---
### 2.3 模块 1：顶导栏

始终固定在页面顶部，absolute top:0，叠加于 M2 头部氛围区上方。

**UI 关联**：`looply-collection-landing-APP-v1.0.pen` → Module 1~3

#### 2.3.1 状态变化

| 场景 | 背景 | 左侧 | 中间 | 右侧 |
|------|------|------|------|------|
| editorial / standard + 未滚过头图 | 透明 | ← 白色返回图标 24px | 空 | 分享白色图标 24px |
| editorial / standard + 已滚过头图高度 | white + 底 1px `$color-border` | ← 深色返回图标 | Collection title（Inter 16px 600）| 分享深色图标 |
| compact | white + 底 1px `$color-border` | ← 深色返回图标 | Collection title | 分享深色图标 |

透明→白色渐变：从滚动距离 = 头图高度 × 70% 开始线性渐入，到 100% 时完全白色。

顶导栏高度 44px；iOS safe-area-inset-top 额外叠加。

---

### 2.4 模块 2：头部氛围区

**UI 关联**：`looply-collection-landing-APP-v1.0.pen` → Module 1（editorial）、Module 2（standard）

#### 2.4.1 三种渲染模式

由 `landing_page_template` 控制：

**editorial（编辑风，默认）**

- 头图高度：280px，fill 模式（铺满裁剪）
- 底部渐变遮罩：从 y=80px 起，`linear-gradient(transparent → #000 60%)`，高度 200px
- 标题：Playfair Display Italic 24px white，绝对定位 bottom 20px left 16px
- tagline：Inter Regular 13px `#FFFFFFCC`，标题下方间距 4px

**standard（标准）**

- 头图高度：180px，fill 模式
- 渐变遮罩：y=40px 起，#000 0%→40% opacity

**compact（紧凑）**

- 模块 2 不渲染，不占位
- Collection 标题直接显示在顶导栏中间（始终 white 背景）
- M3 图文 Label 行（若有）紧接 M1 下方

#### 2.4.2 无图片兜底（landing_page_asset 为空）

| 模板 | 兜底 |
|------|------|
| editorial | 纯色背景 `$color-brand`（#1A1A2E）+ 白色标题 / tagline，高度不变 280px |
| standard | 同上，高度 180px |
| compact | 无变化（本身无图）|

---

### 2.5 模块 3：图文 Label 行

**UI 关联**：`looply-collection-landing-APP-v1.0.pen` → Module 1~3

#### 2.5.1 布局规格

- 行高 48px，左侧 padding 16px，右侧无 padding（横向可滚动，无分页）
- 项目间距 8px

#### 2.5.2 Label Item 规格

纯文字型（无 label_image_url）：height 32px，padding 0 14px，border-radius 16px

图文型（有 label_image_url）：height 32px，padding 0 10px 0 8px，图标 20×20px，gap 6px

| 状态 | 背景 | 描边 | 文字色 |
|------|------|------|------|
| 未激活 | `$color-bg`（#F7F7F7）| `$color-border` 1px | `$color-ink-primary` |
| 激活 | `$color-brand`（#1A1A2E）| 无 | white |

"All" Label：系统自动生成，排最左，默认激活，运营无需配置。

#### 2.5.3 交互规则

- 点击 Label → 触发 Auto-Scroll（见 §2.13）→ 清空所有快筛 + 抽屉筛条件 → 刷新商品列表
- 再次点击已激活 Label → 回到 All（等同点击 All）
- 同一时刻仅一个 Label 激活
- `labels[]` 为空时，M3 整行隐藏，不占位

---

### 2.6 模块 4：集内搜索栏（吸顶层 1）

**UI 关联**：`looply-collection-landing-APP-v1.0.pen` → Module 4

#### 2.6.1 常驻态

- 高度 44px，水平 padding 16px
- 搜索框：border-radius 22px，fill=`$color-bg`，stroke=`$color-border` 1px
- 左侧 Search 图标 16px（`$color-ink-tertiary`），占位文字 `Search in {collection.title}`

#### 2.6.2 激活态

- 右侧出现「Cancel」文字按钮（Inter 14px，`$color-brand`）
- 软键盘弹出；输入过程中触发推荐浮层（见 §2.6.3）

#### 2.6.3 推荐浮层

- 位置：搜索栏正下方，宽度 = 屏幕 - 32px，left 16px
- 样式：white 背景，border-radius 12px，box-shadow，padding 12px 16px
- 内容：高频品牌名 + 品类名（后端按 collection_id 返回，≤10 条），chip 自动换行
- 点击推荐词 → 赋值搜索栏 → 浮层收起 → 软键盘收起 → Chip 加入面包屑 → Auto-Scroll → 刷新
- 禁止在浮层内放「Filter」或「全部筛选」入口

#### 2.6.4 搜索提交与取消

| 动作 | 结果 |
|------|------|
| 键盘 Search 键 | 提交 → 软键盘收起 → Auto-Scroll → 刷新 |
| 点击「Cancel」| 清空输入 → 软键盘收起 → 若原有搜索词则清除该条件并刷新 |
| 搜索词为空时点 Search | 等同 Cancel |
| 点击搜索栏外部（浮层外）| 软键盘收起，输入保留，浮层收起 |
| 搜索进行中点击快筛 Chip | 先收起键盘，再打开 Action Sheet |


---

### 2.7 模块 5：快筛与工具栏（吸顶层 2）

**UI 关联**：`looply-collection-landing-APP-v1.0.pen` → Module 5~8（各 Action Sheet 状态）

#### 2.7.1 工具栏布局

```
├─ 排序按钮（固定左）─┤─── 快筛 Chips（横滑中间）───┤─ 筛选按钮（固定右）─┤
│ Best Match ▽       │  [Condition] [Price] [Brand] │  ⚙ Filter           │
```

- 高度 44px，左侧 padding 16px，右侧 padding 16px
- 快筛 Chips 区域横向可滑动，左右与两侧按钮有 8px 间距

#### 2.7.2 快筛 Chip 通用规格

- 数据来源：`quick_filter_config` 配置的属性维度有序列表；未配置时默认 [Condition, Price, Brand]
- 高度 32px，padding 0 12px，border-radius 16px，Inter 13px

| 状态 | 背景 | 描边 | 文字 |
|------|------|------|------|
| 未激活 | `$color-bg` | `$color-border` 1px | `$color-ink-primary` |
| 已选（有值）| `$color-brand` | 无 | white |
| 已选（有值）| 右侧显示选中数量角标，如 `Brand (3)` | | |

- 点击 Chip → 弹出底部 Action Sheet（见各属性详细说明）
- Action Sheet 关闭时不触发 Auto-Scroll；点击 Action Sheet 内「Apply」后触发 Auto-Scroll 并刷新
- 可选值基于当前有效商品集合动态计算，交集为 0 的值物理隐藏

#### 2.7.3 排序按钮与 Action Sheet

- 默认文案：`Best Match ▽`；选中其他排序后文案更新，如 `Price: Low ▽`
- 点击弹出底部 Action Sheet，标题「Sort by」

| sort_key | 展示文案 |
|---------|---------|
| `recommended` | Best Match（默认）|
| `price_asc` | Price: Low to High |
| `price_desc` | Price: High to Low |
| `newest` | Newest First |
| `popular` | Most Popular |

- 可选项由 `sort_options` 字段配置；为空时展示全部 5 项
- 默认选中项由 `sort_default` 字段决定，默认 `recommended`
- 点击选项 → 即时切换（无 Apply 按钮）→ Action Sheet 自动关闭 → 刷新商品列表
- 排序不影响面包屑区显示

#### 2.7.4 Condition 快筛 Action Sheet

底部 Action Sheet，向上弹出 300ms ease-out，向下收起 250ms ease-in，手柄 indicator 在顶部居中。

**布局结构：**
```
┌──────────────────────────────────┐
│  ─── （handle indicator）        │
│  Condition                  Done │  标题左对齐 Inter 16px 600，Done 右对齐 14px $color-brand
├──────────────────────────────────┤
│  ○ Like New                      │  Inter 14px 600
│    Essentially no signs of use   │  Inter 12px $color-ink-secondary
│                                  │
│  ○ Excellent                     │
│    Slight traces of use          │
│                                  │
│  ○ Very Good                     │
│    Light traces of use           │
│                                  │
│  ○ Good                          │
│    Noticeable traces of use      │
│                                  │
│  ○ Fair                          │
│    Heavy traces of use           │
├──────────────────────────────────┤
│      [ Show 1,245 items ]        │  sticky bottom，fill=$color-brand，white 文字
└──────────────────────────────────┘
```

- 5 个选项固定顺序（Like New / Excellent / Very Good / Good / Fair），多选
- 选中状态：左侧 checkbox 填充 `$color-brand`，行背景 `$color-bg`
- 实时预计算：每次勾选变动即更新底部按钮的 item 数量
- item 数量为 0 时按钮置灰，文案改为「No items match」
- 点击「Done」或下拉 Action Sheet → 关闭，不应用更改（等同取消）
- 点击「Show N items」→ 应用，关闭，更新快筛 Chip 角标，加入面包屑，Auto-Scroll，刷新

#### 2.7.5 Brand 快筛 Action Sheet

```
┌──────────────────────────────────┐
│  ───                             │
│  Brand                      Done │
├──────────────────────────────────┤
│  🔍 Search brands...            │  搜索框，border-radius 8px，fill=$color-bg
├──────────────────────────────────┤
│  [Chanel (42)] [LV (38)]         │  chip 流，两列自然换行
│  [Gucci (25)]  [Dior (19)]       │  每个 chip 右侧显示该品牌商品数量
│  [Hermes (15)] [Prada (12)]      │
│  ··· 默认展示前 12 个 ···          │
│  ↓ Show all 34 brands            │  展开链接，`$color-brand` 14px
├──────────────────────────────────┤
│      [ Show 1,245 items ]        │
└──────────────────────────────────┘
```

- 品牌列表基于当前 Collection 商品动态生成，按商品数量降序
- 每个品牌 chip 显示格式：`Brand Name (N)`，N 为当前筛选上下文内该品牌商品数量
- 默认展示 12 个；点击「Show all N brands」展开全部；展开后出现「Show less」收起
- 搜索框：输入时实时过滤品牌列表（前端本地过滤，不发网络请求）；清空时恢复全量列表
- 多选；已选品牌 chip：fill=`$color-brand`，white 文字
- 点击已选 chip 再次点击 → 取消选中
- 图标：chip 左侧无图标（品牌名已足够区分）
- 关闭规则、Apply 规则同 §2.7.4

#### 2.7.6 Price 快筛 Action Sheet

```
┌──────────────────────────────────┐
│  ───                             │
│  Price                      Done │
├──────────────────────────────────┤
│  ☑ Under $200           (23)    │  预设区间，单行，复选
│  ☐ $200 – $500          (58)    │
│  ☐ $500 – $1,000        (42)    │
│  ☐ $1,000 – $2,000      (31)    │
│  ☐ $2,000+              (19)    │
├──────────────────────────────────┤
│  Custom Range                    │  分组标题
│  Min $[______] — Max $[_______]  │  数字键盘
│  （错误提示区）                    │
├──────────────────────────────────┤
│      [ Show 1,245 items ]        │
└──────────────────────────────────┘
```

**预设区间**：多选（OR 逻辑），可同时选「Under $200」+「$1,000 – $2,000」

**自定义输入**：
- 输入框聚焦时弹出数字键盘（iOS decimal pad / Android number keyboard）
- 一旦开始填写自定义范围 → 自动取消所有预设区间选中
- 重新点击任意预设区间 → 清空自定义输入
- 两者互斥

**校验规则（blur 时触发）**：

| 错误场景 | 提示文案 | 按钮状态 |
|---------|---------|---------|
| Min > Max | Min must be less than Max | 置灰 |
| 输入非数字字符 | Please enter a valid amount | 置灰 |
| Min 或 Max 为负数 | Amount must be 0 or greater | 置灰 |
| Min 和 Max 均为空 | 视为无价格筛选（不报错）| 正常 |
| Min = Max | 合法（精确价格匹配）| 正常 |

- 金额统一取整（floor/ceil 到整数美元），不支持小数
- 每个预设区间右侧动态显示该区间商品数量，实时随其他条件变化

#### 2.7.7 Color / Category 快筛 Action Sheet

当 `quick_filter_config` 中配置了 Color 或 Category 时，对应 Action Sheet 样式如下：

**Color Action Sheet**：
- 色块圆形矩阵，每行 5 个，circle 32px
- 浅色（White、Beige）加 `$color-border` 1px 描边
- 色块下方文字标签 Inter 11px `$color-ink-secondary`
- 选中态：色块内侧 3px `$color-brand` 环形边框

颜色枚举及 hex（固定顺序）：

| 颜色名 | hex |
|--------|-----|
| Black | #1A1A1A |
| White | #FFFFFF |
| Brown | #7C5C3E |
| Beige | #D4B896 |
| Red | #C41E3A |
| Blue | #2B4B8C |
| Green | #3A6B4C |
| Yellow | #F5C518 |
| Pink | #E8839A |
| Purple | #6B3FA0 |
| Orange | #E07035 |
| Gold | #C9A84C |
| Silver | #A8A8A8 |
| Multi | 4 象限拼色渐变 |

**Category Action Sheet**：文字 chip 流，同 Brand Action Sheet 样式，无搜索框，数量 ≤20 时无「Show all」

#### 2.7.8 筛选按钮（Filter 入口）

- 固定右侧，样式：⚙ 图标 + 「Filter」文字，Inter 13px，`$color-ink-primary`
- 有抽屉筛已选条件时：图标右上角显示红色圆点（diameter 6px，fill=#E53935）
- 点击 → 从左侧 slide-in 打开抽屉筛选器（见 §2.11）
- 抽屉已打开时再次点击 → 关闭抽屉（不应用）


---

### 2.8 模块 6：结果数量通栏

- 高度 32px，水平 padding 16px
- 文案：`1,245 items`（实时，千分位格式）；加载中显示 `— items`
- fill=`$color-bg`，文字 `$color-ink-secondary` 13px
- **禁止吸顶**，必须随货架滚动

---

### 2.9 模块 7：已选条件面包屑区

**UI 关联**：`looply-collection-landing-APP-v1.0.pen` → Module 9

#### 2.9.1 显示条件

- 有任意激活条件（Label ≠ All、搜索词 ≠ 空、任意快筛 / 抽屉筛有值）时显示
- 无条件时整区域隐藏，不占位
- **禁止吸顶**

#### 2.9.2 布局

- padding 8px 16px，flex-wrap（允许换行），gap 8px
- 「Clear All」按钮始终固定在最右侧

#### 2.9.3 Chip 样式

```
 ┌──────────────────────┐
 │  Brand: LV  ✕        │  border-radius 12px
 └──────────────────────┘
```

- fill=`$color-accent-light`（浅色强调背景）
- 文字 / ✕ 颜色：`$color-accent`
- 文案格式：`{属性名}: {值}` 或 `{属性名}: {值1}, {值2}` (同属性多值合并为一个 chip)

Chip 文案规则：

| 来源 | Chip 文案示例 |
|------|------|
| Label（非 All）| `Label: Summer Edit` |
| 搜索词 | `Search: chain bag` |
| Condition | `Condition: Like New, Excellent` |
| Brand | `Brand: LV, Chanel` |
| Price 预设 | `Price: Under $200, $200–$500` |
| Price 自定义 | `Price: $300 – $800` |
| Color | `Color: Black, Brown` |
| Category | `Category: Bags` |
| 抽屉筛其他属性 | `{属性名}: {值}` |

#### 2.9.4 逐项移除（逆向同步）

点击 Chip 上的 ✕：

1. 从激活条件中移除该属性的对应值
2. **同步回源**：
   - 来源 = Quick Filter Chip → 更新该 Chip 的选中集合，角标数量减少
   - 来源 = Drawer Filter → 更新 Drawer 内部状态（即使 Drawer 当前关闭）
   - 来源 = Label → 切回 All
   - 来源 = 搜索词 → 清空搜索栏显示
3. 立即重新计算交集，刷新商品列表（不触发 Auto-Scroll）
4. 移除后若所有条件为空 → 面包屑区隐藏

#### 2.9.5 Clear All

- 按钮文案「Clear All」，Inter 13px，`$color-ink-secondary`，无背景
- 点击：清空所有条件（Label→All，搜索→空，快筛→清空，抽屉筛→清空），刷新商品列表
- 面包屑区隐藏

#### 2.9.6 Save 筛选按钮

- 面包屑区最右侧（在 Clear All 按钮更右侧）
- 有已选条件时出现，无条件时隐藏
- 未保存态：☆ Save，Inter 13px，`$color-ink-primary`
- 已保存态：★ Saved，`$color-brand`
- 未登录时点击 → 跳转登录页，登录后回跳自动执行保存
- 已保存状态在刷新页面后保持（后端存储）

---

### 2.10 模块 8：商品网格

**UI 关联**：`looply-collection-landing-APP-v1.0.pen` → Module 1（商品网格区域）

- 双列，列间距 8px，行间距 16px，左右 padding 16px
- 商品卡：复用首页 Feed ProductCard 组件（Feed PRD v2.3 §3.2），不单独设计
- 置顶商品（`pinned_listings`）排网格最前，后端处理，前端无特殊标记
- 加载：同比例灰色骨架屏
- 无限滚动分页，触底前 3 屏预加载下一页
- 商品点击 → 跳转 PDP

---

### 2.11 抽屉筛选器

**UI 关联**：`looply-collection-landing-APP-v1.0.pen` → Module 10（默认）、Module 11（Color 展开）

#### 2.11.1 整体结构与动效

```
┌────────────────────────────┬───────────┐
│  ✕  Filter            Reset│           │
├────────────────────────────┤           │
│  Brand               ▲     │  右侧      │
│  [Chanel] [LV] [Gucci]     │  1/3 露出  │
│  [Dior]   [Hermes]         │  区域      │
│  ↓ Show all 34 brands      │  （无遮罩）│
├────────────────────────────┤           │
│  Price               ▲     │           │
│  ☑ Under $200   (23) │           │
│  ☐ $200–$500    (58) │           │
│  Min $[___] — Max $[___]   │  点击此区  │
├────────────────────────────┤  域收起    │
│  Condition           ▲     │  抽屉      │
│  [Like New] [Excellent]    │           │
│  [Very Good][Good][Fair]   │           │
├────────────────────────────┤           │
│  Color               ▼ （折叠）        │           │
├────────────────────────────┤           │
│  Category            ▼ （折叠）        │           │
├────────────────────────────┤           │
│  [ Apply · 84 items ]      │           │
└────────────────────────────┴───────────┘
 ←── 屏幕宽度 66.6% ──→ ← 33.3% →
```

- 宽度：屏幕 × 66.6%，从左侧 slide-in（250ms ease-out）
- 关闭：slide-out（200ms ease-in）
- 背景：white，左侧无圆角，右侧 border-radius 0（完全贴左边缘）
- 右侧 1/3：无蒙层，底层商品流完全可见

#### 2.11.2 开关路径

| 路径 | 触发方式 |
|------|------|
| 打开 | 点击工具栏「⚙ Filter」按钮 |
| 关闭 A | 点击抽屉内左上角「✕」|
| 关闭 B | 二次点击主页面「⚙ Filter」按钮（抽屉已开时）|
| 关闭 C | 点击右侧 1/3 露出区域（此时该区域商品点击事件临时挂起）|
| 关闭 D | 从抽屉内向右滑动（swipe-to-close，见 §2.11.10）|

路径 A / B / C / D 关闭：均不应用当前抽屉内的选中变更（等同取消）。

只有点击底部「Apply」按钮才提交变更。

#### 2.11.3 顶部操作栏

- 高度 52px，padding 0 16px
- 左侧：「✕」图标 + 「Filter」文字（Inter 16px 600）
- 右侧：「Reset」文字按钮（Inter 14px，`$color-ink-secondary`）
- 分割线：1px `$color-border` 在底部

#### 2.11.4 Brand 属性节

- 默认展开，最多显示 2 行（约 8~10 个 chip，依 chip 宽度自适应）
- Chip 样式：同快筛 Brand Action Sheet（含商品数量）
- 「↓ Show all N brands」展开链接；展开后「↑ Show less」收起
- Brand 内置搜索框：展开全部时出现（≤12 个时不出现）
- 选中状态同快筛，多选

#### 2.11.5 Price 属性节

- 默认展开
- 预设区间：checkboxes 多选（OR 逻辑），右侧显示商品数量
- 自定义输入：Min / Max 输入框，校验规则同 §2.7.6
- 预设 vs 自定义互斥规则同 §2.7.6

#### 2.11.6 Condition 属性节

- 默认展开
- 同快筛 Condition Action Sheet，但以 chip 形式展示（节省空间）
- Chip 格式：`Like New`、`Excellent`、`Very Good`、`Good`、`Fair`
- 选中态 chip：fill=`$color-brand`，white 文字；未选中：`$color-bg` + `$color-border` 描边
- 无描述文字（与 Action Sheet 不同，抽屉空间有限）

#### 2.11.7 Color 属性节

- 默认折叠，点击节标题展开 / 收起（▼ / ▲）
- 展开后：色块圆形矩阵，每行 5 个（宽度 = 抽屉宽度 × 66.6% / 5 - 间距）
- 规格：circle 32px；浅色加 1px 描边；下方文字标签 11px
- 颜色枚举及 hex 同 §2.7.7
- 选中态：色块内侧 3px `$color-brand` 环形边框

#### 2.11.8 Category 及其他属性节

- 默认折叠
- 文字 chip 流，多选，样式同 Condition chip
- 其他由商品属性聚合出的维度：默认折叠，Text chip 多选

#### 2.11.9 Apply 按钮

- 吸底，高度 52px，padding 水平 16px
- fill=`$color-brand`，white 文字，Inter 15px 600
- 文案：「Apply · {N} items」，N = 当前抽屉所有条件 × 当前快筛 × 当前搜索词的交集预计算数量
- N 为 0 时：fill=`$color-border`（置灰），文案「No items match」
- 点击：关闭抽屉 → 应用所有选中条件 → 更新快筛 Chip 角标 → 更新面包屑 → Auto-Scroll → 刷新

#### 2.11.10 Reset 按钮

- 仅清空**抽屉内部**的选中状态，不影响快筛条件
- Reset 后 Apply 按钮显示当前快筛 + 搜索词范围内的商品总数
- 与面包屑「Clear All」的区别：Reset 不关抽屉，也不清快筛

#### 2.11.11 Swipe-to-Close 手势

- 手势：在抽屉面板区域内向右滑动（horizontal swipe）
- 触发阈值：位移 > 抽屉宽度 × 40%，或释放瞬间速度 > 150 px/s
- 实时跟手：抽屉跟随手指位移（`transform: translateX`），超出 0 时不跟随（弹性阻尼）
- 未达阈值释放 → 弹回原位（spring back，300ms ease-out）
- 超过阈值释放 → 动画至关闭（200ms ease-in）
- 关闭效果同路径 A（不应用变更）

#### 2.11.12 快筛与抽屉双向状态同步

- Quick Filter 对某属性已选值 → 打开抽屉时，该属性节内对应 chip 显示为选中
- 抽屉内修改某属性 → Apply 后，对应 Quick Filter Chip 角标更新
- 抽屉 Reset → 不清 Quick Filter
- 面包屑 Clear All → 同时清 Quick Filter 和 Drawer 内部状态


---

### 2.12 全双工筛选交集逻辑

#### 2.12.1 联动公式

```
快筛候选值   = Collection 全集 ∩ 当前 Label ∩ 搜索词 ∩ 抽屉筛已选条件
抽屉筛候选值 = Collection 全集 ∩ 当前 Label ∩ 搜索词 ∩ 快筛已选条件
```

#### 2.12.2 规则

- 任一侧条件变化 → 两侧候选值实时重新计算
- 交集为 0 的属性值：物理隐藏（从 DOM 移除，不占位，不置灰）
- 抽屉内勾选不触发即时货架刷新，统一由 Apply 提交
- Quick Filter Action Sheet 内勾选不触发即时货架刷新，由 Apply 提交

#### 2.12.3 高层级重置规则

切换 Label 或输入新搜索词 → 所有快筛条件 + 抽屉筛条件立即全部清空，面包屑同步清空。

---

### 2.13 Auto-Scroll 与吸顶策略

#### 2.13.1 触发事件

| 触发 | 行为 |
|------|------|
| 点击图文 Label | 平滑滚动至 lock point（搜索栏贴顶）|
| 搜索栏获焦 | 平滑滚动至 lock point |
| 提交搜索 | 平滑滚动至 lock point |
| 点击 Quick Filter 的 Apply | 先关闭 Action Sheet，再执行 Auto-Scroll |
| 抽屉 Apply | 先关闭抽屉，再执行 Auto-Scroll |
| 面包屑 ✕ 逐项移除 | 不触发 Auto-Scroll |
| Clear All | 不触发 Auto-Scroll |

#### 2.13.2 lock point 定义

- lock point = 搜索栏（M4）的顶边紧贴顶导栏（M1）底边
- 滚动量 = 当前 scroll offset 到 M4 顶边距离

#### 2.13.3 回弹恢复

- 头部氛围区和 Label 行重新展现，**仅当用户主动向下拉动（pull-down gesture）时触发**
- 程序 Auto-Scroll 不触发回弹，不会意外展开头图

---

### 2.14 筛选状态保存与恢复

- 入口：面包屑区「☆ Save」按钮（有已选条件时才显示）
- 保存内容：`{label_id, search_keyword, quick_filter_values, drawer_filter_values}`，序列化存云端，与 user_account 绑定
- 保存后：按钮变「★ Saved」
- 未登录：跳转登录页，登录后回跳自动执行保存
- 查看入口：个人中心 → Saved Filters（本文档不定义该页面，V2 规划）
- 恢复：点击已保存的 Filter 记录 → 全量还原所有条件 → 刷新商品列表

---

### 2.15 空态与异常态

**UI 关联**：`looply-collection-landing-APP-v1.0.pen` → Module 12~13

| 状态 | 触发条件 | UI 处理 |
|------|------|------|
| 无效 slug / inactive collection | status ≠ active | 全页 404 |
| 展示时间超出范围 | 超出 display_time | 全页 404 |
| 合集内商品全部下架 | 网格无商品，无筛选条件 | 插画 + "Nothing here yet" + "Browse Other Collections" 按钮 |
| 筛选后 0 件商品 | 有激活条件但交集为空 | 插画 + "No items match your filters" + "Clear All Filters" 链接 |
| 网络异常 | 接口报错 | Toast 提示 + 骨架屏保持 + "Try Again" 按钮 |
| 加载中 | 首次 / 刷新 | 双列骨架屏（同比例灰色色块，含假图假文案区域）|

---

## 三、依赖与风险

### 3.1 上下游依赖

| 依赖 | 说明 | 状态 |
|------|------|------|
| CMS PRD v2.4 §三 合集管理 | 新增 labels / quick_filter_config / sort_options / sort_default 字段 | 需同步 |
| 商品系统 PRD v1.7 属性体系 | Color 色块需要 `color_hex` 属性；attr_key 枚举需与属性定义对齐 | 待确认枚举列表 |
| Feed PRD v2.3 §3.2 ProductCard | 商品网格复用 ProductCard 组件规范 | 已有 |
| 首页 Feed 搜索推荐词接口 | 后端按 collection_id 返回高频品牌 + 品类名（≤10 条）| 新增接口 |
| 筛选候选值动态计算接口 | 实时返回当前条件交集下各属性可用值列表（物理隐藏依赖此接口）| 新增接口 |
| 筛选状态保存接口 | 序列化筛选状态写云端，与 user_account 绑定 | 新增接口 |

### 3.2 风险与待确认项

| 风险 | 说明 | 责任方 |
|------|------|------|
| 筛选候选值动态计算性能 | 每次勾选变动实时请求，需后端预计算或缓存策略 | 后端 |
| Color hex 属性缺失 | 部分老商品无 color_hex，需与商品系统确认兜底策略 | 商品系统 |
| hero_carousel item=1 渲染 | 对齐原 HeroStatic 视觉，需前端确认 | 前端 |
| attr_key 枚举列表 | 需与商品系统 PRD v1.7 对齐完整枚举 | 商品系统 |

---

## 四、版本规划

### 4.1 V1（本文档范围）

| 功能 | 优先级 |
|------|------|
| 头部氛围区（3 种模板）| P0 |
| 图文 Label 行 | P0 |
| 集内搜索 + 推荐浮层 | P0 |
| Quick Filter：Condition / Price / Brand | P0 |
| 抽屉筛选器（Brand / Price / Condition / Color / Category）| P0 |
| 面包屑区 + 逐项移除 + Clear All | P0 |
| Auto-Scroll | P0 |
| 商品网格（复用 ProductCard）| P0 |
| 全双工筛选交集逻辑 | P0 |
| 空态 / 异常态 | P0 |
| 筛选状态保存（云端）| P1 |
| Swipe-to-close 手势 | P1 |
| Quick Filter：Color / Category（按 quick_filter_config 配置）| P1 |

### 4.2 V2 规划

| 功能 | 说明 |
|------|------|
| PC 端 | 独立规划，筛选交互对齐桌面端范式（侧边筛选栏）|
| Collection 内分享 | Share 按钮逻辑 |
| 底部相关 Collection 推荐 | 底部横滑推荐区 |
| 筛选条件 URL 参数化 | 支持分享带筛选状态的链接 |
| Saved Filters 个人中心页 | 查看 / 管理已保存的筛选 |

---

## 七、附录

### 7.1 新增字段清单（需同步至 CMS PRD v2.4 §三）

#### 字段一：`labels[]`（图文筛选 Label 列表）

| 子字段 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| `label_text` | string ≤20 字符 | 是 | Label 展示文案 |
| `label_image_url` | image | 否 | Label 图标（图文型），20×20px |
| `label_scope_type` | enum | 是 | `product_set`（子商品集）/ `attribute_filter`（属性筛）|
| `label_product_set_id` | FK | 条件必填 | scope_type=product_set 时必填 |
| `label_attr_key` | string | 条件必填 | scope_type=attribute_filter 时必填 |
| `label_attr_value` | string | 条件必填 | scope_type=attribute_filter 时必填 |
| `sort_order` | number | 是 | 展示顺序（升序，从 1 开始）|

#### 字段二：`quick_filter_config[]`（快筛属性配置）

| 子字段 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| `attr_key` | string | 是 | 属性键名（condition / price / brand / color / backend_category）|
| `sort_order` | number | 是 | 快筛栏从左到右顺序 |

默认值（未配置时）：[condition, price, brand]

#### 字段三：`sort_options` + `sort_default`

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `sort_options` | array of enum | 否 | 开放的排序选项，空时展示全部 5 项 |
| `sort_default` | enum | 否 | 默认激活排序，默认 `recommended` |

可选值：`recommended` / `price_asc` / `price_desc` / `newest` / `popular`

### 7.2 设计稿索引

本文档 V1 对应原型文件：**`looply-collection-landing-APP-v1.0.pen`**

| Module | 页面名称 | 对应 PRD 章节 |
|--------|------|------|
| Module 1 | 默认态 · Editorial 模板 | §2.3、§2.4（editorial）、§2.5、§2.6、§2.7、§2.10 |
| Module 2 | 默认态 · Standard 模板 | §2.4（standard）|
| Module 3 | 默认态 · Compact 模板 | §2.4（compact）|
| Module 4 | 搜索激活态（含推荐浮层）| §2.6 |
| Module 5 | 排序 Action Sheet | §2.7.3 |
| Module 6 | Condition 快筛 Action Sheet | §2.7.4 |
| Module 7 | Brand 快筛 Action Sheet | §2.7.5 |
| Module 8 | Price 快筛 Action Sheet | §2.7.6 |
| Module 9 | 面包屑已选条件态 | §2.9 |
| Module 10 | 抽屉筛选器 · 默认展开态 | §2.11 |
| Module 11 | 抽屉筛选器 · Color 展开态 | §2.11.7 |
| Module 12 | 空态 · 筛选后无结果 | §2.15 |
| Module 13 | 空态 · 合集商品全部下架 | §2.15 |

*最后更新：2026-06-17 | 作者：Kiro + zz*
