# Looply GA4数据分析 PRD

> 文档版本：v1.9  
> 状态：GA4剩余问题统一收口开发基线  
> 日期：2026-08-31  
> 适用范围：Looply已启用市场的网站行为和电商分析；一期覆盖美国与香港  
> 基线原则：本文件可独立于广告系统开发和上线。旧三渠道广告PRD中的GA4内容已迁移至本文件；冲突时以本文件为准。

## 一、概述

### 1.1 背景与目标

GA4用于分析Looply网站访问、商品浏览、搜索、收藏、加购、结算、购买和退款，不是Google Ads投放的必需组件。本PRD把GA4从广告投放系统中拆出，使网站分析能够独立排期、授权、测试和上线，也避免开发误把GA4 Purchase再次导入Google Ads并形成第二个主要购买转化。

一期建立一个统一业务事件入口、一条`dataLayer → Google Tag Manager → GA4`浏览器链路和一条Purchase/Refund服务端权威链路。GA4不负责广告点击触点、用户来源归因、广告花费或ROAS。

### 1.2 一期目标

1. 创建并配置独立GA4 Property与Web Data Stream，接入美国和香港已启用市场的网站。
2. 通过统一`trackEvent`产生15类浏览器业务/电商事件，经dataLayer与GTM发送至GA4；当前暂不产生Looply主动`page_view`，Purchase与Refund由服务端发送。
3. 正确定义首次页面、SPA路由、硬刷新、组件重渲染和业务操作的排重边界。
4. 支付最终成功后由唯一服务端发送者通过Measurement Protocol发送GA4 Purchase；浏览器成功页不发送、不claim、不补发Purchase。
5. 退款成功只由服务端发送GA4 Refund，并以refund_id主动幂等。
6. 使用区域投递门控、Outbox、服务端幂等、重试、验证端点、告警和对账保证数据质量；一期不接入CMP、不读取同意状态。

### 1.3 成功指标

| 指标 | 目标 | 统计口径 |
|---|---:|---|
| 事件Schema通过率 | ≥99.9% | 进入GA4消费者前通过本地契约校验的事件比例 |
| 同页面生命周期重复浏览事件 | 0 | 组件重复渲染、重复监听、重复接口回调造成的重复 |
| 重复Purchase | 0 | 同一order_id不得形成不同transaction_id或两个主动发送成功记录 |
| Purchase最终覆盖率 | ≥99.9% | 区域投递门控允许的已支付订单具有唯一服务端Purchase任务且最终accepted或明确permanent_failed |
| Refund最终处理率 | ≥99.9% | 区域投递门控允许的成功退款最终accepted或明确permanent_failed |
| PII泄漏 | 0 | DataLayer、日志、死信和告警不含邮箱、电话、姓名、地址或密钥 |
| 事件可追溯性 | 100% | Purchase/Refund可定位业务事实、发送路径、状态和错误 |

### 1.4 用户角色

| 角色 | 职责 | 一期入口 |
|---|---|---|
| 数据分析 | 配置报表、验证事件、分析漏斗 | GA4界面、BigQuery或内部查询 |
| 产品/运营 | 查看行为和电商指标 | GA4报表和探索 |
| Web开发 | 接入trackEvent、页面和浏览器业务触发点，维护dataLayer适配器；在checkout前提交GA4关联上下文 | Web代码 |
| 数据/标签运营 | 配置、审核和发布GA4相关GTM标签 | GTM、GA4界面 |
| 后端/支付开发 | 生成Purchase/Refund权威事实、冻结上下文并由唯一服务端发送者投递 | 订单、支付、异步Worker |
| 合规/运维 | 配置地区策略、权限、密钥和告警 | 受控配置、Secret Manager、监控平台 |

### 1.5 一期范围

- GA4账号、Property、Web Data Stream、Measurement ID、GTM容器和Measurement Protocol API Secret。
- Looply主动`page_view`及17类业务事件；当前GA自动`page_view`按3.4保留并区分来源。
- 统一事件Schema、按市场配置的页面语言、商品层级和金额合同。
- 区域投递门控：EEA、英国、瑞士不加载GA4、不发送事件；地区策略可配置且业务代码不写死US/HK允许名单。
- 服务端Measurement Protocol Purchase与Refund；浏览器不发送Purchase/Refund。
- 浏览器行为事件幂等、服务端电商事实幂等、Outbox、状态、错误、告警和验证。

### 1.6 明确不做

- 不定义Google Merchant Center、Google Ads Tag、AW再营销、Google Ads Conversion、Data Manager或转化调整。
- 不定义Meta或TikTok任何能力。
- 不采集或存储进站触点，不判断Direct，不做30分钟去重、身份缝合、Last-touch、时间衰减归因、广告花费或ROAS。
- 不把GA4 Purchase导入Google Ads并设为第二个主要购买转化；未来若需要GA4受众或转化导入，必须另行评审。
- 不做GA4受众后台、复杂受众编排、预测受众、自动预算或广告激活。
- 不向DataLayer写原始PII，不采集用户出生日期或性别用于分析或广告。
- 不允许业务组件直接调用`gtag`、直接写Measurement ID或绕过统一`trackEvent`；GTM只按已发布的路由矩阵消费dataLayer事件。
- 一期不接CMP，不读取、保存或判断用户Consent/GPC状态，也不提供同意弹窗；CMP、Consent Mode、用户撤回与同意快照在后续版本单独评审接入。

### 1.7 唯一决策

| 主题 | 一期决策 |
|---|---|
| GA4定位 | 独立网站分析能力，不是Google Ads上线前置条件 |
| 事件入口 | 业务页面统一调用trackEvent，不直接散落gtag或dataLayer调用 |
| 浏览器路由 | trackEvent → GA4适配器主动幂等 → dataLayer Custom Event → GTM GA4 Event Tag |
| 页面事件 | 当前保留GA自动page_view；Looply主动page_view暂停；页面实例上下文仍供其他事件关联；硬刷新视为新页面生命周期 |
| 普通事件排重 | GA4不提供通用event_id自动排重，Looply按事件语义主动幂等 |
| Purchase事实 | 支付验签回调第一次将订单推进paid |
| Purchase路由 | 唯一服务端发送者通过Measurement Protocol投递；浏览器不发送、不claim、不补发 |
| Refund | 支付渠道确认成功后服务端发送，refund_id主动幂等 |
| 区域投递门控 | 一期不接CMP、不读取同意状态；可信地区策略禁止时不push GA4事件、不触发GA4标签且零分析请求。EEA、英国、瑞士必须禁止；地区代码和允许名单不得写死在业务代码 |
| 广告激活 | 一期不关联Google Ads，不导入GA4转化或受众 |
| 市场语言 | 页面语言和站点URL由当前Market启用语言配置提供；GA4不预设美国或香港语言集合 |
| 事件币种 | `currency`取商品、购物车、订单或退款业务事实的`currency_code`；Market国家管理法定货币仅作校验基准 |

### 1.8 术语

| 术语 | 定义 |
|---|---|
| GA4 Property | Looply网站分析数据的GA4属性 |
| Web Data Stream | 网站数据流，提供`G-`Measurement ID |
| Google Tag Manager | 浏览器标签路由和环境发布容器；一期使用环境对应的`GTM-`容器 |
| Custom Event | Looply写入dataLayer的自定义事件，由GTM触发器匹配 |
| GA4 Event Tag | GTM中把规范事件参数发送到GA4 Web Data Stream的标签 |
| Measurement Protocol | GA4服务端事件接口；一期用于权威Purchase和Refund |
| page_instance_id | Looply浏览器内一次完整页面生命周期ID，用于页面实例关联和去重；由Web公共页面上下文统一生成，并随适用的GA4事件发送 |
| transaction_id | GA4 Purchase/Refund关联订单的交易ID，固定等于order_id |
| Market国家管理 | 提供市场国家、法定货币、已启用语言及站点URL规则的外部配置；GA4只读消费 |

## 二、GA4资产与全局约束

### 2.1 资产配置

| 配置 | 规则 |
|---|---|
| GA4 Account/Property | staging与production独立 |
| Web Data Stream | 每环境独立，域名与环境一致 |
| Measurement ID | 环境配置，格式`G-...`，不写死在业务组件 |
| GTM Container | 与Google Ads共用同一环境级容器，避免同页加载两个GTM容器；staging与production使用独立环境配置和发布版本，容器ID格式`GTM-...` |
| GTM GA4资产 | Google Tag、15个浏览器业务事件Custom Event触发器、GA4 Event Tag及Data Layer Variables；Purchase/Refund不经过GTM |
| API Secret | Secret Manager保存，仅服务端可读 |
| Debug/Validation | staging启用debug和validation；production禁止长期debug_mode |
| BigQuery Link | 可选分析资产，不影响一期事件发送 |

GA4 Custom definitions只注册确有报表用途且值域受控的参数。本批五个事件新增参数的分析用途按3.5.6执行；`order_id`、`refund_id`等其他高基数字段不注册为自定义维度，避免高基数报告聚合。

GTM内的GA4资产固定配置如下：

| GTM资产 | 触发器/配置 | 用途 |
|---|---|---|
| Google Tag | 区域策略允许后的GA4消费者初始化 | 使用环境Measurement ID；保留当前GA自动page_view；禁止地区不加载共享容器 |
| Custom Event触发器 | `looply_ga4_page_view`及3.3中的15类浏览器业务事件 | 只匹配GA4命名空间，不匹配`looply_ads_*` |
| Data Layer Variables | `ga4_event_name`、页面参数、电商参数、业务参数 | 从规范dataLayer对象读取值，不在GTM猜测或补造业务字段 |
| GA4 Event Tag | 上述16个Custom Event触发器 | 事件名读取`ga4_event_name`，参数按3.2、3.3映射到同一Web Data Stream |

增强型衡量保持开启，但关闭其中的“网站搜索”。Looply主动发送`view_search_results`，不得再由增强型衡量根据URL参数自动生成第二条同义事件。

`page_view_source`和`view_search_results_source`注册为事件范围自定义维度，分别用于识别Looply主动页面事件和主动搜索结果事件。自定义维度只对注册后新处理的数据生效，不回填历史；历史空值不得反推事件来源。

GA4与Google Ads可以共享一个GTM容器，但标签、触发器和目标ID必须分开；两者都由共享的区域策略决定是否加载。禁止使用同一个Purchase标签同时向`G-`和`AW-`目标发送，也禁止把GA4 Purchase导入为另一项Google Ads主要转化。

### 2.2 ID、语言与时间

1. 所有商品事件的`items[].item_id`固定取`listing_public_code`，来源为`listings.public_code`，永久唯一且不可复用；不得使用内部`listing_id`、实物商品编码、SKU或SEO slug。
2. `order_id`是Purchase与Refund的`transaction_id`。
3. `refund_id`标识一次成功退款，仅作为Looply主动幂等和可选自定义诊断参数；GA4订单关联仍用transaction_id。
4. 页面语言、语言区域和页面URL均取当前Market已启用语言配置；事件使用当前页面的真实语言，禁止以任一语言兜底另一语言。
5. 业务事实时间存UTC；Measurement Protocol使用事实发生时间，不使用Worker发送时间。

### 2.3 金额口径

| 字段 | 规则 |
|---|---|
| currency | 取商品、购物车、订单或退款业务事实的`currency_code`；Market国家管理的法定货币仅作校验基准。若不一致，GA4仍发送业务事实币种，不得静默替换；同时记录数据质量诊断并告警，由上游修复市场或价格配置。 |
| ecommerce value | 商品行折后单价×数量之和，不含tax和shipping |
| tax | 订单代收税，单独发送 |
| shipping | 买家实际支付运费，单独发送 |
| item price | 商品行折后单价 |
| discount | 行级或订单优惠分摊到商品行的金额 |
| Refund value | 本次退款涉及的商品金额，不含未退款税费和运费；明细按真实退款项发送 |

金额使用十进制定点数和十进制JSON数字，禁止浮点累计误差。Purchase与Refund的value必须等于items的GA4口径汇总。浏览事件、加购、结账、Purchase、Refund和服务端补传均以上述业务事实币种发送；仅在币种缺失或金额格式非法、无法形成有效金额事件时，服务端投递进入失败处理。

### 2.4 区域投递门控

一期不接入CMP，不读取、保存或判断用户Consent/GPC状态。每次页面初始化和支付/退款事实创建时，系统从可信服务端下发或冻结的地区策略读取`google_measurement_allowed`；不得以浏览器自报地区或业务代码内的国家常量判断。EEA、英国、瑞士在该策略中必须为`false`：浏览器不初始化`window.dataLayer`、不加载GTM或GA4标签、不push `looply_ga4_*`事件且零GA4请求；服务端Purchase/Refund任务标记`suppressed_by_region`且零Measurement Protocol请求。策略允许时，浏览器只初始化一次并发送新产生事件；服务端直接按原可靠投递规则发送。

地区策略必须可配置、版本化和审计，新增市场或法律要求变化仅修改受控配置，不改业务代码。后续CMP版本再增加Consent Mode、用户撤回、GPC和同意快照；不得把一期直接发送解释为用户已授予同意。GA4广告个性化、Google Signals、Google Ads受众共享和`ad_user_data/ad_personalization`不在一期范围，默认不启用。

## 三、统一事件模型

### 3.1 trackEvent契约

```ts
type TrackOptions = {
  eventId?: string;
  occurredAt?: string;
  dedupeScope?: "page" | "session" | "business";
  consumerRoutes?: { ga4: boolean };
  reportToken?: string;
};

type TrackResult =
  | { ok: true; eventId: string }
  | { ok: false; code: "REGION_RESTRICTED" | "INVALID_EVENT" | "INVALID_PAYLOAD" | "DUPLICATE"; message: string };

function trackEvent(
  eventName: string,
  payload: Record<string, unknown>,
  options?: TrackOptions
): TrackResult;
```

业务调用方提供事件名和业务payload。SDK负责事件名和事件本体校验、当前消费者路由、地区策略判断和本地幂等，不抛出影响业务主流程的未捕获异常。区域策略禁止时返回`REGION_RESTRICTED`且不初始化或push；事件名非法、事件重复或无法形成事件本体时不push。本批五个事件的业务参数缺失不属于`INVALID_PAYLOAD`：业务事实成立时事件继续发送，可取参数正常携带，不可取参数省略且不伪造默认值。策略允许时，GA4适配器把浏览器事件规范化为`looply_ga4_*` Custom Event，再执行一次`window.dataLayer.push`。业务组件不得直接调用`gtag`或直接push渠道事件。GTM容器不得自行生成第二套业务事件，也不承担业务幂等。Purchase与Refund均不由浏览器`trackEvent`发送。

### 3.2 公共电商结构

```json
{
  "event": "looply_ga4_view_item",
  "ga4_event_name": "view_item",
  "event_id": "PAGE_INSTANCE_1:CPE2E00000015",
  "event_time": "2026-07-24T12:00:00.000Z",
  "page": {
    "location": "https://looply.com/{market-locale}/products/listing-456",
    "language": "{PAGE_LANGUAGE}",
    "title": "Product title"
  },
  "ecommerce": {
    "currency": "{BUSINESS_CURRENCY}",
    "value": 1000.00,
    "items": [{
      "item_id": "CPE2E00000015",
      "item_name": "Pre-owned item title",
      "item_brand": "Brand",
      "item_category": "Handbags",
      "item_category2": "Shoulder Bags",
      "item_category3": "Designer Bags",
      "item_category4": "Pre-owned",
      "item_category5": "Authenticated",
      "item_variant": "Black / Leather / Gold-tone",
      "condition_grade": "A",
      "discount": 50.00,
      "coupon": "WELCOME",
      "index": 1,
      "price": 1000.00,
      "quantity": 1
    }]
  }
}
```

DataLayer不包含邮箱、电话、姓名、地址、支付卡、IP或广告点击ID。`item_variant`复用商品属性规范结果，顺序为Color / Material / Hardware，缺失片段跳过。一物一码商品quantity固定为1。

`event_id`是Looply SDK排重和日志关联字段，GA4适配器不得默认把它注册或发送为自定义维度。各业务操作ID同样优先用于Looply本地幂等；只有另行定义分析用途、值域和保留策略后才可成为GA4参数。

### 3.3 事件矩阵

`page_view`是基础系统事件；浏览器事件的dataLayer Custom Event固定为`looply_ga4_`加GA4事件名。下表为17类业务事件，其中15类由浏览器触发，`purchase`与`refund`仅由服务端触发：

| Looply事件 | dataLayer Custom Event | GA4事件 | 权威触发时机 | 应传业务信息 |
|---|---|---|---|---|
| lead | looply_ga4_generate_lead | generate_lead | 联系线索接口成功 | lead_id、lead_type |
| sign_up | looply_ga4_sign_up | sign_up | 注册事务成功一次 | registration_id、method |
| login | looply_ga4_login | login | 用户真实登录成功 | login_id、method |
| view_item_list | looply_ga4_view_item_list | view_item_list | 新列表结果请求成功并形成初始展示 | page_instance_id、list_instance_id、placement_id、item_list_id/name、商品真实位置、items；搜索结果页增加搜索上下文 |
| select_item | looply_ga4_select_item | select_item | 用户从列表主动点击商品 | page_instance_id、selection_id、placement_id、item_list_id/name、商品真实位置、items |
| search | looply_ga4_search | search | 用户通过六种正式入口提交搜索 | search_term、trigger_type；联想场景按条件增加建议位置与稳定对象ID |
| view_search_results | looply_ga4_view_search_results | view_search_results | 搜索结果请求形成唯一终态 | page_instance_id、search_term、result_status、duration_ms、view_search_results_source；站内提交且URL存在时增加trigger_type；成功时增加result_count，失败时增加failure_type |
| view_item | looply_ga4_view_item | view_item | 商详核心内容可见 | page_instance_id、currency、value、单个item |
| add_to_wishlist | looply_ga4_add_to_wishlist | add_to_wishlist | 首次收藏事务成功 | wishlist_operation_id、currency、value、items |
| add_to_cart | looply_ga4_add_to_cart | add_to_cart | 加购事务成功 | cart_operation_id、currency、value、items |
| view_cart | looply_ga4_view_cart | view_cart | Shopping Bag或PC Cart Drawer中的非空可购商品成功展示 | page_instance_id、currency、value、items |
| remove_from_cart | looply_ga4_remove_from_cart | remove_from_cart | 当前一物一码商品成功从购物车删除 | currency、value、实际减少数量为1的items |
| begin_checkout | looply_ga4_begin_checkout | begin_checkout | checkout session创建成功 | checkout_id、currency、value、items |
| add_shipping_info | looply_ga4_add_shipping_info | add_shipping_info | 同一checkout首次形成有效配送方式，或之后有效shipping_tier发生变化 | checkout_id、step_version、shipping_tier、金额、items |
| add_payment_info | looply_ga4_add_payment_info | add_payment_info | 支付方式token化保存成功 | checkout_id、step_version、payment_type、金额、items |
| purchase | — | purchase | 订单／支付服务端首次确认order_id进入最终paid；仅服务端 | order_id、value、tax、shipping、currency、items |
| refund | — | refund | 支付渠道确认退款成功；仅服务端 | refund_id、order_id、value、currency、退款items |

次要事件只用于行为和漏斗分析，不在本PRD中定义任何广告优化目标。

### 3.4 page_view与SPA

1. 首次文档加载且页面主路由确认后发送一次Looply主动`page_view`；骨架屏和预取不发送。
2. SPA路由变化、页面标题和规范URL更新、核心页面数据就绪后发送一次新的Looply主动`page_view`。
3. 搜索结果页正式提交新的搜索词并形成新的页面上下文时，生成新的`page_instance_id`并发送一次新的Looply主动`page_view`；同页Apply筛选、Apply排序或Reset沿用当前页面实例，不重复发送。
4. 浏览器硬刷新创建新的`page_instance_id`，发送一次新的Looply主动`page_view`。
5. React组件重复渲染、StrictMode重复挂载、监听器重复注册和接口重复回调不得重复发送。
6. 当前保留GA自动`page_view`。它不能替代Looply主动事件，也不计入“每个页面实例恰好一条主动事件”的次数判断。

`looply_ga4_page_view`是Looply主动事件的唯一入口，必须从Web公共页面上下文读取并携带当前`page_instance_id`和固定参数`page_view_source=looply_custom`。同一页面实例内的`view_search_results`、`view_item_list`、`select_item`、`view_item`和`view_cart`使用同一值；页面刷新或重新进入后使用新值。GA自动`page_view`不携带`page_view_source`，其他事件也不得携带该参数。

适用事件的`page_location`等于事件发生时地址栏中的当前完整URL，包含已经生效的搜索词、筛选和排序参数。`page_referrer`只表示当前页面实例建立前的真实上一页面URL；筛选、排序、组件展开和同页接口刷新不建立新页面实例，也不更新`page_referrer`。从筛选后的列表点击商品时，`select_item.page_location`是筛选后的列表URL；进入PDP后，新页面实例事件的`page_referrer`才是该筛选URL。直达页面允许`page_referrer`为空，不复用前两跳或更早的过期路由，也不猜测来源。

### 3.5 五个变更事件规则

#### 3.5.1 搜索提交与结果

`search`只表示用户正式提交搜索，不由接口成功、零结果或失败反向决定。每次正式提交都按本次用户动作重新组装独立搜索上下文，不继承上一次搜索入口的临时参数。`trigger_type`使用以下六种枚举：

| 枚举值 | 用户动作 | 触发边界 |
|---|---|---|
| `carousel_term_button` | 搜索框展示轮播词且用户未改写，直接点击搜索按钮 | 用户改写内容后点击按钮改用`manual_search_button` |
| `manual_enter` | 用户手动输入后按回车 | 仅输入不发送 |
| `manual_search_button` | 用户手动输入后点击搜索按钮 | 未改写的轮播词使用`carousel_term_button` |
| `suggestion_select` | 用户点击输入联想中的搜索词建议 | 仅该入口携带本次建议位置；存在稳定对象ID时可增加`suggestion_object_id` |
| `history_select` | 用户点击搜索历史中的搜索词 | `search_term`取搜索模块正式输出的分析词 |
| `popular_term_select` | 用户点击搜索页热门搜索词 | 热门品牌和热门Collection入口不属于搜索提交 |

结果页URL携带编码后的搜索词、`trigger_type`以及已生效的筛选和排序上下文。Search与Collection的动态筛选都使用后台配置提供的稳定`dimension_code`和`option_code`形成同一份已Apply筛选事实；前端不维护固定维度白名单，也不使用展示名称作为ID。`view_search_results`和Search／Collection的商品曝光、点击从该公共事实读取筛选上下文。直达搜索URL、刷新或页面恢复不补造`search`；URL没有`trigger_type`时留空，不猜测。只有`trigger_type=suggestion_select`的提交可携带`suggestion_position`和`suggestion_object_id`；其他五种入口必须省略这两个字段，不能残留上一次联想点击的值。

每一次实际发出的搜索结果请求最多产生一条`view_search_results`，`result_status`只能取以下一个值：

| 枚举值 | 含义 | 触发时机 |
|---|---|---|
| `success` | 请求成功且返回至少一个商品 | 成功结果完成展示 |
| `no_results` | 请求成功但商品数为0 | 零结果状态完成展示 |
| `failed` | 非Abort错误且重试结束仍失败 | 失败终态成立 |
| `cancelled` | 被新请求替换、显式取消或离开页面导致请求中止 | 取消终态成立 |

开发可使用不出现在GA4载荷中的内部请求标识处理并发和终态去重。本版本不要求`search_id`或`search_request_id`，历史载荷即使仍携带也不得用于本期事件关联、去重或验收。

每条Looply主动`view_search_results`固定携带`view_search_results_source=looply_custom`。GA自动网站搜索事件不携带该参数，其他事件也不得携带。长期配置关闭增强型衡量中的“网站搜索”；如GA4管理员需要做24～48小时双来源对比，可临时开启，按该来源参数分别统计，完成后再次关闭。

#### 3.5.2 商品曝光与点击

`view_item_list`表示一次成功形成的新商品列表结果。首次结果、已提交筛选／排序／搜索词或首页Tab形成新结果且请求成功时各发送一次；滚动追加、分页、失败、取消、未提交、重复条件、重复回调、缓存复用或结果未变化不发送。`items[]`仅携带本次结果首次成功展示时已加载的商品，商品位置从1开始。每次新结果生成UUID格式`list_instance_id`，后续`select_item`复用该值；同一页面沿用当前`page_instance_id`。卡片可视Hook仅用于一方曝光数据，不调用GA4 `view_item_list`。

`select_item.items[].index`使用筛选、排序和插入完成后的真实商品位置，同样从1开始。同一业务列表的曝光与点击必须使用一致的`placement_id`、`item_list_id`和`item_list_name`；Wishlist统一使用稳定标识`favorites_wishlist`，不得分别使用展示文案或不同常量。PC Favorites Drawer不创建新页面实例、不发送新的`page_view`，曝光和点击沿用打开Drawer前当前页面的`page_instance_id`。

#### 3.5.3 购物车查看与删除

- `view_cart`：同时覆盖Shopping Bag页面和PC Cart Drawer。非空购物车中至少一件可购商品成功展示时发送；Shopping Bag使用该页面新生成的`page_instance_id`，PC Cart Drawer沿用当前所在页面的`page_instance_id`，同一页面实例内各自最多发送一次。`items[]`包含当前展示的全部可购商品，`value`为这些商品金额合计，并携带对应`currency`。空购物车、只有不可购商品、加载失败和同一展示面的重复渲染不发送。
- `remove_from_cart`：只有购物车内容真实减少后发送；本期一物一码商品的实际减少数量固定为1，并携带`currency`、`value`和被删除商品。删除失败、无变化和仅打开操作区不发送。

#### 3.5.4 页面实例公共规则

`page_instance_id`唯一识别用户实际进入并停留的这一次页面。它不是页面URL、GA4 Session ID、Looply Session ID或用户ID。

该ID由Web公共埋点上下文在页面实例建立时生成一次并保存。GA4适配器和一方平台适配器从同一个公共上下文读取；业务页面、搜索模块、商品模块和购物车模块不得分别生成。

| 页面动作 | 处理 |
|---|---|
| 首次到达页面、整页刷新、进入另一个有效路由、浏览器前进或后退重新进入页面 | 生成新的`page_instance_id` |
| 从其他页面提交搜索并进入搜索结果页 | 结果页生成新的`page_instance_id` |
| 已在搜索结果页正式提交新的搜索词并形成新的页面上下文 | 生成新的`page_instance_id` |
| 同一搜索结果页Apply筛选、Apply排序或Reset | 沿用当前`page_instance_id` |
| 列表加载更多、模块重渲染、接口重复回调或同一路由重复监听 | 沿用当前`page_instance_id` |

需要该字段的事件统一从公共上下文读取，不得由GA4 reporter临时生成第二套ID，也不得用URL、Session或用户ID替代。字段缺失时省略该参数，事件仍按已经成立的业务事实正常发送。

#### 3.5.5 字段来源与传递契约

| 字段 | 适用事件 | 谁提供／生成 | 来源与传递链路 | 缺失处理 |
|---|---|---|---|---|
| `event_id` | `view_search_results`及需要事件级幂等的事件 | Web公共事件上下文 | 事件成立时生成；同一事件重试保持同值；每次发送使用独立参数对象 → dataLayer → GTM → GA4 | 无法生成时省略，事件继续发送；不得继承其他事件的操作ID |
| `page_instance_id` | `page_view`、`view_search_results`、`view_item_list`、`select_item`、`view_item`、`view_cart`及其他需要同页关联的事件 | Web公共页面实例上下文 | 按3.5.4生成 → dataLayer → GTM → GA4 | 缺失时省略，事件继续发送；不得生成替代值 |
| `page_location` | 适用的主动页面和业务事件 | 事件发生时浏览器当前URL | 当前完整URL（含已生效搜索词、筛选和排序）→ dataLayer → GTM → GA4 | 同页状态变化后按事件发生时URL更新；不得用基础路由覆盖完整URL |
| `page_referrer` | 适用的主动页面和业务事件 | Web公共页面实例上下文 | 当前页面实例建立前的真实上一页面 → dataLayer → GTM → GA4 | 同一页面实例内保持不变；直达或无法确定时省略，不得承载当前动作URL |
| `page_view_source` | 仅Looply主动`page_view` | GA4适配器 | 固定写入`looply_custom` → dataLayer → GTM → GA4 | 主动事件正常链路应携带；GA自动事件和其他事件不补该字段 |
| `view_search_results_source` | 仅Looply主动`view_search_results` | GA4适配器 | 固定写入`looply_custom` → dataLayer → GTM → GA4 | 主动事件正常链路应携带；GA自动事件和其他事件不补该字段 |
| `search_term` | `search`、有搜索词的`view_search_results`和搜索结果`view_item_list` | 搜索模块 | 复用搜索模块用于构造结果URL的正式分析词 → dataLayer／URL → GTM → GA4 | 取得不到时省略，事件继续发送；不得回退为未经处理的输入原文 |
| `trigger_type` | `search`；站内提交形成的结果和曝光事件 | 搜索交互点 | 按六种动作确定 → dataLayer，同时进入结果页URL → 结果与曝光事件解析 → GA4 | 能取得时携带；直达URL没有时省略，不猜测 |
| `suggestion_position` | 仅`suggestion_select`形成的`search` | 搜索联想列表组件 | 被点击建议在当前联想列表中的实际位置，从1开始 → dataLayer → GTM → GA4 | 能取得时携带；其他入口必须省略；缺失时事件继续发送 |
| `suggestion_object_id` | 仅有稳定建议实体的`suggestion_select` | 搜索模块 | 使用已有稳定建议对象ID → dataLayer → GTM → GA4 | 可选；其他入口必须省略；没有稳定ID时不生成临时ID |
| `filter_ids` | `view_search_results`及Search／Collection筛选后的`view_item_list`、`select_item` | Search／Collection公共筛选上下文 | 只读取最终已Apply的离散筛选事实；每项使用后台稳定`dimension_code:option_code`，按Code稳定排序、去重后用逗号连接，例如`category:CA5GYR4GDRH2K,series:SEB7TNVEXWVF7` → dataLayer → GTM → GA4 | 无筛选时省略；单项缺稳定Code时仅省略该项，事件继续发送；不得用展示名称或前端固定枚举代替；价格区间本期不放入`filter_ids` |
| `sort_type` | `view_search_results`及搜索结果曝光 | 搜索模块／结果URL | 读取当前实际生效的稳定排序枚举，包括默认排序 → dataLayer → GTM → GA4 | 无法确认时省略，事件继续发送；不根据UI文案猜测 |
| `result_status` | `view_search_results` | 搜索结果状态控制器 | 按3.5.1唯一终态 → dataLayer → GTM → GA4 | 缺失时省略，事件继续发送；不得伪造终态 |
| `result_count` | 成功或零结果的`view_search_results` | 搜索接口 | 使用响应总结果数，不使用已渲染卡片数 → dataLayer → GTM → GA4 | 来源正常且能取得时携带；暂时无法取得时省略，事件继续发送 |
| `duration_ms` | `view_search_results` | 搜索请求控制器 | 从结果请求发起到唯一终态的毫秒数 → dataLayer → GTM → GA4 | 来源正常且能取得时携带；暂时无法取得时省略，事件继续发送；不得填写固定值 |
| `failure_type` | `failed`结果事件 | 搜索请求控制器 | 映射为`network_error`、`timeout`、`http_error`、`invalid_response`或`unknown` → dataLayer → GTM → GA4 | `failed`且能取得时携带；缺失时省略，事件继续发送；不得发送错误原文 |
| `placement_id` | `view_item_list`、`select_item` | 当前商品模块 | 按下表使用稳定常量；同一列表曝光与点击保持一致 → dataLayer → GTM → GA4 | 缺失时省略，事件继续发送；不得伪造展示位 |
| `item_list_id`、`item_list_name` | `view_item_list`、`select_item` | 当前商品模块 | 使用同一业务列表的稳定标识；曝光与点击保持一致 → dataLayer items → GTM → GA4 | 缺失时省略，事件继续发送；不得用临时DOM顺序或展示文案分别生成不同值 |
| `items[].item_id` | 三个商品／购物车事件 | 商品或购物车数据 | API的`listing_public_code` → dataLayer items → GTM → GA4 | 能取得时携带；缺失时省略，不得使用内部ID、SKU或SEO slug替代，事件继续发送 |
| `items[].index` | `view_item_list`、`select_item` | 商品列表组件 | 筛选、排序和插入完成后的业务列表位置，从1开始 → dataLayer → GTM → GA4 | 来源正常且能取得时携带；暂时无法取得时省略，事件继续发送；不得用0或猜测值 |
| `currency` | `view_cart`、`remove_from_cart` | 购物车／商品价格上下文 | 与价格同源的实际展示和结算币种 → dataLayer → GTM → GA4 | 能取得时携带；缺失时省略，不写死`USD`，事件继续发送 |
| `value` | `view_cart`、`remove_from_cart` | 购物车状态 | 前者为全部可购商品金额合计，后者为本次真实减少金额 → dataLayer → GTM → GA4 | 能取得时携带；缺失或非法时省略，不填0占位，事件继续发送 |
| `items[].price`、`items[].quantity` | `view_cart`、`remove_from_cart` | 商品／购物车数据 | 当前实际单价和数量；本期一物一码删除数量为1 → dataLayer items → GTM → GA4 | 能取得时携带；缺失时省略，事件继续发送，不根据点击动作或默认值猜测 |
| `step_version` | `add_shipping_info`、`add_payment_info` | Checkout步骤状态 | `add_shipping_info`在同一`checkout_id`首次有效shipping_tier为1，之后仅在有效shipping_tier变化时递增；同一事实重试保持同值 → dataLayer → GTM → GA4 | 取得不到时省略，事件继续发送；不得因地址变化、渲染、离页或无变化操作递增 |

本批五个事件的统一规则：事件是否发送只取决于对应业务事实是否已经发生，不因参数缺失停止发送；参数能够取得时正常携带，无法取得时省略且不伪造默认值。本节所称“应传”表示来源正常时应携带，不表示传输Schema或Zod必须将其声明为阻止事件发送的`required`字段。本期不新增线上参数缺失诊断事件或诊断机制。

动态筛选维度以后台当前配置为准。新增`Series`或后续新增维度时，只要后台同时提供稳定维度Code和选项Code，前端无需再次新增枚举；选择后取消、关闭面板或未Apply的值不进入`filter_ids`，Reset后省略该字段。后台／数据平台维护Code到展示名称的可追溯映射，事件本身只保留稳定Code。

字段统一按以下链路传递：

```text
业务页面或公共上下文形成真实值
→ Web GA4适配器组装looply_ga4_* dataLayer事件
→ GTM Custom Event Trigger命中唯一GA4 Event Tag
→ Data Layer Variable读取同名字段
→ GA4 Event Tag映射事件参数与items[]
→ 浏览器发送g/collect
→ Tag Assistant／DebugView／真实请求验收
```

`placement_id`使用以下封闭值：

| 场景 | `placement_id` |
|---|---|
| 首页For You | `home_feed_for_you` |
| 首页New Arrivals | `home_feed_new_arrivals` |
| Collection商品列表 | `collection_results` |
| 搜索结果列表 | `search_results` |
| 搜索无结果推荐 | `search_no_results_recommendations` |
| 商详You May Also Like | `product_you_may_also_like` |
| 商详Recently Viewed | `product_recently_viewed` |
| PC＋Mobile Wishlist | `favorites_wishlist` |
| PC＋Mobile Recently Viewed | `favorites_recently_viewed` |
| Mobile Favorites推荐 | `favorites_recommendations` |
| Shopping Bag商品列表 | `shopping_bag_items` |

#### 3.5.6 新增参数的GA4分析用途

| 用途 | 参数 | 产品要求 |
|---|---|---|
| GA4标准参数 | `search_term`、`currency`、`value`、`items[]`及`items[].index` | 按GA4标准事件和电商字段使用，不重复注册同义自定义字段 |
| GA4报表／探索维度 | `trigger_type`、`result_status`、`failure_type`、`placement_id`、`sort_type`、`page_view_source`、`view_search_results_source` | 需支持按搜索入口、结果状态、失败类型、商品展示位、排序方式和主动事件来源分析；两个来源参数注册为事件范围自定义维度，其他参数的具体注册方式由GA4技术方案确定 |
| GA4报表／探索指标 | `result_count`、`duration_ms`、`suggestion_position` | 需支持搜索结果数、结果返回耗时和联想点击位置分析；具体注册和配置方式由GA4技术方案确定 |
| 仅原始事件关联与验收 | `event_id`、`page_instance_id`、`suggestion_object_id`、`filter_ids` | 参数仍随适用事件发送，但不注册为GA4自定义维度或指标；用于原始数据、DebugView和请求验收，避免高基数报表 |

#### 3.5.7 配送信息保存事实

`add_shipping_info`表示Checkout首次形成可继续结账的有效配送方式，或之后有效`shipping_tier`发生变化。同一`checkout_id`首次有效tier发送`step_version=1`；只有有效`shipping_tier`变化才递增并再次发送。新建、复用、切换或修改地址后，如果最终有效tier未变化，不新增事件；页面显示变化但没有新的业务保存事实时也不生成事件。本版本不要求`shipping_info_source`，历史代码存在该字段时不得用它改变事件成立条件或幂等结果。

同一`checkout_id`内，首次有效tier使用`step_version=1`，之后每次有效tier变化使用递增且稳定的版本；同一tier事实重试保持版本不变。仅进入或离开Checkout、返回其他页面、组件重渲染、地址变化但tier未变化或校验失败均不发送，也不递增版本。

## 四、排重与事件生命周期

### 4.1 平台边界

GA4普通事件不会按Looply自定义`event_id`或商品ID提供通用自动排重。event_id用于Looply本地幂等、日志和对账，不得依赖GA4丢弃重复普通事件。Purchase的`transaction_id`是平台辅助防线，Looply仍必须主动幂等。

### 4.2 排重矩阵

| 事件类别 | Looply幂等键 | 硬刷新 | 重新进入/真实再次操作 |
|---|---|---:|---:|
| page_view | page_instance_id + route_key | 新发一次 | 新发一次 |
| view_item_list | page_instance_id + placement_id + listing_public_code | 新页面实例重新判断曝光 | 新页面实例重新判断曝光 |
| view_item | page_instance_id + listing_public_code | 新发一次 | 新发一次 |
| search | 单次正式提交的event_id | 刷新不补发 | 新的正式提交发送 |
| view_search_results | 页面实例 + 当前结果URL状态 + 内部请求标识 | 刷新可形成新的结果终态 | 新结果请求形成新的唯一终态 |
| select_item | selection_id | 不因刷新发 | 新点击发 |
| wishlist/cart变更 | 成功事务ID | 不发 | 新成功事务发 |
| view_cart | page_instance_id + 展示面（Shopping Bag／PC Cart Drawer） | 新页面实例重新判断 | 同一页面实例内各展示面最多一次；进入Shopping Bag形成新页面实例后可再发 |
| checkout步骤 | checkout_id + step + step_version | 不因页面展示发 | 实际保存新版本发 |
| purchase | consumer + order_id持久化记录 | 不发 | 同订单永不再发 |
| refund | refund_id服务端幂等 | 不适用 | 新退款ID发 |

### 4.3 SDK与GTM规则

- 全局只允许一个活动GA4适配器和一个共享GTM加载器；重复初始化必须返回已有实例。
- 当前页面生命周期以内存Map排重；需要跨刷新防重的业务事件使用sessionStorage或受控一方持久化记录。
- 浏览器成功页只展示订单支付结果，不产生、claim、确认或补发Purchase。
- SDK不可用或被AdBlock阻断时不影响业务流程；写匿名失败指标。
- 只有事件名非法、地区策略禁止、事件重复或无法形成事件本体时不push dataLayer事件。本批五个事件的业务参数缺失不阻止事件发送；可取参数正常携带，不可取参数省略且不伪造默认值。
- 排重必须发生在`window.dataLayer.push`之前；GTM触发器、标签或GA4平台不得作为Looply业务排重机制。
- 每次组装事件必须创建独立参数对象；发送完成后不得在共享上下文中保留`event_id`、`wishlist_operation_id`、`cart_operation_id`或其他业务操作ID。操作ID只属于产生它的事件，同一事件重试可复用，其他事件不得继承。
- GTM中的Measurement ID、容器ID和发布版本由环境配置管理，业务payload不得携带或覆盖这些配置。

## 五、Purchase与Refund

### 5.1 Purchase事实和上下文

Purchase只在支付渠道异步回调已验签且订单第一次进入最终paid时产生。该事务原子完成订单状态更新、冻结GA4上下文和创建一条`payment.paid`业务Outbox。

GA4上下文由checkout session在支付前保存，至少包含：order_id、checkout_id、paid_at、GA client_id、GA session_id、可选非PII user_id、页面语言、可信event source URL、region_code、region_policy_version、google_measurement_allowed、captured_at、schema_version。不得依赖成功页补齐这些字段。

### 5.2 服务端Purchase唯一投递

1. 订单／支付服务端首次确认`order_id`进入最终`paid`时，原子写入一条`payment.paid`业务事实与一条GA4 Purchase投递任务。
2. 唯一服务端发送者读取权威订单金额、币种、税费、运费、商品明细和支付前冻结的GA4关联上下文，通过Measurement Protocol发送一次`purchase`。
3. `transaction_id`固定等于父订单`order_id`；不得使用子订单号、支付流水号、金额或时间猜测关联。
4. 同一`order_id + purchase + measurement_id`只允许一个逻辑任务；网络失败复用同一幂等键与`transaction_id`重试，不新建第二条成交事实。
5. 浏览器成功页只查询并展示订单状态，不调用`trackEvent('purchase')`，也不参与发送权竞争、执行确认或失败补发。
6. `client_id`、`session_id`及合法来源上下文缺失不阻止Purchase事实成立或服务端投递；系统按数据质量缺口记录并告警，不伪造默认值。

### 5.3 Measurement Protocol要求

服务端使用`paid_at`作为事实发生时间，并使用支付前冻结的`client_id`、`session_id`、可选非PII `user_id`和可信来源上下文保持与原会话的分析关联。Measurement Protocol返回成功只代表请求被接受，不单独证明报表已正确入账；必须通过投递台账及订单`order_id`与GA4 `transaction_id`的定期对账验证完整性和重复情况。

### 5.4 Refund

Refund只在支付渠道确认资金成功退回时产生。每次成功退款以refund_id创建服务端GA4任务，transaction_id固定为原order_id。部分退款发送实际退款items和本次商品金额；全额退款发送完整退款明细。

同一订单允许多次不同refund_id的部分退款。Looply负责refund_id幂等；不得假设GA4会根据自定义refund_id自动排重。Refund不由浏览器发送，避免刷新和客服操作界面产生重复。

## 六、可靠投递与数据模型

### 6.1 状态与幂等

| 对象 | 主动幂等键 |
|---|---|
| payment.paid业务事实 | order_id + payment.paid + sequence_no |
| GA4 Purchase | order_id + purchase + measurement_id |
| GA4 Refund | refund_id + refund + measurement_id |

服务端任务状态：pending、processing、accepted、retryable_failed、permanent_failed。区域策略禁止为`suppressed_by_region`，该状态是零网络请求的业务终态，不伪装成accepted；它只表示一期地区门控，不表示用户曾作出拒绝。

### 6.2 数据表

| 表 | 用途 | 关键字段/约束 |
|---|---|---|
| ga4_property_config | 环境GA4资产 | environment、property_ref、stream_ref、measurement_id、api_secret_ref、status；environment唯一 |
| ga4_event_contract | 事件Schema版本 | event_name、schema_version、required_fields、enabled、effective_at |
| ga4_conversion_context_snapshot | 订单GA4上下文 | order_id唯一；checkout_id、paid_at、market_code、locale_code、currency_code、region_code、region_policy_version、google_measurement_allowed、client_id、session_id、user_id、URL、language、schema_version；市场、币种和地区策略均为事实快照 |
| outbox_event | 共享可靠业务事实 | aggregate+event_type+sequence_no唯一 |
| ga4_upload_log | MP Purchase/Refund台账 | business_event_id+event_type+measurement_id唯一；状态、payload_hash、attempt、response、validation和错误 |
| ga4_job_checkpoint | 异步任务水位 | job_name+scope_key唯一 |

GTM容器ID、环境和已批准发布版本可作为`ga4_property_config`的受控配置字段或配置中心条目保存，不由业务页面传入。本PRD不创建广告账号、Catalog、触点、身份缝合、归因、广告花费或ROAS数据表。

对本批五个事件，`ga4_event_contract.required_fields`不得用于在参数缺失时阻止事件发送；其业务参数按3.5.5的可选传递规则处理。

### 6.3 错误分类

| 类别 | 示例 | 处理 |
|---|---|---|
| transient_network | timeout、连接重置、5xx | retryable_failed、指数退避 |
| rate_limited | 429 | 尊重Retry-After |
| invalid_payload | 事件名、字段、金额或时间非法，或金额事件缺少业务事实币种 | permanent_failed、死信 |
| market_currency_mismatch | 业务事实币种与Market国家法定币种不一致 | 仍发送业务事实币种；记录数据质量诊断并告警，不阻断GA4事件 |
| permission_denied | API Secret/Property权限错误 | permanent_failed、P0告警 |
| dependency_not_ready | 订单上下文暂不可读 | 有界重试 |
| suppressed_by_region | 地区策略禁止Google测量 | 零请求终态 |

GA4 collect返回2xx不代表payload语义正确。staging和预发布必须使用debug validation端点；production持续监控关键事件数量、重复transaction_id和异常下降。

## 七、安全、合规与数据质量

### 7.1 PII禁止项

DataLayer、GA4事件参数、user_id、日志、死信和告警不得包含：邮箱、电话、姓名、完整地址、支付卡号、证件、访问Token或可逆PII。`user_id`只能使用稳定的Looply内部伪名ID，不使用邮箱、手机号或其直接拼接值。

### 7.2 密钥与权限

- Measurement Protocol API Secret只存Secret Manager，仅Purchase/Refund唯一服务端发送者可读。
- staging与production使用不同Property、Stream、Measurement ID和API Secret。
- staging与production使用独立GTM环境配置和发布版本；生产发布需双人复核并可快速回滚。
- GA4访问按最小权限分配；数据分析、配置管理和密钥读取权限分开。
- API Secret轮换前双密钥验证，失败不得回退到代码中的静态密钥。

### 7.3 数据质量监控

- 按事件监控数量、用户数、非法事件率和语言分布。
- Purchase监控权威paid订单数、服务端投递状态、延迟、失败和重复transaction_id，并按order_id定期对账。
- Refund监控处理延迟、失败率和订单关联缺失。
- 区域门控按region_code和策略版本监控允许/禁止数量、`suppressed_by_region`数量及异常地区解析量；禁止地区出现任何GA4请求即P0告警。
- 页面监控page_view/view_item比率、组件重复率和SPA路由缺失。
- 重大版本发布前后比较7日基线；异常下降或突增超过阈值告警。

## 八、环境与发布

| 环境 | 配置与用途 |
|---|---|
| local/dev | 使用本地mock dataLayer，不加载生产GTM，不发送正式GA4 |
| staging | 独立Property、Stream和GTM环境，使用Preview、DebugView、debug_mode和validation验证 |
| production | 正式Property、Stream和已批准GTM发布版本，关闭长期debug，受控灰度 |

发布顺序：事件Schema与SDK单元测试 → GTM Preview验证Custom Event、变量和标签 → staging DebugView验证 → Measurement Protocol validation → 支付/退款联调 → EEA、英国、瑞士禁止地区测试 → GTM生产版本双人复核 → 小流量灰度 → 全量。

GA4项目不阻塞Google Ads或Merchant上线；Google Ads项目也不得成为GA4发布前置条件。

## 九、测试与验收

### 9.1 事件与页面

| 编号 | 场景 | 预期 |
|---|---|---|
| E01 | EEA、英国或瑞士地区 | 不初始化dataLayer、不加载GTM或GA4标签、不push `looply_ga4_*`，零GA4请求 |
| E02 | 区域策略允许 | 共享GTM加载器与GA4适配器各只初始化一次；一期不读取CMP或同意状态 |
| E03 | 首次页面加载 | 核心路由就绪后恰好一次Looply主动page_view，携带页面实例和主动来源参数 |
| E04 | SPA有效路由 | 每次路由恰好一次Looply主动page_view，预取不发；GA自动事件可并存但不替代主动事件 |
| E05 | 硬刷新 | 新page_instance，一次Looply主动page_view和一次view_item；两者使用同一页面实例ID |
| E06 | React重复渲染/StrictMode | 不重复发送 |
| E07 | 商品曝光边界 | 未达到50%、达到不足1秒、后台或失焦不发送；达到50%且持续1秒后发送 |
| E08 | 加购接口重复回调 | 同cart_operation_id一次add_to_cart |
| E09 | 17类Schema | 名称、参数、金额、listing_public_code和语言规则全部通过 |
| E10 | DataLayer扫描 | 无原始PII、点击ID或广告Cookie |
| E11 | GTM Preview逐事件验证 | 每个`looply_ga4_*`只触发一个对应GA4 Event Tag，变量映射完整 |
| E12 | 业务组件静态扫描 | 不存在直接gtag调用、Measurement ID或手写GA4标签 |
| E13 | 香港新增或停用一种市场语言 | 仅按Market配置开始或停止对应页面语言事件，不影响其他市场语言 |
| E14 | 六种正式搜索提交 | 每次只发送一条search，trigger_type与实际入口一致 |
| E15 | 搜索结果终态 | 每次结果请求只产生success、no_results、failed、cancelled之一；直达URL不补search |
| E16 | 搜索结果商品曝光 | 达标商品按page_instance_id + placement_id + listing_public_code去重，并携带当前URL搜索上下文 |
| E17 | Shopping Bag与PC Cart Drawer | 两个展示面均在至少一件可购商品成功展示时发送`view_cart`；Drawer沿用当前页面实例且同一页面实例最多一次，进入Shopping Bag形成新页面实例后可再发送 |
| E18 | 删除购物车商品 | 只有内容真实减少时发送remove_from_cart；失败、无变化和仅打开操作区不发送 |
| E19 | 增强型衡量网站搜索 | 长期关闭“网站搜索”；如临时开启对比，按来源参数拆分并在24～48小时后再次关闭 |

### 9.2 Purchase与Refund

| 编号 | 场景 | 预期 |
|---|---|---|
| P01 | 支付processing | 零Purchase |
| P02 | 重复支付回调 | 一条业务Outbox、一条GA4 Purchase逻辑任务 |
| P03 | 首次确认paid | 唯一服务端发送者通过MP发送一次Purchase，transaction_id等于父订单order_id |
| P04 | 重复Worker或并发消费 | 仅一个逻辑任务取得发送权；其余不新增Purchase事实 |
| P05 | 用户关闭或未打开成功页 | 不影响服务端Purchase投递 |
| P06 | 成功页晚到、刷新或多标签 | 页面只展示订单状态，零浏览器Purchase请求 |
| P07 | GA关联上下文缺失 | Purchase仍投递；缺失字段不伪造，并记录数据质量告警 |
| P08 | 金额3299、税80、运费0 | GA4 value=3299，tax=80，shipping=0 |
| P09 | EEA、英国或瑞士订单/退款 | 浏览器和服务端均零请求，任务为`suppressed_by_region` |
| P10 | validation返回字段错误 | staging放行失败，生产任务不得上线 |
| P11 | 部分退款 | 同原transaction_id，发送本次退款明细 |
| P12 | 多次部分退款 | 不同refund_id分别一次，均关联原order_id |
| P13 | 重复退款回调 | 同refund_id不重复发送 |
| P14 | MP网络超时 | 同幂等键和transaction_id重试 |
| P15 | 业务事实币种与国家法定币种不一致 | 仍发送业务事实币种；记录市场/币种不一致诊断并告警 |

### 9.3 放行清单

- [ ] GA4 Property、Web Stream、Measurement ID和API Secret按环境隔离。
- [ ] staging/production的GTM环境、Google Tag、Custom Event触发器、GA4 Event Tag和变量按矩阵配置并发布。
- [ ] 基础page_view及17类业务事件Schema和触发时机通过。
- [ ] SPA、硬刷新、组件重渲染和业务事务排重通过。
- [ ] 主动`page_view`与主动`view_search_results`来源参数已在dataLayer、GTM、真实请求和GA4中一致，并已注册事件范围自定义维度。
- [ ] 搜索入口上下文、商品曝光／点击位置、页面来源、事件ID隔离、商详页面实例和配送保存版本按9.4通过。
- [ ] 区域策略允许时发送通过；EEA、英国、瑞士不加载GTM/GA4且浏览器与服务端均零请求。
- [ ] Purchase服务端唯一投递、并发消费、重试与浏览器零发送测试通过。
- [ ] Refund部分、多次和重复回调通过。
- [ ] DataLayer与日志PII扫描通过。
- [ ] GTM Preview确认每个浏览器业务事实只触发一次GA4标签，且不存在Purchase Custom Event触发器或浏览器Purchase标签。
- [ ] 已验证美国、香港已启用市场语言均按当前页面真实语言发送。
- [ ] 已验证浏览、加购、服务端Purchase和Refund均取业务事实币种；市场币种不一致时不静默替换且有诊断告警。
- [ ] staging validation、生产灰度和关键指标告警就绪。

### 9.4 线上修复验收要求

本节只规定上线后必须成立的最终行为。历史运行证据、当前通过状态和阻塞记录保存在《Looply GA4线上验收问题与开发修复单 v1.2》，不在PRD重复维护。

| 编号 | 范围 | 验收要求 |
|---|---|---|
| O01 | `search`入口隔离 | 连续执行联想、回车、搜索按钮、历史词、热门词和轮播词；只有联想事件携带本次真实建议位置，其他入口不携带联想字段 |
| O02 | Search页面实例 | 每次正式新搜索形成新`page_instance_id`和一条Looply主动`page_view`；同一搜索链内部ID一致；Apply筛选、排序和Reset沿用当前ID |
| O03 | 动态筛选 | Search／Collection的页面最终状态、URL、公共筛选事实和GA4 `filter_ids`一致；Reset后不残留旧值 |
| O04 | 主动`page_view` | PC＋Mobile每个真实页面实例恰好一条Looply主动事件；允许另有GA自动事件，但自动事件不能替代主动事件 |
| O05 | `page_view`来源 | 仅Looply主动事件携带`page_view_source=looply_custom`；GA自动事件及其他事件不携带 |
| O06 | 搜索结果来源 | 仅Looply主动结果事件携带`view_search_results_source=looply_custom`；长期关闭GA自动网站搜索 |
| O07 | 列表展示 | 新列表结果成功展示时发送一次；滚动、分页、失败、重复条件或结果未变化不发送；不得出现空`items[]` |
| O08 | 商品点击 | 各入口点击位置与真实列表顺序一致；同一列表的曝光与点击使用一致的展示位和列表标识，Wishlist统一为`favorites_wishlist` |
| O09 | 页面URL与来源 | 事件`page_location`等于动作发生时当前完整URL；`page_referrer`等于当前页面实例建立前的真实上一页面。同页筛选／排序只更新后续事件的`page_location`，不更新`page_referrer`；直达允许来源为空 |
| O10 | 事件ID隔离 | 收藏、加购等操作后产生的其他事件不继承前一事件的操作ID；同一事件重试只复用自身ID |
| O11 | 商详页面实例 | `view_item`读取当前PDP的`page_instance_id`；刷新或重新进入产生新ID，同一实例重渲染不重复发送 |
| O12 | 配送方式版本 | 同一checkout首次有效tier发送`step_version=1`；仅有效`shipping_tier`变化时递增并再发送。地址变化但tier不变、离页、重渲染和无真实保存事实均不发送 |
| O13 | 来源字段全链路 | A01/A02必须同时验证Web事件对象、dataLayer、GTM Data Layer Variable、GA4 Event Tag参数映射、生产容器版本和真实`g/collect`请求；只验证Web代码或公共函数不能判通过 |

### 9.5 五个变更事件复验用例

| 编号 | 操作 | 预期结果 |
|---|---|---|
| G01 | 未改写轮播词，点击搜索按钮 | 一条`search`，`trigger_type=carousel_term_button`；结果URL、结果和曝光沿用同值 |
| G02 | 手动输入后按回车 | 一条`search`，`trigger_type=manual_enter` |
| G03 | 手动输入后点击搜索按钮 | 一条`search`，`trigger_type=manual_search_button` |
| G04 | 点击输入联想 | 一条`search`，`trigger_type=suggestion_select`并有从1开始的建议位置 |
| G05 | 点击搜索历史 | 一条`search`，`trigger_type=history_select` |
| G06 | 点击热门搜索词 | 一条`search`，`trigger_type=popular_term_select` |
| G07 | 点击热门品牌或热门Collection | 不发送`search`；按入口点击和目标页访问处理 |
| G08 | 正常有结果搜索 | 一条`search`和一条`view_search_results(success)`；搜索词和枚举与URL一致 |
| G09 | 无结果搜索 | 一条`search`和一条`view_search_results(no_results)`，`result_count=0` |
| G10 | 直达无结果URL | 不补造`search`；发送一条`view_search_results(no_results)` |
| G11 | 搜索结果Apply筛选、Apply排序或Reset | 不新增`search`；生成新的结果终态，沿用当前页面实例和原`trigger_type` |
| G12 | 搜索结果首屏曝光 | 每个达标商品只计一次，具备页面实例、展示位、从1开始的位置及URL搜索上下文 |
| G13 | 页面后台、失焦或商品不足50%／1秒 | 不发送该商品曝光 |
| G14 | Shopping Bag与PC Cart Drawer | Drawer沿用当前页面实例且同一页面实例最多一条`view_cart`；进入Shopping Bag形成新页面实例后可再发送；能够取得的币种、金额和商品参数正常携带 |
| G15 | 空购物车或只有不可购商品 | 不发送`view_cart` |
| G16 | 成功删除商品 | 一条`remove_from_cart`，币种、实际减少金额、商品和数量正确 |
| G17 | 同时观察GA4与一方事件 | 同一页面行为使用相同`page_instance_id` |

每项须保留Tag Assistant、DebugView或浏览器真实`g/collect`请求证据。事件名称、次数、参数和值全部符合本节后，本批五个事件方可判定通过。

## 十、依赖与风险

| 依赖/风险 | 影响 | 控制措施 | 责任方 |
|---|---|---|---|
| 业务页面触发时机不一致 | 漏斗失真 | 统一Schema、权威触发点和自动化测试 | 产品/Web |
| SPA重复监听 | 事件倍增 | 唯一监听器、page_instance和StrictMode测试 | Web |
| GTM触发器重复或变量映射错误 | 漏报、重报或字段错误 | 环境隔离、版本锁定、双人复核、Preview逐事件验收和快速回滚 | 数据/Web |
| GA4普通事件无通用排重 | 指标虚高 | Looply主动幂等，不依赖event_id | Web/数据 |
| 服务端Purchase任务失败 | 成交数据缺失或延迟 | Outbox、幂等重试、死信告警及order_id对账 | 后端/数据 |
| 区域策略配置错误 | 禁止地区产生Google请求或允许地区漏报 | 可信服务端注入、策略版本快照、自动化地区矩阵测试、禁止地区请求P0告警 | 合规/Web |
| collect 2xx但payload无效 | 静默丢数据 | staging validation和指标对账 | 数据/测试 |
| 重复导入Google Ads | 广告转化重复 | 本期不关联Ads、不导入GA4 Purchase | 数据/广告运营 |
| API Secret泄漏 | 数据污染 | Secret Manager、最小权限、轮换 | 运维 |

## 十一、版本与官方依据

### 11.1 v1.8范围

本版本继承v1.7的服务端Purchase、地区门控、页面语言、金额、Refund、五事件和动态筛选规则，并统一剩余问题口径：`page_location`表示事件发生时当前完整URL，`page_referrer`只表示当前页面实例建立前的真实上一页面；`add_shipping_info`按同一checkout首次有效tier及后续tier变化成立；PC Favorites Drawer沿用打开前页面实例；主动事件来源字段必须完成Web、dataLayer、GTM、生产容器和真实请求的全链路验收。规则确认不代表生产已经实现，仍须按第九章验收。

《Looply GA4线上验收问题与开发修复单 v1.2》只保留历史运行证据和复测索引；目标规则以本PRD为准。生产实际GTM容器及权限属于验收阻塞，不改变本PRD的业务规则。

### 11.2 UI

本期不新增GA4运营后台或App页面。业务事件由现有网站页面触发；事件验证使用GA4 DebugView、Realtime、Explorations和内部监控。

### 11.3 官方依据

- [Google Tag Manager dataLayer](https://developers.google.com/tag-platform/tag-manager/datalayer)
- [GTM GA4事件设置](https://support.google.com/tagmanager/answer/9442095)
- [GA4推荐事件](https://developers.google.com/analytics/devguides/collection/ga4/reference/events)
- [GA4 Measurement Protocol概览](https://developers.google.com/analytics/devguides/collection/protocol/ga4)
- [Measurement Protocol参考](https://developers.google.com/analytics/devguides/collection/protocol/ga4/reference)
- [Measurement Protocol事件](https://developers.google.com/analytics/devguides/collection/protocol/ga4/reference/events)

### 11.4 历史关系

`looply-GA4数据分析-PRD-v1.0.md`保留为直接Google Tag方案的历史版本；v1.1为美国单市场GTM基线，v1.2起以Market配置驱动已启用市场语言和币种事实。`looply-站外广告投放系统-PRD-v2.13.md`中的多广告渠道、触点、归因、花费和ROAS内容不属于本GA4范围。旧ER v2.0不是本PRD的数据模型依据。

## 十二、开发集成示例

### 12.1 GTM初始化

共享GTM加载器读取由可信服务端注入的区域策略；`google_measurement_allowed=true`时才按环境加载一次容器并启用GA4适配器。一期不读取CMP或`analytics_storage`状态；EEA、英国、瑞士策略必须禁止加载：

```html
<script>
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({
    'gtm.start': Date.now(),
    event: 'gtm.js'
  });
  // 实际实现由共享加载器异步加载环境对应的 GTM-{CONTAINER_ID}，且只执行一次。
</script>
```

当前保留GA自动`page_view`；首屏和后续SPA有效路由仍必须由Looply显式push一次`looply_ga4_page_view`。主动事件固定携带`page_view_source=looply_custom`，自动事件不携带；报表和验收按该参数识别主动事件。Measurement ID只存在GTM环境变量或受控配置中。

### 12.2 page_view与view_item

```javascript
window.dataLayer.push({
  event: 'looply_ga4_page_view',
  ga4_event_name: 'page_view',
  page_instance_id: '{PAGE_INSTANCE_ID}',
  page_view_source: 'looply_custom',
  page_location: 'https://looply.com/{market-locale}/products/listing-123',
  page_referrer: 'https://looply.com/{market-locale}/search?keyword=chanel',
  page_title: 'Pre-owned Chanel Classic Flap',
  page_language: '{PAGE_LANGUAGE}'
});

window.dataLayer.push({
  event: 'looply_ga4_view_item',
  ga4_event_name: 'view_item',
  page_instance_id: '{PAGE_INSTANCE_ID}',
  currency: '{BUSINESS_CURRENCY}',
  value: 3299.00,
  items: [{
    item_id: 'CPE2E00000015',
    item_name: 'Pre-owned Chanel Classic Flap',
    item_brand: 'Chanel',
    item_category: 'Handbags',
    price: 3299.00,
    quantity: 1
  }]
});
```

### 12.3 Measurement Protocol Purchase

```http
POST https://www.google-analytics.com/mp/collect?measurement_id={GA4_MEASUREMENT_ID}&api_secret={GA4_API_SECRET}
Content-Type: application/json

{
  "client_id": "1234567890.1761581763",
  "user_id": "USER_99",
  "timestamp_micros": "1784894400000000",
  "events": [{
    "name": "purchase",
    "params": {
      "session_id": "1761581763",
      "engagement_time_msec": 1,
      "transaction_id": "ORDER_456",
      "currency": "{BUSINESS_CURRENCY}",
      "value": 3299.00,
      "tax": 80.00,
      "shipping": 0.00,
      "items": [{
        "item_id": "CPE2E00000015",
        "item_name": "Pre-owned Chanel Classic Flap",
        "price": 3299.00,
        "quantity": 1
      }]
    }
  }]
}
```

staging先调用`https://www.google-analytics.com/debug/mp/collect`验证。API Secret不得写日志、数据库payload或前端代码。

### 12.4 Measurement Protocol Refund

```json
{
  "client_id": "1234567890.1761581763",
  "user_id": "USER_99",
  "events": [{
    "name": "refund",
    "params": {
      "transaction_id": "ORDER_456",
      "currency": "{BUSINESS_CURRENCY}",
      "value": 100.00,
      "refund_id": "REFUND_789",
      "items": [{
        "item_id": "CPE2E00000015",
        "price": 100.00,
        "quantity": 1
      }]
    }
  }]
}
```

`refund_id`是Looply自定义审计参数，不替代transaction_id，也不能被视为GA4平台自动排重键。
