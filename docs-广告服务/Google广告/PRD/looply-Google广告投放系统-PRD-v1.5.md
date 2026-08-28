# Looply Google广告投放系统 PRD

> 文档版本：v1.5  
> 状态：一期开发基线  
> 日期：2026-08-28  
> 适用范围：Looply已启用市场的Google Merchant Center与Google Ads能力；一期覆盖美国与香港  
> 基线原则：开发、测试依据本文件实施Google广告能力；GMC Custom Label字段生成、清除、清单和验收以《Looply自建站 GMC Custom Label 规则（AI Coding 执行版 v2.6）》为唯一专项依据。旧三渠道PRD、旧技术方案、归因时序图和旧ER图仅作历史追溯；冲突时以本文件及上述专项规则为准。

## 一、概述

### 1.1 背景与目标

Looply经营高客单价、长决策周期的一物一码二手商品。Google广告一期需要形成四条可独立验证的链路：把合格商品可靠同步至Google Merchant Center；把网站商品行为发送给Google Ads用于零售动态再营销；把最终支付成功通过浏览器和服务端互补发送到同一个Google Ads购买转化操作；退款成功后修正原购买转化价值。

本PRD只定义Google广告能力，不承载网站分析、其他广告渠道、进站触点、身份缝合、广告归因、广告花费和ROAS。Google点击来源上下文由独立“数据来源”需求提供，本系统只消费结果。

### 1.2 一期目标

1. 使用Google Merchant API v1，按Market已启用语言组合同步当前已启用市场商品，覆盖首次同步、增量更新、售罄、下架删除、诊断回拉和失败恢复；当前已启用市场包括美国与香港，代码不得写死市场范围。
2. 提供属性映射与三级类目到Google商品类目ID映射后台，配置保存后立即生效并记录操作日志。
3. 在区域投递门控允许时加载Google Tag Manager（GTM），由GTM发送五类零售动态再营销事件；一期不接入CMP、不读取用户同意状态。
4. 支付最终成功后，由GTM发送Google Ads Purchase Conversion；服务端Data Manager固定作为同一个网站Purchase Conversion Action的额外数据源。
5. 部分退款执行RESTATEMENT，全额退款执行RETRACTION，使Google Ads转化价值与实际剩余支付价值一致。
6. 使用事务Outbox、主动幂等、重试、死信、告警和对账保证商品、购买和退款链路可恢复、可审计。

### 1.3 成功指标

| 指标 | 一期目标 | 统计口径 |
|---|---:|---|
| 合格商品首次提交成功率 | ≥99.5% | 排除Google账号冻结和平台服务中断；按商品×语言计数 |
| 下架、售罄、关键链接变化提交时延 | P95≤5分钟 | 业务事实提交至Merchant API请求被接受 |
| 新品及普通字段变化提交时延 | P95≤30分钟 | 商品变化提交至Merchant API请求被接受 |
| 再营销事件重复触发 | 同一页面生命周期为0 | 组件重复渲染、重复监听和接口重复回调不得重复发送 |
| Purchase最终处理率 | ≥99.9% | 区域投递门控允许的Purchase任务最终accepted或明确permanent_failed |
| 重复购买转化 | 0 | 同订单、同Conversion Action不得生成不同交易ID或重复逻辑任务 |
| 退款调整准确率 | 100% | Google剩余转化价值等于原购买价值减累计成功退款，不小于0 |
| 可追溯性 | 100% | 任一商品、购买或退款任务可定位来源业务事件、请求摘要、状态和错误 |

### 1.4 用户角色

| 角色 | 职责 | 一期入口 |
|---|---|---|
| Google广告运营 | 管理Merchant Center、Google Ads资产、受众和广告系列 | Google平台后台、内部指标与告警 |
| 广告配置管理员 | 维护属性映射和Google商品类目映射 | 广告投放配置后台 |
| 商品运营 | 维护商品、库存、价格、语言内容和数据质量 | 既有商品后台 |
| 客服/财务 | 发起退款、核对退款金额 | 既有订单和支付系统 |
| 开发/运维 | 配置凭证、处理死信、重试和告警 | 内部受控接口、运维平台 |

### 1.5 一期范围

- Google Merchant Catalog：API主数据源、按Market已启用语言生成的商品资源、增量同步、状态和诊断；`customLabel0`至`customLabel4`按专项打标规则生成。
- Google Ads网站事件：Google Tag Manager、Conversion Linker、动态再营销标签、Purchase Conversion Tracking标签。
- Google Ads服务端Purchase：Data Manager在线转化事件。
- Google Ads退款调整：RESTATEMENT与RETRACTION。
- 区域投递门控、浏览器幂等、服务端幂等、Outbox、任务状态和审计。
- PC端属性映射和类目映射后台；不新增App页面。

### 1.6 明确不做

- 不接入Meta或TikTok的Catalog、Pixel、服务端事件、退款、账号资产和报表。
- 不在本PRD内接入GA4；网站分析事件、GA4 Purchase/Refund和Measurement Protocol由独立GA4 PRD定义。
- 不实现触点创建、Direct判断、30分钟去重、anonymous_id身份缝合、Last-touch或时间衰减归因。
- 不拉取Google Ads花费，不计算ROAS，不提供广告分析BI。
- 不做Google Ads广告系列、预算、出价、创意、Listing Group或受众运营后台。
- 不做复杂受众计算，如事件次数阈值、严格事件顺序、高价值客户、跨设备用户；后续依赖独立数据来源或用户标签需求。
- 不把浏览、搜索、列表或加购事件配置为主要转化；一期唯一主要转化是Purchase。
- 一期商品数据源不提供童装、童鞋，因此本系统不设计儿童尺码到`age_group`的推导规则。
- 不使用Google已停用或进入停用周期的旧商品接口和旧批处理动作。
- 一期不接入CMP、不读取或保存用户Consent/GPC状态，也不提供同意弹窗；CMP、Consent Mode、用户撤回与同意快照在后续版本单独评审接入。

### 1.7 唯一业务决策

| 主题 | 一期唯一决策 |
|---|---|
| Catalog主源 | Merchant API v1，新增和更新均走API类型数据源 |
| 本地化商品ID | `{content_language}~{feed_label}~listing_id`；每个已启用市场语言对应一条独立资源 |
| Google商品ID | `offerId=listing_id`；listing_id永不复用 |
| 配置后台 | 只维护按三级类目的color/material/size单属性映射和三级类目到Google商品类目ID映射；保存立即生效 |
| GMC Custom Label | Looply Feed直接写入`customLabel0`至`customLabel4`；规则、版本化开发清单、清除逻辑、账号级数量控制和验收均引用《Looply自建站 GMC Custom Label 规则（AI Coding 执行版 v2.6）》，不在本PRD重复定义；GMC不配置同名Attribute rules |
| 区域投递门控 | 一期不接CMP、不读取同意状态；由可信地区策略配置决定Google数据处理是否允许。EEA、英国、瑞士为禁止地区：不加载GTM或Google Ads JS，不发送浏览器或服务端广告事件；地区代码和允许名单不得写死在业务代码 |
| 再营销 | 业务页面push标准事件到dataLayer，由GTM向`AW-`目标发送五类零售事件，不依赖GA4受众 |
| Purchase浏览器 | GTM中的Google Ads Conversion Tracking标签为主路径，`transaction_id=order_id` |
| Purchase服务端 | Data Manager固定作为同一网站Conversion Action的额外数据源 |
| Purchase事实源 | 支付渠道验签异步回调第一次把订单推进paid |
| 退款 | 部分退款RESTATEMENT；剩余价值为0时RETRACTION |
| 数据来源 | 只消费独立“数据来源”需求输出的Google点击上下文；本系统不创建触点或归因 |
| 可靠投递 | 商品、购买和退款均使用与业务事实同库同事务的Outbox |
| 市场语言来源 | Market国家管理提供已启用语言、页面语言和站点URL规则；广告系统不预设美国或香港语言集合 |
| 市场绑定 | Google账号、Merchant数据源、`feedLabel`和启用状态为环境初始化配置，不提供后台维护入口 |

### 1.8 术语

| 术语 | 定义 |
|---|---|
| listing | 一件可独立售卖和投放的商品，一物一码 |
| Merchant Catalog | Google Merchant Center中的商品集合 |
| API primary | API是商品新增、更新与删除的正式事实来源 |
| accepted | Google API已接收请求，不代表审核完成或广告已展示 |
| processed | 异步状态或诊断已回拉确认 |
| Google Tag Manager（GTM） | 承载Google Ads浏览器标签、变量和触发器的容器；本PRD不通过GTM接入GA4 |
| dataLayer | 业务页面向GTM发布规范事件对象的浏览器内队列；push本身不代表Google已收到事件 |
| 再营销事件 | 用于建立网站访客和动态商品受众的行为事件，不是主要购买转化 |
| Conversion Action | Google Ads中的转化操作；一期Purchase使用一个WEBPAGE类型操作 |
| Data Manager | Google Ads在线转化的服务端额外数据源 |
| 数据来源 | 独立需求，负责Google点击信息的采集、有效性和订单关联；不承担一期Consent判断 |
| Outbox | 与业务状态变更同事务写入、由异步Worker投递的可靠事件记录 |
| feedLabel | Google Merchant用于区分商品投放版本的配置标签；与`offerId`、`contentLanguage`共同确定商品资源，不等同于页面语言或币种 |
| Market国家管理 | 提供市场国家、法定币种、已启用语言与站点URL规则的外部配置；广告系统只读消费 |

## 二、全局约束

### 2.1 ID规则

1. `listing_id`是Catalog、再营销`items[].id`和购买商品明细的唯一商品ID来源，永久不可复用。
2. `order_id`是Purchase统一交易锚点：浏览器使用`transaction_id`，服务端使用`transactionId`，两者必须相等。
3. `refund_id`标识一次支付渠道确认成功的退款；同一订单多次退款使用不同refund_id。
4. Merchant账号、数据源、Google Ads客户、Conversion Action、OAuth和API版本均来自环境配置，不得硬编码。

### 2.2 市场、语言与币种

每个Market的国家、法定币种、已启用语言和站点URL规则均从Market国家管理读取。Google投放初始化配置仅维护该市场对应的Google资产和`feedLabel`。系统对每个“已启用市场 × 已启用语言”创建一条独立Catalog资源；`contentLanguage`由该语言配置映射，`feedLabel`由该市场Google绑定配置提供。

市场语言未就绪时，只跳过该市场语言资源，不阻塞同市场其他语言或其他市场。禁止以任一语言内容兜底另一语言。每条本地化记录的页面`lang`、标题、描述、价格、库存和结构化数据必须与对应市场语言的Catalog一致。

### 2.3 时间与金额

- 数据库存UTC，平台事件时间使用业务事实发生时间，不使用Worker发送时间。
- Google Ads Purchase value为订单最终实付总额，包含买家实际支付的商品、运费和税，折扣已扣除。
- Google退款调整后的价值等于原Purchase value减累计成功退款，最小为0。
- 金额使用`DECIMAL(18,6)`或更高精度；micros转换禁止使用浮点数。
- 商品Feed的`price.currencyCode`取商品所属Market国家管理的法定币种；若商品价格事实缺失币种或与该市场要求不符，阻断该商品在该市场语言Feed的投递并记录准入问题，不影响其他商品或市场语言。
- Google Ads浏览器事件、服务端Purchase和退款调整均取商品、订单或退款业务事实的`currency_code`；不得写死或静默替换为某一市场币种。订单和退款发生时冻结币种快照。

### 2.4 区域投递门控

一期不接入CMP，不读取、保存或判断用户Consent/GPC状态。每次页面初始化和支付/退款事实创建时，系统从可信服务端下发或冻结的地区策略读取`google_measurement_allowed`；不得以浏览器自报地区或业务代码内的国家常量判断。EEA、英国、瑞士在该策略中必须为`false`：浏览器不初始化`window.dataLayer`、不加载GTM容器或Google Ads JS、不push Google Ads事件；服务端Purchase与退款调整任务标记`suppressed_by_region`且零网络请求。策略允许时，浏览器只初始化一次并发送新产生事件；服务端直接按原可靠投递规则发送。

地区策略必须可配置、版本化和审计，新增市场或法律要求变化仅修改受控配置，不改业务代码。Google Merchant商品同步不涉及网站用户行为数据，不受本门控影响。后续CMP版本再增加Consent Mode、用户撤回、GPC和同意快照；不得把一期直接发送解释为用户已授予同意。

## 三、Google Merchant商品同步

### 3.1 商品准入与退出

| 商品状态 | 可售库存 | 本地动作 | Google动作 |
|---|---:|---|---|
| active | >0 | 校验后可同步 | insert全字段重写，availability=IN_STOCK |
| active | =0 | 保留Catalog状态 | insert全字段重写，availability=OUT_OF_STOCK |
| off_shelf | 任意 | 退出所有市场语言资源 | DELETE该商品全部已创建的Market语言ProductInput |

商品新建、标题、`listing_description`、价格、促销、库存、图片、链接、品牌、成色、类目和映射结果变化均创建Catalog Outbox。商详页CMS Description规则的展示字段、展示名、展示开关或排序发生变化，以及规则引用的属性值或属性翻译发生变化时，也必须创建Catalog Outbox并重同步受影响商品。下架是源头全渠道退出信号，本系统不提供商品级人工排除。

一期商品数据源不提供童装、童鞋。广告系统不增加童装、童鞋识别、过滤或排除逻辑，也不为其设计单独的同步状态、错误码、Outbox分支或监控。若未来上游商品范围增加童装或童鞋，必须先升级商品数据契约并补充年龄组、尺码和Google准入规则，不能直接沿用本期固定`adult`规则。

### 3.2 上游字段契约

| 字段 | 必填 | 来源/规则 |
|---|:---:|---|
| listing_id | 是 | 商品系统不可复用ID |
| listing_status | 是 | active/off_shelf |
| available_qty | 是 | 非负整数 |
| localized_title | 按市场语言 | 商品系统按当前Market语言输出：listing.listing_title → product.title |
| localized_listing_description | 否 | 当前市场语言`listing.listing_description`；有值时作为description唯一来源，空值时进入CMS属性描述回退 |
| localized_landing_url | 按市场语言 | Market配置对应语言的HTTPS页面 |
| image_url | 是 | HTTPS主图，可被Google抓取 |
| additional_image_urls | 否 | HTTPS数组，去重且顺序稳定 |
| selling_price | 是 | 当前成交价，正数 |
| regular_price | 否 | 真实划线原价，必须大于selling_price |
| promotion_start_at/end_at | 否 | 两者同时存在且时序合法才发送促销有效期 |
| catalog_condition | 是 | new/used/refurbished；当前二奢默认used |
| brand | 是 | 商品模块规范英文品牌名，不做广告侧二次映射 |
| looply_level3_category_id | 是 | 商品必须挂有效三级类目 |
| category_ancestry | 是 | 当前末级类目到根类目的有效ID路径；一期为三级→二级→一级，用于查找商详页CMS Description规则 |
| pdp_description_attributes | listing_description为空时 | CMS命中规则选择的描述性属性和销售性属性；包含属性类型、当前语言展示名和值、前台展示状态和配置顺序 |
| color/material/size | 否 | 按商品三级类目读取该标准字段唯一映射的类目属性，缺失时省略 |
| age_group | Google要求时 | 一期固定adult，不读取尺码推导 |
| gender | Google要求时 | 按商品模块“适用人群”精确映射 |
| gtin/mpn | 否 | 商品系统独立语义字段；缺失不阻断，不从barcode猜测 |
| condition_grade/wear_description/accessories | 否 | 商品系统事实字段；广告系统不直接拼接到标题或描述，不替代Google condition |

商品进入Looply商品库视为上游已完成必要鉴定，本系统不依赖`authentication_status`。

### 3.3 性别、年龄组、商品标识与属性固定规则

一期不提供性别或年龄组运营规则配置页。同一商品在不同Market语言资源中使用相同的性别、年龄组结果。Catalog适配器不得读取商品标题、描述、图片、购买用户性别或广告受众推断性别。

`age_group`固定输出`adult`。Google商品类目属于“服饰与配饰”ID 166及其下级类目时发送`ADULT`；其他类目仅在Google明确允许或要求时发送，否则省略。年龄组不读取商品尺码，不做儿童年龄段推导。

商品“适用人群”去除首尾空格并转为小写后精确匹配：

| 原值 | gender | 说明 |
|---|---|---|
| 男 / man / male | male | 精确枚举 |
| 女 / woman / female | female | 精确枚举 |
| adult、空值或其他值 | unisex | 不做包含匹配，不从其他字段猜测 |

Google商品类目属于ID 166及其下级类目时发送上述gender结果；其他类目仅在Google明确允许或要求时发送。

`gender`与`age_group`是两个独立Google字段。`adult`只能写入`age_group`，不得作为gender值。

GTIN只接受纯数字GTIN-8、GTIN-12、GTIN-13或GTIN-14，必须通过GS1 Mod-10校验位，并排除全0、重复占位等明显伪值。该校验只证明格式有效，不证明制造商真实性。MPN必须来自独立语义字段，trim后1–70字符，不含HTML、控制字符或N/A、Unknown等占位值。合法值有则发送，无则省略；不发送`identifier_exists`，不从历史barcode猜测GTIN或MPN，也不发送`item_group_id`。

`catalog_condition=refurbished`只用于经过专业翻新、恢复功能且上游有可证明翻新/保修事实的商品；一般二手商品使用used，不因清洁、养护或普通维修改为refurbished。

自定义属性读取链路固定为：

`listing.product_id → product.standard_sku_id → standard_sku_attribute → attribute_def + attribute_option`

后台按“标准字段 + Looply三级类目 + 单个类目属性”维护color/material/size映射。唯一键为`(normalized_field, looply_level3_category_id)`，每条只保存一个`attribute_def_id`；同一类目、同一标准字段不得存在两条有效映射，同一类目属性不得同时映射给多个标准字段。

商品转换时先读取`looply_level3_category_id`，再读取当前标准字段对应的唯一`attribute_def_id`。属性值必须来自该三级类目的属性作用域，并按当前Market语言读取对应翻译；可选属性缺少该语言翻译时省略，禁止以其他语言兜底。空值不得发送null、空字符串、Unknown或N/A。

### 3.4 Google字段转换

标题直接使用商品系统当前语言的有效展示标题，优先级固定为`listing.listing_title → product.title`。`product.title`的生成或维护属于商品系统，广告系统不重复生成。两级字段都为空时阻断对应语言资源。发送前去除首尾空格、控制字符和HTML标签，连续空格归一化，并按Google上限安全截断至150字符。

description按以下唯一规则生成：

1. 当前语言`listing.listing_description`有值时直接使用，不再拼接CMS属性。
2. `listing.listing_description`为空时，从商品当前末级类目开始逐级向父类目查找商详页CMS Description规则；一期查找顺序为三级→二级→一级。使用最近命中的第一条有效规则，命中后停止，不合并父子规则。
3. 命中规则后同时读取规则配置的描述性属性和销售性属性，只读取配置为前台展示且有值的属性，并按CMS配置顺序输出。属性名使用CMS配置的当前语言展示名，属性值使用商品系统当前语言值；Size Guide、item #、隐藏属性、空值和未被命中规则选择的属性不参与生成。
4. 每个属性按`Label: Value.`生成一个完整片段，片段之间以单个空格连接；多值属性在同一片段内用英文逗号和空格分隔。示例：`Color: Black. Material: Caviar leather. Hardware: Gold-tone. Size: Medium.`
5. product.description不参与Google Feed description回退，广告系统也不使用质检字段、AI或未配置的商品全部属性生成兜底描述。

有效CMS规则是指所属PDP模板的Description模块已开启、类目规则存在且未删除。Feed不得自行维护另一套类目继承算法，必须调用与商详页相同的Description规则解析能力；解析结果至少返回命中类目ID、规则ID、规则版本和按顺序排列的属性配置。只有这样才能保证Feed与落地页使用相同的属性范围、展示名和顺序。

无论来源是`listing_description`还是CMS属性，发送前都要去除首尾空格、控制字符和HTML标签并归一化连续空格。手工描述超过5,000字符时在5,000字符以内安全截断；CMS属性描述按完整片段依次加入，加入下一片段将超过5,000字符时停止，不截断属性名或属性值。最终长度必须为1–5,000字符。

语言判断必须使用商品系统和CMS返回的实际内容语言或翻译状态。任一Market语言资源均必须取得真实对应语言内容；翻译服务返回的其他语言Fallback不得作为该语言的description、属性展示名、属性值或title。CMS规则中某一属性缺少当前语言展示名或属性值时跳过该属性；仍有其他合格属性时继续生成，最终无任何合格属性时阻断对应语言资源，但不阻断其他市场语言资源。

| Google字段 | 转换规则 |
|---|---|
| offerId | listing_id |
| contentLanguage | 当前Market语言配置映射的语言代码 |
| feedLabel | 当前Market的Google初始化绑定配置 |
| channel | ONLINE |
| title | 当前语言listing.listing_title；为空取product.title；两级为空阻断该语言 |
| description | 当前语言listing.listing_description有值时直接使用；为空时按当前末级类目→父类目最近命中的CMS Description规则生成；找不到规则或无可用属性时阻断该语言 |
| link | 当前Market语言对应的落地页 |
| imageLink/additionalImageLinks | 规范HTTPS图片 |
| availability | active且库存>0为IN_STOCK；active且库存=0为OUT_OF_STOCK |
| price | 无促销时selling_price；有有效促销时regular_price |
| salePrice | 仅有效促销时使用selling_price |
| salePriceEffectiveDate | 仅开始/结束完整合法时发送 |
| condition | catalog_condition转大写枚举 |
| brand | 商品规范brand |
| googleProductCategory | 当前三级类目映射的google_category_id |
| color/material/size | 按当前三级类目读取该标准字段唯一映射属性的规范值 |
| ageGroup | Google要求时固定ADULT；其他场景可省略 |
| gender | 商品“适用人群”精确映射；缺失且Google明确要求时阻断对应资源 |
| gtin/mpn | 有合法值才发送；都缺失时两个字段均省略，不发送猜测值 |
| customLabel0/customLabel1/customLabel2/customLabel3/customLabel4 | 由《Looply自建站 GMC Custom Label 规则（AI Coding 执行版 v2.6）》生成；未满足规则时在完整Feed payload中清除对应字段 |

二手一物一码不发送`item_group_id`。Custom Label不通过GMC Attribute rules二次处理，Looply Feed直接发送最终值；详细字段规则不在本PRD展开。`product_type`不是必需业务字段，本期不依赖其进行同步和投放。

### 3.5 Feed准入

同步前只使用两类稳定规则码，具体字段错误写入`field_errors_json`：

| 规则码 | 含义 | 典型字段原因 |
|---|---|---|
| SOURCE_DATA_INVALID | Looply源数据不满足既有商品合同 | 必填缺失、价格≤0、URL非法、枚举非法、促销价不小于原价 |
| CHANNEL_REQUIREMENT_UNMET | 源数据有效但缺少Google当前要求 | Google类目映射缺失 |

开发应在商品模块入口优先阻止必填缺失，但广告同步仍必须防御性校验。可选字段为空时省略；可选字段有值但不满足明确格式时只记录该字段错误并按Google合同决定省略或阻断，禁止猜测修复。

`title`和`description`是每个语言资源的必填准入字段。title执行既定优先级后为空，或description执行本节规则后失败，均写入`SOURCE_DATA_INVALID`的`field_errors_json`并阻断当前语言；不得向Google发送空字符串、null或缺少该字段的ProductInput。

description字段原因固定为：

| field_errors_json.reason | 触发条件 | 处理 |
|---|---|---|
| DESCRIPTION_CMS_RULE_NOT_FOUND | listing_description为空，且从商品当前末级类目逐级查到根类目仍无有效CMS Description规则 | 阻断对应语言资源；不得退化为拼接商品全部属性 |
| DESCRIPTION_CMS_VALUES_EMPTY | listing_description为空且已命中CMS规则，但过滤隐藏、空值和当前语言未就绪属性后无可生成片段 | 阻断对应语言资源，不阻断其他语言资源 |

CMS规则查询失败或超时属于依赖暂不可用，不得错误记录为“规则不存在”；同步项保持待重试状态。只有查询成功且确认整条类目路径均无规则时，才能写入`DESCRIPTION_CMS_RULE_NOT_FOUND`。

### 3.6 首次同步与增量

1. 首次同步分页扫描active商品，按每个Market已启用且就绪的语言生成资源。
2. 以配置水位线和`source_version`建立任务；同一商品×语言×source_version只有一个逻辑投递项。
3. 新品P95≤30分钟；库存归零、下架和关键链接变化为P0，P95≤5分钟。
4. 每日执行差异检查：比较商品源版本、规范payload hash、本地最后成功payload和Google状态，补偿漏事件；不做无差别每日全量重推。
5. insert采用当前完整规范payload重写，避免可选字段删除后在Google侧残留。
6. 商详页CMS Description规则新增、编辑、删除或父子类目命中关系改变时，CMS必须发布包含受影响类目ID的配置事件；Catalog消费者展开该类目及下级类目的active商品，创建Catalog Outbox并重新生成完整description。
7. 命中规则引用的属性值或属性翻译变化时，商品/翻译事件必须携带商品ID和语言；Catalog消费者只重建对应商品和受影响语言，不做无差别全量重推。

### 3.7 状态与诊断

Merchant API请求成功只表示accepted。系统必须保存Google资源名和request ID，并主动分页回拉Product及productStatus，归一化为：

| 状态 | 含义 |
|---|---|
| pending | 请求已接收，等待Google处理 |
| processed | 商品已处理且当前可用或有限制 |
| rejected | Google拒绝或商品不可用于目标目的地 |
| deleted | 下架删除已确认或资源不存在 |

Google原始`code/message/field`必须保留在诊断表，不与Looply Feed准入问题混成同一字段。Webhook如未来可用仅作加速，主动回拉和每日对账仍保留。

### 3.8 配置后台

一期菜单只有属性映射和类目映射。

Google市场投放绑定不提供后台页面。每个Market的Google Ads账号、Merchant账号、数据源、`feedLabel`和启用状态在环境部署时初始化；Market国家、法定币种、已启用语言和站点URL规则由Market国家管理提供。发布或启动时必须校验：每个启用市场均存在有效Google绑定，绑定数据源与`feedLabel`可用，且Market已启用语言可生成对应`contentLanguage`。Custom Label也不提供本后台配置页，规则版本和开发清单以专项打标规则为准。初始化配置变更须走受控配置发布流程，不通过本后台人工编辑。

属性映射首页固定展示三行color、material、size，列表字段为标准广告字段、已配置三级类目数、更新时间、操作。点击“配置”进入对应标准字段的三级类目映射子页面。

子页面规则：

1. 列表字段为Looply三级类目、Looply属性、属性ID、更新时间、操作；支持按三级类目名称或ID搜索。
2. 新增时只展示尚未配置当前标准字段的三级类目；已配置当前标准字段的三级类目不得重复创建。
3. 选择三级类目后，属性候选只来自该三级类目的属性作用域，并按销售性属性、描述性属性分组，支持按属性名称或ID搜索。
4. 一个类目在当前标准字段下只可单选一个属性；同一类目属性已映射到其他标准字段时不进入候选。
5. 编辑时标准字段和三级类目只读，只允许替换Looply属性。
6. 删除必须二次确认；删除后重新进入新增候选，并触发该三级类目下active商品按全部已启用Market语言重建完整Catalog payload。
7. 新增、编辑、删除均立即生效，使用`row_version`防并发覆盖；同事务记录操作日志并创建配置Outbox。

类目映射列表字段为Looply类目、Google商品类目ID、更新时间、操作，支持按类目名称或ID搜索。维持一条有效三级类目对应一个Google商品类目正整数ID；不读取一级/二级映射，不按名称猜测。新增只展示未映射三级类目；查看/编辑时Looply三级类目只读；Google商品类目ID必填且只能是正整数。行级操作为查看、编辑，不提供删除。

两个模块均提供操作日志。列表请求期间展示加载态；零数据展示创建入口；查询无结果展示清除筛选；请求失败展示重试。所有页面不承担权限配置，生产权限由Looply统一权限系统处理。UI基线：`looply-广告投放配置后台原型-v1.17.html`。

## 四、Google Ads再营销事件

### 4.1 初始化与边界

业务页面通过统一`trackEvent(eventName,payload,options)`发布规范事件；Google Ads浏览器适配器只订阅本章五类事件。业务组件不得直接调用`gtag`，不得直接写Google Ads Conversion ID或Conversion Label，也不得自行加载Google标签。

浏览器链路固定为：读取由可信服务端注入的区域策略 → `google_measurement_allowed=true`时初始化`window.dataLayer` → 加载环境对应的Google Tag Manager容器`GTM-{CONTAINER_ID}` → 注册Google Ads消费者 → 消费新产生的业务事件 → 完成主动幂等 → `window.dataLayer.push`。一期不读取CMP或用户同意状态；区域策略禁止时不初始化dataLayer、不加载GTM、不push Google Ads事件。地区策略只控制是否进入Google链路，不影响业务页面和订单支付。

GTM发布版本必须包含以下资产：

| GTM资产 | 触发器 | 用途 |
|---|---|---|
| Conversion Linker | 区域策略允许后的GTM All Pages | 保存Google广告点击信息；禁止地区不加载容器，因而不会触发 |
| Google Ads Remarketing | 五个`looply_ads_*` Custom Event | 向`AW-{ACCOUNT_ID}`发送零售动态再营销事件，不带Purchase Conversion Label |
| Google Ads Conversion Tracking | `looply_ads_purchase` Custom Event | 向唯一Purchase Conversion Action发送购买转化 |
| Data Layer Variables | 见4.2字段 | 从dataLayer读取event_name、value、currency、items和transaction_id |

GTM中的Conversion ID、Conversion Label、容器ID和环境发布版本由广告运维配置，不进入业务payload。浏览、搜索、列表和加购标签不得配置为主要转化。

### 4.2 路由矩阵

| Looply业务事件 | dataLayer Custom Event | Google Ads事件 | 权威触发时机 | 必填参数 |
|---|---|---|---|---|
| search | looply_ads_search | view_search_results | 搜索接口成功返回或明确无结果 | search_term；有结果时items |
| view_item_list | looply_ads_view_item_list | view_item_list | 商品列表核心数据成功展示 | item_list_id、items |
| view_item | looply_ads_view_item | view_item | 商详核心内容可见 | value、currency、单个item |
| add_to_cart | looply_ads_add_to_cart | add_to_cart | 加购事务成功 | cart_operation_id、value、currency、items |
| purchase | looply_ads_purchase | purchase + conversion | 后端确认paid且浏览器claim获准 | order_id、transaction_id、value、currency、items、report_token |

每个item固定：

```json
{
  "id": "LISTING_123",
  "google_business_vertical": "retail"
}
```

`id`必须与Merchant Center的offerId一致。一次`looply_ads_purchase` push由GTM触发两个标签：零售再营销标签和Purchase Conversion Tracking标签。两个标签目的不同，只有后者是主要转化；业务页面不得为此重复push两次purchase。

### 4.3 浏览器幂等

| 事件类别 | 排重边界 | 硬刷新/重新进入 |
|---|---|---|
| search/view_item_list/view_item | `page_instance_id + event + route业务键` | 新页面生命周期可再次发送 |
| add_to_cart | 加购成功事务ID | 刷新不得重发 |
| purchase再营销 | `consumer + order_id`持久化记录 | 刷新不得重发 |

排重必须在`window.dataLayer.push`之前完成。GTM只负责路由和发送，不负责业务幂等。React重复渲染、组件重复挂载、骨架屏、预取、同一响应重复回调不得触发新事件。Google Ads不会按商品ID自动排重再营销事件；平台受众成员唯一不等于事件去重，因此必须由Looply主动控制。

### 4.4 浏览器调用示例

商详事件：

```javascript
window.dataLayer.push({
  event: 'looply_ads_view_item',
  google_ads_event_name: 'view_item',
  value: 3299.00,
  currency: '{BUSINESS_CURRENCY}',
  items: [{ id: 'LISTING_123', google_business_vertical: 'retail' }]
});
```

加购：

```javascript
window.dataLayer.push({
  event: 'looply_ads_add_to_cart',
  google_ads_event_name: 'add_to_cart',
  cart_operation_id: 'CART_OP_789',
  value: 3299.00,
  currency: '{BUSINESS_CURRENCY}',
  items: [{ id: 'LISTING_123', google_business_vertical: 'retail' }]
});
```

## 五、Google Ads Purchase与退款

### 5.1 权威事实

Purchase只在支付渠道异步回调已验签且订单第一次进入最终paid时产生。支付授权、创建payment intent、处理中、前端支付SDK回调和仅打开成功页均不是Purchase事实。

第一次进入paid的事务必须原子完成：更新支付/订单状态、冻结Google转化上下文、创建一条`payment.paid`业务Outbox。重复Webhook返回幂等成功，不创建第二条业务事实。

Refund只在支付渠道确认资金成功退回时产生。退款申请、审核、请求受理或处理中不创建成功退款Outbox。

### 5.2 浏览器Purchase Conversion

成功页流程：

1. 查询Looply订单状态，不读取前端支付SDK结果作为事实。
2. processing按1、2、3、5、8秒退避轮询，最长60秒；未paid时不发送。
3. paid时取得冻结的order_id、金额、items和短期`report_token`。
4. 调用Google Ads浏览器claim；只有返回`googleAds=true`时才能push `looply_ads_purchase`。
5. GTM通过同一个Custom Event分别触发零售再营销标签和Purchase Conversion Tracking标签；业务页面不得直接调用标签。
6. `eventCallback`触发后，用report_token记录`gtm_event_completed`；超时或脚本异常记录`gtm_event_failed`。两者都不代表Google最终入账。
7. 刷新、多标签和重复查询复用order_id，不重新发送。

```javascript
window.dataLayer.push({
  event: 'looply_ads_purchase',
  google_ads_event_name: 'purchase',
  order_id: 'ORDER_456',
  transaction_id: 'ORDER_456',
  value: 3379.00,
  currency: '{BUSINESS_CURRENCY}',
  items: [{ id: 'LISTING_123', google_business_vertical: 'retail' }],
  eventCallback: function () {
    acknowledgeGoogleAdsReport('REPORT_TOKEN', 'gtm_event_completed');
  },
  eventTimeout: 2000
});
```

### 5.3 服务端Data Manager

支付Outbox提交后，Dispatcher按`order_id + google_ads + conversion_action_id`创建一条Data Manager逻辑任务。它固定作为GTM浏览器Purchase标签的额外数据源，不因浏览器`gtm_event_completed`而取消。两端必须指向同一个WEBPAGE类型Conversion Action并使用同一order_id。

服务端载荷按实际存在的匹配信息发送：

- 独立“数据来源”需求返回的有效`gclid/gbraid/wbraid`；不存在时不发送空键。
- 区域投递门控允许时，订单受控服务提供并在内存中规范化、SHA-256的邮箱、电话等Google支持标识。
- 支付时可信IP、User-Agent、event source URL和商品明细。
- `transactionId=order_id`、最终实付value、订单业务事实币种、paid_at。

Data Manager成功返回requestId后，网络投递状态为accepted、诊断状态为pending；随后读取diagnostics并更新processed或rejected。rejected必须转permanent_failed并告警。

### 5.4 “数据来源”依赖

Google广告系统调用独立“数据来源”需求取得：

| 字段 | 用途 | 缺失处理 |
|---|---|---|
| source_context_ref | 对账与审计引用 | 记录unavailable，不阻塞支付 |
| gclid/gbraid/wbraid | Google Ads服务端匹配 | 全部缺失时省略，禁止使用其他用户历史值 |
| captured_at/expires_at | 判断上下文是否仍有效 | 过期时不得发送点击ID |
| order/checkout关联结果 | 证明上下文属于当前交易 | 无可靠关联时不得发送点击ID |

本系统不得创建触点表、判断Direct、执行30分钟去重、选择历史触点、进行身份缝合或计算归因。区域投递门控独立于数据来源：支付/退款任务在业务事实创建时冻结`region_code`、策略版本和`google_measurement_allowed`，禁止地区不得调用Data Manager。数据来源服务不可用时不得阻塞下单或支付；区域允许的服务端Purchase可以只使用实际可用的Google支持身份信息发送，并记录`source_context_status=unavailable`。

### 5.5 PII处理

| 字段 | 归一化 | 发送 |
|---|---|---|
| email | trim、Unicode规范化、小写、格式校验 | SHA-256 HEX |
| phone | E.164，移除展示字符 | SHA-256 HEX |
| first/last name | trim、小写、按Google规则处理标点 | Google支持时哈希 |
| address | 使用订单规范地址与两位国家码 | 严格按Google字段合同 |
| click ID/IP/UA | 校验来源和格式 | 原文，不哈希 |

原始PII不得写应用日志、死信、告警或conversion_upload_log。Worker从订单受控服务读取、内存转换后立即释放；日志只保存`match_keys_used`和不可逆payload hash。

### 5.6 退款调整

1. 退款Worker按order_id串行，读取原Purchase value和累计成功退款。
2. 原Google Purchase尚未accepted时进入dependency_not_ready并等待，不先发调整。
3. 剩余价值>0时发送RESTATEMENT，adjustedValue为当前累计剩余价值。
4. 剩余价值=0时发送一次RETRACTION；同一订单不得二次撤回。
5. 每次退款以refund_id主动幂等，乱序到达时按退款账本重算正确累计值。
6. `partialFailure=true`固定开启；逐索引把结果或错误回写对应refund_id。

部分退款示例：

```json
{
  "partialFailure": true,
  "conversionAdjustments": [{
    "conversionAction": "customers/123/conversionActions/456",
    "adjustmentType": "RESTATEMENT",
    "orderId": "ORDER_456",
    "adjustmentDateTime": "2026-07-24 13:30:00+00:00",
    "restatementValue": {"adjustedValue": 3279.00, "currencyCode": "{BUSINESS_CURRENCY}"}
  }]
}
```

## 六、可靠投递与状态

### 6.1 Outbox与幂等

| 业务事件 | 主动幂等键 |
|---|---|
| Catalog | listing_id + locale + action + source_version |
| Purchase业务事实 | order_id + payment.paid + sequence_no |
| Google Ads服务端Purchase | order_id + purchase + conversion_action_id |
| 浏览器Purchase确认 | order_id + google_ads |
| 退款调整 | refund_id + adjustment + conversion_action_id |

Outbox与业务事实在同库同事务写入；Dispatcher幂等创建下游任务。Worker至少一次投递，重试复用同一逻辑记录、交易ID和业务事件ID。

### 6.2 任务状态

| 状态 | 含义 | 后续动作 |
|---|---|---|
| pending | 已创建，等待领取 | Worker领取 |
| processing | Worker持有有效租约 | 成功、失败或租约恢复 |
| accepted | Google已接收或payload hash判定无需重复发送 | Catalog等待诊断；转化等待对账 |
| retryable_failed | 超时、429、5xx、短期依赖未就绪 | 按next_retry_at重试 |
| permanent_failed | 字段、资源或权限确定不可恢复 | 死信、告警、修复后人工重放 |

区域策略禁止另记`suppressed_by_region`，零网络请求，不伪装为accepted。该状态只表示一期地区门控，不表示用户曾作出拒绝。

### 6.3 错误分类

| 类别 | 典型错误 | 处理 |
|---|---|---|
| transient_network | timeout、连接重置、5xx | 指数退避重试 |
| rate_limited | 429、临时配额 | 尊重Retry-After并降低并发 |
| auth_refreshable | 短期token过期 | 刷新一次；持续失败升级 |
| invalid_payload | 格式、金额、枚举非法 | permanent_failed |
| permission_denied | scope或资产权限缺失 | permanent_failed、P0告警 |
| resource_missing | Catalog、数据源或Conversion Action不存在 | permanent_failed、配置告警 |
| dependency_not_ready | 原Purchase未接受、数据来源暂不可用 | 有界重试 |

## 七、数据模型

| 表 | 用途 | 关键字段/约束 |
|---|---|---|
| google_ad_account | Google Ads与Merchant资产配置 | environment、ads_account_ref、merchant_ref、conversion_action_ref、gtm_container_ref、gtm_published_version、credential_ref；环境内账号唯一 |
| google_market_binding | Market到Google资产的初始化绑定 | environment+market_code唯一；market_code、merchant_ref、data_source_ref、feed_label、enabled；写入来源为部署初始化，不提供后台编辑 |
| catalog_locale_config | Market语言Feed配置 | google_market_binding_id+locale_code唯一；locale_code、content_language、landing_url_rule_ref、enabled；由Market已启用语言派生或同步，不维护币种 |
| attribute_mapping | 三级类目属性到color/material/size | `(normalized_field, looply_level3_category_id)`唯一；单个attribute_def_id；同一类目属性不得跨标准字段重复 |
| category_mapping | 三级类目到Google类目ID | looply_level3_category_id唯一；google_category_id正整数 |
| config_audit_log | 配置操作日志 | business_key、action、operator、before/after、created_at |
| catalog_item_state | 商品×语言状态 | listing_id+locale_config_id唯一；保存source_version、payload_hash、description_source、cms_description_rule_ref/version、cms_rule_category_id、Google资源名和平台状态 |
| catalog_sync_task/item | 同步任务和逐商品台账 | item_state+action+source_version唯一 |
| catalog_validation_issue | Looply准入问题 | 两类feed_rule_code、field_errors_json、生命周期 |
| catalog_platform_issue | Google异步诊断 | raw_status/code/field/message原样保存 |
| outbox_event | 可靠业务事实 | aggregate+event_type+sequence_no唯一 |
| google_conversion_context_snapshot | 订单Google上下文 | order_id唯一；paid_at、market_code、locale_code、currency_code、region_code、region_policy_version、google_measurement_allowed、source_context_ref/status、click IDs、IP/UA、URL、language、schema_version；市场、币种和地区策略均为事实快照 |
| browser_google_ads_ack | 浏览器claim和GTM事件完成确认 | order_id唯一；report_token_hash、ack_status、claim_expires_at；ack_status区分gtm_event_completed/gtm_event_failed |
| google_conversion_upload_log | 服务端Purchase/调整台账 | business_event_id+event_type+destination_ref唯一；保存状态、request_id、diagnostic、错误和match_keys_used |
| google_refund_adjustment_state | 累计退款调整 | order_id唯一；original、cumulative、remaining、retracted、version |
| ad_job_checkpoint | 增量任务水位 | job_name+scope_key唯一 |

本PRD不创建触点、身份关联、订单归因、归因功劳、广告维表、广告花费和ROAS数据表。

`catalog_item_state.description_source`枚举固定为：

| 枚举值 | 含义 | 触发时机 | 记录内容 |
|---|---|---|---|
| listing_description | 使用当前语言listing_description | 规范化后非空 | cms_description_rule_ref/version为空 |
| cms_description_rule | 使用CMS属性描述 | listing_description为空且命中有效规则并生成至少一个片段 | 保存命中规则ID、版本和命中类目ID |

## 八、安全、合规与可观测性

### 8.1 安全

- Access Token、Developer Token和Client Secret进入Secret Manager；数据库只存credential_ref。
- 客户端IP只从可信CDN/负载均衡覆盖头解析，不信任任意X-Forwarded-For。
- 商品图片和落地页检查禁止访问内网、环回、链路本地和云元数据地址。
- 支付/退款回调先验签、去重，再改变业务事实。
- Google返回message按不可信文本转义后展示。

### 8.2 保留与删除

- Google点击ID、IP/UA和诊断原文最长保留90天，之后删除或不可逆匿名化。
- Merchant必要状态、操作日志和不含PII的投递审计按公司审计周期保留。
- 用户删除请求按隐私请求流程清理可关联广告数据；已完成财务审计仅保留不可逆摘要。用户同意撤回、GPC及CMP通知不在一期能力内，后续CMP版本接入后补充处理规则。

### 8.3 监控

- Catalog：P0/P1积压、接受率、诊断拒绝率、状态回拉新鲜度。
- 再营销：GTM加载失败、dataLayer路由错误、标签触发失败、同页面生命周期重复率。
- Purchase：GTM Custom Event完成率、Conversion标签触发率、Data Manager接受率、diagnostic拒绝率、重复交易ID。
- Refund：等待原Purchase、RESTATEMENT/RETRACTION失败和积压时长。
- 区域门控：按region_code和策略版本统计允许/禁止数量、`suppressed_by_region`数量及异常地区解析量；禁止地区出现任何Google请求即P0告警。

## 九、环境与外部资产

| 环境 | 必需资产 |
|---|---|
| staging | 独立Merchant测试账号/数据源、Google Ads测试客户或受控低风险账号、独立Conversion Action、独立GTM容器或Environment、OAuth凭证、测试商品和测试落地页 |
| production | 正式Merchant账号/数据源、正式Google Ads客户、正式Conversion Action、正式GTM容器与已审核发布版本、生产OAuth、真实域名验证 |

staging和production不得复用Catalog、数据源、Conversion Action、GTM发布环境或密钥。测试先使用Merchant测试账号、GTM Preview/Tag Assistant、Data Manager `validateOnly=true`和Google Ads诊断；正式环境只允许受控低预算冒烟。GTM发布必须经过双人复核，记录容器ID、发布版本、发布人和时间。

外部前置条件：网站域名在Merchant Center验证并声明；Merchant与Google Ads账号完成关联；运费、配送时效和退货政策在Google后台配置；Google OAuth、Developer Token、账号权限和Conversion Action审核就绪；商详页CMS提供按类目路径解析Description规则的读取能力和配置变更事件，商品/翻译服务提供规则引用属性的多语言值及变更事件。

## 十、测试与验收

### 10.1 Catalog验收

| 编号 | 场景 | 预期 |
|---|---|---|
| C01 | 某Market语言未就绪 | 只跳过该Market语言资源，不阻塞其他已就绪语言或市场 |
| C02 | 美国与香港均有已启用语言 | 按`content_language~feed_label~listing_id`创建各自独立资源，资源名、URL和内容语言均匹配对应Market配置 |
| C03 | 香港新增或停用一种语言 | 仅新增或停止该香港语言资源，不影响美国或香港其他语言 |
| C04 | 新品/普通字段变化 | 30分钟内accepted |
| C05 | 库存归零 | 5分钟内OUT_OF_STOCK |
| C06 | off_shelf | 5分钟内删除全部已创建Market语言资源 |
| C07 | 商品价格币种缺失或不符合所属Market国家法定币种 | 阻断该商品在该Market语言Feed的投递并记录准入问题，不影响其他商品或市场语言 |
| C08 | Google类目映射缺失 | 对应资源CHANNEL_REQUIREMENT_UNMET，不猜父级 |
| C09 | 可选GTIN/MPN缺失 | 省略并继续同步 |
| C10 | 促销有效期完整 | price、salePrice和有效期正确 |
| C11 | 无有效期划线价 | 只按当前真实售价口径发送，不伪造促销期 |
| C12 | 日常差异检查发现漏事件 | 按source_version补偿，不全量重推无变化商品 |
| C13 | insert accepted后异步拒绝 | 主动回拉原始诊断并告警 |
| C14 | Google独立放行 | 未配置其他广告渠道也可完成全部Catalog测试 |
| C15 | 一期上游商品范围核对 | 输入数据不含童装、童鞋；广告系统不存在额外识别、过滤或排除分支 |
| C16 | 成人服饰与配饰商品 | Google要求时ageGroup固定ADULT，gender按适用人群映射 |
| C17 | 同一标准字段为同一三级类目重复新增 | 候选中不可见，后端唯一键拒绝并发重复 |
| C18 | 编辑或删除类目属性映射 | 受影响三级类目商品按全部已启用Market语言创建配置Outbox并重建完整payload |
| C19 | listing_description有值 | 直接作为description，不读取或拼接CMS属性 |
| C20 | listing_description为空，三级无规则、二级有规则 | 使用二级最近命中规则，不再查询或合并一级规则 |
| C21 | listing_description为空，三级至一级均无规则 | `DESCRIPTION_CMS_RULE_NOT_FOUND`，阻断对应语言资源 |
| C22 | CMS规则已命中但所有配置属性为空或当前语言未就绪 | `DESCRIPTION_CMS_VALUES_EMPTY`，只阻断对应语言资源 |
| C23 | CMS规则展示名、开关、排序或属性翻译变化 | 受影响商品创建Catalog Outbox并重新生成完整description |
| C24 | Custom Label字段生成与清除 | 按《Looply自建站 GMC Custom Label 规则（AI Coding 执行版 v2.6）》专项验收；本PRD不重复定义规则细节 |

### 10.2 再营销验收

| 编号 | 场景 | 预期 |
|---|---|---|
| A01 | EEA、英国或瑞士地区 | 不初始化dataLayer、不加载GTM或Google Ads JS，不push Google Ads事件，零广告网络请求 |
| A02 | 区域策略允许 | dataLayer与GTM只初始化一次；一期不读取CMP或同意状态 |
| A03 | 商详组件重复渲染 | 同页面生命周期只发送一次view_item |
| A04 | 商详硬刷新 | 新页面生命周期发送一次新的view_item |
| A05 | 站内离开后重新进入 | 新路由生命周期可再次发送 |
| A06 | 加购接口重复回调 | 同cart_operation_id只发送一次 |
| A07 | 商品ID | items.id与Merchant offerId均为listing_id |
| A08 | 五类路由 | 五个looply_ads_* Custom Event只触发指定Google Ads标签 |
| A09 | 转化目标配置 | 浏览/搜索/加购不作为主要转化 |
| A10 | GTM被拦截 | 业务不受影响，记录失败指标 |
| A11 | 业务代码扫描 | 不存在直接gtag调用、Conversion ID或Conversion Label硬编码 |
| A12 | GTM配置审计 | Conversion Linker、Remarketing、Purchase Conversion标签齐全；禁止地区不得加载容器 |

### 10.3 Purchase与退款验收

| 编号 | 场景 | 预期 |
|---|---|---|
| P01 | 支付授权/processing | 零Purchase Outbox |
| P02 | 重复支付回调 | 一条业务Outbox和一条Data Manager逻辑任务 |
| P03 | 成功页刷新/多标签 | 只push一次looply_ads_purchase，transaction_id不变 |
| P04 | 用户未返回成功页 | 浏览器可缺失，Data Manager继续发送 |
| P05 | 浏览器和服务端 | 同Conversion Action、同order_id |
| P06 | 无click ID、有可用哈希身份且区域允许 | 发送实际可用字段，不拼旧点击ID |
| P07 | 数据来源不可用 | 不阻塞支付；记录unavailable并按可用身份发送 |
| P08 | EEA、英国或瑞士订单/退款 | 浏览器和服务端均零广告请求，任务为`suppressed_by_region` |
| P09 | Data Manager validateOnly | requestId可记录，不产生正式转化 |
| P10 | 诊断拒绝 | accepted转permanent_failed并告警 |
| P11 | 部分退款 | RESTATEMENT为原值减累计退款 |
| P12 | 多次退款乱序 | 串行重算，最终剩余值正确 |
| P13 | 全额退款 | 原Purchase接受后执行一次RETRACTION |
| P14 | 原Purchase未接受 | 退款任务等待，不先调整 |
| P15 | PII日志扫描 | 无原始邮箱、电话、Token或地址 |
| P16 | Worker响应前崩溃 | 同幂等键恢复，无重复交易 |

### 10.4 放行清单

- [ ] Google Merchant按当前已启用市场语言完成创建、更新、售罄、删除、回拉和诊断；当前覆盖美国与香港，代码不得写死市场范围。
- [ ] Market国家管理语言、法定币种和站点URL规则已接入；Google市场绑定已通过环境初始化校验，无后台编辑入口。
- [ ] 属性映射和三级类目映射与原型v1.17一致。
- [ ] listing_description直取、CMS规则逐级查找、属性拼接、无规则/无值阻断和配置变更重同步通过。
- [ ] `customLabel0`至`customLabel4`已按《Looply自建站 GMC Custom Label 规则（AI Coding 执行版 v2.6）》通过专项验收，且GMC未配置同名Attribute rules。
- [ ] 上游一期商品数据已确认不提供童装、童鞋，商品ageGroup固定ADULT通过。
- [ ] 区域策略允许时GTM加载且五类dataLayer事件、GTM路由和页面排重通过；EEA、英国、瑞士零Google请求。
- [ ] GTM Purchase Conversion标签与Data Manager指向同一WEBPAGE Conversion Action。
- [ ] 数据来源依赖的有效性、关联、过期和不可用降级通过。
- [ ] RESTATEMENT/RETRACTION真实合同测试通过。
- [ ] Outbox、租约、重试、死信、人工重放和告警通过故障演练。
- [ ] staging与production资产隔离，生产低预算冒烟完成。

## 十一、依赖与风险

| 依赖/风险 | 影响 | 控制措施 | 责任方 |
|---|---|---|---|
| 商品字段或语言内容不完整 | 商品拒审 | 上游契约、独立语言准入、差异检查 | 商品/翻译 |
| CMS Description规则缺失或变更事件丢失 | 商品阻断或Google描述陈旧 | 类目路径合同、缺失原因码、配置事件、每日payload差异检查 | 商详CMS/广告后端 |
| Merchant API版本变化 | 接口失效 | 版本环境配置、季度检查、合同测试 | 广告后端 |
| Google类目映射错误 | 商品分类或拒审 | 只允许三级类目和官方正整数ID | 运营/后端 |
| 平台配额波动 | SLA失败 | P0优先、限流自适应、配额监控 | 后端/运营 |
| 数据来源未完成 | 服务端匹配率下降 | 允许无click ID发送；禁止广告系统自建触点替代 | 数据来源/广告后端 |
| 浏览器拦截 | 浏览器事件缺失 | 监控；Purchase由Data Manager补充 | Web/后端 |
| 区域策略配置错误 | 禁止地区产生Google请求或允许地区漏报 | 可信服务端注入、策略版本快照、自动化地区矩阵测试、禁止地区请求P0告警 | 合规/Web |
| GTM容器误发布或变量映射错误 | 漏报、重复或错误转化 | 独立环境、版本锁定、双人复核、Preview自动验收、快速回滚 | 广告运营/Web |
| 支付/退款消息丢失 | 漏转化或价值虚高 | 同事务Outbox、对账、死信 | 支付/广告后端 |
| 双Conversion Action | Google Ads购买重复 | 只保留一个主要WEBPAGE Purchase操作 | 广告运营 |

## 十二、版本、UI与官方依据

### 12.1 v1.5范围

本版本在v1.4基础上纳入GMC Custom Label字段：Looply API直接在Feed中生成`customLabel0`至`customLabel4`，完整规则仅引用《Looply自建站 GMC Custom Label 规则（AI Coding 执行版 v2.6）》。本PRD不重复定义标签值、商品筛选、清单、数量控制或审计细节。区域投递门控、市场语言、币种、GTM、可靠投递与成人商品契约保持v1.4基线。后续接入CMP时，必须新版本评审Consent Mode、用户撤回、GPC、同意快照与历史数据处理，不得反向改写一期事实。

### 12.2 UI索引

| 页面 | PC原型 | App |
|---|---|---|
| 属性映射首页、color/material/size三级类目子页、新增/编辑/删除、操作日志 | `looply-广告投放配置后台原型-v1.17.html` | 不做 |
| 类目映射列表、查看/编辑、操作日志 | `looply-广告投放配置后台原型-v1.17.html` | 不做 |

### 12.3 官方依据

- Google Merchant API：[添加与管理商品](https://developers.google.com/merchant/api/guides/products/add-manage)、[最新更新](https://developers.google.com/merchant/api/latest-updates)、[测试账号](https://developers.google.com/merchant/api/guides/accounts/test-accounts)。
- Looply专项规则：[Looply自建站 GMC Custom Label 规则（AI Coding 执行版 v2.6）](/Users/zz/Documents/Codex/2026-07-22/3-8-catalog-pending-outbox-worker/looply-gmc-custom-label-rules-migration-v2.6.md)。
- Google商品类目：[带ID的官方Taxonomy](https://www.google.com/basepages/producttype/taxonomy-with-ids.en-US.txt)（该文件展示语言不代表Feed投放市场或内容语言）。
- Google Ads：[Data Manager在线转化](https://developers.google.com/data-manager/api/devguides/events/google-ads/online)、[发送事件](https://developers.google.com/data-manager/api/devguides/events/send-events)、[转化调整](https://developers.google.com/google-ads/api/docs/conversions/upload-adjustments)。
- Google Tag Manager：[dataLayer](https://developers.google.com/tag-platform/tag-manager/datalayer)、[Google Ads转化标签](https://support.google.com/tagmanager/answer/6105160)、[动态再营销](https://support.google.com/tagmanager/answer/6106009)。

### 12.4 历史资料关系

`looply-Google广告投放系统-PRD-v1.0.md`、`looply-Google广告投放系统-PRD-v1.1.md`、`looply-Google广告投放系统-PRD-v1.2.md`、`looply-Google广告投放系统-PRD-v1.3.md`、`looply-Google广告投放系统-PRD-v1.4.md`、`looply-站外广告投放系统-PRD-v2.13.md`及旧多平台技术方案保留作历史追溯，不是本v1.5开发依赖。旧ER v2.0仍包含多渠道、触点和归因实体；Google专属ER完成后，以本PRD和对应Google ER为准。

## 十三、开发集成示例

### 13.1 Merchant API v1

```http
POST https://merchantapi.googleapis.com/products/v1/accounts/{MERCHANT_ACCOUNT_ID}/productInputs:insert?dataSource=accounts/{MERCHANT_ACCOUNT_ID}/dataSources/{MERCHANT_DATASOURCE_ID}
Authorization: Bearer {GOOGLE_OAUTH_ACCESS_TOKEN}
Content-Type: application/json

{
  "offerId": "LISTING_123",
  "contentLanguage": "{CONTENT_LANGUAGE}",
  "feedLabel": "{FEED_LABEL}",
  "productAttributes": {
    "title": "Pre-owned Chanel Classic Flap Black Caviar Gold-tone - Grade A",
    "description": "Color: Black. Material: Caviar leather. Hardware: Gold-tone. Size: Medium.",
    "link": "https://looply.com/{market-locale}/products/listing-123",
    "imageLink": "https://cdn.looply.com/LISTING_123/main.jpg",
    "availability": "IN_STOCK",
    "condition": "USED",
    "price": {"amountMicros": "3299000000", "currencyCode": "{MARKET_LEGAL_CURRENCY}"},
    "brand": "Chanel",
    "googleProductCategory": "3032",
    "ageGroup": "ADULT",
    "gender": "FEMALE",
    "color": "Black",
    "material": "Caviar leather",
    "size": "Medium"
  }
}
```

删除指定Market语言资源；资源名为`{CONTENT_LANGUAGE}~{FEED_LABEL}~LISTING_123`：

```http
DELETE https://merchantapi.googleapis.com/products/v1/accounts/{MERCHANT_ACCOUNT_ID}/productInputs/{CONTENT_LANGUAGE}~{FEED_LABEL}~LISTING_123?dataSource=accounts/{MERCHANT_ACCOUNT_ID}/dataSources/{MERCHANT_DATASOURCE_ID}
Authorization: Bearer {GOOGLE_OAUTH_ACCESS_TOKEN}
```

### 13.2 Data Manager Purchase

```http
POST https://datamanager.googleapis.com/v1/events:ingest
Authorization: Bearer {GOOGLE_OAUTH_ACCESS_TOKEN}
Content-Type: application/json

{
  "destinations": [{
    "operatingAccount": {"accountType": "GOOGLE_ADS", "accountId": "{GOOGLE_ADS_ACCOUNT_ID}"},
    "loginAccount": {"accountType": "GOOGLE_ADS", "accountId": "{GOOGLE_ADS_LOGIN_ACCOUNT_ID}"},
    "productDestinationId": "{GOOGLE_ADS_CONVERSION_ACTION_ID}"
  }],
  "encoding": "HEX",
  "events": [{
    "adIdentifiers": {"gclid": "{GCLID_IF_AVAILABLE}"},
    "conversionValue": 3379.00,
    "currency": "{BUSINESS_CURRENCY}",
    "eventTimestamp": "2026-07-24T12:00:00Z",
    "transactionId": "ORDER_456",
    "eventSource": "WEB",
    "eventName": "purchase",
    "userData": {"userIdentifiers": [{"emailAddress": "{SHA256_EMAIL}"}]},
    "cartData": {"items": [{"itemId": "LISTING_123", "quantity": 1, "unitPrice": 3299.00}]}
  }],
  "validateOnly": false
}
```

无gclid或哈希身份时删除对应键，不发送空字符串或伪造值。正式响应requestId只代表接收，必须继续读取diagnostics。
