---
name: sync-docs
description: Use when the user wants to upload/sync files to the documentation center, or create/update delivery packages for developers. Triggers on "同步文档", "同步一下", "sync docs", "更新文档中心", "上传", "打交付包", "打包", "交付开发", or when the user just finished updating a module's files (PRD, prototype, ER diagram, etc.) and wants to publish. Also triggers when the user mentions delivering files to developers or packaging latest artifacts.
---

# 文档中心同步 Skill

将模块产物同步到 `~/looply-docs` 文档中心，自动更新 index.html + git push。
同步时检查交付包状态，按需打包最新文件给开发。

## 前置条件

首次使用前确保：
1. 已 clone 仓库：`git clone git@github.com:happy2snow007-blip/looply-docs.git ~/looply-docs`
2. Python 3 可用（macOS 自带）
3. 源文件按子目录结构存放（见下方"子目录结构参考"）

## 执行流程

### 1. 推断模块范围

根据对话上下文推断要同步的模块。不确定时问用户："同步哪个模块？还是全部？"

**已注册模块以 `sync.py` 的 MODULES 字典为唯一准绳（硬性）**：判断一个模块是否已注册，**必须实际查 sync.py**，不能凭下方表格：

```bash
grep -n "^        'name':" ~/looply-docs/sync.py
```

> **为什么必须查**：本表是快照，会滞后于 sync.py。2026-07-22 曾出现表中只有 9 个模块、sync.py 实际已有 19 个的情况（红布林商品对接/红布林订单对接等早已注册但表中没有），若照表判断会误走「新模块注册流程」，重复写入 MODULES 造成冲突。**表格仅供快速参考，冲突时以 sync.py 为准，并顺手回填本表。**

**注册模块快照**（2026-07-22 校准，19 个）：

| 模块 | key | 命令行关键词 | looply-docs 目标目录 |
|------|-----|-------------|-------------------:|
| 登录注册 | `login` | `login` `登录` | docs |
| 首页 | `home` | `home` `首页` | docs-首页 |
| 商品系统 | `product` | `product` `商品` | docs-商品系统 |
| 商详页 | `pdp` | `pdp` `商详` | docs-商详 |
| Market | `market` | `market` | docs-market系统 |
| 多语言管理 | `translation` | `translation` `多语言` | docs-多语言管理 |
| 库存管理 | `inventory` | `inventory` `库存` | docs-库存管理 |
| 汇率管理 | `exchange` | `exchange` `汇率` | docs-汇率管理 |
| 用户管理 | `user` | `user` `用户` | docs-用户管理 |
| 物流管理 | `logistics` | `logistics` `物流` | docs-物流管理 |
| 订阅管理 | `subscription` | `subscription` `订阅` | docs-订阅管理 |
| 购物车 | `cart` | `cart` `购物车` | docs-购物车 |
| 订单支付 | `order` | `order` `订单支付` | docs-订单支付 |
| 订单列表详情 | `order_list` | `order_list` `订单列表` | docs-订单列表详情 |
| 红布林商品对接 | `plm` | `红布林` `plm` `商品对接` | docs-红布林商品对接 |
| 红布林订单对接 | `rhl_order` | `红布林订单` `rhlorder` `订单对接` | docs-红布林订单对接 |
| Shop页导航 | `shop` | `shop` | docs-shop页 |
| 社媒分享管理 | `social_share` | `social_share` `社媒` | docs-社媒分享管理 |
| 收藏与浏览历史 | `favourites_history` | `favourites` `收藏` | docs-收藏与浏览历史 |

只有 **sync.py 中确实没有**该模块时 → 才进入**新模块注册流程**（见步骤 1.2）。

### 1.1 验证源目录路径

路径配置保存在 `~/looply-docs/.sync-paths.json`（已加入 .gitignore，每人各自维护），格式：

```json
{
  "商品系统": "~/Desktop/海外业务/商品",
  "Market": "~/work/market-docs"
}
```

**查找路径优先级**（sync.py 中 `get_source_dir()` 的逻辑）：
1. 读取 `.sync-paths.json`，按模块中文名（`name` 字段）查找
2. 如果没有记录，尝试 MODULES 中的 `default_source`（`$HOME` 展开为实际路径）
3. 如果路径不存在 → 询问用户："`{模块名}` 的文件存放在哪个目录？"

用户提供路径后：
- 验证路径存在
- **自动写入 `.sync-paths.json`**，下次不再询问
- 后续所有步骤中的"源目录"均使用该路径

**子目录结构参考**（不要求全部存在，有什么同步什么）：
```
{源目录}/
├── PRD/              # .md 文件
├── 原型/             # .html 文件
├── 实体关系图/       # .svg 文件
├── 产品架构图/       # .svg 文件（如有）
├── 系统流程图/       # .svg 文件（如有）
├── UI/              # .pen 文件（如有）
├── 调研/            # 调研文档（如有）
├── 评审记录/        # 评审文档（如有）
└── 验收记录/        # 验收文档（如有）
```

### 1.2 新模块注册流程

当用户要同步的模块不在已注册列表中时，只需修改 **sync.py 的 MODULES 字典**即可完成注册。

#### 收集信息

向用户确认：
1. **模块名**（中文，如"订单管理"）
2. **源目录路径**（本地文件存放位置）
3. **目标目录名**（looply-docs 中的文件夹名，建议 `docs-{模块名}`）
4. **命令行关键词**（用于筛选同步，如 `订单`、`order`）
5. **文件命名前缀**（如 `looply-订单管理`，用于正则匹配）

#### 在 sync.py MODULES 中新增条目

```python
'order': {
    'name': '订单管理',
    'default_source': '$HOME/Desktop/海外业务/订单',
    'target': 'docs-订单管理',
    'keywords': ['订单', 'order'],
    'config_key': 'order',
    'artifacts': {
        'prototype': {
            'subdir': '原型',
            'pattern': r'looply-订单管理后台原型-v(.+?)\.html',
            'exclude': r'(backup|对比)',
        },
        'prd': {
            'subdir': 'PRD',
            'pattern': r'looply-订单管理-PRD-v(.+?)\.md',
        },
        'er': {
            'subdir': '实体关系图',
            'pattern': r'looply-订单管理实体关系图-v(.+?)\.svg',
        },
        'delivery': {
            'subdir': '.',
            'pattern': r'订单管理-交付开发 V(.+?)\.zip',
        },
    },
},
```

注意 pattern 的灵活性：
- 版本号部分统一用 `(.+?)` 捕获，可匹配 `1.0`、`21`、`21-antd` 等各种格式
- 大小写 `v`/`V` 需根据用户实际文件名确定
- `config_key` 用于 prototype-config.js 中的键名（原型链接自动跳转）

#### 在 index.html 中新增模块 section

在 `<div class="container" id="content">` 内新增对应的 HTML 区块，参照已有模块的结构。根据源目录中实际有哪些产物类型来决定放哪些 card（没有的不放）。

#### artifacts 完整性检查（硬性）

注册新模块或首次为已有模块打交付包时，必须检查 sync.py MODULES 中该模块的 `artifacts` 字典是否包含 `delivery` 条目。**缺少 `delivery` artifact 会导致 sync.py 无法检测交付包、不会在 index.html 中生成交付包条目。**

检查方法：`grep -A20 "'模块key':" ~/looply-docs/sync.py | grep delivery`

如果没有 → 立即补上：
```python
'delivery': {
    'subdir': '.',
    'pattern': r'{模块名}-交付开发 V(.+?)\.zip',
},
```

同理，所有需要被 sync.py 自动管理版本号和 index.html 条目的产物类型（prototype、prd、er、delivery 等），都必须在 `artifacts` 中配置，否则 sync.py 只会复制文件但不会更新页面。

#### 注册完成后

- 将源目录路径写入 `.sync-paths.json`
- 继续执行后续同步步骤

### 2. 确保 PRD 在线阅读器存在

同步前检查目标目录下 `PRD/index.html` 是否存在。如果模块有 PRD 但缺少阅读器，需要生成。

**如果不存在**，从模板复制并替换：
```bash
cp ~/looply-docs/docs-market系统/PRD/index.html ~/looply-docs/{目标目录}/PRD/index.html
```

替换两处：
- `<title>Looply PRD - Market 主数据 PRD</title>` → `<title>Looply PRD - {模块中文名} PRD</title>`
- `<span class="title">Market 主数据 PRD V1.2</span>` → `<span class="title">{模块中文名} PRD V{版本号}</span>`

**注意**：sync.py 已自动处理 `latest.md`（按版本号选取最新 .md 复制为 latest.md）和 topbar 版本号更新，无需手动处理。

### 3. 确保 index.html 中 PRD 条目有"查看"按钮

检查 `~/looply-docs/index.html` 中该模块 PRD 条目是否包含 `btn-view` 查看按钮。如果只有下载按钮没有查看按钮，需要添加：

```html
<a class="btn btn-view" href="{目标目录}/PRD/index.html" target="_blank">查看</a>
```

放在 `doc-actions` 中、下载按钮之前。

### 4. 检查交付包状态

交付包是给开发的一次性打包产物，包含该模块当前最新的所有设计文件。检查源目录下是否已有 `{模块名}-交付开发 V*` 文件夹：

- **没有交付包** → 提醒用户："该模块还没有交付包，需要新建一个吗？"
  - 确认 → 步骤 5（版本号从 V1.0 开始）
  - 拒绝 → 跳到步骤 6
- **已有交付包** → 问用户："该模块已有交付包，本次需要新增版本吗？"
  - 确认 → 步骤 5（版本号递增）
  - 拒绝 → 跳到步骤 6（只同步文件，不打新包）

### 5. 打包交付包

#### 5.1 确定版本号

查看源目录下已有交付包文件夹，取最大版本号后递增：
- 默认 +0.1（如 V1.0 → V1.1），向用户确认
- 大版本升级（V1.x → V2.0）需用户明确指定
- 日期取当天，格式 YYYYMMDD

#### 5.2 确认文件清单

从各子目录取最新版本文件。列出清单让用户确认后再打包：

| 产物类型 | 源子目录 | 取法 |
|---------|---------|------|
| 原型 | 原型/ | 版本号最大的 .html（排除 backup/对比等） |
| PRD | PRD/ | 版本号最大的 .md |
| ER图 | 实体关系图/ | 版本号最大的 .svg |
| 产品架构图 | 产品架构图/ | 版本号最大的 .svg（如有） |
| 系统流程图 | 系统流程图/ | 版本号最大的 .svg（如有） |
| UI 设计稿 | UI/ | 最新的 .pen 文件（如有） |
| 图片资源 | 原型/ | 同目录下的 .png/.jpg/.svg |

#### 5.3 执行打包

```bash
# 1. 新建文件夹
mkdir -p "{源目录}/{模块名}-交付开发 V{版本号}-{日期}"

# 2. 复制最新文件到文件夹
cp <最新原型> <目标文件夹>/
cp <最新PRD> <目标文件夹>/
cp <最新ER图> <目标文件夹>/

# 3. 压缩为 zip，输出到 looply-docs
cd "{源目录}"
zip -r ~/looply-docs/{目标目录}/{模块名}-交付开发\ V{版本号}-{日期}.zip "{模块名}-交付开发 V{版本号}-{日期}/"
```

### 6. 执行同步

```bash
cd ~/looply-docs && python3 sync.py <模块关键词>
```

全量同步时不加参数：`cd ~/looply-docs && python3 sync.py`

sync.py 自动完成：
1. 从源目录复制文件到 looply-docs 对应目录
2. 按版本号选取最新 PRD .md 复制为 latest.md
3. 检测各产物最新版本，更新 prototype-config.js
4. 更新 index.html 的链接、版本号、日期、历史版本列表
5. 更新各模块 PRD index.html 的 topbar 版本号
6. git add + commit + push

**如果 push 失败（冲突）**：
1. 运行 `git status` 查看冲突文件
2. 运行 `git pull --rebase origin main`
3. 如果 rebase 有冲突：
   - index.html 冲突 → 大概率是两人改了不同模块条目，手动合并保留双方修改
   - 产物文件冲突 → 取版本号更高的文件
4. 解决冲突文件后：`git add <冲突文件> && git rebase --continue`
5. 然后 `git push origin main`
6. 告知用户冲突已解决

**如果 push 报网络错误（HTTP2 framing layer / 超时）**：
不是冲突，是到 GitHub 的连接问题。处理：
1. 先确认无本地代理干扰：`git config --get http.proxy`（用户用 AnyConnect，正常应为空）
2. 降级 HTTP 版本绕过 framing 错误：`git config http.version HTTP/1.1`
3. 重试 `git push origin main`
该配置持久化在仓库，设置一次后续 push 均生效。

### 7. 汇报结果

简要说明：
- 同步了哪些文件
- 版本号变化（如原型 v20→v21）
- PRD 阅读器状态（新建/已有）
- 交付包信息（如有）：文件清单、zip 大小
- git push 是否成功

## 文件命名规范

产物文件应遵循统一命名规则，确保 sync.py 的自动版本检测正常工作：

| 产物类型 | 命名格式 | 示例 |
|---------|---------|------|
| 后台原型 | `{前缀}后台原型-v{版本}.html` | `looply-订单管理后台原型-v3.html` |
| PRD | `{前缀}-PRD-v{版本}.md` | `looply-订单管理-PRD-v1.0.md` |
| ER图 | `{前缀}实体关系图-v{版本}.svg` | `looply-订单管理实体关系图-v2.0.svg` |
| 产品架构图 | `{前缀}产品架构图-v{版本}.svg` | `looply-订单管理产品架构图-v1.0.svg` |
| 系统流程图 | `{前缀}流程图-v{版本}.svg` | `looply-订单管理流程图-v1.0.svg` |
| 交付包 | `{模块名}-交付开发 V{版本}-{日期}.zip` | `订单管理-交付开发 V1.0-20260602.zip` |

## 注意事项

- 同步前不需要用户手动 cd 到任何目录
- git push 失败时告知用户并协助解决，不要静默重试
- 某类产物不存在时跳过即可，不报错
- PRD 阅读器依赖 `latest.md`，sync.py 已自动维护（按版本号选取最新 .md）
- `.sync-paths.json` 是本地配置，已加入 .gitignore，不会被 push
- 新模块注册只需改 sync.py 的 MODULES 字典 + index.html，不需要改其他文件
- **index.html 时间戳统一用「文件 mtime（文件最后更新时间）」并显示到时分（格式 `%Y-%m-%d %H:%M`）**：所有 doc-desc 日期（交付包的 `&middot; 日期`、普通文件的 `更新于 日期`）都表示「该文件最后一次实际更新的时间」，取对应文件的 `os.path.getmtime`，**不要用 `datetime.now()`（脚本运行时间）**。原因：用运行时间会导致任何一次无关同步（改了别的模块、只改脚本空跑等）把日期刷成当天，与文件是否真正变化脱节而失真。sync.py 已按此实现——`build_delivery_desc` 用 zip 的 mtime；`_gen_card` 与「更新于」替换用各自文件路径的 mtime，取不到文件时才退回 `now()`。若日后重构脚本或新增日期展示点，一律用文件 mtime，不要退回到脚本运行时间或只显示到日
