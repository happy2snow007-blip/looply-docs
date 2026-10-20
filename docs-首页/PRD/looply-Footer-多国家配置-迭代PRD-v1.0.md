# Looply Footer 多国家配置迭代 PRD

版本：v1.0（工作稿更新）
日期：2026-10-20

## 一、迭代目标

本次文件配置交付覆盖后台的国家隔离、法律文件、FAQ、社媒账号及生效内容输出。PC Footer 的国家语言入口展示和各页面消费由其他已有需求覆盖，不属于本次后台验收。

本文只记录本次变化；完整后台规则见[文件配置 PRD v1.0](./looply-文件配置-PRD-v1.0.md)，Footer 既有规则及 Contact Us 国家信息增量见[Footer 与关联页面 PRD v0.8](./looply-Footer-PRD-v0.8.md)。Contact Us 页面、四类联系原因、邮箱和提交行为统一引用[Contact Us PRD v0.4](../../docs-Contact-Us/PRD/looply-Contact-Us-PRD-v0.4.md)。

## 二、后台国家范围

- 后台菜单调整为「文件配置」，页面顶部仅保留国家选择；国家来自 C2 业务国家管理，允许提前维护未启用国家。
- 国家和页签切换统一执行文件配置 PRD 第一章的未保存处理：继续编辑或放弃；放弃恢复已保存内容。

## 三、C1 Sell 联动

国家级 Sell 条件和 Footer 入口联动统一引用[C1 Sell 多国家支持迭代 PRD v1.2 · 3.2、3.3 节](../../docs-C1-Sell/PRD/looply-C1-Sell-多国家支持-迭代PRD-v1.2.md)。Contact Us 的 `Selling Inquiries` 及其邮箱按 Contact Us PRD v0.4 第三章处理；其他三类咨询保持可用。

## 四、文件配置职责调整

FAQ 翻译沿用已有资源标识与接入配置；本轮维护条目及源内容版本与既有资源的关联。

法律文件、FAQ 和社媒账号的完整配置规则见 [文件配置 PRD v1.0](./looply-文件配置-PRD-v1.0.md)。

本次变化：法律文件按市场支持语言分别上传并自动预览校验，全部语言通过后发布；保留线上及历史下载，回滚调整为当前国家、同一文件类型按历史发布批次恢复，具体规则见《文件配置 PRD v1.0》2.3 节。FAQ 固定全量覆盖，支持下载后修改或自行制作文件，条目匹配及保存校验见该 PRD 3.1 节；取消启停，支持直接删除、排序及首页精选。上传格式为 .html。

## 五、Contact Us 国家规则

本次在 Contact Us PRD v0.4 基础上保留已确认的国家信息增量：提交关联当前国家、页面语言、所选联系原因、UTC 时间和唯一 Request ID；邮件标题由 v0.4 的原格式调整为包含国家代码的格式，正文同时补充国家上下文和请求信息。

完整标题格式、国家校验、失败重试及最小记录规则在 Footer 全量稿第五章唯一定义。四类联系原因、固定收件邮箱、出售咨询资格、成功后清空四字段等规则继续执行 Contact Us v0.4，不再沿用旧的 BUY／SELL 两类描述。

## 六、Demo 与验收

- 后台交互使用 CMS 统一配置入口 v80 及[当前文件配置 Demo](../原型/looply-Footer-多国家配置-迭代Demo-v1.0.html#/footer)；本次后台验收统一执行文件配置 PRD 第六章。
- Contact Us 国家信息增量按 Footer 全量稿第五章单独核验。Footer 前台入口、法律页、FAQ 页和首页的联合验收由对应消费需求组织。

## 七、关联文档

- 全量规则：[Footer 与关联页面 PRD v0.8](./looply-Footer-PRD-v0.8.md)
- C1 Sell 国家开关：[C1 Sell 多国家支持迭代 PRD v1.2](../../docs-C1-Sell/PRD/looply-C1-Sell-多国家支持-迭代PRD-v1.2.md)
- 接入及交付依赖：[文件配置技术依赖 Checklist](./looply-文件配置-技术依赖Checklist.md)
