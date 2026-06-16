#!/usr/bin/env python3
"""
Looply 地址库管理 实体关系图 SVG 生成脚本

用法：
  python3 gen_address_er_v1.5.py

产出：looply-地址库管理实体关系图-v1.5.dot + .svg（含 JSON + YAML 双 metadata）

前置依赖：
  - brew install graphviz
  - pip3 install graphviz pyyaml

变更记录 v1.5：
  - 新增 address_field_registry（地址字段注册表）：
    - 作为字段的"单一事实来源"，后台配置和校验规则都引用它
    - 包含所有超集字段（含预留字段：alternate_phone_*, district, building_name）
    - 新增 admin_division_level 字段：声明与行政区划层级的映射关系（数据驱动，不硬编码）
  - address_field_validation_rules 新增字段：
    - execute_on: 执行端(client/server/both)
    - severity: 严重程度(error/warning)
  - 新增关系线：
    - address_field_registry → country_address_config（字段注册 → 国家配置引用）
    - address_field_registry → address_field_validation_rules（字段注册 → 校验规则引用）
    - address_field_registry → administrative_division（字段注册 → 行政区划层级映射）
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
# 数据区
# ============================================================

TITLE = 'Looply · 地址库管理 实体关系图'
VERSION = 'v1.5 · 2026-05-17'
OUTPUT_NAME = 'looply-地址库管理实体关系图-v1.5'

LAYERS = {
    'core': {
        'label': '核心层 — 地址数据',
        'fillcolor': '#EBF3FB', 'color': '#a3c4e9', 'fontcolor': '#4A90D9',
        'header_bg': '#4A90D9',
    },
    'config': {
        'label': '配置层 — 字段注册与校验规则',
        'fillcolor': '#FDF2E9', 'color': '#f2c9a3', 'fontcolor': '#E8833A',
        'header_bg': '#E8833A',
    },
    'external': {
        'label': '外部依赖（引用）',
        'fillcolor': '#F3E5F5', 'color': '#ce93d8', 'fontcolor': '#7B1FA2',
        'header_bg': '#7B1FA2',
    },
}

MAPPING_HEADER_BG = '#546E7A'

ENTITIES = [
    {
        'id': 'address', 'name': '用户地址', 'layer': 'core',
        'note': '核心实体，超集字段设计支持多国扩展',
        'fields': [
            {'col': 'id', 'n': '主键 UUID', 'constraint': 'PK'},
            {'col': 'user_id', 'n': '关联用户', 'constraint': 'FK'},
            {'col': 'country_code', 'n': 'ISO 3166-1 国家代码', 'constraint': 'FK'},
            {'col': 'address_type', 'n': '类型(shipping/billing)', 'constraint': ''},
            {'col': 'recipient_first_name', 'n': '收件人名', 'constraint': ''},
            {'col': 'recipient_last_name', 'n': '收件人姓', 'constraint': ''},
            {'col': 'recipient_name', 'n': '完整姓名(冗余拼接)', 'constraint': ''},
            {'col': 'phone_country', 'n': '电话区号(+1)', 'constraint': ''},
            {'col': 'phone_number', 'n': '电话号码', 'constraint': ''},
            {'col': 'alternate_phone_country', 'n': '备用电话区号(中东预留)', 'constraint': ''},
            {'col': 'alternate_phone_number', 'n': '备用电话号码(中东预留)', 'constraint': ''},
            {'col': 'address_line1', 'n': '地址行1(街道)', 'constraint': ''},
            {'col': 'address_line2', 'n': '地址行2(公寓)', 'constraint': ''},
            {'col': 'city', 'n': '城市', 'constraint': ''},
            {'col': 'state_province', 'n': '州/省', 'constraint': ''},
            {'col': 'postal_code', 'n': '邮政编码', 'constraint': ''},
            {'col': 'district', 'n': '区/町(亚洲地址预留)', 'constraint': ''},
            {'col': 'building_name', 'n': '建筑名称(日本预留)', 'constraint': ''},
            {'col': 'is_default', 'n': '是否默认地址', 'constraint': ''},
            {'col': 'place_id', 'n': 'Google Place ID', 'constraint': 'UK'},
            {'col': 'latitude', 'n': '纬度', 'constraint': ''},
            {'col': 'longitude', 'n': '经度', 'constraint': ''},
            {'col': 'verified', 'n': '是否已验证(V1.1预留)', 'constraint': ''},
            {'col': 'verified_at', 'n': '验证时间', 'constraint': ''},
            {'col': 'verified_source', 'n': '验证来源(google/usps/loqate)', 'constraint': ''},
            {'col': 'created_at', 'n': '创建时间', 'constraint': ''},
            {'col': 'updated_at', 'n': '更新时间', 'constraint': ''},
        ],
    },
    {
        'id': 'address_field_registry', 'name': '地址字段注册表', 'layer': 'config',
        'note': '字段单一事实来源，后台配置/校验规则/前端表单均引用此表',
        'fields': [
            {'col': 'id', 'n': '主键 UUID', 'constraint': 'PK'},
            {'col': 'field_name', 'n': '字段标识(=address表列名)', 'constraint': 'UK'},
            {'col': 'field_type', 'n': '字段类型(text/select/phone)', 'constraint': ''},
            {'col': 'category', 'n': '分类(recipient/address/geo)', 'constraint': ''},
            {'col': 'display_name', 'n': '后台展示名', 'constraint': ''},
            {'col': 'admin_division_level', 'n': '关联行政区划层级(NULL=不关联)', 'constraint': ''},
            {'col': 'max_length', 'n': '数据库列最大长度', 'constraint': ''},
            {'col': 'description', 'n': '后台说明(给运营)', 'constraint': ''},
            {'col': 'created_at', 'n': '创建时间', 'constraint': ''},
        ],
    },
    {
        'id': 'country_address_config', 'name': '国家地址配置', 'layer': 'config',
        'note': '定义各国地址字段的可见性、必填性和顺序',
        'fields': [
            {'col': 'id', 'n': '主键 UUID', 'constraint': 'PK'},
            {'col': 'country_code', 'n': '国家代码(引用market)', 'constraint': 'FK,UK'},
            {'col': 'enabled', 'n': '是否启用', 'constraint': ''},
            {'col': 'field_config', 'n': '字段配置(JSON: visible+required_level)', 'constraint': ''},
            {'col': 'field_order', 'n': '字段顺序(JSON)', 'constraint': ''},
            {'col': 'field_i18n_keys', 'n': '字段国际化文案Key(JSON)', 'constraint': ''},
            {'col': 'created_at', 'n': '创建时间', 'constraint': ''},
            {'col': 'updated_at', 'n': '更新时间', 'constraint': ''},
        ],
    },
    {
        'id': 'address_field_validation_rules', 'name': '地址字段校验规则', 'layer': 'config',
        'note': '技术校验(格式/长度)，按priority顺序执行。唯一约束: (country_code, field_name, rule_type, priority)',
        'fields': [
            {'col': 'id', 'n': '主键 UUID', 'constraint': 'PK'},
            {'col': 'country_code', 'n': '国家代码', 'constraint': 'FK'},
            {'col': 'field_name', 'n': '字段名(引用registry)', 'constraint': 'FK'},
            {'col': 'rule_type', 'n': '规则类型(pattern/length/custom)', 'constraint': ''},
            {'col': 'priority', 'n': '执行优先级(值小先执行)', 'constraint': ''},
            {'col': 'pattern', 'n': '正则表达式(pattern/custom时使用)', 'constraint': ''},
            {'col': 'min_length', 'n': '最小长度(length时使用)', 'constraint': ''},
            {'col': 'max_length', 'n': '最大长度(length时使用)', 'constraint': ''},
            {'col': 'execute_on', 'n': '执行端(client/server/both)', 'constraint': ''},
            {'col': 'severity', 'n': '严重程度(error/warning)', 'constraint': ''},
            {'col': 'error_message', 'n': '错误提示文案', 'constraint': ''},
            {'col': 'error_message_i18n_key', 'n': '多语言key', 'constraint': ''},
            {'col': 'enabled', 'n': '是否启用', 'constraint': ''},
            {'col': 'created_at', 'n': '创建时间', 'constraint': ''},
            {'col': 'updated_at', 'n': '更新时间', 'constraint': ''},
        ],
    },
    {
        'id': 'administrative_division', 'name': '行政区划层级', 'layer': 'config',
        'note': '各国行政区划树形数据(州/市/区)，支撑下拉选择',
        'fields': [
            {'col': 'id', 'n': '主键 UUID', 'constraint': 'PK'},
            {'col': 'country_code', 'n': '国家代码', 'constraint': 'FK'},
            {'col': 'level', 'n': '层级(1=州/省 2=市 3=区)', 'constraint': ''},
            {'col': 'code', 'n': '行政区划代码', 'constraint': 'UK'},
            {'col': 'name', 'n': '名称', 'constraint': ''},
            {'col': 'name_local', 'n': '本地语言名称', 'constraint': ''},
            {'col': 'parent_id', 'n': '父级ID(自引用)', 'constraint': 'FK'},
            {'col': 'enabled', 'n': '是否启用', 'constraint': ''},
            {'col': 'sort_order', 'n': '排序权重', 'constraint': ''},
            {'col': 'created_at', 'n': '创建时间', 'constraint': ''},
            {'col': 'updated_at', 'n': '更新时间', 'constraint': ''},
        ],
    },
    {
        'id': 'postal_code_mapping', 'name': '邮编映射表', 'layer': 'config',
        'header_bg': MAPPING_HEADER_BG,
        'note': '邮编→城市/州反查，前端用于城市/州/邮编联动校验。导入时校验state_code须存在于administrative_division(level=1)',
        'fields': [
            {'col': 'id', 'n': '主键 UUID', 'constraint': 'PK'},
            {'col': 'country_code', 'n': '国家代码', 'constraint': 'FK'},
            {'col': 'postal_code', 'n': '邮政编码', 'constraint': 'UK'},
            {'col': 'city', 'n': '城市', 'constraint': ''},
            {'col': 'state_code', 'n': '州/省代码', 'constraint': ''},
            {'col': 'created_at', 'n': '创建时间', 'constraint': ''},
            {'col': 'updated_at', 'n': '更新时间', 'constraint': ''},
        ],
    },
    {
        'id': 'user', 'name': '用户(外部)', 'layer': 'external',
        'note': '用户模块提供，地址库引用user_id',
        'fields': [
            {'col': 'id', 'n': '用户ID', 'constraint': 'PK'},
            {'col': 'email', 'n': '邮箱', 'constraint': ''},
            {'col': 'status', 'n': '账户状态', 'constraint': ''},
        ],
    },
    {
        'id': 'country', 'name': '国家(market模块)', 'layer': 'external',
        'note': 'MARKET模块提供，地址库引用country_code',
        'fields': [
            {'col': 'country_code', 'n': 'ISO 3166-1 alpha-2', 'constraint': 'PK'},
            {'col': 'name', 'n': '国家名称', 'constraint': ''},
            {'col': 'enabled', 'n': '是否启用', 'constraint': ''},
            {'col': 'currency_code', 'n': '货币代码', 'constraint': ''},
        ],
    },
]

RELATIONS = [
    {'from': 'user', 'to': 'address', 'type': '1:N', 'label': '拥有多个地址', 'color': '#1565C0', 'penwidth': 1.8},
    {'from': 'country', 'to': 'address', 'type': '1:N', 'label': '地址所属国家', 'color': '#7B1FA2', 'penwidth': 1.4},
    {'from': 'country', 'to': 'country_address_config', 'type': '1:1', 'label': '国家字段配置', 'color': '#7B1FA2', 'penwidth': 1.4},
    {'from': 'country', 'to': 'address_field_validation_rules', 'type': '1:N', 'label': '校验规则(按国家)', 'color': '#E8833A', 'penwidth': 1.4},
    {'from': 'country', 'to': 'postal_code_mapping', 'type': '1:N', 'label': '邮编数据', 'color': '#7B1FA2', 'penwidth': 1.4},
    {'from': 'country', 'to': 'administrative_division', 'type': '1:N', 'label': '行政区划数据', 'color': '#7B1FA2', 'penwidth': 1.4},
    {'from': 'administrative_division', 'to': 'administrative_division', 'type': '1:N', 'label': '父子层级(自引用)', 'color': '#E8833A', 'penwidth': 1.2, 'style': 'dashed'},
    {'from': 'address_field_registry', 'to': 'country_address_config', 'type': '1:N', 'label': 'field_config引用字段注册', 'color': '#2E7D32', 'penwidth': 1.4, 'style': 'dashed'},
    {'from': 'address_field_registry', 'to': 'address_field_validation_rules', 'type': '1:N', 'label': 'field_name引用注册表', 'color': '#2E7D32', 'penwidth': 1.4},
    {'from': 'address_field_registry', 'to': 'administrative_division', 'type': '1:N', 'label': 'admin_division_level映射', 'color': '#2E7D32', 'penwidth': 1.2, 'style': 'dashed'},
]

DESIGN_RULES = {
    'superset_fields': '超集字段设计：数据库包含所有国家字段，通过country_address_config控制展示',
    'field_registry': 'address_field_registry是字段的单一事实来源，后台配置页从此表读取可选字段列表',
    'admin_division_mapping': 'admin_division_level数据驱动行政区划映射：state_province→L1, city→L2, district→L3，不硬编码',
    'market_integration': '国家可用性引用market模块，地址库不独立维护国家列表',
    'frontend_i18n': '前端多语言采用i18n方案，数据库不存储多语言字段',
    'name_split': 'recipient_first_name + recipient_last_name 拆分存储，支持支付AVS和物流API',
    'name_concat': 'recipient_name 冗余存储拼接结果，拼接顺序由country_address_config.name_format控制',
    'address_type_enum': 'address_type 枚举值: shipping, billing',
    'verified_source_enum': 'verified_source 枚举值: google, usps, loqate',
    'soft_delete': '地址数据支持软删除(CCPA要求可彻底删除)',
    'encryption': 'phone_number, recipient_first_name, recipient_last_name 字段 AES-256 加密存储',
    'place_id_dedup': '通过 place_id 做地址去重(V1.1)',
    'mvp_scope': 'MVP只启用美国(US)，预留字段: alternate_phone_*, district, building_name, verified_*',
    'snapshot_ownership': '订单地址快照(order_address_snapshot)由订单模块管理，不在地址库ER图中体现',
    'validation_execute_on': 'execute_on区分前后端：client=前端实时校验, server=后端提交校验, both=前后端都执行',
    'validation_severity': 'severity区分拦截级别：error=硬拦截阻止保存, warning=软提示允许继续',
    'multi_rule_validation': '同一字段支持多条校验规则，按priority顺序执行，命中首个失败即返回对应error_message',
    'rule_type_enum': 'rule_type 枚举值: pattern(正则格式), length(长度范围), custom(自定义正则)。必填性不在此表',
    'field_config_structure': 'field_config JSON结构: {field_name: {visible: bool, required_level: "required"|"optional"|"hidden"}}，field_name必须存在于address_field_registry',
}


# ============================================================
# 渲染区
# ============================================================

FONT = 'PingFang SC, Microsoft YaHei, Helvetica, sans-serif'
DEFAULT_EDGE_COLOR = '#90CAF9'
DEFAULT_EDGE_FONTCOLOR = '#4A90D9'


def build_card_label(entity):
    """构建 HTML-like 卡片标签"""
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
        <TR><TD BGCOLOR="{header_bg}"><FONT COLOR="white"><B>{entity["name"]} {entity["id"]}</B></FONT></TD></TR>
        {rows}{note_row}</TABLE>
    >'''


def build_graph():
    """构建 Graphviz 图"""
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
    """构建结构化 metadata JSON"""
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
    """从 JSON metadata 生成技术 YAML"""
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
    """在 SVG 中嵌入 JSON + YAML 双 metadata"""
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')
    tree = ET.parse(svg_path)
    root = tree.getroot()

    meta_elem = ET.Element('metadata')

    schema_elem = ET.SubElement(meta_elem, 'er-schema')
    schema_elem.set('format', 'json')
    schema_elem.set('version', '1.3')
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
