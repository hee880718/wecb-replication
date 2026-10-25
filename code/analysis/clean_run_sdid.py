"""Clean run (9 Oct 2026): quarterly SA SDID (15 donors) for the toolmakers and annual SDID for Huawei / ZTE segments via sdid2.sdid. Reproduces registry F8, K1v2, K2v2."""
import pandas as pd, numpy as np, json
src = open('sdid2.py').read().split('\nif __name__')[0]; m = {}; exec(compile(src, 'sdid2', 'exec'), m)
P = pd.read_csv('../../figures/data/quarterly_panel_local_v5.csv', index_col=0); cur = json.load(open('../../figures/data/quarterly_currency_v2.json')); FX = {'CNY': m['FX']['CNY'], 'KRW': m['FX']['KRW']}; U = P.copy()
for f in U.index:
    cc = cur.get(f, 'USD')
    if cc in FX: U.loc[f] = [v / FX[cc][int(p[:4])] if pd.notna(v) else np.nan for p, v in zip(U.columns, U.loc[f])]
per = [p for p in U.columns if '2017Q1' <= p <= '2025Q4']; PRE = [p for p in per if p <= '2022Q3']; POST = [p for p in per if p >= '2022Q4']; L = np.log(U.where(U > 0))[per]; S = L.copy()
for u in L.index:
    for q in (1, 2, 3, 4):
        idx = [p for p in per if int(p[-1]) == q]; S.loc[u, idx] = L.loc[u, idx] - L.loc[u, [p for p in PRE if int(p[-1]) == q]].mean()
S.loc['TR:EQUIP3'] = S.loc[['TR:NAURA', 'TR:AMEC', 'TR:ACMR']].mean(axis=0, skipna=True).values; ctrl = [i for i in S.index if not i.startswith('TR:') and S.loc[i].notna().all()]; m['PRE'], m['POST'] = PRE, POST
val = lambda r: r[0] if isinstance(r, (tuple, list, np.ndarray)) else r
for u in ['TR:EQUIP3', 'TR:NAURA', 'TR:AMEC', 'TR:ACMR']:
    t = val(m['sdid'](S, u, ctrl)); pl = [val(m['sdid'](S, j, [c for c in ctrl if c != j])) for j in ctrl]; print(f"{u[3:]:7} tau={t:+.2f} rank {1+sum(p >= t for p in pl)}/{len(pl)+1}")
D = pd.read_csv('../../figures/data/telecom_device_panel_logUSD_v2.csv', index_col=0); D.columns = D.columns.astype(int); donors = [i for i in D.index if not i.startswith('TR:') and D.loc[i].notna().sum() >= 9]
for tr, pre, post in [('TR:Huawei', [2015, 2016, 2017, 2018, 2019], [2021, 2022, 2023]), ('TR:ZTE_consumer', [2015, 2016, 2017], [2019, 2020, 2021, 2022, 2023]), ('TR:ZTE_carrier', [2015, 2016, 2017], [2019, 2020, 2021, 2022, 2023])]:
    m['PRE'], m['POST'] = pre, post; dd = [d for d in donors if D.loc[d, pre + post].notna().all()]; t = val(m['sdid'](D, tr, dd)); pl = [val(m['sdid'](D, j, [c for c in dd if c != j])) for j in dd]; print(f"{tr[3:]:13} tau={t:+.2f} ({100*(np.exp(t)-1):+.0f}%) donors {len(dd)} rank {1+sum(p <= t for p in pl)}/{len(pl)+1}")
