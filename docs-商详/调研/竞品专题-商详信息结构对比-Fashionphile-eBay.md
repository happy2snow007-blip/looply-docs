# 竞品专题 · 商详页信息结构对比（looply vs Fashionphile vs eBay）

> 生成日期：2026-08-10
> 数据来源：用户提供的三端截图（looply test 环境移动端 / Fashionphile APP / eBay APP）+ 本地 `商详/PRD/looply-商详页-PRD-v1.8.md` 交叉核对
> 对比范围：仅截图可见区域（Condition / Description / Shipping & Returns / 底部 CTA），未覆盖 Gallery、价格区、推荐区
> 用途：与 UI 设计师沟通

---

## 零、先说结论

**这一屏看着乱，绝大部分不是 UI 设计的问题。**

把截图逐条对回 PRD v1.8 之后，可见的 11 个问题里：

| 归属 | 条数 | 该找谁 |
|---|---|---|
| A 测试环境脏数据 | 3 | 无（换真实商品即消失） |
| B CMS 模板没配内容 | 2 | 运营 / 产品自己 |
| C 实现没按 PRD 落 | 3 | 开发 |
| **D 真·设计问题** | **2** | **UI 设计师** |
| E PRD 自身规范缺口 | 1 | 产品（我） |

**拿整屏去找 UI 设计师是找错人。** 真正该跟设计师谈的只有 D 类的 2 条 + E 类衍生的 1 条版式问题。

---

## 一、逐条核对（截图 → PRD）

### A 类 · 测试环境脏数据（不用管）

| # | 现象 | 判定依据 |
|---|---|---|
| A1 | Condition 值是 `NWT`，但进度条 5 段是 Like New / Excellent / Very Good / Good / Fair，**NWT 不在其中** | PRD L700-706 成色枚举固定五级，无 NWT。这是测试数据写了枚举外的值 |
| A2 | 成色描述整行是 `Condition: test` | 明显占位数据 |
| A3 | 属性表出现 `CR: 128GB` / `SIM: Nano-SIM`（3C 属性） | PRD L657 明确支持 Electronics PDP 等多模板，**不能断言是品类串味**，更可能是拿电子类测试商品套了当前模板。**需确认** |

### B 类 · CMS 模板没配内容（找运营/产品）

| # | 现象 | 判定依据 |
|---|---|---|
| B1 | 整页**没有任何信任模块**（无 Certified Authentic 卡片、Condition 区无绿盾徽章、Sticky 栏无 ✓ Verified） | PRD §2.9 定义了 Certified Authentic 卡片（L663：位于 CTA 下方、Condition 上方）；L688 定义 Condition 区绿盾徽章；L595 定义 Sticky 栏 ✓ Verified。**三处同时缺失，指向同一个原因：当前模板的 Certified Authentic 模块没配内容或开关关着**（L667-669 规定未配置即整体隐藏）。机制是有的，内容是空的 |
| B2 | 属性名是 `TR` / `CR` / `SIM` 这种内部缩写，C 端用户读不懂 | PRD L788：属性名取 **CMS 里运营定义的前台展示名 `display_name`**。所以 TR/CR/SIM 是运营填进去的，前端只是照显。**不是设计问题也不是 bug，是配置内容质量问题**（见 E1） |

### C 类 · 实现没按 PRD 落（找开发）

先确认端形态：截图底部是「收藏 \| Add to Bag \| Buy Now」三栏 Sticky 栏（PRD L600 原文），Header 有分享图标（PRD L419 APP 端独有）→ **这是 APP 端布局**，按 APP 端规则判。

| # | 现象 | PRD 怎么规定的 |
|---|---|---|
| C1 | 进度条 5 段**全是同一个浅粉色，看不出当前商品在哪一档**，5 个标签也全是灰的 | L714-715：当前等级段高亮**品牌色**，标签也用品牌色，其余灰色。L708 进一步规定：grade 匹配不上模板等级集合时，**进度条和等级名称应静默隐藏**。现在既没高亮、也没隐藏，而是渲染出一条"全灰无指示"的条 —— **两条兜底规则都没落**。这也是整屏最刺眼的一处：一个信息量为零的组件占了最显眼的位置 |
| C2 | Description 区**没有 item #**（Listing 编号），也**没有商品描述文案** | L775 规定 Description 区含 `item #`（listing_id）；L778/L812 规定 `listing_description` 展示在属性表下方。item # 缺失是实现漏了；描述文案缺失可能是该测试商品 `listing_description` 为空（L821 规定为空则隐藏）→ **item # 要开发查，描述文案需确认数据** |
| C3 | Shipping & Returns **默认展开**，两大段政策文案铺满屏幕 | L850 + 附录 5.2 差异表：**APP 端默认折叠**（原因写的就是"减少首屏滚动深度"）。实现按 PC 端规则渲染了。**这是"乱"的最大单一贡献者** —— 它把两段与本商品无关的通用文案顶到了首屏 |

### D 类 · 真·设计问题（找 UI 设计师）★

| # | 问题 | 说明 |
|---|---|---|
| **D1** | **Size Guide 被塞进了键值行模板，左边写 "Size Guide:"、右边写 "Size Guide"，同一个词出现两遍** | PRD L811 规定属性区统一格式为 `Label: Value`；L805 规定 Size Guide 是固定模块、默认展示名就叫 "Size Guide"。两条规则一撞，就渲染成了现在这样。**根子是：Size Guide 是一个"动作入口"，不是一条"属性值"，不该套 Label: Value 版式。** 需要设计师给一个独立的行样式（整行可点 / 右侧箭头 / 或移出属性表单独成行） |
| **D2** | **同一屏出现两个视觉完全相同的心形图标**（Header 右上 + Sticky 栏左侧） | 按 PRD 这是两个不同功能：Header 的心形是 **Wishlist 入口**（L399 + L425，点了跳收藏夹页），Sticky 栏的心形是 **收藏本商品**（L600）。功能不同、图标相同、同屏出现 → 用户无法预期点哪个会发生什么。**需要设计师做视觉区分**（实心/描边、加计数、或 Header 换成别的入口形态） |

补充一条同类的：Condition 区标题行是 `Condition: NWT`，下面成色描述行又是 `Condition: test` —— **同屏两个 "Condition:" 标签**。值本身是脏数据（A1/A2），但"标题和明细行会撞同一个词"是版式层面可预见的，也值得跟设计师提一句区分手段。

### E 类 · PRD 自身缺口（我要补）

| # | 问题 |
|---|---|
| **E1** | PRD §2.11 / §2.3 对 CMS「前台展示名」**只规定了走翻译、留空则不显示 Label，没有任何质量约束** —— 没说不能填内部缩写、没有字符长度/可读性校验、后台没有预览。结果就是运营填 `TR`/`CR`，前台原样输出给美国消费者。这不是这一次的偶发，是**护栏缺失**，同样的坑会在每个新类目重现 |

---

## 二、竞品做对了什么

### Fashionphile

| 做法 | 对 looply 的意义 |
|---|---|
| Description 是**散文式描述**，第一句就确权确真：「This is the authentic LOUIS VUITTON Monogram Palm Springs Backpack Mini」，然后讲材质、五金、内衬 | looply 机制上有 `listing_description`（PRD L778），只是这次没数据。**差距在内容供给，不在结构** |
| **Size 独立成块给绝对数值**（Base length 6 in / Height 8.5 in / Width 3.5 in / Drop 1.25 in / Drop 19.5 in） | looply 把尺寸全部收在 Size Guide 弹窗里（PRD L795-796），页面上**一个尺寸数字都看不到**。二手箱包用户"合不合适"是核心决策点，藏一层是真实结构差异 → **值得讨论** |
| Shipping 说清了「免什么、什么另收费、怎么查价」，并单列 **Shipping includes: Insurance, signature confirmation…** | 把服务包含项列出来是价值感，不只是免责。looply 本期是写死文案（PRD L844），可作为文案改版参考 |
| 顶部常驻 **Affirm 分期 banner** | 支付能力前置。looply 目前无此位 |
| **单一主 CTA「Add to Bag」**，不做双按钮 | looply 是 Add to Bag + Buy Now 双按钮（PRD L600），已有专题《竞品专题-移动端商详CTA设计》，此处不展开 |

### eBay

| 做法 | 对 looply 的意义 |
|---|---|
| **「About this item」字段名全是人话**：Condition / Quantity / Item number / Bag Width | 直接对照 looply 的 TR/CR/SIM。**这就是 E1 缺的那条护栏的样子** |
| **单位双制**：`15.354 inch(approx) / 39 cm(approx)` | looply PRD L798 明确本期不做单位换算、按录入值原样展示。**已知敞口，PRD 已记**，多国销售铺开时必然要回来处理 |
| **Condition 拆两层**：标准枚举（Pre-owned - Fair）+ 卖家原文（"Condition Rank : B \<Outside\>AB ( GOOD…"），原文**截断 + `>` 进二级页** | 枚举保证可筛选可比价，原文保证不失真。looply 机制其实一样（枚举 grade + 4 个文本字段，PRD L692），**差距在渲染，不在设计思路** |
| 长描述不占主页面：**「See full description ›」** | looply APP 端是 2 行截断 + Read more（PRD L815），思路一致 |
| **Quantity: 1 available** | 二手是单件库存，"仅此一件"是天然稀缺信号。looply 页面上没有任何数量/稀缺表达 → **值得讨论** |
| **「Shop with confidence」三条信任项**（Authenticity Guarantee / Top Rated Plus / Money Back Guarantee），每条 = 图标 + 标题 + 一句人话 + 可点进详情 | looply 的 §2.9 Certified Authentic 是**一张卡**，eBay 是**三条并列**。信息量和可信度不是一个量级 → 见 B1，先把内容配上再谈要不要拆条 |
| 顶部**四步认证流程图**（Make a purchase → Seller ships to eBay → Experts authenticate → eBay ships to you） | 把平台服务链路可视化。二手最大转化阻力是"是不是真的、出问题谁管"，这是最直接的回答 → **looply 无对应设计** |

---

## 三、looply 建议

### 值得借鉴

1. **属性展示名的可读性护栏**（对标 eBay）—— 补进 PRD §2.3，CMS 后台加校验 + 前台预览。这是 E1 的解法
2. **页面上给出关键尺寸数值**（对标 Fashionphile）—— 不必全量，把最影响决策的 2-3 个尺寸提到属性表里，Size Guide 保留作为"怎么量的"说明
3. **信任模块从"一张卡"扩到"三条"**（对标 eBay）—— 但**前提是先把 §2.9 的内容配上**，现在是零

### 要避开的

1. **不要把整屏问题打包丢给 UI 设计师**。这次 11 条里只有 2 条是设计问题，其余是数据/配置/实现。混着提会让设计师改一版还是这个样子
2. **不要在 test 环境脏数据上做设计判断**。NWT / test / 128GB 这些会误导对信息架构的判断，建议先要一个真实商品的链接再做正式评审

### 差异化机会

- looply 的 **CMS 模板 + 类目级属性配置**（PRD §2.3）比 eBay 的固定字段表灵活得多，理论上能做到"箱包看尺寸、腕表看机芯、首饰看材质"。**但灵活性没有护栏就变成 TR/CR/SIM。** 把 E1 补上，这个机制才是优势而不是风险

---

## 四、需要确认的事项

| # | 问题 | 为什么要先确认 |
|---|---|---|
| Q1 | 截图这个商品是电子类测试数据，还是当前 PDP 模板真的把 3C 属性配进了时尚类目？ | 决定 A3 是"不用管"还是"配置错了" |
| Q2 | 当前模板的 Certified Authentic 模块是没配内容，还是开关关着？ | 决定 B1 是内容缺失还是被人关掉了 |
| Q3 | 是否要把关键尺寸提到页面上（对标 Fashionphile）？ | 属于加功能，**需产品先拍板业务策略，再谈改不改设计稿** |
| Q4 | 是否要做"仅此一件"稀缺表达（对标 eBay Quantity）？ | 同上 |
| Q5 | 信任模块要不要从一张卡扩成三条？要不要做认证流程图？ | 同上 |

> Q3-Q5 是加功能，按流程需先确认业务策略，本文档不下结论。
> A/B/C 类共 8 条属于"实现与既有 PRD 不符或数据未就绪"，不涉及新决策，可直接推。

---

## 五、给 UI 设计师的沟通清单（可直接发）

> 只有这三条需要动设计稿：

1. **Size Guide 行需要独立样式** —— 它是入口不是属性值，现在套了 `Label: Value` 版式导致 "Size Guide:" 和 "Size Guide" 重复出现。请给一个整行可点 + 右侧箭头的行样式，或把它移出属性表单独成行
2. **两个心形图标要做视觉区分** —— Header 右上是"去收藏夹"，底部栏是"收藏这件商品"，功能不同但图标完全一样。请区分（实心/描边、或 Header 换入口形态）
3. **Condition 区标题与明细行的标签需要区分手段** —— 现在会出现标题 "Condition: XX" 和明细行 "Condition: XX" 同屏，请在字号/字重/间距上拉开层级，避免读起来像重复了一遍

> 其余问题（进度条不高亮、Shipping 没折叠、属性名是缩写、缺信任模块）**不是设计稿的问题**，分别走开发 / 运营配置 / 数据，已在上文分类。

---

## 附：核对留痕

| 截图观察 | 对应 PRD 位置 |
|---|---|
| 成色五级枚举 | `PRD/looply-商详页-PRD-v1.8.md` L700-706 |
| 进度条高亮规则 | L714-715 |
| grade 匹配不上应静默隐藏 | L708 |
| Certified Authentic 卡片位置 | L663 |
| Condition 区绿盾徽章 | L688 |
| Sticky 栏 ✓ Verified | L595 |
| Description 应含 item # | L775 |
| Description 应含商品描述文案 | L778 / L812 |
| 属性名取 CMS display_name | L788 |
| Size Guide 展示名默认值 | L805 |
| 属性区 Label: Value 格式 | L811 |
| Shipping & Returns APP 端默认折叠 | L850 + 附录 5.2 |
| APP Sticky 三栏布局 | L600 |
| APP 端独有分享按钮 | L419 |
| Header 心形 = Wishlist 入口 | L399 / L425 |
| 本期不做单位换算 | L798 |
