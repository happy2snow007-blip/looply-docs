# Looply 用户系统 · 功能说明文档

> 版本：V3.0 MVP
> 更新日期：2026-06-09
> 文档负责人：产品部
> 状态：初稿

---

## 一、文档说明

### 1.1 文档目的

本文档为 Looply 海外电商平台用户系统 MVP 阶段的详细功能说明，作为设计、研发、测试的交付依据和验收标准。

### 1.2 适用范围

- 本期 MVP 覆盖：注册、登录、退出、密码管理、会话管理、安全风控六个模块
- 适用终端：Web PC 端、APP 移动端
- 目标用户：外部用户（买家）
- **范围说明**：本期 MVP 仅覆盖 C 端用户（买家）的注册登录流程。运营后台、商家后台的登录与权限体系为后续规划，架构预留说明见 8.3

### 1.3 信源分工

| 内容类型 | 信源 | 说明 |
|----------|------|------|
| 静态文案 | 设计稿（Figma） | 页面标题、副标题、按钮文字、placeholder、提示语等以设计稿为准，PRD 不重复描述 |
| 动态错误提示 | PRD | 校验失败、异常场景的错误文案以 PRD 为准，设计稿仅出示意状态 |
| 交互逻辑 | PRD | 操作流程、状态流转、校验规则、异常处理 |
| 视觉样式 | 设计稿（Figma） | 布局、颜色、字号、间距等 |

### 1.4 术语说明

| 术语 | 说明 |
|------|------|
| OAuth 2.0 | 开放授权协议，用于第三方登录 |
| JWT | JSON Web Token，用于无状态身份鉴权 |
| access_token | 短期访问令牌，用于接口鉴权，不落库 |
| refresh_token | 长期刷新令牌，用于换取新的 access_token，存储在服务端 |
| ToS | Terms of Service，服务条款 |
| Remember Me | 登录态保持，免密登录 |
| Provider | 第三方登录服务商（Google / Apple / Facebook） |
| Identifier-First | 统一入口模式，先识别用户身份再决定注册/登录路径（预留） |

### 1.5 全局页面流转

> 仅展示页面之间的跳转关系（从哪到哪），不含业务逻辑判断。完整业务逻辑见系统流程图。

```
首页
├─→ 登录页（Login）
│    ├─→ 注册页（Register）←→ 登录页
│    ├─→ 忘记密码页（ForgotPassword）
│    │    └─→ 验证码页 → 重置密码页（ResetPassword）→ 登录页（回访态 Login-Remembered）
│    ├─→ 验证码页（VerifyCode）→ 风控拦截弹窗（RiskBlocked，触发时）
│    ├─→ 三方登录（OAuth 授权页）→ 首页（成功）/ 邮箱补充页（OAuthEmailSupplement，Facebook 未返回邮箱时）/ 登录页（失败）
│    └─→ 首页（登录成功）
├─→ 回访登录页（Login-Remembered）
│    └─→ 登录页（切换账号）/ 首页（登录成功）
├─→ 服务条款页（TermsOfService）
├─→ 隐私政策页（PrivacyPolicy）
└─→ 协议版本更新弹窗（ConsentUpdateModal，已登录用户触发时）
     ├─→ 当前页面（同意后继续）
     └─→ 登录页（拒绝后退出）

注册页
├─→ 验证码页 → 首页（注册成功）
└─→ 服务条款页 / 隐私政策页

邮箱补充页（OAuthEmailSupplement）
└─→ 验证码页 → 首页（注册成功）

已登录状态
├─→ 密码修改页（ChangePassword）→ 登录页（修改成功后自动跳转）
└─→ 退出确认弹窗（LogoutModal）→ 首页（确认退出）
```

---

## 二、注册模块

### 2.1 模块概述

- **模块目标**：完成新用户账户创建，提升首访转化率
- **优先级**：P0
- **入口**：首页「Sign Up」按钮、营销落地页引导
- **说明**：首页为登录/注册的统一入口，页面顶部提供「Sign In」和「Sign Up」按钮。首页设计稿见独立文件：PC 端 looply-home-PC.pen / APP 端 looply-home-APP.pen（位于「海外业务首页/UI/」目录）

### 2.2 邮箱注册

#### 功能描述

用户通过邮箱地址和密码创建 Looply 账号。

#### 前置条件

- 用户未登录状态
- 用户尚未拥有 Looply 账号

#### 页面布局（PC 端）

- 左侧：品牌展示区（660px 宽），全屏背景图 + 品牌 Logo + 价值主张文案
- 右侧：注册表单区（自适应宽度），垂直居中

#### 操作流程

**主流程：**

1. 用户点击「Sign Up」进入注册页面
2. 用户输入邮箱地址
3. 用户设置密码
4. 用户点击「Sign up」提交注册（页面展示 Clickwrap 协议提示，点击按钮即视为同意）
5. 系统采集设备指纹 + IP
6. 系统校验注册限频（同一设备指纹）
7. 系统校验邮箱是否已注册
8. 系统执行风控检测（参见 六、6.1 风控检测规则）
9. 风控通过，发送 6 位验证码到用户邮箱
10. 跳转至验证码校验页面（VerifyCode）
11. 用户输入验证码，点击「Verify code」
12. 验证通过，创建账号，写入 ConsentRecord（记录注册时生效的 ToS 和 Privacy Policy 版本号）
13. 签发 Token，记录设备指纹并关联 Session
14. 自动登录并跳转至首页

**分支流程：**

- 邮箱格式错误 → 实时提示「Please enter a valid email address」
- 密码不符合规则 → 实时提示具体不符合项
- 邮箱已被注册 → 提示「This email is already registered」，引导跳转登录页
- 注册限频触发 → 提示「Too many attempts, please try again later」
- 风控拦截 → 拦截或要求额外验证
- 验证码错误 → 提示「Wrong code, Please Try again」
- 验证码过期 → 提示「Code has expired. Please request a new one.」

#### 校验规则

| 字段 | 规则 | 校验时机 |
|------|------|----------|
| 邮箱 | 符合邮箱格式（遵循 RFC 5321 标准，最大长度 254 字符，允许加号标签如 user+tag@domain.com） | 失焦时前端校验 + 提交时后端校验 |
| 邮箱 | 未被已有账号占用 | 提交时后端校验 |
| 密码 | 至少 8 位，包含大小写字母和数字 | 实时前端校验 |

#### 异常处理

| 异常场景 | 处理方式 |
|----------|----------|
| 网络请求失败 | Toast 提示「Network error, please try again」 |
| 服务端错误 | Toast 提示「Something went wrong, please try again later」 |
| 注册被限频（风控拦截） | 提示「Too many attempts, please try again later」 |

#### UI 关联

- PC 端：设计稿 Register
- APP 端：设计稿 A-Register

---

### 2.3 OAuth 快捷注册（Google / Apple / Facebook）

#### 功能描述

用户通过第三方账号（Google / Apple / Facebook）一键创建 Looply 账号，降低注册门槛，提升转化。

#### 前置条件

- 用户未登录状态
- 用户拥有对应的第三方账号

#### 操作流程

**主流程：**

1. 用户点击「Continue with Google / Apple / Facebook」按钮
2. 系统采集设备指纹 + IP
3. 系统执行风控检测（规则同邮箱注册）
4. 风控通过，跳转至对应 OAuth 授权页面
5. 用户在第三方页面授权
6. 第三方回调返回授权码
7. 系统用授权码换取 token，获取用户信息（uid / email / name）
8. 系统判断 provider_uid 是否已绑定 Looply 账号
   - 已绑定（老用户）：直接签发 Token，跳转首页（参见 三、3.3）
   - 未绑定：继续下方注册流程
9. 系统判断是否获取到邮箱
   - **未获取到邮箱（Facebook 场景）**：跳转邮箱补充页（OAuthEmailSupplement），流程见 2.4 节
   - 已获取到邮箱：继续下方流程
10. 系统判断邮箱是否已被邮箱注册方式占用
    - 已注册：关联已有账号，写入 OAuth 绑定记录
    - 未注册：创建新账号，写入 ConsentRecord（记录注册时生效的 ToS 和 Privacy Policy 版本号）
11. 根据 Provider 类型执行差异化处理（参见下方 Provider 差异表）
12. 签发 Token，记录设备指纹并关联 Session
13. 跳转至首页

**分支流程：**

- 用户取消授权 → 返回注册页，无提示
- 风控拦截 → 拦截或要求额外验证
- 第三方服务不可用 → 提示「{Provider} sign-in is temporarily unavailable」

#### Provider 差异处理

| Provider | email 处理 | name 处理 | 特殊说明 |
|----------|-----------|-----------|----------|
| Google | email 写入凭证表 | 预填昵称到 user_profile.nickname | 标准流程 |
| Apple | 给了真实邮箱 → 写入凭证表；relay 邮箱 → 不写入 | 预填昵称（仅首次授权返回 firstName + lastName） | Apple Hide My Email 场景需特殊处理 |
| Facebook | 有邮箱 → 写入凭证表；无邮箱 → 跳转邮箱补充页（参见 2.4） | 预填昵称 | 无邮箱时必须补充邮箱才能完成注册 |

#### 技术说明

- 使用 OAuth 2.0 授权码模式
- 服务端实现统一的第三方登录适配层（Provider Pattern），新增登录方式时仅需实现对应 Provider
- Client Secret 仅存储在服务端，禁止暴露到前端
- state 参数必须校验，防止 CSRF 攻击
- 授权码仅可使用一次，有效期极短

#### UI 关联

- 注册页中的「Continue with Google / Apple / Facebook」按钮

---

### 2.4 OAuth 邮箱补充（OAuthEmailSupplement）

#### 功能描述

当 OAuth 授权回调未返回用户邮箱时（目前仅 Facebook 存在此场景），要求用户补充邮箱并完成验证，才能继续完成注册。确保所有用户都拥有可用的邮箱凭证。

#### 前置条件

- OAuth 授权已成功，provider_uid 未绑定已有账号
- Provider 未返回邮箱（当前仅 Facebook 会触发）

#### 页面布局（PC 端）

- 左侧：品牌展示区（同注册页布局）
- 右侧：邮箱补充表单区，垂直居中
  - 页面标题 + 说明文案
  - 邮箱输入框
  - 提交按钮
  - 具体文案见设计稿

#### 操作流程

**主流程：**

1. 系统在 OAuth 回调中检测到未返回邮箱，携带临时 OAuth 凭证跳转至邮箱补充页
2. 用户输入邮箱地址
3. 用户点击提交按钮
4. 系统校验邮箱格式
5. 系统发送 6 位验证码到用户邮箱
6. 跳转至验证码校验页面（VerifyCode）
7. 用户输入验证码，点击验证
8. 验证通过，系统判断邮箱是否已被邮箱注册方式占用：
   - **已注册**：关联已有账号，写入 OAuth 绑定记录（Facebook 绑定到已有账号），将验证后的邮箱写入凭证表
   - **未注册**：创建新账号，将邮箱写入凭证表，写入 ConsentRecord
9. 签发 Token，记录设备指纹并关联 Session
10. 跳转至首页

**分支流程：**

- 邮箱格式错误 → 实时提示「Please enter a valid email address」
- 验证码错误 → 提示「Wrong code, Please Try again」
- 验证码过期 → 提示「Code has expired. Please request a new one.」
- 用户关闭页面/返回 → 注册中断，OAuth 凭证失效，下次登录需重新授权

#### 校验规则

| 字段 | 规则 | 校验时机 |
|------|------|----------|
| 邮箱 | 符合邮箱格式（RFC 5321 标准，最大长度 254 字符） | 失焦时前端校验 + 提交时后端校验 |

#### 异常处理

| 异常场景 | 处理方式 |
|----------|----------|
| 网络请求失败 | Toast 提示「Network error, please try again」 |
| 服务端错误 | Toast 提示「Something went wrong, please try again later」 |
| 临时 OAuth 凭证过期 | 提示「Session expired, please try again」，跳转回登录页 |

#### 技术说明

- OAuth 回调后生成临时凭证（如短时效 token），携带 provider_uid 和 provider_name 等信息，用于邮箱补充完成后关联账号
- 临时凭证有效期建议 10 分钟，过期需重新发起 OAuth 授权
- 邮箱验证码复用现有验证码发送和校验逻辑（参见 2.8 邮箱验证码校验）

#### UI 关联

- PC 端：设计稿 OAuthEmailSupplement（待设计）
- APP 端：设计稿 A-OAuthEmailSupplement（待设计）

---

### 2.5 统一注册入口

#### 功能描述

注册页面提供统一入口，整合邮箱注册和三方快捷注册，用户可自由选择。

#### 页面元素（PC 端）

- 标题 + 副标题
- 邮箱输入框
- 密码输入框（带显示/隐藏切换）+ 密码规则提示
- 注册主按钮
- 分隔线 + OAuth 三方登录按钮（Google / Apple / Facebook）
- Clickwrap 协议提示（点击按钮即视为同意）
- 底部切换至登录页链接
- 具体文案见设计稿

#### 交互说明

- 页面默认展示邮箱注册表单
- 表单下方通过分隔线「or」连接三方登录按钮
- 页面底部提供「Already have an account? Sign in」链接跳转登录页

#### Identifier-First 统一入口（预留）

当前采用分离式注册/登录入口。预留 Identifier-First 统一入口模式：

- 迁移方案：前置 `/api/auth/identify` 端点，返回 `{action: register|login, methods: [...]}`
- 现有注册/登录后端流程段零改动，仅新增路由层
- 待业务成熟后评估是否启用

#### 页面状态变体

| 状态 | 说明 | 设计稿（PC） | 设计稿（APP） |
|------|------|-------------|-------------|
| 默认状态 | 按钮始终可点击，采用 Clickwrap 协议同意方式 | Register | A-Register |
| 置灰状态 | 表单未填写完整时，「Sign up」按钮置灰不可点击（灰色背景 + 灰色文字），引导用户填完必填项 | 同 Register（前端控制） | A-Register-DisabledState |
| 错误状态 | 邮箱校验失败（如已注册），输入框红色边框 + 下方 inline 错误提示 | 同 Register（前端控制） | A-Register-ErrorState |

---

### 2.6 密码设置

#### 功能描述

用户在注册时设置账号密码，密码需满足安全性要求。

#### 密码规则

密码校验规则详见 6.3 密码校验。

#### 交互说明

- 密码输入框默认隐藏内容，提供「显示/隐藏」切换（eye-off / eye 图标）
- 密码框下方显示规则提示文案

---

### 2.7 协议承接

#### 功能描述

注册流程中嵌入服务条款（ToS）和隐私政策（Privacy Policy）的确认环节，确保合规。

#### 交互说明

**注册页（邮箱注册）：**
- 采用 Clickwrap 方式：展示协议提示文案，Terms 和 Privacy Policy 为可点击链接
- 用户点击注册按钮即视为同意协议，无需单独勾选
- 协议页面支持返回注册页，保留已填写信息

**登录页：**
- 底部展示协议提示（无复选框），Terms 和 Privacy Policy 为可点击链接

#### 合规要求

- 注册页和登录页均采用 Clickwrap 方式（点击操作按钮即视为同意），符合美国市场主流合规实践
- 记录用户同意的时间戳和协议版本号
- 后续如进入欧洲市场（GDPR），需改为 Active Opt-in 方式（主动勾选复选框），届时按地区差异化处理

#### 2.7.1 服务条款页面（Terms of Service）

##### 功能描述

展示 Looply 平台的服务条款完整内容，用户在注册前可查阅。

##### 入口

- 注册页 / 登录页协议文案中的「Terms of Service」/「Terms」链接
- 页面底部（Footer）链接（未来扩展）

##### 页面元素

- 顶部导航栏：返回按钮 + Logo
- 内容区域：协议正文（长文本，支持滚动）
- 最后更新日期

##### 内容来源

- 协议正文由法务提供，运营通过后台「用户管理 → 协议管理」发布和更新（详见用户管理模块 PRD）
- 前端通过接口动态拉取当前生效版本的协议内容进行渲染

##### 交互说明

- 从注册页点击链接进入，新页面打开（非弹窗）
- 返回注册页时，保留用户已填写的表单信息
- PC 端和 APP 端共用同一份协议内容，仅布局适配不同
- 纯展示页面，无需登录即可访问
- 页面底部显示「最后更新日期」，取自服务端协议生效时间

##### UI 关联

- PC 端：设计稿 TermsOfService
- APP 端：设计稿 A-TermsOfService

#### 2.7.2 隐私政策页面（Privacy Policy）

##### 功能描述

展示 Looply 平台的隐私政策完整内容，告知用户个人数据的收集、使用和保护方式。

##### 入口

- 注册页 / 登录页协议文案中的「Privacy Policy」链接
- 页面底部（Footer）链接（未来扩展）

##### 页面元素

- 顶部导航栏：返回按钮 + Logo
- 内容区域：隐私政策正文（长文本，支持滚动）
- 最后更新日期

##### 内容来源

- 协议正文由法务提供，运营通过后台「用户管理 → 协议管理」发布和更新（详见用户管理模块 PRD）
- 前端通过接口动态拉取当前生效版本的协议内容进行渲染

##### 交互说明

- 从注册页点击链接进入，新页面打开（非弹窗）
- 返回注册页时，保留用户已填写的表单信息
- PC 端和 APP 端共用同一份协议内容，仅布局适配不同
- 纯展示页面，无需登录即可访问
- 页面底部显示「最后更新日期」，取自服务端协议生效时间

##### 合规要求

- 隐私政策内容需符合目标市场的数据保护法规（如 GDPR、CCPA 等）

##### UI 关联

- PC 端：设计稿 PrivacyPolicy
- APP 端：设计稿 A-PrivacyPolicy

---

### 2.8 邮箱验证码校验

#### 功能描述

用户在注册或忘记密码流程中，通过输入系统发送至邮箱的 6 位数字验证码完成身份验证。注册场景和忘记密码场景共用同一个 VerifyCode 页面。

#### 使用场景

| 场景 | 触发时机 | 验证通过后 |
|------|----------|------------|
| 邮箱注册 | 用户提交注册信息后 | 创建账号，自动登录跳转首页 |
| 忘记密码 | 用户提交邮箱后 | 跳转至重置密码页面 |

#### 页面元素

- 邮件图标 + 标题 + 副标题
- 6 位验证码输入框（每位独立输入框，当前焦点框高亮）
- 主操作按钮
- 重发链接
- 底部返回链接
- 具体文案见设计稿

#### 验证码规则

| 规则 | 说明 |
|------|------|
| 格式 | 6 位纯数字 |
| 有效期 | 10 分钟 |
| 使用次数 | 一次性，验证成功后立即失效 |
| 错误次数限制 | 连续输错 5 次后验证码失效，需重新发送 |
| 新码覆盖旧码 | 重新发送后，旧验证码立即失效 |

#### 重发机制

| 规则 | 说明 |
|------|------|
| 冷却时间 | 发送后 60 秒内不可重发，重发链接变为倒计时文案（见页面状态变体） |
| 每小时上限 | 同一邮箱滑动窗口 60 分钟内最多发送 5 次 |
| 达到上限 | 提示「Too many requests. Please try again later.」 |

#### 页面状态变体

| 状态 | 说明 | 设计稿（PC） | 设计稿（APP） |
|------|------|-------------|-------------|
| 默认状态（可重发） | Resend 为紫色可点击链接 | VerifyCode | A-VerifyCode |
| 已填充态 | 用户输入验证码后的状态，Resend 链接可点击 | VerifyCode-fill | A-VerifyCode-fill |
| 倒计时状态 | 倒计时文案为灰色不可点击，60 秒后自动恢复为可重发状态 | VerifyCode-Countdown | A-VerifyCode-Countdown |
| 错误状态 | 验证码校验失败，输入框显示错误样式 | —（前端控制） | A-VerifyCode-Error |

#### 交互说明

- 输入框自动聚焦第一位，输入后自动跳转下一位
- 支持粘贴完整 6 位验证码，自动填充所有输入框
- 输入完 6 位后「Verify code」按钮可点击
- 删除键可回退到上一位输入框

#### 异常处理

| 异常场景 | 处理方式 |
|----------|----------|
| 验证码错误 | 输入框下方提示「Wrong code, Please Try again」，清空输入框 |
| 验证码过期 | 提示「Code has expired. Please request a new one.」 |
| 连续 5 次错误 | 提示「Too many failed attempts. Please request a new code.」，当前验证码失效 |
| 网络请求失败 | Toast 提示「Network error, please try again」 |

#### UI 关联

- PC 端：设计稿 VerifyCode / VerifyCode-Countdown
- APP 端：设计稿 A-VerifyCode / A-VerifyCode-Countdown

---

### 2.9 价值点展示

#### 功能描述

注册/登录页面左侧（PC端）展示 Looply 平台的品牌视觉和核心价值主张，提升注册意愿。

#### 展示内容

- 全屏品牌背景图（660px 宽）
- 品牌 Logo（白色透明底）
- 品牌价值主张文案

#### 交互说明

- 纯展示区域，无交互操作
- PC 端位于表单左侧，固定 660px 宽度
- APP 端不展示（空间有限，优先展示表单）

---

## 三、登录模块

### 3.1 模块概述

- **模块目标**：保障用户顺畅进入站内，支持账户恢复
- **优先级**：P0
- **入口**：首页「Sign In」按钮、注册页引导链接、Session 过期后跳转
- **说明**：用户通过首页顶部「Sign In」按钮进入登录页面。首页设计稿见独立文件（同上）

### 3.2 邮箱密码登录

#### 功能描述

用户通过已注册的邮箱和密码登录 Looply 平台。

#### 前置条件

- 用户未登录状态
- 用户已拥有 Looply 账号

#### 页面布局（PC 端）

- 左侧：品牌展示区（660px 宽），与注册页共用布局
- 右侧：登录表单区（自适应宽度），垂直居中

#### 页面元素（PC 端）

- 标题 + 副标题
- 邮箱输入框
- 密码输入框（带显示/隐藏切换）
- Remember me 复选框 + Forgot password 链接（同一行，两端对齐）
- 登录主按钮
- 分隔线 + OAuth 三方登录按钮（Google / Apple / Facebook）
- 底部协议提示
- 底部切换至注册页链接
- 具体文案见设计稿

#### 操作流程

**主流程：**

1. 用户进入登录页面
2. 用户输入邮箱地址
3. 用户输入密码
4. 用户点击「Sign in」
5. 系统采集设备指纹 + IP
6. 系统执行风控检测（规则同注册）
7. 风控通过，校验邮箱是否存在
8. 校验密码错误次数是否 >= 5 次（是则锁定 30 分钟）
9. 校验密码是否正确
10. 签发 Token（设置 Cookie），记录设备指纹并关联 Session
11. 登录成功，跳转至首页（或登录前访问的页面）

**分支流程：**

- 邮箱格式错误 → 实时提示「Please enter a valid email address」
- 风控拦截 → 拦截或要求额外验证
- 邮箱未注册 → 提示「Incorrect email or password」（不暴露邮箱是否存在）
- 密码错误 → 提示「Incorrect email or password」
- 账号被锁定 → 提示「Account locked. Too many failed attempts. Please try again in 30 minutes.」
- 账号被冻结 → 页面顶部 ErrorBanner 提示「Your account has been suspended. Please contact support@looply.com for assistance.」

#### 校验规则

| 字段 | 规则 | 校验时机 |
|------|------|----------|
| 邮箱 | 符合邮箱格式 | 失焦时前端校验 |
| 密码 | 非空 | 提交时前端校验 |
| 邮箱+密码 | 匹配已有账号 | 提交时后端校验 |

#### 异常处理

| 异常场景 | 处理方式 |
|----------|----------|
| 连续输错密码（达到 5 次） | 账号锁定 30 分钟，页面展示锁定提示 |
| 网络请求失败 | Toast 提示重试 |

#### 页面状态变体

| 状态 | 说明 | 设计稿（PC） | 设计稿（APP） |
|------|------|-------------|-------------|
| 默认状态 | 空表单 | Login | A-Login |
| 密码可见 | 点击 eye 图标后密码明文显示 | Login-PasswordVisible | A-Login-PasswordVisible |
| 错误状态（密码隐藏） | 输入框红色边框 + 字段下方 inline 错误提示，密码为密文 | Login-ErrorState | A-Login-error-password off |
| 错误状态（密码可见） | 同上，但密码为明文显示 | —（前端控制） | A-Login-error-password on |
| 加载状态 | 按钮显示 loading 动画 + spinner | Login-LoadingState | A-Login-LoadingState |

#### UI 关联

- PC 端：设计稿 Login / Login-PasswordVisible / Login-ErrorState / Login-LoadingState
- APP 端：设计稿 A-Login / A-Login-PasswordVisible / A-Login-error-password off / A-Login-error-password on / A-Login-LoadingState

---

### 3.3 OAuth 快捷登录（Google / Apple / Facebook）

#### 功能描述

已通过第三方注册的用户，使用对应账号一键登录。未注册用户点击后自动走注册流程（参见 2.3）。

#### 操作流程

**主流程：**

1. 用户点击「Continue with Google / Apple / Facebook」
2. 系统采集设备指纹 + IP，执行风控检测
3. 风控通过，跳转至对应 OAuth 授权页
4. 用户授权，系统获取用户信息
5. 系统判断 provider_uid 是否已绑定
   - 已绑定（老用户）：直接签发 Token，记录设备指纹并关联 Session，跳转首页
   - 未绑定：走 OAuth 注册流程（参见 2.3 步骤 9 起）

**分支流程：**

- 用户取消授权 → 返回登录页
- 风控拦截 → 拦截或要求额外验证
- 第三方服务不可用 → 提示使用邮箱密码登录
- 账号被冻结 → 跳转登录页，页面顶部 ErrorBanner 提示「Your account has been suspended. Please contact support@looply.com for assistance.」

#### 外部服务依赖

| Provider | 授权协议 | 配置平台 | 需获取信息 |
|----------|----------|----------|-----------|
| Google | OAuth 2.0 | Google Cloud Console | email, profile |
| Apple | OAuth 2.0 + OIDC | Apple Developer | email, name（仅首次） |
| Facebook | OAuth 2.0 | Meta for Developers | email, name |

#### 接入流程（技术侧）

**一、前期配置（一次性，每个 Provider）**

1. 在对应平台创建应用 / 项目
2. 配置 OAuth 2.0 同意屏幕（应用名称、授权域名、隐私政策链接等）
3. 创建 OAuth 2.0 客户端凭据
4. 配置授权重定向 URI：`https://www.looply.com/api/auth/{provider}/callback`
5. 获取 Client ID 和 Client Secret，配置到服务端环境变量

**二、授权流程（每次登录）**

```
用户浏览器                    Looply 服务端                  Provider 服务
    |                              |                              |
    |-- 1. 点击三方登录 ---------->|                              |
    |                              |-- 2. 生成 state 参数 -------->|
    |<--- 3. 302 重定向至 Provider -|                              |
    |                              |                              |
    |-- 4. 用户授权 ------------->|                              |
    |                              |                              |
    |<--- 5. 携带 code 回调 ------|                              |
    |-- 6. code 发送到服务端 ---->|                              |
    |                              |-- 7. 用 code 换取 Token ---->|
    |                              |<-- 8. 返回 access_token -----|
    |                              |-- 9. 获取用户信息 ---------->|
    |                              |<-- 10. 返回 uid/email/name --|
    |                              |                              |
    |                              |-- 11. 查询/创建 Looply 账号  |
    |                              |-- 12. 签发 Looply Token      |
    |<--- 13. 登录成功，跳转 -----|                              |
```

**三、安全要求**

- Client Secret 仅存储在服务端，禁止暴露到前端
- state 参数必须校验，防止 CSRF 攻击
- 授权码（code）仅可使用一次，且有效期极短（通常 10 分钟）
- access_token 不持久化存储，用完即弃
- 仅通过服务端发起 Token 交换请求，禁止前端直接调用

---

### 3.4 忘记密码

#### 功能描述

用户忘记密码时，通过邮箱验证身份并重置密码。

#### 前置条件

- 用户已注册 Looply 账号
- 用户能访问注册邮箱

#### 页面元素

- 图标 + 标题 + 副标题
- 邮箱输入框
- 主操作按钮
- 底部返回链接
- 具体文案见设计稿

#### 操作流程

**主流程：**

1. 用户在登录页点击「Forgot password?」
2. 跳转至忘记密码页面
3. 用户输入注册邮箱
4. 用户点击「Send reset code」
5. 系统校验邮箱格式
6. 系统校验邮箱是否存在（不存在也返回成功提示，防枚举）
7. 系统校验发信限频
8. 发送 6 位验证码到用户邮箱
9. 跳转至验证码校验页面（VerifyCode）
10. 用户输入验证码，点击「Verify code」
11. 验证通过，跳转至重置密码页面

**分支流程：**

- 邮箱格式错误 → 提示「Please enter a valid email address」
- 输入的邮箱未注册 → 仍提示「If this email is registered, you will receive a verification code」（防枚举）
- 发信限频触发 → 提示「Too many requests. Please try again later.」
- 验证码校验相关分支 → 参见 2.8 邮箱验证码校验

#### UI 关联

- PC 端：设计稿 ForgotPassword
- APP 端：设计稿 A-ForgotPassword

---

### 3.5 重置密码

#### 功能描述

用户通过验证码校验后，设置新密码。

#### 前置条件

- 用户已通过忘记密码流程中的验证码校验（参见 2.8）

#### 页面元素

- 图标 + 标题 + 副标题（含密码规则说明）
- 新密码输入框（带显示/隐藏切换）
- 确认密码输入框（带显示/隐藏切换）
- 主操作按钮
- 底部返回链接
- 具体文案见设计稿

#### 操作流程

**主流程：**

1. 验证码校验通过后，自动跳转至重置密码页面
2. 用户输入新密码
3. 用户输入确认密码
4. 用户点击「Reset password」
5. 系统校验密码规则
6. 系统校验新密码与旧密码是否相同（不能相同）
7. 更新密码哈希
8. 失效所有旧 Token
9. 写入审计日志（重置密码）
10. Toast 提示「Password updated successfully」，2 秒后自动跳转至登录页：若本地存在回访信息（Login-Remembered），跳转回访登录页；否则跳转标准登录页，邮箱输入框预填用户邮箱

**分支流程：**

- 密码不符合规则 → 提示具体不符合项
- 确认密码不一致 → 提示「Passwords do not match」
- 新密码与旧密码相同 → 提示「New password must be different from your current password」
- 重置会话过期（验证码校验通过后 15 分钟内未完成重置） → 提示「Session expired. Please start over.」，跳转至忘记密码页面

#### 密码规则

- 与注册时密码规则一致（参见 2.6 密码设置）

#### UI 关联

- PC 端：设计稿 ResetPassword
- APP 端：设计稿 A-ResetPassword

---

### 3.6 登录态保持

#### 功能描述

用户登录成功后，系统通过 JWT 方案维持登录态。access_token 短期有效用于接口鉴权，refresh_token 长期有效用于刷新。

#### 交互说明

- 登录表单中提供「Remember me」复选框
- 勾选后，refresh_token 有效期 30 天
- 未勾选时，refresh_token 为会话级，浏览器关闭后失效

#### 有效期规则

| 场景 | access_token | refresh_token | 说明 |
|------|-------------|---------------|------|
| PC 端勾选 Remember Me | 短期（如 15 分钟） | 30 天 | 30 天内 refresh_token 可换取新 access_token |
| PC 端未勾选 | 短期（如 15 分钟） | 会话级 | 浏览器关闭后 refresh_token 失效 |
| APP 端 | 短期（如 15 分钟） | 30 天 | APP 端无 Remember Me 复选框，默认 30 天有效期 |
| Token 自然过期 | - | - | 触发 Token 刷新流程（参见 五、5.2） |
| 用户持续活跃 | 自动续期 | 滑动续期 | 每次刷新时 refresh_token 过期时间重新计算 |

#### Cookie 存储说明

| 属性 | 值 | 说明 |
|------|-----|------|
| Name | `looply_refresh_token` | refresh_token 标识 |
| Domain | `.looply.com` | 主域名下共享 |
| Path | `/` | 全站生效 |
| Max-Age | `2592000`（30天） | 勾选 Remember Me 时设置 |
| HttpOnly | `true` | 禁止 JS 读取，防 XSS |
| Secure | `true` | 仅 HTTPS 传输 |
| SameSite | `Lax` | 防 CSRF，允许顶级导航携带 |

#### 安全说明

- access_token 不落库，仅存在于内存 / HTTP Header 中
- refresh_token 存储在服务端，关联 Session
- 用户主动退出时，清除 Cookie 和服务端 refresh_token
- 密码修改后，所有已签发的 refresh_token 失效，用户需重新登录
- Cookie 设置 HttpOnly + Secure + SameSite，防止 XSS 和 CSRF 攻击

---

### 3.7 回访用户登录页（Login-Remembered）

#### 功能描述

当用户之前勾选了「Remember me」并在有效期内再次访问登录页时，系统识别回访用户身份，展示个性化的登录页面变体，预填充用户邮箱，降低登录操作成本。

#### 触发条件

- 用户之前登录时勾选了「Remember me」
- Cookie 尚在有效期内但 Token 已过期（需重新输入密码）
- 本地存储中保留了用户邮箱信息

#### 与标准登录页的结构差异

| 元素 | 标准登录页（Login） | 回访登录页（Login-Remembered） |
|------|---------------------|-------------------------------|
| 切换账号链接 | 无 | 有（点击跳转标准登录页） |
| 用户头像 | 无 | 显示用户首字母圆形头像 |
| 标题 | 通用欢迎语 | 个性化欢迎语（含用户名） |
| 副标题 | 通用描述 | 显示用户邮箱 |
| 邮箱输入框 | 需用户输入 | 无（已识别用户） |
| 密码输入框 | 空 | 空，需用户输入 |
| Remember me | 未勾选 | PC 端保留，APP 端无 |
| Forgot password | 有 | 有 |
| OAuth 按钮 | 有 | 无 |
| 底部注册切换 | 有 | 无 |

#### 交互说明

- 点击「Use another account」→ 清除本地回访信息，跳转至标准登录页
- 密码输入框自动获取焦点，减少操作步骤
- 其余交互逻辑与标准登录页一致（参见 3.2）

#### 技术说明

- 回访用户识别基于本地存储（localStorage），存储字段：邮箱、用户名、首字母
- 用户主动退出时清除本地存储的回访信息

#### UI 关联

- PC 端：设计稿 Login-Remembered
- APP 端：设计稿 A-Login-Remembered

---

## 四、退出模块

### 4.1 模块概述

- **模块目标**：形成完整账户闭环，满足 PC 端账号切换与安全需求
- **优先级**：P0
- **入口**：用户头像下拉菜单 / 设置页面

### 4.2 主动退出

#### 功能描述

用户主动触发退出登录操作。

#### 页面元素（退出确认弹窗）

- 遮罩层（半透明背景）
- 弹窗卡片（居中显示）
  - 标题 + 说明文案
  - 确认按钮（主按钮）+ 取消按钮（次按钮），并排显示
- 具体文案见设计稿

#### 操作流程

**主流程：**

1. 用户点击退出入口
2. 弹出确认弹窗
3. 用户点击「Yes, Sign Out」确认
4. 系统清除 Session / Token（包括 refresh_token）
5. 跳转至首页

**分支流程：**

- 用户点击「Cancel」→ 关闭弹窗，保持当前状态
- 退出请求失败 → 前端强制清除本地 Token，跳转首页

#### UI 关联

- PC 端：设计稿 LogoutModal
- APP 端：设计稿 A-LogoutModal

---

### 4.3 退出入口

#### 功能描述

在合适的位置提供退出登录入口，确保用户可发现。

#### 入口位置

| 终端 | 入口位置 |
|------|----------|
| PC 端 | 页面右上角用户头像 → 下拉菜单 → 「Sign Out」 |
| APP 端 | 「我的」页面底部 → 「Sign Out」按钮 |

---

### 4.4 退出跳转

#### 功能描述

退出登录后的页面跳转逻辑。

#### 跳转规则

| 场景 | 跳转目标 |
|------|----------|
| 用户主动退出 | 跳转至首页 |
| Session 过期被动退出 | 跳转至首页，显示「Session expired」提示 |
| 安全强制退出（密码修改等） | 跳转至首页，显示对应提示 |
| 账号被冻结（运营操作） | 跳转至登录页，页面顶部 ErrorBanner 提示「Your account has been suspended. Please contact support@looply.com for assistance.」 |
| 协议版本更新拒绝同意 | 强制退出登录，跳转至首页 |

> **备注**：首页设计稿见独立文件：PC 端 looply-home-PC.pen / APP 端 looply-home-APP.pen（位于「海外业务首页/UI/」目录）。

---

### 4.5 退出反馈

#### 功能描述

退出操作的全流程需有明确的用户反馈。

#### 反馈方式

| 节点 | 反馈方式 |
|------|----------|
| 点击退出 | 弹出确认弹窗 |
| 确认退出中 | 按钮显示 loading 状态 |
| 退出成功 | 跳转首页（即为成功反馈） |
| 退出失败 | Toast 提示「Sign out failed, please try again」 |

---

### 4.6 账号注销（Account Deletion）

#### 功能描述

用户通过邮件向运营团队申请注销账号，由运营在后台「用户管理」模块执行注销操作。本期不提供用户端自助注销入口。

#### 注销后处理

| 处理项 | 说明 |
|--------|------|
| 登录态 | 立即清除所有 Token 和 Cookie |
| 用户数据 | 按数据保留策略处理（见下方） |
| 第三方绑定 | 解除所有 OAuth 绑定关系 |
| 邮箱释放 | 注销后邮箱立即释放，可用于重新注册（视为新账号，不恢复旧数据） |

#### 数据处理策略（立即匿名化）

注销执行后，系统立即对个人身份信息（PII）进行匿名化处理，记录保留但不可再关联到具体个人。匿名化满足 GDPR/CCPA 删除权要求，不做物理删除。

| 数据类型 | 处理方式 | 说明 |
|----------|----------|------|
| 账号信息（邮箱、用户名等） | 立即匿名化（如邮箱置为 `deleted_{uid}@anonymous`） | 记录保留，PII 不可识别 |
| 交易记录 | 永久保留（关联匿名化后的账号） | 财务合规要求 |
| 用户内容（商品、评价） | 下架但保留 | 涉及其他用户的交易记录完整性 |
| 个人信息（姓名、地址、手机号等） | 立即匿名化 | PII 脱敏，记录保留 |

---

## 五、密码管理与会话管理模块

### 5.1 密码修改（登录态）

#### 功能描述

已登录用户主动修改当前密码。与「忘记密码」不同，此功能需要用户先验证旧密码。

#### 前置条件

- 用户已登录状态
- 用户拥有密码（仅 OAuth 注册的用户无此功能入口）

#### 入口

- 账号设置页面 → 「Change Password」（具体设置页尚未设计，仅作示意）

#### 操作流程

**主流程：**

1. 用户进入密码修改页面
2. 用户输入旧密码
3. 系统校验旧密码是否正确
4. 旧密码正确 → 用户输入新密码
5. 系统校验新旧密码是否相同（不能相同）
6. 系统校验新密码是否符合密码规则
7. 更新密码哈希
8. 终止所有其他 Session（当前 Session 保留）
9. 写入审计日志（改密码）
10. Toast 提示「Password updated successfully」，返回上一页面

**分支流程：**

- 旧密码错误 → 提示「Incorrect password」
- 新旧密码相同 → 提示「New password must be different from your current password」
- 新密码不符合规则 → 提示具体不符合项

#### 密码规则

- 与注册时密码规则一致（参见 2.6 密码设置）

#### 安全说明

- 修改密码后，除当前 Session 外的所有 Session 立即失效
- 其他设备需重新登录

#### UI 关联

- PC 端：设计稿 ChangePassword
- APP 端：设计稿 A-ChangePassword

---

### 5.2 Token 刷新

#### 功能描述

当 access_token 过期时，系统自动使用 refresh_token 换取新的 access_token，实现无感续期。

#### 触发条件

- 前端检测到 access_token 过期（接口返回 401 或本地判断过期）

#### 刷新流程

1. 前端检测 access_token 过期
2. 携带 refresh_token 请求刷新接口
3. 系统校验 refresh_token 是否有效
   - 无效 → 返回 401，前端清除本地 Token，跳转首页提示重新登录
4. 系统校验 Session 状态是否活跃
   - 已终止 → 返回 401（已终止）
5. 签发新 access_token
6. 滑动续期 refresh_token（重新计算过期时间）
7. 刷新完成，前端用新 access_token 重试原请求

#### 异常处理

| 异常场景 | 处理方式 |
|----------|----------|
| refresh_token 无效/过期 | 返回 401，跳转首页，提示「Session expired. Please sign in again.」 |
| Session 已被终止 | 返回 401，跳转首页，提示「Session expired. Please sign in again.」 |
| 网络请求失败 | 前端重试 1 次，仍失败则提示用户 |

#### 技术说明

- access_token 采用 JWT 格式，不落库，服务端无状态验证
- refresh_token 存储在服务端，关联 Session 记录
- 每次刷新时 refresh_token 滑动续期，只要用户持续使用就不会过期

---

### 5.3 会话失效（被动退出）

#### 功能描述

当用户的登录会话失效时，系统自动处理并引导用户重新登录。

#### 失效场景

| 场景 | 触发条件 |
|------|----------|
| Token 自然过期 | access_token 和 refresh_token 均过期 |
| 密码被修改 | 用户修改密码后，所有其他 Session 的 refresh_token 失效 |
| 管理员强制下线 | 后台操作使指定用户 Session 失效 |
| 账号被锁定 | 触发安全策略后，当前 Session 失效 |

#### 处理流程

1. 前端请求接口返回 401 状态码
2. 前端尝试 Token 刷新（参见 5.2）
3. 刷新失败 → 清除本地存储的 Token / Cookie
4. 跳转至首页
5. 首页展示提示信息「Session expired. Please sign in again.」
6. 登录成功后，尝试恢复用户之前访问的页面

---

### 5.4 协议版本检测

#### 功能描述

当平台更新服务条款或隐私政策时，系统检测协议版本变化，弹窗要求已登录用户确认新版协议。

#### 版本管理规则

- **版本号格式**：递增整数（v1、v2、v3...）
- **ToS 和 Privacy Policy 各自独立版本号**，互不影响
- **协议内容由法务提供，运营通过后台发布**（详见用户管理模块 PRD「协议管理」）

#### 检测时机

| 时机 | 说明 |
|------|------|
| 用户登录成功时 | 登录接口返回当前协议版本，前端比对用户已同意版本 |
| 已登录用户访问页面时 | 前端调用版本检查接口，按会话级缓存（同一会话内仅检查一次，不重复请求） |

#### 操作流程

**主流程：**

1. 系统检测到用户已同意的协议版本 < 当前生效版本
2. 弹出协议更新弹窗（仅提示有变更的协议，如只有 ToS 更新则只弹 ToS）
3. 用户点击「同意」
4. 系统写入 ConsentRecord（记录协议类型、版本号、同意时间、用户国家）
5. 正常访问页面

**分支流程：**

- 用户拒绝同意 → 强制退出登录，跳转至首页
- ToS 和 Privacy Policy 同时更新 → 弹窗中同时展示两份协议的更新提示，用户一次确认

#### 协议类型枚举

| 协议类型 | 含义 | 适用场景 |
|----------|------|----------|
| 隐私政策（Privacy Policy） | 平台数据收集、使用、共享的隐私声明 | 注册时同意 + 版本更新后重新同意 |
| 服务条款（Terms of Service） | 平台使用的权利义务条款 | 注册时同意 + 版本更新后重新同意 |

#### UI 关联

- PC 端：设计稿 ConsentUpdateModal
- APP 端：设计稿 A-ConsentUpdateModal

---

## 六、安全风控模块

### 6.1 模块概述

- **模块目标**：保障基础账户安全，降低恶意操作风险
- **优先级**：P0
- **作用范围**：贯穿注册、登录、OAuth 认证、密码重置全流程

### 6.2 风控检测规则

#### 功能描述

在注册、登录、OAuth 认证等关键节点，系统采集设备指纹和 IP 信息，执行风控检测。

#### 检测规则与异常判定

| 序号 | 检测项 | 异常判定口径 | 处置动作 |
|------|--------|-------------|---------|
| 1 | 设备指纹是否已知 | 系统无该设备记录 = 未知设备 | 创建设备记录；单独不触发拦截，作为其他维度的加权因素 |
| 2 | 是否信任设备 | 前期简化：所有已知设备视为信任设备，不启用信任设备功能。后续开放后，用户主动标记「Trust this device」的设备为信任设备，未标记的已知设备为不信任 | 前期：不触发额外验证。后续开放后：不信任设备 → 发送邮箱验证码 |
| 3 | IP 地理位置异常 | 与上一次成功登录的 IP 所在州（State）不同 = 异地；与账号注册国不同 = 跨国 | 跨州 → 发送邮箱验证码；跨国 → 直接拦截 |
| 4 | 暴力破解检测 | 同一 IP 在 10 分钟内对不同账号发起 ≥10 次登录请求 | 该 IP 下所有请求弹图形验证码（CAPTCHA），持续 30 分钟 |
| 5 | 综合风险评估 | 由以上四项组合判定，具体评分模型由技术侧设计 | 低风险 → 放行；中风险 → 邮箱验证码；高风险 → 拦截 |

> **暴力破解检测（第4项）与 6.4 登录限错的关系说明**：
> - 登录限错（6.4）：单账号维度，同一账号连续输错 5 次 → 锁定该账号 30 分钟
> - 暴力破解检测（第4项）：单 IP 维度，同一 IP 短时间内扫多个账号 → 该 IP 弹 CAPTCHA
> - 两层独立运行，互不影响，可同时触发

#### 额外验证方式

| 触发场景 | 验证方式 | 说明 |
|----------|---------|------|
| 不信任设备登录（前期不启用） | 邮箱验证码 | 向账号绑定邮箱发送 6 位验证码 |
| IP 跨州异地 | 邮箱验证码 | 向账号绑定邮箱发送 6 位验证码 |
| IP 跨国 | 直接拦截 | 不提供验证通道，弹出拦截弹窗 |
| 暴力破解触发 | 图形验证码（CAPTCHA） | 该 IP 下所有请求需通过 CAPTCHA，持续 30 分钟 |

#### 高风险拦截处理

- **拦截弹窗提示**：「Sign-in blocked. We noticed a sign-in attempt from an unusual location. For your security, this request has been blocked.」
- **MVP 阶段不提供自助申诉渠道**，仅展示拦截弹窗 + 返回登录页按钮
- **拦截记录写入风控日志**，客服后台可查询

#### 应用场景

- 邮箱注册（步骤 6-9）
- 邮箱登录（步骤 5-6）
- OAuth 认证（步骤 2-3）

#### 技术说明

- 设备指纹采集在前端完成，提交到后端
- 风控检测结果关联 Session 记录
- 通过风控后，设备指纹与 Session 绑定

#### 风控拦截弹窗（RiskBlocked）

##### 功能描述

当系统检测到高风险行为（如跨国 IP 登录）时，以模态弹窗形式展示拦截提示，阻止用户继续操作。MVP 阶段仅展示拦截提示，不提供自助申诉渠道。

##### 页面元素

- 半透明遮罩层（覆盖当前页面）
- 弹窗卡片（居中显示）
  - 警告图标 + 标题 + 说明文案
  - 返回登录页按钮
- 具体文案见设计稿

##### 交互说明

- 弹窗为只读状态，用户无法绕过拦截
- 点击遮罩层不关闭弹窗（强制阅读）
- 点击「Back to sign in」跳转至标准登录页

##### UI 关联

- PC 端：设计稿 RiskBlocked
- APP 端：设计稿 A-RiskBlocked

---

#### 跨州异地登录验证页面（VerifyCode-CrossStateLogin）

##### 功能描述

当系统检测到用户从与上次登录不同的州（State）发起登录时，触发额外的邮箱验证码验证。页面基于标准 VerifyCode 页面，顶部增加位置异常提示 Banner。

##### 与标准 VerifyCode 页面的差异

| 元素 | 标准 VerifyCode | CrossStateLogin 变体 |
|------|----------------|---------------------|
| 顶部 Banner | 无 | 橙色位置提示 Banner（背景 #FFF7ED） |
| Banner 文案 | - | 「We noticed a sign-in attempt from a new location. Please verify your identity.」 |
| 其余元素 | 标准验证码输入 | 与标准 VerifyCode 一致 |

##### 交互说明

- 位置提示 Banner 为纯展示，不可关闭
- 验证码输入、重发、错误处理等逻辑与标准 VerifyCode 一致（参见 2.8）
- 验证通过后，正常完成登录流程

##### UI 关联

- PC 端：设计稿 VerifyCode-CrossStateLogin
- APP 端：设计稿 A-VerifyCode-CrossStateLogin

---

### 6.3 密码校验

#### 功能描述

对用户设置的密码进行安全性校验，确保密码强度达标。

#### 校验规则

| 规则 | 说明 |
|------|------|
| 最小长度 | 8 个字符 |
| 最大长度 | 64 个字符 |
| 大写字母 | 至少包含 1 个 A-Z |
| 小写字母 | 至少包含 1 个 a-z |
| 数字 | 至少包含 1 个 0-9 |

#### 应用场景

- 注册时设置密码
- 忘记密码后重置密码
- 登录态下修改密码

#### 交互说明

- 实时校验，逐条显示是否满足（通过/未通过状态）
- 全部通过后「提交」按钮可点击

---

### 6.4 登录限错

#### 功能描述

限制登录密码错误次数，防止暴力破解。

#### 规则

| 条件 | 处理 |
|------|------|
| 连续输错 5 次 | 账号锁定 30 分钟 |
| 锁定期间尝试登录 | 提示「Account locked. Too many failed attempts. Please try again in 30 minutes.」 |
| 锁定到期 | 自动解锁，错误计数重置 |
| 登录成功 | 错误计数重置 |

#### 技术说明

- 错误计数基于账号维度（非 IP 维度）
- 锁定状态存储在服务端

---

### 6.5 注册限频

#### 功能描述

限制同一设备在短时间内的注册请求次数，防止批量注册。

#### 规则

| 维度 | 限制 |
|------|------|
| 同一设备指纹 | 滑动窗口 60 分钟内最多注册 3 个账号 |

#### 触发后处理

- 提示「Too many attempts. Please try again later.」
- 不暴露具体限制规则

---

### 6.6 发信限频

#### 功能描述

限制验证码邮件的发送频率，防止邮件轰炸。适用于注册验证码和忘记密码验证码两个场景。

#### 规则

| 维度 | 限制 |
|------|------|
| 同一邮箱 | 60 秒内不可重复发送 |
| 同一邮箱 | 滑动窗口 60 分钟内最多发送 5 封 |

#### 交互说明

- 发送成功后按钮显示倒计时（60s）
- 达到小时上限后提示「Too many requests. Please try again later.」

---

### 6.7 异常提示

#### 功能描述

当系统检测到异常行为时，向用户展示明确的提示信息。

#### 异常场景与提示

| 异常场景 | 提示内容 | 展示方式 |
|----------|----------|----------|
| 账号被锁定 | Too many failed attempts. Account locked for 30 minutes. | 页面顶部 Banner |
| 账号被冻结 | Your account has been suspended. Please contact support@looply.com for assistance. | 页面顶部 Banner |
| 登录密码错误 | Incorrect email or password | 输入框下方错误提示 |
| 邮箱格式错误 | Please enter a valid email address | 输入框下方错误提示 |
| 网络错误 | Network error, please try again | Toast 提示 |
| 服务端错误 | Something went wrong, please try again later | Toast 提示 |
| 注册被限频 | Too many attempts, please try again later | Toast 提示 |
| 风控拦截（跨国/高风险） | Unusual activity detected. Your request has been blocked for security reasons. | 拦截弹窗 |
| 风控异地验证（跨州） | We noticed a login from a new location. Please verify your identity. | 页面顶部 Banner + 跳转邮箱验证码页 |
| 暴力破解触发 CAPTCHA | Please complete the verification to continue. | 弹出图形验证码（CAPTCHA） |

#### 错误提示展示方式

系统提供两种错误提示组件，按场景分开使用，**禁止同一条错误信息同时使用两种方式展示**：

| 组件 | 适用场景 | 样式 | 示例页面 |
|------|---------|------|---------|
| ErrorBanner | 页面级提示：系统提示、风控拦截、异地登录警告等，错误无法归因到具体字段 | 红/橙色背景条 + 图标 + 文案，位于表单区域顶部 | RiskBlocked、VerifyCode-CrossStateLogin |
| Input/Error | 字段级提示：表单校验错误，错误可归因到具体输入框 | 输入框红色边框 + 下方红色错误文案 | Login-ErrorState、Register-ErrorState |

**混用规则：**

- 同一页面可以同时出现两种组件（如：顶部 Banner 提示会话过期 + 字段 inline 提示格式错误），但同一条错误信息只能用一种方式展示
- 表单校验类错误（邮箱格式、密码规则）统一用 Input/Error
- 系统级错误（网络异常、服务不可用）统一用 Toast，不用 Banner 或 Input/Error

#### 设计原则

- 错误提示使用红色文字 + 错误图标
- 安全相关提示不暴露系统内部逻辑（如不区分"邮箱不存在"和"密码错误"）
- 所有提示文案需支持多语言

### 6.8 审计日志

#### 功能描述

记录用户账号的关键安全操作，用于安全审计和问题排查。审计日志为后台记录，用户端无感知。

#### 操作类型枚举

| 操作类型 | 含义 | 触发时机 |
|----------|------|----------|
| 改密码 | 用户修改登录密码 | 登录态下通过密码修改页完成新密码设置 |
| 重置密码 | 通过忘记密码流程重置密码 | 验证码校验通过后设置新密码 |
| 绑定凭证 | 添加邮箱登录凭证 | 三方登录用户补充邮箱+密码（预留，当前 MVP 不涉及） |
| 解绑凭证 | 移除邮箱登录凭证 | 用户移除邮箱密码登录方式（预留，当前 MVP 不涉及） |
| 绑定三方 | 关联第三方登录 | OAuth 首次授权后将 Provider 绑定到已有账号 |
| 解绑三方 | 移除第三方登录 | 用户移除某个 Provider 的关联（预留，当前 MVP 不涉及） |
| 注销 | 账号注销 | 运营在后台执行账号注销操作 |

#### 记录内容

每条审计日志记录以下信息：
- 操作类型（见上表）
- 操作详情（JSON 格式，记录操作的具体内容，如修改了哪个 Provider）
- 操作时的 IP 地址
- 操作时的设备信息

---

## 七、依赖与风险

### 7.1 外部服务依赖

| 服务 | 用途 | Provider | 前置准备 |
|------|------|----------|----------|
| Google OAuth | 三方注册/登录 | Google Cloud Console | 创建项目、配置同意屏幕、获取 Client ID/Secret、配置回调 URI |
| Apple OAuth | 三方注册/登录 | Apple Developer | 注册 App ID、配置 Sign in with Apple、获取密钥、**注册发件域名和发件邮箱**（用于向 Private Relay 地址发送邮件，需完成 SPF + DKIM 验证，否则系统邮件将被 Apple relay 服务器拒收） |
| Facebook OAuth | 三方注册/登录 | Meta for Developers | 创建应用、配置 Facebook Login、获取 App ID/Secret |
| 邮件发送服务 | 验证码发送（注册、忘记密码、跨州验证） | 待技术选型（如 SendGrid、AWS SES） | 服务商账号注册、域名验证、发信额度申请 |

### 7.2 上下游系统依赖

| 系统/模块 | 依赖关系 | 说明 |
|-----------|----------|------|
| 用户管理后台 | 下游依赖 | 协议管理（发布/更新协议内容和版本）、账号冻结、账号注销操作 |
| 首页模块 | 上游依赖 | 登录/注册入口页面，退出后跳转目标 |

### 7.3 风险项

| 风险 | 影响 | 应对措施 |
|------|------|----------|
| Apple/Facebook OAuth 审核周期长 | 可能延迟三方登录上线 | 提前提交审核，Google 优先接入，Apple/Facebook 可降级为二期 |
| Apple Private Relay 发件域名未注册 | 选择"Hide My Email"的 Apple 用户无法收到系统邮件（验证码、订单通知等），relay 服务器返回 550 unauthorized sender | 在 Apple Developer 后台注册 looply 发件域名和邮箱，完成 SPF + DKIM 验证；**必须在 Apple 登录上线前完成** |
| 邮件发送服务商未选型 | 阻塞验证码功能 | 尽早完成技术选型和域名验证 |
| CAPTCHA 服务商未选型 | 阻塞暴力破解防护 | 暂可用简单限频兜底，CAPTCHA 作为增强项 |

---

## 八、版本规划

### 8.1 MVP 范围（当前版本）

| 模块 | 功能 |
|------|------|
| 注册 | 邮箱注册、OAuth 快捷注册（Google/Apple/Facebook）、验证码校验、协议承接 |
| 登录 | 邮箱密码登录、OAuth 快捷登录、忘记密码/重置密码、登录态保持、回访用户登录 |
| 退出 | 主动退出、账号注销（运营代操作） |
| 密码管理 | 密码修改（登录态） |
| 会话管理 | Token 刷新、会话失效、协议版本检测 |
| 安全风控 | 设备指纹、IP 异地检测、暴力破解防护、登录限错、注册限频、发信限频 |

### 8.2 后续迭代方向

| 方向 | 说明 | PRD 预留位置 |
|------|------|-------------|
| Identifier-First 统一入口 | 先识别用户身份再决定注册/登录路径，简化入口 | 2.4 已预留方案 |
| 信任设备功能 | 用户主动标记信任设备，非信任设备触发额外验证 | 6.2 标注"前期不启用" |
| 手机号注册/登录 | 扩展注册入口，需处理交叉检测和账号枚举风险 | — |
| 用户端自助注销 | 替代运营代操作，用户端完成身份验证后自助注销 | 4.6 当前为运营代操作 |
| GDPR Active Opt-in | 进入欧洲市场后，协议同意改为主动勾选方式 | 2.6 已预留说明 |
| 协议管理后台 | 运营自助编辑发布协议内容，替代开发手动更新 | 用户管理模块待优化清单 |
| 年龄筛查（18+ 声明） | 注册时确认用户已满 18 岁（COPPA 合规），可通过 ToS 条款覆盖或独立复选框实现 | 需求优先级 R8 |
| 运营后台登录与 RBAC | 运营后台接入 SSO 登录和 C 端同源登录，RBAC 权限管理 | 8.3 架构预留 |
| 商家入驻与商家后台 | 商家通过 C 端同源方式登录，商家维度权限管理 | 8.3 架构预留 |

### 8.3 架构预留：运营后台与商家入驻

> 本节描述未来规划的系统扩展方向，当前 MVP 不实现，但当前设计需预留扩展空间。

#### 8.3.1 业务背景

未来计划接入运营后台（Admin Console）支持内部运营团队管理平台业务，同时支持商家入驻（Merchant Onboarding），商家通过商家后台管理自有店铺。

#### 8.3.2 用户角色模型

| 身份类型 | 说明 |
|----------|------|
| 普通买家 | 通过 C 端注册/登录，使用平台购物功能 |
| 商家 | 通过 C 端同源方式（邮箱密码/OAuth）登录，入驻开店并管理自有店铺；同一用户可同时为买家和商家 |
| 运营人员（兼买家） | 同一身份既可通过 C 端邮箱密码/OAuth 登录使用买家功能，也可登录运营后台进行管理操作 |
| 纯运营人员 | 仅通过 SSO 登录运营后台，不使用 C 端功能，无 C 端注册账号 |

#### 8.3.3 各端登录方式

| 端 | 登录方式 | 说明 |
|----|----------|------|
| C 端（买家/商家） | 邮箱密码、OAuth（Google/Apple/Facebook） | 即当前 MVP 实现的登录方式，买家和商家共用 |
| 运营后台 | SSO 单点登录（如 SAML/OIDC） | 仅运营人员使用，通过企业身份提供商认证 |
| 运营后台 | C 端同源登录（邮箱密码/OAuth） | 运营人员同时也是平台用户时，可复用 C 端凭证登录运营后台 |

#### 8.3.4 认证与鉴权架构

| 层级 | 体系 | 说明 |
|------|------|------|
| 身份认证（Authentication） | **一套**，统一身份层 | C 端、商家后台、运营后台共享用户身份标识和认证能力（邮箱密码校验、OAuth 认证）；SSO 认证成功后同样映射到统一身份层 |
| 鉴权授权（Authorization） | **三套**，各端独立 | C 端：基于用户身份的基础权限控制；商家后台：基于商家维度的权限管理（店铺级操作权限）；运营后台：RBAC（基于角色的访问控制），支持角色定义、权限分配、菜单/操作级别的细粒度管控 |

#### 8.3.5 对当前 MVP 设计的预留要求

| 预留点 | 说明 |
|--------|------|
| 用户身份层独立 | user 表作为统一身份源，可被 C 端、商家后台、运营后台共同引用，不耦合任何业务角色信息（角色由各业务域管理） |
| 认证与授权解耦 | 当前认证接口（注册/登录/密码管理/Token 刷新）不嵌入授权逻辑，授权由各端独立实现 |
| JWT payload 可扩展 | Token 结构预留扩展空间，未来可增加 role/scope 等字段标识接入端和权限上下文 |
| OAuth 凭证可复用 | 同一用户的 OAuth 绑定关系在各端之间共享，不重复绑定 |

---

## 九、附录

### 9.1 设计稿索引

| 页面 | PC 端设计稿 | APP 端设计稿 |
|------|------------|------------|
| 登录 | Login | A-Login |
| 登录-密码可见状态 | Login-PasswordVisible | A-Login-PasswordVisible |
| 登录-错误状态（密码隐藏） | Login-ErrorState | A-Login-error-password off |
| 登录-错误状态（密码可见） | —（前端控制） | A-Login-error-password on |
| 登录-加载状态 | Login-LoadingState | A-Login-LoadingState |
| 回访登录 | Login-Remembered | A-Login-Remembered |
| 注册 | Register | A-Register |
| 注册-错误状态 | —（前端控制） | A-Register-ErrorState |
| 注册-置灰状态 | —（前端控制） | A-Register-DisabledState |
| 验证码 | VerifyCode | A-VerifyCode |
| 验证码-已填充态 | VerifyCode-fill | A-VerifyCode-fill |
| 验证码-倒计时状态 | VerifyCode-Countdown | A-VerifyCode-Countdown |
| 验证码-错误状态 | —（前端控制） | A-VerifyCode-Error |
| 验证码-跨州异地登录 | VerifyCode-CrossStateLogin | A-VerifyCode-CrossStateLogin |
| 忘记密码 | ForgotPassword | A-ForgotPassword |
| 重置密码 | ResetPassword | A-ResetPassword |
| 隐私政策 | PrivacyPolicy | A-PrivacyPolicy |
| 服务条款 | TermsOfService | A-TermsOfService |
| 退出确认（弹窗） | LogoutModal | A-LogoutModal |
| 风控拦截（弹窗） | RiskBlocked | A-RiskBlocked |
| 密码修改 | ChangePassword | A-ChangePassword |
| OAuth 邮箱补充 | OAuthEmailSupplement（待设计） | A-OAuthEmailSupplement（待设计） |
| 协议版本更新（弹窗） | ConsentUpdateModal | A-ConsentUpdateModal |

### 9.2 修订记录

| 版本 | 日期 | 修改内容 | 修改人 |
|------|------|----------|--------|
| V1.0 | 2026-03-18 | 初稿，覆盖 MVP 四个模块 | 产品部 |
| V1.1 | 2026-03-18 | 补充 Google 登录接入流程及外部服务依赖；完善登录态 Cookie 存储规则 | 产品部 |
| V1.2 | 2026-03-18 | 首页作为登录/注册统一入口；退出登录跳转至首页 | 产品部 |
| V1.3 | 2026-03-18 | 新增邮箱验证码校验（2.8）；注册流程加入验证码步骤；忘记密码改为验证码方式 | 产品部 |
| V1.4 | 2026-03-18 | 新增服务条款页面（2.6.1）和隐私政策页面（2.6.2） | 产品部 |
| V1.5 | 2026-03-18 | 新增回访用户登录页（3.7 Login-Remembered） | 产品部 |
| V1.6 | 2026-03-18 | 移除密码强度指示器；新增国家/地区选择器（1.4） | 产品部 |
| V1.7 | 2026-03-30 | 新增账号注销（4.6）、OAuth 补充信息页（2.9）；国家选择器改为模态弹窗 | 产品部 |
| V2.0 | 2026-03-30 | 基于系统流程图 V7 和 PC v2 设计稿全面重写。新增：OAuth 三方登录扩展为 Google/Apple/Facebook 三个 Provider 及差异处理；密码修改（登录态）；Token 刷新机制（JWT 方案，access_token 不落库）；协议版本检测；账号注销支持 OAuth 用户；Identifier-First 统一入口预留；登录页面状态变体（ErrorState/LoadingState/PasswordVisible）；风控检测规则细化。登录态保持改为 JWT 双 Token 方案。设计稿索引更新为 PC v2 版本 | 产品部 |
| V2.1 | 2026-03-31 | 补齐 APP 端设计稿关联（15 个页面更新为实际设计稿）；新增 4 个页面说明：注册置灰状态（Register-DisabledState）、OAuth 补充信息置灰状态（OAuthSupplementary-DisabledState）、风控拦截页（RiskBlocked）、跨州异地登录验证页（VerifyCode-CrossStateLogin）；设计稿索引从 17 项扩展为 21 项 | 产品部 |
| V2.2 | 2026-03-31 | 关联首页设计稿（looply-home-PC.pen / looply-home-APP.pen），移除 3 处"首页尚未设计"备注 | 产品部 |
| V2.3 | 2026-03-31 | 删除 OAuth 补充信息页（OAuthSupplementary）：移除章节 2.7（原）、设计稿索引 2 项、接口 /api/auth/oauth/supplement；OAuth 注册完成后直接跳转首页；章节重新编号（2.9→2.8） | 产品部 |
| V2.4 | 2026-03-31 | APP 端设计稿优化：风控拦截页（RiskBlocked）改为弹窗样式；A-Login-ErrorState 移除冗余顶部错误 Banner；A-Register 简化密码区域（移除确认密码和密码规则，改为单行提示）；全部 icon 居中展示 | 产品部 |
| V2.5 | 2026-03-31 | 同步 H5 设计稿变更：返回链接文案统一为「Back」+ lucide arrow-left 图标（涉及 VerifyCode、ForgotPassword、ResetPassword）；服务条款/隐私政策页面 TopBar 布局修正为「左侧 Back 按钮 + 右侧 Logo」；AccountDeletion Cancel 改为按钮样式（Button/Outline） | 产品部 |
| V2.6 | 2026-04-04 | 基于 PC-v2 和 APP-v3 设计稿对齐更新。新增：验证码倒计时状态页（VerifyCode-Countdown）；注册页状态变体（ErrorState、DisabledState）。修改：Login-ErrorState 移除顶部 ErrorBanner，仅保留字段级 inline 错误提示。新增错误提示展示规范（ErrorBanner 页面级 vs Input/Error 字段级，禁止同一错误重复展示）。APP 端国家选择改为全屏引导页（Onboarding-CountryConfirm 替代 CountrySelector 弹窗）。设计稿索引统一 APP 端命名（H5/ → A-），从 18 项扩展为 21 项 | 产品部 |
| V2.7 | 2026-06-03 | 设计稿从 Pencil 迁移至 Figma，基于 Figma 6.2 版本对齐。**新增**：信源分工规则（1.3，静态文案以设计稿为准、动态错误以 PRD 为准）；验证码已填充态（VerifyCode-fill）和错误态（VerifyCode-Error）；登录错误状态拆分 password on/off 变体（APP 端）。**删除**：国家/地区选择器章节（原 2.2，本期不做）及 APP 端国家确认引导页（Onboarding-CountryConfirm）。**修改**：Login-Remembered PC 端保留 Remember me；VerifyCode 错误文案改为「Wrong code, Please Try again」；Login-LoadingState 移除"待补"标注（已补齐）；全文静态文案清理（页面元素只保留结构描述，具体文案参见设计稿）。章节重新编号（2.3→2.2 起）。设计稿索引从 21 项调整为 23 项（删 1 加 3） | 产品部 |
| V2.8 | 2026-06-03 | **修改**：重置密码成功后跳转逻辑优化（3.5）——若本地存在回访信息则跳转 Login-Remembered，否则跳转标准登录页并预填邮箱。**删除**：注册限频移除同一 IP 维度限制（6.5），仅保留设备指纹维度（避免共享 IP 误伤），同步更新注册流程步骤描述（2.1）；发信限频移除同一 IP 维度限制（6.6），仅保留同一邮箱维度；账号注销（4.6）改为运营代操作模式，删除用户端自助流程（页面元素、身份验证、操作流程、校验规则），保留注销后处理和数据保留策略；设计稿索引删除 AccountDeletion / A-AccountDeletion（23→21 项）。**新增**：冻结账号用户端处理——邮箱登录（3.2）和 OAuth 登录（3.3）分支流程新增"账号被冻结"分支；退出跳转（4.4）新增冻结场景；异常提示表（6.7）新增"账号被冻结"行。**修改**：注销数据处理策略（4.6）——移除 30 天冷静期，改为立即匿名化（PII 脱敏，记录保留不物理删除）；邮箱立即释放；deactivated_at 语义从"注销申请时间"改为"注销执行时间"。**统一术语**：全文"吊销"统一改为"终止"（与 ER 图 session.status 枚举"已终止"对齐）。**修改**：协议内容来源（2.6.1/2.6.2）从前端硬编码改为服务端管理+前端动态拉取，内容由法务提供、运营通过后台发布（详见用户管理模块 PRD）；协议版本检测（5.4）补充版本管理规则（递增整数，ToS 和 PP 独立版本号）、检测时机（登录时+会话级缓存）、独立更新提示逻辑。**自检修正**：新增全局页面流转（1.5）；协议子章节编号修正（2.5.1/2.5.2→2.6.1/2.6.2）；密码规则（2.5）去重改为引用 6.3；新增审计日志操作类型枚举定义（6.8，6 种操作类型）；新增协议类型枚举定义（5.4）；新增依赖与风险章节（七）；新增版本规划章节（八）；附录编号修正（八→九）。**模拟评审修正**：审计日志新增"重置密码"操作类型（6.8，6→7 种）；邮箱注册（2.2）和 OAuth 注册（2.3）补充 ConsentRecord 写入步骤；密码校验新增最大长度 64 字符（6.3）；登录态有效期规则新增 APP 端策略（3.6，默认 30 天）；邮箱校验补充 RFC 5321 标准和 254 字符上限（2.2）；注册限频（6.5）、发信限频（6.6）、重发机制（2.7）统一为"滑动窗口 60 分钟"；版本规划新增"年龄筛查（18+ 声明）"迭代方向（8.2） | 产品部 |
| V3.0 | 2026-06-09 | **新增**：架构预留章节（8.3）——运营后台与商家入驻的登录方式、用户角色模型（买家/商家/运营人员/纯运营人员）、认证与鉴权架构（身份认证一套、鉴权授权三套）、对当前 MVP 的 4 项预留要求（身份层独立、认证授权解耦、JWT 可扩展、OAuth 凭证可复用）；适用范围（1.2）补充范围说明；后续迭代方向（8.2）新增运营后台登录与 RBAC、商家入驻与商家后台两项 | 产品部 |
| V2.9 | 2026-06-04 | **新增**：OAuth 邮箱补充页（2.4 OAuthEmailSupplement）——Facebook 授权未返回邮箱时，要求用户补充邮箱并验证后才能完成注册；补充邮箱若已被注册则关联已有账号。**修改**：OAuth 注册主流程（2.3）新增"未获取邮箱→跳转邮箱补充页"分支（步骤 9）；Provider 差异表 Facebook 行更新为"无邮箱→跳转邮箱补充页"（删除原"标记待补邮箱"方案）。全局页面流转（1.5）新增邮箱补充页节点。设计稿索引新增 OAuthEmailSupplement / A-OAuthEmailSupplement（21→23 项，待设计）。章节重新编号（原 2.4~2.8→2.5~2.9）。**关联更新**：系统流程图 V7→V8（段③ OAuth认证新增"获取到邮箱?"判断节点，Facebook无邮箱走邮箱补充流程；Facebook MB分支简化为直接写入凭证表） | 产品部 |
