#!/usr/bin/env python3
"""
Looply 物流管理后台原型生成器
==============================
基于 admin-prototype-skill-pack 数据驱动架构。
"""

import os

MODULE_NAME = "物流管理"
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "looply-物流管理后台原型-v2.html")

# ── 侧边栏菜单结构 ──
MENU = [
    {"label": "物流配置", "icon": "truck", "children": [
        {"id": "carrier-list", "label": "承运商管理", "icon": "carrier"},
        {"id": "delivery-rules", "label": "配送限制", "icon": "shield"},
        {"id": "status-mapping", "label": "状态映射", "icon": "mapping"},
    ]},
    {"type": "divider"},
    {"label": "物流追踪", "icon": "target", "children": [
        {"id": "tracking-list", "label": "运单追踪", "icon": "search"},
        {"id": "tracking-platform", "label": "追踪平台管理", "icon": "settings"},
    ]},
]

# ── 模拟数据 ──
DATA = {
    "carriers": [
        {"id": "CR001", "name": "UPS", "code": "ups", "services": "Ground, Express", "status": "启用", "updated": "2026-05-01 10:00"},
        {"id": "CR002", "name": "FedEx", "code": "fedex", "services": "Ground, Home Delivery", "status": "启用", "updated": "2026-05-01 10:00"},
        {"id": "CR003", "name": "USPS", "code": "usps", "services": "Ground Advantage", "status": "停用", "updated": "2026-04-20 14:30"},
    ],
    "delivery_rules": [
        {"id": "DR001", "type": "PO Box", "pattern": "PO Box / P.O. Box / Post Office Box", "status": "禁止配送", "scope": "全品类"},
        {"id": "DR002", "type": "军事地址 (APO/FPO/DPO)", "pattern": "State = AA/AE/AP", "status": "禁止配送", "scope": "全品类"},
        {"id": "DR003", "type": "美国海外领地", "pattern": "State = GU/PR/VI/AS/MP", "status": "禁止配送", "scope": "全品类"},
        {"id": "DR004", "type": "夏威夷/阿拉斯加", "pattern": "State = HI/AK", "status": "允许配送", "scope": "全品类"},
    ],
    "tracking_providers": [
        {"id": "TP001", "name": "AfterShip", "type": "追踪聚合", "status": "启用", "api_key": "asat_••••••••••••••••", "last_sync": "2026-05-08 16:30", "monthly_quota": "23 / 50"},
        {"id": "TP002", "name": "17TRACK", "type": "追踪聚合", "status": "停用", "api_key": "未配置", "last_sync": "—", "monthly_quota": "—"},
        {"id": "TP003", "name": "EasyPost", "type": "全链路API", "status": "停用", "api_key": "未配置", "last_sync": "—", "monthly_quota": "—"},
        {"id": "TP004", "name": "Shippo", "type": "全链路API", "status": "停用", "api_key": "未配置", "last_sync": "—", "monthly_quota": "—"},
    ],
    "tracking": [
        {"order_id": "ORD-20260508-001", "shipment_id": "SHP-20260508-001", "tracking_no": "1Z999AA10123456784", "carrier": "UPS", "status": "运输中", "last_update": "2026-05-08 16:30", "dest": "New York, NY"},
        {"order_id": "ORD-20260507-003", "shipment_id": "SHP-20260507-003", "tracking_no": "1Z999AA10123456785", "carrier": "UPS", "status": "已签收", "last_update": "2026-05-08 09:15", "dest": "Los Angeles, CA"},
        {"order_id": "ORD-20260506-007", "shipment_id": "SHP-20260506-007", "tracking_no": "9400111899223100012", "carrier": "FedEx", "status": "已发货", "last_update": "2026-05-07 14:00", "dest": "Chicago, IL"},
        {"order_id": "ORD-20260505-012", "shipment_id": "SHP-20260505-012", "tracking_no": "1Z999AA10123456786", "carrier": "UPS", "status": "异常", "last_update": "2026-05-06 11:20", "dest": "Houston, TX"},
    ],
    "status_mapping": [
        {"carrier_status": "InTransit", "shipment_status": "运输中", "order_status": "配送中", "trigger_action": "更新订单状态为配送中", "enabled": "启用"},
        {"carrier_status": "OutForDelivery", "shipment_status": "派送中", "order_status": "配送中", "trigger_action": "推送买家通知", "enabled": "启用"},
        {"carrier_status": "Delivered", "shipment_status": "已签收", "order_status": "待确认收货", "trigger_action": "触发确认收货倒计时", "enabled": "启用"},
        {"carrier_status": "AttemptFail", "shipment_status": "投递失败", "order_status": "配送异常", "trigger_action": "通知运营介入", "enabled": "启用"},
        {"carrier_status": "Exception", "shipment_status": "异常", "order_status": "配送异常", "trigger_action": "创建异常工单", "enabled": "启用"},
        {"carrier_status": "Expired", "shipment_status": "超时未更新", "order_status": "配送异常", "trigger_action": "通知运营跟进", "enabled": "停用"},
    ],
}

# ══════════════════════════════════════════
# ICONS
# ══════════════════════════════════════════

ICONS = {
    "truck": '<svg class="mi" aria-hidden="true" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="4" width="10" height="8" rx="1"/><path d="M11 7h3l2 3v4h-5V7z"/><circle cx="5" cy="14" r="1.5"/><circle cx="14" cy="14" r="1.5"/></svg>',
    "target": '<svg class="mi" aria-hidden="true" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="9" r="6.5"/><circle cx="9" cy="9" r="3.5"/><circle cx="9" cy="9" r="1" fill="currentColor"/></svg>',
    # 二级图标 class="ci"
    "carrier": '<svg class="ci" aria-hidden="true" viewBox="0 0 15 15" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="3" width="8" height="7" rx="1"/><path d="M9 5.5h2.5l1.5 2.5v3H9V5.5z"/><circle cx="4" cy="11.5" r="1.2"/><circle cx="11.5" cy="11.5" r="1.2"/></svg>',
    "shield": '<svg class="ci" aria-hidden="true" viewBox="0 0 15 15" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"><path d="M7.5 1.5L2.5 3.5v4c0 3.5 5 6 5 6s5-2.5 5-6v-4L7.5 1.5z"/><path d="M5.5 7.5l1.5 1.5 3-3"/></svg>',
    "mapping": '<svg class="ci" aria-hidden="true" viewBox="0 0 15 15" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"><path d="M2 4h4M9 4h4M2 7.5h4M9 7.5h4M2 11h4M9 11h4"/><path d="M6 4l3 3.5M6 7.5h3M6 11l3-3.5"/></svg>',
    "search": '<svg class="ci" aria-hidden="true" viewBox="0 0 15 15" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"><circle cx="6.5" cy="6.5" r="4"/><path d="M10 10l3.5 3.5"/></svg>',
    "settings": '<svg class="ci" aria-hidden="true" viewBox="0 0 15 15" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"><circle cx="7.5" cy="7.5" r="2"/><path d="M7.5 2v1.5M7.5 11.5V13M2 7.5h1.5M11.5 7.5H13M3.8 3.8l1 1M10.2 10.2l1 1M3.8 11.2l1-1M10.2 4.8l1-1"/></svg>',
}

ARROW_SVG = '<svg class="arrow" aria-hidden="true" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M6 4L10 8L6 12"/></svg>'
ARROW_SM_SVG = '<svg class="arrow-sm" aria-hidden="true" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 3.5L9 7L5 10.5"/></svg>'

# ══════════════════════════════════════════
# CSS
# ══════════════════════════════════════════

CSS = """\
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#F9FAFB;color:#1F2937;font-size:14px}
.header{height:60px;background:#FFFFFF;color:#1F2937;display:flex;align-items:center;padding:0 24px;border-bottom:1px solid #E5E7EB}
.logo{font-size:18px;font-weight:700;letter-spacing:1px;display:flex;align-items:center}
.header-divider{width:1px;height:20px;background:#E5E7EB;margin:0 16px}
.system-label{font-size:14px;font-weight:500;color:#6B7280;letter-spacing:0.3px}
.breadcrumb{margin-left:auto;color:#9CA3AF;font-size:13px;font-weight:400}
.breadcrumb:empty{display:none}
.container{display:flex;height:calc(100vh - 60px)}
.sidebar{width:220px;background:#FFFFFF;overflow:auto;flex-shrink:0;border-right:none;box-shadow:3px 0 12px rgba(0,0,0,0.06);padding:8px 0}
.main{flex:1;overflow:auto;padding:28px}
.menu-solo{display:flex;align-items:center;padding:12px 16px;color:#374151;cursor:pointer;font-size:14px;font-weight:500;transition:background .15s;border-left:3px solid transparent;outline:none;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.menu-solo:hover{background:rgba(0,0,0,.04)}
.menu-solo:focus-visible{box-shadow:inset 0 0 0 2px rgba(124,58,237,.4)}
.menu-solo.active{color:#7C3AED;background:linear-gradient(90deg,rgba(124,58,237,.12),transparent);font-weight:600;border-left-color:#7C3AED}
.menu-solo .mi{width:18px;height:18px;margin-right:10px;flex-shrink:0;opacity:.55}
.menu-solo.active .mi{opacity:1}
.menu-divider{height:1px;background:#F3F4F6;margin:8px 16px}
.menu-group{margin-bottom:0}
.menu-parent{display:flex;align-items:center;padding:12px 16px;color:#374151;cursor:pointer;font-size:14px;font-weight:500;transition:background .15s;user-select:none;border-left:3px solid transparent;outline:none;overflow:hidden}
.menu-parent:hover{background:rgba(0,0,0,.04)}
.menu-parent:focus-visible{box-shadow:inset 0 0 0 2px rgba(124,58,237,.4)}
.menu-parent .mi{width:18px;height:18px;margin-right:10px;flex-shrink:0;opacity:.55}
.menu-parent .arrow{margin-left:auto;width:16px;height:16px;transition:transform .2s;opacity:.4;flex-shrink:0}
.menu-group.open>.menu-parent .arrow{transform:rotate(90deg)}
.menu-parent.active-parent{color:#7C3AED;font-weight:600;border-left-color:#7C3AED}
.menu-parent.active-parent .mi{opacity:1}
.menu-children{max-height:0;overflow:hidden;transition:max-height .3s cubic-bezier(.4,0,.2,1)}
.menu-group.open>.menu-children{max-height:none}
.menu-child{display:flex;align-items:center;padding:10px 16px 10px 44px;color:#4B5563;cursor:pointer;font-size:13px;transition:all .15s;border-left:3px solid transparent;outline:none;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.menu-child:hover{color:#374151;background:rgba(0,0,0,.03)}
.menu-child:focus-visible{box-shadow:inset 0 0 0 2px rgba(124,58,237,.4)}
.menu-child.active{color:#7C3AED;background:linear-gradient(90deg,rgba(124,58,237,.1),transparent);border-left-color:#7C3AED;font-weight:600}
.menu-child .ci{width:15px;height:15px;margin-right:8px;flex-shrink:0;opacity:.45}
.menu-child.active .ci{opacity:.8}
@media(prefers-reduced-motion:reduce){.menu-children,.menu-parent .arrow,.menu-solo,.menu-child{transition:none !important}}
.page{display:none}.page.active{display:block}
.card{background:#fff;border-radius:16px;box-shadow:0 10px 24px rgba(16,24,40,.06);padding:28px}
.card+.card{margin-top:18px}
.page-head{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;margin-bottom:18px}
.page-title{font-size:20px;font-weight:700;margin-bottom:6px}
.page-desc{color:#6B7280;font-size:13px;max-width:760px}
.head-actions{display:flex;gap:10px;flex-wrap:wrap}
.toolbar{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin-bottom:16px}
.toolbar .input,.toolbar select{height:34px;border:1px solid #D1D5DB;border-radius:8px;padding:0 12px;background:#fff}
.btn{height:34px;padding:0 14px;border:1px solid #D1D5DB;background:#fff;border-radius:8px;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;font-size:13px}
.btn.primary{background:#7C3AED;border-color:#7C3AED;color:#fff}
.btn.danger{background:#fff;border-color:#DC2626;color:#DC2626}
.kpi{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:16px}
.kpi .item{background:#FAF5FF;border:1px solid #DDD6FE;border-radius:14px;padding:14px}
.kpi .num{font-size:24px;font-weight:700;color:#7C3AED;margin-bottom:4px}
.muted{color:#6B7280;font-size:12px}
.table-wrap{border:1px solid #E5E7EB;border-radius:14px;overflow:hidden;background:#fff}
table{width:100%;border-collapse:collapse}
th{background:#FFFFFF;padding:10px 12px;text-align:left;font-size:12px;color:#6B7280;border-bottom:1px solid #E5E7EB;text-transform:uppercase;letter-spacing:.02em}
td{padding:11px 12px;border-bottom:1px solid #F3F4F6;font-size:13px;vertical-align:top}
tr:hover{background:#FAF5FF}
.tag{display:inline-block;padding:2px 8px;border-radius:999px;font-size:12px;margin-right:4px}
.tag.on{background:#F0FDF4;color:#16A34A;border:none}
.tag.off{background:#F3F4F6;color:#6B7280;border:none}
.tag.sale{background:#EFF6FF;color:#2563EB;border:none}
.tag.pending{background:#FFFBEB;color:#D97706;border:none}
.tag.req{background:#FEF2F2;color:#DC2626;border:none}
.tag.warn{background:#FFF1F2;color:#E11D48;border:none}
.form-section{margin-bottom:24px}
.form-section .section-title{font-size:15px;font-weight:600;margin-bottom:12px;padding-bottom:8px;border-bottom:1px solid #E5E7EB}
.form-grid{display:grid;grid-template-columns:150px 1fr;gap:12px 16px;align-items:center}
.label{color:#6B7280;font-size:13px}
.field{min-height:36px;border:1px solid #D1D5DB;border-radius:8px;background:#fff;padding:8px 12px;display:flex;align-items:center}
.field.readonly{background:#F9FAFB;color:#6B7280}
.form-actions{display:flex;gap:12px;justify-content:flex-end;padding-top:16px;border-top:1px solid #E5E7EB;margin-top:24px}
.section-title{font-size:14px;font-weight:700;margin-bottom:10px;color:#7C3AED}
.rail-note{padding:12px 14px;border-radius:10px;background:#F3EEFF;border:1px solid #DDD6FE;color:#6D28D9;font-size:12px;line-height:1.6;margin-bottom:16px}
.empty-state{display:flex;flex-direction:column;align-items:center;padding:60px 20px;text-align:center}
.empty-state .empty-icon{width:48px;height:48px;color:#9CA3AF;margin-bottom:16px}
.empty-state .empty-title{font-size:16px;font-weight:600;color:#1F2937;margin-bottom:8px}
.empty-state .empty-desc{font-size:13px;color:#6B7280;margin-bottom:24px;max-width:360px}
.timeline{border-left:2px solid #E5E7EB;margin-left:8px;padding-left:20px}
.timeline-item{position:relative;padding-bottom:20px}
.timeline-item:last-child{padding-bottom:0}
.timeline-item::before{content:'';position:absolute;left:-25px;top:4px;width:10px;height:10px;border-radius:50%;background:#E5E7EB;border:2px solid #fff}
.timeline-item.active::before{background:#7C3AED}
.timeline-item .time{font-size:12px;color:#9CA3AF;margin-bottom:2px}
.timeline-item .event{font-size:13px;color:#1F2937}
.timeline-item .location{font-size:12px;color:#6B7280;margin-top:2px}
.toggle{position:relative;width:40px;height:22px;background:#D1D5DB;border-radius:11px;cursor:pointer;display:inline-block}
.toggle.on{background:#7C3AED}
.toggle::after{content:'';position:absolute;top:2px;left:2px;width:18px;height:18px;background:#fff;border-radius:50%;transition:transform .2s}
.toggle.on::after{transform:translateX(18px)}
.op-log{margin-top:24px;padding-top:24px;border-top:1px solid #E5E7EB}
.op-log-title{font-size:15px;font-weight:600;margin-bottom:12px}
"""


# ══════════════════════════════════════════
# Helper 函数
# ══════════════════════════════════════════

def table_html(headers, rows):
    thead = ''.join(f'<th>{h}</th>' for h in headers)
    tbody = []
    for row in rows:
        tbody.append('<tr>' + ''.join(f'<td>{c}</td>' for c in row) + '</tr>')
    return f'<div class="table-wrap"><table><thead><tr>{thead}</tr></thead><tbody>{"".join(tbody)}</tbody></table></div>'


def kpi_cards(items):
    cards = []
    for item in items:
        cards.append(f'<div class="item"><div class="num">{item["num"]}</div><div class="muted">{item["label"]}</div></div>')
    return f'<div class="kpi">{"".join(cards)}</div>'


def tag(text, style="on"):
    return f'<span class="tag {style}">{text}</span>'


def status_tag(status):
    style_map = {"启用": "on", "停用": "off", "禁止配送": "req", "允许配送": "on",
                 "运输中": "sale", "已签收": "on", "已发货": "pending", "异常": "warn",
                 "派送中": "sale", "投递失败": "warn", "超时未更新": "off"}
    return tag(status, style_map.get(status, "opt"))


def page_head(title, desc="", actions_html=""):
    return f'<div class="page-head"><div><div class="page-title">{title}</div><div class="page-desc">{desc}</div></div><div class="head-actions">{actions_html}</div></div>'


def toolbar_html(inner):
    return f'<div class="toolbar">{inner}</div>'


# ══════════════════════════════════════════
# 侧边栏生成器
# ══════════════════════════════════════════

def _get_icon(icon_key):
    if not icon_key:
        return ''
    if icon_key.startswith('<svg'):
        return icon_key
    return ICONS.get(icon_key, '')


def menu_html():
    parts = []
    group_counter = [0]

    def render_l2(items):
        for item in items:
            if item.get("id"):
                icon = _get_icon(item.get("icon"))
                parts.append(f'<div class="menu-child" tabindex="0" role="menuitem" data-page="{item["id"]}">{icon}<span>{item["label"]}</span></div>')

    for item in MENU:
        if item.get("type") == "divider":
            parts.append('<div class="menu-divider" role="separator"></div>')
        elif item.get("id"):
            icon = _get_icon(item.get("icon"))
            parts.append(f'<div class="menu-solo" tabindex="0" role="menuitem" data-page="{item["id"]}">{icon}<span>{item["label"]}</span></div>')
        elif item.get("children"):
            group_counter[0] += 1
            gid = f'children-{group_counter[0]}'
            icon = _get_icon(item.get("icon"))
            parts.append(f'<div class="menu-group">')
            parts.append(f'<div class="menu-parent" tabindex="0" role="button" aria-expanded="false" aria-controls="{gid}" onclick="toggleGroup(this)">{icon}<span>{item["label"]}</span>{ARROW_SVG}</div>')
            parts.append(f'<div class="menu-children" id="{gid}" role="group">')
            render_l2(item["children"])
            parts.append('</div></div>')

    return '\n'.join(parts)


# ══════════════════════════════════════════
# 页面函数
# ══════════════════════════════════════════

def page_carrier_list():
    rows = []
    edit_btn = '<button class="btn" onclick="showSubPage(\'carrier\',\'edit\')">编辑</button>'
    for c in DATA["carriers"]:
        rows.append([
            f'<b>{c["id"]}</b>',
            c["name"],
            f'<span class="muted">{c["code"]}</span>',
            c["services"],
            status_tag(c["status"]),
            c["updated"],
            edit_btn
        ])
    stats = kpi_cards([
        {"num": "3", "label": "承运商总数"},
        {"num": "2", "label": "已启用"},
        {"num": "1", "label": "已停用"},
        {"num": "5", "label": "服务类型"},
    ])
    tb = toolbar_html('<input class="input" placeholder="搜索承运商名称/编码"><select><option>全部状态</option><option>启用</option><option>停用</option></select><button class="btn">查询</button>')
    body = table_html(['ID', '承运商', '编码', '服务类型', '状态', '更新时间', '操作'], rows)
    add_btn = '<button class="btn primary" onclick="showSubPage(\'carrier\',\'create\')">新增承运商</button>'
    head = page_head("承运商管理", "配置平台可用的物流承运商及其服务类型", add_btn)
    return f'''
    <div class="page" id="page-carrier-list-list">
    <div class="card">
      {head}
      {stats}
      {tb}
      {body}
    </div>
    </div>'''


def page_carrier_edit():
    back_btn = '<button class="btn" onclick="navigateTo(\'carrier-list\',\'承运商管理\')">返回列表</button>'
    head = page_head("编辑承运商 — UPS", "修改承运商基本信息和服务配置", back_btn)
    enabled = status_tag("启用")
    disabled = status_tag("停用")
    return f'''
    <div class="page" id="page-carrier-edit">
    <div class="card">
      {head}
      <div class="form-section">
        <div class="section-title">基本信息</div>
        <div class="form-grid">
          <div class="label">承运商名称</div><div class="field">UPS</div>
          <div class="label">承运商编码</div><div class="field">ups</div>
          <div class="label">官网</div><div class="field">https://www.ups.com</div>
          <div class="label">状态</div><div class="field"><span class="toggle on"></span></div>
        </div>
      </div>
      <div class="form-section">
        <div class="section-title">服务类型</div>
        <div class="table-wrap"><table>
          <thead><tr><th>服务名称</th><th>服务编码</th><th>预计时效</th><th>状态</th></tr></thead>
          <tbody>
            <tr><td>UPS Ground</td><td>ups_ground</td><td>3-5 工作日</td><td>{enabled}</td></tr>
            <tr><td>UPS Express</td><td>ups_express</td><td>1-2 工作日</td><td>{enabled}</td></tr>
            <tr><td>UPS SurePost</td><td>ups_surepost</td><td>5-7 工作日</td><td>{disabled}</td></tr>
          </tbody>
        </table></div>
      </div>
      <div class="form-section">
        <div class="section-title">追踪配置</div>
        <div class="form-grid">
          <div class="label">追踪号格式</div><div class="field">1Z[A-Z0-9]{{16}}</div>
          <div class="label">追踪链接模板</div><div class="field">https://www.ups.com/track?tracknum={{tracking_no}}</div>
        </div>
      </div>
      <div class="form-actions">
        <button class="btn" onclick="navigateTo('carrier-list','承运商管理')">取消</button>
        <button class="btn primary">保存</button>
      </div>
      <div class="op-log">
        <div class="op-log-title">操作记录</div>
        <div class="table-wrap"><table>
          <thead><tr><th>操作时间</th><th>操作人</th><th>操作类型</th><th>操作内容</th></tr></thead>
          <tbody>
            <tr><td class="muted">2026-05-01 10:00</td><td>admin</td><td><b>创建</b></td><td class="muted">创建承运商 UPS</td></tr>
          </tbody>
        </table></div>
      </div>
    </div>
    </div>'''


def page_carrier_create():
    back_btn = '<button class="btn" onclick="navigateTo(\'carrier-list\',\'承运商管理\')">返回列表</button>'
    head = page_head("新增承运商", "添加新的物流承运商", back_btn)
    return f'''
    <div class="page" id="page-carrier-create">
    <div class="card">
      {head}
      <div class="form-section">
        <div class="section-title">基本信息</div>
        <div class="form-grid">
          <div class="label">承运商名称</div><div class="field" style="color:#9CA3AF">请输入承运商名称</div>
          <div class="label">承运商编码</div><div class="field" style="color:#9CA3AF">请输入唯一编码（如 ups、fedex）</div>
          <div class="label">官网</div><div class="field" style="color:#9CA3AF">https://</div>
          <div class="label">状态</div><div class="field"><span class="toggle on"></span></div>
        </div>
      </div>
      <div class="form-section">
        <div class="section-title">追踪配置</div>
        <div class="form-grid">
          <div class="label">追踪号格式</div><div class="field" style="color:#9CA3AF">正则表达式</div>
          <div class="label">追踪链接模板</div><div class="field" style="color:#9CA3AF">使用 {{tracking_no}} 作为占位符</div>
        </div>
      </div>
      <div class="form-actions">
        <button class="btn" onclick="navigateTo('carrier-list','承运商管理')">取消</button>
        <button class="btn primary">保存</button>
      </div>
    </div>
    </div>'''


def page_delivery_rules():
    rows = []
    edit_btn = '<button class="btn">编辑</button>'
    for r in DATA["delivery_rules"]:
        rows.append([
            f'<b>{r["id"]}</b>',
            r["type"],
            f'<span class="muted">{r["pattern"]}</span>',
            status_tag(r["status"]),
            r["scope"],
            edit_btn
        ])
    body = table_html(['ID', '限制类型', '识别规则', '配送状态', '适用范围', '操作'], rows)
    head = page_head("配送限制", "管理不可配送的地址类型和区域限制规则。买家下单时系统自动校验地址可达性。")
    return f'''
    <div class="page" id="page-delivery-rules-list">
    <div class="card">
      {head}
      <div class="rail-note">当前配送范围：美国本土 50 州 + DC。PO Box、军事地址、海外领地默认禁止配送（行业惯例：奢侈品需签收确认）。</div>
      {body}
    </div>
    </div>'''


def page_tracking_list():
    rows = []
    detail_link_tpl = '<a href="#" style="color:#7C3AED;text-decoration:none" onclick="showSubPage(\'tracking\',\'detail\')">{oid}</a>'
    detail_btn = '<button class="btn" onclick="showSubPage(\'tracking\',\'detail\')">详情</button>'
    for t in DATA["tracking"]:
        rows.append([
            detail_link_tpl.format(oid=t["order_id"]),
            f'<span class="muted">{t["shipment_id"]}</span>',
            f'<b>{t["tracking_no"]}</b>',
            t["carrier"],
            status_tag(t["status"]),
            t["dest"],
            t["last_update"],
            detail_btn
        ])
    stats = kpi_cards([
        {"num": "4", "label": "运单总数"},
        {"num": "1", "label": "运输中"},
        {"num": "1", "label": "已签收"},
        {"num": "1", "label": "异常"},
    ])
    tb = toolbar_html('<input class="input" placeholder="搜索订单号/发货单号/运单号"><select><option>全部状态</option><option>运输中</option><option>已签收</option><option>异常</option></select><select><option>全部承运商</option><option>UPS</option><option>FedEx</option></select><button class="btn">查询</button>')
    add_btn = '<button class="btn primary" onclick="showSubPage(\'tracking\',\'create\')">录入运单号</button>'
    head = page_head("运单追踪", "录入运单号并追踪物流轨迹，系统通过追踪平台自动获取状态更新", add_btn)
    body = table_html(['订单号', '发货单号', '运单号', '承运商', '状态', '目的地', '最后更新', '操作'], rows)
    return f'''
    <div class="page" id="page-tracking-list-list">
    <div class="card">
      {head}
      {stats}
      {tb}
      {body}
    </div>
    </div>'''


def page_tracking_create():
    back_btn = '<button class="btn" onclick="navigateTo(\'tracking-list\',\'运单追踪\')">返回列表</button>'
    head = page_head("录入运单号", "将线下获取的运单号关联到订单，系统将自动开始追踪", back_btn)
    return f'''
    <div class="page" id="page-tracking-create">
    <div class="card">
      {head}
      <div class="form-section">
        <div class="section-title">运单信息</div>
        <div class="form-grid">
          <div class="label">关联订单号</div><div class="field" style="color:#9CA3AF">请输入或选择订单号</div>
          <div class="label">运单号</div><div class="field" style="color:#9CA3AF">请输入承运商提供的运单号</div>
          <div class="label">承运商</div><div class="field" style="color:#9CA3AF">自动识别（或手动选择）</div>
        </div>
      </div>
      <div class="rail-note">录入运单号后，系统将调用 AfterShip API 自动识别承运商并开始追踪。轨迹更新通过 Webhook 实时推送。</div>
      <div class="form-actions">
        <button class="btn" onclick="navigateTo('tracking-list','运单追踪')">取消</button>
        <button class="btn primary">确认录入</button>
      </div>
    </div>
    </div>'''


def page_tracking_detail():
    back_btn = '<button class="btn" onclick="navigateTo(\'tracking-list\',\'运单追踪\')">返回列表</button>'
    head = page_head("运单详情 — 1Z999AA10123456784", "订单 ORD-20260508-001 的物流追踪信息", back_btn)
    in_transit = status_tag("运输中")
    return f'''
    <div class="page" id="page-tracking-detail">
    <div class="card">
      {head}
      <div class="form-section">
        <div class="section-title">发货层级关系</div>
        <div class="rail-note">订单可能包含多个发货单（Shipment），每个发货单对应一个运单号。本页面展示单个发货单的追踪信息。</div>
        <div class="form-grid">
          <div class="label">订单号</div><div class="field">ORD-20260508-001</div>
          <div class="label">发货单号</div><div class="field"><b>SHP-20260508-001</b></div>
          <div class="label">运单号</div><div class="field"><b>1Z999AA10123456784</b></div>
        </div>
      </div>
      <div class="form-section">
        <div class="section-title">基本信息</div>
        <div class="form-grid">
          <div class="label">承运商</div><div class="field">UPS</div>
          <div class="label">当前状态</div><div class="field">{in_transit}</div>
          <div class="label">目的地</div><div class="field">New York, NY 10001</div>
          <div class="label">预计送达</div><div class="field">2026-05-10</div>
        </div>
      </div>
      <div class="form-section">
        <div class="section-title">物流轨迹</div>
        <div class="timeline">
          <div class="timeline-item active">
            <div class="time">2026-05-08 16:30</div>
            <div class="event">包裹已到达中转站</div>
            <div class="location">Newark, NJ</div>
          </div>
          <div class="timeline-item active">
            <div class="time">2026-05-08 08:15</div>
            <div class="event">包裹已离开发货仓</div>
            <div class="location">Edison, NJ</div>
          </div>
          <div class="timeline-item active">
            <div class="time">2026-05-07 18:00</div>
            <div class="event">承运商已揽收</div>
            <div class="location">Edison, NJ</div>
          </div>
          <div class="timeline-item">
            <div class="time">2026-05-07 15:30</div>
            <div class="event">面单已生成，等待揽收</div>
            <div class="location">Looply Warehouse</div>
          </div>
        </div>
      </div>
    </div>
    </div>'''


def page_tracking_platform():
    rows = []
    edit_btn = '<button class="btn" onclick="showSubPage(\'tracking-platform\',\'edit\')">编辑</button>'
    for tp in DATA["tracking_providers"]:
        rows.append([
            f'<b>{tp["id"]}</b>',
            tp["name"],
            tp["type"],
            status_tag(tp["status"]),
            tp["api_key"],
            tp["last_sync"],
            tp["monthly_quota"],
            edit_btn
        ])
    add_btn = '<button class="btn primary" onclick="showSubPage(\'tracking-platform\',\'create\')">新增追踪平台</button>'
    head = page_head("追踪平台管理", "配置物流追踪平台的 API 连接和 Webhook 设置，支持多平台切换", add_btn)
    body = table_html(['ID', '平台名称', '类型', '状态', 'API Key', '最后同步', '月度配额', '操作'], rows)
    return f'''
    <div class="page" id="page-tracking-platform-list">
    <div class="card">
      {head}
      <div class="rail-note">追踪聚合平台（AfterShip、17TRACK）支持 1,000+ 承运商自动识别；全链路 API（EasyPost、Shippo）同时支持面单生成和追踪。</div>
      {body}
    </div>
    </div>'''


def page_tracking_platform_edit():
    back_btn = '<button class="btn" onclick="navigateTo(\'tracking-platform\',\'追踪平台管理\')">返回列表</button>'
    head = page_head("编辑追踪平台 — AfterShip", "修改追踪平台的 API 配置和 Webhook 设置", back_btn)
    return f'''
    <div class="page" id="page-tracking-platform-edit">
    <div class="card">
      {head}
      <div class="form-section">
        <div class="section-title">基本信息</div>
        <div class="form-grid">
          <div class="label">平台名称</div><div class="field">AfterShip</div>
          <div class="label">平台类型</div><div class="field">追踪聚合</div>
          <div class="label">状态</div><div class="field"><span class="toggle on"></span></div>
        </div>
      </div>
      <div class="form-section">
        <div class="section-title">API 配置</div>
        <div class="form-grid">
          <div class="label">API Key</div><div class="field">asat_••••••••••••••••</div>
          <div class="label">API 版本</div><div class="field">2024-10</div>
          <div class="label">连接状态</div><div class="field">{status_tag("启用")} <span class="muted" style="margin-left:8px">最后验证: 2026-05-08 10:00</span></div>
        </div>
      </div>
      <div class="form-section">
        <div class="section-title">Webhook 配置</div>
        <div class="form-grid">
          <div class="label">Webhook URL</div><div class="field">https://api.looply.com/webhooks/aftership</div>
          <div class="label">签名密钥</div><div class="field">whsec_••••••••••••</div>
          <div class="label">状态</div><div class="field">{status_tag("启用")}</div>
          <div class="label">最后接收</div><div class="field">2026-05-08 16:30 <span class="muted">（3 分钟前）</span></div>
        </div>
      </div>
      <div class="form-section">
        <div class="section-title">配额使用</div>
        <div class="form-grid">
          <div class="label">当月追踪量</div><div class="field">23 / 50（免费档）</div>
          <div class="label">计费周期</div><div class="field">2026-05-01 ~ 2026-05-31</div>
          <div class="label">套餐</div><div class="field">Free Plan <span class="muted">（50 shipments/month）</span></div>
        </div>
      </div>
      <div class="form-actions">
        <button class="btn">测试连接</button>
        <button class="btn" onclick="navigateTo('tracking-platform','追踪平台管理')">取消</button>
        <button class="btn primary">保存配置</button>
      </div>
      <div class="op-log">
        <div class="op-log-title">操作记录</div>
        <div class="table-wrap"><table>
          <thead><tr><th>操作时间</th><th>操作人</th><th>操作类型</th><th>操作内容</th></tr></thead>
          <tbody>
            <tr><td class="muted">2026-05-01 10:00</td><td>admin</td><td><b>创建</b></td><td class="muted">创建追踪平台 AfterShip</td></tr>
          </tbody>
        </table></div>
      </div>
    </div>
    </div>'''


def page_tracking_platform_create():
    back_btn = '<button class="btn" onclick="navigateTo(\'tracking-platform\',\'追踪平台管理\')">返回列表</button>'
    head = page_head("新增追踪平台", "添加新的物流追踪平台", back_btn)
    webhook_placeholder = 'https://api.looply.com/webhooks/{platform}'
    return f'''
    <div class="page" id="page-tracking-platform-create">
    <div class="card">
      {head}
      <div class="form-section">
        <div class="section-title">基本信息</div>
        <div class="form-grid">
          <div class="label">平台名称</div><div class="field" style="color:#9CA3AF">请选择（AfterShip / 17TRACK / EasyPost / Shippo）</div>
          <div class="label">平台类型</div><div class="field" style="color:#9CA3AF">根据选择自动填充</div>
          <div class="label">状态</div><div class="field"><span class="toggle on"></span></div>
        </div>
      </div>
      <div class="form-section">
        <div class="section-title">API 配置</div>
        <div class="form-grid">
          <div class="label">API Key</div><div class="field" style="color:#9CA3AF">请输入平台提供的 API Key</div>
          <div class="label">API 版本</div><div class="field" style="color:#9CA3AF">请输入 API 版本（如 2024-10）</div>
        </div>
      </div>
      <div class="form-section">
        <div class="section-title">Webhook 配置</div>
        <div class="form-grid">
          <div class="label">Webhook URL</div><div class="field" style="color:#9CA3AF">{webhook_placeholder}</div>
          <div class="label">签名密钥</div><div class="field" style="color:#9CA3AF">请输入 Webhook 签名密钥</div>
        </div>
      </div>
      <div class="form-actions">
        <button class="btn" onclick="navigateTo('tracking-platform','追踪平台管理')">取消</button>
        <button class="btn primary">保存</button>
      </div>
    </div>
    </div>'''


def page_status_mapping():
    rows = []
    for m in DATA["status_mapping"]:
        rows.append([
            f'<code style="background:#F3F4F6;padding:2px 6px;border-radius:4px;font-size:12px">{m["carrier_status"]}</code>',
            status_tag(m["shipment_status"]),
            status_tag(m["order_status"]),
            m["trigger_action"],
            status_tag(m["enabled"]),
            '<button class="btn">编辑</button>'
        ])
    return f'''
    <div class="page" id="page-status-mapping-list">
    <div class="card">
      {page_head("状态映射", "配置承运商物流状态与 Looply 内部状态的映射关系，以及状态变更时触发的自动操作")}
      <div class="rail-note">
        <b>三层状态说明：</b><br>
        • <b>Carrier Status</b>（承运商状态）：来自 UPS/FedEx 等承运商的原始物流状态<br>
        • <b>Shipment Status</b>（发货单状态）：Looply 内部的发货单履约状态<br>
        • <b>Order Status</b>（订单状态）：发货单状态变更时触发的订单级状态变更
      </div>
      {table_html(['承运商状态', '发货单状态', '订单状态变更', '触发操作', '启用状态', '操作'], rows)}
    </div>
    </div>'''


# ── 注册所有页面函数 ──
PAGES = [
    page_carrier_list,
    page_carrier_edit,
    page_carrier_create,
    page_delivery_rules,
    page_tracking_list,
    page_tracking_create,
    page_tracking_detail,
    page_tracking_platform,
    page_tracking_platform_edit,
    page_tracking_platform_create,
    page_status_mapping,
]


# ══════════════════════════════════════════
# JS
# ══════════════════════════════════════════

JS = """\
window.toggleGroup = function(parent) {
  var group = parent.closest('.menu-group');
  group.classList.toggle('open');
  parent.setAttribute('aria-expanded', group.classList.contains('open'));
};
function clearAllActive() {
  document.querySelectorAll('.menu-solo,.menu-child').forEach(function(el){el.classList.remove('active')});
  document.querySelectorAll('.menu-parent').forEach(function(el){el.classList.remove('active-parent')});
}
function navigateTo(pageId, label) {
  clearAllActive();
  document.querySelectorAll('.page').forEach(function(p){p.classList.remove('active')});
  var target = document.getElementById('page-' + pageId + '-list') || document.getElementById('page-' + pageId);
  if (target) target.classList.add('active');
  document.querySelector('.breadcrumb').textContent = label || '';
}
function showSubPage(module, action) {
  document.querySelectorAll('.page').forEach(function(p){p.classList.remove('active')});
  var target = document.getElementById('page-' + module + '-' + action);
  if (target) target.classList.add('active');
}
document.querySelectorAll('[data-page]').forEach(function(item) {
  item.addEventListener('click', function() {
    var pageId = this.dataset.page;
    var label = this.querySelector('span') ? this.querySelector('span').textContent : '';
    navigateTo(pageId, label);
    this.classList.add('active');
    var group = this.closest('.menu-group');
    if (group) { group.classList.add('open'); var p = group.querySelector('.menu-parent'); if(p) p.classList.add('active-parent'); }
  });
});
var firstMenu = document.querySelector('[data-page]');
if (firstMenu) firstMenu.click();
"""


# ══════════════════════════════════════════
# 组装 & 输出
# ══════════════════════════════════════════

def build():
    pages_content = '\n'.join(fn() for fn in PAGES)
    html = f"""<!DOCTYPE html>
<html lang='zh-CN'>
<head>
<meta charset='UTF-8'>
<meta name='viewport' content='width=device-width,initial-scale=1.0'>
<title>Looply {MODULE_NAME}后台原型</title>
<style>
{CSS}
</style>
</head>
<body>
<div class='header'>
  <div class='logo'><img src="logo-new.png" height="28" alt="Looply"></div>
  <div class='header-divider'></div>
  <span class='system-label'>{MODULE_NAME}系统</span>
  <div class='breadcrumb'></div>
</div>
<div class='container'>
  <div class='sidebar' role="navigation" aria-label="主导航">
{menu_html()}
  </div>
  <div class='main'>
{pages_content}
  </div>
</div>
<script>
{JS}
</script>
</body>
</html>"""
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Generated: {OUTPUT_FILE}")


if __name__ == '__main__':
    build()
