"""§5.3 / Appendix D: compliance-signature permutation tests on annual China revenue shares of 7 vendors (registry W3a–c)."""
import pandas as pd, numpy as np
from itertools import combinations
jp = pd.read_csv('../../figures/data/japan_china_share.csv').rename(columns={'fy': 'year'}); us = pd.read_csv('../../figures/data/us_china_share.csv'); us['year'] = pd.to_datetime(us.report_date).dt.year; us = us[us.form == '10-K'][['firm', 'year', 'share']]
p = pd.concat([jp, us]); ctrl = {'AMAT': 1, 'KLAC': 1, 'LRCX': 1, 'TEL': 1, 'SCREEN': 1, 'DISCO': 0, 'ULVAC': 0}; p = p[p.firm.isin(ctrl) & (p.year >= 2018)]; W = p.pivot_table(index='firm', columns='year', values='share'); firms = list(W.index)
def lvl(df, tr): g = {f: (df.loc[f, [c for c in df.columns if 2023 <= c <= 2025]].mean() - df.loc[f, [c for c in df.columns if 2019 <= c <= 2021]].mean()) for f in df.index}; return 100*(np.mean([g[f] for f in df.index if tr[f]]) - np.mean([g[f] for f in df.index if not tr[f]]))
def vol(df, tr): v = {f: df.loc[f, [c for c in df.columns if c >= 2022]].dropna().diff().std() for f in df.index}; return 100*(np.mean([v[f] for f in df.index if tr[f]]) - np.mean([v[f] for f in df.index if not tr[f]]))
def nrm(df, tr): ch = {f: (df.loc[f].dropna().iloc[-1] - df.loc[f].dropna().iloc[-2]) for f in df.index}; return 100*(np.mean([ch[f] for f in df.index if tr[f]]) - np.mean([ch[f] for f in df.index if not tr[f]]))
for fn, nm in [(lvl, 'level 2023-25 vs 2019-21'), (vol, 'volatility after 2022'), (nrm, 'normalization (latest - prior)')]:
    est = fn(W, ctrl); perm = [fn(W, {f: int(f in c) for f in firms}) for c in combinations(firms, 5)]; print(f"{nm}: {est:+.1f} pp · p = {np.mean(np.abs(np.array(perm)) >= abs(est) - 1e-9):.3f} · rank {1 + sum(abs(x) > abs(est) for x in perm)}/{len(perm)}")
