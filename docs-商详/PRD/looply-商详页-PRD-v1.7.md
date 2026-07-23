# looply 商详页 PRD V1.7

> **版本**：V1.7 | **日期**：2026-07-23
>
> **定位**：本文档定义商详页所有模块的数据来源、取值规则、业务逻辑和边界处理。不含端交互行为（PC/APP 各自的交互说明文档维护）。
>
> **数据模型基于**：商品系统 PRD v1.7 · 商品系统 ER v2.6 · Market 主数据 PRD v1.2 · Market ER v5.0 · 多语言模块 PRD v3.2 · 多语言 ER v2.4 · 多语言接入规范（产品版）v3.2 · 库存管理 PRD v1.2 · 库存 ER v4.1 · 汇率管理 PRD v4.2
>
> **本版变更（V1.7）**：**多语言接入需求并入本 PRD。** 原独立的《looply-商详页多语言接入-PRD》系列（v1.0~v1.3）全部废弃，其内容按多语言模块 v3.2 新标准（建卡 translation_resource + 页面聚合 resource_group + storage_mode 存储方式）并入本文档 §1.7 多语言支持（三段结构）、§2.2 翻译资源映射与接入实施、§2.3 CMS 写入触发翻译。本版将「多语言 v3.2 建卡 + 聚合 + storage_mode 能力上线」列为商详页多语言上线的硬前置（见第三章）。

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
| CMS 后台页面交互 | 后台的页面交互、表单校验等由 CMS 后台原型文档维护；CMS 配置的业务规则（模板管理、模块开关、保存、变更记录等）在本文档 2.3 节定义 |
| 后端接口设计 | API 路径、参数格式属于技术文档范畴 |

### 1.3 用户角色

| 角色 | 说明 |
|------|------|
| 买家（C 端用户） | 浏览商品、了解成色、比价、加购或直接结算 |

> 商详页仅面向 C 端买家，不涉及商家后台或运营后台视角。

### 1.4 核心场景

| 场景 | 用户行为 | 关键模块 |
|------|---------|---------|
| 了解商品基本信息 | 查看品牌、标题、价格、描述 | 商品信息区、Description 描述折叠区 |
| 了解平台信任保障 | 查看认证、成色检查、售后保障承诺 | Certified Authentic 鉴定认证 |
| 评估二手品质 | 查看成色等级、成色进度条、成色描述、配件信息，查看 Condition Guide | Condition 成色折叠区 |
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
CTA 按钮
  ↓
Certified Authentic 鉴定认证
  ↓
Condition 成色折叠区
  ↓
Description 描述折叠区（含商品描述文案）
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

> **V1.5 变更**：原独立的"商品描述"模块合并到 Description 描述折叠区（属性表下方展示商品描述文案）；新增 Certified Authentic 模块（位于 CTA 和 Condition 之间）。

### 1.6 术语说明

| 术语 | 说明 |
|------|------|
| listing | 渠道挂牌记录，一个实物商品在不同渠道可以有不同的 listing |
| product | 实物商品（二手商品），每件商品一条 product 记录 |
| SPU | 标品（Standard Product Unit），如"LV Speedy 25"，product 通过 standard_sku 关联到 SPU |
| standard_sku | 标品 SKU，SPU 下按销售属性（颜色、尺码）区分的标准单品 |
| Market | 市场区域（如 US Market），决定默认语言、默认货币、配送策略 |
| PDP 模板 | 商详页内容模板，将 Certified Authentic / Condition / Description 的配置捆绑管理，一个模板关联一组类目 |
| CMS 配置 | 通过后台管理系统配置的内容，按 PDP 模板组织，支持模板级和类目级两种粒度 |
| 币种转换 | 当用户选择的展示货币与 listing 定价货币不同时，按汇率换算并适配尾数规则 |
| 展示标题 | 渠道商品的前台展示标题（listing_title），默认使用商品原始名称，可按渠道差异化修改 |
| 语言包 | 前端维护的静态 UI 文案国际化文件（storage_mode=`language_pack`），不进翻译中心 translation 表，但多语言后台提供查看/修改面 |
| 翻译服务 | 多语言模块对外提供的统一内容查询和写入接口 |
| translation_resource（建卡） | 翻译中心一级对象，一张卡片对应一类可翻译内容（含 resource_type / display_name / domain / group_code / key_type / storage_mode）。须先建卡再注册字段、推送源文 |
| resource_group（聚合组） | 把一个 C 端页面下的多张卡片聚合成一个导航单元。商详页聚合组 group_code=`pdp`（详见 1.7 B 段） |
| storage_mode | 存储方式：`translation_table`（翻译中心，保存写入翻译服务触发 AI 翻译）/ `language_pack`（语言包，后台改后同步回语言包） |
| 禁译词 | 通过术语表（glossary_concept）标记为不翻译的词，如奢侈品品牌名 |

### 1.7 多语言支持

商详页面向全球市场，几乎所有用户可见文本都需要多语言支持。本节按多语言接入规范（产品版）v3.2 的三段结构（A 静态 UI 文案 / B 动态业务内容 / C Fallback）定义商详页 C 端的内容接入；配套的 CMS 配置后台仅面向内部运营、本期仅中文、不接入多语言（其编辑的内容会显示到 C 端，接的是内容不是界面，见 B 段）。翻译资源到各页面元素的完整映射、CMS 写入规范见 §2.2；多币种策略见本节末尾。

> **模块边界**：多语言模块 = 平台方，制定并提供翻译接入的标准与平台能力（建卡机制、页面聚合、字段注册、读写接口、Fallback、术语表、domain / storage_mode 元数据）。商详页 = 接入方。其中第一类静态文案（语言包）、第二类 CMS 配置内容均由**商详页自建自维**（含 CMS 配置后台的建卡、字段注册、保存写入）；第三类内容来自**商品系统**，商详页对其只读取。

**A. 静态 UI 文案**

商详页的固定 UI 文案（按钮、区域标题、提示语、Toast、空状态、法律/免责声明等）由前端语言包实现（storage_mode=`language_pack`）。技术上走语言包落地，**多语言后台额外提供查看/修改面**——运营可在翻译中心（商详页聚合卡的"页面文案"分组）查看/修改静态文案的各语言值，保存后同步回语言包（同步机制由技术方案定）。作为聚合组成员 `page-pdp`（"页面文案"分组）登记。本文档不列具体文案原文，仅按类别登记范围（Header 导航/搜索占位、价格与税费提示、CTA 与各类 Toast、各折叠区标题与展开按钮、推荐区/浏览历史区域标题与售罄标签、Footer 链接与声明、APP 分享入口文案等）；含变量文案（如收藏人数）由前端渲染时注入变量。

**B. 动态业务内容 —— 翻译服务接入**

商详页**自身产生**、需多语言的业务字段为第二类 CMS 配置内容（Certified Authentic、Condition 等级体系、成色详细信息展示名、Description 属性展示名）。这些内容由商详页 CMS 配置后台按多语言 v3.2 标准**新建 4 张翻译卡片**（先建卡 → 再注册字段 → 保存时写入翻译服务触发 AI 翻译），4 张卡统一归入"商详页"聚合组。接入清单：

| 域名 | 卡片名 | 卡片编码（resource_type） | 字段（fieldName） | 中文显示名 | 数据类型 | 展示面 |
|------|-------|--------------------------|-------------------|-----------|---------|-------|
| 前端页面 | 商详-鉴定认证 | `pdp_template` | `ca_title` | 鉴定认证标题 | text | PDP Certified Authentic 区 |
| 前端页面 | 商详-鉴定认证 | `pdp_template` | `ca_desc` | 鉴定认证描述 | text | PDP Certified Authentic 区 |
| 前端页面 | 商详-鉴定认证 | `pdp_template` | `ca_detail` | 鉴定认证详情 | rich_text | PDP Certified Authentic 详情弹层 |
| 前端页面 | 商详-成色等级 | `pdp_condition_grade` | `grade_name` | 成色等级名称 | text | PDP Condition 进度条 / Guide |
| 前端页面 | 商详-成色等级 | `pdp_condition_grade` | `grade_description` | 成色等级描述 | text | PDP Condition Guide |
| 前端页面 | 商详-成色展示名 | `pdp_condition_display` | `display_name` | 成色展示名 | text | PDP 成色详细信息（字段名） |
| 前端页面 | 商详-属性展示名 | `pdp_description_display` | `display_name` | 属性展示名 | text | PDP Description（属性名 / Size Guide） |

> `ca_detail` 为富文本，允许加粗/斜体/列表/链接；内嵌图片上的文字不会被翻译。`display_name` 为运营配置的前台展示名（label），与展示的**值**是两回事——值来自商品系统（第三类，见下）。

**"商详页"聚合组声明（resource_group）**

上述 4 类 CMS 卡片 + 第一类静态文案卡片，按多语言 v3.2 声明为**一个页面聚合组**，避免 5 张卡零散扔在"前端页面"域、运营认不出同属商详页：

- **group_code**：`pdp` ｜ **group_name**：商详页 ｜ **domain**：前端页面（`frontend_page`）｜ **成员数**：5（1 类静态文案 + 4 类 CMS 动态内容）
- 数据层仍是 5 张独立卡片（各自建卡、各自注册字段、各自单层"实例 × 平铺字段"）；聚合只发生在导航展示层（多语言后台一张聚合卡 + 5 分组子导航，对应多语言原型 v13）。

| sort | 成员（子导航名） | resource_type | display_name（卡片展示名） | key_type | storage_mode | 配置粒度 |
|------|----------------|---------------|--------------------------|----------|--------------|---------|
| 1 | 页面文案 | `page-pdp` | 商详-页面文案 | `static_content` | `language_pack` | 页面级（静态文案） |
| 2 | 鉴定认证 | `pdp_template` | 商详-鉴定认证 | `entity_field` | `translation_table` | 模板级 |
| 3 | 成色等级 | `pdp_condition_grade` | 商详-成色等级 | `entity_field` | `translation_table` | 模板 × 等级 |
| 4 | 成色展示名 | `pdp_condition_display` | 商详-成色展示名 | `entity_field` | `translation_table` | 类目 × 字段 |
| 5 | 属性展示名 | `pdp_description_display` | 商详-属性展示名 | `entity_field` | `translation_table` | 类目 × 属性 |

> 建卡（migration）、聚合组声明、字段注册均在商详页 CMS 配置后台开发联调阶段完成，作为上线硬前置——未建卡则源文写入被拒绝（详见 §2.2）。`domain` / `group_code` 编码以多语言模块元数据实际定义为准。

**上游模块产生的内容（第三类，商详页只读取）**：商品标题、描述、品牌名、类目名、属性名/值、质检文本（成色概述/外观/配件/补充说明）、成色等级 grade 值等，由**商品系统**负责接入（各自拥有商品域卡片），商详页只调用翻译服务读取展示、不建卡不写入。完整字段清单不在此代列，以商品模块实际建卡的 resourceType 为准（见 §2.2）。

**C. Fallback 规则**

引用多语言 PRD §4.6 统一策略：有译文返回译文 → 有过期译文返回旧译文 → 无记录返回英文源文本。平台统一规则，商详页不自定义（详见 §2.2）。

**多币种策略**：

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

### 2.2 翻译资源映射与接入实施

**功能描述**

本节是 §1.7 三段框架的实施明细层，定义：① 各页面元素 ↔ 翻译资源（resourceType.fieldName）的完整映射；② 第二类 CMS 内容的建卡前置与写入翻译服务规范；③ 前端读取规范、Fallback、不翻译内容、术语表、RTL。所有动态内容统一调用翻译服务查询接口获取当前语言译文，商详页不处理翻译内部逻辑（默认语言短路、Fallback 等由翻译服务内部处理，商详页仅接收最终结果）。

#### 2.2.1 各页面元素翻译资源映射（全量）

| 页面元素 | 类别 | resource_type | fieldName | resource_id | 归属 / storage_mode |
|---------|------|---------------|-----------|-------------|--------------------|
| 展示标题、渠道描述 | 第三类 | `listing` | `listing_title` / `listing_description` | listing_id | 商品域 · translation_table |
| 通用标题（兜底） | 第三类 | `product` | `title` | product_id | 商品域 · translation_table |
| 成色概述/外观/配件/补充说明（值） | 第三类 | `product` | `condition_summary` / `appearance_desc` / `accessories_info` / `supplement_notes` | product_id | 商品域 · translation_table |
| 标品名、标品描述（兜底） | 第三类 | `spu` | `spu_name` / `description` | spu_id | 商品域 · translation_table |
| 品牌名（禁译词） | 第三类 | `brand` | `brand_name` | brand_id | 商品域 · translation_table |
| 类目名 | 第三类 | `category` | `category_name` | category_id | 商品域 · translation_table |
| 属性名（兜底） | 第三类 | `attribute` | `attribute_name` | attribute_id | 商品域 · translation_table |
| 属性值 | 第三类 | `attribute_option` | `option_value` | option_id | 商品域 · translation_table |
| 成色等级 grade 值（如 `Excellent`） | 第三类 | `enum` | `grade` | -- | 商品域 · translation_table |
| 鉴定认证标题/描述/详情 | 第二类 | `pdp_template` | `ca_title` / `ca_desc` / `ca_detail` | template_id | 聚合组 pdp · translation_table |
| 成色等级名称/描述（体系配置） | 第二类 | `pdp_condition_grade` | `grade_name` / `grade_description` | 等级配置记录 ID | 聚合组 pdp · translation_table |
| 成色详细信息展示名 | 第二类 | `pdp_condition_display` | `display_name` | 展示名配置记录 ID | 聚合组 pdp · translation_table |
| 属性/Size Guide 展示名 | 第二类 | `pdp_description_display` | `display_name` | 展示名配置记录 ID | 聚合组 pdp · translation_table |
| 静态 UI 文案（按钮/标题/Toast 等） | 第一类 | `page-pdp` | 各 Key | -- | 聚合组 pdp · language_pack |

> **grade 与成色等级体系是两套独立内容**：商品成色 grade 值（`enum`，商品域维护并接入，商详只读取）驱动"当前商品等级徽章"；CMS 配置的成色等级体系（`pdp_condition_grade`，商详自建卡）驱动"进度条分段 + Condition Guide"。二者互不打通、各自单独接入，不存在二选一。
>
> **第三类 resourceType 待商品模块对接确认**：上表第三类卡片标识以商品模块实际建卡为准（商品域 `attribute` 等口径待收敛）。商详页作为读取方须在商品模块卡片标识固化后核对本表，不得靠名称相似推断（见第三章风险项）。

#### 2.2.2 第二类 CMS 内容建卡与写入翻译服务规范

**建卡前置（硬前置）**：商详页 CMS 配置后台上线前，须由多语言模块通过 migration 在 `translation_resource` 建立 §1.7 B 段的 4 张卡片（写入 resource_type + display_name + domain=前端页面 + group_code=`pdp` + key_type=`entity_field` + storage_mode=`translation_table`），并声明聚合组 `resource_group=pdp`（5 成员 + sort_order），再在 `translatable_field_config` 注册各字段。**未建卡则源文写入被拒绝**（防止游离译文）。

**写入时机**（CMS 保存即写入翻译服务触发翻译）：

| CMS 操作 | 写入行为 |
|---------|---------|
| 新建模板并填鉴定认证 | 写入 3 条源语言记录（ca_title / ca_desc / ca_detail），触发首次翻译 |
| 编辑鉴定认证内容 | 更新对应源语言记录，触发过期检测和重译 |
| 新增成色等级 | 写入 2 条源语言记录（grade_name / grade_description） |
| 编辑/删除成色等级 | 更新记录触发重译 / 调用删除接口清除该等级所有译文 |
| 新增/编辑类目级成色展示名 | 每个展示名写入或更新 1 条源语言记录 |
| 新增/编辑类目级属性展示名 | 每个展示名写入或更新 1 条源语言记录 |
| 删除类目级规则 | 清除该规则下所有展示名译文记录 |
| 删除 PDP 模板 | 清除该模板及其关联的所有 CMS 译文记录 |

**写入参数**：`resourceType` + `resourceId`（配置记录 ID）+ `fieldName` + `source_language_code`（本期固定 `en`）+ `translated_value`（运营填写的源文本）。同一份内容由 `(resourceType, resourceId, fieldName)` 定位。

**异常处理**：翻译服务不可用时源内容写入异步重试、不阻塞 CMS 保存；卡片/字段未注册被拒时提示运营"该内容尚未接入翻译中心，请联系管理员完成建卡/注册"并阻止源文推送；查询返回空时前端展示英文源文本（Fallback）。

#### 2.2.3 前端读取规范

- 查询参数：`resourceType` + `resourceId` + `fieldName` + `language_code`（用户当前语言）；翻译服务内部处理 Fallback，商详页只接收最终结果
- 当前语言 = Market 默认语言时，翻译服务返回源语言记录（短路优化由翻译服务内部处理）
- **批量查询**：商详页一次加载涉及多个 resourceType，应使用翻译服务批量查询能力，一次请求获取所有译文，避免逐字段查询

#### 2.2.4 Fallback 策略

引用多语言 PRD §4.6 统一策略，三类内容统一：

| 优先级 | 条件 | 展示内容 |
|-------|------|---------|
| 1 | 目标语言有译文（translated） | 展示译文 |
| 2 | 目标语言有过期译文（outdated） | 展示旧译文（翻译服务内部处理，商详页不感知） |
| 3 | 无译文记录 | 展示英文源文本 |

> 第一类（语言包）缺目标语言时由前端 i18n 框架降级显示英文；第二/三类（translation_table）Fallback 由翻译服务内部处理。商详页均只接收最终结果。

#### 2.2.5 不翻译的内容

| 内容 | 原因 |
|------|------|
| `listing.listing_id`（Listing 编号） | 唯一标识，各语言相同 |
| 品牌名（大部分奢侈品品牌） | 通过术语表 `glossary_concept` 标记为禁译词，正常接入翻译服务、返回结果已含原文 |
| 图片 URL | 无需翻译 |
| 价格数值 / 货币符号 | 数值仅做币种转换；货币符号取自 `currency` 表，不走翻译 |
| 语言名称 / 货币名称 | 取自 Market 模块（language / currency 表），不走翻译 |
| Lightbox 计数器（"2 / 6"） | 纯数字格式 |

#### 2.2.6 术语表与 RTL

- **品牌名禁译词**：奢侈品品牌名（如 LOUIS VUITTON、CHANEL）在全球各语言保持原文，须在多语言模块术语表注册为禁译词（rule_type=do_not_translate），品牌数据初始化时批量导入。商详页正常调用翻译服务即可，翻译服务返回结果已含原文。
- **RTL 布局**：当用户语言 `language.rtl=true`（如阿拉伯语、希伯来语）时，页面整体镜像布局（文字右对齐、图片区与信息区左右互换），由前端 CSS `dir="rtl"` 处理。多语言内容本身不受影响，三类内容读取方式不因 RTL 变化。

---

### 2.3 CMS 配置规则

**功能描述**

商详页部分模块的展示内容由 CMS 后台配置驱动。配置通过 **PDP 模板（Template）** 组织，每个模板关联一组类目，模板内分模块管理配置。后台操作流程详见 CMS 配置后台原型文档。

#### PDP 模板

**模板概念**

PDP 模板是商详页内容配置的顶层组织单元。一个模板定义了一组商详页的 Certified Authentic、Condition 等级体系和 Description 属性展示规则。

| 属性 | 说明 |
|------|------|
| 模板名称 | 运营自定义（如"Luxury PDP"、"Electronics PDP"），不允许重名，最大 50 字符 |
| 模板描述 | 选填，用于标注模板用途（如"适用于奢侈品箱包、珠宝、腕表类目"） |
| 关联类目 | 一个模板关联一组类目；一个类目只能属于一个模板 |
| 模板级配置 | Certified Authentic、Condition 等级体系——同一模板下所有类目共享 |
| 类目级配置 | Description 属性展示——模板内按类目差异化配置 |

**模板与类目的关系**

- 一个类目只能关联到一个 PDP 模板（1:N 关系，模板:类目）
- 未关联任何模板的类目，商详页上 Certified Authentic 不展示、Condition 仅展示基本成色信息（无进度条和等级体系）、Description 不展示
- 修改模板关联的类目即时生效

#### 可配置模块

| 模块 | 配置粒度 | 可配置内容 | 详见章节 |
|------|---------|-----------|---------|
| Certified Authentic 鉴定认证 | 模板级 | 标题、描述文案、详细说明（半层弹窗内容） | 2.9 |
| Condition 成色 | 模板级 + 类目级 | 模板级：成色等级体系（等级名称 + 描述）；类目级：成色详细信息展示配置（定义展示名 + 绑定数据源字段 + 排序） | 2.10 |
| Description 描述 | 类目级（模板内） | 属性展示配置（定义展示名 + 绑定数据源 + 排序），含 Size Guide | 2.11 |

#### 不可配置（固定）模块

Breadcrumb、Gallery、商品信息区、CTA 按钮、Shipping & Returns、推荐区、浏览历史、Footer、Lightbox——这些模块的数据来源固定，无需后台配置。

> Shipping & Returns 本期为前端固定文案，后续配送模块就绪且规则更灵活时再升级为 CMS 配置。

#### Condition 成色详细信息配置规则

Condition 模块的成色详细信息在模板内按类目配置，每个类目独立维护一套字段展示规则（与 Description 属性配置模式一致）：

- 每个类目一条规则，从 `product_inspection` 可用字段中选择要展示的字段，定义展示名和排序
- 可配置的数据源字段：`condition_summary`（成色概述）、`appearance_desc`（外观状况）、`accessories_info`（配件情况）、`supplement_notes`（补充说明）
- 每个字段可自定义展示名（如珠宝类 appearance_desc → "Chain"，箱包类 → "Exterior"），展示名走翻译
- 同一模板内不同类目可配置不同的字段集合和展示名
- **新增规则时类目选择互斥**：同 Description，已配置类目置灰不可选
- 类目规则**整条替换**，不做字段级合并
- 删除某类目的规则后，该类目商品的成色详细信息区域不展示（仅保留进度条 + Condition Guide + 徽章）

#### Description 属性配置规则

Description 模块在模板内按类目配置，每个类目独立维护一套属性展示规则：

- 每个类目一条规则，定义展示哪些属性、展示名、排序
- 同一模板内不同类目可配置不同的属性集合
- **新增规则时类目选择互斥**：下拉列表仅展示当前模板关联的类目，已配置规则的类目置灰显示"xxx（已配置）"不可选择。所有类目均已配置时，提示"当前模板下所有类目已配置，如需调整请编辑已有规则"
- 类目规则**整条替换**，不做属性级合并
- 删除某类目的规则后，该类目商品的 Description 区域整体隐藏
- 模板内所有类目的规则均被删除时，该模板下所有商品的 Description 区域隐藏

#### 保存行为

- 当前不设草稿态，保存即生效
- 运营点击「保存」后，配置立即应用到前台商详页
- 不设审批流程

#### 模块开关

- Certified Authentic / Condition / Description 模块各有独立开关
- 模块开关关闭后，前台商详页不展示该模块的 CMS 配置内容（完全隐藏，无默认内容）
  - **Condition 例外**：Condition 模块开关仅控制模板级 CMS 配置的部分（进度条 + Condition Guide）。关闭后这些内容不展示，但成色详细信息（CMS 类目级配置的展示名 + product_inspection 数据值）仍保留展示（属于商品固有质检信息，不受模块开关控制）
- 开关切换即时生效，不需要额外保存操作
- 开关作用于整个模板（即模板下所有关联类目统一生效）

#### Size Guide 默认值策略

- 新增 Description 规则时 Size Guide 作为固定模块自动带入属性列表，默认开启
- 运营可通过开关控制该类目是否展示 Size Guide 入口
- 关闭 Size Guide = 该类目下商详页不展示 Size Guide 入口
- 前台渲染时，即使 Size Guide 开启，如果该商品无尺寸测量数据，链接自动不展示（静默隐藏）
- Size Guide 数据来源关联商品的尺寸测量方法：后台按末级类目配置多套 SVG 测量示意图（不同形状比例），前端根据商品实测尺寸比值自动匹配最合适的模板，用实测数据动态填充 SVG 标记位

#### 配置变更记录

记录所有 CMS 配置操作，用于审计追溯：

| 记录字段 | 说明 |
|---------|------|
| 操作人 | 执行配置操作的运营人员 |
| 操作时间 | 精确到分钟 |
| 所属模板 | 该操作所在的 PDP 模板 |
| 所属模块 | 模板管理 / Certified Authentic / Condition / Description / 模块管理 |
| 操作类型 | 创建模板 / 编辑模板 / 删除模板 / 编辑配置 / 新增规则 / 编辑规则 / 删除规则 / 关闭模块 / 开启模块 |
| 变更详情 | 具体变更内容，示例见下表 |

**操作类型与变更详情示例**

| 操作类型 | 所属模块 | 变更详情示例 |
|---------|---------|------------|
| 创建模板 | 模板管理 | 创建「Luxury PDP」，关联 Jewelry & Accessories / Bags / Watches |
| 编辑模板 | 模板管理 | 修改「Luxury PDP」名称为「Premium PDP」 |
| 删除模板 | 模板管理 | 删除「Electronics PDP」 |
| 编辑配置 | Certified Authentic | 修改 Certified Authentic 标题和描述文案 |
| 新增规则 | Description | 新增 Watches 类目级 Description 属性配置 |
| 编辑规则 | Condition | 修改 Bags 类目级成色详细信息配置：新增 Care Notes 字段 |
| 删除规则 | Description | 删除 Shoes 类目级 Description 属性配置 |
| 关闭模块 | 模块管理 | 关闭「Luxury PDP」的 Condition 模块 |
| 开启模块 | 模块管理 | 开启「Luxury PDP」的 Condition 模块 |

- 永久保留，不设滚动清理（配置变更频率低，存储成本可忽略）
- 支持按所属模板和所属模块筛选

#### 操作权限

- 当前不做权限细分，所有后台运营人员均可配置规则和查看变更记录
- 后续接入权限系统后按角色区分（CMS 管理员 / 只读运营）

#### CMS 配置内容的翻译接入

- CMS 配置的可翻译文本（Certified Authentic 标题/描述/详情、Condition 等级名/描述、成色详细信息展示名、Description 属性/Size Guide 展示名）均属**第二类内容**，由商详页 CMS 配置后台按多语言 v3.2 标准接入：**先建卡（4 张卡，归入聚合组 pdp）→ 注册字段 → 保存时写入翻译服务触发 AI 翻译**。建卡/注册/写入规范详见 §2.2.2，卡片与字段清单见 §1.7 B 段
- 保存写入以源语言（英文）录入，译文由翻译服务自动生成；翻译完成前前台按英文源文本展示（Fallback，见 §2.2.4）
- 翻译内部流程（AI 翻译调用、过期检测、术语匹配等）不在本文档定义，详见多语言模块 PRD v3.2

---

### 2.4 Header 导航栏

**功能描述**

页面顶部固定导航栏，提供品牌 Logo、品类导航、语言/货币切换、账户/搜索/收藏/购物车入口。APP 端另有分享按钮。

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

**APP 端分享按钮**

- APP 端顶部导航栏包含分享按钮，点击唤起 Share To 底部弹层
- PC 端无分享功能
- 分享弹层的渠道列表、分享内容组装、链接追踪等详见 Share To PRD

**边界情况**

- 未登录时点击 Account 图标，跳转登录页
- 未登录时点击 Wishlist 图标，直接打开 Wishlist 页面，展示当前 Cookie 中的收藏数据（不引导登录）
- 未登录时点击购物车图标，直接打开购物车页面，展示当前 Cookie 中的加购数据（不引导登录）

**UI 关联**

- PC 端：Figma Looply-v1.0 → PDP-PC → Header
- APP 端：Figma Looply-v1.0 → PDP-APP → Header

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
- 品牌名和品类名可点击，本期统一跳转 www.looply.com（后续 Collection 聚合页上线后分别跳转品牌聚合页和商品列表页）
- 最后一段（商品标题）为当前页，不可点击

**边界情况**

- 品类层级 > 3 层时，只展示最后 3 级，首段以 "..." 替代
- 商品名过长时文本自然换行，不截断

**UI 关联**

- PC 端：Figma Looply-v1.0 → PDP-PC → Breadcrumb
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
| 收藏按钮状态 | 收藏模块 | 已登录：调用收藏模块查询接口，判断当前用户是否已收藏该 listing；未登录：从 Cookie 读取本地收藏状态 |
| 收藏人数 | 收藏模块 | 调用收藏模块收藏计数接口。有收藏时展示（如 "12 people wishlisted"），无收藏时不展示 |

**展示规则**

- 主图和缩略图的显示尺寸以 Figma 设计稿为准，图片 URL 按实际渲染尺寸请求对应分辨率
- 点击主图进入 Lightbox 全屏查看模式（详见 2.16）
- 收藏按钮点击切换收藏/取消收藏状态。已登录时调用收藏模块接口；未登录时存入 Cookie，不触发登录流程（登录后自动合并 Cookie 收藏到账号）

**边界情况**

- 仅 1 张图：隐藏缩略图行和翻页控件
- 图片加载失败：显示灰色占位图 + 品牌 Logo 水印
- PC 端图片数量 > 6：缩略图区域自动换行为两行
- APP 端图片数量 > 10：缩略图区域可水平滚动

**UI 关联**

- PC 端：Figma Looply-v1.0 → PDP-PC → Gallery
- APP 端：Figma Looply-v1.0 → PDP-APP → Gallery

---

### 2.7 商品信息区（品牌 / 标题 / 价格 / Tax）

**功能描述**

展示商品核心信息：品牌名、商品标题、价格（含促销价和划线价）、Tax 提示。价格体系（币种转换、促销价计算）在本节统一定义，其他模块引用。

**数据来源与取值规则**

| 页面元素 | 数据源 | 取值逻辑 |
|---------|-------|---------|
| 品牌名 | `brand.brand_name_en` | 链路：`spu.series_id` → `series.brand_id` → `brand`。通常禁译（术语表标记）。点击跳转（本期写死 www.looply.com，后续 Collection 上线后跳品牌聚合页） |
| 商品标题 | `listing.listing_title` > `product.title` | 展示标题优先；`product.title` 为空时系统自动拼接：`{关键属性值} {spu_name}`。走翻译 |
| 现价 | `listing.listing_price` 或 `promotion_price` | 有促销价时展示促销价，无促销价时展示 listing_price |
| 划线价 | `listing.compare_at_price` 或 `listing.listing_price` | 优先级：①有促销价时划线价=listing_price ②无促销但有 compare_at_price 且 > listing_price 时划线价=compare_at_price ③均无则不展示 |
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
- 汇率查询失败时：回退到定价货币原价展示，价格下方附提示 "Price shown in [定价货币]"（走翻译，`resource_type='ui'`）
- 结算货币：用户下单时使用当前看到的展示货币，不回退到定价货币

**促销价展示逻辑**

促销价由促销模块计算输出，不存储在 listing 表中。

| 场景 | 现价 | 划线价 | Save |
|------|------|-------|------|
| 有促销价（`promotion_price < listing_price`） | promotion_price | max(listing_price, compare_at_price)（删除线） | 划线价 - promotion_price |
| 无促销价，有 compare_at_price 且 > listing_price | listing_price | compare_at_price（删除线） | compare_at_price - listing_price |
| 无促销价，无 compare_at_price | listing_price | 不展示 | 不展示 |

> 注意：现价、划线价均需做币种转换 + 尾数适配后再计算 Save。Save = 转换后划线价 - 转换后现价，Save 本身不做尾数处理。

**展示规则**

- 品牌名：大写字母展示，点击跳转（本期写死 www.looply.com）
- 货币符号：取 `currency.currency_symbol`（如 "$"）
- 符号位置：取 `market_currency.symbol_position`（`before` = 前置如 `$12.99`，`after` = 后置如 `12.99€`），Market 级配置
- 小数位数：取 `currency.decimal_places`（如 USD=2 位，JPY=0 位）

**边界情况**

- 标题为空的三级兜底：`listing.listing_title` → `product.title` → 系统拼接 `{关键属性值} {spu_name}`

**UI 关联**

- PC 端：Figma Looply-v1.0 → PDP-PC → Product Info
- APP 端：Figma Looply-v1.0 → PDP-APP → Product Info

---

### 2.8 CTA 按钮

**功能描述**

核心转化模块，包含 Add to Cart 按钮和 Buy Now 按钮。PC 端 CTA 按钮在页面内独立展示，APP 端 CTA 按钮在 Sticky 底部购买栏中（常驻屏幕底部，替代 APP 底部 TabBar）。

#### 商品可售性判断

商详页按钮状态由 `listing_status` + 库存状态共同决定：

| listing_status | 库存状态 | 页面展示 |
|---|---|---|
| `active` | 有库存 | Add to Cart 可点击，正常购买 |
| `active` | 已预留 / 已售出 | Sold Out 灰色不可点击 |
| `off_shelf` | -- | 商品信息正常展示，CTA 区域显示"商品已下架"提示并禁用所有按钮 |

> listing_status 为两状态（active/off_shelf）。off_shelf 通过 off_shelf_reason 区分下架原因（manual/out_of_stock/blocked/item_invalid），商详页不区分下架原因，统一展示"商品已下架"。off_shelf 时页面级行为：Gallery、品牌/标题/价格、Condition、Description、Shipping & Returns 等信息模块**正常展示**（用户可浏览商品详情做参考），仅 CTA 按钮区域替换为"This item is no longer available"提示文案 + 按钮禁用灰态。推荐区和浏览历史正常展示（引导用户发现其他商品）。收藏按钮仍可操作。库存可售状态由库存服务统一维护，商详页调用库存服务可售库存查询接口，返回 `available_qty > 0` 即可售。

**数据来源与取值规则**

| 页面元素 | 数据源 | 取值逻辑 |
|---------|-------|---------|
| Add to Cart 按钮价格 | 同 2.7 现价 | 展示当前现价，做币种转换 |
| 按钮文案 | 翻译模块 | `resource_type='ui'`，如 `btn.add_to_cart`、`btn.buy_now` |
| Verified 标记（APP 端） | CMS 模板配置（2.9） | 当前模板的 Certified Authentic 模块已配置内容时，在 Sticky 底部栏显示绿色 "✓ Verified" 认证标记 |

**展示规则**

- Buy Now：点击直接进入结算流程（跳过购物车，直接结算当前商品），未登录用户同样可点击，登录判断由结算流程处理（非商详页职责）
- APP 端 Sticky 底部栏：三栏布局（左侧收藏 | Add to Cart | Buy Now），仅展示现价，不重复展示划线价和 Save（上方信息区已有）
- APP 端商详页隐藏底部 TabBar，由 Sticky 底部购买栏替代

#### Add to Cart 行为

| 场景 | 行为 |
|------|------|
| 正常加购（可售库存 > 购物车中该商品数量） | 飞入动效（商品图飞向购物车 icon）+ 购物车角标数量 +1 + 按钮文字变 "Added ✓"（PC 2 秒 / APP 1.5 秒后恢复） |
| 超出库存（可售库存 ≤ 购物车中该商品数量） | toast "Maximum quantity reached"，不加购 |

> 二手商品可售库存通常为 1，首次加购正常飞入，重复点击即命中库存上限提示。规则通用，不区分商品类型。
>
> **按钮防重复点击**：从飞入动效开始到 "Added ✓" 状态恢复期间，Add to Cart 按钮为禁用态（不可点击），防止重复加购触发错误提示。

#### 操作时 toast 文案

| 场景 | toast 文案 |
|------|-----------|
| 加购超出库存 | "Maximum quantity reached" |
| Buy Now 时已售罄 | "This item is no longer available" |
| 进入结算前价格变化 | "Price has been updated, please review before checkout" |

> toast 文案均走翻译模块（`resource_type='ui'`），上表为英文原文。

**边界情况**

- Sold Out 时：Add to Cart 和 Buy Now 均禁用，变灰色。Gallery 区收藏按钮仍可操作、收藏人数仍展示（用户可收藏售罄商品）

**UI 关联**

- PC 端：Figma Looply-v1.0 → PDP-PC → CTA
- APP 端：Figma Looply-v1.0 → PDP-APP → Sticky Bottom Bar

---

### 2.9 Certified Authentic 鉴定认证

**功能描述**

展示平台对商品认证、成色检查和售后保障的信任承诺，帮助用户建立购买信心。内容由 CMS 后台按 PDP 模板级别配置，同一模板下所有类目的商品共享同一套鉴定认证声明。

**数据来源与取值规则**

| 页面元素 | 数据源 | 取值逻辑 |
|---------|-------|---------|
| 标题 | CMS 模板配置 | 如 "Confidence in Every Find"。走翻译（`resource_type='pdp_template'`） |
| 描述文案 | CMS 模板配置 | 简要说明（如 "Each luxury piece is carefully reviewed for authenticity, condition, and listing accuracy."）。走翻译 |
| 详细说明 | CMS 模板配置 | 点击后展示的完整内容（多段落，如认证流程、成色分级标准、售后保障条款等）。走翻译 |

**CMS 配置**

通过 CMS 后台的 PDP 模板 → Certified Authentic 模块配置：

- **模板级配置**：同一模板下所有关联类目共享同一套 Certified Authentic 内容
- **三个字段**：标题（`title`，必填）、描述文案（`desc`，必填）、详细说明（`detail`，富文本编辑器，选填）。保存时校验标题和描述非空，为空时提示错误阻止保存
- **页面内直接编辑**：三个字段在模板配置页面内直接编辑，无需打开弹窗。详细说明字段使用富文本编辑器，支持加粗、斜体、列表、链接等格式
- **模块开关**：关闭后前台不展示 Certified Authentic 区域
- **不同模板可配不同内容**：如 Luxury PDP 模板强调认证鉴定，Electronics PDP 模板强调功能测试

**展示规则**

- 以卡片形式展示，包含标题 + 描述文案 + 可点击的箭头/入口
- 点击卡片或箭头打开详细说明：PC 端弹窗展示，APP 端 Bottom Sheet（半层弹窗）展示
- 位于 CTA 区域下方、Condition 折叠区上方

**边界情况**

- 当前商品所属类目未关联任何 PDP 模板：Certified Authentic 区域不展示
- 模板的 Certified Authentic 模块开关关闭：不展示
- 标题或描述为空：不展示（三个字段中标题和描述为必填）

**UI 关联**

- PC 端：Figma Looply-v1.0 → PDP-PC → Certified Authentic
- APP 端：Figma Looply-v1.0 → PDP-APP → Certified Authentic

---

### 2.10 Condition 成色折叠区

**功能描述**

展示二手商品的成色信息，是 looply 作为二手平台的核心差异化模块。包含成色等级（含分段进度条）、Condition Guide 入口、鉴定认证徽章、成色描述、外观描述、配件信息、补充描述。

**数据来源与取值规则**

| 页面元素 | 数据源 | 取值逻辑 |
|---------|-------|---------|
| Certified Authentic 徽章 | CMS 模板配置（2.9） | 当前模板的 Certified Authentic 模块已配置内容时展示绿色盾牌 + "Certified Authentic"。点击打开详情弹层（详见 2.9）。模块未配置内容或开关关闭时隐藏 |
| 成色等级 | `product_inspection.grade` | 商品系统固定枚举值（如 `Like New` / `Excellent` / `Very Good` / `Good` / `Fair`），商品录入时选取，走翻译（`resource_type='enum'`） |
| 成色等级进度条 | CMS 模板配置 + `product_inspection.grade` | 分段进度条展示模板配置的展示等级，高亮当前商品等级（详见下方「分段进度条」） |
| Condition Guide | CMS 模板配置 | 展示模板定义的所有等级名称和描述（详见下方「Condition Guide」） |
| 成色详细信息 | CMS 类目级配置 + `product_inspection` 字段 | 展示哪些字段、展示名、排序由 CMS 按类目配置（同 Description 模式）。数据值取自 `product_inspection` 对应字段，走翻译。可配置的数据源字段：`condition_summary`（成色概述）、`appearance_desc`（外观状况）、`accessories_info`（配件情况）、`supplement_notes`（补充说明）。有值时展示，为空时该行隐藏 |

#### 成色等级体系

`product_inspection.grade` 是商品系统的固定枚举值，商品录入时由运营从系统预定义的等级中选取。CMS 模板的等级配置**仅控制前台展示**（进度条分段、Condition Guide 内容），不影响商品录入流程。

**商品系统等级枚举（固定）**

| 等级名称 | 含义 |
|---------|------|
| Like New | 几乎全新，无可见使用痕迹，所有原始组件完好 |
| Excellent | 极轻微使用痕迹，远距离不可见 |
| Very Good | 轻微使用痕迹，近距离可见 |
| Good | 中等使用痕迹 |
| Fair | 明显使用痕迹，仍然结构完好可用 |

> CMS 模板配置的等级集合决定前台进度条展示哪些段、Condition Guide 展示哪些等级说明。商品的 `grade` 值不受 CMS 模板影响（由商品系统固定枚举控制）。如果商品的 grade 在当前模板的等级集合中匹配不上，进度条和等级名称静默隐藏。不同模板可配置不同的展示等级集合（如 Electronics PDP 可配置 Mint / Excellent / Good / Fair 四级）。

#### 分段进度条

- 进度条分为等宽的 N 段（N = 模板定义的等级数量）
- 每段对应一个等级，从高到低依次排列（如 Like New → Excellent → Very Good → Good → Fair）
- 当前商品等级对应的段高亮为品牌色，其余段为浅色（具体色值以 Figma 设计稿为准）
- 每段下方显示等级名称标签，当前等级标签为品牌色，其余为灰色

#### Condition Guide

- 通过成色等级旁的信息图标（ⓘ）触发
- PC 端打开弹窗，APP 端打开 Bottom Sheet
- 展示当前模板定义的所有成色等级，每个等级包含名称和详细描述
- 等级按从高到低排列
- 数据来源：CMS 模板的 Condition 等级配置

#### CMS 配置

通过 CMS 后台的 PDP 模板 → Condition 模块配置：

- **成色等级配置（模板级）**：配置该模板前台展示的等级集合（等级名称 + 等级描述），仅控制进度条和 Condition Guide 的展示内容，不影响商品录入的 grade 枚举
- **等级数量灵活**：不同模板可配置不同数量的展示等级，最少 2 个（进度条至少需要 2 段才有对比意义），无上限约束
- **等级排序**：按配置顺序从高到低排列，排序即展示顺序
- **等级删除**：允许删除已被商品使用的等级。删除后，前台渲染时如果商品的 grade 在当前模板等级集合中匹配不上，进度条和等级名称不展示（静默隐藏），成色详细信息保留展示
- **成色详细信息配置（类目级）**：模板内按类目配置，定义前台展示哪些 `product_inspection` 字段、展示名和排序。与 Description 属性配置模式一致：
  - 每个类目一条规则，选择要展示的字段（`condition_summary` / `appearance_desc` / `accessories_info` / `supplement_notes`），同一类目规则内每个数据源字段最多选一次
  - 每个字段可自定义展示名（如珠宝类 appearance_desc → "Chain"，箱包类 → "Exterior"），展示名走翻译；展示名留空时前台只展示值
  - 拖拽调整字段排序
  - 新增规则时类目选择互斥（同 Description，已配置的类目置灰不可选）
  - 未配置规则的类目：成色详细信息区域不展示（仅保留进度条 + Condition Guide + 徽章）
- **模块开关**：关闭后前台不展示 Condition 折叠区的进度条和 Condition Guide（但成色详细信息仍展示，详见 2.3 模块开关说明）

**展示规则**

- 默认展开（核心二手差异信息，用户最关注）
- 展示顺序：成色等级（含进度条）+ Condition Guide 入口 → 徽章 → 成色详细信息（按 CMS 配置的字段顺序展示）
- 每个字段格式："展示名: 值"（展示名由 CMS 类目级配置，值取自 product_inspection 对应字段）。展示名为空时前台只展示值，不带冒号（如 condition_summary 通常不设展示名，直接展示成色概述文案）
- APP 端每个字段独立截断，超过 3 行时截断并渐隐，点击 "Read more" 展开该段，展开后变为 "Read less" 可收起
- PC 端所有字段全文展示，不截断
- Certified Authentic 徽章：模板未配置 Certified Authentic 内容或模块开关关闭时隐藏（详见 2.9）

**边界情况**

- CMS 配置的某字段在 product_inspection 中值为空时：该行整体隐藏（含展示名），不留空白
- 当前类目未配置成色详细信息规则：整个成色详细信息区域隐藏，仅保留进度条 + Condition Guide + 徽章
- CMS 配置的所有字段在 product_inspection 中均为空时：成色详细信息区域整体隐藏，仅保留进度条 + Condition Guide + 徽章
- APP 端某段文案不足 3 行时：不截断，不显示 Read more 按钮
- 当前商品所属类目未关联模板：不展示进度条和 Condition Guide，仅展示基本成色文本信息

**UI 关联**

- PC 端：Figma Looply-v1.0 → PDP-PC → Condition + Condition Guide Modal
- APP 端：Figma Looply-v1.0 → PDP-APP → Condition

---

### 2.11 Description 描述折叠区

**功能描述**

展示商品的属性信息（如材质、颜色、尺寸等）和商品描述文案，由 CMS 配置驱动展示哪些属性和排序。包含 Listing 编号、Size Guide 入口和商品描述段落。

**数据来源与取值规则**

| 页面元素 | 数据源 | 取值逻辑 |
|---------|-------|---------|
| item # | `listing.listing_id` | Listing 编号，对外展示，不翻译 |
| 描述属性（如 Material、Length） | `spu_attribute_value` + `attribute_def` | 通过 `standard_sku` → `spu` → `spu_attribute_value` 取值。属性名取值见下方「属性名取值逻辑」，属性值走翻译 |
| 销售属性（如 Color、Size） | `standard_sku_attribute` | 通过 `standard_sku_id` 查询。属性名取值见下方「属性名取值逻辑」，属性值走翻译 |
| 商品描述文案 | `listing.listing_description` | 渠道描述，走翻译。展示在属性表下方 |

**属性展示筛选流程**

商品系统维护了完整的属性集，商详页不全量展示，经过以下筛选：

1. **查询展示范围**：通过 CMS 配置，根据当前商品的 `category_id` 查询该类目的属性展示配置（模板内按类目配置，详见 2.3）
2. **取值**：描述属性从 `spu_attribute_value` 取值，销售属性从 `standard_sku_attribute` 取值
3. **过滤空值**：属性值为空的行不展示
4. **排序**：按 CMS 配置的排序顺序展示
5. **属性名取值**：取 CMS 配置中运营定义的前台展示名（`display_name`），展示名进翻译模块输出多语言版本。展示名为空时，前台不展示属性名 Label，仅展示属性值
6. **属性值翻译**：属性值走翻译模块

**Size Guide（尺寸测量方法）**

点击打开尺寸标注弹窗（PC 端弹窗 / APP 端 Bottom Sheet），展示逻辑分两种模式：

- **有 SVG 模板时（Template Mode）**：后台按末级类目配置一组 SVG 测量示意图（每套对应一种形状比例，预留 `data-slot` 标记位），前端根据当前商品的实测尺寸（长宽高比值）自动匹配最接近的模板 → 用实测数据填充 `data-slot` 占位符 → 拼接单位后渲染标注图
- **无模板时（Fallback）**：退化为纯文字列表，展示尺寸类属性（如 Length: 12.2 in, Width: 5.5 in）

> **度量单位（本期策略）**：本期属性值按录入值原样展示，不做运行时单位转换。商品录入时按目标市场习惯录入（如美国市场录 inches）。后续扩展欧洲等市场时再设计按 Market 偏好自动换算的方案。

**CMS 配置**

通过 CMS 后台的 PDP 模板 → Description 模块，按类目配置：

- **类目级配置**：每个类目一条规则，定义前台展示名 + 绑定数据源属性 + 拖拽调整排序
- **Size Guide**：固定模块，选择类目后自动带入属性列表，始终保留不可删除。运营可编辑前台展示名（默认 "Size Guide"）、拖拽调整在属性列表中的位置、通过开关控制显示/隐藏。数据源为尺寸测量方法（类目级多套 SVG 模板 + 尺寸比值自动匹配 + 商品实测数据），不可更换。前台渲染时如果该商品无尺寸测量数据或 Size Guide 已关闭，链接不展示
- **模块开关**：关闭后前台不展示 Description 区域

**展示规则**

- 默认展开
- 属性区：每行一条属性，格式 "Label: Value"
- 商品描述文案：展示在属性表下方，作为描述折叠区的一部分
- PC 端全文展示，不截断
- APP 端属性数量 > 8 行时截断，底部显示 "Show more attributes" 展开
- APP 端商品描述文案默认截断 2 行，末尾渐隐，点击 "Read more" 展开全文
- CMS 中配置了 Size Guide 但该商品无尺寸测量数据时：Size Guide 链接不展示（静默隐藏，不报错）

**边界情况**

- 属性值为空时：该行不展示
- 商品描述文案为空时：该段落区域隐藏，不留空白
- 当前类目未配置尺寸测量方法 SVG 模板，或商品实测尺寸无法匹配到任何模板：Size Guide 退化为文字列表
- 属性值带特殊字符：做 HTML 转义
- 当前类目未配置 Description 规则：整个 Description 折叠区隐藏
- APP 端商品描述文案不足 2 行：不截断，不显示 Read more 按钮

**UI 关联**

- PC 端：Figma Looply-v1.0 → PDP-PC → Description + Size Guide Modal
- APP 端：Figma Looply-v1.0 → PDP-APP → Description

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

- PC 端：Figma Looply-v1.0 → PDP-PC → Shipping & Returns
- APP 端：Figma Looply-v1.0 → PDP-APP → Shipping & Returns

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
| 划线价 | `listing.compare_at_price` 或 `listing.listing_price` | 同 2.7 划线价逻辑（促销→listing_price，无促销→compare_at_price），做币种转换 + 尾数适配 |
| Save | 划线价 - 现价 | 均经币种转换后计算，不做尾数处理 |
| 收藏数 | 收藏模块 | 调用收藏模块收藏计数接口，无收藏时不显示数字 |
| 收藏按钮状态 | 收藏模块 | 同 2.6 Gallery 收藏按钮 |

**展示规则**

- 点击整张卡片跳转对应商品的商详页
- 收藏按钮点击直接收藏/取消收藏（无需进入详情页），未登录时存入 Cookie（同 2.6 Gallery 收藏逻辑）
- 卡片标题超 2 行截断

**展示数量**

- 最大展示 50 条，推荐引擎返回超过 50 条时截断
- 最少 2 条才展示推荐区，不足 2 条时整个区域隐藏
- APP 端水平滑动浏览

**边界情况**

- 推荐数据为空或不足 2 条：整个区域隐藏
- PC 端推荐 < 6 张：隐藏 Next 按钮，卡片靠左对齐

**UI 关联**

- PC 端：Figma Looply-v1.0 → PDP-PC → You May Also Like
- APP 端：Figma Looply-v1.0 → PDP-APP → You May Also Like

---

### 2.14 Recently Viewed 浏览历史

**功能描述**

展示用户最近浏览过的商品，帮助用户回到之前看过的商品。

**数据来源与取值规则**

| 页面元素 | 数据源 | 取值逻辑 |
|---------|-------|---------|
| 浏览记录 | `user_view_history` | 已登录：按 `viewed_at` 倒序取最近 30 条；未登录：使用浏览器 localStorage 记录（最多保存 30 条，超出时淘汰最旧记录） |
| 卡片字段 | 同 2.13 商品卡片字段映射 | 通用卡片结构 |

**展示规则**

- 当前商品不在浏览历史中重复展示
- 交互行为同推荐区（卡片点击、收藏）

**边界情况**

- 无浏览历史：整个区域隐藏
- 浏览记录中的商品售罄（active + 无库存）：标记 "Sold Out" 标签，卡片仍可点击进入商详页
- 浏览记录中的商品已下架（off_shelf）：从列表移除

**UI 关联**

- PC 端：Figma Looply-v1.0 → PDP-PC → Recently Viewed
- APP 端：Figma Looply-v1.0 → PDP-APP → Recently Viewed

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

- PC 端：Figma Looply-v1.0 → PDP-PC → Footer
- APP 端：Figma Looply-v1.0 → PDP-APP → Footer

---

### 2.16 Lightbox 灯箱

**功能描述**

Gallery 主图点击后的全屏图片查看器，支持左右切换浏览所有商品图片。

**数据来源与取值规则**

- 图片数据同 2.6 Gallery，使用高清 URL（尺寸以 Figma 设计稿为准）
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

- PC 端：Figma Looply-v1.0 → PDP-PC → Lightbox
- APP 端：Figma Looply-v1.0 → PDP-APP → Gallery（Lightbox 部分）

---

## 三、依赖与风险

### 上下游系统依赖

| 依赖模块 | 提供内容 | 当前状态 | 风险 |
|---------|---------|---------|------|
| 商品域 | 商品基础数据（listing、product、SPU、属性） | 已有 | -- |
| Market 模块 | 语言/货币配置（含状态过滤、符号位置、RTL） | 已有 | -- |
| 汇率管理模块 | 平台汇率（已含点差）查询接口 | 已有 | -- |
| 商品定价（尾差规则） | 心理定价尾数策略（.99/.95/整十等） | 已设计（商品系统 PRD 2.8.1） | -- |
| 多语言模块 v3.2（建卡+聚合+storage_mode） | translation_resource 建卡（migration）、resource_group 页面聚合、translation_domain 域元数据、translatable_field_config 字段注册、storage_mode 机制、翻译服务查询+写入接口、Fallback、术语表禁译、静态文案后台查改+语言包同步 | v3.2 立项，随 ER v2.4 / 原型 v13 交付 | **硬前置**：三项能力（建卡 / 页面聚合 / storage_mode）须先于商详页多语言功能上线，否则 §1.7 聚合组、§2.2 新建卡片无法落地。第二类 CMS 建卡/注册/写入为商详页自身交付范围，只依赖该平台能力 |
| 商品系统（第三类译文） | 商品域各卡片（listing/product/spu/brand/category/attribute/attribute_option/enum grade）的建卡与译文写入 | 部分待对接 | 商详页依赖其卡片 resourceType 稳定作为读取契约，须待商品模块卡片标识固化后核对 §2.2.1 |
| CMS 系统 | PDP 模板管理、模块配置（Certified Authentic / Condition / Description） | 原型 v3 已出 | 需开发实现；CMS 域新建等级展示配置表（商品系统 grade 枚举不变） |
| 促销模块 | 促销价计算 | 待设计 | 促销价计算逻辑未定义，当前商详页按"无促销价"展示 |
| 收藏模块 | 收藏状态查询、收藏计数 | 待设计 | 收藏模块未设计，需对外提供查询接口 |
| 用户域 | 浏览历史 | 待设计 | `user_view_history` 实体未设计 |
| 库存模块 | 商品可售状态 | 已有 | -- |
| 推荐引擎 | 推荐商品列表 | 待设计 | 推荐算法和输出格式未定义 |
| 搜索服务 | Header 搜索功能 | 待设计 | 独立模块 |
| 前台类目 | Header 导航链接 | 待设计 | 本期跳转地址写死 |
| 购物车/订单域 | Cart 角标数量、Add to Cart / Buy Now 接口 | 设计中 | 购物车有 ER 图，无 PRD |
| 配送模块 | Shipping & Returns 内容（后续 CMS 化） | 待设计 | 本期前端固定文案，后续配送模块就绪后升级 |
| 营销模块 | Newsletter 订阅 | 待设计 | Footer 邮箱订阅功能 |
| Share To | APP 端分享功能 | 已有（其他同事负责） | 详见 Share To PRD |

### 风险项

| 风险 | 影响 | 应对 |
|------|------|------|
| Condition 等级展示配置 | CMS 域需新建等级展示配置表（模板 → 展示等级名称 + 描述 + 排序），商品系统 `product_inspection.grade` 固定枚举不变，无迁移风险 | 仅 CMS 域新增，不影响商品录入 |
| 多语言 v3.2 能力未按期上线 | 建卡/聚合/storage_mode 缺失，商详第一、二类无法落地 | 列为商详多语言上线硬前置；上线前与多语言模块确认 v3.2 进度，未就绪则商详多语言顺延 |
| 聚合成员归属/排序靠 config 配错 | 聚合卡成员缺失或子导航顺序乱 | 上线前核对 group=pdp 的 5 个成员清单 + sort_order（§1.7 B 段） |
| 第三类 resourceType 未与商品模块对齐 | 商详读取时卡片标识对不上、取不到译文 | 商品模块卡片标识固化后核对 §2.2.1；联调阶段逐项验证 `(resourceType, resourceId, fieldName)` 可查得译文 |
| 商详 CMS 建卡/字段注册遗漏 | CMS 保存时源文写入被拒 | 上线前逐项核对建卡清单 + 注册清单 + 聚合声明（§2.2.2），作为上线 checklist |
| 收藏模块未设计 | 收藏状态和收藏人数无法展示 | 收藏按钮和人数需等收藏模块就绪后接入 |
| 浏览历史实体未设计 | 已登录用户浏览历史无法持久化 | 先用 localStorage 兜底 |
| 促销模块未设计 | 所有商品仅展示 listing_price，无促销价 | 价格展示逻辑已预留促销价入口，模块就绪后无需改动商详页 |

---

## 四、版本规划

### 当前版本（MVP）

- 商详页所有模块的展示逻辑（含 Certified Authentic、Condition 进度条 / Condition Guide）
- CMS 后台配置（PDP 模板管理、Certified Authentic / Condition / Description 三模块配置）
- 币种转换（汇率换算 + 尾差规则，详见商品系统 PRD 2.8.1）
- 多语言接入（按多语言 v3.2 标准）：静态文案语言包落地 + 后台可查改；第二类 4 类 CMS 内容建卡 + 字段注册 + CMS 保存写入触发翻译；第三类读取商品域译文；声明"商详页"聚合组（pdp，5 成员）；Fallback；RTL；品牌名禁译词导入

### 后续迭代方向

| 方向 | 说明 |
|------|------|
| 促销价展示 | 促销模块就绪后接入商详页 |
| 收藏功能 | 收藏模块就绪后接入 |
| 前台类目导航 | 前台类目模块就绪后替换写死链接 |
| 推荐引擎接入 | 推荐算法就绪后替换推荐区数据源 |
| Shipping & Returns CMS 化 | 配送模块就绪后，Shipping 文案从写死升级为 CMS 配置，支持按 Market 差异化 |
| 相似商品引导卡 | APP 设计稿中有"Want to find more similar products?"引导卡（售罄/推荐不足时展示，点击跳转相似商品列表页并自动带入筛选条件），本期不做，后续视推荐引擎能力决定 |
| 多语言卡片/分组运营自助编辑 | 商详聚合组成员、排序由运营在多语言后台自助编辑（本期走 migration/config），待多语言运营编辑控制台上线后单独立项 |

---

## 五、附录

### 5.1 设计稿索引

| 模块 | PC 端设计稿 | APP 端设计稿 |
|------|-----------|------------|
| 整体页面 | [Figma Looply-v1.0 PDP-PC](https://www.figma.com/design/rLK7XCdVvYqEHQHd7WjOkk/Looply-v1.0?node-id=454-5904) | [Figma Looply-v1.0 PDP-APP](https://www.figma.com/design/rLK7XCdVvYqEHQHd7WjOkk/Looply-v1.0?node-id=452-4153) |
| CMS 后台 | looply-商详页CMS配置后台原型-v3-antd.html | -- |

### 5.2 PC / APP 端差异对照表

以下为两端允许的差异，交互说明各自维护具体细节：

| 模块 | PC 端 | APP 端 |
|------|------|--------|
| 面包屑 | 有 | 无 |
| Gallery 切换方式 | 鼠标悬停缩放 + 点击缩略图 | 左右滑动 |
| 缩略图选中样式 | 深色边框 + 透明度 0.7→1 | 紫色边框 + 透明度 0.6→1 |
| CTA 按钮位置 | 页面内独立按钮 | Sticky 底部购买栏 |
| Certified Authentic 详细说明 | 弹窗展示 | Bottom Sheet 展示 |
| Condition Guide | 弹窗展示 | Bottom Sheet 展示 |
| Condition 成色区文本 | 全文展示 | 选填字段每段独立截断 3 行 + Read more |
| Description 属性截断 | 不截断 | > 8 行截断 + Show more |
| Description 商品描述 | 全文展示 | 2 行截断 + Read more |
| Size Guide | 弹窗展示 | Bottom Sheet 展示 |
| Shipping & Returns 默认状态 | 默认展开 | 默认折叠 |
| 推荐区导航 | Carousel 左右箭头 | 水平滑动 |
| Lightbox 操作 | 键盘导航（Escape / 箭头） | 手势（滑动 / 双指缩放） |
| 分享按钮 | 无 | 有（Header 右上角分享图标，点击打开分享半层，详见 Share To PRD） |
| Add to Cart 反馈 | 文字变 "Added ✓"，2 秒恢复 | 文字变 "Added ✓" + 浅绿色背景，1.5 秒恢复 |
| Add to Cart 飞入动效 | 商品图飞向右上角购物车图标 + 角标 +1 | 商品图飞向 Header 右上角购物车图标 + 角标 +1 |
| Footer 导航展示 | 链接列表直接展示 | 手风琴展开 |
| Footer 免责声明 | 有 | 无 |
| Sticky 底部购买栏 | 无 | 有（详见 2.8 APP Sticky 部分） |

### 5.3 待补充项汇总

| 项目 | 类型 | 所属域 | 说明 |
|------|------|-------|------|
| PDP 模板 ER 设计 | 新实体 | CMS 域 | 模板表、模板-类目关联表、Certified Authentic 配置表、Condition 等级展示配置表（`product_inspection.grade` 固定枚举不变，无需迁移） |
| 收藏模块 | 模块设计 | 独立模块 | 对外提供收藏状态查询、收藏计数、收藏/取消收藏等接口 |
| `user_view_history` | 新实体 | 用户域 | user_id + listing_id + viewed_at |
| 前台类目模块 | 新模块 | 独立模块 | Header 导航栏数据源 |
| 推荐引擎 | 模块设计 | 独立模块 | 推荐算法和输出格式 |
| Shipping & Returns 内容 | CMS 配置 | 内容域 | 按 Market 区分政策内容 |

### 5.4 关联文档索引

| 文档 | 位置 | 说明 |
|------|------|------|
| PC 端设计稿 | [Figma Looply-v1.0 PDP-PC](https://www.figma.com/design/rLK7XCdVvYqEHQHd7WjOkk/Looply-v1.0?node-id=454-5904) | PC 端商详页设计稿 |
| APP 端设计稿 | [Figma Looply-v1.0 PDP-APP](https://www.figma.com/design/rLK7XCdVvYqEHQHd7WjOkk/Looply-v1.0?node-id=452-4153) | APP 端商详页设计稿 |
| CMS 后台原型 | `~/Desktop/海外业务/商详/原型/looply-商详页CMS配置后台原型-v3-antd.html` | PDP 模板管理 + Certified Authentic / Condition / Description 三模块后台配置（antd 版）。V1.7 未改，沿用 V1.1 |
| 多语言模块 PRD v3.2 | `~/Desktop/海外业务/多语言/PRD/looply-多语言模块-PRD-v3.2.md` | 建卡 + 页面聚合 + storage_mode 能力、翻译服务集成规范（§4.6 Fallback） |
| 多语言接入规范（产品版）v3.2 | `~/Desktop/海外业务/多语言/looply-多语言接入规范-产品版-v3.2.md` | "动态套动态"拆 resource_type + resource_group 聚合、静态文案后台可查改、§1.7 三段写法 |
| 多语言管理后台原型 v13 | 多语言目录 | 商详页聚合卡 + 5 分组子导航、Key 管理只读 |
| 商详页多语言接入 PRD 系列（已废弃） | `~/Desktop/海外业务/商详/PRD/looply-商详页多语言接入-PRD-v1.0~v1.3.md` | 已废弃（2026-07-23），内容并入本 PRD §1.7 / §2.2 / §2.3，不再维护 |
| 数据来源与取值逻辑 V1.3 | `~/Desktop/海外业务/商详/looply-商详页-数据来源与取值逻辑.html` | 历史参考（已被本 PRD 替代） |
| 数据来源与实现逻辑 V2.0 | `~/Desktop/海外业务/商详/looply-商详页-数据来源与实现逻辑-V2.0.md` | 历史参考（已被本 PRD 替代） |

---

> 版本变更记录已独立存放：`~/Desktop/海外业务/商详/looply-商详页系统-变更日志.md`
