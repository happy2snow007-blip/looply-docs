# C1 Sell 本轮开发反馈回复

C1 Sell 本轮反馈结论如下，请以用户端 PRD v0.7、运营后台 PRD v1.1 及当前 Figma UI 为准。

## 1. 时间口径

- 所有时间字段按洛杉矶时区 `America/Los_Angeles` 存储，接口传输时保留明确的时区偏移，避免夏令时切换产生歧义。
- 页面展示、日期筛选、Contact Us 提交时间及 Request ID 的 `YYMMDD`，与 C2 保持一致，按美东时区 `America/New_York` 计算并自动适配夏令时。
- Preferred date 按用户选择的日期值保存，不进行跨时区换日。

## 2. Appointments Download

- 保留 Download 功能，导出当前关键词和日期筛选共同命中的全部预约记录。
- CSV 不包含图片文件、照片链接或 Attachment ID。
- 图片仅允许已登录的 C1 运营人员在预约详情中在线查看。
- 每次成功下载继续记录下载账号、下载时间、筛选条件和导出记录数。
- 同步或异步生成由技术根据数据量决定；如果需要限制导出数量或改变“导出全部筛选结果”的规则，再找产品确认。

## 3. 翻译

- Category name 新增并登记 `seller_category` 翻译资源，字段为 `name`，支持 `en-US → es-US`，缺少西语译文时回退英语。
- Brand name 属于品牌专有名词，不翻译。
- 页面按钮、标题、提示和校验等静态 UI 文案复用现有自动翻译能力。
- Seller Agreement 不自动翻译，英语和西语分别使用业务提供文档中的正式正文。
- `domain_code`、`group_code`、稳定资源 ID 和 catalog 登记由多语言/开发按现有翻译系统规范确定，不需要产品选择。

## 4. UI 与输入资料

- PC 和 Mobile 都属于本期范围，分别以当前 C1 Figma 对应设计为准，Mobile 不按 PC 缩放实现。
- Figma 节点、PRD、运营后台 Demo 和 manifest 路径由开发按最新文件重新登记，不继续使用旧路径。
- Mobile 如果缺少具体页面或状态，由 UI 补齐设计，不缩减已确认范围。
- 运营后台以当前 HTML Demo 演示核心正常流程，异常状态和完整验收边界以运营后台 PRD 为准。

## 5. 已有明确结论

- 确认邮件属于本期：预约创建后自动发送，后台展示 `Pending / Sent / Failed`，失败支持人工重发。
- In-Home 不增加协议勾选框，点击 `Submit Request` 即表示同意 Seller Agreement，并记录协议版本和同意时间。
- Ship To Us 必须勾选 Seller Agreement。
- ZIP City/State 回填复用现有 `Postal/addressconfig`。
- Category name 在 C1 Sell 范围内大小写不敏感且不可重复。
- Appointments 搜索范围仅为 Request ID、Full name、Email。
- 当前后台采用单一 C1 运营角色；字段脱敏、细分权限、通用操作审计和数据保留策略按 PRD 作为后续规划。
- Seller Agreement 与 FAQ 使用产品提供的现有业务文档；发布时请固定对应正文版本及生效时间。

## 6. 技术与安全实现

以下不需要产品二选一，由技术、安全或国际化负责人按照现有平台规范设计：

- C1 游客图片上传如何适配现有登录限制和 9 张限制；产品规则仍为最多上传 10 张。
- 防重复提交的幂等键、限流窗口和错误码。
- OpenAPI snapshot、manifest 和正式输入路径同步。
- 邮件 Pending 超时、自动重试及最终转为 Failed 的阈值。
- 预约详情图片的登录鉴权方式。
- 翻译资源的技术标识与 catalog 登记。

如果技术方案需要新增验证码等用户交互、限制导出数量、减少 Mobile 范围或改变上述产品规则，再单独提交产品确认。当前没有其他待产品确认项。
