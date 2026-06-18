# looply 商详页系统 - 变更日志

## V1.6 — 2026-06-18

**二轮对齐 Figma PC/APP 设计稿 + CMS 原型 v3，PRD-原型交叉校验**

### 命名统一
- Trust Statement 和 Certified Authentic 合并为 Certified Authentic（全局 32+ 处替换）

### 变更
- Certified Authentic 徽章改为纯 CMS 驱动（移除 is_authenticated 依赖，有 CMS 配置即展示）
- Condition 成色详细信息从 4 个固定字段改为 CMS 类目级配置（同 Description 模式，定义展示名+绑定数据源+排序）
- 翻译 Fallback 从四级简化为二级（平台默认语言→原文）
- 成色等级明确为商品系统固定枚举（CMS 模板仅控制前台展示，不影响商品录入）
- Size Guide 数据来源从"单模板"改为"多模板+按尺寸比值自动匹配"
- 面包屑品牌/品类跳转本期写死 www.looply.com（依赖 collection 模块）
- Gallery 图片尺寸约束改为以 Figma 设计稿为准

### 新增
- 非促销划线价 compare_at_price（listing 级，3 级优先：促销价 > compare_at_price > 不展示）
- Cookie 未登录收藏/加购支持
- Condition 成色详细信息展示名为空时只展示值的规则
- 同一类目数据源字段互斥（最多选一次）
- Condition 模块开关关闭时类目级配置仍可编辑

### CMS 原型同步
- Condition 面板新增类目级成色详细信息配置（规则表+编辑/新增/删除弹窗+预览）
- 数据源 Select 加互斥
- 模块开关关闭时模板级置灰+类目级正常

### 风险项降级
- Condition 等级 ER 扩展从"grade 字段迁移"降为"CMS 域新增展示配置表，无迁移风险"

---

## V1.5 — 2026-06-17

**对齐 Figma 设计稿 + CMS 原型 v3**

### 新增
- Certified Authentic 鉴定认证模块（2.9 节，CMS 模板级配置，含标题/描述/详细说明半层弹窗）
- PDP 模板概念（2.3 节重写，模板关联类目，模板级管理 Certified Authentic + Condition，类目级管理 Description）
- Condition 分段进度条和 Condition Guide 弹窗（2.10 节）
- 成色等级前台展示从固定 4 级扩展为模板可配置展示等级集合（默认 5 级：Like New / Excellent / Very Good / Good / Fair，商品系统 grade 枚举不变）

### 变更
- Description CMS 配置从「类目 > 品牌 > 系列」三级继承简化为仅按类目配置（2.11 节）
- 商品描述文案从独立模块合并到 Description 折叠区（属性表下方展示）
- CMS 变更记录新增模板管理/模块管理操作类型

### 移除
- CTA 按钮区的支付方式图标列表（Figma 设计稿已不包含，对齐删除）

### 更新
- 设计稿引用从 HTML 交互说明切换为 Figma 在线设计稿
- CMS 后台原型引用更新为 v3

### 评审修正
- Condition 模块开关增加例外说明（仅控制进度条+Guide，质检信息保留）
- 进度条色值删除改为以 Figma 为准
- 等级数量删除 3-6 限制
- 补充等级删除后匹配不上的处理（静默隐藏）
- Size Guide 默认值简化为统一开启+前台无数据自动隐藏
- 变更记录筛选缩减为模板+模块 2 个维度
- Certified Authentic 补充保存非空校验
- Certified Authentic 编辑改为页面内直接编辑（去掉弹窗），详细说明字段改为富文本编辑器

---

## V1.4 — 2026-06-11

**新增 CMS 后台业务规则（2.3 节扩展）**

### 新增
- 作用域唯一性约束（重复报错）
- 保存行为（保存即生效，无草稿态）
- 筛选联动规则（选择即筛选 + 品牌级联）
- 模块开关行为（关闭=完全隐藏，即时生效）
- Size Guide 默认值策略（按类目区分默认开/关）
- 配置变更记录（永久保留，4 种操作类型）
- 操作权限（当前不限，预留扩展）
- 属性展示名翻译流程（自动入队列）

### 完善
- 继承机制补充边界（所有层级删除→不展示）

### 更新
- CMS 后台原型引用改为 antd 版

---

## V1.3 — 2026-06-10

### 修正
- 收藏相关数据源从直查 user_wishlist 改为调用收藏模块接口（收藏模块独立设计，对外提供查询能力）
- 移除 SEO 章节（SEO 为独立模块）
- 商品描述仅取 listing.listing_description，移除 product.description 兜底
- 库存可售判断改为调用库存服务可售库存查询接口，不暴露内部计算公式

---

## V1.2 — 2026-06-10

**全量交叉对齐商品/Market/翻译/库存/汇率五模块最新方案**

### 修正
- 成色字段从 product 表移至 product_inspection 表
- supplement_notes 替代 additional_desc
- Gallery 图片从 JSON 数组改为 product_image 独立表
- 汇率从直查表改为调汇率模块统一接口
- 语言/货币列表增加 status=active 过滤和 priority 排序
- 新增货币符号位置 symbol_position
- 库存可售状态改为调用库存服务查询接口

### 新增
- 翻译 Fallback 四级优先策略
- RTL 布局支持
- 收藏人数展示
- 度量单位本期策略说明

---

## V1.1 — 2026-06-10

**对齐商品系统 PRD v1.7**

### 变更
- Condition 折叠区全面重写（成色等级 4 级、4 个文本字段替代结构化质检项、删除 CMS 配置）
- listing_status 简化为两状态
- 鉴定信息字段扩展
- 尾差规则从"待设计"更新为引用商品系统 PRD 2.8.1
- 新增展示标题术语

---

## V1.0 — 2026-05-26

**初版**

- 定义商详页 12 个模块的数据来源、取值规则和边界处理
