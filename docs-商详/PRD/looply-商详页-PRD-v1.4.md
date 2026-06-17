# looply 商详页 PRD V1.4

> **版本**：V1.4 | **日期**：2026-06-11
>
> **定位**：本文档定义商详页所有模块的数据来源、取值规则、业务逻辑和边界处理。不含端交互行为（PC/APP 各自的交互说明文档维护）。
>
> **数据模型基于**：商品系统 PRD v1.7 · 商品系统 ER v2.6 · Market 主数据 PRD v1.2 · Market ER v5.0 · 翻译模块 PRD v1.1 · 翻译 ER v2.1 · 库存管理 PRD v1.1 · 库存 ER v4.0 · 汇率管理 PRD v4.2

---

## 一、概述

### 1.1 背景与目标

looply 是二手奢侈品电商平台，商详页（Product Detail Page, PDP）是用户了解商品信息、建立信任、完成购买决策的核心页面。

本 PRD 的目标：

- 统一定义商详页各模块的数据来源和取值规则，作为 PC 端和 APP 端共同遵循的逻辑层
- 衔接 CMS 配置后台，明确哪些内容由后台配置驱动
- 消除 PC/APP 两端交互说明中数据逻辑重复维护导致的不一致问题

### 1.2 不做什么

| 不做 | 说明 |
|------|------|
| 端交互行为 | hover、手势、动效、布局尺寸等由 PC/APP 各自的交互说明文档维护 |
| CMS 后台页面交互 | 后台的页面交互、表单校验等由 CMS 后台原型文档维护；CMS 配置的业务规则（继承、保存、变更记录等）在本文档 2.3 节定义 |
| 后端接口设计 | API 路径、参数格式属于技术文档范畴 |

### 1.3 用户角色

| 角色 | 说明 |
|------|------|
| 买家（C 端用户） | 浏览商品、了解成色、比价、加购或直接结算 |

> 商详页仅面向 C 端买家，不涉及商家后台或运营后台视角。

### 1.4 核心场景

| 场景 | 用户行为 | 关键模块 |
|------|---------|---------|
| 了解商品基本信息 | 查看品牌、标题、价格、描述 | 商品信息区、商品描述 |
| 评估二手品质 | 查看成色等级、成色与外观描述、鉴定认证、配件信息 | Condition 成色折叠区 |
| 了解商品属性 | 查看材质、颜色、尺寸等属性，查看尺寸标注 | Description 描述折叠区 |
| 查看商品实拍图 | 浏览图片、放大查看细节 | Gallery、Lightbox |
| 了解物流与退换政策 | 查看运费、退货政策 | Shipping & Returns |
| 购买决策 | 加入购物车或直接结算 | CTA 按钮、APP Sticky 底部栏 |
| 发现更多商品 | 浏览推荐商品、查看最近浏览 | 推荐区、浏览历史 |

### 1.5 模块导航说明

商详页是单页面，由以下模块从上到下组成：

```
Header 导航栏
  ↓
面包屑（PC 独有）
  ↓
Gallery 图片区
  ↓
商品信息区（品牌 / 标题 / 价格 / Tax）
  ↓
商品描述
  ↓
CTA 按钮 & 支付方式
  ↓
Condition 成色折叠区
  ↓
Description 描述折叠区
  ↓
Shipping & Returns 折叠区
  ↓
You May Also Like 推荐区
  ↓
Recently Viewed 浏览历史
  ↓
Footer 页脚
```

其中 Lightbox（灯箱）为 Gallery 主图点击后的全屏查看器。

### 1.6 术语说明

| 术语 | 说明 |
|------|------|
| listing | 渠道挂牌记录，一个实物商品在不同渠道可以有不同的 listing |
| product | 实物商品（二手商品），每件商品一条 product 记录 |
| SPU | 标品（Standard Product Unit），如"LV Speedy 25"，product 通过 standard_sku 关联到 SPU |
| standard_sku | 标品 SKU，SPU 下按销售属性（颜色、尺码）区分的标准单品 |
| Market | 市场区域（如 US Market），决定默认语言、默认货币、配送策略 |
| CMS 配置 | 通过后台管理系统配置的内容，支持按维度（类目/品牌/系列）差异化 |
| 币种转换 | 当用户选择的展示货币与 listing 定价货币不同时，按汇率换算并适配尾数规则 |
| 展示标题 | 渠道商品的前台展示标题（listing_title），默认使用商品原始名称，可按渠道差异化修改 |

### 1.7 多语言 / 多币种策略

**多语言**：
- 商详页几乎所有文本内容都经过翻译模块处理（详见 2.2 翻译规则）
- 品牌名等特定内容通过术语表标记为禁译词
- 翻译版本由用户当前语言决定，语言可通过 Header 切换
- RTL 布局：当用户语言的 `language.rtl=true`（如阿拉伯语、希伯来语）时，页面整体镜像布局（文字右对齐、图片区和信息区左右互换等）。具体布局适配由前端 CSS `dir="rtl"` 处理

**多币种**：
- 所有价格展示均以用户当前选择的货币为准
- 当展示货币与定价货币不同时，做汇率换算 + 尾数规则适配（详见 2.7 价格体系）
- 结算时使用用户当前看到的展示货币，不回退到定价货币

---

## 二、需求详细描述

### 2.1 运行时上下文

**功能描述**

商详页加载时，系统需要确定 4 个上下文参数，所有数据查询都依赖这些参数。

**上下文参数**

| 参数 | 确定方式 | 影响范围 |
|------|---------|---------|
| `market_id` | 用户访问的域名/URL 决定（如 looply.com → US Market） | 默认语言、默认货币、配送政策、支付方式、内容版本 |
| `language_code` | 默认 = Market 默认语言（`market_language.is_default=true`），用户可通过 Header 切换 | 所有文本的翻译版本 |
| `currency_code` | 默认 = Market 默认货币（`market_currency.is_default=true`），用户可通过 Header 切换 | 价格展示币种、货币符号、小数位 |
| `channel_id` | 当前访问渠道（自营线上商城 = 固定值） | 查哪条 listing 记录 |

**页面入参**

通过 URL 获取 `listing_id`（或 `product_id` + `channel_id` 组合），作为整个页面的数据查询起点。

---

### 2.2 翻译规则

**功能描述**

商详页几乎所有文本内容都需要多语言支持。翻译通过统一的 `translation` 表查询，当前语言等于 Market 默认语言时直接取源值，不查翻译表。

**resource_type 全量清单**

| resource_type | 翻译内容 | 页面元素 | resource_id | field_name |
|---------------|---------|---------|-------------|------------|
| `listing` | 渠道级内容 | 展示标题、描述 | listing_id | `listing_title`, `listing_description` |
| `product` | 实物商品内容 | 通用标题 | product_id | `title` |
| `product_inspection` | 质检/成色内容 | 成色描述、外观描述、配件信息、补充描述 | product_id | `condition_summary`, `appearance_desc`, `accessories_info`, `supplement_notes` |
| `spu` | 标品内容 | 标品名、标品描述 | spu_id | `spu_name`, `description` |
| `brand` | 品牌名 | 面包屑、信息区、卡片 | brand_id | `brand_name` |
| `category` | 类目名 | 面包屑 | category_id | `category_name` |
| `attribute` | 属性展示名 | Description 折叠区左列 | attribute_id | `display_name`（CMS 覆盖值）或 `attribute_name`（兜底） |
| `attribute_option` | 属性值 | Description 折叠区右列 | option_id | `option_value` |
| `enum` | 枚举展示名 | 成色等级 | -- | 枚举值（如 `NWT`, `Excellent`） |
| `ui` | 界面文案 | 按钮、徽章、Tax 提示 | -- | Key（如 `btn.add_to_cart`） |
| `content` | CMS 内容 | Shipping & Returns | content_id | `body` |

**翻译查询优先级（Fallback 策略）**

商详页查询翻译时，按以下优先级取值：

| 优先级 | 条件 | 展示内容 |
|--------|------|---------|
| 1 | 目标语言有 `status=approved` 的译文 | 展示该译文 |
| 2 | 目标语言有 `status=pending_review` 的译文（AI/人工翻译完成，未审核） | 展示该译文（AI 翻译质量已足够可读） |
| 3 | 目标语言有 `status=outdated` 的译文（源内容已变更，旧译文可能不准确） | 展示旧译文（有旧译文优于无译文） |
| 4 | 目标语言无任何翻译记录 | 回退到 Market 默认语言的源值 |

> 当用户当前语言 = Market 默认语言时，直接取源值，不查翻译表。

**不翻译的内容**

| 内容 | 原因 |
|------|------|
| `listing.listing_id`（Listing 编号） | 唯一标识，各语言相同 |
| 品牌名（大部分奢侈品品牌） | 通过术语表 `glossary_concept` 标记为禁译词 |
| 图片 URL | 无需翻译 |
| 价格数值 | 数值不翻译，仅做币种转换 |
| 货币符号 | 取自 `currency` 表，不走翻译 |

---

### 2.3 CMS 配置规则

**功能描述**

商详页部分模块的展示内容由 CMS 后台配置驱动，支持按「类目 > 品牌 > 系列」维度差异化配置。后台操作流程详见 CMS 配置后台原型文档。

**可配置模块**

| 模块 | 可配置内容 | 详见章节 |
|------|-----------|---------|
| Description 描述 | 属性展示配置（定义展示名 + 绑定数据源 + 排序），含 Size Guide（固定模块，选择类目后自动带入） | 2.11 |

**不可配置（固定）模块**

Breadcrumb、Gallery、商品信息区、商品描述、Condition 成色、CTA & 支付方式、Shipping & Returns、推荐区、浏览历史、Footer、Lightbox——这些模块的数据来源固定，无需后台配置。

> CTA 支付方式图标本期写死 12 个，后续支付模块就绪后升级为动态配置。Shipping & Returns 本期为前端固定文案，后续配送模块就绪且规则更灵活时再升级为 CMS 配置。

**继承机制**

适用于 Description 模块的展示配置：

- 按 **系列 > 品牌 > 类目** 逐级查找，命中即停
- 示例：LV Monogram 项链 → 先找「Jewelry > LV > Monogram」→ 无则找「Jewelry > LV」→ 无则找「Jewelry」兜底
- 子级规则**整条覆盖**父级，不做属性级合并
- 删除子级规则后**立即**回退到继承父级，无延迟生效
- 所有层级规则均被删除（含类目级兜底）时，前台 Description 区域整体隐藏，不展示

**作用域唯一性**

- 同一作用域（类目 + 品牌 + 系列的组合）只能存在一条规则
- 新增规则时，若选择的作用域已有规则，系统报错提示"该作用域已存在规则，请编辑现有规则"

**保存行为**

- 当前不设草稿态，保存即生效
- 运营点击「保存」后，规则立即应用到前台商详页
- 不设审批流程

**筛选联动规则**

规则列表支持按类目和品牌筛选：

| 筛选器 | 行为 |
|-------|------|
| 类目筛选 | 选择即筛选（无查询按钮），展示该类目及其下属所有层级规则 |
| 品牌筛选 | 跟随类目级联——选择类目后，品牌下拉只显示该类目下已有规则的品牌 |
| 组合筛选 | 类目 + 品牌同时选中时，展示该品牌及其下属系列的规则 |
| 无结果 | 表格空态显示"未找到匹配的规则" |

**模块开关**

- Description 模块开关关闭后，前台商详页不展示 Description 区域（完全隐藏，无默认内容）
- 开关切换即时生效，不需要额外保存操作
- 后续其他可配置模块沿用同一套开关逻辑

**Size Guide 默认值策略**

- 新增规则时 Size Guide 作为固定模块自动带入属性列表
- 有尺码概念的类目（Jewelry / Bags / Clothing 等）：Size Guide 默认开启
- 无尺码概念的类目（Electronics 等）：Size Guide 默认关闭
- 关闭 Size Guide = 该作用域下商详页不展示 Size Guide 入口
- Size Guide 数据来源关联商品属性中的尺码体系（`size_system` + `size_mapping` + `dimension_diagram`）

**配置变更记录**

记录所有 CMS 配置操作，用于审计追溯：

| 记录字段 | 说明 |
|---------|------|
| 操作人 | 执行配置操作的运营人员 |
| 操作时间 | 精确到分钟 |
| 操作类型 | 新增规则 / 编辑规则 / 删除规则 / 模块开关变更 |
| 变更详情 | 涉及的作用域 + 具体变更内容（如"新增 Material / Color 2 个属性"、"关闭 Size Guide"） |

- 永久保留，不设滚动清理（配置变更频率低，存储成本可忽略）
- 支持按操作人和操作类型筛选

**操作权限**

- 当前不做权限细分，所有后台运营人员均可配置规则和查看变更记录
- 后续接入权限系统后按角色区分（CMS 管理员 / 只读运营）

**属性展示名与翻译**

- 运营配置的属性前台展示名（`display_name`），保存后自动进入翻译队列，由翻译模块统一处理
- 翻译完成前，前台按原始语言（英文）展示
- 翻译流程不在本文档定义，详见翻译模块 PRD

---

### 2.4 Header 导航栏

**功能描述**

页面顶部固定导航栏，提供品牌 Logo、品类导航、语言/货币切换、账户/搜索/收藏/购物车入口。

**数据来源与取值规则**

| 页面元素 | 数据源 | 取值逻辑 |
|---------|-------|---------|
| 导航链接 | 前台类目（待设计） | 本期跳转地址统一写死为 `www.looply.com`，后期接入前台类目模块 |
| 语言列表 | `market_language` + `language` | 当前 `market_id` 关联的语言中，**仅展示 `status=active` 的记录**（`planning`/`suspended` 不对 C 端展示）。按 `priority` 升序排列，默认选中 `is_default=true` |
| 货币列表 | `market_currency` + `currency` | 当前 `market_id` 关联的货币中，**仅展示 `status=active` 的记录**。按 `priority` 升序排列，默认选中 `is_default=true` |
| Cart 角标数量 | 订单域 | 当前购物车商品数量，0 时不显示角标 |

**展示规则**

- 语言切换后整站内容翻译为目标语言
- 货币切换后整站价格按汇率换算为目标货币展示（含尾数适配）
- 导航链接由 CMS 或后台配置管理，支持按 Market 差异化展示

**边界情况**

- 未登录时点击 Account 或 Wishlist 图标，跳转登录页

**UI 关联**

- PC 端：looply-商详页-PC-交互说明.html → Module 1
- APP 端：looply-商详页-APP-v3.html → Module 1

---

### 2.5 面包屑（PC 独有）

**功能描述**

展示当前商品在品牌和品类体系中的层级路径，辅助用户定位和导航。APP 端无此模块。

**数据来源与取值规则**

| 页面元素 | 数据源 | 取值逻辑 |
|---------|-------|---------|
| 品牌名 | `brand.brand_name_en` | 通常禁译（术语表标记） |
| 品类名 | `backend_category.category_name` | 链路：`spu.category_id` → `backend_category`，走翻译 |
| 商品标题 | `listing.listing_title` > `product.title` | 展示标题优先，走翻译 |

**展示规则**

- 层级格式：品牌 > 品类 > 商品标题
- 品牌名和品类名可点击，分别跳转品牌聚合页和商品列表页
- 最后一段（商品标题）为当前页，不可点击

**边界情况**

- 品类层级 > 3 层时，只展示最后 3 级，首段以 "..." 替代
- 商品名过长时文本自然换行，不截断

**UI 关联**

- PC 端：looply-商详页-PC-交互说明.html → Module 2
- APP 端：无（APP 端不展示面包屑）

---

### 2.6 Gallery 图片区

**功能描述**

展示商品图片（实拍图为主），支持缩略图切换、全屏灯箱查看。二手商品的实拍图是用户评估商品品质的核心依据。

**数据来源与取值规则**

| 页面元素 | 数据源 | 取值逻辑 |
|---------|-------|---------|
| 商品图片 | `product_image` 表（实拍图） | `WHERE product_id=? ORDER BY sort_order ASC`。**仅当实拍图为空（0 张）时**兜底取 `spu_image`（标品图，`image_type=main`，按 `sort_order` 排序） |
| 缩略图排序 | 同上 | 按 `sort_order` 排序 |
| 收藏按钮状态 | 收藏模块 | 已登录：调用收藏模块查询接口，判断当前用户是否已收藏该 listing；未登录：默认未收藏 |
| 收藏人数 | 收藏模块 | 调用收藏模块收藏计数接口。有收藏时展示（如 "12 people wishlisted"），无收藏时不展示 |

**展示规则**

- 主图使用 width=1200 高清 URL，缩略图使用 width=200
- 点击主图进入 Lightbox 全屏查看模式（详见 2.16）
- 收藏按钮点击切换收藏/取消收藏状态，未登录时先触发登录流程

**边界情况**

- 仅 1 张图：隐藏缩略图行和翻页控件
- 图片加载失败：显示灰色占位图 + 品牌 Logo 水印
- PC 端图片数量 > 6：缩略图区域自动换行为两行
- APP 端图片数量 > 10：缩略图区域可水平滚动

**UI 关联**

- PC 端：looply-商详页-PC-交互说明.html → Module 3
- APP 端：looply-商详页-APP-v3.html → Module 2

---

### 2.7 商品信息区（品牌 / 标题 / 价格 / Tax）

**功能描述**

展示商品核心信息：品牌名、商品标题、价格（含促销价和划线价）、Tax 提示。价格体系（币种转换、促销价计算）在本节统一定义，其他模块引用。

**数据来源与取值规则**

| 页面元素 | 数据源 | 取值逻辑 |
|---------|-------|---------|
| 品牌名 | `brand.brand_name_en` | 链路：`spu.series_id` → `series.brand_id` → `brand`。通常禁译（术语表标记）。点击跳转品牌聚合页 |
| 商品标题 | `listing.listing_title` > `product.title` | 展示标题优先；`product.title` 为空时系统自动拼接：`{关键属性值} {spu_name}`。走翻译 |
| 现价 | `listing.listing_price` 或 `promotion_price` | 有促销价时展示促销价，无促销价时展示 listing_price |
| 划线价 | `listing.listing_price` | 仅当促销价存在时展示（加删除线） |
| Save 差值 | 划线价 - 现价 | 均经币种转换后计算差值，差值本身不做尾数处理 |
| Tax 提示 | 翻译模块 | 固定文案 "No extra sales tax added at checkout."，按 Market 税务政策可能变化（如含税市场显示 "Includes VAT"）。`resource_type='ui'` |

#### 价格体系

**定价货币赋值逻辑**

`listing.currency_code` 在 listing 创建时自动取渠道 Market 的默认货币，不可手动修改。

链路：`channel.market_id` → `market_currency(is_default=true)` → `currency_code` → 写入 `listing.currency_code`

**币种转换流程**

当用户当前货币 ≠ listing 定价货币（`listing.currency_code`）时：

```
定价金额 → 汇率换算 → 尾差规则适配 → 最终展示价
```

- 汇率换算：调用汇率管理模块统一查询接口（详见汇率管理 PRD v4.2），传入 `from`（定价货币）+ `to`（用户货币），返回已含点差的平台汇率 `rate`。目标金额 = 源金额 × rate。汇率每日定时发布一次，日内固定
- 尾差规则适配：通过尾差规则（详见商品系统 PRD 2.8.1），按三层优先级生效（货币级 > Market 级 > 系统默认），支持 .99 / .95 / .00 / 整十 / 整百等尾数策略，采用四舍五入取整
- 用户当前货币 = 定价货币时直接展示，不做转换
- 结算货币：用户下单时使用当前看到的展示货币，不回退到定价货币

**促销价展示逻辑**

促销价由促销模块计算输出，不存储在 listing 表中。

| 场景 | 现价 | 划线价 | Save |
|------|------|-------|------|
| 有促销价（`promotion_price < listing_price`） | promotion_price | listing_price（删除线） | listing_price - promotion_price |
| 无促销价 | listing_price | 不展示 | 不展示 |

> 注意：现价、划线价均需做币种转换 + 尾数适配后再计算 Save。Save = 转换后划线价 - 转换后现价，Save 本身不做尾数处理。

**展示规则**

- 品牌名：大写字母展示，可点击跳转品牌聚合页
- 货币符号：取 `currency.currency_symbol`（如 "$"）
- 符号位置：取 `market_currency.symbol_position`（`before` = 前置如 `$12.99`，`after` = 后置如 `12.99€`），Market 级配置
- 小数位数：取 `currency.decimal_places`（如 USD=2 位，JPY=0 位）

**边界情况**

- 标题为空的三级兜底：`listing.listing_title` → `product.title` → 系统拼接 `{关键属性值} {spu_name}`

**UI 关联**

- PC 端：looply-商详页-PC-交互说明.html → Module 4
- APP 端：looply-商详页-APP-v3.html → Module 3

---

### 2.8 商品描述

**功能描述**

展示商品的营销性描述文案，描述品牌、品类、材质、成色特征等。

**数据来源与取值规则**

| 页面元素 | 数据源 | 取值逻辑 |
|---------|-------|---------|
| 描述文案 | `listing.listing_description` | 渠道描述，走翻译 |

**展示规则**

- PC 端全文展示，不做截断
- APP 端默认截断 2 行，末尾渐隐，点击 "Read more" 展开全文，展开后变为 "Read less" 可收起

**边界情况**

- 描述为空时：整个段落区域隐藏，不留空白
- APP 端文案不足 2 行时：不截断，不显示 Read more 按钮

**UI 关联**

- PC 端：looply-商详页-PC-交互说明.html → Module 5（描述部分）
- APP 端：looply-商详页-APP-v3.html → Module 4

---

### 2.9 CTA 按钮 & 支付方式

**功能描述**

核心转化模块，包含 Add to Cart 按钮、Checkout 按钮和支付方式图标展示。PC 端 CTA 按钮在页面内独立展示，APP 端 CTA 按钮在 Sticky 底部购买栏中（常驻屏幕底部，替代 APP 底部 TabBar）。

#### 商品可售性判断

商详页按钮状态由 `listing_status` + 库存状态共同决定：

| listing_status | 库存状态 | 页面展示 |
|---|---|---|
| `active` | 有库存 | Add to Cart 可点击，正常购买 |
| `active` | 已预留 / 已售出 | Sold Out 灰色不可点击 |
| `off_shelf` | -- | 页面显示"商品已下架"提示 |

> listing_status 为两状态（active/off_shelf）。off_shelf 通过 off_shelf_reason 区分下架原因（manual/out_of_stock/blocked/item_invalid），商详页不区分下架原因，统一展示"商品已下架"。库存可售状态由库存服务统一维护，商详页调用库存服务可售库存查询接口，返回 `available_qty > 0` 即可售。

**数据来源与取值规则**

| 页面元素 | 数据源 | 取值逻辑 |
|---------|-------|---------|
| Add to Cart 按钮价格 | 同 2.7 现价 | 展示当前现价，做币种转换 |
| 按钮文案 | 翻译模块 | `resource_type='ui'`，如 `btn.add_to_cart`、`btn.checkout` |
| 支付方式图标 | CMS 配置 | **本期写死**（12 个固定图标），后期由支付模块按 `market_id` / `country` 动态配置 |
| Verified 标记（APP 端） | `product_inspection.is_authenticated` | `is_authenticated=true` 时在 Sticky 底部栏显示绿色 "✓ Verified" 认证标记 |

**支付方式图标列表（本期固定）**

AMEX / Apple Pay / Diners Club / Discover / Google Pay / JCB / Maestro / Mastercard / PayPal / UnionPay / VISA / Klarna

**本期固定，后续升级**

支付方式图标本期前端写死 12 个全量展示，后续支付模块就绪后按 Market 动态配置可用支付方式。

**展示规则**

- Add to Cart：点击加入购物车，成功后按钮文字变为 "Added ✓" 并在短时间后恢复
- Checkout：点击直接进入结算流程（跳过购物车，直接结算当前商品）
- 支付方式图标纯展示，不可点击
- 未登录时点击按钮，先触发登录流程
- APP 端 Sticky 底部栏：三栏布局（左侧价格 | Add to Cart | Checkout），仅展示现价，不重复展示划线价和 Save（上方信息区已有）
- APP 端商详页隐藏底部 TabBar，由 Sticky 底部购买栏替代

**边界情况**

- 描述为空时：CTA 按钮上移（PC 端）
- Sold Out 时：两个按钮均禁用，变灰色

**UI 关联**

- PC 端：looply-商详页-PC-交互说明.html → Module 5（CTA + 支付方式部分）
- APP 端：looply-商详页-APP-v3.html → Module 5（支付方式）+ Module 12（Sticky 底部栏）

---

### 2.10 Condition 成色折叠区

**功能描述**

展示二手商品的成色信息，是 looply 作为二手平台的核心差异化模块。包含鉴定认证徽章、整体成色等级、成色描述、外观描述、配件信息、补充描述。

**数据来源与取值规则**

| 页面元素 | 数据源 | 取值逻辑 |
|---------|-------|---------|
| Certified Authentic 徽章 | `product_inspection.is_authenticated` + `product_inspection.authenticator` | `is_authenticated=true` 时展示绿色盾牌 + "Certified Authentic — by {authenticator}"。点击跳转鉴定说明页面（展示鉴定机构介绍、证书编号 `certificate_number`、鉴定日期 `auth_date` 等完整信息）。`is_authenticated=false` 时隐藏 |
| 成色等级 | `product_inspection.grade` | ENUM(NWT/Excellent/Good/Fair)，映射为展示名，走翻译（`resource_type='enum'`） |
| 成色描述 | `product_inspection.condition_summary` | 必填字段，整体成色概述，始终展示。走翻译（`resource_type='product'`, `field_name='condition_summary'`） |
| 外观描述 | `product_inspection.appearance_desc` | 选填，描述各部位外观状况。有值时展示，为空时隐藏该段。走翻译（`resource_type='product'`, `field_name='appearance_desc'`） |
| 配件信息 | `product_inspection.accessories_info` | 选填，描述配件齐全情况。有值时展示，为空时隐藏该段。走翻译（`resource_type='product'`, `field_name='accessories_info'`） |
| 补充描述 | `product_inspection.supplement_notes` | 选填，养护信息或功能使用情况等。有值时展示，为空时隐藏该段。走翻译（`resource_type='product'`, `field_name='supplement_notes'`） |

**成色等级枚举定义**

| 枚举值 | 展示名 | 含义 |
|--------|-------|------|
| NWT | New With Tags | 近全新带标签 |
| Excellent | Excellent | 几乎全新，极轻微使用痕迹 |
| Good | Good | 轻微使用痕迹 |
| Fair | Fair | 明显使用痕迹 |

**展示规则**

- 默认展开（核心二手差异信息，用户最关注）
- 展示顺序（固定）：徽章 → 成色等级 → 成色描述 → 外观描述 → 配件信息 → 补充描述
- 成色描述为核心字段，PC 端和 APP 端均全文展示，不截断
- APP 端选填字段（外观描述、配件信息、补充描述）：每段独立截断，超过 3 行时截断并渐隐，点击 "Read more" 展开该段，展开后变为 "Read less" 可收起
- PC 端所有字段全文展示，不截断
- Certified Authentic 徽章：鉴定状态="未鉴定"时隐藏

**边界情况**

- 外观描述 / 配件信息 / 补充描述为空时：该段落整体隐藏（含标题），不留空白
- 三个选填字段全部为空时：仅展示徽章 + 成色等级 + 成色描述
- APP 端某段文案不足 3 行时：不截断，不显示 Read more 按钮

**UI 关联**

- PC 端：looply-商详页-PC-交互说明.html → Module 6
- APP 端：looply-商详页-APP-v3.html → Module 6

---

### 2.11 Description 描述折叠区

**功能描述**

展示商品的属性信息（如材质、颜色、尺寸等），由 CMS 配置驱动展示哪些属性和排序。包含 Listing 编号和 Size Guide 入口。

**数据来源与取值规则**

| 页面元素 | 数据源 | 取值逻辑 |
|---------|-------|---------|
| item # | `listing.listing_id` | Listing 编号，对外展示，不翻译 |
| 描述属性（如 Material、Length） | `spu_attribute_value` + `attribute_def` | 通过 `standard_sku` → `spu` → `spu_attribute_value` 取值。属性名取值见下方「属性名取值逻辑」，属性值走翻译 |
| 销售属性（如 Color、Size） | `standard_sku_attribute` | 通过 `standard_sku_id` 查询。属性名取值见下方「属性名取值逻辑」，属性值走翻译 |

**属性展示筛选流程**

商品系统维护了完整的属性集，商详页不全量展示，经过以下筛选：

1. **查询展示范围**：通过 `attribute_scope_config`，根据当前商品的 `category_id` + `brand_id` + `series_id` 查询可展示属性定义（CMS 配置驱动，继承规则详见 2.3）
2. **取值**：描述属性从 `spu_attribute_value` 取值，销售属性从 `standard_sku_attribute` 取值
3. **过滤空值**：属性值为空的行不展示
4. **排序**：按 CMS 配置的排序顺序展示
5. **属性名取值**：取 CMS 配置中运营定义的前台展示名（`display_name`），展示名进翻译模块输出多语言版本。展示名为空时，前台不展示属性名 Label，仅展示属性值
6. **属性值翻译**：属性值走翻译模块

**Size Guide（尺寸测量方法）**

点击打开尺寸标注弹窗（PC 端弹窗 / APP 端 Bottom Sheet），展示逻辑分两种模式：

- **有 SVG 模板时（Template Mode）**：后台按末级类目配置 SVG 示意图模板（设计师出图，预留 `data-slot` 标记位置），前端根据当前商品所属类目查找模板 → 用 SKU 实测值替换 `data-slot` 占位符 → 拼接单位后渲染标注图
- **无模板时（Fallback）**：退化为纯文字列表，展示尺寸类属性（如 Length: 12.2 in, Width: 5.5 in）

> **度量单位（本期策略）**：本期属性值按录入值原样展示，不做运行时单位转换。商品录入时按目标市场习惯录入（如美国市场录 inches）。后续扩展欧洲等市场时再设计按 Market 偏好自动换算的方案。

**CMS 配置**

通过 CMS 后台的「Description 描述」模块配置：

- **属性展示配置**：定义前台展示名 + 绑定数据源属性 + 拖拽调整排序（操作顺序：先填展示名，再选数据源）
- **Size Guide**：固定模块，选择类目后自动带入属性列表，始终保留不可删除。运营可编辑前台展示名（默认 "Size"）、拖拽调整在属性列表中的位置、通过开关控制显示/隐藏。数据源为尺码体系（`size_system` + `size_mapping` + `dimension_diagram`），不可更换。前台渲染时如果该商品无尺码数据或 Size Guide 已关闭，链接不展示
- **继承规则**：按 系列 > 品牌 > 类目 逐级查找（详见 2.3）

**展示规则**

- 默认展开
- 每行一条属性，格式 "Label: Value"
- APP 端属性数量 > 8 行时截断，底部显示 "Show more attributes" 展开
- CMS 中配置了 Size Guide 但该商品无尺码数据时：Size Guide 链接不展示（静默隐藏，不报错）

**边界情况**

- 属性值为空时：该行不展示
- 当前类目未配置尺寸测量方法 SVG 模板：Size Guide 退化为文字列表
- 属性值带特殊字符：做 HTML 转义

**UI 关联**

- PC 端：looply-商详页-PC-交互说明.html → Module 7
- APP 端：looply-商详页-APP-v3.html → Module 7

---

### 2.12 Shipping & Returns 折叠区

**功能描述**

展示物流配送政策和退换货政策。本期为前端固定文案，后续配送模块就绪且规则更灵活时升级为 CMS 动态配置。

**数据来源与取值规则**

| 页面元素 | 数据源 | 取值逻辑 |
|---------|-------|---------|
| Free Shipping 文案 | 前端固定文案 | 本期写死，走翻译模块（`resource_type='ui'`） |
| Easy Returns 文案 | 前端固定文案 | 本期写死，走翻译模块（`resource_type='ui'`） |
| Policy 链接 | 前端固定配置 | 链接地址写死（如 `https://looply.com/pages/return-policy`） |

**展示规则**

- PC 端默认展开，APP 端默认折叠（减少首屏滚动深度）
- Policy 链接：PC 端新标签页打开，APP 端 Webview 或原生页面打开

**UI 关联**

- PC 端：looply-商详页-PC-交互说明.html → Module 8
- APP 端：looply-商详页-APP-v3.html → Module 8

---

### 2.13 You May Also Like 推荐区

**功能描述**

展示推荐引擎输出的相关商品，帮助用户发现更多感兴趣的商品。

**数据来源与取值规则**

推荐引擎输出 `listing_id` 列表，卡片数据从商品域获取。

**商品卡片字段映射**（推荐区和浏览历史通用）

| 卡片元素 | 数据源 | 取值逻辑 |
|---------|-------|---------|
| 图片 | `product_image`（`sort_order` 最小） > `spu_image` | 取首张实拍图，无实拍图时取标品主图 |
| 品牌名 | `brand.brand_name_en` | 通常禁译 |
| 商品名 | `listing.listing_title` > `product.title` | 展示标题优先，走翻译 |
| 现价 | `listing.listing_price` 或 `promotion_price` | 有促销价时展示促销价，做币种转换 + 尾数适配（见 2.7） |
| 划线价 | `listing.listing_price` | 仅促销时展示，做币种转换 + 尾数适配 |
| Save | 划线价 - 现价 | 均经币种转换后计算，不做尾数处理 |
| 收藏数 | 收藏模块 | 调用收藏模块收藏计数接口，无收藏时不显示数字 |
| 收藏按钮状态 | 收藏模块 | 同 2.6 Gallery 收藏按钮 |

**展示规则**

- 点击整张卡片跳转对应商品的商详页
- 收藏按钮点击直接收藏/取消收藏（无需进入详情页），未登录时触发登录流程
- 卡片标题超 2 行截断

**边界情况**

- 推荐数据为空：整个区域隐藏
- PC 端推荐 < 6 张：隐藏 Next 按钮，卡片靠左对齐

**UI 关联**

- PC 端：looply-商详页-PC-交互说明.html → Module 9
- APP 端：looply-商详页-APP-v3.html → Module 9

---

### 2.14 Recently Viewed 浏览历史

**功能描述**

展示用户最近浏览过的商品，帮助用户回到之前看过的商品。

**数据来源与取值规则**

| 页面元素 | 数据源 | 取值逻辑 |
|---------|-------|---------|
| 浏览记录 | `user_view_history` | 已登录：按 `viewed_at` 倒序取最近 N 条；未登录：使用浏览器 localStorage 记录 |
| 卡片字段 | 同 2.13 商品卡片字段映射 | 通用卡片结构 |

**展示规则**

- 当前商品不在浏览历史中重复展示
- 交互行为同推荐区（卡片点击、收藏）

**边界情况**

- 无浏览历史：整个区域隐藏
- 浏览记录中的商品已下架：标记 "Sold" 标签或从列表移除

**UI 关联**

- PC 端：looply-商详页-PC-交互说明.html → Module 10
- APP 端：looply-商详页-APP-v3.html → Module 10

---

### 2.15 Footer 页脚

**功能描述**

页面底部，包含关于信息、客服链接、Newsletter 订阅、社交媒体链接、支付/认证/物流合作信息、法律链接。

**数据来源与取值规则**

| 页面元素 | 数据源 | 取值逻辑 |
|---------|-------|---------|
| 文案（About / Customer Service 等） | CMS + 翻译模块 | `resource_type='ui'`，自管理 Key |
| Newsletter 订阅 | 营销模块 | 输入邮箱提交，成功/失败反馈 |
| 社交媒体链接 | 平台配置 | 可能按 Market 区分（如欧洲不展示 TikTok） |
| 法律链接 | 平台配置 | Accessibility Statement / Privacy Policy / Terms of Service |
| 支付/认证/物流图标 | 平台配置 | 纯展示，不可点击 |

**展示规则**

- PC 端：链接列表直接展示
- APP 端：About / Customer Service 用手风琴展开
- PC 端底部有免责声明（"Looply is an independent resale platform, not affiliated with..."），APP 端不展示

**UI 关联**

- PC 端：looply-商详页-PC-交互说明.html → Module 11
- APP 端：looply-商详页-APP-v3.html → Module 11

---

### 2.16 Lightbox 灯箱

**功能描述**

Gallery 主图点击后的全屏图片查看器，支持左右切换浏览所有商品图片。

**数据来源与取值规则**

- 图片数据同 2.6 Gallery，使用高清 URL（width=1200）
- 切换图片时同步更新 Gallery 缩略图高亮

**展示规则**

- 底部居中显示计数器（如 "2 / 6"），每次切换同步更新
- 打开时锁定页面背景滚动，关闭后恢复
- **不循环播放**：第一张图时 Prev 按钮禁用，最后一张图时 Next 按钮禁用
- PC 端支持键盘导航（Escape 关闭、左右箭头切换），APP 端支持手势操作（左右滑动切换、双指缩放）

**边界情况**

- 仅 1 张图：隐藏 Prev/Next 按钮和计数器
- 图片加载慢：显示 loading spinner 占位

**UI 关联**

- PC 端：looply-商详页-PC-交互说明.html → Module 12
- APP 端：looply-商详页-APP-v3.html → Module 2（Lightbox 部分）

---

## 三、依赖与风险

### 上下游系统依赖

| 依赖模块 | 提供内容 | 当前状态 | 风险 |
|---------|---------|---------|------|
| 商品域 | 商品基础数据（listing、product、SPU、属性） | 已有 | -- |
| Market 模块 | 语言/货币配置（含状态过滤、符号位置、RTL） | 已有 | -- |
| 汇率管理模块 | 平台汇率（已含点差）查询接口 | 已有 | -- |
| 商品定价（尾差规则） | 心理定价尾数策略（.99/.95/整十等） | 已设计（商品系统 PRD 2.8.1） | -- |
| 翻译模块 | 多语言文本 | 已有 | -- |
| 促销模块 | 促销价计算 | 待设计 | 促销价计算逻辑未定义，当前商详页按"无促销价"展示 |
| 收藏模块 | 收藏状态查询、收藏计数 | 待设计 | 收藏模块未设计，需对外提供查询接口 |
| 用户域 | 浏览历史 | 待设计 | `user_view_history` 实体未设计 |
| 库存模块 | 商品可售状态 | 已有 | -- |
| 推荐引擎 | 推荐商品列表 | 待设计 | 推荐算法和输出格式未定义 |
| 搜索服务 | Header 搜索功能 | 待设计 | 独立模块 |
| 支付模块 | 支付方式图标配置 | 待设计 | 本期写死 12 个固定图标 |
| 前台类目 | Header 导航链接 | 待设计 | 本期跳转地址写死 |
| CMS 系统 | 后台配置能力 | 原型已出 | 需开发实现 |

### 风险项

| 风险 | 影响 | 应对 |
|------|------|------|
| 收藏模块未设计 | 收藏状态和收藏人数无法展示 | 收藏按钮和人数需等收藏模块就绪后接入 |
| 浏览历史实体未设计 | 已登录用户浏览历史无法持久化 | 先用 localStorage 兜底 |
| 促销模块未设计 | 所有商品仅展示 listing_price，无促销价 | 价格展示逻辑已预留促销价入口，模块就绪后无需改动商详页 |

---

## 四、版本规划

### 当前版本（MVP）

- 商详页所有模块的展示逻辑
- CMS 后台配置（Description 属性展示）
- 币种转换（汇率换算 + 尾差规则，详见商品系统 PRD 2.8.1）
- 多语言翻译

### 后续迭代方向

| 方向 | 说明 |
|------|------|
| 促销价展示 | 促销模块就绪后接入商详页 |
| 收藏功能 | 收藏模块就绪后接入 |
| 支付方式动态配置 | 支付模块就绪后按 Market 动态展示 |
| 前台类目导航 | 前台类目模块就绪后替换写死链接 |
| 推荐引擎接入 | 推荐算法就绪后替换推荐区数据源 |
| Shipping & Returns CMS 化 | 配送模块就绪后，Shipping 文案从写死升级为 CMS 配置，支持按 Market 差异化 |

---

## 五、附录

### 5.1 设计稿索引

| 模块 | PC 端设计稿 | APP 端设计稿 |
|------|-----------|------------|
| 整体页面 | looply-商详页-PC-v1.3.html | looply-商详页-APP-v3.html |
| 交互说明 | looply-商详页-PC-交互说明.html | looply-商详页-APP-v3.html（含交互说明） |
| CMS 后台 | looply-商详页CMS配置后台原型-v1-antd.html | -- |

### 5.2 PC / APP 端差异对照表

以下为两端允许的差异，交互说明各自维护具体细节：

| 模块 | PC 端 | APP 端 |
|------|------|--------|
| 面包屑 | 有 | 无 |
| Gallery 切换方式 | 鼠标悬停缩放 + 点击缩略图 | 左右滑动 |
| 缩略图选中样式 | 深色边框 + 透明度 0.7→1 | 紫色边框 + 透明度 0.6→1 |
| 商品描述 | 全文展示 | 2 行截断 + Read more |
| Condition 成色区文本 | 全文展示 | 选填字段每段独立截断 3 行 + Read more |
| Description 属性截断 | 不截断 | > 8 行截断 + Show more |
| CTA 按钮位置 | 页面内独立按钮 | Sticky 底部购买栏 |
| Shipping & Returns 默认状态 | 默认展开 | 默认折叠 |
| 推荐区导航 | Carousel 左右箭头 | 水平滑动 |
| Lightbox 操作 | 键盘导航（Escape / 箭头） | 手势（滑动 / 双指缩放） |
| Add to Cart 反馈 | 文字变 "Added ✓"，2 秒恢复 | 文字变 "Added ✓" + 浅绿色背景，1.5 秒恢复 |
| Footer 导航展示 | 链接列表直接展示 | 手风琴展开 |
| Footer 免责声明 | 有 | 无 |
| Sticky 底部购买栏 | 无 | 有（详见 2.9 APP Sticky 部分） |

### 5.3 待补充项汇总

| 项目 | 类型 | 所属域 | 说明 |
|------|------|-------|------|
| 收藏模块 | 模块设计 | 独立模块 | 对外提供收藏状态查询、收藏计数、收藏/取消收藏等接口 |
| `user_view_history` | 新实体 | 用户域 | user_id + listing_id + viewed_at |
| 前台类目模块 | 新模块 | 独立模块 | Header 导航栏数据源 |
| 支付模块配置 | 模块设计 | 支付模块 | 按 Market 配置可用支付方式 |
| 推荐引擎 | 模块设计 | 独立模块 | 推荐算法和输出格式 |
| Shipping & Returns 内容 | CMS 配置 | 内容域 | 按 Market 区分政策内容 |

### 5.4 关联文档索引

| 文档 | 位置 | 说明 |
|------|------|------|
| PC 端交互说明 | `~/Desktop/海外业务/商详/UI/looply-商详页-PC-交互说明.html` | 12 模块的 PC 端交互行为 |
| APP 端交互说明 | `~/Desktop/海外业务/商详/UI/looply-商详页-APP-v3.html` | 12 模块的 APP 端交互行为 |
| CMS 后台原型 | `~/Desktop/海外业务/商详/原型/looply-商详页CMS配置后台原型-v1-antd.html` | Description 模块的后台配置操作（antd 版） |
| 数据来源与取值逻辑 V1.3 | `~/Desktop/海外业务/商详/looply-商详页-数据来源与取值逻辑.html` | 历史参考（已被本 PRD 替代） |
| 数据来源与实现逻辑 V2.0 | `~/Desktop/海外业务/商详/looply-商详页-数据来源与实现逻辑-V2.0.md` | 历史参考（已被本 PRD 替代） |

---

## 版本记录

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| V1.0 | 2026-05-26 | 初版，定义商详页 12 个模块的数据来源、取值规则和边界处理 |
| V1.1 | 2026-06-10 | 对齐商品系统 PRD v1.7：Condition 折叠区全面重写（成色等级 4 级、4 个文本字段替代结构化质检项、删除 CMS 配置）；listing_status 简化为两状态；鉴定信息字段扩展；尾差规则从"待设计"更新为引用商品系统 PRD 2.8.1；新增展示标题术语 |
| V1.2 | 2026-06-10 | 全量交叉对齐商品/Market/翻译/库存/汇率五模块最新方案。**修正**：成色字段从 product 表移至 product_inspection 表；supplement_notes 替代 additional_desc；Gallery 图片从 JSON 数组改为 product_image 独立表；汇率从直查表改为调汇率模块统一接口；语言/货币列表增加 status=active 过滤和 priority 排序；新增货币符号位置 symbol_position；库存可售状态改为调用库存服务查询接口。**新增**：翻译 Fallback 四级优先策略；RTL 布局支持；收藏人数展示；度量单位本期策略说明 |
| V1.3 | 2026-06-10 | **修正**：收藏相关数据源从直查 user_wishlist 改为调用收藏模块接口（收藏模块独立设计，对外提供查询能力）；移除 SEO 章节（SEO 为独立模块）；商品描述仅取 listing.listing_description，移除 product.description 兜底；库存可售判断改为调用库存服务可售库存查询接口，不暴露内部计算公式 |
| V1.4 | 2026-06-11 | **新增 CMS 后台业务规则（2.3 节扩展）**：作用域唯一性约束（重复报错）；保存行为（保存即生效，无草稿态）；筛选联动规则（选择即筛选 + 品牌级联）；模块开关行为（关闭=完全隐藏，即时生效）；Size Guide 默认值策略（按类目区分默认开/关）；配置变更记录（永久保留，4 种操作类型）；操作权限（当前不限，预留扩展）；属性展示名翻译流程（自动入队列）。**完善**：继承机制补充边界（所有层级删除→不展示）。**更新**：CMS 后台原型引用改为 antd 版 |
