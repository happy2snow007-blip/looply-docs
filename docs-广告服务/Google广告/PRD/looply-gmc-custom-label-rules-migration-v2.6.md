# Looply 自建站 GMC Custom Label 规则（AI Coding 执行版 v2.6）

## 0. 文档定位与运行时输入

本版是 AI Coding 和开发验收唯一使用的当前规则，只描述 Looply 自建站运行逻辑。运行时输入仅限当前 Looply 商品/Offer/库存/类目数据、Looply 支付成功订单事件，以及以下版本化开发清单。

| 规则 | 文件 | Sheet | 数据区 | 当前数量 |
|---|---|---|---|---:|
| Top50 | `outputs/gmc-brand-series-mapping-20260828/looply-top50-looply-series-development-list.xlsx` | `Top50开发清单` | `Looply品牌`、`Looply系列`、`Looply系列ID` | 50 个组合 |
| Top30 | `outputs/gmc-brand-series-mapping-20260828/looply-top30-looply-series-development-list.xlsx` | `Top30开发清单` | `Looply品牌`、`Looply系列`、`Looply系列ID` | 93 个组合 |
| 历史出单初始清单 | `outputs/order-brand-series-mapping-20260828/looply-historical-sold-brand-series-development-list.xlsx` | `历史出单开发清单` | `Looply品牌`、`Looply系列`、`Looply系列ID` | 117 个组合 |

三份清单均只保留 Looply 字段，并按三列组合去重。开发以 `Looply品牌 + Looply系列ID` 精确匹配；`Looply系列` 仅用于展示、排查和审计，不能作为模糊匹配依据。

GMC 的每个 `custom_label_n` 的不同值上限按 **Merchant Account** 计算，不按 Market 或数据源分别计算。多个 Market 或数据源只要绑定到同一 `merchant_ref`，即共同占用该 Merchant Account 下相同 `custom_label_n` 的值额度。

## 1. 通用商品条件

五个标签均只针对当前 Market 中同时满足以下条件的商品：

- 商品状态为在售；
- 商品已发布到当前 Market 销售渠道；
- 当前可售库存 `available_quantity >= 1`；
- 当前 Market Offer、价格、库存和落地页有效。

任一条件不满足时，下一次 Feed 重算必须清除该商品不再满足条件的 `custom_label_n`，不得保留旧值。

## 2. 类目与 `custom_label_0`

商品是否为包袋由当前 Looply 类目树动态派生，不读取标题：

- `Luggage & Bags > Bags` 节点及所有后代：`is_bag=true`，`custom_label_0 = bag`；
- `Luggage & Bags > Bag Accessories` 及所有后代：`custom_label_0 = accessories`；
- `Jewelry & Accessories > Accessories`、`Jewelry`、`Watch Accessories` 及所有后代：`custom_label_0 = accessories`；
- `Jewelry & Accessories > Watches` 及所有后代：`custom_label_0 = watches`；
- `Pocket Watch`、`Clock` 当前无商品，暂不写入；
- 当前没有受控电子类目，`3C` 暂不写入。

包袋根节点 `category_code` 为 `CAZ0VHQPG842Q`。开发必须依据类目树父子关系判断后代，不得硬编码三级类目。商品类目移动后，触发当前 Market Feed 重算，先清除旧标签，再按新类目重新计算。

## 3. `custom_label_1`：Top50

读取第 0 节 Top50 清单。商品满足通用商品条件、`is_bag=true`，且 `Looply品牌 + Looply系列ID` 精确命中时：

```text
custom_label_1 = "top50-260713"
```

商品未命中清单时不写入。尺寸、材质、颜色、包型和商品标题不参与匹配。

## 4. `custom_label_2`：在售包袋品牌+系列

对满足通用商品条件、`is_bag=true`、品牌和系列有效的商品，生成：

```text
custom_label_2 = normalize(brand) + "__" + normalize(series)
```

`custom_label_2` 是本期唯一可能大量产生不同值的标签。Google 对同一 Merchant Account 的 `custom_label_2` 有 1,000 个不同值上限；本期采用 **账号全局 950** 的保留上限，为现有其他数据源、人工规则和数据波动预留空间。

### 4.1 账号全局 950 算法

1. 统计范围按 `merchant_ref` 分组。`merchant_ref` 相同的所有启用 Market、语言资源和数据源共同参与；不得按 `market_code`、`feed_label`、`data_source_ref` 或语言分别保留 950 个值。
2. 在每个 `merchant_ref` 范围内，仅统计当前满足通用商品条件、`is_bag=true`、品牌和系列有效的唯一可投放 Offer。相同 `merchant_ref` 下同一 `custom_label_2` 值在多个 Market、语言资源或数据源中出现时，合并计数，不重复占用不同值额度。
3. 按 `custom_label_2` 分组，计算每个标签值的 `eligible_offer_count`。
4. 若不同 `custom_label_2` 值不超过 950 个，全部保留；超过 950 个时，按 `eligible_offer_count` 降序、`brand_key` 升序、`series_key` 升序排序，只保留前 950 个标签值。
5. 未保留标签值对应的全部商品不写入 `custom_label_2`，记录 `excluded_label_value_limit`；不得改写为 `brand__other`，不得随机截断，也不得以 Market 或数据源分片绕过上限。
6. 每次相关商品、库存、Offer、Market 绑定或数据源绑定变化后，按同一算法重算对应 `merchant_ref` 的完整候选集合；此前被排除的组合在重新进入前 950 时自动恢复。
7. 若 Market 绑定到不同的 `merchant_ref`，各 Merchant Account 独立执行本算法，各自最多保留 950 个不同值。

`normalize()` 必须使用 Feed 服务唯一的、版本化的标准化函数，至少固定 Unicode NFKC、去除首尾空格、转小写、连续空格归一、`&`/连字符/斜杠归一规则；不得按标题、材质、尺寸、包型或相似度推测品牌或系列。品牌或系列缺失、冲突或无法标准化时不写入该标签，并记录 `unresolved_brand_series`。

## 5. `custom_label_3`：Top30

### 5.1 范围边界

Top30 的来源为 `包袋销量top数据0806.xlsx` 的 `Sheet1` 中 **B:G 六个系列列**，每列 30 条，共 180 条原始规则。六个来源品牌列及其 Looply 标准品牌固定如下：

| 来源列 | Looply品牌 |
|---|---|
| `LV` | `LOUIS VUITTON` |
| `GUCCI` | `GUCCI` |
| `Chanel` | `CHANEL` |
| `Prada` | `PRADA` |
| `Hermes` | `HERMÈS` |
| `Dior` | `DIOR` |

`Sheet1` A 列虽列出了其他品牌名称，但 A 列没有对应的品牌专属 Top30 系列列。因此 A 列中除以上六个品牌外的品牌，**不属于本期 Top30 规则**，不得因品牌名称出现而生成 `custom_label_3`。例如 Bottega Veneta、Celine、Saint Laurent、Fendi、Burberry、Chloé、Balenciaga、Loewe、Goyard、Miu Miu、Givenchy 均不纳入本期 Top30。

运行时不读取原始 Top30 表，只读取第 0 节已映射的 Top30 开发清单。该清单的 93 个 Looply 组合完全来自上述六个来源品牌列；其他品牌不会出现在本期清单中。

### 5.2 打标规则

商品满足通用商品条件、`is_bag=true`，且 `Looply品牌 + Looply系列ID` 精确命中 Top30 清单时，按命中品牌写入：

```text
custom_label_3 = normalize(brand) + "-top30"
```

同一品牌命中清单内任一系列即可写入该品牌标签。未命中清单不写入。不得按标题、材质、尺寸、包型、相似度、A 列品牌或其他非清单数据猜测系列/扩展品牌范围。

未来需要增加其他品牌时，业务必须先补充该品牌独立的 Top30 系列清单、完成 Looply 系列 ID 映射并发布新的 Top30 开发清单；不得仅凭品牌名称加入。

## 6. `custom_label_4`：历史出单

### 6.1 初始清单

读取第 0 节历史出单初始清单。商品满足通用商品条件、`is_bag=true`，且 `Looply品牌 + Looply系列ID` 命中初始清单或后续历史集合时：

```text
custom_label_4 = "historical-sold"
```

### 6.2 Looply 支付成功订单追加

Looply 自建站订单行在支付服务确认真实收款成功/已捕获后，使用支付成功时订单行的品牌、系列和系列 ID 快照，将该组合追加到历史集合。

- 真实用户支付成功后即算历史出单；
- 后续部分退款、全额退款或订单取消，均不从历史集合删除；
- 支付失败、待支付、支付处理中、未确认收款的订单不追加；
- 同一订单行必须幂等，建议键：`source_order_id + source_order_line_id`；
- 订单行缺少唯一系列 ID 或品牌/系列冲突时不追加，记录 `unresolved_historical_sold_mapping`。

### 6.3 测试邮箱排除

订单邮箱去除首尾空格并转小写后，若精确命中以下任一邮箱，即使支付成功也不追加：

```text
johnnywang0402@gmail.com
yangmingjing@zhuanzhuan.com
qiuhong@zhuanzhuan.com
chenxiaoru@zhuanzhuan.com
happy2snow007@gmail.com
cxc.pku@gmail.com
234387800@qq.com
ytoffee2@gmail.com
zhuowu78@gmail.com
wjn_wjn@hotmail.com
angelbaoweigg12138@gmail.com
chenxinyue@zhuanzhuan.com
yinyuanlu@zhuanzhuan.com
```

不得使用包含匹配、域名匹配或模糊匹配。邮箱为空时不能自动判定为测试订单，应记录邮箱缺失并按支付事实处理。

## 7. Feed 计算顺序与审计

1. 读取当前 Market 商品、Offer、库存和类目树；
2. 派生 `is_bag` 与 `custom_label_0`；
3. 读取商品当前 `Looply品牌`、`series_id`；
4. 读取 Top50 清单并生成 `custom_label_1`；
5. 按 `merchant_ref` 计算并应用跨数据源的 `custom_label_2` 账号全局 950 值上限；
6. 读取 Top30 清单并生成 `custom_label_3`；
7. 读取历史出单初始清单和 Looply 支付成功订单历史集合，生成 `custom_label_4`；
8. 对下架、库存为 0、Market 不可售、Offer 无效或移出包袋类目的商品清除不再满足条件的标签；
9. 输出审计：`top50_list_match`、`top30_list_match`、`historical_sold_initial_list_match`、`historical_sold_paid_order_append`、`excluded_test_email`、`unresolved_historical_sold_mapping`、`unresolved_brand_series`、`excluded_out_of_stock_or_not_on_sale`、`excluded_label_value_limit`。`custom_label_2` 审计必须包含 `merchant_ref`、标签值、`eligible_offer_count`、排名、保留结果、排除原因和计算版本。

## 8. 验收要求

- 三份开发清单均可读取，且只包含 Looply 三字段；
- Top30 清单只包含 LOUIS VUITTON、GUCCI、CHANEL、PRADA、HERMÈS、DIOR 六个品牌；
- A 列出现但不在上述六个品牌范围的商品，即使属于包袋也不写入 `custom_label_3`；
- Top30 商品必须同时命中正确品牌和系列 ID，不能仅按品牌打标；
- 同一 `merchant_ref` 下存在多个 Market 或数据源时，`custom_label_2` 的不同值合计最多为 950，不能对每个数据源各保留 950；
- 同一 `merchant_ref` 的候选值超过 950 时，按 `eligible_offer_count`、品牌键、系列键的固定排序保留前 950，所有来源均使用相同结果；
- 不同 `merchant_ref` 的 Merchant Account 独立计算 `custom_label_2` 上限；
- 历史出单初始清单可读到 117 个唯一组合；
- 真实用户支付成功后追加历史组合，后续退款/取消仍保留；
- 13 个测试邮箱即使支付成功也不追加；
- 重复订单事件不会重复写入历史集合；
- `LV × TM` 等无系列 ID 数据不会错误归入其他系列；
- 库存变 0、商品下架或移出包袋类目时清除当前 Feed 标签，但不删除历史集合事实。

## 9. 版本说明

v2.6 相对 v2.5：确认 GMC custom label 的不同值上限按 Merchant Account 而非数据源或 Market 计算；`custom_label_2` 改为按 `merchant_ref` 跨数据源统一排序并最多保留 950 个不同值，补充相应重算、审计和验收要求。其他规则沿用 v2.5。
