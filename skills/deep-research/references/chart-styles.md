# 图表风格参考

根据报告的调研类型选择对应的视觉风格主题。同一份报告内所有图表使用同一主题。

---

## 主题映射表

| 调研类型 | 风格主题 | 配色基调 | 结构图风格 | 统计图风格 |
|---------|---------|---------|-----------|-----------|
| 技术选型 / 架构 | `tech-blue` | 商务蓝灰 | 圆角现代 | 极简白底 |
| 行业 / 市场分析 | `biz-warm` | 暖色商务（蓝+橙） | 圆角现代 | seaborn 风格 |
| 学术 / 理论研究 | `academic` | 黑白灰 | 直角工程 | ggplot 风格 |
| 性能 / benchmark | `dark-tech` | 科技深色 | 直角工程 | 深色极简 |
| 竞品 / 产品分析 | `product` | 多彩克制 | 圆角现代 | 极简白底 |
| 可行性探索 | `tech-blue` | 商务蓝灰 | 圆角现代 | 极简白底 |

---

## 通用设置

所有主题共享以下基础设置：

```python
import matplotlib
matplotlib.use('Agg')  # 非交互模式
import matplotlib.pyplot as plt
from matplotlib import font_manager
import platform

# 中文字体设置
def setup_chinese_font():
    """自动检测并设置中文字体"""
    system = platform.system()
    if system == 'Darwin':  # macOS
        font_candidates = ['PingFang SC', 'STHeiti', 'Heiti TC', 'Arial Unicode MS']
    elif system == 'Linux':
        font_candidates = ['Noto Sans CJK SC', 'WenQuanYi Micro Hei', 'Droid Sans Fallback']
    else:  # Windows
        font_candidates = ['Microsoft YaHei', 'SimHei', 'FangSong']

    available_fonts = [f.name for f in font_manager.fontManager.ttflist]
    for font in font_candidates:
        if font in available_fonts:
            plt.rcParams['font.sans-serif'] = [font, 'DejaVu Sans']
            plt.rcParams['axes.unicode_minus'] = False
            return font
    # 回退：使用系统默认
    plt.rcParams['axes.unicode_minus'] = False
    return None

# 通用图表参数
CHART_DPI = 150
FIGURE_SIZE_NORMAL = (10, 6)      # 普通图表
FIGURE_SIZE_WIDE = (12, 6)        # 宽图（对比类）
FIGURE_SIZE_SQUARE = (8, 8)       # 方形（雷达图、饼图）
FIGURE_SIZE_TALL = (10, 8)        # 高图（热力图）
```

---

## 主题：tech-blue（商务蓝灰）

适用于技术选型、架构分析、可行性探索。专业、冷静、可信赖。

### matplotlib 配置

```python
TECH_BLUE = {
    'colors': {
        'primary': '#2563EB',
        'secondary': '#60A5FA',
        'accent': '#F59E0B',
        'success': '#10B981',
        'danger': '#EF4444',
        'neutral': '#6B7280',
        'light': '#F3F4F6',
        'palette': ['#2563EB', '#60A5FA', '#F59E0B', '#10B981', '#8B5CF6', '#EF4444', '#EC4899', '#6B7280'],
    },
    'style': {
        'figure.facecolor': 'white',
        'axes.facecolor': 'white',
        'axes.edgecolor': '#E5E7EB',
        'axes.grid': True,
        'grid.color': '#F3F4F6',
        'grid.alpha': 0.8,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'font.size': 11,
        'axes.titlesize': 14,
        'axes.titleweight': 'bold',
        'axes.labelsize': 11,
    }
}
```

### graphviz 配置

```python
TECH_BLUE_GRAPHVIZ = {
    'graph_attrs': {
        'bgcolor': 'white',
        'fontname': 'PingFang SC',
        'fontsize': '12',
        'rankdir': 'TB',        # 默认从上到下
        'splines': 'ortho',     # 直角连线
        'nodesep': '0.8',
        'ranksep': '1.0',
        'pad': '0.5',
    },
    'node_attrs': {
        'shape': 'box',
        'style': 'rounded,filled',
        'fillcolor': '#EFF6FF',
        'color': '#2563EB',
        'fontname': 'PingFang SC',
        'fontsize': '11',
        'fontcolor': '#1E3A5F',
        'penwidth': '1.5',
        'margin': '0.3,0.15',
    },
    'edge_attrs': {
        'color': '#6B7280',
        'fontname': 'PingFang SC',
        'fontsize': '10',
        'fontcolor': '#6B7280',
        'arrowsize': '0.8',
        'penwidth': '1.2',
    },
    # 特殊节点类型
    'node_types': {
        'highlight': {'fillcolor': '#2563EB', 'fontcolor': 'white'},
        'warning': {'fillcolor': '#FEF3C7', 'color': '#F59E0B'},
        'success': {'fillcolor': '#D1FAE5', 'color': '#10B981'},
        'danger': {'fillcolor': '#FEE2E2', 'color': '#EF4444'},
        'group': {'style': 'rounded,dashed', 'fillcolor': '#F9FAFB', 'color': '#D1D5DB'},
    }
}
```

---

## 主题：biz-warm（暖色商务）

适用于行业分析、市场调研。温暖、亲和、易于理解。

### matplotlib 配置

```python
BIZ_WARM = {
    'colors': {
        'primary': '#1E40AF',
        'secondary': '#F97316',
        'accent': '#0EA5E9',
        'success': '#22C55E',
        'danger': '#DC2626',
        'neutral': '#78716C',
        'light': '#FFF7ED',
        'palette': ['#1E40AF', '#F97316', '#0EA5E9', '#22C55E', '#A855F7', '#DC2626', '#EC4899', '#78716C'],
    },
    'style': {
        'figure.facecolor': 'white',
        'axes.facecolor': '#FEFCE8' + '10',  # 极淡暖底
        'axes.edgecolor': '#E5E7EB',
        'axes.grid': True,
        'grid.color': '#F5F5F4',
        'grid.alpha': 0.6,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'font.size': 11,
        'axes.titlesize': 14,
        'axes.titleweight': 'bold',
        'axes.labelsize': 11,
    }
}
```

### graphviz 配置

```python
BIZ_WARM_GRAPHVIZ = {
    'graph_attrs': {
        'bgcolor': 'white',
        'fontname': 'PingFang SC',
        'fontsize': '12',
        'rankdir': 'TB',
        'splines': 'curved',    # 曲线连线，更柔和
        'nodesep': '0.8',
        'ranksep': '1.0',
    },
    'node_attrs': {
        'shape': 'box',
        'style': 'rounded,filled',
        'fillcolor': '#FFF7ED',
        'color': '#F97316',
        'fontname': 'PingFang SC',
        'fontsize': '11',
        'fontcolor': '#44403C',
        'penwidth': '1.5',
        'margin': '0.3,0.15',
    },
    'edge_attrs': {
        'color': '#78716C',
        'fontname': 'PingFang SC',
        'fontsize': '10',
        'arrowsize': '0.8',
        'penwidth': '1.2',
    },
    'node_types': {
        'highlight': {'fillcolor': '#1E40AF', 'fontcolor': 'white'},
        'secondary': {'fillcolor': '#FFEDD5', 'color': '#EA580C'},
        'success': {'fillcolor': '#DCFCE7', 'color': '#22C55E'},
        'group': {'style': 'rounded,dashed', 'fillcolor': '#FFFBEB', 'color': '#D6D3D1'},
    }
}
```

---

## 主题：academic（学术黑白）

适用于学术研究、理论分析。严谨、简洁、打印友好。

### matplotlib 配置

```python
ACADEMIC = {
    'colors': {
        'primary': '#1F2937',
        'secondary': '#6B7280',
        'accent': '#374151',
        'success': '#4B5563',
        'danger': '#1F2937',
        'neutral': '#9CA3AF',
        'light': '#F9FAFB',
        'palette': ['#1F2937', '#6B7280', '#9CA3AF', '#D1D5DB', '#374151', '#4B5563', '#E5E7EB', '#111827'],
    },
    'style': {
        'figure.facecolor': 'white',
        'axes.facecolor': '#F9FAFB',
        'axes.edgecolor': '#D1D5DB',
        'axes.grid': True,
        'grid.color': '#E5E7EB',
        'grid.alpha': 1.0,
        'grid.linestyle': '--',
        'axes.spines.top': False,
        'axes.spines.right': False,
        'font.size': 11,
        'axes.titlesize': 13,
        'axes.titleweight': 'bold',
        'axes.labelsize': 11,
    }
}
```

### graphviz 配置

```python
ACADEMIC_GRAPHVIZ = {
    'graph_attrs': {
        'bgcolor': 'white',
        'fontname': 'PingFang SC',
        'fontsize': '11',
        'rankdir': 'TB',
        'splines': 'ortho',
        'nodesep': '0.6',
        'ranksep': '0.8',
    },
    'node_attrs': {
        'shape': 'box',
        'style': 'filled',         # 无圆角，工程风
        'fillcolor': 'white',
        'color': '#374151',
        'fontname': 'PingFang SC',
        'fontsize': '10',
        'fontcolor': '#1F2937',
        'penwidth': '1.0',
        'margin': '0.25,0.12',
    },
    'edge_attrs': {
        'color': '#6B7280',
        'fontname': 'PingFang SC',
        'fontsize': '9',
        'arrowsize': '0.7',
        'penwidth': '1.0',
    },
    'node_types': {
        'highlight': {'fillcolor': '#E5E7EB', 'penwidth': '2.0'},
        'group': {'style': 'dashed', 'fillcolor': '#F9FAFB', 'color': '#9CA3AF'},
    }
}
```

---

## 主题：dark-tech（科技深色）

适用于性能评测、benchmark 对比。酷炫、数据密集、技术感。

### matplotlib 配置

```python
DARK_TECH = {
    'colors': {
        'primary': '#22D3EE',
        'secondary': '#A78BFA',
        'accent': '#34D399',
        'success': '#34D399',
        'danger': '#F87171',
        'neutral': '#9CA3AF',
        'light': '#1F2937',
        'palette': ['#22D3EE', '#A78BFA', '#34D399', '#FBBF24', '#F87171', '#FB923C', '#E879F9', '#9CA3AF'],
    },
    'style': {
        'figure.facecolor': '#0F172A',
        'axes.facecolor': '#1E293B',
        'axes.edgecolor': '#334155',
        'axes.grid': True,
        'grid.color': '#334155',
        'grid.alpha': 0.5,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'text.color': '#E2E8F0',
        'axes.labelcolor': '#CBD5E1',
        'xtick.color': '#94A3B8',
        'ytick.color': '#94A3B8',
        'font.size': 11,
        'axes.titlesize': 14,
        'axes.titleweight': 'bold',
        'axes.labelsize': 11,
    }
}
```

### graphviz 配置

```python
DARK_TECH_GRAPHVIZ = {
    'graph_attrs': {
        'bgcolor': '#0F172A',
        'fontname': 'PingFang SC',
        'fontsize': '12',
        'fontcolor': '#E2E8F0',
        'rankdir': 'TB',
        'splines': 'ortho',
        'nodesep': '0.8',
        'ranksep': '1.0',
    },
    'node_attrs': {
        'shape': 'box',
        'style': 'filled',
        'fillcolor': '#1E293B',
        'color': '#22D3EE',
        'fontname': 'PingFang SC',
        'fontsize': '11',
        'fontcolor': '#E2E8F0',
        'penwidth': '1.5',
        'margin': '0.3,0.15',
    },
    'edge_attrs': {
        'color': '#475569',
        'fontname': 'PingFang SC',
        'fontsize': '10',
        'fontcolor': '#94A3B8',
        'arrowsize': '0.8',
        'penwidth': '1.2',
    },
    'node_types': {
        'highlight': {'color': '#34D399', 'fillcolor': '#064E3B'},
        'warning': {'color': '#FBBF24', 'fillcolor': '#422006'},
        'danger': {'color': '#F87171', 'fillcolor': '#450A0A'},
        'group': {'style': 'dashed', 'fillcolor': '#0F172A', 'color': '#334155'},
    }
}
```

---

## 主题：product（多彩克制）

适用于竞品分析、产品对比。多彩但不花哨，每个竞品一个专属色。

### matplotlib 配置

```python
PRODUCT = {
    'colors': {
        'primary': '#6366F1',
        'secondary': '#EC4899',
        'accent': '#14B8A6',
        'success': '#22C55E',
        'danger': '#EF4444',
        'neutral': '#6B7280',
        'light': '#F9FAFB',
        # 竞品专属色，最多支持 8 个对比对象
        'palette': ['#6366F1', '#EC4899', '#14B8A6', '#F59E0B', '#3B82F6', '#EF4444', '#8B5CF6', '#06B6D4'],
    },
    'style': {
        'figure.facecolor': 'white',
        'axes.facecolor': 'white',
        'axes.edgecolor': '#E5E7EB',
        'axes.grid': True,
        'grid.color': '#F3F4F6',
        'grid.alpha': 0.8,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'font.size': 11,
        'axes.titlesize': 14,
        'axes.titleweight': 'bold',
        'axes.labelsize': 11,
    }
}
```

### graphviz 配置

```python
PRODUCT_GRAPHVIZ = {
    'graph_attrs': {
        'bgcolor': 'white',
        'fontname': 'PingFang SC',
        'fontsize': '12',
        'rankdir': 'LR',        # 左到右，适合对比布局
        'splines': 'curved',
        'nodesep': '0.8',
        'ranksep': '1.2',
    },
    'node_attrs': {
        'shape': 'box',
        'style': 'rounded,filled',
        'fillcolor': '#F5F3FF',
        'color': '#6366F1',
        'fontname': 'PingFang SC',
        'fontsize': '11',
        'fontcolor': '#312E81',
        'penwidth': '1.5',
        'margin': '0.3,0.15',
    },
    'edge_attrs': {
        'color': '#9CA3AF',
        'fontname': 'PingFang SC',
        'fontsize': '10',
        'arrowsize': '0.8',
        'penwidth': '1.0',
    },
    'node_types': {
        'product_a': {'fillcolor': '#EEF2FF', 'color': '#6366F1'},
        'product_b': {'fillcolor': '#FCE7F3', 'color': '#EC4899'},
        'product_c': {'fillcolor': '#CCFBF1', 'color': '#14B8A6'},
        'winner': {'fillcolor': '#6366F1', 'fontcolor': 'white', 'penwidth': '2.5'},
        'group': {'style': 'rounded,dashed', 'fillcolor': '#F9FAFB', 'color': '#D1D5DB'},
    }
}
```

---

## 使用方式

生成图表时，根据当前报告的调研类型找到对应主题，然后：

1. **matplotlib 图表**：在脚本开头调用 `setup_chinese_font()`，然后用 `plt.rcParams.update(theme['style'])` 应用样式，用 `theme['colors']['palette']` 作为颜色序列
2. **graphviz 图表**：创建 Digraph/Graph 时传入 `graph_attr`、`node_attr`、`edge_attr`，特殊节点用 `node_types` 覆盖默认样式

始终确保同一份报告内所有图表使用同一主题，保持视觉一致性。
