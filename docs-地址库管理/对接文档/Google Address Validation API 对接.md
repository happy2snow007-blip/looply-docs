# Google Address Validation API 对接

## 一、API 概览

| 维度 | 说明 |
| --- | --- |
| 端点 | `POST https://addressvalidation.googleapis.com/v1:validateAddress` |
| 认证 | `X-Goog-Api-Key` 请求头 |
| 用途 | 验证地址可投递性、标准化地址格式、返回组件级确认状态 |
| 适用场景 | 每次新增或编辑美国地址、且本地硬校验通过后，在保存前调用；不在输入过程中实时调用 |

## 二、请求结构

```http
POST https://addressvalidation.googleapis.com/v1:validateAddress
Content-Type: application/json
X-Goog-Api-Key: YOUR_API_KEY

{
  "address": {
    "regionCode": "US",
    "locality": "Mountain View",
    "administrativeArea": "CA",
    "postalCode": "94043",
    "addressLines": ["1600 Amphitheatre Pkwy"]
  },
  "enableUspsCass": true
}
```

### 请求参数说明

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `address.regionCode` | string | ✅ | ISO 3166-1 alpha-2 国家码，Looply 固定 `"US"` |
| `address.locality` | string | 否 | 城市 |
| `address.administrativeArea` | string | 否 | 州（如 `"CA"`） |
| `address.postalCode` | string | 否 | 邮编 |
| `address.addressLines` | string[] | ✅ | 地址行数组，可传 1-2 行 |
| `enableUspsCass` | boolean | 否 | 设为 `true` 启用 USPS CASS 验证（美国地址强烈建议开启） |

### Looply 传参映射

```javascript
function buildValidationRequest(looplyAddress) {
  return {
    address: {
      regionCode: 'US',
      locality: looplyAddress.city,
      administrativeArea: looplyAddress.state,
      postalCode: looplyAddress.postal_code,
      addressLines: [
        looplyAddress.address_line1,
        looplyAddress.address_line2,
      ].filter(Boolean),
    },
    enableUspsCass: true,
  };
}
```

## 三、响应结构

```json
{
  "result": {
    "verdict": {
      "inputGranularity": "PREMISE",
      "validationGranularity": "PREMISE",
      "geocodeGranularity": "PREMISE",
      "addressComplete": true,
      "hasUnconfirmedComponents": false,
      "hasInferredComponents": false,
      "hasReplacedComponents": false
    },
    "address": {
      "formattedAddress": "1600 Amphitheatre Parkway, Mountain View, CA 94043-1351, USA",
      "postalAddress": {
        "regionCode": "US",
        "postalCode": "94043-1351",
        "administrativeArea": "CA",
        "locality": "Mountain View",
        "addressLines": ["1600 Amphitheatre Pkwy"]
      },
      "addressComponents": [
        {
          "componentName": { "text": "1600", "languageCode": "en" },
          "componentType": "street_number",
          "confirmationLevel": "CONFIRMED"
        },
        {
          "componentName": { "text": "Amphitheatre Parkway", "languageCode": "en" },
          "componentType": "route",
          "confirmationLevel": "CONFIRMED"
        },
        {
          "componentName": { "text": "Mountain View", "languageCode": "en" },
          "componentType": "locality",
          "confirmationLevel": "CONFIRMED"
        },
        {
          "componentName": { "text": "CA", "languageCode": "en" },
          "componentType": "administrative_area_level_1",
          "confirmationLevel": "CONFIRMED"
        },
        {
          "componentName": { "text": "94043-1351", "languageCode": "en" },
          "componentType": "postal_code",
          "confirmationLevel": "CONFIRMED"
        }
      ]
    },
    "geocode": {
      "location": { "latitude": 37.4220656, "longitude": -122.0840897 },
      "plusCode": { "globalCode": "849VCWC8+W5" }
    },
    "metadata": {
      "business": false,
      "residential": true,
      "poBox": false
    },
    "uspsData": {
      "standardizedAddress": {
        "firstAddressLine": "1600 AMPHITHEATRE PKWY",
        "cityStateZipAddressLine": "MOUNTAIN VIEW CA 94043-1351"
      },
      "dpvConfirmation": "Y",
      "dpvFootnote": "AABB",
      "postOfficeCity": "MOUNTAIN VIEW",
      "postOfficeState": "CA"
    }
  },
  "responseId": "uuid-xxx-xxx"
}
```

## 四、Looply 处理场景决策树

Google 官方建议将验证结果分为三类动作：**Accept（接受）**、**Confirm（确认）**、**Fix（修正）**。以下是 Looply 的具体处理方案：

| possibleNextAction | 示例场景 | 核心读取字段 | 前端路由 | 是否阻断保存 |
| --- | --- | --- | --- | --- |
| ACCEPT | 地址完全正确 | `formattedAddress` | 静默保存 | 否 |
| CONFIRM | 拼写纠错 / ZIP+4 补全 | `hasReplacedComponents`, `addressComponents[].replaced` | Page 12 对比弹窗 | 否（选择后保存） |
| CONFIRM_ADD_SUBPREMISES | 多单元建筑缺 Apt | `dpvConfirmation: "D"` | Page 14 Apt 提示 | 否 |
| FIX | 街道/城市不存在 | `hasUnconfirmedComponents`, `unconfirmedComponentTypes` | Page 13 Inline error | 阻断 |

### 四种 possibleNextAction 场景映射示例

#### 1. ACCEPT — 自动通过

用户输入：

```
1600 Amphitheatre Pkwy, Mountain View, CA 94043
```

API 关键返回：

```json
{
  "verdict": {
    "possibleNextAction": "ACCEPT",
    "validationGranularity": "PREMISE",
    "hasReplacedComponents": false,
    "hasInferredComponents": false,
    "hasUnconfirmedComponents": false
  },
  "address": {
    "formattedAddress": "1600 Amphitheatre Pkwy, Mountain View, CA 94043, USA"
  },
  "uspsData": {
    "dpvConfirmation": "Y"
  }
}
```

前端行为：静默保存，Toast `"Address saved"`，无弹窗。

#### 2. CONFIRM — 展示建议地址让用户确认

用户输入：

```
123 Main Stret, New York, NY 10001
```

（Street 拼错为 Stret，ZIP 缺少 +4）

API 关键返回：

```json
{
  "verdict": {
    "possibleNextAction": "CONFIRM",
    "validationGranularity": "PREMISE",
    "hasReplacedComponents": true,
    "hasInferredComponents": true,
    "hasUnconfirmedComponents": false
  },
  "address": {
    "formattedAddress": "123 Main Street, New York, NY 10001-2345, USA",
    "addressComponents": [
      { "componentName": { "text": "Street" }, "componentType": "route", "replaced": true },
      { "componentName": { "text": "10001-2345" }, "componentType": "postal_code", "inferred": true }
    ]
  }
}
```

前端行为（Page 12）：

```
┌─ You entered ──────────┐  ┌─ Suggested ─────────────┐
│ ○                       │  │ ●                        │
│ 123 Main Stret          │  │ 123 Main [Street]        │
│ New York, NY            │  │ New York, NY             │
│ 10001                   │  │ [10001-2345]             │
└─────────────────────────┘  └──────────────────────────┘
         [] = 差异高亮 (标红)
```

#### 3. CONFIRM_ADD_SUBPREMISES — 提醒补充 Apt/Unit

用户输入：

```
350 5th Ave, New York, NY 10118
```

（帝国大厦地址，多单元建筑，未填 Suite/Floor）

API 关键返回：

```json
{
  "verdict": {
    "possibleNextAction": "CONFIRM_ADD_SUBPREMISES",
    "validationGranularity": "PREMISE",
    "hasReplacedComponents": false,
    "hasUnconfirmedComponents": false
  },
  "address": {
    "formattedAddress": "350 5th Ave, New York, NY 10118, USA"
  },
  "uspsData": {
    "dpvConfirmation": "D"
  }
}
```

前端行为（Page 14）：

```
┌─────────────────────────────────────────┐
│ ℹ️ This address may need an apartment   │
│    or suite number.                     │
└─────────────────────────────────────────┘

[Street Address] "350 5th Ave"          ← 正常
[Apt / Suite / Unit] ""                 ← 紫色边框高亮 ($border-focus)
                     "Add Apt/Suite for faster delivery"

─────────────────────────────────────────
[Save Address] (Primary)                ← 不阻断，允许直接保存
```

#### 4. FIX — 阻止继续并要求修改

用户输入：

```
999 Nonexistent Blvd, Faketown, NY 10001
```

（街道和城市都不存在）

API 关键返回：

```json
{
  "verdict": {
    "possibleNextAction": "FIX",
    "validationGranularity": "OTHER",
    "hasReplacedComponents": false,
    "hasUnconfirmedComponents": true
  },
  "address": {
    "formattedAddress": "999 Nonexistent Blvd, Faketown, NY 10001, USA",
    "unconfirmedComponentTypes": ["street_number", "route", "locality"],
    "addressComponents": [
      { "componentName": { "text": "999" }, "componentType": "street_number", "confirmationLevel": "UNCONFIRMED_BUT_PLAUSIBLE" },
      { "componentName": { "text": "Nonexistent Blvd" }, "componentType": "route", "confirmationLevel": "UNCONFIRMED_AND_SUSPICIOUS" },
      { "componentName": { "text": "Faketown" }, "componentType": "locality", "confirmationLevel": "UNCONFIRMED_AND_SUSPICIOUS" }
    ]
  }
}
```

前端行为（Page 13）：

```
┌─────────────────────────────────────────┐
│ ⚠️ We couldn't verify this address.     │
│    Please check the highlighted fields. │
└─────────────────────────────────────────┘

[Street Address] "999 Nonexistent Blvd"   ← 红色边框
  "We couldn't verify this address."

[City] "Faketown"                          ← 红色边框
  "We couldn't verify this address."

[State] "NY"                               ← 正常（已确认）
[ZIP] "10001"                              ← 正常（已确认）

─────────────────────────────────────────
[Save Address] (Primary，保持不可提交；用户修改问题字段后重新触发 Validation)
```

> `FIX` 为硬拦截：不得提供 `Save as entered`、二次确认或任何覆盖保存入口；不得创建/更新地址，也不得记录 `user_overridden`。用户修改红框字段后，必须重新调用 Validation，只有结果不再为 `FIX` 才可继续保存。

## 五、配送限制边界

PO Box、APO/FPO/DPO 及自定义限制不属于 Address Validation 的全局拦截规则。地址保存阶段不做配送限制校验；仅在结算页，按购物车商品所属商家已启用的固定/自定义配送限制规则校验并拦截。详细规则及面向用户的配送提示以《地址库管理 PRD》2.1.7 为唯一来源。

## 六、地址需要 Fix 时的组合，以及文案

| Google component / 场景 | Looply UI字段 | 推荐提示文案 | 类型 | 是否建议拦截 |
| --- | --- | --- | --- | --- |
| street_number unconfirmed | Address Line 1 | We couldn't verify this address. | 错误 | FIX 时硬拦截 |
| route unconfirmed | Address Line 1 | We couldn't verify this address. | 错误 | FIX 时硬拦截 |
| street_number + route 同时异常 | Address Line 1 | We couldn't verify this address. | 错误 | FIX 时硬拦截 |
| postal_code unconfirmed | ZIP Code | We couldn't verify this address. | 错误 | FIX 时硬拦截 |
| postal_code mismatch | ZIP Code | We couldn't verify this address. | 错误 | FIX 时硬拦截 |
| locality unconfirmed | City | We couldn't verify this address. | 错误 | FIX 时硬拦截 |
| administrative_area_level_1 unconfirmed | State | We couldn't verify this address. | 错误 | FIX 时硬拦截 |

文案展示规则：顶部保留通用警告 `We couldn't verify this address. Please check the highlighted fields.`；每个命中 `unconfirmedComponentTypes` 的可定位字段均使用红色边框，且在字段下方展示统一文案 `We couldn't verify this address.`。前端不得硬编码该英文，使用 i18n key 由翻译中心提供 market 当前启用语言的译文；英文为基准。

## 七、计费与调用时机建议

| 建议 | 说明 |
| --- | --- |
| 调用时机 | 每次新增或编辑地址保存时调用，不要在输入过程中实时调用；地址字段发生修改后需重新验证；仅在地址未变且已有非 FIX 验证结果时可复用结果 |
| 与 Autocomplete 配合 | Autocomplete 选中的地址通常质量高，但仍需 Validation 确认可投递性 |
| enableUspsCass | 美国地址必须开启，获取 `dpvConfirmation` 是判断可投递性的核心依据 |
| 缓存 | 同一地址短时间内不重复调用（如用户确认后再次提交） |
| 费用 | 约 $0.017/次（按量计费），比退货/重发成本低得多 |

## 八、恶意拦截

| 规则 | 参数 | 触发后行为 |
| --- | --- | --- |
| Autocomplete 防抖 | 400ms | 前端控制，无感知 |
| Autocomplete 单会话上限 | 50 次 | 静默停止，允许手动输入 |
| 单账号/IP/设备，新增地址每日上限 | 10 次/天 | 超过后展示 reCAPTCHA；验证通过可继续当前新增操作 |
| 单账号/IP/设备，修改地址每日上限 | 10 次/天 | 超过后展示 reCAPTCHA；验证通过可继续当前修改操作 |
