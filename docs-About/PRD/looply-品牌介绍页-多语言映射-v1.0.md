# 品牌介绍三页多语言资源映射 v1.0

本表定义品牌 PRD §7.1 的资源接入要求，英文正文仍以 Figma 为唯一来源，不维护第二份文案。三页 PC／Mobile 共用同一业务字段，布局取对应端设计稿。

## 1. 语种、归属与迁移

- 市场与语言选择执行[首页 PRD v1.10 §2.1](../../docs-首页/PRD/looply-首页-PRD-v1.10.md)：美国市场，英语／西语，按当前 locale 展示。英文为源语言，西语为目标语言；缺失或空白西语译文时，该字段回退英文，其他字段正常展示。此兜底延续历史 About v0.3 §3.1；不因单字段缺译切换整页语言或跳转。
- 动态业务内容按下表接入翻译中心；静态按钮、页名、返回使用 Web message package；Logo、图片本体、材料原件、品牌／机构标识、数字值、单位符号、办公地址及链接地址保持原值。数字所在说明句仍需翻译，数字和单位语义保持一致。
- 资源卡片与字段是本次要求，不表示已注册或上线。`domain=brand`、`domainName=Looply`；以 migration 注册新增卡片／字段后接入源文和译文，既有内容与译文保留。

| 业务对象 | 卡片处理 | resourceType | 翻译中心路径 |
|---|---|---|---|
| About 页面内容 | 延续原 About 资源契约并扩展新模块字段；既有同义字段复用 | brand_about_page | 多语言管理 → Looply → About Looply |
| 集团页面内容 | 新建卡片 | brand_group_page | 多语言管理 → Looply → Our Group |
| 可持续发展页面内容 | 新建卡片 | brand_sustainability_page | 多语言管理 → Looply → Sustainability |

About 旧版未在下表列出的字段保留供历史页面使用，不绑定到新模块。新旧字段不能只因位置接近而搬移译文；同一字段的英文内容更新后，按翻译平台源文更新流程维护译文。本表为当前页面的字段全集。

## 2. brand_about_page

| fieldName | 业务字段／展示面（PC 与 Mobile） |
|---|---|
| `hero_title` | 首屏主张 |
| `hero_body` | 首屏介绍 |
| `inventory_caption` | 商品数量说明 |
| `warehouse_caption` | 仓储面积说明 |
| `story_title` | 品牌故事标题 |
| `story_body` | 品牌故事正文 |
| `beliefs_title` | 品牌理念标题 |
| `beliefs_statement` | 品牌理念主张 |
| `beliefs_body` | 品牌理念正文 |
| `ways_eyebrow` | 买卖模块引导语 |
| `ways_title` | 买卖模块标题 |
| `buyer_title` | 买家卡标题 |
| `buyer_body` | 买家卡正文 |
| `seller_title` | 卖家卡标题 |
| `seller_body` | 卖家卡正文 |
| `work_eyebrow` | 工作方式引导语 |
| `work_title` | 工作方式标题 |
| `authentication_title` | 专业鉴定标题 |
| `authentication_body` | 专业鉴定正文 |
| `condition_title` | 成色说明标题 |
| `condition_body` | 成色说明正文 |
| `photography_title` | 实物拍摄标题 |
| `photography_body` | 实物拍摄正文 |
| `services_eyebrow` | 卖家服务引导语 |
| `services_title` | 卖家服务标题 |
| `services_body` | 卖家服务介绍 |
| `in_home_title` | 上门服务标题 |
| `in_home_body` | 上门服务正文 |
| `visit_title` | 到店服务标题 |
| `visit_body` | 到店服务正文 |
| `ship_title` | 邮寄服务标题 |
| `ship_body` | 邮寄服务正文 |
| `connect_title` | 联系模块标题 |
| `contact_title` | 联系团队标题 |
| `contact_body` | 联系团队正文 |
| `office_title` | 办公地点标题 |
| `appointment_note` | 预约说明 |

## 3. brand_group_page

| fieldName | 业务字段／展示面（PC 与 Mobile） |
|---|---|
| `hero_title` | 集团主张 |
| `hero_body` | 集团介绍 |
| `sales_caption` | 销量说明及统计截止日期 |
| `expertise_title` | 团队能力标题 |
| `expertise_intro` | 团队能力简介 |
| `expertise_body_1` | 团队经验段落 |
| `expertise_body_2` | 检查规模段落 |
| `expertise_closing` | 团队能力收束段落 |
| `authentication_title` | 鉴定能力标题 |
| `authentication_body` | 鉴定能力正文 |
| `condition_title` | 成色评估标题 |
| `condition_body` | 成色评估正文 |
| `valuation_title` | 估值标题 |
| `valuation_body` | 估值正文 |
| `stores_eyebrow` | 门店引导语 |
| `stores_title` | 门店标题 |
| `stores_body` | 门店介绍 |
| `inventory_caption` | 商品规模说明 |
| `shanghai_name` | 上海门店城市名 |
| `shanghai_location` | 上海门店位置 |
| `shanghai_body` | 上海门店说明 |
| `beijing_name` | 北京门店城市名 |
| `beijing_location` | 北京门店位置 |
| `beijing_body` | 北京门店说明 |
| `sustainability_eyebrow` | 可持续发展引导语 |
| `sustainability_title` | 可持续发展标题 |
| `sustainability_body` | 可持续发展正文 |
| `about_card_title` | About导流卡标题 |
| `about_card_body` | About导流卡正文 |
| `authentication_card_title` | 鉴定导流卡标题 |
| `authentication_card_body` | 鉴定导流卡正文 |

## 4. brand_sustainability_page

| fieldName | 业务字段／展示面（PC 与 Mobile） |
|---|---|
| `hero_title` | 首屏主张 |
| `hero_body` | 首屏介绍 |
| `action_eyebrow` | 行动引导语 |
| `action_title` | 行动标题 |
| `sbti_title` | SBTi卡片标题 |
| `sbti_body` | SBTi卡片正文 |
| `cdp_title` | CDP卡片标题 |
| `cdp_body` | CDP卡片正文 |
| `leed_title` | LEED卡片标题 |
| `leed_body` | LEED卡片正文 |
| `solar_location` | 光伏设施名称 |
| `solar_title` | 光伏小标题 |
| `solar_result` | 光伏减排结果及年份 |
| `solar_body` | 光伏用电说明 |
| `cop_eyebrow` | 大会引导语 |
| `cop_title` | 大会模块标题 |
| `cop28_meta` | COP28年份／大会／地点 |
| `cop28_title` | COP28标题 |
| `cop28_body` | COP28正文 |
| `cop29_meta` | COP29年份／大会／地点 |
| `cop29_title` | COP29标题 |
| `cop29_body` | COP29正文 |
| `cop30_meta` | COP30年份／大会／地点 |
| `cop30_title` | COP30标题 |
| `cop30_body` | COP30正文 |
| `cop31_meta` | COP31年份／大会／地点 |
| `cop31_title` | COP31标题 |
| `cop31_body` | COP31正文 |
| `cta_title` | 底部转化标题 |
| `cta_body` | 底部转化正文 |

## 5. 静态 UI 文案标识

下列均为 message package 标识，读取当前 locale，缺译回退英文。公共 Header／Footer 的现有文案标识由公共组件维护；同一页面名在内容页与公共入口复用对应页名文案。

| 标识 | 用途 |
|---|---|
| `about.title` | About 页名，延续原标识 |
| `brand.group.page_title` | Our Group 页名 |
| `brand.sustainability.page_title` | Sustainability 页名 |
| `brand.back` | 返回操作可访问名称 |
| `account.about.title` | Account Settings 底部 About 入口及 About 列表页标题 |
| `account.about.authenticity` | About 列表的 Authenticity 入口；源文与 PC Footer 相同 |
| `brand.hero.select_image` | 首图指示条可访问名称，包含图片序号 |
| `brand.gallery.select_image` | 门店缩略图可访问名称，包含门店与图片序号 |
| `brand.about.shop_cta` | 品牌 PRD §6 中 about／shop 对应入口；显示文案取 Figma |
| `brand.about.sell_cta` | 品牌 PRD §6 中 about／sell 对应入口；显示文案取 Figma |
| `about.authentication_cta` | 品牌 PRD §6 中 about／authentication 对应入口；显示文案取 Figma |
| `brand.about.seller_services_cta` | 品牌 PRD §6 中 about／seller_services 对应入口；显示文案取 Figma |
| `brand.about.contact_cta` | 品牌 PRD §6 中 about／contact 对应入口；显示文案取 Figma |
| `brand.about.group_cta` | 品牌 PRD §6 中 about／group 对应入口；显示文案取 Figma |
| `brand.about.sustainability_cta` | 品牌 PRD §6 中 about／sustainability 对应入口；显示文案取 Figma |
| `brand.about.booking_cta` | 品牌 PRD §6 中 about／booking 对应入口；显示文案取 Figma |
| `brand.group.expertise_authentication_cta` | 品牌 PRD §6 中 group／expertise_authentication 对应入口；显示文案取 Figma |
| `brand.group.sustainability_cta` | 品牌 PRD §6 中 group／sustainability 对应入口；显示文案取 Figma |
| `brand.group.about_cta` | 品牌 PRD §6 中 group／about 对应入口；显示文案取 Figma |
| `brand.group.authentication_cta` | 品牌 PRD §6 中 group／authentication 对应入口；显示文案取 Figma |
| `brand.sustainability.sbti_cta` | 品牌 PRD §6 中 sustainability／sbti 对应入口；显示文案取 Figma |
| `brand.sustainability.cdp_cta` | 品牌 PRD §6 中 sustainability／cdp 对应入口；显示文案取 Figma |
| `brand.sustainability.leed_cta` | 品牌 PRD §6 中 sustainability／leed 对应入口；显示文案取 Figma |
| `brand.sustainability.cop28_cta` | 品牌 PRD §6 中 sustainability／cop28 对应入口；显示文案取 Figma |
| `brand.sustainability.shop_cta` | 品牌 PRD §6 中 sustainability／shop 对应入口；显示文案取 Figma |
| `brand.sustainability.sell_cta` | 品牌 PRD §6 中 sustainability／sell 对应入口；显示文案取 Figma |

`about.authentication_cta` 沿用原标识，按当前 Figma 更新源文与对应译文；旧 `about.discover_more_cta` 不绑定到语义不同的新入口。三页各模块标题和正文使用上述业务资源，不作为静态 UI 重复维护。H5 About 列表其余三行复用 `about.title`、`brand.group.page_title`、`brand.sustainability.page_title`。
