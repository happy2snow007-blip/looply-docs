# Landing v0.3 预评审修复复检

> 日期：2026-10-16  
> 实际复检模型：`gpt-6-astra / high`  
> 标准：《Looply 开发交付文档 Review 标准》v0.1（2026-08-13），`prd-writing`、`prd-review-simulation`  
> 范围：本次六项问题确认修改后的受影响完整章节与引用回读；不是重新扩展范围的全量模拟评审。R1/R2仍存在真实证据缺口，不能宣称正式Review全部通过。

## 1. 输入与覆盖

已回读当前PRD全文，重点逐句复检§1.5、§2.1–2.4、§2.6–2.8、依赖、验收和索引，以及Checklist、修订记录。引用章节回读：首页PRD v1.10 §2.1；Collection PRD v1.6 §2.5、§3.4、§4.4。源Demo回读最终Slogan样式、预览、图片读取／更换、保存校验及对应表单。

- [预评审原报告](https://happy2snow007-blip.github.io/looply-docs/docs-Landing%E9%A1%B5%E9%85%8D%E7%BD%AE/%E8%AF%84%E5%AE%A1%E8%AE%B0%E5%BD%95/looply-marketing-landing-PRD-v0.3-%E9%A2%84%E8%AF%84%E5%AE%A1-2026-10-16.md)
- [R1/R2证据补充](https://happy2snow007-blip.github.io/looply-docs/docs-Landing%E9%A1%B5%E9%85%8D%E7%BD%AE/%E8%AF%84%E5%AE%A1%E8%AE%B0%E5%BD%95/looply-marketing-landing-v0.3-R1-R2%E4%BE%9D%E8%B5%96%E8%AF%81%E6%8D%AE%E8%A1%A5%E5%85%85-2026-10-16.md)
- [当前PRD](https://happy2snow007-blip.github.io/looply-docs/docs-Landing%E9%A1%B5%E9%85%8D%E7%BD%AE/PRD/looply-marketing-landing-PRD-v0.3.md)
- [源Demo](https://happy2snow007-blip.github.io/looply-docs/docs-Landing%E9%A1%B5%E9%85%8D%E7%BD%AE/%E5%8E%9F%E5%9E%8B/looply-%E7%A4%BE%E5%AA%92%E5%88%86%E4%BA%AB-Landing%E9%A1%B5%E9%85%8D%E7%BD%AE-antd-%E5%8E%9F%E5%9E%8B-v6-standalone.html)
- [单文件Demo](https://happy2snow007-blip.github.io/looply-docs/docs-Landing%E9%A1%B5%E9%85%8D%E7%BD%AE/%E5%8E%9F%E5%9E%8B/looply-%E7%A4%BE%E5%AA%92%E5%88%86%E4%BA%AB-Landing%E9%A1%B5%E9%85%8D%E7%BD%AE-antd-%E5%8E%9F%E5%9E%8B-v6-standalone.html)

本复检任务只写本报告，没有修改正式需求、Demo或发布文件。浏览器与Node测试由主任务执行，下面明确区分其测试结果与本任务源码／文档回读。

## 2. 逐项状态

| 编号 | 原等级 | 状态 | 复检依据及剩余边界 |
|---|---|---|---|
| R1 动态文案资源映射 | P1 | **部分补齐，证据待核** | PRD§1.5现有三字段业务归属表，明确Landing页面／图片对象和PC/H5、语言维护范围，未伪造resourceType或fieldName；Checklist逐项跟踪准确卡片、路径、语种及缺译规范。已确认的复用决定不变，准确资源映射仍未取得，不能关闭。 |
| R2 现行复用基线 | P1 | **语言引用已补，其他证据待核** | 首页v1.10 §2.1确实定义英语/西语、当前locale、游客浏览器保存／登录账号保存及统一message package；PRD引用真实存在且内容相符。该章未定义统一缺译兜底；客服组件、支持编辑的现行短链规范仍未取得。Checklist明确旧v1.1不可代替现行实现，不能整体关闭。 |
| D1 Slogan长文案 | P1 | **修复，定向实测通过，关闭** | 源Demo210–214行在最终作用域允许flex换行，入口flex收缩、max-width:100%、white-space:normal及overflow-wrap:anywhere，H5特定选择器覆盖旧nowrap；预览仍只把入口包在a中。PRD§2.3长文案行为及UI责任边界保留。主任务提供本轮PC/H5连续60个W不溢出的运行证据，见第5节。 |
| D2 更换图片失败保原图 | P1 | **修复，定向实测通过，关闭** | 源399行readImage在类型／大小合法、FileReader成功且Image解码成功后才更新图片；失败分支只提示、不写图片；408行已有图状态新增“更换图片”，无图上传共用读取路径，不修改入口配置。主任务Node及浏览器分别覆盖读／解码失败、超限和正常替换，原图与入口保留结果符合PRD，见第5节。 |
| R3 隐藏入口免校验 | P2 | **修复并回读通过** | PRD§6“入口校验”明确有图／Slogan非空时校验，隐藏入口免校验；回读§2.2无图保留入口及§2.3空Slogan保留跳转，与源码save的跳过条件一致。未改变原已确认行为。 |
| R4 重复／冗余 | P2 | **修复并回读通过，关闭** | 旧优惠依赖已删除；Slogan整条点击区重复已去除；地址章节改为引用Collection更新规则；历史快照只读重复已删。复检提出的两处同段重复也已由主任务最小合并，本任务再次完整回读§2.2与§2.8，见下节。必要Scope、迁移及历史非冻结边界保留。 |

## 3. R4最后两处合并与回读

1. PRD§2.2第60行已将成功替换与失败保留分开表达，失败仅保留一处“上传失败保留原图和入口配置并反馈失败”。再次阅读整节，上传／更换／删除各自结果及入口配置保留规则完整，没有因去重遗漏异常反馈。
2. PRD§2.8第161行已删除“商品模块记录Collection引用”重复分句，保留“商品模块仅记录关联Collection标识”及不冻结Collection、商品结果／价格／库存的边界；保障改为“展示、跳转状态”，与三态的业务含义一致。再次阅读整节及§2.4引用，无新增冲突。

两处均在已授权范围内完成，不涉及新产品选择。本轮R4不再有待修改项，不继续删除必要范围、迁移或异常说明。

## 4. 四项专项结果

| 专项 | 当前复检结论 | 说明 |
|---|---|---|
| 准确性 | **本次文案修正通过；整体仍受R1/R2证据缺口限制** | R3条件、业务对象和语言引用准确；不把未取得的资源／组件标成已核实。 |
| 冲突 | **本轮受影响正文与D1/D2定向验证通过** | 无图／空Slogan例外已统一，D1/D2取得运行证据；无All等Landing布局例外不被Collection旧稿覆盖。外部现行基线未取得部分仍按R2保留，不能宣称所有跨制品已对齐。 |
| 重复 | **本轮修复范围通过** | 第3节两处最小合并已完成并回读，原R4问题关闭。 |
| 冗余 | **本轮修复范围通过** | 优惠依赖及两处无增量同义句已清理；UI尺寸职责、迁移及历史非冻结规则保留有独立验收意义。 |

## 5. 测试证据边界

主任务报告两版编译与14项静态检查通过。随后完成[本轮线上单文件页](https://happy2snow007-blip.github.io/looply-docs/docs-Landing页配置/原型/looply-社媒分享-Landing页配置-antd-原型-v6-standalone.html?v=f595247)的定向实测；本任务收到测试结果后与实际源码逐项核对，未冒称自行执行浏览器操作。

| 验证 | 主任务实际结果 | 本轮判断 |
|---|---|---|
| D1·H5连续60个W | 入口宽323.77px／预览375px，右侧越界量-22.23px；Slogan容器scrollWidth/clientWidth均373，white-space为normal | 原反例已修复，完整折行且无水平溢出 |
| D1·PC连续60个W | 容器scrollWidth/clientWidth均455，右侧越界量-21px | 定向长字符不溢出通过 |
| D2·损坏png替换 | 初传product0，随后用损坏png替换，解码失败后原图src不变、入口“Keep CTA”保留 | 失败保原图和入口通过 |
| D2·大于3MiB替换 | 替换被拒，原图src仍不变 | 大小拒绝替换通过 |
| D2·正常替换 | product1替换后src改变，入口“Keep CTA”保留 | 成功替换且保留入口通过 |
| D2·Node异常链路 | FileReader失败、Image解码失败、超限均保OLD；成功才更新NEW | 与源码仅成功后写图片的结构对应 |
| 浏览器错误日志 | error日志为空 | 本轮路径未观察到浏览器错误 |

运行截图：[长文案修复结果](https://happy2snow007-blip.github.io/looply-docs/docs-Landing%E9%A1%B5%E9%85%8D%E7%BD%AE/UI/v03-review-long-label-fixed.jpg)。主任务已退出测试表单返回列表，未保存测试记录。

负的右侧越界量表示入口右边界仍在预览以内。本轮关闭的是已提出的长字符溢出和替换失败丢原图问题，不等同全部字号、触控尺寸、所有设备或生产媒体接口均已验收。

最新独立UI、生产翻译、客服及短链接入仍未验收。本次不要求产品新增像素规格；也不因为尚未生产联调就把已有完整业务规则重列为PRD缺规则。

## 6. 快照

| 制品 | 最终回读SHA-256 |
|---|---|
| PRD v0.3 | `ca19b3771e385410feeeed292a27146186b9c0d734ffb5ba4df70015a71f9d7e` |
| V6源Demo | `aa88d768373c6d8c127a8dac7df38853cee02867b0c9a2ea8d59a8fd14e7a353` |
| V6单文件Demo | `bd4e2666c0d18b5780d12fbff9f09173ff8888d179641905f2b834990d07b6ff` |

最终结论：**D1、D2、R3、R4已修复并关闭；R1、R2部分补齐，准确标识和现行实现证据仍待对应开发核实。原六项中剩余P1 2项，P0 0项、P2 0项。** 本次定向修复与复检完成，但正式模拟评审和完整开发交付基线仍不能标记全部通过；不得将明确列出的依赖缺口隐藏为“全部已完成”。
