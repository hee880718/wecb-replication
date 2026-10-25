import os as _os; ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)) if '__file__' in globals() else _os.getcwd(), '..', '..')); PROC = _os.path.join(ROOT, 'data', 'processed'); FIGD = _os.path.join(ROOT, 'figures', 'data')
import pandas as pd, numpy as np
from scipy.optimize import minimize
FX = {  # 연평균 근사: CNY/USD, JPY/USD, KRW/USD, USD/EUR (문서화된 근사치 — 현지통화 결과로 강건성 확인)
 'CNY': {2016:6.64,2017:6.75,2018:6.62,2019:6.91,2020:6.90,2021:6.45,2022:6.73,2023:7.08,2024:7.19,2025:7.18},
 'JPY': {2016:108.8,2017:112.2,2018:110.4,2019:109.0,2020:106.8,2021:109.8,2022:131.5,2023:140.5,2024:151.4,2025:149.0},
 'KRW': {2016:1160,2017:1130,2018:1100,2019:1166,2020:1180,2021:1144,2022:1292,2023:1306,2024:1364,2025:1420},
 'EUR': {2016:1.107,2017:1.130,2018:1.181,2019:1.120,2020:1.142,2021:1.183,2022:1.053,2023:1.081,2024:1.082,2025:1.13}}
YRS = list(range(2017, 2026)); PRE = [y for y in YRS if y <= 2022]; POST = [y for y in YRS if y >= 2023]
def build(usd=True):
    S = {}
    c = pd.read_csv(_os.path.join(PROC, 'EDGAR_controls_revenue_frames_19firms.csv'))
    a = c[(c.freq=='A')].pivot_table(index='firm', columns='year', values='revenue', aggfunc='first')
    for f in a.index:
        if f == 'ACMR': continue
        s = a.loc[f]
        if f == 'ASML' and usd: s = s * pd.Series(FX['EUR'])
        S['US/EU:'+f] = s
    j = pd.read_csv(_os.path.join(PROC, 'edinet_revenue_annual.csv'))
    for f in ['TEL','SCREEN','Lasertec','DISCO','Advantest','TokyoSeimitsu','ULVAC','JEOL']:
        s = j[j.firm==f].assign(cal=lambda x: x.fy-1).set_index('cal').revenue_jpy   # 3월 결산 → 역년(9개월 귀속)
        S['JP:'+f] = s / pd.Series(FX['JPY']) if usd else s
    k = pd.read_csv(_os.path.join(PROC, 'dart_revenue_annual.csv'))
    for f in ['WonikIPS','PSK','Jusung','EugeneTech','TES']:
        s = k[k.firm==f].set_index('year').revenue_krw; S['KR:'+f] = s / pd.Series(FX['KRW']) if usd else s
    cn = pd.read_csv(_os.path.join(PROC, 'CN_equipment_annual_parsed_NAURA_AMEC_Piotech.csv')).drop_duplicates(['firm','year'])
    cn['tot'] = cn[['rev_Q1','rev_Q2','rev_Q3','rev_Q4']].sum(axis=1, min_count=4)
    T = {'NAURA_equip': cn[cn.firm=='NAURA'].set_index('year')['seg_电子工艺装备'], 'AMEC': cn[cn.firm=='AMEC'].set_index('year')['tot']}
    sm = pd.read_csv(_os.path.join(PROC, 'SMIC_quarterly_parsed_2004-2026.csv')); sm = sm[sm.revenue_usd_k.notna()].copy(); sm['y'] = sm.quarter.str[:4].astype(int)
    T['SMIC'] = sm.groupby('y').revenue_usd_k.sum() * 1000
    T['HuaHong'] = pd.Series({2017:808,2018:930,2019:933,2020:961,2021:1631,2022:2475,2023:2286,2024:2004,2025:2402}) * 1e6
    for f in ['NAURA_equip','AMEC']:
        if usd: T[f] = T[f] / pd.Series(FX['CNY'])
    Y = pd.DataFrame({k: v.reindex(YRS) for k, v in {**S, **{'TR:'+k: v for k, v in T.items()}}.items()}).T.astype(float)
    return np.log(Y.where(Y > 0))
def sdid(Y, tr, ctrl):
    yt = Y.loc[tr]; pre = [y for y in PRE if pd.notna(yt[y])]; post = [y for y in POST if pd.notna(yt[y])]
    C = Y.loc[ctrl, pre + post].dropna(); n = len(C)
    Cp, Cq = C[pre].values, C[post].values
    dif = np.diff(Cp, axis=1); zeta = (1 * len(post)) ** 0.25 * np.nanstd(dif)
    def wobj(v):  # v = [w0, ω...]
        w0, w = v[0], v[1:]; return np.sum((w0 + Cp.T @ w - yt[pre].values) ** 2) + zeta**2 * len(pre) * np.sum(w**2)
    r = minimize(wobj, np.r_[0, np.ones(n)/n], bounds=[(None,None)] + [(0,1)]*n, constraints={'type':'eq','fun':lambda v: v[1:].sum()-1}, method='SLSQP')
    w = r.x[1:]
    target = Cq.mean(axis=1)
    def lobj(v):
        l0, l = v[0], v[1:]; return np.sum((l0 + Cp @ l - target) ** 2) + 1e-6 * np.sum(l**2)
    rl = minimize(lobj, np.r_[0, np.ones(len(pre))/len(pre)], bounds=[(None,None)] + [(0,1)]*len(pre), constraints={'type':'eq','fun':lambda v: v[1:].sum()-1}, method='SLSQP')
    lam = rl.x[1:]
    tau = (yt[post].mean() - lam @ yt[pre].values) - w @ (Cq.mean(axis=1) - Cp @ lam)
    return tau, dict(zip(C.index, w)), dict(zip(pre, lam)), list(C.index), pre, post
