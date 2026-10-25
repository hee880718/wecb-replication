"""Appendix Fig A1 — controlled vs uncontrolled HS8 lines, allied-origin imports (2019 = 1)."""
import housestyle as H, matplotlib.pyplot as plt, pandas as pd, numpy as np, os
H.setup(); D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
w = pd.read_csv(f'{D}/gacc_hs8_by_line.csv'); w = w[w.allied]; t = w.pivot_table(index='hs8', columns='year', values='usd', aggfunc='sum').fillna(0) / 1e9; t.index = t.index.astype(str)
C = {'84862039': 'other lithography', '84862021': 'CVD', '84862041': 'dry etch', '84862029': 'other deposition'}; U = {'84862010': 'furnaces', '84862022': 'PVD', '84862031': 'steppers', '84862050': 'implanters', '84862049': 'wet etch / strip'}
fig, ax = plt.subplots(1, 2, figsize=(8.27, 3.9), sharey=True); fig.subplots_adjust(top=0.74, bottom=0.17, left=0.08, right=0.97, wspace=0.08)
for a, Dd, ttl, col in [(ax[0], C, 'a. Controlled lines', H.C['red']), (ax[1], U, 'b. Uncontrolled lines', H.C['grey'])]:
    H.ax_clean(a); a.axvline(2022.8, color=H.C['pink'], lw=0.9)
    ends = []
    for k, nm in Dd.items():
        if k in t.index and t.loc[k, 2019] > 0: y = (t.loc[k] / t.loc[k, 2019]).values; a.plot(t.columns, y, marker='o', ms=2.8, lw=1.5, color=col, alpha=0.95 if Dd is C else 0.8); ends.append([np.log(y[-1]), nm])
    ends.sort()
    for i in range(1, len(ends)):
        if ends[i][0] - ends[i-1][0] < 0.09: ends[i][0] = ends[i-1][0] + 0.09
    for ly, nm in ends: a.text(2025.15, np.exp(ly), nm, fontsize=6.3, va='center', color=H.C['ink'])
    a.set_xlim(2018.8, 2027); a.set_yscale('log'); a.set_yticks([0.5, 1, 2, 4, 8]); a.set_yticklabels(['0.5', '1', '2', '4', '8']); a.set_title(ttl, loc='left', fontsize=9, weight='bold', color=H.C['ink']); a.set_xticks(range(2019, 2026)); a.set_xticklabels([f"'{str(y)[2:]}" for y in range(2019, 2026)], fontsize=7); a.tick_params(axis='y', labelsize=7)
ax[0].set_ylabel('Imports from US, Japan, Netherlands (2019 = 1, log)', fontsize=7.5)
H.headline(fig, 'No compliance ladder at the tariff line either', 'Three of the four controlled tool categories rose at least as much as the uncontrolled ones after October 2022; the fourth, other deposition, is a small line (0.09 bn dollars in 2019) that fell. Shape tests on level, volatility and 2025 normalization are all insignificant (Appendix C).')
H.source(fig, 'Source: GACC HS8 monthly imports from the United States, Japan and the Netherlands, summed by year and indexed to 2019. Classification of lines in Appendix A; HS 84862090 (mixed) excluded. 2019 levels, USD bn: other lithography 1.08, CVD 0.59, dry etch 1.28, other deposition 0.09; furnaces 0.96, PVD 0.25, steppers 0.94, implanters 0.39, wet etch/strip 0.24.')
H.save(fig, 'figA1_hs8_lines', t.reset_index())
