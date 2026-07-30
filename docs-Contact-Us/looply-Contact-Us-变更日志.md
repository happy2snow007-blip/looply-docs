# Looply Contact Us 变更日志

## 基线版本（已交付开发）

**V1.0（2026-07-24）**
- 交付内容：
  - PRD：`looply-Contact-Us-PRD-v0.1.md`
  - 原型：`looply-contact-us-prototype-v0.1.html`
  - Checklist：`looply-Contact-Us-Checklist-v0.1.md`
- 交付位置：`/Users/zz/Documents/Looply/deliveries/contact-us/Contact Us-交付开发 V1.0-20260724/`

---

## V1.1（进行中）— 未交付

### 变更内容

#### PRD 调整

##### 🔄 法律文件与市场版本管理（迭代中）
- **PRD 版本**：v0.1 → v0.2
- **PRD 文件**：`looply-Contact-Us-PRD-v0.2.md`
- **状态说明**：已补充通用产品规则，香港市场法律适配明确放入后续阶段，不纳入本期开发
- **变更内容**：
  - 法律文件按市场 / 国家、语言、版本号、生效日期和审核状态配置，不在前端写死单一国家版本；
  - Contact Us 与公共 Footer 使用同一市场法律文件映射；
  - 缺少已批准生效映射时，发布检查失败，不静默回退到未经确认的其他市场版本；
  - 香港市场后续接入前须完成 Privacy Policy、Terms of Service、语言、版本号、生效日期和链接的法务确认；本期不实现香港市场映射。
  - 当前版本不接入 hCaptcha、Google reCAPTCHA 或其他 CAPTCHA，页面不展示第三方验证码声明；
  - Full Name、Email、Message 均为必填，校验通过后由 Looply 服务端将表单信息发送至 `service@looply.com`。
  - 本期不建立独立 Contact Us 业务记录或用户侧咨询历史；邮件为唯一业务记录，必要技术日志不记录 Full Name、Email 或 Message 原文。
  - 以 Figma《Looply v1.0》为当前 UI 基线；页面仅展示 Email 与 Email Response Time，删除电话、注册地址和退货地址提示。
  - 邮箱格式错误、提交中、成功和失败状态按 Figma 文案及表现更新。
- **迭代记录**：
  - 2026-07-28：因香港市场已纳入后续规划，补充法律文件版本与国家适用规则，并明确本期不接入香港市场映射。
  - 2026-07-29：确认切换为 Google reCAPTCHA、三字段必填及服务端邮件接收规则；同步更新 PRD v0.2、主原型 v0.1 和 PC 视觉稿 v0.2。
  - 2026-07-30：确认提交内容不另存；同步更新 PRD v0.2、Checklist、修订记录和模拟评审处理状态。
  - 2026-07-30：最终确认当前版本不使用任何 CAPTCHA；删除 PRD、Checklist、主原型和 PC 视觉稿中的验证码声明、验证流程、状态、异常、埋点及依赖。
  - 2026-07-30：同步修正默认态描述，游客字段为空，登录用户自动带入 Full Name 和 Email，Message 为空。
  - 2026-07-30：确认 UI 为最终展示基线；仅保留 Email 与 Email Response Time，删除电话和地址；邮箱校验提示改为 `Incorrect email`，提交中 Send 置灰，成功提示改为 `Thanks for contacting us. We’ll get back to you as soon as possible.`，失败提示改为 `Submit failed, please try again.`。

### 影响范围

- **PRD**：已更新（v0.2）
- **Checklist**：已更新数据保存边界、Figma UI 基线、联系信息和状态文案
- **模拟评审记录**：#3 验证码方案、#4 数据保存边界、#5 登录用户默认态已收口
- **原型**：主原型 v0.1、PC 视觉稿 v0.2 作为历史评审产物保留，不作为当前 UI 验收基线
- **文档中心**：同步当前工作稿；V1.0 交付包作为历史版本保留，不在本次更新

### 待办事项

- [ ] 后续阶段启动时，由法务确认香港市场 Privacy Policy、Terms of Service 的适用范围与具体文本；
- [ ] 后续阶段确认香港市场语言版本（英文、繁体中文或双语）；
- [ ] 后续阶段确认各法律文件版本号、生效日期、审核状态和链接；
- [ ] 后续阶段确认市场配置缺失时的发布阻断检查由哪个系统负责。
