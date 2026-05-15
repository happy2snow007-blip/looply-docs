#!/usr/bin/env python3
"""
looply 汇率管理实体关系图 SVG 生成脚本

用法：
  python3 gen_汇率管理_er.py

产出：
  - looply-汇率管理实体关系图.dot
  - looply-汇率管理实体关系图.svg（含 JSON + YAML 双 metadata）

前置依赖：
  - brew install graphviz
  - pip3 install graphviz pyyaml
"""
import graphviz
import json
import os
import re
import xml.etree.ElementTree as ET
import yaml

if os.path.isdir('/opt/homebrew/bin'):
    os.environ['PATH'] = '/opt/homebrew/bin:' + os.environ.get('PATH', '')

# ============================================================
# 数据区（唯一数据源）
# ============================================================

TITLE = 'looply · 汇率管理 实体关系图'
VERSION = 'v3.3 · 2026-05-14'
OUTPUT_NAME = 'looply-汇率管理实体关系图'

# --- 分层定义 ---
LAYERS = {
    'ref': {
        'label': '外部引用(币种管理模块)',
        'fillcolor': '#f3f4f6', 'color': '#9ca3af', 'fontcolor': '#6b7280',
        'header_bg': '#6b7280',
    },
    'source': {
        'label': '数据获取',
        'fillcolor': '#fef3c7', 'color': '#f59e0b', 'fontcolor': '#92400e',
        'header_bg': '#d97706',
    },
    'process': {
        'label': '数据加工',
        'fillcolor': '#dbeafe', 'color': '#3b82f6', 'fontcolor': '#1e40af',
        'header_bg': '#2563eb',
    },
    'publish': {
        'label': '发布与服务',
        'fillcolor': '#e0e7ff', 'color': '#6366f1', 'fontcolor': '#4338ca',
        'header_bg': '#4f46e5',
    },
    'audit': {
        'label': '审计与日志',
        'fillcolor': '#fee2e2', 'color': '#ef4444', 'fontcolor': '#991b1b',
        'header_bg': '#dc2626',
    },
}

# --- 实体定义 ---
ENTITIES = [
    {
        'id': 'currency', 'name': '币种主数据', 'layer': 'ref',
        'fields': [
            {'col': 'id', 'n': '主键', 'constraint': 'PK'},
            {'col': 'code', 'n': 'ISO 4217简码', 'constraint': 'UK'},
            {'col': 'symbol', 'n': '币种符号', 'constraint': ''},
            {'col': 'decimal_precision', 'n': '小数精度', 'constraint': ''},
            {'col': 'status', 'n': '启停状态', 'constraint': ''},
        ],
    },
    {
        'id': 'exchange_rate_source', 'name': '汇率数据源', 'layer': 'source',
        'fields': [
            {'col': 'id', 'n': '主键', 'constraint': 'PK'},
            {'col': 'name', 'n': '数据源名称', 'constraint': 'UK'},
            {'col': 'api_url', 'n': 'API地址', 'constraint': ''},
            {'col': 'api_key', 'n': 'API密钥(加密)', 'constraint': ''},
            {'col': 'priority', 'n': '优先级(主/备)', 'constraint': ''},
            {'col': 'fetch_interval', 'n': '拉取间隔(秒)', 'constraint': ''},
            {'col': 'status', 'n': '启停状态', 'constraint': ''},
            {'col': 'last_fetch_at', 'n': '最近拉取时间', 'constraint': ''},
            {'col': 'last_fetch_status', 'n': '最近拉取状态', 'constraint': ''},
            {'col': 'created_at', 'n': '创建时间', 'constraint': ''},
            {'col': 'updated_at', 'n': '更新时间', 'constraint': ''},
        ],
    },
    {
        'id': 'exchange_rate_raw', 'name': '原始汇率', 'layer': 'source',
        'note': 'UK: base + target + fetched_at; 直接采集仅USD→X; 派生记录source_id为空',
        'fields': [
            {'col': 'id', 'n': '主键', 'constraint': 'PK'},
            {'col': 'source_id', 'n': '数据源(派生为空)', 'constraint': 'FK'},
            {'col': 'base_currency_id', 'n': '基准币种', 'constraint': 'FK'},
            {'col': 'target_currency_id', 'n': '目标币种', 'constraint': 'FK'},
            {'col': 'source_type', 'n': '来源(直接采集/派生)', 'constraint': ''},
            {'col': 'market_rate', 'n': '中间价', 'constraint': ''},
            {'col': 'fetched_at', 'n': '采集/计算时间', 'constraint': ''},
            {'col': 'expires_at', 'n': '失效时间', 'constraint': ''},
            {'col': 'status', 'n': '状态(正常/异常)', 'constraint': ''},
        ],
    },
    {
        'id': 'spread_rule', 'name': '点差规则', 'layer': 'process',
        'note': '全局: base+target=NULL; 方向点差覆盖全局; UK: base+target',
        'fields': [
            {'col': 'id', 'n': '主键', 'constraint': 'PK'},
            {'col': 'base_currency_id', 'n': '基准币种(空=全局)', 'constraint': 'FK'},
            {'col': 'target_currency_id', 'n': '目标币种(空=全局)', 'constraint': 'FK'},
            {'col': 'spread_rate', 'n': '点差比例(如0.02)', 'constraint': ''},
            {'col': 'priority', 'n': '优先级', 'constraint': ''},
            {'col': 'status', 'n': '启停状态', 'constraint': ''},
            {'col': 'created_at', 'n': '创建时间', 'constraint': ''},
            {'col': 'updated_at', 'n': '更新时间', 'constraint': ''},
        ],
    },
    {
        'id': 'exchange_rate_published', 'name': '已发布汇率', 'layer': 'publish',
        'note': 'UK: base + target; 同一有向币种对仅一条生效; 币种停用后置为 disabled_by_currency',
        'fields': [
            {'col': 'id', 'n': '主键', 'constraint': 'PK'},
            {'col': 'base_currency_id', 'n': '基准币种', 'constraint': 'FK'},
            {'col': 'target_currency_id', 'n': '目标币种', 'constraint': 'FK'},
            {'col': 'market_rate', 'n': '中间价(含派生)', 'constraint': ''},
            {'col': 'source_type', 'n': '来源(直接/逆向/交叉)', 'constraint': ''},
            {'col': 'spread_rate', 'n': '应用的点差', 'constraint': ''},
            {'col': 'published_rate', 'n': '平台汇率', 'constraint': ''},
            {'col': 'publish_type', 'n': '发布方式(定时/手动)', 'constraint': ''},
            {'col': 'published_by', 'n': '发布人(系统/运营)', 'constraint': ''},
            {'col': 'published_at', 'n': '发布时间', 'constraint': ''},
            {'col': 'status', 'n': '状态(生效/已替换/停用)', 'constraint': ''},
        ],
    },
    {
        'id': 'rate_change_log', 'name': '汇率变动日志', 'layer': 'audit',
        'note': '操作类型: 定时发布/手动发布/设置固定汇率/回滚/点差调整/币种停用; 同批次发布共享 batch_id',
        'fields': [
            {'col': 'id', 'n': '主键', 'constraint': 'PK'},
            {'col': 'snapshot_batch_id', 'n': '发布批次号(可空)', 'constraint': ''},
            {'col': 'target_currency_id', 'n': '目标币种', 'constraint': 'FK'},
            {'col': 'operation_type', 'n': '操作类型', 'constraint': ''},
            {'col': 'old_rate', 'n': '变更前汇率', 'constraint': ''},
            {'col': 'new_rate', 'n': '变更后汇率', 'constraint': ''},
            {'col': 'change_reason', 'n': '变更原因', 'constraint': ''},
            {'col': 'operator', 'n': '操作人', 'constraint': ''},
            {'col': 'created_at', 'n': '操作时间', 'constraint': ''},
        ],
    },
]

# --- 关系定义 ---
RELATIONS = [
    {'from': 'exchange_rate_raw', 'to': 'exchange_rate_source', 'type': 'N:1', 'label': '来源',
     'color': '#d97706', 'penwidth': 1.4},
    {'from': 'exchange_rate_raw', 'to': 'currency', 'type': 'N:1', 'label': '基准/目标币种',
     'color': '#6b7280', 'penwidth': 1.2},
    {'from': 'spread_rule', 'to': 'currency', 'type': 'N:1', 'label': '基准/目标币种(可空)',
     'color': '#2563eb', 'penwidth': 1.2, 'style': 'dashed'},
    {'from': 'exchange_rate_published', 'to': 'currency', 'type': 'N:1', 'label': '基准/目标币种',
     'color': '#4f46e5', 'penwidth': 1.4},
    {'from': 'exchange_rate_published', 'to': 'exchange_rate_raw', 'type': 'N:1', 'label': '加工来源',
     'color': '#2563eb', 'penwidth': 1.2, 'style': 'dashed'},
    {'from': 'exchange_rate_published', 'to': 'spread_rule', 'type': 'N:1', 'label': '应用点差',
     'color': '#2563eb', 'style': 'dashed'},
    {'from': 'rate_change_log', 'to': 'currency', 'type': 'N:1', 'label': '目标币种',
     'color': '#dc2626'},
    {'from': 'rate_change_log', 'to': 'exchange_rate_published', 'type': 'N:1', 'label': '关联发布记录',
     'color': '#dc2626', 'penwidth': 1.2, 'style': 'dashed'},
]

# --- 设计规则（嵌入 metadata 供技术参考）---
DESIGN_RULES = {
    'naming_alignment': '实体名、字段名与产品架构图保持一致',
    'currency_external': 'currency 实体来自币种管理模块，本模块只引用不创建',
    'raw_uniqueness': 'exchange_rate_raw 唯一键 (base_currency_id, target_currency_id, fetched_at)；直接采集仅 USD→X，派生记录 source_id 为空',
    'spread_rule_global': 'spread_rule 中 base/target 同时为空表示全局点差；方向点差按 priority 覆盖全局',
    'published_active_one': '同一有向币种对在 exchange_rate_published 中仅一条 status=active；币种停用时批量置为 disabled_by_currency',
    'rate_change_log_batch': '同一次发布批次的多币种变动共享 snapshot_batch_id，便于回滚整批',
}


# ============================================================
# 渲染区（一般不用动）
# ============================================================

FONT = 'PingFang SC, Microsoft YaHei, Helvetica, sans-serif'
DEFAULT_EDGE_COLOR = '#90CAF9'
DEFAULT_EDGE_FONTCOLOR = '#4A90D9'


def build_card_label(entity):
    layer = LAYERS[entity['layer']]
    header_bg = entity.get('header_bg', layer['header_bg'])

    rows = ''
    for f in entity['fields']:
        constraint_str = f'[{f["constraint"]}]' if f['constraint'] else ''
        rows += f'<TR><TD ALIGN="LEFT">{f["col"]} {f["n"]}</TD><TD>{constraint_str}</TD></TR>\n'

    note_row = ''
    if entity.get('note'):
        note_row = f'<TR><TD COLSPAN="2" BGCOLOR="#E3F2FD"><FONT POINT-SIZE="10"><I>{entity["note"]}</I></FONT></TD></TR>\n'

    return f'''<
      <TABLE BORDER="2" CELLBORDER="0" CELLSPACING="0" CELLPADDING="6">
        <TR><TD COLSPAN="2" BGCOLOR="{header_bg}"><FONT COLOR="white"><B>{entity["name"]} {entity["id"]}</B></FONT></TD></TR>
        {rows}{note_row}</TABLE>
    >'''


def build_graph():
    dot = graphviz.Digraph(
        name='ER',
        format='svg',
        engine='dot',
        graph_attr={
            'rankdir': 'LR',
            'fontname': FONT,
            'fontsize': '14',
            'bgcolor': '#f8f9fc',
            'pad': '0.8',
            'nodesep': '0.3',
            'ranksep': '0.6',
            'compound': 'true',
            'label': f'<<B>{TITLE}</B><BR/><FONT POINT-SIZE="10">{VERSION}</FONT>>',
            'labelloc': 't',
        },
        node_attr={
            'fontname': FONT,
            'shape': 'none',
            'margin': '0',
        },
        edge_attr={
            'fontname': FONT,
            'fontsize': '10',
            'color': '#999999',
            'arrowsize': '0.7',
            'penwidth': '1.0',
        },
    )

    for layer_id, layer_cfg in LAYERS.items():
        entities = [e for e in ENTITIES if e['layer'] == layer_id]
        if not entities:
            continue
        with dot.subgraph(name=f'cluster_{layer_id}') as sub:
            sub.attr(
                label=f'<<B>{layer_cfg["label"]}</B>>',
                style='filled,rounded',
                fillcolor=layer_cfg['fillcolor'],
                color=layer_cfg['color'],
                fontcolor=layer_cfg['fontcolor'],
                fontsize='14',
                penwidth='2.5',
                margin='16',
            )
            for entity in entities:
                sub.node(entity['id'], label=build_card_label(entity))

    for rel in RELATIONS:
        edge_attrs = {}
        label_text = f'{rel["type"]} {rel["label"]}'.strip() if rel['label'] else rel['type']
        edge_color = rel.get('color', DEFAULT_EDGE_COLOR)
        edge_attrs['color'] = edge_color
        edge_attrs['fontcolor'] = rel.get('color', DEFAULT_EDGE_FONTCOLOR)
        edge_attrs['label'] = label_text
        if rel.get('penwidth'):
            edge_attrs['penwidth'] = str(rel['penwidth'])
        if rel.get('style'):
            edge_attrs['style'] = rel['style']
        dot.edge(rel['from'], rel['to'], **edge_attrs)

    return dot


def build_metadata():
    tables = []
    for entity in ENTITIES:
        tables.append({
            'name': entity['id'],
            'comment': entity['name'],
            'columns': [
                {
                    'name': f['col'],
                    'comment': f['n'],
                    'constraint': ', '.join(
                        {'PK': 'PRIMARY KEY', 'FK': 'FOREIGN KEY', 'UK': 'UNIQUE'}[p]
                        for p in (x.strip() for x in f['constraint'].split(','))
                        if p in ('PK', 'FK', 'UK')
                    ) if f['constraint'] else '',
                }
                for f in entity['fields']
            ],
            'note': entity.get('note', ''),
        })

    return json.dumps({
        'title': TITLE,
        'version': VERSION,
        'tables': tables,
        'relations': RELATIONS,
        'design_rules': DESIGN_RULES,
    }, ensure_ascii=False, indent=2)


def build_tech_yaml(meta_json):
    data = json.loads(meta_json)

    def represent_none(dumper, _data):
        return dumper.represent_scalar('tag:yaml.org,2002:null', '')
    yaml.add_representer(type(None), represent_none)

    output = {
        'title': data['title'],
        'version': data['version'],
        'tables': [],
        'relations': data['relations'],
        'design_rules': data.get('design_rules', {}),
    }
    for table in data['tables']:
        t = {
            'name': table['name'],
            'comment': table['comment'],
            'note': table.get('note', ''),
            'columns': [],
        }
        for col in table['columns']:
            t['columns'].append({
                'name': col['name'],
                'comment': col['comment'],
                'constraint': col['constraint'] if col['constraint'] else None,
                'type': None,
                'nullable': None,
                'default': None,
                'enum_values': None,
                'index': None,
            })
        output['tables'].append(t)

    return yaml.dump(output, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)


def embed_metadata(svg_path, meta_json):
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')
    tree = ET.parse(svg_path)
    root = tree.getroot()

    meta_elem = ET.Element('metadata')

    schema_elem = ET.SubElement(meta_elem, 'er-schema')
    schema_elem.set('format', 'json')
    schema_elem.set('version', '1.0')
    schema_elem.text = '\n' + meta_json + '\n'

    yaml_str = build_tech_yaml(meta_json)
    tech_elem = ET.SubElement(meta_elem, 'er-tech-spec')
    tech_elem.set('format', 'yaml')
    tech_elem.text = yaml_str

    root.insert(0, meta_elem)
    tree.write(svg_path, encoding='unicode', xml_declaration=True)

    with open(svg_path, 'r', encoding='utf-8') as f:
        svg_content = f.read()
    svg_content = re.sub(
        r'<er-tech-spec format="yaml">(.*?)</er-tech-spec>',
        lambda m: f'<er-tech-spec format="yaml"><![CDATA[\n{yaml_str}]]></er-tech-spec>',
        svg_content, flags=re.DOTALL
    )
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)


def main():
    dot = build_graph()
    dot.render(OUTPUT_NAME, cleanup=False)
    print(f'Generated: {OUTPUT_NAME}.dot')
    print(f'Generated: {OUTPUT_NAME}.svg')

    svg_path = f'{OUTPUT_NAME}.svg'
    meta_json = build_metadata()
    embed_metadata(svg_path, meta_json)
    print(f'Metadata embedded into {svg_path} (JSON + YAML)')

    data = json.loads(meta_json)
    print(f'  Tables: {len(data["tables"])}')
    print(f'  Relations: {len(data["relations"])}')
    print(f'  Design rules: {len(data["design_rules"])}')


if __name__ == '__main__':
    main()
