# Looply Footer 与关联页面 PRD v0.8

> 本稿汇总 Footer 既有入口规则及关联模块引用；文件配置后台执行《文件配置 PRD v1.0》，Contact Us 页面执行《Contact Us PRD v0.4》及本文第五章的国家信息增量。

## 一、范围

本 PRD 包含：

- PC Web Footer 各入口的跳转目标；
- Contact Us 页面规则引用及国家信息增量；
- Your Privacy Choices 页面需求。
- 法律文件、FAQ 与社媒账号的后台配置引用和消费职责边界。

About Looply 与 Authenticity 不纳入本稿当前接入范围。Shipping、Returns 及个人中心 `Privacy & Data` 的页面内部规则由各自模块负责。Newsletter 邮箱提交不属于页面跳转，不在本 PRD 中定义。

## 二、Footer 统一规则

- 本节适用于 PC Web Footer；品牌区展示 Logo 和品牌短句，无点击交互。
- Shop、Sell、Support 的普通入口使用默认清单，名称读取对应模块提供的本地化文案；站内路由模板按当前国家和语言拼接 locale。国家级目标差异由入口所属模块提供，文件配置后台不维护普通入口的名称、URL、启停或排序。
- Shop 入口与 PC 顶导的关联见 4.3 节；C1 入口的国家生效条件和隐藏范围统一执行[C1 Sell 多国家支持迭代 PRD v1.2 · 3.2、3.3 节](../../docs-C1-Sell/PRD/looply-C1-Sell-多国家支持-迭代PRD-v1.2.md)。
- Contact Us 页面及其中出售咨询的国家差异见第五章。

### 2.1 文件配置与消费边界

法律文件、FAQ 和社媒账号的录入、校验、发布、历史版本及生效内容输出统一见[文件配置 PRD v1.0](./looply-文件配置-PRD-v1.0.md)。本全量稿通过引用纳入其有效规则，不重复定义后台配置。

本次文件配置交付止于后台生效内容输出。Footer 国家／语言识别、入口可见性与回退，以及法律文件页、FAQ 页、首页的消费行为由其他已有前端需求负责；其职责及引用记录见[技术依赖 Checklist](./looply-文件配置-技术依赖Checklist.md)。

## 三、Footer 入口跳转清单

| 区域 | 入口 | 点击后跳转至 | 路径 / 地址 | 打开方式 |
|---|---|---|---|---|
| Support | My Account | 个人中心；游客展示未登录态，登录用户展示登录态 | 个人中心统一路由（正式路径由账户模块确认） | 当前标签页 |
| Support | Shipping | Shipping 页面 | `/shipping` | 当前标签页 |
| Support | Returns | Returns 页面 | `/returns` | 当前标签页 |
| Support | Contact Us | Contact Us 页面 | `/contact-us` | 当前标签页 |
| Social | Facebook | 当前国家配置的 Looply Facebook 账号 | 当前国家后台配置 | 新标签页 |
| Social | TikTok | 当前国家配置的 Looply TikTok 账号 | 当前国家后台配置 | 新标签页 |
| Social | Instagram | 当前国家配置的 Looply Instagram 账号 | 当前国家后台配置 | 新标签页 |
| Social | YouTube | 当前国家配置的 Looply YouTube 账号 | 当前国家后台配置 | 新标签页 |
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
| Facebook | 按当前国家读取 Footer 后台配置的有效账号地址 |
| TikTok | 按当前国家读取 Footer 后台配置的有效账号地址 |
| Instagram | 按当前国家读取 Footer 后台配置的有效账号地址 |
| YouTube | 按当前国家读取 Footer 后台配置的有效账号地址 |

### 4.2 需要先开发目标页面，再接入跳转

| 入口 | 目标页面开发依据 | Footer 接入条件 |
|---|---|---|
| Shipping | 对应模块提供的独立 PRD / UI | 页面可访问后接入 `/shipping` |
| Returns | 对应模块提供的独立 PRD / UI | 页面可访问后接入 `/returns` |
| Contact Us | Contact Us PRD v0.4 及本稿第五章国家信息增量 | 页面可访问后接入 `/contact-us` |
| Accessibility Statement | UI 设计；内容参考现有线上版本 | 自建页面可访问后接入 `/pages/accessibility-statement` |
| Privacy Policy | UI 设计；内容参考现有线上版本 | 自建页面可访问后接入 `/pages/privacy-policy` |
| Terms of Service | UI 设计；内容参考现有线上版本 | 自建页面可访问后接入 `/pages/terms-of-service` |
| Your Privacy Choices | 本 PRD 第六节及 UI 最终稿 | 自建页面及正式站内路由就绪后接入 |

### 4.3 依赖顶导清单确认

Shop 不单独开发 Footer 配置或目标页面。PC 顶导固定入口清单确认后，Footer 使用相同的入口名称、顺序和跳转路径进行接入。

## 五、Contact Us 页面与国家信息增量

### 5.1 页面规则引用

Contact Us 的页面布局、四类联系原因、收件邮箱、表单字段、校验、状态、多语言及 UI 输入统一执行[Contact Us PRD v0.4](../../docs-Contact-Us/PRD/looply-Contact-Us-PRD-v0.4.md)。本文只补充以下已确认的国家信息及地址规则；既有页面行为不在此维护第二份定义。

### 5.2 国家上下文与邮件提交增量

- 使用提交时全站已经确定的当前站点国家。带国家子目录的 URL 以 URL 国家为准；裸域沿用全站国家识别结果，不根据 IP、用户输入或邮箱再次判断。国家缺失或校验失败时阻止提交并提示刷新，不默认归属美国。
- 服务端生成并校验 `country_code`，使用 ISO 两位大写代码；用户不可编辑，前端传入值不能覆盖服务端判断。
- 每次提交关联 `country_code`、当前页面 `language`、所选联系原因对应的 `inquiry_type`、服务端 UTC `submitted_at` 和唯一 `contact_request_id`。联系原因及收件邮箱采用 Contact Us v0.4 第三章的四分类。
- 本次将 Contact Us v0.4 第五章的原邮件标题更新为 `Looply Contact Us | {submitted_at_utc} | {full_name} | {country_code}`；服务端清理姓名中的换行符和 `|`。邮件正文在 v0.4 所选联系原因和用户输入基础上增加国家、页面语言、Request ID 及 UTC 提交时间。
- 发送失败时保留输入，重试复用同一 `contact_request_id`；成功状态和清空四字段的结果按 Contact Us v0.4 第五章执行。
- 系统仅保留最小发送记录：Request ID、国家、联系原因、提交时间、接收邮箱、发送结果和错误码；姓名、用户邮箱和留言原文不进入普通技术日志。用户回复地址和原始输入处理执行 Contact Us v0.4。

### 5.3 国家地址

- 开发按 `country_code` 维护地址配置，地图图片、地址正文和地图定位链接作为同一组发布。
- 前台使用 5.2 节的当前站点国家读取地址；不根据 IP 重新判断，也不读取其他国家地址作为回退。
- 存在完整配置时展示地址卡片；点击地图图片或地址正文均打开该国家地图定位链接。任一配置缺失、链接无效或地图图片加载失败时隐藏整个地址卡片，表单和联系信息继续展示。
- 地址正文按对应国家的法定地址原文展示，不翻译；Address 标签为静态 UI 文案。变更随对应国家配置发布，其他国家不受影响。

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
| 文件配置后台 | 文件配置 PRD v1.0 及其 Demo | 按该 PRD 第六章验收；接入证据统一核对技术依赖 Checklist |
| Contact Us | Contact Us PRD v0.4 的 UI 输入及本稿第五章 | 页面、四分类邮件路由按 v0.4 验收；另核验国家标题、上下文、请求标识和国家地址增量 |
| Your Privacy Choices | Your Privacy Choices Web Demo v0.1；本 PRD 已确认英文文案 | UI 提供正式稿；补充正式站内路由；验证 Global Privacy Control 处理能力与文案一致 |
| Privacy & Data | 所属模块正式设计 | 支持游客 / 登录用户访问及稳定定位目标设置区域 |

## 八、验收标准

文件配置验收统一引用[文件配置 PRD v1.0 · 第六章](./looply-文件配置-PRD-v1.0.md#六验收与关联)，验收范围止于后台生效内容输出。Contact Us 页面和四分类提交按 v0.4 验收，另核验本文第五章国家信息增量；PC Footer 及其他消费页面由对应前端需求组织联合验收。
