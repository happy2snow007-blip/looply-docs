# Looply Footer 与关联页面 PRD v0.5

> 本版本以 `looply-CMS统一配置入口-antd-原型-v78.html` 为后台交互基线。普通 Footer 入口不提供独立后台配置；后台仅维护法律文件和 FAQ。法律文件使用法务语言版本和富文本内容，FAQ 上传英语富文本解析为列表；两类内容均执行格式、链接和版本冲突校验。

## 一、范围

本 PRD 包含：

- PC Web Footer 各入口的跳转目标；
- Contact Us 页面需求；
- Your Privacy Choices 页面需求。
- Footer 法律文件与 FAQ 的后台配置、版本同步和前台读取规则。

About Looply 与 Authenticity 的页面需求、路径及接入方式待定，当前版本不接入。Shipping、Returns 及个人中心 `Privacy & Data` 的页面内部规则由各自模块负责。Newsletter 邮箱提交不属于页面跳转，不在本 PRD 中定义。

## 二、Footer 统一规则

- Footer 的 `Shop`、`Sell`、`Support` 三个板块按国家读取内容。普通入口不提供逐条展示、启停或排序配置；C1 Sell 相关入口统一消费当前国家的 Sell 业务开关，具体国家生效条件以《C1 Sell 多国家支持迭代 PRD》为准。
- 以上三个板块的站内 URL 使用统一国家语言路径，前台根据当前国家和语言自动拼接 locale，例如 `/en-US/collections/new-arrivals`。后台默认保存不含 locale 的路由模板；如某国家存在不同目标，再配置国家级 URL 覆盖。
- `Sell` 板块及 Support 中的 `Seller FAQ`、法律区的 `Seller Agreement` 受当前国家 Sell 业务开关控制；未开放 Sell 的国家不展示这些入口。
- 法律文件内容按“国家 + 法务语言”维护。法务提供的版本直接发布，不使用大模型自动翻译；法律入口 URL 可按国家语言路径或国家级覆盖解析。
- FAQ 按国家维护英语原文；前台展示时接入翻译系统自动翻译，不在后台维护 FAQ 的多语言正文。
- Shop、Sell、Support 的入口名称属于静态/动态展示文案的翻译系统范围；后台只维护稳定入口标识，不重复录入译文。
- Shop、Sell、Support 不提供运营逐条编辑入口名称、URL 的后台页签；前台按当前国家、语言和 Sell 业务状态自动生成最终入口。Footer 后台仅保留法律文件和 FAQ 配置。
- 品牌区仅展示 Logo 和品牌短句，无点击交互。
- Footer 跳转规则适用于 PC Web；Mobile Web / App 不使用本节规则。

### 2.1 国家化读取与回退

1. 前台先确定当前国家和语言，再读取默认 Footer 入口清单及法律文件、FAQ等国家级内容配置。
2. Shop、Sell、Support 普通入口使用路由模板拼接当前 locale；入口名称从翻译系统读取，译文缺失时按翻译系统统一回退规则处理。
3. 国家差异通过国家级内容配置和全站业务开关处理，不复制整套入口清单，也不在 Footer 后台逐条配置入口展示或排序。
4. 国家未开放 Sell 时，Sell 板块以及所有 Sell 相关入口均不展示；C1 具体规则以《C1 Sell 多国家支持迭代 PRD》为准。
5. `Contact Us` 页面本身属于全站客服入口，不因 Sell 未开放而隐藏；页面根据当前国家的 Sell 业务开关动态隐藏 Sell 专属内容。

### 2.2 Footer 后台信息架构

Footer 后台使用页面顶部的国家作为配置范围，仅包含以下两个页签：

| 页签 | 维护对象 | 内容语言 | 前台使用位置 |
|---|---|---|---|
| 法律文件 | 开发预置的法律文件类型及其内容版本 | 按国家和法务语言维护 | 对应法律文件页面 |
| FAQ | 当前国家的 FAQ 英语原文 | 仅维护英语原文 | 独立 FAQ 页面；首页底部精选 FAQ |

切换国家后，列表、版本状态和可编辑内容全部切换至该国家的数据。法律文件页签额外选择法务语言；FAQ 不提供语言选择。

### 2.3 法律文件配置

#### 2.3.1 文件类型与列表

- 法律文件类型由开发预置稳定标识、固定名称和前台路由。运营后台不创建文件类型，也不修改文件名称。
- 新增法律文件类型时，开发先完成类型标识、固定名称和前台入口接入，再由运营在后台维护各国家和法务语言的内容版本。
- 列表展示：文件类型、后台版本、线上生效版本、同步状态和操作。
- 每个文件始终提供 `下载线上版`，下载当前线上生效版本的富文本文件；操作同时包括 `上传新版本`，线上版本高于后台版本时额外展示 `拉取最新版`。

#### 2.3.2 编辑字段

| 字段 | 控件 | 必填 | 规则 |
|---|---|---:|---|
| 文件名称 | 只读文本 | 是 | 展示开发预置名称，不可编辑 |
| 法务语言 | 单选下拉 | 是 | 选项来自当前国家支持的法务版本语言 |
| 版本号 | 单行输入 | 是 | 保存后形成新的内容版本；同一文件、国家和法务语言内不可重复 |
| 文件内容 | 富文本文件上传 | 是 | 上传法务确认的富文本文件，解析后生成新版本 |

后台不提供在线修改法律正文的能力。运营先下载当前线上最新版，在本地完成法务修订后上传富文本文件；系统解析并预览标题、正文段落、粗体、斜体、列表、引用、表格、分割线、链接和同页锚点，确认后以新版本保存。保存前可进入前台预览，按 PC 和 Mobile 内容容器检查格式和链接表现。

法律文件按“国家 + 文件类型 + 法务语言”读取生效版本。法务文本及其链接文字均不进入自动翻译；前台直接展示所选法务语言的已发布版本。

#### 2.3.3 链接规则

| 链接类型 | 保存规则 | 前台处理 |
|---|---|---|
| HTTPS 外部链接 | 校验为合法 `https://` URL 后保存 | 使用配置地址打开 |
| 站内相对路径 | 保存不含域名和 locale 的相对路径 | 根据当前国家和语言补齐 locale |
| 同页锚点 | 保存 `#锚点标识`；目标标识在正文内唯一 | 在当前法律文件页面定位 |

系统在粘贴、导入和保存时清洗富文本，移除脚本、`data:` URL、iframe 和其他可执行内容；发现非法链接时阻止保存并定位对应链接。链接显示文字属于正文的一部分，按法律文件的法务版本原样展示。

#### 2.3.4 版本同步与并发冲突

运营后台是法律文件内容的唯一事实来源。开发负责初始化首版内容；初始化完成后，前台读取运营后台发布版本。

1. 后台同时记录后台最新版本、线上生效版本、当前草稿的来源版本、更新时间和操作人。
2. 用户开始编辑时，草稿绑定当前线上生效版本作为来源版本。
3. 打开列表、进入编辑和点击保存时均比对线上版本与来源版本。
4. 版本一致时允许保存新版本；保存成功后保留历史版本和操作记录。
5. 线上版本更新且后台没有草稿时，系统拉取线上版本并生成“外部同步”记录。
6. 线上版本更新且后台已有草稿时，后台保留草稿并标记 `线上有新版本`，禁止旧草稿覆盖；用户先查看差异并拉取最新版，再基于最新版重新编辑。
7. 应急情况下开发直接修改线上内容时，线上必须返回可比较的版本标识；后台发现差异后按第 5、6 条处理。

法律文件同步状态枚举如下：

| 枚举值 | 含义 | 触发时机 | 可执行操作 |
|---|---|---|---|
| 生效中 | 后台最新发布版本与线上版本一致 | 版本比对一致 | 上传新版本、预览 |
| 草稿 | 后台存在未发布的新版本，来源版本仍为线上最新版 | 保存草稿后 | 继续编辑、预览、发布 |
| 线上有新版本 | 线上版本高于草稿来源版本 | 打开列表、进入编辑或保存时发现冲突 | 查看差异、拉取最新版 |
| 同步失败 | 线上版本查询或内容拉取失败 | 同步请求失败 | 重试同步；保留现有内容和草稿 |

### 2.4 FAQ 配置

#### 2.4.1 导入与解析

FAQ 按国家维护英语原文。运营先从后台下载当前国家的最新版富文本，在该文件基础上修改，再上传 `.docx`、`.html` 或 `.rtf` 文件。

固定模板中，问题标题样式识别为问题，从该标题后的正文到下一个问题标题之前识别为答案。答案保留段落、粗体、斜体、列表和链接。上传后先展示解析结果、问题数量和链接数量；用户选择 `覆盖当前国家 FAQ` 或 `追加到当前列表` 后保存。

上传文件携带来源版本号；解析和保存时均比对当前线上版本。来源版本落后时阻止覆盖或追加，并提示重新下载最新版。解析失败时保留当前 FAQ，按问题顺序提示具体错误，例如问题缺少答案、标题层级无法识别或链接协议非法。

FAQ 文本进入翻译系统；链接 URL 不翻译。站内相对路径由前台根据当前国家和语言补齐 locale。FAQ 使用与法律文件相同的链接类型、安全清洗和前台预览规则。

#### 2.4.2 解析后列表

每条 FAQ 展示问题、答案摘要、启用状态、首页精选状态和操作。列表支持拖拽调整独立 FAQ 页面的展示顺序，并支持启用、停用和删除。

- 独立 FAQ 页面展示当前国家所有启用 FAQ，按列表顺序排列。
- 首页底部展示当前国家中“启用且首页精选”的 FAQ。
- `首页精选` 使用独立开关；FAQ 停用时系统同步关闭其首页精选状态。
- 首页精选从同一 FAQ 列表中过滤生成，沿用独立 FAQ 页面的列表顺序。
- 删除前显示确认信息；确认后从独立 FAQ 页面和首页精选中同时移除。已发布版本保留删除前的历史记录。

FAQ 状态枚举如下：

| 枚举值 | 含义 | 触发时机 | 前台结果 |
|---|---|---|---|
| 启用 | FAQ 可被前台读取 | 导入后启用或人工启用 | 展示于独立 FAQ 页面；首页精选开启时同时展示于首页 |
| 停用 | FAQ 暂停前台展示 | 人工停用 | 独立 FAQ 页面和首页均不展示 |

### 2.5 异常与权限

| 场景 | 后台处理 |
|---|---|
| 线上版本查询失败 | 显示 `同步失败`，保留列表和草稿；禁用发布，提供重试 |
| 保存时发生版本冲突 | 阻止保存，展示后台版本、线上版本和差异入口 |
| 富文本包含非法内容或链接 | 阻止保存，定位问题节点并提示允许的格式或协议 |
| FAQ 文件解析失败 | 不改变现有 FAQ，展示逐项错误并允许重新上传 |
| 当前用户无编辑权限 | 页面只读，隐藏保存、导入、启停、删除和排序操作 |
| 目标数据已被删除或文件类型不存在 | 关闭编辑抽屉，刷新列表并提示数据已更新 |
| 网络异常 | 保留当前输入和已选文件，提供重试；不得将失败操作显示为已保存 |

### 2.6 数据来源与多语言分类

| 内容 | 数据来源 | 多语言分类 | 前台处理 |
|---|---|---|---|
| 法律文件固定名称 | 开发预置文件类型 | 静态 UI 文案 | 使用稳定 message key 展示 |
| 法律文件正文及正文内链接文字 | 法务提供的对应语言版本 | 不翻译 | 按国家和法务语言读取已发布版本 |
| FAQ 问题和答案 | 当前国家上传的英语富文本 | 动态业务内容 | 英语原文进入翻译系统；译文缺失按翻译系统统一回退规则 |
| 法律文件与 FAQ 链接 URL | 富文本内容 | 不翻译 | 外链原样使用；站内相对路径补齐 locale；锚点当前页定位 |
| 后台标签、按钮、校验和状态提示 | 前后端 message package | 静态 UI 文案 | 按运营后台语言展示 |

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

### 5.3.1 Sell 业务国家差异

Contact Us 页面按当前国家读取 Sell 业务状态：

- 当前国家支持 Sell 时，联系主题下拉框展示 `Selling to Looply`，联系信息区域展示 `For selling inquiries: sell@looply.com`；提交 Sell 咨询时按 Sell 咨询路由处理。
- 当前国家不支持 Sell 时，联系主题下拉框不展示 `Selling to Looply`，联系信息区域不展示 `For selling inquiries: sell@looply.com`；页面仅保留普通购物咨询和 `service@looply.com`。
- 页面标题、说明、地址、普通购物咨询邮箱、Email、Message 和 `Send` 按钮不受 Sell 状态影响。
- 前端隐藏不替代服务端校验。服务端根据当前国家 Sell 状态校验提交内容；未开放国家提交 Sell 类型时拒绝该请求并返回普通客服入口提示，不得将请求发送至 Sell 邮箱。

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
| Footer 后台 · 法律文件 | CMS 统一配置入口 antd 原型 v78；本 PRD 2.2、2.3、2.5、2.6 | 开发预置文件类型；内容服务提供版本查询、拉取、差异和发布能力；完成富文本安全清洗与 PC/Mobile 预览 |
| Footer 后台 · FAQ | CMS 统一配置入口 antd 原型 v78；本 PRD 2.2、2.4、2.5、2.6 | 提供 FAQ 富文本模板、版本标识、解析服务、翻译资源接入及首页精选读取接口 |
| Contact Us | Figma《Looply v1.0》及 Mobile Contact Us 状态节点；本 PRD 第五节 | Figma 成功态同步为三字段清空；上线前复核客服邮箱与响应时效，并完成服务端邮件发送能力 |
| About Looply | 需求待定 | PRD、UI、路径及接入方式确认后再发布 |
| Authenticity | 需求待定 | PRD、UI、路径及接入方式确认后再发布 |
| Your Privacy Choices | Your Privacy Choices Web Demo v0.1；本 PRD 已确认英文文案 | UI 提供正式稿；补充正式站内路由；验证 Global Privacy Control 处理能力与文案一致 |
| Privacy & Data | 所属模块正式设计 | 支持游客 / 登录用户访问及稳定定位目标设置区域 |

## 八、验收标准

### 8.1 法律文件

1. 后台仅展示开发预置的法律文件类型，运营不能新增或修改文件名称。
2. 切换国家和法务语言后，列表和编辑内容读取对应范围的数据。
3. 富文本格式、合法链接和同页锚点在后台预览及 PC/Mobile 前台保持一致。
4. 脚本、`data:` URL、iframe、非法协议和无目标锚点不能通过保存校验。
5. 后台版本与线上版本一致时可以保存新版本，并保留历史版本、时间和操作人。
6. 线上版本较新且存在后台草稿时，旧草稿不能覆盖线上版本；列表与编辑抽屉均显示版本冲突和拉取入口。
7. 同步失败时保留现有列表与草稿，发布不可用，重试成功后恢复正常。
8. 前台按国家、文件类型和法务语言读取生效版本，正文和链接文字不经过自动翻译。

### 8.2 FAQ

1. 后台可下载当前国家最新版 FAQ 富文本，并识别上传文件的来源版本。
2. 模板内每个问题及答案被解析为独立 FAQ；段落、强调、列表及合法链接保持完整。
3. 解析失败、非法链接或来源版本落后时不改变当前 FAQ，并显示可定位的错误。
4. 覆盖导入替换当前国家 FAQ；追加导入保留现有 FAQ 并增加新条目。
5. FAQ 支持拖拽排序、启用、停用、删除和首页精选设置；停用时同步取消首页精选。
6. 独立 FAQ 页面仅展示当前国家启用项；首页仅展示启用且首页精选的项目，两处均沿用后台 FAQ 列表顺序。
7. FAQ 英语文本进入翻译系统；链接 URL 不翻译，站内相对路径按当前国家和语言补齐 locale。
8. 无编辑权限用户只能查看列表和版本状态，不能保存、导入、启停、删除或排序。
