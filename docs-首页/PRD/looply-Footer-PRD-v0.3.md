# Looply Footer 与关联页面 PRD v0.3

## 一、范围

本 PRD 包含：

- PC Web Footer 各入口的跳转目标；
- Your Privacy Choices 页面需求。

About Looply 与 Authenticity 的页面需求、路径及接入方式待定，当前版本不接入。Contact Us、Shipping、Returns 及个人中心 `Privacy & Data` 的页面内部规则由各自模块负责。Newsletter 邮箱提交不属于页面跳转，不在本 PRD 中定义。

## 二、Footer 统一规则

- Shop 与 PC 顶导使用同一份固定入口清单，不接运营配置；具体名称、顺序和跳转路径待确认。
- 品牌区仅展示 Logo 和品牌短句，无点击交互。
- Footer 跳转规则适用于 PC Web；Mobile Web / App 不使用本节规则。

## 三、Footer 入口跳转清单

| 区域 | 入口 | 点击后跳转至 | 路径 / 地址 | 打开方式 |
|---|---|---|---|---|
| Support | My Account | 个人中心；游客展示未登录态，登录用户展示登录态 | 个人中心统一路由（正式路径由账户模块确认） | 当前标签页 |
| Support | Shipping | Shipping 页面 | `/shipping` | 当前标签页 |
| Support | Returns | Returns 页面 | `/returns` | 当前标签页 |
| Support | Contact Us | Contact Us 页面 | `/contact-us` | 当前标签页 |
| About | About Looply | 待定（需求未确认） | 待定 | 待定 |
| About | Authenticity | 待定（需求未确认） | 待定 | 待定 |
| Social | Facebook | Looply Facebook | `https://www.facebook.com/share/1CEdkGST1V/?mibextid=wwXIfr` | 新标签页 |
| Social | TikTok | Looply TikTok | `https://www.tiktok.com/@looply_luxury` | 新标签页 |
| Social | Instagram | Looply Instagram | `https://www.instagram.com/looply_luxury/` | 新标签页 |
| Social | YouTube | Looply YouTube | `https://www.youtube.com/@looply_luxury` | 新标签页 |
| Legal | Accessibility Statement | Looply 自建 Accessibility Statement 页面 | `/pages/accessibility-statement` | 当前标签页 |
| Legal | Privacy Policy | Looply 自建 Privacy Policy 页面 | `/pages/privacy-policy` | 当前标签页 |
| Legal | Your Privacy Choices | Your Privacy Choices 独立说明页 | 正式站内路由待确认 | 当前标签页 |
| Legal | Terms of Service | Looply 自建 Terms of Service 页面 | `/pages/terms-of-service` | 当前标签页 |

Accessibility Statement、Privacy Policy、Terms of Service 均由 Looply 自行开发页面，最终 UI 由 UI 设计提供。页面内容分别参考现有线上版本：

- Accessibility Statement：`https://looply.com/pages/accessibility-statement`
- Privacy Policy：`https://looply.com/pages/privacy-policy`
- Terms of Service：`https://looply.com/pages/terms-of-service`

## 四、开发实施分类

### 4.1 已有目标，可直接接入跳转

| 入口 | 开发处理 |
|---|---|
| My Account | 接入现有个人中心能力；打开统一个人中心页面，并按当前登录状态展示未登录态或登录态 |
| Facebook | 直接接入已提供的外部地址 |
| TikTok | 直接接入已提供的外部地址 |
| Instagram | 直接接入已提供的外部地址 |
| YouTube | 直接接入已提供的外部地址 |

### 4.2 需要先开发目标页面，再接入跳转

| 入口 | 目标页面开发依据 | Footer 接入条件 |
|---|---|---|
| Shipping | 对应模块提供的独立 PRD / UI | 页面可访问后接入 `/shipping` |
| Returns | 对应模块提供的独立 PRD / UI | 页面可访问后接入 `/returns` |
| Contact Us | 独立《Looply Contact Us PRD v0.1》及对应 UI | 页面可访问后接入 `/contact-us` |
| About Looply | 待定（需求未确认） | PRD、UI、路径及接入方式确认后再接入 |
| Authenticity | 待定（需求未确认） | PRD、UI、路径及接入方式确认后再接入 |
| Accessibility Statement | UI 设计；内容参考现有线上版本 | 自建页面可访问后接入 `/pages/accessibility-statement` |
| Privacy Policy | UI 设计；内容参考现有线上版本 | 自建页面可访问后接入 `/pages/privacy-policy` |
| Terms of Service | UI 设计；内容参考现有线上版本 | 自建页面可访问后接入 `/pages/terms-of-service` |
| Your Privacy Choices | 本 PRD 第五节及 UI 最终稿 | 自建页面及正式站内路由就绪后接入 |

### 4.3 依赖顶导清单确认

Shop 不单独开发 Footer 配置或目标页面。PC 顶导固定入口清单确认后，Footer 使用相同的入口名称、顺序和跳转路径进行接入。

## 五、Your Privacy Choices 页面

### 5.1 目标、角色与范围

页面用于说明 Looply 对 Cookie、类似技术及广告相关信息的使用，并引导用户进入个人中心 `Privacy & Data` 管理隐私选择。

- 用户角色：游客、登录用户；两类用户使用相同页面和跳转路径。
- 终端范围：PC Web 与 Mobile Web；App 不在本期范围。
- 页面流转：`Footer · Your Privacy Choices` → `Your Privacy Choices 说明页` → `Manage Privacy Choices` → `个人中心 · Privacy & Data · Privacy Choices 设置区域`。
- 说明页正式站内路由待确认。

### 5.2 页面布局

- 页面复用对应 Web 终端的公共 Header 和 Footer。
- PC Web：左侧展示页面标题和引导语，右侧内容卡片展示说明文案、管理入口和 Privacy Policy 入口。
- Mobile Web：标题、引导语和内容卡片按顺序纵向展示，内容与交互不变。
- 页面顶部展示面包屑：`Home / Your Privacy Choices`。

### 5.3 页面元素

| 页面元素 | 展示内容 | 静态文案标识 | 交互 |
|---|---|---|---|
| 页面标题 | `Your Privacy Choices` | `privacy_choices.page.title` | 无 |
| 引导语 | `You have choices about how Looply uses certain information.` | `privacy_choices.page.intro` | 无 |
| 内容卡片标题 | `Manage how your information is used` | `privacy_choices.card.title` | 无 |
| 隐私说明正文 | 使用下方已确认英文文案，共四段 | `privacy_choices.card.description_1` 至 `privacy_choices.card.description_4` | 无 |
| 管理提示 | `Manage your choices at any time in Privacy & Data.` | `privacy_choices.card.manage_prompt` | 无 |
| 管理入口 | `Manage Privacy Choices`＋右箭头 | `privacy_choices.action.manage` | 进入个人中心 `Privacy & Data` 并定位到 Privacy Choices 设置区域 |
| 辅助说明 | `To learn more about how Looply handles personal information, read our Privacy Policy.` | `privacy_choices.card.privacy_policy_prompt` | `Privacy Policy` 进入 `/pages/privacy-policy` |

已确认英文文案如下，开发按段落顺序展示，不改写、不合并：

As described in our Privacy Policy, we collect personal information from your interactions with us and our website, including through cookies and similar technologies. We may also share this personal information with third parties, including advertising partners. We do this in order to show you ads on other websites that are more relevant to your interests and for other reasons outlined in our privacy policy.

Sharing of personal information for targeted advertising based on your interaction on different websites may be considered "sales", "sharing", or "targeted advertising" under certain U.S. state privacy laws. Depending on where you live, you may have the right to opt out of these activities. If you would like to exercise this opt-out right, please follow the instructions below.

If you visit our website with the Global Privacy Control opt-out preference signal enabled, depending on where you are, we will treat this as a request to opt-out of activity that may be considered a “sale” or “sharing” of personal information or other uses that may be considered targeted advertising for the device and browser you used to visit our website.

**To opt out of the "sale" or "sharing" of your personal information collected using cookies and other device-based identifiers as described above, you must be browsing from one of the applicable US states referred to above.**

### 5.4 交互与状态

- Footer 入口在当前标签页打开说明页。
- 面包屑 `Home` 返回首页。
- `Manage Privacy Choices` 使用文字＋右箭头形式，不使用大面积按钮。
- 点击 `Manage Privacy Choices` 后进入个人中心 `Privacy & Data`，并自动定位至同时包含 `Cookie Preferences` 和 `Do Not Sell or Share My Personal Information` 的设置区域。
- 点击 `Privacy Policy` 在当前标签页进入 `/pages/privacy-policy`。
- 页面内容固定，仅提供默认展示态；公共 Header、Footer、面包屑及链接状态沿用 Web 公共组件规则。

### 5.5 边界、依赖与多语言

- 本页仅负责说明和跳转；隐私选择的保存、生效及数据处理由 `Privacy & Data` 模块负责。
- 依赖 `Privacy & Data` 同时支持游客和登录用户访问，并提供稳定定位到目标设置区域的能力。
- 文案已确认；上线前须验证网站能够按第三段承诺识别并处理 Global Privacy Control 信号，且处理范围与适用州规则一致。
- 页面文案均为静态 UI 文案，使用 `privacy_choices.*` 稳定标识和 Web 统一 message package，不进入翻译中心业务资源卡片。
- 当前 Web Demo：`prototypes/homepage/looply-your-privacy-choices-web-demo-v0.1.html`；其中简化的 `Privacy & Data` 仅验证跳转与定位，不作为下游页面开发依据。

## 六、UI 与发布依赖汇总

| 页面 / 模块 | 当前依据 | 发布前要求 |
|---|---|---|
| Footer | 用户提供的 PC Footer 截图及本 PRD 跳转规则 | UI 提供正式 Footer 样式 |
| About Looply | 需求待定 | PRD、UI、路径及接入方式确认后再发布 |
| Authenticity | 需求待定 | PRD、UI、路径及接入方式确认后再发布 |
| Your Privacy Choices | Your Privacy Choices Web Demo v0.1；本 PRD 已确认英文文案 | UI 提供正式稿；补充正式站内路由；验证 Global Privacy Control 处理能力与文案一致 |
| Privacy & Data | 所属模块正式设计 | 支持游客 / 登录用户访问及稳定定位目标设置区域 |
