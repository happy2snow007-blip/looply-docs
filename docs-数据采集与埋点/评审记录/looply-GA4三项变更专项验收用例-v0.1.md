# Looply GA4 三项变更专项验收用例

> 版本：v0.1  
> 日期：2026-09-01  
> 适用范围：`view_item_list`、`page_view`、`view_search_results` 三项临时收口变更

## 一、view_item_list

| 场景 | 预期 |
|---|---|
| 首次列表请求成功 | 发送1条；含初始已加载商品和新的`list_instance_id` |
| 搜索／筛选／排序／首页Tab形成新结果且请求成功 | 发送1条新的`view_item_list` |
| 滚动、分页追加、失败、取消、未提交、重复条件、结果未变化、重复回调 | 0条 |
| 后续商品点击 | `select_item`复用当前列表的`list_instance_id` |
| 卡片达到可视阈值 | 仅保留一方曝光，不产生GA4 `view_item_list` |

## 二、page_view

| 场景 | 预期 |
|---|---|
| 硬加载 | 有GA自动`page_view`，无Looply主动`page_view` |
| 现有SPA导航 | 按当前GA自动history配置实测记录，不新增受控SPA Tag |
| 任意业务页面事件 | 页面实例上下文仍可关联；不产生`looply_ga4_page_view` |

## 三、view_search_results

| 场景 | 预期 |
|---|---|
| 成功、零结果、失败、取消 | 每个请求唯一终态仅1条主动事件 |
| 请求替换、晚到回调、重复回调、离页后结果 | 不重复发送 |
| 业务字段 | 保留`result_status`、`result_count`、`duration_ms`、`filter_ids`、`sort_type`及来源字段 |
| GA4网站搜索 | 设置保持关闭；不得出现自动第二条同名事件 |
