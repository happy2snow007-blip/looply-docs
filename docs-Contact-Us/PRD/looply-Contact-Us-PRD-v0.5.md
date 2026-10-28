# Looply Contact Us PRD v0.5

> 版本日期：2026-10-28
> 本文为全量有效规则工作稿；历史版本保留追溯。本次变化索引见《looply-Contact-Us-商品咨询迭代-PRD-v0.1.md》。

> UI 基线：[Looply 1.1 · 1027－客服弹层间距调整，新增商品卡](https://www.figma.com/design/sAOLkw0gIl1bwQRYCDqKuW/Looply-1.1?node-id=7267-64380&m=dev)，2026-10-28 核对。

## 一、范围与入口

Contact Us 为游客和登录用户提供咨询表单。访问和提交无需登录。普通入口为 PC Footer、Mobile 个人中心；本次仅调整商品详情与 Checkout 入口的咨询弹层，其他入口保持原状。

| 入口 | 初始商品 | 联系原因 | 内容构成 |
|---|---|---|---|
| 商品详情 | 当前商品 | 固定 Shopping Inquiries | 咨询表单 |
| Checkout | 本次结算商品 | 固定 Shopping Inquiries | 咨询表单 |
| 普通入口（沿用） | 沿用原表单 | 用户选择 | 咨询表单、地图、地址、邮箱列表 |

带入商品默认勾选。商品相关入口隐藏联系原因，提交至第三章 Shopping Inquiries 对应邮箱；即使最终没有选中商品，该分类仍保持不变。

页面不接入 CAPTCHA。咨询邮件为业务记录；不建立独立 Contact Us 业务记录或用户侧咨询历史。技术日志和埋点不得记录姓名、邮箱或留言原文。

## 二、页面展示

普通页面：PC 左侧地址与邮箱卡片、右侧表单；Mobile 单列。邮箱卡片标题为 `Email`，分类顺序见第三章，分类标题与邮箱分行，邮箱调用对应 mailto。地图与地址沿用现有配置。

商品相关入口使用现有咨询弹层；顶部展示 `Contact Us` 和关闭按钮。顶部说明沿用：`If you need any help, please contact us below. We usually respond within 1–2 business days.`

商详与 Checkout 弹层移除现有 `What can we help you with?` 标题及下拉框、Send 下方重复的回复时效说明，以及四类咨询名称与邮箱列表。回复时效仅在顶部说明展示。

普通入口沿用联系原因、Full Name、Email、Message、Send；商品详情与 Checkout 弹层为商品区域、Full Name、Email、Message、Send。

## 三、联系原因与分发

联系原因标签和占位为 `What can we help you with?`。

| 顺序 | 分类 | 适用咨询 | 收件邮箱 |
|---|---|---|---|
| 1 | Shopping Inquiries | 购物、订单、退货及买家服务；商品相关入口自动归入 | service@looply.com |
| 2 | Selling Inquiries | 向 Looply 出售商品 | sell@looply.com |
| 3 | Social Collaborations | 社媒达人、博主及内容合作 | influencer@looply.com |
| 4 | Corporate Partnerships | 企业、品牌商务合作 | partnerships@looply.com |

Selling Inquiries 仅在当前国家 C2 已启用且 Sell 已开放时展示并允许提交；其余分类不受 Sell 开关影响。服务端再次校验国家状态。已选出售咨询变为不可用时取消分类，保留其他输入并要求重选，不自动改投其他邮箱。

## 四、表单字段与校验

| 字段 | 必填与初始值 | 校验及错误 |
|---|---|---|
| 联系原因 | 必填；普通入口初始未选择，商品相关入口按第一章固定 | 必须为当前可用分类；`Please select a topic.` |
| Full Name | 必填；游客为空，登录用户带入账户姓名 | 去首尾空格后 1–100 字符；空值 `Enter your full name.`，超长 `Full name must be 100 characters or fewer.` |
| Email | 必填；游客为空，登录用户带入账户邮箱 | 去首尾空格后基础邮箱格式、最多 254 字符；空值 `Enter your email.`，格式错误 `Incorrect email` |
| Message | 必填；初始为空 | 去首尾空格后 1–2,000 字符；空值 `Enter your message.`，超长 `Message must be 2,000 characters or fewer.` |
| 咨询商品 | 仅商详与 Checkout 弹层，选填；默认值见第一章 | 通过第五章选择商品 |

姓名、邮箱、留言在失焦与 Send 时校验，错误显示在字段附近；未通过则阻止提交。账户资料读取失败时允许手动输入。编辑姓名与邮箱仅用于本次咨询。

占位分别为 `Enter your name`、`Enter your email`、`Enter your message`。用户输入保持原文。

## 五、咨询商品

### 5.1 表单展示与勾选

区域标题为 `Items you’re inquiring about`，右侧操作 `＋ Add items`。每件商品展示勾选框、缩略图、品牌、名称、成色和价格，沿用购物车小卡形式，展示信息来自商品数据。

用户可取消并重新勾选；取消后卡片保留在当前表单中。最终提交仅使用勾选商品。没有商品时仍可填写并发送咨询。

### 5.2 选择视图

点击 Add items，在 Contact Us 弹层上方叠加商品选择弹层；底层咨询表单保留已填写内容和当前商品选择。顶部为 `Add items` 标题和右上角关闭按钮 ×，来源为 `Recently viewed`、`Wishlist`，首次进入默认 Recently viewed。两处沿用 5.1 的商品小卡。

游客与登录用户均可使用 Recently viewed 和 Wishlist，无需为选择咨询商品登录。两个来源的空态与加载失败展示沿用对应 UI 设计稿。

已添加商品按当前勾选状态回显且可取消；切换来源保留本次选择，同一商品跨来源去重。底部按钮为 `Done`，允许以空选择确认。

Done 将本次最终选择替换咨询商品列表，关闭商品选择弹层并返回底层咨询表单；右上角 × 放弃本次修改，恢复进入选择视图前的商品及勾选状态，仅关闭商品选择弹层并回到底层咨询表单。以上操作只改变本次咨询范围。

## 六、发送与邮件

服务端按第三章固定映射校验并分发，客户端不能自行指定任意收件地址。邮件标题为 `Looply Contact Us - {submission time} - {Full Name}`，用户填写的 Email 作为回复地址。

正文按联系原因、Full Name、Email、Message 展示。在 Message 后、邮件正文最底部附上选中商品链接。链接区域标题为 `Items:`，每条一行，按 `Item 1: {商品链接}`、`Item 2: {商品链接}` 格式连续编号，单件也从 `Item 1` 开始；编号仅为本封邮件内的排列序号。仅提交去重后的链接，移除从 `?` 开始的参数。前台商品名称、商品编号、图片、成色及价格不作为新增商品信息提交。无商品则省略 Items 标题及链接部分。

| 状态 | 用户可见结果 |
|---|---|
| 提交中 | Send 置灰，禁止重复提交，保留全部内容 |
| 成功 | 邮件服务确认受理后，商详与 Checkout 入口关闭整个 Contact Us 弹窗；普通入口留在当前位置，清空姓名、邮箱、留言和分类；成功 Toast 展示 4 秒 |
| 失败 | 网络、超时、邮件服务拒绝或系统异常时保留输入及商品选择，允许重试；分类失效按第三章处理 |

成功文案：`Thanks for contacting us. We’ll get back to you as soon as possible.`；失败文案：`Submit failed, please try again.`

商详与 Checkout 入口提交成功关闭后，再次打开按第一章入口重新初始化咨询商品并默认勾选。

仅修改商品选择后主动关闭 Contact Us 弹窗时，直接关闭并放弃本次商品选择，不弹离开确认。商品选择变化不参与下述表单离开确认判断；若原有表单字段也发生变化，仍按下述规则处理。

姓名、邮箱、留言和可选联系原因以首次值为基线；字段变化后离开表单，沿用离开确认：`Leave without sending?` / `Your message hasn’t been sent. If you leave, your changes will be lost.`，`Stay` 保留，`Leave` 放弃并离开。商品选择弹层的 × 关闭按 5.2 处理。普通入口提交成功后，已清空字段作为新基线；商详与 Checkout 提交成功触发的关闭直接执行，不触发未发送离开确认。浏览器关闭、App 终止或跨设备访问不恢复草稿。

## 七、依赖与兼容

| 依赖 | 要求 |
|---|---|
| 商品详情、Checkout | 提供入口对应商品和可用于邮件的商品链接；展示字段沿用商品数据与当前价格、币种展示规则 |
| 最近浏览、Wishlist | 提供当前用户可访问的商品列表；选择咨询商品不改动来源记录 |
| 邮件服务 | 支持第三章分发、用户回复地址和正文末尾商品链接；受理前不显示成功 |
| 国家配置 | 前台与服务端对 C2、Sell 可用条件保持一致 |
| 公共法律文件 | 复用当前国家、语言下已批准生效的映射 |

普通页面表单局部失败时联系信息继续展示；联系信息失败时表单继续使用，失败区域提供 Retry。公共框架失败使用公共错误规则。

## 八、多语言、数据与引用

固定标题、分类、标签、按钮、占位和提示属于静态 UI 文案，进入 message package。新增文案包含 `Items you’re inquiring about`、`＋ Add items`、`Add items`、`Recently viewed`、`Wishlist`、`Done`。商品品牌、名称及成色复用商品已有翻译结果；邮箱、商品链接和用户输入保持原文。

### 8.1 数据与埋点

原有 Contact Us 提交、邮箱点击规则沿用《数据采集与埋点产品需求》；商品咨询补充以下采集要求。

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
- 提交结果中的商品数使用本次提交时的选中商品快照，去重计数；无商品时记为 0。成功、失败沿用第六章发送结果定义，成功表示邮件服务受理。
- 埋点不记录姓名、邮箱和留言原文。商品链接用于咨询邮件，不作为本次埋点新增字段。

### 8.2 引用依据

历史基线：Contact Us PRD v0.4（2026-10-14）；本次交互依据：2026-10-26 至 2026-10-27 用户截图、对话确认及 contact-demo.html。Demo 为模拟交互，不能作为已上线或运行验收证据。
