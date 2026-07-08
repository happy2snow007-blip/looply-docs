# Looply Favourites 变更日志

---

## v1.1（2026年7月）

**文件**：looply-Favourites-PRD-v1.1.md  
**配套原型**：looply-favourites-prototype-v6.html  
**状态**：迭代版本

### 主要变更

- **页面结构调整**：从「子 Tab 切换」改为「概览页 + 全屏面板」双层结构。概览页聚合展示 Wishlist / Recently Viewed / Recommended 三个区块。
- **降价强调入口**：Wishlist 和 Recently Viewed 区块各新增绿色强调条，显示降价/促销商品数量，点击后深链进入对应全屏面板的 Price Drop / On Sale tab。
- **全屏面板三 Tab 筛选**：Wishlist 面板改为 All / In Stock / Price Drop 三个 tab；Recently Viewed 面板改为 All / In Stock / On Sale 三个 tab，替换原有的 pill 筛选。
- **Saved Searches 移除**：本期从 Favourites 模块完全移除，不设占位页，二期单独立项。
- **Recommended 升级**：从「占位页」升级为实际功能——概览页底部展示双列瀑布流商品 Feed，与首页 Feed 卡片风格一致，无独立全屏面板。
- **Header 图标修正**：右侧图标改为搜索 + 购物车（原为搜索 + 用户）。

---

## v1.0（2026年7月）

**文件**：looply-Favourites-PRD-v1.0.md
**状态**：全新创建，首个版本

### 主要内容

- 新建 Favourites 模块 PRD，作为 APP Tab Bar 第 3 Tab 的聚合收藏中心。
- 定义 4 个子 Tab 框架：Wishlist / Recently Viewed / Saved Searches（占位）/ Recommended（占位）。
- Wishlist 子 Tab：完整复用「收藏与浏览历史 PRD v1.0」§2.1 全部规则，含筛选/降价高亮/失效态/Buy Now/无限滚动/空态。
- Recently Viewed 子 Tab：完整复用「收藏与浏览历史 PRD v1.0」§2.2 全部规则，含单条删除/Clear All 居中弹窗/失效态/Buy Now/无限滚动/空态。
- 公共组件：ProductCard 提取为公共组件，定义失效态三态完整枚举（active / active+discount / sold+off_shelf）。
- 跨模块横切：未登录双行分离模型 + 登录后复制上移，完全引用原 PRD 第四章。
- 与原独立页模式唯一差异：无返回键，通过子 Tab 切换导航。

### 参考输入源

- 收藏与浏览历史 PRD v1.0（业务规则完整引用）
- APP 设计稿截图（收藏列表 / 浏览历史 / Clear All 弹窗 / loading 规范）
- 原型 looply-favourites-prototype-v3.html
