# Looply Contact Us 设计 Checklist v0.1

> 状态：Contact Us 需求已确认，已生成 PRD v0.2 并合并至 Footer PRD v0.3
> 更新日期：2026-07-30
> 当前 UI：[Looply v1.0](https://www.figma.com/design/rLK7XCdVvYqEHQHd7WjOkk/Looply-v1.0?t=VQDfvElDOm7kMhSj-0)
> Mobile 状态稿：[Looply v1.0 · node 6772:3636](https://www.figma.com/design/rLK7XCdVvYqEHQHd7WjOkk/Looply-v1.0?node-id=6772-3636&t=pVFMkiNnle3oB3B1-0)

## 一、输入源盘点

| 输入源 | 当前情况 | 处理方式 |
|---|---|---|
| Figma《Looply v1.0》 | 已提供设计文件和 Mobile Contact Us 状态节点 | 作为当前 UI、联系信息和状态文案基线 |
| Looply 现有 PC 页面 | 已提供历史页面 | 仅作为早期输入，不覆盖当前 Figma 设计 |
| PC 端入口 | 已确认：首页 Footer → Contact Us | 纳入当前版本 |
| Mobile 端入口 | 已确认：个人中心 → Contact Us | 纳入当前版本 |
| Mobile 端设计稿 | 已提供 | 节点覆盖默认、邮箱校验错误、填写完成、提交成功和提交失败 |
| 产品架构图 | 暂未发现 Contact Us 专项内容 | 当前不阻塞轻量页面方案讨论 |
| 系统流程图 | 暂未发现 | 当前提交与邮件发送流程已在 PRD 2.1.6 闭合 |
| ER 图 | 本页面无专项输入源 | 本期不建立独立 Contact Us 业务记录，无需新增对应业务实体 |
| 竞品调研 | 本次不单独开展 | 用户确认直接参考 Looply 现有页面 |

## 二、已确认设计

### 2.1 页面入口

| 终端 | 页面入口 | 结果 |
|---|---|---|
| PC Web | 首页 Footer → Contact Us | 打开 Contact Us 页面 |
| Mobile | 游客态和登录态的个人中心 → Contact Us | 打开 Contact Us 页面，不触发登录 |

### 2.2 联系表单字段

当前版本沿用现有页面的三个字段，不增加订单号、问题类型或附件上传。

| 字段 | 页面文案 | 控件类型 |
|---|---|---|
| 姓名 | Full Name | 单行文本输入框 |
| 邮箱 | Email | 邮箱输入框 |
| 留言 | Message | 多行文本输入框 |

提交操作文案沿用 `Send`。

### 2.3 联系信息

- 页面仅展示 Email 和 Email Response Time；
- Email：`service@looply.com`；
- Email Response Time：`We generally respond to customer inquiries within 1–2 business days.`；
- 电话、注册地址及退货地址提示不属于当前设计。

## 三、已收口的提交规则

### 3.1 提交校验与结果反馈

- 三个字段均为必填，并在失焦和点击 Send 时校验；
- 提交中禁止重复点击；
- 提交中 Send 置灰；
- 提交成功后不跳转；游客和登录用户均清空 Full Name、Email、Message，再显示 `Thanks for contacting us. We’ll get back to you as soon as possible.`；
- 成功 Toast 展示 4 秒后自动消失；
- 提交失败时显示 `Submit failed, please try again.`，保留内容并允许重试；
- 邮箱格式错误提示为 `Incorrect email`；
- PC 与 Mobile 均不接入 hCaptcha、Google reCAPTCHA 或其他 CAPTCHA，也不展示第三方验证码声明。

### 3.2 留言接收渠道

- Contact Us 表单由 Looply 服务端发送至 `service@looply.com`；
- 邮件内容包含用户提交的 Full Name、Email 和 Message；
- 邮件为当前版本唯一业务记录，不建立独立 Contact Us 业务记录或用户侧咨询历史；
- 必要技术日志不记录 Full Name、Email 或 Message 原文；
- 用户浏览器不直接发送邮件；
- 仅在邮件服务确认已受理发送请求后，页面显示提交成功。

### 3.3 用户确认邮件

- 当前版本不向用户自动发送确认邮件；
- 提交结果仅在 Contact Us 页面内反馈；
- 客服后续从 `service@looply.com` 人工回复用户填写的 Email。

### 3.4 Mobile 游客入口

- 游客态和登录态的个人中心均展示 Contact Us；
- 游客点击后直接进入页面，不触发登录或注册；
- 游客与登录用户均可查看联系信息并提交表单。

### 3.5 登录用户字段初始值

- 登录用户进入页面时自动带入账户姓名和邮箱，游客保持空白；
- 登录用户可修改自动带入的姓名和邮箱；
- 修改后的邮箱只作为本次客服回复地址，不回写账户邮箱；
- 账户姓名或邮箱缺失、读取失败时，对应字段保持空白并允许手动填写；
- 提交成功后，游客和登录用户均清空 Full Name、Email、Message；登录用户停留在当前页面时不重新带入账户姓名和邮箱。

### 3.6 未提交内容与离开确认

- 当前任一字段值与页面初始值不同时，点击页面返回或站内跳转显示 `Leave without sending?`；
- 点击 Stay 留在页面并保留内容，点击 Leave 清空内容并继续离开；
- 提交成功并清空字段后，以空白字段作为新的页面初始值，离开页面不再提示；
- 关闭浏览器、App 被系统终止或跨设备访问时，不保存、不恢复草稿。

## 四、上线依赖

- 技术配置服务端邮件发送能力，并确保 `service@looply.com` 可正常收信；
- 客服与运营复核客服邮箱和响应时效；
- 开发按 Figma《Looply v1.0》实现 PC 与 Mobile 的字段错误、提交中、成功和失败状态。
- 设计将 Figma 成功态同步为 Full Name、Email、Message 均已清空。

## 五、产出文件

- `docs/product/looply-Contact-Us-PRD-v0.2.md`
- `docs/product/looply-Contact-Us-PRD-修订记录.md`
- `docs/product/looply-Footer-PRD-v0.3.md`
- `prototypes/contact-us/looply-contact-us-prototype-v0.1.html`

## 六、原型一致性检查

- 已覆盖 PC 首页 Footer → Contact Us，以及 Mobile 游客态 / 登录态个人中心 → Contact Us；
- 已覆盖游客空白字段、登录用户账户姓名与邮箱自动带入且可编辑；
- Figma 状态稿覆盖字段错误、填写完成、提交成功和提交失败；PRD 补充提交中和未提交离开规则；
- 已验证 Stay 保留内容，Leave 清空内容并离开，Mobile 返回后回到个人中心；
- 当前版本不展示验证码及第三方验证码声明，联系邮箱及表单接收邮箱为 `service@looply.com`；
- 本地原型 v0.1 与 PC 视觉稿 v0.2 属于历史评审产物，仍包含已删除的电话、地址或旧状态文案，不作为当前 UI 验收基线。
