# looply 多语言模块 PRD（v3.2 能力迭代）

> **版本**：V3.2 | **日期**：2026-07-23 | **状态**：评审版
>
> **本版定位**：在 v3.1 基础上新增两项能力并追认一项已实现能力，解决"商详接多语言"暴露的 v3.1 单层模型缺口。**本文档为增量迭代——只写新增/变更部分；未列章节（翻译流程、术语管理、Fallback、系统边界等）完全沿用 v3.1。**
>
> **本版新增/变更**：
> 1. **能力一 · 翻译资源目录（建卡 + 域元数据）**：把散落的 `resource_type` 开放字段升级为显式建卡（`translation_resource`）+ 域元数据（`translation_domain`）。
> 2. **能力二 · 页面聚合（`resource_group`）**：把一个 C 端页面下的多个资源卡片聚合成一个导航单元，解决"动态套动态"导致的卡片零散。
> 3. **能力三 · 静态文案后台管理（追认已实现）**：`storage_mode` 区分"翻译中心 / 语言包"，静态文案语言包落地 + 后台可查改。
>
> **配套产物**：ER v2.4（`looply-多语言模块实体关系图-v2.4.svg`）· 接入规范（产品版）v3.2 · 后台原型 v13（`looply-多语言管理后台原型-v13-antd.html`）
>
> **触发来源**：商详接多语言。商详 CMS 配置内容是"动态套动态"结构（模板/类目容器 → 容器下的字段/等级/展示名），且有"页面静态文案 + 多个自产资源类型"同属一页的诉求——v3.1 的"一个业务对象一张卡、卡内字段平铺"单层模型无法优雅承载（接入规范 v3.1 §4.2 已预判此类超纲）。

---

## 一、背景与能力缺口

### 1.1 v3.1 的模型边界

v3.1 的翻译中心是**单层结构**：`domain（域）→ resource_type（卡片，开放字段）→ resource_id（实例）→ field_name（字段，平铺）`。绝大多数业务落在此范围。

### 1.2 商详接入暴露的三个缺口

| # | 缺口 | 现象 | 本版能力 |
|---|------|------|---------|
| 1 | **resource_type 无显式登记** | 卡片只是 `translatable_field_config` 里的一个开放字符串，没有卡片级实体承载展示名/域/对接状态，无法"先建卡再注册字段" | 能力一：建卡 `translation_resource` |
| 2 | **一页多资源会散成多张卡** | 商详有 1 类静态 + 4 类 CMS 动态资源，按 v3.1 会散成 5 张互不关联的卡扔在"前端页面"域，运营认不出同属商详页（接入规范 §4.2 警示的"卡片零散"） | 能力二：页面聚合 `resource_group` |
| 3 | **静态文案后台无处管理** | 静态文案走语言包，v3.1 规范 §三定为"后台不碰"，但实际有"运营能在后台查看/修改静态文案多语言值"的诉求（已实现） | 能力三：`storage_mode` + 后台管理口径 |

---

## 二、能力一：翻译资源目录（建卡 + 域元数据）

### 2.1 建卡 translation_resource

翻译中心新增一级对象 **翻译资源（卡片）**：一张卡 = 一个 `resource_type`（一个业务实体类型，或一类页面文案）。运营按"**域 → [分组] → 卡片 → 实例 → 字段**"定位维护。

**卡片字段**（详见 ER v2.4）：

| 字段 | 说明 |
|------|------|
| resource_type | 资源类型编码（主键），如 `pdp_template` / `catalog_brand` / `page-pdp` |
| display_name | 卡片展示名，如"商详-鉴定认证" |
| domain | 归属域（FK → translation_domain） |
| group_code | 聚合归属（FK → resource_group，可空 = 独立卡） |
| key_type | 卡片类型：`entity_field`（业务字段）/ `static_content`（页面文案） |
| storage_mode | 存储方式：`translation_table`（翻译中心）/ `language_pack`（语言包）——见能力三 |
| source_system | 来源系统 / 归属模块 |
| integration_status | 对接状态：`connected` 已对接 / `pending` 待对接 / `placeholder` 占位 |
| sort_order | 排序权重 |

### 2.2 域元数据 translation_domain

新增 **翻译域**：`domain`（编码）+ `domain_name`（显示名，如 商品域 / 前端页面 / 通知模板）+ `sort_order`。翻译中心导航页按域分 Tab **由后端元数据驱动**，不再前端硬编码。

### 2.3 建卡与字段注册的关系（先建卡再注册）

- 业务模块上线前须**先建卡**（在 `translation_resource` 写入 resource_type + display_name + domain + [group_code]），**再注册字段**（`translatable_field_config`，resource_type 为 FK 指向建卡）。
- **未建卡则源文写入被拒**（防止产生游离译文）。
- `translatable_field_config` 本版改造：`resource_type` 由开放字段升为 **FK → translation_resource**；卡片级属性（display_name / key_type / source_system）上移至 `translation_resource`；字段配置表只保留字段级属性（config_id / resource_type FK / field_name / field_label / field_type / sort_order / status）。

### 2.4 建卡方式（本期）

- **本期建卡走 migration / config**（由开发在业务模块联调阶段执行），**不做运营自助建卡界面**。
- 运营在 Translation 导航页**查看**卡片（含对接状态），在翻译详情页维护译文；不新增/编辑卡片本身。
- 运营自助编辑/排序卡片、分组、域 → 见 §九 后续诉求。

---

## 三、能力二：页面聚合（resource_group）

### 3.1 概念与模型

新增 **资源分组（页面聚合）**：把一个 C 端页面下的多个 `resource_type` 卡片聚合成一个**导航单元**。

**分组字段**：`group_code`（主键，如 `pdp`）+ `group_name`（显示名，如"商详页"）+ `domain`（归属域）+ `sort_order` + `status`。`translation_resource.group_code` 指向它。

> **数据层 vs 展示层**：数据层仍是 N 个独立 `resource_type`（各自建卡、各自注册字段、各自单层）；聚合只发生在**导航展示层**——把同 `group_code` 的卡片合并为一张聚合卡。不破坏 v3.1 的单层字段模型。

### 3.2 Translation 导航页：聚合卡

| 元素 | 说明 |
|------|------|
| 聚合卡 | 同一 `group_code` 的成员卡片，在导航页合并为**一张聚合卡**（卡名 = group_name，如"商详页"），不再各自出卡 |
| 进度 | 聚合卡进度 = 各成员进度合计 |
| 对接状态 | 聚合卡对接状态由成员汇总（有占位/待对接成员时整体标注对应状态） |
| 独立卡 | `group_code` 为空的资源仍作**独立卡**展示（向后兼容，v3.1 所有卡片不受影响） |

### 3.3 翻译详情页：子导航切换成员

点进聚合卡 → 详情页顶部用**子导航（分组切换）**在各成员 `resource_type` 间切换；每个成员内部仍是 Master（实例）- Detail（平铺字段）标准结构。子导航同时标注该成员的 `resource_type`、配置粒度、`storage_mode`（翻译中心 / 语言包）。

> 对应原型 v13：Translation 导航页"商详页"聚合卡 → 翻译详情页 5 分组（页面文案 / 鉴定认证 / 成色等级 / 成色展示名 / 属性展示名）子导航。

### 3.4 向后兼容

- 未定义 `resource_group` 的资源、v3.1 既有全部卡片，**行为不变**（独立卡）。
- 聚合是可选的组织层，不强制。

### 3.5 边界（本期）

- **本期分组配置走 migration / config**（哪些 resource_type 归哪个 group、排序），不做运营自助编辑分组界面。
- 运营自助编辑/排序分组 → 见 §九 后续诉求。

---

## 四、能力三：静态文案后台管理（追认已实现）

### 4.1 storage_mode：翻译中心 vs 语言包

`translation_resource.storage_mode` 区分内容落地方式：

| storage_mode | 含义 | 落地存储 | 后台行为 |
|--------------|------|---------|---------|
| `translation_table` | 动态业务内容 | translation 表 | 保存写入翻译服务，触发 AI 翻译 |
| `language_pack` | 页面静态文案 | 前端语言包 | 多语言后台提供查看/修改面，保存后同步回语言包 |

### 4.2 静态文案：语言包落地 + 后台查改

- 静态 UI 文案技术上仍走前端语言包落地（能力已实现）。
- 多语言后台提供**查看/修改面**：运营能在后台管理静态文案的多语言值，保存后同步回语言包（同步机制由技术方案定）。
- 对齐 v3.1 §2.2 static_content 参考方案（"运营能在后台动态管理前端页面文案的多语言内容，实现方式技术团队定"）。

### 4.3 与动态内容的差异（防混淆）

| 维度 | 动态业务内容（translation_table） | 静态文案（language_pack） |
|------|--------------------------------|--------------------------|
| 落地存储 | translation 表 | 语言包 |
| 源文写入 | 业务后台/CMS 保存时写翻译服务 | 后台编辑保存 → 同步语言包 |
| 翻译 | 保存触发 AI 翻译 | 同样可翻译（源文/译文可编辑） |
| 后台界面 | 同一套翻译详情界面，`storage_mode` 标注"翻译中心 / 语言包"区分 | 同左 |

### 4.4 展示位置（重要）

- 静态文案的后台查看/修改在 **Translation 翻译详情页**（作为聚合卡里的"页面文案"分组，或独立卡），**不在 Key 管理页**。
- **Key 管理页只读**，且**页面静态语言包字段不进 Key 管理列表**（Key 管理只读查看业务模块注册的翻译 key）。

---

## 五、数据模型增量（对应 ER v2.4）

| 表 | 变更 | 说明 |
|----|------|------|
| `translation_domain` | **新增** | 域元数据：domain / domain_name / sort_order / status |
| `resource_group` | **新增** | 页面聚合：group_code / group_name / domain(FK) / sort_order / status |
| `translation_resource` | **新增** | 建卡：resource_type(PK) / display_name / domain(FK) / group_code(FK,可空) / key_type / storage_mode / source_system / integration_status / sort_order |
| `translatable_field_config` | **改造** | resource_type 由开放字段 → FK→translation_resource；display_name / key_type / source_system 上移至 translation_resource；保留 config_id / resource_type(FK) / field_name / field_label / field_type / sort_order / status |
| `translation` | 不变 | resource_type 仍为 EAV 字段，逻辑引用 translation_resource.resource_type |
| `language` / `glossary_concept` / `glossary_translation` | 不变 | 沿用 v3.1 |

> `sort_order` 已在三张新表预留，为将来"卡片/分组/域 编辑排序"（§九 后续诉求）铺好数据基础，届时无需再改 ER。

---

## 六、后台改动点（对应原型 v13）

| 页面 | 改动 | 状态 |
|------|------|------|
| Translation 导航页 | 同一 group_code 成员合并为聚合卡；域 Tab 由 domain 元数据驱动 | 原型 v12/v13 已体现 |
| 翻译详情页 | 聚合卡进入后顶部子导航切换成员；标注 resource_type / 粒度 / storage_mode | 原型 v12/v13 已体现 |
| Key 管理页 | **本期只读不改**：只读查看业务模块注册的翻译 key，静态语言包字段不进列表，无手动注册/编辑（对齐 v1 实现） | 原型 v13 已对齐 |

---

## 七、接入规范 v3.2 升版要点

本版能力做成通用后，接入规范（产品版）同步升 v3.2（详见 `looply-多语言接入规范-产品版-v3.2.md`）：

1. **§4.2**："动态套动态"从"超纲、提需求" → "**页面聚合已支持**：容器级拆成独立 resource_type 分别建卡，再用 resource_group 聚合到一个页面单元；接入方声明聚合组即可"。
2. **§三 / §七 A 段**：静态文案从"仅语言包、后台不碰" → "**语言包落地 + 后台可查改**"。

---

## 八、依赖与风险

| 风险/依赖 | 影响 | 应对 |
|----------|------|------|
| 建卡能力（migration + 域元数据）未上线 | 业务模块无法建卡、无法注册字段 | 列为业务接入硬前置 |
| 聚合成员归属/排序靠 config，配置错漏 | 聚合卡成员缺失或顺序乱 | 上线前核对各 group 成员清单 + sort_order |
| 静态文案语言包同步机制未定 | 后台改了不同步/延迟 | 同步机制由技术方案定，产品声明"保存后同步语言包"诉求 |
| 向后兼容 | v3.1 既有卡片行为改变 | 未归组资源保持独立卡，回归验证既有卡片 |

---

## 九、版本规划

### 9.1 本期（v3.2）

- 建卡（translation_resource）+ 域元数据（translation_domain）
- 页面聚合（resource_group）：导航聚合卡 + 详情子导航
- storage_mode + 静态文案后台管理口径（追认已实现）
- translatable_field_config 改造（resource_type 升 FK）
- 建卡/分组/域 **靠 migration/config 落地**，Key 管理页只读不改

### 9.2 后续诉求（本期不做）

| 方向 | 说明 | 触发 |
|------|------|------|
| **卡片/分组/域 运营编辑 + 排序管理** | 运营自助增改删、排序 translation_resource / resource_group / translation_domain 的管理控制台；ER 已预留 sort_order，届时只加运营界面 | 单独立项，出独立原型 + PRD，与商详接多语言解耦 |
| Key 管理页升级为可维护 | 若上述编辑能力落地，Key/建卡管理页从只读升级 | 跟随上一条 |

---

## 附录

### A. 配套产物索引

| 产物 | 文件 |
|------|------|
| ER 图 v2.4 | `实体关系图/looply-多语言模块实体关系图-v2.4.svg` |
| 后台原型 v13 | `原型/looply-多语言管理后台原型-v13-antd.html` |
| 接入规范 v3.2 | `looply-多语言接入规范-产品版-v3.2.md` |
| 上游触发 | `商详/PRD/looply-商详页多语言接入-PRD-v1.2.md`、`商详/looply-商详接多语言-实施计划-v1.0.md` |

### B. 与 v3.1 的关系

本文档为 v3.1 的能力增量。未在本文档出现的章节（一~九除新增外的翻译流程、术语管理、Fallback、系统边界等）**完全沿用 v3.1**。
