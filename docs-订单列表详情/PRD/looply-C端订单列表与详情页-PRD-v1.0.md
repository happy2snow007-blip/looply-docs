# Looply C 端订单列表页 & 订单详情页 PRD v1.0

> 买家侧"我的订单"列表页 + 订单详情页完整需求定义
>
> Version 1.0 · 2026-07-05 · 面向：前端 / 后端开发

---

## 一、概述

### 1.1 背景与目标

本 PRD 定义买家在 looply 平台查看已购订单的完整体验，包含"我的订单"列表页和单笔订单详情页（含物流追踪、退款详情）。

**核心目标：**

- 让买家清晰查看所有历史订单及其当前状态
- 按状态筛选快速定位目标订单
- 在详情页内查看完整订单信息：商品、物流、支付、退款
- 物流追踪和退款详情通过弹窗/底部抽屉展示，减少页面跳转
- PC 和 APP 双端适配，体验一致

### 1.2 前置依赖

| 依赖模块 | 说明 |
|---------|------|
| 订单状态模型 | 引用《looply 订单支付 PRD v1.0》第二章分层状态模型 |
| 支付渠道 | 引用《支付渠道对接集成说明文档 v1.0》 |
| 物流管理 | 物流轨迹数据由物流模块提供 |
| 用户管理 | 登录态、地址管理 |

### 1.3 术语说明

引用《looply 订单支付 PRD v1.0》1.6 术语说明，本文档额外定义：

| 术语 | 说明 |
|------|------|
| 发货组（Fulfillment Group） | 一个订单可能分多个包裹发货，每个包裹对应一个发货组 |
| 物流状态卡 | 订单详情页顶部的物流进度摘要卡片 |
| 追踪弹窗 | 展示完整物流轨迹的模态弹窗（PC）或底部抽屉（APP） |
| 退款弹窗 | 展示单笔退款详细信息的模态弹窗（PC）或底部抽屉（APP） |

---

## 二、我的订单列表页（My Orders）

### 2.1 页面入口

- 登录后，顶部导航 → 用户头像 → My Account → Orders
- 底部 Tab（APP 端）→ My Account → Orders
- 订单成功页 "View Order Details" 按钮

**前置条件：** 用户必须已登录。未登录用户访问时 redirect 到登录页，登录后跳回。

### 2.2 页面布局

| 端 | 布局方式 |
|----|---------|
| PC 端 | 左右分栏：左侧 MY ACCOUNT 侧边导航（Orders / Wishlist / Address / Payment / Settings），右侧为订单列表主内容 |
| APP 端 | 顶部导航栏（返回 + "My Orders" 标题 + 搜索按钮）+ Tab 筛选栏 + 垂直滚动列表 |

### 2.3 页面元素

#### 2.3.1 PC 端侧边导航

| 元素 | 说明 |
|------|------|
| 标题 | "MY ACCOUNT"（大写灰色小字） |
| Orders | 带订单图标 + 右侧数字角标（总订单数），当前页高亮 |
| Wishlist | 带心形图标 + 右侧数字角标 |
| Address | 带定位图标 |
| Payment | 带银行卡图标 |
| Settings | 带齿轮图标 |

#### 2.3.2 页面标题与搜索

| 端 | 元素 | 说明 |
|----|------|------|
| PC | 页面标题 | "My Orders"，左对齐 |
| PC | 搜索框 | 右侧，placeholder "Search orders"，支持按订单号模糊搜索 |
| APP | 顶部导航 | 左侧返回箭头 + 居中标题 "My Orders" + 右侧搜索图标 |

#### 2.3.3 状态 Tab 筛选栏

水平 Tab 栏，用于按订单状态筛选：

| Tab | 显示文案 | 筛选条件 | 角标 |
|-----|---------|---------|------|
| All | "All" | 显示全部订单 | 无 |
| Confirmed | "Confirmed" | order_status = paid | 该状态数量（有则显示） |
| On its way | "On its way" | order_status = shipped | 该状态数量（有则显示） |
| Completed | "Completed" | order_status = completed | 无 |

**交互说明：**

- 默认选中 "All" Tab
- 切换 Tab 不刷新页面，前端筛选（数据量小于 50 时）或接口重新请求
- APP 端 Tab 栏支持水平滑动（当 Tab 数量多时）
- Tab 角标仅在数量 > 0 时显示
- Cancelled 状态订单仅在 "All" Tab 下可见，不设独立 Tab

#### 2.3.4 订单卡片

每条订单以卡片形式展示，卡片内包含：

**PC 端订单卡片结构：**

```
┌─────────────────────────────────────────────────────────────┐
│  ← 上一单          (分页箭头轮播)           下一单 →        │
│                                                             │
│  商品图 1  商品图 2  商品图 3 ...    $总金额               │
│                                     (N Items) [如多件显示]  │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  #订单号   [状态标签]                确认日期               │
└─────────────────────────────────────────────────────────────┘
```

**APP 端订单卡片结构：**

```
┌──────────────────────────────────────────────┐
│  #订单号                     [状态标签]       │
│  Confirmed Jun 4, 2026                       │
│                                              │
│  商品图1  商品图2  商品图3   $总金额         │
│                              (N Items)       │
│                                              │
│                        [View Details]        │
└──────────────────────────────────────────────┘
```

#### 2.3.5 订单卡片字段说明

| 字段 | 数据来源 | 说明 |
|------|---------|------|
| 订单号 | order.order_no | 格式 #LPY-20260604-0847 或 #2026060408471234 |
| 状态标签 | order.order_status | 见下方状态标签样式 |
| 确认日期 | order.created_at | 格式 "Confirmed Jun 4, 2026" |
| 商品图片 | order_item.product_image | 最多展示 3 张缩略图（PC 端轮播可查看全部） |
| 总金额 | order.total_amount | 格式 "$1,524.00" |
| 商品件数 | count(order_items) | 单件商品不显示件数标注；多件显示 "(N Items)" |
| 退款标记 | 聚合 order_item.refund_status | 若有 refunded 的商品，对应商品图上叠加 "Refund" 角标 |

**状态标签样式：**

| order_status | 标签文案 | 标签样式 |
|-------------|---------|---------|
| paid | "Confirmed" | 蓝色背景 + 蓝色文字 (#EFF6FF / #2563EB) |
| shipped | "On its way" | 橙色背景 + 橙色文字 (#FFF7ED / #EA580C) |
| completed | "Completed" | 绿色背景 + 绿色文字 (#ECFDF5 / #059669) |
| cancelled | "Cancelled" | 灰色背景 + 灰色文字 (#F3F4F6 / #6B7280) |

#### 2.3.6 分页与排序

| 规则 | 说明 |
|------|------|
| 排序 | 按 order.created_at 倒序（最新在前） |
| 分页 | PC 端每页 10 条，底部分页器；APP 端无限滚动加载，每次 10 条 |
| 空态 | 无订单时显示空态插图 + "You haven't placed any orders yet" + "Continue Shopping" 按钮 |

### 2.4 操作流程

1. 用户进入 "My Orders" 页面，默认加载 "All" Tab 下全部订单
2. 用户可通过 Tab 筛选查看特定状态的订单
3. 用户可通过搜索框输入订单号搜索
4. 点击订单卡片（PC 端点击卡片任意位置 / APP 端点击 "View Details" 按钮）→ 进入订单详情页

### 2.5 异常处理

| 异常 | 处理方式 |
|------|---------|
| 网络异常 | 显示错误提示 + 重试按钮 |
| 接口超时 | 列表区域 skeleton 加载态，超时后显示 "Loading failed, please try again" |
| 搜索无结果 | 显示 "No orders found for 'xxx'" |

---

## 三、订单详情页（Order Detail）

### 3.1 页面入口

- 订单列表页 → 点击订单卡片
- 订单成功页 → "View Order Details" 按钮
- 邮件通知中的 "View Order" 链接
- URL 直接访问：`/account/orders/{order_id}`

### 3.2 页面布局

| 端 | 布局方式 |
|----|---------|
| PC 端 | 左右分栏（同列表页侧边导航），右侧为订单详情主内容，垂直排列各信息卡片 |
| APP 端 | 顶部导航栏（返回 + "Order Details" 标题 + 通知铃铛）+ 垂直滚动内容 |

### 3.3 页面头部

#### 3.3.1 面包屑导航（仅 PC 端）

格式：`My Orders > Order #LPY-20260604-0847`

"My Orders" 可点击返回列表页。

#### 3.3.2 订单标识信息

| 字段 | 说明 |
|------|------|
| 订单号 | 格式 "Order #LPY-20260604-0847"（PC 端），"#LPY-20260604-0847"（APP 端，附带复制按钮） |
| 状态标签 | 同列表页状态标签样式 |
| 确认日期 | "Confirmed Jun 4, 2026"，PC 端右对齐，APP 端在订单号下方 |

### 3.4 物流状态卡（Fulfillment Status Card）

详情页顶部紧接订单头部的核心信息卡片，根据订单当前物流状态展示不同内容。

#### 3.4.1 状态变体

| order_status | 卡片展示内容 | 可点击 |
|-------------|-------------|--------|
| paid（待发货） | **"Preparing for shipment"** + 配送时效说明："shipped within 1–3 business days after payment, with delivery in 3–7 business days after shipment." + 📦 图标 | 否 |
| shipped（运输中） | **"On the way to you"** + 预计送达日期 "Est. delivery: May 22 - May 24, 2026" + 🚚 图标 + 右箭头 | 是，点击展开追踪弹窗 |
| completed（已签收） | **"Delivered on May 23, 2026"** + 签收信息 "Signed by John D. · May 23, 2026, 11:42 AM" + ✓ 图标 + 右箭头 | 是，点击展开追踪弹窗 |
| cancelled | **"Order cancelled (N Refunds completed)"** + 退款总额 "$1,575.20 total refunded" + 右箭头 | 是，点击展开退款汇总 |

#### 3.4.2 多包裹场景

当一个订单包含多个发货组（包裹）时：

- 物流状态卡按包裹分组，每个包裹独立一张卡片
- 卡片标题格式："Package 1" + 包裹状态标签（Preparing / Shipped / Delivered）
- 每个包裹卡片可独立点击查看该包裹的物流轨迹

**包裹状态标签样式：**

| package_status | 文案 | 样式 |
|---------------|------|------|
| pending | "Preparing" | 蓝色文字 |
| shipped | "In Transit" | 橙色文字 |
| received | "Delivered" | 绿色文字 |

### 3.5 商品列表

#### 3.5.1 商品行信息

每件商品以行卡片展示：

| 字段 | 说明 |
|------|------|
| 商品图片 | 56×56px（APP）/ 64×64px（PC），圆角 |
| 品牌 | 大写灰色小字，如 "LOUIS VUITTON" |
| 商品名称 | 主文字，如 "Silver tone metal silver necklace" |
| 成色等级 | 标签样式 "Condition: Very Good" |
| 价格 | 右对齐，加粗，如 "$651" |
| 退款标记 | 若该商品 refund_status = refunded，商品图上叠加 "Refund" 角标（红底白字） |

#### 3.5.2 退款信息行

如果订单中有已完成的退款，在商品列表区域内显示退款摘要行（APP 端为可点击卡片）：

| 字段 | 说明 |
|------|------|
| 标题 | "Refund completed on Jun 5, 2026"（以退款完成日期为准） |
| 副标题 | "$873.00 returned to Visa ending in 6324" |
| 右箭头 | 可点击，展开退款详情弹窗 |

退款行在商品列表中按退款完成时间倒序排列，紧邻对应的被退商品下方。

### 3.6 Shipping & Delivery 区块

| 字段 | 说明 |
|------|------|
| 区块标题 | "Shipping & Delivery" |
| Shipping Address 标签 | 灰色小字 |
| 收件人姓名 | 如 "John Smith" |
| 详细地址 | 多行显示：街道 → 城市, 州 ZIP → 电话 |
| 示例 | "1600 Amphitheatre Pkwy, Apt 4B<br>Mountain View, CA 94043<br>(212) 555-0147" |

### 3.7 Payment 区块

| 字段 | 说明 |
|------|------|
| 区块标题 | "Payment" |
| 支付方式 | "Paid with" + 支付方式 logo（Visa/Mastercard/PayPal/Klarna/Apple Pay）+ 脱敏卡号（如 "**** **** **** 6324"） |
| Billing Address 标签 | 灰色小字 |
| 账单地址 | 若与收货地址相同显示 "Same As Shipping Address"；否则显示完整账单地址 |

### 3.8 Order Summary 区块

| 字段 | 说明 | 格式示例 |
|------|------|---------|
| Subtotal | 商品小计 + 件数 | "Subtotal (2 items)" → "$1,524.00" |
| Shipping | 运费 | "Shipping" → "Free" 或 "$XX.XX" |
| Tax | 税费（如订单含税则显示此行，否则不显示） | "Tax" → "$51.20" |
| **Total** | 订单总额（加粗） | "Total" → "$1,524.00" |
| Refund | 退款汇总（如有退款则显示此行） | "Refund (1 item)" → "-$873.00"（紫色文字） |

**金额计算规则：**
- Total = Subtotal + Shipping + Tax - Discount（如有优惠）
- Refund 行仅展示已退款成功的金额总和，不参与 Total 计算，作为附加信息展示
- Tax 行：仅在订单记录了税费时显示；若为 0 则不显示该行

### 3.9 页面底部

| 端 | 元素 | 说明 |
|----|------|------|
| APP | "Continue Shopping" 按钮 | 全宽黑色实心按钮，点击跳转首页 |
| PC | "Continue Shopping" 按钮 | 居中黑色实心按钮，点击跳转首页 |

---

## 四、物流追踪弹窗（Tracking Details）

### 4.1 触发方式

| 端 | 触发交互 | 展示形式 |
|----|---------|---------|
| PC | 点击物流状态卡 / 点击 "View Tracking" 按钮 | 页面居中模态弹窗（遮罩层） |
| APP | 点击物流状态卡 / 上滑 | 底部抽屉（Bottom Sheet），全屏覆盖 |

### 4.2 弹窗内容

#### 4.2.1 头部信息表

三行表格展示关键物流信息：

| 字段 | 说明 | 示例 |
|------|------|------|
| Carrier | 承运商名称 | "FedEx" |
| Tracking No. | 运单号 + 复制图标（点击复制到剪贴板） | "7489 2104 5678" |
| Est. delivery / Status | 运输中时为预计送达日期范围；已签收时为 "Delivered"（紫色文字） | "May 22 - May 24, 2026" 或 "Delivered" |

#### 4.2.2 追踪历史（Tracking History）

以时间线形式展示物流事件，从最新到最早：

**每条事件包含：**

| 字段 | 说明 |
|------|------|
| 状态标题 | 如 "In Transit" / "Delivered" / "Out for Delivery" / "Info Received" |
| 详细描述 | 如 "Arrived at transit hub" / "Signed by John D. at front door" |
| 地点 | 📍 地标格式："Los Angeles, CA" 或 "Shanghai, CN" |
| 时间 | "May 19, 2026 · 10:32 AM" |

**时间线样式：**

- 最新事件（第一条）：左侧实心紫色圆点 + 状态文字为紫色加粗
- 历史事件：左侧空心灰色圆点 + 状态文字为黑色加粗
- 圆点之间用竖线（虚线或实线）连接

**时间线状态枚举：**

| tracking_status | 显示文案 |
|----------------|---------|
| info_received | "Info Received" |
| in_transit | "In Transit" |
| out_for_delivery | "Out for Delivery" |
| delivered | "Delivered" |
| exception | "Exception" |

#### 4.2.3 弹窗关闭

- PC 端：右上角 × 按钮，或点击遮罩层
- APP 端：右上角 × 按钮，或下滑关闭

---

## 五、退款详情弹窗（Refund Details）

### 5.1 触发方式

| 端 | 触发交互 | 展示形式 |
|----|---------|---------|
| PC | 点击退款摘要行的右箭头 | 页面居中模态弹窗 |
| APP | 点击退款摘要行 | 底部抽屉（Bottom Sheet） |

### 5.2 弹窗内容

| 字段 | 说明 | 示例 |
|------|------|------|
| 标题 | "Refund Details" | — |
| Refund Total | 退款金额 + 状态标签 | "$652.00" + [Completed] 绿色标签 |
| Reason | 退款原因 | "Changed my mind" |
| Processed on | 退款完成日期 | "Jun 3, 2026" |
| Refund method | 退回渠道 + 脱敏卡号 | Visa logo + "**** **** 6324" |
| 退款商品 | 关联的退款商品信息（图片 + 品牌 + 名称） | 同商品行格式 |

### 5.3 退款状态标签

| refund_order.status | 标签文案 | 标签样式 |
|--------------------|---------|---------| 
| pending | "Processing" | 橙色背景 + 橙色文字 |
| succeeded | "Completed" | 绿色背景 + 绿色文字 |
| failed | "Failed" | 红色背景 + 红色文字 |

### 5.4 弹窗关闭

同物流追踪弹窗规则。

---

## 六、订单详情页状态变体

以下列出不同 order_status 下详情页的关键差异：

### 6.1 Confirmed 状态（order_status = paid）

| 区域 | 展示内容 |
|------|---------|
| 状态标签 | [Confirmed] 蓝色 |
| 物流状态卡 | "Preparing for shipment" + 时效说明文案 |
| 商品列表 | 全部商品（若有退款中的商品，不特殊标记——本期退款不由买家发起） |
| 操作按钮 | 无额外操作（本期不提供买家侧取消功能） |

### 6.2 On Its Way 状态（order_status = shipped）

| 区域 | 展示内容 |
|------|---------|
| 状态标签 | [On its way] 橙色 |
| 物流状态卡 | "On the way to you" + 预计送达时间，可点击查看追踪 |
| 商品列表 | 按包裹分组展示（若有多包裹），每组显示对应包裹内的商品 |
| 退款行 | 若有已完成退款，显示退款摘要行 |

### 6.3 Completed 状态（order_status = completed）

| 区域 | 展示内容 |
|------|---------|
| 状态标签 | [Completed] 绿色 |
| 物流状态卡 | "Delivered on May 23, 2026" + 签收信息，可点击查看追踪 |
| 商品列表 | 全部商品 |
| 退款行 | 若有已完成退款，显示退款摘要行 |
| Order Summary | Refund 行显示退款汇总 |

### 6.4 Cancelled 状态（order_status = cancelled）

| 区域 | 展示内容 |
|------|---------|
| 状态标签 | [Cancelled] 灰色 |
| 物流状态卡 | "Order cancelled (N Refunds completed)" + 退款总额，可点击查看退款汇总 |
| 商品列表 | 全部商品（不标记退款角标——因全部已退） |
| 操作按钮 | 底部 "Continue Shopping" 按钮 |

---

## 七、数据接口需求

### 7.1 订单列表接口

```
GET /api/orders
```

**请求参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| status | string | 否 | 筛选状态：paid / shipped / completed / cancelled；不传返回全部 |
| keyword | string | 否 | 搜索关键词（匹配订单号） |
| page | int | 否 | 页码，默认 1 |
| page_size | int | 否 | 每页条数，默认 10 |

**响应结构（列表项）：**

| 字段 | 说明 |
|------|------|
| order_id | 订单 ID |
| order_no | 订单号 |
| order_status | 状态枚举 |
| created_at | 创建时间 |
| total_amount | 总金额 |
| currency | 币种 |
| item_count | 商品件数 |
| items_preview | 商品预览数组（前 3 件），含 image_url, has_refund |
| status_counts | 各状态订单数量（用于 Tab 角标） |

### 7.2 订单详情接口

```
GET /api/orders/{order_id}
```

**响应结构：**

| 字段 | 说明 |
|------|------|
| order_id | 订单 ID |
| order_no | 订单号 |
| order_status | 状态枚举 |
| created_at | 创建时间 |
| items[] | 商品列表（含 fulfillment_status, refund_status, package_id） |
| packages[] | 包裹列表（含 carrier, tracking_no, package_status, est_delivery_start, est_delivery_end, delivered_at, signed_by） |
| shipping_address | 收货地址快照 |
| billing_address | 账单地址快照（null 则同收货地址） |
| payment_method | 支付方式信息（type, brand_logo, last_four） |
| summary | 金额汇总（subtotal, shipping_fee, tax, discount, total） |
| refunds[] | 退款列表（含 refund_id, amount, status, reason, processed_at, method, related_items） |

### 7.3 物流轨迹接口

```
GET /api/orders/{order_id}/packages/{package_id}/tracking
```

**响应结构：**

| 字段 | 说明 |
|------|------|
| carrier | 承运商 |
| tracking_no | 运单号 |
| status | 当前状态（in_transit / delivered 等） |
| est_delivery | 预计送达日期范围 |
| events[] | 轨迹事件数组，每项含 status, description, location, timestamp |

---

## 八、多语言

本模块的前端语言包命名空间：

| 命名空间 | 覆盖页面 | 包含内容 |
|---------|---------|---------|
| myOrders | 订单列表页 | Tab 文案、空态提示、搜索 placeholder、"View Details" 按钮 |
| orderDetail | 订单详情页 | 区块标题、物流状态文案、退款文案、按钮文案 |
| tracking | 追踪弹窗 | 字段标签、状态文案 |
| refund | 退款弹窗 | 字段标签、状态文案 |

---

## 九、设计稿关联

### 9.1 APP 端

| 页面 / 状态 | Figma 设计稿名称 | 说明 |
|------------|-----------------|------|
| 订单列表-全部 | My Orders - All Tab (Full) | 含 4 种状态订单混排 |
| 订单列表-带角标 | My Orders - All Tab with counts | Tab 栏显示数量角标 |
| 订单详情-Confirmed（待发货） | Order Detail - Confirmed - Preparing | 物流卡为 "Preparing for shipment" |
| 订单详情-On its way | Order Detail - On Its Way | 物流卡为 "On the way to you" + 预计日期 |
| 订单详情-Completed | Order Detail - Completed - Delivered | 物流卡为 "Delivered on..." |
| 订单详情-Cancelled | Order Detail - Cancelled | 物流卡为 "Order cancelled" |
| 订单详情-不同账单地址 | Order Detail - Diff Billing Address | Payment 区块展示完整账单地址 |
| 订单详情-含税 | Order Detail - With Tax | Order Summary 含 Tax 行 |
| 物流追踪-运输中 | Tracking Details - In Transit | 底部抽屉，最新事件为 In Transit |
| 物流追踪-已签收 | Tracking Details - Delivered | 底部抽屉，最新事件为 Delivered |
| 退款详情弹窗 | Refund Details Modal | 底部抽屉，退款完成信息 |

### 9.2 PC 端

| 页面 / 状态 | Figma 设计稿名称 | 说明 |
|------------|-----------------|------|
| 订单列表 | My Orders - PC | 左右分栏，订单卡片列表 |
| 订单详情-各状态 | Order Detail - PC (State Switcher) | 通过顶部 Tab 切换 Confirmed / On its way / Completed / Cancelled |
| 物流追踪弹窗-已签收 | Tracking Details - PC Modal - Delivered | 居中模态弹窗 |

---

## 十、交互规范补充

### 10.1 加载态

| 场景 | PC 端 | APP 端 |
|------|-------|--------|
| 列表首次加载 | Skeleton 占位（3 条卡片骨架） | Skeleton 占位（3 条卡片骨架） |
| 列表翻页/加载更多 | 底部 loading spinner | 底部 loading spinner |
| 详情页加载 | 全页 skeleton | 全页 skeleton |
| 物流追踪弹窗加载 | 弹窗内 spinner | 抽屉内 spinner |

### 10.2 复制交互

| 可复制字段 | 交互 |
|-----------|------|
| 订单号 | 点击复制按钮 → 复制到剪贴板 → 显示 toast "Copied to clipboard" |
| 运单号 | 点击复制图标 → 复制到剪贴板 → 显示 toast "Tracking number copied" |

### 10.3 通知铃铛（APP 端详情页右上角）

- 图标：铃铛 🔔
- 功能预留：点击后续跳转通知中心（本期无实际功能，展示即可）

### 10.4 PC 端状态切换器（设计稿特有）

PC 端订单详情页设计稿中包含一个状态切换器（State Tab），用于在同一页面内展示同一订单的不同状态样貌（仅用于设计评审 / 开发参照），**实际开发不实现此切换器**，详情页仅展示订单真实状态。

---

## 十一、版本记录

| 版本 | 日期 | 修改内容 | 作者 |
|------|------|---------|------|
| v1.0 | 2026-07-05 | 初始版本 | — |
