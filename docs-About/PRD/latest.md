# Looply 品牌介绍页 PRD v1.0

> 覆盖页面：About Looply、Our Group、Sustainability  
> 终端：PC Web、Mobile Web  
> 日期：2026-11-24

## 1. 范围与设计依据

三页分别承担品牌介绍、集团能力介绍、可持续发展介绍，并通过正文入口连接购物、卖货、鉴定与联系页面。游客与登录用户均可浏览。

本次交付三页内容区、页面间跳转、About 首图轮播、门店图库，以及 H5 Account Settings 的 About 入口与四项列表。卖货、预约、鉴定、联系和购物页面承接各自业务流程。

**页面文案、数值、配图、图片顺序及视觉样式以用户维护的 Figma 为准，PRD 不另建文案副本。**本文补充静态设计稿未表达完整的交互与跳转规则。

| 页面 | PC 设计稿 | Mobile 设计稿 |
|---|---|---|
| About Looply | [PC About · 10889:2631](https://www.figma.com/design/sAOLkw0gIl1bwQRYCDqKuW/Looply-1.1?node-id=10889-2631) | [Mobile About · 10889:3845](https://www.figma.com/design/sAOLkw0gIl1bwQRYCDqKuW/Looply-1.1?node-id=10889-3845) |
| Our Group | [PC Group · 10889:3080](https://www.figma.com/design/sAOLkw0gIl1bwQRYCDqKuW/Looply-1.1?node-id=10889-3080) | [Mobile Group · 10889:4013](https://www.figma.com/design/sAOLkw0gIl1bwQRYCDqKuW/Looply-1.1?node-id=10889-4013) |
| Sustainability | [PC Sustainability · 10889:3475](https://www.figma.com/design/sAOLkw0gIl1bwQRYCDqKuW/Looply-1.1?node-id=10889-3475) | [Mobile Sustainability · 10889:4154](https://www.figma.com/design/sAOLkw0gIl1bwQRYCDqKuW/Looply-1.1?node-id=10889-4154) |

设计基线：Looply 1.1「11.24-About Looply 全新改版」。H5 [Account Settings](https://www.figma.com/design/sAOLkw0gIl1bwQRYCDqKuW/Looply-1.1?node-id=10889-8262) 与 [About 列表页](https://www.figma.com/design/sAOLkw0gIl1bwQRYCDqKuW/Looply-1.1?node-id=10889-8476) 同属本次入口范围。

## 2. 公共规则

### 2.1 页面入口与导航

- PC 公共 Footer 的 About 栏提供三页入口，接入规则见[Footer PRD v0.8](../../docs-首页/PRD/looply-Footer-PRD-v0.8.md)；页面正文入口按第 6 节跳转。
- Mobile 首页推荐 Feed 内的 About 入口、个人中心 About Banner 均进入 About Looply；入口展示由各来源页面负责，点击采集见统一埋点需求 §8.7。
- H5 个人中心 Account Settings 最后一项为 About，进入 §2.3 的 About 列表页。
- PC 接入站点公共 Header、Footer。公共搜索、账户、收藏、购物袋、订阅及语言选择由公共组件负责。
- Mobile 顶部展示返回按钮与当前页面名称。点击返回回到上一级页面；直接打开且无返回历史时进入首页，沿用原 About 返回规则。
- 进入任一介绍页时展示该页内容。正文内站内链接在当前页面打开，目标页面负责其登录、资格判断和异常处理。

### 2.2 内容与图片

- 文案按 Figma 的模块、层级、强调样式和顺序展示；文本自然换行，不以截断正文维持固定卡片高度。
- 同一模块在 PC 与 Mobile 使用对应端设计稿的排列和裁切；不能直接缩放整张 PC 页面作为手机页面。
- 图片加载期间保留对应图片区域；加载失败时保留中性底色，文字、链接及其他已加载模块继续可用。刷新页面可重新加载，沿用原 About 图片降级规则。
- 展示图片按内容图处理；可切换图片的操作仅定义在第 3.2、4.2 节。

### 2.3 H5 Account Settings · About 入口与列表页

Account Settings 底部新增一行 About，位于该设置列表最后，沿用设置行的整行点击与右箭头样式。游客和登录用户均可使用。点击在当前标签页进入 About 列表页，保留当前站点国家及语言。

列表页顶部为返回按钮和标题 About，正文按以下顺序展示四行，每行文字及右箭头共同组成一个点击区域。四项与 PC Footer 的 About 栏目标一致。

| 顺序 | 入口 | 点击目标 |
|---|---|---|
| 1 | About Looply | About Looply 页面 |
| 2 | Authenticity | 鉴定介绍页，与 §6 鉴定目标一致 |
| 3 | Our Group | Our Group 页面 |
| 4 | Sustainability | Sustainability 页面 |

点击任一行在当前标签页进入对应页面；从目标页返回时回到 About 列表页，列表页返回时回到个人中心。直接访问列表且无站内返回历史时，返回个人中心。目标页面内部规则由所属模块负责。

Account Settings 的 About 进入此列表；个人中心原 About Banner 和首页 Feed 的 About 仍直接进入 About Looply。入口文案使用静态 UI 多语言资源，映射见 §7.1；来源点击、列表访问和列表内点击见统一采集 §8.7。

## 3. About Looply

### 3.1 模块与排列

| 顺序 | 模块 | 展示内容与操作 | PC / Mobile 差异 |
|---|---|---|---|
| 1 | 品牌首屏与 Our Story | 品牌介绍、首图轮播、两项品牌数据、品牌故事、集团入口 | PC 首屏文字左右排列，数据并列；Mobile 文字上下排列，两项数据并列 |
| 2 | What we believe | 品牌理念与 Sustainability 入口 | 两端按对应稿居中展示 |
| 3 | Two Ways Into Looply | 买家与卖家两张图文卡，分别提供购物和卖货入口 | PC 并列；Mobile 先买家、后卖家 |
| 4 | How we work | 专业鉴定、成色说明、实物拍摄三项说明，两张配图，鉴定入口 | PC 图文左右；Mobile 配图位于三项说明之前 |
| 5 | Local seller services | 上门、到店、邮寄三项服务介绍，以及统一卖家服务入口 | PC 三列；Mobile 按同顺序纵向排列 |
| 6 | Let’s connect | 办公区图片、联系入口、地址、预约说明与预约入口 | PC 图文左右；Mobile 图片在前，随后联系与预约信息 |

各模块按上表顺序组成同一长页。服务卡展示服务说明，通过统一入口进入卖货页；联系与预约使用各自入口。

### 3.2 首图轮播

对应设计：第 1 节 PC／Mobile About Looply 首图区域。

1. 共 4 张图，首次打开展示 Figma 图片顺序中的第 1 张，下方对应指示条为选中态。
2. 页面可见时每 4 秒切换到下一张；第 4 张之后回到第 1 张。
3. 点击任一指示条，立即展示对应图片并更新选中态；从本次操作起重新计时 4 秒。
4. 选中图片与选中指示条始终一一对应；切换时保持图片容器尺寸，页面其余内容不跳动。

## 4. Our Group

### 4.1 模块与排列

| 顺序 | 模块 | 展示内容与操作 | PC / Mobile 差异 |
|---|---|---|---|
| 1 | 集团介绍 | 集团与 Looply 的关系、累计售出数据及截止日期 | PC 介绍与数据左右排列；Mobile 上下排列 |
| 2 | Pre-owned luxury expertise | 团队照片墙、团队经验与累计检查说明、三项能力、鉴定入口 | PC 照片墙下方分列正文与能力；Mobile 按对应稿纵向排列 |
| 3 | Super Zhuanzhuan | 门店介绍及商品规模，上海、北京两家门店的图库、名称、位置、面积和说明 | PC 两店并列；Mobile 先上海、后北京 |
| 4 | Sustainability | 可持续发展图文介绍与页面入口 | PC 图文左右；Mobile 按对应稿纵向排列 |
| 5 | 关联页面 | About 与 Authentication 两张导流卡 | PC 并列；Mobile 上下排列 |

集团介绍中的成交、鉴定和商品规模分别随各自说明展示，不将集团数据改写为 Looply 自身业务数据。

### 4.2 门店图库

对应设计：第 1 节 PC／Mobile Our Group 的 Super Zhuanzhuan 门店区域。

1. 上海、北京各 3 张图片，顺序、素材及默认主图按 Figma。
2. 每个图库包含一张主图及下方 3 个缩略图。首次打开选中第 1 个缩略图，主图展示对应图片。
3. 点击缩略图，替换本门店主图，并将选中标识移到该缩略图；门店信息保持原内容。
4. 两个图库独立切换；操作上海图库不改变北京图库，反之亦然。
5. 切换图片保持主图容器大小。图库由缩略图手动切换；重复点击当前缩略图保持当前状态。

## 5. Sustainability

### 5.1 模块与排列

| 顺序 | 模块 | 展示内容与操作 | PC / Mobile 差异 |
|---|---|---|---|
| 1 | 可持续发展首屏 | 背景图、主张与介绍 | PC 文字叠在图片上；Mobile 图片与文字分区 |
| 2 | Sustainability in action | SBTi、CDP、LEED 三张证据卡及对应材料入口 | PC 三列；Mobile 按同顺序纵向排列 |
| 3 | Rooftop solar | 青岛仓储与鉴定中心配图、减排数据、用电说明 | PC 图文左右；Mobile 上图下文 |
| 4 | Local action. Global dialogue. | COP28、COP29、COP30、COP31 四条图文内容 | PC 两列两行；Mobile 按年份升序纵排 |
| 5 | 底部转化区 | 背景图、介绍、购物与卖货两个按钮 | PC 按钮并列；Mobile 购物在上、卖货在下 |

### 5.2 证据与报道入口

- 每张证据卡的链接打开对应机构目标页、评分报告或证书，材料与卡片项目对应。
- 光伏模块中的年份、减排数据及用电说明作为一个内容单元展示，完整保留单位。
- COP 按 2023 → 2024 → 2025 → 2026 排列。COP28 提供报道入口；其余三条展示图文内容。
- SBTi 目标页、CDP 评分图片、LEED 证书均在当前标签页打开；图片和 PDF 使用浏览器原生展示。COP28 报道在新标签页打开，保留当前介绍页。

## 6. 正文跳转表

下列英文用于识别入口，最终显示文案取自 Figma。站内目标保留当前语言；表中路径为英文目标。三页互跳以页面名称标识，不将本地 Demo 文件名作为生产地址。

| 页面 / 入口 | 目标 |
|---|---|
| About / Meet our Group | Our Group |
| About / Explore our approach to sustainability | Sustainability |
| About / Explore the collection | 首页：/en-US |
| About / How selling works | 卖货首页：/en-US/sell |
| About / Explore our authentication process | 鉴定页：/en-US/authenticity |
| About / Explore seller services | 卖货首页：/en-US/sell |
| About / Contact us | 联系页：/en-US/pages/contact |
| About / Book an appointment | 预约页：/en-US/sell/request |
| Group / See how Looply authenticates | 鉴定页：/en-US/authenticity |
| Group / Explore the Group’s sustainability efforts | Sustainability |
| Group / About Looply | About Looply |
| Group / Our authentication process | 鉴定页：/en-US/authenticity |
| Sustainability / Check our targets on SBTi | [SBTi 目标页面](https://sciencebasedtargets.org/target-dashboard) |
| Sustainability / View 2023 score report | Demo 对应材料：assets/sustainability/cdp-score-2023.png |
| Sustainability / View certificate | Demo 对应材料：assets/sustainability/leed-gold.pdf |
| Sustainability / Read the press release | [COP28 英文报道](https://www.prnewswire.com/apac/news-releases/zhuanzhuan-makes-debut-at-cop28-the-first-chinese-secondhand-platform-on-the-global-stage-302015081.html) |
| Sustainability / Shop pre-owned | 新品集合：/en-US/collections/new-arrivals |
| Sustainability / Sell to Looply | 卖货首页：/en-US/sell |

## 7. 接入依赖

| 依赖 | 本次要求 |
|---|---|
| 目标业务页 | 第 6 节目标承接实际购物、卖货、预约、联系及鉴定流程；介绍页只负责入口 |
| 证据素材 | 发布后的评分图片、证书文件可访问，内容与对应项目一致；Demo 相对路径只用于定位源材料 |
| 多语言 | 英文设计稿作为源文案；三页资源字段、静态 UI 标识和缺译结果执行 §7.1 |
| 数据采集 | 三页访问、18 个正文入口、首图及门店图库手动切换、Mobile 返回、两个 Mobile 来源入口及 Footer 导航统一执行[数据采集与埋点产品需求 v2.1 §8.7](looply-数据采集与埋点产品需求-v2.1.md#87-品牌介绍三页采集补充2026-11-24)；复用原 About 五个点位，自动轮播不记手动操作 |

### 7.1 多语言接入

执行[品牌介绍三页多语言资源映射 v1.0](looply-品牌介绍页-多语言映射-v1.0.md)：延续 About 资源并扩展字段，新建 Group 与 Sustainability 资源；三页 PC／Mobile 共用同一内容源。字段、语种、缺译兜底、固定 UI 标识和资源迁移要求集中维护在该表，文案正文仍只取 Figma。

## 8. 验收要点

1. PC 与 Mobile 分别对照第 1 节对应画板，核对三页模块顺序、文案、素材、重点数字及单位；不以旧 Demo 文案覆盖设计稿。
2. About 首次展示第 1 张；每 4 秒顺序切换并循环；点击任一指示条可切换到正确图片，选中态和计时同步。
3. 上海、北京各 3 张图；点击缩略图只更新所属门店，选中态准确，主图区域不因图片变化而改变高度。
4. 按第 6 节逐项检查目标，特别区分 About 购物入口进入首页、Sustainability 购物入口进入新品集合。
5. 三张证据卡分别在当前标签页打开对应目标；COP28 在新标签页打开英文报道并保留介绍页。
6. Mobile 有历史时返回上一页，无历史时进入首页；游客与登录态均可阅读内容与操作入口。
7. 图片加载失败不遮挡正文和 CTA，不将其他成功模块替换为整页错误。
8. 各端正文完整显示；窄屏不出现横向溢出、图片挤压文字或按钮遮挡。
9. 埋点按统一需求 §8.7 验收：检查访问、18 个正文入口、主动图片切换、返回、两个 Mobile 来源入口及 PC Footer；自动轮播与重复选中不补造手动切换事件。
10. 英／西语分别检查三页及内部跳转；缺少某字段西语译文时仅该字段显示英文，其他译文正常展示；材料原件保持原内容。
11. H5 游客／登录态分别检查 Account Settings 末尾 About → 四项列表 → 对应内容页，确认顺序、整行点击、国家／语言保留及逐级返回；原 Banner／Feed 仍直达 About Looply。列表直达时返回个人中心。
