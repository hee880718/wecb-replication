import os as _os; ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..')); PROC = _os.path.join(ROOT, 'data', 'processed'); FIGD = _os.path.join(ROOT, 'figures', 'data')
import pandas as pd, numpy as np, json, textwrap, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams.update({'font.family':'serif','font.size':9,'axes.spines.top':False,'axes.spines.right':False,'axes.edgecolor':'#444','axes.linewidth':0.6,'xtick.color':'#444','ytick.color':'#444','figure.facecolor':'white','savefig.dpi':300})
H = {'title':'#6E0E18','red':'#A11C22','pink':'#E8B4A4','navy':'#1F3A5F','grey':'#9AA3AD','ink':'#333333','light':'#D9DEE3'}; OUT = _os.path.join(ROOT, 'figures', 'data')
P = pd.read_csv(_os.path.join(FIGD, 'quarterly_panel_local_v5.csv'), index_col=0); cur = json.load(open(_os.path.join(FIGD, 'quarterly_currency_v2.json')))
FX = {'CNY':{2016:6.64,2017:6.75,2018:6.62,2019:6.91,2020:6.90,2021:6.45,2022:6.73,2023:7.08,2024:7.19,2025:7.18},'KRW':{2016:1160,2017:1130,2018:1100,2019:1166,2020:1180,2021:1144,2022:1292,2023:1306,2024:1364,2025:1420}}
U = P.copy()
for f in U.index:
    cc = cur.get(f, 'USD')
    if cc in FX: U.loc[f] = [v / FX[cc][int(p[:4])] if pd.notna(v) else np.nan for p, v in zip(U.columns, U.loc[f])]
yrs = list(range(2017, 2026)); A = pd.DataFrame({y: U[[c for c in U.columns if c.startswith(str(y))]].sum(axis=1, min_count=4) for y in yrs})
cn = ['TR:NAURA','TR:AMEC','TR:ACMR']; peers = [i for i in A.index if not i.startswith('TR:') and A.loc[i].notna().all()]
idx = lambda s: 100*s/s[2019]; cn_idx = idx(A.loc[cn].sum()); peer_idx = A.loc[peers].apply(idx, axis=1); peer_med = peer_idx.median(); lo, hi = peer_idx.quantile(0.25), peer_idx.quantile(0.75)
b = np.polyfit(range(2017, 2023), np.log(cn_idx[list(range(2017, 2023))].values), 1); own = pd.Series(np.exp(np.polyval(b, yrs)), index=yrs)
g_cn = cn_idx.pct_change()*100; g_pe = (A.loc[peers].sum()).pct_change()*100
cn6 = pd.read_csv(_os.path.join(PROC, 'cn6_revenue_annual.csv')); cne = pd.read_csv(_os.path.join(PROC, 'CN_equipment_annual_parsed_NAURA_AMEC_Piotech.csv')).drop_duplicates(['firm','year'])
ann = {}
for f in ['NAURA','AMEC']: s = cne[cne.firm==f].set_index('year'); ann[f] = (s.rev_Q1+s.rev_Q2+s.rev_Q3+s.rev_Q4)
ann['ACM Research'] = A.loc['TR:ACMR']
for f, nm in [('Kingsemi','Kingsemi'),('Changchuan_test','Changchuan'),('Jingce_metrology','Jingce')]: ann[nm] = cn6[cn6.firm==f].set_index('year').rev_cny
def dg(s):
    s = s.dropna(); pre = [y for y in range(2019, 2023) if y in s.index and y-1 in s.index]; post = [y for y in range(2023, 2026) if y in s.index and y-1 in s.index and s[y-1] > 0]
    return (np.mean([100*(s[y]/s[y-1]-1) for y in post]) - np.mean([100*(s[y]/s[y-1]-1) for y in pre])) if pre and post else np.nan
foot = [('NAURA\netch, deposition', True), ('AMEC\netch', True), ('ACM Research\ncleaning', True), ('Kingsemi\ntrack', False), ('Changchuan\nback-end test', False), ('Jingce\ndisplay metrology', False)]
vals = [dg(ann[n.split('\n')[0]]) for n, _ in foot]; print("성장률 변화(pp):", dict(zip([n.split(chr(10))[0] for n, _ in foot], np.round(vals, 0))))
for titled in (True, False):
    fig = plt.figure(figsize=(8.27, 7.4)); gs = fig.add_gridspec(2, 2, height_ratios=[1.25, 1], hspace=0.55, wspace=0.32, left=0.08, right=0.97, top=0.85 if titled else 0.96, bottom=0.1)
    a = fig.add_subplot(gs[0, :]); a.grid(axis='y', color=H['light'], lw=0.6); a.set_axisbelow(True); a.tick_params(length=0)
    a.fill_between(yrs, lo.values, hi.values, color='#E6E8EB', lw=0); a.plot(yrs, peer_med.values, color=H['grey'], lw=2, ls='--'); a.plot(yrs, own.values, color=H['navy'], lw=1.6, ls=':'); a.plot(yrs, cn_idx.values, color=H['red'], lw=2.6, marker='o', ms=4)
    a.axvspan(2022.75, 2025.5, color=H['pink'], alpha=0.18, lw=0); a.text(2022.85, 32, 'Oct-2022 controls', fontsize=7, color='#555')
    a.text(2025.1, cn_idx[2025]*0.93, f'actual {cn_idx[2025]:.0f}', color=H['red'], fontsize=8.5, weight='bold', va='center'); a.text(2025.1, own[2025]*0.92, f'own pre-2022 trend {own[2025]:.0f}', color=H['navy'], fontsize=7.5, va='center'); a.text(2025.1, peer_med[2025], f'foreign peers (median) {peer_med[2025]:.0f}', color='#666', fontsize=7.5, va='center')
    a.set_xlim(2016.8, 2027.3); a.set_yscale('log'); a.set_yticks([50, 100, 200, 400, 800, 1600]); a.set_yticklabels(['50', '100', '200', '400', '800', '1,600']); a.set_ylabel('Revenue, 2019 = 100 (log scale)', fontsize=8)
    a.set_title('a. Chinese etch/deposition/cleaning makers slowed a little after 2022; foreign peers stalled', loc='left', fontsize=9.3, weight='bold', color=H['ink'])
    bx = fig.add_subplot(gs[1, 0]); bx.grid(axis='y', color=H['light'], lw=0.6); bx.set_axisbelow(True); bx.tick_params(length=0)
    gy = [y for y in yrs if y >= 2018]; w = 0.38; bx.bar([y - w/2 for y in gy], g_cn[gy].values, w, color=H['red']); bx.bar([y + w/2 for y in gy], g_pe[gy].values, w, color=H['grey']); bx.axhline(0, color='#444', lw=0.8)
    for y in gy: bx.text(y - w/2, g_cn[y] + 2, f'{g_cn[y]:+.0f}', ha='center', fontsize=6.3, color=H['red']); bx.text(y + w/2, g_pe[y] + (2 if g_pe[y] >= 0 else -7), f'{g_pe[y]:+.0f}', ha='center', fontsize=6.3, color='#666')
    bx.text(2021.3, 76, 'Chinese toolmakers (3)', color=H['red'], fontsize=7.3, weight='bold'); bx.text(2021.3, 69, 'foreign toolmakers (12)', color='#666', fontsize=7.3); bx.set_ylim(-25, 84); bx.set_xticks(gy); bx.set_xticklabels([f"'{str(y)[2:]}" for y in gy], fontsize=7.5); bx.set_ylabel('Annual revenue growth (%)', fontsize=8)
    bx.set_title('b. Growth every year: slower, never negative', loc='left', fontsize=9.3, weight='bold', color=H['ink'])
    c = fig.add_subplot(gs[1, 1]); c.grid(axis='x', color=H['light'], lw=0.6); c.set_axisbelow(True); c.tick_params(length=0)
    ypos = np.arange(len(foot))[::-1]; c.barh(ypos, vals, color=[H['red'] if f[1] else H['grey'] for f in foot], height=0.6); c.axvline(0, color='#444', lw=0.8)
    for y, v in zip(ypos, vals):
        if pd.notna(v): c.text(v + (1.5 if v >= 0 else -1.5), y, f'{v:+.0f} pp', va='center', ha='left' if v >= 0 else 'right', fontsize=7, color=H['ink'])
    c.set_yticks(ypos); c.set_yticklabels([f[0] for f in foot], fontsize=7.2); c.set_xlabel('Change in average annual growth, 2023–25 vs 2019–22 (pp)', fontsize=7.5); c.set_xlim(-135, 30)
    c.set_title('c. Growth slowed least where the decree bit', loc='left', fontsize=9.3, weight='bold', color=H['ink'])
    if titled: fig.text(0.01, 0.985, 'Did the controls speed Chinese toolmakers up? No. Stop them? Also no.', fontsize=12.5, color=H['title'], weight='bold', va='top'); fig.text(0.01, 0.948, textwrap.fill('Revenue kept rising at 30–40 percent a year while foreign peers stalled in 2023–24 — and the slowdown was smallest in the segments the decree actually covered', 118), fontsize=9, color='#555', va='top')
    fig.text(0.01, 0.008, textwrap.fill("Sources: audited annual revenue in USD — NAURA, AMEC, ACM Research (cninfo, SEC); 12 U.S. and Korean toolmakers with complete quarterly data (SEC EDGAR, OpenDART). Panel a: band = interquartile range of foreign peers' indices; own trend = log-linear fit 2017–2022 extrapolated. Panel c: annual reports (cninfo); controlled segments in red.", 150), fontsize=6.5, color='#666', va='bottom', linespacing=1.3)
    fig.savefig(OUT + f"F2alt_feed_plain{'' if titled else '_notitle'}.png"); plt.close(fig)
print("F2alt 확정")
