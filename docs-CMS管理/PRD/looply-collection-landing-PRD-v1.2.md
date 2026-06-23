# Looply · Collection 落地页 — 产品需求文档

**版本** v1.2 | **日期** 2026-06-17 | **受众** UI 设计师 · 前端开发
**依赖** CMS PRD v2.4 · 商品系统 PRD v1.7 · 首页 PRD v1.0
**范围** Collection 落地页 · Mobile 端（PC 端 V2）

**v1.1 → v1.2 变更说明**：搜索栏并入顶导（不再独立吸顶层）；头部模板简化为单一 standard 样式（删除 editorial/compact）；Quick Filter 改为点选即触发（删除 Apply 按钮）；Price 筛选改为 Range Slider（删除预设区间和 Min/Max 输入框）；§1.2 删除 C1 回收入口、URL 参数化、Price 区间 CMS 配置化等对读者无意义条目；§2.5 降级页面改为友好提示页（删除 404 表述）；CMS 字段需求大幅扩写（§4.1）；补充排序枚举定义及 hot_score 来源说明；§1.5 删除登录回跳逻辑行；Label 术语补充「图文筛」别名。

---

## 目录

- [§1 概述](#1-概述)
- [§2 数据逻辑层](#2-数据逻辑层)
  - [§2.1 CMS 字段映射](#21-cms-字段映射)
  - [§2.2 Collection 全集定义](#22-collection-全集定义)
  - [§2.3 筛选候选值联动规则](#23-筛选候选值联动规则)
  - [§2.4 筛选状态保存机制](#24-筛选状态保存机制)
  - [§2.5 空态与降级规则](#25-空态与降级规则)
- [§3 页面与交互](#3-页面与交互)
  - [§3.1 页面整体布局与吸顶](#31-页面整体布局与吸顶)
  - [§3.2 顶导栏](#32-顶导栏)
  - [§3.3 头部氛围区](#33-头部氛围区)
  - [§3.4 图文 Label 行](#34-图文-label-行)
  - [§3.5 集内搜索栏](#35-集内搜索栏)
  - [§3.6 快筛与工具栏](#36-快筛与工具栏)
  - [§3.7 结果数量通栏](#37-结果数量通栏)
  - [§3.8 面包屑区](#38-面包屑区)
  - [§3.9 商品网格](#39-商品网格)
  - [§3.10 抽屉筛选器](#310-抽屉筛选器)
  - [§3.11 Auto-Scroll 行为](#311-auto-scroll-行为)
- [§4 依赖与风险](#4-依赖与风险)
- [§5 版本规划](#5-版本规划)
- [§6 附录](#6-附录)

---

## §1 概述

### §1.1 背景与目标

Collection 落地页是 Looply 的「主题货架」页，承接首页 home_collections 坑位和 Shop 页 shop_collections 坑位的跳转。

**目标**：
1. 通过运营配置的视觉素材传递合集氛围，建立品牌信任
2. 提供完整筛选链路（搜索 + 快筛 + 抽屉筛），帮用户快速锁定目标商品
3. 「零空结果」体验——交集为 0 的属性值物理隐藏，用户不会走进死胡同
4. 复用首页 Feed ProductCard 组件，保持全站视觉一致性

### §1.2 不做什么

| 不做 | 说明 |
|------|------|
| PC 端 | V1 仅 Mobile，PC 端独立规划（V2）|
| Collection 内分享 | Share 按钮 UI 预留，逻辑 V2 |
| 底部相关推荐 | Collection 页底部不做相关推荐入口，V2 规划 |
| 筛选条件分享链接 | URL 参数由后端在用户分享时自动生成，V1 不做显式「复制筛选链接」功能 |

### §1.3 用户角色

| 角色 | 说明 |
|------|------|
| 买家（C 端 Mobile 用户）| 浏览合集商品、筛选选品、跳转 PDP |

### §1.4 核心场景

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

### §1.5 全局页面流转

```
首页 home_collections 坑位 ──→ Collection 落地页
Shop 页 shop_collections 坑位 ──→ Collection 落地页
Collection 落地页 ──→ PDP（点击商品卡）
```

### §1.6 术语说明

| 术语 | 定义 |
|------|------|
| Collection | CMS 合集实体，对应 URL `/collections/{slug}` |
| Collection 全集 | 该 Collection 下所有 `listing_status = active` 的商品，不附加任何筛选条件（见 §2.2） |
| Label | Collection 内运营配置的二级分区入口，即「图文筛」——每个 Label 对应一张图文卡片，点击后过滤该分区的商品 |
| Quick Filter（快筛）| 吸顶栏内的属性 Chip，点击弹出 Action Sheet |
| Drawer Filter（抽屉筛）| 屏幕左侧 66.6% 宽无遮罩抽屉，全量属性维度 |
| 面包屑（Breadcrumb）| 已选条件 Chip 展示区，在商品网格正上方 |
| Auto-Scroll | 筛选动作触发时页面自动平滑滚至搜索栏贴顶 |
| lock point | Auto-Scroll 目标：搜索栏贴紧顶导栏底部 |
| 物理隐藏 | 候选值不在后端返回列表中时前端不渲染该值，从 DOM 移除，不占位、不置灰 |

---

## §2 数据逻辑层

> 本章统一定义后端计算规则和前端消费的数据约定。页面模块的 UI 与交互细节见第三章。

### §2.1 CMS 字段映射

#### §2.1.1 现有 CMS 字段

| CMS 字段 | 前端用途 | 备注 |
|---------|------|------|
| `title` | 顶导栏标题 + 头部大标题 | |
| `tagline` | 头部副标题 | ≤60 字符，由 CMS 校验 |
| `landing_page_asset` | 头部背景图 URL | 为空时前端走兜底（品牌色背景） |
| `product_sets[]` | 商品来源，多集合并去重 | 后端排序后下发，前端直接渲染 |
| `pinned_listings[]` | 置顶商品 ID 列表 | 前端只管放最前，无特殊标记 |
| `status` | active 才可访问 | |
| `display_start_time` / `display_end_time` | 超出范围后端返回空数据，前端展示「合集暂不可访问」友好提示页 | 前端不判断时间 |
| `labels[].label_text` | Label 展示文案 | |
| `labels[].label_image_url` | Label 图标（有则图文型，无则纯文字型） | |
| `labels[].label_scope_type` + 关联字段 | 决定点击 Label 后过滤逻辑（由后端执行，前端只传 `label_id`） | |
| `labels[].sort_order` | Label 排列顺序 | |
| `quick_filter_config[].attr_key` + `sort_order` | 快筛栏展示哪些属性、展示顺序 | |
| `sort_options` | 排序 Action Sheet 开放哪几个选项 | |
| `sort_default` | 默认激活排序是哪个 | |

#### §2.1.2 本文档新增字段

详见附录 §6.1，需同步至 CMS PRD v2.4 §三 合集管理。

---

### §2.2 Collection 全集定义

**Collection 全集** = 该 Collection 下所有 `listing_status = active` 的商品，不附加任何用户筛选条件。

全集是所有候选值计算的基准锚点，不随用户操作改变。

---

### §2.3 筛选候选值联动规则

#### §2.3.1 联动公式

**维度 X 的候选值** =

```
Collection 全集（§2.2）
∩ 当前 Label 范围
∩ 搜索词
∩ 所有其他已激活条件（快筛 + 抽屉筛，排除维度 X 本身）
```

换句话说：用当前所有条件——但排除维度 X 自己——圈出商品集合，再从这个集合里反查维度 X 有哪些值出现过，那些值就是可展示的候选值。

**示例**：

> 用户在「Chanel Bags」Collection 里已激活：Brand = Chanel、Price < $2,000。
> 此时计算 Color 的候选值：取全集 ∩ 无 Label 过滤 ∩ 无搜索词 ∩ Brand=Chanel ∩ Price<$2,000（**不加** Color 条件）→ 得到 320 件商品 → 反查这 320 件的颜色 → 得 Black: 180, Beige: 90, Red: 50
>
> Color Action Sheet 只展示这 3 个颜色，其余颜色物理隐藏。
>
> 若用户再选中 Color = Black，计算 Brand 候选值时同样把 Brand 条件排除在外，确保用户还能切换品牌。

#### §2.3.2 计算规则

- 任一已激活条件变化 → 所有维度候选值实时重新计算
- 不在返回候选列表中的属性值：前端不渲染（即「物理隐藏」，前端无需主动过滤）
- **联动约束同时作用于维度本身和维度内的候选值（key 和 value 均受约束）**：后端返回某维度候选值时，同步返回该维度下每个值（value）的商品数量，数量为 0 的 value 不下发，前端不渲染
- Quick Filter：每个维度单选，点选后立即触发货架刷新（无 Apply 按钮）
- 抽屉筛：勾选后不即时刷新，统一由底部 Apply 按钮提交
- 动态计算接口的 debounce / cache 策略由后端决定，PRD 仅定义规则

#### §2.3.3 高层级重置规则

切换 Label 或输入新搜索词 → 所有快筛条件 + 抽屉筛条件立即全部清空，面包屑同步清空。

---

### §2.4 筛选状态保存机制

- 入口：面包屑区「☆ Save」按钮（有已选条件时才显示）
- 保存内容：`{label_id, search_keyword, quick_filter_values, drawer_filter_values}`，序列化存云端，与 `user_account` 绑定
- 保存后：按钮变「★ Saved」，同时 Toast 提示「Filters saved」
- 未登录：跳转登录页，登录后自动回跳并执行保存
- **V1 不提供查看已保存筛选的入口**；已保存的筛选在后端持久化，V2 在个人中心「Saved Filters」页面统一管理和复用

---

### §2.5 空态与降级规则

**UI 关联**：`looply-collection-landing-APP-v1.0.pen` → Module 12~13

| 状态 | 触发条件 | 处理 |
|------|------|------|
| 无效 slug / inactive | `status ≠ active` | 友好提示页：插画 + "This collection is no longer available" + "Browse Collections" 按钮，跳转合集列表页 |
| 展示时间超出范围 | 超出 `display_time` | 友好提示页：插画 + "This collection has ended" + "Browse Collections" 按钮 |
| 合集内商品全部下架 | 网格无商品，无筛选条件 | 插画 + "Nothing here yet" + "Browse Other Collections" 按钮 |
| 筛选后 0 件商品 | 有激活条件但交集为空 | 插画 + "No items match your filters" + "Clear All Filters" 链接 |
| 网络异常 | 接口报错 | Toast 提示"Something went wrong" + 骨架屏保持 + "Try Again" 按钮（点击重新请求）|
| 加载中 | 首次进入 / 刷新 | 双列骨架屏：上方头部区灰色色块占位（与头图等比例），下方商品卡等比例灰色色块 2 列排列，含假图区和假文案区 |

---

## §3 页面与交互

> 本章按模块顺序定义各 UI 区域的外观、状态变化和交互行为。数据计算逻辑见第二章。

### §3.1 页面整体布局与吸顶

#### §3.1.1 纵向模块列表

```
┌─────────────────────────────┐
│  M1. 顶导栏 + 搜索栏（44px） │  ★ 始终固定（搜索并入顶导）
├─────────────────────────────┤
│  M2. 头部氛围区（180px）     │  随流滚动
├─────────────────────────────┤
│  M3. 图文 Label 行（48px）   │  随流滚动
╠═════════════════════════════╣
│  M4. 快筛与工具栏（44px）    │  ★ 吸顶（z-index 100）
╠═════════════════════════════╣
│  M5. 结果数量通栏（32px）    │  随流滚动（禁止吸顶）
├─────────────────────────────┤
│  M6. 已选条件面包屑区（fit） │  随流滚动（禁止吸顶）
├─────────────────────────────┤
│  M7. 商品网格（动态高度）    │  随流滚动
└─────────────────────────────┘
```

#### §3.1.2 吸顶触发条件

- M4 快筛工具栏在页面向上滚动越过 M3 底部时锁定吸顶
- 吸顶后，M2 头部氛围区和 M3 图文 Label 行在视觉上折叠至顶导后方（用户继续向上滚已无法看到）
- 吸顶样式：背景 white，底部 1px solid `$color-border`，z-index 100
- 用户主动向下拉动（pull-down gesture）时，M2/M3 重新展开

---

### §3.2 顶导栏与搜索栏

始终固定在页面顶部，z-index 200，叠加于头部氛围区上方。搜索栏内嵌在顶导栏内，不独立占行。

**UI 关联**：`looply-collection-landing-APP-v1.0.pen` → Module 1~3

#### §3.2.1 顶导布局

顶导栏高度 44px + iOS safe-area-inset-top。从左到右：
- 左侧：← 返回图标 24px
- 中间：搜索栏（flex:1，左右 padding 8px）
- 右侧：分享图标 24px（UI 预留，逻辑 V2）

搜索栏外观：border-radius 20px，fill=`rgba(255,255,255,0.15)`（头图上方）/ `$color-bg`（白色顶导上方），placeholder「Search in this collection」，Inter 14px，左侧 🔍 图标 14px，有输入时右侧出现 ✕ 清空按钮。

#### §3.2.2 顶导背景状态

| 场景 | 背景 | 图标色 |
|------|------|------|
| 未滚过头图 | 透明 | 白色 |
| 已滚过头图高度 | white + 底 1px `$color-border` | 深色 |

透明→白色渐变：从滚动距离 = 头图高度 × 70% 开始线性渐入，至 100% 时完全白色。

#### §3.2.3 搜索交互

- 点击搜索栏获焦 → 键盘弹起，推荐词浮层出现（白色背景，radius 12px，阴影）
- 推荐词内容：后端按 `collection_id` 返回高频品牌名 + 品类名，≤10 条
- 点击推荐词或键盘 Search/Return → 提交搜索词，触发 Auto-Scroll → 货架刷新
- 搜索词作为一个筛选维度参与联动公式（§2.3.1），与快筛、抽屉筛取交集
- 提交新搜索词 → 清空所有快筛 + 抽屉筛条件（见 §2.3.3）
- 浮层关闭：失焦 / 提交 / 点 ✕

---

### §3.3 头部氛围区

**UI 关联**：`looply-collection-landing-APP-v1.0.pen` → Module 2（standard）

#### §3.3.1 渲染规格（Standard 样式，唯一模板）

- 头图高度：180px，fill 模式（铺满裁剪）
- 底部渐变遮罩：从 y=40px 起，`linear-gradient(transparent → rgba(0,0,0,0.4))`，高度 140px
- 标题：Inter 600 20px white，绝对定位 bottom 16px left 16px
- tagline：Inter Regular 13px `#FFFFFFCC`，标题下方间距 4px

#### §3.3.2 无图片兜底（`landing_page_asset` 为空）

纯色背景 `$color-brand`（#1A1A2E）+ 白色标题 / tagline，高度不变 180px。

---

### §3.4 图文 Label 行

**UI 关联**：`looply-collection-landing-APP-v1.0.pen` → Module 1~3

#### §3.4.1 布局规格

- 行高 48px，左侧 padding 16px，右侧无 padding（横向可滚动，无分页）
- 项目间距 8px

#### §3.4.2 Label Item 规格

纯文字型（无 `label_image_url`）：height 32px，padding 0 14px，border-radius 16px

图文型（有 `label_image_url`）：height 32px，padding 0 10px 0 8px，图标为 **圆形** 20×20px（`border-radius:50%`，fill 模式裁剪），图标与文字 gap 6px

| 状态 | 背景 | 描边 | 文字色 |
|------|------|------|------|
| 未激活 | `$color-bg`（#F7F7F7）| `$color-border` 1px | `$color-ink-primary` |
| 激活 | `$color-brand`（#1A1A2E）| 无 | white |

"All" Label：系统自动生成，排最左，默认激活，运营无需配置。

#### §3.4.3 交互规则

- 点击 Label → 触发 Auto-Scroll（见 §3.11）→ 清空所有快筛 + 抽屉筛条件（见 §2.3.3）→ 后端按新 `label_id` 刷新商品列表
- 再次点击已激活 Label → 回到 All（等同点击 All）
- 同一时刻仅一个 Label 激活
- `labels[]` 为空时，M3 整行隐藏，不占位

---

### §3.5 集内搜索

> 搜索栏已并入顶导栏（§3.2），本节不再单独描述外观规格。搜索词作为筛选维度参与联动公式（§2.3.1）。

---

### §3.6 快筛与工具栏

**UI 关联**：`looply-collection-landing-APP-v1.0.pen` → Module 5~8

#### §3.6.1 整体布局

- 高度 44px，横向可滚动，左 padding 16px，项目间距 8px
- 从左到右依次：排序 Chip → 快筛 Chip（按 `quick_filter_config.sort_order`）→ Filter 按钮（固定最右）
- 排序 Chip 始终显示，不受 `quick_filter_config` 控制
- **Quick Filter 为单选、点选即触发**：每个维度 Action Sheet 内点选一项 → 立即关闭 Action Sheet → 立即刷新货架（无 Apply 按钮）；如需多维度组合筛选，使用抽屉筛（§3.10）

#### §3.6.2 快筛 Chip 样式与显示规则

**显示条件**：某维度在当前 Collection 全集（§2.2）中有 ≥2 个不同值时才渲染该 Chip；否则整个 Chip 物理隐藏，不占位。（例：单品牌 Collection 中 Brand Chip 无意义，隐藏。）

| 状态 | 样式 |
|------|------|
| 无选中值 | `$color-bg` 背景 + `$color-border` 1px 描边，文字 `$color-ink-primary` |
| 有选中值 | `$color-brand` 背景，white 文字，右侧数字角标（选中值数量）|

- Chip 文字：属性名（如「Condition」「Price」「Brand」）
- 点击 Chip → 弹出对应 Action Sheet（从底部 slide-up）

#### §3.6.3 Condition Action Sheet（4 级，与商品系统 PRD v1.7 对齐）

- Action Sheet 标题「Condition」，底部「Apply · N items」按钮
- 4 个选项，每项含展示名 + 描述，多选；顺序固定：

| 内部枚举值 | 前台展示名 | 描述文字 |
|--------|--------|------|
| `NWT` | Like New | Essentially no signs of use, with original tags |
| `excellent` | Excellent | Minimal signs of use |
| `good` | Good | Light traces of use |
| `fair` | Fair | Noticeable traces of use |

- 候选值物理隐藏规则：当前全集中无该成色商品时，对应选项不渲染
- V1 前端硬编码展示名与描述；内部枚举值与商品系统 PRD v1.7 保持一致

#### §3.6.4 Price Action Sheet

Price 筛选使用 **Range Slider**，不做预设区间。

- Action Sheet 标题「Price」
- 双端滑动条（range slider）：左端 = 最低价，右端 = 最高价
- 滑块上方实时显示当前选中金额，格式「$200 — $1,000」
- 滑动范围由后端动态返回：当前 Collection 全集中最低价 ~ 最高价（取整到整数美元）
- 拖动结束（touch-end）后立即触发货架刷新（不需要 Apply）
- 重置：拖回两端 = 无价格筛选

#### §3.6.5 Brand Action Sheet

- Chip 流，多选，每个 Chip 右侧显示该品牌商品数量
- ≥13 个品牌时出现搜索框（在 Chip 流上方）
- 「Show all N brands」展开链接；展开后「Show less」收起
- 候选值由联动公式实时计算（见 §2.3）

#### §3.6.6 Color Action Sheet

- 色块圆形矩阵，每行 5 个，circle 32px
- 浅色（White、Beige）加 `$color-border` 1px 描边；下方文字标签 11px
- 选中态：色块内侧 3px `$color-brand` 环形边框
- 颜色枚举（固定顺序）：Black / White / Brown / Beige / Red / Blue / Green / Yellow / Pink / Purple / Orange / Gold / Silver / Multi（4象限拼色）
- 候选值物理隐藏：不在联动公式结果集中的颜色不渲染

#### §3.6.7 Category Action Sheet

- 文字 Chip 流，多选，无搜索框（≤20 项时）
- 候选值由联动公式实时计算

#### §3.6.8 排序 Action Sheet

- 标题「Sort by」，单选，选中后立即应用（无 Apply 按钮）
- 可选项由 `sort_options` CMS 按 Collection 配置，默认全部展示

| 排序选项 | 说明 | 排序逻辑 |
|------|------|------|
| Recommended（默认）| 综合推荐排序 | 后端算法，综合热度 + 相关性 |
| Price: Low to High | 价格升序 | 按 `listing_price` ASC |
| Price: High to Low | 价格降序 | 按 `listing_price` DESC |
| Newest | 最新上架 | 按 `listed_at` DESC |
| Most Popular | 最热销 | 按 `hot_score` DESC，hot_score 计算规则与首页 Feed 热度算法一致（见《首页 Feed PRD v2.3》§hot_score 定义）|

- `sort_options` 和 `sort_default` 在 CMS 按 Collection 独立配置，详见 §6.1.3
- 不同 Collection 可以开放不同排序选项，例如新品合集只开放 Newest，热卖合集默认 Most Popular

#### §3.6.9 Filter 按钮

- 固定最右，样式：⚙ 图标 + 「Filter」文字，Inter 13px
- 有抽屉筛已选条件时：图标右上角红色圆点（6px，#E53935）
- 点击 → 打开抽屉筛选器（见 §3.10）


---

### §3.7 结果数量通栏

- 高度 32px，水平 padding 16px
- 文案：`1,245 items`（实时，千分位格式）；加载中显示 `— items`
- fill=`$color-bg`，文字 `$color-ink-secondary` 13px
- **禁止吸顶**，必须随货架滚动

---

### §3.8 面包屑区

**UI 关联**：`looply-collection-landing-APP-v1.0.pen` → Module 9

#### §3.8.1 显示条件

- 有任意激活条件（Label ≠ All、搜索词 ≠ 空、任意快筛 / 抽屉筛有值）时显示
- 无条件时整区域隐藏，不占位
- **禁止吸顶**

#### §3.8.2 布局

- padding 8px 16px，flex-wrap（允许换行），gap 8px
- 「Clear All」按钮始终固定在最右侧；「☆ Save」在 Clear All 右侧

#### §3.8.3 Chip 样式

- fill=`$color-accent-light`，文字 / ✕ 颜色：`$color-accent`，border-radius 12px
- 文案格式：`{属性名}: {值}` 或 `{属性名}: {值1}, {值2}`（同属性多值合并一个 chip）

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

#### §3.8.4 逐项移除

点击 Chip ✕：
1. 从激活条件中移除该属性对应值
2. 同步回源：来源为快筛 → 更新 Chip 角标；来源为抽屉筛 → 更新抽屉内部状态；来源为 Label → 切回 All；来源为搜索词 → 清空搜索栏
3. 立即重新计算，刷新商品列表（**不触发** Auto-Scroll）
4. 移除后所有条件为空 → 面包屑区隐藏

#### §3.8.5 Clear All

- 文案「Clear All」，Inter 13px，`$color-ink-secondary`，无背景
- 点击：清空所有条件（Label→All，搜索→空，快筛→清空，抽屉筛→清空），刷新商品列表

#### §3.8.6 Save 按钮

- 有已选条件时出现；未保存态「☆ Save」，已保存态「★ Saved」（`$color-brand`）
- 未登录时点击 → 跳转登录页，登录后回跳自动执行保存（见 §2.4）

---

### §3.9 商品网格

**UI 关联**：`looply-collection-landing-APP-v1.0.pen` → Module 1（网格区域）

- 双列，列间距 8px，行间距 16px，左右 padding 16px
- 商品卡：复用首页 Feed ProductCard 组件（Feed PRD v2.3 §3.2），不单独设计
- 置顶商品（`pinned_listings`）排网格最前，后端处理，前端无特殊标记
- 加载：同比例灰色骨架屏
- 无限滚动分页，触底前 3 屏预加载下一页
- 点击商品 → 跳转 PDP


---

### §3.10 抽屉筛选器

**UI 关联**：`looply-collection-landing-APP-v1.0.pen` → Module 10（默认）、Module 11（Color 展开）

#### §3.10.1 整体结构

```
┌────────────────────────────┬───────────┐
│  ✕  Filter            Reset│           │
├────────────────────────────┤ 右侧 1/3  │
│  Brand               ▲     │ 露出区域  │
│  [Chanel] [LV] [Gucci]...  │（无遮罩） │
├────────────────────────────┤           │
│  Price               ▲     │           │
├────────────────────────────┤           │
│  Condition           ▲     │           │
├────────────────────────────┤           │
│  Color               ▼     │           │
├────────────────────────────┤           │
│  ...其他属性节...           │           │
├────────────────────────────┤           │
│  [ Apply · 84 items ]      │           │
└────────────────────────────┴───────────┘
 ←── 屏幕宽度 66.6% ──→ ← 33.3% →
```

- 宽度：屏幕 × 66.6%，从左侧 slide-in（250ms ease-out）
- 背景 white，右侧 1/3 无蒙层，底层商品流完全可见

#### §3.10.2 开关路径

| 路径 | 触发方式 | 是否应用变更 |
|------|------|------|
| 打开 | 点击工具栏「⚙ Filter」按钮 | — |
| 关闭 A | 点击抽屉内「✕」| 否（取消）|
| 关闭 B | 二次点击「⚙ Filter」| 否（取消）|
| 关闭 C | 点击右侧 1/3 露出区域 | 否（取消）|
| 关闭 D | 向右 swipe-to-close | 否（取消）|
| 提交 | 点击底部「Apply」| 是 |

#### §3.10.3 顶部操作栏

- 高度 52px，padding 0 16px
- 左侧：「✕」图标 + 「Filter」文字（Inter 16px 600）
- 右侧：「Reset」文字按钮（Inter 14px，`$color-ink-secondary`）
- 底部 1px `$color-border` 分割线

#### §3.10.4 Brand 属性节

- 默认展开，最多显示 2 行（约 8~10 个 chip）
- Chip 样式：含商品数量，多选
- 「↓ Show all N brands」展开链接，展开后「↑ Show less」收起
- 展开全部时（>12 个）出现搜索框；≤12 个时无搜索框

#### §3.10.5 Price 属性节

- 默认展开
- **Range Slider**，规格与 §3.6.4 一致
- 抽屉内拖动不即时刷新，纳入 Apply 统一提交

#### §3.10.6 Condition 属性节（4 级，与商品系统 PRD v1.7 对齐）

- 默认展开
- Chip 形式展示，多选，无描述文字（抽屉空间有限）
- 枚举同 §3.6.3，前台展示名：Like New / Excellent / Good / Fair
- 选中态 Chip：fill=`$color-brand`，white 文字；未选中：`$color-bg` + `$color-border` 描边

#### §3.10.7 Color 属性节

- 默认折叠，点击节标题展开 / 收起
- 展开后：色块圆形矩阵，每行 5 个（circle 32px），下方文字标签 11px
- 选中态：色块内侧 3px `$color-brand` 环形边框
- 颜色枚举同 §3.6.6

#### §3.10.8 其他属性节通用规范

> 适用维度：Series / Material / Size / Authentication / Category

**显示规则**：该维度在当前 Collection 全集中有 ≥2 个不同值时才渲染该属性节；否则整节物理隐藏。

| 维度 | 控件样式 | 选择模式 | 说明 |
|------|------|------|------|
| Series | Chip grid + 搜索框 | 多选 | 同 Brand 节样式 |
| Material | Chip grid + 搜索框 | 多选 | 同 Brand 节样式 |
| Size | Visual chip grid | 多选 | 同 Color 节样式，无色块 |
| Authentication | Text chip，固定 2 项 | 单选 | Authenticated / Unverified |
| Category | Text chip 流 | 多选 | 同原有规范 |

各节默认折叠，点击节标题展开 / 收起。

#### §3.10.9 Apply 按钮

- 吸底，高度 52px，padding 水平 16px
- fill=`$color-brand`，white 文字，Inter 15px 600
- 文案：「Apply · {N} items」，N = 当前抽屉所有条件 × 快筛 × 搜索词预计算交集数量
- N = 0 时：fill=`$color-border`（置灰），文案「No items match」
- 点击：关闭抽屉 → 应用条件 → 更新快筛 Chip 角标 → 更新面包屑 → 触发 Auto-Scroll → 刷新商品列表

#### §3.10.10 Reset 按钮

- 仅清空抽屉内部选中状态，不影响快筛条件
- Reset 后 Apply 按钮显示当前快筛 + 搜索词范围内的商品总数
- 与面包屑「Clear All」区别：Reset 不关抽屉，也不清快筛

#### §3.10.11 Swipe-to-Close 手势

- 在抽屉区域内向右水平滑动
- 触发阈值：位移 > 抽屉宽度 × 40%，或释放速度 > 150 px/s
- 实时跟手（`transform: translateX`）；未达阈值 → 弹回（300ms ease-out）；超过阈值 → 关闭（200ms ease-in）
- 关闭效果同路径 A（不应用变更）

#### §3.10.12 快筛与抽屉双向状态同步

- Quick Filter 对某属性已选值 → 打开抽屉时，该属性节对应 chip 显示为选中
- 抽屉内修改 → Apply 后，对应 Quick Filter Chip 角标更新
- 抽屉 Reset → 不清 Quick Filter
- 面包屑 Clear All → 同时清 Quick Filter 和 Drawer 内部状态


---

### §3.11 Auto-Scroll 行为

#### §3.11.1 触发事件

| 触发动作 | 行为 |
|------|------|
| 点击图文 Label | 平滑滚动至 lock point |
| 搜索栏获焦 | 平滑滚动至 lock point |
| 提交搜索 | 平滑滚动至 lock point |
| Quick Filter 点选（即触发）| 立即刷新货架，同时执行 Auto-Scroll |
| 抽屉 Apply | 先关闭抽屉，再执行 Auto-Scroll |
| 面包屑 ✕ 逐项移除 | **不触发** Auto-Scroll |
| 面包屑 Clear All | **不触发** Auto-Scroll |

#### §3.11.2 lock point 定义

lock point = 搜索栏（M4）顶边紧贴顶导栏（M1）底边。

滚动量 = 当前 scroll offset 到 M4 顶边的距离，使用 `scrollTo({behavior: 'smooth'})`。

#### §3.11.3 回弹恢复

头部氛围区和 Label 行重新展现，**仅当用户主动向下拉动（pull-down gesture）时触发**，程序 Auto-Scroll 不触发回弹。

---

## §4 依赖与风险

### §4.1 CMS 侧需求（需向 CMS PRD v2.4 提需求）

Collection 落地页筛选体验的灵活性高度依赖 CMS 的配置能力。以下 5 类配置需求需在 CMS PRD v2.4 §三「合集管理」中完整定义。

#### §4.1.1 图文筛（Label）卡片配置

每个 Collection 可配置若干图文筛卡片，每张卡片定义：

| 字段 | 说明 |
|------|------|
| `label_text` | 卡片展示文案，≤20 字符 |
| `label_image_url` | 卡片图标 URL，圆形裁剪展示，为空则纯文字型 |
| `label_scope_type` | 筛选方式：`product_set`（绑定子商品集）/ `attribute_filter`（绑定属性键值对）|
| `label_product_set_id` | scope=product_set 时必填，指向商品子集 |
| `label_attr_key` + `label_attr_value` | scope=attribute_filter 时必填，如 key=brand, value=Chanel |
| `sort_order` | 卡片在 Label 行的展示顺序（升序，从 1 开始）|

**兜底策略**：若某 Collection 未配置任何 Label，前端隐藏图文筛行，不占位。

#### §4.1.2 图文筛排序

- 排序由 `labels[].sort_order` 字段决定
- CMS 运营侧需提供拖拽排序或数字输入的排序编辑界面
- 系统自动生成的「All」卡片始终置首，`sort_order = 0`，不可配置

#### §4.1.3 快筛栏配置（哪些维度出现、以什么顺序）

| 字段 | 说明 |
|------|------|
| `quick_filter_config[].attr_key` | 该 Collection 快筛栏展示哪些维度，枚举见 §6.1.2 |
| `quick_filter_config[].sort_order` | 每个维度在快筛栏中的位置（从左到右，排序 Chip 固定最左）|
| `quick_filter_config[].enum_order` | 该维度内枚举值的展示顺序（JSON 数组，值排在前）|

**兜底策略**：若 Collection 未配置 `quick_filter_config`，前端默认展示 Condition / Price / Brand 三个维度，顺序不变。

#### §4.1.4 抽屉筛配置（哪些维度出现、以什么顺序、枚举值排序）

| 字段 | 说明 |
|------|------|
| `drawer_filter_config[].attr_key` | 该 Collection 抽屉筛展示哪些维度 |
| `drawer_filter_config[].sort_order` | 每个维度在抽屉内的位置（从上到下）|
| `drawer_filter_config[].enum_order` | 该维度内枚举值的展示顺序（JSON 数组）|
| `drawer_filter_config[].default_expanded` | 该节默认是否展开（布尔值）|

**兜底策略**：若 Collection 未配置 `drawer_filter_config`，前端默认展示 Brand / Price / Condition / Color / Category，顺序不变，Brand/Price/Condition 默认展开，其余折叠。

#### §4.1.5 排序选项配置

| 字段 | 说明 |
|------|------|
| `sort_options` | 该 Collection 开放哪些排序选项（数组，枚举见 §6.1.3）|
| `sort_default` | 默认激活的排序项，必须在 `sort_options` 中 |

**兜底策略**：若未配置，展示全部 5 个排序选项，默认 Recommended。

---

### §4.2 其他上下游依赖

| 依赖 | 说明 | 状态 |
|------|------|------|
| 商品系统 PRD v1.7 属性体系 | Condition 4 级枚举、`color_hex` 字段、attr_key 枚举须对齐 | 待确认 |
| Feed PRD v2.3 §3.2 ProductCard | 商品网格复用 ProductCard 组件 | 已有 |
| 搜索推荐词接口 | 后端按 `collection_id` 返回高频品牌 + 品类名（≤10 条）| 新增接口 |
| 筛选候选值动态计算接口 | 实时返回当前条件交集下各属性候选值列表及各值商品数量 | 新增接口 |
| 筛选状态保存接口 | 序列化筛选状态写云端，与 `user_account` 绑定 | 新增接口 |
| 首页 Feed hot_score | Most Popular 排序复用 hot_score 算法（见首页 Feed PRD v2.3）| 已有算法，确认接口是否通用 |

### §4.3 风险与待确认项

| 风险 | 说明 | 责任方 |
|------|------|------|
| 筛选候选值动态计算性能 | 每次条件变动实时请求，需后端预计算或缓存 | 后端 |
| Color hex 字段缺失 | 部分老商品无 `color_hex`，需商品系统确认兜底策略 | 商品系统 |
| `color_hex` 字段归属 | 建议在属性选项表增加 `display_color_hex` 字段，需同步至商品系统 PRD | 商品系统 |
| Price Range Slider 区间端点 | 动态取全集最低/最高价，空合集时端点值兜底方案待定 | 后端 |

---

## §5 版本规划

### §5.1 V1（本文档范围）

| 功能 | 优先级 |
|------|------|
| 头部氛围区（Standard 模板）| P0 |
| 图文 Label 行（图文筛）| P0 |
| 顶导搜索栏 + 推荐词浮层 | P0 |
| Quick Filter：Condition / Price Slider / Brand（点选即触发）| P0 |
| 抽屉筛选器（Brand / Price / Condition / Color / Category + 其他属性节）| P0 |
| 面包屑区 + 逐项移除 + Clear All | P0 |
| Auto-Scroll | P0 |
| 商品网格（复用 ProductCard）| P0 |
| 筛选候选值联动计算 | P0 |
| 友好降级页（合集下线 / 空态 / 网络异常）| P0 |
| CMS 图文筛 / 快筛 / 抽屉筛 / 排序配置 | P0 |
| 筛选状态保存（云端，无查看入口）| P1 |
| Swipe-to-close 手势 | P1 |
| Quick Filter：Color / Category（按 `quick_filter_config` 配置）| P1 |

### §5.2 V2 规划

| 功能 | 说明 |
|------|------|
| PC 端 | 独立规划，侧边筛选栏范式 |
| Collection 内分享 | Share 按钮逻辑 |
| 底部相关推荐 | 底部横滑推荐区 |
| Saved Filters 个人中心页 | 查看 / 管理 / 复用已保存的筛选 |
| 筛选分享链接 | 带筛选状态的分享 URL |


---

## §6 附录

### §6.1 新增字段清单（需同步至 CMS PRD v2.4 §三）

#### §6.1.1 `labels[]` — 图文筛选 Label 列表

| 子字段 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| `label_text` | string ≤20 字符 | 是 | Label 展示文案 |
| `label_image_url` | image URL | 否 | Label 图标（图文型），20×20px |
| `label_scope_type` | enum | 是 | `product_set`（子商品集）/ `attribute_filter`（属性筛）|
| `label_product_set_id` | FK | 条件必填 | `scope_type=product_set` 时必填 |
| `label_attr_key` | string | 条件必填 | `scope_type=attribute_filter` 时必填 |
| `label_attr_value` | string | 条件必填 | `scope_type=attribute_filter` 时必填 |
| `sort_order` | number | 是 | 展示顺序（升序，从 1 开始）|

#### §6.1.2 `quick_filter_config[]` — 快筛属性配置

| 子字段 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| `attr_key` | enum | 是 | 见下方枚举 |
| `sort_order` | number | 是 | 快筛栏从左到右顺序 |

`attr_key` 枚举（V1 支持范围）：

| 值 | 说明 | 控件 |
|----|------|------|
| `condition` | 成色等级 | Action Sheet（4 级，点选即触发）|
| `price` | 价格区间 | Range Slider Action Sheet |
| `brand` | 品牌 | Chip 流 Action Sheet（点选即触发）|
| `color` | 颜色 | 色块矩阵 Action Sheet（点选即触发）|
| `category` | 类目 | Text Chip Action Sheet（点选即触发）|
| `series` | 系列 | Chip 流 Action Sheet（点选即触发）|
| `material` | 材质 | Chip 流 Action Sheet（点选即触发）|
| `size` | 尺寸 | Visual Chip Action Sheet（点选即触发）|
| `auth_status` | 认证状态 | Text Chip（2 项）Action Sheet |

默认值（未配置时）：`[condition, price, brand]`

> 注意：`price` 和 `auth_status` 在抽屉筛中走固定控件路径。

#### §6.1.3 `sort_options` + `sort_default`

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `sort_options` | array of enum | 否 | 开放的排序选项，空时展示全部 5 项 |
| `sort_default` | enum | 否 | 默认激活排序，默认 `recommended` |

可选值：`recommended` / `price_asc` / `price_desc` / `newest` / `popular`

#### §6.1.4 `drawer_filter_config[]` — 抽屉筛选器配置（新增）

| 子字段 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| `attr_key` | enum | 是 | 枚举同 §6.1.2 |
| `sort_order` | number | 是 | 该节在抽屉中的上下顺序 |
| `enum_order` | array of string | 否 | 该维度内枚举值的展示顺序（未配置则按商品数量降序）|
| `default_expanded` | boolean | 否 | 默认是否展开，默认 false（Brand/Price/Condition 默认 true）|

---

本文档 V1 对应原型文件：**`looply-collection-landing-APP-v1.0.pen`**

| Module | 页面名称 | 对应 PRD 章节 |
|--------|------|------|
| Module 1 | 默认态 · Standard 模板 | §3.1、§3.2、§3.3、§3.4、§3.6、§3.9 |
| Module 2 | 搜索激活态（含推荐浮层）| §3.2.3 |
| Module 3 | 排序 Action Sheet | §3.6.8 |
| Module 4 | Condition 快筛 Action Sheet | §3.6.3 |
| Module 5 | Brand 快筛 Action Sheet | §3.6.5 |
| Module 6 | Price 快筛 Range Slider | §3.6.4 |
| Module 7 | 面包屑已选条件态 | §3.8 |
| Module 8 | 抽屉筛选器 · 默认展开态 | §3.10 |
| Module 9 | 抽屉筛选器 · Color 展开态 | §3.10.7 |
| Module 10 | 降级页 · 合集下线 | §2.5 |
| Module 11 | 降级页 · 筛选后 0 件 | §2.5 |

---

### §6.3 筛选维度全集（V1 支持范围）

| 维度 | 数据字段 | 挂载层级 | 走 attr_key 动态路径 | 快筛控件 | 快筛默认展示 | 抽屉筛支持 |
|------|------|------|------|------|------|------|
| Brand | `brand_id` → 品牌名 | SPU | 否（结构字段）| Chip + 搜索 | ✓（默认）| ✓ |
| Series | `series_id` → 系列名 | SPU | 否（结构字段）| Chip + 搜索 | 可配置 | ✓ |
| Category | `category_id` → 类目名 | SPU | 否（结构字段）| Text chip | 可配置 | ✓ |
| Color | `attr_key=color` | SKU（销售属性）| 是 | Visual chip | 可配置 | ✓ |
| Material | `attr_key=material` | SKU（销售属性）| 是 | Chip + 搜索 | 可配置 | ✓ |
| Size | `attr_key=size` | SKU（销售属性）| 是 | Visual chip | 可配置 | ✓ |
| Condition | `condition_grade` | Product | 否（结构字段）| List + 描述 | ✓（默认）| ✓ |
| Authentication | `auth_status` | Product | 否（结构字段）| Text chip 2 项 | 可配置 | ✓ |
| Price | `listing_price` | Listing | 否（价格字段）| Range picker | ✓（默认）| ✓ |

