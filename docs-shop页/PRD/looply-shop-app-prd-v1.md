# Looply App 端 Shop 页 PRD v1.0

> **版本**：v1.0
> **日期**：2026-06-26
> **作者**：产品团队
> **状态**：待评审
> **相关文件**：
> - 前端原型：`/Users/zz/looply/shop/前端原型/looply-shop-app-v0.2.html`
> - 后台原型：`/Users/zz/looply/shop/后台原型/looply-shop导航-后台原型-v0.2-antd.html`

---

## 目录

1. [文档说明](#1-文档说明)
2. [页面整体结构](#2-页面整体结构)
3. [各模块详细需求](#3-各模块详细需求)
4. [交互规则](#4-交互规则)
5. [视觉规范](#5-视觉规范)
6. [数据接口说明](#6-数据接口说明)
7. [边界情况与异常处理](#7-边界情况与异常处理)

---

## 1. 文档说明

### 1.1 背景与目的

Shop 页是 Looply App 底部导航的核心入口之一，用户从此处进入按品类和品牌浏览二手商品的主路径。本文档描述 Shop 页的完整导航结构、内容渲染规则、交互逻辑和视觉规范，供前端开发、后台开发、运营和 QA 团队参考。

### 1.2 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|----------|
| v1.0 | 2026-06-26 | 初版，基于前端原型 v0.2 全量整理 |

### 1.3 不做什么（V1 范围限制）

| 不做 | 说明 |
|------|------|
| Shop 页搜索能力 | 搜索由顶部统一搜索框承接 |
| 个性化排序算法 | For You 推荐 V1 可用规则排序或静态数据，V2 对接推荐系统 |
| PC 端适配 | V1 仅 App 端，PC 端另行出稿 |
| 商品筛选/排序器 | 圆形卡片点击跳转到独立的商品列表筛选页，筛选能力由该页面承接 |

### 1.4 名词对照

| 中文 | 英文 | 说明 |
|------|------|------|
| 顶导 Tab | Top Category Tab | 页面顶部横向可滑动的主品类导航，共 6 个 |
| 左导 | Left Nav | 主体区左侧纵向二级导航，宽 108px |
| 右内容区 | Right Content Area | 左导右侧的内容渲染区 |
| 渲染类型 | navItem.type | 决定右内容区渲染方式的字段，共 5 种 |
| 圆形卡片 | Circle Card | 正方形容器 + border-radius 50% 的子类目卡片 |
| 叶节点 | Leaf | 无子页导航的末级导航项（type = leaf） |
| 品牌钻取 | Brand Drill-Down | Brands Tab 下点击品牌进入品牌子系列的层级跳转 |
| Collection List | Collection List | 叶节点子系列 ≤5 个时展示的带缩略图行式列表 |
| Product Grid | Product Grid | 叶节点子系列 >5 个时展示的 2 列商品卡片网格 |

---

## 2. 页面整体结构

### 2.1 页面布局概览

```
┌─────────────────────────────────────────────┐
│  TopBar（约 56px）                           │  固定，不随页面滚动
│  Logo + 搜索框 + 收藏图标 + 购物袋图标        │
├─────────────────────────────────────────────┤
│  Top Tab Bar（约 44px）                      │  固定，横向可滑动
│  New Arrivals / Brands / Bags / ...          │
├──────────────┬──────────────────────────────┤
│  Left Nav    │  Right Content Area          │
│  108px 宽    │  flex: 1                     │  两侧独立纵向滚动
│  纵向滚动    │  纵向滚动                     │
│              │                              │
└──────────────┴──────────────────────────────┘
│  Bottom Tab Bar（约 54px）                   │  固定
│  Home / Shop（激活）/ Favourites / Account   │
└─────────────────────────────────────────────┘
```

### 2.2 各区域说明

**TopBar（顶部工具栏）**
- Logo：文字"Looply"，颜色 #7C3AED，加粗
- 搜索框：占 flex: 1，圆角胶囊，灰底，placeholder 文案"Search bags, brands, jewelry..."
- 右侧图标：收藏心形图标 + 购物袋图标，各自可点击进入对应页面
- 背景白色，底部有 1px 分割线

**Top Tab Bar（顶部主品类导航）**
- 横向排列，支持手势横向滑动，滚动条隐藏
- 共 6 个 Tab：New Arrivals / Brands / Bags / Jewelry & Accessories / Watches / Electronics
- 激活态：紫色文字 + 底部 2px 紫色下划线

**主体区（Left Nav + Right Content）**
- 两列布局，左导固定 108px，右侧内容区占剩余宽度
- 两个区域各自独立纵向滚动，互不影响
- 左导背景色 #FAFAFA（浅灰），右内容区背景色 #FFFFFF

**Bottom Tab Bar（底部导航栏）**
- 4 个 Tab：Home / Shop / Favourites / Account
- Shop Tab 激活，其余 Tab 灰色默认态

---

## 3. 各模块详细需求

### 3.1 顶导 Tab

共 6 个 Tab，按以下顺序排列：

| 序号 | id | 显示文案 |
|------|----|----------|
| 1 | new_arrivals | New Arrivals |
| 2 | brands | Brands |
| 3 | bags | Bags |
| 4 | jewelry | Jewelry & Accessories |
| 5 | watches | Watches |
| 6 | electronics | Electronics |

**行为规则**：
- 默认激活第 1 个 Tab（New Arrivals），左导和右内容区显示该 Tab 的默认内容
- 点击 Tab 时，顶导激活态切换，左导重置为该 Tab 的第一个导航项，右内容区重新渲染
- Brands Tab 若处于品牌钻取状态（Level 3），切换 Tab 时清空钻取层级，回到初始状态
- 当前激活 tabId 写入路由状态，支持页面刷新后恢复上次位置

### 3.2 左侧二级导航（Left Nav）

#### 3.2.1 样式规范

| 属性 | 值 |
|------|----|
| 宽度 | 108px（固定，不随内容变化） |
| 背景色 | #FAFAFA |
| 右侧边框 | 1px solid #F3F4F6 |
| 单项 padding | 13px 10px 13px 14px |
| 字号 | 13px |
| 行高 | 1.35（允许两行折行） |
| 默认文字色 | #374151 |
| 激活背景 | #FFFFFF |
| 激活文字色 | #7C3AED，font-weight 700 |
| 激活左边框 | border-left 3px solid #7C3AED |
| hover 态 | background #F3EEFF，color #7C3AED |

#### 3.2.2 各 Tab 完整导航项列表

**New Arrivals Tab（20 项）**

| 序号 | id | 显示文案 | type |
|------|----|----------|------|
| 1 | na_for_you | For You | reco |
| 2 | na_bags | Bags | leaf |
| 3 | na_jewelry | Jewelry | leaf |
| 4 | na_watches | Watches | leaf |
| 5 | na_acc | Accessories | leaf |
| 6 | na_elec | Electronics | leaf |
| 7 | na_under500 | Under $500 | leaf |
| 8 | na_trending | Trending Now | leaf |
| 9 | na_staff | Staff Picks | leaf |
| 10 | na_rare | Rare Finds | leaf |
| 11 | na_likenew | Like New | leaf |
| 12 | na_vintage | Vintage | leaf |
| 13 | na_icons | Iconic Pieces | leaf |
| 14 | na_mini | Mini Bag Moment | leaf |
| 15 | na_monogram | Monogram Edit | leaf |
| 16 | na_chain | Chain Bag Edit | links |
| 17 | na_neutrals | Neutrals Only | links |
| 18 | na_colorpop | Color Pop | links |
| 19 | na_quiet | Quiet Luxury | links |
| 20 | na_gifts | Gift Ideas | links |

**Brands Tab（10 项）**

| 序号 | id | 显示文案 | type |
|------|----|----------|------|
| 1 | br_for_you | For You | reco |
| 2 | br_luxury_bag | Luxury Bags | brand_circles |
| 3 | br_sale | On Sale | brand_circles |
| 4 | br_new_week | New This Week | brand_circles |
| 5 | br_staff | Staff Picks | brand_circles |
| 6 | br_jewelry | Fine Jewelry | brand_circles |
| 7 | br_watches | Watches | brand_circles |
| 8 | br_tech | Electronics | brand_circles |
| 9 | br_under500 | Under $500 | brand_circles |
| 10 | br_vintage | Vintage | brand_circles |

**Bags Tab（9 项）**

| 序号 | id | 显示文案 | type |
|------|----|----------|------|
| 1 | for_you | For You | reco |
| 2 | new | New In | reco |
| 3 | all | All Bags | sub |
| 4 | shoulder | Shoulder | leaf |
| 5 | tote | Tote | leaf |
| 6 | crossbody | Crossbody | leaf |
| 7 | mini | Mini Bags | leaf |
| 8 | clutch | Clutches | leaf |
| 9 | belt | Belt Bags | leaf |

**Jewelry & Accessories Tab（12 项）**

| 序号 | id | 显示文案 | type |
|------|----|----------|------|
| 1 | for_you | For You | reco |
| 2 | new | New In | reco |
| 3 | necklaces | Necklaces | leaf |
| 4 | rings | Rings | leaf |
| 5 | bracelets | Bracelets | leaf |
| 6 | earrings | Earrings | leaf |
| 7 | sets | Jewelry Sets | leaf |
| 8 | scarves | Scarves | leaf |
| 9 | sunglasses | Sunglasses | leaf |
| 10 | belts | Belts | leaf |
| 11 | wallets | Wallets | leaf |
| 12 | hats | Hats | leaf |

**Watches Tab（9 项）**

| 序号 | id | 显示文案 | type |
|------|----|----------|------|
| 1 | for_you | For You | reco |
| 2 | new | New In | reco |
| 3 | women | Women's | leaf |
| 4 | men | Men's | leaf |
| 5 | luxury | Luxury | leaf |
| 6 | sport | Sport | leaf |
| 7 | rolex | Rolex | leaf |
| 8 | omega | Omega | leaf |
| 9 | cartier | Cartier | leaf |

**Electronics Tab（9 项）**

| 序号 | id | 显示文案 | type |
|------|----|----------|------|
| 1 | for_you | For You | reco |
| 2 | new | New In | reco |
| 3 | phones | Phones | leaf |
| 4 | laptops | Laptops | leaf |
| 5 | tablets | Tablets | leaf |
| 6 | audio | Audio | leaf |
| 7 | cameras | Cameras | leaf |
| 8 | gaming | Gaming | leaf |
| 9 | wearables | Wearables | leaf |

### 3.3 右侧内容区——5 种渲染类型

右内容区根据当前激活导航项的 `type` 字段决定渲染方式，共 5 种。

#### 3.3.1 type: reco（推荐页）

**适用导航项**：For You、New In

**页面结构**（从上到下）：

**区块一：9 个圆形快捷类目**
- 标题：导航项 label，字号 15px，加粗，上下内边距 14px/8px
- 3 列圆形卡片网格，gap 8px，左右 padding 10px
- 9 个子类目固定：Shoulder Bags / Tote Bags / Crossbody / Mini Bags / Clutches / Belt Bags / New Arrivals / Under $500 / Trending Now

**圆形图片规则（关键差异）**：

| 场景 | 圆形内容 |
|------|----------|
| New Arrivals Tab 的 For You（id = na_for_you） | 真实商品图片，object-fit: contain，白底圆形，1px #E5E7EB 边框 |
| 其他所有 reco 项（Bags/Jewelry/Watches 等 Tab 的 For You 和 New In） | 彩色背景（10 色循环） + emoji |

**区块二：商品推荐（You May Also Like）**
- 分隔条：height 8px，background #F9FAFB
- 标题："You May Also Like"，字号 15px，加粗
- 2 列商品卡片网格（商品卡片规范见 3.5 节）

---

#### 3.3.2 type: brand_circles（品牌圆形，Brands Tab 专属）

**适用导航项**：Brands Tab 下 For You 之外的 9 个分组（Luxury Bags / On Sale / New This Week / Staff Picks / Fine Jewelry / Watches / Electronics / Under $500 / Vintage）

此类型有两个层级（Level 2 / Level 3）：

**Level 2 — 品牌列表页**
- 3 列圆形卡片，彩色背景 + 品牌 emoji
- 每个圆形 label 显示品牌名
- 下方"You May Also Like"商品推荐区（2 列商品卡片）
- 点击任意品牌圆形 → 进入 Level 3

**Level 3 — 品牌子系列页**
- 顶部"返回"按钮：`← 品牌名`，字号 12px，紫色，点击后回到 Level 2
- 展示该品牌下的子系列圆形（彩色背景 + emoji，3 列）
- 下方"You May Also Like"商品推荐区（2 列商品卡片）
- 点击子系列圆形 → 跳转对应商品列表页

**层级切换规则**：
- Level 2 → Level 3：右内容区内部状态更新（不改变左导激活项）
- Level 3 → Level 2：点击返回按钮，右内容区恢复 Level 2 内容
- 切换顶导 Tab：清空钻取层级，下次进入 Brands Tab 从 Level 2 开始

---

#### 3.3.3 type: sub（父节点子分类聚合，Bags Tab 专属）

**适用导航项**：Bags Tab 的 All Bags

- 展示该 Tab 下所有叶节点分类的圆形卡片聚合（3 列网格）
- 包含：Shoulder Bags / Tote Bags / Crossbody / Mini Bags / Clutches / Belt Bags / New Arrivals / Under $500 / Trending Now（与原型 sub 结构对齐）
- 点击圆形 → 左导切换到对应的叶节点，右内容区渲染对应 leaf 内容

---

#### 3.3.4 type: leaf（叶节点分类页）

**适用导航项**：New Arrivals Tab 大多数项、Bags/Jewelry/Watches/Electronics Tab 的具体分类项

**页面结构（从上到下）**：

**区块一：子系列圆形**
- 3 列圆形卡片，展示该分类下的子系列（彩色背景 + emoji）
- 子系列数据来自后台配置的 SubCollection 列表

**区块二：根据子系列数量切换展示方式**

| 子系列数量 | 展示方式 |
|-----------|----------|
| ≤ 5 个 | Collection List（带大图 + 缩略图的列表行） |
| > 5 个 | Product Grid（2 列商品卡片网格） |

**Collection List 每行结构**：
- 高度：140px（coll-body 区域）
- 左侧 cover 区：彩色背景色块，居中大 emoji，圆角 8px，flex: 1
- 右侧 thumbs 区：2×2 缩略图网格，gap 4px，flex: 1
- 顶部 name 行：collection 名称（12px，加粗）+ 右侧箭头"›"
- 整行 padding：10px 12px，底部 1px 分割线，点击跳转到该 collection 商品列表

**Product Grid**：
- 2 列商品卡片网格（商品卡片规范见 3.5 节）

---

#### 3.3.5 type: links（编辑主题链接，New Arrivals Tab 专属）

**适用导航项**：Chain Bag Edit / Neutrals Only / Color Pop / Quiet Luxury / Gift Ideas

- 单列文字链接列表，不使用圆形卡片
- 每行 padding：11px 14px，字号 13px，color #6B7280，底部 1px 分割线
- 点击激活态：background #F3EEFF，color #7C3AED
- 点击链接项 → 跳转到对应主题筛选结果页（URL 由 links 配置的 slug 决定）

**各 links 类目的链接项**：

| 导航项 | 链接文案（示例，运营可配） |
|--------|--------------------------|
| Chain Bag Edit | Chain Shoulder / Chain Crossbody / Chain Mini / Chain Clutch / Gold Chain / Silver Chain / Pearl Chain / Mixed Chain |
| Neutrals Only | All Beige / All Black / All White / Camel & Tan / Nude Tones / Stone & Sand / Greige Edit / Off-White Only |
| Color Pop | Bold Red / Electric Blue / Hot Pink / Sunshine Yellow / Emerald Green / Cobalt / Orange / Purple / Coral / Turquoise |
| Quiet Luxury | Minimalist Bags / No-Logo Pieces / Clean Lines / Tonal Outfits / Understated Luxury / Bottega Edit / The Row Edit / Loro Piana / Brunello Cucinelli |
| Gift Ideas | Under $200 / Under $500 / Under $1,000 / For Her / For Him / For the Collector / Luxury Splurge / Everyday Gifting / Gift Sets |

### 3.4 圆形卡片规范

圆形卡片是 Shop 页核心视觉单元，用于子类目、品牌、子系列的快捷入口展示。

**容器尺寸**：
- 3 列等宽 grid，列间距 8px，左右 padding 10px
- 每个卡片宽度由 grid 列宽决定，高度 = 宽度（aspect-ratio: 1）
- border-radius: 50%，overflow: hidden

**背景色（10 色循环）**：

按卡片在列表中的 index % 10 取色：

| index | 色值 |
|-------|------|
| 0 | #EDE9FE（浅紫） |
| 1 | #FCE7F3（浅粉） |
| 2 | #FEF3C7（浅黄） |
| 3 | #D1FAE5（浅绿） |
| 4 | #DBEAFE（浅蓝） |
| 5 | #FEE2E2（浅红） |
| 6 | #F3F4F6（浅灰） |
| 7 | #FDF4FF（浅紫粉） |
| 8 | #ECFDF5（浅薄荷） |
| 9 | #FFF7ED（浅橙） |

**内容**：
- 普通模式：彩色背景 + 居中 emoji，emoji 字号约 22px
- 图片模式（仅 New Arrivals Tab 的 For You）：背景白色 + 真实商品图，1px #E5E7EB 边框，图片 object-fit: contain

**卡片 label**：
- 显示在圆形下方，字号 11px，color #374151，text-align: center，行高 1.3
- 允许最多 2 行，超出截断

### 3.5 商品卡片规范

商品卡片用于所有"You May Also Like"推荐区和 Product Grid 区域。

**布局**：2 列网格，gap 8px，左右 padding 10px

**卡片结构**：

```
┌──────────────────────┐
│  商品图片区（1:1比例）│
│  [Sold Out 标签]     │  ← 左上角，有售罄时展示
│  [♡ 收藏图标]        │  ← 右上角，常显
└──────────────────────┤
│  品牌名               │  大写，加粗，10px
│  商品名               │  小字，灰色，11px，最多2行
│  现价  [折扣标签]     │  现价加粗 13px；标签紫色 pill
│  ~~原价~~             │  划线，灰色，有折扣时展示
└──────────────────────┘
```

**字段定义**：

| 字段 | 必须 | 规格 |
|------|------|------|
| 品牌名 | 是 | font-size 10px，font-weight 700，color #111827，text-transform uppercase |
| 商品名 | 是 | font-size 11px，color #6B7280，line-height 1.3，最多 2 行省略 |
| 现价 | 是 | font-size 13px，font-weight 700，color #111827 |
| 原价 | 否 | font-size 11px，color #9CA3AF，text-decoration line-through，有折扣时展示 |
| 折扣标签 | 否 | 文案示例"Save $1,500"或"35% Off"，紫色 pill（color #7C3AED，bg #EDE9FE，border-radius 10px，padding 1px 6px，font-size 10px） |
| Sold Out 标签 | 否 | 绝对定位左上角，bg rgba(255,255,255,0.92)，color #374151，border-radius 20px，font-size 10px，font-weight 600 |
| 收藏心形 | 是 | 绝对定位右上角，font-size 16px，已收藏 = 紫色实心，未收藏 = 灰色空心，点击触发收藏/取消收藏 |

**商品图片区**：
- aspect-ratio 1:1，background #F3F4F6（图片加载前的占位色）
- 图片渲染：width 86%，height 86%，object-fit: contain，居中显示

---

## 4. 交互规则

### 4.1 顶导 Tab 切换

1. 点击顶导 Tab → 激活态更新（紫色文字 + 底部下划线）
2. 左导自动重置，默认选中该 Tab 的第一个导航项（index = 0）
3. 右内容区重新渲染第一个导航项的内容
4. 如果此前在 Brands Tab Level 3（品牌子系列页），清空钻取层级，再次进入 Brands Tab 从 Level 2 开始
5. 顶导横向滑动时不触发 Tab 切换，只有明确点击才切换

### 4.2 左导导航项切换

1. 点击左导项 → 激活态更新（紫色文字 + 左边框 + 白底）
2. 右内容区根据新激活项的 type 渲染对应内容
3. 右内容区滚动位置重置到顶部
4. 左导自身滚动位置不变

### 4.3 品牌钻取（Brands Tab 专属）

| 操作 | 结果 |
|------|------|
| 点击 brand_circles 类型下的品牌圆形 | 右内容区切换到 Level 3，左导激活项不变 |
| 点击 Level 3 顶部"← 品牌名"返回按钮 | 右内容区回到 Level 2，左导激活项不变 |
| 点击 Level 3 子系列圆形 | 跳转到对应商品列表筛选页 |
| 切换顶导 Tab 后再回到 Brands Tab | Level 2（初始态），不保留上次钻取位置 |

### 4.4 圆形卡片点击（非品牌类）

- 点击 reco / sub / leaf 类型下的圆形卡片 → 跳转到对应分类的商品列表筛选页
- 跳转携带参数：分类 slug 或 collection_id

### 4.5 商品卡片交互

| 操作 | 结果 |
|------|------|
| 点击卡片主体（图片区/信息区） | 跳转商品详情页 |
| 点击收藏心形 | 未登录：弹登录引导；已登录：切换收藏状态，心形即时反馈（实心/空心） |
| 售罄商品 | 可点击卡片进详情页（不拦截），Sold Out 标签仅作视觉提示 |

### 4.6 搜索框交互

- 点击搜索框 → 跳转 / 展开搜索页（不在本页停留）
- 搜索框始终可见，不受 Tab 切换影响

### 4.7 购物袋图标

- 点击 → 跳转购物车页面
- 有商品时显示数量红点 badge（数字，最大显示 99+）

### 4.8 收藏图标（TopBar）

- 点击 → 跳转收藏列表页

---

## 5. 视觉规范

### 5.1 主色系

| 场景 | 色值 |
|------|------|
| 品牌主色 | #7C3AED |
| 顶导激活文字 | #7C3AED |
| 顶导激活下划线 | 2px solid #7C3AED |
| 左导激活文字 | #7C3AED |
| 左导激活左边框 | 3px solid #7C3AED |
| 左导激活背景 | #FFFFFF |
| 折扣标签背景 | #EDE9FE |
| 折扣标签文字 | #7C3AED |
| links 点击激活背景 | #F3EEFF |
| links 点击激活文字 | #7C3AED |

### 5.2 背景色系

| 区域 | 色值 |
|------|------|
| 页面背景 | #FFFFFF |
| 左导背景 | #FAFAFA |
| 分割线 | #F3F4F6 |
| 分隔色块（推荐区间隔） | #F9FAFB |
| 商品图片占位色 | #F3F4F6 |

### 5.3 圆形卡片背景 10 色循环

按卡片 index % 10 取色，详见 3.4 节背景色表。

### 5.4 间距规范

| 位置 | 间距值 |
|------|--------|
| TopBar padding | 14px 16px 10px |
| 顶导单项 padding | 10px 14px |
| 左导单项 padding | 13px 10px 13px 14px |
| 右内容区 section-title padding | 14px 12px 8px |
| 圆形卡片 grid 左右 padding | 10px |
| 圆形卡片 grid gap | 8px |
| 商品卡片 grid 左右 padding | 10px |
| 商品卡片 grid gap | 8px |

### 5.5 字体规范

| 层级 | 字号 | 字重 | 颜色 |
|------|------|------|------|
| section 标题 | 15px | 700 | #111827 |
| 左导文字（默认） | 13px | 400 | #374151 |
| 左导文字（激活） | 13px | 700 | #7C3AED |
| 顶导 Tab（默认） | 14px | 400 | #6B7280 |
| 顶导 Tab（激活） | 14px | 700 | #7C3AED |
| 圆形卡片 label | 11px | 400 | #374151 |
| 商品品牌名 | 10px | 700 | #111827 |
| 商品名 | 11px | 400 | #6B7280 |
| 商品现价 | 13px | 700 | #111827 |
| 商品原价 | 11px | 400 | #9CA3AF |
| collection name | 12px | 600 | #111827 |
| links 文字 | 13px | 400 | #6B7280 |
| Brand 返回按钮 | 12px | 400 | #7C3AED |

---

## 6. 数据接口说明

> 本节定义前后端数据约定的字段结构，不是 HTTP 接口规格。API 路径和参数由开发另行定义。

### 6.1 顶导 Tab（Tab）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | 是 | 唯一标识，如 `new_arrivals` |
| label | string | 是 | 前端显示文案，如 `New Arrivals` |
| sort | number | 是 | 排序权重，数值越小越靠前 |
| active | boolean | 是 | 是否在前台显示 |

### 6.2 左导导航项（NavItem）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | 是 | 唯一标识，如 `na_for_you` |
| tab_id | string | 是 | 所属 Tab 的 id |
| label | string | 是 | 前端显示文案 |
| type | enum | 是 | 渲染类型：`reco` / `brand_circles` / `sub` / `leaf` / `links` |
| emoji | string | 否 | Brands Tab brand_circles 项展示的图标 |
| sort | number | 是 | 在该 Tab 左导内的排序 |
| active | boolean | 是 | 是否在前台显示 |

**type 枚举说明**：

| 枚举值 | 含义 | 适用 Tab |
|--------|------|----------|
| reco | 推荐页，含 9 个圆形快捷入口 + 商品推荐 | 所有 Tab |
| brand_circles | 品牌圆形双层钻取（Level 2 / Level 3） | 仅 Brands Tab |
| sub | 子分类聚合页（展示下级叶节点圆形） | 仅 Bags Tab 的 All Bags |
| leaf | 叶节点分类页，含子系列圆形 + Collection List 或 Product Grid | 大多数 Tab |
| links | 文字链接列表，主题编辑类 | 仅 New Arrivals Tab |

### 6.3 圆形卡片（SubCollection）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | 是 | 唯一标识 |
| nav_item_id | string | 是 | 所属导航项 id |
| name | string | 是 | 显示名称，如 `Shoulder` |
| emoji | string | 是 | 显示 emoji |
| count | number | 是 | 展示用商品数量（非实时，由后台配置或定时同步） |
| slug | string | 否 | 对应 collection 或分类的跳转 slug |
| sort | number | 是 | 在该导航项下的排序 |
| active | boolean | 是 | 是否在前台显示 |

### 6.4 品牌子系列（BrandSubCollection）

仅 Brands Tab Level 3 使用，通过品牌名关联。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| brand_name | string | 是 | 品牌名称，如 `Hermès`，关联上级 SubCollection.name |
| children | array | 是 | 子系列列表 |
| children[].name | string | 是 | 子系列名称 |
| children[].emoji | string | 是 | 子系列 emoji |
| children[].count | number | 是 | 商品数量（展示用） |
| children[].slug | string | 否 | 跳转 slug |
| children[].sort | number | 是 | 排序 |
| children[].active | boolean | 是 | 是否显示 |

### 6.5 links 链接项（LinksItem）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | 是 | 唯一标识 |
| nav_item_id | string | 是 | 所属 links 类型导航项 id |
| label | string | 是 | 显示文案，如 `Chain Shoulder` |
| slug | string | 是 | 跳转 slug，对应商品列表筛选页的主题标识 |
| sort | number | 是 | 排序 |
| active | boolean | 是 | 是否显示 |

### 6.6 商品卡片（ProductCard）

Shop 页商品卡片仅用于推荐展示，字段为轻量级 listing 摘要：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | 是 | 商品 listing id |
| brand | string | 是 | 品牌名，前端转大写展示 |
| name | string | 是 | 商品标题 |
| price | string | 是 | 现价，含货币符号，如 `$1,200` |
| original_price | string | 否 | 原价，有折扣时展示 |
| save_label | string | 否 | 折扣标签文案，如 `Save $1,500` 或 `35% Off` |
| sold_out | boolean | 否 | 是否售罄，默认 false |
| is_favorited | boolean | 否 | 当前用户是否已收藏，未登录为 false |
| image_url | string | 否 | 商品主图 URL，无图时前端用占位色块 |

### 6.7 Shop 页接口数据

前端加载 Shop 页时请求的数据结构：

```
GET /api/v1/shop/nav
Response:
{
  tabs: Tab[],                        // 顶导 Tab 列表（active=true），按 sort 排序
  nav_items: NavItem[],               // 所有 Tab 的导航项，前端按 tab_id 分组
  sub_collections: SubCollection[],   // 所有圆形卡片，前端按 nav_item_id 分组
  brand_subs: BrandSubCollection[],   // 品牌子系列（Level 3 数据）
  links: LinksItem[],                 // links 类型的链接项，按 nav_item_id 分组
}

GET /api/v1/shop/reco-products?context={nav_item_id}
Response:
{
  products: ProductCard[],  // 推荐商品列表，最多 20 条
}
```

---

## 7. 边界情况与异常处理

### 7.1 数据为空

| 场景 | 处理方式 |
|------|----------|
| Tab 列表为空（全部 inactive） | 不展示 Top Tab Bar，主体区显示空状态页："Shop is being updated, check back soon." |
| 某个 Tab 无激活的导航项 | 该 Tab 从前台隐藏（视同 inactive） |
| 某导航项无圆形卡片（sub/leaf 类型） | 不显示圆形区域，直接显示商品推荐区；若推荐也为空，显示 empty state |
| links 类型无链接项 | 显示 empty state：图标 + "No content available" |
| 推荐商品列表为空 | 不显示"You May Also Like"标题和分隔条，直接隐藏整个推荐区块 |
| 品牌 Level 3 子系列为空 | 不显示圆形区，显示商品推荐区；若推荐也为空，显示 empty state |

### 7.2 图片加载失败

| 场景 | 处理方式 |
|------|----------|
| 商品主图加载失败 | 保持 #F3F4F6 灰底占位，不显示破图标 |
| New Arrivals For You 圆形图片加载失败 | 降级为白底 + 默认 emoji（🛍） |
| Collection List 缩略图加载失败 | 保持灰底占位 |

### 7.3 网络异常

| 场景 | 处理方式 |
|------|----------|
| 首次加载失败 | 全页显示错误状态：图标 + "Something went wrong. Pull to refresh." |
| Tab 切换后数据加载失败 | 右内容区显示错误提示 + "Retry" 按钮，左导和顶导保持正常显示 |
| 商品推荐加载失败 | 静默失败，隐藏推荐区块，不影响圆形卡片部分 |
| 收藏操作失败 | 心形状态回滚到操作前，Toast 提示"Failed to save. Please try again." |

### 7.4 登录态

| 场景 | 处理方式 |
|------|----------|
| 未登录用户访问 Shop 页 | 正常访问浏览，不强制登录 |
| 未登录用户点击收藏 | 弹出登录引导弹窗，引导跳转登录页 |
| 登录后返回 Shop 页 | 商品卡片收藏状态更新为已登录用户的实际收藏状态 |

### 7.5 内容极端情况

| 场景 | 处理方式 |
|------|----------|
| 圆形卡片 label 超长（>6 个字符） | 最多 2 行，超出省略"…" |
| 品牌名过长（顶导 Tab 文案不超过 20 字符） | 截断 + 省略号，后台配置时提示建议长度 |
| 商品名称超长 | 最多 2 行，超出省略 |
| 导航项数量超多（单 Tab 超过 30 项） | 左导正常展示，纵向可滚动；后台配置时提示建议不超过 25 项 |
| Sold Out 商品点击 | 可正常跳转详情页，详情页展示库存状态 |

### 7.6 加载状态

| 区域 | 加载态 |
|------|--------|
| 顶导 Tab | 首次加载时显示 3 个骨架 Tab 占位 |
| 左导 | 显示 5 行灰色骨架条 |
| 圆形卡片区 | 3 列 × 3 行灰色圆形骨架 |
| 商品卡片区 | 2 列 × 3 行商品卡片骨架 |
| Collection List | 3 行 140px 高骨架块 |
