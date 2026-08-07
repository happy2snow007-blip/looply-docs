# Looply 地址校验规则 V1.2（美国本地校验）

**适用范围**：美国地址新增、编辑

**来源**：`Looply地址校验规则V1.2-美国本地校验.xlsx` · 工作表「美国本地校验」

| 字段 | 校验维度 | 规则描述 | 拦截类型 | 触发时机 | 提示文案（英文） | 提示文案（中文参考） | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| first_name | 必填 | 必填 | 硬拦截 | 失焦 | First name is required | 请输入名字 | — |
| first_name | 长度 | 1–50 字符 | 硬拦截 | 失焦 | First name must be between 1 and 50 characters | 名字长度需在 1–50 个字符之间 | — |
| first_name | 字符集 | 英文字母、扩展拉丁字符、空格、连字符、撇号 | 硬拦截 | 失焦 | First name contains invalid characters | 名字包含无效字符 | — |
| last_name | 必填 | 必填 | 硬拦截 | 失焦 | Last name is required | 请输入姓氏 | — |
| last_name | 长度 | 1–50 字符 | 硬拦截 | 失焦 | Last name must be between 1 and 50 characters | 姓氏长度需在 1–50 个字符之间 | — |
| last_name | 字符集 | 英文字母、扩展拉丁字符、空格、连字符、撇号 | 硬拦截 | 失焦 | Last name contains invalid characters | 姓氏包含无效字符 | — |
| phone | 必填 | 必填；表单固定展示 +1 前缀 | 硬拦截 | 失焦 | Phone number is required | 请输入电话号码 | — |
| phone | 格式 | 去除格式符后为 10 位数字 | 硬拦截 | 失焦 | Please enter a valid 10-digit US phone number | 请输入有效的 10 位美国电话号码 | — |
| phone | 区号 | 区号首位为 2–9 | 硬拦截 | 失焦 | Invalid US phone format | 美国电话号码格式无效 | — |
| address_line1 | 必填 | 必填 | 硬拦截 | 提交 | Street address is required | 请输入街道地址 | — |
| address_line1 | 长度 | 1–100 字符 | 硬拦截 | 提交 | Address must be between 1 and 100 characters | 地址长度需在 1–100 个字符之间 | — |
| address_line1 | 字符集 | 字母、数字、扩展拉丁字符及常用地址标点 | 硬拦截 | 提交 | Address contains invalid characters | 地址包含无效字符 | 禁止 HTML 标签、注入字符组合和路径遍历模式 |
| address_line2 | 必填 | 选填 | — | — | — | — | — |
| address_line2 | 长度 | 0–100 字符 | 硬拦截 | 提交 | Address must be 100 characters or less | 公寓、套房或单元号不超过 100 个字符 | — |
| address_line2 | 字符集 | 同 address_line1 | 硬拦截 | 提交 | Address contains invalid characters | 地址包含无效字符 | — |
| city | 必填 | 必填 | 硬拦截 | 提交 | City is required | 请输入城市 | — |
| city | 长度 | 1–50 字符 | 硬拦截 | 提交 | City must be between 1 and 50 characters | 城市长度需在 1–50 个字符之间 | — |
| city | 字符集 | 英文字母、扩展拉丁字符、空格、连字符、撇号 | 硬拦截 | 提交 | City name contains invalid characters | 城市名称包含无效字符 | — |
| city | ZIP联动（建议） | ZIP 反查建议城市；仅映射库存在唯一可信城市时展示 | 软提示 | City 或 ZIP 失焦 | This city doesn't match the ZIP code. Did you mean {suggested_city}? | 城市与邮编不匹配，建议填写 {suggested_city} | 不自动回填、不阻止保存；使用独立、经数据验收的 ZIP→城市数据源 |
| state_province | 必填 | 必填，下拉选择 | 硬拦截 | 提交 | State is required | 请选择州 | 页面显示名为 State |
| state_province | 枚举范围 | 美国 50 州 + DC | 硬拦截 | 提交 | Invalid state code | 州代码无效 | 下拉数据来自已启用的行政区划 |
| state_province | State↔ZIP | 使用 postal_code_mapping 检查 ZIP 与所选 State 的映射关系；不一致时仅提示 | 软提示 | State 或 ZIP 失焦、提交 | Please double-check that the ZIP Code matches the selected state. | 请再次确认 ZIP Code 是否与所选 State 匹配。 | State 与 ZIP 标为黄色提示态；适用于手动输入、浏览器原生填充和 Autocomplete 回填后的最终字段值；不自动修改、不阻止保存；映射表导入期间不提示 |
| postal_code | 必填 | 必填 | 硬拦截 | 失焦 | ZIP code is required | 请输入邮编 | — |
| postal_code | 格式 | 5 位数字或 ZIP+4（如 94102 或 94102-1234） | 硬拦截 | 失焦 | Invalid ZIP Code format | 邮编格式无效 | — |
