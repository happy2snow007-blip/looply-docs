# Looply Favorites 变更日志

> 当前状态：迭代中，尚未确认正式交付基线。  
> 本日志仅记录 Favorites Overview 综合 PRD 与 V9 原型的实际变化，不代表已交付开发。

## 当前进行中版本

### v2.9（2026-07-16）— 评审结论已收口，已同步文档中心

#### 变更内容

- **PRD 版本**：v2.8 → v2.9，新建 `looply-Favorites-PRD-v2.9.md`，保留 v2.8 及更早历史版本；
- 同屏相同 `listing_id` 的 Wishlist 心形使用同一状态：乐观联动，失败时所有同商品心形统一回滚；模块结构仅在权威刷新后更新；
- Recommended for You 已有缓存 Feed 时，刷新失败保留 Feed 并静默处理；首次失败与加载更多失败仍使用各自原有规则；
- 新增 Favorites 静态 UI 文案表，明确稳定 i18n key、`en-US`、`es-US`、使用位置、变量与 Price Drop 复数规则；
- Sold Out 且未收藏的商品统一显示置灰空心并禁用点击；Sold Out 已收藏仍允许移出 Wishlist。

#### 影响范围

- **PRD**：已新增 v2.9，同步修订记录与模拟评审处理状态；
- **原型**：继续使用 V9；本轮不改变 Demo 视觉，正式 UI 复用 App 全局 UI 规范；
- **多语言**：新增美国英语与美国西班牙语交付值，上线前需完成统一语言审校；
- **数据与实体**：无新增实体、字段或埋点范围。

#### 待办事项

- [x] 模拟评审 4 项问题获得产品确认并写入 PRD；
- [x] 完成 v2.9 PRD 自检；
- [x] 同步 PRD v2.9 到文档中心 Favorites 对应位置。

### v2.8（2026-07-16）— 本地评审稿，未上传

#### 变更内容

- **PRD 版本**：v2.7 → v2.8，新建 `looply-Favorites-PRD-v2.8.md`，保留所有历史版本；
- 缓存刷新失败从“App 公共组件占位”收口为模块标题下的轻量行内提示：保留缓存、可见失败、仅重试失败模块；Wishlist 与 Recently Viewed 使用一致结构；
- 三处 Wishlist 写入失败统一为“乐观切换 → 回滚 → 轻量 Toast `Couldn’t update Wishlist. Try again.`”；取消收藏成功仍不提示；
- 明确商品状态仅消费在售与 Sold Out；Sold Out 未收藏不可加入、已收藏仍可移出；
- V9 Demo 同步模块内刷新失败提示和三处任意可操作心形失败回滚 + 轻量 Toast。

#### 影响范围

- **PRD**：已新增 v2.8 本地评审稿，并更新独立修订记录；
- **原型**：V9 已同步本轮刷新失败与心形写入失败演示；
- **评审**：待完成 PRD 自检与模拟评审；
- **外部依赖**：App 页面容器仍负责刷新触发；Wishlist 写入服务需返回成功或失败结果；推荐上游需过滤 Sold Out。

#### 待办事项

- [ ] 完成 v2.8 PRD 自检与模拟评审；
- [ ] 产品确认评审问题处理方式后，再收口正式交付版本；
- [ ] 用户确认后再同步文档中心。

### v2.7（2026-07-16）— 本地评审稿，未上传

#### 变更内容

- **PRD 版本**：v2.6 → v2.7，新建 `looply-Favorites-PRD-v2.7.md`，保留所有历史版本；
- 刷新触发改为遵循 App 统一页面刷新策略；Favorites 明确页面级下拉刷新并行请求 Wishlist、Recently Viewed 与 Recommended for You，以及缓存、部分失败和整页失败边界；
- 缓存刷新失败改为“保留旧内容 + 可见 App 公共组件占位 + 仅重试失败模块”；
- Wishlist、Recently Viewed 与 Recommend 的 Heart failed 统一为任意可操作心形乐观切换后回滚，写入中不可重复点击；
- `Both failed` 与 `All data failed` 从 Recently Viewed 的单模块状态选择器迁移为页面级组合状态；
- Recommend 移除 Sold Out Demo 状态与样式，PRD 明确推荐上游仅返回可购买商品；
- PRD 正文不含变更摘要或修订表，修订记录与变更日志继续独立维护。

#### 影响范围

- **PRD**：已新增 v2.7 本地评审稿；
- **原型**：V9 已更新刷新失败、心形失败、页面组合失败和 Recommend 可购买约束演示；
- **评审记录**：`Favorites-第二轮评审-Checklist-20260716.md` 作为本轮收口清单；
- **App 页面容器 / Wishlist / 推荐上游**：开发前仍需对齐公共刷新组件、刷新触发策略和推荐可购买过滤契约。

#### 待办事项

- [ ] 产品审阅 v2.7 PRD 与 V9 Demo；
- [ ] 与 App 页面容器确认正式公共刷新失败组件和刷新生命周期；
- [ ] 与 Wishlist / 浏览历史确认公共写入失败反馈和权威刷新返回契约；
- [ ] 用户确认后再上传或同步文档中心。

### v2.3（2026-07-16）— 本地评审稿，未上传

#### 变更内容

- **PRD 版本**：v2.2 → v2.3，新建 `looply-Favorites-PRD-v2.3.md`，保留全部历史版本；
- PRD 顶部新增 6 条“本版变更摘要”，正文只保留当前有效规则，修订记录和完整变更日志继续独立维护；
- Wishlist 与 Recently Viewed Loading 统一为静态标题、无可见数量占位、3 张同结构商品卡骨架；
- Recently Viewed 移除时钟图标并支持 Wishlist 心形操作，收藏变化不移除浏览记录卡片；
- Sold Out 收藏规则收敛为四种状态：在售可加入/移出，Sold Out 未收藏不可加入、已收藏可移出；
- Price Drop 完全使用各自上游返回的可购买总数，统一单复数文案及 `N = 0` / 失败隐藏规则；
- 补齐登录与匿名主体规则：入口不硬拦截，登录、注册、退出或主体变化后重新获取当前主体结果；
- 补齐模块失败、两个核心模块失败和全部业务内容不可用时的整页错误边界；
- 新增翻译归属清单，区分静态 UI、动态商品内容和不翻译字段，并记录成色资源归属待技术核验；
- 数据与埋点调整为数据平台建设期的简版业务采集要求，不锁定最终事件名和技术实现。
- **2026-07-16 Demo 增量**：Recommended for You 加载到底后静默隐藏加载区域，不展示 `You've seen it all` 结束文案。
- **2026-07-16 Demo 修正**：Wishlist 概览、Recently Viewed 概览和完整 Wishlist 的 Sold Out 已收藏商品均可取消收藏；取消后商品卡保留、心形变为空并禁用再次收藏。

#### 影响范围

- **PRD**：已新增 v2.3 本地产品评审稿；
- **原型**：继续使用 V9，已覆盖本轮 Wishlist、Recently Viewed、Price Drop、Sold Out、Loading 与整页失败演示；
- **修订记录 / Checklist**：已同步 v2.3 状态；
- **商品与多语言依赖**：开发前需核验商品标题、品牌和成色等级的实际翻译资源标识；
- **数据平台依赖**：开发前确认最终事件命名、公共属性、曝光及去重标准；
- **架构图 / ER 图 / 泳道图**：未新增实体、模块边界或跨角色流程，本次无需调整。

#### 待办事项

- [ ] 产品审阅 v2.3 本地 PRD 与预览；
- [ ] 用户确认后再更新文档中心或创建线上变更；
- [ ] 与商品、多语言、Home、统一身份、App 容器和数据平台完成开发前对齐。

### v2.2（2026-07-15）— 本地评审稿，未上传

#### 变更内容

- **PRD 版本**：v2.1 → v2.2，新建 `looply-Favorites-PRD-v2.2.md`，保留 v2.1；
- **原型版本**：V9 持续迭代；
- Wishlist 空态 `Explore`、少量商品 `Add more`，Recently Viewed 空态 `Explore`、单商品 `Explore more` 统一切换到 Home；
- 四个入口均定位到 `Explore Finds` 区域并选中 `For You`，不进入 Shop，也不停留在 Home 顶部。
- **2026-07-16 Demo 增量**：Recently Viewed 商品卡移除时钟图标并支持 Wishlist 心形操作，心形点击不穿透商品详情；
- 新增 Recently Viewed 收藏写入失败回滚轻提示；Sold Out 未收藏不可加入，已收藏仍可移出；
- Wishlist 完整列表取消收藏改为心形立即变空、卡片保留至刷新，包含 Sold Out 已收藏商品；
- Wishlist / Recently Viewed 新增 Price Drop 数量为 1 的单数文案演示；
- Price Drop 提示条去除模块内重复的 `wishlist/viewed` 来源词，统一为 `1 item dropped in price` / `{N} items dropped in price`；
- 新增 `Page · All data failed` 整页错误演示；两个核心模块失败但 Recommend 可用时仍展示 Recommend，所有数据源不可用时才进入整页错误；
- Wishlist / Recently Viewed Loading 均保持 3 张同结构商品卡骨架。

#### 影响范围

- **PRD**：新增 v2.2 本地评审稿及修订记录；
- **原型**：V9 Home 目标页改为 `Explore Finds · For You` 定位演示；
- **原型异常与收藏交互**：V9 已同步本轮已确认的 Wishlist、Recently Viewed、Price Drop、Sold Out 和整页失败规则；
- **Home 依赖**：需支持从 Favorites 携带目标区域与目标 Feed 状态进入。

#### 待办事项

- [ ] 产品评审 v2.2；
- [ ] 用户确认后创建文档中心独立分支和 PR；
- [ ] 与 Home 负责同事对齐定位参数和返回行为。

### v2.1（2026-07-15）— 本地评审稿，未上传

#### 变更内容

- **PRD 版本**：v2.0 → v2.1，新建 `looply-Favorites-PRD-v2.1.md`，保留 v2.0；
- **原型版本**：V9 持续迭代；
- Favorites 聚合页 `Liked Items` 统一更名为 `Wishlist`，同步模块标题、空态、错误、Price Drop 文案、Demo 状态选择器和无障碍名称；
- 取消收藏由“立即移除商品 + 3 秒 Undo”调整为：心形立即变空、卡片和当前显示数量保留、刷新后按 Wishlist 权威结果移除；
- 刷新前再次点击空心心形可恢复收藏；收藏操作失败时恢复原心形状态；
- 明确当前页面 View all / Add more 阈值在取消后不立即变化，刷新后随权威总数更新。

#### 影响范围

- **PRD**：新增 v2.1 本地评审稿及修订记录；
- **原型**：Wishlist 标题和延迟移除交互已更新；
- **Wishlist 依赖**：需确认完整页使用相同的收藏交互和刷新口径；
- **Recently Viewed / Recommend**：模块规则无变化。

#### 待办事项

- [ ] 产品评审 v2.1；
- [ ] 用户确认后再上传或创建在线文档；
- [ ] 正式交付前确认版本基线。

### v2.0（2026-07-15）— 本地评审稿，未上传

#### 新增交付物

- **综合 PRD**：`looply-Favorites-PRD-v2.0.md`
- **状态**：🔄 迭代中
- **说明**：在保留历史 PRD 的前提下，新建 v2.0，不覆盖 v1.3。

#### 变更内容

- 将综合 PRD 的职责收缩为 Favorites Overview 聚合展示，不再定义 Wishlist、完整浏览历史、匿名关联或推荐算法；
- 整合 Liked Items v1.10 和 Recently Viewed v1.5 的已确认展示规则；
- Liked Items 和 Recently Viewed 横向最多预览 30 件，并按各自数量阈值展示 View all 或 Home 引导；
- Price Drop 数量完全使用 Wishlist 或浏览历史上游结果，只统计仍在售且降价的商品，排除 Sold Out；
- Recommended for You 仅在推荐上游返回非空个性化结果时展示；行为数据不足、空结果或失败时静默隐藏；
- 推荐卡支持收藏，心形与商品卡点击区域独立；标题不展示副标题；
- Search 进入统一全局搜索，Cart 进入购物车；返回 Favorites 恢复页面状态；
- 明确模块失败不等于整页失败，并补充三个模块的一致性检查和原型字段映射；
- V9 原型增加 Recommend 可用、无用户数据和加载失败演示状态，并将 Liked 状态选择器统一命名为 `Liked · ...`。

#### 自检结果

- Liked Items 与 Recently Viewed Loading 均为 `Loading…`、3 张骨架卡，并隐藏 View all 与 Price Drop；
- Liked Items 与 Recently Viewed 同时失败时分别显示轻量错误，Recommend 有结果时继续展示；
- Recommend 在无用户数据和加载失败时均完全隐藏；
- `Recommended for You` 无副标题；推荐心形和卡片跳转已验证互不穿透；
- V9 浏览器运行未发现错误日志。

#### 影响范围

- **PRD**：新增综合 v2.0 本地评审稿；历史版本保留；
- **原型**：V9 持续迭代，已同步 Recommend 和状态选择器；
- **修订记录**：已追加 v2.0；
- **上游依赖**：Wishlist、浏览历史、推荐、商品、Home、Search、Cart 和页面容器；
- **架构图 / ER 图 / 流程图**：本期无新增实体或跨角色流程，未调整。

#### 待办事项

- [ ] 产品评审 v2.0 本地文档内容；
- [ ] 用户确认后再上传或生成在线文档；
- [ ] 与 Wishlist、完整浏览历史负责同事对齐 All / Price Drop 初始定位方式；
- [ ] 与推荐团队对齐“可以推荐 / 不推荐”的结果口径及必要商品字段；
- [ ] 与客户端确认 Search、Cart、Home、商品详情返回 Favorites 的位置恢复；
- [ ] UI 评审确认 V9 Demo 与正式全局组件的复用方式；
- [ ] 正式交付开发前确认交付基线、版本号和交付包范围。

---

## 使用说明

- 只有用户明确确认定稿并准备交付开发后，才建立正式交付包；
- 上传、发布或创建在线文档属于后续动作，本次未执行；
- 后续修改继续追加到当前进行中版本，定稿时再收敛最终方案。
