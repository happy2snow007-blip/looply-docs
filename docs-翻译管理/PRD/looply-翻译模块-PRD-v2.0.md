# looply 翻译模块 PRD

> 版本：V2.0  
> 日期：2026-06-21  
> 状态：评审版  
> 变更：基于 ER 图 v2.2 和原型 v9 全面重写。移除审核流程和任务管理（本期不做），新增双触发机制、图片资产翻译、多源语言支持、BFF 集成规范

---

## 一、概述

### 1.1 背景与目标

looply 作为面向全球市场的二手电商平台，需要将商品信息、页面文案、通知模板、法律文档等内容翻译为多种目标语言，以支撑多国销售。

翻译模块是 looply 的基础能力模块，为所有业务模块提供统一的多语言翻译服务。

**核心目标**：

1. 统一翻译管理后台，运营可集中管理所有业务内容的翻译
2. AI 自动翻译为主，人工修正为辅，无审核环节，追求翻译效率
3. 注册表模式接入，各业务模块按需注册可翻译字段，翻译模块不感知业务细节
4. 术语表保证品牌名、专业术语在所有语言中的翻译一致性

### 1.2 本期不做

| 不做的事 | 理由 |
|---------|------|
| 审核/审批流程 | 本期 AI 直译 + 人工可修正，无审核节点 |
| 翻译任务/批量作业管理 | 本期全部自动触发，不做手动创建批量任务 |
| 翻译历史版本 | 只保留当前有效版本，变更通过审计日志追溯 |
| 商家端翻译界面 | 本期只做运营后台 |
| 多渠道差异化翻译 | 所有渠道使用同一份翻译 |
| 语言列表管理 | 语言归属 Market 模块，翻译模块只引用 |
| 翻译设置页面 | AI 翻译模型、提示词模板等参数本期写死代码，不做后台配置界面 |
| Key 导出功能 | 本期只做导入，不做 CSV 导出 |

### 1.3 用户角色

| 角色 | 说明 | 主要操作 |
|------|------|---------|
| 翻译运营 | 负责翻译内容管理和质量修正 | 查看翻译进度、修正翻译、管理术语表 |
| 系统管理员 | 负责翻译模块配置 | 注册可翻译字段（Key 管理）、配置翻译设置 |
| 业务模块（系统） | 推送翻译请求的上游系统 | 自动推送 translation_request |

### 1.4 术语说明

| 术语 | 说明 |
|------|------|
| Key | 可翻译字段的注册标识，对应 translatable_field_config 中一条记录 |
| resource_type | 资源类型标识（如 listing、product、page-home），由业务模块定义 |
| key_type | Key 的存储类型：entity_field（源在业务表）/ static_content（源在翻译模块） |
| 翻译请求 | translation_request 表中的记录，是翻译触发的统一入口 |
| source_hash | 源文本的哈希值，用于检测源内容是否变更 |
| 术语概念 | glossary_concept 中的一条记录，一个源词条目对应多个目标语言译法 |

### 1.5 多语言策略

- **语言标识**：使用 ISO 639-1 语言代码（如 en、fr、de、es、ja）
- **源语言**：不固定为英文。每个商家有自己的默认内容语言（merchant.default_content_language），不同资源的源语言可能不同
- **目标语言**：由 Market 模块管理的已开通语言决定
- **读取时不需要知道源语言**：通过 resource_id + field_name + language_code 即可查询译文
- **RTL 支持**：language 表标记是否从右到左（rtl），前端渲染时据此调整布局方向

---

## 二、数据架构

### 2.1 本地化内容分离原则

平台中的商品/内容数据分为两类：

| 类别 | 存储位置 | 示例 |
|------|---------|------|
| 结构化数据 | 业务表原字段 | 价格、库存、重量、尺寸、brand_id、成色等级 |
| 本地化内容 | 翻译模块管理 | 标题、描述、SEO 文案、CMS 内容、Banner 图、法律文档 |

**判断标准**：该字段的值是否随语言/地区变化？是 → 本地化内容；否 → 结构化数据。

### 2.2 key_type 双类型语义

翻译模块通过 translatable_field_config.key_type 区分两种内容来源：

| key_type | 源内容存储位置 | 翻译内容存储位置 | 触发方式 |
|----------|--------------|----------------|---------|
| entity_field | 业务表（如 product.title） | 翻译模块（仅目标语言） | 业务模块推送 translation_request |
| static_content | 翻译模块（所有语言含源语言） | 翻译模块（所有语言含源语言） | 翻译模块内部生成 translation_request |

**entity_field 规则**：
- 源语言内容始终在业务表中维护，翻译模块不存副本
- 翻译模块只存储目标语言翻译
- 业务模块在资源创建或内容变更时推送 translation_request

**static_content 规则**：
- 源语言内容也存在翻译模块的 translation 表中（language_code = source_language_code）
- 运营在翻译后台直接编辑源语言内容
- 编辑保存时，翻译模块自动为所有目标语言生成 translation_request

### 2.3 翻译状态定义

translation 表的 status 字段只有两个值：

| 状态值 | 中文显示 | 含义 |
|--------|---------|------|
| translated | 已翻译 | AI 或人工翻译完成，当前有效 |
| outdated | 待更新 | 源内容已变更，当前译文可能不准确 |

**"未翻译"不是数据库状态**：未翻译 = translation 表中无对应记录。前端根据"注册字段总数 - 已有翻译记录数"计算未翻译数量。

### 2.4 数据模型概览

本 PRD 数据模型依据翻译模块实体关系图 v2.2，包含 6 张表：

| 实体 | 说明 | 归属 |
|------|------|------|
| language | 语言 | 外部引用（Market 模块） |
| translation_request | 翻译请求 | 翻译模块核心表 |
| translation | 翻译内容 | 翻译模块核心表 |
| glossary_concept | 术语概念 | 翻译模块规则表 |
| glossary_translation | 术语翻译 | 翻译模块规则表 |
| translatable_field_config | 可翻译字段配置 | 翻译模块规则表 |

详细字段定义见：`~/Desktop/海外业务/翻译/实体关系图/looply-翻译模块实体关系图-v2.2.svg`

---

## 三、翻译流程

### 3.1 自动翻译路径

翻译从触发到完成的完整路径：

```
触发 → translation_request(pending)
     → 系统消费 → 调用 AI 翻译
     → 写入 translation 表(status=translated)
     → translation_request(completed)
```

**关键设计**：无中间审核环节。AI 翻译完成后直接标记为 translated，运营可事后修正。

### 3.2 双触发机制

#### 3.2.1 外部触发（entity_field）

触发时机：业务模块在以下场景推送 translation_request：
- 资源创建（新商品上架、新类目添加）
- 资源内容变更（商品标题修改、描述更新）

推送内容：resource_type、resource_id、resource_name、field_name、source_language_code、source_text、source_hash、source_version

#### 3.2.2 内部触发（static_content）

触发时机：运营在翻译后台编辑 static_content 类型的源语言内容并保存时

系统行为：
1. 更新 translation 表中源语言记录的 translated_value
2. 计算新的 source_hash
3. 为所有目标语言自动生成 translation_request（status=pending）

### 3.3 过期检测（outdated）

当源内容变更时，已有译文需要标记为过期：

1. 新的 translation_request 到达
2. 系统比对新 source_hash 与 translation 表中已有记录的 source_hash
3. hash 不同 → 将该 resource_type + resource_id + field_name 下所有目标语言的 translation.status 更新为 outdated
4. 触发自动重新翻译（调用 AI 翻译服务）
5. 翻译完成后 status 更新为 translated

### 3.4 翻译请求消费规则

| 规则 | 说明 |
|------|------|
| 前置校验 | 检查 translatable_field_config 表，resource_type + field_name 必须已注册且 status=active |
| 未注册的请求 | 忽略，status 保持 pending（等待字段注册后再处理） |
| 字段注册触发回扫 | 当 translatable_field_config 新注册字段（status 变为 active）时，系统自动查询并消费所有 resource_type + field_name 匹配的 pending request |
| 幂等性 | 同一 resource_type + resource_id + field_name + source_hash 只处理一次 |
| hash 相同 | 源内容未变更，忽略请求，标记为 completed |
| hash 不同 | 源内容变更，标记旧译文 outdated，触发重新翻译 |

### 3.5 前端读取时的 Fallback 策略

当前端请求某语言的翻译时，按以下优先级返回：

1. translation 表中有对应语言记录且 status=translated → 返回译文
2. translation 表中有对应语言记录且 status=outdated → 返回旧译文（带标记，提示可能过期）
3. 无翻译记录 → 返回源语言原文（entity_field 从业务表取，static_content 从 translation 表源语言记录取）

---

## 四、前端集成

### 4.1 BFF 解析模式

前端不直接调用翻译模块 API。由 BFF（Backend for Frontend）层统一处理多语言解析：

1. 前端请求携带 Accept-Language 头（如 `fr`）
2. BFF 从业务模块获取资源数据（结构化数据 + 源语言内容）
3. BFF 批量查询翻译模块，获取目标语言译文
4. BFF 将译文覆盖到响应的对应字段中返回前端

### 4.2 批量查询接口

翻译模块提供批量查询接口，BFF 一次请求获取多个资源的多个字段翻译：

查询参数：
- resource_type + resource_id 列表
- language_code（目标语言）

返回结构：按 resource_id + field_name 组织的译文 map。

### 4.3 多源语言处理

不同商家的商品可能有不同源语言（如日本商家源语言为 ja，美国商家源语言为 en）。

**读取时透明**：BFF 查询翻译时只需传 resource_id + field_name + 目标 language_code，翻译模块内部通过 translation 表的 source_language_code 字段处理多源语言，调用方无需关心源语言是什么。

---

## 五、功能模块

### 5.1 翻译内容导航

**功能类型**：页面型

**功能描述**

以卡片网格形式展示所有可翻译资源，按业务域分组，运营可快速定位到具体资源进行翻译管理。

**页面元素**

| 元素 | 说明 |
|------|------|
| 域分组标签（Tab） | 全部 / 商品域 / 前端页面 / 通知模板 |
| 语言选择器 | 选择当前查看的目标语言 |
| 搜索框 | 按资源名称搜索 |
| 资源卡片网格 | 每个资源类型一张卡片，显示：资源名称、resource_type、翻译进度（已翻译/总字段数）、待更新数 |

**资源类型列表**

| 域 | resource_type | 显示名称 | 字段数（示例） |
|----|--------------|---------|--------------|
| 商品域 | listing | 渠道商品 | 按实际注册字段 |
| 商品域 | product | 实物商品 | - |
| 商品域 | spu | 标品SPU | - |
| 商品域 | sku | 标品SKU | - |
| 商品域 | category | 类目 | - |
| 商品域 | brand | 品牌 | - |
| 商品域 | series | 系列 | - |
| 商品域 | attribute | 属性 | - |
| 商品域 | attribute_option | 属性选项 | - |
| 商品域 | enum | 成色等级 | - |
| 前端页面 | page-auth | 登录注册 | - |
| 前端页面 | page-home | 首页 | 含图片资产 |
| 前端页面 | page-collection | 集合页 | - |
| 前端页面 | page-pdp | 商详页 | - |
| 前端页面 | page-cart | 购物车 | - |
| 前端页面 | page-checkout | 结账页 | - |
| 前端页面 | page-order-success | 下单成功 | - |
| 前端页面 | page-orders | 订单列表 | - |
| 前端页面 | page-account | 账户中心 | - |
| 前端页面 | page-search | 搜索页 | - |
| 前端页面 | page-nav | 导航栏 | - |
| 前端页面 | page-help | 帮助中心 | - |
| 前端页面 | legal-tos | 服务条款 | - |
| 前端页面 | legal-privacy | 隐私政策 | - |
| 前端页面 | legal-return | 退货政策 | - |
| 前端页面 | legal-cookie | Cookie政策 | - |
| 通知模板 | notif-email | 邮件模板 | - |
| 通知模板 | notif-message | 站内消息 | - |

**操作流程**

1. 运营进入翻译内容页，默认显示"全部"标签
2. 选择目标语言（如 fr 法语）
3. 卡片显示每个资源类型在该语言下的翻译进度
4. 点击某资源卡片 → 进入翻译详情页

**交互说明**
- 卡片进度使用进度条 + 数字（如 12/15）
- 有"待更新"内容的卡片显示橙色角标
- 域分组 Tab 后面显示该域的资源数量（如"商品域 10"）

**UI 关联**
- PC 端：`looply-翻译管理后台原型-v9-antd.html` → 翻译内容导航页

---

### 5.2 翻译详情页（Master-Detail）

**功能类型**：页面型

**功能描述**

左侧展示某资源类型下的所有资源实例列表（Master），右侧展示选中资源的逐字段翻译对照（Detail），支持文本翻译和图片翻译。

**页面布局**

| 区域 | 内容 |
|------|------|
| 左侧面板（Master） | 资源实例列表，显示：资源名称、resource_id、翻译进度条 |
| 右侧面板（Detail） | 选中资源的逐字段翻译，每字段一行：源文本 + 译文输入框 + 操作按钮 |

**左侧面板元素**

| 元素 | 说明 |
|------|------|
| 搜索框 | 按资源名称/ID 搜索 |
| 状态筛选 | 全部 / 已翻译 / 待更新 / 未翻译 |
| 资源列表 | 每行显示：资源名称、翻译进度（如 3/5）、状态色标 |

**右侧面板元素**

| 元素 | 说明 |
|------|------|
| 资源信息栏 | 资源名称、resource_type、resource_id |
| 一键AI翻译按钮 | 对所有未翻译 + 待更新字段执行 AI 翻译 |
| 字段翻译行 | 每个注册字段一行 |

**字段翻译行结构（文本字段）**

| 元素 | 说明 |
|------|------|
| 字段标签 | field_label（如"商品标题"） |
| 源文本 | entity_field：只读显示源语言内容；static_content：TextArea 可编辑 |
| 译文输入框 | TextArea，可编辑 |
| AI翻译按钮 | 对该字段执行 AI 翻译 |
| 状态标签 | 已翻译（绿）/ 待更新（橙）/ 未翻译（灰） |

**字段翻译行结构（图片字段）**

| 元素 | 说明 |
|------|------|
| 字段标签 | field_label（如"首页 Banner"） |
| 源图片预览 | entity_field：只读显示；static_content：可点击重新上传 |
| 译图预览 | 显示目标语言图片缩略图（无则显示占位） |
| 上传按钮 | 上传目标语言图片，获取 CDN URL 写入 translated_value |
| 状态标签 | 同文本字段 |

**static_content 源文本编辑规则**

static_content 类型的字段，源文本区域为可编辑状态：
- 文本字段：源文本显示为 TextArea，运营可直接修改
- 图片字段：源图片区域可点击重新上传
- 保存时：更新 translation 表中源语言记录的 translated_value，重新计算 source_hash，自动为所有目标语言生成 translation_request（触发重新翻译）

**操作流程**

手动编辑译文：
1. 运营在译文输入框中输入/修改内容
2. 点击保存按钮
3. 系统写入 translation 表：translated_value = 输入内容，translation_source = manual，status = translated

单字段 AI 翻译：
1. 运营点击某字段的"AI翻译"按钮
2. 系统调用 AI 翻译服务，传入源文本 + 术语表约束
3. 翻译结果填入译文输入框
4. 系统写入 translation 表：translation_source = ai，status = translated

一键 AI 翻译：
1. 运营点击"一键AI翻译"按钮
2. 系统对所有 status 为"未翻译"或"待更新"的字段批量调用 AI 翻译
3. 结果逐字段写入 translation 表

上传翻译图片：
1. 运营点击图片字段的"上传"按钮
2. 选择本地图片文件
3. 系统上传至 CDN，获取 URL
4. 写入 translation 表：translated_value = CDN URL，translation_source = manual，status = translated

**异常处理**

| 异常场景 | 处理方式 |
|---------|---------|
| AI 翻译服务不可用 | 提示"AI翻译服务暂时不可用，请手动编辑" |
| 保存失败 | 提示"保存失败，请重试"，保留输入内容 |
| 图片上传失败 | 提示"上传失败"，保留原图 |

**UI 关联**
- PC 端：`looply-翻译管理后台原型-v9-antd.html` → 翻译详情页

---

### 5.3 Key 管理

**功能类型**：页面型

**功能描述**

展示所有已注册的可翻译字段（translatable_field_config），支持新增、编辑、导入、导出。

**页面元素**

| 元素 | 说明 |
|------|------|
| 注册 Key 按钮 | 打开注册弹窗 |
| 批量导入按钮 | 打开批量导入弹窗 |
| 搜索框 | 按 resource_type 或 field_name 搜索 |
| key_type 筛选 | 全部 / 业务字段 / 页面文案 |
| 状态筛选 | 全部 / 已激活 / 未激活 / 已废弃 |
| Key 列表表格 | 列见下表 |

**表格列定义**

| 列 | 对应字段 | 说明 |
|----|---------|------|
| Key | resource_type + "." + field_name | 如 "product.title" |
| Key 类型 | key_type | 业务字段 / 页面文案 |
| 字段类型 | field_type | text / image / rich_text |
| 来源/归属 | source_system | 商品中心 / 首页 / 结账页 等 |
| 资源类型 | resource_type + resource_label | 如 "product（商品）"（仅业务字段显示） |
| 字段 | field_name + field_label | 如 "title（商品标题）"（仅业务字段显示） |
| 状态 | status | 已激活 / 未激活 / 已废弃 |
| 操作 | - | 编辑 |

**key_type 枚举值与显示名映射**

| 数据库值 | 中文显示名 | 含义 |
|---------|-----------|------|
| entity_field | 业务字段 | 源内容在业务表，翻译模块只存目标语言翻译 |
| static_content | 页面文案 | 源内容在翻译模块，所有语言（含源语言）均在此维护 |

**注册 Key（弹窗） — 分模式表单**

首选 Key 类型，根据选择展示不同表单：

**模式一：业务字段（entity_field）**

| 字段 | 必填 | 说明 |
|------|------|------|
| key_type | 是 | 固定：业务字段 |
| source_system | 是 | 来源模块（商品中心 / 类目中心 / 品牌中心 等） |
| resource_type | 是 | 实体类型标识，如 product |
| resource_label | 是 | 实体类型显示名，如"商品" |
| field_name | 是 | 字段标识，如 title |
| field_label | 是 | 字段显示名，如"商品标题" |
| field_type | 是 | 下拉：text / image / rich_text |
| Key 名称（自动） | — | 自动拼接：resource_type.field_name（只读展示） |

**模式二：页面文案（static_content）**

| 字段 | 必填 | 说明 |
|------|------|------|
| key_type | 是 | 固定：页面文案 |
| source_system | 是 | 归属页面（首页 / 商详页 / 购物车 / 结账页 等） |
| field_name | 是 | Key 名称，如 hero.title（完整 Key = 页面前缀 + 名称） |
| field_label | 是 | 字段显示名，如"Banner 标题" |
| field_type | 是 | 下拉：text / image / rich_text |
| 源文本 | 是 | 输入源语言原文（文本）或上传源图片（图片） |

**校验规则**

| 规则 | 说明 |
|------|------|
| resource_type + field_name 联合唯一 | 不能重复注册 |
| resource_type 格式 | 小写字母、数字、连字符、下划线，最大 50 字符 |
| field_name 格式 | 小写字母、数字、下划线、点号，最大 100 字符 |

**批量导入**

支持 CSV 格式导入，模板包含所有必填字段。导入后显示：成功数 / 失败数 / 失败明细。

**UI 关联**
- PC 端：`looply-翻译管理后台原型-v9-antd.html` → Key管理页

---

### 5.4 术语表管理

**功能类型**：页面型

**功能描述**

管理术语概念和各语言标准译法。术语规则在 AI 翻译时自动应用，保证翻译一致性。

**页面布局**

左侧为术语概念列表，右侧为选中概念的各语言译法（与翻译详情页类似的 Master-Detail 结构）。

**左侧列表元素**

| 元素 | 说明 |
|------|------|
| 添加术语按钮 | 打开添加弹窗 |
| 搜索框 | 按源词搜索 |
| 规则筛选 | 全部 / 禁译词 / 强制术语 |
| 术语列表 | 每行：源词、规则类型标签、翻译覆盖率 |

**右侧详情元素**

| 元素 | 说明 |
|------|------|
| 源词信息 | 源词、规则类型、使用场景说明、状态 |
| 编辑按钮 | 编辑源词信息 |
| 各语言译法表格 | 列：目标语言、标准译法（可编辑）、状态 |
| 保存按钮 | 保存所有修改 |

**术语规则类型**

| 枚举值 | 中文 | AI翻译约束 |
|--------|------|-----------|
| do_not_translate | 禁译词 | 所有语言保留原文不翻译 |
| mandatory | 强制术语 | 必须使用指定译法 |

**添加术语（弹窗）**

| 字段 | 必填 | 说明 |
|------|------|------|
| source_term | 是 | 源术语（如 "looply"） |
| source_language_code | 是 | 源语言 |
| rule_type | 是 | 规则类型 |
| context | 否 | 使用场景说明 |

**校验规则**

| 规则 | 说明 |
|------|------|
| source_language_code + source_term 联合唯一 | 同一源语言下源词不能重复 |
| source_term 最大 200 字符 | - |
| translated_term 最大 500 字符 | - |

**UI 关联**
- PC 端：`looply-翻译管理后台原型-v9-antd.html` → 术语表管理页

---

---

## 六、术语管理

### 6.1 术语在翻译中的应用

AI 翻译时，系统自动将术语表规则注入翻译请求：

1. 查询 glossary_concept 表中 status=active 的所有术语
2. 按 rule_type 组织约束指令：
   - do_not_translate → 告知 AI 保留原文
   - mandatory → 告知 AI 必须使用指定译法
3. 将约束指令附加到翻译提示词中

### 6.2 术语覆盖率

术语的翻译覆盖率 = 该概念已有 active 译法的目标语言数 / 系统已开通目标语言总数

- 禁译词：显示"自动锁定"（无需人工翻译）
- 强制术语：显示覆盖率（如 3/5），提醒运营补齐缺失语言

### 6.3 术语状态管理

| 操作 | 效果 |
|------|------|
| 废弃术语 | glossary_concept.status = deprecated，AI 翻译不再应用该规则 |
| 废弃单条译法 | glossary_translation.status = deprecated，该语言不再约束 |
| 恢复术语 | status 改回 active，规则重新生效 |

---

## 七、系统边界

### 7.1 系统定位

翻译模块是 looply 的多语言基础设施层，定位为"翻译内容的统一管理和分发中心"。

### 7.2 边界判断原则

- 归本模块：与多语言翻译内容的存储、触发、执行、查询直接相关的能力
- 不归本模块：语言本身的管理、业务数据的管理、前端渲染逻辑

### 7.3 归属判定

| 能力项 | 归属 | 说明 |
|--------|------|------|
| 翻译内容存储和查询 | ✅ 翻译模块 | 核心职责 |
| AI 翻译执行 | ✅ 翻译模块 | 调用 AI 服务翻译文本 |
| 翻译过期检测 | ✅ 翻译模块 | 通过 source_hash 对比 |
| 术语表管理 | ✅ 翻译模块 | 翻译质量保障 |
| 可翻译字段注册 | ✅ 翻译模块 | 注册表模式核心 |
| static_content 源内容编辑 | ✅ 翻译模块 | UI文案等内容在此维护 |
| 语言列表管理 | ❌ Market 模块 | 翻译模块只引用 |
| 国家/地区管理 | ❌ Market 模块 | - |
| 商品数据管理 | ❌ 商品模块 | 翻译模块不感知业务实体细节 |
| 前端多语言渲染 | ❌ 前端/BFF | 翻译模块只提供数据 |
| CDN 图片存储 | ❌ 基础设施 | 翻译模块只存 CDN URL |

### 7.4 对外接口

| 接口方向 | 对接方 | 交互方式 |
|---------|--------|---------|
| 入（接收） | 各业务模块 | 业务模块写入 translation_request 表 |
| 出（提供） | BFF 层 | 批量查询翻译接口（resource_ids + language_code → 译文 map） |
| 引用 | Market 模块 | 读取 language 表获取已开通语言列表 |

---

## 附录

### A. 设计稿索引

| 页面 | 设计稿 |
|------|--------|
| 翻译内容导航 | `looply-翻译管理后台原型-v9-antd.html` → 翻译内容导航页 |
| 翻译详情（Master-Detail） | `looply-翻译管理后台原型-v9-antd.html` → 翻译详情页 |
| Key 管理 | `looply-翻译管理后台原型-v9-antd.html` → Key管理页 |
| 术语表管理 | `looply-翻译管理后台原型-v9-antd.html` → 术语表管理页 |

原型文件：`~/Desktop/海外业务/翻译/原型/looply-翻译管理后台原型-v9-antd.html`

### B. 实体关系图

`~/Desktop/海外业务/翻译/实体关系图/looply-翻译模块实体关系图-v2.2.svg`

### C. 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| V1.0 | 2026-05-15 | 初版 |
| V1.1 | 2026-05-18 | 调整章节顺序 |
| V2.0 | 2026-06-21 | 全面重写：移除审核流程和任务管理，新增双触发机制、图片资产翻译、多源语言支持、BFF 集成规范；数据模型从 8 表精简为 6 表 |
