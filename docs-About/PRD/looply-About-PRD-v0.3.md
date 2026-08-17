# Looply About 页面 PRD v0.3

> 模块：About Looply
>
> 版本：v0.3
>
> 日期：2026-08-17
>
> 状态：基于最新 PC / Mobile UI 稿、2026-08-07 Authentication 参考截图及 2026-08-17 Who We Are UI 截图的当前工作稿

## 一、概述

### 1.1 背景与目标

About 页面帮助用户在浏览商品前理解 Looply 的品牌定位、循环理念、平台体验标准及鉴定能力，并通过两个明确入口继续浏览：了解鉴定方式或进入首页 For You。

当前版本面向游客与登录用户展示同一页面内容，不依赖登录态。

### 1.2 当前版本范围

1. 提供 Web PC 与 Mobile About 页面。
2. 展示品牌定位、Slogan、品牌故事、三项信念、五项平台体验与鉴定说明。
3. 提供鉴定页和首页 For You 两个页面跳转入口。
4. 复用全站 Header、Footer、语言选择、搜索、账户、收藏和购物袋公共组件。

### 1.3 用户角色与核心场景

| 用户角色 | 核心场景 | 页面结果 |
|---|---|---|
| 游客 | 通过 Footer 或外部落地页进入 About，判断平台是否可信 | 了解品牌与鉴定能力，进入 Authentication 或 Home For You |
| 登录用户 | 购物前了解平台规则与品牌定位 | 阅读页面并继续浏览 For You |

### 1.4 全局页面流转

`Home / Footer About Looply → About Looply → Authentication`

`Home / Footer About Looply → About Looply → Home / For You`

`Mobile 上一级页面 → About Looply → 返回上一级页面`

当 Mobile 端不存在可返回的上一级页面时，返回按钮进入 Home / For You。

### 1.5 术语说明

| 术语 | 含义 |
|---|---|
| For You | 首页中面向用户推荐商品的内容视图 |
| Authentication 页面 | 独立展示鉴定流程、规则与保障口径的页面 |
| About 页面 | 面向用户说明 Looply 品牌定位、理念与信任基础的介绍页 |

### 1.6 输入源与覆盖结论

| 输入源 | 用途 | 结论 |
|---|---|---|
| PC UI 截图 `img_v3_02149_501c101d-c208-460e-b101-11b1ae55d40g.png` | PC 布局与展示内容基线 | 已覆盖 |
| Mobile UI 截图 `img_v3_02149_a4236bac-a454-4c54-81bf-28f591dceefg.png` | Mobile 布局与交互基线 | 已覆盖 |
| 用户于 2026-08-07 提供的 Authentication UI 截图 | Authentication 正文分段基线 | 已覆盖：首句单独成段，其余正文为第二段 |
| 用户于 2026-08-17 提供的 Who We Are UI 截图 | Who We Are 的 PC 端展示顺序与视觉层级基线 | 已覆盖；Mobile 复用相同内容顺序 |
| 已确认 About 英文文案 | 模块正文口径 | 已覆盖 |
| `docs/research/about-us/looply-About-Looply-竞品调研-v0.1.md` | 页面信息层级参考 | 已覆盖 |
| 产品架构图、系统流程图、ER 图 | 本模块无新增业务实体或跨页面业务流程 | 本版本不涉及 |

PC UI 的 `Who We Are` 与 Mobile UI 的 `Who we are` 统一为 `Who We Are`。三项信念统一为 `Personal Style`、`Trust`、`Never Secondary`；PC 与 Mobile 使用相同标题及正文。

## 二、需求详细描述

### 2.1 About 页面【页面型】

#### 2.1.1 功能描述

系统按固定顺序展示 About 内容模块：Hero、Who We Are、What We Believe、What You'll Find on Looply、Why Our Authentication Stands Apart、Shop with Confidence 和 Footer。

#### 2.1.2 页面布局

| 模块 | PC 端 | Mobile 端 |
|---|---|---|
| 顶部导航 | 复用 Web 全局 Header，展示 Logo、语言选择、类目导航及公共功能图标 | 复用 Mobile 顶部栏，展示返回按钮与居中标题 `About Us` |
| Hero | 横向大图；图片中央叠加定位与 Slogan | 横向圆角图片；图片内叠加定位与 Slogan |
| Who We Are | 居中标题；开篇引言、分隔线、三段主体正文与居中收束句按视觉层级展示 | 使用与 PC 相同的内容顺序；具体字号和留白按 Mobile 设计稿适配 |
| What We Believe | 三列卡片，同时展示图片、标题和正文 | 三张纵向卡片，单卡顺序为图片、标题、正文 |
| What You'll Find | 左侧五条编号清单，右侧展示配图 | 标题下展示五条编号清单 |
| Authentication | 左图右文；标题、正文、收束句与文字链接位于右侧 | 标题、图片、正文、收束句与文字链接自上而下排列 |
| Shop with Confidence | 全宽背景图；居中标题与主按钮 | 全宽背景图；居中标题与主按钮 |
| Footer | 复用 Web Footer | 复用 Mobile Footer；当前 UI 未展示时由公共组件规则决定 |

#### 2.1.3 内容与展示规则

##### Hero

| 内容项 | 展示值 |
|---|---|
| 定位 | `Authenticated Luxury Resale` |
| Slogan | `Designer pieces deserve another chapter.` |
| 图片 | 使用已发布的 About Hero 图片；图片上叠加深色遮罩以保证文字可读 |

##### Who We Are

标题展示 `Who We Are`。正文以固定视觉层级展示，英文文案保持以下内容与顺序：

1. 开篇引言：居中、斜体展示 `A loop is never just a return—it is the beginning of a new chapter.`
2. 分隔线：展示于开篇引言之后、主体正文之前。
3. 主体正文：左对齐依次展示：
   - `At Looply, we believe that beautifully made pieces should not be confined to a single chapter. The pieces we cherish—the ones shaped by craftsmanship and intention—deserve to be rediscovered, reinterpreted, and passed on, gathering meaning as they move from one life to another.`
   - `Looply exists to make that movement feel effortless. Through careful curation and rigorous authentication, we replace the uncertainty long associated with resale with confidence, clarity, and ease.`
   - `Based in Los Angeles, Looply was founded in 2026 to bring this belief to life—creating a more trusted and considered way for exceptional pieces to continue their stories.`
4. 收束句：主体正文之后居中、斜体展示 `Here, designer pieces don’t simply change hands—their stories, beauty, and significance live on.`

##### What We Believe

三张卡片按固定顺序展示；卡片不触发页面跳转。

| 顺序 | 标题 | 正文 | 图片 |
|---|---|---|---|
| 1 | `Personal Style` | `That resale is more than a conscious choice—it is a modern expression of personal style: considered, confident, and distinctly your own.` | 已发布的个人风格主题图片 |
| 2 | `Trust` | `That trust should come standard. Through rigorous authentication and clear condition details, we help you understand every piece and choose with confidence.` | 已发布的信任主题图片 |
| 3 | `Never Secondary` | `That secondhand should never feel secondary. Every part of the experience should reflect the same commitment to care, clarity, and ease.` | 已发布的二手体验主题图片 |

##### What You'll Find on Looply

标题展示 `What You'll Find on Looply`。清单按编号 01 至 05 展示：

| 编号 | 文案 |
|---|---|
| 01 | `Pieces from the world’s most sought-after luxury brands` |
| 02 | `A clear and detailed presentation of condition and craftsmanship` |
| 03 | `Exacting standards of authentication and condition grading` |
| 04 | `Pricing that reflects condition, value, and rarity` |
| 05 | `An experience designed to feel assured, from first glance to final delivery` |

PC 端与该清单并列展示体验主题图片；Mobile 端仅展示标题与清单。

##### Why Our Authentication Stands Apart

标题展示 `Why Our Authentication Stands Apart`，正文按以下两段依次展示：

1. `Every item offered on Looply undergoes a dual authentication process combining expert human review with our proprietary AI technology.`
2. `Our authentication specialists draw on collective experience gained through the inspection and authentication of more than 1.28 million items—expertise that has helped shape and refine the rigorous methods now applied at Looply. By combining human discernment and judgment with the speed, consistency, and precision of AI, this approach allows us to stand behind every eligible item with the Looply Lifetime Authenticity Guarantee.`

收束句展示：

`Because confidence, like style, should feel effortless.`

文字链接展示 `Explore Our Authentication Process`。

##### Shop with Confidence

全宽背景图上展示标题 `Shop with Confidence` 和按钮 `Discover More`。该模块位于 Authentication 模块之后、Footer 之前。

#### 2.1.4 操作流程

| 用户操作 | 触发位置 | 系统结果 |
|---|---|---|
| 点击返回 | Mobile 顶部左侧 | 返回上一级页面；无上一级页面时进入 Home / For You |
| 点击鉴定入口 | `Explore Our Authentication Process` | 进入独立 Authentication 页面 |
| 点击发现更多 | `Discover More` | 进入 Home / For You |
| 点击共享 Header / Footer 链接 | 公共组件 | 按公共组件定义执行对应跳转 |

#### 2.1.5 页面状态与异常处理

| 场景 | 页面构成 | 处理规则 |
|---|---|---|
| 默认态 | 全部文本、图片、CTA 和公共组件 | 按 UI 稿顺序展示 |
| 单张内容图片加载中 | 文本与其余模块正常展示；图片区域展示与原图容器等比例的中性色骨架 | 图片加载完成后替换为正式图片 |
| 单张内容图片加载失败 | 文本与 CTA 正常展示；图片区域展示中性品牌底色 | 用户刷新页面后重新请求图片 |
| Authentication 页面不可达 | About 页内容保持可读 | 跳转目标页按其页面级异常规则处理 |
| Home / For You 不可达 | About 页内容保持可读 | 跳转目标页按其页面级异常规则处理 |

#### 2.1.6 UI 关联

| 终端 | 设计稿 |
|---|---|
| PC | `img_v3_02149_501c101d-c208-460e-b101-11b1ae55d40g.png`；Who We Are 以用户于 2026-08-17 提供的截图为最新基线 |
| Mobile | `/Users/zz/Desktop/img_v3_02149_a4236bac-a454-4c54-81bf-28f591dceefg.png` |

### 2.2 公共 Header 与 Footer【公共组件引用】

About 页面接入既有 Web / Mobile Header 与 Footer。Header 中类目导航、语言选择、搜索、账户、收藏、购物袋；Footer 中导航、订阅、支付与物流信息均按各自公共组件 PRD 实现。

本页面只定义 About 内容区和两个页面内 CTA；不重复定义公共组件的字段、校验和异常规则。

## 三、多语言、数据与埋点

### 3.1 多语言归属

| 内容类别 | 内容 | 归属与稳定标识 | 缺失译文兜底 |
|---|---|---|---|
| 动态业务内容 | Hero 定位与 Slogan、Who We Are 正文、三张信念卡片、五条体验清单、鉴定正文与收束句、转化区标题 | 新建翻译资源卡片 `brand_about_page`；`domain=brand`；`domainName=Looply`；字段见下表 | 展示英文源文案 |
| 静态 UI 文案 | `About Us`、`Explore Our Authentication Process`、`Discover More` | message package：`about.title`、`about.authentication_cta`、`about.discover_more_cta` | 展示英文默认文案 |
| 不翻译 | Logo、图标、编号 `01` 至 `05`、图片本体 | 不接入翻译 | 不适用 |

`brand_about_page` 字段：

| fieldName | 展示面 |
|---|---|
| `positioning` | Hero |
| `slogan` | Hero |
| `who_we_are_title` | Who We Are |
| `who_we_are_paragraph_1` 至 `who_we_are_paragraph_5` | Who We Are；展示顺序固定为 `1 → 2 → 3 → 5 → 4`，其中 `1` 与 `4` 使用引言 / 收束句样式 |
| `beliefs_title` | What We Believe |
| `belief_1_title` 至 `belief_3_title` | What We Believe |
| `belief_1_body` 至 `belief_3_body` | What We Believe |
| `find_title` | What You'll Find on Looply |
| `find_item_1` 至 `find_item_5` | What You'll Find on Looply |
| `authentication_title` | Authentication |
| `authentication_body_1` | Authentication 第一段正文 |
| `authentication_body_2` | Authentication 第二段正文 |
| `authentication_closing` | Authentication |
| `shop_confidence_title` | Shop with Confidence |

### 3.2 埋点

| 事件名 | 触发时机 | 必填属性 |
|---|---|---|
| `about_page_view` | About 页面首屏成功展示 | `page_surface`、`locale`、`entry_source` |
| `about_authentication_cta_click` | 点击鉴定入口 | `page_surface`、`locale`、`cta_name=authentication_process` |
| `about_for_you_cta_click` | 点击 Discover More | `page_surface`、`locale`、`cta_name=discover_more` |
| `about_mobile_back_click` | Mobile 点击返回 | `locale`、`has_history` |

`page_surface` 枚举：

| 枚举值 | 含义 | 触发时机 | 记录内容 / 适用场景 |
|---|---|---|---|
| `web_pc` | Web PC 页面 | 页面访问与 CTA 点击 | PC 布局访问 |
| `web_mobile` | Web Mobile 页面 | 页面访问与 CTA 点击 | Mobile 布局访问 |

## 四、依赖与风险

| 依赖项 | 关键要求 |
|---|---|
| Home / For You | 提供稳定的首页 For You 页面入口，供 `Discover More` 跳转 |
| Authentication 页面 | 提供独立可访问页面，承接鉴定流程、保障适用范围和详情说明 |
| Header / Footer 公共组件 | 提供与当前 Web / Mobile UI 一致的导航与页脚能力 |
| 图片与 CDN | 提供已授权的 Hero、三项信念、体验、鉴定和底部转化区图片，并支持按终端裁切 |
| 翻译中心 | 支持 `brand_about_page` 资源卡片与英文缺失兜底 |
| 品牌与法务口径 | 在发布前核验 `Los Angeles`、`founded in 2026`、`1.28 million items`、AI 鉴定及 `Lifetime Authenticity Guarantee` 的证明材料、适用范围和用户可见条款 |

## 五、版本规划

### 5.1 当前版本 v0.3

包含完整 About 展示、PC / Mobile 自适应布局、Authentication 跳转、For You 跳转、图片加载降级、多语言资源定义和基础埋点。

### 5.2 后续迭代方向

本版本不定义后续扩展范围。新增品牌故事、内容管理能力或新的转化入口时，另行确认并进入后续版本。

## 六、附录

### 6.1 设计稿索引

| 页面 | PC UI | Mobile UI |
|---|---|---|
| About Looply | `img_v3_02149_501c101d-c208-460e-b101-11b1ae55d40g.png`；Who We Are 以 2026-08-17 用户截图为最新基线 | `img_v3_02149_a4236bac-a454-4c54-81bf-28f591dceefg.png` |

### 6.2 字段级 UI 对照

| 模块 | PRD 定义 | PC UI | Mobile UI | 结论 |
|---|---|---|---|---|
| Hero | 定位 + Slogan + 图片 | 一致 | 一致 | 已对齐 |
| Who We Are | 标题、居中斜体开篇引言、分隔线、三段左对齐主体正文、居中斜体收束句；顺序 `1 → 2 → 3 → 5 → 4` | 已按 2026-08-17 最新截图更新 | 使用相同文案与顺序；新截图未覆盖 Mobile 的字号与留白 | PC 已对齐；Mobile 需按本内容顺序完成视觉适配 |
| What We Believe | 3 张图片卡片；统一标题和正文 | 卡片 2 标题展示 `Trust` | Mobile 使用相同标题与正文 | 已按最新确认文案更新 PRD；UI 如仍为旧标题需同步 |
| What You'll Find | 标题 + 5 项编号清单；PC 右图、Mobile 无图 | 一致 | 一致 | 已对齐 |
| Authentication | 图片、标题、两段正文、收束句、CTA | 最新截图将首句单独成段，其余正文为第二段 | Mobile 使用相同两段正文顺序 | PRD 已按最新截图更新；Demo v0.2 的单段正文需同步 |
| Shop with Confidence | 标题 + Discover More 跳转 For You | 一致 | 一致 | 已对齐 |
