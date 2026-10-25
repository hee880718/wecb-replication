"""Appendix Fig A2 — permutation distribution of the compliance-cycle statistic (21 assignments)."""
import housestyle as H, matplotlib.pyplot as plt, pandas as pd, numpy as np, os
from itertools import combinations
H.setup(); D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
jp = pd.read_csv(f'{D}/japan_china_share.csv').rename(columns={'fy': 'year'}); us = pd.read_csv(f'{D}/us_china_share.csv'); us['year'] = pd.to_datetime(us.report_date).dt.year; us = us[us.form == '10-K'][['firm', 'year', 'share']]
p = pd.concat([jp, us]); ctrl = {'AMAT': 1, 'KLAC': 1, 'LRCX': 1, 'TEL': 1, 'SCREEN': 1, 'DISCO': 0, 'ULVAC': 0}; p = p[p.firm.isin(ctrl) & (p.year >= 2018)]; W = p.pivot_table(index='firm', columns='year', values='share'); firms = list(W.index)
def vol(df, tr): v = {f: df.loc[f, [c for c in df.columns if c >= 2022]].dropna().diff().std() for f in df.index}; return 100 * (np.mean([v[f] for f in df.index if tr[f]]) - np.mean([v[f] for f in df.index if not tr[f]]))
est = vol(W, ctrl); perm = sorted(vol(W, {f: int(f in c) for f in firms}) for c in combinations(firms, 5))
fig, ax = plt.subplots(figsize=(8.27, 3.0)); fig.subplots_adjust(top=0.72, bottom=0.24, left=0.07, right=0.98); H.ax_clean(ax, grid='x')
ax.scatter(perm, np.zeros(len(perm)), s=28, color=H.C['grey'], zorder=2); ax.scatter([est], [0], s=70, color=H.C['red'], zorder=3); ax.text(est - 0.2, 0.25, f'actual assignment  {est:+.1f} pp\nrank 1 of 21 (p = 0.048)', ha='right', fontsize=7, color=H.C['red'])
ax.set_yticks([]); ax.set_ylim(-0.4, 0.8); ax.set_xlabel('Post-2022 volatility of China share, treated minus untreated (pp)', fontsize=7.5); ax.tick_params(axis='x', labelsize=7); ax.spines['left'].set_visible(False)
H.headline(fig, 'The compliance cycle is the largest of all 21 possible assignments', 'Each dot is the volatility statistic for one choice of five "controlled" vendors among seven (AMAT, KLA, Lam, Tokyo Electron, SCREEN, DISCO, ULVAC). The true assignment sits at the extreme.')
H.source(fig, 'Sources: SEC 10-K and EDINET annual China revenue shares, 2018–2026 (AMAT through FY2025). Statistic: standard deviation of annual changes from 2022 onward, treated mean minus untreated mean. Firm-level, pp: TEL 12.9, Lam 11.3, SCREEN 11.2, KLA 10.7, AMAT 8.6; DISCO 4.6, ULVAC 2.9. Next-largest assignment 4.4.')
H.save(fig, 'figA2_permutation', pd.DataFrame({'statistic': perm}))
