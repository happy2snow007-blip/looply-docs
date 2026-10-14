# Looply About 与鉴定页埋点开发清单 v1.0

> 日期：2026-10-14。范围：一方平台，PC Web＋Mobile Web，游客与登录态；现有英／西语页面共用稳定点位标识。

## 1. 开发改动

新增 13 个正文入口点击；调整已有首屏保障条款点击的目标标识；补齐 3 个鉴定详情页的页面标识。沿用现有 `page_view` 与 `ui_interaction`，保持现有页面和公共导航采集。

## 2. 点击点位

下表全部在用户真实点击链接时记录一条 `ui_interaction`，`action=select`，`tracking_context.module_id=content_navigation`。T01 复用现有触发点，仅将 `target_id` 从 `returns/returns` 改为 `returns`；其余 13 行补充触发点。表中编号仅供文档定位，不上报。

| 编号 | 发生页 | 点击入口 | interaction_name | element_id | target_id | 目标路径（en-US） |
|---|---|---|---|---|---|---|
| A01 | About | Explore the collection | about_navigation | about_shop_link | home | /en-US |
| A02 | About | How selling works | about_navigation | about_sell_link | c1_sell_home | /en-US/sell |
| A03 | About | Learn about Looply Authentication | about_navigation | about_authentication_link | authentication | /en-US/authenticity |
| A04 | About | Explore seller services | about_navigation | about_seller_services_link | c1_sell_home | /en-US/sell |
| A05 | About | Contact us（正文底部） | about_navigation | about_contact_link | contact_us | /en-US/pages/contact |
| T01 | 鉴定 | View guarantee terms（首屏） | guarantee_navigation | guarantee_details_link | returns | /en-US/pages/returns#money-back-guarantee |
| T02 | 鉴定 | Explore bag authentication | authentication_navigation | authentication_bags_link | authentication_bags | /en-US/authenticity/bags |
| T03 | 鉴定 | Explore jewelry authentication | authentication_navigation | authentication_jewelry_link | authentication_jewelry | /en-US/authenticity/jewelry |
| T04 | 鉴定 | Explore watch authentication | authentication_navigation | authentication_watches_link | authentication_watches | /en-US/authenticity/watches |
| T05 | 鉴定 | Contact us（FAQ 旁） | authentication_navigation | authentication_contact_link | contact_us | /en-US/pages/contact |
| T06 | 鉴定 | 证书 FAQ：contact our team | authentication_navigation | faq_certificate_contact_link | contact_us | /en-US/pages/contact |
| T07 | 鉴定 | 三倍赔偿 FAQ：View guarantee terms and eligibility requirements | guarantee_navigation | faq_guarantee_terms_link | returns | /en-US/pages/returns#money-back-guarantee |
| T08 | 鉴定 | 成色 FAQ：Contact our team | authentication_navigation | faq_condition_contact_link | contact_us | /en-US/pages/contact |
| T09 | 鉴定 | 成色 FAQ：Returns & Refunds policy | authentication_navigation | faq_condition_returns_link | returns | /en-US/pages/returns |

## 3. 公共字段与页面标识

- 事件业务字段为 `data.interaction_name/action/element_id/target_id`，取第 2 节固定值。
- `entities.page` 记录操作发生页：About 为 `page_type=other,page_id=about`；鉴定主页为 `page_type=other,page_id=authentication`。
- `entities.tracking_context` 携带 `module_id` 和当前公共 `page_instance_id`；身份、Session、市场、国家、语言复用已生效公共采集规则。跳转前保留发生页上下文，不能把点击归到目标页。
- 英／西语使用相同事件与元素 ID，目标 URL 保持当前语言。上报稳定 ID，不以展示文案为 ID。
- 本次普通内容链接不追加 `source_event_id`，不上传联系方式、FAQ 正文或自由输入。

三个详情页已有页面访问事件，只补 `entities.page.page_id`，不再发送第二条访问事件：

| 路径后缀（忽略语言前缀） | page_type | page_id |
|---|---|---|
| /authenticity/bags | other | authentication_bags |
| /authenticity/jewelry | other | authentication_jewelry |
| /authenticity/watches | other | authentication_watches |

目标标识 `home`、`c1_sell_home`、`authentication`、`contact_us`、`returns` 对应本次实测目标页的既有 `page_id`。此处 `returns` 专指 `/pages/returns` 政策内容页；`returns/returns` 是旧产品字典中的售后业务分类，不用于本清单的链接目标。此次不更名政策页既有 `page_id`，不改售后业务点位。

## 4. 触发与去重

1. 同一次链接操作只产生一条点击事件，文字、图标和父容器不重复记录；技术重试复用原事件标识。
2. 点击事实不依赖目标页加载成功；目标页面真实到达后由公共逻辑记录 `page_view`。不另加“跳转成功”事件。
3. 直接打开、刷新或真实路由进入详情页时，页面访问沿用公共规则；同页 hash 定位不生成新的页面访问。
4. FAQ 展开、收起、默认展开、图片点击、滚动及模块曝光不纳入本次新增需求。为点击答案内链接而展开 FAQ 时，仅记录链接点击。
5. Header、Footer 使用各自现有公共点位，不触发本表正文点位。重复主动点击属于新的真实操作，不按目标 URL 合并两个不同卖货入口。

## 5. 验收

- PC 与 Mobile、英／西语逐行点击第 2 节入口：每次恰好一条 `ui_interaction`，四个业务字段与表一致，发生页和公共页面实例正确；游客与登录态均可采集。
- T01 与 T07 的元素 ID 不同，目标都为政策页 `returns`；实际链接定位到 `money-back-guarantee` 章节。About 两个 Sell 入口分别可识别。
- 三个详情页分别直达、刷新、由鉴定主页进入：已有 `page_view` 带正确页面标识，不双发；刷新与实际重新进入使用公共新页面实例。
- 初始渲染、FAQ 切换、只滚动、同页锚点变更不补造本次点击或页面访问。
- 浏览器采集请求成功与 DWD 落库分两层验收。请求使用当前生产有效 Schema；数据按小时闭合后核对事件和字段，不能仅凭 HTTP 200 宣称落库完成。

## 6. 接入依赖与基线

开发将本表映射登记到源仓点位清单，并与当前有效事件 Schema 校验；沿用线上 SDK，不回退到查询指南旧 Schema 快照。2026-10-14 实测 `page_view` 为 `1-0-0`、`ui_interaction` 为 `1-1-0`；本需求仅使用已实测存在的点击字段。

本需求不新增用户可见文案或业务实体。展示基线为 2026-10-14 读取的线上 About／Authentication 页面；本次只定义采集，不改变布局和 FAQ 文案。GA4 专项事件不在本次变更范围。
