#!/usr/bin/env python3
"""
结构图表生成器 - 基于 graphviz
支持：流程图、架构图、泳道图、层次图、关系图、时序流、对比图

用法：
    python generate_diagram.py --config diagram_config.json --output output.png --theme tech-blue

diagram_config.json 示例见本文件末尾的 EXAMPLES。
"""

import json
import sys
import argparse
import platform

import graphviz


# ============================================================
# 主题配置
# ============================================================

THEMES = {
    'tech-blue': {
        'graph': {'bgcolor': 'white', 'fontsize': '12', 'rankdir': 'TB',
                  'splines': 'ortho', 'nodesep': '0.8', 'ranksep': '1.0', 'pad': '0.5'},
        'node': {'shape': 'box', 'style': 'rounded,filled', 'fillcolor': '#EFF6FF',
                 'color': '#2563EB', 'fontsize': '11', 'fontcolor': '#1E3A5F',
                 'penwidth': '1.5', 'margin': '0.3,0.15'},
        'edge': {'color': '#6B7280', 'fontsize': '10', 'fontcolor': '#6B7280',
                 'arrowsize': '0.8', 'penwidth': '1.2'},
        'node_types': {
            'highlight': {'fillcolor': '#2563EB', 'fontcolor': 'white'},
            'warning': {'fillcolor': '#FEF3C7', 'color': '#F59E0B'},
            'success': {'fillcolor': '#D1FAE5', 'color': '#10B981'},
            'danger': {'fillcolor': '#FEE2E2', 'color': '#EF4444'},
            'group': {'style': 'rounded,dashed', 'fillcolor': '#F9FAFB', 'color': '#D1D5DB'},
        }
    },
    'biz-warm': {
        'graph': {'bgcolor': 'white', 'fontsize': '12', 'rankdir': 'TB',
                  'splines': 'curved', 'nodesep': '0.8', 'ranksep': '1.0'},
        'node': {'shape': 'box', 'style': 'rounded,filled', 'fillcolor': '#FFF7ED',
                 'color': '#F97316', 'fontsize': '11', 'fontcolor': '#44403C',
                 'penwidth': '1.5', 'margin': '0.3,0.15'},
        'edge': {'color': '#78716C', 'fontsize': '10', 'arrowsize': '0.8', 'penwidth': '1.2'},
        'node_types': {
            'highlight': {'fillcolor': '#1E40AF', 'fontcolor': 'white'},
            'secondary': {'fillcolor': '#FFEDD5', 'color': '#EA580C'},
            'success': {'fillcolor': '#DCFCE7', 'color': '#22C55E'},
            'group': {'style': 'rounded,dashed', 'fillcolor': '#FFFBEB', 'color': '#D6D3D1'},
        }
    },
    'academic': {
        'graph': {'bgcolor': 'white', 'fontsize': '11', 'rankdir': 'TB',
                  'splines': 'ortho', 'nodesep': '0.6', 'ranksep': '0.8'},
        'node': {'shape': 'box', 'style': 'filled', 'fillcolor': 'white',
                 'color': '#374151', 'fontsize': '10', 'fontcolor': '#1F2937',
                 'penwidth': '1.0', 'margin': '0.25,0.12'},
        'edge': {'color': '#6B7280', 'fontsize': '9', 'arrowsize': '0.7', 'penwidth': '1.0'},
        'node_types': {
            'highlight': {'fillcolor': '#E5E7EB', 'penwidth': '2.0'},
            'group': {'style': 'dashed', 'fillcolor': '#F9FAFB', 'color': '#9CA3AF'},
        }
    },
    'dark-tech': {
        'graph': {'bgcolor': '#0F172A', 'fontsize': '12', 'fontcolor': '#E2E8F0',
                  'rankdir': 'TB', 'splines': 'ortho', 'nodesep': '0.8', 'ranksep': '1.0'},
        'node': {'shape': 'box', 'style': 'filled', 'fillcolor': '#1E293B',
                 'color': '#22D3EE', 'fontsize': '11', 'fontcolor': '#E2E8F0',
                 'penwidth': '1.5', 'margin': '0.3,0.15'},
        'edge': {'color': '#475569', 'fontsize': '10', 'fontcolor': '#94A3B8',
                 'arrowsize': '0.8', 'penwidth': '1.2'},
        'node_types': {
            'highlight': {'color': '#34D399', 'fillcolor': '#064E3B'},
            'warning': {'color': '#FBBF24', 'fillcolor': '#422006'},
            'danger': {'color': '#F87171', 'fillcolor': '#450A0A'},
            'group': {'style': 'dashed', 'fillcolor': '#0F172A', 'color': '#334155'},
        }
    },
    'product': {
        'graph': {'bgcolor': 'white', 'fontsize': '12', 'rankdir': 'LR',
                  'splines': 'curved', 'nodesep': '0.8', 'ranksep': '1.2'},
        'node': {'shape': 'box', 'style': 'rounded,filled', 'fillcolor': '#F5F3FF',
                 'color': '#6366F1', 'fontsize': '11', 'fontcolor': '#312E81',
                 'penwidth': '1.5', 'margin': '0.3,0.15'},
        'edge': {'color': '#9CA3AF', 'fontsize': '10', 'arrowsize': '0.8', 'penwidth': '1.0'},
        'node_types': {
            'product_a': {'fillcolor': '#EEF2FF', 'color': '#6366F1'},
            'product_b': {'fillcolor': '#FCE7F3', 'color': '#EC4899'},
            'product_c': {'fillcolor': '#CCFBF1', 'color': '#14B8A6'},
            'winner': {'fillcolor': '#6366F1', 'fontcolor': 'white', 'penwidth': '2.5'},
            'group': {'style': 'rounded,dashed', 'fillcolor': '#F9FAFB', 'color': '#D1D5DB'},
        }
    },
}


def get_font():
    """获取当前系统可用的中文字体。"""
    system = platform.system()
    if system == 'Darwin':
        return 'PingFang SC'
    elif system == 'Linux':
        return 'Noto Sans CJK SC'
    else:
        return 'Microsoft YaHei'


def build_graph(config, theme_name, output):
    """根据配置生成 graphviz 图表。"""
    theme = THEMES.get(theme_name, THEMES['tech-blue'])
    font = get_font()

    # 基础属性
    graph_attrs = {**theme['graph'], 'fontname': font}
    node_attrs = {**theme['node'], 'fontname': font}
    edge_attrs = {**theme['edge'], 'fontname': font}

    # 覆盖方向（如果配置指定了）
    if 'rankdir' in config:
        graph_attrs['rankdir'] = config['rankdir']

    # 创建图
    dot = graphviz.Digraph(
        config.get('title', 'diagram'),
        graph_attr=graph_attrs,
        node_attr=node_attrs,
        edge_attr=edge_attrs,
    )

    # 添加标题
    if config.get('title'):
        dot.attr(label=config['title'], labelloc='t', fontsize='16')

    # 添加子图（泳道 / 分组）
    for i, group in enumerate(config.get('groups', [])):
        with dot.subgraph(name=f'cluster_{i}') as sg:
            group_style = theme.get('node_types', {}).get('group', {})
            sg.attr(label=group['label'], fontname=font, fontsize='13',
                    style=group_style.get('style', 'rounded,dashed'),
                    color=group_style.get('color', '#D1D5DB'),
                    fillcolor=group_style.get('fillcolor', '#F9FAFB'),
                    bgcolor=group_style.get('fillcolor', '#F9FAFB'))
            for node in group.get('nodes', []):
                attrs = _node_attrs(node, theme)
                sg.node(node['id'], node.get('label', node['id']), **attrs)

    # 添加独立节点
    for node in config.get('nodes', []):
        attrs = _node_attrs(node, theme)
        dot.node(node['id'], node.get('label', node['id']), **attrs)

    # 添加边
    for edge in config.get('edges', []):
        edge_extra = {}
        if 'label' in edge:
            edge_extra['label'] = edge['label']
        if 'style' in edge:
            edge_extra['style'] = edge['style']
        if 'color' in edge:
            edge_extra['color'] = edge['color']
        dot.edge(edge['from'], edge['to'], **edge_extra)

    # 渲染
    # output 可能是 "path/to/file.png"，需要去掉扩展名
    output_base = output.rsplit('.', 1)[0] if '.' in output else output
    output_format = output.rsplit('.', 1)[1] if '.' in output else 'png'

    dot.render(output_base, format=output_format, cleanup=True)
    print(f'图表已生成: {output}')


def _node_attrs(node, theme):
    """根据节点类型获取样式属性。"""
    attrs = {}
    node_type = node.get('type')
    if node_type and node_type in theme.get('node_types', {}):
        attrs.update(theme['node_types'][node_type])
    # 允许节点级别的自定义属性覆盖主题
    for key in ['shape', 'style', 'fillcolor', 'color', 'fontcolor', 'penwidth']:
        if key in node:
            attrs[key] = node[key]
    return attrs


def main():
    parser = argparse.ArgumentParser(description='生成结构图表')
    parser.add_argument('--config', required=True, help='图表配置 JSON 文件路径')
    parser.add_argument('--output', required=True, help='输出文件路径（如 output.png）')
    parser.add_argument('--theme', default='tech-blue', help='主题名称')
    args = parser.parse_args()

    with open(args.config, 'r', encoding='utf-8') as f:
        config = json.load(f)

    build_graph(config, args.theme, args.output)


if __name__ == '__main__':
    main()


# ============================================================
# 配置示例（供参考，不执行）
# ============================================================
"""
流程图:
{
    "title": "用户认证流程",
    "rankdir": "TB",
    "nodes": [
        {"id": "start", "label": "用户请求", "shape": "ellipse"},
        {"id": "auth", "label": "身份验证"},
        {"id": "check", "label": "权限检查"},
        {"id": "ok", "label": "允许访问", "type": "success"},
        {"id": "deny", "label": "拒绝访问", "type": "danger"}
    ],
    "edges": [
        {"from": "start", "to": "auth"},
        {"from": "auth", "to": "check", "label": "验证通过"},
        {"from": "auth", "to": "deny", "label": "验证失败"},
        {"from": "check", "to": "ok", "label": "有权限"},
        {"from": "check", "to": "deny", "label": "无权限"}
    ]
}

泳道图:
{
    "title": "订单处理流程",
    "rankdir": "LR",
    "groups": [
        {
            "label": "用户端",
            "nodes": [
                {"id": "submit", "label": "提交订单"},
                {"id": "pay", "label": "支付"}
            ]
        },
        {
            "label": "订单服务",
            "nodes": [
                {"id": "create", "label": "创建订单"},
                {"id": "validate", "label": "校验库存"}
            ]
        },
        {
            "label": "支付服务",
            "nodes": [
                {"id": "charge", "label": "扣款"},
                {"id": "notify", "label": "通知结果"}
            ]
        }
    ],
    "edges": [
        {"from": "submit", "to": "create"},
        {"from": "create", "to": "validate"},
        {"from": "validate", "to": "pay", "label": "库存充足"},
        {"from": "pay", "to": "charge"},
        {"from": "charge", "to": "notify"}
    ]
}

架构图:
{
    "title": "微服务架构",
    "rankdir": "TB",
    "groups": [
        {
            "label": "接入层",
            "nodes": [
                {"id": "gateway", "label": "API Gateway", "type": "highlight"}
            ]
        },
        {
            "label": "服务层",
            "nodes": [
                {"id": "user", "label": "用户服务"},
                {"id": "order", "label": "订单服务"},
                {"id": "pay", "label": "支付服务"}
            ]
        },
        {
            "label": "数据层",
            "nodes": [
                {"id": "mysql", "label": "MySQL"},
                {"id": "redis", "label": "Redis"}
            ]
        }
    ],
    "edges": [
        {"from": "gateway", "to": "user"},
        {"from": "gateway", "to": "order"},
        {"from": "gateway", "to": "pay"},
        {"from": "user", "to": "mysql"},
        {"from": "order", "to": "mysql"},
        {"from": "pay", "to": "redis"}
    ]
}
"""
