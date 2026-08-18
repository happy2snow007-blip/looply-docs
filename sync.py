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
import zipfile
from datetime import datetime
from pathlib import Path
from urllib.parse import quote as url_quote, unquote as url_unquote

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
        'default_source': '$HOME/looply/首页',
        'target': 'docs-首页',
        'keywords': ['首页', 'home'],
        'config_key': None,
        'artifacts': {
            'prd': {
                'subdir': 'PRD',
                'pattern': r'looply-首页-PRD-v(.+?)\.md',
            },
            'prd_feed': {
                'subdir': 'feed-prd',
                'pattern': r'Looply-首页Feed-PRD-v(.+?)\.md',
            },
        },
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
                'pattern': r'looply-商详页CMS配置后台原型-v(.+?)\.html',
            },
            'prototype_pc': {
                'subdir': 'UI',
                'pattern': r'looply-商详页-PC-v(.+?)\.html',
            },
            'prototype_app': {
                'subdir': 'UI',
                'pattern': r'looply-商详页-APP-v(.+?)\.html',
            },
            'prd': {
                'subdir': 'PRD',
                'pattern': r'looply-商详页-PRD-v(.+?)\.md',
            },
            'delivery': {
                'subdir': '.',
                'pattern': r'商详-交付开发 V(.+?)\.zip',
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
        'name': '多语言管理',
        'default_source': '$HOME/Desktop/海外业务/多语言',
        'target': 'docs-多语言管理',
        'keywords': ['翻译', 'translation', '多语言'],
        'config_key': 'translation',
        'artifacts': {
            'prototype': {
                'subdir': '原型',
                'pattern': r'looply-多语言管理后台原型-v(.+?)\.html',
                'exclude': r'(backup)',
            },
            'prd': {
                'subdir': 'PRD',
                'pattern': r'looply-多语言模块-PRD-v(.+?)\.md',
            },
            'er': {
                'subdir': '实体关系图',
                'pattern': r'looply-多语言模块实体关系图-v(.+?)\.svg',
            },
            'delivery': {
                'subdir': '.',
                'pattern': r'多语言-交付开发 V(.+?)\.zip',
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
        'default_source': '$HOME/Desktop/汇率管理',
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
    'logistics': {
        'name': '物流管理',
        'default_source': '$HOME/Desktop/物流管理',
        'target': 'docs-物流管理',
        'keywords': ['物流', 'logistics'],
        'config_key': 'logistics',
        'artifacts': {
            # 主原型锁定 antd 版本：源目录同时存在 v5.10.html 与 v5.10-antd.html，
            # 二者版本号都解析为 5.10，必须用 -antd 后缀消歧，确保 antd 版作主原型。
            'prototype': {
                'subdir': '原型',
                'pattern': r'looply-物流管理后台原型-v(.+?)-antd\.html',
                'exclude': r'(backup|对比)',
            },
            'prd': {
                'subdir': 'PRD',
                'pattern': r'looply-物流信息服务-PRD-v(.+?)\.md',
            },
            'er': {
                'subdir': '实体关系图',
                'pattern': r'looply-物流管理实体关系图-v(.+?)\.svg',
            },
            'delivery': {
                'subdir': '.',
                'pattern': r'物流管理-交付开发 V(.+?)\.zip',
            },
        },
    },
    'subscription': {
        'name': '订阅管理',
        'default_source': '$HOME/Desktop/订阅管理',
        'target': 'docs-订阅管理',
        'keywords': ['订阅', 'subscription', 'subscribe'],
        'config_key': 'subscription',
        'artifacts': {
            # 主原型为 antd 版：源目录命名为 "订阅管理-antd-原型-v{n}.html"
            'prototype': {
                'subdir': '原型',
                'pattern': r'looply-订阅管理-antd-原型-v(.+?)\.html',
                'exclude': r'(backup|对比|report)',
            },
            'prd': {
                'subdir': 'PRD',
                'pattern': r'looply-用户订阅管理-PRD-v(.+?)\.md',
            },
            'er': {
                'subdir': '实体关系图',
                'pattern': r'looply-用户订阅管理实体关系图-v(.+?)\.svg',
            },
            'delivery': {
                'subdir': '.',
                'pattern': r'订阅管理-交付开发 V(.+?)\.zip',
            },
        },
    },
    'cart': {
        'name': '购物车',
        'default_source': '$HOME/Desktop/海外业务/购物车',
        'target': 'docs-购物车',
        'keywords': ['购物车', 'cart', '购物'],
        'config_key': None,
        'artifacts': {
            'prd': {
                'subdir': 'PRD',
                'pattern': r'购物车PRD-V(.+?)\.md',
            },
            'er': {
                'subdir': '实体关系图',
                'pattern': r'looply-购物车实体关系图-v(.+?)\.svg',
            },
            'delivery': {
                'subdir': '.',
                'pattern': r'购物车-交付开发 V(.+?)\.zip',
            },
        },
    },
    'order': {
        'name': '订单支付',
        'default_source': '$HOME/Desktop/海外业务/订单支付',
        'target': 'docs-订单支付',
        'keywords': ['订单', 'order', '支付'],
        'config_key': 'order',
        'artifacts': {
            'prototype': {
                'subdir': '原型',
                'pattern': r'looply-订单管理后台原型-v(.+?)\.html',
                'exclude': r'(backup|对比|report)',
            },
            'prd': {
                'subdir': 'PRD',
                'pattern': r'looply-订单支付-PRD-v(.+?)\.md',
            },
            'er': {
                'subdir': '实体关系图',
                'pattern': r'looply-订单模块实体关系图-v(.+?)\.svg',
            },
            'flowchart': {
                'subdir': '系统流程图',
                'pattern': r'looply-订单支付系统流程图-v(.+?)\.svg',
            },
            'delivery': {
                'subdir': '.',
                'pattern': r'订单支付-交付开发 V(.+?)\.zip',
            },
        },
    },
    'plm': {
        'name': '红布林商品对接',
        'default_source': '$HOME/Desktop/海外业务/红布林商品对接',
        'target': 'docs-红布林商品对接',
        'keywords': ['红布林', 'plm', '商品对接'],
        'config_key': 'plm',
        'artifacts': {
            'prototype': {
                'subdir': '原型',
                'pattern': r'looply-红布林商品对接-antd-原型-v(.+?)\.html',
                'exclude': r'(backup|对比|report)',
            },
            'prd': {
                'subdir': 'PRD',
                'pattern': r'looply-红布林商品对接-PRD-v(.+?)\.md',
            },
            'flowchart': {
                'subdir': '系统流程图',
                'pattern': r'looply-商品业务全流程系统流程图-v(.+?)\.svg',
            },
            'delivery': {
                'subdir': '.',
                'pattern': r'红布林商品对接-交付开发 V(.+?)\.zip',
            },
        },
    },
    'rhl_order': {
        'name': '红布林订单对接',
        'default_source': '$HOME/Desktop/海外业务/红布林订单对接',
        'target': 'docs-红布林订单对接',
        'keywords': ['红布林订单', 'rhlorder', '订单对接'],
        'config_key': 'rhl_order',
        'artifacts': {
            'prototype': {
                'subdir': '原型',
                'pattern': r'looply-红布林订单对接-后台原型-v(.+?)\.html',
                'exclude': r'(backup|report)',
            },
            'prd': {
                'subdir': 'PRD',
                'pattern': r'looply-红布林订单对接-PRD-v(.+?)\.md',
            },
            'flowchart': {
                'subdir': '系统流程图',
                'pattern': r'looply-交易链路与国内二奢系统衔接-系统流程图-v(.+?)\.svg',
            },
            'delivery': {
                'subdir': '.',
                'pattern': r'红布林订单对接-交付开发 V(.+?)\.zip',
            },
        },
    },
    'shop': {
        'name': 'shop页',
        'default_source': '$HOME/Desktop/looply/06shop',
        'target': 'docs-shop页',
        'keywords': ['shop', 'Shop', '导航'],
        'config_key': 'shop',
        'artifacts': {
            'prototype': {
                'subdir': '后台原型',
                'source_subdir': '后台原型',
                'pattern': r'looply-shop页导航栏配置-后台原型-v(.+?)-antd\.html',
                'exclude': r'(backup|PC)',
            },
            'prototype_app': {
                'subdir': '原型',
                'source_subdir': '前端原型',
                'pattern': r'looply-shop-app-v(.+?)\.html',
                'exclude': r'(backup|奢侈品)',
            },
            'prd': {
                'subdir': 'PRD',
                'source_subdir': 'prd',
                'pattern': r'looply-shop-app-prd-v(.+?)\.md',
            },
            'prd_html': {
                'subdir': 'PRD',
                'pattern': r'looply-shop-app-PRD\.html',
            },
        },
    },
    'search': {
        'name': '搜索',
        'default_source': '$HOME/Documents/Looply/prototypes/search',
        'target': 'docs-搜索',
        'keywords': ['搜索', 'search'],
        'sidebar_group': 'C端卖场',
        'config_key': None,
        'artifacts': {
            'prototype': {
                'subdir': '原型',
                'source_subdir': '.',
                'pattern': r'looply-global-search-ui-review-v(.+?)\.html',
            },
            'dev_review': {
                'subdir': '原型',
                'source_subdir': '.',
                'pattern': r'looply-global-search-dev-review-v(.+?)\.html',
            },
            'prd': {
                'subdir': 'PRD',
                'source_subdir': '../../docs/product',
                'pattern': r'looply-Web全局搜索-PRD-v(.+?)\.md',
            },
        },
    },
    'social_share': {
        'name': '社媒分享管理',
        'default_source': '$HOME/Desktop/社媒分享',
        'target': 'docs-社媒分享管理',
        'keywords': ['社媒', '分享', 'share', 'social'],
        'config_key': 'social_share',
        'artifacts': {
            # 主原型为后台 antd 短链管理控制台；C 端前端原型已迁 Figma，.pen 不进文档中心
            'prototype': {
                'subdir': '原型',
                'pattern': r'looply-社媒分享管理-antd-原型-v(.+?)\.html',
                'exclude': r'(backup|对比|report)',
            },
            'prd': {
                'subdir': 'PRD',
                'pattern': r'looply-社媒分享管理-PRD-v(.+?)\.md',
            },
            'er': {
                'subdir': '实体关系图',
                'pattern': r'looply-社媒分享实体关系图-v(.+?)\.svg',
            },
        },
    },
    'favourites_history': {
        'name': '收藏与浏览历史',
        'default_source': '$HOME/Desktop/个人中心',
        'target': 'docs-收藏与浏览历史',
        'keywords': ['收藏与浏览历史', '收藏', '浏览历史', 'wishlist', 'recently viewed'],
        # 当前前端原型以 Figma 为单一最新入口，不从本地 HTML 自动选版。
        'config_key': None,
        # 与个人中心共用源目录，仅发布本模块匹配的 PRD 文件。
        'sync_prd_only': True,
        'artifacts': {
            'prd': {
                'subdir': 'PRD',
                'pattern': r'looply-收藏与浏览历史-PRD-v(.+?)\.md',
            },
            'er': {
                'subdir': '实体关系图',
                'pattern': r'looply-收藏与浏览历史实体关系图-v(.+?)\.svg',
            },
            'delivery': {
                'subdir': '.',
                'pattern': r'收藏与浏览历史-交付开发 V(.+?)\.zip',
            },
        },
    },
    'account_center': {
        'name': '个人中心',
        'default_source': '$HOME/Desktop/个人中心',
        'target': 'docs-个人中心',
        'keywords': ['个人中心', 'account center', 'account'],
        # 当前前端设计稿以 Figma 为唯一入口，不从本地原型文件选版。
        'config_key': None,
        # 此目录也承载收藏与浏览历史；个人中心仅发布自身 PRD。
        'sync_prd_only': True,
        'artifacts': {
            'prd': {
                'subdir': 'PRD',
                'pattern': r'looply-个人中心-PRD-v(.+?)\.md',
            },
        },
    },
    'collection': {
        'name': 'Collection管理',
        'prd_variants': {
            'collection': {'pattern': r'looply-collection-landing-PRD-v(.+?)\.md', 'title': 'Collection 落地页 PRD'},
            'category': {'pattern': r'looply-类目管理-PRD-v(.+?)\.md', 'title': '类目管理 PRD'},
        },
        'default_source': '$HOME/Desktop/Collection管理',
        'target': 'docs-Collection管理',
        'keywords': ['collection', 'Collection', '类目', '类目管理'],
        'config_key': 'collection',
        'artifacts': {
            # 后台主原型锁定 antd 版：源目录同时存在 v0.x.html 与 v0.x-antd.html，
            # 版本号都解析为 0.x，必须用 -antd 后缀消歧，确保 antd 版作主原型。
            'prototype': {
                'subdir': '原型',
                'pattern': r'looply-类目管理-后台-v(.+?)-antd\.html',
                'exclude': r'(backup|对比|report)',
            },
            # 前台类目页原型（PC / Mobile），各自独立卡片
            'prototype_cat_pc': {
                'subdir': '原型',
                'pattern': r'looply-类目页-PC-v(.+?)\.html',
                'exclude': r'(无结果)',
            },
            'prototype_cat_mobile': {
                'subdir': '原型',
                'pattern': r'looply-类目页-Mobile-v(.+?)\.html',
            },
            # 类目管理 PRD 为本模块主 PRD（落地页内容已并入 v0.21）
            'prd': {
                'subdir': 'PRD',
                'pattern': r'looply-类目管理-PRD-v(.+?)\.md',
            },
            'er': {
                'subdir': '实体关系图',
                'pattern': r'looply-类目管理-ER-v(.+?)\.svg',
            },
        },
    },
    'order_list': {
        'name': '订单列表详情',
        'default_source': '$HOME/Desktop/海外业务/订单列表详情',
        'target': 'docs-订单列表详情',
        'keywords': ['订单列表', 'order_list', '订单详情'],
        'config_key': None,
        'artifacts': {
            'prd': {
                'subdir': 'PRD',
                'pattern': r'looply-C端订单列表与详情页-PRD-v(.+?)\.md',
            },
            'delivery': {
                'subdir': '.',
                'pattern': r'订单列表详情-交付开发 V(.+?)\.zip',
            },
        },
    },
    'contact': {
        'name': 'Contact Us',
        'default_source': '/Users/zz/Documents/Looply/deliveries/contact-us',
        'target': 'docs-Contact-Us',
        'keywords': ['contact', 'Contact Us', '联系我们'],
        'config_key': 'contact',
        'sidebar_group': '基础服务域',
        'artifacts': {
            'prototype': {
                'subdir': '原型',
                'pattern': r'looply-contact-us-prototype-v(.+?)\.html',
            },
            'prd': {
                'subdir': 'PRD',
                'pattern': r'looply-Contact-Us-PRD-v(.+?)\.md',
            },
            'delivery': {
                'subdir': '.',
                'pattern': r'Contact Us-交付开发 V(.+?)\.zip',
            },
        },
    },
    'privacy_legal': {
        'name': '隐私与法律',
        'default_source': '/Users/zz/Documents/Looply/deliveries/privacy-legal',
        'target': 'docs-隐私与法律',
        'keywords': ['隐私', '法律', 'privacy', 'legal'],
        'config_key': None,
        'sidebar_group': '基础服务域',
        'prd_variants': {
            'privacy_choices': {
                'pattern': r'looply-Your-Privacy-Choices-PRD-v(.+?)\.md',
                'title': 'Your Privacy Choices PRD',
            },
        },
        'artifacts': {
            'prototype': {
                'subdir': '原型',
                'pattern': r'looply-your-privacy-choices-web-demo-v(.+?)\.html',
            },
            'prd': {
                'subdir': 'PRD',
                'pattern': r'looply-Your-Privacy-Choices-PRD-v(.+?)\.md',
            },
            'delivery': {
                'subdir': '.',
                'pattern': r'隐私与法律-交付开发 V(.+?)\.zip',
            },
        },
    },
    'marketing': {
        'name': '营销活动',
        'default_source': '$HOME/Desktop/海外业务/营销活动',
        'target': 'docs-营销活动',
        'keywords': ['营销活动', 'marketing', 'promotion', '营销'],
        'config_key': 'marketing',
        'sidebar_group': '交易域',
        'artifacts': {
            'prototype': {
                'subdir': '原型',
                'pattern': r'looply-营销活动-antd-原型-v(.+?)\.html',
                'exclude': r'(backup|对比)',
            },
            'prd': {
                'subdir': 'PRD',
                'pattern': r'looply-营销活动-PRD-v(.+?)\.md',
            },
            'er': {
                'subdir': '实体关系图',
                'pattern': r'looply-营销活动实体关系图-v(.+?)\.svg',
            },
            'delivery': {
                'subdir': '.',
                'pattern': r'营销活动-交付开发 V(.+?)\.zip',
            },
        },
    },
    'aftersale': {
        'name': '售后',
        'default_source': '$HOME/Desktop/海外业务/售后',
        'target': 'docs-售后',
        'keywords': ['售后', 'aftersale', 'after_sale', 'aftersales'],
        'config_key': 'aftersale',
        'sidebar_group': '交易域',
        'artifacts': {
            'prototype': {
                'subdir': '原型',
                'pattern': r'looply-售后管理后台原型-v(.+?)\.html',
                'exclude': r'(backup|对比)',
            },
            'prd': {
                'subdir': 'PRD',
                'pattern': r'looply-售后-PRD-v(.+?)\.md',
            },
            'er': {
                'subdir': '实体关系图',
                'pattern': r'looply-售后模块实体关系图-v(.+?)\.svg',
            },
            'flowchart': {
                'subdir': '系统流程图',
                'pattern': r'looply-售后系统流程图-v(.+?)\.svg',
            },
            'delivery': {
                'subdir': '.',
                'pattern': r'售后-交付开发 V(.+?)\.zip',
            },
        },
    },
    'aftersale_cx': {
        'name': '售后列表详情',
        'default_source': '$HOME/Desktop/海外业务/售后列表详情',
        'target': 'docs-售后列表详情',
        'keywords': ['售后列表', '售后详情', '售后C端', 'aftersale_cx'],
        'config_key': None,
        'sidebar_group': '交易域',
        # UI/ 下的 HTML 原型自 PRD v1.0（2026-08-05）起已降级为历史参考，
        # 界面一律以 Figma 设计稿为准，不发布到文档中心以免开发照着过期原型实现。
        'skip_subdirs': ['UI'],
        'artifacts': {
            'prd': {
                'subdir': 'PRD',
                'pattern': r'looply-售后列表详情-PRD-v(.+?)\.md',
            },
            'delivery': {
                'subdir': '.',
                'pattern': r'售后列表详情-交付开发 V(.+?)\.zip',
            },
        },
    },
    'data_tracking': {
        'name': '数据采集与埋点',
        'default_source': '/Users/zz/Documents/Looply',
        'target': 'docs-数据采集与埋点',
        'keywords': ['数据采集', '埋点', 'data_tracking'],
        'config_key': None,
        'sidebar_group': '数据与分析',
        'artifacts': {
            'prd': {
                'subdir': 'PRD',
                'source_subdir': 'docs/product',
                'pattern': r'looply-数据采集与埋点产品需求-v(.+?)\.md',
            },
            'spec': {
                'subdir': '口径说明',
                'source_subdir': 'docs/product',
                'pattern': r'looply-GA4(?:首版变更清单|埋点变更清单)-v(.+?)\.md',
            },
            'delivery': {
                'subdir': '.',
                'pattern': r'数据采集与埋点-交付开发 V(.+?)\.zip',
            },
        },
    },
    'about': {
        'name': 'About Looply',
        'default_source': '/Users/zz/Documents/Looply/deliveries/about-us',
        'target': 'docs-About',
        'keywords': ['about', 'About', 'About Us', 'about-us', '品牌介绍'],
        'config_key': None,
        'sidebar_group': 'C端卖场',
        'artifacts': {
            'prd': {
                'subdir': 'PRD',
                'pattern': r'looply-About-PRD-v(.+?)\.md',
            },
            'ui_pc': {
                'subdir': 'UI',
                'pattern': r'looply-about-us-ui-pc-v(.+?)\.png',
            },
            'ui_mobile': {
                'subdir': 'UI',
                'pattern': r'looply-about-us-ui-mobile-v(.+?)\.png',
            },
            'delivery': {
                'subdir': '.',
                'pattern': r'About Looply-交付开发 V(.+?)\.zip',
            },
        },
    },
}

# ─── 自动发现新模块 ────────────────────────────────────────────────────────────────

def _infer_artifact(full_dir, subdir_name, expected_keyword=None):
    """扫描子目录，从文件名推断版本正则。返回 (pattern, ext) 或 (None, None)。"""
    d = os.path.join(full_dir, subdir_name)
    if not os.path.isdir(d):
        return None, None
    for fname in sorted(os.listdir(d)):
        if fname.startswith('.') or fname in ('latest.md', 'index.html'):
            continue
        if expected_keyword and expected_keyword not in fname:
            continue
        m = re.search(r'-[vV](.+?)\.(\w+)$', fname)
        if m and fname.startswith('looply-'):
            prefix = fname[:m.start()]
            ext = m.group(2)
            pattern = re.escape(prefix) + r'-v(.+?)\.' + re.escape(ext)
            return pattern, ext
    return None, None


def auto_discover_modules():
    """扫描 docs-*/ 目录，发现未注册模块并自动生成配置。"""
    registered_targets = {m['target'] for m in MODULES.values()}
    discovered = {}

    for entry in sorted(os.listdir(REPO_DIR)):
        full_path = os.path.join(REPO_DIR, entry)
        if not os.path.isdir(full_path) or not entry.startswith('docs-'):
            continue
        if entry in registered_targets or entry == 'docs':
            continue

        mod_name = entry.replace('docs-', '')
        artifacts = {}

        proto_pat, _ = _infer_artifact(full_path, '原型', '后台原型')
        if not proto_pat:
            proto_pat, _ = _infer_artifact(full_path, '原型')
        if proto_pat:
            artifacts['prototype'] = {'subdir': '原型', 'pattern': proto_pat}

        prd_pat, _ = _infer_artifact(full_path, 'PRD', 'PRD')
        if prd_pat:
            artifacts['prd'] = {'subdir': 'PRD', 'pattern': prd_pat}

        er_pat, _ = _infer_artifact(full_path, '实体关系图', '实体关系图')
        if er_pat:
            artifacts['er'] = {'subdir': '实体关系图', 'pattern': er_pat}

        arch_pat, _ = _infer_artifact(full_path, '产品架构图', '产品架构图')
        if arch_pat:
            artifacts['architecture'] = {'subdir': '产品架构图', 'pattern': arch_pat}

        flow_pat, _ = _infer_artifact(full_path, '系统流程图', '流程图')
        if flow_pat:
            artifacts['flowchart'] = {'subdir': '系统流程图', 'pattern': flow_pat}

        if not artifacts:
            # 检查是否只有调研文档（需求分析）
            for sub in ('调研', '需求分析'):
                if os.path.isdir(os.path.join(full_path, sub)):
                    artifacts['_has_content'] = True
                    break
            if not artifacts:
                continue

        config_key = mod_name if 'prototype' in artifacts else None

        discovered[f'_auto_{mod_name}'] = {
            'name': mod_name,
            'default_source': '',
            'target': entry,
            'keywords': [mod_name],
            'config_key': config_key,
            'artifacts': {k: v for k, v in artifacts.items() if k != '_has_content'},
            '_auto_discovered': True,
        }

    return discovered


# ─── index.html 区块自动生成 ──────────────────────────────────────────────────────

_CARD_META = {
    'er':           ('实体关系图',  'icon-svg',  'S'),
    'architecture': ('产品架构图',  'icon-svg',  'S'),
    'flowchart':    ('系统流程图',  'icon-svg',  'S'),
    'prototype':    ('后台原型',    'icon-html', 'H'),
    'dev_review':   ('开发评审版',  'icon-html', 'H'),
    'prd':          ('PRD 文档',    'icon-md',   'M'),
    'prd_md':       ('PRD 文档',    'icon-md',   'M'),
    'prd_html':     ('PRD 文档',    'icon-html', 'H'),
    'spec':         ('GA4 埋点变更', 'icon-md',   'M'),
    'delivery':     ('交付包',      'icon-zip',  'Z'),
    'ui_pc':        ('PC UI 基线',  'icon-html', 'P'),
    'ui_mobile':    ('Mobile UI 基线', 'icon-html', 'M'),
}

_STAGE2_TYPES = ('er', 'architecture', 'flowchart')
_STAGE3_TYPES = ('prototype', 'dev_review', 'prd', 'prd_md', 'prd_html', 'spec', 'ui_pc', 'ui_mobile', 'delivery')


def _gen_card(mod_name, target_dir, art_type, file_name, ver, today):
    """生成单个文档卡片 HTML。"""
    card_title, icon_cls, icon_letter = _CARD_META.get(art_type, ('文档', 'icon-md', 'D'))
    subdir = 'PRD' if art_type.startswith('prd') else {
        'er': '实体关系图', 'architecture': '产品架构图',
        'flowchart': '系统流程图', 'prototype': '原型', 'dev_review': '原型', 'spec': '口径说明',
        'ui_pc': 'UI', 'ui_mobile': 'UI',
    }.get(art_type, '')
    href = f'{target_dir}/{subdir}/{file_name}' if subdir else f'{target_dir}/{file_name}'

    # 文档显示名
    if art_type == 'prototype':
        doc_label = f'{mod_name}后台原型 v{ver}'
    elif art_type == 'dev_review':
        doc_label = f'{mod_name}开发评审版 v{ver}'
    elif art_type == 'delivery':
        doc_label = f'{mod_name}交付开发 V{ver}'
    elif art_type.startswith('prd'):
        doc_label = f'{mod_name} PRD v{ver}'
    elif art_type == 'spec':
        doc_label = f'GA4 埋点变更清单 v{ver}'
    elif art_type == 'er':
        doc_label = f'{mod_name}实体关系图 v{ver}'
    elif art_type == 'architecture':
        doc_label = f'{mod_name}产品架构图 v{ver}'
    elif art_type == 'flowchart':
        doc_label = f'{mod_name}系统流程图 v{ver}'
    elif art_type == 'ui_pc':
        doc_label = f'{mod_name} PC UI 基线 v{ver}'
    elif art_type == 'ui_mobile':
        doc_label = f'{mod_name} Mobile UI 基线 v{ver}'
    else:
        doc_label = f'{mod_name} v{ver}'

    dl_label = 'Markdown' if art_type == 'prd' or art_type == 'prd_md' else '下载'

    # 日期用文件 mtime（文件最后更新时间），取不到退回传入的 today
    _fpath = os.path.join(REPO_DIR, url_unquote(href))
    if os.path.isfile(_fpath):
        stamp = datetime.fromtimestamp(os.path.getmtime(_fpath)).strftime('%Y-%m-%d %H:%M')
    else:
        stamp = today

    return f"""
      <div class="card">
        <div class="card-title">{card_title}</div>
        <ul class="doc-list">
          <li class="doc-item">
            <div class="doc-icon {icon_cls}">{icon_letter}</div>
            <div class="doc-info">
              <div class="doc-name">{doc_label} <span class="badge">最新</span></div>
              <div class="doc-desc">更新于 {stamp}</div>
            </div>
            <div class="doc-actions">
              <a class="btn btn-view" href="{href}" target="_blank">查看</a>
              <a class="btn btn-download" href="{href}" download>{dl_label}</a>
            </div>
          </li>
        </ul>
      </div>"""


def generate_index_section(mod_name, target_dir, found_arts, today):
    """为新模块生成完整的 index.html 区块 HTML。
    found_arts: {art_type: (file_name, ver_str)}
    """
    stage2 = [(t, found_arts[t]) for t in _STAGE2_TYPES if t in found_arts]
    stage3 = [(t, found_arts[t]) for t in _STAGE3_TYPES if t in found_arts]

    parts = []
    parts.append(f'\n  <!-- ==================== {mod_name}模块 ==================== -->')
    parts.append(f'  <div class="module-section" data-module="{mod_name}">')

    if stage2:
        parts.append('')
        parts.append('    <!-- 阶段2 产品架构 -->')
        parts.append('    <div class="stage-group">')
        parts.append('      <div class="stage-header">')
        parts.append('        <div class="stage-dot" style="background:#8b5cf6"></div>')
        parts.append('        <span class="stage-label">阶段2 产品架构</span>')
        parts.append('        <div class="stage-line"></div>')
        parts.append('      </div>')
        for art_type, (fname, ver) in stage2:
            parts.append(_gen_card(mod_name, target_dir, art_type, fname, ver, today))
        parts.append('\n    </div>')

    if stage3:
        parts.append('')
        parts.append('    <!-- 阶段3 需求设计 -->')
        parts.append('    <div class="stage-group">')
        parts.append('      <div class="stage-header">')
        parts.append('        <div class="stage-dot" style="background:#3b82f6"></div>')
        parts.append('        <span class="stage-label">阶段3 需求设计</span>')
        parts.append('        <div class="stage-line"></div>')
        parts.append('      </div>')
        for art_type, (fname, ver) in stage3:
            parts.append(_gen_card(mod_name, target_dir, art_type, fname, ver, today))
        parts.append('    </div>')

    parts.append('')
    parts.append('  </div>')
    parts.append(f'  <!-- ==================== {mod_name}模块 END ==================== -->\n')

    return '\n'.join(parts)


def ensure_index_sections(new_modules_arts):
    """检查 index.html 中是否缺少模块区块，缺少则自动插入。
    new_modules_arts: {mod_key: {art_type: (file_name, ver_str)}}
    """
    index_path = os.path.join(REPO_DIR, 'index.html')
    content = open(index_path, 'r', encoding='utf-8').read()
    today = datetime.now().strftime('%Y-%m-%d %H:%M')
    inserted = []

    for mod_key, arts in new_modules_arts.items():
        mod_config = MODULES[mod_key]
        mod_name = mod_config['name']
        target_dir = mod_config['target']
        marker = f'<!-- ==================== {mod_name}模块 ==================== -->'
        if marker in content:
            continue
        if not arts:
            continue
        section = generate_index_section(mod_name, target_dir, arts, today)
        # 插入到 footer 之前
        # 容器收尾锚点（index.html 结构演进过，保留多个候选依次尝试）
        candidates = [
            '\n</div><!-- .container -->\n\n<div class="footer">',
            '\n</div>\n\n<div class="footer">',
        ]
        for insert_before in candidates:
            if insert_before in content:
                content = content.replace(insert_before, section + insert_before)
                inserted.append(mod_name)
                break
        else:
            print(f'  [警告] index.html 未找到插入锚点，{mod_name} 区块未生成')

    if inserted:
        # 侧边导航 GROUPS 是写死的 JS 数组，区块插了但导航没加 = 页面上点不到。
        for name in inserted:
            groups_match = re.search(r'var GROUPS = \[(.*?)\];', content, re.DOTALL)
            if groups_match and re.search(rf"['\"]{re.escape(name)}['\"]", groups_match.group(1)):
                continue
            mod_config = next((cfg for cfg in MODULES.values() if cfg['name'] == name), {})
            sidebar_group = mod_config.get('sidebar_group', '基础服务域')
            # 追加到该分组**末尾**：新模块自然落在分组底部，不打乱既有模块的排列顺序。
            # （早期为插到开头，导致每加一个新模块就把整组顺序推乱一次。）
            m = re.search(rf"\{{ name: '{re.escape(sidebar_group)}', modules: \[([^\]]*)\]", content)
            if m:
                inner = m.group(1).rstrip()
                new_inner = f"{inner}, '{name}'" if inner else f"'{name}'"
                content = content[:m.start(1)] + new_inner + content[m.end(1):]
                print(f'  [新增] index.html 侧边导航添加 {name}（{sidebar_group}，置于分组末尾）')
            else:
                print(f'  [警告] 未找到侧边导航 GROUPS，{name} 需手工加入导航')
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)
        for name in inserted:
            print(f'  [新增] index.html 添加 {name} 模块区块')
    return inserted


# ─── admin.html 自动更新 ─────────────────────────────────────────────────────────

def update_admin_html(all_proto_keys):
    """更新 admin.html 的 MODULES 数组，确保包含所有有原型的模块。
    all_proto_keys: [(config_key, label)] 按显示顺序排列
    """
    admin_path = os.path.join(REPO_DIR, 'admin.html')
    content = open(admin_path, 'r', encoding='utf-8').read()

    # 提取现有 MODULES 块
    m = re.search(r'(const MODULES = \[)(.*?)(\];)', content, re.DOTALL)
    if not m:
        return

    existing_block = m.group(2)

    # 解析已有条目的 key
    existing_keys = set(re.findall(r"key:\s*'([^']+)'", existing_block))

    # 检查是否有新条目需要添加
    new_entries = []
    for config_key, label in all_proto_keys:
        if config_key not in existing_keys:
            new_entries.append(f"  {{ key: '{config_key}', label: '{label}', url: P['{config_key}'] }},")

    if not new_entries:
        return

    # 在 ]; 之前插入新条目
    old_block = m.group(0)
    # 找到最后一个 }, 或 } 的位置
    last_entry_end = existing_block.rstrip()
    new_block = m.group(1) + existing_block.rstrip('\n') + '\n' + '\n'.join(new_entries) + '\n' + m.group(3)
    content = content.replace(old_block, new_block)

    with open(admin_path, 'w', encoding='utf-8') as f:
        f.write(content)
    for entry in new_entries:
        key_m = re.search(r"key: '([^']+)'", entry)
        if key_m:
            print(f'  [新增] admin.html 添加 {key_m.group(1)} 模块入口')


# ─── 失效配置巡检 ────────────────────────────────────────────────────────────────

def check_orphan_config():
    """巡检 prototype-config.js / admin.html 中指向已删除文件的残留配置。

    update_prototype_config() 与 update_admin_html() 都是「只增不删」：模块下线或
    目录搬迁后，配置里的旧条目不会被清理，后台菜单会静默变成死链（曾出现 CMS管理、
    翻译管理两项挂了 8 天无人发现）。这里只告警不自动删除，避免误伤——例如源文件
    临时未同步、或某次同步只跑了单个模块。
    """
    problems = []

    cfg_path = os.path.join(REPO_DIR, 'prototype-config.js')
    cfg_keys = set()
    if os.path.exists(cfg_path):
        content = open(cfg_path, 'r', encoding='utf-8').read()
        for key, path in re.findall(r"^\s*'([^']+)':\s*'([^']+)'", content, re.M):
            cfg_keys.add(key)
            if path.startswith('http'):
                continue
            if not os.path.isfile(os.path.join(REPO_DIR, path)):
                problems.append(f"prototype-config.js 的 '{key}' 指向的文件不存在 → {path}")

    admin_path = os.path.join(REPO_DIR, 'admin.html')
    if os.path.exists(admin_path):
        content = open(admin_path, 'r', encoding='utf-8').read()
        m = re.search(r'const MODULES = \[(.*?)\];', content, re.DOTALL)
        if m:
            for key in re.findall(r"key:\s*'([^']+)'", m.group(1)):
                if key == 'home' or key in cfg_keys:
                    continue
                problems.append(f"admin.html 的菜单项 '{key}' 在 prototype-config.js 中无对应路径")

    if problems:
        print('\n  [告警] 后台原型配置存在失效项（菜单点进去会 404，需手工清理）:')
        for p in problems:
            print(f'    - {p}')
    else:
        print('  [巡检] 后台原型配置全部有效')
    return problems


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

    # 个人中心与收藏/浏览历史共用源目录，按模块白名单隔离发布范围。
    if MODULES[mod_key].get('sync_prd_only'):
        src_prd = os.path.join(source_dir, 'PRD')
        if not os.path.isdir(src_prd):
            return
        dst_prd = os.path.join(REPO_DIR, target_dir, 'PRD')
        os.makedirs(dst_prd, exist_ok=True)
        for f in globmod.glob(os.path.join(src_prd, '*.md')):
            if os.path.isfile(f) and re.fullmatch(
                MODULES[mod_key]['artifacts']['prd']['pattern'], os.path.basename(f)
            ):
                smart_cp(f, dst_prd)
        latest_md = find_latest_prd_md(dst_prd)
        if latest_md:
            src_latest = os.path.join(dst_prd, latest_md)
            dst_latest = os.path.join(dst_prd, 'latest.md')
            if not os.path.isfile(dst_latest) or not files_equal(src_latest, dst_latest):
                shutil.copy2(src_latest, dst_latest)
        return

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

    # PRD；少数模块的源文件与原型不在同一子目录，可通过 source_subdir 指定。
    prd_config = MODULES.get(mod_key, {}).get('artifacts', {}).get('prd', {})
    src_prd = os.path.normpath(os.path.join(source_dir, prd_config.get('source_subdir', 'PRD')))
    if os.path.isdir(src_prd):
        dst_prd = os.path.join(REPO_DIR, target_dir, 'PRD')
        os.makedirs(dst_prd, exist_ok=True)
        # 社媒分享 PRD 用自包含 html 阅读器（无模板阅读器），需同步 .html
        prd_exts = ['.docx', '.md']
        if target_dir == 'docs-社媒分享管理':
            prd_exts.append('.html')
        for ext in prd_exts:
            for f in globmod.glob(os.path.join(src_prd, f'*{ext}')):
                if os.path.isfile(f) and (not prd_config.get('source_subdir') or re.match(prd_config.get('pattern', r'.*'), os.path.basename(f))):
                    smart_cp(f, dst_prd)
        # 用版本号（而非 mtime）选取最新 md 作为 latest.md
        if prd_config.get('source_subdir'):
            matched_md = [os.path.basename(f) for f in globmod.glob(os.path.join(src_prd, '*.md'))
                          if re.match(prd_config.get('pattern', r'.*'), os.path.basename(f))]
            latest_md = max(matched_md, key=lambda name: parse_version(re.match(prd_config['pattern'], name).group(1))) if matched_md else None
        else:
            latest_md = find_latest_prd_md(src_prd)
        if latest_md:
            dst_latest = os.path.join(dst_prd, 'latest.md')
            src_latest = os.path.join(src_prd, latest_md)
            if not os.path.isfile(dst_latest) or not files_equal(src_latest, dst_latest):
                shutil.copy2(src_latest, dst_latest)

    # 指标口径等模块专属说明文件；只同步注册正则命中的文件。
    spec_config = MODULES.get(mod_key, {}).get('artifacts', {}).get('spec', {})
    if spec_config:
        src_spec = os.path.normpath(os.path.join(source_dir, spec_config.get('source_subdir', spec_config['subdir'])))
        dst_spec = os.path.join(REPO_DIR, target_dir, spec_config['subdir'])
        if os.path.isdir(src_spec):
            os.makedirs(dst_spec, exist_ok=True)
            for f in globmod.glob(os.path.join(src_spec, '*.md')):
                if os.path.isfile(f) and re.fullmatch(spec_config['pattern'], os.path.basename(f)):
                    smart_cp(f, dst_spec)

    # 评审记录
    sync_subdir(source_dir, target_dir, '评审记录', ['.md'])

    # 验收记录
    sync_subdir(source_dir, target_dir, '验收记录', ['.md'])

    # 模块可声明 skip_subdirs 跳过某些子目录（如产物已迁 Figma、本地文件降级为历史参考）
    skip_subdirs = MODULES.get(mod_key, {}).get('skip_subdirs', [])

    # UI 设计稿
    if 'UI' not in skip_subdirs:
        sync_subdir(source_dir, target_dir, 'UI', ['.pen', '.html', '.png', '.jpg', '.jpeg'])

    # 原型（HTML + 图片）；一个模块可声明多个原型制品及各自的源/目标子目录。
    for art_type, prototype_config in MODULES.get(mod_key, {}).get('artifacts', {}).items():
        if not art_type.startswith('prototype'):
            continue
        prototype_source_subdir = prototype_config.get('source_subdir', '原型')
        src_proto = os.path.normpath(os.path.join(source_dir, prototype_source_subdir))
        dst_proto = os.path.join(REPO_DIR, target_dir, prototype_config.get('subdir', '原型'))
        if not os.path.isdir(src_proto):
            continue
        os.makedirs(dst_proto, exist_ok=True)
        prototype_pattern = prototype_config.get('pattern', r'.*')
        restrict_to_pattern = 'source_subdir' in prototype_config
        for ext in ['.html', '.png', '.jpg', '.svg']:
            for f in globmod.glob(os.path.join(src_proto, f'*{ext}')):
                excluded = prototype_config.get('exclude') and re.search(prototype_config['exclude'], os.path.basename(f), re.I)
                if os.path.isfile(f) and not excluded and (not restrict_to_pattern or re.fullmatch(prototype_pattern, os.path.basename(f))):
                    smart_cp(f, dst_proto)

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
    for delivery_dir in globmod.glob(os.path.join(source_dir, '*交付开发*')):
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
    # 已注册模块按固定顺序排前面，自动发现的追加在后面
    _fixed_order = ['product', 'market', 'inventory', 'translation', 'exchange', 'user', 'pdp']
    ordered_keys = [k for k in _fixed_order if k in current]
    for k in sorted(current.keys()):
        if k not in ordered_keys:
            ordered_keys.append(k)
    if not ordered_keys:
        return
    lines = []
    max_key_len = max(len(k) for k in ordered_keys)
    for key in ordered_keys:
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


def build_delivery_desc(zip_path):
    """从交付包 zip 内容生成 doc-desc：清爽的「类型 版本」清单（覆盖全部文件），如
    'PRD v1.7 + CMS 后台原型 v3 + 差异汇总 + 图片资源 &middot; 日期'。"""
    if not os.path.isfile(zip_path):
        return None

    _ORDER = {'prd': 1, 'proto': 2, 'pc': 3, 'app': 4, 'er': 5, 'arch': 6, 'flow': 7,
              'diff': 8, 'changelog': 9, 'doc': 10, 'img': 99}
    parts = []
    has_images = False

    with zipfile.ZipFile(zip_path, 'r') as zf:
        for info in zf.infolist():
            raw_name = info.filename
            try:
                raw_name = raw_name.encode('cp437').decode('utf-8')
            except (UnicodeDecodeError, UnicodeEncodeError):
                pass
            basename = os.path.basename(raw_name)
            if not basename or basename.startswith('.'):
                continue
            low = basename.lower()

            m = re.search(r'PRD[- ]*[vV](.+?)\.md', basename)
            if m:
                parts.append((_ORDER['prd'], f'PRD v{m.group(1)}')); continue
            m = re.search(r'(?:CMS[^.]*)?后台原型[- ]*[vV](.+?)\.html', basename)
            if m:
                label = 'CMS 后台原型' if 'CMS' in basename else '后台原型'
                parts.append((_ORDER['proto'], f'{label} v{m.group(1)}')); continue
            m = re.search(r'-PC[- ]*[vV](.+?)\.html', basename)
            if m:
                parts.append((_ORDER['pc'], f'PC 原型 v{m.group(1)}')); continue
            m = re.search(r'-APP[- ]*[vV](.+?)\.html', basename)
            if m:
                parts.append((_ORDER['app'], f'APP 原型 v{m.group(1)}')); continue
            m = re.search(r'原型[- ]*[vV](.+?)\.html', basename)
            if m:
                parts.append((_ORDER['proto'], f'后台原型 v{m.group(1)}')); continue
            m = re.search(r'prototype[- ]*[vV](.+?)\.html', basename, re.IGNORECASE)
            if m:
                parts.append((_ORDER['proto'], f'原型 v{m.group(1)}')); continue
            m = re.search(r'实体关系图[- ]*[vV](.+?)\.(?:svg|html)', basename)
            if m:
                parts.append((_ORDER['er'], f'ER图 v{m.group(1)}')); continue
            m = re.search(r'产品架构图[- ]*[vV](.+?)\.svg', basename)
            if m:
                parts.append((_ORDER['arch'], f'架构图 v{m.group(1)}')); continue
            m = re.search(r'流程图[- ]*[vV](.+?)\.svg', basename)
            if m:
                parts.append((_ORDER['flow'], f'流程图 v{m.group(1)}')); continue

            if low.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                has_images = True; continue
            if basename.endswith('.md'):
                if '差异' in basename or '汇总' in basename or 'diff' in low:
                    parts.append((_ORDER['diff'], '差异汇总')); continue
                if '变更日志' in basename or 'changelog' in low:
                    parts.append((_ORDER['changelog'], '变更日志')); continue
                parts.append((_ORDER['doc'], os.path.splitext(basename)[0])); continue
            # 其他文件：列基础名兜底，确保不漏
            parts.append((_ORDER['doc'], basename))

    if has_images:
        parts.append((_ORDER['img'], '图片资源'))

    if not parts:
        return None

    parts.sort(key=lambda x: x[0])
    seen, labels = set(), []
    for _, label in parts:
        if label not in seen:
            seen.add(label); labels.append(label)

    date_str = datetime.fromtimestamp(os.path.getmtime(zip_path)).strftime('%Y-%m-%d %H:%M')
    return ' + '.join(labels) + f' &middot; {date_str}'


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
            href_dir_encoded = url_quote(href_dir, safe='/')
            href_variants = [re.escape(href_dir)]
            if href_dir_encoded != href_dir:
                href_variants.append(re.escape(href_dir_encoded))
            # 部分编码变体：仅模块目录名编码，子目录保持原文
            parts = href_dir.rstrip('/').split('/')
            if len(parts) >= 1:
                partial = url_quote(parts[0], safe='-') + '/' + '/'.join(parts[1:]) + '/'
                if partial not in (href_dir, href_dir_encoded):
                    href_variants.append(re.escape(partial))
            regex = re.compile(r'(href="(?:' + '|'.join(href_variants) + r'))([^"]+)(")')
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
                        rel_path = url_unquote(os.path.join(href_dir, new_file))
                        if rel_path in _updated_files:
                            changed_items.add(current_item_start)
                        else:
                            # 文件内容已同步但日期可能过时：用源文件 mtime 对比页面日期（含时分，避免同日不同时被漏判）
                            dst_file = os.path.join(REPO_DIR, rel_path)
                            if os.path.isfile(dst_file):
                                file_date = datetime.fromtimestamp(os.path.getmtime(dst_file)).strftime('%Y-%m-%d %H:%M')
                                # 检查页面上的日期是否早于文件日期（按 年-月-日 时:分 比较，页面无时分时也判为更早）
                                for scan_j in range(current_item_start, min(current_item_start + 10, len(lines))):
                                    m = re.search(r'更新于 (\d{4}-\d{2}-\d{2}(?: \d{2}:\d{2})?)', lines[scan_j])
                                    if m and m.group(1) < file_date:
                                        changed_items.add(current_item_start)
                                        break

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
                    new_ver_text = f'{"V" if upd.get("art_type") == "delivery" else "v"}{new_ver}'
                    if old_ver_text != new_ver_text:
                        new_line = new_line[:ver_match.start()] + new_ver_text + new_line[ver_match.end():]
                        changed = True
        if current_item_start in changed_items and 'doc-desc' in new_line and '更新于' in new_line:
            # 日期用文件 mtime（文件最后更新时间），非脚本运行时间；取不到再退回 now
            file_dt = None
            _upd = item_map.get(current_item_start)
            if _upd and _upd.get('href_dir') and _upd.get('new_file'):
                _fpath = os.path.join(REPO_DIR, url_unquote(_upd['href_dir'] + _upd['new_file']))
                if os.path.isfile(_fpath):
                    file_dt = datetime.fromtimestamp(os.path.getmtime(_fpath)).strftime('%Y-%m-%d %H:%M')
            stamp = file_dt or datetime.now().strftime('%Y-%m-%d %H:%M')
            new_line = re.sub(r'更新于 \d{4}-\d{2}-\d{2}(\s+\d{2}:\d{2})?', f'更新于 {stamp}', new_line)
            if new_line != line:
                changed = True
        if current_item_start in changed_items and 'doc-desc' in new_line and ('含 PRD' in new_line or '含原型' in new_line):
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
        # 交付包 doc-desc 自动生成（基于 zip 内容）
        if current_item_start in item_map and item_map[current_item_start].get('art_type') == 'delivery' and 'doc-desc' in new_line:
            upd = item_map[current_item_start]
            zip_rel = upd['href_dir'] + upd['new_file']
            zip_path = os.path.join(REPO_DIR, zip_rel)
            desc = build_delivery_desc(zip_path)
            if desc:
                new_line = re.sub(r'(<div class="doc-desc">).*?(</div>)', rf'\1{desc}\2', new_line)
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
                        href_prefix_encoded = url_quote(href_prefix, safe='/')
                        # 部分编码变体
                        hp_parts = href_prefix.rstrip('/').split('/')
                        href_prefix_partial = url_quote(hp_parts[0], safe='-') + '/' + '/'.join(hp_parts[1:]) + '/' if len(hp_parts) >= 1 else ''
                        if href_prefix not in lookback and href_prefix_encoded not in lookback and (not href_prefix_partial or href_prefix_partial not in lookback):
                            continue
                        prefix_alts = [re.escape(href_prefix)]
                        if href_prefix_encoded != href_prefix:
                            prefix_alts.append(re.escape(href_prefix_encoded))
                        if href_prefix_partial and href_prefix_partial not in (href_prefix, href_prefix_encoded):
                            prefix_alts.append(re.escape(href_prefix_partial))
                        # 遍历卡片里的**所有** href，任一匹配文件名规则即命中。
                        # 不能只取第一个：PRD 卡的第一个按钮通常是「查看 → PRD/index.html」（在线阅读器），
                        # 它匹配不上 looply-xxx-PRD-vN.md，只看第一个会误判成「这不是 PRD 卡」而跳过历史版本。
                        href_m = None
                        for cand in re.finditer(r'href="(?:' + '|'.join(prefix_alts) + r')([^"]+)"', lookback):
                            fname = cand.group(1)
                            if re.match(file_pattern, fname) or re.match(file_pattern, url_unquote(fname)):
                                href_m = cand
                                break
                        if href_m:
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
                href_prefix_enc = url_quote(href_prefix, safe='/')
                for hist_file, hist_ver in history:
                    href = f'{href_prefix_enc}{hist_file}'
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


def update_prd_variants():
    """多 PRD 混装目录：为每份 PRD 维护独立的 latest-{key}.md 与命名阅读器。

    背景：find_latest_prd_md 是跨全目录取版本号最大的 .md，与 PRD 归属无关。
    一个目录塞多份 PRD 时（如 Collection管理 有 collection-landing 和 类目管理），
    latest.md 会被版本号最大的那份占据，且随版本增长可能突然切换到另一份 PRD。
    故为每份 PRD 单独维护 latest 文件，命名阅读器各读各的。
    """
    updated = []
    for mod_key, cfg in MODULES.items():
        variants = cfg.get('prd_variants')
        if not variants:
            continue
        prd_dir = os.path.join(REPO_DIR, cfg['target'], 'PRD')
        if not os.path.isdir(prd_dir):
            continue
        for vkey, vcfg in variants.items():
            pat = re.compile(vcfg['pattern'])
            best, best_ver = None, (0,)
            for fname in os.listdir(prd_dir):
                m = pat.fullmatch(fname)
                if not m:
                    continue
                ver = tuple(int(x) for x in m.group(1).split('.'))
                if ver > best_ver:
                    best_ver, best = ver, fname
            if not best:
                continue
            ver_str = '.'.join(str(x) for x in best_ver)
            # 1) 维护该 PRD 专属的 latest 文件
            latest_name = f'latest-{vkey}.md'
            shutil.copy2(os.path.join(prd_dir, best),
                         os.path.join(prd_dir, latest_name))
            # 2) 更新命名阅读器：数据源指向自己的 latest、topbar 写自己的版本
            reader = os.path.join(prd_dir, f'index-{vkey}.html')
            if os.path.isfile(reader):
                html = open(reader, encoding='utf-8').read()
                html = re.sub(r"latest(?:-[\w]+)?\.md", latest_name, html)
                html = re.sub(r'<span class="title">[^<]*</span>',
                              f'<span class="title">{vcfg["title"]} V{ver_str}</span>',
                              html, count=1)
                html = re.sub(r'<title>[^<]*</title>',
                              f'<title>Looply PRD - {vcfg["title"]}</title>',
                              html, count=1)
                open(reader, 'w', encoding='utf-8').write(html)
            updated.append(f'{cfg["name"]}/{vkey} v{ver_str}')
    if updated:
        for u in updated:
            print(f'  [更新] PRD 变体 {u}')
    return updated


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
                m = re.search(r'[版本]\*{0,2}\s*[:：]\s*[vV]?([\d.]+)', line)
                if not m:
                    m = re.search(r'PRD\s+[vV]([\d.]+)', line)
                if not m:
                    m = re.search(r'[*]*版本[*]*\s*[:：]\s*[vV]?([\d.]+)', line)
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

    # Phase 0: 自动发现新模块
    discovered = auto_discover_modules()
    if discovered:
        MODULES.update(discovered)
        for dk, dc in discovered.items():
            print(f'  [自动发现] {dc["name"]} → {dc["target"]}')

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

    if not synced_modules and not discovered:
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
                if art_type == 'prototype' and config_key:
                    subdir_nv = art_config['subdir']
                    pat_nv = art_config['pattern']
                    target_sub = os.path.join(REPO_DIR, module_dir, subdir_nv)
                    if os.path.isdir(target_sub):
                        for fname in os.listdir(target_sub):
                            if re.fullmatch(pat_nv, fname):
                                rel = f'{module_dir}/{subdir_nv}/{fname}' if subdir_nv != '.' else f'{module_dir}/{fname}'
                                latest_prototypes[config_key] = rel
                                break
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

    # 为本次同步且尚未展示的模块生成 index.html 区块
    if synced_modules:
        new_arts = {}
        for mod_key in synced_modules:
            arts = {}
            mod_config = MODULES[mod_key]
            for art_type, art_config in mod_config.get('artifacts', {}).items():
                ver_key = (mod_key, art_type)
                if ver_key in all_versions:
                    fname, _ = find_latest_file(
                        mod_config['target'], art_config['subdir'],
                        art_config['pattern'], art_config.get('exclude'))
                    if fname:
                        arts[art_type] = (fname, all_versions[ver_key])
            if arts:
                new_arts[mod_key] = arts
        if new_arts:
            ensure_index_sections(new_arts)

    if index_updates:
        update_index_html(index_updates, all_versions, all_history)

    update_prd_variants()
    update_prd_index_topbar()

    # 更新 admin.html 的模块列表
    all_proto_keys = []
    for mod_key, mod_config in MODULES.items():
        ck = mod_config.get('config_key')
        if ck and ck in (latest_prototypes or {}):
            all_proto_keys.append((ck, mod_config['name']))
        elif ck:
            # 检查 prototype-config.js 中是否已存在
            cfg_path = os.path.join(REPO_DIR, 'prototype-config.js')
            if os.path.exists(cfg_path):
                cfg_content = open(cfg_path, 'r', encoding='utf-8').read()
                if f"'{ck}'" in cfg_content:
                    all_proto_keys.append((ck, mod_config['name']))
    if all_proto_keys:
        update_admin_html(all_proto_keys)

    # 收尾巡检：暴露指向已删除文件的残留配置（只告警，不自动删）
    check_orphan_config()

    # Phase 3: Git
    print('\n[Phase 3] Git 提交...')
    if os.environ.get('SYNC_SKIP_GIT') == '1':
        print('  [跳过] 按调用方要求保留 Git 提交步骤，稍后按模块范围提交')
        return
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
