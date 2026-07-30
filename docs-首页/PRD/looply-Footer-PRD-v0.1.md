# Looply PC Web Footer 跳转 PRD v0.1

## 一、范围

本 PRD 只定义 PC Web Footer 中各入口点击后的跳转目标，不展开目标页面内部逻辑。

Contact Us 由独立 PRD 负责。Newsletter 邮箱提交不属于页面跳转，不在本 PRD 中定义。

## 二、统一规则

- Shop 与 PC 顶导使用同一份固定入口清单，不接运营配置；具体名称、顺序和跳转路径待确认。
- 品牌区仅展示 Logo 和品牌短句，无点击交互。
- Mobile Web / App 不使用本 PRD。

## 三、入口跳转清单

| 区域 | 入口 | 点击后跳转至 | 路径 / 地址 | 打开方式 |
|---|---|---|---|---|
| Support | My Account | 游客进入登录页；登录用户进入个人中心默认页 | `/login`；已登录用户由账户模块重定向 | 当前标签页 |
| Support | Shipping | Shipping 页面 | `/shipping` | 当前标签页 |
| Support | Returns | Returns 页面 | `/returns` | 当前标签页 |
| Support | Contact Us | Contact Us 页面 | `/contact-us` | 当前标签页 |
| About | About Looply | About Us 页面 | `/about-looply` | 当前标签页 |
| About | Authenticity | Authenticity 页面 | `/authenticity` | 当前标签页 |
| Social | Facebook | Looply Facebook | `https://www.facebook.com/share/1CEdkGST1V/?mibextid=wwXIfr` | 新标签页 |
| Social | TikTok | Looply TikTok | `https://www.tiktok.com/@looply_luxury` | 新标签页 |
| Social | Instagram | Looply Instagram | `https://www.instagram.com/looply_luxury/` | 新标签页 |
| Social | YouTube | Looply YouTube | `https://www.youtube.com/@looply_luxury` | 新标签页 |
| Legal | Accessibility Statement | Looply 自建 Accessibility Statement 页面 | `/pages/accessibility-statement` | 当前标签页 |
| Legal | Privacy Policy | Looply 自建 Privacy Policy 页面 | `/pages/privacy-policy` | 当前标签页 |
| Legal | Your Privacy Choices | Your Privacy Choices 独立说明页 | 对应页面正式站内路由 | 当前标签页 |
| Legal | Terms of Service | Looply 自建 Terms of Service 页面 | `/pages/terms-of-service` | 当前标签页 |

Accessibility Statement、Privacy Policy、Terms of Service 均由 Looply 自行开发页面，最终 UI 由 UI 设计提供。页面内容分别参考现有线上版本：

- Accessibility Statement：`https://looply.com/pages/accessibility-statement`
- Privacy Policy：`https://looply.com/pages/privacy-policy`
- Terms of Service：`https://looply.com/pages/terms-of-service`

Your Privacy Choices 的页面 UI 由 UI 设计提供，页面内容以法务最终确认版本为准；页面内部规则见独立的《Looply Your Privacy Choices PRD v0.1》。

## 四、开发实施分类（补充）

本节用于帮助开发区分“只需配置跳转”与“需要先开发目标页面”。入口、路径及打开方式仍以第三节为准。

### 4.1 已有目标，可直接接入跳转

| 入口 | 开发处理 |
|---|---|
| My Account | 接入现有登录 / 个人中心能力，按第三节路径跳转 |
| Facebook | 直接接入已提供的外部地址 |
| TikTok | 直接接入已提供的外部地址 |
| Instagram | 直接接入已提供的外部地址 |
| YouTube | 直接接入已提供的外部地址 |

### 4.2 需要先开发目标页面，再接入跳转

| 入口 | 目标页面开发依据 | Footer 接入条件 |
|---|---|---|
| Shipping | 对应模块提供的独立 PRD / UI | 页面可访问后接入 `/shipping` |
| Returns | 对应模块提供的独立 PRD / UI | 页面可访问后接入 `/returns` |
| Contact Us | 独立《Looply Contact Us PRD v0.1》及对应 UI | 页面可访问后接入 `/contact-us` |
| About Looply | About Us 对应 PRD / UI | 页面可访问后接入 `/about-looply` |
| Authenticity | Authenticity 对应 PRD / UI | 页面可访问后接入 `/authenticity` |
| Accessibility Statement | UI 设计；内容参考现有线上版本 | 自建页面可访问后接入 `/pages/accessibility-statement` |
| Privacy Policy | UI 设计；内容参考现有线上版本 | 自建页面可访问后接入 `/pages/privacy-policy` |
| Terms of Service | UI 设计；内容参考现有线上版本 | 自建页面可访问后接入 `/pages/terms-of-service` |
| Your Privacy Choices | 独立《Looply Your Privacy Choices PRD v0.1》、UI 设计及法务最终文案 | 自建页面及正式站内路由就绪后接入 |

### 4.3 依赖顶导清单确认

Shop 不单独开发 Footer 配置或目标页面。PC 顶导固定入口清单确认后，Footer 使用相同的入口名称、顺序和跳转路径进行接入。
