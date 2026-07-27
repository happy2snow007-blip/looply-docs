# Looply Your Privacy Choices PRD v0.1 模拟评审

> 初次评审日期：2026-07-24  
> 最新闭环复评日期：2026-07-27  
> 正式评审与闭环复评模型：`gpt-5.6-sol / high`  
> 最新确认范围：Web 全端，包含 PC Web 与 Mobile Web；App 不在本期范围  
> 评审角色：开发、测试、设计  
> 评审边界：不评技术选型；不评 GPC、Cookie 保存/生效、下游设置内部逻辑；未修改 PRD 或 Demo

## 一、制品盘点与前置状态

### 1.1 已读取制品

| 制品 | 文件 | 用途 |
|---|---|---|
| 项目背景 | `context/PROJECT_BACKGROUND.md` | 核对已确认背景、Web / Mobile Web 基线及多语言基线 |
| PRD | `docs/product/looply-Your-Privacy-Choices-PRD-v0.1.md` | 正式评审主体 |
| PRD 写作自检 | `docs/reviews/privacy-legal/looply-Your-Privacy-Choices-PRD-自检-2026-07-24.md` | 核验模拟评审前置条件 |
| Web Demo | `prototypes/homepage/looply-your-privacy-choices-web-demo-v0.1.html` | PC Web / Mobile Web 字段、布局、入口与交互对照 |
| 下游参考图 | `img_v3_0213t_a1f48072-d61b-453a-b9cc-f1c5d4832dcg.jpg`（V4-PC-PrivacyData） | 核对下游 PC 参考页是否包含两个目标设置区域 |

未提供当前说明页的正式 UI 设计稿、ER 图、系统流程图、产品架构图或调研报告。该页不新增、编辑或流转业务实体，因此 ER 图缺失不影响本次评审。下游参考图仅覆盖 PC；Mobile Web 的 Privacy & Data 正式设计未在本次制品中提供，故本次只能核对 Demo 的跳转契约，不能据此宣称下游 Mobile Web 页面已经设计、开发或验收。

浏览器运行环境本次不可用，未取得 PC / Mobile Web 实际运行截图。Demo 已按完整 HTML、CSS、DOM 与事件脚本逐行核对。2026-07-27 复核时，`https://www.test.looply.com/` 与 `https://www.test.looply.com/legal/privacy` 均返回 HTTP 200 状态。

### 1.2 自检前置状态

已读取更新后的 PRD 写作自检记录。记录覆盖章节、PC Web / Mobile Web 用户路径、页面归属、响应式 UI 关联、字段映射、角色、术语、正文减法、多语言归类及 B1-B4 适用性核验，结论为已满足进入正式模拟评审的前置条件。

本次闭环复评在该前置基础上独立从开发、测试、设计三角色重新审查，不把写作自检直接当作正式评审结论。

## 二、最新范围与依赖确认

| 项目 | 最新结论 |
|---|---|
| 当前直接对象 | PC Web 与 Mobile Web Footer 点击后的 Your Privacy Choices 固定说明页，以及 Home、Manage Privacy Choices、Privacy Policy 三类跳转 |
| 不在范围 | App |
| 用户角色 | 游客与登录用户；两者入口、页面内容和跳转路径一致，游客也可进入个人中心 |
| PC Web 布局 | 左右双栏 |
| Mobile Web 布局 | 单列；页面标题、引导语、内容卡片依次纵向展示，卡片内容与交互不变 |
| 响应式边界 | Demo 在视口宽度 `≤1023px` 时进入 Mobile Web 规则，`≥1024px` 时使用 PC Web 规则 |
| 下游对象 | Privacy & Data 中的 Cookie Preferences、Do Not Sell or Share My Personal Information 区域 |
| 下游预览边界 | Demo 内 Privacy & Data 只验证跳转及定位；内部字段、开关状态、保存与生效不作为本 PRD 的设计依据 |
| 外部依赖 | PRD 已声明 PC / Mobile Web 公共 Header、Footer、面包屑、游客可访问的 Privacy & Data、稳定定位位置、Privacy Policy 地址及法务审核依赖 |

此前按“仅 PC Web、排除移动网页”形成的临时闭环结论已被用户最新范围纠正取代，不再作为有效结论。当前有效范围仅为“PC Web＋Mobile Web，排除 App”。

## 三、跨制品一致性检查

### 3.1 页面字段与文案

PC Web 与 Mobile Web 共用同一套 DOM，因此以下用户可见字段及稳定文案标识在两端完全相同：

| 页面元素 | 文案 / 标识 | PC Web | Mobile Web |
|---|---|---|---|
| 页面标题 | `Your Privacy Choices` / `privacy_choices.page.title` | 一致 | 一致 |
| 引导语 | PRD 第 2.3 节固定文案 / `privacy_choices.page.intro` | 一致 | 一致 |
| 卡片标题 | `Manage how your information is used` / `privacy_choices.card.title` | 一致 | 一致 |
| 说明文案 1 | `privacy_choices.card.description_usage` | 一致 | 一致 |
| 说明文案 2 | `privacy_choices.card.description_rights` | 一致 | 一致 |
| 管理入口 | `Manage Privacy Choices` / `privacy_choices.action.manage` | 一致 | 一致 |
| 辅助说明 | `privacy_choices.card.privacy_policy_prompt` | 一致 | 一致 |

全部文案已归类为静态 UI 文案，使用 Web message package；v0.1 源文案为 `en-US`，其他已启用语言及译文缺失兜底沿用全局规则并在最终总 PRD 维护。PC Web 与 Mobile Web 不存在独立文案分支。

### 3.2 响应式布局

| 检查项 | PRD | Demo | 结论 |
|---|---|---|---|
| PC 主体 | 左右双栏 | 默认使用 `250px + 1fr` 双栏 | 一致 |
| Mobile 主体 | 标题、引导语、卡片纵向单列 | `≤1023px` 时 `.privacy-layout` 切换为单列，卡片置于引导语下方 | 一致 |
| 761-1023px 区间 | 属于 Mobile Web 单列体验 | 最新 Demo 已将响应式断点调整为 `1023px`，同时取消 `body` 最小宽度 | 一致；此前发现的区间缺口已关闭 |
| Mobile Header | 复用 Mobile Web 公共 Header | Demo 隐藏 PC 导航，保留 Logo、Search、Account | 与当前 Demo 规则一致；正式公共组件以所属规范为准 |
| Mobile Footer | 复用 Mobile Web 公共 Footer，并保留入口 | Demo 调整为移动布局，法律链接区域仍包含 `Your Privacy Choices` | 一致 |
| Mobile 触控入口 | 管理入口内容与交互不变 | `Manage Privacy Choices` 最小高度为 44px | 一致 |

### 3.3 入口与页面路径

| 动作 | PC Web | Mobile Web | 结论 |
|---|---|---|---|
| Footer · Your Privacy Choices | Footer 法律链接区存在入口 | 响应式 Footer 法律链接区保留同一入口 | 一致 |
| 面包屑 Home | 指向 `https://www.test.looply.com/` | 使用同一链接 | 一致，HTTP 200 |
| Logo | 指向 `https://www.test.looply.com/` | 使用同一链接 | 一致，HTTP 200 |
| Manage Privacy Choices | 切换到简化 Privacy & Data 目标页并定位 `#privacy-choices` | 使用同一 DOM、脚本和定位容器 | 一致 |
| Privacy Policy | 指向 `https://www.test.looply.com/legal/privacy`，不被脚本拦截 | 使用同一链接 | 一致，HTTP 200 |
| 浏览器返回 | 使用统一浏览器返回规则 | 使用同一 history / popstate 逻辑 | 一致 |

### 3.4 下游参考图

PC 下游参考图同时包含 `Cookie Preferences` 与 `Do Not Sell or Share My Personal Information`，和 PRD 的定位目标一致。参考图中的 Request a Copy of Your Data、Delete Account、侧边导航及更多说明属于下游内部内容，PRD 已明确排除；Demo 的简化不构成本模块差异。

## 四、处理汇总

| # | 等级 | 问题 | 最新处理结果 |
|---|---|---|---|
| 1 | P1 | Web 范围、Mobile Web 入口与响应式布局未闭合 | ✅ 已关闭：最新范围为 PC Web＋Mobile Web、排除 App；Demo 使用 `1023px` 断点覆盖窄屏与常见横屏区间 |
| 2 | P1 | Demo 的 Home 与 Privacy Policy 点击结果和 PRD 不一致 | ✅ 已关闭：已使用有效测试站地址并移除 Privacy Policy Toast 拦截 |
| 3 | P1 | 静态 UI 文案未按多语言基线分类 | ✅ 已关闭：已补 `privacy_choices.*` 稳定标识、Web message package、`en-US` 源文案及全局语种 / 兜底归属 |

## 五、P0（规则缺失或制品矛盾，阻塞开发）

未发现 P0。PC Web / Mobile Web 的范围、布局、入口、主路径、角色与下游职责边界均已定义，PRD 与 Demo 没有阻塞性矛盾。

## 六、P1（规则不完整，影响质量）

当前没有未关闭 P1。

原 P1-1 曾在错误的“仅 PC Web”范围下被临时关闭；用户纠正为 Web 全端后，本次已按 PC Web＋Mobile Web 重新评审。复评中发现的 761-1023px 响应式区间缺口已通过将 Demo 断点调整至 `1023px` 关闭，故不保留为未关闭问题。

## 七、P2（描述可更精确）

未发现 P2。Demo 已明确给出响应式边界，PRD 已明确两种用户可见布局及其内容顺序；未发现会影响当前开发或测试预期的描述歧义。

## 八、P3（锦上添花）

未发现 P3。本次不提出纯样式偏好或超出当前范围的增强建议。

## 九、三角色结论

| 角色 | 闭环复评结论 |
|---|---|
| 开发 | PC Web 与 Mobile Web 的范围、布局分支、Footer 入口、三类跳转和静态文案归属已闭合；未发现状态流转、实体变更或下游保存规则方面的本模块问题。 |
| 测试 | 可按 `≥1024px` PC 双栏、`≤1023px` Mobile 单列建立跨端用例；两端共用字段、入口与路径，当前没有无法判定的验收项。 |
| 设计 | PC / Mobile 的内容层级一致，差异仅为布局与对应公共 Header / Footer；Mobile Footer 保留隐私入口，未发现无理由的跨端差异。 |

## 十、统计与发布建议

- 当前未关闭 P0：0 个
- 当前未关闭 P1：0 个
- 当前未关闭 P2：0 个
- 当前未关闭 P3：0 个
- 当前未关闭合计：0 个
- 历史提出 P1：3 个，已关闭 3 个

**发布建议：有条件建议作为 PC Web / Mobile Web 的最终开发与测试基线并进入发布准备。** 当前没有未关闭评审问题。实际对外上线前仍须：

1. 取得 PRD 第三章声明的美国法务或合规负责人文案审核；
2. 由 Privacy & Data 所属模块确认 Mobile Web 目标页可供游客和登录用户访问，并能稳定定位到两个设置区域。

以上两项属于 PRD 已声明的发布依赖；本次制品未提供其完成证明，因此不把它们视为已完成事实。

## 十一、正式评审自检

- 已覆盖开发、测试、设计三个角色；
- 已以用户最新范围纠正所有“仅 PC Web / 排除移动网页”的旧结论；
- 已逐项核对 PC Web / Mobile Web 的布局、入口、路径、文案与角色一致性；
- 已检查 761-1023px 反例，确认最新版 Demo 的 `1023px` 断点已关闭该缺口；
- 未把 Mobile Web 下游正式 UI 缺失证据误写为已验收能力；
- 未提出技术实现选型，未越界评审 GPC、保存、生效或下游内部设置；
- P3 占比为 0，未为凑数制造问题；
- 评审记录存放在 `docs/reviews/privacy-legal/`。
