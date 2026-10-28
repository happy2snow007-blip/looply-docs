# Looply Contact Us 商品咨询迭代 PRD v0.1

> 日期：2026-10-28
> 范围：仅商品详情与 Checkout 入口的咨询弹层；其他入口保持原状。完整规则见《looply-Contact-Us-PRD-v0.5.md》。

> UI 基线：[Looply 1.1 · 1027－客服弹层间距调整，新增商品卡](https://www.figma.com/design/sAOLkw0gIl1bwQRYCDqKuW/Looply-1.1?node-id=7267-64380&m=dev)，2026-10-28 核对。

## 一、目标与入口

让客服直接识别用户咨询的商品，减少补充商品链接的往返沟通。

商详和 Checkout 入口均通过底部弹层打开 Contact Us。

| 入口 | 默认咨询商品 | 联系原因 |
|---|---|---|
| 商品详情 | 当前商品，默认勾选 | 自动归为 Shopping Inquiries |
| Checkout | 本次结算商品，默认勾选 | 自动归为 Shopping Inquiries |

两个入口的邮件自动发送至 service@looply.com。相对现有弹层，移除：

- `What can we help you with?` 标题及咨询类型下拉框。
- Send 下方的 `We generally respond to customer inquiries within 1–2 business days.` 回复时效说明。
- Send 下方的四类咨询名称及对应邮箱列表。

顶部 Contact Us 标题、关闭按钮及原说明文案保留，回复时效在顶部说明中展示一次。

## 二、表单中的商品区域

商品区域位于姓名字段之前。

标题使用 `Items you’re inquiring about`，右侧为 `＋ Add items`。商品采用购物车小卡，展示勾选框、缩略图、品牌、商品名称、成色和价格。用户通过勾选调整咨询范围，商品展示信息由系统提供。

取消勾选后商品仍留在当前表单列表，允许重新勾选；提交仅携带已勾选商品。未选择商品时仍可提交一般咨询，入口确定的购物咨询类型保持不变。

仅修改商品选择后主动关闭 Contact Us 弹窗时，直接关闭并放弃本次商品选择，不弹离开确认。商品选择变化不参与表单离开确认判断；原有表单字段发生变化时，仍沿用全量 PRD 第六章的离开确认规则。

## 三、选择商品

点击 `＋ Add items`，在 Contact Us 弹层上方叠加商品选择弹层；底层咨询表单保留已填写内容和当前商品选择。

选择弹层顶部为 `Add items` 标题和右上角关闭按钮 ×；下方提供 `Recently viewed`、`Wishlist` 两个来源，商品卡展示与第二章一致。首次进入默认显示 Recently viewed。

游客与登录用户均可使用 Recently viewed 和 Wishlist，无需为选择咨询商品登录。两个来源的空态与加载失败展示沿用对应 UI 设计稿。

已添加商品默认按表单当前勾选状态回显，并允许取消或重新选中。切换来源保留本次选择，同一商品跨来源去重。底部操作为 `Done`。

- 点击 Done：以本次最终勾选结果统一更新咨询商品列表，关闭商品选择弹层并返回底层咨询表单；全部取消也可确认。
- 点击右上角 ×：放弃本次修改，恢复进入选择视图前的商品与勾选状态，仅关闭商品选择弹层并返回底层咨询表单。
- 选择视图内操作只调整本次咨询商品，不改变购物车、Wishlist 或最近浏览记录。

## 四、提交与邮件变化

商品附加信息仅提交用户最终选中商品的链接，去重后每条一行；链接去掉从 `?` 开始的查询参数。前台小卡的图片、品牌、名称、成色、价格和商品编号不作为本次新增商品信息提交。

邮件正文先沿用联系原因、Full Name、Email、Message；商品链接位于 Message 之后、整封邮件正文最底部。链接区域标题为 `Items:`，每行按 `Item 1: {商品链接}`、`Item 2: {商品链接}` 格式连续编号，单件也从 `Item 1` 开始。编号仅为本封邮件内的排列序号。未选商品时省略标题及链接部分。

示例：

```text
Shopping Inquiries
Full Name: …
Email: …
Message: …

Items:
Item 1: https://www.looply.com/en-US/product/gucci-leather-belt-brown-CP2R36F9V7RVC
```

字段校验、邮件标题、回复地址与发送反馈沿用全量 PRD 第四、六章。

商详与 Checkout 入口提交成功后，关闭整个 Contact Us 弹窗。再次打开时按入口重新初始化咨询商品：商详带入当前商品，Checkout 带入本次结算商品，默认勾选。

## 五、数据与埋点

本次商品咨询埋点仅覆盖商品详情与 Checkout 入口，统一使用 `ui_interaction`。以下为本期新增或扩展的定义；开发需同步登记事件字段、枚举及模块到埋点契约。既有公共事件封装沿用统一规范。

| 动作 | module_id | interaction_name | action | element_id | 必填附加字段 |
|---|---|---|---|---|---|
| 点击 Add items | contact_items | inquiry_item_picker | open | contact_add_items_button | inquiry_entry |
| 勾选商品 | contact_items | inquiry_item_selection | select | contact_item_checkbox | inquiry_entry、selection_surface、item_source |
| 取消勾选 | contact_items | inquiry_item_selection | deselect | contact_item_checkbox | inquiry_entry、selection_surface、item_source |
| 点击 Done | contact_items | inquiry_item_picker | confirm | contact_items_done_button | inquiry_entry、selected_item_count、added_item_count、removed_item_count |
| 表单提交结果 | contact_form | contact_request | submit | contact_submit_button | inquiry_entry、selected_item_count；保留原有结果字段 |

| 字段 | 类型 | 取值与含义 |
|---|---|---|
| inquiry_entry | string | `product_detail` / `checkout`；打开咨询弹层时确定，后续操作保持不变，不依赖 source_page_id |
| selection_surface | string | `form`：咨询表单的商品列表；`picker`：Add items 选择视图 |
| item_source | string | `default` / `recently_viewed` / `wishlist`；表单记录默认带入或最近一次确认添加来源，选择视图记录本次操作所在 Tab |
| selected_item_count | integer | 去重后的最终选中商品数，非负；Done 使用确认结果，提交事件使用本次提交快照 |
| added_item_count | integer | 相对进入选择视图时已选集合，Done 确认时新增的商品数，非负 |
| removed_item_count | integer | 相对进入选择视图时已选集合，Done 确认时移除的商品数，非负 |

表单中的勾选、取消直接改变本次咨询范围；商品选择弹层仅改变临时选择，点击 Done 后才更新咨询范围，右上角 ×则放弃本次修改。两处均上报实际发生的勾选或取消操作，以 selection_surface 区分。

Add items 在用户点击时上报一次；每次实际勾选状态变化上报一次；Done 每次确认上报一次。提交结果扩展现有 contact_request / submit，结果字段沿用现有定义（success / failed）；统计时不叠加 contact_submit / submit，不因本期扩展再发送一份提交结果事件。

统计规则：

- 默认勾选、状态回显及切换来源引起的渲染不计为用户勾选操作。选择视图内的商品来源按本次操作所在的 Recently viewed 或 Wishlist 记录；表单中的商品来源按默认带入或最近一次确认添加的来源记录。
- 商品来源按一次弹窗会话管理：入口默认商品的表单来源固定为 `default`，取消再勾选仍保持 default；其他商品在选择视图最后一次从未选变为选中时记录对应 Tab，Done 后提交该来源供表单使用。同一商品跨 Tab 仅展示或保持选中不改来源；取消后在另一 Tab 重新勾选，使用后一个 Tab。右上角 × 同时放弃本次来源变更，表单直接取消、重选不改既有来源。
- 点击 Send 后，若表单校验未通过，本次尝试上报一次 `contact_request / submit`，`result_state=failed`、`failure_type=validation_failed`，携带 `inquiry_entry` 和当次去重后的 `selected_item_count`（可为 0）；不发送邮件。失焦校验不触发提交结果事件。校验通过后的发送成功或失败按本次发送终态上报一次；沿用既有失败分类，不上报自由错误文本。统计“邮件发送失败”时排除 validation_failed。
- Done 的新增、移除数量，以进入选择视图时已勾选的商品集合为基线，与确认时的集合比较；商品去重计数。未调整直接确认时新增、移除均为 0，全部取消时最终选中商品数为 0。
- 右上角 × 放弃的选择不计入 Done 确认结果；此前真实发生的勾选、取消仍作为操作事件保留。
- 提交结果中的商品数使用本次提交时的选中商品快照，去重计数；无商品时记为 0。成功、失败沿用全量 PRD 第六章发送结果定义，成功表示邮件服务受理。
- 埋点不记录姓名、邮箱和留言原文。商品链接用于咨询邮件，不作为本次埋点新增字段。

## 六、关联与验收

交互依据为 2026-10-26 至 2026-10-27 本次对话确认与 contact-demo.html；商品卡参照用户提供的购物车截图。Demo 为交互示意，示例商品及价格不作为真实业务数据。

验收需覆盖入口默认商品与分类、表单取消及重新勾选、选择视图跨来源选择与去重、Done 全量更新、× 关闭撤销修改、表单输入保留，以及邮件末尾仅包含去参数后的选中商品链接。

埋点验收覆盖两个入口、两处勾选操作及三类商品来源；核对默认勾选不报操作、Done 无变化与全部取消的数量、× 关闭放弃不报 Done，以及提交成功和失败时商品数量与本次提交快照一致。
