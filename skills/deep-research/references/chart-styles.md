# 图表风格参考

根据报告的调研类型选择对应的视觉风格主题。同一份报告内所有图表使用同一主题。

---

## 主题映射表

| 调研类型 | 风格主题 | 配色基调 | 统计图风格 |
|---------|---------|---------|-----------|
| 技术选型 / 架构 | `tech-blue` | 商务蓝灰 | 极简白底 |
| 行业 / 市场分析 | `biz-warm` | 暖色商务（蓝+橙） | seaborn 风格 |
| 学术 / 理论研究 | `academic` | 黑白灰 | ggplot 风格 |
| 性能 / benchmark | `dark-tech` | 科技深色 | 深色极简 |
| 竞品 / 产品分析 | `product` | 多彩克制 | 极简白底 |
| 可行性探索 | `tech-blue` | 商务蓝灰 | 极简白底 |

> **结构图表**统一使用 Diagram skill 的设计规范（`~/.claude/skills/diagram/references/design-system.md`），不再按主题区分结构图风格。

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

---

## 使用方式

生成图表时，根据当前报告的调研类型找到对应主题，然后：

1. **统计图表（bridge.py）**：JSON 配置中无需指定主题，bridge.py 使用 Diagram skill 统一设计规范
2. **结构图表（capture.py）**：编写 HTML 时参考 Diagram skill 的 `references/design-system.md` 配色规范

> 结构图表（流程图、架构图等）统一使用 Diagram skill 的 HTML/SVG 模板 + capture.py 截图，不再使用 graphviz。

始终确保同一份报告内所有图表使用同一主题，保持视觉一致性。
