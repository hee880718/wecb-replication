"""§5.2 / Appendix C: HS8 shape tests (registry A1), clean re-run 2026-10-25. Controlled lines 84862039/21/41/29 vs uncontrolled 84862010/22/31/50/49,
allied origins (US, JP, NL). Statistics are means of line-level measures; p-values from all 126 assignments of four 'controlled' lines among nine (two-sided)."""
import pandas as pd, numpy as np
from itertools import combinations
w = pd.read_csv('../../data/processed/GACC_batch1_combined_hs8_monthly.csv.gz', low_memory=False); w['usd'] = pd.to_numeric(w['usd'], errors='coerce'); w['hs8'] = w['Commodity code'].astype(str).str[:8]; w['ym'] = w['Date of data'].astype(str); w['year'] = w.ym.str[:4].astype(int); w['allied'] = w['Trading partner'].isin(['United States', 'Japan', 'Netherlands'])
C = {'84862039', '84862021', '84862041', '84862029'}; U = {'84862010', '84862022', '84862031', '84862050', '84862049'}; lines = sorted(C | U)
sub = w[w.allied & w.hs8.isin(lines)]; m = sub.groupby(['hs8', 'ym']).usd.sum().unstack().fillna(0); m = m[[c for c in m.columns if '201901' <= c <= '202512']]; ann = sub.groupby(['hs8', 'year']).usd.sum().unstack().fillna(0)
lv = {l: np.log(ann.loc[l, [2023, 2024, 2025]].sum() / ann.loc[l, [2019, 2020, 2021]].sum()) for l in lines}
vo = {l: np.log(m.loc[l][[c for c in m.columns if c >= '202211']].replace(0, np.nan)).diff().std() for l in lines}
nr = {l: np.log(ann.loc[l, 2025] / ann.loc[l, 2024]) for l in lines}
def stat(d, tr): return np.mean([d[l] for l in lines if tr[l]]) - np.mean([d[l] for l in lines if not tr[l]])
for nm, d in [('level 2023-25 vs 2019-21', lv), ('volatility of monthly log changes after Oct 2022', vo), ('normalization 2025 vs 2024', nr)]:
    a = stat(d, {l: l in C for l in lines}); perms = [stat(d, {l: l in c for l in lines}) for c in combinations(lines, 4)]; pv = np.mean([abs(p) >= abs(a) - 1e-12 for p in perms]); print(f"{nm:50} {a:+.3f}  p = {pv:.2f} ({int(round(pv*126))}/126)")
