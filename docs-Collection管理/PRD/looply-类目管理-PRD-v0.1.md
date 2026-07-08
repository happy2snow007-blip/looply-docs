# Looply 海外业务 · Collection 管理模块 PRD

**版本**：v0.1  
**创建日期**：2026-06-04  
**目标读者**：研发团队（前端、后端、测试）  
**产品负责人**：Looply 产品团队  
**状态**：待评审

---

## 目录

- [一、概述](#一概述)
  - [1.1 背景与目标](#11-背景与目标)
  - [1.2 不做什么](#12-不做什么)
  - [1.3 用户角色](#13-用户角色)
  - [1.4 核心场景](#14-核心场景)
  - [1.5 全局页面流转](#15-全局页面流转)
  - [1.6 术语说明](#16-术语说明)
  - [1.7 多语言 / 多国家策略](#17-多语言--多国家策略)
- [二、需求详细描述](#二需求详细描述)
  - [2.1 公共组件：条件构建器](#21-公共组件条件构建器)
  - [2.2 后台管理端：Collection 列表页](#22-后台管理端collection-列表页)
  - [2.3 后台管理端：新建 Collection（向导流程）](#23-后台管理端新建-collection向导流程)
  - [2.4 后台管理端：Collection 详情页（编辑向导）](#24-后台管理端collection-详情页编辑向导)
  - [2.5 后台管理端：筛选维度管理](#25-后台管理端筛选维度管理)
  - [2.6 前台 C 端：Collection 页（类目浏览页）](#26-前台-c-端collection-页类目浏览页)
  - [2.7 机制：Meta SEO 降级链](#27-机制meta-seo-降级链)
  - [2.8 机制：商品准入与状态同步](#28-机制商品准入与状态同步)
  - [2.9 机制：前台收藏（Favorites）](#29-机制前台收藏favorites)
  - [2.10 机制：品牌驱动 Collection（品牌页）](#210-机制品牌驱动-collection品牌页)
- [三、依赖与风险](#三依赖与风险)
- [四、版本规划](#四版本规划)
- [五、数据与埋点](#五数据与埋点)
- [六、附录](#六附录)

---

## 一、概述

### 1.1 背景与目标

Looply 是转转国际业务旗下面向美国市场的大牌二手奢侈品电商平台，切入品类为二手奢侈品（包袋、首饰、配饰）。

**当前问题**：商品系统（PRD V0.8）已完成后台类目（backend_category）和属性体系的建设，但后台类目是面向数据管理的内部分类，无法直接作为消费者的浏览导航入口。缺乏前台商品分组和展示能力，消费者无法按品类浏览商品。

**本模块目标**：
- 搭建前台商品分组系统（Collection），让运营可以灵活创建、管理商品展示分组
- 支持两种选品模式（自动规则选品 / 手动精选），覆盖绝大多数运营场景
- 提供筛选维度管理能力，让每个 Collection 页面有合理的筛选过滤能力
- 为消费者提供流畅的前台分类浏览体验（PC 端 + 移动端）

**设计原则**：
- 前后台完全解耦：Collection 是展示分组，不干预商品自身的上下架状态
- 扁平结构：Collection 无层级嵌套（参考 Shopify 模式），导航层级由独立 Navigation 模块承载
- 商品粒度为 listing 级别：每件实物商品（listing）独立展示，不按 SPU 聚合
- 零 AI 依赖（MVP）：所有功能纯配置驱动

### 1.2 不做什么

| 范围 | 说明 |
|---|---|
| 前台导航菜单管理 | Navigation 模块独立建设，本模块不包含 |
| 广告 Feed 分类映射 | Google Shopping 等平台的 Feed 分类不纳入 Collection 管理，独立模块处理 |
| 前后台类目映射关系 | 商品系统 PRD V0.3 规划，不在本模块 |
| 多渠道可见性控制 | MVP 只有美国线上官网一个渠道，不做多渠道渠道控制 |
| AI 动态推荐规则 | MVP 不依赖 AI，所有选品规则纯配置 |
| 混合选品模式（规则+手动置顶） | 后续增强，MVP 两种模式互斥 |
| 收藏夹的降价/到货通知 | 依赖通知体系，MVP 不做 |
| 品牌优先独立导航（/brands/{slug}） | 独立品牌路由后续规划；本次 MVP 以「品牌驱动 Collection」复用 /collections/ 实现品牌页，见 §2.10 |

### 1.3 用户角色

| 角色 | 描述 | 主要操作 |
|---|---|---|
| 运营 | Looply 内部运营人员，负责商品分组和日常选品 | 创建/编辑 Collection、配置选品规则、管理筛选器 |
| 超级管理员 | 系统管理员 | 管理筛选维度池、配置系统级 Collection（All Products） |
| 消费者（C端用户） | 访问 Looply 的美国用户 | 浏览 Collection 页、筛选商品、收藏商品 |
| 匿名用户 | 未登录的访客 | 浏览 Collection 页、筛选商品、收藏商品（存本地） |

### 1.4 核心场景

**后台管理端：**
1. 运营创建新的季节性 Collection（如 Holiday Gifts），设置自动选品规则，配置筛选维度
2. 运营创建编辑精选 Collection，手动挑选商品，调整商品排列顺序
3. 运营临时下架某个 Collection（活动结束），保留配置，下次活动前一键恢复
4. 超级管理员创建全局筛选维度（如 Color 维度关联 color + bag_color 两个属性），供各 Collection 引用
5. 运营为 All Products Collection 配置筛选维度和 SEO 信息

**前台 C 端：**
1. 消费者通过导航进入某个 Collection 页，浏览商品，按品牌/价格/成色筛选
2. 消费者收藏感兴趣的商品（未登录时也可收藏）
3. 消费者切换排序方式（Price: Low to High），筛选后发现无结果，使用 Clear Filters 重置

### 1.5 全局页面流转

```
【后台管理端】
Collection 列表页
  ├─→ 新建 Collection（Step 1 基础信息 → Step 2 商品来源 → Step 3 筛选配置）
  └─→ Collection 详情页（Step 1 基础信息 → Step 2 商品来源 → Step 3 筛选配置）
        └─→ [手动选品模式] 侧滑抽屉：选品器

筛选维度管理页
  └─→ 侧滑面板：新建/编辑筛选维度

【前台 C 端】
Collection 页（有商品）
  ├─→ 商品详情页（/p/{product-slug}）
  └─→ Collection 页（筛选/排序状态，同一页内更新）

Collection 页（无结果状态）
  └─→ Collection 页（点击 Clear Filters 回到有商品状态）
```

### 1.6 术语说明

| 术语 | 说明 |
|---|---|
| Collection | 前台商品分组，Shopify 式扁平结构，无层级嵌套。即本模块核心管理对象 |
| backend_category | 后台类目，商品系统已有，用于属性作用域配置和数据管理，不面向消费者 |
| listing | 一件实物商品的销售记录，Collection 中商品的最小粒度 |
| filter_dimension | 筛选维度，封装了属性/品牌/价格等数据源，作为前台筛选器的配置层 |
| Quick Filters | 类目页顶部的快捷筛选 Chip，点击即应用预设筛选条件 |
| rule_config | 自动选品规则的 JSON 配置，支持嵌套条件分组（AND/OR） |
| Pin | 将某件商品固定到指定位置，商品下架后 pin 记录清除 |
| WYSIWYG | What You See Is What You Get，后台商品列表顺序与前端展示顺序完全一致 |
| source_type | Collection 的商品来源类型：rule（自动选品）/ manual（手动选品） |
| All Products | 系统级内置 Collection，覆盖所有 active listing，不可删除、不可关闭 |

### 1.7 多语言 / 多国家策略

| 项目 | 说明 |
|---|---|
| 前台语言 | 仅英语（en-US），MVP 不做多语言 |
| 后台语言 | 简体中文界面，Collection 名称字段支持 name_en（必填）和 name_zh（选填） |
| 货币 | 美元（USD），全平台统一 |
| 时区 | 后台显示 UTC+8（北京时间），前台显示 UTC-5/UTC-8（美东/美西），「最近N天」等时间条件以 UTC 计算 |
| 合规 | MVP 以美国用户为主，收藏功能使用 localStorage，无服务端数据采集，暂不涉及 GDPR |

---

## 二、需求详细描述

### 2.1 公共组件：条件构建器

**功能描述**

条件构建器是一个可嵌套的规则编辑器，用于：
1. 自动选品模式：定义 Collection 的商品准入条件
2. 手动选品模式：在选品器抽屉中用于筛选候选商品

支持 Magento 式嵌套分组逻辑（每个分组有独立的 AND/OR 开关，分组内可再嵌套子分组）。

**条件字段完整枚举**

| 字段名 | 字段来源 | 可用操作符 | 值输入控件 | 备注 |
|---|---|---|---|---|
| backend_category | backend_category 表 | 等于其中之一 / 不等于其中任一 | 树形多选弹出框 | 选择后台类目 |
| brand | brand 表 | 等于其中之一 / 不等于其中任一 | 搜索多选 | |
| series | series 表（关联 brand） | 等于其中之一 / 不等于其中任一 | 级联：先选品牌，再选系列 | 已选品牌时自动过滤系列选项 |
| price | listing.listing_price | 等于 / 大于 / 小于 / 介于 | 数值输入框 / 双值输入 | 介于时显示最小值+最大值两个输入框 |
| condition | used_item.grade | 等于其中之一 / 不等于其中任一 | 枚举多选（固定3个值） | 枚举值：A（几乎全新）/ B（轻微使用痕迹）/ C（明显使用痕迹）；以商品系统 PRD v0.8 为准 |
| listing_date | listing.listed_at | 最近N天 / 介于 | 「最近N天」→ 数字输入+「天」后缀；「介于」→ 日期选择器 | 「最近N天」为动态滚动窗口，每日凌晨重新评估 |
| stock_status | listing.stock_status | 等于其中之一 / 不等于其中任一 | 枚举多选 | 枚举值：在库 / 在途 / 在售 / 已售 |
| tag | 商品标签系统（预留） | 包含其中之一 / 不包含其中任一 | 标签多选输入 | 字段为多值，用「包含」系列操作符 |
| title | listing.title / spu.name | 包含 / 不包含 | 文本输入框 | 关键词模糊匹配 |
| custom_attribute | attribute_def.* | 动态（取决于属性输入控件类型） | 二级选择：先选属性，再选操作符和值 | 见下方自定义属性说明 |

**操作符体系枚举**

| 操作符组 | 操作符 | 适用字段类型 | 语义说明 |
|---|---|---|---|
| 单值枚举组 | 等于其中之一 | 单值枚举字段（brand、series、condition、stock_status、backend_category、single_select属性） | 商品的该字段值 = 选项中的任意一个（OR） |
| 单值枚举组 | 不等于其中任一 | 同上 | 商品的该字段值不等于选项中的任何一个 |
| 多值字段组 | 包含其中之一 | 多值字段（tag、multi_select属性） | 商品的值集合中，至少有一个命中选项（交集非空） |
| 多值字段组 | 不包含其中任一 | 同上 | 商品的值集合中，没有任何一个命中选项（交集为空） |
| 数值组 | 等于 / 大于 / 小于 / 介于 | price、number_input属性 | 标准数值比较 |
| 文本组 | 包含 / 不包含 | title、text_input属性 | 关键词子串匹配 |
| 时间组 | 最近N天 | listing_date | 动态滚动窗口 |
| 时间组 | 介于 | listing_date | 固定日期区间 |

**自定义属性（custom_attribute）二级交互**

- 第一级：从当前已关联后台类目的属性池中选择属性（如 bag_size、color、material）
- 第二级：系统根据属性输入控件类型（input_type）自动切换可用操作符和值输入控件：
  - single_select → 等于其中之一 / 不等于其中任一 + 枚举多选
  - multi_select → 包含其中之一 / 不包含其中任一 + 枚举多选
  - number_input → 等于 / 大于 / 小于 / 介于 + 数字输入
  - text_input → 包含 / 不包含 + 文本输入

**嵌套分组逻辑**

- 顶层为一个条件组，有「所有（AND）」/「任一（OR）」逻辑选择器
- 每个条件组内可添加：条件行（单条件）、子条件组（嵌套）
- 子条件组同样有独立的 AND/OR 逻辑选择器
- 嵌套层级：理论无限，实际建议不超过 3 层，超过时无 UI 限制但给出提示
- UI 视觉区分：每层子组用缩进 + 左侧竖线标识

**rule_config JSON 结构示例**

```json
{
  "logic": "AND",
  "conditions": [
    {"field": "backend_category", "operator": "IN", "value": ["CAT-1003"]},
    {"field": "brand", "operator": "IN", "value": ["BRD-001"]},
    {
      "logic": "OR",
      "conditions": [
        {"field": "custom_attribute", "operator": "IN", "value": ["Red","Black"], "attribute_id": "ATTR-color"},
        {"field": "custom_attribute", "operator": "IN", "value": ["Leather"], "attribute_id": "ATTR-material"}
      ]
    },
    {"field": "price", "operator": "BETWEEN", "value": [500, 5000]}
  ]
}
```

**校验规则**

| 规则 | 说明 |
|---|---|
| 每个条件行必须填写操作符和值 | 缺少任意一项时，保存按钮置灰或提示「请补全所有条件」 |
| custom_attribute 必须先选属性 | 属性未选时操作符和值控件不出现 |
| price 介于：最小值 < 最大值 | 不满足时提示「价格区间无效：最小值必须小于最大值」 |
| listing_date 最近N天：正整数 | 输入非正整数时提示「请输入正整数天数」 |
| 至少有一条完整条件（自动选品模式） | 无任何条件时允许保存，系统视为「全量 active listing」 |

---

### 2.2 后台管理端：Collection 列表页

**功能描述**

运营查看所有 Collection 的汇总视图，支持搜索、状态筛选、跳转新建/编辑。

**页面元素**

- **页头**：页面标题「Collection 列表」+ 描述文案 + 「+ 新建 Collection」按钮
- **统计卡片区**（只读展示）：
  - Collection 总数
  - 启用中数量
  - 下架数量
  - 空 Collection 数量（商品数 = 0）
- **搜索框**：按 Collection 名称模糊搜索
- **列表表格**：见下方字段说明

**列表字段**

| 列名 | 说明 |
|---|---|
| 入口图 | 40×40px 商品图，未设置时显示灰色占位块 |
| Collection 名称 | 英文名称（name_en） |
| URL Slug | 完整 URL，如 `/collections/shoulder-bags` |
| 商品数 | 当前 active listing 数量（自动选品：实时计算；手动选品：已添加且 active 的数量） |
| 选品模式 | 「自动选品」/「手动选品」标签 |
| 状态 | 「启用」/「下架」标签 |
| 操作 | 「编辑」按钮（跳转详情页）+ 「删除」按钮（系统级 Collection 不显示删除按钮） |

**特殊规则**

- All Products Collection 始终显示在列表中，操作列只有「配置」按钮（无删除按钮）
- All Products 行的「选品模式」显示「系统自动」，「状态」始终为启用且不可修改
- 列表按 `sort_order` 升序排列，相同 sort_order 时按创建时间降序
- 列表支持表头排序：名称（字母序）/ 创建时间
- 不支持拖拽排序（Collection 展示顺序由 Navigation 模块控制）

**页面状态变体**

| 状态 | 表现 |
|---|---|
| 加载中 | 表格行显示骨架屏 |
| 搜索无结果 | 表格区域显示「未找到匹配的 Collection」 |
| 列表为空（无任何 Collection） | 提示「还没有 Collection，立即创建第一个」，显示新建按钮 |

**操作流程**

- 点击「+ 新建 Collection」→ 跳转新建向导页
- 点击「编辑」→ 跳转 Collection 详情页（编辑向导）
- 点击「删除」→ 弹出二次确认弹窗「确认删除《{名称}》？此操作不可恢复，Collection 内商品不受影响。」→ 确认后删除，Toast 提示「已删除」

**异常处理**

- 删除请求失败 → Toast 提示「删除失败，请稍后重试」
- 数据加载失败 → 显示空状态 + 重试按钮

**UI 关联**

- PC 端：后台原型 v0.11 → Collection 列表页
- 移动端：后台管理不做移动端适配

---

### 2.3 后台管理端：新建 Collection（向导流程）

**功能描述**

3 步向导引导运营创建新 Collection：Step 1 基础信息 → Step 2 商品来源 → Step 3 筛选配置。

**前置条件**

运营点击「+ 新建 Collection」按钮，跳转至新建页。

**操作流程**

**Step 1：基础信息**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| Collection 名称（英文）| 文本输入 | ✅ 必填 | 最大 100 字符；实时同步生成 URL Slug（转小写+连字符，如 "Shoulder Bags" → "shoulder-bags"） |
| Collection 名称（中文）| 文本输入 | 选填 | 最大 100 字符，内部运营用 |
| URL Slug | 文本输入 | ✅ 必填 | 自动生成但可手动修改；全局唯一校验；只允许小写字母、数字、连字符；系统自动前缀 `/collections/` |
| 入口图 | 图片上传 | 选填 | 建议尺寸 800×600px，支持 JPG/PNG/WebP，最大 5MB |
| H1 标题 | 文本输入 | 选填 | 页面主标题，留空时前台显示 Collection 名称 |
| Collection 描述 | 富文本 | 选填 | 显示在前台 Collection 页顶部。**SEO 上为可选增强**：建议 1–2 句帮助理解品类即可，**勿为 SEO 堆砌大段文案**（Google 明确反对，详见 SEO 合集 §4.2.1）。页面可索引不依赖此字段，而依赖足量商品 + H1 + 面包屑 |
| Meta Title | 文本输入 | 选填 | 留空时按降级链自动生成，placeholder 提示：「留空自动生成。优先级：❶ H1 标题 \| Looply  ❷ Collection 名称 \| Looply」 |
| Meta Description | 多行文本 | 选填 | 建议 120-160 字符；placeholder 提示：「建议 120-160 字符。留空自动生成。优先级：❶ Collection 描述前 160 字符  ❷ Shop {名称} at Looply. Authenticated pre-owned luxury at up to 70% off retail.」 |

Step 1 完成后「下一步」按钮解锁条件：Collection 名称（英文）和 URL Slug 均已填写。

**Step 2：商品来源**

运营选择两种模式之一（互斥单选）：

**模式 A：自动选品**
- 提示文案：「通过条件组合自动匹配商品，新上架符合条件的商品自动纳入，售出/下架商品自动移出。」
- 条件构建器（引用 §2.1 公共组件）
- 预览区：「符合条件商品 N 件」（实时查询，防抖 500ms）
- 默认排序配置（下拉选择）：Featured（手动排序）/ Most Relevant / Newest / Price: Low to High / Price: High to Low
- 若默认排序选择「Featured（手动排序）」，则解锁商品列表中的 Position 编辑功能

**模式 B：手动选品**
- 提示文案：「手动添加商品，只有明确添加的商品才会出现在前台。适合编辑精选、活动专题。」
- 显示「+ 添加商品」按钮，点击打开侧滑抽屉选品器（见 §2.4 中的选品器描述）
- 已选商品列表（空状态时展示引导文案「点击「添加商品」开始选品」）

Step 2 完成条件：手动选品模式下需至少添加 1 件商品；自动选品模式下无强制要求（无条件 = 全量）。

**Step 3：筛选配置**

- 提示：「Collection 创建后，在此配置前台筛选器。」
- 若 Collection 尚未保存，显示锁定态「请先保存 Collection 并配置商品来源」
- 保存后加载筛选维度配置界面（与详情页 Step 3 相同，见 §2.4）

**校验规则**

| 字段 | 规则 | 触发时机 |
|---|---|---|
| Collection 名称（英文）| 不能为空；最大 100 字符 | 失焦 + 提交 |
| URL Slug | 不能为空；只允许 `a-z0-9-`；全局唯一；不能使用系统保留词（all、new、search、shop） | 失焦 + 提交 |
| URL Slug 唯一性 | 冲突时提示「该 Slug 已被使用，建议：{name}-2」 | 失焦 + 提交 |

**异常处理**

- URL Slug 冲突 → 行内错误「该 Slug 已被占用，建议：{slug}-2」
- 网络异常（保存失败）→ Toast「保存失败，请检查网络后重试」，不清除用户已输入内容
- 图片上传失败 → 行内提示「图片上传失败，请重试」

**UI 关联**

- PC 端：后台原型 v0.11 → 新建 Collection 页（Step 1/2/3）
- 移动端：不适配

---

### 2.4 后台管理端：Collection 详情页（编辑向导）

**功能描述**

与新建向导结构相同的 3 步向导，用于编辑已有 Collection。除 All Products 有特殊锁定规则外，其他 Collection 均可完整编辑。

**All Products 特殊规则**

| 字段 | 是否可编辑 |
|---|---|
| Collection 名称 | ❌ 锁定（"All Products"） |
| URL Slug | ✅ 可修改（如改为 `/collections/shop`） |
| 状态 | ❌ 锁定（始终启用，不可下架） |
| 商品来源模式 | ❌ 锁定（固定为自动选品，条件为「所有 active listing」） |
| 条件构建器 | ❌ 不可编辑（条件为空，等于全量） |
| H1/描述/Meta/入口图/筛选/排序 | ✅ 均可编辑 |
| 删除操作 | ❌ 不存在删除按钮 |

**Step 2：商品来源（含商品列表）**

**自动选品模式：**

- 条件构建器：编辑已保存的规则
- 商品列表区域：展示当前匹配的商品列表（WYSIWYG，按前端实际展示顺序排列）
  - 列：商品缩略图（36×36px）| 商品名称 | 品牌 | 价格 | Position（行内可编辑数字） | 操作
  - Position 列：
    - 已固定商品：显示 📌 + 数字输入框，输入新数字可修改位置，清空输入框可取消固定
    - 未固定商品：输入框为空（placeholder 显示「自动」），输入数字即固定到该位置
    - 批量固定：勾选多件商品 → 输入起始位置 → 按勾选顺序连续填充 position 值
  - 操作列：「隐藏」按钮（隐藏后显示「已隐藏」badge + 「显示」按钮）+ 「查看详情」链接（跳转商品管理模块）
  - 被隐藏的商品在后台列表中灰显，前端不展示但后台保留
  - 自动选品无「移除」操作（移除后下次同步会重新加入）
  - 默认排序下拉：同新建 Step 2，选「Featured」时显示 Position 列并解锁编辑

**手动选品模式：**

- 商品列表区域：展示已添加的商品（WYSIWYG 排序）
  - 列：商品缩略图 | 商品名称 | 品牌 | 价格 | 销售状态 | 可见状态 | Position | 操作
  - 销售状态：「在售」/ 「已下架」（灰显）/ 「已售出」（灰显）；仅手动选品列表展示
  - 可见状态：「可见」/ 「已隐藏」；仅手动选品列表展示
  - Position 列：同自动选品，行内数字输入
  - 操作列：「隐藏/显示」切换 + 「移除」（断开选品关系，不可恢复）+ 「查看详情」链接
  - 状态筛选器：全部 / 在售 / 已下架 / 已售出
  - 「+ 添加商品」按钮：打开侧滑抽屉选品器

**侧滑抽屉：选品器（手动选品专用）**

- 触发：点击「+ 添加商品」
- 抽屉内容：
  - 标题：「添加商品 - 手动选品」
  - 条件构建器（复用 §2.1，此处作为候选商品筛选器，不保存为选品规则）
  - 候选商品列表（带 checkbox 多选，每行含商品图/名称/品牌/价格/成色）
  - 分页（每页 20 条）
  - 底部固定操作栏：「添加选中商品（N）」主按钮 + 「取消」按钮
- 已在已选列表中的商品，checkbox 置灰不可重复添加

**Step 3：筛选配置**

- 从全局筛选维度池中选择要在本 Collection 展示的维度
- 已选维度列表（可拖拽排序）：
  - 列：维度名称 | 展示名称（可修改）| 类型 | 填充率（只读，每日更新）| 默认展开/折叠 | 是否 Quick Filter | 操作
  - Quick Filter 开关打开后，显示 Quick Filter 标签名输入框和预设条件配置
- 「+ 从维度池添加」：弹出维度选择器，展示所有 active 维度，支持搜索
- Quick Filters 汇总区：展示已配置的 Quick Filter 条目，可拖拽调整顺序（建议 5-8 个）
- 零结果说明：「填充率低于阈值的维度将在前台自动隐藏（每日更新），前台零结果的筛选选项实时隐藏」

**Collection 状态管理**

| 操作 | 说明 | 二次确认 |
|---|---|---|
| 下架（Archived）| 页面标题区或详情页顶部操作按钮；URL 返回 404；商品可见性不受影响；所有配置完整保留 | ✅ 「确认下架？消费者将无法访问该 Collection，但商品可通过其他途径发现。」 |
| 恢复启用（Active）| 下架状态时显示「恢复启用」按钮；一键恢复，无需重新配置 | ❌ 无需确认 |
| 删除 | 永久删除 Collection 及选品关系（商品不受影响）；有手动选品关联时，删除同时清除 fc_manual_product 记录 | ✅ 「确认永久删除？该操作不可撤销。」 |

**校验规则**（与新建相同，补充：）

| 规则 | 说明 |
|---|---|
| URL Slug 修改唯一性 | 修改后的 Slug 不能与其他 Collection（包括自身原值外）重复 |
| Position 值 | 正整数，不超过当前 Collection 商品总数；相同 position 时，后提交的覆盖先提交的（系统自动顺移） |

**异常处理**

- 批量保存 Position 失败 → 行内提示失败的行，已成功的保留
- 从选品器添加商品后，已选列表加载失败 → Toast「添加完成，但列表刷新失败，请手动刷新页面」
- 商品详情跳转：用新标签页打开商品管理模块，不影响当前编辑状态

**UI 关联**

- PC 端：后台原型 v0.11 → Collection 详情页（Step 1/2/3）；侧滑抽屉选品器
- 移动端：不适配

---

### 2.5 后台管理端：筛选维度管理

**功能描述**

维护全局筛选维度池。运营/管理员在此注册维度，各 Collection 在详情页 Step 3 引用这些维度。

**页面元素**

- 页头：「筛选维度管理」+ 描述 + 「+ 新建维度」按钮
- 说明文案：「筛选维度是数据源的封装层，支持 6 种数据源类型：属性(attribute)、品牌(brand)、系列(series)、价格(price)、成色(condition)、尺码(size_system)。维度创建后可在各 Collection 的筛选配置中引用。」
- 维度列表表格（见下方字段）

**维度列表字段**

| 列名 | 说明 |
|---|---|
| 维度名称（英文/中文）| dimension_name_en + dimension_name_zh |
| 数据源类型 | attribute / brand / series / price / condition / size_system 标签 |
| 展示类型 | checkbox / range / color_swatch / size_grid / radio / search_list |
| 填充率阈值 | min_fill_rate，如「30%」 |
| 引用数量 | 当前被多少个 Collection 引用（只读） |
| 状态 | 启用 / 停用 |
| 操作 | 「编辑」按钮 |

**新建/编辑维度（侧滑面板）**

**基础配置：**

| 字段 | 必填 | 说明 |
|---|---|---|
| 维度名称（英文）| ✅ | 如 "Color"、"Brand"、"Size (US)" |
| 维度名称（中文）| 选填 | 后台运营用 |
| 数据源类型 | ✅ | 下拉选择，6种类型，选择后触发级联配置 |
| 展示类型 | ✅ | 下拉选择，根据数据源类型过滤可用项 |
| 最低填充率阈值 | 选填 | 默认 30%；低于此阈值的维度在前台自动隐藏 |

**数据源类型级联配置矩阵：**

| 数据源类型 | 是否展示「关联属性」配置 | 是否展示「值归一化」配置 | 特有配置 |
|---|---|---|---|
| attribute | ✅ 展示（多选标签，选择多个 attribute_def） | ✅ 展示 | 值归一化分组 |
| brand | ❌ | ❌ | 无 |
| series | ❌ | ❌ | 无 |
| price | ❌ | ❌ | 价格区间配置（自定义分档，如 <$500 / $500-$1000 / $1000+） |
| condition | ❌ | ❌ | 无 |
| size_system | ❌ | ❌ | 见下方「尺码维度配置」 |

**attribute 类型：关联属性 + 值归一化配置**

- 关联属性：多选标签模式，从全量 attribute_def 中搜索选择（支持关联多个，如 color + Color + bag_color）
- priority 字段：同一维度下多个关联属性的优先级（数字越大越优先）
- 值归一化配置区域：
  - 系统自动扫描所有关联属性的已有值，展示原始值列表
  - 运营将语义相同的原始值拖入同一分组（如 Red、red、RED → 展示为 "Red"）
  - 未分组的值默认各自独立展示
  - 支持手动新建分组、修改展示名称、删除分组
  - color_swatch 展示类型时：分组编辑器增加「颜色十六进制」输入框

**price 类型：价格区间配置**

- 默认分档：Under $500 / $500-$1,000 / $1,000-$3,000 / $3,000+
- 运营可自定义分档数量和区间边界
- 每档有一个「标签名称」（展示给消费者）和「最小值/最大值」字段

**size_system 类型：尺码维度配置**

| 字段 | 必填 | 说明 |
|---|---|---|
| 关联尺码体系 | ✅ | 单选下拉，列出商品系统所有 size_system（US / EU / UK / IT / FR / SHOE_US / SHOE_EU / RING_US / BELT_CM 等） |
| 适用类目（只读）| — | 跟随所选体系自动展示：服装 / 鞋类 / 配饰 |
| ONE SIZE 处理策略 | ✅ | 包容性筛选（推荐）/ 独立选项 / 排除；枚举说明见下方 |
| 启用跨体系换算 | 开关 | 用户筛选 US 8 时，同时匹配 UK 6 / EU 39 等价值商品（基于 size_conversion 表） |
| 启用品牌尺码兼容 | 开关 | 同时匹配品牌专属尺码体系等价值（基于品牌尺码换算表） |

**ONE SIZE 处理策略枚举**

| 枚举值 | 含义 |
|---|---|
| inclusive（包容性筛选，推荐）| 筛选某个具体尺码时，结果中同时包含标注为 ONE SIZE 的商品 |
| standalone（独立选项）| ONE SIZE 作为单独筛选项出现，不自动纳入其他尺码的筛选结果 |
| exclude（排除）| ONE SIZE 商品不出现在尺码筛选器中 |

**校验规则**

| 字段 | 规则 |
|---|---|
| 维度名称（英文）| 不能为空；最大 50 字符；全局唯一（提示「该维度名称已存在」） |
| attribute 类型：关联属性 | 至少选择 1 个 attribute_def |
| price 类型：区间配置 | 最小值必须 < 最大值；区间不能重叠 |
| size_system 类型：关联尺码体系 | 必选 |

**停用维度规则**

- 停用一个维度时，检查其是否被 Collection 引用
- 有引用时：弹窗警告「该维度被 N 个 Collection 引用，停用后这些 Collection 的筛选配置中该维度将不再展示。确认停用？」

**异常处理**

- 扫描关联属性原始值超时（属性值过多）→ 展示「扫描中，请稍后刷新」提示
- 保存失败 → Toast「保存失败，请稍后重试」，保留编辑状态

**UI 关联**

- PC 端：后台原型 v0.11 → 筛选维度管理页；侧滑面板（新建/编辑维度）
- 移动端：不适配

---

### 2.6 前台 C 端：Collection 页（类目浏览页）

**功能描述**

消费者访问某个 Collection 的商品列表页，支持筛选、排序、商品浏览、收藏。URL 格式：`/collections/{slug}`。

**前置条件**

Collection 状态为「启用（active）」。

**页面布局**

PC 端（≥1024px）：

```
[ Header 全局导航 ]
[ 面包屑：Home / {Collection名称} ]
[ Collection 入口图 Banner（可选，有入口图时展示）]
[ Quick Filters Chips 横向滚动 ]
[ 商品数量 + 排序下拉 ]
[ 左侧筛选面板（280px） | 商品网格（4列，剩余宽度）]
[ 分页器 ]
```

移动端（<768px）：

```
[ Header 简化导航 ]
[ Quick Filters Chips 横向滚动 ]
[ 商品数量 + [Filter] [Sort] 按钮固定栏 ]
[ 商品网格（2列）]
[ 无限滚动 ]
```

**页面元素**

**面包屑**（PC端）
- 格式：`Home / {Collection名称}`
- Home 链接到首页，Collection名称为当前页不可点击

**Quick Filters**
- 运营配置的 Quick Filter Chip 列表，横向滚动
- 商品数为 0 的 Chip 自动隐藏（前端实时判断）
- 选中态：深色背景 + 白色文字；未选中态：白色背景 + 灰色边框
- 可叠加：多个 Quick Filter 可同时选中

**商品计数 + 排序**
- 文案：「N items found」（N 随筛选实时变化）
- 排序下拉选项（枚举，固定 5 个）：

| 选项 | 对应 sort_key | 说明 |
|---|---|---|
| Featured | manual（手动排序）| 运营手工编排的顺序，为该 Collection 默认排序时展示 |
| Most Relevant | relevance | 算法/权重推荐 |
| Newest | listed_at DESC | 最新上架 |
| Price: Low to High | listing_price ASC | 价格升序 |
| Price: High to Low | listing_price DESC | 价格降序 |

- 默认选中排序：由 Collection 的「默认排序」配置决定

**左侧筛选面板**（PC端，固定 280px）
- 每个筛选维度为一个可折叠分组（手风琴式）
- 默认展开/折叠：由 fc_filter_config.default_expanded 控制
- 每个选项后显示商品数量（N），数量为 0 的选项不展示
- 填充率低于维度阈值时，整个维度分组不展示
- 顶部「Clear All」按钮：清除当前所有筛选条件

各展示类型规格：

| dimension_type | 前端组件 | 交互说明 |
|---|---|---|
| checkbox | 多选勾选列表，默认显示前 5 项，「Show more...」展开全部 | 支持多选 |
| search_list | 带搜索框的多选列表（品牌用） | 支持搜索过滤 + 多选 |
| range | 价格区间，快捷选项（单选）+ 自定义最小/最大值输入框 | 单选快捷项 或 自定义区间 |
| color_swatch | 色块网格，每个色块 24×24px，悬停显示颜色名称 | 支持多选 |
| size_grid | 尺码标签网格，按 size_system 排序 | 支持多选 |
| radio | 单选列表 | 单选 |

**移动端筛选交互（底部抽屉式）**
- 点击「Filter」按钮 → 抽屉从底部滑出，占屏幕 80% 高度
- 第一级：维度列表；点击某维度 → 进入第二级（具体选项）
- 底部固定「Apply Filters（N items）」按钮，N 实时更新
- 支持手势下滑关闭抽屉
- Filter 按钮显示已选条件数量（如「Filter (3)」）

**商品卡片**

PC 端（200×320px）：

| 区域 | 内容 |
|---|---|
| 商品图片（200×200px）| 纯白背景，Hover 切换第二张图 |
| 认证徽章 | `🔒 Authenticated`，仅 $500+ 商品显示，图片左上角 |
| 品牌名称 | 加粗，12px，全大写 |
| 商品标题 | 14px，最多 2 行，超出省略 |
| 价格 | 现价（加粗）+ 原价（删除线，灰色，若有）|
| 成色 + 尺寸 | 灰色，12px |
| 收藏按钮 | 心形图标，右上角；点击收藏/取消收藏 |

移动端（167.5×280px）：与 PC 端同字段，简化部分：移除原价、移除点赞数，认证徽章简写为「Auth」。

**空结果状态（筛选无结果）**

触发条件：用户应用筛选条件后 items.length === 0（不是独立页面，同一 URL 切换状态）。

页面结构：
- 左侧筛选面板保留（显示当前选中状态，方便逐一取消）
- 商品区域：`0 items found`
- Empty State 区域：搜索图标 + 「No results found」标题 + 「Try adjusting your filters or browse other collections.」引导文案
- 两个 CTA：「Clear Filters」（主按钮）/ 「Browse All Items」（次按钮，链接到 /collections/all）
- 推荐区域：「Popular in {Collection Name}」，展示该 Collection 热门商品 4 张卡片（按点赞数降序，忽略当前筛选条件取）

Collection 状态为下架（archived）：
- URL 返回 404 页面
- 推荐引导到首页或 All Products

**筛选条件持久化**

- 筛选状态以 URL Query Parameter 持久化：`/collections/shoulder-bags?brand=chanel&condition=A,B&price_max=3000&sort=newest`
- 筛选参数页（有 query params）加 `<meta name="robots" content="noindex">` 防止搜索引擎收录筛选结果页
- 支持浏览器前进/后退（PushState）

**分页策略**

- PC 端：传统分页，每页 24 件商品，显示页码
- 移动端：无限滚动，每次加载 12 件，距底部 200px 时预加载

**SEO 相关**

- `<title>`：见 §2.7 Meta 降级链
- `<meta name="description">`：见 §2.7 Meta 降级链
- `<link rel="canonical">`：指向不带 Query Params 的 Collection URL
- Structured Data（BreadcrumbList + CollectionPage）
- 面包屑结构化数据格式：

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://looply.com"},
    {"@type": "ListItem", "position": 2, "name": "{Collection名称}", "item": "https://looply.com/collections/{slug}"}
  ]
}
```

**异常处理**

- Collection 不存在（slug 错误）或已下架 → 返回 404 页面
- 商品列表接口失败 → 展示错误状态 + 「Refresh」按钮
- 筛选选项加载失败 → 筛选面板展示「筛选器暂时不可用」，商品列表正常展示

**UI 关联**

- PC 端：前台类目页原型 v0.3（`looply-类目页-PC-v0.3.html`）；无结果状态：`looply-类目页-PC-v0.3-无结果.html`
- 移动端：`looply-类目页-Mobile-v0.2.html`

---

### 2.7 机制：Meta SEO 降级链

**功能描述**

Collection 页面的 `<title>` 和 `<meta name="description">` 根据以下降级链自动生成，确保即使运营未手动填写 SEO 字段，每个页面也有合理的 Meta 信息。

**触发条件**

每次 Collection 页面被请求时，服务端根据字段优先级动态生成 Meta 标签。

**Meta Title 降级链**

| 优先级 | 条件 | 输出 |
|---|---|---|
| 1 | `seo_title` 字段有值 | 直接使用 seo_title |
| 2 | `seo_title` 为空，`h1_title` 有值 | `{h1_title} \| Looply` |
| 3 | `seo_title` 和 `h1_title` 均为空 | `{name_en} \| Looply` |

**Meta Description 降级链**

| 优先级 | 条件 | 输出 |
|---|---|---|
| 1 | `seo_description` 字段有值 | 直接使用 seo_description |
| 2 | `seo_description` 为空，`description` 有值 | description 去 HTML 标签后截取前 160 字符（超出部分加 `...`） |
| 3 | `seo_description` 和 `description` 均为空 | `Shop {name_en} at Looply. Authenticated pre-owned luxury at up to 70% off retail.` |

**规则说明**

- `name_en` 是必填字段，保证优先级 3 永远能生成兜底值
- 后台原型中，Meta Title 和 Meta Description 输入框的 placeholder 直接展示降级优先级说明，让运营清楚留空后的效果

**后台预览功能**

- SEO 字段下方实时展示「生效预览」区域
- 字段为空时，预览区以灰色斜体展示降级后的默认值
- 预览格式参考 Google 搜索结果样式（标题蓝色链接 + 描述灰色摘要）

---

### 2.8 机制：商品准入与状态同步

**功能描述**

Collection 是展示分组，不控制商品本身的上下架状态。商品准入条件和状态变化时的处理逻辑如下。

**商品准入条件**

进入 Collection 展示的商品必须同时满足：
1. `item_status = 销售中`
2. 在当前渠道有 `listing_status = active` 的渠道商品记录

不满足上述任一条件的商品不出现在任何 Collection 前端展示中。

**状态变化处理逻辑**

| 场景 | 自动选品 Collection | 手动选品 Collection |
|---|---|---|
| 商品上架（listing active）| 自动纳入（匹配规则时）| 不自动纳入（需手动添加）|
| 商品下架（listing off_shelf）| 自动移出前端展示 | 前端不展示，后台保留记录（灰显 + 「已下架」badge）|
| 商品售出（item sold）| 自动移出 | 前端不展示，后台保留记录（灰显 + 「已售出」badge）|
| 商品重新上架 | 自动回来（仍匹配规则时）| 自动恢复前端展示，position 保留 |

**自动选品 Pin 记录清除机制**

- 当商品因下架/停售/售出等原因移出自动选品 Collection 时，同步清除该商品在本 Collection 的 pin 记录（fc_manual_product 中的 pinned=true 记录）
- 商品重新上架后：重新匹配进 Collection，但无 pin 位置（进入未固定状态），运营需重新 pin
- 原因：避免 pin 位置冲突，MVP 选择最简方案

**手动选品商品保留机制**

- 手动选品的商品下架/售出后，`fc_manual_product` 记录保留
- 后台展示「已下架」/「已售出」灰显状态，前端不展示
- 商品重新上架后，自动恢复前端展示，position 保留
- 运营可在后台移除这些不可用商品，或等其重新上架

**隐藏与移除的区别**

| 操作 | 适用模式 | 数据变化 | 前端 | 可恢复 |
|---|---|---|---|---|
| 隐藏（Hide）| 自动选品 + 手动选品 | 自动选品：添加排除记录；手动选品：`is_hidden=true` | 不展示 | ✅ 可「显示」恢复 |
| 移除（Remove）| 仅手动选品 | 删除 `fc_manual_product` 记录 | 不展示 | ❌ 需重新手动添加 |

**自动选品隐藏实现**

最终展示商品集合 = 规则匹配的商品 - 隐藏列表中的商品（`fc_hidden_product` 独立存储，不修改 rule_config）

**上架时间条件同步频率**

- 「最近N天」条件：每日凌晨（UTC+8 00:00）重新评估，超出天数范围的商品自动移出
- 「介于（固定区间）」条件：同样每日同步评估
- 不提供实时同步（精确到分钟）——「New Arrivals」类场景每日同步足够

---

### 2.9 机制：前台收藏（Favorites）

**功能描述**

消费者点击商品卡片上的心形收藏按钮，将商品加入收藏夹。MVP 阶段未登录用户数据存 localStorage，后续登录时合并到服务端。

**触发条件**

任意状态下（已登录 / 未登录）点击商品卡片收藏按钮。

**处理流程**

**未登录用户：**
1. 点击心形 → 立即变为实心（红色）
2. Toast 提示：「Added to Favorites」（2秒后消失）
3. 收藏数据：`localStorage.set('looply_favorites', [...listing_ids])`
4. 再次点击 → 取消收藏，心形恢复空心，Toast：「Removed from Favorites」

**已登录用户（登录后迁移到服务端，非 MVP，占位描述）：**
- 收藏直接写服务端，不依赖 localStorage

**收藏夹页面（/favorites）**【⚠️ 待设计：无原型设计稿】

- 读取 localStorage，调用 API 批量获取商品最新状态后渲染
- 已售出/已下架商品：卡片标记「Sold」灰显，保留在列表（不静默删除）
- 空状态：展示「No favorites yet. Start exploring!」引导语

**后续迁移路径（非 MVP，上线通知体系时实施）**

1. 用户注册/登录时，前端将 localStorage 收藏自动 merge 到服务端账号
2. merge 逻辑：取并集去重，已售商品标记「已售」保留
3. merge 完成后清空 localStorage
4. 收藏夹页顶部引导条：「Sign in to get price drop alerts and restock notifications」

**规则说明**

- 已知局限（MVP 阶段可接受）：
  - 换设备 / 清缓存 = 收藏数据丢失
  - 无法做用户行为归因
  - 多标签页同时操作无原生同步（发生概率极低）
- 决策依据：MVP 无通知体系，强制登录的即时 ROI 不足，优先降低使用摩擦（参考 Shopify Swym Wishlist Plus 默认模式）

**UI 关联**

- PC 端：商品卡片收藏按钮（右上角心形图标）；收藏夹页 ⚠️ 待设计稿
- 移动端：商品卡片收藏按钮；收藏夹页 ⚠️ 待设计稿

---

### 2.10 机制：品牌驱动 Collection（品牌页）

**功能描述**

品牌页是面向消费者的「某品牌全部在售商品」聚合页（如 Pre-Owned Chanel）。MVP 不新建独立的 `/brands/` 路由，而是**复用 Collection 体系**：品牌页本质是一个商品来源为 `brand` 规则的 Collection，URL 仍为 `/collections/{brand-slug}`。

**设计目标（解决运营痛点）**：
- 运营不再为每个品牌手动挑商品（靠 brand 规则自动聚合）；
- 品牌名称/描述/logo 等信息**不在 Collection 重复维护**，以「品牌管理」为唯一数据源；
- 新品上架按品牌自动进、售出自动出（复用 §2.8 状态同步）。

**实现方式：复用现有 rule 引擎 + 轻量品牌关联**

品牌页 = `source_type='rule'` 的 Collection，其 `rule_config` 为品牌条件（条件构建器 §2.1 已支持 `brand` 字段，零引擎改动）：

```json
{ "logic": "AND", "conditions": [ {"field": "brand", "operator": "IN", "value": ["BRD-001"]} ] }
```

在此基础上，collection 表新增一个可空字段 `linked_brand_id`（外键 → 品牌管理 brand 表），用于：
1. 标识该 Collection 是"品牌页"（值非空即为品牌页）；
2. SEO 字段降级时实时读取品牌管理（见下方降级链扩展），避免双写；
3. 前台输出 Brand 结构化数据（见 SEO 处理）。

> 说明：商品聚合完全走现有 rule 引擎，本小节新增的仅是 `linked_brand_id` 关联字段 + 一个"从品牌生成 Collection"的创建入口，不引入新的选品机制。

**「从品牌生成 Collection」创建入口**

Collection 列表页「+ 新建 Collection」旁增加「从品牌生成」入口：
1. 运营选择一个或多个品牌（来自品牌管理）；
2. 系统对每个所选品牌自动创建一个 Collection：
   - `source_type='rule'`，`rule_config` 自动写入 `{brand IN [该品牌]}`；
   - `linked_brand_id` 关联该品牌；
   - `url_slug` 默认取品牌管理的 `brand_slug`（纳入全局 slug 唯一性校验，见 §2.3）；
   - H1/描述/Meta/入口图**留空**（前台渲染时降级读品牌管理，运营无需填写）；
3. 支持批量生成；生成后可像普通 Collection 一样在详情页编辑（如覆盖 H1、追加筛选维度）。

**「品牌管理」需补充的字段（依赖商品系统）**

品牌管理原为商品系统内部数据，作为品牌页数据源需补充以下面向消费者/SEO 的字段（一次性补充，所有品牌页自动复用）：

| 字段 | 用途 | 缺失后果 |
|---|---|---|
| brand_slug | 品牌页 URL 段（小写连字符；与 collection slug **同池唯一**） | 无法生成 URL |
| brand_h1 / display_name | 页面 H1（如 "Pre-Owned Chanel"） | H1 缺失 |
| brand_description（建议 1–2 句，可选） | 页面顶部品牌简介 | **可选增强**（非可索引前提）；利于用户理解与 GEO 引用。品牌页可索引依赖足量在售商品 + H1 + 面包屑，详见 SEO 合集 §4.2.1 |
| brand_meta_title / brand_meta_description | SERP 展示（可走降级链兜底） | 靠降级链生成 |
| brand_logo / brand_banner | 页面头图 + Brand 结构化数据 | schema 不完整 |

**Meta / 内容降级链扩展（基于 §2.7）**

品牌驱动 Collection（`linked_brand_id` 非空）的字段降级，在 §2.7 通用降级链基础上插入"品牌管理"层：

| 内容 | 降级顺序 |
|---|---|
| H1 | collection.h1_title → 品牌管理 brand_h1 → `Pre-Owned {brand_name}` |
| 描述/导语 | collection.description → 品牌管理 brand_description |
| Meta Title | collection.seo_title → 品牌管理 brand_meta_title → `Pre-Owned {brand_name} \| Looply` |
| Meta Description | collection.seo_description → 品牌管理 brand_meta_description → collection/品牌描述前 160 字符 → `Shop authenticated pre-owned {brand_name} at Looply.` |
| logo / banner | collection.icon_url/banner_url → 品牌管理 brand_logo/brand_banner |

**SEO / GEO 处理（品牌驱动 Collection 专属）**

| 项 | 规则 |
|---|---|
| 空品牌页 | 该品牌 0 件在售时，页面 `noindex` 且不进 sitemap（防薄内容）；有货自动转 index |
| 结构化数据 | 在通用 BreadcrumbList + CollectionPage 基础上，**额外输出 schema.org `Brand`**（name/logo/description）；PDP 的 brand 字段指向同一品牌实体，强化品牌实体信号（GEO 关键） |
| canonical | 自指向 `/collections/{brand-slug}`（无 query 参数版） |
| sitemap | 品牌页单列 `sitemap-brands.xml`（或在 collections 段内标识），与 SEO 规范对齐 |
| 筛选参数 | 同普通 Collection，带 query 参数页 noindex,follow |

**品类筛选范围说明（MVP 取舍）**

- 品牌页**不提供品类（包/首饰/配饰）筛选**：品牌页即该品牌全品类在售商品，不再按品类细分（与 R-15「backend_category 不作为筛选维度数据源」一致，无矛盾）。
- 由此带来的 SEO 取舍：MVP **不单独承载 "pre-owned chanel bags" 这类品类×品牌交叉中长尾**（既不在品牌页内细分，也不升格为独立可索引页）。用户如需品类细分，走"导航 → 品类页 → 叠加品牌筛选"路径（品类页支持按 brand 筛选）。
- Phase 2 重启路径：若数据显示交叉词有显著搜索量，可按 SEO 规范的"高搜索量组合升格为正式 collection 页"机制，将选定的品类×品牌组合做成带独立 slug + 导语的可索引 Collection。

**与现有机制的复用关系**

| 能力 | 复用 | 改动 |
|---|---|---|
| 商品聚合 | §2.1 条件构建器 brand 字段 + §2.8 状态同步 | 无 |
| 前台页面（筛选/排序/Quick Filter/收藏/无结果/分页） | §2.6 Collection 页 | 无 |
| 后台管理（列表/详情/状态） | §2.2 / §2.4 | 仅加"从品牌生成"入口 |
| Meta 降级 | §2.7 | 插入品牌管理层 |
| 数据模型 | collection 表 | 新增 linked_brand_id 字段；品牌管理补 SEO 字段 |

## 三、依赖与风险

### 3.1 上下游系统依赖

| 依赖模块 | 依赖内容 | 优先级 |
|---|---|---|
| 商品管理模块 | listing、used_item、spu 等数据表；条件构建器所需的 backend_category、brand、series、attribute_def 数据；商品详情页跳转链接格式；**商品的 `primary_collection`（主归属）字段，用于 PDP 面包屑与 schema，见 R-19** | P0（阻塞）|
| 品牌管理（商品系统） | 品牌页数据源；需补充 brand_slug / brand_h1 / brand_description / brand_meta_* / brand_logo 等面向消费者与 SEO 的字段，见 §2.10 | P1（品牌页依赖）|
| 尺码管理模块 | size_system、size_conversion 表；品牌尺码换算表 | P1（筛选维度尺码类型依赖）|
| 用户账号系统 | 登录态识别；后续收藏 merge 依赖 | P2（MVP 不阻塞）|
| Navigation 导航模块 | 前台导航菜单中展示哪些 Collection；面包屑层级数据 | P2（MVP 手动配置面包屑兜底）|
| 图片 CDN / 对象存储 | Collection 入口图上传存储 | P1 |

### 3.2 外部服务依赖

本模块 MVP 无强依赖外部第三方服务。

### 3.3 风险

| 风险项 | 描述 | 缓解措施 |
|---|---|---|
| 自动选品每日同步延迟 | 「最近N天」商品每日凌晨同步，理论上存在最长 24h 的数据延迟 | 标注为设计决策，前台展示「New Arrivals」类 Collection 可接受每日同步 |
| 筛选器填充率统计性能 | 每日 cron 计算所有 Collection × 所有维度的填充率，数据量大时可能超时 | 后端拆分为增量更新 + 批量任务；MVP 数据量小，暂不优化 |
| URL Slug 变更 SEO 影响 | 运营修改 Slug 后原 URL 失效 | 提示运营「修改 Slug 会导致原 URL 失效，建议配置 301 重定向」；301 重定向功能由 SEO 工程师独立处理 |
| localStorage 收藏数据丢失 | 用户清缓存或换设备后收藏丢失 | 已在设计决策中记录为可接受的 MVP trade-off |
| 条件构建器嵌套层级过深 | 运营创建极深的嵌套规则，导致查询性能下降 | 超过 3 层嵌套时 UI 给出提示；后端设置最大嵌套层数限制（建议 5 层） |

---

## 四、版本规划

### 4.1 MVP（当前版本）范围

| 功能模块 | MVP 包含 |
|---|---|
| Collection 管理 | 后台 CRUD、扁平结构、启用/下架二态、All Products 系统级 Collection |
| 自动选品 | 条件构建器（9字段）、嵌套 AND/OR 分组、每日同步、Pin+Rule 排序 |
| 手动选品 | 侧滑抽屉选品器、行内 Position 编辑、隐藏/移除 |
| 筛选维度管理 | 6种数据源类型、多源属性绑定、值归一化、尺码体系配置 |
| Collection 筛选配置 | 从维度池选择维度、拖拽排序、Quick Filters 配置 |
| 前台 Collection 页 | PC端+移动端、左侧筛选面板、Quick Filters、排序（5选项）、商品卡片、无结果状态 |
| Meta SEO 降级链 | 三级降级、后台实时预览 |
| 前台收藏 | localStorage 存储、未登录可用 |

### 4.2 后续迭代方向

| 方向 | 说明 |
|---|---|
| AI 动态 Quick Filters | 基于库存热度、用户历史、价格分布、趋势自动生成 Chip |
| AI 推荐规则 | 基于商品池自动推荐选品条件 |
| 混合选品模式 | 自动规则选品 + 手动置顶 Boost/Bury 合并 |
| Navigation 导航模块联动 | 自动生成多级面包屑，Collection 排序由导航控制 |
| 收藏通知体系 | 降价提醒、到货通知，需与账号系统联动 |
| 品牌优先导航（/brands/{slug}）| 品牌页独立建设 |
| 渠道 Feed 管理 | Google Shopping 等平台的分类映射，独立模块 |
| 用户尺码偏好记忆 | 跨 Collection 持久化尺码筛选设置 |
| 个性化排序 | 基于用户历史行为的推荐排序 |

---

## 五、数据与埋点

### 5.1 关键前台埋点事件

| 事件名 | 触发时机 | 关键字段 |
|---|---|---|
| collection_view | 用户进入 Collection 页 | collection_id, collection_name, product_count |
| filter_apply | 用户应用筛选条件 | collection_id, filter_dimension, filter_value |
| filter_clear | 用户清空全部筛选 | collection_id |
| quick_filter_click | 用户点击 Quick Filter Chip | collection_id, chip_label |
| sort_change | 用户切换排序方式 | collection_id, sort_key_from, sort_key_to |
| product_card_click | 用户点击商品卡片 | collection_id, listing_id, position_in_list |
| favorite_add | 用户收藏商品 | listing_id, user_logged_in（true/false）|
| favorite_remove | 用户取消收藏 | listing_id |
| empty_state_view | 筛选无结果状态展示 | collection_id, applied_filters |
| clear_filters_click | 无结果页点击 Clear Filters | collection_id |

### 5.2 后台操作日志（审计）

关键后台操作需记录操作日志（操作人、操作时间、操作内容）：

| 操作 | 记录内容 |
|---|---|
| 创建 Collection | 新 Collection 的 fc_id、名称、URL |
| 修改 Collection 选品规则 | 修改前后的 rule_config |
| 下架/恢复 Collection | 状态变更 |
| 删除 Collection | 被删除的 Collection 信息快照 |
| 修改筛选维度 | 修改前后的配置 |

---

## 六、附录

### 6.1 设计稿索引

| 页面/状态 | 端 | 原型文件 | 版本 |
|---|---|---|---|
| Collection 列表页 | 后台 PC | `looply-类目管理-后台-v0.11.html` | v0.11 |
| 新建 Collection（Step 1/2/3）| 后台 PC | `looply-类目管理-后台-v0.11.html` | v0.11 |
| Collection 详情页（Step 1/2/3）| 后台 PC | `looply-类目管理-后台-v0.11.html` | v0.11 |
| 侧滑抽屉：选品器 | 后台 PC | `looply-类目管理-后台-v0.11.html` | v0.11 |
| 侧滑面板：筛选维度编辑 | 后台 PC | `looply-类目管理-后台-v0.11.html` | v0.11 |
| 筛选维度管理页 | 后台 PC | `looply-类目管理-后台-v0.11.html` | v0.11 |
| Collection 页（有商品）| 前台 PC | `looply-类目页-PC-v0.3.html` | v0.3 |
| Collection 页（无结果状态）| 前台 PC | `looply-类目页-PC-v0.3-无结果.html` | v0.3 |
| Collection 页（有商品）| 前台移动端 | `looply-类目页-Mobile-v0.2.html` | v0.2 |
| 收藏夹页（/favorites）| 前台 PC | ⚠️ 待设计稿 | — |
| 收藏夹页（/favorites）| 前台移动端 | ⚠️ 待设计稿 | — |

### 6.2 数据模型

以下为本模块核心表结构，详细 DDL 以工程数据库为准，此处仅列字段语义供评审参考。

**collection 表**（对应 frontend_category，建议更名为 collection）

| 字段 | 类型 | 说明 |
|---|---|---|
| fc_id | VARCHAR(20) PK | Collection 唯一标识 |
| name_en | VARCHAR(100) NOT NULL | 英文名称，必填，前台展示 |
| name_zh | VARCHAR(100) | 中文名称，选填，后台运营用 |
| url_slug | VARCHAR(100) NOT NULL UNIQUE | URL 路径段，全局唯一 |
| icon_url | VARCHAR(255) | 入口图 URL |
| banner_url | VARCHAR(255) | Banner 图 URL（预留） |
| description | TEXT | Collection 描述（富文本），前台展示 |
| seo_title | VARCHAR(200) | 手动 Meta Title，选填 |
| seo_description | VARCHAR(500) | 手动 Meta Description，选填 |
| h1_title | VARCHAR(200) | 页面 H1，选填 |
| source_type | ENUM('rule','manual') | 商品来源类型 |
| rule_config | JSON | 自动选品嵌套条件 JSON；手动选品时为 NULL |
| linked_brand_id | VARCHAR(20) FK NULL | 关联品牌管理 brand 表；非空时该 Collection 为「品牌驱动 Collection（品牌页）」，SEO 字段降级读品牌管理，见 §2.10 |
| default_sort_key | ENUM('manual','relevance','newest','price_asc','price_desc') | 前台默认排序 |
| display_mode | ENUM('grid','list','featured') | 展示模式，默认 grid |
| products_per_page | INT DEFAULT 24 | 每页商品数（PC端） |
| status | ENUM('active','archived') | 启用 / 下架 |
| sort_order | INT DEFAULT 0 | 列表排序权重 |
| is_system | BOOLEAN DEFAULT FALSE | 系统级 Collection（All Products），不可删除不可下架 |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 最后更新时间 |

**fc_manual_product 表**

| 字段 | 类型 | 说明 |
|---|---|---|
| id | BIGINT PK | 自增主键 |
| fc_id | VARCHAR(20) FK | 所属 Collection |
| listing_id | VARCHAR(20) FK | 商品 listing ID |
| sort_order | INT DEFAULT 0 | 排序位置（position） |
| pinned | BOOLEAN DEFAULT FALSE | 是否固定 |
| is_hidden | BOOLEAN DEFAULT FALSE | 是否在本 Collection 中隐藏 |
| created_at | TIMESTAMP | 添加时间 |
| UNIQUE | (fc_id, listing_id) | 同一商品不可重复添加 |

**fc_hidden_product 表**（自动选品排除记录）

| 字段 | 类型 | 说明 |
|---|---|---|
| id | BIGINT PK | 自增主键 |
| fc_id | VARCHAR(20) FK | 所属 Collection |
| listing_id | VARCHAR(20) FK | 被排除的商品 listing ID |
| created_at | TIMESTAMP | 隐藏时间 |
| UNIQUE | (fc_id, listing_id) | 防止重复记录 |

**filter_dimension 表**

| 字段 | 类型 | 说明 |
|---|---|---|
| dimension_id | VARCHAR(20) PK | 维度唯一标识 |
| dimension_name_en | VARCHAR(50) NOT NULL | 英文名称 |
| dimension_name_zh | VARCHAR(50) | 中文名称 |
| dimension_type | ENUM('checkbox','range','color_swatch','size_grid','radio','search_list') | 前端展示类型 |
| source_type | ENUM('attribute','brand','series','price','condition','size_system') | 数据源类型 |
| source_config | JSON | 各数据源类型的特有配置（尺码体系配置、价格分档等） |
| value_mapping | JSON | 值归一化规则（attribute类型用）；含 normalize / range / color_hex 三种规则 |
| min_fill_rate | DECIMAL(3,2) DEFAULT 0.30 | 最低填充率阈值（低于此值前台隐藏） |
| status | ENUM('active','inactive') | 启用 / 停用 |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 最后更新时间 |

**filter_dimension_source 表**（attribute类型的多源绑定）

| 字段 | 类型 | 说明 |
|---|---|---|
| id | BIGINT PK | 自增主键 |
| dimension_id | VARCHAR(20) FK | 所属筛选维度 |
| attribute_id | VARCHAR(20) FK | 关联的 attribute_def ID |
| priority | INT DEFAULT 0 | 同维度下多源优先级（值大优先） |
| UNIQUE | (dimension_id, attribute_id) | 防止重复绑定 |

**fc_filter_config 表**

| 字段 | 类型 | 说明 |
|---|---|---|
| id | BIGINT PK | 自增主键 |
| fc_id | VARCHAR(20) FK | 所属 Collection |
| dimension_id | VARCHAR(20) FK | 引用的筛选维度 |
| display_name_en | VARCHAR(50) | 在本 Collection 中的展示名称（覆盖维度默认名称） |
| sort_order | INT DEFAULT 0 | 筛选面板中的排列顺序 |
| is_collapsible | BOOLEAN DEFAULT TRUE | 是否可折叠 |
| default_expanded | BOOLEAN DEFAULT TRUE | 默认是否展开 |
| is_quick_filter | BOOLEAN DEFAULT FALSE | 是否作为 Quick Filter Chip |
| quick_filter_label | VARCHAR(50) | Quick Filter 的标签文本 |
| quick_filter_preset | JSON | Quick Filter 预设条件，如 `{"price_max": 500}` |
| status | ENUM('active','inactive') | 是否在本 Collection 中启用 |
| UNIQUE | (fc_id, dimension_id) | 同一维度在一个 Collection 中只能配置一次 |

### 6.3 业务规则汇总（快速索引）

| # | 规则 | 所在章节 |
|---|---|---|
| R-01 | Collection 无层级嵌套，扁平结构，展示顺序由 Navigation 模块控制 | §1.1 |
| R-02 | 商品粒度为 listing 级别，不按 SPU 聚合 | §1.6 |
| R-03 | 自动选品 / 手动选品两种模式互斥 | §2.3 |
| R-04 | 条件构建器同一组内同一字段可多条（OR语义），跨分组为 AND/OR 由分组逻辑决定 | §2.1 |
| R-05 | URL Slug 全局唯一，只允许 a-z0-9-，修改 Slug 建议同步配置 301 重定向 | §2.3 |
| R-06 | Collection 状态只有 active / archived 两态，下架保留配置 | §2.4 |
| R-07 | All Products：不可删除、不可下架、商品来源不可修改 | §2.4 |
| R-08 | 自动选品商品下架时，同步清除 pin 记录（不持久化） | §2.8 |
| R-09 | 手动选品商品下架时，fc_manual_product 记录保留，前端灰显 | §2.8 |
| R-10 | 后台商品列表顺序 = 前端实际展示顺序（WYSIWYG） | §2.4 |
| R-11 | 筛选参数 URL 加 noindex 防止搜索引擎收录 | §2.6 |
| R-12 | Quick Filter 商品数为 0 时前端不展示该 Chip | §2.6 |
| R-13 | 筛选维度填充率低于阈值时，前台整个维度分组不展示 | §2.5 |
| R-14 | 收藏 MVP 阶段存 localStorage，不强制登录 | §2.9 |
| R-15 | 后台类目（backend_category）不作为筛选维度数据源，只用于自动选品规则的条件字段 | §2.5 |
| R-16 | 品牌页复用 Collection（source_type=rule + brand 条件 + linked_brand_id），不新建 /brands/ 路由；品牌信息以品牌管理为唯一数据源 | §2.10 |
| R-17 | 品牌页不做品类筛选；MVP 不单独承载品类×品牌交叉中长尾，Phase 2 可升格 | §2.10 |
| R-18 | 空品牌页（0 件在售）noindex 且不进 sitemap，有货自动转 index | §2.10 |
| R-19 | 商品可同属多个 Collection；PDP 面包屑与 BreadcrumbList schema 恒定取「主归属 Collection（primary_collection）」，不随用户来路变（广告直链/搜索/外链均一致）。主归属优先取品类 Collection。`primary_collection` 字段归商品/PDP 侧，需与商品系统对齐 | §2.10、SEO 合集 §2.2.1 |

---

*文档结束*

*关联文件：*
- *后台原型：`海外业务类目管理/原型/looply-类目管理-后台-v0.11.html`*
- *前台原型：`海外业务类目管理/原型/looply-类目页-PC-v0.3.html`*
- *需求分析：`海外业务类目管理/需求分析/分类页设计方案讨论稿.md`*
