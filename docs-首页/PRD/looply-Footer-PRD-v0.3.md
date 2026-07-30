# Looply Footer 与关联页面 PRD v0.3

## 一、范围

本 PRD 包含：

- PC Web Footer 各入口的跳转目标；
- Contact Us 页面需求；
- Your Privacy Choices 页面需求。

About Looply 与 Authenticity 的页面需求、路径及接入方式待定，当前版本不接入。Shipping、Returns 及个人中心 `Privacy & Data` 的页面内部规则由各自模块负责。Newsletter 邮箱提交不属于页面跳转，不在本 PRD 中定义。

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
| Contact Us | 本 PRD 第五节及 Contact Us 对应 UI | 页面可访问后接入 `/contact-us` |
| About Looply | 待定（需求未确认） | PRD、UI、路径及接入方式确认后再接入 |
| Authenticity | 待定（需求未确认） | PRD、UI、路径及接入方式确认后再接入 |
| Accessibility Statement | UI 设计；内容参考现有线上版本 | 自建页面可访问后接入 `/pages/accessibility-statement` |
| Privacy Policy | UI 设计；内容参考现有线上版本 | 自建页面可访问后接入 `/pages/privacy-policy` |
| Terms of Service | UI 设计；内容参考现有线上版本 | 自建页面可访问后接入 `/pages/terms-of-service` |
| Your Privacy Choices | 本 PRD 第六节及 UI 最终稿 | 自建页面及正式站内路由就绪后接入 |

### 4.3 依赖顶导清单确认

Shop 不单独开发 Footer 配置或目标页面。PC 顶导固定入口清单确认后，Footer 使用相同的入口名称、顺序和跳转路径进行接入。

## 五、Contact Us 页面

### 5.1 页面目标、角色与入口

Contact Us 为游客和登录用户提供统一的客服联系方式与留言提交能力，页面不要求登录。

- PC Web：`首页 Footer → Contact Us`，当前标签页进入 `/contact-us`。
- Mobile Web / App：游客态和登录态的个人中心均展示 Contact Us 入口；点击后直接进入页面，不触发登录或注册。
- 页面用于咨询订单、退货、商品和平台服务问题，并展示客服邮箱和响应时效。

### 5.2 页面布局

| 终端 | 页面框架与内容顺序 |
|---|---|
| PC Web | 使用 PC Web 公共 Header 与 Footer；展示形式以 Figma《Looply v1.0》为准；内容依次为页面标题与引导语、联系表单、Email、Email Response Time |
| Mobile Web / App | 使用 Mobile 公共页面框架，顶部提供返回操作；展示形式以 Figma 指定节点为准；内容按单列依次展示页面标题与引导语、联系表单、Email、Email Response Time |

Mobile 与 PC 使用相同字段、联系信息和提交规则。

### 5.3 页面元素

| 区域 | 元素 | 英文文案 / 内容 | 交互 |
|---|---|---|---|
| 页面标题 | 标题 | `Contact us` | 无 |
| 联系表单 | 姓名 | `Full Name` | 单行输入，必填 |
| 联系表单 | 邮箱 | `Email` | 邮箱输入，必填 |
| 联系表单 | 留言 | `Message` | 多行输入，必填 |
| 联系表单 | 提交按钮 | `Send` | 提交表单 |
| 联系信息 | Email | `service@looply.com` | 点击后调用系统邮件应用 |
| 帮助说明 | Email Response Time | `We generally respond to customer inquiries within 1–2 business days.` | 无 |

### 5.4 字段初始值与校验

| 字段 | 必填 | 长度 / 格式 | 校验时机 | 错误反馈 |
|---|---|---|---|---|
| Full Name | 是 | 去除首尾空格后 1–100 个字符 | 失焦、点击 Send | 为空提示 `Enter your full name.`；超长提示 `Full name must be 100 characters or fewer.` |
| Email | 是 | 去除首尾空格后符合基础邮箱格式，最多 254 个字符 | 失焦、点击 Send | 为空提示 `Enter your email.`；格式错误提示 `Incorrect email` |
| Message | 是 | 去除首尾空格后 1–2,000 个字符 | 失焦、点击 Send | 为空提示 `Enter your message.`；超长提示 `Message must be 2,000 characters or fewer.` |

- 游客进入页面时，三个字段均为空。
- 登录用户进入页面时，Full Name 和 Email 自动带入账户姓名和邮箱，Message 为空；账户任一字段为空时，对应输入框保持空白。
- 登录用户可以修改自动带入的姓名和邮箱；修改值只用于本次 Contact Us 提交和客服回复，不更新账户资料。
- 任一字段校验失败时，错误显示在对应字段附近，保留其他已填内容且不提交。
- 用户原始输入不翻译、不改写。

### 5.5 提交流程与数据处理

1. 用户填写 Full Name、Email 和 Message，点击 `Send`。
2. 页面校验三个必填字段；校验通过后进入提交中状态，禁止重复提交。
3. Looply 服务端将三个字段发送至 `service@looply.com`；用户浏览器不直接发送邮件。
4. 仅在邮件服务确认已受理发送请求后，页面显示成功提示。
5. 提交成功后不跳转；游客和登录用户均清空 Full Name、Email、Message，并显示成功 Toast。
6. 客服后续从 `service@looply.com` 人工回复用户填写的 Email。

邮件是当前版本唯一业务记录。Looply 不建立独立的 Contact Us 业务记录或用户侧咨询历史，不向用户自动发送确认邮件；必要技术日志不记录 Full Name、Email 或 Message 原文。

当前版本不接入 hCaptcha、Google reCAPTCHA 或其他 CAPTCHA，也不展示第三方验证码声明。

### 5.6 页面状态与异常

| 状态 | 触发条件 | 页面表现 | 可用操作 |
|---|---|---|---|
| 默认态 | 页面正常打开 | 游客三个字段为空；登录用户自动带入 Full Name 和 Email；完整联系信息正常展示 | 填写、提交、点击客服邮箱 |
| 字段错误态 | 输入未通过校验 | 对应字段显示错误，保留全部已填内容 | 修改后重新提交 |
| 提交中 | 字段校验通过，正在提交 | `Send` 置灰不可点击，字段保留并暂不可再次提交 | 等待结果 |
| 提交成功 | 邮件服务确认已受理发送请求 | 页面保持当前位置，清空 Full Name、Email、Message，显示 `Thanks for contacting us. We’ll get back to you as soon as possible.` | 可重新填写 |
| 提交失败 | 网络、邮件服务或系统异常 | 显示 `Submit failed, please try again.`，保留三个字段 | 点击 Send 重试 |
| 离开确认 | 当前字段值与页面初始值不同，用户返回或发起站内跳转 | 显示 `Leave without sending?` 弹窗 | `Stay` 保留内容；`Leave` 放弃内容并继续离开 |

局部异常按模块降级：表单加载失败时 Email 与 Email Response Time 继续展示，表单区域提供 Retry；联系信息加载失败时表单继续可用，联系信息区域提供 Retry。登录用户账户信息读取失败时，Full Name 和 Email 保持空白，由用户手动填写。

成功 Toast 持续展示 4 秒后自动消失；清空后的空白字段作为新的页面初始值，用户离开时不触发未提交内容确认。失败提示不清空字段。

关闭浏览器、App 被系统终止或跨设备访问时，不保存、不恢复未提交内容。

### 5.7 多语言、埋点与发布依赖

- 页面标题、字段标签、按钮、校验提示、状态提示和联系信息标签属于静态 UI 文案，使用稳定 message key 管理；用户输入属于原始内容，不翻译。
- 埋点覆盖页面展示、提交点击、校验失败、提交结果及邮箱点击；不得记录 Full Name、Email 或 Message 原文。
- 客服邮箱和响应时效上线前由客服与运营复核。
- UI 设计文件：[Looply v1.0](https://www.figma.com/design/rLK7XCdVvYqEHQHd7WjOkk/Looply-v1.0?t=VQDfvElDOm7kMhSj-0)。
- Mobile Contact Us 状态稿：[Looply v1.0 · node 6772:3636](https://www.figma.com/design/rLK7XCdVvYqEHQHd7WjOkk/Looply-v1.0?node-id=6772-3636&t=pVFMkiNnle3oB3B1-0)，覆盖默认、邮箱校验错误、填写完成、提交成功和提交失败状态。

## 六、Your Privacy Choices 页面

### 6.1 目标、角色与范围

页面用于说明 Looply 对 Cookie、类似技术及广告相关信息的使用，并引导用户进入个人中心 `Privacy & Data` 管理隐私选择。

- 用户角色：游客、登录用户；两类用户使用相同页面和跳转路径。
- 终端范围：PC Web 与 Mobile Web；App 不在本期范围。
- 页面流转：`Footer · Your Privacy Choices` → `Your Privacy Choices 说明页` → `Manage Privacy Choices` → `个人中心 · Privacy & Data · Privacy Choices 设置区域`。
- 说明页正式站内路由待确认。

### 6.2 页面布局

- 页面复用对应 Web 终端的公共 Header 和 Footer。
- PC Web：左侧展示页面标题和引导语，右侧内容卡片展示说明文案、管理入口和 Privacy Policy 入口。
- Mobile Web：标题、引导语和内容卡片按顺序纵向展示，内容与交互不变。
- 页面顶部展示面包屑：`Home / Your Privacy Choices`。

### 6.3 页面元素

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

### 6.4 交互与状态

- Footer 入口在当前标签页打开说明页。
- 面包屑 `Home` 返回首页。
- `Manage Privacy Choices` 使用文字＋右箭头形式，不使用大面积按钮。
- 点击 `Manage Privacy Choices` 后进入个人中心 `Privacy & Data`，并自动定位至同时包含 `Cookie Preferences` 和 `Do Not Sell or Share My Personal Information` 的设置区域。
- 点击 `Privacy Policy` 在当前标签页进入 `/pages/privacy-policy`。
- 页面内容固定，仅提供默认展示态；公共 Header、Footer、面包屑及链接状态沿用 Web 公共组件规则。

### 6.5 边界、依赖与多语言

- 本页仅负责说明和跳转；隐私选择的保存、生效及数据处理由 `Privacy & Data` 模块负责。
- 依赖 `Privacy & Data` 同时支持游客和登录用户访问，并提供稳定定位到目标设置区域的能力。
- 文案已确认；上线前须验证网站能够按第三段承诺识别并处理 Global Privacy Control 信号，且处理范围与适用州规则一致。
- 页面文案均为静态 UI 文案，使用 `privacy_choices.*` 稳定标识和 Web 统一 message package，不进入翻译中心业务资源卡片。
- 当前 Web Demo：`prototypes/homepage/looply-your-privacy-choices-web-demo-v0.1.html`；其中简化的 `Privacy & Data` 仅验证跳转与定位，不作为下游页面开发依据。

## 七、UI 与发布依赖汇总

| 页面 / 模块 | 当前依据 | 发布前要求 |
|---|---|---|
| Footer | 用户提供的 PC Footer 截图及本 PRD 跳转规则 | UI 提供正式 Footer 样式 |
| Contact Us | Figma《Looply v1.0》及 Mobile Contact Us 状态节点；本 PRD 第五节 | Figma 成功态同步为三字段清空；上线前复核客服邮箱与响应时效，并完成服务端邮件发送能力 |
| About Looply | 需求待定 | PRD、UI、路径及接入方式确认后再发布 |
| Authenticity | 需求待定 | PRD、UI、路径及接入方式确认后再发布 |
| Your Privacy Choices | Your Privacy Choices Web Demo v0.1；本 PRD 已确认英文文案 | UI 提供正式稿；补充正式站内路由；验证 Global Privacy Control 处理能力与文案一致 |
| Privacy & Data | 所属模块正式设计 | 支持游客 / 登录用户访问及稳定定位目标设置区域 |
