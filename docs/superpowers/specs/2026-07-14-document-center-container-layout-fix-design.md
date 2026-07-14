# 文档中心正文容器布局修复设计

## 背景

文档中心首页的公共样式为 `.container { margin: 28px 32px; }`。登录注册等前 15 个模块位于 `.container` 内，导航与正文卡片之间具有统一间距；Favourites 及其后的模块位于 `.container` 外，导致正文卡片紧贴侧栏。

根因是 `index.html` 在“订单列表/详情”模块之后提前关闭了 `.container`，而 Favourites、收藏与浏览历史、shop页、Collection管理和社媒分享管理是在该闭合标签之后追加的。

## 目标

- 保证首页所有 `.module-section` 都由同一个 `#content.container` 包裹。
- 让 Favourites、收藏与浏览历史、shop页、Collection管理和社媒分享管理获得与登录注册一致的 32px 正文侧边距。
- 不改变模块内容、顺序、链接、版本信息和现有视觉样式。

## 方案

采用最小 HTML 结构修复：

1. 删除 Favourites 模块之前提前出现的 `.container` 闭合标签。
2. 在社媒分享管理模块结束后、Footer 之前补上 `.container` 闭合标签。
3. 保留 Footer 在 `.main-content` 内、`.container` 外，避免 Footer 继承正文卡片边距。

不采用模块级 margin 补丁，因为该方案会掩盖错误 DOM 层级；不为每个模块增加独立容器，因为会增加无必要的重复结构。

## 验证

修复前先运行结构回归检查，确认测试能检测到 5 个模块不在 `.container` 内。修复后重新运行并满足：

- 首页全部 20 个 `.module-section` 的最近 `.container` 祖先均为 `#content`。
- `.container` 在 Footer 之前正确闭合。
- Git diff 只包含闭合标签移动和本设计说明。
- 推送后在 GitHub Pages 检查目标模块的正文左边距与登录注册一致。

## 发布与回滚

验证通过后提交并直接推送 `main`。若线上验证失败，回滚该修复提交即可恢复原有结构；本次不触碰文档产物和同步配置。
