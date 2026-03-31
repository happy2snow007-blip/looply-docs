# Looply 用户系统 · 功能说明文档

> 版本：V2.5 MVP
> 更新日期：2026-03-31
> 文档负责人：产品部
> 状态：初稿

---

## 一、文档说明

### 1.1 文档目的

本文档为 Looply 海外电商平台用户系统 MVP 阶段的详细功能说明，作为设计、研发、测试的交付依据和验收标准。

### 1.2 适用范围

- 本期 MVP 覆盖：注册、登录、退出、密码管理、会话管理、安全风控六个模块
- 适用终端：Web PC 端、H5 移动端
- 目标用户：外部用户（买家）

### 1.3 术语说明

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

### 1.4 国家/地区选择器（Country Selector）

#### 功能描述

国家/地区选择器以模态弹窗形式呈现，用于用户选择所在国家/地区。在注册相关页面中作为触发入口（下拉样式），点击后弹出完整的国家选择弹窗。

#### 出现位置

**触发入口（下拉样式）：**

| 页面 | PC 端 | H5 端 |
|------|-------|-------|
| 注册页 | 右侧表单区域右上角 | 暂无 |
| 登录页 | 右侧表单区域右上角 | 暂无 |
| 回访登录页 | 右侧表单区域右上角 | 暂无 |

**触发入口元素：**

- 国旗 emoji（如 🇺🇸）
- 国家/地区名称（如 "United States"）
- 下拉箭头图标

#### 弹窗页面元素

- 半透明遮罩层（点击遮罩关闭弹窗）
- 弹窗卡片（480px 宽，居中显示，圆角 20px）
  - 标题栏：「Select your country」+ 关闭按钮（×）
  - 搜索框：placeholder「Search countries...」，带搜索图标，圆角 10px
  - 国家列表（可滚动）：
    - 每行：国旗 emoji + 国家名称，圆角 10px，内边距 14px 20px
    - 当前选中项：紫色高亮背景（#F0EAFF）+ 紫色文字 + 勾选图标
    - 未选中项：白色背景，hover 时显示浅灰背景
  - 底部确认栏：「Confirm」主按钮（与弹窗等宽，顶部分隔线）

#### MVP 支持的国家列表

| 国旗 | 国家名称 |
|------|----------|
| 🇺🇸 | United States |
| 🇬🇧 | United Kingdom |
| 🇩🇪 | Germany |
| 🇫🇷 | France |
| 🇮🇹 | Italy |
| 🇪🇸 | Spain |
| 🇯🇵 | Japan |

#### 交互说明

- 点击触发入口 → 弹出国家选择弹窗，遮罩层覆盖当前页面
- 搜索框支持按国家名称实时过滤列表
- 点击国家行 → 该行高亮为选中状态（紫色背景 + 勾选图标）
- 点击「Confirm」→ 确认选择，关闭弹窗，触发入口更新为选中的国家
- 点击关闭按钮（×）或遮罩层 → 取消选择，关闭弹窗，保持原选中值
- 默认值：根据用户 IP 自动识别，默认 United States
- 弹窗打开时，搜索框自动获取焦点

#### 校验规则

| 场景 | 规则 |
|------|------|
| 注册页 | MVP 阶段仅展示，不影响注册流程 |

#### 技术说明

- MVP 阶段：前端静态组件，国家列表硬编码，选择结果存储到用户 profile 的 `country_code` 字段
- 搜索为前端本地过滤，无需后端接口
- 后续迭代：接入 i18n 国际化框架，国家选择影响语言和地区配置

#### UI 关联

- PC 端：设计稿 CountrySelector
- H5 端：设计稿 H5/CountrySelector（底部弹出式，圆角顶部卡片）

---

## 二、注册模块

### 2.1 模块概述

- **模块目标**：完成新用户账户创建，提升首访转化率
- **优先级**：P0
- **入口**：首页「Sign Up」按钮、营销落地页引导
- **说明**：首页为登录/注册的统一入口，页面顶部提供「Sign In」和「Sign Up」按钮。首页设计稿见独立文件：PC 端 looply-home-PC.pen / H5 端 looply-home-H5.pen（位于「海外业务首页/UI/」目录）

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
6. 系统校验注册限频（同一 IP / 设备指纹）
7. 系统校验邮箱是否已注册
8. 系统执行风控检测（参见 六、5.1 风控检测规则）
9. 风控通过，发送 6 位验证码到用户邮箱
10. 跳转至验证码校验页面（VerifyCode）
11. 用户输入验证码，点击「Verify code」
12. 验证通过，创建账号，签发 Token，记录设备指纹并关联 Session
13. 自动登录并跳转至首页

**分支流程：**

- 邮箱格式错误 → 实时提示「Please enter a valid email address」
- 密码不符合规则 → 实时提示具体不符合项
- 邮箱已被注册 → 提示「This email is already registered」，引导跳转登录页
- 注册限频触发 → 提示「Too many attempts, please try again later」
- 风控拦截 → 拦截或要求额外验证
- 验证码错误 → 提示「Invalid verification code」
- 验证码过期 → 提示「Code has expired. Please request a new one.」

#### 校验规则

| 字段 | 规则 | 校验时机 |
|------|------|----------|
| 邮箱 | 符合邮箱格式（xxx@xxx.xx） | 失焦时前端校验 + 提交时后端校验 |
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
- H5 端：设计稿 H5/Register

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
9. 系统判断邮箱是否已被邮箱注册方式占用
   - 已注册：关联已有账号，写入 OAuth 绑定记录
   - 未注册：创建新账号
10. 根据 Provider 类型执行差异化处理（参见下方 Provider 差异表）
11. 签发 Token，记录设备指纹并关联 Session
12. 跳转至首页

**分支流程：**

- 用户取消授权 → 返回注册页，无提示
- 风控拦截 → 拦截或要求额外验证
- 第三方服务不可用 → 提示「{Provider} sign-in is temporarily unavailable」

#### Provider 差异处理

| Provider | email 处理 | name 处理 | 特殊说明 |
|----------|-----------|-----------|----------|
| Google | email 写入凭证表 | 预填昵称到 user_profile.nickname | 标准流程 |
| Apple | 给了真实邮箱 → 写入凭证表；relay 邮箱 → 不写入 | 预填昵称（仅首次授权返回 firstName + lastName） | Apple Hide My Email 场景需特殊处理 |
| Facebook | 有邮箱 → 写入凭证表；无邮箱 → 标记待补邮箱 | 预填昵称 | 无邮箱用户允许注册，后续引导绑定（参见待办） |

#### 技术说明

- 使用 OAuth 2.0 授权码模式
- 服务端实现统一的第三方登录适配层（Provider Pattern），新增登录方式时仅需实现对应 Provider
- Client Secret 仅存储在服务端，禁止暴露到前端
- state 参数必须校验，防止 CSRF 攻击
- 授权码仅可使用一次，有效期极短

#### UI 关联

- 注册页中的「Continue with Google / Apple / Facebook」按钮

---

### 2.4 统一注册入口

#### 功能描述

注册页面提供统一入口，整合邮箱注册和三方快捷注册，用户可自由选择。

#### 页面元素（PC 端）

- 标题「Create your account」
- 副标题「Shop verified luxury, delivered to you」
- 邮箱输入框（label: Email）
- 密码输入框（label: Password，带显示/隐藏切换）
- 密码提示「At least 8 characters with a mix of letters, numbers, and symbols」
- 「Sign up」主按钮（紫色）
- 分隔线「or」
- 「Continue with Google」按钮
- 「Continue with Apple」按钮
- 「Continue with Facebook」按钮
- 协议提示文案「By signing up, you agree to our Terms and Privacy Policy」（Clickwrap 方式，点击按钮即视为同意）
- 底部切换「Already have an account? Sign in」

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

| 状态 | 说明 | 设计稿（PC） | 设计稿（H5） |
|------|------|-------------|-------------|
| 默认状态 | 按钮始终可点击，采用 Clickwrap 协议同意方式 | Register | H5/Register |

---

### 2.5 密码设置

#### 功能描述

用户在注册时设置账号密码，密码需满足安全性要求。

#### 密码规则

- 最少 8 个字符
- 必须包含大写字母（A-Z）
- 必须包含小写字母（a-z）
- 必须包含数字（0-9）
- 可选：包含特殊字符

#### 交互说明

- 密码输入框默认隐藏内容，提供「显示/隐藏」切换（eye-off / eye 图标）
- 密码框下方显示规则提示文案

---

### 2.6 协议承接

#### 功能描述

注册流程中嵌入服务条款（ToS）和隐私政策（Privacy Policy）的确认环节，确保合规。

#### 交互说明

**注册页（邮箱注册）：**
- 采用 Clickwrap 方式：三方登录按钮下方展示协议提示文案「By creating an account, you agree to our Terms and Privacy Policy」
- 「Terms」和「Privacy Policy」为可点击链接，点击后跳转至对应页面
- 用户点击「Sign up」按钮即视为同意协议，无需单独勾选
- 协议页面支持返回注册页，保留已填写信息

**登录页：**
- 底部展示文案（无复选框）：「By signing in, you agree to our Terms and Privacy Policy」
- 「Terms」和「Privacy Policy」为可点击链接

#### 合规要求

- 注册页和登录页均采用 Clickwrap 方式（点击操作按钮即视为同意），符合美国市场主流合规实践
- 记录用户同意的时间戳和协议版本号
- 后续如进入欧洲市场（GDPR），需改为 Active Opt-in 方式（主动勾选复选框），届时按地区差异化处理

#### 2.6.1 服务条款页面（Terms of Service）

##### 功能描述

展示 Looply 平台的服务条款完整内容，用户在注册前可查阅。

##### 入口

- 注册页 / 登录页协议文案中的「Terms of Service」/「Terms」链接
- 页面底部（Footer）链接（未来扩展）

##### 页面元素

- 顶部导航栏：左侧「Back」按钮（lucide arrow-left 图标 + 文字） + 右侧 Looply Logo，底部分隔线
- 内容区域：协议正文（长文本，支持滚动）
- 最后更新日期

##### 内容来源

- MVP 阶段：前端静态页面，内容由法务提供，硬编码在前端
- 后续迭代：可接入 CMS 管理，支持动态更新

##### 交互说明

- 从注册页点击链接进入，新页面打开（非弹窗）
- 返回注册页时，保留用户已填写的表单信息
- PC 端和 H5 端共用同一份协议内容，仅布局适配不同
- 纯展示页面，无需登录即可访问

##### UI 关联

- PC 端：设计稿 TermsOfService
- H5 端：设计稿 H5/TermsOfService

#### 2.6.2 隐私政策页面（Privacy Policy）

##### 功能描述

展示 Looply 平台的隐私政策完整内容，告知用户个人数据的收集、使用和保护方式。

##### 入口

- 注册页 / 登录页协议文案中的「Privacy Policy」链接
- 页面底部（Footer）链接（未来扩展）

##### 页面元素

- 顶部导航栏：左侧「Back」按钮（lucide arrow-left 图标 + 文字） + 右侧 Looply Logo，底部分隔线
- 内容区域：隐私政策正文（长文本，支持滚动）
- 最后更新日期

##### 内容来源

- MVP 阶段：前端静态页面，内容由法务提供，硬编码在前端
- 后续迭代：可接入 CMS 管理，支持动态更新

##### 交互说明

- 从注册页点击链接进入，新页面打开（非弹窗）
- 返回注册页时，保留用户已填写的表单信息
- PC 端和 H5 端共用同一份协议内容，仅布局适配不同
- 纯展示页面，无需登录即可访问

##### 合规要求

- 隐私政策内容需符合目标市场的数据保护法规（如 GDPR、CCPA 等）
- 内容更新时需通知已注册用户（后续迭代）

##### UI 关联

- PC 端：设计稿 PrivacyPolicy
- H5 端：设计稿 H5/PrivacyPolicy

---

### 2.7 邮箱验证码校验

#### 功能描述

用户在注册或忘记密码流程中，通过输入系统发送至邮箱的 6 位数字验证码完成身份验证。注册场景和忘记密码场景共用同一个 VerifyCode 页面。

#### 使用场景

| 场景 | 触发时机 | 验证通过后 |
|------|----------|------------|
| 邮箱注册 | 用户提交注册信息后 | 创建账号，自动登录跳转首页 |
| 忘记密码 | 用户提交邮箱后 | 跳转至重置密码页面 |

#### 页面元素

- 邮件图标（紫色圆形背景 + mail 图标）
- 标题「Check your email」
- 副标题「We sent a 6-digit code to your email. Enter it below to verify your account.」
- 6 位验证码输入框（每位独立输入框，48×56px，圆角 12px，当前焦点框高亮）
- 「Verify code」主按钮
- 重发行「Didn't receive the code? Resend」
- 底部「Back」返回链接（左侧 lucide arrow-left 图标 + 文字）

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
| 冷却时间 | 发送后 60 秒内不可重发，按钮显示倒计时 |
| 每小时上限 | 同一邮箱每小时最多发送 5 次 |
| 达到上限 | 提示「Too many requests. Please try again later.」 |

#### 交互说明

- 输入框自动聚焦第一位，输入后自动跳转下一位
- 支持粘贴完整 6 位验证码，自动填充所有输入框
- 输入完 6 位后「Verify code」按钮可点击
- 删除键可回退到上一位输入框

#### 异常处理

| 异常场景 | 处理方式 |
|----------|----------|
| 验证码错误 | 输入框下方提示「Invalid verification code」，清空输入框 |
| 验证码过期 | 提示「Code has expired. Please request a new one.」 |
| 连续 5 次错误 | 提示「Too many failed attempts. Please request a new code.」，当前验证码失效 |
| 网络请求失败 | Toast 提示「Network error, please try again」 |

#### UI 关联

- PC 端：设计稿 VerifyCode
- H5 端：设计稿 H5/VerifyCode

---

### 2.8 价值点展示

#### 功能描述

注册/登录页面左侧（PC端）展示 Looply 平台的品牌视觉和核心价值主张，提升注册意愿。

#### 展示内容

- 全屏品牌背景图（660px 宽）
- 品牌 Logo（白色透明底）
- 品牌价值主张文案

#### 交互说明

- 纯展示区域，无交互操作
- PC 端位于表单左侧，固定 660px 宽度
- H5 端不展示（空间有限，优先展示表单）

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

- 标题「Welcome back」
- 副标题「Sign in to your Looply account」
- 邮箱输入框（label: Email，placeholder: Enter your email）
- 密码输入框（label: Password，placeholder: Enter your password，带显示/隐藏切换）
- Remember me 复选框 + 「Forgot password?」链接（同一行，两端对齐）
- 「Sign in」主按钮（紫色）
- 分隔线「or」
- 「Continue with Google」按钮
- 「Continue with Apple」按钮
- 「Continue with Facebook」按钮
- 底部协议文案「By signing in, you agree to our Terms and Privacy Policy」
- 底部切换「Don't have an account? Sign up」

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

| 状态 | 说明 | 设计稿 |
|------|------|--------|
| 默认状态 | 空表单 | Login |
| 密码可见 | 点击 eye 图标后密码明文显示 | Login-PasswordVisible |
| 错误状态 | 输入框红色边框 + 错误提示 + 错误 Toast | Login-ErrorState |
| 加载状态 | 按钮显示 loading 动画 | Login-LoadingState |

#### UI 关联

- PC 端：设计稿 Login / Login-PasswordVisible / Login-ErrorState / Login-LoadingState
- H5 端：设计稿 H5/Login / H5/Login-PasswordVisible / H5/Login-ErrorState / H5/Login-LoadingState

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

- 钥匙图标（紫色圆形背景 + key-round 图标）
- 标题「Forgot password?」
- 副标题「No worries. Enter your email and we'll send you a code to reset your password.」
- 邮箱输入框（label: Email address，placeholder: Enter your email）
- 「Send reset code」主按钮
- 底部「Back」返回链接（左侧 lucide arrow-left 图标 + 文字）

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
- H5 端：设计稿 H5/ForgotPassword

---

### 3.5 重置密码

#### 功能描述

用户通过验证码校验后，设置新密码。

#### 前置条件

- 用户已通过忘记密码流程中的验证码校验（参见 2.8）

#### 页面元素

- 锁图标（紫色圆形背景 + lock-keyhole 图标）
- 标题「Set new password」
- 副标题「Your new password must be at least 8 characters and include a number and a special character.」
- 新密码输入框（label: New password，placeholder: Enter new password，带显示/隐藏切换）
- 确认密码输入框（label: Confirm password，placeholder: Confirm new password，带显示/隐藏切换）
- 「Reset password」主按钮
- 底部「Back」返回链接（左侧 lucide arrow-left 图标 + 文字）

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
10. 提示「Password updated successfully」
11. 自动跳转至登录页

**分支流程：**

- 密码不符合规则 → 提示具体不符合项
- 确认密码不一致 → 提示「Passwords do not match」
- 新密码与旧密码相同 → 提示「New password must be different from your current password」
- 重置会话过期（验证码校验通过后 15 分钟内未完成重置） → 提示「Session expired. Please start over.」，跳转至忘记密码页面

#### 密码规则

- 与注册时密码规则一致（参见 2.5 密码设置）

#### UI 关联

- PC 端：设计稿 ResetPassword
- H5 端：设计稿 H5/ResetPassword

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
| 勾选 Remember Me | 短期（如 15 分钟） | 30 天 | 30 天内 refresh_token 可换取新 access_token |
| 未勾选 | 短期（如 15 分钟） | 会话级 | 浏览器关闭后 refresh_token 失效 |
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

#### 页面元素（与标准登录页的差异）

| 元素 | 标准登录页（Login） | 回访登录页（Login-Remembered） |
|------|---------------------|-------------------------------|
| 顶部操作 | 无 | 「Not you? Use another account」链接 |
| 用户头像 | 无 | 显示用户首字母圆形头像（72×72px，紫色背景 #F0EAFF） |
| 标题 | Welcome back | Welcome back, {用户名} |
| 副标题 | Sign in to your Looply account | 显示用户邮箱 |
| 邮箱输入框 | 空，需用户输入 | 无（已识别用户） |
| 密码输入框 | 空 | 空，需用户输入 |
| Remember me | 未勾选 | 无（已是回访状态） |
| Forgot password | 有 | 有 |
| OAuth 按钮 | 有 | 无 |
| 底部切换 | Don't have an account? Sign up | 无 |

#### 交互说明

- 点击「Use another account」→ 清除本地回访信息，跳转至标准登录页
- 密码输入框自动获取焦点，减少操作步骤
- 其余交互逻辑与标准登录页一致（参见 3.2）

#### 技术说明

- 回访用户识别基于本地存储（localStorage），存储字段：邮箱、用户名、首字母
- 用户主动退出时清除本地存储的回访信息

#### UI 关联

- PC 端：设计稿 Login-Remembered
- H5 端：设计稿 H5/Login-Remembered

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
- 弹窗卡片（420×260px，圆角 16px，居中显示）
  - 标题「Sign Out」
  - 说明文案「Are you sure you want to sign out of your Looply account?」
  - 「Yes, Sign Out」主按钮（紫色）
  - 「Cancel」次按钮（灰色边框样式）
  - 两个按钮并排显示，间距 12px

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
- H5 端：设计稿 H5/LogoutModal

---

### 4.3 退出入口

#### 功能描述

在合适的位置提供退出登录入口，确保用户可发现。

#### 入口位置

| 终端 | 入口位置 |
|------|----------|
| PC 端 | 页面右上角用户头像 → 下拉菜单 → 「Sign Out」 |
| H5 端 | 「我的」页面底部 → 「Sign Out」按钮 |

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
| 协议版本更新拒绝同意 | 强制退出登录，跳转至首页 |

> **备注**：首页设计稿见独立文件：PC 端 looply-home-PC.pen / H5 端 looply-home-H5.pen（位于「海外业务首页/UI/」目录）。

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

用户主动发起永久删除账号操作。注销后账号数据不可恢复，需通过身份验证后方可执行。

#### 前置条件

- 用户已登录状态
- 用户无进行中的订单（活跃订单需先完成或取消）

#### 入口

- 账号设置页面 → 「Delete Account」（具体设置页尚未设计，仅作示意）

#### 页面元素

- 警告图标（红色三角感叹号，红色圆形背景 #FEF2F2）
- 标题「Delete your account」
- 说明文案「This action is permanent and cannot be undone. All your data, listings, and purchase history will be deleted.」
- 红色警告区域（背景 #FEF2F2，圆角 10px）：
  - 警告图标（circle-alert）+ 警告文案「You will lose access to all purchases, seller earnings, and saved items. Active orders must be completed before deletion.」
- 密码确认输入框：
  - 标签「Password」
  - placeholder「Enter your password to confirm」
  - 支持密码显示/隐藏切换
- 「Permanently delete account」主按钮（红色 #EF4444）
- 「Cancel」次按钮（灰色边框样式，与主按钮等宽）

#### 操作流程

**主流程：**

1. 用户进入账号注销页面
2. 阅读注销警告信息
3. 系统校验身份验证方式：
   - 有密码的用户 → 输入密码验证
   - 仅 OAuth 注册的用户（无密码）→ 重新进行 OAuth 授权验证
4. 点击「Permanently delete account」
5. 系统校验身份
6. 身份验证通过 → 标记账号 status = 注销，记录 deactivated_at
7. 吊销所有 Session
8. 写入审计日志（注销）
9. 清除本地登录态，跳转至首页
10. 展示 Toast 提示「Your account has been deleted」

**分支流程：**

- 密码错误 → 提示「Incorrect password」，不执行注销
- OAuth 重新授权失败 → 提示「Verification failed」，不执行注销
- 存在进行中的订单 → 提示「Please complete or cancel your active orders before deleting your account.」，按钮置灰
- 用户点击「Cancel」→ 返回上一页面
- 网络请求失败 → Toast 提示「Network error, please try again」

#### 校验规则

| 字段 | 规则 | 校验时机 |
|------|------|----------|
| 密码 | 非空 | 提交时前端校验 |
| 密码 | 与当前账号密码匹配 | 提交时后端校验 |
| 活跃订单 | 无进行中的订单 | 进入页面时后端校验 |

#### 注销后处理

| 处理项 | 说明 |
|--------|------|
| 登录态 | 立即清除所有 Token 和 Cookie |
| 用户数据 | 按数据保留策略处理（见下方） |
| 第三方绑定 | 解除所有 OAuth 绑定关系 |
| 邮箱释放 | 注销后邮箱可用于重新注册（需等待冷却期） |

#### 数据保留策略

| 数据类型 | 处理方式 | 说明 |
|----------|----------|------|
| 账号信息 | 软删除，保留 30 天后物理删除 | 防误操作，支持 30 天内联系客服恢复 |
| 交易记录 | 永久保留（脱敏） | 财务合规要求 |
| 用户内容（商品、评价） | 下架但保留 | 涉及其他用户的交易记录完整性 |
| 个人信息（姓名、地址等） | 30 天后物理删除 | GDPR/CCPA 合规 |

#### 注销冷静期说明

- 注销后 30 天内可联系客服恢复
- 超过 30 天数据永久删除
- 冷静期内账号不可登录

#### 安全说明

- 有密码用户必须通过密码验证身份
- 仅 OAuth 注册用户（无密码）通过重新 OAuth 授权验证身份
- 注销操作记录到审计日志
- 30 天冷却期内，使用同一邮箱注册视为新账号，不恢复旧数据

#### UI 关联

- PC 端：设计稿 AccountDeletion
- H5 端：设计稿 H5/AccountDeletion

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
8. 吊销所有其他 Session（当前 Session 保留）
9. 写入审计日志（改密码）
10. 提示「Password updated successfully」

**分支流程：**

- 旧密码错误 → 提示「Incorrect password」
- 新旧密码相同 → 提示「New password must be different from your current password」
- 新密码不符合规则 → 提示具体不符合项

#### 密码规则

- 与注册时密码规则一致（参见 2.5 密码设置）

#### 安全说明

- 修改密码后，除当前 Session 外的所有 Session 立即失效
- 其他设备需重新登录

#### UI 关联

- PC 端：设计稿 ChangePassword
- H5 端：设计稿 H5/ChangePassword

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
   - 已吊销 → 返回 401（已吊销）
5. 签发新 access_token
6. 滑动续期 refresh_token（重新计算过期时间）
7. 刷新完成，前端用新 access_token 重试原请求

#### 异常处理

| 异常场景 | 处理方式 |
|----------|----------|
| refresh_token 无效/过期 | 返回 401，跳转首页，提示「Session expired. Please sign in again.」 |
| Session 已被吊销 | 返回 401，跳转首页，提示「Session expired. Please sign in again.」 |
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

当平台更新服务条款或隐私政策时，系统在用户访问任意页面时检测协议版本变化，弹窗要求用户确认新版协议。

#### 触发条件

- 用户已登录状态
- 用户访问任意页面时
- 系统检测到协议版本有更新（用户上次同意的版本 < 当前最新版本）

#### 操作流程

**主流程：**

1. 用户访问任意页面
2. 系统检测协议版本是否有更新
   - 无更新 → 正常访问
   - 有更新 → 弹出协议更新弹窗
3. 用户阅读并点击「同意」
4. 系统提交同意请求
5. 写入 ConsentRecord（记录协议版本 + 国家）
6. 正常访问页面

**分支流程：**

- 用户拒绝同意 → 强制退出登录，跳转至首页

#### 技术说明

- 协议版本号存储在服务端配置中
- 用户同意记录存储在 ConsentRecord 表，包含协议版本号、同意时间、用户国家
- 前端在每次页面加载时调用接口检查协议版本（可缓存，降低请求频率）

#### UI 关联

- PC 端：设计稿 ConsentUpdateModal
- H5 端：设计稿 H5/ConsentUpdateModal

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
- 弹窗卡片（居中显示，圆角 20px，白色背景）
  - 警告图标（红色圆形背景 + shield-alert 图标，居中）
  - 标题「Sign-in blocked」（居中）
  - 说明文案「We noticed a sign-in attempt from an unusual location. For your security, this request has been blocked.」（居中）
  - 「Back to sign in」按钮（灰色边框样式，与弹窗等宽）

##### 交互说明

- 弹窗为只读状态，用户无法绕过拦截
- 点击遮罩层不关闭弹窗（强制阅读）
- 点击「Back to sign in」跳转至标准登录页

##### UI 关联

- PC 端：设计稿 RiskBlocked
- H5 端：设计稿 H5/RiskBlocked

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
- H5 端：设计稿 H5/VerifyCode-CrossStateLogin

---

### 6.3 密码校验

#### 功能描述

对用户设置的密码进行安全性校验，确保密码强度达标。

#### 校验规则

| 规则 | 说明 |
|------|------|
| 最小长度 | 8 个字符 |
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

限制同一 IP / 设备在短时间内的注册请求次数，防止批量注册。

#### 规则

| 维度 | 限制 |
|------|------|
| 同一 IP | 每小时最多注册 5 个账号 |
| 同一设备指纹 | 每小时最多注册 3 个账号 |

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
| 同一邮箱 | 每小时最多发送 5 封 |
| 同一 IP | 每小时最多触发 10 次发送 |

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
| 登录密码错误 | Incorrect email or password | 输入框下方错误提示 |
| 邮箱格式错误 | Please enter a valid email address | 输入框下方错误提示 |
| 网络错误 | Network error, please try again | Toast 提示 |
| 服务端错误 | Something went wrong, please try again later | Toast 提示 |
| 注册被限频 | Too many attempts, please try again later | Toast 提示 |
| 风控拦截（跨国/高风险） | Unusual activity detected. Your request has been blocked for security reasons. | 拦截弹窗 |
| 风控异地验证（跨州） | We noticed a login from a new location. Please verify your identity. | 页面顶部 Banner + 跳转邮箱验证码页 |
| 暴力破解触发 CAPTCHA | Please complete the verification to continue. | 弹出图形验证码（CAPTCHA） |

#### 设计原则

- 错误提示使用红色文字 + 错误图标
- 安全相关提示不暴露系统内部逻辑（如不区分"邮箱不存在"和"密码错误"）
- 所有提示文案需支持多语言

---

## 七、附录

### 7.1 设计稿索引

| 页面 | PC 端设计稿 | H5 端设计稿 |
|------|------------|------------|
| 登录 | Login | H5/Login |
| 登录-密码可见状态 | Login-PasswordVisible | H5/Login-PasswordVisible |
| 登录-错误状态 | Login-ErrorState | H5/Login-ErrorState |
| 登录-加载状态 | Login-LoadingState | H5/Login-LoadingState |
| 回访登录 | Login-Remembered | H5/Login-Remembered |
| 注册 | Register | H5/Register |
| 验证码 | VerifyCode | H5/VerifyCode |
| 验证码-跨州异地登录 | VerifyCode-CrossStateLogin | H5/VerifyCode-CrossStateLogin |
| 忘记密码 | ForgotPassword | H5/ForgotPassword |
| 重置密码 | ResetPassword | H5/ResetPassword |
| 隐私政策 | PrivacyPolicy | H5/PrivacyPolicy |
| 服务条款 | TermsOfService | H5/TermsOfService |
| 国家选择器（弹窗） | CountrySelector | H5/CountrySelector |
| 账号注销 | AccountDeletion | H5/AccountDeletion |
| 退出确认（弹窗） | LogoutModal | H5/LogoutModal |
| 风控拦截（弹窗） | RiskBlocked | H5/RiskBlocked |
| 密码修改 | ChangePassword | H5/ChangePassword |
| 协议版本更新（弹窗） | ConsentUpdateModal | H5/ConsentUpdateModal |

### 7.2 接口清单（参考）

| 接口 | 方法 | 说明 |
|------|------|------|
| /api/auth/register | POST | 邮箱注册（提交注册信息，发送验证码） |
| /api/auth/register/verify | POST | 注册验证码校验，校验通过后创建账号 |
| /api/auth/login | POST | 邮箱密码登录 |
| /api/auth/logout | POST | 退出登录 |
| /api/auth/google | GET | Google OAuth 跳转 |
| /api/auth/google/callback | GET | Google OAuth 回调 |
| /api/auth/apple | GET | Apple OAuth 跳转 |
| /api/auth/apple/callback | GET | Apple OAuth 回调 |
| /api/auth/facebook | GET | Facebook OAuth 跳转 |
| /api/auth/facebook/callback | GET | Facebook OAuth 回调 |
| /api/auth/forgot-password | POST | 发送忘记密码验证码 |
| /api/auth/forgot-password/verify | POST | 忘记密码验证码校验 |
| /api/auth/reset-password | POST | 重置密码 |
| /api/auth/change-password | POST | 修改密码（登录态） |
| /api/auth/verify-code/resend | POST | 重新发送验证码 |
| /api/auth/token/refresh | POST | 刷新 access_token |
| /api/auth/delete-account | POST | 账号注销（需身份验证） |
| /api/auth/consent/check | GET | 检查协议版本是否需要更新 |
| /api/auth/consent/agree | POST | 提交协议同意记录 |

### 7.3 修订记录

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
| V2.1 | 2026-03-31 | 补齐 H5 端设计稿关联（15 个页面更新为实际设计稿）；新增 4 个页面说明：注册置灰状态（Register-DisabledState）、OAuth 补充信息置灰状态（OAuthSupplementary-DisabledState）、风控拦截页（RiskBlocked）、跨州异地登录验证页（VerifyCode-CrossStateLogin）；设计稿索引从 17 项扩展为 21 项 | 产品部 |
| V2.2 | 2026-03-31 | 关联首页设计稿（looply-home-PC.pen / looply-home-H5.pen），移除 3 处"首页尚未设计"备注 | 产品部 |
| V2.3 | 2026-03-31 | 删除 OAuth 补充信息页（OAuthSupplementary）：移除章节 2.7（原）、设计稿索引 2 项、接口 /api/auth/oauth/supplement；OAuth 注册完成后直接跳转首页；章节重新编号（2.9→2.8） | 产品部 |
| V2.4 | 2026-03-31 | H5 端设计稿优化：风控拦截页（RiskBlocked）改为弹窗样式；H5/Login-ErrorState 移除冗余顶部错误 Banner；H5/Register 简化密码区域（移除确认密码和密码规则，改为单行提示）；全部 icon 居中展示 | 产品部 |
| V2.5 | 2026-03-31 | 同步 H5 设计稿变更：返回链接文案统一为「Back」+ lucide arrow-left 图标（涉及 VerifyCode、ForgotPassword、ResetPassword）；服务条款/隐私政策页面 TopBar 布局修正为「左侧 Back 按钮 + 右侧 Logo」；AccountDeletion Cancel 改为按钮样式（Button/Outline） | 产品部 |
