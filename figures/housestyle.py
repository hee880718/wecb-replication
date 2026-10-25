"""House style for all paper figures. One rule set; every figure script imports this.
Outputs: save(fig, name, data=None) -> name.png (300 dpi), name.pdf (vector), name.csv (data behind the figure)."""
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt; import pandas as pd, textwrap, os
C = {'red': '#A11C22', 'navy': '#1F3A5F', 'grey': '#9AA3AD', 'pink': '#E8B4A4', 'ink': '#333333', 'light': '#D9DEE3', 'title': '#6E0E18', 'sub': '#555555', 'src': '#666666'}
EVENTS = [('2018-04', 'ZTE denial'), ('2019-05', 'Huawei listed'), ('2020-09', 'Huawei chips'), ('2022-10', 'US rule'), ('2023-07', 'JP rule'), ('2023-09', 'NL rule'), ('2024-12', 'US rule II')]
FULL, HALF = (8.27, 4.4), (4.0, 3.2)
def setup():
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8, 'axes.spines.top': False, 'axes.spines.right': False, 'axes.edgecolor': '#444', 'axes.linewidth': 0.6, 'xtick.color': '#444', 'ytick.color': '#444', 'figure.facecolor': 'white', 'savefig.dpi': 300, 'pdf.fonttype': 42})
def ax_clean(ax, grid='y'):
    ax.grid(axis=grid, color=C['light'], lw=0.6); ax.set_axisbelow(True); ax.tick_params(length=0)
def event_lines(ax, keys, ypos=0.97, color=None, label=True):
    for k, lab in EVENTS:
        if k in keys:
            x = int(k[:4]) + (int(k[5:7]) - 1) / 12; ax.axvline(x, color=color or C['pink'], lw=1)
            if label: ax.text(x + 0.05, ypos, lab, transform=ax.get_xaxis_transform(), fontsize=6.2, color=C['sub'], rotation=90, va='top')
def band(ax, start, end, label=None, color=None, alpha=0.18):
    """Shaded period (announcement-to-effect window, downturn, etc.)"""
    ax.axvspan(start, end, color=color or C['pink'], alpha=alpha, lw=0)
    if label: ax.text((start + end) / 2, 0.98, label, transform=ax.get_xaxis_transform(), fontsize=6.2, color=C['sub'], ha='center', va='top')
def note(ax, xy, text, xytext, color=None):
    """Narrative annotation with a thin arrow"""
    ax.annotate(text, xy=xy, xytext=xytext, textcoords='data', fontsize=6.6, color=color or C['ink'], ha='left', va='center', arrowprops=dict(arrowstyle='-', color=C['sub'], lw=0.6, shrinkA=0, shrinkB=2))
def bignum(ax, text, sub=None):
    """Large key-number callout at the top-right of an axes"""
    ax.text(1.0, 1.02, text, transform=ax.transAxes, fontsize=13, weight='bold', color=C['red'], ha='right', va='bottom')
    if sub: ax.text(1.0, 1.15, sub, transform=ax.transAxes, fontsize=6.4, color=C['sub'], ha='right', va='bottom')
def headline(fig, title, sub, top=0.985):
    fig.text(0.01, top, title, fontsize=12.5, color=C['title'], weight='bold', va='top'); fig.text(0.01, top - 0.058, textwrap.fill(sub, 125), fontsize=8.6, color=C['sub'], va='top')
def source(fig, text): fig.text(0.01, 0.01, textwrap.fill(text, 160), fontsize=6.3, color=C['src'], va='bottom', linespacing=1.3)
def save(fig, name, data=None, outdir=os.path.dirname(os.path.abspath(__file__))):
    for ext in ('png', 'pdf'): fig.savefig(os.path.join(outdir, f'{name}.{ext}'))
    if data is not None: pd.DataFrame(data).to_csv(os.path.join(outdir, f'{name}.csv'), index=False)
    plt.close(fig); print('saved', name)
