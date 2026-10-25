"""Appendix Fig A5 — quarterly gap paths vs foreign-peer synthetic control (ridge-augmented SC), with placebo band."""
import housestyle as H, matplotlib.pyplot as plt, pandas as pd, numpy as np, json, os
from scipy.optimize import minimize
H.setup(); D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
P = pd.read_csv(f'{D}/quarterly_panel_local_v5.csv', index_col=0); cur = json.load(open(f'{D}/quarterly_currency_v2.json'))
FX = {'CNY': {2016: 6.64, 2017: 6.75, 2018: 6.62, 2019: 6.91, 2020: 6.90, 2021: 6.45, 2022: 6.73, 2023: 7.08, 2024: 7.19, 2025: 7.18}, 'KRW': {2016: 1160, 2017: 1130, 2018: 1100, 2019: 1166, 2020: 1180, 2021: 1144, 2022: 1292, 2023: 1306, 2024: 1364, 2025: 1420}}
U = P.copy()
for f in U.index:
    cc = cur.get(f, 'USD')
    if cc in FX: U.loc[f] = [v / FX[cc][int(p[:4])] if pd.notna(v) else np.nan for p, v in zip(U.columns, U.loc[f])]
per = [p for p in U.columns if '2017Q1' <= p <= '2025Q4']; PRE = [p for p in per if p <= '2022Q3']; POST = [p for p in per if p >= '2022Q4']
L = np.log(U.where(U > 0))[per]; S = L.copy()
for u in L.index:
    for q in (1, 2, 3, 4):
        idx = [p for p in per if int(p[-1]) == q]; S.loc[u, idx] = L.loc[u, idx] - L.loc[u, [p for p in PRE if int(p[-1]) == q]].mean()
S.loc['TR:EQUIP3'] = S.loc[['TR:NAURA', 'TR:AMEC', 'TR:ACMR']].mean(axis=0, skipna=True).values; ctrl = [i for i in S.index if not i.startswith('TR:') and S.loc[i].notna().all()]
def simplex(X, y):
    n = X.shape[1]; return minimize(lambda w: np.sum((X @ w - y) ** 2), np.ones(n) / n, bounds=[(0, 1)] * n, constraints={'type': 'eq', 'fun': lambda w: w.sum() - 1}, method='SLSQP').x
def gap_path(tr, cs):
    yt = S.loc[tr]; pre = [p for p in PRE if pd.notna(yt[p])]; post = [p for p in POST if pd.notna(yt[p])]; C = S.loc[cs, pre + post].dropna(); Cp, Cq = C[pre].values.T, C[post].values.T; yp, yq = yt[pre].values, yt[post].values
    w = simplex(Cp, yp); B = np.linalg.solve(Cp.T @ Cp + np.eye(Cp.shape[1]), Cp.T @ (yp - Cp @ w)); return pd.Series(yq - (Cq @ w + Cq @ B), index=post)
units = [('TR:EQUIP3', 'Three-firm aggregate'), ('TR:NAURA', 'NAURA'), ('TR:AMEC', 'AMEC'), ('TR:ACMR', 'ACM Research')]; plac = pd.DataFrame({j: gap_path(j, [c for c in ctrl if c != j]) for j in ctrl})
lo, hi = plac.quantile(0.05, axis=1), plac.quantile(0.95, axis=1); x = np.arange(len(POST)); lab = [p if p.endswith('Q1') else '' for p in POST]
fig, axes = plt.subplots(2, 2, figsize=(8.27, 5.4), sharex=True, sharey=True); fig.subplots_adjust(top=0.76, bottom=0.1, left=0.08, right=0.95, hspace=0.45, wspace=0.12); rows = []
for ax, (u, nm) in zip(axes.ravel(), units):
    H.ax_clean(ax); g = gap_path(u, ctrl); ax.fill_between(x, lo.values, hi.values, color='#E8EAED', lw=0); ax.axhline(0, color='#444', lw=0.7); ax.plot(x, g.values, color=H.C['red'], lw=1.9, marker='o', ms=2.6)
    ax.axvline(POST.index('2025Q1') - 0.5, color=H.C['pink'], lw=0.9); ax.set_title(nm, loc='left', fontsize=8.6, weight='bold', color=H.C['ink']); ax.set_xticks(x); ax.set_xticklabels([l[:4] if l else '' for l in lab], fontsize=7); ax.tick_params(axis='y', labelsize=7)
    ax.text(x[-1] + 0.2, g.values[-1], f'{g.values[-1]:+.2f}', fontsize=6.6, color=H.C['red'], va='center'); rows += [{'unit': nm, 'quarter': q, 'gap': v} for q, v in g.items()]
axes[0, 0].set_ylabel('Gap vs synthetic control, log points', fontsize=7); axes[1, 0].set_ylabel('Gap vs synthetic control, log points', fontsize=7); axes[0, 0].text(0.02, 0.95, 'band: 5th–95th percentile of 15 placebo paths\npink line: December 2024 designations', transform=axes[0, 0].transAxes, fontsize=6.2, color=H.C['sub'], va='top')
H.headline(fig, 'The gap over foreign peers kept widening, quarter by quarter', 'Revenue gap of each Chinese toolmaker over its ridge-augmented synthetic control of 15 foreign suppliers, 2022Q4–2025Q4, seasonally adjusted quarterly accounts in USD; grey band shows where placebo paths (each foreign donor treated in turn) lie.')
H.source(fig, 'Sources: SEC EDGAR, OpenDART, cninfo quarterly reports; panel quarterly_panel_local_v5. Pre-period 2017Q1–2022Q3 (AMEC 2019Q1–2022Q3); ridge penalty 1; seasonal adjustment by quarter-specific pre-period means; aggregate = mean of the three log series; band from placebo paths on the full pre-period.')
H.save(fig, 'figA5_feed_dynamics', pd.DataFrame(rows))
