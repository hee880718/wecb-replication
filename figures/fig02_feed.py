"""Fig 2 — shielded substitution: three paths, annual growth, footprint."""
import housestyle as H, matplotlib.pyplot as plt, pandas as pd, numpy as np, os
H.setup(); D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
A = pd.read_csv(f'{D}/annual_revenue_usd_panel.csv', index_col=0); A.columns = A.columns.astype(int); yrs = list(A.columns)
cn = ['TR:NAURA', 'TR:AMEC', 'TR:ACMR']; peers = [i for i in A.index if not i.startswith('TR:') and A.loc[i].notna().all()]
idx = lambda s: 100 * s / s[2019]; cn_idx = idx(A.loc[cn].sum()); pidx = A.loc[peers].apply(idx, axis=1); pmed, lo, hi = pidx.median(), pidx.quantile(.25), pidx.quantile(.75)
b = np.polyfit(range(2017, 2023), np.log(cn_idx[list(range(2017, 2023))].values), 1); own = pd.Series(np.exp(np.polyval(b, yrs)), index=yrs)
g_cn = cn_idx.pct_change() * 100; g_pe = A.loc[peers].sum().pct_change() * 100
cne = pd.read_csv(f'{D}/cn_equipment_annual.csv').drop_duplicates(['firm', 'year']); cn6 = pd.read_csv(f'{D}/cn6_revenue_annual.csv')
ann = {f: (lambda s: s.rev_Q1 + s.rev_Q2 + s.rev_Q3 + s.rev_Q4)(cne[cne.firm == f].set_index('year')) for f in ['NAURA', 'AMEC']}; ann['ACM Research'] = A.loc['TR:ACMR']
for f, nm in [('Kingsemi', 'Kingsemi'), ('Changchuan_test', 'Changchuan'), ('Jingce_metrology', 'Jingce')]: ann[nm] = cn6[cn6.firm == f].set_index('year').rev_cny
def dg(s):
    s = s.dropna(); pre = [y for y in range(2019, 2023) if y in s.index and y - 1 in s.index]; post = [y for y in range(2023, 2026) if y in s.index and y - 1 in s.index and s[y - 1] > 0]
    return (np.mean([100 * (s[y] / s[y - 1] - 1) for y in post]) - np.mean([100 * (s[y] / s[y - 1] - 1) for y in pre])) if pre and post else np.nan
foot = [('NAURA', 'etch, deposition', True), ('AMEC', 'etch', True), ('ACM Research', 'cleaning', True), ('Kingsemi', 'track', False), ('Changchuan', 'back-end test', False), ('Jingce', 'display metrology', False)]
vals = [dg(ann[n]) for n, _, _ in foot]
fig = plt.figure(figsize=(8.27, 7.0)); gs = fig.add_gridspec(2, 2, height_ratios=[1.05, 1], hspace=0.42, wspace=0.7, left=0.09, right=0.97, top=0.81, bottom=0.13)
a = fig.add_subplot(gs[0, :]); H.ax_clean(a); a.fill_between(yrs, lo.values, hi.values, color='#E8EAED', lw=0); a.plot(yrs, pmed.values, color=H.C['grey'], lw=1.8, ls='--'); a.plot(yrs, own.values, color=H.C['navy'], lw=1.4, ls=':'); a.plot(yrs, cn_idx.values, color=H.C['red'], lw=2.2, marker='o', ms=3.5)
a.axvline(2022.8, color=H.C['pink'], lw=0.9); a.text(2022.85, 0.97, 'US rule', transform=a.get_xaxis_transform(), fontsize=6.2, color=H.C['sub'], rotation=90, va='top')
for y, s, c, w in [(cn_idx[2025], f'Chinese toolmakers  {cn_idx[2025]:.0f}', H.C['red'], 'bold'), (own[2025], f'own 2017–22 trend  {own[2025]:.0f}', H.C['navy'], 'normal'), (pmed[2025], f'foreign peers, median  {pmed[2025]:.0f}', H.C['sub'], 'normal')]: a.text(2025.15, y, s, fontsize=6.8, color=c, va='center', weight=w)
a.set_xlim(2016.8, 2028); a.set_ylim(30, 1700); a.set_yscale('log'); a.set_yticks([50, 100, 200, 400, 800, 1600]); a.set_yticklabels(['50', '100', '200', '400', '800', '1,600'], fontsize=7); a.set_ylabel('Revenue, 2019 = 100 (log)', fontsize=7.5); a.set_xticks(yrs); a.set_xticklabels([f"'{str(y)[2:]}" for y in yrs], fontsize=7)
a.set_title('a. Three paths: actual, own pre-control trend, foreign peers (band = interquartile range)', loc='left', fontsize=9, weight='bold', color=H.C['ink'])
bx = fig.add_subplot(gs[1, 0]); H.ax_clean(bx); gy = [y for y in yrs if y >= 2018]; w = 0.38
bx.bar([y - w / 2 for y in gy], g_cn[gy].values, w, color=H.C['red']); bx.bar([y + w / 2 for y in gy], g_pe[gy].values, w, color=H.C['grey']); bx.axhline(0, color='#444', lw=0.7)
for y in gy: bx.text(y - w / 2, g_cn[y] + 2, f'{g_cn[y]:+.0f}', ha='center', fontsize=6, color=H.C['red']); bx.text(y + w / 2, g_pe[y] + (2 if g_pe[y] >= 0 else -7), f'{g_pe[y]:+.0f}', ha='center', fontsize=6, color=H.C['sub'])
bx.text(0.98, 0.95, 'red: Chinese toolmakers (3)\ngrey: foreign suppliers (15), aggregate', transform=bx.transAxes, fontsize=6.4, color=H.C['sub'], va='top', ha='right'); bx.set_ylim(-25, 100); bx.set_xticks(gy); bx.set_xticklabels([f"'{str(y)[2:]}" for y in gy], fontsize=7); bx.set_ylabel('Annual revenue growth, %', fontsize=7.5); bx.tick_params(axis='y', labelsize=7)
bx.set_title('b. Growth slowed after 2022; it never turned negative', loc='left', fontsize=9, weight='bold', color=H.C['ink'])
c = fig.add_subplot(gs[1, 1]); H.ax_clean(c, grid='x'); ypos = np.arange(len(foot))[::-1]; c.barh(ypos, vals, color=[H.C['red'] if f[2] else H.C['grey'] for f in foot], height=0.6); c.axvline(0, color='#444', lw=0.7)
for y, v in zip(ypos, vals):
    if pd.notna(v): c.text(v + (2 if v >= 0 else -2), y, f'{v:+.0f}', va='center', ha='left' if v >= 0 else 'right', fontsize=6.6, color=H.C['ink'])
c.set_yticks(ypos); c.set_yticklabels([f'{n}  ({s})' for n, s, _ in foot], fontsize=6.6); c.set_xlabel('Change in average annual growth, 2023–25 vs 2019–22 (pp)', fontsize=7); c.set_xlim(-135, 30); c.tick_params(axis='x', labelsize=7)
c.set_title('c. Smallest slowdown where the rule bit', loc='left', fontsize=9, weight='bold', color=H.C['ink']); c.text(0.02, 0.04, 'red: segments covered by the rule', transform=c.transAxes, fontsize=6.2, color=H.C['sub'], va='bottom')
H.headline(fig, 'Shielded substitution: domestic toolmakers slowed, foreign peers stalled', 'Revenue of NAURA, AMEC and ACM Research against two counterfactuals: the median of fifteen foreign equipment and equipment-component suppliers and their own 2017–2022 trend. Growth after the October 2022 rule stayed below the pre-control trend but, unlike foreign peers, never turned negative; the slowdown was smallest in the segments the rule covered.')
H.source(fig, 'Sources: audited annual revenue in USD, sums of quarters (cninfo, SEC EDGAR, OpenDART); annual reports for panel c (cninfo). Foreign suppliers: Applied Materials, KLA, Teradyne, Axcelis, Advanced Energy, Entegris, FormFactor, Ichor, Kulicke & Soffa, MKS, Onto, Eugene Technology, Jusung, TES, Wonik IPS. Own trend: log-linear fit 2017–2022, extrapolated. Changchuan in panel c uses the one comparable post-2022 year; the AMEC pre-period covers 2020–22 (data from 2019).')
data = pd.DataFrame({'year': yrs, 'chinese_index': cn_idx.values, 'own_trend': own.values, 'peer_median': pmed.values, 'peer_q25': lo.values, 'peer_q75': hi.values, 'growth_cn': g_cn.values, 'growth_peers': g_pe.values})
H.save(fig, 'fig02_feed', data)
