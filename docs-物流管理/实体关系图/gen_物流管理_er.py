#!/usr/bin/env python3
"""
Looply 物流管理 实体关系图 SVG 生成脚本

用法：
  python3 gen_物流管理_er.py

产出：looply-物流管理实体关系图.dot + .svg（含 JSON + YAML 双 metadata）

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

# 确保 Graphviz 可执行文件在 PATH 中（macOS brew 安装路径）
if os.path.isdir('/opt/homebrew/bin'):
    os.environ['PATH'] = '/opt/homebrew/bin:' + os.environ.get('PATH', '')

# ============================================================
# 数据区（唯一数据源，改实体只改这里）
# ============================================================

TITLE = 'looply · 物流管理 实体关系图'
VERSION = 'v1.9 · 2026-05-13'
OUTPUT_NAME = 'looply-物流管理实体关系图'

# --- 分层定义 ---
LAYERS = {
    'external': {
        'label': '外部实体（订单/商品）',
        'fillcolor': '#FFF9E6', 'color': '#FFD54F', 'fontcolor': '#F57F17',
        'header_bg': '#FFA726',
    },
    'international': {
        'label': '国际段追踪',
        'fillcolor': '#E3F2FD', 'color': '#90CAF9', 'fontcolor': '#1565C0',
        'header_bg': '#1976D2',
    },
    'domestic': {
        'label': '国内段追踪',
        'fillcolor': '#F3E5F5', 'color': '#CE93D8', 'fontcolor': '#6A1B9A',
        'header_bg': '#8E24AA',
    },
    'carrier': {
        'label': '承运商配置',
        'fillcolor': '#E8F5E9', 'color': '#A5D6A7', 'fontcolor': '#2E7D32',
        'header_bg': '#43A047',
    },
    'delivery': {
        'label': '配送限制',
        'fillcolor': '#FFEBEE', 'color': '#EF9A9A', 'fontcolor': '#C62828',
        'header_bg': '#E53935',
    },
}

MAPPING_HEADER_BG = '#546E7A'

# --- 实体定义 ---
ENTITIES = [
    # ========== 外部实体 ==========
    {
        'id': 'orders', 'name': '订单', 'layer': 'external',
        'note': '外部实体：订单系统管理',
        'fields': [
            {'col': 'id', 'n': '订单ID', 'constraint': 'PK'},
            {'col': 'order_no', 'n': '订单号', 'constraint': 'UK'},
            {'col': 'status', 'n': '订单状态', 'constraint': ''},
            {'col': 'recipient_name', 'n': '收件人姓名', 'constraint': ''},
            {'col': 'recipient_phone', 'n': '收件人电话', 'constraint': ''},
            {'col': 'shipping_address_line1', 'n': '地址行1', 'constraint': ''},
            {'col': 'shipping_address_line2', 'n': '地址行2', 'constraint': ''},
            {'col': 'shipping_city', 'n': '城市', 'constraint': ''},
            {'col': 'shipping_state', 'n': '州/省', 'constraint': ''},
            {'col': 'shipping_zip', 'n': '邮编', 'constraint': ''},
            {'col': 'shipping_country', 'n': '国家代码', 'constraint': ''},
            {'col': 'total_amount', 'n': '订单金额', 'constraint': ''},
            {'col': 'created_at', 'n': '创建时间', 'constraint': ''},
            {'col': 'updated_at', 'n': '更新时间', 'constraint': ''},
        ],
    },
    {
        'id': 'order_items', 'name': '订单商品行', 'layer': 'external',
        'note': '外部实体：订单系统管理',
        'fields': [
            {'col': 'id', 'n': '商品行ID', 'constraint': 'PK'},
            {'col': 'order_id', 'n': '关联订单', 'constraint': 'FK'},
            {'col': 'product_id', 'n': '关联商品', 'constraint': 'FK'},
            {'col': 'quantity', 'n': '数量', 'constraint': ''},
            {'col': 'unit_price', 'n': '单价', 'constraint': ''},
            {'col': 'sku', 'n': 'SKU编码', 'constraint': ''},
        ],
    },
    {
        'id': 'products', 'name': '商品', 'layer': 'external',
        'note': '外部实体：商品系统管理',
        'fields': [
            {'col': 'id', 'n': '商品ID', 'constraint': 'PK'},
            {'col': 'sku', 'n': 'SKU编码', 'constraint': 'UK'},
            {'col': 'name', 'n': '商品名称', 'constraint': ''},
            {'col': 'category', 'n': '品类', 'constraint': ''},
            {'col': 'weight', 'n': '重量(kg)', 'constraint': ''},
            {'col': 'origin_country', 'n': '原产国', 'constraint': ''},
        ],
    },

    # ========== 国际段追踪 ==========
    {
        'id': 'shipments', 'name': '国际运单', 'layer': 'international',
        'fields': [
            {'col': 'id', 'n': '运单ID', 'constraint': 'PK'},
            {'col': 'order_id', 'n': '关联订单', 'constraint': 'FK'},
            {'col': 'tracking_no', 'n': '运单号', 'constraint': 'UK'},
            {'col': 'shipment_type', 'n': '发货类型', 'constraint': ''},
            {'col': 'carrier_id', 'n': '承运商', 'constraint': 'FK'},
            {'col': 'aftership_status', 'n': 'AfterShip一级tag', 'constraint': ''},
            {'col': 'internal_status', 'n': 'Looply内部状态', 'constraint': ''},
            {'col': 'destination', 'n': '目的地', 'constraint': ''},
            {'col': 'weight', 'n': '包裹重量(kg)', 'constraint': ''},
            {'col': 'remark', 'n': '备注（无SKU配件说明）', 'constraint': ''},
            {'col': 'shipped_at', 'n': '发货时间', 'constraint': ''},
            {'col': 'estimated_delivery_at', 'n': '预计送达时间', 'constraint': ''},
            {'col': 'delivered_at', 'n': '签收时间', 'constraint': ''},
            {'col': 'last_tracking_update', 'n': '最后轨迹更新时间', 'constraint': ''},
            {'col': 'created_at', 'n': '创建时间', 'constraint': ''},
            {'col': 'updated_at', 'n': '更新时间', 'constraint': ''},
        ],
    },
    {
        'id': 'shipment_items', 'name': '运单商品明细', 'layer': 'international',
        'header_bg': MAPPING_HEADER_BG,
        'note': '记录每个包裹包含哪些商品，支持拆包发货',
        'fields': [
            {'col': 'id', 'n': '明细ID', 'constraint': 'PK'},
            {'col': 'shipment_id', 'n': '关联运单', 'constraint': 'FK'},
            {'col': 'order_item_id', 'n': '关联订单商品行', 'constraint': 'FK'},
            {'col': 'quantity', 'n': '本包裹发货数量', 'constraint': ''},
            {'col': 'created_at', 'n': '创建时间', 'constraint': ''},
        ],
    },
    {
        'id': 'tracking_checkpoints', 'name': '国际轨迹节点', 'layer': 'international',
        'fields': [
            {'col': 'id', 'n': '节点ID', 'constraint': 'PK'},
            {'col': 'shipment_id', 'n': '关联运单', 'constraint': 'FK'},
            {'col': 'tag', 'n': 'AfterShip一级状态(原始)', 'constraint': ''},
            {'col': 'subtag', 'n': 'AfterShip二级状态(原始)', 'constraint': ''},
            {'col': 'message', 'n': '轨迹描述原文', 'constraint': ''},
            {'col': 'mapped_internal_status', 'n': '映射后Looply内部状态', 'constraint': ''},
            {'col': 'display_i18n_key', 'n': '映射后i18n key', 'constraint': ''},
            {'col': 'city', 'n': '城市', 'constraint': ''},
            {'col': 'state', 'n': '州/省', 'constraint': ''},
            {'col': 'zip', 'n': '邮编', 'constraint': ''},
            {'col': 'country_iso3', 'n': '国家代码', 'constraint': ''},
            {'col': 'location', 'n': '完整地点描述', 'constraint': ''},
            {'col': 'checkpoint_time', 'n': '事件时间', 'constraint': ''},
            {'col': 'created_at', 'n': '创建时间', 'constraint': ''},
        ],
    },

    # ========== 国内段追踪 ==========
    {
        'id': 'domestic_trackings', 'name': '国内运单', 'layer': 'domestic',
        'fields': [
            {'col': 'id', 'n': '国内运单ID', 'constraint': 'PK'},
            {'col': 'order_id', 'n': '关联订单', 'constraint': 'FK'},
            {'col': 'domestic_tracking_no', 'n': '国内运单号', 'constraint': 'UK'},
            {'col': 'domestic_carrier_id', 'n': '国内承运商', 'constraint': 'FK'},
            {'col': 'origin', 'n': '发货地', 'constraint': ''},
            {'col': 'destination', 'n': '目的地（上海仓）', 'constraint': ''},
            {'col': 'status', 'n': '状态', 'constraint': ''},
            {'col': 'remark', 'n': '备注（包裹内容说明）', 'constraint': ''},
            {'col': 'estimated_arrival', 'n': '预计到达', 'constraint': ''},
            {'col': 'actual_arrival', 'n': '实际到达', 'constraint': ''},
            {'col': 'created_at', 'n': '创建时间', 'constraint': ''},
            {'col': 'updated_at', 'n': '更新时间', 'constraint': ''},
        ],
    },
    {
        'id': 'domestic_checkpoints', 'name': '国内轨迹节点', 'layer': 'domestic',
        'fields': [
            {'col': 'id', 'n': '节点ID', 'constraint': 'PK'},
            {'col': 'domestic_tracking_id', 'n': '关联国内运单', 'constraint': 'FK'},
            {'col': 'message', 'n': '轨迹描述', 'constraint': ''},
            {'col': 'location', 'n': '地点', 'constraint': ''},
            {'col': 'event_type', 'n': '事件类型', 'constraint': ''},
            {'col': 'checkpoint_time', 'n': '事件时间', 'constraint': ''},
            {'col': 'created_at', 'n': '创建时间', 'constraint': ''},
        ],
    },
    {
        'id': 'domestic_carriers', 'name': '国内承运商', 'layer': 'domestic',
        'fields': [
            {'col': 'id', 'n': '承运商ID', 'constraint': 'PK'},
            {'col': 'name', 'n': '承运商名称', 'constraint': 'UK'},
            {'col': 'code', 'n': '编码', 'constraint': 'UK'},
            {'col': 'status', 'n': '状态', 'constraint': ''},
            {'col': 'created_at', 'n': '创建时间', 'constraint': ''},
        ],
    },

    # ========== 承运商配置 ==========
    {
        'id': 'carriers', 'name': '国际承运商', 'layer': 'carrier',
        'fields': [
            {'col': 'id', 'n': '承运商ID', 'constraint': 'PK'},
            {'col': 'name', 'n': '承运商名称', 'constraint': 'UK'},
            {'col': 'slug', 'n': 'AfterShip slug', 'constraint': 'UK'},
            {'col': 'tracking_platform_id', 'n': '归属追踪平台', 'constraint': 'FK'},
            {'col': 'status', 'n': '状态', 'constraint': ''},
            {'col': 'logo_url', 'n': 'Logo地址', 'constraint': ''},
            {'col': 'created_at', 'n': '创建时间', 'constraint': ''},
            {'col': 'updated_at', 'n': '更新时间', 'constraint': ''},
        ],
    },
    {
        'id': 'tracking_platforms', 'name': '追踪平台', 'layer': 'carrier',
        'fields': [
            {'col': 'id', 'n': '平台ID', 'constraint': 'PK'},
            {'col': 'name', 'n': '平台名称', 'constraint': 'UK'},
            {'col': 'api_key', 'n': 'API Key（加密）', 'constraint': ''},
            {'col': 'webhook_secret', 'n': 'Webhook密钥（加密）', 'constraint': ''},
            {'col': 'webhook_url', 'n': 'Webhook回调地址', 'constraint': ''},
            {'col': 'status', 'n': '状态', 'constraint': ''},
            {'col': 'last_synced_at', 'n': '最后同步时间', 'constraint': ''},
            {'col': 'created_at', 'n': '创建时间', 'constraint': ''},
            {'col': 'updated_at', 'n': '更新时间', 'constraint': ''},
        ],
    },
    {
        'id': 'status_mappings', 'name': '状态映射', 'layer': 'carrier',
        'header_bg': MAPPING_HEADER_BG,
        'note': '追踪平台一级/二级状态 → Looply内部状态的可配置映射，支持多语言展示',
        'fields': [
            {'col': 'id', 'n': '映射ID', 'constraint': 'PK'},
            {'col': 'tracking_platform_id', 'n': '关联追踪平台', 'constraint': 'FK'},
            {'col': 'platform_tag', 'n': '平台一级状态(tag)', 'constraint': ''},
            {'col': 'platform_tag_meaning', 'n': '一级状态含义', 'constraint': ''},
            {'col': 'platform_subtag', 'n': '平台二级状态(subtag)', 'constraint': ''},
            {'col': 'platform_subtag_meaning', 'n': '二级状态含义', 'constraint': ''},
            {'col': 'internal_status', 'n': 'Looply内部状态', 'constraint': ''},
            {'col': 'display_text_key', 'n': '买家端一级i18n key', 'constraint': ''},
            {'col': 'display_detail_key', 'n': '买家端二级i18n key', 'constraint': ''},
            {'col': 'sort_order', 'n': '排序', 'constraint': ''},
            {'col': 'created_at', 'n': '创建时间', 'constraint': ''},
            {'col': 'updated_at', 'n': '更新时间', 'constraint': ''},
        ],
    },

    # ========== 配送限制 ==========
    {
        'id': 'delivery_rules', 'name': '配送限制规则', 'layer': 'delivery',
        'fields': [
            {'col': 'id', 'n': '规则ID', 'constraint': 'PK'},
            {'col': 'rule_code', 'n': '规则编码', 'constraint': 'UK'},
            {'col': 'rule_name', 'n': '规则名称', 'constraint': ''},
            {'col': 'restriction_type', 'n': '限制类型', 'constraint': ''},
            {'col': 'match_method', 'n': '匹配方式', 'constraint': ''},
            {'col': 'match_field', 'n': '匹配字段', 'constraint': ''},
            {'col': 'buyer_message_i18n_key', 'n': '买家端提示i18n key', 'constraint': ''},
            {'col': 'scope_type', 'n': '适用范围', 'constraint': ''},
            {'col': 'country_code', 'n': '国家代码', 'constraint': ''},
            {'col': 'description', 'n': '规则描述', 'constraint': ''},
            {'col': 'status', 'n': '状态', 'constraint': ''},
            {'col': 'created_at', 'n': '创建时间', 'constraint': ''},
            {'col': 'updated_at', 'n': '更新时间', 'constraint': ''},
        ],
    },
    {
        'id': 'delivery_rule_keywords', 'name': '规则关键词', 'layer': 'delivery',
        'fields': [
            {'col': 'id', 'n': '关键词ID', 'constraint': 'PK'},
            {'col': 'rule_id', 'n': '关联规则', 'constraint': 'FK'},
            {'col': 'keyword', 'n': '匹配关键词', 'constraint': ''},
            {'col': 'sort_order', 'n': '排序', 'constraint': ''},
        ],
    },
]

# --- 关系定义 ---
RELATIONS = [
    {'from': 'orders', 'to': 'order_items', 'type': '1:N', 'label': '包含商品行', 'color': '#FFA726'},
    {'from': 'products', 'to': 'order_items', 'type': '1:N', 'label': '出现在订单行', 'color': '#FFA726'},
    {'from': 'orders', 'to': 'shipments', 'type': '1:N', 'label': '产生运单', 'color': '#1976D2', 'penwidth': 1.8},
    {'from': 'shipments', 'to': 'shipment_items', 'type': '1:N', 'label': '包含商品', 'color': '#1976D2'},
    {'from': 'order_items', 'to': 'shipment_items', 'type': '1:N', 'label': '发货明细', 'color': '#1976D2'},
    {'from': 'shipments', 'to': 'tracking_checkpoints', 'type': '1:N', 'label': '轨迹节点', 'color': '#1976D2'},
    {'from': 'orders', 'to': 'domestic_trackings', 'type': '1:N', 'label': '关联国内运单', 'color': '#8E24AA', 'penwidth': 1.8},
    {'from': 'domestic_trackings', 'to': 'domestic_checkpoints', 'type': '1:N', 'label': '轨迹节点', 'color': '#8E24AA'},
    {'from': 'carriers', 'to': 'shipments', 'type': '1:N', 'label': '承运', 'color': '#43A047'},
    {'from': 'tracking_platforms', 'to': 'carriers', 'type': '1:N', 'label': '对接承运商', 'color': '#43A047'},
    {'from': 'tracking_platforms', 'to': 'status_mappings', 'type': '1:N', 'label': '状态映射', 'color': '#43A047'},
    {'from': 'domestic_carriers', 'to': 'domestic_trackings', 'type': '1:N', 'label': '承运', 'color': '#8E24AA'},
    {'from': 'delivery_rules', 'to': 'delivery_rule_keywords', 'type': '1:N', 'label': '包含关键词', 'color': '#E53935'},
]

# --- 设计规则 ---
DESIGN_RULES = {
    'shipment_items': 'shipment_items 中间表支持拆包发货，记录每个包裹包含哪些商品。有 SKU 的商品通过 order_item_id 关联，无 SKU 的配件通过 shipments.remark 文本说明',
    'shipment_type_enum': 'shipment_type 枚举值: outbound(正常发货), return(退货), exchange_return(换货退回), exchange_outbound(换货发出), replacement(补发)',
    'status_mapping': 'status_mappings 表存储追踪平台一级(tag)+二级(subtag)状态→Looply内部状态的可配置映射。查找顺序：先精确匹配 tag+subtag，匹配不到则 fallback 到 tag 一级映射',
    'checkpoint_mapping': 'tracking_checkpoints 接收 Webhook 时立即完成状态映射，存储 mapped_internal_status 和 display_i18n_key。买家端展示时直接读取，无需实时查表。历史轨迹不受后续映射规则调整影响',
    'i18n_display': '买家端物流状态文案通过 i18n key 实现多语言：display_text_key 为一级状态文案，display_detail_key 为二级细粒度文案。映射时优先使用 display_detail_key，无值时 fallback 到 display_text_key',
    'subtag_mapping': '二级状态(subtag)映射为可选配置，platform_subtag 为空表示一级映射',
    'domestic_scope': '国内段仅供内部运营监控，用户端不可见',
    'delivery_rules_mvp': 'MVP 仅支持地址行匹配，V2 扩展品类/SKU 维度',
    'encryption': 'API Key/Secret 字段必须加密存储（AES-256）',
    'webhook': 'AfterShip Webhook 推送 + 定时任务拉取双重保障',
    'deduplication': 'tracking_checkpoints 通过联合唯一索引 (shipment_id, checkpoint_time, tag, message) 去重',
}


# ============================================================
# 渲染区（改样式改这里，一般不用动）
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
    """从 JSON metadata 生成技术 YAML（每个 column 追加技术待填字段）"""
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
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

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

