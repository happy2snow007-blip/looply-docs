# Looply 用户系统 · 功能说明文档

> 版本：V1.7 MVP
> 更新日期：2026-03-30
> 文档负责人：产品部
> 状态：初稿

---

## 一、文档说明

### 1.1 文档目的

本文档为 Looply 海外电商平台用户系统 MVP 阶段的详细功能说明，作为设计、研发、测试的交付依据和验收标准。

### 1.2 适用范围

- 本期 MVP 覆盖：注册、登录、退出、安全风控四个模块
- 适用终端：Web PC 端、H5 移动端
- 目标用户：外部用户（买家）

### 1.3 术语说明

| 术语 | 说明 |
|------|------|
| OAuth 2.0 | 开放授权协议，用于第三方登录 |
| Session | 用户会话，用于维持登录状态 |
| Token | 用户身份凭证，用于接口鉴权 |
| ToS | Terms of Service，服务条款 |
| Remember Me | 登录态保持，免密登录 |

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
| OAuth 补充信息页 | 表单中 Country / Region 字段 | 暂无 |

**触发入口元素：**

- 国旗 emoji（如 🇺🇸）
- 国家/地区名称（如 "United States"）
- 下拉箭头图标

#### 弹窗页面元素

- 半透明遮罩层（点击遮罩关闭弹窗）
- 弹窗卡片（480px 宽，居中显示）
  - 标题栏：「Select your country」+ 关闭按钮（×）
  - 搜索框：placeholder「Search countries...」，带搜索图标
  - 国家列表（可滚动）：
    - 每行：国旗 emoji + 国家名称
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
| OAuth 补充信息页 | 必选字段，未选择时「Complete Setup」按钮置灰 |

#### 技术说明

- MVP 阶段：前端静态组件，国家列表硬编码，选择结果存储到用户 profile 的 `country_code` 字段
- 搜索为前端本地过滤，无需后端接口
- 后续迭代：接入 i18n 国际化框架，国家选择影响语言和地区配置

#### UI 关联

- PC 端：设计稿 Screen/CountrySelector（模态弹窗）
- H5 端：待设计

---

## 二、注册模块

### 2.1 模块概述

- **模块目标**：完成新用户账户创建，提升首访转化率
- **优先级**：P0
- **入口**：首页「Sign Up」按钮、营销落地页引导
- **说明**：首页为登录/注册的统一入口，页面顶部提供「Sign In」和「Sign Up」按钮。（首页尚未设计，以下描述仅作示意）

### 2.2 邮箱注册

#### 功能描述

用户通过邮箱地址和密码创建 Looply 账号。

#### 前置条件

- 用户未登录状态
- 用户尚未拥有 Looply 账号

#### 操作流程

**主流程：**

1. 用户点击「Sign Up」进入注册页面
2. 用户输入邮箱地址
3. 用户设置密码（输入两次确认）
4. 用户勾选「同意服务条款和隐私政策」
5. 用户点击「Create Account」提交注册
6. 系统校验信息，发送 6 位验证码到用户邮箱
7. 跳转至验证码校验页面（VerifyCode）
8. 用户输入验证码，点击「Verify code」
9. 验证通过，创建账号，自动登录并跳转至首页

**分支流程：**

- 邮箱已被注册 → 提示「This email is already registered」，引导跳转登录页
- 邮箱格式错误 → 实时提示「Please enter a valid email address」
- 密码不符合规则 → 实时提示具体不符合项
- 未勾选协议 → 按钮置灰不可点击
- 验证码错误 → 提示「Invalid verification code」
- 验证码过期 → 提示「Code has expired. Please request a new one.」

#### 校验规则

| 字段 | 规则 | 校验时机 |
|------|------|----------|
| 邮箱 | 符合邮箱格式（xxx@xxx.xx） | 失焦时前端校验 + 提交时后端校验 |
| 邮箱 | 未被已有账号占用 | 提交时后端校验 |
| 密码 | 至少 8 位 | 实时前端校验 |
| 密码 | 包含大小写字母和数字 | 实时前端校验 |
| 确认密码 | 与密码一致 | 实时前端校验 |
| 协议勾选 | 必须勾选 | 前端校验 |

#### 异常处理

| 异常场景 | 处理方式 |
|----------|----------|
| 网络请求失败 | Toast 提示「Network error, please try again」 |
| 服务端错误 | Toast 提示「Something went wrong, please try again later」 |
| 注册被限频（风控拦截） | 提示「Too many attempts, please try again later」 |

#### UI 关联

- PC 端：设计稿 Screen/Register
- H5 端：设计稿 H5/Register

---

### 2.3 Google 快捷注册

#### 功能描述

用户通过 Google 账号一键创建 Looply 账号，降低注册门槛，提升转化。

#### 前置条件

- 用户未登录状态
- 用户拥有 Google 账号

#### 操作流程

**主流程：**

1. 用户点击「Continue with Google」按钮
2. 系统跳转至 Google OAuth 授权页面
3. 用户在 Google 页面选择账号并授权
4. Google 回调返回用户信息（邮箱、头像、昵称）
5. 系统判断该 Google 账号是否已关联 Looply 账号
   - 未关联：自动创建新账号，绑定 Google 信息
   - 已关联：直接登录该账号
6. 跳转至首页

**分支流程：**

- 用户取消 Google 授权 → 返回注册页，无提示
- Google 返回的邮箱已被邮箱注册方式占用 → 提示「This email is already registered. Please sign in with your password or link your Google account.」
- Google 服务不可用 → 提示「Google sign-in is temporarily unavailable」

#### 技术说明

- 使用 OAuth 2.0 授权码模式
- 需获取用户 email、profile scope
- 回调地址需在 Google Console 配置

#### UI 关联

- 注册页中的「Continue with Google」按钮

---

### 2.4 统一注册入口

#### 功能描述

注册页面提供统一入口，整合邮箱注册和 Google 快捷注册两种方式，用户可自由选择。

#### 交互说明

- 页面默认展示邮箱注册表单
- 表单下方通过分隔线「or」连接 Google 注册按钮
- 页面底部提供「Already have an account? Sign in」链接跳转登录页

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

- 密码输入框默认隐藏内容，提供「显示/隐藏」切换
- 确认密码不一致时实时提示

---

### 2.6 协议承接

#### 功能描述

注册流程中嵌入服务条款（ToS）和隐私政策（Privacy Policy）的确认环节，确保合规。

#### 交互说明

- 注册表单底部展示复选框 + 协议文案：「I agree to the Terms of Service and Privacy Policy」
- 「Terms of Service」和「Privacy Policy」为可点击链接，点击后跳转至对应页面
- 未勾选时「Create Account」按钮置灰不可点击
- 协议页面支持返回注册页，保留已填写信息

#### 合规要求

- 必须为主动勾选（opt-in），不可默认勾选
- 记录用户同意的时间戳和协议版本号

#### 2.6.1 服务条款页面（Terms of Service）

##### 功能描述

展示 Looply 平台的服务条款完整内容，用户在注册前可查阅。

##### 入口

- 注册页协议文案中的「Terms of Service」链接
- 页面底部（Footer）链接（未来扩展）

##### 页面元素

- 页面标题「Terms of Service」
- 协议正文内容区域（长文本，支持滚动）
- 最后更新日期
- 返回操作（浏览器返回 / 页面返回按钮）

##### 内容来源

- MVP 阶段：前端静态页面，内容由法务提供，硬编码在前端
- 后续迭代：可接入 CMS 管理，支持动态更新

##### 交互说明

- 从注册页点击链接进入，新页面打开（非弹窗）
- 返回注册页时，保留用户已填写的表单信息
- PC 端和 H5 端共用同一份协议内容，仅布局适配不同
- 纯展示页面，无需登录即可访问

##### UI 关联

- PC 端：设计稿 Screen/TermsOfService
- H5 端：设计稿 H5/TermsOfService

#### 2.6.2 隐私政策页面（Privacy Policy）

##### 功能描述

展示 Looply 平台的隐私政策完整内容，告知用户个人数据的收集、使用和保护方式。

##### 入口

- 注册页协议文案中的「Privacy Policy」链接
- 页面底部（Footer）链接（未来扩展）

##### 页面元素

- 页面标题「Privacy Policy」
- 隐私政策正文内容区域（长文本，支持滚动）
- 最后更新日期
- 返回操作（浏览器返回 / 页面返回按钮）

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

- PC 端：设计稿 Screen/PrivacyPolicy
- H5 端：设计稿 H5/PrivacyPolicy

---

### 2.7 价值点展示

#### 功能描述

注册页面左侧（PC端）或顶部（H5端）展示 Looply 平台的核心价值主张，提升注册意愿。

#### 展示内容

- 品牌 Logo
- 主标题：「Start your global e-commerce journey」
- 副标题：平台优势描述
- 品牌视觉元素/插图

#### 交互说明

- 纯展示区域，无交互操作
- PC 端位于注册表单左侧，占页面约 40% 宽度
- H5 端不展示（空间有限，优先展示表单）

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

- 邮件图标（紫色圆形背景）
- 标题「Check your email」
- 副标题「We sent a 6-digit code to {用户邮箱}」
- 6 位验证码输入框（每位独立输入框，当前焦点框高亮）
- 「Verify code」主按钮
- 重发行「Didn't receive a code? Resend (倒计时)」
- 底部「Back to sign in」返回链接

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

- PC 端：设计稿 Screen/VerifyCode
- H5 端：设计稿 H5/VerifyCode

---

### 2.9 OAuth 补充信息页（OAuthSupplementary）

#### 功能描述

用户通过第三方登录（Google/Apple/Facebook）首次注册后，引导补充必要的个人信息（显示名称、国家/地区），完善用户档案。用户可选择跳过，后续在个人设置中补充。

#### 触发条件

- 用户通过 OAuth 首次注册成功（新建账号）
- 用户尚未填写 display name 或 country 信息

#### 页面元素

- 图标（紫色圆形背景 + 用户确认图标）
- 标题「Almost there!」
- 副标题「Complete your profile to start shopping. Just a few more details needed.」
- OAuth 连接状态标签：
  - 绿色背景 + 勾选图标
  - 文案「Connected with {Provider} as {用户邮箱}」（如 "Connected with Google as sarah@gmail.com"）
- 表单字段：
  - Display Name 输入框（标签「Display Name」，placeholder「Enter your display name」）
  - Country / Region 选择器（点击弹出国家选择弹窗，参见 1.4）
- 协议勾选：「I agree to the Terms of Service and Privacy Policy」
- 「Complete Setup」主按钮（紫色）
- 「Skip for now — I'll complete this later」跳过链接

#### 操作流程

**主流程：**

1. OAuth 首次注册成功后，自动跳转至补充信息页
2. 页面展示 OAuth 连接状态（Provider 名称 + 邮箱）
3. 用户输入 Display Name
4. 用户选择 Country / Region（点击弹出国家选择弹窗）
5. 用户勾选协议
6. 用户点击「Complete Setup」
7. 系统保存补充信息
8. 跳转至首页

**分支流程：**

- 用户点击「Skip for now」→ 跳过补充信息，直接跳转首页，后续在个人设置中补充
- Display Name 为空 → 提示「Please enter a display name」
- 未选择国家 → 提示「Please select your country」
- 未勾选协议 → 「Complete Setup」按钮置灰不可点击
- 网络请求失败 → Toast 提示「Network error, please try again」

#### 校验规则

| 字段 | 规则 | 校验时机 | 是否必填 |
|------|------|----------|----------|
| Display Name | 1-50 个字符，不含特殊符号 | 提交时前端校验 | 是（提交时） |
| Country / Region | 必须从列表中选择 | 提交时前端校验 | 是（提交时） |
| 协议勾选 | 必须勾选 | 前端校验 | 是 |

#### 预填充规则

| 字段 | 预填充来源 | 说明 |
|------|------------|------|
| Display Name | OAuth Provider 返回的 name 字段 | Google 返回 displayName；Apple 首次授权返回 firstName + lastName；Facebook 返回 name。如 Provider 未返回则留空 |
| Country / Region | 用户 IP 自动识别 | 默认 United States |
| 协议勾选 | 不预填 | 必须用户主动勾选（合规要求） |

#### 跳过机制

- 用户可跳过补充信息，不影响基本功能使用
- 跳过后，系统在以下时机再次引导补充：
  - 首次下单时（Country 影响配送和税费计算）
  - 个人设置页面中展示「Complete your profile」提示
- 跳过不等于拒绝协议：OAuth 注册时已通过 Provider 的授权流程，Looply 的 ToS 在首次实际交易前必须确认

#### 技术说明

- Display Name 存储到 `user_profile.nickname` 字段
- Country 存储到 `user_profile.country_code` 字段
- OAuth Provider 信息从注册流程上下文传递，不重新请求
- 跳过状态记录到 `user_profile.profile_completed` 字段（boolean）

#### UI 关联

- PC 端：设计稿 Screen/OAuthSupplementary
- H5 端：待设计

---

## 三、登录模块

### 3.1 模块概述

- **模块目标**：保障用户顺畅进入站内，支持账户恢复
- **优先级**：P0
- **入口**：首页「Sign In」按钮、注册页引导链接、Session 过期后跳转
- **说明**：用户通过首页顶部「Sign In」按钮进入登录页面。（首页尚未设计，以下描述仅作示意）

### 3.2 邮箱密码登录

#### 功能描述

用户通过已注册的邮箱和密码登录 Looply 平台。

#### 前置条件

- 用户未登录状态
- 用户已拥有 Looply 账号

#### 操作流程

**主流程：**

1. 用户进入登录页面
2. 用户输入邮箱地址
3. 用户输入密码
4. 用户点击「Sign In」
5. 系统校验邮箱和密码
6. 登录成功，跳转至首页（或登录前访问的页面）

**分支流程：**

- 邮箱未注册 → 提示「Account not found」，引导注册
- 密码错误 → 提示「Incorrect password」，显示「Forgot password?」链接
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
| 连续输错密码（达到限制） | 账号锁定 30 分钟，页面展示锁定提示 |
| 网络请求失败 | Toast 提示重试 |

#### UI 关联

- PC 端：设计稿 Screen/Login
- H5 端：设计稿 H5/Login

---

### 3.3 Google 快捷登录

#### 功能描述

已通过 Google 注册的用户，使用 Google 账号一键登录。本功能基于 Google OAuth 2.0 协议实现，需接入 Google 外部服务。

#### 操作流程

**主流程：**

1. 用户点击「Continue with Google」
2. 跳转至 Google OAuth 授权页
3. 用户选择已关联的 Google 账号
4. 系统校验 Google 账号关联状态
   - 已关联 Looply 账号 → 直接登录
   - 未关联 → 自动创建新账号并登录（等同 Google 注册流程）
5. 跳转至首页

**分支流程：**

- 用户取消 Google 授权 → 返回登录页
- Google 服务不可用 → 提示使用邮箱密码登录

#### 外部服务依赖

本功能需接入以下 Google 外部服务：

| 服务 | 用途 | 说明 |
|------|------|------|
| Google Cloud Console | 项目管理 | 创建 OAuth 2.0 客户端凭据（Client ID / Client Secret） |
| Google Identity Platform | 身份认证 | 提供 OAuth 2.0 授权端点和 Token 端点 |
| Google People API | 用户信息 | 获取用户邮箱、头像、昵称等 Profile 信息 |

#### 接入流程（技术侧）

**一、前期配置（一次性）**

1. 在 [Google Cloud Console](https://console.cloud.google.com/) 创建项目
2. 启用 Google Identity 和 People API
3. 配置 OAuth 2.0 同意屏幕（Consent Screen）
   - 应用名称：Looply
   - 授权域名：looply.com
   - 隐私政策链接、服务条款链接
4. 创建 OAuth 2.0 客户端凭据
   - 应用类型：Web Application
   - 授权重定向 URI：`https://www.looply.com/api/auth/google/callback`（生产）/ `http://localhost:3000/api/auth/google/callback`（开发）
5. 获取 Client ID 和 Client Secret，配置到服务端环境变量

**二、授权流程（每次登录）**

```
用户浏览器                    Looply 服务端                  Google 服务
    |                              |                              |
    |-- 1. 点击 Google 登录 ------>|                              |
    |                              |-- 2. 生成 state 参数 -------->|
    |<--- 3. 302 重定向至 Google ---|                              |
    |                              |                              |
    |-- 4. 用户在 Google 授权 ---->|                              |
    |                              |                              |
    |<--- 5. 携带 code 回调 -------|                              |
    |-- 6. code 发送到服务端 ----->|                              |
    |                              |-- 7. 用 code 换取 Token ---->|
    |                              |<-- 8. 返回 access_token -----|
    |                              |-- 9. 用 Token 获取用户信息 ->|
    |                              |<-- 10. 返回 email/profile ---|
    |                              |                              |
    |                              |-- 11. 查询/创建 Looply 账号  |
    |                              |-- 12. 签发 Looply Token      |
    |<--- 13. 登录成功，跳转首页 --|                              |
```

**三、关键参数**

| 参数 | 值 |
|------|-----|
| 授权端点 | `https://accounts.google.com/o/oauth2/v2/auth` |
| Token 端点 | `https://oauth2.googleapis.com/token` |
| 用户信息端点 | `https://www.googleapis.com/oauth2/v2/userinfo` |
| Scope | `openid email profile` |
| Response Type | `code`（授权码模式） |
| state 参数 | 服务端生成随机值，防 CSRF 攻击 |

**四、安全要求**

- Client Secret 仅存储在服务端，禁止暴露到前端
- state 参数必须校验，防止 CSRF 攻击
- 授权码（code）仅可使用一次，且有效期极短（通常 10 分钟）
- access_token 不持久化存储，用完即弃
- 仅通过服务端发起 Token 交换请求，禁止前端直接调用

#### 未来扩展说明

当前架构基于 OAuth 2.0 标准协议，后续接入 Apple、Facebook 等第三方登录时，可复用现有流程框架：

| 未来接入 | 授权协议 | 复用部分 | 新增部分 |
|----------|----------|----------|----------|
| Apple Sign In | OAuth 2.0 + OIDC | 授权码交换流程、账号绑定逻辑、前端按钮组件 | Apple Developer 配置、JWT 解析 |
| Facebook Login | OAuth 2.0 | 授权码交换流程、账号绑定逻辑、前端按钮组件 | Facebook App 配置、Graph API 调用 |

建议服务端实现统一的第三方登录适配层（Provider Pattern），新增登录方式时仅需实现对应 Provider，无需修改核心登录逻辑。

---

### 3.4 忘记密码

#### 功能描述

用户忘记密码时，通过邮箱验证身份并重置密码。

#### 前置条件

- 用户已注册 Looply 账号
- 用户能访问注册邮箱

#### 操作流程

**主流程：**

1. 用户在登录页点击「Forgot password?」
2. 跳转至忘记密码页面
3. 用户输入注册邮箱
4. 用户点击「Send Reset Code」
5. 系统发送 6 位验证码到用户邮箱
6. 跳转至验证码校验页面（VerifyCode）
7. 用户输入验证码，点击「Verify code」
8. 验证通过，跳转至重置密码页面

**分支流程：**

- 输入的邮箱未注册 → 出于安全考虑，仍提示「If this email is registered, you will receive a verification code」（不暴露邮箱是否已注册）
- 重复发送 → 限制 60 秒内不可重复发送，显示倒计时
- 验证码校验相关分支 → 参见 2.8 邮箱验证码校验

#### UI 关联

- PC 端：设计稿 Screen/ForgotPassword
- H5 端：设计稿 H5/ForgotPassword

---

### 3.5 重置密码

#### 功能描述

用户通过验证码校验后，设置新密码。

#### 前置条件

- 用户已通过忘记密码流程中的验证码校验（参见 2.8）

#### 操作流程

**主流程：**

1. 验证码校验通过后，自动跳转至重置密码页面
2. 用户输入新密码（两次确认）
3. 用户点击「Reset Password」
4. 密码重置成功，提示「Password updated successfully」
5. 自动跳转至登录页

**分支流程：**

- 新密码与旧密码相同 → 提示「New password must be different from your current password」
- 重置会话过期（验证码校验通过后 15 分钟内未完成重置） → 提示「Session expired. Please start over.」，跳转至忘记密码页面

#### 密码规则

- 与注册时密码规则一致（参见 2.5 密码设置）

#### UI 关联

- PC 端：设计稿 Screen/ResetPassword
- H5 端：设计稿 H5/ResetPassword

---

### 3.6 登录态保持

#### 功能描述

用户登录成功后，系统通过 Cookie 维持登录态。默认保持 30 天有效期，用户无需重复登录。

#### 交互说明

- 登录表单中提供「Remember me」复选框
- 勾选后，Cookie 有效期 30 天，用户即使不操作也保持登录状态
- 未勾选时，Cookie 为会话级，浏览器关闭后失效

#### 有效期规则

| 场景 | Cookie / Token 有效期 | 说明 |
|------|----------------------|------|
| 勾选 Remember Me | 30 天 | 用户不操作期间 Cookie 持续有效，30 天内再次访问自动登录 |
| 未勾选 | 会话级 | 浏览器关闭后 Cookie 失效，需重新登录 |
| Token 自然过期 | - | 跳转至首页，提示「Session expired」 |
| 用户持续活跃 | 自动延长有效期 | 用户每次访问网站时，Cookie 过期时间从当前时刻重新计算 30 天。只要用户持续使用，登录状态不会过期 |

#### Cookie 存储说明

| 属性 | 值 | 说明 |
|------|-----|------|
| Name | `looply_token` | Token 标识 |
| Domain | `.looply.com` | 主域名下共享 |
| Path | `/` | 全站生效 |
| Max-Age | `2592000`（30天） | 勾选 Remember Me 时设置 |
| HttpOnly | `true` | 禁止 JS 读取，防 XSS |
| Secure | `true` | 仅 HTTPS 传输 |
| SameSite | `Lax` | 防 CSRF，允许顶级导航携带 |

#### 安全说明

- 用户主动退出时，无论是否勾选 Remember Me，均清除 Cookie 和服务端 Token
- 密码修改后，所有已签发 Token 失效，用户需重新登录
- Cookie 设置 HttpOnly + Secure + SameSite，防止 XSS 和 CSRF 攻击
- 服务端 Token 采用不可预测的随机值，禁止使用可逆编码

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
| 用户头像 | 无 | 显示用户头像首字母圆形头像 |
| 标题 | Welcome back | Welcome back, {用户名} |
| 副标题 | Sign in to your Looply account | 显示用户邮箱 |
| 邮箱输入框 | 空，需用户输入 | 预填充用户邮箱 |
| 密码输入框 | 空 | 空，需用户输入 |
| Remember me | 未勾选 | 已勾选 |
| 其他元素 | - | 与标准登录页一致 |

#### 交互说明

- 用户可修改预填充的邮箱地址（切换账号场景）
- 密码输入框自动获取焦点，减少操作步骤
- 其余交互逻辑与标准登录页一致（参见 3.2）

#### 技术说明

- 回访用户识别基于本地存储（localStorage），存储字段：邮箱、用户名首字母
- 用户主动退出时清除本地存储的回访信息

#### UI 关联

- PC 端：设计稿 Screen/Login-Remembered
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

#### 操作流程

**主流程：**

1. 用户点击退出入口
2. 弹出确认弹窗「Are you sure you want to sign out?」
3. 用户点击「Yes, sign out」确认
4. 系统清除当前 Session / Token
5. 跳转至首页（首页尚未设计，仅作示意）

**分支流程：**

- 用户点击「Cancel」→ 关闭弹窗，保持当前状态
- 退出请求失败 → 前端强制清除本地 Token，跳转首页

#### UI 关联

- PC 端：设计稿 Screen/LogoutModal
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

> **备注**：首页尚未设计，上述跳转目标仅作示意。首页将作为登录/注册的统一入口，退出后回到首页引导用户重新登录或浏览。

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

用户主动发起永久删除账号操作。注销后账号数据不可恢复，需通过密码确认身份后方可执行。

#### 前置条件

- 用户已登录状态
- 用户无进行中的订单（活跃订单需先完成或取消）

#### 入口

- 账号设置页面 → 「Delete Account」（具体设置页尚未设计，仅作示意）

#### 页面元素

- 警告图标（红色三角感叹号，红色圆形背景）
- 标题「Delete your account」
- 说明文案「This action is permanent and cannot be undone. All your data, listings, and purchase history will be deleted.」
- 红色警告区域：
  - 警告图标 + 警告文案「You will lose access to all purchases, seller earnings, and saved items. Active orders must be completed before deletion.」
- 密码确认输入框：
  - 标签「Password」
  - placeholder「Enter your password to confirm」
  - 支持密码显示/隐藏切换
- 「Permanently delete account」主按钮（红色，强调不可逆）
- 「Cancel」次按钮（灰色边框样式）

#### 操作流程

**主流程：**

1. 用户进入账号注销页面
2. 阅读注销警告信息
3. 输入当前账号密码
4. 点击「Permanently delete account」
5. 系统校验密码
6. 密码正确 → 执行账号注销
7. 清除本地登录态，跳转至首页
8. 展示 Toast 提示「Your account has been deleted」

**分支流程：**

- 密码错误 → 提示「Incorrect password」，不执行注销
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

#### 安全说明

- 必须通过密码验证身份，不可跳过
- OAuth 注册用户（无密码）的注销方式：后续迭代支持，MVP 阶段仅邮箱注册用户可注销
- 注销操作记录到审计日志
- 30 天冷却期内，使用同一邮箱注册视为新账号，不恢复旧数据

#### UI 关联

- PC 端：设计稿 Screen/AccountDeletion
- H5 端：待设计

---

## 五、安全风控模块

### 5.1 模块概述

- **模块目标**：保障基础账户安全，降低恶意操作风险
- **优先级**：P0
- **作用范围**：贯穿注册、登录、密码重置全流程

### 5.2 密码校验

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

#### 交互说明

- 实时校验，逐条显示是否满足（通过/未通过状态）
- 全部通过后「提交」按钮可点击

---

### 5.3 登录限错

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

#### UI 关联

- PC 端：设计稿 Screen/ErrorState（账号锁定状态）
- H5 端：设计稿 H5/ErrorState

---

### 5.4 注册限频

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

### 5.5 发信限频

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

### 5.6 异常提示

#### 功能描述

当系统检测到异常行为时，向用户展示明确的提示信息。

#### 异常场景与提示

| 异常场景 | 提示内容 | 展示方式 |
|----------|----------|----------|
| 账号被锁定 | Too many failed attempts. Account locked for 30 minutes. | 页面顶部 Banner |
| 登录密码错误 | Incorrect password | 输入框下方错误提示 |
| 邮箱格式错误 | Please enter a valid email address | 输入框下方错误提示 |
| 网络错误 | Network error, please try again | Toast 提示 |
| 服务端错误 | Something went wrong, please try again later | Toast 提示 |
| 注册被限频 | Too many attempts, please try again later | Toast 提示 |

#### 设计原则

- 错误提示使用红色文字 + 错误图标
- 安全相关提示不暴露系统内部逻辑
- 所有提示文案需支持多语言

---

### 5.7 会话失效

#### 功能描述

当用户的登录会话（Session/Token）失效时，系统自动处理并引导用户重新登录。

#### 失效场景

| 场景 | 触发条件 |
|------|----------|
| Token 自然过期 | 超过有效期（会话级或 30 天） |
| 密码被修改 | 用户修改密码后，所有已有 Token 失效 |
| 管理员强制下线 | 后台操作使指定用户 Token 失效 |
| 账号被锁定 | 触发安全策略后，当前 Session 失效 |

#### 处理流程

1. 前端请求接口返回 401 状态码
2. 前端清除本地存储的 Token
3. 跳转至首页
4. 首页展示提示信息（如「Session expired. Please sign in again.」）
5. 登录成功后，尝试恢复用户之前访问的页面

#### UI 关联

- PC 端：设计稿 Screen/SessionExpired
- H5 端：设计稿 H5/SessionExpired

---

## 六、附录

### 6.1 设计稿索引

| 页面 | PC 端设计稿 | H5 端设计稿 |
|------|------------|------------|
| 注册 | Screen/Register | H5/Register |
| 登录 | Screen/Login | H5/Login |
| 登录-密码可见状态 | Screen/Login-PasswordVisible | 待设计 |
| 登录-加载状态 | Screen/Login-LoadingState | 待设计 |
| 回访登录 | Screen/Login-Remembered | H5/Login-Remembered |
| 忘记密码 | Screen/ForgotPassword | H5/ForgotPassword |
| 重置密码 | Screen/ResetPassword | H5/ResetPassword |
| 验证码 | Screen/VerifyCode | H5/VerifyCode |
| OAuth 补充信息 | Screen/OAuthSupplementary | 待设计 |
| 国家选择器（弹窗） | Screen/CountrySelector | 待设计 |
| 退出确认 | Screen/LogoutModal | H5/LogoutModal |
| 账号注销 | Screen/AccountDeletion | 待设计 |
| 会话过期 | Screen/SessionExpired | H5/SessionExpired |
| 账号锁定 | Screen/ErrorState | H5/ErrorState |
| 服务条款 | Screen/TermsOfService | H5/TermsOfService |
| 隐私政策 | Screen/PrivacyPolicy | H5/PrivacyPolicy |

### 6.2 接口清单（参考）

| 接口 | 方法 | 说明 |
|------|------|------|
| /api/auth/register | POST | 邮箱注册（提交注册信息，发送验证码） |
| /api/auth/register/verify | POST | 注册验证码校验，校验通过后创建账号 |
| /api/auth/login | POST | 邮箱密码登录 |
| /api/auth/logout | POST | 退出登录 |
| /api/auth/google | GET | Google OAuth 跳转 |
| /api/auth/google/callback | GET | Google OAuth 回调 |
| /api/auth/forgot-password | POST | 发送忘记密码验证码 |
| /api/auth/forgot-password/verify | POST | 忘记密码验证码校验 |
| /api/auth/reset-password | POST | 重置密码 |
| /api/auth/verify-code/resend | POST | 重新发送验证码 |
| /api/auth/verify-token | GET | 校验 Token 有效性 |
| /api/auth/delete-account | POST | 账号注销（需密码确认） |
| /api/auth/oauth/supplement | POST | OAuth 补充信息提交（display name + country） |

### 6.3 修订记录

| 版本 | 日期 | 修改内容 | 修改人 |
|------|------|----------|--------|
| V1.0 | 2026-03-18 | 初稿，覆盖 MVP 四个模块 | 产品部 |
| V1.1 | 2026-03-18 | 补充 Google 登录接入流程及外部服务依赖；完善登录态 Cookie 存储规则 | 产品部 |
| V1.2 | 2026-03-18 | 首页作为登录/注册统一入口；退出登录跳转至首页（首页尚未设计，仅示意） | 产品部 |
| V1.3 | 2026-03-18 | 新增邮箱验证码校验（2.8）；注册流程加入验证码步骤；忘记密码改为验证码方式；重置密码前置条件调整；补充验证码相关接口 | 产品部 |
| V1.4 | 2026-03-18 | 新增服务条款页面（2.6.1）和隐私政策页面（2.6.2）功能说明；更新设计稿索引 | 产品部 |
| V1.5 | 2026-03-18 | 新增回访用户登录页（3.7 Login-Remembered）功能说明及设计稿；更新设计稿索引 | 产品部 |
| V1.6 | 2026-03-18 | 移除密码强度指示器需求（2.5）；新增国家/地区选择器说明（1.4） | 产品部 |
| V1.7 | 2026-03-30 | 新增账号注销（4.6）、OAuth 补充信息页（2.9）功能说明；国家选择器（1.4）从下拉改为模态弹窗；更新设计稿索引（新增 5 个页面）；新增 2 个接口 | 产品部 |
