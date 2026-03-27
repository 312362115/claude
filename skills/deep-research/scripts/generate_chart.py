#!/usr/bin/env python3
"""
统计图表生成器 - 基于 matplotlib
支持：柱状图、分组柱状图、折线图、饼图、环形图、雷达图、热力图、散点图、堆叠柱状图

用法：
    python generate_chart.py --config chart_config.json --output output.png
"""

import json
import sys
import argparse
import platform
import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap


# ============================================================
# 主题配置 — 每个主题包含调色板 + 全局样式 + 渐变色
# ============================================================

THEMES = {
    'tech-blue': {
        'palette': ['#3B82F6', '#60A5FA', '#F59E0B', '#10B981', '#8B5CF6', '#EF4444', '#EC4899', '#6B7280'],
        'gradient_pairs': [('#3B82F6', '#93C5FD'), ('#60A5FA', '#BFDBFE'), ('#F59E0B', '#FDE68A'),
                           ('#10B981', '#6EE7B7'), ('#8B5CF6', '#C4B5FD'), ('#EF4444', '#FCA5A5')],
        'heatmap_cmap': ['#EFF6FF', '#BFDBFE', '#60A5FA', '#2563EB', '#1E40AF'],
        'bg': 'white', 'text': '#1E293B', 'subtitle': '#64748B', 'grid': '#F1F5F9',
    },
    'biz-warm': {
        'palette': ['#2563EB', '#F97316', '#0EA5E9', '#22C55E', '#A855F7', '#DC2626', '#EC4899', '#78716C'],
        'gradient_pairs': [('#2563EB', '#93C5FD'), ('#F97316', '#FDBA74'), ('#0EA5E9', '#7DD3FC'),
                           ('#22C55E', '#86EFAC'), ('#A855F7', '#C4B5FD'), ('#DC2626', '#FCA5A5')],
        'heatmap_cmap': ['#FFF7ED', '#FED7AA', '#FB923C', '#EA580C', '#9A3412'],
        'bg': 'white', 'text': '#292524', 'subtitle': '#78716C', 'grid': '#F5F5F4',
    },
    'academic': {
        'palette': ['#374151', '#6B7280', '#9CA3AF', '#4B5563', '#1F2937', '#D1D5DB', '#111827', '#E5E7EB'],
        'gradient_pairs': [('#374151', '#6B7280'), ('#6B7280', '#9CA3AF'), ('#9CA3AF', '#D1D5DB'),
                           ('#4B5563', '#9CA3AF'), ('#1F2937', '#374151'), ('#D1D5DB', '#E5E7EB')],
        'heatmap_cmap': ['#F9FAFB', '#E5E7EB', '#9CA3AF', '#4B5563', '#1F2937'],
        'bg': 'white', 'text': '#111827', 'subtitle': '#6B7280', 'grid': '#F3F4F6',
    },
    'dark-tech': {
        'palette': ['#22D3EE', '#A78BFA', '#34D399', '#FBBF24', '#F87171', '#FB923C', '#E879F9', '#9CA3AF'],
        'gradient_pairs': [('#22D3EE', '#0E7490'), ('#A78BFA', '#6D28D9'), ('#34D399', '#047857'),
                           ('#FBBF24', '#B45309'), ('#F87171', '#B91C1C'), ('#FB923C', '#C2410C')],
        'heatmap_cmap': ['#0F172A', '#1E3A5F', '#0EA5E9', '#22D3EE', '#ECFEFF'],
        'bg': '#0F172A', 'text': '#F1F5F9', 'subtitle': '#94A3B8', 'grid': '#1E293B',
    },
    'product': {
        'palette': ['#6366F1', '#EC4899', '#14B8A6', '#F59E0B', '#3B82F6', '#EF4444', '#8B5CF6', '#06B6D4'],
        'gradient_pairs': [('#6366F1', '#A5B4FC'), ('#EC4899', '#F9A8D4'), ('#14B8A6', '#5EEAD4'),
                           ('#F59E0B', '#FDE68A'), ('#3B82F6', '#93C5FD'), ('#EF4444', '#FCA5A5')],
        'heatmap_cmap': ['#F5F3FF', '#C4B5FD', '#8B5CF6', '#6D28D9', '#4C1D95'],
        'bg': 'white', 'text': '#1E1B4B', 'subtitle': '#6B7280', 'grid': '#F5F3FF',
    },
}


def setup_chinese_font():
    """自动检测并设置中文字体。"""
    system = platform.system()
    if system == 'Darwin':
        candidates = ['PingFang SC', 'STHeiti', 'Heiti TC', 'Arial Unicode MS']
    elif system == 'Linux':
        candidates = ['Noto Sans CJK SC', 'WenQuanYi Micro Hei', 'Droid Sans Fallback']
    else:
        candidates = ['Microsoft YaHei', 'SimHei', 'FangSong']

    available = [f.name for f in font_manager.fontManager.ttflist]
    for font in candidates:
        if font in available:
            plt.rcParams['font.sans-serif'] = [font, 'DejaVu Sans']
            plt.rcParams['axes.unicode_minus'] = False
            return font
    plt.rcParams['axes.unicode_minus'] = False
    return None


def apply_base_style(theme):
    """应用通用基础样式。"""
    plt.rcParams.update({
        'figure.facecolor': theme['bg'],
        'axes.facecolor': theme['bg'],
        'axes.edgecolor': theme['grid'],
        'axes.grid': False,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.spines.left': True,
        'axes.spines.bottom': True,
        'font.size': 12,
        'axes.titlesize': 18,
        'axes.titleweight': 'bold',
        'axes.labelsize': 12,
        'xtick.labelsize': 11,
        'ytick.labelsize': 11,
        'text.color': theme['text'],
        'axes.labelcolor': theme['text'],
        'xtick.color': theme['subtitle'],
        'ytick.color': theme['subtitle'],
        'figure.dpi': 150,
    })
    if theme['bg'] != 'white':
        plt.rcParams['axes.spines.left'] = False
        plt.rcParams['axes.spines.bottom'] = False


def add_grid(ax, theme, axis='y'):
    """添加柔和的参考线。"""
    ax.grid(axis=axis, color=theme['grid'], linewidth=0.8, alpha=0.6)
    ax.set_axisbelow(True)


def style_title(ax, title, theme, pad=20):
    """统一的标题样式。"""
    ax.set_title(title, fontsize=17, fontweight='bold', color=theme['text'],
                 pad=pad, loc='left')


def add_legend(ax, theme, loc='auto', **kwargs):
    """统一的图例样式，默认放在底部不遮挡数据。"""
    if loc == 'auto':
        legend = ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12),
                           ncol=10, frameon=False, fontsize=11,
                           labelcolor=theme['subtitle'], **kwargs)
    else:
        legend = ax.legend(loc=loc, frameon=True, fancybox=True, shadow=False,
                           framealpha=0.9, edgecolor=theme['grid'], fontsize=11, **kwargs)
        legend.get_frame().set_linewidth(0.8)
    return legend


# ============================================================
# 图表生成函数
# ============================================================

def bar_chart(config, theme, output):
    """柱状图"""
    fig, ax = plt.subplots(figsize=config.get('figsize', [8, 5]))
    labels = config['labels']
    values = config['values']
    palette = theme['palette']
    colors = [palette[i % len(palette)] for i in range(len(labels))]

    x = np.arange(len(labels))
    bars = ax.bar(x, values, color=colors, width=0.55, edgecolor='white', linewidth=1.5,
                  zorder=3)

    # 数值标注
    if config.get('show_values', True):
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(values) * 0.025,
                    f'{val:g}', ha='center', va='bottom', fontsize=11, fontweight='bold',
                    color=theme['text'])

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    add_grid(ax, theme)
    style_title(ax, config.get('title', ''), theme)
    ax.set_xlabel(config.get('xlabel', ''), labelpad=10)
    ax.set_ylabel(config.get('ylabel', ''), labelpad=10)
    ax.spines['left'].set_color(theme['grid'])
    ax.spines['bottom'].set_color(theme['grid'])
    plt.tight_layout(pad=1.5)
    fig.savefig(output, dpi=config.get('dpi', 150), bbox_inches='tight',
                facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close(fig)


def grouped_bar_chart(config, theme, output):
    """分组柱状图"""
    fig, ax = plt.subplots(figsize=config.get('figsize', [8, 5]))
    labels = config['labels']
    groups = config['groups']
    palette = theme['palette']

    x = np.arange(len(labels))
    n = len(groups)
    width = 0.65 / n

    for i, group in enumerate(groups):
        offset = (i - n / 2 + 0.5) * width
        color = palette[i % len(palette)]
        bars = ax.bar(x + offset, group['values'], width, label=group['name'],
                      color=color, edgecolor='white', linewidth=1.2, zorder=3)
        if config.get('show_values', True):
            for bar, val in zip(bars, group['values']):
                ax.text(bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + max(group['values']) * 0.025,
                        f'{val:g}', ha='center', va='bottom', fontsize=9.5,
                        fontweight='bold', color=theme['text'])

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    add_grid(ax, theme)
    style_title(ax, config.get('title', ''), theme)
    ax.set_xlabel(config.get('xlabel', ''), labelpad=10)
    ax.set_ylabel(config.get('ylabel', ''), labelpad=10)
    ax.spines['left'].set_color(theme['grid'])
    ax.spines['bottom'].set_color(theme['grid'])

    add_legend(ax, theme)
    plt.tight_layout(pad=1.5)
    fig.savefig(output, dpi=config.get('dpi', 150), bbox_inches='tight',
                facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close(fig)


def line_chart(config, theme, output):
    """折线图"""
    fig, ax = plt.subplots(figsize=config.get('figsize', [8, 5]))
    x = config['x']
    palette = theme['palette']

    for i, series in enumerate(config['series']):
        color = palette[i % len(palette)]
        ax.plot(x, series['values'], color=color, label=series['name'],
                marker='o', markersize=7, markerfacecolor='white',
                markeredgecolor=color, markeredgewidth=2.5,
                linewidth=2.5, zorder=3)

    add_grid(ax, theme)
    style_title(ax, config.get('title', ''), theme)
    ax.set_xlabel(config.get('xlabel', ''), labelpad=10)
    ax.set_ylabel(config.get('ylabel', ''), labelpad=10)
    ax.spines['left'].set_color(theme['grid'])
    ax.spines['bottom'].set_color(theme['grid'])

    add_legend(ax, theme)
    plt.tight_layout(pad=1.5)
    fig.savefig(output, dpi=config.get('dpi', 150), bbox_inches='tight',
                facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close(fig)


def pie_chart(config, theme, output):
    """饼图 / 环形图"""
    fig, ax = plt.subplots(figsize=config.get('figsize', [7, 7]))
    labels = config['labels']
    values = config['values']
    palette = theme['palette']
    colors = [palette[i % len(palette)] for i in range(len(labels))]

    wedgeprops = {'edgecolor': 'white', 'linewidth': 2.5}
    if config.get('donut', False):
        wedgeprops['width'] = 0.4

    wedges, texts, autotexts = ax.pie(
        values, labels=labels, colors=colors, autopct='%1.1f%%',
        startangle=90, wedgeprops=wedgeprops,
        textprops={'fontsize': 12, 'color': theme['text']},
        pctdistance=0.75)

    for t in autotexts:
        t.set_fontweight('bold')
        t.set_fontsize(11)

    style_title(ax, config.get('title', ''), theme, pad=25)
    plt.tight_layout(pad=1.5)
    fig.savefig(output, dpi=config.get('dpi', 150), bbox_inches='tight',
                facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close(fig)


def radar_chart(config, theme, output):
    """雷达图"""
    fig, ax = plt.subplots(figsize=config.get('figsize', [8, 8]),
                           subplot_kw=dict(polar=True))
    categories = config['categories']
    palette = theme['palette']
    N = len(categories)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]

    # 背景样式
    ax.set_facecolor(theme['bg'])
    ax.spines['polar'].set_color(theme['grid'])
    ax.spines['polar'].set_linewidth(0.5)
    ax.grid(color=theme['grid'], linewidth=0.8, alpha=0.5)
    ax.tick_params(colors=theme['subtitle'])

    for i, series in enumerate(config['series']):
        color = palette[i % len(palette)]
        values = series['values'] + series['values'][:1]
        ax.plot(angles, values, color=color, linewidth=2.8, label=series['name'], zorder=3)
        ax.fill(angles, values, color=color, alpha=0.12)
        # 数据点
        ax.scatter(angles[:-1], series['values'], color=color, s=50, zorder=4,
                   edgecolors='white', linewidth=1.5)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=12, color=theme['text'])

    # 标题和图例
    ax.set_title(config.get('title', ''), fontsize=17, fontweight='bold',
                 color=theme['text'], pad=30, loc='center')
    add_legend(ax, theme, loc='upper right', bbox_to_anchor=(1.2, 1.05))

    plt.tight_layout(pad=2.0)
    fig.savefig(output, dpi=config.get('dpi', 150), bbox_inches='tight',
                facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close(fig)


def heatmap_chart(config, theme, output):
    """热力图"""
    fig, ax = plt.subplots(figsize=config.get('figsize', [8, 4.5]))
    data = np.array(config['data'])
    row_labels = config.get('row_labels', [str(i) for i in range(data.shape[0])])
    col_labels = config.get('col_labels', [str(i) for i in range(data.shape[1])])

    # 使用主题渐变色
    cmap_colors = theme.get('heatmap_cmap', ['#EFF6FF', '#2563EB', '#1E3A5F'])
    custom_cmap = LinearSegmentedColormap.from_list('custom', cmap_colors, N=256)

    im = ax.imshow(data, cmap=custom_cmap, aspect='auto')

    ax.set_xticks(np.arange(len(col_labels)))
    ax.set_yticks(np.arange(len(row_labels)))
    ax.set_xticklabels(col_labels, fontsize=12)
    ax.set_yticklabels(row_labels, fontsize=13, fontweight='bold')
    plt.setp(ax.get_xticklabels(), rotation=30, ha='right')

    # 去除边框
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(top=False, bottom=False, left=False, right=False)

    # 数值标注
    if config.get('show_values', True):
        vmax = data.max()
        vmin = data.min()
        mid = (vmax + vmin) / 2
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                text_color = 'white' if data[i, j] > mid else theme['text']
                ax.text(j, i, f'{data[i, j]:g}', ha='center', va='center',
                        color=text_color, fontsize=13, fontweight='bold')

    # 色条
    cbar = fig.colorbar(im, ax=ax, shrink=0.8, aspect=30, pad=0.04)
    cbar.outline.set_visible(False)
    cbar.ax.tick_params(labelsize=10, colors=theme['subtitle'])

    style_title(ax, config.get('title', ''), theme, pad=15)
    plt.tight_layout(pad=1.5)
    fig.savefig(output, dpi=config.get('dpi', 150), bbox_inches='tight',
                facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close(fig)


def scatter_chart(config, theme, output):
    """散点图"""
    fig, ax = plt.subplots(figsize=config.get('figsize', [8, 5]))
    palette = theme['palette']

    for i, series in enumerate(config['series']):
        color = palette[i % len(palette)]
        sizes = series.get('sizes', [80] * len(series['x']))
        ax.scatter(series['x'], series['y'], c=color, s=sizes, alpha=0.75,
                   label=series['name'], edgecolors='white', linewidth=1.5, zorder=3)
        if config.get('show_labels', False) and 'labels' in series:
            # 交替上下偏移避免文字重叠
            offsets = [(10, 10), (10, -15), (-10, 12), (-10, -15)]
            for idx, (x, y, label) in enumerate(zip(series['x'], series['y'], series['labels'])):
                ox, oy = offsets[idx % len(offsets)]
                ax.annotate(label, (x, y), textcoords='offset points', xytext=(ox, oy),
                            fontsize=10, fontweight='bold', color=theme['text'],
                            arrowprops=dict(arrowstyle='-', color=theme['grid'], lw=0.8))

    add_grid(ax, theme, axis='both')
    style_title(ax, config.get('title', ''), theme)
    ax.set_xlabel(config.get('xlabel', ''), labelpad=10)
    ax.set_ylabel(config.get('ylabel', ''), labelpad=10)
    ax.spines['left'].set_color(theme['grid'])
    ax.spines['bottom'].set_color(theme['grid'])

    add_legend(ax, theme)
    plt.tight_layout(pad=1.5)
    fig.savefig(output, dpi=config.get('dpi', 150), bbox_inches='tight',
                facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close(fig)


def stacked_bar_chart(config, theme, output):
    """堆叠柱状图"""
    fig, ax = plt.subplots(figsize=config.get('figsize', [8, 5]))
    labels = config['labels']
    groups = config['groups']
    palette = theme['palette']

    bottom = np.zeros(len(labels))
    x = np.arange(len(labels))
    for i, group in enumerate(groups):
        color = palette[i % len(palette)]
        ax.bar(x, group['values'], bottom=bottom, label=group['name'],
               color=color, edgecolor='white', linewidth=1.2, width=0.55, zorder=3)
        bottom += np.array(group['values'])

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    add_grid(ax, theme)
    style_title(ax, config.get('title', ''), theme)
    ax.set_xlabel(config.get('xlabel', ''), labelpad=10)
    ax.set_ylabel(config.get('ylabel', ''), labelpad=10)
    ax.spines['left'].set_color(theme['grid'])
    ax.spines['bottom'].set_color(theme['grid'])

    add_legend(ax, theme)
    plt.tight_layout(pad=1.5)
    fig.savefig(output, dpi=config.get('dpi', 150), bbox_inches='tight',
                facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close(fig)


# ============================================================
# 主入口
# ============================================================

CHART_TYPES = {
    'bar': bar_chart,
    'grouped_bar': grouped_bar_chart,
    'line': line_chart,
    'pie': pie_chart,
    'radar': radar_chart,
    'heatmap': heatmap_chart,
    'scatter': scatter_chart,
    'stacked_bar': stacked_bar_chart,
}


def main():
    parser = argparse.ArgumentParser(description='生成统计图表')
    parser.add_argument('--config', required=True, help='图表配置 JSON 文件路径')
    parser.add_argument('--output', required=True, help='输出 PNG 文件路径')
    parser.add_argument('--theme', default='tech-blue', help='主题名称')
    args = parser.parse_args()

    with open(args.config, 'r', encoding='utf-8') as f:
        config = json.load(f)

    setup_chinese_font()
    theme = THEMES.get(args.theme, THEMES['tech-blue'])
    apply_base_style(theme)

    chart_type = config.get('type', 'bar')
    if chart_type not in CHART_TYPES:
        print(f'不支持的图表类型: {chart_type}，支持的类型: {list(CHART_TYPES.keys())}')
        sys.exit(1)

    CHART_TYPES[chart_type](config, theme, args.output)
    print(f'图表已生成: {args.output}')


if __name__ == '__main__':
    main()
