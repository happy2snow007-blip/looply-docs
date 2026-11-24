# Looply 品牌介绍页 Checklist

> 日期：2026-11-24。用于本轮 PRD 输入核对与差异确认；不是开发需求基线。

## 1. 范围与来源

用户要求对照 Demo 与 Figma 编写 PRD。指定文件包含三页、六个画板：

| 页面 | PC 画板 | Mobile 画板 | 本地 Demo |
|---|---|---|---|
| About Looply | [4:24](https://www.figma.com/design/kbUnfwTCHtQKpBwD9XGo5c/About-Looply?node-id=4-24) | [19:2](https://www.figma.com/design/kbUnfwTCHtQKpBwD9XGo5c/About-Looply?node-id=19-2) | outputs/brand-pages-20261117/demo/Looply_About.html |
| Our Group | [4:887](https://www.figma.com/design/kbUnfwTCHtQKpBwD9XGo5c/About-Looply?node-id=4-887) | [20:233](https://www.figma.com/design/kbUnfwTCHtQKpBwD9XGo5c/About-Looply?node-id=20-233) | outputs/brand-pages-20261117/demo/Looply_Group.html |
| Sustainability | [4:1409](https://www.figma.com/design/kbUnfwTCHtQKpBwD9XGo5c/About-Looply?node-id=4-1409) | [21:464](https://www.figma.com/design/kbUnfwTCHtQKpBwD9XGo5c/About-Looply?node-id=21-464) | outputs/brand-pages-20261117/demo/Looply_Sustainability.html |

本次实际读取六个画板的结构、可见文字与整页截图。用户链接的 21:559 是 Mobile 光伏正文，不是整个文件的页面范围。读取时间不能替代设计稿最后更新时间：工具未返回文件版本号或最后修改时间。

线上 Demo 通过网页读取工具打开失败，本轮可确认的 Demo 证据是上述本地源文件，不宣称已验证线上与本地一致。

补充来源：

- docs/product/looply-About-PRD-v0.3.md：2026-08-17 历史 About 需求，页面结构和部分承诺已与新设计不同，保留历史，不直接搬用。
- docs/product/looply-About与鉴定页改版-PRD-v0.1.md：2026-10-08 保障条款跳转专项；不是本次三页总 PRD。
- docs/product/looply-About与鉴定页-埋点开发清单-v1.0.md：2026-10-14，复用已有 About 正文点位的依据；新页面、新入口不自动视为已覆盖。
- docs/research/about-us/looply-About-Looply-竞品调研-v0.1.md：2026-08-05 历史调研，仅作背景，不反向覆盖本轮 Figma。
- outputs/brand-pages-20261117/HANDOFF-20261119.md：历史 Demo 交接，部分内容已被后续对话和设计替换。
- docs/reviews/品牌介绍页/evidence/figma-text-20261124.json：本次读取的 PC / Mobile 文案快照。

## 2. 差异与确认项

以下是 2026-11-24 首次读取时的差异快照。用户随后确认：文案统一由用户在 Figma 维护，PRD 不逐条列文案；不再逐项要求批准文案纠错。门店按 Figma 各 3 张，首图采用指示条＋每 4 秒自动轮播＋点击切换。尚未改动 Figma、Demo 或线上页面。

| 编号 | 对照结果 | 影响 | 建议处理 | 状态 |
|---|---|---|---|---|
| D01 | PC 和 Mobile 的 SBTi 卡片正文写 LEED；LEED 卡片正文写 SBTi。PC 节点 4:1437 / 4:1459，Mobile 21:547 / 21:531 | 两张证据卡的标题、说明和链接不匹配 | 交换回对应正文，沿用此前确认的缩短文案 | 已收口：文案以用户维护的 Figma 为准 |
| D02 | Mobile Sustainability 首屏 21:521 仍是旧版 craftsmanship / beauty / significance；PC 4:1420 和 Demo 已是精简文案 | 同页跨端内容不同 | 两端统一 PC 新版 | 已收口：文案以用户维护的 Figma 为准 |
| D03 | Our Group PC 三项能力是 Luxury authentication / Condition assessment / Resale valuation；Mobile 28:4409 起却复制 About 的鉴定／成色／实拍三项，并含 1.28 million | 集团能力介绍跨端含义不同 | Mobile 按 PC 三项集团能力统一 | 已收口：文案以用户维护的 Figma 为准 |
| D04 | About PC / Mobile 的鉴定正文仍含 1.28 million；Demo 只保留鉴定说明，不含该数字 | 新旧统计口径并存；不能与集团 10 million 混为同一指标 | About 沿用 Demo 鉴定正文，集团统计留在 Our Group | 已收口：文案以用户维护的 Figma 为准 |
| D05 | Figma 每个门店 3 张；Demo 每店 4 张且包含此前用户指定的顺序与扩图 | 图数、素材、顺序不同 | 按 Figma 3 张或保留 Demo 4 张，需选择 | 已确认：按 Figma 各 3 张 |
| D06 | About Figma 首图是 4 个指示条，左右箭头／计数／暂停为隐藏层；Demo 是箭头＋计数＋暂停、4 秒自动轮播。所核对节点无原型 reactions | 无法仅据静态稿确定自动播放与手动行为 | Figma 外观＋4 秒轮播＋点击指示条切换，或仅手动 | 已确认：Figma 指示条＋4 秒自动轮播＋点击切换 |
| D07 | Sustainability Demo 保留旧版认证、光伏与 COP 文案；Figma COP 文案已采用后续版本 | 将 Demo 文案抄进 PRD 会回退已确认内容 | 用 Figma 当前 COP 文案及此前确认的光伏口径；D01、D02 单独纠正 | 已收口：文案以用户维护的 Figma 为准 |
| D08 | About 上门服务：Figma 为 Serving many parts of Greater LA；Demo 为 Available across the Greater LA area | 服务覆盖口径不同 | 以 Figma 的限定范围为展示口径；服务页负责实际资格判断 | 按 UI 基线整理 |
| D09 | Mobile Figma 为返回按钮＋页名，没有画出公共 Footer / 底部导航；Demo 有电商公共导航与 Footer | 页面壳不同，不可从 Demo 直接照搬 | 展示按 Mobile Figma；返回动作可参考历史 About 规则，但仍需核对当前公共组件 | 待公共规则核对 |
| D10 | PC Figma 导航有 Watches / Watchs 重复，公共 Footer 有多个入口；Demo 部分 Footer 链接禁用、订阅只是演示提示 | 静态示意不能作为新增业务能力或可用链接证明 | 本次正文与公共导航分工；不把错字、演示订阅成功或禁用占位当需求 | 待公共组件引用核对 |

## 3. 无争议页面覆盖清单

| 页面 | 顺序 | 内容与操作 | 跨端结构 |
|---|---|---|---|
| About | 1 | 品牌介绍、4 张首图、60,000+ items、107,000+ sq. ft.、Our Story、Meet our Group | PC 首屏左右文字；Mobile 上下排列，两个指标并列 |
| About | 2 | What we believe、可持续发展入口 | 两端居中长文模块 |
| About | 3 | Two Ways Into Looply：买／卖两张卡、购物／卖货入口 | PC 并列；Mobile 买卡在前、卖卡在后 |
| About | 4 | How we work：鉴定、成色、实拍、鉴定页入口 | PC 文字与两图左右；Mobile 两图在文字项之前 |
| About | 5 | 上门、到店、邮寄三种卖家服务及统一服务入口 | PC 三列；Mobile 按同顺序纵向排列 |
| About | 6 | 洛杉矶办公区图片、联系入口、地址、预约入口 | PC 图文左右；Mobile 图片在前，联系和预约顺排 |
| Our Group | 1 | 集团关系、5.5M、Pre-owned luxury items sold、As of October 2026 | PC 文案与数字左右；Mobile 上下 |
| Our Group | 2 | 团队照片墙、经验与统计、能力三项、鉴定页入口 | 三项能力内容差异见 D03 |
| Our Group | 3 | 门店总介绍、60,000+、上海／北京图库、名称、位置、面积和说明 | PC 两店并列；Mobile 上海后北京 |
| Our Group | 4 | Sustainability 图文、可持续发展页入口 | PC 图文左右；Mobile 标题正文、图片、链接 |
| Our Group | 5 | About／Authentication 两张导流卡 | PC 并列；Mobile 上下 |
| Sustainability | 1 | 品牌循环主张与楼梯背景图 | PC 文字叠图；Mobile 图片与文字分区 |
| Sustainability | 2 | SBTi、CDP、LEED 三张证据卡及材料入口 | PC 三列；Mobile 按同顺序纵排 |
| Sustainability | 3 | 青岛办公楼光伏图、2025 年 527.7 metric tons、994,540 kWh 用电说明 | PC 图文左右；Mobile 上图下文 |
| Sustainability | 4 | COP28／29／30／31，按 2023→2026；只有 COP28 有报道链接 | PC 2×2；Mobile 逐条纵排 |
| Sustainability | 5 | Keep good pieces in use、购物／卖货 CTA | PC 两按钮并列；Mobile 两按钮纵排 |

## 4. 正文链接核对

此表是本地 Demo 实际目标，不代表目标页面已验收，也不把 Demo 文件名当生产路由。

| 发生页／入口 | 实际目标 |
|---|---|
| About / Meet our Group | Our Group 页面 |
| About / Explore our approach to sustainability | Sustainability 页面 |
| About / Explore the collection | https://www.looply.com/en-US |
| About / How selling works；Explore seller services | https://www.looply.com/en-US/sell |
| About / Explore our authentication process | https://www.looply.com/en-US/authenticity |
| About / Contact us | https://www.looply.com/en-US/pages/contact |
| About / Book an appointment | https://www.looply.com/en-US/sell/request |
| Group / See how Looply authenticates；Our authentication process | https://www.looply.com/en-US/authenticity |
| Group / Explore the Group’s sustainability efforts | Sustainability 页面 |
| Group / About Looply | About 页面 |
| Sustainability / Check our targets on SBTi | https://sciencebasedtargets.org/target-dashboard |
| Sustainability / View 2023 score report | assets/sustainability/cdp-score-2023.png |
| Sustainability / View certificate | assets/sustainability/leed-gold.pdf |
| Sustainability / Read the press release | https://www.prnewswire.com/apac/news-releases/zhuanzhuan-makes-debut-at-cop28-the-first-chinese-secondhand-platform-on-the-global-stage-302015081.html |
| Sustainability / Shop pre-owned | https://www.looply.com/en-US/collections/new-arrivals |
| Sustainability / Sell to Looply | https://www.looply.com/en-US/sell |

## 5. 数据与边界

- 5.5M 为集团累计售出二手奢侈品，截至 October 2026；不改写为 Looply 自身成交量。
- 10 million 为团队累计检查／鉴定量；1.35 million 包含非真品或未达平台标准，不能全部解释为假货。
- About 的 60,000+ 与 Group 的 60,000+ 描述主体不同，按各自说明展示，不推导库存接口或自动更新机制。
- 107,000+ sq. ft. 是支撑美国业务的亚洲仓储面积；上海 ~65,000、北京 ~32,000 是门店面积。
- 光伏 994,540 kWh 的口径是建筑使用屋顶系统所发电量；不能直接改成系统总发电量。527.7 metric tons 与 2025 年绑定。
- COP31 内容按用户提供报道和设计稿表述：分享质检、数字档案，以及就再利用判定和减排核算交流；不扩大为国际互认已经达成。
- 本次是内容页 PRD；鉴定页人物素材此前只讨论过建议，未收到更换确认，也没有本次鉴定页新稿，不能自动纳入改版需求。
- 英文稿完整，西语文案与新页面生产路由尚未从当前输入中取得；不能从历史英西语支持推断新增内容已翻译。

## 6. 文档与评审状态

准备沿用既有 About PRD 版本历史，形成覆盖三页的本轮工作稿，并独立维护修订记录。本 Checklist 记录输入冲突，不承担正式需求职责。

已读取 prd-writing、prd-review-simulation 及《Looply 开发交付文档 Review 标准》v0.1。用户确认后已创建 docs/product/looply-About-PRD-v1.0.md，覆盖三个品牌页，不复制英文正文。文案差异改为由用户维护 Figma；截图与文字快照只用于追溯，不是另一套文案基线。正式评审记录另存。

### 接入准备事项（不新增产品取舍）

- Figma 工具未返回版本号/更新时间；开发前需记录用户完成文案维护后的发布版本，当前读取快照不是最终文案冻结证明。
- 新页面生产路由由开发登记；PRD 以语义目标定义互跳。
- 三页字段级映射已写入《品牌介绍三页多语言资源映射 v1.0》；语种采用首页 v1.10 的英语／西语，缺译延续 About 英文兜底。资源注册、源文及译文接入仍需实施验证，不能宣称已接通。
- 新页面及入口的采集规则已补齐统一需求§8.7；技术接入、既有目标ID绑定及落库验证仍需实施。
- 当前为需求工作稿，不是上线或运行态验收结论。

### 2026-11-24 埋点补充

用户明确要求补全埋点。已在统一产品需求 v2.1 §8.7 写入三页访问、18 个正文链接、首图／图库主动切换及返回规则，PRD 仅引用唯一规则位置。原“新增埋点待补”状态由本条替代。实施阶段绑定预约、新品集合的既有目标页 ID 与素材 ID，尚未进行代码接入或落库验收。

### 2026-11-24 预评审修正回读

- R01至R05已完成本地文档修正，详见《预评审修正复检-20261124》。Footer当前工作版本为v0.4。
- 重新读取Figma六画板：SBTi／LEED正文、Mobile可持续发展首屏、Mobile Group三项能力均已修正；旧快照差异不再作为待修项。工具仍未提供文件版本号或更新时间，保留当前读取快照供追溯。
- About首屏旧购物／卖货按钮及箭头／计数控件位于隐藏父层，未作为额外可见入口统计。

### H5 Account Settings About列表（用户已确认）

- 用户确认单个About入口进入四项列表页，顺序与品牌Figma PC Footer一致：About Looply、Authenticity、Our Group、Sustainability。
- 已写入品牌PRD §2.3、§8，资源映射及统一采集§8.7；原Feed／Banner直达About Looply保留。
- 当前读取Looply 1.1（sAOLkw0gIl1bwQRYCDqKuW）个人中心页面552:1761，最新有日期分区为1109-列表左边icon去掉灰底；另外未标日期画板10889:8262中Account Settings末行10889:8472已为About。
- 列表画板10889:8476顶栏为About，但四行仍为Privacy Policy、Terms of Service、Shipping & Delivery、Returns & Refunds，需UI按用户本轮确认替换为品牌四项。布局沿用现有设置／列表样式；本次未修改Figma，未宣称新列表视觉验收通过。
- 文档中心Footer已有v0.8，仍不含品牌入口，不能用本地旧v0.4覆盖其多国家／文件配置变化。下次同步时将本轮品牌入口增量合入v0.8当前规则；本次只改本地品牌工作稿，未发布或覆盖其他模块文件。
