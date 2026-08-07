# Google Places Autocomplete API (New v1) 完整总结

> **新版变化**：返回结果减少到最多 5 个，更少、更精准，采用 AI 排序。

## 一、整体流程

```
用户输入地址 → Autocomplete（补全建议） → 用户选择 → Place Details（获取结构化地址） → 填入 Looply 表单
```

新版是 **两步调用**，Autocomplete 只返回建议列表，需要再调 Place Details 拿到完整的地址组件。

## 二、Step 1 — Autocomplete（自动补全）

### 请求

```http
POST https://places.googleapis.com/v1/places:autocomplete
```

### 请求头

```http
Content-Type: application/json
X-Goog-Api-Key: YOUR_API_KEY
X-Goog-FieldMask: suggestions.placePrediction.placeId,suggestions.placePrediction.text.text,suggestions.placePrediction.structuredFormat
```

### 请求体

```json
{
  "input": "1600 Amphithea",
  "includedRegionCodes": ["us"],
  "languageCode": "en",
  "includedPrimaryTypes": ["street_address", "subpremise", "premise"],
  "sessionToken": "a1528fgh-29gh-…"
}
```

### 入参字段说明

| 参数 | 类型 | 必填 | Looply 建议值 | 说明 |
| --- | --- | --- | --- | --- |
| `input` | string | ✅ | 用户实时输入 | 搜索文本，逐字符触发 |
| `includedRegionCodes` | string[] | 推荐 | `["us"]` | 限定美国地址，CLDR 区域码 |
| `includedPrimaryTypes` | string[] | 推荐 | `["street_address", "subpremise", "premise"]` | 只返回真实地址，过滤掉餐厅/景点等 |
| `languageCode` | string | 推荐 | `"en"` | 返回英文结果 |
| `sessionToken` | string | 强烈推荐 | UUID | 绑定 autocomplete + details 为一次会话计费，不传则每次按键单独收费 |
| `locationBias` | object | 可选 | — | 软偏向某区域（circle 或 rectangle），不限制结果范围 |
| `locationRestriction` | object | 可选 | — | 硬限制只返回该区域内结果 |
| `origin` | object | 可选 | — | 起点坐标，用于计算 `distanceMeters` |
| `inputOffset` | integer | 可选 | — | 光标位置，用于输入中间插入字符的场景 |

### 响应示例

```json
{
  "suggestions": [
    {
      "placePrediction": {
        "placeId": "ChIJtYuu0V25j4ARwu5e4wwRYgE",
        "text": {
          "text": "1600 Amphitheatre Parkway, Mountain View, CA, USA"
        },
        "structuredFormat": {
          "mainText": {
            "text": "1600 Amphitheatre Parkway"
          },
          "secondaryText": {
            "text": "Mountain View, CA, USA"
          }
        }
      }
    },
    {
      "placePrediction": {
        "placeId": "ChIJkbeSa_BfijkRiXTRNb2Z1tY",
        "text": {
          "text": "1600 Amphitheatre Pkwy, Suite 200, Mountain View, CA, USA"
        },
        "structuredFormat": {
          "mainText": {
            "text": "1600 Amphitheatre Pkwy, Suite 200"
          },
          "secondaryText": {
            "text": "Mountain View, CA, USA"
          }
        }
      }
    },
    {
      "placePrediction": {
        "placeId": "ChIJ2eUgeAK6j4ARbn5u_wAGqWA",
        "text": {
          "text": "160 Amphitheatre Drive, San Jose, CA, USA"
        },
        "structuredFormat": {
          "mainText": {
            "text": "160 Amphitheatre Drive"
          },
          "secondaryText": {
            "text": "San Jose, CA, USA"
          }
        }
      }
    }
  ]
}
```

> 前端下拉渲染时用 `structuredFormat`：主文本加粗/大字，副文本灰色/小字。

### 出参字段说明

| 字段 | 说明 | Looply 用途 |
| --- | --- | --- |
| `suggestions[]` | 建议列表（最多 5 条） | 渲染下拉选项 |
| `.placePrediction` | 地点预测（另有 `queryPrediction` 是搜索词建议，忽略即可） | — |
| `.placeId` | 地点唯一 ID | 传给 Step 2 获取详细地址 |
| `.text.text` | 完整地址文本 | 下拉列表显示文本 |
| `.text.matches[]` | 用户输入匹配的高亮位置 | 下拉列表加粗匹配部分 |
| `.structuredFormat.mainText` | 主要文本（街道地址） | 下拉列表第一行 |
| `.structuredFormat.secondaryText` | 次要文本（城市/州） | 下拉列表第二行 |
| `.types` | 地点类型标签 | 可用于筛选过滤 |
| `.distanceMeters` | 距 `origin` 的距离 | Looply 暂不需要 |

## 三、Step 2 — Place Details（获取结构化地址）

用户从下拉选择后，用 `placeId` 获取完整地址组件。

### 请求

```http
GET https://places.googleapis.com/v1/places/ChIJtYuu0V25j4ARwu5e4wwRYgE
```

### 请求头

```http
X-Goog-Api-Key: YOUR_API_KEY
X-Goog-FieldMask: addressComponents,formattedAddress
```

> ⚠️ `X-Goog-FieldMask` 必填，不传报错。只取需要的字段，按字段 SKU 计费。Looply 地址场景只需 `addressComponents,formattedAddress`。

### 响应示例

```json
{
  "formattedAddress": "1600 Amphitheatre Parkway, Mountain View, CA 94043, USA",
  "addressComponents": [
    {
      "longText": "1600",
      "shortText": "1600",
      "types": ["street_number"],
      "languageCode": "en"
    },
    {
      "longText": "Amphitheatre Parkway",
      "shortText": "Amphitheatre Pkwy",
      "types": ["route"],
      "languageCode": "en"
    },
    {
      "longText": "Mountain View",
      "shortText": "Mountain View",
      "types": ["locality", "political"],
      "languageCode": "en"
    },
    {
      "longText": "Santa Clara County",
      "shortText": "Santa Clara County",
      "types": ["administrative_area_level_2", "political"],
      "languageCode": "en"
    },
    {
      "longText": "California",
      "shortText": "CA",
      "types": ["administrative_area_level_1", "political"],
      "languageCode": "en"
    },
    {
      "longText": "United States",
      "shortText": "US",
      "types": ["country", "political"],
      "languageCode": "en"
    },
    {
      "longText": "94043",
      "shortText": "94043",
      "types": ["postal_code"],
      "languageCode": "en"
    },
    {
      "longText": "1234",
      "shortText": "1234",
      "types": ["postal_code_suffix"],
      "languageCode": "en"
    }
  ]
}
```

### addressComponents 各组件类型说明

| `types` 值 | 含义 | 取值方式 | 示例 |
| --- | --- | --- | --- |
| `street_number` | 门牌号 | shortText | `"1600"` |
| `route` | 街道名 | shortText（缩写）或 longText（全称） | `"Amphitheatre Pkwy"` / `"Amphitheatre Parkway"` |
| `subpremise` | 子单元（公寓/套房号） | shortText | `"Apt 4B"` |
| `locality` | 城市 | longText | `"Mountain View"` |
| `sublocality_level_1` | 子区域（NYC 五个区等） | longText | `"Manhattan"`（NYC 没有 locality，回退到此字段） |
| `administrative_area_level_1` | 州 | shortText | `"CA"` |
| `administrative_area_level_2` | 县 | longText | `"Santa Clara County"`（Looply 不需要） |
| `country` | 国家 | shortText | `"US"` |
| `postal_code` | 邮编（5位） | shortText | `"94043"` |
| `postal_code_suffix` | 邮编后缀（+4） | shortText | `"1234"`（有时不返回） |

## 四、Google → Looply 字段映射

```
Google addressComponents                    Looply 字段
─────────────────────────────              ─────────────
street_number.shortText + " "              ─┐
  + route.shortText                         ├→ address_line1
                                           ─┘

subpremise.shortText                       ──→ address_line2
                                               （无则留空，有则加 "Apt " 前缀）

locality.longText                          ──→ city
  ↓ 回退
sublocality_level_1.longText                   （NYC 等特殊城市）

administrative_area_level_1.shortText      ──→ state（两位缩写如 "CA"）

postal_code.shortText                      ─┐
  + "-" + postal_code_suffix.shortText      ├→ postal_code
  （suffix 有则拼，无则只用5位）             ─┘

country.shortText                          ──→ country_code（固定 "US"）

first_name / last_name                     ──→ Google 不返回，用户手动填写
phone                                      ──→ Google 不返回，用户手动填写
```
