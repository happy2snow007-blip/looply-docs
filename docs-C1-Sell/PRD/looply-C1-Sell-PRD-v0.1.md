# Looply C1 Sell PRD（讨论稿）

版本：v0.1  
日期：2026-09-02  
状态：讨论稿，非开发定稿

## 一、概述

### 1.1 背景与目标

C1 Sell 面向希望将符合条件的品牌商品出售给 Looply 的用户。当前 Demo 以三种售卖方式帮助用户选择合适的提交路径，并通过 ZIP Code 对 In-Home Service 进行初步区域判断。

目标：让用户理解三种售卖方式，快速判断是否支持上门服务，并进入对应操作入口。

### 1.2 当前版本范围

- Sell 首页及三种方式：In-Home Appointment、Visit Looply、Ship to Us。
- Service Area 页面：区域说明、ZIP Code 查询、覆盖/未覆盖结果。
- Contact Us 页面：联系信息与咨询表单 Demo。
- Header、Footer、Mobile bottom navigation 与 Sell 页面整合。

### 1.3 用户角色

- 访客：浏览 Sell 信息、查询服务区域、提交联系表单。
- 客户代表：后续确认用户完整地址与预约（当前仅作为业务说明，未实现后台流程）。

### 1.4 术语说明

| 术语 | 含义 |
|---|---|
| C1 Sell | Looply 卖家侧业务 |
| In-Home Service | 上门回收服务 |
| Visit Looply | 用户到 Looply 指定地点提交商品 |
| Ship to Us | 用户邮寄符合条件的商品 |
| ZIP Code | 美国五位邮政编码，用于初步区域判断 |

### 1.5 全局页面流转

`Sell 首页 → Service Area → ZIP 查询结果 → In-Home Appointment / Sell 首页 Three Ways to Sell / Contact Us`

`Sell 首页 → Accepted Brands / Condition Guide / FAQ / Seller Terms / Sales Agreement`

## 二、需求详细描述

### 2.1 Sell 首页与三种售卖方式

**功能描述**：展示三种售卖方式及其适用场景，引导用户进入对应流程。

**页面元素**：

- In-Home Appointment：预约上门服务。
- Visit Looply：到店提交。
- Ship to Us：邮寄提交。
- Sell Now 主 CTA。
- Accepted Brands、Condition Guide、FAQ 等辅助入口。

**操作流程**：

- 用户点击 In-Home Appointment，进入上门预约入口。
- 用户点击 Visit Looply 或 Ship to Us，进入对应方式说明或流程入口。
- 用户点击 Service Area，进入服务区域查询页。

**UI 关联**：

- PC：`index.html`（v2.6.4 Demo）。
- Mobile：`looply-sell-page-mobile-demo.html` 及 `index.html` 移动端布局（v2.6.4 Demo）。

### 2.2 Service Area 页面

**功能描述**：用户输入五位 ZIP Code，查询所在区域是否提供 In-Home Service。

**页面布局**：

- 页面标题：`In-Home Service Across Greater Los Angeles`。
- 服务范围说明及 Greater Los Angeles、Orange County 城市列表。
- ZIP Code 输入区及 `Check Availability` 按钮。
- 结果区根据查询结果展示一组操作。
- 页面底部保留免责声明和 `Sell Now`。

**输入与校验**：

| 字段 | 控件 | 规则 | 校验时机 |
|---|---|---|---|
| ZIP Code | 单行输入框 | 必须为五位数字 | 点击查询或按 Enter |

**查询结果**：

| 状态 | 展示 | 操作 |
|---|---|---|
| 覆盖 | `In-Home Service available`、`Great news—we serve your area.` 及地址需代表确认的说明 | `Request an In-Home Appointment` → `index.html?open=sell&mode=home` |
| 未覆盖 | `Other selling options`、说明仍可通过到店或邮寄出售 | `Explore Other Ways to Sell` → `index.html#ways`；`Contact us` → `contact-us.html` |

**异常状态**：

- 非五位数字：提示 `Enter a valid five-digit ZIP code.`。
- 配置加载中：提示服务区域数据仍在加载。
- 配置读取失败：提示暂时无法查询，并提供 Contact Us 方向。

**业务规则**：ZIP 查询仅提供初步区域判断；完整地址和预约仍由客户代表确认。当前 ZIP 库是否可作为正式对客覆盖数据，待业务确认。

**UI 关联**：PC / Mobile：`service-area.html`（v2.6.4 Demo）。

### 2.3 Contact Us 页面

**功能描述**：为用户提供咨询入口。

**页面元素**：

- 标题：`How can we help?`
- Name、Email、Subject、Message 字段。
- `sell@looply.com`；电话当前显示 `To be confirmed`。
- 地址：`6300 Wilshire Blvd, Los Angeles, CA 90048`。

**操作流程**：用户提交合法表单后显示成功提示。当前 Demo 将表单内容暂存在浏览器会话中，不代表真实发送。

**UI 关联**：PC / Mobile：`contact-us.html`（v2.6.4 Demo）。

## 三、依赖与风险

- ZIP 覆盖配置：`config/service-zip-ranges.json`；正式数据来源和更新责任待确认。
- 上门预约流程、地址确认和客户代表工作台尚未纳入当前 Demo。
- Contact Us 真实邮件服务商、发送域名、隐私政策与数据保存期限待确认。
- Visit Looply 地点、Ship to Us 物流、支付及 SLA 规则待确认。

## 四、版本规划

### 当前版本（讨论稿）

完成 Sell 信息展示、Service Area ZIP 初步查询、结果分流和 Contact Us Demo。

### 后续迭代方向

- 完整地址确认与上门预约。
- Visit Looply 地点与营业信息。
- Ship to Us 包装、物流和状态跟踪。
- Contact Us 接入真实提交及客服处理链路。

## 五、附录：设计稿索引

| 页面 | PC | Mobile | 基线 |
|---|---|---|---|
| Sell 首页 | `index.html` | `looply-sell-page-mobile-demo.html` | v2.6.4 Demo |
| Service Area | `service-area.html` | `service-area.html` 移动布局 | v2.6.4 Demo |
| Contact Us | `contact-us.html` | `contact-us.html` 移动布局 | v2.6.4 Demo |

## 六、待确认项

- ZIP 覆盖库是否允许正式对客使用。
- 三种售卖方式各自的真实后续流程与本期边界。
- 上门预约是否需要登录、地址字段和可预约时间选择。
- Contact Us 是否接入真实邮件或工单系统。
- PC / Mobile UI 是否以 v2.6.4 Demo 作为最终视觉基线。
