"""§5.1 / Figure 3: ladder tests on three customs sources with v2 baskets; writes ladder_v2_three_sources_RW.csv.
Inputs (figures/data): china_exports_baskets_v2_{baci,comtrade,mirror}.csv built from BACI V202601 and the UN Comtrade HS6 warehouse
(China-reported: reporter 156 flow X; importer-reported: reporters as importers, flow M, partner 156).
Baskets v2: WFE 848610/20/40/90+903082/903141; SEMI 8541 ex-PV + 8542; NET 851761/62; SERVER 847141/49/50/70; CONS 851712/13+847130+852872."""
import pandas as pd, numpy as np
ALLIES = [392, 410, 490, 528, 276, 826, 250, 380, 124, 36, 702]; PRE, POST = [2019, 2020, 2021], [2023, 2024]; G = ['WFE', 'SEMI', 'NETWORK', 'SERVER', 'CONSUMER']
def gap(sub, dests):
    t = sub[sub.partner.isin(dests)].groupby('year').value_usd.sum().reindex(range(2019, 2025), fill_value=0); r = sub[~sub.partner.isin(dests)].groupby('year').value_usd.sum().reindex(range(2019, 2025), fill_value=0)
    return np.nan if t[POST].sum() <= 0 or t[PRE].sum() <= 0 else (np.log(t[POST].sum()) - np.log(t[PRE].sum())) - (np.log(r[POST].sum()) - np.log(r[PRE].sum()))
def rw_stepdown(act, P):
    k = len(act); order = np.argsort(act); adj = np.zeros(k); prev = 0
    for step, idx in enumerate(order):
        rest = order[step:]; maxstat = np.nanmin(P[:, rest], axis=1); p = (1 + np.sum(maxstat <= act[idx])) / (len(maxstat) + 1); adj[idx] = max(p, prev); prev = adj[idx]
    return adj
rows = []
for name, fn in [('BACI', 'china_exports_baskets_v2_baci.csv'), ('CN', 'china_exports_baskets_v2_comtrade.csv'), ('MIR', 'china_exports_baskets_v2_mirror.csv')]:
    df = pd.read_csv(f'../../figures/data/{fn}'); df = df[df.partner != 0]; base = df[df.year.isin(PRE)].groupby('partner').value_usd.sum().sort_values(ascending=False); top40 = [p for p in base.index if p != 842][:40]; pool = [p for p in base.index[:70] if p != 842]
    rng = np.random.default_rng(7); draws = [list(rng.choice(pool, 11, replace=False)) for _ in range(100)]
    aU = np.array([gap(df[df.grp == g], [842]) for g in G]); PU = np.nan_to_num(np.array([[gap(df[df.grp == g], [d]) for g in G] for d in top40])); aA = np.array([gap(df[df.grp == g], ALLIES) for g in G]); PA = np.nan_to_num(np.array([[gap(df[df.grp == g], d) for g in G] for d in draws]))
    rwU, rwA = rw_stepdown(aU, PU), rw_stepdown(aA, PA)
    for i, g in enumerate(G): rows.append({'source': name, 'basket': g, 'us_pct': round(100*(np.exp(aU[i])-1)), 'us_p': round((1 + np.sum(PU[:, i] <= aU[i])) / (len(PU) + 1), 3), 'us_rw_p': round(rwU[i], 3), 'allies_pct': round(100*(np.exp(aA[i])-1)), 'allies_p': round((1 + np.sum(PA[:, i] <= aA[i])) / (len(PA) + 1), 3), 'allies_rw_p': round(rwA[i], 3)})
pd.DataFrame(rows).to_csv('ladder_v2_three_sources_RW.csv', index=False); print(pd.DataFrame(rows).to_string(index=False))
