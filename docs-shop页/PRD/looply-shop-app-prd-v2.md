# Looply Shop 页导航 PRD v2

**版本**：v2.0  
**更新日期**：2026-06  
**范围**：App 端 Shop 页——顶导 Tab、左侧一级导航、二级/三级圆形卡片的展示与跳转逻辑  
**相关文件**：`looply-shop-app-v0.2.html`（前端原型）、`looply-shop导航-后台原型-v0.4-antd.html`（后台配置原型）

---

## 1. 核心设计原则

Shop 页导航**只做路由，不挂商品**。所有导航项、圆形卡片的唯一目的是引导用户进入某个 Collection 的商品列表页。

Collection 是独立的商品集合实体，由商品后台维护。导航后台只负责配置"哪些 Collection 出现在哪里、叫什么名字、用什么图"。

---

## 2. 页面整体结构

```
┌─────────────────────────────────────┐
│  TopBar：Logo + 搜索框 + 收藏 + 购物袋  │
├─────────────────────────────────────┤
│  顶导 Tab（横向可滚动）                │
│  New Arrivals · Brands · Bags · …   │
├──────────┬──────────────────────────┤
│          │                          │
│  一级导航  │   右侧内容区               │
│  （左侧）  │                          │
│          │                          │
├──────────┴──────────────────────────┤
│  底部 TabBar：Home · Shop · Fav · Me │
└─────────────────────────────────────┘
```

### 2.1 TopBar
- Logo「Looply」紫色 #7C3AED，字重 800
- 搜索框：占剩余宽度，圆角胶囊，placeholder「Search bags, brands, jewelry…」
- 右侧图标：收藏心形、购物袋

### 2.2 顶导 Tab
- 横向排列，内容超出时可横滑，隐藏滚动条
- 激活态：紫色文字 + 底部紫色 2px 下划线
- 切换 Tab 时：左侧导航重置到该 Tab 第一项

### 2.3 一级导航（左侧）
- 宽度 108px，灰底 #FAFAFA，右侧 1px 分隔线
- 激活态：白底 + 左侧 3px 紫色竖线 + 紫色文字加粗
- 可独立滚动

### 2.4 右侧内容区
- 根据当前一级导航项的配置渲染，详见第 4 节

### 2.5 底部 TabBar
- 4 项：Home / Shop（激活）/ Favourites / Account
- SVG 图标，激活态紫色

---

## 3. 数据模型

### 3.1 Tab（顶导）
```
Tab {
  id        string   // 唯一标识
  name      string   // 显示名称，如 "Bags"
  image     string   // 图标/缩略图 URL（可选）
  enabled   boolean  // 是否在前台展示
  order     number   // 排序
  navItems  NavItem[] // 该 Tab 下的一级导航项列表
}
```

### 3.2 NavItem（一级导航项）
```
NavItem {
  id           string       // 唯一标识
  name         string       // 显示名称，如 "Shoulder Bags"
  image        string       // 图片 URL
  enabled      boolean
  order        number
  collections  string[]     // 关联的 Collection ID 列表（必须 ≥1 个）
  circles      CircleL2[]   // 二级圆形列表（数量 = collections.length）
}
```

**关键规则**：`circles` 的数量与 `collections` 一一对应。每个 CircleL2 对应 `collections[i]`。

### 3.3 CircleL2（二级圆形）
```
CircleL2 {
  id           string      // 唯一标识
  name         string      // 显示名称
  image        string      // 圆形内图片 URL
  enabled      boolean
  order        number
  collections  string[]    // 关联的 Collection ID 列表
                           // 数量=1 → 点击直接跳 collection 页
                           // 数量>1 → 展开三级圆形
  circles      CircleL3[]  // 三级圆形（仅当 collections.length > 1 时有效）
}
```

### 3.4 CircleL3（三级圆形）
```
CircleL3 {
  id          string    // 唯一标识
  name        string    // 显示名称
  image       string    // 圆形内图片 URL
  enabled     boolean
  order       number
  // 无 collections 字段
  // 对应的 collection 由父级 CircleL2.collections[i] 决定
}
```

### 3.5 Collection（来自商品后台，只读引用）
```
Collection {
  id    string
  name  string
  slug  string   // URL 标识，如 "shoulder-bags"
}
```

---

## 4. 右侧内容区渲染规则

规则极简，只看**当前一级导航项关联了几个 collection**：

### 情况 A：NavItem.circles 为空 / collections 只有 1 个且无二级配置
> 直接展示该 collection 的商品（兜底，通常不应出现）

### 情况 B：NavItem 有多个二级圆形（常规情况）

右侧展示：
1. 标题（= NavItem.name）
2. 3列圆形卡片网格，每个圆形 = 一个 CircleL2
3. 分隔线
4.「You May Also Like」+ 推荐商品卡片（2列）

**圆形点击行为**：
- CircleL2.collections.length === 1 → 跳转该 collection 页
- CircleL2.collections.length > 1 → 右侧内容替换为三级圆形列表

### 情况 C：进入三级（CircleL2 展开后）

右侧展示：
1. 返回按钮（← 返回上级）
2. 标题（= CircleL2.name）
3. 3列圆形卡片网格，每个圆形 = 一个 CircleL3
4. 分隔线
5. 「You May Also Like」+ 推荐商品卡片

**圆形点击行为**：CircleL3 固定跳转对应 collection 页（由父级 CircleL2.collections[i] 决定）

---

## 5. 圆形卡片视觉规范

- 宽度：列宽 100%（3列网格，gap 8px）
- 高宽比：1:1（aspect-ratio: 1）
- 圆形：border-radius: 50%，overflow: hidden
- 图片：object-fit: contain，尺寸 100%
- 无图时：彩色背景 + emoji，10色循环：
  `#EDE9FE / #FCE7F3 / #FEF3C7 / #D1FAE5 / #DBEAFE / #FEE2E2 / #F3F4F6 / #FDF4FF / #ECFDF5 / #FFF7ED`
- 标签：居中，11px，#374151，最多2行

---

## 6. 商品推荐卡片规范（You May Also Like）

- 2列网格，gap 8px
- 卡片圆角 10px，轻阴影
- 字段：品牌名（大写加粗 10px）/ 商品名（11px 灰）/ 现价（13px 粗）/ 原价（划线灰，可选）/ 折扣标签（紫色 pill，可选）/ Sold Out 标签（左上角，可选）/ 收藏心形（右上角）

---

## 7. 交互规则

| 操作 | 行为 |
|---|---|
| 切换顶导 Tab | 左侧导航重置到第一项，右侧内容重置 |
| 点击左侧一级导航 | 右侧渲染对应二级圆形列表 |
| 点击二级圆形（单 collection） | 跳转 collection 商品列表页 |
| 点击二级圆形（多 collection） | 右侧内容替换为三级圆形，左导保持不变 |
| 点击三级圆形 | 跳转对应 collection 商品列表页 |
| 点击三级返回按钮 | 右侧回到二级圆形视图 |

---

## 8. 后台配置能力

运营在后台需要配置：

**Tab 层**
- 新增/删除/排序/启停 Tab
- 编辑 Tab 名称

**一级导航层**
- 在某个 Tab 下新增/删除/排序/启停导航项
- 配置名称、图片
- 从 Collection 库多选关联 collections（驱动二级圆形数量）

**二级圆形层**
- 编辑每个二级圆形的名称、图片
- 从 Collection 库选关联 collections（1个或多个，驱动是否有三级）
- 排序/启停

**三级圆形层**
- 编辑名称、图片
- 排序/启停
- collection 归属自动继承父级，无需手动配置

**Collection 库**（只读引用，数据来自商品后台）
- 搜索、预览 collection 名称和 slug

---

## 9. 边界情况

| 情况 | 处理 |
|---|---|
| 导航项无二级圆形 | 不在前台展示该导航项 |
| 圆形图片加载失败 | 降级为彩色背景 + 首字母 |
| Collection 被删除 | 后台提示关联断开，前台该圆形隐藏 |
| Tab 下无启用的导航项 | 该 Tab 不在前台展示 |
| 三级圆形数量与二级关联 collection 数不一致 | 后台校验并提示，多余的三级隐藏，缺少的自动补位 |
