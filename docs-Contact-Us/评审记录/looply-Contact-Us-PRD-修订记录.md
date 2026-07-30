# Looply Contact Us PRD 修订记录

| 版本 | 日期 | 修改人 | 修改内容 |
|---|---|---|---|
| v0.1 | 2026-07-24 | Codex | 首次生成 Contact Us 轻量 PRD；明确 PC / Mobile 入口、游客可用性、登录用户字段自动带入、联系表单、未提交离开确认、hCaptcha、联系信息、提交状态、服务端发送至 `service@looply.com` 的接收规则及人工回复方式 |
| v0.2 | 2026-07-30 | Codex | 新增法律文件按市场配置、版本号、生效日期、语言和审核状态管理的通用规则；明确香港市场法律适配属于后续阶段；确认当前版本不接入 hCaptcha、Google reCAPTCHA 或其他 CAPTCHA，并删除验证码声明、验证步骤、状态、异常、埋点及外部依赖；确认 Full Name、Email、Message 均必填，表单由 Looply 服务端发送至 `service@looply.com`；本期不建立独立 Contact Us 业务记录，邮件为唯一业务记录，必要技术日志不记录表单原文 |
