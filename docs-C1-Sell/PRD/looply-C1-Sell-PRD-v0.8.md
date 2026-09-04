# Looply C1 Sell PRD

版本：v0.8  日期：2026-09-04  状态：开发评审候选版

## 一、产品范围

C1 Sell 为用户提供三种出售方式：In-Home Appointment、Visit Looply、Ship To Us。本次用户端开发范围覆盖 PC / Mobile 入口、Sell 首页、Accepted Brands、Condition Guidelines、Service Area、预约提交和 Contact Us。运营后台由独立 PRD 定义；埋点后续补充。预约确认邮件属于本期范围。

PC 与 Mobile 均纳入本期。两端业务流程、字段、校验、状态和跳转结果一致；入口、布局及交互触发方式分别以 Figma 对应 PC / Mobile UI 为准，Mobile 不按 PC 页面缩放实现。

用户无需登录即可进入并提交 Seller Request。游客提交后以系统生成的 Request ID 标识本次申请，不要求绑定 Looply 账号。

## 二、入口与页面

| 页面 / 区域 | 入口与核心交互 |
|---|---|
| Sell 首页 | PC Header `SELL`、Footer Sell 分组、Mobile Sell Tab；Hero `Sell Now` 进入预约，`Explore your options` 定位 Three Ways to Sell |
| Three Ways to Sell | In-Home / Visit / Ship 方式卡片；PC 侧卡 Hover 后放大并展示对应详情；Mobile 使用 Figma Mobile UI 中的独立交互，不使用 Hover |
| What We Buy | 固定约 10 个品牌横向滚动；`View All Brands & Categories` 进入完整品牌页 |
| Selling Tips / How to Get Paid | 展示说明和步骤，不设置额外跳转 |
| FAQ / 底部 CTA | FAQ 折叠；`View All FAQs` 进入 Seller FAQ；`Sell Now` 进入预约 |
| Footer 新增 | Sell with Looply、Accepted Brands、Service Area、Condition Guidelines、Seller FAQ、Seller Agreement |
| Accepted Brands | 品类筛选、品牌首字符实时过滤；完整列表读取后台生效配置 |
| Condition Guidelines | 9 个成色判断模块，前 8 个按 Accepted / Not Accepted 展示；Jewelry and Watches 按 UI 合并说明展示 |
| Service Area | ZIP 查询；返回覆盖、未覆盖或非法 ZIP 状态 |

## 三、预约流程

### 3.1 个人信息

采集 `First name *`、`Last name *`、`Phone *`、`Email *`。联系授权必须勾选；未勾选时阻止进入下一步并展示字段错误。联系授权文案链接复用 C2 的 `Privacy Policy` 和 `Terms of Service`。`Continue` 校验通过后进入下一步。

### 3.2 物品信息

品类读取运营后台全部 Active 配置并按后台顺序展示，至少选择一项且支持多选；品牌至少输入一项且支持多选。选择品类后按对应品类下的 Active 品牌配置联想，未选择品类不联想；后台未配置的品牌仍可手动输入。总件数为必填单选：1–2、3–5、6–9、10+；补充备注为选填，最多 300 个字符。照片选填，最多 10 张。必填项缺失 Toast：`Please complete all required fields to continue.`

### 3.3 选择售卖方式

用户输入必填 ZIP，系统复用地址页 ZIP 校验并查询覆盖配置。支持上门时默认勾选 `In-Home Appointment`；不支持上门时默认勾选 `Ship To Us`，`In-Home Appointment` 置灰；`Visit Looply` 始终可选。

ZIP 输入接受 5 位格式（如 `90048`）和 ZIP+4 格式（如 `90048-1234`）。上门覆盖统一取前 5 位查询。用户在 Step 4 修改 ZIP 后，系统重新查询覆盖；若新 ZIP 不支持上门，则不能提交 In-Home，需要返回 Step 3 选择其他可用方式。

预约流程固定为四步：Step 1 个人信息、Step 2 物品信息、Step 3 ZIP 与售卖方式、Step 4 方式信息（In-Home / Visit Looply / Ship To Us 分支）。进度条始终展示四段，方式分支属于第 4 步。

Step 3 查询完成后展示 `In-Home Appointment`、`Ship To Us`、`Visit Looply` 三张售卖方式卡片及对应说明。用户可点击任一可用卡片切换方式；系统保留已填写的 ZIP 和物品信息，进入 Step 4 时展示所选方式表单。未覆盖时 In-Home 卡片置灰，仅 Ship To Us 与 Visit Looply 可选；点击 `Continue` 进入所选方式的 Step 4，点击 `Back` 返回 Step 2。

### 3.4 方式信息

- In-Home：Street address、City、State、ZIP code 必填；Apartment、Preferred date、Referral code 选填。保持 UI 当前设计，不设置协议勾选框；用户点击 `Submit Request` 即表示同意 Seller Agreement，系统记录本次适用的协议版本和提交时间。
- Visit Looply：固定地址 `6300 Wilshire Blvd, Los Angeles, CA 90048 Appointment only.`；Preferred date、Referral code 选填。
- Ship To Us：Street address、City、State、ZIP code 和 Seller Agreement 勾选必填；Apartment 选填。

提交失败时停留在 Step 4，保留全部已填信息并展示提交失败提示及 `Retry`；点击 `Retry` 重新提交，并继续执行公共防重复提交规则。

### 3.5 成功页与 Request ID

成功页展示 `Request received`、Selling method、Total pieces 和 Preferred date（未填写时隐藏整行）。Request ID 格式为 `[METHOD]-[YYMMDD]-[LOCATION]-[RANDOM]`：方法码 `IH` / `VL` / `ST`；日期为正式提交日期；Visit Looply 的 Location 为 `LA`，其他方式使用客户地址州缩写；RANDOM 为后台生成并校验唯一性的 6 位大写字母和数字。

## 四、配置与数据来源

In-Home 支持 ZIP、可回收品类及品类对应品牌由运营后台维护，后台字段、层级、状态和生效规则详见[《C1 Sell 运营后台 PRD》](./looply-C1-Sell-运营后台-PRD-v1.2.md)。前台仅读取生效配置；ZIP 覆盖判断与品牌 / 品类可回收判断相互独立。首页 What We Buy 滚动品牌为固定内容，不读取后台。

## 五、Contact Us

页面字段：Business Type（Sell / Buy）、Full Name、Email、Message，均为必填。Sell 提交至 `sell@looply.com`，Buy 提交至 `service@looply.com`。邮件标题统一为 `Looply Contact Us - {submission time} - {Full Name}`，正文包含页面填写信息。

## 六、邮件、后台与法律文件

预约记录及运营后台规则由[《C1 Sell 运营后台 PRD》](./looply-C1-Sell-运营后台-PRD-v1.2.md)独立定义。预约提交成功后，由 `sell@looply.com` 自动向用户发送确认邮件；发送状态和失败后的人工重发在运营后台处理。其他预约后续指引邮件后续补充。Contact Us 的 Sell / Buy 邮箱分流仍属于本期范围。

全站 `Terms of Service`、`Privacy Policy`、`Your Privacy Choices` 与 C2 共用，直接复用现有页面，不重新建设。Sell 使用 `Seller Agreement`；英文和西语版本均以[业务提供文档](https://zhuanspirit.feishu.cn/docx/X2vjdYalQopAskxavSTcB4pAnR2?from=from_copylink)中的对应文本为准，西语版本直接使用文档内容，不进行自动翻译。开发需按文档版本发布对应语言页面。

## 七、多语言、埋点与校验

本期支持英语（`en-US`）和西语（`es-US`）。普通 UI 文案复用现有自动翻译能力，无需产品逐条提供西语译文；译文缺失时回退英语。运营配置的 Category name 作为动态业务内容接入 `seller_category` 翻译资源，源语言为英语、目标语言为西语，缺少西语译文时回退英语。Seller Agreement 属于例外：英语和西语均直接使用业务文档中的对应正文，不进行自动翻译。

埋点需求后续补充，不纳入本次用户端开发范围和验收范围。

表单复用现有公共校验、错误提示和提交中防重复规则。未提交的普通表单字段在同一设备、同一浏览器保存 30 天，再次打开时自动恢复；主动关闭流程不清除草稿，提交成功后立即清除。不支持跨浏览器或跨设备恢复。

照片不跨次恢复，用户再次打开表单时需要重新选择。已经临时上传但未提交的照片在 24 小时后自动清除。照片格式、单张大小、内容校验和安全扫描复用现有公共图片上传能力；C1 额外限制总数最多 10 张。

所有时间字段按洛杉矶时区 `America/Los_Angeles` 存储，接口传输时保留明确的时区偏移，避免夏令时切换产生歧义。页面时间展示、Contact Us 提交时间以及 Request ID 中的 `YYMMDD` 与 C2 保持一致，统一按美东时区 `America/New_York` 计算并自动适配夏令时。Preferred date 按用户选择的日期值保存，不进行跨时区换日。

## 八、验收标准

1. PC / Mobile 可从各自入口进入 Sell，页面和交互与 Figma 及逐页交互清单一致。
2. 首页各屏、Footer 新增入口、Accepted Brands、Condition Guidelines、Service Area 状态和预约四步流程均可按清单验收。
3. ZIP 覆盖结果正确触发方式默认选择和置灰规则。
4. 必填 / 选填、品牌联想、照片上限、协议链接和公共校验符合本 PRD。
5. 成功页 Request ID 和字段隐藏规则符合本 PRD。
6. Contact Us 按 Sell / Buy 正确分流邮箱和邮件标题。
7. PC 与 Mobile 的业务结果一致，入口、布局与交互形式分别符合 Figma 对应端设计。

## 附录：逐页交互清单 v0.1（完整内容）

# Looply C1 Sell 逐页交互清单

## 首页第一屏（PC）

> UI 基线：用户提供的 Figma 截图。本文只描述这一屏看到的内容、可点击元素及点击结果。

### 1. 页面内容

| 区域 | 展示内容 |
|---|---|
| 第一排 Header | LOOPLY Logo；搜索框（占位文案 `Vintage Jewelry`）；搜索图标；`SELL` 按钮 |
| 第二排导航 | Hand Bags、Shoes、Jewelry、Watches、Accessories、Electronics、Brands |
| 第二排右侧 | 地球 / 语言国家图标、Account、Favorites、Bag 图标 |
| Hero 标签 | `SELL WITH LOOPLY` |
| Hero 标题 | `Sell from Home. Get Paid on the Spot.` |
| Hero 说明 | `We authenticate your pieces, make you an offer, and pay you in one visit. Fast and simple, so you have time for everything else.` |
| Hero 服务提示 | `Free In-Home Appointments · Visit Us · Ship to Us` |
| Hero 按钮 | `Sell Now`：点击打开 Sell 预约流程第 1 步；`Explore your options`：点击滚动到首页 Three Ways to Sell 区域 |
| Why Looply | `Sell from Home`、`Immediate Payment`、`On-the-Spot Offer`、`Competitive Pricing`，每项包含对应说明文案 |

### 2. 本屏状态

- 搜索框默认显示占位文案 `Vintage Jewelry`，不视为已输入关键词。
- Hero 图片、标题、说明和两个按钮在默认状态同时展示。
- Header 与第二排导航固定为 PC 两排结构；窗口缩小时按 Figma 响应式规则处理。

### 3. 页面流转

`首页第一屏 → Sell Now → Sell 预约 Step 1`

`首页第一屏 → Explore your options → 首页 Three Ways to Sell`


## 首页第二屏：Three Ways to Sell（PC）

### 1. 页面内容

| 区域 | 展示内容 |
|---|---|
| 区块标题 | `THREE WAYS TO SELL`；`Choose how you’d like to sell.` |
| 主卡片 | `In-Home Appointment`；标签 `Chosen By 80% Of Sellers`；说明 `Sell your luxury pieces from the comfort of your home.`；链接 `Available across the Greater LA area.` |
| 主卡片流程 | `How It Works`；01 `Start Your Request`；02 `Confirm Your Appointment`；03 `Meet & Review at Home`；04 `Get Paid on the Spot`，每步配对应说明 |
| 右侧卡片一 | `Visit Looply`；`Meet Us At Our Office.`；默认收起卡片 |
| 右侧卡片二 | `Ship To Us`；`Complimentary Shipping Across The U.S.`；默认收起卡片 |

### 2. 点击交互

| 可点击元素 | 点击结果 |
|---|---|
| `Available across the Greater LA area.` | 进入 Service Area 页面，用 ZIP 查询上门服务覆盖 |
| `Visit Looply` 卡片 Hover | 卡片放大并切换为主卡片，展示 `Bring your luxury pieces to our office for an efficient, in-person review.`、Looply 地址、`How It Works` 四步：`Start Your Request`、`Confirm Your Visit`、`Visit & Get an Offer`、`Get Paid on the Spot`；另一张方式卡片缩小为侧卡 |
| `Ship To Us` 卡片 Hover | 卡片放大并切换为主卡片，展示 `Send eligible pieces from anywhere in the U.S. with complimentary shipping.`、`How It Works` 四步：`Submit Your Request`、`Receive Your Estimated Offer`、`Choose & Ship`、`Final Offer & Payment`；另一张方式卡片缩小为侧卡 |
| Hover 后主卡片中的流程步骤 | 流程说明文字，不单独设置点击行为 |
| 主卡片中的方式标题 / 说明 | 信息展示；不直接提交预约 |

### 3. 页面流转

`首页第二屏 → Available across the Greater LA area. → Service Area`

`首页第二屏 → Visit Looply 卡片 Hover → Visit Looply 详情态`

`首页第二屏 → Ship To Us 卡片 Hover → Ship To Us 详情态`

## 首页第三屏：What We Buy（PC）

| 区域 | 展示内容 | 点击结果 |
|---|---|---|
| 标题区 | `WHAT WE BUY`；`From icons to modern classics.`；`Explore accepted brands across handbags, jewelry and watches.` | 信息展示 |
| 品牌展示 | 固定展示并横向滚动精选品牌：Hermès、Chanel、Cartier、Louis Vuitton、Van Cleef & Arpels、Dior 等约 10 个品牌 | 信息展示，不读取后台配置 |
| 入口 | `View All Brands & Categories` | 进入 Accepted Brands 页面 |

## 首页第四屏：Selling Tips + How to Get Paid（PC）

| 区域 | 展示内容 | 点击结果 |
|---|---|---|
| Selling Tips 图片卡 | `SELLING TIPS`；`A little preparation makes selling easier.` | 信息展示，不单独跳转 |
| Tips 列表 | `01 Gather Original Accessories` — `Bring any original boxes, dust bags, straps, pouches, receipts, warranty cards or service records you still have.`；`02 Share the Condition` — `Tell us about visible wear, repairs, engraving, missing parts or modifications.`；`03 Check What We Buy` — `Review our accepted brands, categories and condition guidelines before you begin.` | 信息展示，不单独跳转 |
| How to Get Paid | `HOW TO GET PAID`；`Get paid without waiting for your item to sell.`；`Because Looply buys accepted pieces directly, payment can begin as soon as you accept the final offer and required checks are complete.` | 信息展示 |
| 付款步骤 | `Review Your Offer` — `Decide with no obligation to sell`；`Complete the Checks` — `Agreement, identity and ownership`；`Receive Your Payment` — `Payment details are confirmed with you directly` | 信息展示，不单独跳转 |

## 首页第五屏：FAQ（PC）

| 区域 | 展示内容 | 点击结果 |
|---|---|---|
| FAQ 标题 | `FAQ`；`More questions?`；按钮 `View All FAQs` | 点击 `View All FAQs` 进入 Seller FAQ 页面 |
| FAQ 问题列表 | `What pieces does Looply buy?`；`What conditions do you accept?`；`Is the In-Home Appointment complimentary?`；`How is my offer determined?`；`How does Looply review my item?`；`What happens if I do not accept the offer?`；`What if I live outside Los Angeles?` | 点击问题行展开 / 收起答案；同一时间按 UI 状态展示展开内容 |
| 已展开问题 | `What pieces does Looply buy?`；答案包含 `Looply currently considers select designer handbags, jewelry and watches.` 及 `Brands & Categories` 内链 | 点击 `Brands & Categories` 进入 Accepted Brands 页面 |

## 首页第六屏：底部 CTA（PC）

| 区域 | 展示内容 | 点击结果 |
|---|---|---|
| CTA 文案 | `A REFINED, PERSONAL WAY TO SELL LUXURY.`；`Ready when you are.`；`Share a few details, and a client representative will take it from there.` | 信息展示 |
| CTA 按钮 | `Sell Now` | 打开 Sell 预约流程第 1 步 |

## 首页吸底 CTA（PC）

| 页面位置 / 状态 | 展示内容 | 交互 |
|---|---|---|
| 首屏 | 不展示吸底 CTA | 页面按首屏原有 Hero 按钮展示 |
| 中间内容区 | 左侧 `Ready when you are.`；右侧 `SELL NOW` | 吸底固定；点击 `SELL NOW` 打开 Sell 预约流程第 1 步 |
| 最后一屏（FAQ / 底部 CTA / Footer） | 不展示吸底 CTA | 使用页面自身的底部 CTA `Sell Now` |

吸底 CTA 随页面滚动进入中间内容区后出现，离开中间内容区进入首屏或最后一屏时隐藏；打开预约流程后隐藏，关闭流程后按当前页面位置恢复。

## 首页 Footer 新增内容（PC）

以下仅记录截图红框标出的 C1 新增入口；Footer 其他既有内容沿用全站规则，不在本清单重复描述。

| 区域 | 新增内容 | 点击结果 |
|---|---|---|
| Sell 分组 | `Sell with Looply`、`Accepted Brands`、`Service Area` | 分别进入 Sell 首页、Accepted Brands、Service Area |
| Sell 分组 | `Condition Guidelines` | 进入 Condition Guidelines 页面 |
| Support 分组 | `Seller FAQ` | 进入 Seller FAQ 页面 |
| 法律链接 | `Seller Agreement` | 进入 Seller Agreement 页面 |

## Service Area 页面（PC）

### 1. 默认状态

| 区域 | 展示内容 | 点击结果 |
|---|---|---|
| 页面标题 | `SERVICE AREA`；`In-Home Service Across Greater Los Angeles` | 信息展示 |
| 页面说明 | `Complimentary In-Home Appointments are available across Greater Los Angeles, including parts of Orange County.` | 信息展示 |
| ZIP 查询区 | `Check your ZIP code`；`Check whether we offer In-Home Service in your area.`；输入框占位 `Enter ZIP code`；按钮 `Check Availability` | 输入 ZIP 并点击查询，进入查询结果状态 |
| 服务区域说明 | `Greater Los Angeles`：`Beverly Hills, Santa Monica, West Hollywood, Malibu, Culver City, Pasadena, Glendale, Burbank, Manhattan Beach, Long Beach, and surrounding communities.`；`Orange County`：`Irvine, Newport Beach, Laguna, Costa Mesa, Huntington Beach, Laguna Beach, Laguna Niguel, San Clemente and surrounding communities.` | 信息展示 |

### 2. 查询结果状态

| 状态 | 页面内容 | 可点击交互与结果 |
|---|---|---|
| 非法 ZIP | 沿用现有地址页 ZIP 校验的红色边框和错误提示 `Enter a valid ZIP code.` | 接受 5 位 ZIP 或 ZIP+4；修改 ZIP 或重新点击 `Check Availability` |
| 未覆盖 | `OTHER SELLING OPTIONS`；`In-Home Service isn’t available in your area yet.`；`You can still sell with Looply by visiting us or shipping your pieces.`；按钮 `Explore Other Ways to Sell` | 返回 Sell 首页的 `Three Ways to Sell` 区域 |
| 已覆盖 | `IN-HOME SERVICE AVAILABLE`；`Great news—we serve your area.`；`In-Home Service is available in your area. A client representative will confirm your address and appointment.`；按钮 `Request an In-Home Appointment` | 从预约 Step 1 开始；自动预填本次查询的 ZIP，并将 In-Home 记录为预选意向。用户完成 Step 1、Step 2 后进入 Step 3，仍可查看并切换其他可用方式 |

点击 `Check Availability` 后显示查询中状态。覆盖配置读取失败时展示 `Something went wrong. Please try again.` 和 `Retry` 按钮；点击 `Retry` 重新查询，失败时保留 ZIP 输入内容。

### 3. 页面流转

`Service Area 默认 → Check Availability → 非法 ZIP / 未覆盖 / 已覆盖`

`未覆盖 → Explore Other Ways to Sell → Sell 首页 Three Ways to Sell`

`已覆盖 → Request an In-Home Appointment → 预约 Step 1（预填 ZIP / 预选 In-Home 意向）`

## Sell 预约流程第二步：物品信息（PC）

| 区域 | 展示内容 / 交互 |
|---|---|
| 页面标题 | `Tell us about your pieces.` |
| 品类 | `What would you like to sell?`；动态展示运营后台全部 Active 品类并按后台顺序排列，支持多选且至少选择一项；`Handbags`、`Jewelry`、`Watches` 仅为当前配置示例 |
| 品牌 | `Which brands?`；提示 `Showing brands for your selected categories. Brand not listed? Enter it here.`；支持多选和自由输入 |
| 品牌联想 | 选择品类后，用户开始输入品牌时，按所选品类从后台生效品牌配置实时联想；未选择品类时不提供联想；后台未配置的品牌仍允许用户手动输入并提交 |
| 总件数 | `Approximately how many pieces in total?`；必填单选：`1–2`、`3–5`、`6–9`、`10+` |
| 用户补充说明 | `Anything else we should know? (Optional)`；占位 `Models, condition, repairs or other details`；选填，最多 300 个字符，显示当前字数 / 300 |
| 照片 | `Add photos (Optional)`；最多上传 10 张；已上传图片展示缩略图和删除按钮；说明 `Clear photos can help your luxury specialist prepare for the conversation.` |
| 操作按钮 | `Back` 返回第一步；`Continue` 进入第三步 |

### 校验与提示

- 品类、品牌和总件数为必填项；用户补充说明和照片为可选项。
- 未填写任一必填项点击 `Continue` 时，停留在当前页并显示 Toast：`Please complete all required fields to continue.`
- 用户补充说明达到 300 个字符后停止继续输入。
- 照片超过 10 张时，阻止继续添加并提示：`You can upload up to 10 photos.`
- 品牌联想结果仅提供选择建议，不限制自由输入品牌。

## Sell 预约流程第三步：选择售卖方式（PC）

| 区域 | 展示内容 / 交互 |
|---|---|
| 页面标题 | `Find the Best Way to Sell` |
| 页面说明 | `Enter your ZIP code and we’ll recommend the selling options available in your area.` |
| ZIP 字段 | `Enter your ZIP code *`；输入框预填或展示用户已填写的 ZIP（示例 `90048`） |
| 操作按钮 | `Back` 返回第二步并保留物品信息；`Continue` 校验 ZIP 后查询服务覆盖并进入对应售卖方式结果 |

### 交互规则

- 用户点击 `Continue` 后，系统复用地址页 ZIP 校验，并根据 ZIP 覆盖配置计算可用售卖方式；ZIP+4 取前 5 位查询覆盖。
- 查询结果用于推荐售卖方式：覆盖区域优先推荐 `In-Home Appointment`；未覆盖区域推荐 `Visit Looply` 或 `Ship To Us`。
- ZIP 支持上门时：`In-Home Appointment` 默认勾选并高亮，`Visit Looply` 与 `Ship To Us` 保持可选。
- ZIP 不支持上门时：`Ship To Us` 默认勾选并高亮，`In-Home Appointment` 置灰且不可选；`Visit Looply` 保持可选。
- 上门支持的 ZIP 列表由运营后台配置并维护；前台查询只使用当前生效的 ZIP 配置。
- 用户可在可选方式之间切换；置灰方式不响应点击。
- ZIP 非法时停留当前页，沿用地址页错误提示并保留输入；查询失败时显示可重试提示。

## Sell 预约流程第一步：个人信息（PC）

| 区域 | 展示内容 / 交互 |
|---|---|
| 顶部操作 | 返回按钮；关闭按钮；四段式进度条，当前第一段高亮 |
| 页面标题 | `Let’s start with you.` |
| 表单字段 | `First name *`、`Last name *`、`Phone *`（国家码 `+1`）、`Email *` |
| 联系授权 | 必须勾选；展示经法务确认的联系授权文案，并提供 `Privacy Policy` 与 `Terms of Service` 链接 |
| 法律入口 | `Privacy Policy`：复用 C2 的 Privacy Policy；`Terms of Service`：复用 C2 的 Terms of Service。两者均为可点击文本链接。 |
| 主按钮 | `Continue`；信息填写完成且勾选授权后进入下一步；未勾选时停留当前页并展示字段错误 |

点击 `Continue` 时沿用现有公共表单校验；校验通过进入预约流程第二步，校验失败在当前字段展示错误并保留已填内容。返回按钮回到进入预约前的页面，关闭按钮按草稿保存规则处理。

## Accepted Brands 页面（PC）

### 1. 页面内容

| 区域 | 展示内容 |
|---|---|
| 页面标题 | `Brands & Categories`；`Accepted Brands` |
| 搜索框 | 占位文案 `Search a designer`；搜索图标；输入第一个字符即开始实时过滤 |
| 左侧筛选 | `Browse by Category`；`All` 以及运营后台全部 Active 品类（可显示对应品牌数量）；选择 `All` 展示全部 Active 品牌；`Handbags`、`Jewelry`、`Watches` 仅为当前配置示例 |
| 品牌列表 | 按首字母分组展示品牌名称，如 A、B、C、D、F、G、H、J、L、M、P、S、T、V |

### 2. 点击与输入交互

| 元素 / 操作 | 结果 |
|---|---|
| 搜索框输入第一个字符 | 立即开始过滤，不需要点击搜索按钮；列表实时更新为名称包含该输入内容的品牌，并保留首字母分组 |
| 继续输入字符 | 按完整关键词继续缩小结果；无匹配时显示无结果提示 |
| 清空搜索框 | 恢复当前品类下的完整品牌列表 |
| 任一 Active 品类 | 切换品类，列表刷新为该品类下的 Active 品牌；搜索关键词继续保留并参与过滤 |
| 品牌名称 | 当前页面展示品牌信息，不跳转 |
| Header `SELL` | 进入 C1 Sell 首页 |
| Footer `Sell with Looply` | 进入 C1 Sell 首页 |

### 3. 数据规则

- 品类和品牌列表读取运营后台中状态为“生效”的配置。
- Sell 首页 What We Buy 横向滚动的精选品牌为固定展示内容，不读取后台配置；本页完整品牌列表仍以后台 Active 配置为准。
- 首页不展示的品牌仍可在完整 Accepted Brands 页面展示。
- 品牌按后台配置的标准名称和首字母分组；停用品牌不出现在新列表中。

### 4. 页面状态

| 状态 | 展示与操作 |
|---|---|
| Loading | 品类与品牌区域展示加载状态，搜索和品类切换暂不可用 |
| 配置加载失败 | 展示 `Something went wrong. Please try again.` 和 `Retry`；点击后重新加载 |
| 当前品类无品牌 | 展示 `No accepted brands are currently available in this category.`，用户可切换其他品类 |
| 搜索无匹配 | 展示 `No brands found.` 和 `Clear search`；点击后清空关键词并恢复当前品类品牌列表 |

## Condition Guidelines 页面（PC）

页面标题：`Condition Guidelines`。页面按以下 9 个模块展示示例图片；前 8 个模块分别列出 Accepted 与 Not Accepted 标准，第 9 个 `Jewelry and Watches` 按 UI 合并说明展示：

| 模块 | Accepted | Not Accepted |
|---|---|---|
| 1. Brand and Authentication Details | 品牌标记、序列号、产地标识及其他识别细节清晰可读 | 关键识别细节缺失、无法读取或无法验证 |
| 2. Exterior and Corners | 轻微划痕、磨损或边角使用痕迹 | 孔洞、深度划痕、大面积剥落或缺失图案 |
| 3. Stains and Discoloration | 轻微、局部污渍或细微颜色变化 | 大面积或明显污渍、颜色转移、水渍、严重褪色、霉变或腐蚀 |
| 4. Overall Shape | 轻微塌陷或变形但整体形状仍保持 | 无法恢复的严重塌陷、变形或失去形状 |
| 5. Interior and Lining | 轻微使用痕迹、小污点或轻微划痕 | 严重污渍、粘性、起皮、剥落、粉化或霉变 |
| 6. Handles and Straps | 轻微磨损或开裂，但提手 / 肩带仍可使用 | 断裂、严重开裂或无法使用 |
| 7. Hardware, Closures, and Accessories | 轻微划痕或褪色；缺少不影响正常使用的配件可接受 | 拉链、扣件损坏或缺少导致无法正常使用的部件 |
| 8. Repairs and Replacement Parts | 特定奢侈品可酌情接受轻微专业维修 | 重大改装、非原厂配件或更换主体结构 / 主要部件 |
| 9. Jewelry and Watches | 珠宝轻微裂纹或缺石、手表轻微问题可由专业人员评估 | 珠宝无法正常使用；手表涉及水晶、表盘、表冠、表带或内部机芯的严重问题 |

页面无独立提交操作；用户可通过 Footer 的 `Sell with Looply` 返回 Sell 首页，或通过品牌 / FAQ 内链继续浏览。

## 首页首屏展示与点击边界

首屏继续展示 Header、Hero 和 Why Looply 内容。首屏仅设置两个可点击 CTA：Hero `Sell Now` 打开预约流程第 1 步，`Explore your options` 滚动到首页 Three Ways to Sell 区域。Why Looply 的标题与说明为展示信息，不设置独立点击行为。

## Seller FAQ 页面（PC / Mobile）

页面标题为 `Seller FAQ`，展示与首页 FAQ 相同的 7 个问题：`What pieces does Looply buy?`、`What conditions do you accept?`、`Is the In-Home Appointment complimentary?`、`How is my offer determined?`、`How does Looply review my item?`、`What happens if I do not accept the offer?`、`What if I live outside Los Angeles?`。用户点击问题行展开 / 收起对应答案；答案内容以[业务 FAQ 文档](https://zhuanspirit.feishu.cn/docx/FhCvdYCxgoFRtCxekE6cdRFdnfg)为准。`Brands & Categories` 为可点击内链，进入 Accepted Brands；Sell 首页入口 `View All FAQs` 进入本页。PC 与 Mobile 使用同一问题和答案，布局按 Figma 对应稿适配。

## Policies 页面（PC / Mobile）

在现有 Policies 页面新增入口：标题 `Seller Agreement`，说明 `Terms and responsibilities for selling your pieces to Looply`。点击后进入当前语言对应的 Seller Agreement 页面。

## Seller Agreement 文档引用

Seller Agreement 的业务正文和条款口径以[业务提供的 Seller Agreement 文档](https://zhuanspirit.feishu.cn/docx/X2vjdYalQopAskxavSTcB4pAnR2?from=from_copylink)为准。PRD 仅定义页面入口、展示和跳转，不复制条款全文。

## Sell 预约流程第四步：In-Home Appointment（PC）

| 字段 / 区域 | 展示内容 | 必填 | 交互 / 规则 |
|---|---|---:|---|
| 页面标题 | `In-Home Appointment`；`We come to your home at no cost.` | — | 信息展示 |
| Street address | `Street address *` | 是 | 输入上门地址 |
| Apartment | `Apartment, suite, etc. (Optional)` | 否 | 输入公寓 / 套房等补充地址 |
| City | `City *` | 是 | 输入城市 |
| State | `State *` | 是 | 选择州；用于 Request ID 的 LOCATION |
| ZIP code | `ZIP code *` | 是 | 沿用地址页 ZIP 校验，并与第三步查询结果保持一致 |
| Preferred date | `Preferred date (Optional)` | 否 | 日期选择器；提交后由代表确认可用性 |
| Referral code | `Apply referral code (Optional)` | 否 | 输入推荐码 |
| 提示文案 | `A client representative will contact you to confirm appointment availability. By submitting this request, you agree to our Seller Agreement.` | — | `Seller Agreement` 为可点击链接，进入 Seller Agreement 页面；保持当前 UI，不增加勾选框；点击 `Submit Request` 即表示同意，并记录协议版本和提交时间 |
| 操作按钮 | `Back`、`Submit Request` | — | Back 返回第三步；Submit Request 校验必填项并提交预约 |

点击 `Submit Request` 时，Street address、City、State、ZIP code 任一为空则阻止提交并显示公共表单错误提示；校验通过后创建预约并进入 Request received 成功页。

## Sell 预约流程第四步：Visit Looply（PC）

| 字段 / 区域 | 展示内容 | 必填 | 交互 / 规则 |
|---|---|---:|---|
| 页面标题 | `Book an Office Appointment` | — | 信息展示 |
| 页面说明 | `Choose a preferred date, or leave it open for a client representative to contact you.` | — | 信息展示 |
| 门店地址 | `Looply address`；`6300 Wilshire Blvd, Los Angeles, CA 90048 Appointment only.` | — | 固定展示，不可编辑 |
| Preferred date | `Preferred date (Optional)` | 否 | 日期选择器；不选择时由客户代表联系确认 |
| Referral code | `Apply referral code (Optional)` | 否 | 输入推荐码 |
| 提示文案 | `A client representative will contact you to confirm appointment availability.` | — | 信息展示 |
| 操作按钮 | `Back`、`Submit Request` | — | Back 返回第三步；Submit Request 提交到店预约 |

提交时仅校验公共表单规则；Preferred date 和 Referral code 为空也可以提交。提交成功后创建预约并进入 Request received 成功页。

## Sell 预约流程第四步：Ship To Us（PC）

| 字段 / 区域 | 展示内容 | 必填 | 交互 / 规则 |
|---|---|---:|---|
| 页面标题 | `Submit a Shipping Request` | — | 信息展示 |
| 页面说明 | `Tell us where we’ll be receiving your shipment, and we’ll send the applicable shipping instructions.` | — | 信息展示 |
| Street address | `Street address *` | 是 | 输入收货地址 |
| Apartment | `Apartment, suite, etc. (Optional)` | 否 | 输入公寓 / 套房等补充地址 |
| City | `City *` | 是 | 输入城市 |
| State | `State *` | 是 | 从州下拉列表选择 |
| ZIP code | `ZIP code *` | 是 | 沿用地址页 ZIP 校验 |
| 协议勾选 | `By submitting this shipping request, I agree to the Looply Seller Agreement, confirm that my items ...` | 是 | 必须勾选；`Seller Agreement` 为可点击链接 |
| 提交说明 | 提交后的联系说明按 UI 展示；成功页不展示确认邮件发送状态 | — | 信息展示 |
| 操作按钮 | `Back`、`Submit Request` | — | Back 返回第三步；Submit Request 校验并提交邮寄请求 |

Street address、City、State、ZIP code 和协议勾选缺失时阻止提交并显示公共表单错误提示；提交成功后创建预约并进入 Request received 成功页。

## 提交成功反馈页：Request received（PC）

| 区域 | 展示内容 / 规则 |
|---|---|
| 成功提示 | `Request received`；`Thank you. We’ll be in touch.`；客户代表将在 24 小时内通过电话、短信或邮件联系 |
| Request ID | 按 `[METHOD]-[YYMMDD]-[LOCATION]-[RANDOM]` 生成并展示。`METHOD`：`IH` / `VL` / `ST`；`YYMMDD` 为正式提交日期；`LOCATION` 为履约州缩写（Visit Looply 固定 `LA`，In-Home / Ship To Us 使用客户地址州缩写）；`RANDOM` 为后台生成的 6 位大写字母和数字组合，生成后校验唯一性 |
| Selling method | 展示用户最终选择的售卖方式：`In-Home Appointment`、`Visit Looply` 或 `Ship To Us` |
| Total pieces | 展示用户在物品信息步骤选择的数量 |
| Preferred date | 展示用户填写的日期；未填写时隐藏整行，不展示空值 |
| 关闭 / 返回 | 成功页为终态，不提供返回上一步；仅提供关闭或返回 Sell 首页，且不得再次提交同一申请 |

## Contact Us 页面（PC）

| 字段 / 区域 | 展示内容 | 必填 | 交互 / 规则 |
|---|---|---:|---|
| 页面标题 | `Contact us`；`If you have any questions about your order, returns, products, or our services, please contact us using the information below.` | — | 信息展示 |
| Business Type | `Business Type`；占位 `Select a business type`；选项 `Sell`、`Buy` | 是 | 必须选择业务类型 |
| Full Name | `Full Name`；占位 `Enter your name` | 是 | 输入姓名 |
| Email | `Email`；占位 `Enter your email` | 是 | 复用公共邮箱格式校验 |
| Message | `Message`；占位 `Enter your message` | 是 | 输入咨询内容 |
| 提交按钮 | `Send` | — | 校验通过后提交到对应邮箱 |
| 提交说明 | `We generally respond to customer inquiries within 1-2 business days.` | — | 信息展示 |

### 邮件分流规则

| Business Type | 收件邮箱 | 邮件标题 |
|---|---|---|
| `Sell` | `sell@looply.com` | `Looply Contact Us - {submission time} - {Full Name}` |
| `Buy` | `service@looply.com` | `Looply Contact Us - {submission time} - {Full Name}` |

邮件正文包含用户填写的 Business Type、Full Name、Email 和 Message。提交成功显示成功提示；提交失败保留输入并允许重试。
