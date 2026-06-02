#!/usr/bin/env python3
"""
自动检测各模块最新版本文件，更新 prototype-config.js 和 index.html。
在 sync.sh 中于文件复制完成后、git 操作之前调用。

自动更新"最新"条目的链接、版本号、日期，并维护历史版本列表。
"""

import os
import re
import sys
from datetime import datetime

REPO_DIR = os.path.dirname(os.path.abspath(__file__))

# 模块筛选：命令行参数作为关键词过滤
MODULE_FILTER = sys.argv[1:] if len(sys.argv) > 1 else []

# ─── 模块配置 ───────────────────────────────────────────────────────────────────

MODULES = {
    'product': {
        'dir': 'docs-商品系统',
        'config_key': 'product',
        'artifacts': {
            'prototype': {
                'subdir': '原型',
                'pattern': r'looply-商品管理后台原型-v(.+?)\.html',
                'exclude': r'(backup|对比|1对1|1对N)',
            },
            'prd': {
                'subdir': 'PRD',
                'pattern': r'looply-商品系统-PRD-v(.+?)\.md',
            },
            'er': {
                'subdir': '实体关系图',
                'pattern': r'looply-商品主数据实体关系图-v(.+?)\.svg',
            },
            'architecture': {
                'subdir': '产品架构图',
                'pattern': r'looply-商品系统产品架构图-v(.+?)\.svg',
            },
            'flowchart': {
                'subdir': '系统流程图',
                'pattern': r'looply-商品系统流程图-v(.+?)\.svg',
            },
            'delivery': {
                'subdir': '.',
                'pattern': r'商品-交付开发 V(.+?)\.zip',
            },
        },
    },
    'market': {
        'dir': 'docs-market系统',
        'config_key': 'market',
        'artifacts': {
            'prototype': {
                'subdir': '原型',
                'pattern': r'looply-market后台原型-v(.+?)\.html',
                'exclude': r'(backup|对比|分页|独立域名)',
            },
            'prd': {
                'subdir': 'PRD',
                'pattern': r'looply-market主数据-PRD-v(.+?)\.md',
            },
            'er': {
                'subdir': '实体关系图',
                'pattern': r'looply-market主数据实体关系图-v(.+?)\.svg',
            },
            'delivery': {
                'subdir': '.',
                'pattern': r'market-交付开发 V(.+?)\.zip',
            },
        },
    },
    'inventory': {
        'dir': 'docs-库存管理',
        'config_key': 'inventory',
        'artifacts': {
            'prototype': {
                'subdir': '原型',
                'pattern': r'looply-库存管理后台原型-v(.+?)\.html',
                'exclude': r'(backup)',
            },
            'prd': {
                'subdir': 'PRD',
                'pattern': r'looply-库存管理-PRD-v(.+?)\.md',
            },
            'er': {
                'subdir': '实体关系图',
                'pattern': r'looply-库存系统实体关系图-v(.+?)\.svg',
            },
            'delivery': {
                'subdir': '.',
                'pattern': r'库存-交付开发 V(.+?)\.zip',
            },
        },
    },
    'translation': {
        'dir': 'docs-翻译管理',
        'config_key': 'translation',
        'artifacts': {
            'prototype': {
                'subdir': '原型',
                'pattern': r'looply-翻译管理后台原型-v(.+?)\.html',
                'exclude': r'(backup)',
            },
            'prd': {
                'subdir': 'PRD',
                'pattern': r'looply-翻译模块-PRD-v(.+?)\.md',
            },
            'er': {
                'subdir': '实体关系图',
                'pattern': r'looply-翻译模块实体关系图-v(.+?)\.svg',
            },
        },
    },
    'exchange': {
        'dir': 'docs-汇率管理',
        'config_key': 'exchange',
        'artifacts': {
            'prototype': {
                'subdir': '原型',
                'pattern': r'looply-汇率管理后台原型-v(.+?)\.html',
                'exclude': r'(backup)',
            },
            'prd_html': {
                'subdir': 'PRD',
                'pattern': r'looply-汇率管理-PRD-v(.+?)\.html',
            },
            'prd_md': {
                'subdir': 'PRD',
                'pattern': r'looply-汇率管理-PRD-v(.+?)\.md',
            },
            'er': {
                'subdir': '实体关系图',
                'pattern': r'looply-汇率管理实体关系图-v(.+?)\.svg',
            },
            'architecture': {
                'subdir': '产品架构图',
                'pattern': r'looply-汇率管理-产品架构图-v(.+?)\.svg',
            },
        },
    },
    'user': {
        'dir': 'docs-用户管理',
        'config_key': 'user',
        'artifacts': {
            'prototype': {
                'subdir': '原型',
                'pattern': r'looply-用户管理后台原型-v(.+?)\.html',
                'exclude': r'(backup)',
            },
            'prd': {
                'subdir': 'PRD',
                'pattern': r'looply-用户管理-PRD-v(.+?)\.md',
            },
        },
    },
    'pdp': {
        'dir': 'docs-商详',
        'config_key': 'pdp',
        'artifacts': {
            'prototype': {
                'subdir': '原型',
                'pattern': r'looply-商详页CMS配置后台原型\.html',
                'no_version': True,
            },
        },
    },
    'login': {
        'dir': 'docs',
        'config_key': None,
        'artifacts': {
            'architecture': {
                'subdir': '产品架构图',
                'pattern': r'looply-登录注册模块产品架构图-v(.+?)\.svg',
            },
            'flowchart': {
                'subdir': '系统流程图',
                'pattern': r'looply-登录注册系统流程图-v(.+?)\.svg',
                'exclude': r'(横向泳道)',
            },
            'delivery': {
                'subdir': '.',
                'pattern': r'登录注册-交付开发 V(.+?)\.zip',
            },
        },
    },
}


# ─── 版本号解析 ─────────────────────────────────────────────────────────────────

def parse_version(ver_str):
    """
    解析版本号为可比较的元组。
    '1.0' → (1, 0), '32' → (32,), '21-antd' → (21,), '6-风格A-活力亲和' → (6,)
    """
    m = re.match(r'(\d+(?:\.\d+)?)', ver_str)
    if not m:
        return (0,)
    parts = m.group(1).split('.')
    return tuple(int(p) for p in parts)


def find_latest_file(module_dir, subdir, pattern, exclude=None):
    """扫描目录，返回版本号最高的文件名和版本字符串。"""
    if subdir == '.':
        search_dir = os.path.join(REPO_DIR, module_dir)
    else:
        search_dir = os.path.join(REPO_DIR, module_dir, subdir)

    if not os.path.isdir(search_dir):
        return None, None

    best_file = None
    best_ver = None
    best_parsed = (0,)

    for fname in os.listdir(search_dir):
        if exclude and re.search(exclude, fname):
            continue
        m = re.match(pattern, fname)
        if m:
            ver_str = m.group(1)
            parsed = parse_version(ver_str)
            if parsed > best_parsed:
                best_parsed = parsed
                best_ver = ver_str
                best_file = fname

    return best_file, best_ver


def find_all_files(module_dir, subdir, pattern, exclude=None):
    """扫描目录，返回所有匹配文件，按版本号降序排列。返回 [(filename, ver_str), ...]"""
    if subdir == '.':
        search_dir = os.path.join(REPO_DIR, module_dir)
    else:
        search_dir = os.path.join(REPO_DIR, module_dir, subdir)

    if not os.path.isdir(search_dir):
        return []

    results = []
    for fname in os.listdir(search_dir):
        if exclude and re.search(exclude, fname):
            continue
        m = re.match(pattern, fname)
        if m:
            ver_str = m.group(1)
            parsed = parse_version(ver_str)
            results.append((fname, ver_str, parsed))

    results.sort(key=lambda x: x[2], reverse=True)
    return [(fname, ver_str) for fname, ver_str, _ in results]


# ─── prototype-config.js 更新 ──────────────────────────────────────────────────

def update_prototype_config(latest_prototypes):
    """重写 prototype-config.js。"""
    config_path = os.path.join(REPO_DIR, 'prototype-config.js')

    # 读取现有配置作为 fallback
    current = {}
    if os.path.exists(config_path):
        content = open(config_path, 'r', encoding='utf-8').read()
        for m in re.finditer(r"'(\w+)':\s*'([^']+)'", content):
            current[m.group(1)] = m.group(2)

    # 用检测到的最新值覆盖
    for key, path in latest_prototypes.items():
        if path:
            current[key] = path

    # 固定顺序输出
    key_order = ['product', 'market', 'inventory', 'translation', 'exchange', 'user', 'pdp']
    lines = []
    max_key_len = max(len(k) for k in key_order if k in current)
    for key in key_order:
        if key in current:
            padding = ' ' * (max_key_len - len(key) + 1)
            lines.append(f"  '{key}':{padding}'{current[key]}'")

    output = """/**
 * Looply 后台原型路径配置（单一数据源）
 *
 * 此文件由 update-index.py 自动生成，请勿手动修改。
 *
 * 使用方式：
 *   index.html — 在原型链接上加 data-prototype="模块key"，JS 自动替换 href
 *   admin.html — MODULES 数组从 PROTOTYPE_CONFIG 读取 url
 */
var PROTOTYPE_CONFIG = {
""" + ',\n'.join(lines) + ',\n};\n'

    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(output)


# ─── index.html 更新（只改"最新"条目，不动历史版本） ─────────────────────────────

def update_index_html(updates, all_versions, all_history=None):
    """
    三遍处理 index.html：
    第一遍：替换 href，记录每个 doc-item 块对应的 update 条目，跟踪变更
    第二遍：更新 doc-name 版本号、doc-desc 日期、交付包 doc-desc 内容
    第三遍：为所有制品类型插入/更新历史版本列表
    """
    index_path = os.path.join(REPO_DIR, 'index.html')
    lines = open(index_path, 'r', encoding='utf-8').readlines()
    changed = False

    # ── 第一遍：替换 href，记录 doc-item 块 → update 的映射 ──
    # item_map: line_index_of_doc_item_start → upd
    item_map = {}
    changed_items = set()   # doc-item blocks whose href actually changed
    in_history = False
    current_item_start = None

    for i, line in enumerate(lines):
        if 'history-list' in line and '<ul' in line:
            in_history = True
        if in_history and '</ul>' in line:
            in_history = False
            continue
        if in_history:
            continue

        if '<li class="doc-item">' in line:
            current_item_start = i

        if '</li>' in line and current_item_start is not None:
            current_item_start = None

        for upd in updates:
            href_dir = upd['href_dir']
            file_pattern = upd['file_pattern']
            new_file = upd['new_file']

            regex = re.compile(r'(href="' + re.escape(href_dir) + r')([^"]+)(")')
            match = regex.search(lines[i])
            if match:
                old_filename = match.group(2)
                if re.match(file_pattern, old_filename):
                    # 记录块
                    if current_item_start is not None:
                        item_map[current_item_start] = upd
                    # 替换文件名
                    if old_filename != new_file:
                        lines[i] = lines[i][:match.start()] + match.group(1) + new_file + match.group(3) + lines[i][match.end():]
                        changed = True
                        if current_item_start is not None:
                            changed_items.add(current_item_start)

    # ── 第二遍：更新 doc-name 版本号 + 交付包 doc-desc ──
    in_history = False
    current_item_start = None
    new_lines = []

    for i, line in enumerate(lines):
        if 'history-list' in line and '<ul' in line:
            in_history = True
        if in_history and '</ul>' in line:
            in_history = False
            new_lines.append(line)
            continue
        if in_history:
            new_lines.append(line)
            continue

        if '<li class="doc-item">' in line:
            current_item_start = i

        new_line = line

        # 更新 doc-name 版本号
        if current_item_start in item_map and 'doc-name' in line and '<span class="badge">' in line:
            upd = item_map[current_item_start]
            new_ver = upd.get('new_ver', '')
            if new_ver:
                # 用源文件完整版本字符串替换 doc-name 中的版本号
                # 匹配从 v/V 开始到 <span 之前的所有文字（含空格和中文描述）
                ver_regex = re.compile(r'(?<=\s)[vV].+?(?=\s*<span)')
                ver_match = ver_regex.search(new_line)
                if ver_match:
                    old_ver_text = ver_match.group(0)
                    new_ver_text = f'v{new_ver}'
                    if old_ver_text != new_ver_text:
                        new_line = new_line[:ver_match.start()] + new_ver_text + new_line[ver_match.end():]
                        changed = True

        # 更新 doc-desc 日期（当 href 发生变化时）
        if current_item_start in changed_items and 'doc-desc' in new_line and '更新于' in new_line:
            today = datetime.now().strftime('%Y-%m-%d')
            new_line = re.sub(r'更新于 \d{4}-\d{2}-\d{2}(\s+\d{2}:\d{2})?', f'更新于 {today}', new_line)
            if new_line != line:
                changed = True

        # 更新交付包 doc-desc
        if 'doc-desc' in new_line and '含 PRD' in new_line:
            for mod_name in set(upd.get('mod_name', '') for upd in updates):
                if not mod_name:
                    continue
                mod_dir = MODULES.get(mod_name, {}).get('dir', '')
                if not mod_dir:
                    continue
                # 确认交付包属于该模块：
                # 方式1: 前10行包含模块目录（href 在 desc 前面的情况）
                # 方式2: doc-name 中包含模块名关键词（如 "market-交付开发"）
                recent = ''.join(new_lines[-10:])
                # 模块名关键词映射
                mod_keywords = {
                    'market': 'market',
                    'product': '商品',
                    'inventory': '库存',
                    'translation': '翻译',
                    'exchange': '汇率',
                    'user': '用户',
                    'login': '登录注册',
                }
                keyword = mod_keywords.get(mod_name, mod_name)
                if mod_dir not in recent and keyword not in recent:
                    continue

                prd_ver = all_versions.get((mod_name, 'prd')) or all_versions.get((mod_name, 'prd_md'))
                if prd_ver:
                    new_line = re.sub(r'PRD [vV][\d.]+', f'PRD V{prd_ver}', new_line)
                proto_ver = all_versions.get((mod_name, 'prototype'))
                if proto_ver:
                    new_line = re.sub(r'后台原型 [vV][\w.-]+', f'后台原型 v{proto_ver}', new_line)
                    new_line = re.sub(r'原型 [vV][\w.-]+', f'原型 v{proto_ver}', new_line)
                er_ver = all_versions.get((mod_name, 'er'))
                if er_ver:
                    new_line = re.sub(r'ER图 [vV][\d.]+', f'ER图 v{er_ver}', new_line)

            if new_line != line:
                changed = True

        if '</li>' in new_line and current_item_start is not None:
            current_item_start = None

        new_lines.append(new_line)

    # ── 第三遍：为所有制品类型插入/更新历史版本列表 ──
    if all_history:
        # 历史版本列表中每种制品的显示格式: (版本前缀, 链接属性, 链接文字)
        HISTORY_ITEM_FMT = {
            'prototype': ('v', 'target="_blank"', '查看'),
            'er':        ('v', 'target="_blank"', '查看'),
            'architecture': ('v', 'target="_blank"', '查看'),
            'flowchart':    ('v', 'target="_blank"', '查看'),
            'prd':       ('V', 'download', 'Markdown'),
            'prd_html':  ('V', 'download', 'HTML'),
            'prd_md':    ('V', 'download', 'Markdown'),
            'delivery':  ('V', 'download', '下载'),
        }

        final_lines = []
        i = 0
        while i < len(new_lines):
            line = new_lines[i]

            # 检测主 doc-list 的 </ul>，在其后插入/更新历史版本
            matched_key = None
            if '</ul>' in line and i >= 2:
                lookback = ''.join(new_lines[max(0, i-8):i+1])
                if 'history-list' not in lookback:
                    for (mod_name, art_type), hist_info in all_history.items():
                        mod_dir = hist_info['dir']
                        subdir = hist_info['subdir']
                        file_pattern = hist_info.get('file_pattern', '')
                        if subdir == '.':
                            href_prefix = f'{mod_dir}/'
                        else:
                            href_prefix = f'{mod_dir}/{subdir}/'
                        if href_prefix not in lookback:
                            continue
                        if subdir == '.':
                            # 根目录制品（如交付包）：需验证 href 中的文件名匹配 pattern
                            href_m = re.search(r'href="' + re.escape(href_prefix) + r'([^"]+)"', lookback)
                            if href_m and re.match(file_pattern, href_m.group(1)):
                                matched_key = (mod_name, art_type)
                                break
                        else:
                            # 子目录制品：路径前缀已足够精确
                            matched_key = (mod_name, art_type)
                            break

            if matched_key:
                hist_info = all_history[matched_key]
                mod_dir = hist_info['dir']
                subdir = hist_info['subdir']
                history = hist_info['history']
                art_type = hist_info['art_type']
                if subdir == '.':
                    href_prefix = f'{mod_dir}/'
                else:
                    href_prefix = f'{mod_dir}/{subdir}/'

                ver_prefix, link_attr, link_label = HISTORY_ITEM_FMT.get(art_type, ('v', 'download', '下载'))

                # 先输出当前 </ul> 行
                final_lines.append(line)
                i += 1

                # 如果下一行已有 history-toggle，收集已有条目
                existing_lines = []   # 保留的已有 history-item 行
                existing_hrefs = set()
                if i < len(new_lines) and 'history-toggle' in new_lines[i]:
                    i += 1  # skip toggle
                    # 收集 history-list 中的现有条目
                    while i < len(new_lines):
                        hist_line = new_lines[i]
                        if 'history-item' in hist_line:
                            existing_lines.append(hist_line)
                            for href_m in re.finditer(r'href="([^"]+)"', hist_line):
                                existing_hrefs.add(href_m.group(1))
                        if '</ul>' in hist_line:
                            i += 1
                            break
                        i += 1

                # 找出磁盘上有但历史列表中缺失的文件
                new_items = []
                for hist_file, hist_ver in history:
                    href = f'{href_prefix}{hist_file}'
                    if href not in existing_hrefs:
                        new_items.append(f'          <li class="history-item">{ver_prefix}{hist_ver} <a href="{href}" {link_attr}>{link_label}</a></li>\n')

                if new_items or existing_lines:
                    indent = '        '
                    final_lines.append(f'{indent}<div class="history-toggle" onclick="this.nextElementSibling.classList.toggle(\'open\')">历史版本 ▾</div>\n')
                    final_lines.append(f'{indent}<ul class="doc-list history-list">\n')
                    # 新增条目在前（按版本降序），已有条目在后
                    final_lines.extend(new_items)
                    final_lines.extend(existing_lines)
                    final_lines.append(f'{indent}</ul>\n')
                    if new_items:
                        changed = True
            else:
                final_lines.append(line)
                i += 1

        new_lines = final_lines

    if changed:
        with open(index_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print('  [更新] index.html 已更新')
    else:
        print('  [无变化] index.html 无需更新')


# ─── 主流程 ────────────────────────────────────────────────────────────────────

def main():
    print('=== update-index.py: 自动检测最新版本 ===')

    latest_prototypes = {}  # config_key -> relative_path
    index_updates = []      # 用于更新 index.html
    all_versions = {}       # (mod_name, art_type) -> ver_str
    all_history = {}        # (mod_name, art_type) -> {...} 所有制品的历史版本

    # art_type 到 doc-name 显示关键词的映射
    ART_DISPLAY_MAP = {
        'prototype': '后台原型',
        'prd': 'PRD',
        'prd_html': 'PRD',
        'prd_md': 'PRD',
        'er': '实体关系图',
        'architecture': '产品架构图',
        'flowchart': '系统流程图',
        'delivery': '交付开发',
    }

    for mod_name, mod_config in MODULES.items():
        module_dir = mod_config['dir']
        config_key = mod_config['config_key']

        # 模块筛选
        if MODULE_FILTER:
            matched = any(kw in mod_name or kw in module_dir for kw in MODULE_FILTER)
            if not matched:
                continue

        for art_type, art_config in mod_config['artifacts'].items():
            if art_config.get('no_version'):
                continue

            subdir = art_config['subdir']
            pattern = art_config['pattern']
            exclude = art_config.get('exclude')

            latest_file, latest_ver = find_latest_file(module_dir, subdir, pattern, exclude)
            if not latest_file:
                continue

            print(f'  {mod_name}/{art_type}: {latest_file} (v{latest_ver})')

            # 记录版本号
            all_versions[(mod_name, art_type)] = latest_ver

            # 收集历史版本（除最新外的所有版本），用于自动维护历史版本列表
            all_files = find_all_files(module_dir, subdir, pattern, exclude)
            if len(all_files) > 1:
                all_history[(mod_name, art_type)] = {
                    'dir': module_dir,
                    'subdir': subdir,
                    'history': all_files[1:],
                    'art_type': art_type,
                    'file_pattern': pattern,
                }

            # 原型 → 更新 prototype-config.js
            if art_type == 'prototype' and config_key:
                if subdir == '.':
                    rel_path = f'{module_dir}/{latest_file}'
                else:
                    rel_path = f'{module_dir}/{subdir}/{latest_file}'
                latest_prototypes[config_key] = rel_path

            # 构建 index.html 更新规则
            if subdir == '.':
                href_dir = f'{module_dir}/'
            else:
                href_dir = f'{module_dir}/{subdir}/'

            index_updates.append({
                'href_dir': href_dir,
                'file_pattern': pattern,
                'new_file': latest_file,
                'new_ver': latest_ver,
                'mod_name': mod_name,
                'art_type': art_type,
                'art_display': ART_DISPLAY_MAP.get(art_type, ''),
            })

    # 更新 prototype-config.js
    if latest_prototypes:
        update_prototype_config(latest_prototypes)
        print('  [更新] prototype-config.js 已更新')

    # 更新 index.html（改链接 + 改版本号文字 + 改交付包描述 + 交付包历史版本）
    if index_updates:
        update_index_html(index_updates, all_versions, all_history)

    # 更新各模块 PRD index.html 的 topbar 版本号
    update_prd_index_topbar()


# ─── PRD index.html topbar 版本同步 ─────────────────────────────────────────────

def update_prd_index_topbar():
    """扫描各模块 PRD/latest.md 提取版本号，同步更新 PRD/index.html 的 topbar 标题。"""
    import glob

    # 收集所有 PRD index.html 路径
    prd_dirs = glob.glob(os.path.join(REPO_DIR, 'docs*/PRD'))
    prd_dirs += glob.glob(os.path.join(REPO_DIR, 'docs/PRD'))

    changed_count = 0
    for prd_dir in prd_dirs:
        latest_md = os.path.join(prd_dir, 'latest.md')
        index_html = os.path.join(prd_dir, 'index.html')
        if not os.path.isfile(latest_md) or not os.path.isfile(index_html):
            continue

        # 从 latest.md 前 10 行提取版本号
        version = None
        with open(latest_md, 'r', encoding='utf-8') as f:
            for line in f.readlines()[:10]:
                # 匹配各种格式：**版本**: V1.1, 版本：V0.9, # 标题 V1.0, 文档版本：v4.2
                m = re.search(r'[版本|版本]\s*[:：]\s*[vV]?([\d.]+)', line)
                if not m:
                    m = re.search(r'PRD\s+[vV]([\d.]+)', line)
                if m:
                    version = m.group(1)
                    break

        if not version:
            continue

        # 读取 index.html，替换 topbar 中的版本号
        content = open(index_html, 'r', encoding='utf-8').read()
        # 匹配 <span class="title">...PRD V1.0</span> 或类似
        new_content = re.sub(
            r'(<span class="title">[^<]*?PRD\s+)[vV][\d.]+',
            lambda m: m.group(1) + 'V' + version,
            content
        )
        if new_content != content:
            with open(index_html, 'w', encoding='utf-8') as f:
                f.write(new_content)
            rel_path = os.path.relpath(index_html, REPO_DIR)
            print(f'  [更新] {rel_path} topbar → V{version}')
            changed_count += 1

    if changed_count == 0:
        print('  [无变化] PRD index.html topbar 均已是最新')


if __name__ == '__main__':
    main()
