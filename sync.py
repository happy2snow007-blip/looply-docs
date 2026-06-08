#!/usr/bin/env python3
"""
Looply 文档中心同步脚本（合并版）

功能：
1. 从源目录复制产物文件到 looply-docs 对应目录
2. 自动检测最新版本，更新 index.html 和 prototype-config.js
3. 更新 PRD index.html 的 topbar 版本号
4. git commit + push

用法：
  python3 sync.py              # 同步全部模块
  python3 sync.py market       # 仅同步 market 模块
  python3 sync.py 商品 库存    # 同步多个模块

路径覆盖：
  每人可在 .sync-paths.json 中配置自己的源目录路径，
  该文件已加入 .gitignore，不会被 push。
"""

import os
import sys
import re
import json
import shutil
import subprocess
import glob as globmod
from datetime import datetime
from pathlib import Path

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
_updated_files = set()

# ─── 模块配置 ───────────────────────────────────────────────────────────────────
# 每个模块：default_source（默认源目录）、target（looply-docs 中的目标目录）、
#           keywords（用于命令行筛选匹配）、artifacts（用于版本检测的产物配置）

MODULES = {
    'login': {
        'name': '登录注册',
        'default_source': '$HOME/Desktop/海外业务/登录注册',
        'target': 'docs',
        'keywords': ['登录', '注册', 'login'],
        'config_key': None,
        'artifacts': {
            'prd': {
                'subdir': 'PRD',
                'pattern': r'Looply用户系统-登录注册功能说明文档-V(.+?)\.md',
            },
            'er': {
                'subdir': '实体关系图',
                'pattern': r'looply-登录注册模块实体关系图-v(.+?)\.html',
            },
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
    'home': {
        'name': '首页',
        'default_source': '$HOME/Desktop/海外业务首页',
        'target': 'docs-首页',
        'keywords': ['首页', 'home'],
        'config_key': None,
        'artifacts': {},
    },
    'product': {
        'name': '商品系统',
        'default_source': '$HOME/Desktop/海外业务/商品',
        'target': 'docs-商品系统',
        'keywords': ['商品', 'product'],
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
    'pdp': {
        'name': '商详页',
        'default_source': '$HOME/Desktop/海外业务/商详',
        'target': 'docs-商详',
        'keywords': ['商详', 'pdp'],
        'config_key': 'pdp',
        'artifacts': {
            'prototype': {
                'subdir': '原型',
                'pattern': r'looply-商详页CMS配置后台原型\.html',
                'no_version': True,
            },
        },
    },
    'market': {
        'name': 'Market',
        'default_source': '$HOME/Desktop/海外业务/market',
        'target': 'docs-market系统',
        'keywords': ['market', 'Market'],
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
    'translation': {
        'name': '翻译管理',
        'default_source': '$HOME/Desktop/海外业务/翻译',
        'target': 'docs-翻译管理',
        'keywords': ['翻译', 'translation'],
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
    'inventory': {
        'name': '库存管理',
        'default_source': '$HOME/Desktop/海外业务/库存',
        'target': 'docs-库存管理',
        'keywords': ['库存', 'inventory'],
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
    'exchange': {
        'name': '汇率管理',
        'default_source': '$HOME/Desktop/海外业务/汇率管理',
        'target': 'docs-汇率管理',
        'keywords': ['汇率', 'exchange'],
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
        'name': '用户管理',
        'default_source': '$HOME/Desktop/海外业务/用户管理',
        'target': 'docs-用户管理',
        'keywords': ['用户', 'user'],
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
            'delivery': {
                'subdir': '.',
                'pattern': r'用户管理-交付开发 V(.+?)\.zip',
            },
        },
    },
}

# ─── 路径解析 ─────────────────────────────────────────────────────────────────────

def expand_path(p):
    """展开 $HOME 和 ~ 为实际路径。"""
    return os.path.expandvars(os.path.expanduser(p))


def load_sync_paths():
    """读取 .sync-paths.json，返回 {模块名: 路径} 字典。"""
    config_path = os.path.join(REPO_DIR, '.sync-paths.json')
    if os.path.isfile(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def get_source_dir(mod_key, mod_config):
    """
    确定模块的源目录。优先级：
    1. .sync-paths.json 中的配置（按模块中文名查找）
    2. MODULES 中的 default_source
    如果目录不存在，返回 None（跳过该模块）。
    """
    sync_paths = load_sync_paths()
    mod_name = mod_config['name']

    # 优先用 .sync-paths.json 配置
    if mod_name in sync_paths:
        path = expand_path(sync_paths[mod_name])
        if os.path.isdir(path):
            return path

    # 其次用默认路径
    default = expand_path(mod_config['default_source'])
    if os.path.isdir(default):
        return default

    return None


# ─── 文件复制 ─────────────────────────────────────────────────────────────────────

def smart_cp(src, dst_dir):
    """
    只在文件内容有变化时才复制（避免刷新未改动文件的修改时间）。
    兜底：源文件 mtime 更新时强制复制（防 Pencil MCP 延迟写入导致 cmp 误判）。
    """
    dst = os.path.join(dst_dir, os.path.basename(src))
    if not os.path.isfile(dst):
        shutil.copy2(src, dst)
        _updated_files.add(os.path.relpath(dst, REPO_DIR))
        return True
    # 内容不同 → 复制
    if not files_equal(src, dst):
        shutil.copy2(src, dst)
        _updated_files.add(os.path.relpath(dst, REPO_DIR))
        return True
    # 内容相同但源更新 → 复制（mtime 兜底）
    if os.path.getmtime(src) > os.path.getmtime(dst):
        shutil.copy2(src, dst)
        _updated_files.add(os.path.relpath(dst, REPO_DIR))
        return True
    return False


def files_equal(a, b):
    """二进制比较两个文件是否相同。"""
    try:
        with open(a, 'rb') as fa, open(b, 'rb') as fb:
            while True:
                chunk_a = fa.read(8192)
                chunk_b = fb.read(8192)
                if chunk_a != chunk_b:
                    return False
                if not chunk_a:
                    return True
    except IOError:
        return False


def sync_subdir(source_dir, target_dir, subdir, extensions):
    """同步源目录下某个子目录的指定扩展名文件。"""
    src_path = os.path.join(source_dir, subdir)
    if not os.path.isdir(src_path):
        return
    dst_path = os.path.join(REPO_DIR, target_dir, subdir)
    os.makedirs(dst_path, exist_ok=True)
    for ext in extensions:
        for f in globmod.glob(os.path.join(src_path, f'*{ext}')):
            if os.path.isfile(f):
                smart_cp(f, dst_path)


def sync_module_files(source_dir, target_dir, mod_key):
    """复制模块的所有产物文件到 looply-docs 目标目录。"""

    # 调研
    sync_subdir(source_dir, target_dir, '调研', ['.md'])

    # 产品架构图
    sync_subdir(source_dir, target_dir, '产品架构图', ['.svg'])

    # 实体关系图
    sync_subdir(source_dir, target_dir, '实体关系图', ['.svg'])
    # HTML 格式：商品模块不同步，其他模块同步
    if target_dir != 'docs-商品系统':
        sync_subdir(source_dir, target_dir, '实体关系图', ['.html'])

    # 系统流程图
    sync_subdir(source_dir, target_dir, '系统流程图', ['.svg'])

    # PRD
    src_prd = os.path.join(source_dir, 'PRD')
    if os.path.isdir(src_prd):
        dst_prd = os.path.join(REPO_DIR, target_dir, 'PRD')
        os.makedirs(dst_prd, exist_ok=True)
        for ext in ['.docx', '.md']:
            for f in globmod.glob(os.path.join(src_prd, f'*{ext}')):
                if os.path.isfile(f):
                    smart_cp(f, dst_prd)
        # 用版本号（而非 mtime）选取最新 md 作为 latest.md
        latest_md = find_latest_prd_md(src_prd)
        if latest_md:
            dst_latest = os.path.join(dst_prd, 'latest.md')
            src_latest = os.path.join(src_prd, latest_md)
            if not os.path.isfile(dst_latest) or not files_equal(src_latest, dst_latest):
                shutil.copy2(src_latest, dst_latest)

    # 评审记录
    sync_subdir(source_dir, target_dir, '评审记录', ['.md'])

    # 验收记录
    sync_subdir(source_dir, target_dir, '验收记录', ['.md'])

    # UI 设计稿
    sync_subdir(source_dir, target_dir, 'UI', ['.pen'])

    # 原型（HTML + 图片）
    sync_subdir(source_dir, target_dir, '原型', ['.html', '.png', '.jpg', '.svg'])

    # 变更日志
    dst_root = os.path.join(REPO_DIR, target_dir)
    for f in globmod.glob(os.path.join(source_dir, 'looply-*变更日志*.md')):
        if os.path.isfile(f):
            smart_cp(f, dst_root)

    # 交付包 zip
    for f in globmod.glob(os.path.join(source_dir, '*交付开发*.zip')):
        if os.path.isfile(f):
            smart_cp(f, dst_root)

    # 核心差异汇总
    for delivery_dir in globmod.glob(os.path.join(source_dir, '交付开发*')):
        if os.path.isdir(delivery_dir):
            for f in globmod.glob(os.path.join(delivery_dir, '*核心差异*.md')):
                if os.path.isfile(f):
                    smart_cp(f, dst_root)


def find_latest_prd_md(prd_dir):
    """用版本号（而非 mtime）找到 PRD 目录下版本最高的 .md 文件。"""
    best_file = None
    best_ver = (0,)
    for fname in os.listdir(prd_dir):
        if not fname.endswith('.md') or fname == 'latest.md':
            continue
        m = re.search(r'[vV](\d+(?:\.\d+)?)', fname)
        if m:
            ver = tuple(int(x) for x in m.group(1).split('.'))
            if ver > best_ver:
                best_ver = ver
                best_file = fname
    # 如果没有带版本号的文件，fallback 到 mtime
    if not best_file:
        md_files = [f for f in os.listdir(prd_dir)
                    if f.endswith('.md') and f != 'latest.md']
        if md_files:
            best_file = max(md_files,
                           key=lambda f: os.path.getmtime(os.path.join(prd_dir, f)))
    return best_file


# ─── 版本检测与 index.html 更新 ──────────────────────────────────────────────────
# （原 update-index.py 的逻辑，整合到此处）

def parse_version(ver_str):
    """解析版本号为可比较的元组。"""
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
    """扫描目录，返回所有匹配文件，按版本号降序。"""
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


def update_prototype_config(latest_prototypes):
    """重写 prototype-config.js。"""
    config_path = os.path.join(REPO_DIR, 'prototype-config.js')
    current = {}
    if os.path.exists(config_path):
        content = open(config_path, 'r', encoding='utf-8').read()
        for m in re.finditer(r"'(\w+)':\s*'([^']+)'", content):
            current[m.group(1)] = m.group(2)
    for key, path in latest_prototypes.items():
        if path:
            current[key] = path
    key_order = ['product', 'market', 'inventory', 'translation', 'exchange', 'user', 'pdp']
    lines = []
    keys_present = [k for k in key_order if k in current]
    if not keys_present:
        return
    max_key_len = max(len(k) for k in keys_present)
    for key in key_order:
        if key in current:
            padding = ' ' * (max_key_len - len(key) + 1)
            lines.append(f"  '{key}':{padding}'{current[key]}'")
    output = """/**
 * Looply 后台原型路径配置（单一数据源）
 *
 * 此文件由 sync.py 自动生成，请勿手动修改。
 */
var PROTOTYPE_CONFIG = {
""" + ',\n'.join(lines) + ',\n};\n'
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(output)


def update_index_html(updates, all_versions, all_history=None):
    """更新 index.html：替换链接、版本号、日期、历史版本列表。"""
    index_path = os.path.join(REPO_DIR, 'index.html')
    lines = open(index_path, 'r', encoding='utf-8').readlines()
    changed = False

    # 第一遍：替换 href
    item_map = {}
    changed_items = set()
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
                    if current_item_start is not None:
                        item_map[current_item_start] = upd
                    if old_filename != new_file:
                        lines[i] = lines[i][:match.start()] + match.group(1) + new_file + match.group(3) + lines[i][match.end():]
                        changed = True
                        if current_item_start is not None:
                            changed_items.add(current_item_start)
                    elif current_item_start is not None:
                        rel_path = os.path.join(href_dir, new_file)
                        if rel_path in _updated_files:
                            changed_items.add(current_item_start)

    # 第二遍：更新版本号和日期
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
        if current_item_start in item_map and 'doc-name' in line and '<span class="badge">' in line:
            upd = item_map[current_item_start]
            new_ver = upd.get('new_ver', '')
            if new_ver:
                ver_regex = re.compile(r'(?<=\s)[vV].+?(?=\s*<span)')
                ver_match = ver_regex.search(new_line)
                if ver_match:
                    old_ver_text = ver_match.group(0)
                    new_ver_text = f'v{new_ver}'
                    if old_ver_text != new_ver_text:
                        new_line = new_line[:ver_match.start()] + new_ver_text + new_line[ver_match.end():]
                        changed = True
        if current_item_start in changed_items and 'doc-desc' in new_line and '更新于' in new_line:
            today = datetime.now().strftime('%Y-%m-%d')
            new_line = re.sub(r'更新于 \d{4}-\d{2}-\d{2}(\s+\d{2}:\d{2})?', f'更新于 {today}', new_line)
            if new_line != line:
                changed = True
        if 'doc-desc' in new_line and '含 PRD' in new_line:
            for mod_key, mod_config in MODULES.items():
                mod_dir = mod_config['target']
                mod_keywords_map = {
                    'market': 'market', 'product': '商品', 'inventory': '库存',
                    'translation': '翻译', 'exchange': '汇率', 'user': '用户', 'login': '登录注册',
                }
                keyword = mod_keywords_map.get(mod_key, mod_config['name'])
                recent = ''.join(new_lines[-10:])
                if mod_dir not in recent and keyword not in recent:
                    continue
                prd_ver = all_versions.get((mod_key, 'prd')) or all_versions.get((mod_key, 'prd_md'))
                if prd_ver:
                    new_line = re.sub(r'PRD [vV][\d.]+', f'PRD V{prd_ver}', new_line)
                proto_ver = all_versions.get((mod_key, 'prototype'))
                if proto_ver:
                    new_line = re.sub(r'后台原型 [vV][\w.-]+', f'后台原型 v{proto_ver}', new_line)
                    new_line = re.sub(r'原型 [vV][\w.-]+', f'原型 v{proto_ver}', new_line)
                er_ver = all_versions.get((mod_key, 'er'))
                if er_ver:
                    new_line = re.sub(r'ER图 [vV][\d.]+', f'ER图 v{er_ver}', new_line)
                arch_ver = all_versions.get((mod_key, 'architecture'))
                if arch_ver:
                    new_line = re.sub(r'架构图 [vV][\d.]+', f'架构图 v{arch_ver}', new_line)
                flow_ver = all_versions.get((mod_key, 'flowchart'))
                if flow_ver:
                    new_line = re.sub(r'流程图 [vV][\d.]+', f'流程图 v{flow_ver}', new_line)
            if new_line != line:
                changed = True
        if '</li>' in new_line and current_item_start is not None:
            current_item_start = None
        new_lines.append(new_line)

    # 第三遍：历史版本列表
    if all_history:
        HISTORY_ITEM_FMT = {
            'prototype': ('v', 'target="_blank"', '查看'),
            'er': ('v', 'target="_blank"', '查看'),
            'architecture': ('v', 'target="_blank"', '查看'),
            'flowchart': ('v', 'target="_blank"', '查看'),
            'prd': ('V', 'download', 'Markdown'),
            'prd_html': ('V', 'download', 'HTML'),
            'prd_md': ('V', 'download', 'Markdown'),
            'delivery': ('V', 'download', '下载'),
        }
        final_lines = []
        i = 0
        while i < len(new_lines):
            line = new_lines[i]
            matched_key = None
            if '</ul>' in line and i >= 2:
                lookback = ''.join(new_lines[max(0, i-8):i+1])
                if 'history-list' not in lookback:
                    for (mk, art_type), hist_info in all_history.items():
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
                            href_m = re.search(r'href="' + re.escape(href_prefix) + r'([^"]+)"', lookback)
                            if href_m and re.match(file_pattern, href_m.group(1)):
                                matched_key = (mk, art_type)
                                break
                        else:
                            matched_key = (mk, art_type)
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
                final_lines.append(line)
                i += 1
                existing_lines = []
                existing_hrefs = set()
                if i < len(new_lines) and 'history-toggle' in new_lines[i]:
                    i += 1
                    while i < len(new_lines):
                        hist_line = new_lines[i]
                        if 'history-item' in hist_line:
                            # Filter out entries whose files no longer exist or match current latest
                            keep = True
                            for href_m in re.finditer(r'href="([^"]+)"', hist_line):
                                href_path = os.path.join(REPO_DIR, href_m.group(1))
                                if not os.path.isfile(href_path):
                                    keep = False
                                    break
                                # Also skip if same as current latest
                                latest_ver = all_versions.get(matched_key)
                                if latest_ver and href_prefix in href_m.group(1):
                                    latest_file_candidates = [f for f, v in history] if history else []
                                    current_latest = all_versions.get(matched_key)
                                    if current_latest and f'{ver_prefix}{current_latest}' in hist_line.split('<')[0]:
                                        keep = False
                                        break
                            if keep:
                                existing_lines.append(hist_line)
                                for href_m in re.finditer(r'href="([^"]+)"', hist_line):
                                    existing_hrefs.add(href_m.group(1))
                        if '</ul>' in hist_line:
                            i += 1
                            break
                        i += 1
                new_items = []
                for hist_file, hist_ver in history:
                    href = f'{href_prefix}{hist_file}'
                    if href not in existing_hrefs:
                        new_items.append(f'          <li class="history-item">{ver_prefix}{hist_ver} <a href="{href}" {link_attr}>{link_label}</a></li>\n')
                if new_items or existing_lines:
                    indent = '        '
                    final_lines.append(f'{indent}<div class="history-toggle" onclick="this.nextElementSibling.classList.toggle(\'open\')">历史版本 ▾</div>\n')
                    final_lines.append(f'{indent}<ul class="doc-list history-list">\n')
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


def update_prd_index_topbar():
    """扫描各模块 PRD/latest.md 提取版本号，同步更新 PRD/index.html 的 topbar 标题。"""
    prd_dirs = globmod.glob(os.path.join(REPO_DIR, 'docs*/PRD'))
    prd_dirs += globmod.glob(os.path.join(REPO_DIR, 'docs/PRD'))
    changed_count = 0
    for prd_dir in prd_dirs:
        latest_md = os.path.join(prd_dir, 'latest.md')
        index_html = os.path.join(prd_dir, 'index.html')
        if not os.path.isfile(latest_md) or not os.path.isfile(index_html):
            continue
        version = None
        with open(latest_md, 'r', encoding='utf-8') as f:
            for line in f.readlines()[:10]:
                m = re.search(r'[版本]\s*[:：]\s*[vV]?([\d.]+)', line)
                if not m:
                    m = re.search(r'PRD\s+[vV]([\d.]+)', line)
                if m:
                    version = m.group(1)
                    break
        if not version:
            continue
        content = open(index_html, 'r', encoding='utf-8').read()
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


# ─── 主流程 ────────────────────────────────────────────────────────────────────

def main():
    # 解析命令行参数
    module_filter = sys.argv[1:] if len(sys.argv) > 1 else []

    print('=== sync.py: Looply 文档同步 ===')

    # Phase 1: 文件复制
    print('\n[Phase 1] 复制文件...')
    synced_modules = []

    for mod_key, mod_config in MODULES.items():
        # 模块筛选
        if module_filter:
            matched = any(
                kw in mod_key or
                kw in mod_config['name'] or
                any(kw in k for k in mod_config['keywords'])
                for kw in module_filter
            )
            if not matched:
                continue

        source_dir = get_source_dir(mod_key, mod_config)
        if not source_dir:
            continue

        target_dir = mod_config['target']
        print(f'  {mod_config["name"]}: {source_dir} → {target_dir}')
        sync_module_files(source_dir, target_dir, mod_key)
        synced_modules.append(mod_key)

    if not synced_modules:
        print('  没有找到可同步的模块（源目录不存在或未配置路径）')

    # Phase 2: 版本检测与 index.html 更新
    print('\n[Phase 2] 检测最新版本...')
    latest_prototypes = {}
    index_updates = []
    all_versions = {}
    all_history = {}

    for mod_key, mod_config in MODULES.items():
        if module_filter:
            matched = any(
                kw in mod_key or
                kw in mod_config['name'] or
                any(kw in k for k in mod_config['keywords'])
                for kw in module_filter
            )
            if not matched:
                continue

        module_dir = mod_config['target']
        config_key = mod_config.get('config_key')

        for art_type, art_config in mod_config.get('artifacts', {}).items():
            if art_config.get('no_version'):
                continue
            subdir = art_config['subdir']
            pattern = art_config['pattern']
            exclude = art_config.get('exclude')

            latest_file, latest_ver = find_latest_file(module_dir, subdir, pattern, exclude)
            if not latest_file:
                continue

            print(f'  {mod_config["name"]}/{art_type}: {latest_file} (v{latest_ver})')
            all_versions[(mod_key, art_type)] = latest_ver

            all_files = find_all_files(module_dir, subdir, pattern, exclude)
            if len(all_files) > 1:
                all_history[(mod_key, art_type)] = {
                    'dir': module_dir,
                    'subdir': subdir,
                    'history': all_files[1:],
                    'art_type': art_type,
                    'file_pattern': pattern,
                }

            if art_type == 'prototype' and config_key:
                if subdir == '.':
                    rel_path = f'{module_dir}/{latest_file}'
                else:
                    rel_path = f'{module_dir}/{subdir}/{latest_file}'
                latest_prototypes[config_key] = rel_path

            if subdir == '.':
                href_dir = f'{module_dir}/'
            else:
                href_dir = f'{module_dir}/{subdir}/'

            index_updates.append({
                'href_dir': href_dir,
                'file_pattern': pattern,
                'new_file': latest_file,
                'new_ver': latest_ver,
                'mod_name': mod_key,
                'art_type': art_type,
            })

    if latest_prototypes:
        update_prototype_config(latest_prototypes)
        print('  [更新] prototype-config.js')

    if index_updates:
        update_index_html(index_updates, all_versions, all_history)

    update_prd_index_topbar()

    # Phase 3: Git
    print('\n[Phase 3] Git 提交...')
    os.chdir(REPO_DIR)
    status = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
    if status.stdout.strip():
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        subprocess.run(['git', 'add', '-A'], check=True)
        subprocess.run(['git', 'commit', '-m', f'sync: 文档更新 {timestamp}'], check=True)
        result = subprocess.run(['git', 'push', 'origin', 'main'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f'  [完成] 已同步并推送 ({timestamp})')
        else:
            print(f'  [失败] push 失败，可能需要先 pull:\n{result.stderr}')
            sys.exit(1)
    else:
        print('  [无变化] 没有文件更新')


if __name__ == '__main__':
    main()
