#!/usr/bin/env python3
"""
自动检测各模块最新版本文件，更新 prototype-config.js 和 index.html。
在 sync.sh 中于文件复制完成后、git 操作之前调用。

关键约束：只更新"最新"条目的链接，不修改历史版本列表。
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

def update_index_html(updates):
    """
    逐行解析 index.html，只在非 history-list 区域内替换匹配的 href。
    updates: list of dicts with {href_dir, file_pattern, new_file}
    """
    index_path = os.path.join(REPO_DIR, 'index.html')
    lines = open(index_path, 'r', encoding='utf-8').readlines()

    in_history = False
    changed = False
    new_lines = []

    for line in lines:
        # 检测是否进入/离开 history-list 区域
        if 'history-list' in line and '<ul' in line:
            in_history = True
        if in_history and '</ul>' in line:
            in_history = False
            new_lines.append(line)
            continue

        if in_history:
            # 历史版本区域，不修改
            new_lines.append(line)
            continue

        # 非历史区域，尝试替换
        new_line = line
        for upd in updates:
            href_dir = upd['href_dir']
            file_pattern = upd['file_pattern']
            new_file = upd['new_file']

            # 匹配 href="目录/文件名"
            regex = re.compile(r'(href="' + re.escape(href_dir) + r')([^"]+)(")')
            match = regex.search(new_line)
            if match:
                old_filename = match.group(2)
                if re.match(file_pattern, old_filename):
                    new_line = new_line[:match.start()] + match.group(1) + new_file + match.group(3) + new_line[match.end():]
                    if old_filename != new_file:
                        changed = True

        new_lines.append(new_line)

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
            })

    # 更新 prototype-config.js
    if latest_prototypes:
        update_prototype_config(latest_prototypes)
        print('  [更新] prototype-config.js 已更新')

    # 更新 index.html（只改最新条目）
    if index_updates:
        update_index_html(index_updates)


if __name__ == '__main__':
    main()
