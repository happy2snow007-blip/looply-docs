# Looply Your Privacy Choices PRD v0.1

## 一、概述

### 1.1 子模块名称

Your Privacy Choices。

### 1.2 功能目标

为 Web 用户提供清晰的隐私选择说明入口，并引导用户进入个人中心已有的 `Privacy & Data` 页面管理 Cookie Preferences 及 `Do Not Sell or Share My Personal Information` 设置。

### 1.3 用户角色

- 游客；
- 登录用户。

两类用户使用相同页面和跳转路径，均可进入个人中心的隐私设置区域。

### 1.4 页面流转

`Footer · Your Privacy Choices` → `Your Privacy Choices 说明页` → `Manage Privacy Choices` → `个人中心 · Privacy & Data · Privacy Choices 设置区域`

### 1.5 当前终端范围

本期覆盖 PC Web 与 Mobile Web；App 不属于本 PRD 范围。

## 二、Your Privacy Choices 说明页

### 2.1 功能描述

用户点击全站 Footer 中的 `Your Privacy Choices` 后，进入独立说明页。页面向用户简要说明 Looply 对 Cookie、类似技术及广告相关信息的使用，并提供进入现有隐私设置区域的入口。

### 2.2 页面布局

页面复用对应 Web 终端的全局 Header 和 Footer：

- PC Web 主体采用左右双栏布局：左侧展示页面标题和简短引导语，右侧使用内容卡片展示说明文案、管理入口及 Privacy Policy 入口；
- Mobile Web 主体改为单列布局：页面标题、引导语和内容卡片按顺序纵向展示；卡片内容与交互不变。

页面顶部展示面包屑：`Home / Your Privacy Choices`。

### 2.3 页面元素

| 页面元素 | 展示内容 | 静态文案标识 | 交互 |
|---|---|---|---|
| 页面标题 | `Your Privacy Choices` | `privacy_choices.page.title` | 无 |
| 引导语 | `You have choices about how Looply uses certain information. Manage them at any time in Privacy & Data.` | `privacy_choices.page.intro` | 无 |
| 内容卡片标题 | `Manage how your information is used` | `privacy_choices.card.title` | 无 |
| 说明文案 1 | `Looply uses cookies and similar technologies to improve your experience, understand site usage, and support advertising.` | `privacy_choices.card.description_usage` | 无 |
| 说明文案 2 | `Depending on where you live, you may have the right to manage cookie preferences or opt out of the sale or sharing of personal information and targeted advertising.` | `privacy_choices.card.description_rights` | 无 |
| 管理入口 | `Manage Privacy Choices`＋右箭头 | `privacy_choices.action.manage` | 点击后进入个人中心 `Privacy & Data` 页面，并定位到 Privacy Choices 设置区域 |
| 辅助说明 | `To learn more about how Looply handles personal information, read our Privacy Policy.` | `privacy_choices.card.privacy_policy_prompt` | `Privacy Policy` 为可点击链接，进入隐私政策页面 |

### 2.4 交互规则

- Footer 中的 `Your Privacy Choices` 在当前页面打开说明页。
- 点击面包屑中的 `Home` 返回首页。
- `Manage Privacy Choices` 使用文字＋右箭头形式展示，不使用大面积按钮样式。
- 点击 `Manage Privacy Choices` 后，进入个人中心 `Privacy & Data` 页面，并自动定位到包含 `Cookie Preferences` 和 `Do Not Sell or Share My Personal Information` 的设置区域。
- 游客与登录用户的入口、页面内容和跳转行为一致。
- 点击 `Privacy Policy` 进入 Looply Privacy Policy 页面。
- 页面返回行为沿用 Web 端统一浏览器返回规则。

### 2.5 页面状态

该页面内容为固定说明内容，仅提供默认展示态。Header、Footer、面包屑及链接交互沿用对应 Web 终端的公共组件规则。

### 2.6 UI 关联

- Web Demo：`prototypes/homepage/looply-your-privacy-choices-web-demo-v0.1.html`
- 下游页面：个人中心 `Privacy & Data` 页面中的 `Cookie Preferences` 与 `Do Not Sell or Share My Personal Information` 区域。
- Demo 内的 `Privacy & Data` 仅为验证跳转及定位效果的简化目标页，不作为该下游页面的设计或开发依据；下游页面内容以其所属模块的正式设计为准。

### 2.7 文案归类

本页标题、说明文案及操作文案均属于静态 UI 文案，使用 Web 端统一 message package 及第 2.3 节定义的稳定文案标识管理，不进入翻译中心业务资源卡片。v0.1 以第 2.3 节的 `en-US` 文案为源文案；其他已启用语言及译文缺失兜底沿用 Web 端全局多语言规则，在最终总 PRD 中统一维护。

## 三、依赖与风险

- 依赖 PC Web 与 Mobile Web 的全局 Header、Footer 和面包屑组件。
- 依赖个人中心 `Privacy & Data` 页面同时支持游客和登录用户访问。
- 依赖 `Privacy & Data` 页面提供可稳定定位至 Privacy Choices 设置区域的页面位置。
- 依赖 Privacy Policy 页面提供有效访问地址。
- 页面英文隐私说明属于对外合规文案，上线前须由美国法务或合规负责人审核确认。
- 本页面仅负责说明和跳转；用户隐私选择的保存、生效及下游数据处理规则由 `Privacy & Data` 模块负责。

## 四、版本范围

v0.1 包含 PC Web 与 Mobile Web 的 `Your Privacy Choices` 说明页、Footer 入口以及向现有隐私设置区域和 Privacy Policy 的跳转。

## 五、附录

| 页面 | PC Web / Mobile Web Demo | 其他终端 |
|---|---|---|
| Your Privacy Choices 说明页 | `looply-your-privacy-choices-web-demo-v0.1.html`（响应式覆盖 PC Web 与 Mobile Web） | App 本期不涉及 |
