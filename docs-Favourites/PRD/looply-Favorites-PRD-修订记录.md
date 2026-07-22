# Looply Favorites PRD 修订记录

| 版本 | 日期 | 修改人 | 修改内容 |
|---|---|---|---|
| v1.0 | 2026-07（原文未记录具体日期） | 未记录 | 建立 Favourites 聚合入口，采用四个子 Tab；Saved Searches 与 Recommended 为占位，配套原型 v3。 |
| v1.1 | 2026-07-07 | 未记录 | 改为概览页与全屏面板结构；移除 Saved Searches；Recommended 改为 Feed；配套原型 v6。 |
| v1.2 | 2026-07-14 | Codex 草拟，待产品确认 | 以 V8 为基线统一 Favorites、Liked Items、Recently Viewed、推荐 Feed 和 Me；补充促销口径、匿名身份、状态同步及验收标准。 |
| v1.3 | 2026-07-14 | Codex 草拟，待产品确认 | 基于 V8 实际页面交互补齐加载、失败、离线、空态、并发冲突、迟到响应、跨端同步和恢复规则；新增原型字段映射、依赖关键假设及健壮性自检。 |
| v2.0 | 2026-07-15 | Codex 草拟，待产品评审 | 按 V9 重构为 Favorites Overview 聚合展示 PRD；收缩 Wishlist、完整浏览历史、身份和推荐算法边界，整合 Liked Items、Recently Viewed、条件推荐、全局搜索、购物车及模块级异常规则。 |
| v2.1 | 2026-07-15 | Codex 草拟，待产品评审 | 聚合页 `Liked Items` 统一更名为 `Wishlist`；取消收藏改为心形取消填充但卡片和当前数量暂不移除，下次刷新后按权威结果移除，不再使用立即移除与 Undo。 |
| v2.2 | 2026-07-15 | Codex 草拟，待产品评审 | Wishlist 与 Recently Viewed 的 Explore、Add more、Explore more 统一跳转至 Home，并定位 `Explore Finds · For You`。 |
| v2.3 | 2026-07-16 | Codex 草拟，待产品评审 | 收口评审结论：统一双模块 Loading 与异常层级；Recently Viewed 支持 Wishlist；明确 Sold Out、Price Drop、整页失败、登录与匿名主体切换；新增多语言归属和简版数据采集要求。 |
| v2.4 | 2026-07-16 | Codex 草拟，待产品评审 | 清理正文的模板标记和内部跳转锚点；美国 MVP 语言范围明确为英语（en-US）和西班牙语（es-US）。 |
| v2.5 | 2026-07-16 | Codex 草拟，待产品评审 | 明确 Wishlist 与 Recently Viewed 的 View all 为跳转入口，不属于 Favorites 内加载更多；移除横向补充失败及列表末尾 Retry 状态。 |
| v2.6 | 2026-07-16 | Codex 草拟，待产品评审 | 缓存刷新失败改为调用 App 全局组件；Favorites 仅定义保留缓存内容和当前模块重试，不再定义独立提示条样式、文案或交互。 |
| v2.7 | 2026-07-16 | Codex 草拟，待产品评审 | 第二轮评审收口：刷新触发复用 App 统一策略；下拉刷新并行请求三个模块；缓存刷新失败可见且仅重试失败模块；三处心形失败统一回滚；组合失败改为页面状态；推荐上游只返回可购买商品。 |
| v2.8 | 2026-07-16 | Codex 草拟，待产品评审 | 补齐 V9 最新交互：缓存刷新失败统一在对应模块标题下显示行内提示与模块级 Retry；统一 Wishlist 写入失败回滚后的轻量 Toast；明确仅有在售 / Sold Out 两类商品状态，Sold Out 已收藏仍可取消；推荐上游仅返回可购买商品。 |
| v2.9 | 2026-07-20 | Codex 根据产品确认收口 | 写入模拟评审的 4 项确认结论；正文按封闭范围原则精简，删除已由正向规则覆盖的替代方案、解释性反例和下游完整列表加载细节，不改变产品行为与验收边界。 |
| v2.10 | 2026-07-22 | Codex 根据产品确认补充 | 明确 Favorites 本期仅支持 App 与 H5 Mobile，H5 Mobile 沿用 App 的移动端页面结构与交互体验；PC Web 不在本期范围，并补充对应验收标准。 |
| v2.11 | 2026-07-22 | Codex 根据产品确认补充 | 收口 Recommended for You 的行为来源、仅浏览分段判断、购买信号边界和结果过滤；Recently Viewed 概览卡与完整页统一为删除浏览记录，不显示 Wishlist 心形，并补充删除失败、i18n、埋点和验收规则。 |
