> 生成日期：2026-05-19
> 数据来源：WebSearch
> 建议刷新：3 个月后或业务重大变化时

# 移动端商详页 CTA 设计竞品对比

## 核心问题

商详页底部购买区的展示策略：**页内固定** vs **Sticky 底栏** vs **两者并存（智能显隐）**

---

## 功能对比表

| 维度 | Amazon | eBay | Temu | Shein |
|------|--------|------|------|-------|
| CTA 展示位置 | 页内 + App 底部固定栏 | 页内（页面顶部区域） | 页内（多按钮区） | Sticky 底栏（始终可见） |
| 主 CTA 按钮 | "Add to Cart"（黄色）+ "Buy Now"（橙色） | "Buy It Now"（蓝色）+ "Add to Cart" | "加入购物车" + "立即结账" | "加入购物车"（单 CTA） |
| 次 CTA | "Add to today's delivery"（2025 新增，Prime 专属） | "Add to Watch List"（收藏） | 无明确次 CTA | 收藏心形图标（图标形式） |
| Sticky 底栏 | App 端有，Web 端无 | 无 | 无 | 有，始终吸底显示 |
| 按钮颜色 | 黄（加车）+ 橙（立购）— 高饱和度色 | 蓝色系 | 橙红色系 | 黑色（加车）|
| 购买栏信息密度 | 价格 + 配送预估 + 主次 CTA | 价格 + 主次 CTA + 数量选择 | 价格 + 多 CTA | 价格 + 单 CTA（极简） |
| 规格选择时机 | 点击 CTA 后弹出规格抽屉 | 页内直接选 | 页内直接选 | 点击 CTA 后弹出规格抽屉 |

---

## 各家亮点

### Amazon
- **双按钮颜色差异化**：黄色（加车）和橙色（立购）颜色不同，功能一目了然，不需要靠大小或位置传达优先级
- **2025 新增**："Add to today's delivery"（今日达专属按钮），将配送时效直接嵌入 CTA，减少用户跳转查询
- **规格延迟选择**：点击 CTA 后弹出规格抽屉，降低页面视觉复杂度
- **App 底栏**：App 端进入商详时底部有固定购买栏，Web 端以页内为主

### eBay
- **2024 年简化改版**：将 PC 和 App 端体验统一，精简信息层级
- **Search 页快速购买**：搜索结果页直接添加"Add to Cart"按钮，可跳过商详页，适合二手标品场景
- **三按钮结构**：Buy It Now + Add to Cart + Add to Watch List，适配拍卖/固定价混合场景
- **无 Sticky 栏**：页内 CTA 在屏幕顶部区域，依赖用户主动滑回，有流失风险

### Temu
- **问题设计被广泛批评**："Go to Cart" 和 "Checkout" 两个按钮功能相近，造成用户认知混乱
- **信息噪音淹没 CTA**：折扣标签、倒计时、社会证明堆叠，购买区域视觉权重被稀释
- **无清晰 Sticky 策略**：依赖页内按钮，但信息密度高导致 CTA 不突出
- **教训**：多按钮不等于高转化，功能相近的按钮反而降低决策效率

### Shein
- **Sticky 底栏策略最彻底**：购买栏始终可见，用户在任何滚动位置都能直接购买
- **CTA 区域极简**：底栏仅"加入购物车"一个主操作，收藏用图标，不占文字按钮空间
- **规格延迟选择**：点击加购后弹出尺码/颜色选择抽屉，页面内不展示规格组件
- **大量社会证明**：数百条评论 + 真实买家图，弥补无法试穿的信任缺口——这是 Shein 的特殊解法，源于其信任基础薄弱

---

## 行业数据

- 移动端 Sticky 加购按钮可带来 **8-15% 转化率提升**（Shopify 生态多个 A/B 测试）
- 抽屉式规格选择（点击 CTA 后弹出）可带来约 **5.2% 订单量提升**（98% 统计显著性）
- 2025 年约 **75% 移动端电商站点**已采用 Sticky 加购按钮

---

## looply 建议

### 值得借鉴

1. **Shein 的 Sticky 底栏策略**：始终吸底，消除"找不到加购按钮"的摩擦，行业最佳实践
2. **Amazon/Shein 的规格抽屉**：点击 CTA 后才弹出规格，保持购买区简洁，商品信息页面流更连贯
3. **Amazon 的双按钮颜色差异化**：主次 CTA 用不同颜色区分（不用依赖大小/位置），对 looply 来说可用"描边按钮 + 紫色实心"对应
4. **Shein 的收藏图标化**：收藏用图标，不和购买按钮竞争视觉权重

### 要避开的

1. **Temu 的多按钮歧义**：功能相近的按钮（"加入购物车" vs "去结账"）不要放同一层级、同一视觉权重
2. **eBay 的无 Sticky 策略**：页内 CTA 滚出视口后无兜底，用户需要滑回，增加流失风险
3. **Shein 的整体信息密度模式**：靠信息量堆叠解决信任问题是 Shein 的特殊路径；looply 有质检背书，应以"精准信任"替代"量大取胜"

### 差异化机会

1. **质检标签内嵌 Sticky 底栏**：在底栏价格旁显示"质检：优品"，把信任信号和购买动作放在同一视觉区域——这是四家竞品都没有做的
2. **双 CTA 语义清晰化**："加入购物车"（白底描边）+ "立即结账"（紫色实心），参考 Amazon 双按钮逻辑但用 looply 品牌色系
3. **Sticky 底栏轻量化**：不堆叠信息，只放价格 + 质检标签 + 双按钮，比 Temu 更克制，比 Amazon 更精简

---

## CTA 策略决策：推荐方案

基于竞品分析，**推荐 looply 商详页采用纯 Sticky 底栏策略**，移除页内双按钮：

**底栏结构**：
```
[质检图标 + 等级文字] [价格]   [加入购物车（描边）] [立即结账（紫色实心）]
```

**理由**：
- 页内已有商品图、描述、规格展示，CTA 不需要在页内重复占位
- Sticky 底栏视觉权重集中，不被页面内容稀释
- 与 Shein（Sticky）和 Amazon App（底栏）的主流策略一致
- 页内取消双按钮后，商品信息流更连贯，评论/推荐区可上移

**当前 Pencil 设计稿现状**：
- `Sii04`（商详主页面）：页内有 CTAGroup（QcZzC）需删除
- `PwUiB`（说明帧）：Sticky 底栏设计需完善（加入质检标签 + 双按钮规范）

---

*数据来源：[Design Critique: Temu](https://ixd.prattsi.org/2025/02/design-critique-temu/) · [Decluttering Shein](https://medium.com/@isirostion/decluttering-shein-a-heuristic-redesign-2508f4445a84) · [Sticky Add to Cart Best Practices](https://easyappsecom.com/guides/sticky-add-to-cart-best-practices) · [eBay Quick Add to Cart](https://www.valueaddedresource.net/ebay-add-to-cart-button-search/) · [Sticky ATC Conversion Data](https://growthrock.co/sticky-add-to-cart-button-example/)*
