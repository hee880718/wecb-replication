"""Clean re-run (2026-10-25; aggregate = mean of the three firms' log series) of the 112-specification curve: 2 preps (SA, TTM) x 2 counterfactuals (peers, own trend) x 4 units x 7 estimators.
Quarterly panel 2017Q1-2025Q4, 15 complete foreign donors, treatment from 2022Q4. Effects in log points (mean post-period gap)."""
import pandas as pd, numpy as np, json, sys, os
from scipy.optimize import minimize
D = 'data' if os.path.isdir('data') else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'figures', 'data')
P = pd.read_csv(f'{D}/quarterly_panel_local_v5.csv', index_col=0); cur = json.load(open(f'{D}/quarterly_currency_v2.json'))
FX = {'CNY': {2016: 6.64, 2017: 6.75, 2018: 6.62, 2019: 6.91, 2020: 6.90, 2021: 6.45, 2022: 6.73, 2023: 7.08, 2024: 7.19, 2025: 7.18}, 'KRW': {2016: 1160, 2017: 1130, 2018: 1100, 2019: 1166, 2020: 1180, 2021: 1144, 2022: 1292, 2023: 1306, 2024: 1364, 2025: 1420}}
U = P.copy()
for f in U.index:
    cc = cur.get(f, 'USD')
    if cc in FX: U.loc[f] = [v / FX[cc][int(p[:4])] if pd.notna(v) else np.nan for p, v in zip(U.columns, U.loc[f])]
per = [p for p in U.columns if '2017Q1' <= p <= '2025Q4']; PRE = [p for p in per if p <= '2022Q3']; POST = [p for p in per if p >= '2022Q4']
L = np.log(U.where(U > 0))[per]; L.loc['TR:EQUIP3'] = L.loc[['TR:NAURA', 'TR:AMEC', 'TR:ACMR']].mean(axis=0, skipna=True)   # aggregate = mean of the three log series
ctrl = [i for i in L.index if not i.startswith('TR:') and L.loc[i].notna().all()]
def prep_SA(X):
    S = X.copy()
    for u in X.index:
        for q in (1, 2, 3, 4):
            idx = [p for p in per if int(p[-1]) == q]; S.loc[u, idx] = X.loc[u, idx] - X.loc[u, [p for p in PRE if int(p[-1]) == q]].mean()
    return S
def prep_TTM(X):
    allp = [p for p in U.columns if p <= '2025Q4']; Lf = np.log(U.where(U > 0))[allp]; Lf.loc['TR:EQUIP3'] = Lf.loc[['TR:NAURA', 'TR:AMEC', 'TR:ACMR']].mean(axis=0, skipna=True); T = pd.DataFrame(index=X.index, columns=per, dtype=float)
    for u in X.index:
        v = np.exp(Lf.loc[u]); r = v.rolling(4).sum(); T.loc[u] = np.log(r[per].values.astype(float))
    return T
def detrend(X):   # own-trend counterfactual: remove each unit's pre-period linear trend
    t = np.arange(len(per)); S = X.copy()
    for u in X.index:
        y = X.loc[u].values; m = ~np.isnan(y[:len(PRE)])
        if m.sum() >= 8: b = np.polyfit(t[:len(PRE)][m], y[:len(PRE)][m], 1); S.loc[u] = y - np.polyval(b, t)
        else: S.loc[u] = np.nan
    return S
def simplex(X, y): n = X.shape[1]; return minimize(lambda w: np.sum((X @ w - y) ** 2), np.ones(n) / n, bounds=[(0, 1)] * n, constraints={'type': 'eq', 'fun': lambda w: w.sum() - 1}, method='SLSQP').x
def est_SC(y, C): w = simplex(C[:, :len(PRE)].T, y[:len(PRE)]); return np.mean(y[len(PRE):] - C[:, len(PRE):].T @ w)
def est_ASCM(y, C, lam=1.0):
    Cp, Cq = C[:, :len(PRE)].T, C[:, len(PRE):].T; w = simplex(Cp, y[:len(PRE)]); B = np.linalg.solve(Cp.T @ Cp + lam * np.eye(Cp.shape[1]), Cp.T @ (y[:len(PRE)] - Cp @ w)); return np.mean(y[len(PRE):] - (Cq @ w + Cq @ B))
def est_SDID(y, C):
    Cp, Cq = C[:, :len(PRE)], C[:, len(PRE):]; n = len(C); dif = np.diff(Cp, axis=1); zeta = (len(POST)) ** 0.25 * np.nanstd(dif)
    r = minimize(lambda v: np.sum((v[0] + Cp.T @ v[1:] - y[:len(PRE)]) ** 2) + zeta ** 2 * len(PRE) * np.sum(v[1:] ** 2), np.r_[0, np.ones(n) / n], bounds=[(None, None)] + [(0, 1)] * n, constraints={'type': 'eq', 'fun': lambda v: v[1:].sum() - 1}, method='SLSQP'); w = r.x[1:]
    rl = minimize(lambda v: np.sum((v[0] + Cp @ v[1:] - Cq.mean(axis=1)) ** 2) + 1e-6 * np.sum(v[1:] ** 2), np.r_[0, np.ones(len(PRE)) / len(PRE)], bounds=[(None, None)] + [(0, 1)] * len(PRE), constraints={'type': 'eq', 'fun': lambda v: v[1:].sum() - 1}, method='SLSQP'); lam = rl.x[1:]
    return (y[len(PRE):].mean() - lam @ y[:len(PRE)]) - w @ (Cq.mean(axis=1) - Cp @ lam)
def est_TWFE(y, C): return (y[len(PRE):].mean() - y[:len(PRE)].mean()) - (C[:, len(PRE):].mean() - C[:, :len(PRE)].mean())
def est_BJS(y, C):   # TWFE fitted on untreated cells, imputed counterfactual for treated post
    M = np.vstack([C, y]); mask = np.ones_like(M, bool); mask[-1, len(PRE):] = False
    a = np.zeros(M.shape[0]); b = np.zeros(M.shape[1]); mu = np.nanmean(M[mask])
    for _ in range(200):
        R = M - mu - b[None, :]; a = np.array([np.mean(R[i][mask[i]]) for i in range(M.shape[0])]); R = M - mu - a[:, None]; b = np.array([np.mean(R[:, t][mask[:, t]]) for t in range(M.shape[1])])
    imp = mu + a[-1] + b[len(PRE):]; return np.mean(y[len(PRE):] - imp)
def est_GSC(y, C, r=2):   # interactive fixed effects: factors from control panel, loadings from treated pre-period
    Cm = C - C.mean(axis=1, keepdims=True); tm = Cm.mean(axis=0); F = np.linalg.svd(Cm - tm, full_matrices=False)[2][:r]   # r x T factors
    yc = y - y[:len(PRE)].mean(); X = np.c_[np.ones(len(PRE)), F[:, :len(PRE)].T]; coef = np.linalg.lstsq(X, yc[:len(PRE)] - tm[:len(PRE)], rcond=None)[0]
    cf = tm[len(PRE):] + coef[0] + F[:, len(PRE):].T @ coef[1:]; return np.mean(yc[len(PRE):] - cf)
def est_MC(y, C, lam=0.5, iters=300):   # soft-impute nuclear-norm matrix completion with unit/time FE
    M = np.vstack([C, y]); obs = np.ones_like(M, bool); obs[-1, len(PRE):] = False; Z = np.where(obs, M, np.nanmean(M[obs]))
    for _ in range(iters):
        a = Z.mean(axis=1, keepdims=True); b = (Z - a).mean(axis=0, keepdims=True); Rz = Z - a - b
        u, s, vt = np.linalg.svd(Rz, full_matrices=False); Lr = (u * np.maximum(s - lam, 0)) @ vt + a + b; Z = np.where(obs, M, Lr)
    return np.mean(y[len(PRE):] - Lr[-1, len(PRE):])
EST = {'SDID': est_SDID, 'SC': est_SC, 'ASCM': est_ASCM, 'GSC': est_GSC, 'MC': est_MC, 'BJS': est_BJS, 'TWFE': est_TWFE}
rows = []
for prep_name, prep in [('SA', prep_SA), ('TTM', prep_TTM)]:
    X = prep(L)
    for cf_name, cf in [('peers', lambda Z: Z), ('own trend', detrend)]:
        Y = cf(X)
        for unit in ['EQUIP3', 'NAURA', 'AMEC', 'ACMR']:
            y = Y.loc['TR:' + unit].values.astype(float); cs = [c for c in ctrl if Y.loc[c].notna().all()]; C = Y.loc[cs].values.astype(float)
            ok = ~np.isnan(y)
            if ok.sum() < len(per):   # AMEC starts 2019: trim periods to the unit's observed window
                y2 = y[ok]; C2 = C[:, ok]; npre = int(ok[:len(PRE)].sum())
            else: y2, C2, npre = y, C, len(PRE)
            for en, fn in EST.items():
                try:
                    PRE_save, POST_save = PRE, POST; globals()['PRE'] = PRE[:npre] if npre < len(PRE) else PRE
                    tau = fn(y2, C2)
                finally: globals()['PRE'] = PRE_save
                rows.append({'prep': prep_name, 'counterfactual': cf_name, 'unit': unit, 'estimator': en, 'tau': float(tau)})
S = pd.DataFrame(rows); S['pct'] = 100 * (np.exp(S.tau) - 1); S[['prep', 'counterfactual', 'unit', 'estimator', 'tau']].to_csv(f'{D}/spec_curve_feed.csv', index=False)
print("n =", len(S))
for cfn in ['peers', 'own trend']:
    x = S[S.counterfactual == cfn]; print(f"{cfn:10} median {x.pct.median():+.0f}% · >0 {100*(x.pct>0).mean():.0f}% · min {x.pct.min():+.0f} max {x.pct.max():+.0f}")
print(S[(S.prep == 'SA') & (S.counterfactual == 'peers')].pivot(index='unit', columns='estimator', values='tau').round(2).to_string())
print(S[(S.prep == 'SA') & (S.counterfactual == 'own trend')].pivot(index='unit', columns='estimator', values='tau').round(2).to_string())

# placebo ranks for the SA specifications reported in the text (ASCM vs peers, ASCM vs own trend, SDID vs peers)
X = prep_SA(L); out = []
for cf_name, cf in [('peers', lambda Z: Z), ('own trend', detrend)]:
    Y = cf(X)
    for unit in ['EQUIP3', 'NAURA', 'AMEC', 'ACMR']:
        y = Y.loc['TR:' + unit].values.astype(float); cs = [c for c in ctrl if Y.loc[c].notna().all()]; ok = ~np.isnan(y); npre = int(ok[:len(PRE)].sum())
        for en in (['ASCM', 'SDID'] if cf_name == 'peers' else ['ASCM']):
            PRE_save = PRE; globals()['PRE'] = PRE[:npre] if npre < len(PRE) else PRE
            C = Y.loc[cs].values.astype(float)[:, ok]; t = EST[en](y[ok], C)
            pl = [EST[en](Y.loc[j].values.astype(float)[ok], Y.loc[[c for c in cs if c != j]].values.astype(float)[:, ok]) for j in cs]
            globals()['PRE'] = PRE_save; out.append({'counterfactual': cf_name, 'unit': unit, 'estimator': en, 'tau': round(t, 3), 'rank': 1 + sum(p >= t for p in pl), 'n_paths': len(pl) + 1})
R = pd.DataFrame(out); R.to_csv(f'{D}/spec_curve_ranks.csv', index=False); print(R.to_string(index=False))
