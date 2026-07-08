# Looply · CMS 首页配置 PRD

**版本** v1.2 | **日期** 2026-07-08 | **范围** 首页资源位配置（Banner + Collection 坑位 + SEO 配置）

---

## 一、概述

### 1.1 背景与目标

Looply 首页内容需要运营团队高频更新，包括 Banner 大图、Collection 入口等。本模块目标是让运营在不依赖开发的情况下，完成首页两个核心坑位的内容日常管理。

**设计原则：**

- **骨架写死，内容放开**：首页 Section 的上下顺序由产品硬编码，运营只配各 Section 内的内容，不能改页面结构
- **全局上下文常驻**：顶部紫色 Sticky Bar 始终显示当前操作的「市场 · 渠道 · 终端」，避免误操作
- **预览上下文常驻**：配置资源位时，右侧始终展示对应终端（App/PC）的完整页面预览，当前编辑坑位高亮紫色框，其他 Section 灰显占位
- **即时生效**：上线开关打开后前台直接读取，无需开发部署

### 1.2 本期范围

本文档仅覆盖**首页配置**模块，对应 `cms.looply.com` 后台左侧导航「首页」条目。

本期支持坑位：
- 首页 Banner（`home_banner`）
- 首页 Collection（`home_collection`）

本期新增：
- 首页 SEO 配置（页面级 Meta Title、Meta Description、OG 分享图）

本期不覆盖：Shop 页、合集管理、全局配置、搜索配置。

### 1.3 用户角色

一期只有一种角色：**运营**，登录即有全部操作权限。

### 1.4 页面入口

```
cms.looply.com
└── 主导航（左侧固定）
    └── 首页    ← 直接可点击，进入首页配置编辑器
```

> 「首页」是左侧导航的直接顶级条目，无父级分组，点击后进入首页资源位配置页面。

---

## 二、核心概念

| 概念 | 说明 |
|------|------|
| 坑位（Zone） | 首页上固定的内容承载区，由产品定义，运营不可新建 |
| 模板（Template） | 坑位支持的视觉样式，由开发实现，运营只选不建 |
| 配置（Config） | 运营在某个坑位用某个模板填充的一条内容记录。每条配置 = 一个素材（图片）+ 关联一个合集 |

**配置与前台展示关系：**

同一坑位下多条上线配置，统一以横向平铺+支持左右滑动方式在前台展示：
- **Banner 坑位**（`banner_image`）：多条配置自动轮播，用户也可左右滑动切换
- **Collection 坑位**（卡片/Chip 类）：多条配置横向排列，用户主动左右滑动，不自动轮播

---

## 三、全局配置 Bar

### 3.1 位置与外观

- 位置：位于顶部 Header 下方，**Sticky**，始终可见（`position: sticky; top: 60px; z-index: 99`）
- 背景色：紫色浅底（`#F3EEFF`），左侧边框线（`1px solid #DDD6FE`）
- 内容：「全局筛选 (Global Context)」标签 + 三个下拉选择器（市场、渠道、终端）

### 3.2 三个维度

| 字段 | 当前值 | 交互方式 |
|------|--------|---------|
| 市场（Market） | US（唯一选项）| Select 下拉，当前仅 US |
| 渠道（Channel） | 官方站（唯一选项）| Select 下拉，当前仅官方站 |
| 终端（Terminal） | App / PC | Select 下拉，切换后预览区实时切换为对应终端预览 |

### 3.3 作用范围

全局 Config Bar 选定的市场+渠道+终端，决定：
1. 左侧坑位配置列表中展示哪套数据
2. 右侧预览面板渲染哪个终端的效果（App 手机框架 / PC 浏览器框架）
3. 进入配置编辑器后，基本信息区「市场/渠道/终端」字段置灰只读，展示当前全局值

### 3.4 DimBadge（维度标签）

配置编辑器 Header 区展示一个蓝色胶囊 Badge，内容为 `market · channel · terminal`（如 `US · 官方站 · 📱 App`），用于在编辑态始终提示当前配置归属维度。

---

## 四、坑位清单

| zone_key | 中文名 | 配置上限 | 支持模板 |
|---------|--------|---------|---------|
| `home_banner` | 首页 Banner | 4 | `banner_image`（唯一） |
| `home_collection` | 首页 Collection | 8 | `collection_card_slide`（唯一）|

---

## 五、模板清单

| template_key | 中文名 | 适用坑位 | MVP 优先级 | 说明 |
|-------------|--------|---------|-----------|------|
| `banner_image` | Banner 大图 | `home_banner` | **P0** | 单图全幅展示，支持文案叠层 |
| `collection_card_slide` | 合集滑动卡片 | `home_collection` | **P0** | 图片卡片 + 合集信息，横向滑动 |

> `home_banner` 坑位只有一个模板（`banner_image`），进入编辑器后不展示模板选卡，系统自动应用 `banner_image`。

> `home_collection` 坑位本期只实现 `collection_card_slide` 一种模板，进入编辑器后不展示模板选卡，系统自动应用 `collection_card_slide`。其余模板后期上线后再开放选择。

---

## 六、配置字段结构

### 6.1 通用字段（所有模板共用）

| 字段 | 标签 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `config_name` | 配置名称 | text | 否 | 运营内部备注，不对外展示 |
| `market_id` | 市场 | readonly | 是 | 由全局 Config Bar 锁定，进入编辑器后置灰 |
| `channel` | 渠道 | readonly | 是 | 由全局 Config Bar 锁定，进入编辑器后置灰 |
| `terminal` | 终端 | readonly | 是 | 由全局 Config Bar 锁定，进入编辑器后展示为只读 span |
| `zone_key` | 坑位 | readonly | 是 | 由坑位行选定，进入编辑器后置灰 |
| `collection_id` | 关联合集 | select | 是 | 按 `market_id` 过滤可用合集；选后自动填充 `landing_page` / `landing_page_url` |
| `landing_page` | 落地页名称 | readonly | 自动填充 | 从关联合集读取，只读展示，可点击跳转 |
| `landing_page_url` | 落地页链接 | hidden | 自动填充 | 从关联合集读取，后台不直接展示 URL，通过点击 `landing_page` 跳转 |
| `title` | 标题 | text | 否 | 字符限制见 §6.2；选择合集后**自动填入合集标题**（仅当字段为空时自动填）；支持覆盖修改 |
| `subtitle` | 副标题 | text | 否 | 字符限制见 §6.2；选择合集后**自动填入合集副标题**（仅当字段为空时自动填）；支持覆盖修改 |
| `text_color` | 文字颜色 | radio | 否 | `light`（白色，默认）/ `dark`（黑色） |
| `asset_image` | 素材图片 | image | 必填 | 仅本地上传；规格见 §十、素材上传规范 |
| `online` | 上线开关 | switch | — | 打开 = 上线（生效中）；关闭 = 下线（已暂停） |

### 6.2 字符数限制

| 字段 | 限制 | 备注 |
|------|------|------|
| `title` | ≤ 30 字符 | 所有终端统一 |
| `subtitle` | Mobile（App）≤ 30 字符；PC ≤ 100 字符 | 按当前终端动态切换上限 |

编辑框显示实时字符计数（`showCount`），达到上限后不可继续输入。

### 6.3 标题/副标题自动填充规则

1. 运营选择「关联合集」时，系统从合集数据中读取 `title` 和 `subtitle`
2. **仅当对应字段当前为空**时自动写入，已有内容不覆盖
3. 自动填入后可手动修改，修改后不再随合集变化
4. 若留空，前台展示时读取合集原始标题/副标题作为 fallback（C 端逻辑，非 CMS 逻辑）

---

## 七、配置状态

| 状态 key | 中文 | 触发条件 | 前台行为 |
|---------|------|---------|---------|
| `active` | 生效中 | `online = true` | 前台展示 |
| `paused` | 已暂停 | `online = false` | 前台不展示，保留配置 |

> **本期去掉时间驱动状态**。状态纯由上线开关决定，无 `start_time`、`end_time`、`not_started`、`expired` 状态。

---

## 八、页面结构与交互

### 8.1 整体布局

```
┌─────────────────────────────────────────────────────────────────┐
│  顶部 Header（含 Logo、全局导航）                                  │
├─────────────────────────────────────────────────────────────────┤
│  全局 Config Bar（Sticky，紫色底）                                │
│  全局筛选  [🇺🇸 US ▾]  [官方站 ▾]  [📱 App ▾]                   │
├──────────────────────────────────┬──────────────────────────────┤
│  左侧主区域（52% 宽）             │  右侧预览区（flex:1）          │
│  ┌─── KPI 概览 ───────────────┐  │  （手机框架 / 浏览器框架）      │
│  │ 总配置数 · 生效中 · 已暂停   │  │                              │
│  └────────────────────────────┘  │                              │
│  ┌─── 坑位选择行 ─────────────┐  │                              │
│  │ [首页 Banner] [首页Collection] │  │                              │
│  └────────────────────────────┘  │                              │
│  ┌─── 配置列表 / 编辑器 ───────┐  │                              │
│  │ （点击行进入编辑器，原位替换） │  │                              │
│  └────────────────────────────┘  │                              │
└──────────────────────────────────┴──────────────────────────────┘
```

### 8.2 KPI 概览区

展示三个数值卡片（紫色渐变底）：
- 总配置数：当前市场+渠道+终端下所有坑位的配置总数
- 生效中：`online = true` 的配置数
- 已暂停：`online = false` 的配置数

### 8.3 坑位选择行（Zone Filter Bar）

- 水平排列的坑位 Chip 按钮，每个按钮显示坑位名称 + 当前生效配置数
- 同一时刻只能选中一个坑位（单选）
- 选中态：紫底白字；未选中：白底灰字带边框
- 选中坑位后，下方展示该坑位的配置列表；右侧预览对应坑位高亮紫色框

### 8.4 配置列表视图

每条配置展示：

| 元素 | 说明 |
|------|------|
| 缩略图 | 44×44px，`object-fit: cover`；无图时展示灰色占位 |
| 配置名称 | `config_name`，运营内部备注 |
| 模板标签 | `template_key` 对应中文名，灰色小字 |
| 状态 Tag | 「生效中」（绿色）/ 「已暂停」（灰色）|
| 上线开关 | Switch，切换后立即改变状态 |
| 拖拽手柄（⠿）| 拖拽行至目标位置后释放，即完成排序 |
| 删除按钮 | 红色文字按钮；**仅「已暂停」状态显示**；点击弹出确认弹窗 |
| 编辑图标 | `EditOutlined`，点击进入编辑器（原位替换列表面板） |

> **删除约束**：仅「已暂停」状态的配置可以删除，删除按钮仅在该状态下显示。生效中的配置需先关闭上线开关变为「已暂停」后才能删除，不可绕过此限制。

#### 列表底部操作区

- 「+ 新建配置」按钮
- 达到坑位配置上限时，按钮禁用，提示：「已达上限（N/N），需先下线一条现有配置」

### 8.5 配置编辑器（左侧原位替换）

点击「新建配置」或列表行编辑图标后，左侧面板切换为编辑器，右侧预览同步联动（`onLiveUpdate` 回调实时更新预览内容）。

#### 8.5.1 编辑器 Header

- 左上：DimBadge（`US · 官方站 · 📱 App`）
- 标题输入：`config_name` 内联编辑，无边框 Input
- 右侧：当前状态 Tag + 「取消」按钮 + 「保存」按钮（含 Check 图标）

#### 8.5.2 基本信息区（置灰只读）

四列网格：
1. 市场（Market）：disabled Select
2. 渠道（Channel）：disabled Select
3. 终端（Terminal）：只读样式的 span（不使用 Select，避免视觉混淆）
4. 坑位：ReadonlyField，展示坑位中文名

#### 8.5.3 模板选择区

- **`home_banner` 坑位**：不展示模板选卡，系统自动应用 `banner_image`，无需运营选择
- **`home_collection` 坑位**：本期只有 `collection_card_slide` 一种模板，不展示模板选卡，系统自动应用，无需运营选择

#### 8.5.4 素材与内容区

**素材图片（非 chip 模板必填）：**

- 已上传：展示缩略图（80px，圆角 6px），右上角 ✕ 清除按钮
- 未上传：虚线上传区（点击/拖拽），显示规格提示
  - Banner 坑位：`JPG/PNG/WebP · 750×400px（Mobile）· 1440×600px（PC）· 建议 ≤ 500KB`
  - Collection 坑位：`JPG/PNG/WebP · 300×300px · 建议 ≤ 200KB`

**关联合集（必填）：**

- Select 下拉，按当前 `market_id` 过滤可用合集
- 选中后显示「落地页」只读字段（页面名称，可点击预览跳转）
- 选中后若 `title`/`subtitle` 为空，自动填入合集对应值

**标题字段：**

- `maxLength: 30`，`showCount` 显示计数
- `placeholder`：若已关联合集则展示合集标题作为 placeholder 提示

**副标题字段：**

- Mobile：`maxLength: 30`；PC：`maxLength: 100`；`showCount` 显示计数
- `placeholder`：展示合集副标题（若有）

**文字颜色：**

- Radio.Button 组：「浅色（白）」/ 「深色（黑）」，默认浅色

#### 8.5.5 上线状态区

- Switch 开关：`checkedChildren="上线"` / `unCheckedChildren="下线"`
- 开关右侧说明文字：「当前配置将在 C 端展示」/ 「当前配置不在 C 端展示」
- 新建配置默认 `online = false`（默认已暂停，需手动上线）

---

## 九、SEO 配置

### 9.1 入口与位置

SEO 配置为**首页级别**的页面元数据配置，独立于坑位资源位配置。入口：左侧配置面板顶部 Tab 行最右侧「🔍 SEO 配置」标签，点击后左侧面板切换为 SEO 配置表单；右侧预览面板仍展示当前首页预览（无特定坑位高亮）。

### 9.2 字段说明

| 字段 | 标签 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `meta_title` | Meta Title | text | 否 | `≤ 60 字符`，`showCount`；留空自动使用：`Looply \| Authenticated Pre-Owned Luxury Bags, Watches & More` |
| `meta_desc` | Meta Description | textarea | 否 | 建议 120–160 字符，`maxLength: 160`，`showCount`；留空自动生成：`Shop authenticated pre-owned luxury bags, watches, jewelry and accessories from Chanel, Louis Vuitton, Rolex and more. Expertly authenticated and quality assured.` |
| `og_image` | OG 分享图 | image | 否 | 1200×630px，JPG/PNG，≤ 500KB；留空使用系统默认 Looply 品牌图 |

**完整 URL 展示**（只读）：`https://looply.com/`，固定显示，不可修改。

### 9.3 Google 搜索预览

SEO 配置区底部展示实时的 Google 搜索结果预览卡，包含：
- 标题（蓝色超链接样式，使用 `meta_title` 或默认值）
- URL（`https://looply.com`，绿色）
- 描述摘要（`meta_desc` 或默认值）

### 9.4 保存逻辑

- 点击「保存 SEO 配置」按钮后，字段生效并推送到前台 SEO 层（即时生效）
- 成功后按钮旁展示绿色「✓ 已保存」提示

### 9.5 市场维度

当前首页 SEO 配置不区分终端（App/PC 共用同一份，SEO 主要影响 PC 端搜索抓取）。如需未来支持多市场多语言 Meta，可扩展按 `market` 存储多套，本期不做。

---

## 十、预览面板

### 10.1 终端切换

全局 Config Bar 的「终端」选择决定预览终端：

| 终端 | 预览框架 | 尺寸 |
|------|---------|------|
| App | 手机框架（圆角黑色边框，含刘海）| 宽 375px，屏幕高 620px |
| PC | 浏览器框架（含地址栏、三色点）| 宽 680px，屏幕高 560px |

### 10.2 当前坑位高亮

- 当前选中（正在编辑或选中）的坑位区域：紫色外发光边框（`box-shadow: 0 0 0 2px #7C3AED`）+ 左上角紫色小标签显示坑位名
- 其他 Section：`opacity: 0.4`，灰显占位

### 10.3 联动逻辑

编辑器中每次字段变更（`onLiveUpdate`）立即推送到预览面板，无需保存，实时可见。

---

## 十一、素材上传规范

| 坑位 | 终端 | 推荐尺寸 | 格式 | 文件大小建议 |
|------|------|---------|------|------------|
| `home_banner` | Mobile（App）| 750×400px | JPG/PNG/WebP | ≤ 500KB |
| `home_banner` | PC | 1440×600px | JPG/PNG/WebP | ≤ 500KB |
| `home_collection` | 全终端 | 300×300px | JPG/PNG/WebP | ≤ 200KB |

上传失败时提示：「Upload failed. Try again」

---

## 十二、操作确认规范

| 操作 | 是否需要确认弹窗 | 弹窗文案 |
|------|----------------|---------|
| 切换模板（已有填写内容）| 是 | 「切换模板将清空已填参数，确认继续？」|
| 删除配置 | 是 | 「删除后不可恢复，确认删除？」|
| 切换模板（无内容）| 否 | 直接切换 |

---

## 十三、空状态与边界

| 场景 | 处理方式 |
|------|---------|
| 坑位无配置 | 展示首次使用引导态 |
| 达到坑位配置上限 | 「新建配置」按钮禁用，展示上限提示 |
| 关联合集无合集数据 | Select 展示空态提示 |

---

## 十四、数据结构参考

```typescript
interface Config {
  id: string;
  zone: 'home_banner' | 'home_collection';
  template: 'banner_image' | 'collection_card_slide';
  name: string;           // config_name，内部备注
  img: string;            // asset_image URL
  collId: string;         // collection_id
  online: boolean;        // 上线开关
  order: number;          // 展示排序
  title: string;          // 标题，可覆盖合集标题
  subtitle: string;       // 副标题，可覆盖合集副标题
  textColor: 'light' | 'dark';
}

interface ConfigsStore {
  [key: string]: {          // key = `${market}:${channel}:${terminal}`
    home_banner: Config[];
    home_collection: Config[];
  };
}
```

**状态计算：**

```
computeStatus(cfg) = cfg.online ? 'active' : 'paused'
```

**SEO 配置结构（首页级别，独立于 Config 列表）：**

```typescript
interface HomeSeoConfig {
  market: string;           // 预留多市场扩展，当前固定 'US'
  meta_title: string;       // 留空使用默认值
  meta_desc: string;        // 留空使用默认值，建议 120-160 字符
  og_image: string;         // OG 分享图 URL，留空使用系统默认品牌图
}
```

---

## 十五、翻译模块对接清单

> V1.0 上线（美国英语单市场）全部内容英文硬编码，**无需实际翻译**。本节为预对接需求：提前向翻译侧注册 resource_type 和字段清单，多语言启动时 CMS 写入接口直接对接，无需临时补设计。

### 15.1 需要提给翻译侧的（CMS 运营动态配置内容）

| 内容 | resource_type | field_name | 说明 |
|------|--------------|------------|------|
| Banner 标题 | `cms_home_banner` | `title` | 运营在 CMS 填写，每条配置独立；resource_id = config.id |
| Banner 副标题 | `cms_home_banner` | `subtitle` | 同上 |
| Collection 标题 | `cms_home_collection` | `title` | 同上 |
| Collection 副标题 | `cms_home_collection` | `subtitle` | 同上 |
| 首页 SEO Meta Title | `cms_home_seo` | `meta_title` | 首页级别，resource_id = market_id |
| 首页 SEO Meta Description | `cms_home_seo` | `meta_desc` | 同上 |

> 以上 resource_type 命名需与翻译侧确认后在 `translatable_field_config` 表注册。翻译模块 PRD v3.1 §3.2 将「Banner / 运营配置」标注为「模块未设计」，这是首次提出对接需求。

### 15.2 不需要提给翻译侧的

| 内容 | 类型 | 说明 |
|------|------|------|
| 配置名称（config_name） | 不翻译 | 运营内部备注，不对外展示 |
| CMS 后台界面文字 | 不翻译 | 运营使用，固定语言 |
| OG 分享图 | 不翻译 | 图片不区分语言 |

---

## 十六、版本变更日志

### v1.2（2026-07-08）

基于原型 v1.4 更新。

| # | 章节 | 变更内容 | 变更原因 |
|---|------|---------|---------|
| 1 | §一·1.2 范围 | 新增「首页 SEO 配置」到本期范围 | SEO 是新增需求 |
| 2 | 新增 §九 SEO 配置 | 全新章节：入口、字段（Meta Title / Meta Description / OG 图）、Google 预览、保存逻辑、市场维度说明 | 需要让运营可配置首页 SEO 元数据 |
| 3 | §九–§十四 章节编号 | 原 §九 预览面板 → §十；原 §十–§十四 依次 +1 | 新增 §九 SEO 章节后顺序后移 |
| 4 | §十四 数据结构 | 新增 `HomeSeoConfig` 接口 | 同 §九 SEO 配置新增 |
| 5 | 新增 §十五 翻译模块对接清单 | 明确需提给翻译侧的 CMS 动态内容字段（Banner/Collection/SEO，resource_type + field_name）；不需翻译侧介入的内容单独列出 | 与翻译模块预对接，多语言启动时无需临时补设计 |
| 6 | §十五→§十六 章节编号 | 原 §十五 版本变更日志 → §十六 | 新增 §十五 翻译对接章节后顺序后移 |

---

### v1.1（2026-07-08）

基于原型 v1.3 更新。

| # | 章节 | 变更内容 | 变更原因 |
|---|------|---------|---------|
| 1 | §四 坑位清单 | `home_collection` 本期支持模板改为仅 `collection_card_slide` | 本期 Collection 只实现横向滑动卡片一种形式，其余后期上线 |
| 2 | §五 模板清单 | 删除 `collection_chip`、`collection_card_small` 两行 | 同上，本期不做 |
| 3 | §六 配置字段 | 删除 §6.2 collection_chip 特殊说明整节 | 无 chip 模板，相关说明无效 |
| 4 | §八·8.4 配置列表 | 排序方式由「上↑/下↓按钮」改为**拖拽手柄**（⠿） | 拖拽更直观，多条配置时操作效率更高 |
| 5 | §八·8.4 配置列表 | 明确删除约束：仅「已暂停」状态可删除，删除按钮仅该状态显示 | 防止误删线上正在使用的配置 |
| 6 | §十三 数据结构 | `template` 类型移除 `collection_chip`、`collection_card_small` | 同模板清单变更 |

---

### v1.0（2026-07-08）

首版 PRD，基于首页配置原型 v1.2 编写。

**与老版资源位配置 PRD（v2.5.1）的主要差异：**

| # | 差异项 | 老版（v2.5.1）| 本版（v1.0）|
|---|--------|-------------|------------|
| 1 | 覆盖范围 | 首页 + Shop 页共 4 个坑位 | 仅首页 2 个坑位 |
| 2 | 模板数量 | 5 个（含 banner_video）| 4 个，去掉 banner_video |
| 3 | Banner 模板选择 | 展示模板选卡 | home_banner 无选卡，自动应用 banner_image |
| 4 | 配置状态 | 4 态（not_started / active / paused / expired），时间驱动 | 2 态（active / paused），纯开关驱动 |
| 5 | 生效时间 | 有 start_time / end_time | 无，已移除 |
| 6 | 按钮文案（CTA）| 有 cta_text 字段 | 无，已移除 |
| 7 | 标题/副标题 | 字符限制「待与设计对齐」| 明确：title ≤ 30；subtitle Mobile ≤ 30 / PC ≤ 100 |
| 8 | 自动填充 | 未定义 | 选合集后自动填入 title/subtitle（空时填入）|
| 9 | 全局维度选择 | 列表顶部三层级联筛选 | 顶部 Sticky 全局 Config Bar（紫色，与导航配置对齐） |
| 10 | 左侧导航 | 「资源位管理 > 首页」二级结构 | 「首页」直接顶级条目 |
