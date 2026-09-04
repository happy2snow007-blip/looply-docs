# Looply C1 Sell PRD

版本：v0.3  日期：2026-09-03  状态：评审稿

## 一、产品范围

C1 Sell 为用户提供三种出售方式：In-Home Appointment、Visit Looply、Ship To Us。本版本覆盖 PC / Mobile 入口、Sell 首页、Accepted Brands、Condition Guidelines、Service Area、预约提交、Contact Us、确认邮件和 C1 运营后台基础流程。

PC 与 Mobile 入口和布局以 Figma《LOOPLY 草稿》为准；逐页文案、字段、状态、按钮及跳转以[逐页交互清单](./looply-C1-Sell-逐页交互清单-v0.1.md)为准。该清单是本 PRD 的 UI 交互附件，不再以 Demo 作为设计基线。

## 二、入口与页面

| 页面 / 区域 | 入口与核心交互 |
|---|---|
| Sell 首页 | PC Header `SELL`、Footer Sell 分组、Mobile Sell Tab；Hero `Sell Now` 进入预约，`Explore your options` 定位 Three Ways to Sell |
| Three Ways to Sell | In-Home / Visit / Ship 方式卡片；侧卡 Hover 后放大并展示对应详情 |
| What We Buy | 固定约 10 个品牌横向滚动；`View All Brands & Categories` 进入完整品牌页 |
| Selling Tips / How to Get Paid | 展示说明和步骤，不设置额外跳转 |
| FAQ / 底部 CTA | FAQ 折叠；`View All FAQs` 进入 Seller FAQ；`Sell Now` 进入预约 |
| Footer 新增 | Sell with Looply、Accepted Brands、Service Area、Condition Guidelines、Seller FAQ、Seller agreement |
| Accepted Brands | 品类筛选、品牌首字符实时过滤；完整列表读取后台生效配置 |
| Condition Guidelines | 9 个成色判断模块，展示 Accepted / Not Accepted 标准 |
| Service Area | ZIP 查询；返回覆盖、未覆盖或非法 ZIP 状态 |

## 三、预约流程

### 3.1 个人信息

采集 `First name *`、`Last name *`、`Phone *`、`Email *`。联系授权文案链接复用 C2 的 `Privacy Policy` 和 `Terms of Service`。`Continue` 校验通过后进入下一步。

### 3.2 物品信息

`Handbags`、`Jewelry`、`Watches` 品类至少选择一项且支持多选；品牌至少输入一项且支持多选。选择品类后按后台生效配置联想品牌，未选择品类不联想；后台未配置的品牌仍可手动输入。照片选填，最多 10 张。必填项缺失 Toast：`Please select at least one category and enter at least one brand to continue.`

### 3.3 选择售卖方式

用户输入必填 ZIP，系统复用地址页 ZIP 校验并查询覆盖配置。支持上门时默认勾选 `In-Home Appointment`；不支持上门时默认勾选 `Ship To Us`，`In-Home Appointment` 置灰；`Visit Looply` 始终可选。

### 3.4 方式信息

- In-Home：Street address、City、ZIP code 必填；Apartment、Preferred date、Referral code 选填；提交时同意 Seller Terms。
- Visit Looply：固定地址 `6300 Wilshire Blvd, Los Angeles, CA 90048 Appointment only.`；Preferred date、Referral code 选填。
- Ship To Us：Street address、City、State、ZIP code 和 Mail-in Terms 勾选必填；Apartment 选填；提交后邮件发送后续邮寄信息。

### 3.5 成功页与 Request ID

成功页展示 `Request received`、Selling method、Total pieces 和 Preferred date（未填写时隐藏整行）。Request ID 格式为 `[METHOD]-[YYMMDD]-[LOCATION]-[RANDOM]`：方法码 `IH` / `VL` / `ST`；日期为正式提交日期；Visit Looply 的 Location 为 `LA`，其他方式使用客户地址州缩写；RANDOM 为后台生成并校验唯一性的 4 位大写字母和数字。

## 四、配置与数据来源

- In-Home 支持 ZIP 由运营后台新增、编辑、启用 / 停用；前台仅读取生效配置。
- 品类与品牌映射由运营后台维护；Accepted Brands 读取生效配置。
- 首页 What We Buy 滚动品牌为固定内容，不读取后台。
- ZIP 与品牌 / 品类独立判断，不要求三者组合命中。

## 五、Contact Us

页面字段：Business Type（Sell / Buy）、Full Name、Email、Message，均为必填。Sell 提交至 `sell@looply.com`，Buy 提交至 `service@looply.com`。邮件标题统一为 `Looply Contact Us - {submission time} - {Full Name}`，正文包含页面填写信息。

## 六、邮件、后台与法律文件

预约成功后发送确认邮件并写入 `https://ops.looply.com/` 的 C1 Sell 独立模块。C1 后台基础范围为查看、筛选、分配负责人、更新预约状态、备注和重发邮件；权限分级、脱敏、审计、导出和数据保留列入后续版本。

全站 `Terms of Service`、`Privacy Policy`、`Your Privacy Choices` 与 C2 共用；Sell 使用 `Seller Terms`、`Mail-in Terms` 和 `Sales Agreement`。Seller Agreement 正文以[业务提供文档](https://zhuanspirit.feishu.cn/docx/X2vjdYalQopAskxavSTcB4pAnR2?from=from_copylink)为准。

## 七、多语言、埋点与校验

静态 UI 文案使用统一 message key；品牌、品类、FAQ、城市和法律正文按翻译资源管理；当前基线为 `en-US`，缺失译文回退英文。关键埋点覆盖 Sell 首页、CTA、ZIP 查询、预约步骤、提交结果、确认邮件、Contact Us 和后台操作；不记录姓名、邮箱、电话、完整地址、Message 原文或照片。

表单复用现有公共校验、错误提示、提交中防重复和草稿恢复规则。未提交草稿在同一设备同一浏览器自动恢复，提交成功后清除。

## 八、验收标准

1. PC / Mobile 可从各自入口进入 Sell，页面和交互与 Figma 及逐页交互清单一致。
2. 首页各屏、Footer 新增入口、Accepted Brands、Condition Guidelines、Service Area 状态和预约四步流程均可按清单验收。
3. ZIP 覆盖结果正确触发方式默认选择和置灰规则。
4. 必填 / 选填、品牌联想、照片上限、协议链接和公共校验符合本 PRD。
5. 成功页 Request ID、字段隐藏规则、确认邮件和后台预约记录符合本 PRD。
6. Contact Us 按 Sell / Buy 正确分流邮箱和邮件标题。
