# Looply PC／Mobile 全页面有意义操作覆盖清单

> 版本：v0.2  
> 日期：2026-08-19  
> UI 基线：Figma `Looply 1.1`（用户确认当前最新版）  
> 运行态补充：`https://www.test.looply.com/`，仅在 Figma 无法确定真实跳转或运行状态时使用  
> 文档用途：逐页面核对所有有意义的用户操作及其数据采集需求；本文件是核对工作稿，不直接替代《数据采集与埋点产品需求》。

## 一、核对规则

每个模块依次核对 Mobile 和 PC；两端不存在的页面明确标记不适用，不根据另一端推测。

每个操作记录：页面、模块／状态、操作对象、用户动作、建议事件、稳定业务名称、必要业务信息、当前 PRD 覆盖状态和证据。Loading、空态、错误态等纯展示状态不自动定义为点击事件；其中真实存在的 Retry、Explore、提交等操作单独记录。原始 DOM 点击、输入过程、敏感输入及无分析价值的交互噪声不采集。

## 二、核对范围与进度

| 顺序 | 模块 | Mobile | PC | 状态 |
|---:|---|---|---|---|
| 1 | 搜索 | 已核对 | 已核对 | 已完成 |
| 2 | 首页 | 已核对 | 已核对 | 已完成 |
| 3 | Looply Authentication | 已核对 | 已核对 | 已完成 |
| 4 | Collection | 已核对 | 已核对 | 已完成 |
| 5 | 注册登录 | 已核对 | 已核对 | 已完成 |
| 6 | 商详 | 已核对 | 已核对 | 已完成 |
| 7 | My Order＋Order Details | 已核对 | 已核对 | 已完成 |
| 8 | Returns | 已核对 | 已核对 | 已完成 |
| 9 | Delivery | 已核对 | 已核对 | 已完成 |
| 10 | Shopping Bag | 已核对 | 已核对 | 已完成 |
| 11 | Checkout | 已核对 | 已核对 | 已完成 |
| 12 | 个人中心 | 已核对 | 已核对 | 已完成 |
| 13 | 个人中心 Account | 已核对 | 已核对 | 已完成 |
| 14 | Contact Us | 已核对 | 已核对 | 已完成 |
| 15 | About Us | 已核对 | 已核对 | 已完成 |

## 三、逐模块核对

### 3.1 搜索

#### 3.1.1 UI 与运行态证据

- Mobile Figma：已核对搜索入口、关键词推荐、筛选、加载失败、无结果及无结果推荐等状态。
- PC Figma：已核对普通展开、联想、筛选未选和筛选已选等状态。
- 测试站：已核对搜索入口、取消、最近搜索、热门搜索词、搜索结果、筛选、排序、商品卡、收藏入口及结果列表；测试站只用于补充真实运行状态，不反向覆盖 Figma 1.1。

#### 3.1.2 搜索入口与提交

| 端 | 模块／状态 | 有意义操作 | 建议记录 | 稳定业务名称 | 必要业务信息 | 当前 PRD |
|---|---|---|---|---|---|---|
| PC＋Mobile | 搜索入口 | 打开搜索区域 | `ui_interaction` | `module_id=search_panel`；`interaction_name=search_panel`；`action=open`；`element_id=search_entry`；`target_id=search_panel` | 所在页面、搜索入口 | 已覆盖 P13 |
| PC＋Mobile | 搜索入口 | 取消／关闭搜索区域 | `ui_interaction` | 同上，`action=close`；`element_id=search_close` | 所在页面、搜索入口、结果状态 | 已覆盖 P13 |
| PC＋Mobile | 轮播词 | 未输入内容，点击搜索按钮提交当前轮播词 | `search` | `trigger_type=carousel_term_button` | 搜索模块正式输出的分析词、轮播词稳定 ID／位置和目标结果页URL上下文 | 已覆盖 P15 |
| PC＋Mobile | 手动输入 | 输入后按回车提交 | `search` | `trigger_type=manual_enter` | 搜索模块正式输出的分析词和目标结果页URL上下文 | 已覆盖 P15；输入过程不采集 |
| PC＋Mobile | 手动输入 | 输入后点击搜索按钮提交 | `search` | `trigger_type=manual_search_button` | 同上 | 已覆盖 P15 |
| PC＋Mobile | 输入联想 | 点击一条联想建议 | `search` | `trigger_type=suggestion_select` | 建议类型、建议稳定对象 ID、位置和目标结果页URL上下文 | 已覆盖 P15；不另记第二条点击事件 |
| PC＋Mobile | 最近搜索 | 点击历史搜索词 | `search` | `trigger_type=history_select` | 历史词稳定值／位置和目标结果页URL上下文 | 已覆盖 P15 |
| PC＋Mobile | 热门搜索 | 点击热门搜索词 | `search` | `trigger_type=popular_term_select` | 热门词稳定 ID／位置和目标结果页URL上下文 | 已覆盖 P15 |
| PC＋Mobile | 热门品牌 | 点击品牌入口并进入 Collection | `ui_interaction`＋目标页 `page_view` | `action=select_popular_brand`；`element_id=popular_brand_item`；`target_id=collection_id` | `collection_id`、位置、原页面与入口 | 已覆盖 P14；不计为搜索 |
| PC＋Mobile | 热门 Collection | 点击 Collection 入口并进入 Collection | `ui_interaction`＋目标页 `page_view` | `action=select_popular_collection`；`element_id=popular_collection_item`；`target_id=collection_id` | `collection_id`、位置、原页面与入口 | 已覆盖 P14；不计为搜索 |

输入字符、光标移动、输入框聚焦、联想词或热门内容仅展示，不形成用户行为事件；采集侧不得读取或上传搜索输入原文。

#### 3.1.3 搜索结果与商品行为

| 端 | 模块／状态 | 有意义操作或业务事实 | 建议记录 | 必要业务信息 | 当前 PRD |
|---|---|---|---|---|---|
| PC＋Mobile | 搜索请求 | 搜索进入成功有结果、成功无结果、失败或取消中的唯一终态 | `view_search_results` | 结果页`page_instance_id`、URL结构化搜索上下文、`result_status`；成功时`result_count`，失败时`failure_type` | 已覆盖 P16 |
| PC＋Mobile | 结果列表 | 商品满足 50% 可视且连续 1 秒 | `view_item_list` | 当前结果页URL结构化搜索上下文、商品三 ID、`position`、`exposure_id`、列表／模块／`page_instance_id` | 已覆盖 P16 |
| PC＋Mobile | 结果商品卡 | 点击图片、标题或价格进入商详 | `select_item` | 当前结果页`page_instance_id`、URL结构化搜索上下文、商品三 ID、位置、曝光及来源上下文 | 已覆盖通用 P08 |
| PC＋Mobile | 结果商品卡 | 点击收藏／取消收藏 | `add_to_wishlist`／`remove_from_wishlist` | 商品三 ID、当前结果页`page_instance_id`、URL结构化搜索上下文、列表／模块、位置、动作结果 | 已覆盖商品意向事件；需在 P16 页面行明确引用 |
| PC＋Mobile | 结果列表 | 向下滚动触发加载更多 | 不单独记录滚动事件 | 新商品满足曝光规则后分别记录 `view_item_list` | 已覆盖；接口请求不冒充用户行为 |
| PC＋Mobile | 零结果推荐 | 推荐商品达到曝光条件／点击商品 | `view_item_list`／`select_item` | 当前结果页`page_instance_id`、URL结构化搜索上下文、推荐请求、零结果场景、位置、商品三 ID | 已覆盖 P18 |
| PC＋Mobile | 加载失败 | 用户点击 Retry（UI 实际提供时） | `ui_interaction` | `action=retry`、原失败操作稳定 ID、当前结果页`page_instance_id`、动作结果 | 通用 Retry 已覆盖；开发前需确认失败稿是否保留可点击 Retry |

#### 3.1.4 筛选与排序

| 端 | 模块／状态 | 有意义操作 | 建议记录 | 必要业务信息 | 当前 PRD |
|---|---|---|---|---|---|
| PC＋Mobile | 筛选 | 打开／关闭筛选面板 | `ui_interaction` | `action=open_filter/close_filter`、面板稳定 ID | 打开已覆盖 P17；`close_filter`需补稳定动作 |
| PC＋Mobile | 筛选分组 | 展开／收起 Price、Condition、Brand、Category、Color、Size、Material 等分组 | `ui_interaction` | `action=expand_filter_group/collapse_filter_group`、筛选分组稳定 ID | **缺失，需补** |
| PC＋Mobile | 筛选选项 | 选择／取消价格、成色、品牌、类目、颜色、尺码、材质等条件 | `ui_interaction` | `action=change_filter`、筛选项与结构化值、选择状态 | 已覆盖 P17 |
| PC＋Mobile | 筛选分组 | 点击 View all 展开更多选项 | `ui_interaction` | `action=view_all_filter_options`、筛选分组稳定 ID | **缺失，需补** |
| PC＋Mobile | 筛选 | Reset | `ui_interaction`＋`view_search_results` | `action=reset`；清空URL筛选参数；结果更新后记录当前`page_instance_id`和URL上下文 | 已覆盖 P17 |
| PC＋Mobile | 筛选 | Apply | `ui_interaction`＋`view_search_results` | `action=apply_filter`；URL写入已生效`filters[]`；结果更新后记录终态 | 已覆盖 P17 |
| PC＋Mobile | 排序 | 打开／关闭排序选单 | `ui_interaction` | `action=open_sort/close_sort`、排序控件 ID | 打开已覆盖 P17；`close_sort`需补稳定动作 |
| PC＋Mobile | 排序 | 选择 Recommended、Newest、Price low→high、Price high→low | `ui_interaction`＋`view_search_results` | `action=change_sort/apply_sort`；URL写入稳定`sort_type`；结果更新后记录终态 | 已覆盖 P17 |

Mobile 使用全屏／抽屉式筛选，PC 使用侧栏／展开式筛选；两端交互形态不同，但使用同一业务动作和字段口径，端别由公共上下文区分。

#### 3.1.5 本模块结论

搜索模块主体已覆盖；当前发现需要补入数据采集 PRD 的明确缺口为：

1. 筛选面板关闭：`close_filter`；
2. 排序选单关闭：`close_sort`；
3. 筛选分组展开／收起：`expand_filter_group`、`collapse_filter_group`；
4. 查看某筛选分组全部选项：`view_all_filter_options`；
5. 在搜索结果页面行明确说明收藏／取消收藏复用 `add_to_wishlist`／`remove_from_wishlist`。

以上均不需要新增统一业务事件；前三类与 View all 复用 `ui_interaction`，收藏复用既有业务事件。

### 3.2 首页

#### 3.2.1 UI 与运行态证据

- Mobile Figma：已核对 8.17 Banner 更新、8.13 鉴定入口更新、商品卡、Back to Top、顶部滚动反白及首页完整画板。
- PC Figma：已核对首页鉴定入口、Collections、Banner、Header＋Footer 及不同画布尺寸。
- 测试站：已核对 Header、Hero Banner、鉴定模块、Curated Collections、For You／New Arrivals、商品 Feed、购物保障及 Footer。测试站用于确认真实入口与跳转，不覆盖 Figma 1.1 的设计状态。

#### 3.2.2 首页专属模块

| 端 | 模块 | 有意义操作或业务事实 | 建议记录 | 稳定业务名称 | 必要业务信息 | 当前 PRD |
|---|---|---|---|---|---|---|
| PC＋Mobile | 首页 | 页面成功到达 | `page_view` | `page_type=home`、`page_id=home` | `page_instance_id`及公共上下文 | 已覆盖 P01 |
| PC＋Mobile | Hero Banner | 点击轮播点、滑动切换 Banner | `ui_interaction` | `module_id=home_banner`；`interaction_name=banner`；`action=change`；`element_id=banner_item` | 当前／目标 Banner ID、位置、活动配置、结果 | 已覆盖 P04 |
| PC＋Mobile | Hero Banner | 点击 Explore 按钮 | `ui_interaction`＋目标页 `page_view` | `action=select`；`element_id=explore_button`；`target_id=目标页面ID` | Banner ID、活动配置、目标及结果 | 已覆盖 P04 |
| PC＋Mobile | Hero Banner | 点击 Banner 图片或整张可点击区域 | `ui_interaction`＋目标页 `page_view` | `action=select`；`element_id=banner_item`；`target_id=目标页面ID` | Banner ID、活动配置、位置、目标及结果 | **缺失，需补** |
| PC＋Mobile | Looply Authentication | 点击 Explore Details 进入鉴定介绍 | `ui_interaction`＋目标页 `page_view` | `module_id=home_authentication`；`interaction_name=authentication_entry`；`action=select`；`element_id=explore_details_button`；`target_id=authentication` | 首页、入口、目标及导航结果 | **缺失，需补** |
| PC＋Mobile | Curated Collections | 横向滑动集合轨道 | `ui_interaction` | `module_id=curated_collections`；`interaction_name=collection_rail`；`action=scroll` | 轨道 ID、滑动前后位置、结果 | 已覆盖 P05 |
| PC＋Mobile | Curated Collections | 点击 Collection 卡片 | `ui_interaction`＋目标页 `page_view` | `action=select`；`element_id=collection_card`；`target_id=collection_id` | `collection_id`、运营配置、位置及结果 | 已覆盖 P05 |
| PC＋Mobile | Explore Finds Feed | 切换 For You／New Arrivals | `ui_interaction` | `module_id=home_feed_tabs`；`interaction_name=feed_tab`；`action=change` | 前一 Tab、目标 Tab、结果 | 已覆盖 P06 |
| PC＋Mobile | Explore Finds Feed | 商品达到 50% 可视且连续 1 秒 | `view_item_list` | `module_id=home_product_feed` | 商品三 ID、场景、推荐请求、位置、曝光 ID、页面实例 | 已覆盖 P07 |
| PC＋Mobile | Explore Finds Feed | 点击商品图片、标题或价格进入商详 | `select_item` | 继承当前 Feed 的模块、场景和入口 | 商品三 ID、推荐请求、曝光、位置和来源 | 已覆盖通用 P08 |
| PC＋Mobile | Explore Finds Feed | 点击收藏／取消收藏 | `add_to_wishlist`／`remove_from_wishlist` | 继承当前 Feed 的模块、场景和入口 | 商品三 ID、推荐请求、曝光、位置和动作结果 | 统一事件已存在；**需在首页 Feed 行明确引用** |
| Mobile | 页面导航 | 点击 Back to Top | `ui_interaction` | `module_id=home_navigation`；`interaction_name=page_navigation`；`action=back_to_top`；`element_id=back_to_top_button`；`target_id=page_top` | 页面实例、点击结果 | 已覆盖 P20；PC 当前未见对应设计 |

Banner 自动轮播、页面自然滚动、模块自动加载、顶部滚动反白、购物保障内容展示均不单独形成用户行为事件。

#### 3.2.3 全站 Header（在首页核对，其他页面复用）

| 端 | 操作 | 建议记录 | 稳定业务名称 | 必要业务信息 | 当前 PRD |
|---|---|---|---|---|---|
| PC＋Mobile | 点击 Logo 返回首页 | `ui_interaction`＋目标页 `page_view` | `module_id=global_header`；`interaction_name=header_navigation`；`action=select`；`element_id=home_logo`；`target_id=home` | 当前页面、目标及结果 | P02未明确 Header Logo，**需补** |
| PC | 点击 Handbags、Shoes、Brands、Jewelry、Watches、Designers 等顶部导航 | `ui_interaction`＋目标页 `page_view` | `module_id=global_header`；`interaction_name=header_navigation`；`action=select`；`element_id=header_nav_item` | 导航项稳定 ID、目标 Collection／页面及结果 | P02原则覆盖，**需补入口枚举** |
| PC | 打开／关闭 More navigation；选择其中入口 | `ui_interaction`＋目标页 `page_view` | `interaction_name=header_more_navigation`；`action=open/close/select`；`element_id=more_navigation_button/more_nav_item` | 入口 ID、目标及结果 | **缺失，需补** |
| PC＋Mobile | 打开 Market & Language；选择 Market／Language | `ui_interaction` | `interaction_name=market_language`；`action=open/close/select_market/select_language` | 前一值、目标稳定值、结果；不记录自由文本 | **缺失，需补** |
| PC＋Mobile | 打开搜索 | 复用搜索模块 P13 | `module_id=search_panel`，入口区分 `pc_header_search/mobile_search_entry` | 当前页面、搜索入口、结果 | 已覆盖 P13 |
| PC＋Mobile | 点击 Account／Me 入口 | `ui_interaction`＋目标页 `page_view` | `interaction_name=header_navigation`；`element_id=account_entry`；`target_id=account` | 登录／游客路径、目标及结果 | P02原则覆盖，**需补 Header 入口枚举** |
| PC＋Mobile | 点击 Favorites 入口 | `ui_interaction`＋目标页或面板结果 | `interaction_name=header_navigation`；`element_id=favorites_entry`；`target_id=favorites` | 登录拦截、目标形态及结果 | P02原则覆盖，**需补 Header 入口枚举** |
| PC＋Mobile | 点击 Cart 入口 | `ui_interaction`＋目标页或面板结果 | `interaction_name=header_navigation`；`element_id=cart_entry`；`target_id=cart` | 目标形态及结果 | P02原则覆盖，**需补 Header 入口枚举** |
| Mobile | 点击底部 Home／Shop／Favorites／Me | `ui_interaction`＋目标页 `page_view` | P02 `module_id=global_navigation`；`entry_context=mobile_bottom_nav` | 导航项 ID、目标页面、结果 | 已覆盖 P02 |

#### 3.2.4 全站 Footer（在首页核对，其他页面复用）

| 端 | 操作 | 建议记录 | 稳定业务名称 | 必要业务信息 | 当前 PRD |
|---|---|---|---|---|---|
| PC＋实际展示 Footer 的 Mobile Web | 点击 Shop、Support、About、Legal 各站内入口 | `ui_interaction`＋目标页 `page_view` | `module_id=footer`；`interaction_name=footer_navigation`；`action=select`；`element_id=footer_link` | Footer 分组、入口稳定 ID、目标 `page_id`及结果 | P49部分覆盖；**需补完整入口枚举** |
| PC＋实际展示 Footer 的 Mobile Web | 输入邮箱并点击 Subscribe | `ui_interaction` | `interaction_name=newsletter_subscription`；`action=submit`；`element_id=subscribe_button`；`target_id=newsletter` | 提交结果、订阅来源；不得记录邮箱原文 | **缺失，需补** |
| PC＋实际展示 Footer 的 Mobile Web | 点击 Facebook／TikTok／Instagram／YouTube | `ui_interaction` | `interaction_name=footer_social_navigation`；`action=select`；`element_id=social_link`；`target_id=社交平台稳定枚举` | 平台、站外链接类型、结果 | **缺失，需补** |

支付方式、鉴定合作方、物流合作方 Logo 仅展示时不记录事件；若后续改为可点击入口，再按 Footer 外链规则补充。

#### 3.2.5 本模块结论

首页已有 Banner 切换／Explore、Collections、Feed Tab、商品曝光／点击、Mobile Back to Top 等主体埋点。当前需要补入正式数据采集 PRD 的内容为：

1. Hero Banner 整张可点击区域；
2. 首页鉴定模块 Explore Details；
3. 首页 Feed 商品收藏／取消收藏的页面映射；
4. Header Logo、顶部导航枚举、More navigation、Market & Language、Account、Favorites、Cart；
5. Footer 全量入口枚举、Newsletter 提交和社交平台入口。

以上均复用现有 `ui_interaction`、`page_view`、`add_to_wishlist`和`remove_from_wishlist`，不新增统一事件。

### 3.3 Looply Authentication

#### 3.3.1 UI 与运行态证据

Figma 1.1 同时存在 Mobile、PC 的 Looply Authentication 页面；测试站已核对页面主体，包括鉴定介绍、鉴定流程内容、3× Money-Back Guarantee 说明和 See Guarantee Details 入口。当前视频区域在运行态表现为展示图片，未确认可播放控件，因此不虚构视频播放埋点。

#### 3.3.2 有意义操作清单

| 端 | 模块 | 有意义操作或业务事实 | 建议记录 | 稳定业务名称 | 必要业务信息 | 当前 PRD |
|---|---|---|---|---|---|---|
| PC＋Mobile | Authentication 页面 | 页面成功到达 | `page_view` | `page_type=content`；`page_id=authentication` | 页面实例、来源页面／入口及公共上下文 | P01可复用，但**页面映射缺失，需补** |
| PC＋Mobile | 3× Money-Back Guarantee | 点击 See Guarantee Details | `ui_interaction`＋目标页 `page_view` | `module_id=authentication_guarantee`；`interaction_name=guarantee_navigation`；`action=select`；`element_id=guarantee_details_link`；`target_id=returns` | 当前页面、入口、目标及导航结果 | **缺失，需补** |
| PC＋Mobile | Header／Footer | 点击全站公共入口 | 复用首页 3.2.3、3.2.4 的公共规则 | 继承 `global_header`／`footer` 稳定名称 | 当前页面应记录为 `authentication` | 公共规则补齐后复用 |

鉴定介绍正文、图片、承诺说明、How We Do It 内容和保障条款仅展示时不记录交互事件。若后续设计将鉴定视频改为可播放控件，应再增加播放／暂停／播放完成的有意义互动；当前版本不纳入。

#### 3.3.3 本模块结论

需要补入正式数据采集 PRD 的内容只有两项：Authentication 页面稳定映射，以及 See Guarantee Details 入口。均复用 `page_view`和`ui_interaction`，不新增统一事件。

### 3.4 Collection

#### 3.4.1 UI 与运行态证据

Figma 1.1 同时存在 Mobile、PC Collection 页面；测试站已核对集合标题、筛选、排序、商品列表、商品收藏及滚动加载。Mobile 的筛选采用抽屉／全屏形态，PC 为侧栏形态，两端业务动作保持一致。

#### 3.4.2 有意义操作清单

| 端 | 模块 | 有意义操作或业务事实 | 建议记录 | 稳定业务名称 | 必要业务信息 | 当前 PRD |
|---|---|---|---|---|---|---|
| PC＋Mobile | Collection 页面 | 具体集合页成功到达 | `page_view` | `page_type=listing`；`page_id=collection`；`module_id=collection_product_list` | `collection_id`、页面实例、入口及运营配置 | 已覆盖 P10 |
| PC＋Mobile | 商品列表 | 商品满足 50% 可视且连续 1 秒 | `view_item_list` | `module_id=collection_product_list`；`scene_id=collection` | `collection_id`、商品三 ID、位置、曝光 ID、页面实例 | 已覆盖 P12／统一曝光规则 |
| PC＋Mobile | 商品卡 | 点击图片、标题或价格进入商详 | `select_item` | 继承 Collection 列表上下文 | `collection_id`、商品三 ID、位置、曝光及来源 | 已覆盖通用 P08 |
| PC＋Mobile | 商品卡 | 点击 Save／取消收藏 | `add_to_wishlist`／`remove_from_wishlist` | 继承 Collection 列表上下文 | `collection_id`、商品三 ID、位置、曝光及结果 | 统一事件已存在；**需在 Collection 页面行明确引用** |
| PC＋Mobile | 筛选 | 打开／关闭筛选面板 | `ui_interaction` | `module_id=collection_list_controls`；`interaction_name=filter_sort`；`action=open_filter/close_filter` | `collection_id`、面板 ID、结果 | 打开已覆盖 P11；`close_filter`需补 |
| PC＋Mobile | 筛选分组 | 展开／收起 Category、Color、Condition、Price、Series、Attribute Group、Brands 等分组 | `ui_interaction` | `action=expand_filter_group/collapse_filter_group`；`element_id=filter_group`；`target_id=筛选分组稳定ID` | `collection_id`、分组 ID、结果 | **缺失，需补** |
| PC＋Mobile | 筛选项／Quick Filter | 选择或取消一个结构化筛选条件 | `ui_interaction` | `action=change_filter`；`element_id=filter_control` | `collection_id`、筛选项、结构化值、选择状态 | 已覆盖 P11；Quick Filter复用同一动作 |
| PC＋Mobile | 筛选分组 | 点击 View all 展开更多选项 | `ui_interaction` | `action=view_all_filter_options`；`element_id=filter_group`；`target_id=筛选分组稳定ID` | `collection_id`、分组 ID、结果 | **缺失，需补** |
| PC＋Mobile | 筛选 | Reset／Apply | `ui_interaction` | `action=reset/apply_filter` | `collection_id`、正式生效的结构化筛选条件、结果 | 已覆盖 P11 |
| PC＋Mobile | 排序 | 打开／关闭排序选单 | `ui_interaction` | `action=open_sort/close_sort`；`element_id=sort_control` | `collection_id`、排序控件、结果 | 打开已覆盖 P11；`close_sort`需补 |
| PC＋Mobile | 排序 | 选择 Recommended、Newest、Price low→high、Price high→low | `ui_interaction` | `action=change_sort/apply_sort`；`element_id=sort_control`；`target_id=稳定排序值` | `collection_id`、前一值、目标值、结果 | 已覆盖 P11 |
| PC＋Mobile | 滚动加载 | 新批次商品返回并达到曝光条件 | 仅记录新增商品的 `view_item_list` | 沿用 Collection 列表上下文 | 批次／请求、商品、位置及曝光 ID | 已覆盖 P12；接口请求与自然滚动不单独记事件 |
| PC＋Mobile | Header／Footer | 点击公共入口 | 复用 3.2.3、3.2.4 | 当前页面记录为 `collection` | `collection_id`、目标及结果 | 公共规则补齐后复用 |

集合 Hero 图、标题、描述、商品数量、价格文本和筛选结果自动刷新仅展示时不记录用户操作。

#### 3.4.3 本模块结论

Collection 主体已覆盖。需要补充：商品收藏／取消收藏的页面映射、筛选和排序关闭、筛选分组展开／收起、View all。均复用已有事件，不新增统一事件。

### 3.5 注册登录

#### 3.5.1 UI 证据

- Mobile Figma：Login、Register、密码错误、注册邮箱错误、提交中、Remembered Login、验证码普通／填写／倒计时、Forgot Password、Change Password、Consent Update Modal、Risk Blocked、Terms、Privacy、Sign-out 弹窗及账号删除状态。
- PC Figma：Login、Register、Login Error、Already Login、验证码普通／填写／倒计时／跨状态登录、Forgot Password、Set Password、Terms、Privacy、Blocked、Sign Out、Update及账号删除状态。
- 登录、注册、验证码、密码、账号删除等输入可能包含个人信息或凭据；普通分析事件只记录稳定动作和低基数结果，不采集输入内容。

#### 3.5.2 登录与注册主流程

| 端 | 模块／状态 | 有意义操作或业务事实 | 建议记录 | 稳定业务名称 | 必要业务信息 | 当前 PRD |
|---|---|---|---|---|---|---|
| PC＋Mobile | Login／Register | 登录页或注册页成功到达 | `page_view` | `page_type=auth`；`page_id=login/sign_up` | 页面实例、认证入口、来源页面 | 已覆盖 P41 |
| PC＋Mobile | Login／Register | 切换 Login／Register | `ui_interaction` | `module_id=auth_form`；`interaction_name=authentication`；`action=change_tab`；`element_id=auth_tab`；`target_id=login/sign_up` | 前一页面、目标页面、结果 | 已覆盖 P41 |
| PC＋Mobile | Login | 点击提交登录 | `ui_interaction` | `action=submit_form`；`element_id=auth_submit_button`；`target_id=login` | 登录方式、低基数提交结果／失败分类；不含账号密码 | 已覆盖 P41 |
| PC＋Mobile | Login | 登录事务真实成功 | `login` | 统一 `login` 事件 | `anonymous_id`、`user_id`、登录方式、身份状态；无 PII | 已覆盖 C14／统一事件 |
| PC＋Mobile | Register | 点击提交注册 | `ui_interaction` | `action=submit_form`；`element_id=auth_submit_button`；`target_id=sign_up` | 注册方式、低基数提交结果／失败分类；不含账号密码 | 已覆盖 P41 |
| PC＋Mobile | Register | 注册事务真实成功 | `sign_up` | 统一 `sign_up` 事件 | `anonymous_id`、`user_id`、注册方式、来源；无 PII | 已覆盖 C13／统一事件 |
| PC＋Mobile | Remembered Login | 选择已记忆账号继续登录／选择其他账号（控件实际存在时） | `ui_interaction` | `interaction_name=remembered_login`；`action=continue/switch_account`；`element_id=remembered_account/other_account` | 认证入口、结果；不得记录账号原文 | **缺失，需补稳定动作** |

表单聚焦、输入字符、密码显示／隐藏、字段逐次校验、Skeleton 和提交中动画不单独形成分析事件；提交的最终成功／校验失败／认证失败使用同一次提交动作的结果表达。

#### 3.5.3 验证码与密码流程

| 端 | 模块／状态 | 有意义操作 | 建议记录 | 稳定业务名称 | 必要业务信息 | 当前 PRD |
|---|---|---|---|---|---|---|
| PC＋Mobile | Login | 点击 Forgot Password | `ui_interaction`＋目标页 `page_view` | `module_id=auth_recovery`；`interaction_name=password_recovery`；`action=start`；`element_id=forgot_password_link`；`target_id=forgot_password` | 来源、目标及结果 | **缺失，需补** |
| PC＋Mobile | Verify Code | 点击发送／重新发送验证码 | `ui_interaction` | `interaction_name=verification_code`；`action=send/resend`；`element_id=verification_code_button`；`target_id=verification_code` | 验证场景、结果、低基数失败分类；不得记录验证码 | **缺失，需补** |
| PC＋Mobile | Verify Code | 提交验证码 | `ui_interaction` | `action=submit`；`element_id=verification_code_submit` | 验证场景、结果；不得记录验证码 | **缺失，需补** |
| PC＋Mobile | Forgot／Set／Change Password | 提交设置或修改密码 | `ui_interaction` | `interaction_name=password_recovery`；`action=submit_password`；`element_id=password_submit_button`；`target_id=set_password/change_password` | 场景、结果、低基数失败分类；不得记录密码 | **缺失，需补** |
| PC＋Mobile | 恢复流程 | 返回上一步／返回登录（控件实际存在时） | `ui_interaction`＋目标页 `page_view` | `action=back`；`element_id=auth_back_button`；`target_id=目标认证页面` | 当前步骤、目标及结果 | **缺失，需补稳定动作** |

验证码倒计时开始／结束、输入位变化和自动聚焦仅为界面状态，不单独记录事件。

#### 3.5.4 协议、同意与异常状态

| 端 | 模块／状态 | 有意义操作 | 建议记录 | 稳定业务名称 | 必要业务信息 | 当前 PRD |
|---|---|---|---|---|---|---|
| PC＋Mobile | 登录／注册表单 | 点击 Terms of Service／Privacy Policy | `ui_interaction`＋目标页 `page_view` | `module_id=auth_legal`；`interaction_name=legal_navigation`；`action=select`；`element_id=terms_link/privacy_link`；`target_id=terms_of_service/privacy_policy` | 来源页面、目标及结果 | **缺失，需补** |
| Mobile | Consent Update Modal | 用户确认或关闭同意更新弹窗（按实际按钮） | `ui_interaction` | `module_id=auth_consent_modal`；`interaction_name=consent_update`；`action=confirm/close` | 同意版本、动作结果；不记录文案原文 | **缺失，需补** |
| PC＋Mobile | Risk Blocked／Blocked | 用户点击页面提供的返回、关闭或联系客服入口（控件实际存在时） | `ui_interaction`＋可能的目标页 `page_view` | `module_id=auth_blocked_state`；按实际控件登记 `action`、`element_id`和`target_id` | 低基数阻断分类、目标及结果 | **需根据具体按钮补稳定映射** |

错误提示、Blocked 文案、倒计时、加载和蒙层仅展示时不形成事件；错误原因只能使用封闭低基数分类，不上传自由错误文本。

#### 3.5.5 本模块结论

当前 PRD 仅概括了切换、提交、错误和成功，尚不能让开发覆盖完整认证流程。需要补充：Remembered Login、Forgot Password、验证码发送／重发／提交、设置／修改密码、返回登录、Terms／Privacy入口、Consent Update Modal及Blocked状态中的实际按钮。登录成功和注册成功继续使用既有 `login`、`sign_up`，其余复用 `ui_interaction`与`page_view`，不新增统一事件。

### 3.6 商详

#### 3.6.1 UI 与运行态证据

Mobile、PC Figma 及测试站已核对：顶部返回／分享／购物袋、商品图片与全屏预览、收藏、Add to Bag、Buy Now、Sold Out、鉴定说明、Condition Guide、Description、Size Guide、Shipping & Returns、You May Also Like、Recently Viewed、Find More、Share To 弹层及加载／库存／价格变化状态。

#### 3.6.2 商品主体与购买操作

| 端 | 有意义操作或业务事实 | 建议记录 | 稳定业务名称／必要信息 | 当前 PRD |
|---|---|---|---|---|
| PC＋Mobile | 商详成功到达及核心商品信息可分析 | `page_view`＋`view_item` | `page_id=product_detail`、商品三 ID、价格、币种、来源 | 已覆盖 P01／P19 |
| Mobile及实际提供返回控件的PC | 点击返回 | `ui_interaction`＋目标页结果 | `module_id=product_header`；`action=back`；`element_id=back_button`；`target_id=previous_page_or_home` | **缺失，需补** |
| PC＋Mobile | 点击购物袋入口 | `ui_interaction`＋目标页 `page_view` | `action=select_cart`；`element_id=cart_entry`；`target_id=cart`；商品上下文 | Header公共规则需明确商详入口 |
| PC＋Mobile | 收藏／取消收藏 | `add_to_wishlist`／`remove_from_wishlist` | 商品三 ID、商详来源 | 已覆盖 P23 |
| PC＋Mobile | 加入购物袋或数量真实增加 | `add_to_cart` | 商品三 ID、购物车、数量、价格和来源 | 已覆盖 P24 |
| PC＋Mobile | Buy Now进入Checkout | `begin_checkout` | 商品三 ID、`source_type=buy_now`、现有`checkout_start` | 已覆盖 P25 |
| PC＋Mobile | 点击Share | `ui_interaction` | P50 `module_id=product_share`；商品三 ID、打开结果 | 已覆盖 P50 |

Sold Out、价格变化和库存变化是展示／业务状态；只有收藏、加购、开始结算等真实结果成立时记录对应业务事件。Toast、角标变化和按钮文案反馈不重复造事件。

#### 3.6.3 图片浏览与预览

| 端 | 操作 | 建议记录 | 稳定业务名称／必要信息 | 当前 PRD |
|---|---|---|---|---|
| PC＋Mobile | 点击缩略图、上一张／下一张、主图横滑切图 | `ui_interaction` | `module_id=product_gallery`；`action=change`；前后图片位置、商品三 ID | 已覆盖 P21 |
| PC＋Mobile | 点击主图进入全屏预览 | `ui_interaction` | `interaction_name=product_image_preview`；`action=open`；`element_id=main_image`；当前图片位置 | **缺失，需补** |
| PC＋Mobile | 关闭全屏预览 | `ui_interaction` | `action=close`；`element_id=image_preview_close`；保持的图片位置 | **缺失，需补** |
| PC＋Mobile | 预览内切图 | 复用图片 `change` | 预览场景、前后图片位置 | P21需明确预览场景复用 |
| Mobile | 双指／双击缩放进入或退出放大状态 | `ui_interaction` | `action=zoom_in/zoom_out`；图片位置、结果 | **缺失，需补** |

放大后的拖拽位移、无状态变化的边界滑动和单张图片加载反馈不单独记录分析事件。

#### 3.6.4 信息区、说明弹层与推荐

| 端 | 操作 | 建议记录 | 稳定业务名称／必要信息 | 当前 PRD |
|---|---|---|---|---|
| PC＋Mobile | 展开／收起 Condition、Description、Shipping & Returns | `ui_interaction` | P22 `module_id=product_information`；区块 ID、`expand/collapse` | 已覆盖 P22 |
| PC＋Mobile | 打开／关闭 Certified Authentic 弹层 | `ui_interaction` | `interaction_name=product_info_modal`；`action=open/close`；`target_id=certified_authentic` | **缺失，需补** |
| PC＋Mobile | 打开／关闭 Condition Guide | `ui_interaction` | 同上，`target_id=condition_guide` | **缺失，需补** |
| PC＋Mobile | 打开／关闭 Size Guide（实际支持该类目时） | `ui_interaction` | 同上，`target_id=size_guide` | **缺失，需补** |
| PC＋Mobile | You May Also Like／Recently Viewed商品曝光与点击 | `view_item_list`／`select_item` | 推荐请求、场景、模块、位置、商品三 ID | 已覆盖 P26 |
| PC＋Mobile | 推荐商品收藏／取消收藏 | `add_to_wishlist`／`remove_from_wishlist` | 推荐场景、商品三 ID、位置及来源 | 统一事件已存在；**需在P26明确引用** |
| PC＋Mobile | 横滑推荐列表／点击上一页下一页 | `ui_interaction` | `interaction_name=recommendation_rail`；`action=scroll/previous/next`；推荐模块及结果 | **缺失，需补** |
| PC＋Mobile | 点击Recently Viewed的View all／模块箭头 | `ui_interaction`＋目标页 `page_view` | `action=view_all`；`element_id=module_view_all`；`target_id=recently_viewed` | **缺失，需补** |
| PC＋Mobile | 点击Find More进入相似商品列表 | `ui_interaction`＋目标页 `page_view` | `module_id=similar_products_entry`；`action=select`；`element_id=find_more_button`；目标及当前商品三 ID | **缺失，需补** |

#### 3.6.5 Share To弹层

| 端 | 操作 | 建议记录 | 稳定业务名称／必要信息 | 当前 PRD |
|---|---|---|---|---|
| PC＋Mobile | 关闭分享弹层（关闭按钮、蒙层、下滑） | `ui_interaction` | `module_id=product_share`；`action=close`；关闭方式、商品三 ID | **缺失，需补** |
| PC＋Mobile | 选择WhatsApp、Message、Facebook、Pinterest、X、Messenger等渠道 | `ui_interaction` | `action=select_channel`；`element_id=share_channel`；`target_id=渠道稳定枚举`；商品三 ID、调用结果 | P50仅覆盖Share按钮，**渠道操作缺失** |
| PC＋Mobile | Copy Link | `ui_interaction` | `action=copy_link`；`element_id=copy_link_button`；商品三 ID、复制结果 | **缺失，需补** |
| PC＋Mobile | More调起系统分享面板 | `ui_interaction` | `action=open_system_share`；`element_id=more_share_button`；商品三 ID、调用结果 | **缺失，需补** |

不采集分享文案、联系人、外部账号或用户在外部应用中的行为；外部应用是否最终发送成功不冒充站内事实。

#### 3.6.6 本模块结论

商详购买主链路已覆盖，但页面交互仍需补：返回与购物袋入口、图片预览／关闭／缩放、三个说明弹层、推荐横滑／翻页／收藏／View all、Find More，以及Share To弹层的关闭、渠道、Copy Link和More。全部复用既有事件，不新增统一事件。

### 3.7 My Order＋Order Details

#### 3.7.1 UI 证据

Mobile、PC Figma 已核对订单列表、状态筛选、订单搜索展开／输入／自动检索／点击结果、订单详情首屏、Confirmed／On Its Way／Completed／Cancelled、单一物流、Billing／Shipping不同、Tax、营销信息、Refund弹窗和Contact入口。

#### 3.7.2 订单列表

| 端 | 操作或业务事实 | 建议记录 | 稳定业务名称／必要信息 | 当前 PRD |
|---|---|---|---|---|
| PC＋Mobile | My Orders页面到达 | `page_view` | `page_type=order`；`page_id=orders` | 已覆盖 P45 |
| PC＋Mobile | 切换Processing／Shipped／Delivered／Refunds等状态筛选 | `ui_interaction` | P45 `module_id=order_list`；`action=filter_status`；状态稳定值 | 已覆盖 P45 |
| PC＋Mobile | 点击订单卡进入详情 | `ui_interaction`＋详情页 `page_view` | `action=select_order`；`element_id=order_item`；`target_id=order_id` | 已覆盖 P45 |
| PC＋Mobile | 打开／关闭订单搜索 | `ui_interaction` | `interaction_name=order_search`；`action=open/close`；`element_id=order_search_entry` | **缺失，需补** |
| PC＋Mobile | 订单关键词形成一次正式查询／自动检索 | `ui_interaction` | `action=submit/auto_query`；`target_id=order_search`；查询结果状态 | **缺失，需补**；不得记录输入原文 |
| PC＋Mobile | 点击订单搜索结果进入详情 | `ui_interaction`＋详情页 `page_view` | `action=select_result`；`element_id=order_search_result`；`target_id=order_id` | **缺失，需补** |

订单列表加载、空态和订单状态展示不重造订单业务事实；只有Retry或用户主动操作才记录事件。

#### 3.7.3 订单详情

| 端 | 操作 | 建议记录 | 稳定业务名称／必要信息 | 当前 PRD |
|---|---|---|---|---|
| PC＋Mobile | 订单详情成功到达 | `page_view` | `page_type=order`；`page_id=order_detail`；`order_id` | 已覆盖 P46 |
| PC＋Mobile | 复制订单号 | `ui_interaction` | P46 `action=copy_order_id`；复制结果；`order_id` | 已覆盖 P46 |
| PC＋Mobile | 点击物流／Tracking入口 | `ui_interaction`＋目标结果 | P46 `action=select_tracking`；`order_id`、目标及结果 | 已覆盖 P46 |
| PC＋Mobile | 点击Return／售后入口 | `ui_interaction`＋目标页 `page_view` | P46 `action=select_return`；`order_id`、目标及结果 | 已覆盖 P46 |
| PC＋Mobile | 打开／关闭Refund说明弹窗 | `ui_interaction` | `module_id=order_refund_modal`；`interaction_name=refund_information`；`action=open/close`；`order_id` | **缺失，需补** |
| PC＋Mobile | 点击Contact／Customer Care入口 | `ui_interaction`＋目标页或外部目标结果 | `module_id=order_support`；`interaction_name=support_navigation`；`action=select`；`element_id=contact_entry`；`target_id=contact` | **缺失，需补** |
| PC＋Mobile | 页面返回 | `ui_interaction`＋目标页结果 | `module_id=order_detail_header`；`action=back`；`element_id=back_button`；`target_id=orders_or_previous` | **缺失，需补** |

订单状态、金额、Tax、地址、物流、退款结果和营销透传内容均从业务数据展示，不因页面展示生成新的订单、退款或营销事件；事件不得携带地址、电话等个人信息。

#### 3.7.4 本模块结论

订单状态Tab、订单选择、复制订单号、物流及退货入口已有覆盖。需要补：订单搜索全流程、Refund弹窗、Contact入口和页面返回。均使用 `ui_interaction`／`page_view`，订单和退款事实继续读取业务表或权威事件。

### 3.8 Returns

#### 3.8.1 UI 证据

Mobile、PC Figma 已核对：Returns列表与空态、按订单过滤、不可申请的多种原因、单／多商品选择、退货原因弹窗、图片上传前后、提交成功、驳回后修改与重新提交、取消退货、审核／寄回／判责／退款／关闭／完成状态、退款扣费说明和寄回说明。

#### 3.8.2 Returns列表与申请

| 端 | 操作或业务事实 | 建议记录 | 稳定业务名称／必要信息 | 当前 PRD |
|---|---|---|---|---|
| PC＋Mobile | Returns页面到达 | `page_view` | `page_type=returns`；`page_id=returns` | 已覆盖 P47／P48 |
| PC＋Mobile | 按订单筛选Returns列表 | `ui_interaction` | `module_id=returns_list`；`interaction_name=returns_filter`；`action=select_order/clear`；`target_id=order_id` | **缺失，需补** |
| PC＋Mobile | 选择Returns列表中的售后单 | `ui_interaction`＋详情状态页 `page_view` | `action=select_return_case`；`element_id=return_case_item`；`target_id=return_application_id` | P48过于概括，**需补稳定动作** |
| PC＋Mobile | 多商品订单选择／取消一个退货商品 | `ui_interaction` | P47 `module_id=returns_application`；`action=select_item/unselect_item`；`target_id=order_item_id` | P47仅有选择，**需补取消选择** |
| PC＋Mobile | 打开／关闭退货原因弹窗 | `ui_interaction` | `interaction_name=return_reason`；`action=open/close`；`element_id=return_reason_control` | **缺失，需补** |
| PC＋Mobile | 选择退货原因 | `ui_interaction` | P47 `action=select_reason`；低基数原因枚举、`order_item_id` | 已覆盖；自由说明不采集 |
| PC＋Mobile | 上传／删除／替换凭证图片 | `ui_interaction` | `interaction_name=return_evidence`；`action=upload/delete/replace`；图片数量、结果 | **缺失，需补**；不得上传图片内容、文件名或地址到普通分析事件 |
| PC＋Mobile | 提交申请 | `ui_interaction` | P47 `action=submit`；`element_id=return_submit_button`；`target_id=order_item_id`；结果 | 已覆盖 P47；业务受理结果读取售后表 |
| PC＋Mobile | 修改被驳回／待修改的申请 | `ui_interaction` | `interaction_name=return_application`；`action=edit`；`target_id=return_application_id` | **缺失，需补** |
| PC＋Mobile | 重新提交修改后的申请 | `ui_interaction` | `action=resubmit`；`element_id=return_resubmit_button`；售后对象、结果 | **缺失，需补** |
| PC＋Mobile | 取消退货并确认／关闭确认框 | `ui_interaction` | P47基础上拆分 `action=open_cancel/confirm_cancel/close_cancel`；`target_id=return_application_id` | P47仅概括cancel，**需拆稳定动作** |

#### 3.8.3 说明入口与状态页

| 端 | 操作 | 建议记录 | 稳定业务名称／必要信息 | 当前 PRD |
|---|---|---|---|---|
| PC＋Mobile | 打开／关闭退款扣费说明 | `ui_interaction` | `module_id=returns_information`；`interaction_name=refund_fee_information`；`action=open/close`；售后对象 | **缺失，需补** |
| PC＋Mobile | 打开／关闭How to Return／怎么寄回说明 | `ui_interaction` | `interaction_name=return_shipping_information`；`action=open/close`；售后对象 | **缺失，需补** |
| PC＋Mobile | 状态页返回／联系客服 | `ui_interaction`＋目标结果 | `action=back/contact_support`；`element_id=back_button/support_button`；目标为Returns上一页或`contact_us` | 已补入v1.5 P56 |
| PC＋Mobile | 待审核／待修改状态点击Update My Request／Cancel Request | `ui_interaction` | `action=update_request/open_cancel_request`；对应稳定按钮；`target_id=return_application_id` | 已补入v1.5 P56 |
| PC＋Mobile | 审核通过待寄回：复制寄回单号／查看物流 | `ui_interaction`＋目标结果 | `action=copy_return_tracking/view_return_tracking`；对应稳定控件；`target_id=shipment_id` | 已补入v1.5 P56 |
| PC＋Mobile | 打开／关闭How to ship it back | `ui_interaction` | `interaction_name=return_shipping_information`；`action=open/close`；`target_id=return_application_id` | 已补入v1.5 P56 |
| PC＋Mobile | 打开／关闭Return deduction说明 | `ui_interaction` | `interaction_name=refund_fee_information`；`action=open/close`；`target_id=return_application_id` | 已补入v1.5 P56 |

空态、不可申请原因、审核中、已关闭、待退款、退款中、退款在途和已完成等仅展示时不形成用户行为事件；售后状态、受理、拒绝、结案和退款金额继续读取售后／退款权威事实。

#### 3.8.4 本模块结论

Returns已按Figma各状态页补齐实际操作：列表筛选、售后单选择、取消商品选择、原因弹窗、凭证图片、编辑／重新提交、取消确认、扣费说明、寄回说明、返回、联系客服、Update My Request、Cancel Request及寄回物流操作。仍不新增售后业务事件，页面动作使用 `ui_interaction`，状态读取业务表。

### 3.9 Delivery

#### 3.9.1 UI 证据

Mobile、PC Figma 已核对。两端均包含物流详情弹窗的在途状态和送达状态；送达状态包含初始位置与滑动到底两种设计状态。该模块展示订单物流轨迹，不创建新的履约业务事实。

#### 3.9.2 有意义操作

| 端 | 操作 | 建议记录 | 稳定业务名称／必要信息 | 当前 PRD |
|---|---|---|---|---|
| PC＋Mobile | 打开物流详情弹窗 | `ui_interaction` | `module_id=delivery_tracking`；`interaction_name=tracking_details`；`action=open`；`element_id=tracking_details_entry`；`target_id=shipment_id`；`order_id` | P45仅概括“进入物流详情”，需补稳定动作 |
| PC＋Mobile | 关闭物流详情弹窗 | `ui_interaction` | `module_id=delivery_tracking`；`interaction_name=tracking_details`；`action=close`；`element_id=tracking_details_close`；`target_id=shipment_id` | **缺失，需补** |
| PC＋Mobile | 在物流轨迹中滚动到底 | 不单独记录 | 页面滚动本身不构成独立业务意图；如需分析内容是否被看到，应另定义内容曝光规则，本期不新增 | 无需补埋点 |

物流在途、送达及轨迹节点来自履约业务数据；仅展示或滚动不生成新的物流事件。事件不得携带收货地址、姓名、电话或完整物流文本。

#### 3.9.3 本模块结论

Delivery只需把“进入物流详情”拆成可实施的打开／关闭动作；在途、送达和轨迹内容直接读取履约业务数据，不新增物流状态埋点。

### 3.10 Shopping Bag

#### 3.10.1 UI 与运行证据

Mobile Figma 已核对购物袋首屏、兜底、取消全选和少量商品状态；PC Figma 已核对多商品、兜底、未登录、已登录、优惠券和失效商品状态。测试站同时核对空购物袋及 Continue Shopping。此前 Mobile 运行态已实际验证逐项选择、Select All、左滑露出 Move To Wishlist／Delete、删除商品及 Check Out。

#### 3.10.2 商品与选择操作

| 端 | 操作 | 建议记录 | 稳定业务名称／必要信息 | 当前 PRD |
|---|---|---|---|---|
| PC＋Mobile | 购物袋成功展示 | `view_cart` | `cart_id`、金额币种、`items[]`商品三 ID、数量 | 已覆盖 P29 |
| PC＋Mobile | 点击购物袋商品进入商详 | `select_item`＋目标页 `page_view` | `module_id=shopping_bag_items`；商品三 ID、位置、来源上下文 | P30已覆盖 |
| PC＋Mobile | 选择／取消选择单个商品 | `ui_interaction` | P31 `action=select_item/unselect_item`；`target_id=listing_public_code` | 已覆盖 |
| PC＋Mobile | 全选／取消全选 | `ui_interaction` | P31 `action=select_all/unselect_all`；选中数量、结果 | 已覆盖 |
| PC＋Mobile | 增加／减少商品数量 | `ui_interaction` | `interaction_name=cart_quantity`；`action=increase/decrease`；商品三 ID、变更前后数量、结果 | **缺失，需补**；仅适用于UI实际允许调整数量的商品 |
| Mobile | 左滑打开／关闭商品操作区 | `ui_interaction` | P32 `action=reveal/close`；`element_id=cart_item_action_panel`；商品三 ID | P32仅有reveal，**需补close** |
| PC＋Mobile | 删除商品成功 | `remove_from_cart` | `cart_id`、商品三 ID、数量、金额币种、交互关联 ID | 已覆盖 P33 |
| PC＋Mobile | Move To Wishlist | `add_to_wishlist`＋`remove_from_cart` | 两个真实状态转换共享交互关联 ID；商品三 ID、各自结果 | 已覆盖 P34 |
| PC＋Mobile | 点击Check Out | `begin_checkout`／沿用搜推 `checkout_start` 进入一方平台 | `cart_id`、金额币种、`items[]`、来源为购物袋 | 已覆盖 P35 |

#### 3.10.3 空态、优惠券与异常状态

| 端 | 操作 | 建议记录 | 稳定业务名称／必要信息 | 当前 PRD |
|---|---|---|---|---|
| PC＋Mobile | 空购物袋点击Continue Shopping | `ui_interaction`＋目标页 `page_view` | `module_id=cart_empty_state`；`interaction_name=continue_shopping`；`action=select`；`element_id=continue_shopping_button`；目标页面 | **缺失，需补** |
| PC＋Mobile | 输入并Apply优惠券 | `ui_interaction` | `module_id=cart_coupon`；`interaction_name=coupon`；`action=apply`；优惠结果枚举、金额变化；不得上传用户输入原文 | P39仅覆盖Checkout优惠码，购物袋场景**需补稳定节点** |
| PC＋Mobile | 移除已应用优惠券 | `ui_interaction` | `module_id=cart_coupon`；`action=remove`；优惠类型／结果 | **缺失，需补** |
| PC＋Mobile | 未登录状态点击登录／继续 | `ui_interaction`＋目标页结果 | `module_id=cart_authentication`；`interaction_name=authentication_entry`；`action=select`；稳定入口 ID | **缺失，需补** |
| PC | 失效商品区点击Clear all | `ui_interaction`；实际移除结果复用`remove_from_cart` | `module_id=cart_unavailable_items`；`action=clear_unavailable_items`；`element_id=clear_all_button`；`cart_id`、受影响商品数量和结果 | 已补入v1.5 P58 |

购物袋兜底、登录态、优惠券是否有效和商品失效均为页面状态或业务校验结果；不能把页面展示本身记成成功业务事件。地址、自由输入优惠码和错误原文不得进入普通分析事件。

#### 3.10.4 本模块结论

购物袋补充项已写入v1.5：数量调整、Mobile关闭左滑操作区、空态Continue Shopping、购物袋优惠券、未登录入口，以及PC失效商品区Clear all。PC与Mobile使用相同业务动作名，仅控件形态不同。

### 3.11 Checkout

#### 3.11.1 UI 与运行证据

Mobile、PC Figma 已核对 Checkout 主页面、地址填写及弹窗、联系方式与配送信息、单／多商品、优惠码输入／成功／报错、支付成功页优惠展示，以及 PC 安全码和Phone提示状态。测试站已实际核对联系方式与配送字段、营销订阅开关、Card／PayPal／Klarna方式切换和固定 Pay Now；未执行Pay Now，不把支付结果写成已验证。

#### 3.11.2 联系方式、地址与配送

| 端 | 操作 | 建议记录 | 稳定业务名称／必要信息 | 当前 PRD |
|---|---|---|---|---|
| PC＋Mobile | Checkout页面到达 | `page_view` | `page_type=checkout`；`page_id=checkout`；`checkout_session_id`如已存在 | 已覆盖 P36-P40 上下文 |
| PC＋Mobile | 勾选／取消营销订阅 | `ui_interaction` | P36 `interaction_name=marketing_subscription`；`action=enable/disable`；结果；不得带邮箱 | 已覆盖 P36 |
| PC＋Mobile | 新增、编辑或选择已有配送地址 | `ui_interaction` | `module_id=checkout_delivery_address`；`interaction_name=delivery_address`；`action=add/edit/select`；`target_id=address_id`或稳定新增目标；结果 | P37仅定义ready结果，**缺失用户动作** |
| PC＋Mobile | 保存地址 | `ui_interaction` | `action=save`；`element_id=delivery_address_save_button`；`target_id=address_id`或`new_address`；校验结果；不得携带地址明文 | **缺失，需补** |
| PC＋Mobile | 打开／关闭Phone说明 | `ui_interaction` | `interaction_name=phone_information`；`action=open/close`；`element_id=phone_information_control` | **缺失，需补** |
| PC＋Mobile | 选择配送方式并达到可继续结账状态 | 选择动作 `ui_interaction`；ready事实 `add_shipping_info` | P37 `shipping_tier`、`reuse_existing`、`items[]`、结果 | 已覆盖 P37；需保留新增／复用信息区别 |

#### 3.11.3 支付、优惠与提交

| 端 | 操作 | 建议记录 | 稳定业务名称／必要信息 | 当前 PRD |
|---|---|---|---|---|
| PC＋Mobile | 选择Card／PayPal／Klarna等支付方式 | `ui_interaction` | P38 `interaction_name=payment_method`；`action=select`；低基数 `payment_type`、结果 | 已覆盖 P38 |
| PC＋Mobile | 支付信息达到可继续结账状态 | `add_payment_info` | `checkout_session_id`、`payment_type`、是否复用已有信息、`items[]`；不得携带卡号、token或网关原文 | 已覆盖 P38；需覆盖新增与复用两类用户 |
| PC | 打开／关闭安全码说明 | `ui_interaction` | `module_id=checkout_payment`；`interaction_name=security_code_information`；`action=open/close`；稳定控件 ID | **缺失，需补** |
| PC＋Mobile | Apply优惠码 | `ui_interaction` | P39 `action=apply`；优惠结果枚举、金额变化；不得上传输入原文 | 已覆盖 P39 |
| PC＋Mobile | 移除已应用优惠码 | `ui_interaction` | P39 `action=remove`；优惠类型、结果 | P39已有remove |
| PC＋Mobile | 点击Pay Now | `pay_now_click` | P40 `checkout_session_id`、提交校验结果、`items[]` | 已覆盖 P40；订单创建与支付结果由服务端权威事实提供 |
| Mobile | 支付成功页复制订单号 | `ui_interaction` | `module_id=payment_success`；`action=copy_order_id`；`element_id=order_id_copy_button`；`target_id=order_id` | 已补入v1.5 P59 |
| Mobile | 支付成功页点击Continue Shopping | `ui_interaction`＋目标页 `page_view` | `module_id=payment_success`；`action=continue_shopping`；`element_id=continue_shopping_button`；`target_id=shop`；`order_id` | 已补入v1.5 P59 |

#### 3.11.4 本模块结论

Checkout补充项已写入v1.5：地址新增／编辑／选择／保存、Phone与安全码说明，以及支付成功页复制订单号和Continue Shopping。地址、卡号、电话、邮箱、优惠码原文及网关返回原文不得进入普通分析事件。

### 3.12 个人中心（地址管理）

#### 3.12.1 UI 证据

PC、Mobile Figma 已核对个人中心地址编辑、State与ZIP不匹配提示及ZIP弱拦截状态。地址内容属于个人信息，只记录操作类型与结果，不记录字段值。

#### 3.12.2 有意义操作

| 端 | 操作 | 建议记录 | 稳定业务名称／必要信息 | 当前 PRD |
|---|---|---|---|---|
| PC＋Mobile | 进入地址列表／地址编辑页 | `page_view` | `page_type=account_address_list/account_address_edit`；稳定 `page_id` | P43仅概括地址管理，**需补页面映射** |
| PC＋Mobile | 点击新增地址 | `ui_interaction` | P43 `action=add`；`element_id=add_address_button`；`target_id=new_address` | P43已有add |
| PC＋Mobile | 点击编辑地址 | `ui_interaction` | P43 `action=edit`；`element_id=edit_address_button`；`target_id=address_id` | P43已有edit |
| PC＋Mobile | 保存地址 | `ui_interaction` | P43 `action=save`；`element_id=save_address_button`；`target_id=address_id/new_address`；`result_state` | P43已有save |
| PC＋Mobile | 删除地址并确认／取消 | `ui_interaction` | P43拆分 `action=open_delete/confirm_delete/cancel_delete`；`target_id=address_id` | P43仅有delete，**需拆确认动作** |
| PC＋Mobile | 设为默认地址 | `ui_interaction` | P43 `action=set_default`；`target_id=address_id`；结果 | P43已有set_default |
| PC＋Mobile | 取消编辑／返回 | `ui_interaction`＋目标页结果 | `action=cancel/back`；稳定控件 ID；`target_id=account_address_list` | **缺失，需补** |

State与ZIP不匹配、必填缺失和保存失败属于本次保存的 `result_state`／低基数 `failure_type`，不得上传地址、ZIP、姓名或电话原文。

### 3.13 个人中心 Account

#### 3.13.1 UI 证据

Mobile、PC Figma 最新可见稿已核对：登录／未登录Account、订单状态入口、Profile昵称与Gender、Country／Region、Language、Currency、Subscriptions各状态、Policies、Privacy／Manage Your Data和Log Out。测试站登录态也已确认订单状态、Profile、Addresses、市场／语言／币种、订阅与Privacy & Data入口。

#### 3.13.2 页面入口与账户操作

| 端 | 操作 | 建议记录 | 稳定业务名称／必要信息 | 当前 PRD |
|---|---|---|---|---|
| PC＋Mobile | 进入Account首页 | `page_view` | `page_type=account`；`page_id=account`；登录状态 | P42需明确登录／未登录共用页面模板 |
| PC＋Mobile | 点击订单状态入口 | `ui_interaction`＋目标页 `page_view` | `module_id=account_orders`；`interaction_name=order_status_entry`；`action=select`；`target_id=processing/shipped/delivered/refunds` | **缺失，需补** |
| PC＋Mobile | 点击Profile／Addresses／Policies／Privacy等菜单 | `ui_interaction`＋目标页 `page_view` | `module_id=account_navigation`；`interaction_name=account_section`；`action=select`；稳定 `target_id` | P42 `select_section`过于概括，**需补完整枚举** |
| PC＋Mobile | 编辑昵称／选择Gender并保存 | `ui_interaction` | P42 `action=edit/save`；`target_id=nickname/gender`；结果；不得携带昵称原文 | P42需补具体目标枚举 |
| PC＋Mobile | 选择Country／Region、Language、Currency | `ui_interaction` | `module_id=account_preferences`；`interaction_name=preference`；`action=open/select/close`；`target_id=country_region/language/currency`；选择后的稳定枚举 | P42仅有select_preference，**需拆控件动作** |
| PC＋Mobile | 订阅／取消订阅 | `ui_interaction` | P44 `action=subscribe/unsubscribe`；登录状态、结果；不得带邮箱 | P44已有主要动作；需覆盖未登录、写入中、失败与成功结果 |
| PC＋Mobile | 点击Manage Your Data／隐私功能 | `ui_interaction`＋目标页 `page_view` | `module_id=account_privacy`；`interaction_name=privacy_action`；按UI实际功能登记 `open_download_data/open_delete_account/open_privacy_preferences` 等稳定动作 | **缺失，需按最新UI补**；不得把设计稿当成已上线能力 |
| PC＋Mobile | Log Out并确认／取消 | `ui_interaction` | `module_id=account_authentication`；`interaction_name=logout`；`action=open/confirm/cancel`；结果 | P49仅写logout，**需拆确认动作** |
| PC＋Mobile | 未登录状态点击Login／Register | `ui_interaction`＋目标页 `page_view` | `module_id=account_authentication`；`interaction_name=authentication_entry`；`action=login/register`；稳定入口 | **缺失，需补** |

#### 3.13.3 本模块结论

Account现稿的通用 `select_section` 不足以让开发逐项实施。需补齐订单状态入口、全部账户菜单、偏好弹层、Profile编辑目标、订阅结果、隐私功能入口和登出确认。个人资料内容不进入普通分析事件。

### 3.14 Contact Us

#### 3.14.1 UI 与运行证据

Mobile、PC Figma 已核对Contact Us默认、填写完成、提交成功和提交报错状态，以及联系邮箱、服务时间和Your Privacy Choices入口。测试站Footer确认存在Contact Us入口并指向`/en-US/pages/contact`；本轮该目标页导航超时，因此运行态表单未作为已验证证据。

#### 3.14.2 有意义操作

| 端 | 操作 | 建议记录 | 稳定业务名称／必要信息 | 当前 PRD |
|---|---|---|---|---|
| PC＋Mobile | Contact Us页面到达 | `page_view` | `page_type=contact_us`；`page_id=contact_us` | 当前缺独立页面映射，**需补** |
| PC＋Mobile | 提交联系表单 | `ui_interaction` | `module_id=contact_form`；`interaction_name=contact_request`；`action=submit`；`result_state=success/failed`；低基数 `failure_type` | **缺失，需补** |
| PC＋Mobile | 点击联系邮箱 | `ui_interaction` | `module_id=contact_information`；`interaction_name=email_contact`；`action=select`；`element_id=contact_email_link`；结果 | **缺失，需补**；不得上传邮箱地址或邮件内容 |
| PC＋Mobile | 点击Your Privacy Choices | `ui_interaction`＋目标页 `page_view` | `module_id=contact_footer`；`interaction_name=policy_navigation`；`action=select`；`target_id=your_privacy_choices` | **缺失，需补** |

姓名、邮箱、电话、主题、自由文本、附件及错误原文不得进入普通分析事件；表单输入、聚焦和逐字段修改不单独记录，避免采集敏感内容和噪声。

#### 3.14.3 本模块结论

Contact Us需新增页面映射、表单提交结果、联系邮箱和隐私入口点击。只采集操作与低基数结果，不采集表单内容。

### 3.15 About Us

#### 3.15.1 UI 证据

Mobile、PC Figma 已核对About Us页面；最新稿主要为Who We Are等内容与样式调整。当前没有看到需要形成独立业务事件的表单或业务状态。

#### 3.15.2 有意义操作

| 端 | 操作 | 建议记录 | 稳定业务名称／必要信息 | 当前 PRD |
|---|---|---|---|---|
| PC＋Mobile | About Us页面到达 | `page_view` | `page_type=about_us`；`page_id=about_us` | 当前缺独立页面映射，**需补** |
| PC＋Mobile | 页面内实际存在的导航型CTA | `ui_interaction`＋目标页 `page_view` | `module_id=about_us_content`；`interaction_name=about_navigation`；`action=select`；按UI实际CTA登记稳定 `element_id/target_id` | Figma当前可见层级未确认独立CTA；如开发页面存在则补入，不得猜测 |

普通内容滚动、阅读和文字选择不单独采集。

#### 3.15.3 本模块结论

About Us当前只确定需要稳定 `page_view` 页面映射；没有证据支持新增专属业务事件。若最终页面包含导航型CTA，再按实际控件补一条 `ui_interaction`。

