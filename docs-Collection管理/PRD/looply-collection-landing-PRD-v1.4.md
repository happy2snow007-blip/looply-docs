# Looply · Collection 落地页 — 产品需求文档

**版本** v1.4 | **日期** 2026-06-23 | **受众** UI 设计师 · 前端开发 · CMS 开发
**依赖** CMS PRD v2.4 · 商品系统 PRD v1.7 · 首页 PRD v1.0
**范围** Collection 落地页 · Mobile 端（PC 端 V2）

**v1.3 → v1.4 变更说明**：架构重构——引入 Template / UI Variant / Dictionary 三层配置体系，叠加 Collection Content 形成四层架构；Collection Basic Info 新增 `market_id` / `channel_id` / `subtitle`，`template_id` 替代原 `landing_page_template`；Visual Filter 配置字段对齐最终版（`filter_condition` + `status` 字段）；Quick Filter / Drawer Filter 配置结构简化为 `attr_key + enabled + sort_order`；`authentication` 从 CMS 可配维度中删除；Sort 配置结构调整为 `sort_key + enabled + sort_order + is_default`；Filter Bar 作为独立 Block Type 存在，包含 Sort（左）+ Drawer 入口（右）；筛选维度 UI 行为（value_display_type / selection_mode / group_by 等）统一由 UI Variant 决定，不再由 Collection Content 配置。

---

## 目录

- [§1 概述](#1-概述)
- [§2 配置架构层](#2-配置架构层)
  - [§2.1 四层配置体系](#21-四层配置体系)
  - [§2.2 Template 配置](#22-template-配置)
  - [§2.3 UI Variant 配置](#23-ui-variant-配置)
  - [§2.4 Dictionary 配置](#24-dictionary-配置)
- [§3 数据逻辑层](#3-数据逻辑层)
  - [§3.1 Collection Content 字段映射](#31-collection-content-字段映射)
  - [§3.2 Collection 全集定义](#32-collection-全集定义)
  - [§3.3 筛选候选值联动规则](#33-筛选候选值联动规则)
  - [§3.4 筛选状态保存机制](#34-筛选状态保存机制)
  - [§3.5 空态与降级规则](#35-空态与降级规则)
- [§4 页面与交互](#4-页面与交互)
  - [§4.1 页面整体布局与吸顶](#41-页面整体布局与吸顶)
  - [§4.2 顶导栏与搜索栏](#42-顶导栏与搜索栏)
  - [§4.3 头部氛围区（Banner Block）](#43-头部氛围区banner-block)
  - [§4.4 图文筛行（Visual Filter Block）](#44-图文筛行visual-filter-block)
  - [§4.5 集内搜索](#45-集内搜索)
  - [§4.6 快筛栏（Quick Filter Block）](#46-快筛栏quick-filter-block)
  - [§4.7 工具栏（Filter Bar Block）](#47-工具栏filter-bar-block)
  - [§4.8 结果数量通栏](#48-结果数量通栏)
  - [§4.9 面包屑区](#49-面包屑区)
  - [§4.10 商品网格（Product Grid Block）](#410-商品网格product-grid-block)
  - [§4.11 抽屉筛选器](#411-抽屉筛选器)
  - [§4.12 Auto-Scroll 行为](#412-auto-scroll-行为)
- [§5 依赖与风险](#5-依赖与风险)
- [§6 版本规划](#6-版本规划)
- [§7 附录](#7-附录)

---

## §1 概述

### §1.1 背景与目标

Collection 落地页是 Looply 的「主题货架」页，承接首页 home_collections 坑位和 Shop 页 shop_collections 坑位的跳转。

**目标**：
1. 通过运营配置的视觉素材传递合集氛围，建立品牌信任
2. 提供完整筛选链路（图文筛 + 快筛 + 抽屉筛），帮用户快速锁定目标商品
3. 「零空结果」体验——交集为 0 的属性值物理隐藏，用户不会走进死胡同
4. 复用首页 Feed ProductCard 组件，保持全站视觉一致性
5. 通过 Template / UI Variant 配置体系支持多种页面结构，无需开发即可新建页面模板

### §1.2 不做什么

| 不做 | 说明 |
|------|------|
| PC 端 | V1 仅 Mobile，PC 端独立规划（V2） |
| Collection 内分享 | Share 按钮 UI 预留，逻辑 V2 |
| 底部相关推荐 | Collection 页底部不做相关推荐入口，V2 规划 |
| 筛选条件分享链接 | URL 参数由后端在用户分享时自动生成，V1 不做显式「复制筛选链接」功能 |
| Search Block | 一期不做，Template 可预留，逻辑 V2 |

### §1.3 用户角色

| 角色 | 说明 |
|------|------|
| 买家（C 端 Mobile 用户）| 浏览合集商品、筛选选品、跳转 PDP |

### §1.4 核心场景

| 场景 | 用户动作 | 关键模块 |
|------|------|------|
| 氛围浏览 | 进入页面后滑动浏览海报和商品 | Banner Block、商品网格 |
| 主题切入 | 点击图文筛 Label 切换子主题 | Visual Filter Block |
| 关键词搜索 | 在集内搜索栏输入品牌名/品类 | 集内搜索（顶导内嵌）|
| 快速筛选 | 点击快筛 Chip，弹出二级面板，Apply 提交 | Quick Filter Block |
| 精细筛选 | 打开抽屉筛，多维度组合，Apply 提交 | 抽屉筛选器（Filter Bar Block 触发）|
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
| Collection Content | 运营在 CMS 配置的合集内容（标题、Banner 图、图文筛项目、筛选器维度、排序等）|
| Template | 产品/设计/Admin 配置的页面结构模板，定义页面由哪些 Block 组成、顺序及各 Block 使用的 UI Variant |
| UI Variant | 定义某类 Block 的展示样式、交互规则（如 Chip 高度、是否支持 View All、分组方式等）|
| Dictionary | 系统级映射字典，如 Color Dictionary（颜色码→展示名称+色值+色系）、Price Band Dictionary |
| Block | 页面的组成单元，类型见 §2.2.3 |
| Visual Filter | 图文筛，Block 类型之一，运营配置图文 Label 列表，用户点击切换子主题商品池 |
| Label | Visual Filter Block 内运营配置的一个图文筛项目 |
| Quick Filter | 快筛，Block 类型之一，横排滚动 Chip 栏 |
| Filter Bar | Block 类型之一，包含 Sort（左）+ Drawer Filter 入口（右）|
| Drawer Filter | 屏幕左侧 66.6% 宽无遮罩抽屉，全量属性维度，Apply 后提交 |
| Collection 全集 | 该 Collection 下所有 `listing_status = active` 的商品，不附加任何筛选条件（见 §3.2）|
| 面包屑（Breadcrumb）| 已选条件 Chip 展示区，在商品网格正上方 |
| Auto-Scroll | 筛选动作触发时页面自动平滑滚至搜索栏贴顶 |
| lock point | Auto-Scroll 目标：搜索栏贴紧顶导栏底部 |
| 物理隐藏 | 候选值不在后端返回列表中时前端不渲染该值，从 DOM 移除 |
| View All | 快筛二级面板/抽屉筛属性节内候选项超过 8 个时出现的展开控件 |

---
## §2 配置架构层

> 本章描述 Collection 页面的配置体系。这是 v1.4 相对 v1.3 最核心的架构变化。

### §2.1 四层配置体系

Collection 页面的配置分为四个层级，由不同角色负责维护：

| 层级 | 配置主体 | 职责 |
|------|------|------|
| Collection Content | 运营 | 配置页面展示什么内容（Banner 图、图文筛项、筛选器维度列表、排序选项等）|
| Template | 产品/设计/Admin | 配置页面由哪些 Block 组成、Block 顺序、每个 Block 使用哪个 UI Variant |
| UI Variant | 产品/设计/Admin | 配置每个 Block 长什么样、如何排列、如何交互、内容展示规则 |
| Dictionary | 产品/运营/Admin | 配置颜色映射（Color Dictionary）、价格区间（Price Band Dictionary）等基础字典 |

**关系说明**：

```
Collection ──关联──▶ Template
                        │
                        ├── Block 1: banner ──────▶ UI Variant: banner_v1
                        ├── Block 2: visual_filter ─▶ UI Variant: visual_filter_v1
                        ├── Block 3: quick_filter ──▶ UI Variant: quick_filter_v1
                        ├── Block 4: filter_bar ────▶ UI Variant: filter_bar_v1
                        └── Block 5: product_grid ──▶ UI Variant: product_grid_v1
```

- **Template 决定**：页面有哪些模块、模块顺序、每个模块使用哪个 UI Variant
- **UI Variant 决定**：Chip 长什么样、Color 如何展示、是否支持 Group By、每行几个 Value、Drawer 多宽等所有展示行为
- **Collection Content 决定**：每个模块内展示什么内容（具体图片、文案、哪些筛选维度、哪些排序项）
- **Dictionary 决定**：颜色展示名称与色值映射、Price Band 区间定义

运营创建 Collection 时必须先选择 Template。后续各模块的展示行为规则均继承自 Template 所引用的 UI Variant，运营只需关注内容配置，不决定界面样式。

---

### §2.2 Template 配置

Template 由产品/设计/Admin 维护，运营只能从已有 Template 中选择。

#### §2.2.1 Template 基础字段

| 配置项 | 中文名称 | 示例 | 说明 |
|--------|--------|------|------|
| `template_id` | 模板 ID | `collection_app_default_v1` | 模板唯一标识，系统生成 |
| `template_name` | 模板名称 | `Collection App Default` | 后台展示名称 |
| `platform` | 平台 | `app` | `app` / `web` |
| `app_shell_id` | 页面框架 | `collection_app_shell_v1` | 决定该页面使用哪套顶导、底导、系统级导航交互 |
| `preview_image_url` | 模板预览图 | `xxx.png` | 页面整体预览，运营选模板时展示 |
| `description` | 模板说明 | `Standard Collection Template` | 模板用途说明 |
| `status` | 状态 | `active` | `draft` / `active` / `deprecated` |

#### §2.2.2 Page Block 配置（Block Builder 模式）

Template 采用 Block Builder 模式，页面由多个 Block 组成。同一种 Block 类型支持重复出现（如多个 `visual_filter` Block 并排）。

| 配置项 | 中文名称 | 示例 | 说明 |
|--------|--------|------|------|
| `block_order` | Block 顺序 | `1, 2, 3...` | 页面从上到下的展示顺序 |
| `block_type` | Block 类型 | `visual_filter` | 见下方枚举 |
| `block_variant_id` | UI 方案 | `visual_filter_v1` | 当前 Block 使用的 UI Variant |
| `enabled` | 是否启用 | `true` | 是否展示该 Block |

#### §2.2.3 Block Type 枚举

| block_type | 中文名称 | 说明 |
|------------|--------|------|
| `search` | 搜索 | 集内搜索框（一期不做，Template 可预留）|
| `banner` | Banner | 头部氛围图 |
| `visual_filter` | 图文筛 | 图文 Label 横滑行 |
| `quick_filter` | 快筛 | 属性 Chip 横滑栏 |
| `filter_bar` | 排序 + 抽屉筛栏 | Sort（左）+ Drawer Filter 入口（右）|
| `product_grid` | 商品列表 | 商品卡双列网格 |

#### §2.2.4 默认模板示例（`collection_app_default_v1`）

| 顺序 | Block 类型 | UI Variant |
|------|-----------|-----------|
| 1 | `banner` | `banner_v1` |
| 2 | `visual_filter` | `visual_filter_v1` |
| 3 | `quick_filter` | `quick_filter_v1` |
| 4 | `filter_bar` | `filter_bar_v1` |
| 5 | `product_grid` | `product_grid_v1` |

#### §2.2.5 Template 数量限制

| 平台 | 最少 Block 数 | 最大 Block 数 | 来源 |
|------|------------|------------|------|
| APP | Template 配置 | Template 配置 | Template 自定义 |

---

### §2.3 UI Variant 配置

UI Variant 由产品/设计/Admin 维护，定义某类 Block 的所有展示与交互规则。

#### §2.3.1 UI Variant 基础字段

| 配置项 | 中文名称 | 示例 | 说明 |
|--------|--------|------|------|
| `variant_id` | UI 方案 ID | `quick_filter_v1` | UI 方案唯一标识 |
| `variant_name` | UI 方案名称 | `Quick Filter Inline Card` | 后台展示名称 |
| `block_type` | Block 类型 | `quick_filter` | 适用于哪个 Block |
| `platform` | 平台 | `app` | `app` / `web` |
| `preview_image_url` | UI 预览图 | `xxx.png` | UI 效果预览 |
| `status` | 状态 | `active` | 是否可被 Template 引用 |

#### §2.3.2 Banner Variant（block_type = banner）

| 配置项 | 示例 | 说明 |
|--------|------|------|
| `image_ratio` | — | 图片比例 |
| `image_height` | `180px` | Banner 高度 |
| `image_fit` | `cover` | 图片裁切方式 |
| `title_overlay_enabled` | `true` | 标题是否叠加在图片上 |

> 完整字段需设计 & 前端介入确认。

#### §2.3.3 Visual Filter Variant（block_type = visual_filter）

| 配置项 | 示例 | 说明 |
|--------|------|------|
| `item_layout` | `image_text` | 图文布局 |
| `image_shape` | `round` | 圆图/方图 |
| `image_size` | `48px` | 图片尺寸 |
| `image_ratio` | `1:1` | 图片比例 |
| `layout_type` | `horizontal_scroll` | 横滑/Grid |
| `visible_count_per_screen` | — | 一屏展示几个 Label |
| `min_item_count` | — | 最少配置几个 Label |
| `max_item_count` | — | 最多配置几个 Label |
| `label_max_length` | — | 文案最大长度 |
| `label_line_count` | — | 文案最大行数 |
| `active_style` | `purple_border` | 选中态样式 |

> 完整字段需设计 & 前端介入确认。

#### §2.3.4 Quick Filter Variant（block_type = quick_filter）

**一级筛选 UI 配置**：

| 配置项 | 示例 | 说明 | 枚举 |
|--------|------|------|------|
| `quick_filter_bar_style` | `horizontal_scroll` | 快筛栏排列方式 | — |
| `min_attribute_count` | — | 最少筛选维度数量 | — |
| `max_attribute_count` | — | 最多筛选维度数量 | — |
| `layout_type` | `横滑` | 快筛栏不同筛选排布方式 | — |
| `panel_style` | `inline_card` | 二级展开方式 | 一期只有向下展开 |
| `entry_chip_height` | `36px` | 一级 Chip 高度 | — |
| `entry_chip_radius` | `18px` | 一级 Chip 圆角 | — |
| `selected_style` | `purple_tint` | 一级筛选选中态样式 | — |
| `sticky_enabled` | `true` | 是否吸顶 | — |

**二级筛选（per 维度）UI 配置**：

| 配置项 | 示例 | 说明 | 枚举 |
|--------|------|------|------|
| `attr_key` | `brand` | 一级筛选维度 | 见 §7.1.2 |
| `value_display_type` | `text_chip` | 筛选项样式 | `text_chip` / `color_chip` / `price_band_slider` |
| `selection_mode` | `multi` | 选择方式 | `multi` / `range` |
| `group_by` | `category_l2` | 分组规则 | `none` / `category_l2` |
| `value_column_count` | — | Value 每行展示数量 | — |
| `value_default_visible_count` | — | 默认展示 Value 数量 | — |
| `value_view_all_enabled` | `true` | 是否支持 View All | — |
| `value_view_all_position` | `bottom` | View All 位置 | — |
| `color_chip_size` | `32px` | Color Chip 尺寸（仅 color_chip 时有效）| — |
| `value_selected_style` | `purple_tint` | 二级筛选选中态样式 | — |

#### §2.3.5 Filter Bar Variant（block_type = filter_bar）

**Filter Bar 外层配置**：

| 配置项 | 示例 | 说明 |
|--------|------|------|
| `layout_type` | `left_right` | 左右布局 |
| `left_component` | `sort` | 左侧：排序 |
| `right_component` | `drawer_trigger` | 右侧：抽屉筛入口 |
| `sticky_enabled` | `true` | 是否吸顶 |
| `bar_height` | `44px` | 工具栏高度 |

**Sort 排序字段配置**：

| 配置项 | 示例 | 说明 |
|--------|------|------|
| `panel_style` | `inline_card` | 二级展开方式 |
| `value_selected_style` | `purple_tint` | 排序选中态样式 |

**Drawer Filter Variant 外层配置（抽屉筛）**：

| 配置项 | 示例 | 说明 |
|--------|------|------|
| `drawer_position` | `left` | 左侧滑出抽屉 |
| `drawer_width` | — | 占屏宽度 |
| `default_expanded_count` | — | 默认展开几个维度 |

**Drawer Filter Variant 二级筛选（per 维度）配置**：

| 配置项 | 示例 | 说明 | 枚举 |
|--------|------|------|------|
| `attr_key` | `brand` | 一级筛选维度 | 见 §7.1.3 |
| `value_display_type` | `text_chip` | 筛选项样式 | `text_chip` / `color_chip` / `price_band_slider` |
| `selection_mode` | `multi` | 选择方式 | `multi` / `range` |
| `group_by` | `category_l2` | 分组规则 | `none` / `category_l2` |
| `value_column_count` | — | Value 每行展示数量 | — |
| `value_default_visible_count` | — | 默认展示 Value 数量 | — |
| `value_view_all_enabled` | `true` | 是否支持 View All | — |
| `value_view_all_position` | `bottom` | View All 位置 | — |
| `color_chip_size` | `32px` | Color Chip 尺寸 | — |
| `value_selected_style` | `purple_tint` | 二级筛选选中态样式 | — |
| `price_value_default_visible_count` | — | 价格带默认展示数量（attr_key = price 时有效）| — |

#### §2.3.6 Product Grid Variant（block_type = product_grid）

| 配置项 | 示例 | 说明 |
|--------|------|------|
| `column_count` | `2` | 商品列数 |
| `card_style` | `feed_product_card` | 商品卡样式 |
| `row_gap` | `16px` | 行间距 |
| `column_gap` | `8px` | 列间距 |

---

### §2.4 Dictionary 配置

#### §2.4.1 Color Dictionary

颜色码到展示名称、色值、色系的映射表，由产品/运营/Admin 维护。

| 配置项 | 示例 | 说明 |
|--------|------|------|
| `color_code` | `black` | 商品颜色值（与商品系统对应）|
| `display_name` | `Black` | 前台展示名称 |
| `color_hex` | `#000000` | 色值，用于色块渲染 |
| `color_family` | — | 色系分组 |

#### §2.4.2 Price Band Dictionary

价格区间配置，用于 Quick Filter 和 Drawer Filter 的 Price 维度。

| 配置项 | 示例 | 说明 |
|--------|------|------|
| `band_label` | `Under $500` | 展示文案 |
| `min_price` | `null` | 最低价格（null 表示无下限）|
| `max_price` | `500` | 最高价格（null 表示无上限）|

> Price Band 可在 Collection Content 层按合集独立覆盖（见 §3.1.3）。

---
## §3 数据逻辑层

> 本章定义后端计算规则和前端消费的数据约定。配置架构见第二章，UI 与交互细节见第四章。

### §3.1 Collection Content 字段映射

运营在 CMS 配置 Collection 内容时，操作以下字段：

#### §3.1.1 Collection Basic Info（基础信息）

| CMS 字段 | 中文名称 | 示例 | 枚举/来源 | 说明 | 备注 |
|---------|--------|------|---------|------|------|
| `status` | 状态 | `active` | `draft` / `active` / `inactive` | 控制 Collection 是否上线 | `inactive` 时允许仅保存基础信息；`active` 时其余必填项需校验通过 |
| `collection_id` | Collection ID | 系统生成 | 系统生成 | Collection 唯一标识 | 不可编辑 |
| `collection_name` | 后台名称 | `Luxury Bags Internal` | 文本 | 后台管理使用 | 必填 |
| `title` | 页面标题 | `Luxury Bags` | 文本 | 顶导栏标题 + Banner 大标题 | 最大长度由 Template 决定 |
| `subtitle` | 页面副标题 | `Timeless Pieces` | 文本 | Banner 副标题 | 可选，最大长度由 Template 决定 |
| `market_id` | 市场 | `US` | 市场配置中心 | 控制商品池范围 | — |
| `channel_id` | 渠道 | `APP` | 渠道配置中心 | — | — |
| `template_id` | 页面模板 | `collection_app_default_v1` | Template Library | 决定页面结构与交互 | 运营只能选择可用模板 |

#### §3.1.2 Banner 配置

| CMS 字段 | 中文名称 | 示例 | 说明 | 备注 |
|---------|--------|------|------|------|
| `module_enabled` | 是否展示 Banner | `TRUE` | 是否展示 Banner Block | `FALSE` 时不校验 Banner 内容 |
| `banner_image_url` | Banner 图片 | `xxx.jpg` | 图片上传 | 图片尺寸由 Template 决定 |

#### §3.1.3 Visual Filter（图文筛）配置

**模块配置**：

| CMS 字段 | 中文名称 | 示例 | 说明 | 备注 |
|---------|--------|------|------|------|
| `module_enabled` | 是否展示图文筛 | `TRUE` | 是否展示 Visual Filter Block | `FALSE` 时不校验图文筛配置 |

**图文筛项配置（每项）**：

| CMS 字段 | 中文名称 | 示例 | 说明 | 备注 |
|---------|--------|------|------|------|
| `status` | 是否展示 | `active` | `active` / `inactive` | 用于临时隐藏单个图文筛项 |
| `label_text` | 展示文案 | `Chanel Classic` | 文本 | 文案长度由 Template 决定 |
| `image_url` | 图片 | `xxx.jpg` | 图片上传 | 图片尺寸由 Template 决定 |
| `filter_condition` | 筛选条件 | `Brand=Chanel` | CMS 规则编辑器 | 决定该图文 Label 对应哪些商品，基于当前 Collection 商品池生效 |
| `sort_order` | 排序 | 正整数 | 展示顺序 | 支持拖拽排序 |

**图文筛数量限制**：仅当 `module_enabled = TRUE` 时生效，最少/最大数量由所选 Template 的 Visual Filter Variant 配置。

系统自动生成「All」Label，固定置首（sort_order = 0），运营不可配置。

#### §3.1.4 Quick Filter（快筛）配置

**模块配置**：

| CMS 字段 | 中文名称 | 说明 |
|---------|--------|------|
| `module_enabled` | 是否展示快筛 | `FALSE` 时不校验快筛配置 |

**快筛项配置（每项）**：

| CMS 字段 | 中文名称 | 示例 | 说明 | 备注 |
|---------|--------|------|------|------|
| `attr_key` | 筛选字段 | `brand` | 商品属性字段 | 必填，枚举见 §7.1.2 |
| `enabled` | 是否展示 | `TRUE` | 是否展示该快筛项 | 用于临时隐藏单个筛选项 |
| `sort_order` | 排序 | 正整数 | 从左到右排序 | — |

`attr_key` 枚举：`brand` / `series` / `category` / `material` / `color` / `size` / `condition` / `price`

**快筛数量限制**：最少/最大维度数量由所选 Template 的 Quick Filter Variant 配置。

#### §3.1.5 Drawer Filter（抽屉筛）配置

**模块配置**：

| CMS 字段 | 中文名称 | 说明 |
|---------|--------|------|
| `module_enabled` | 是否展示抽屉筛 | `FALSE` 时不校验抽屉筛配置 |

**抽屉筛项配置（每项）**：

| CMS 字段 | 中文名称 | 示例 | 说明 | 备注 |
|---------|--------|------|------|------|
| `attr_key` | 筛选字段 | `brand` | 商品属性字段 | 必填，枚举见 §7.1.3 |
| `enabled` | 是否展示 | `TRUE` | 是否展示该抽屉筛项 | 用于临时隐藏单个筛选项 |
| `sort_order` | 排序 | 正整数 | 从上到下排序 | — |

`attr_key` 枚举：`brand` / `series` / `category` / `material` / `color` / `size` / `condition` / `price`

#### §3.1.6 Sort（排序）配置

**模块配置**：

| CMS 字段 | 中文名称 | 说明 |
|---------|--------|------|
| `module_enabled` | 是否展示排序 | `FALSE` 时不校验排序配置 |

**排序项配置（每项）**：

| CMS 字段 | 中文名称 | 示例 | 说明 | 备注 |
|---------|--------|------|------|------|
| `sort_key` | 排序字段 | `recommended` | CMS 配置排序方式 | 客户端只消费排序字段 |
| `enabled` | 是否展示 | `TRUE` | 是否展示该排序项 | 用于临时隐藏单个排序项 |
| `sort_order` | 展示顺序 | 正整数 | 展示顺序 | — |
| `is_default` | 默认排序 | `true` | 默认选中项 | 只能有一个 |

`sort_key` 枚举：`recommended` / `price_asc` / `price_desc` / `newest` / `popular`

**兜底策略**：若 Collection 未配置排序，展示全部 5 个选项，默认 `recommended`。

---

### §3.2 Collection 全集定义

**Collection 全集** = 该 Collection 下所有 `listing_status = active` 的商品，不附加任何用户筛选条件。

全集是所有候选值计算的基准锚点，不随用户操作改变。

---

### §3.3 筛选候选值联动规则

#### §3.3.1 联动公式

**维度 X 的候选值** =

```
Collection 全集（§3.2）
∩ 当前 Label 范围（Visual Filter 选中项）
∩ 搜索词
∩ 所有其他已激活条件（快筛 + 抽屉筛，排除维度 X 本身）
```

换句话说：用当前所有条件——但排除维度 X 自己——圈出商品集合，再从这个集合里反查维度 X 有哪些值出现过，那些值就是可展示的候选值。

**示例**：

> 用户在「Chanel Bags」Collection 里已激活：Brand = Chanel、Price < $2,000。
> 此时计算 Color 的候选值：取全集 ∩ 无 Label 过滤 ∩ 无搜索词 ∩ Brand=Chanel ∩ Price<$2,000（不加 Color 条件）→ 得到 320 件商品 → 反查颜色 → 得 Black: 180, Beige: 90, Red: 50
>
> Color 二级面板只展示这 3 个颜色，其余颜色物理隐藏。

#### §3.3.2 计算规则

- 任一已激活条件变化 → 所有维度候选值实时重新计算
- 不在返回候选列表中的属性值：前端物理隐藏（不渲染，不占位）
- 后端返回某维度候选值时，同步返回每个值的商品数量，数量为 0 的 value 不下发
- 后端返回候选值须为**全量**列表（不截断），前端负责展示截断和 View All 逻辑
- Quick Filter：多选，Apply 提交后触发货架刷新
- 抽屉筛：勾选后不即时刷新，统一由底部 Apply 按钮提交
- 动态计算接口的 debounce / cache 策略由后端决定

#### §3.3.3 高层级重置规则

切换 Label 或输入新搜索词 → 所有快筛条件 + 抽屉筛条件立即全部清空，面包屑同步清空。

#### §3.3.4 Price 筛选合并规则

Price 支持两种选择方式，两者取**并集**后作为价格筛选条件：

- **价格带**：运营配置若干价格区间（基于 Price Band Dictionary），用户多选，每个区间内的商品均纳入结果
- **Range Slider**：双端滑块自定义区间，Slider 最大值为本 Collection 最贵 listing 价格

**并集逻辑**：

```
价格筛选结果 = 所有选中价格带覆盖的价格范围 ∪ Slider 区间
```

示例：选中「$500–$1,000」价格带 + Slider 拖到「$200–$400」→ 商品价格在 [$200–$400] ∪ [$500–$1,000] 范围内均显示。

只使用其中一种时退化为单区间筛选。两种方式均未选时，视为无价格筛选条件。

---

### §3.4 筛选状态保存机制

- 入口：面包屑区「☆ Save」按钮（有已选条件时才显示）
- 保存内容：`{label_id, search_keyword, quick_filter_values, drawer_filter_values}`，序列化存云端，与 `user_account` 绑定
- 保存后：按钮变「★ Saved」，Toast 提示「Filters saved」
- 未登录：跳转登录页，登录后自动回跳并执行保存
- **V1 不提供查看已保存筛选的入口**；已保存的筛选后端持久化，V2 在个人中心统一管理和复用

---

### §3.5 空态与降级规则

| 状态 | 触发条件 | 处理 |
|------|------|------|
| 无效 slug / inactive | `status ≠ active` | 友好提示页：插画 + "This collection is no longer available" + "Browse Collections" 按钮 |
| 展示时间超出范围 | 超出 `display_time` | 友好提示页：插画 + "This collection has ended" + "Browse Collections" 按钮 |
| 合集内商品全部下架 | 网格无商品，无筛选条件 | 插画 + "Nothing here yet" + "Browse Other Collections" 按钮 |
| 筛选后 0 件商品 | 有激活条件但交集为空 | 插画 + "No items match your filters" + "Clear All Filters" 链接 |
| 网络异常 | 接口报错 | Toast "Something went wrong" + 骨架屏保持 + "Try Again" 按钮 |
| 加载中 | 首次进入/刷新 | 双列骨架屏：上方头部区灰色色块占位（与头图等比例），下方商品卡等比例灰色色块 2 列排列 |

---
## §4 页面与交互

> 本章按模块顺序定义各 UI 区域的外观、状态变化和交互行为。数据计算逻辑见第三章，配置架构见第二章。

### §4.1 页面整体布局与吸顶

#### §4.1.1 纵向模块列表

页面 Block 的顺序由所选 Template 决定。以默认模板 `collection_app_default_v1` 为例：

```
┌─────────────────────────────┐
│  顶导栏 + 搜索栏（44px）     │  ★ 始终固定（搜索并入顶导）
├─────────────────────────────┤
│  Banner Block（180px）      │  随流滚动
├─────────────────────────────┤
│  Visual Filter Block（48px）│  随流滚动
╠═════════════════════════════╣
│  Quick Filter Block（44px） │  ★ 吸顶（z-index 100）
╠═════════════════════════════╣
│  Filter Bar Block（44px）   │  ★ 吸顶（z-index 99，Quick Filter 下方）
╠═════════════════════════════╣
│  结果数量通栏（32px）        │  随流滚动（禁止吸顶）
├─────────────────────────────┤
│  已选条件面包屑区（fit）     │  随流滚动（禁止吸顶）
├─────────────────────────────┤
│  Product Grid Block（动态）  │  随流滚动
└─────────────────────────────┘
```

#### §4.1.2 吸顶触发条件

- Quick Filter Block 在页面向上滚动越过 Visual Filter Block 底部时锁定吸顶
- Filter Bar Block 紧贴 Quick Filter Block 下方一起吸顶
- 吸顶样式：背景 white，底部 1px solid `$color-border`
- 用户主动向下拉动时，Banner 和 Visual Filter Block 重新展开

---

### §4.2 顶导栏与搜索栏

始终固定在页面顶部，z-index 200，叠加于 Banner Block 上方。搜索栏内嵌在顶导栏内，不独立占行。

#### §4.2.1 顶导布局

顶导栏高度 44px + iOS safe-area-inset-top。从左到右：
- 左侧：← 返回图标 24px
- 中间：搜索栏（flex:1，左右 padding 8px）
- 右侧：分享图标 24px（UI 预留，逻辑 V2）

搜索栏外观：border-radius 20px，fill=`rgba(255,255,255,0.15)`（头图上方）/ `$color-bg`（白色顶导上方），placeholder「Search in this collection」，Inter 14px，左侧搜索图标 14px，有输入时右侧出现 ✕ 清空按钮。

#### §4.2.2 顶导背景状态

| 场景 | 背景 | 图标色 |
|------|------|------|
| 未滚过 Banner | 透明 | 白色 |
| 已滚过 Banner 高度 | white + 底 1px `$color-border` | 深色 |

透明→白色渐变：从滚动距离 = Banner 高度 × 70% 开始线性渐入，至 100% 完全白色。

#### §4.2.3 搜索交互

- 点击搜索栏获焦 → 键盘弹起，推荐词浮层出现（白色背景，radius 12px，阴影）
- 推荐词内容：后端按 `collection_id` 返回高频品牌名 + 品类名，≤10 条
- 点击推荐词或键盘 Search/Return → 提交搜索词，触发 Auto-Scroll，货架刷新
- 搜索词参与联动公式（§3.3.1），与快筛、抽屉筛取交集
- 提交新搜索词 → 清空所有快筛 + 抽屉筛条件（见 §3.3.3）
- 浮层关闭：失焦 / 提交 / 点 ✕

---

### §4.3 头部氛围区（Banner Block）

#### §4.3.1 渲染规格（Standard 样式）

Banner Block 的具体样式由所选 Banner Variant 决定，默认规格：

- 头图高度：180px，fill 模式（铺满裁剪）
- 底部渐变遮罩：从 y=40px 起，`linear-gradient(transparent → rgba(0,0,0,0.4))`，高度 140px
- 标题（`title`）：Inter 600 20px white，绝对定位 bottom 16px left 16px
- 副标题（`subtitle`）：Inter Regular 13px `#FFFFFFCC`，标题下方间距 4px

#### §4.3.2 无图片兜底（`banner_image_url` 为空）

纯色背景 `$color-brand`（#1A1A2E）+ 白色标题 / 副标题，高度不变 180px。

---

### §4.4 图文筛行（Visual Filter Block）

#### §4.4.1 布局规格

由 Visual Filter Variant 决定展示规格，默认：
- 行高 48px，左侧 padding 16px，右侧无 padding（横向可滚动，无分页）
- 项目间距 8px

#### §4.4.2 Label Item 规格

纯文字型（无 `image_url`）：height 32px，padding 0 14px，border-radius 16px

图文型（有 `image_url`）：height 32px，padding 0 10px 0 8px，图标为圆形 20×20px（`border-radius:50%`，fill 模式裁剪），图标与文字 gap 6px

| 状态 | 背景 | 描边 | 文字色 |
|------|------|------|------|
| 未激活 | `$color-bg`（#F7F7F7）| `$color-border` 1px | `$color-ink-primary` |
| 激活 | `$color-brand`（#1A1A2E）| 无 | white |

「All」Label：系统自动生成，排最左，默认激活，运营无需配置。

#### §4.4.3 交互规则

- 点击 Label → 触发 Auto-Scroll → 清空所有快筛 + 抽屉筛条件（§3.3.3）→ 后端按新 Label 刷新商品列表
- 再次点击已激活 Label → 回到 All
- 同一时刻仅一个 Label 激活
- 所有 items `status = inactive` 或图文筛 `module_enabled = FALSE` 时，Block 整行隐藏，不占位

---

### §4.5 集内搜索

> 搜索栏已并入顶导栏（§4.2），本节不再单独描述外观规格。搜索词参与联动公式（§3.3.1）。

---

### §4.6 快筛栏（Quick Filter Block）

#### §4.6.1 整体布局

- 高度 44px，横向可滚动，左 padding 16px，项目间距 8px
- 排列顺序：按 `sort_order` 从左到右渲染 `enabled = TRUE` 的筛选维度 Chip
- Filter Bar Block 中的 Sort 与 Drawer 入口不属于 Quick Filter Block

#### §4.6.2 快筛交互通用规则（Apply + Clear 模式）

- 点击快筛 Chip → 从底部 slide-up 弹出二级面板
- 面板底部固定两个按钮：
  - **Clear**：清空当前维度所有已选项，面板保持打开
  - **Apply**：提交当前选中项，关闭面板，触发 Auto-Scroll，刷新货架
- 未做任何改动时 Apply 等同关闭（不触发刷新）
- Clear 后直接关闭（非 Apply）：不提交，恢复打开前状态

#### §4.6.3 快筛 Chip 样式与显示规则

**显示条件**：某维度在当前 Collection 全集中有 ≥2 个不同值时才渲染该 Chip；否则整个 Chip 物理隐藏，不占位。

| 状态 | 样式 |
|------|------|
| 无选中值 | `$color-bg` 背景 + `$color-border` 1px 描边，文字 `$color-ink-primary` |
| 有选中值 | `$color-brand` 背景，white 文字，右侧数字角标（选中值数量）|

#### §4.6.4 快筛二级面板通用规范（View All 规则）

| 筛选项类型 | 条件 | 面板高度 | View All |
|---------|------|------|------|
| Color | 固定展示全部 | 内容自适应 | 不需要 |
| Price | 固定展示 Slider + 价格带 | 内容自适应 | 不需要 |
| Condition | 固定展示全部 4 项 | 内容自适应 | 不需要 |
| 其他维度 | ≤8 个候选项 | 内容自适应 | 不展示 |
| 其他维度 | >8 个候选项 | 内容自适应（仅前 8 项）| 展示 View All |
| 其他维度 | View All 展开后 | `min(360px, 屏幕高度 × 45%)`，内部滚动 | View All 文案隐藏 |

- View All 触发条件：当前维度候选项总数 > 8
- Size 维度按 Category 分组时，View All 阈值按所有分组内选项**总数**统一计算，不是每组各计 8

#### §4.6.5 Brand 二级面板

- 普通 Chip 流，多选，每个 Chip 右侧显示该品牌商品数量
- View All 规则适用（§4.6.4）
- ≥13 个品牌且 View All 展开后，面板内出现搜索框（在 Chip 流上方）

#### §4.6.6 Series / Category / Material 二级面板

- 普通 Chip 流，多选
- View All 规则适用（§4.6.4）

#### §4.6.7 Color 二级面板

- 色块圆形矩阵，每行 5 个，circle 32px，不适用 View All
- 浅色（White、Beige）加 `$color-border` 1px 描边；下方文字标签 11px
- 选中态：色块内侧 3px `$color-brand` 环形边框
- 颜色枚举与展示：从 Color Dictionary 读取 `color_code → display_name + color_hex`
- 候选值物理隐藏：不在联动公式结果集中的颜色不渲染

#### §4.6.8 Size 二级面板

- 按 Category 分组展示：存在多个 Category 时，每组先展示 Category 名称，再列该 Category 下可选 Size
- 当前 Collection 只有一个 Category 时，退化为平铺，不展示分组标题
- 控件形式：Visual chip（无色块）
- 选中态：改变 Chip 背景色与描边，不加圆点、不加勾选图标
- 多选
- View All 规则适用（§4.6.4），阈值按所有分组总数统一计算

#### §4.6.9 Condition 二级面板

- 4 个成色卡片，多选，不适用 View All
- 每张卡片含展示名 + 描述文字

| 内部枚举值 | 前台展示名 | 描述文字 |
|--------|--------|------|
| `NWT` | Like New | Essentially no signs of use, with original tags |
| `excellent` | Excellent | Minimal signs of use |
| `good` | Good | Light traces of use |
| `fair` | Fair | Noticeable traces of use |

- 候选值物理隐藏：当前全集中无该成色商品时，对应卡片不渲染
- V1 前端硬编码展示名与描述，内部枚举值与商品系统 PRD v1.7 保持一致

#### §4.6.10 Price 二级面板

Price 采用「价格带多选 + Range Slider」双控件，两者取并集（规则见 §3.3.4）。不适用 View All。

**价格带区域**：
- 展示 Price Band Dictionary 配置的价格区间，前端逐条展示为普通 Chip，多选
- 每个 Chip 显示区间文案（如「Under $500」「$500–$1,000」「Over $1,000」）
- 选中态：`$color-brand` 背景，white 文字

**Range Slider 区域**：
- 双端滑动条，位于价格带 Chip 下方
- 滑动范围：Collection 全集内最低价 ~ 最高价（取整到整数美元）
- Slider 最大值为本 Collection 最贵 listing 价格
- 滑块上方实时显示当前区间，格式「$200 — $1,000」
- 重置：拖回两端 = 无 Slider 筛选

---

### §4.7 工具栏（Filter Bar Block）

Filter Bar Block 是独立的 Block，包含 Sort（左侧）和 Drawer Filter 入口（右侧），与 Quick Filter Block 分开吸顶。

**布局**：
- 高度 44px，Sort 固定左侧，Drawer Filter 入口固定右侧
- 快筛 Chip 不属于 Filter Bar，属于 Quick Filter Block

#### §4.7.1 Sort 排序（Filter Bar 左侧）

- 点击 Sort Chip → 弹出二级面板「Sort by」
- 列表形式，单选，选中后立即生效（无单独 Apply 按钮），面板关闭
- 可选项由 Collection 内 Sort 配置的 `enabled = TRUE` 项决定

| 排序选项 | 说明 | 排序逻辑 |
|------|------|------|
| Recommended（默认）| 综合推荐排序 | 后端综合热度 + 相关性 |
| Price: Low to High | 价格升序 | `listing_price` ASC |
| Price: High to Low | 价格降序 | `listing_price` DESC |
| Newest | 最新上架 | `listed_at` DESC |
| Most Popular | 最热销 | `hot_score` DESC，算法与首页 Feed 一致（见《首页 Feed PRD v2.3》§hot_score 定义）|

#### §4.7.2 Drawer Filter 入口（Filter Bar 右侧）

- 样式：⚙ 图标 + 「Filter」文字，Inter 13px
- 有抽屉筛已选条件时：图标右上角红色圆点（6px，#E53935）
- 点击 → 打开抽屉筛选器（见 §4.11）

---

### §4.8 结果数量通栏

- 高度 32px，水平 padding 16px
- 文案：`1,245 items`（实时，千分位格式）；加载中显示 `— items`
- fill=`$color-bg`，文字 `$color-ink-secondary` 13px
- **禁止吸顶**，必须随货架滚动

---

### §4.9 面包屑区

#### §4.9.1 显示条件

- 有任意激活条件（Label ≠ All、搜索词 ≠ 空、任意快筛/抽屉筛有值）时显示
- 无条件时整区域隐藏，不占位
- **禁止吸顶**

#### §4.9.2 布局

- padding 8px 16px，flex-wrap（允许换行），gap 8px
- 「Clear All」按钮始终固定最右侧；「☆ Save」在 Clear All 右侧

#### §4.9.3 Chip 样式

- fill=`$color-accent-light`，文字 / ✕ 颜色：`$color-accent`，border-radius 12px
- 文案格式：`{属性名}: {值}` 或 `{属性名}: {值1}, {值2}`（同属性多值合并一个 chip）

| 来源 | Chip 文案示例 |
|------|------|
| Label（非 All）| `Label: Summer Edit` |
| 搜索词 | `Search: chain bag` |
| Condition | `Condition: Like New, Excellent` |
| Brand | `Brand: LV, Chanel` |
| Price 价格带 | `Price: Under $500, $500–$1,000` |
| Price Slider | `Price: $200 – $400` |
| Price 两者均有 | `Price: Under $500, $200–$400` |
| Color | `Color: Black, Brown` |
| Category | `Category: Bags` |
| 抽屉筛其他属性 | `{属性名}: {值}` |

#### §4.9.4 逐项移除

点击 Chip ✕：
1. 从激活条件中移除该属性对应值
2. 同步回源：来源快筛 → 更新 Chip 角标；来源抽屉筛 → 更新抽屉内部状态；来源 Label → 切回 All；来源搜索词 → 清空搜索栏
3. 立即重新计算，刷新商品列表（**不触发** Auto-Scroll）
4. 移除后所有条件为空 → 面包屑区隐藏

#### §4.9.5 Clear All

- 点击：清空所有条件（Label→All，搜索→空，快筛→清空，抽屉筛→清空），刷新商品列表

#### §4.9.6 Save 按钮

- 有已选条件时出现；未保存态「☆ Save」，已保存态「★ Saved」（`$color-brand`）
- 未登录时点击 → 跳转登录页，登录后回跳自动执行保存（见 §3.4）

---

### §4.10 商品网格（Product Grid Block）

- 双列，列间距 8px，行间距 16px，左右 padding 16px（由 Product Grid Variant 决定）
- 商品卡：复用首页 Feed ProductCard 组件（Feed PRD v2.3 §3.2）
- 置顶商品（`pinned_listings`）排网格最前，后端处理，前端无特殊标记
- 加载：同比例灰色骨架屏
- 无限滚动分页，触底前 3 屏预加载下一页
- 点击商品 → 跳转 PDP

---

### §4.11 抽屉筛选器

由 Filter Bar Block 右侧「⚙ Filter」入口触发。

#### §4.11.1 整体结构

```
┌────────────────────────────┬───────────┐
│  ✕  Filter            Reset│           │
├────────────────────────────┤ 右侧 1/3  │
│  Brand                 ▼   │ 露出区域  │
├────────────────────────────┤（无遮罩） │
│  Series                ▼   │           │
├────────────────────────────┤           │
│  Category              ▼   │           │
├────────────────────────────┤           │
│  Color                 ▼   │           │
├────────────────────────────┤           │
│  Material              ▼   │           │
├────────────────────────────┤           │
│  Size                  ▼   │           │
├────────────────────────────┤           │
│  Condition             ▼   │           │
├────────────────────────────┤           │
│  Price                 ▼   │           │
├────────────────────────────┤           │
│  [ Apply · 84 items ]      │           │
└────────────────────────────┴───────────┘
 ←── 屏幕宽度 66.6% ──→ ← 33.3% →
```

- 宽度：屏幕 × 66.6%，从左侧 slide-in（250ms ease-out）
- 背景 white，右侧 1/3 无蒙层，底层商品流完全可见
- 维度节的顺序和显示/隐藏由 Collection 内 Drawer Filter 配置的 `sort_order` 和 `enabled` 决定
- 默认展开几个维度由 Drawer Filter Variant 的 `default_expanded_count` 决定；未展开的节点显示为折叠态

#### §4.11.2 抽屉筛维度规则总表

| 筛选维度 | 二级展示形式 | 支持搜索 | 选择方式 |
|---------|-----------|--------|--------|
| Brand | 品牌列表（普通 Chip 流）| 否 | 多选 |
| Series | 系列列表（普通 Chip 流）| 否 | 多选 |
| Category | 类目列表（Text Chip 流）| 否 | 多选 |
| Color | 色块矩阵（同 §4.6.7）| 否 | 多选 |
| Material | 材质列表（普通 Chip 流）| 否 | 多选 |
| Size | 按 Category 分组的尺寸列表（Visual chip）| 否 | 多选 |
| Condition | 成色卡片（同 §4.6.9）| 否 | 多选 |
| Price | 价格带 + Range Slider（同 §4.6.10，取并集）| 否 | 价格带多选 + Slider 区间 |

**展示规则**：各维度节内候选项的 View All 规则与快筛二级面板完全一致（见 §4.6.4），包括豁免维度、8 个截断阈值、展开后高度 `min(360px, 屏幕高度 × 45%)`。

**显示规则**：某维度在当前 Collection 全集中有 ≥2 个不同值时才渲染该属性节；否则整节物理隐藏，不占位。

#### §4.11.3 开关路径

| 路径 | 触发方式 | 是否应用变更 |
|------|------|------|
| 打开 | 点击 Filter Bar Block「⚙ Filter」按钮 | — |
| 关闭 A | 点击抽屉内「✕」| 否（取消）|
| 关闭 B | 点击右侧 1/3 露出区域 | 否（取消）|
| 关闭 C | 向右 swipe-to-close | 否（取消）|
| 提交 | 点击底部「Apply」| 是 |

#### §4.11.4 顶部操作栏

- 高度 52px，padding 0 16px
- 左侧：「✕」图标 + 「Filter」文字（Inter 16px 600）
- 右侧：「Reset」文字按钮（Inter 14px，`$color-ink-secondary`）
- 底部 1px `$color-border` 分割线

#### §4.11.5 Apply 按钮

- 吸底，高度 52px，padding 水平 16px
- fill=`$color-brand`，white 文字，Inter 15px 600
- 文案：「Apply · {N} items」，N = 当前抽屉所有条件 × 快筛 × 搜索词预计算交集数量
- N = 0 时：fill=`$color-border`（置灰），文案「No items match」
- 点击：关闭抽屉 → 应用条件 → 更新快筛 Chip 角标 → 更新面包屑 → 触发 Auto-Scroll → 刷新商品列表

#### §4.11.6 Reset 按钮

- 仅清空抽屉内部选中状态，不影响快筛条件
- Reset 后 Apply 按钮显示当前快筛 + 搜索词范围内的商品总数
- 与面包屑「Clear All」区别：Reset 不关抽屉，也不清快筛

#### §4.11.7 Swipe-to-Close 手势

- 在抽屉区域内向右水平滑动
- 触发阈值：位移 > 抽屉宽度 × 40%，或释放速度 > 150 px/s
- 实时跟手（`transform: translateX`）；未达阈值 → 弹回（300ms ease-out）；超过阈值 → 关闭（200ms ease-in）
- 关闭效果同路径 A（不应用变更）

#### §4.11.8 快筛与抽屉双向状态同步

- Quick Filter 对某属性已选值 → 打开抽屉时，该属性节对应 chip 显示为选中
- 抽屉内修改 → Apply 后，对应 Quick Filter Chip 角标更新
- 抽屉 Reset → 不清 Quick Filter
- 面包屑 Clear All → 同时清 Quick Filter 和 Drawer 内部状态

---

### §4.12 Auto-Scroll 行为

#### §4.12.1 触发事件

| 触发动作 | 行为 |
|------|------|
| 点击图文 Label | 平滑滚动至 lock point |
| 搜索栏获焦 | 平滑滚动至 lock point |
| 提交搜索 | 平滑滚动至 lock point |
| 快筛 Apply | 关闭面板后执行 Auto-Scroll |
| 抽屉 Apply | 先关闭抽屉，再执行 Auto-Scroll |
| 面包屑 ✕ 逐项移除 | **不触发** Auto-Scroll |
| 面包屑 Clear All | **不触发** Auto-Scroll |

#### §4.12.2 lock point 定义

lock point = Quick Filter Block 顶边紧贴顶导栏底部。

滚动量 = 当前 scroll offset 到 Quick Filter Block 顶边的距离，使用 `scrollTo({behavior: 'smooth'})`。

---
## §5 依赖与风险

### §5.1 CMS 侧需求（需向 CMS PRD v2.4 提需求）

#### §5.1.1 Template 管理

- Admin 侧需提供 Template 编辑器（Block Builder 模式），支持无代码方式快速搭建页面模板
- Template 状态管理：draft / active / deprecated
- Template 关联 UI Variant 的绑定关系维护

#### §5.1.2 UI Variant 管理

- Admin 侧需提供 UI Variant 配置界面，覆盖 §2.3 各节字段
- UI Variant 与 block_type 绑定，不同 block_type 的 Variant 不可混用
- UI Variant 状态管理：active 才可被 Template 引用

#### §5.1.3 Visual Filter（图文筛）内容配置

| 字段 | 说明 |
|------|------|
| `module_enabled` | 是否展示 Visual Filter Block |
| `status` | 单项 active / inactive |
| `label_text` | 展示文案，最大长度由 Variant 决定 |
| `image_url` | 图片上传 |
| `filter_condition` | CMS 规则编辑器，支持属性条件组合 |
| `sort_order` | 支持拖拽排序 |

**兜底**：若无 active 的图文筛项，前端隐藏 Visual Filter Block，不占位。

#### §5.1.4 Quick Filter 内容配置

| 字段 | 说明 |
|------|------|
| `module_enabled` | 是否展示 Quick Filter Block |
| `attr_key` | 枚举见 §7.1.2 |
| `enabled` | 单项显示开关 |
| `sort_order` | 展示顺序（左→右）|

**兜底**：若 Collection 未配置快筛，前端默认展示 Condition / Price / Brand 三个维度。

#### §5.1.5 Drawer Filter 内容配置

| 字段 | 说明 |
|------|------|
| `module_enabled` | 是否展示 Drawer Filter |
| `attr_key` | 枚举见 §7.1.3 |
| `enabled` | 单项显示开关 |
| `sort_order` | 展示顺序（上→下）|

**兜底**：若 Collection 未配置抽屉筛，前端按 §4.11.2 维度规则总表顺序展示全部维度。

#### §5.1.6 Sort 内容配置

| 字段 | 说明 |
|------|------|
| `module_enabled` | 是否展示排序 |
| `sort_key` | 枚举：`recommended` / `price_asc` / `price_desc` / `newest` / `popular` |
| `enabled` | 单项显示开关 |
| `sort_order` | 展示顺序 |
| `is_default` | 默认选中项（唯一）|

#### §5.1.7 Dictionary 管理

- Color Dictionary：`color_code → display_name + color_hex + color_family`，需提供管理界面
- Price Band Dictionary：全局默认配置，可在单个 Collection 内覆盖

---

### §5.2 其他上下游依赖

| 依赖 | 说明 | 状态 |
|------|------|------|
| 商品系统 PRD v1.7 属性体系 | Condition 4 级枚举、`color_code` 字段、attr_key 枚举须对齐 | 待确认 |
| Feed PRD v2.3 §3.2 ProductCard | 商品网格复用 ProductCard 组件 | 已有 |
| 搜索推荐词接口 | 后端按 `collection_id` 返回高频品牌 + 品类名（≤10 条）| 新增接口 |
| 筛选候选值动态计算接口 | 实时返回当前条件交集下各属性全量候选值列表及各值商品数量；Size 维度须附带 Category 分组结构 | 新增接口 |
| 筛选状态保存接口 | 序列化筛选状态写云端，与 `user_account` 绑定 | 新增接口 |
| 首页 Feed hot_score | Most Popular 排序复用 hot_score 算法（见首页 Feed PRD v2.3）| 已有算法，确认接口是否通用 |

---

### §5.3 风险与待确认项

| 风险 | 说明 | 责任方 |
|------|------|------|
| Template / UI Variant 系统开发成本 | 新增两层配置体系，Admin 侧需要较大开发量（Block Builder + Variant 编辑器），需确认 CMS 排期 | CMS 开发 |
| 筛选候选值动态计算性能 | 每次条件变动实时请求全量候选值，需后端预计算或缓存 | 后端 |
| Color Dictionary 数据初始化 | `color_code` 与商品系统字段对齐、初始数据导入，需与商品系统协同 | 商品系统 + 运营 |
| Price Range Slider 区间端点 | 动态取全集最低/最高价，空合集时端点值兜底方案待定 | 后端 |
| Size 分组接口结构 | 候选值接口需对 size 维度返回 Category 分组结构，与现有接口格式不同 | 后端 |
| Authentication 维度处理 | v1.3 支持 authentication 作为 CMS 可配维度，v1.4 已从 attr_key 枚举移除；若有历史 Collection 配置了 authentication，需明确迁移策略 | 后端 + CMS |

---

## §6 版本规划

### §6.1 V1（本文档范围）

| 功能 | 优先级 |
|------|------|
| 四层配置体系（Template / UI Variant / Dictionary / Collection Content）| P0 |
| Banner Block（Standard 模板）| P0 |
| Visual Filter Block（图文筛）| P0 |
| Quick Filter Block：全维度 Apply + Clear 模式 | P0 |
| Quick Filter：View All（>8 项截断，含高度规格）| P0 |
| Quick Filter：Size 按 Category 分组 | P0 |
| Quick Filter：Price 价格带 + Slider 并集 | P0 |
| Filter Bar Block（Sort + Drawer 入口）| P0 |
| 抽屉筛选器（全维度对齐快筛展示规则）| P0 |
| 面包屑区 + 逐项移除 + Clear All | P0 |
| Auto-Scroll | P0 |
| Product Grid Block（复用 ProductCard）| P0 |
| 筛选候选值联动计算（全量，含 Size 分组）| P0 |
| 友好降级页（合集下线 / 空态 / 网络异常）| P0 |
| CMS：Template / UI Variant / Dictionary 管理界面 | P0 |
| CMS：Visual Filter / Quick Filter / Drawer Filter / Sort 配置 | P0 |
| 顶导搜索栏 + 推荐词浮层 | P0 |
| 筛选状态保存（云端，无查看入口）| P1 |
| Swipe-to-close 手势 | P1 |

### §6.2 V2 规划

| 功能 | 说明 |
|------|------|
| PC 端 | 独立规划，侧边筛选栏范式 |
| Search Block | 集内搜索 Block，Template 可配置为页面顶部独立 Block |
| Collection 内分享 | Share 按钮逻辑 |
| 底部相关推荐 | 底部横滑推荐区 |
| Saved Filters 个人中心页 | 查看 / 管理 / 复用已保存的筛选 |
| 筛选分享链接 | 带筛选状态的分享 URL |

---

## §7 附录

### §7.1 筛选维度枚举

#### §7.1.1 筛选维度全集（V1 支持范围）

| 维度 | 数据字段 | 快筛控件 | 快筛支持 | 抽屉筛支持 | 选择方式 |
|------|------|------|------|------|------|
| Brand | `brand_id` → 品牌名 | Chip 流 + 搜索（View All 展开后）| ✓（可配置）| ✓ | 多选 |
| Series | `series_id` → 系列名 | Chip 流 | ✓（可配置）| ✓ | 多选 |
| Category | `category_id` → 类目名 | Text chip | ✓（可配置）| ✓ | 多选 |
| Color | `attr_key=color` | 色块矩阵（全量）| ✓（可配置）| ✓ | 多选 |
| Material | `attr_key=material` | Chip 流 | ✓（可配置）| ✓ | 多选 |
| Size | `attr_key=size` | 分 Category 分组 Visual Chip | ✓（可配置）| ✓ | 多选 |
| Condition | `condition_grade` | 成色卡片（全量 4 项）| ✓（默认）| ✓ | 多选 |
| Price | `listing_price` | 价格带 Chip + Range Slider | ✓（默认）| ✓ | 价格带多选 + Slider 区间（并集）|
| Sort | — | 列表（单选即生效）| ✓（始终，在 Filter Bar）| ✓ | 单选 |

> **v1.4 变更**：`authentication` 从可配维度中移除，不再支持通过 CMS attr_key 配置。

#### §7.1.2 Quick Filter `attr_key` 枚举

| 值 | 说明 | UI 形式 |
|----|------|------|
| `brand` | 品牌 | Chip 流 |
| `series` | 系列 | Chip 流 |
| `category` | 类目 | Text Chip |
| `material` | 材质 | Chip 流 |
| `color` | 颜色 | 色块矩阵 |
| `size` | 尺寸 | 分组 Visual Chip |
| `condition` | 成色等级 | 成色卡片 |
| `price` | 价格区间 | 价格带 Chip + Range Slider |

默认值（Collection 未配置时）：`[condition, price, brand]`

#### §7.1.3 Drawer Filter `attr_key` 枚举

与 Quick Filter 相同，包含：`brand` / `series` / `category` / `material` / `color` / `size` / `condition` / `price`

---

### §7.2 Sort `sort_key` 枚举

| sort_key | 展示文案 | 排序逻辑 |
|---------|--------|------|
| `recommended` | Recommended | 后端综合算法（热度 + 相关性）|
| `price_asc` | Price: Low to High | `listing_price` ASC |
| `price_desc` | Price: High to Low | `listing_price` DESC |
| `newest` | Newest | `listed_at` DESC |
| `popular` | Most Popular | `hot_score` DESC |

---

### §7.3 设计稿模块索引

本文档 V1 对应原型文件：**`looply-collection-landing-APP-v1.0.pen`**（待 v1.4 设计稿输出后更新）

| Module | 页面名称 | 对应 PRD 章节 |
|--------|------|------|
| Module 1 | 默认态（Banner + Visual Filter + Quick Filter + Filter Bar + 商品网格）| §4.1～§4.4, §4.6, §4.7, §4.10 |
| Module 2 | 搜索激活态（含推荐浮层）| §4.2.3 |
| Module 3 | Sort Action Sheet | §4.7.1 |
| Module 4 | Condition 快筛二级面板 | §4.6.9 |
| Module 5 | Brand 快筛二级面板 | §4.6.5 |
| Module 6 | Price 快筛（价格带 + Slider）| §4.6.10 |
| Module 7 | 面包屑已选条件态 | §4.9 |
| Module 8 | 抽屉筛选器 · 默认折叠态 | §4.11 |
| Module 9 | 抽屉筛选器 · Color 展开态 | §4.11.2 |
| Module 10 | 降级页 · 合集下线 | §3.5 |
| Module 11 | 降级页 · 筛选后 0 件 | §3.5 |
