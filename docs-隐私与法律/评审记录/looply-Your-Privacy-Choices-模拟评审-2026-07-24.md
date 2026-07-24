# Looply Your Privacy Choices PRD v0.1 模拟评审

> 评审日期：2026-07-24
> 正式评审模型：`gpt-5.6-sol / high`
> 闭环复核日期：2026-07-24
> 闭环复核模型：`gpt-5.6-sol / high`
> 评审范围：开发、测试、设计三角色的业务规则完整性与 PRD / Demo 一致性
> 评审边界：不评技术选型；不评 GPC、Cookie 保存/生效、下游设置内部逻辑；不修改 PRD 或 Demo

## 一、制品盘点与前置状态

### 1.1 已读取制品

| 制品 | 文件 | 用途 |
|---|---|---|
| 项目背景 | `context/PROJECT_BACKGROUND.md` | 核对已确认背景、Web / Mobile 基线及多语言检查基线 |
| PRD | `docs/product/looply-Your-Privacy-Choices-PRD-v0.1.md` | 正式评审主体 |
| PRD 写作自检 | `docs/reviews/privacy-legal/looply-Your-Privacy-Choices-PRD-自检-2026-07-24.md` | 核验模拟评审前置条件 |
| Web Demo | `prototypes/homepage/looply-your-privacy-choices-web-demo-v0.1.html` | 字段、布局与交互对照 |
| 下游参考图 | `img_v3_0213t_a1f48072-d61b-453a-b9cc-f1c5d4832dcg.jpg`（V4-PC-PrivacyData） | 核对跳转目标是否包含 Cookie Preferences 与 Do Not Sell or Share 区域 |

未提供当前说明页的正式 UI 设计稿、ER 图、系统流程图、产品架构图或调研报告。该页不新增、编辑或流转业务实体，因此 ER 图缺失不影响本次评审；其余缺失制品仅限制对正式视觉规范和调研结论的核对，不据此虚构问题。

浏览器运行环境本次不可用，未取得实际运行截图；Demo 已按完整 HTML、CSS、DOM 与事件脚本逐行核对，并结合下游参考图检查跳转目标。闭环复核时另以非敏感最小请求验证测试站链接：`https://www.test.looply.com/` 与 `https://www.test.looply.com/legal/privacy` 均返回 HTTP 200。正式评审结论与制品盘点、规范读取相互区分。

### 1.2 自检前置状态

已读取 2026-07-24 更新后的 PRD 写作自检记录。记录覆盖 A 类章节、用户路径、页面归属、PC Web UI 关联、PRD / Demo 字段映射、角色、术语、正文减法与多语言归类，以及 B1-B4 适用性核验，结论为“已满足进入正式模拟评审的前置条件”。

本次正式评审在此前置基础上独立从三角色重新审查；后文发现的问题不改变“已执行并通过写作自检”这一前置事实。

## 二、范围与依赖确认

| 项目 | 评审结论 |
|---|---|
| 当前直接对象 | PC Web Footer 点击后的 Your Privacy Choices 固定说明页，以及从该页发起的 Home、Manage Privacy Choices、Privacy Policy 三个跳转动作；移动网页与 App 不在本期范围 |
| 用户角色 | 游客与登录用户；两者路径一致。游客也可进入个人中心，不提出登录拦截问题 |
| 下游对象 | Privacy & Data 中的 Cookie Preferences、Do Not Sell or Share My Personal Information 区域 |
| 下游预览边界 | Demo 内 Privacy & Data 仅验证跳转与定位；其内部字段、开关状态、保存与生效规则不作为本 PRD 的设计依据 |
| 明确不评 | GPC、Cookie 保存/生效、下游设置内部逻辑、技术实现方案 |
| 外部依赖状态 | PRD 第三章已声明公共 Header / Footer / 面包屑、游客可访问的 Privacy & Data、稳定定位位置、Privacy Policy 地址及法务审核依赖；下游参考图证明两个目标区域已有设计参考，不将其误判为“概念未定义” |

## 三、跨制品一致性检查

### 3.1 PRD 与 Demo 字段及承载结构

| 页面元素 / 规则 | PRD | Demo | 结论 |
|---|---|---|---|
| 页面标题 | `Your Privacy Choices` | 同文案 | 一致 |
| 引导语 | 指定固定英文文案 | 同文案 | 一致 |
| 内容卡片标题 | `Manage how your information is used` | 同文案 | 一致 |
| 说明文案 1 | 指定固定英文文案 | 同文案 | 一致 |
| 说明文案 2 | 指定固定英文文案 | 同文案 | 一致 |
| 管理入口 | 文字＋右箭头 | 文字＋右箭头 | 一致 |
| 面包屑 Home | 返回首页 | 指向 `https://www.test.looply.com/`，HTTP 200 | 一致；P1-2 已关闭 |
| 辅助说明与 Privacy Policy | 指定固定文案并进入 Privacy Policy | 文案一致，指向 `https://www.test.looply.com/legal/privacy`，HTTP 200，未再被脚本拦截 | 一致；P1-2 已关闭 |
| 主跳转目标 | Privacy & Data 的 Privacy Choices 设置区域 | Demo 切换到简化 Privacy & Data 目标页，并定位到包含两个区域的容器 | 与 PRD 第 2.6 节的“简化目标页”声明一致 |
| 终端与 PC 主体布局 | 仅 PC Web，左右双栏；移动网页与 App 不涉及 | `body` 设置 `min-width: 1024px`，左右双栏，已移除窄屏响应式规则 | 一致；P1-1 已关闭 |
| 文案归类与标识 | 全部为静态 UI 文案，使用 Web message package；第 2.3 节逐项定义 `privacy_choices.*` 稳定标识；v0.1 源文案为 `en-US`，其他语言与兜底引用全局规则 | 页面元素与 PRD 固定源文案一致 | 当前子模块规则已闭合；P1-3 已关闭 |

本页没有列表、表单、枚举或可变业务实体，不适用列表列、筛选、表单控件、枚举值及数据录入结构对照。

### 3.2 PRD 与下游参考图

下游参考图中同时存在 `Cookie Preferences` 与 `Do Not Sell or Share My Personal Information`，与 PRD 第 2.4、2.6、3 章声明的目标区域一致。参考图还包含 Request a Copy of Your Data、Delete Account、侧边导航及更完整的说明文案；这些属于下游页面内部内容，PRD 已明确排除，Demo 的简化不构成本模块差异。

## 四、处理汇总

| # | 等级 | 角色 | 问题 | 处理方式 |
|---|---|---|---|---|
| 1 | P1 | 开发 / 设计 / 测试 | Web 范围是否包含移动网页、窄屏入口与布局未闭合 | ✅ 已关闭：用户确认仅 PC Web；PRD 与 Demo 已同步收口 |
| 2 | P1 | 测试 / 设计 | Demo 的 Home 与 Privacy Policy 点击结果和 PRD 不一致 | ✅ 已关闭：已改为测试站有效地址并移除 Privacy Policy Toast 拦截；两地址均实测 HTTP 200 |
| 3 | P1 | 开发 / 测试 | 新增静态 UI 文案未按项目多语言基线分类 | ✅ 已关闭：已补静态 UI、`privacy_choices.*` 稳定标识、Web message package、`en-US` 源文案及全局规则归属 |

## 五、P0（规则缺失或制品矛盾，阻塞开发）

未发现 P0。核心页面字段、主跳转对象、游客与登录用户路径、下游职责边界均已定义；下游预览简化有明确声明，不构成制品矛盾。

## 六、P1（规则不完整，影响质量）

### 1. [已关闭][开发 / 设计 / 测试] Web 范围与窄屏规则未闭合

- **原位置**：PRD 第 1.2、2.2、4 章及附录；原 Demo 窄屏 CSS。
- **用户结论**：本页面仅 PC 端有。
- **修正证据**：PRD 第 1.2、1.5、2.2、2.5、4 章及附录均明确为 PC Web，并排除移动网页与 App；Demo 第 20 行设置 `min-width: 1024px`，已移除 `max-width: 760px` 响应式规则。
- **复核结论**：开发、设计和测试均可按 PC Web 左右双栏形成唯一预期，P1 已关闭。

### 2. [已关闭][测试 / 设计] Demo 的 Home 与 Privacy Policy 点击结果和 PRD 不一致

- **原位置**：PRD 第 2.4 节；原 Demo 的 Home 占位链接与 Privacy Policy Toast 拦截。
- **修正证据**：Demo 的 Logo、说明页与下游预览页面包屑 Home 均指向 `https://www.test.looply.com/`；卡片和 Footer 的 Privacy Policy 均指向 `https://www.test.looply.com/legal/privacy`；脚本不再拦截 Privacy Policy。两地址于闭环复核时均返回 HTTP 200。
- **边界确认**：`Manage Privacy Choices` 继续使用同页简化下游预览，符合 PRD 第 2.6 节的明确声明。
- **复核结论**：PRD 与 Demo 对 Home、Privacy Policy 和 Manage Privacy Choices 三类跳转的表达已一致，P1 已关闭。

### 3. [已关闭][开发 / 测试] 静态 UI 文案未按项目多语言基线分类

- **原位置**：PRD 第 2.3 节与附录；项目背景第十六节。
- **修正证据**：PRD 第 2.3 节已为页面标题、引导语、卡片标题、两段说明、管理入口和辅助说明逐项定义 `privacy_choices.*` 稳定静态文案标识；第 2.7 节明确这些标识由 Web 统一 message package 管理，不进入翻译中心业务资源卡片。v0.1 以第 2.3 节 `en-US` 文案为源文案，其他已启用语言及缺失译文兜底沿用全局规则并在最终总 PRD 统一维护。
- **复核结论**：该最小归类同时具备类别、稳定标识、管理归属与源文案，符合“子模块只描述本功能、语言总表与统一验收留在最终总 PRD”的项目分工，P1 已完整关闭。

## 七、P2（描述可更精确）

闭环复核未发现新的 P2。

## 八、P3（锦上添花）

未发现 P3。本次不提出纯样式偏好或文案润色建议。

## 九、三角色结论

| 角色 | 结论 |
|---|---|
| 开发 | PC Web 范围、左右双栏、三个跳转动作及静态文案归属均已闭合；未发现状态流转、实体变更或下游保存规则方面的本模块缺口。 |
| 测试 | PC 默认态、游客/登录用户一致路径、Home / Privacy Policy 外链、Manage 简化预览及浏览器返回均已有单一验收预期；闭环复核未发现新增问题。 |
| 设计 | PC 说明页字段与布局和 Demo 一致，下游定位对象与参考图一致；移动网页与 App 已明确排除，闭环复核未发现新增问题。 |

## 十、统计与发布建议

- 当前未关闭 P0：0 个
- 当前未关闭 P1：0 个
- 当前未关闭 P2：0 个
- 当前未关闭 P3：0 个
- 当前未关闭合计：0 个
- 历史提出 P1：3 个，已关闭 3 个

**发布建议：有条件建议作为最终开发 / 测试基线并进入发布准备。** 3 个历史 P1 已全部关闭，当前没有未关闭评审问题。功能正式上线前仍必须取得 PRD 第三章已声明的美国法务或合规负责人文案审核；评审制品未提供该审核已完成的证明，因此在法务 / 合规确认前不建议实际对外上线。

## 十一、正式评审自检

- 已覆盖开发、测试、设计三个角色；
- 原 3 个问题均指向 PRD 与关联制品的具体位置，闭环复核逐项补充了用户结论、修正证据与关闭结论；
- 开发、测试、设计三个角色均已复核；关闭后未发现新问题，故不为凑数新增提问；
- 未提出技术实现或技术选型；
- 已完成 PRD / Demo 字段、承载结构、布局与交互对照；
- 已检查并明确排除游客访问、下游内部设置、GPC、Cookie 保存/生效等越界问题；
- P3 占比为 0，未为凑数制造问题；
- 评审记录存放在 `docs/reviews/privacy-legal/`。
