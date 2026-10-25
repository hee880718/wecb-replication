"""Fig 4 — specification curve: 112 feed estimates, by counterfactual."""
import housestyle as H, matplotlib.pyplot as plt, pandas as pd, numpy as np, os
H.setup(); D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
s = pd.read_csv(f'{D}/spec_curve_feed.csv'); s['pct'] = 100 * (np.exp(s.tau) - 1); s = s.sort_values('pct').reset_index(drop=True); cap = 400; s['yplot'] = s.pct.clip(upper=cap); nclip = int((s.pct > cap).sum())
fig = plt.figure(figsize=(8.27, 6.6)); gs = fig.add_gridspec(2, 1, height_ratios=[1.6, 1], hspace=0.3, left=0.2, right=0.97, top=0.80, bottom=0.09)
a = fig.add_subplot(gs[0]); H.ax_clean(a); x = np.arange(len(s))
for cf, col, lab in [('peers', H.C['red'], 'vs foreign peers'), ('own trend', H.C['navy'], 'vs own pre-2022 trend')]:
    m = s.counterfactual == cf; a.scatter(x[m], s.yplot[m], s=14, color=col, zorder=3)
    med = s.pct[m].median(); share = 100 * (s.pct[m] > 0).mean(); a.axhline(med, color=col, lw=0.8, ls=':'); a.text(2, med + 12 if cf == 'peers' else -55, f'{lab}: median {med:+.0f}%, {share:.0f}% of estimates > 0', fontsize=6.8, color=col, va='bottom')
a.axhline(0, color='#444', lw=0.8); a.set_xlim(-1, len(s) + 1); a.set_ylim(-70, cap + 25); a.set_ylabel('Estimated effect on quarterly revenue, %', fontsize=7.5); a.set_xticks([]); a.tick_params(axis='y', labelsize=7)
if nclip: a.text(len(s) - 1, cap + 8, f'{nclip} estimates above {cap}% shown at {cap}%', fontsize=6.3, color=H.C['sub'], ha='right')
a.set_title('a. All 112 estimates, sorted', loc='left', fontsize=9, weight='bold', color=H.C['ink'])
b = fig.add_subplot(gs[1], sharex=a); b.tick_params(length=0); b.set_axisbelow(True)
rows = [('counterfactual', 'own trend', 'own trend'), ('counterfactual', 'peers', 'foreign peers'), ('estimator', 'SDID', 'SDID'), ('estimator', 'SC', 'synthetic control'), ('estimator', 'ASCM', 'augmented SC'), ('estimator', 'GSC', 'generalized SC'), ('estimator', 'MC', 'matrix completion'), ('estimator', 'BJS', 'imputation (BJS)'), ('estimator', 'TWFE', 'two-way FE'), ('prep', 'SA', 'seasonally adjusted'), ('prep', 'TTM', 'trailing 4 quarters'), ('unit', 'EQUIP3', 'aggregate of three'), ('unit', 'NAURA', 'NAURA'), ('unit', 'AMEC', 'AMEC'), ('unit', 'ACMR', 'ACM Research')]
rows = [r for r in rows if (s[r[0]] == r[1]).any()]
for i, (col, val, lab) in enumerate(rows[::-1]):
    m = (s[col] == val).values; b.scatter(x[m], np.full(m.sum(), i), s=9, color=H.C['ink'], marker='|', lw=0.8)
b.set_yticks(range(len(rows))); b.set_yticklabels([r[2] for r in rows[::-1]], fontsize=6.6)
for y in (1.5, 7.5, 9.5): b.axhline(y, color=H.C['light'], lw=0.6); b.set_xlabel('Specification rank', fontsize=7.5); b.tick_params(axis='x', labelsize=7); b.set_ylim(-0.6, len(rows) - 0.4)
b.set_title('b. Which choices each estimate uses', loc='left', fontsize=8, weight='bold', color=H.C['ink'])
H.headline(fig, 'The counterfactual, not the method, decides the size of the feed', 'Every estimate against foreign peers is large and almost always positive; against each firm\'s own pre-control trend the same methods give small effects. Acceleration is not identified; insulation is.')
H.source(fig, 'Source: 112 specifications on the quarterly panel (NAURA, AMEC, ACM Research and their aggregate; 15 foreign donors; 2017Q1–2025Q4), varying estimator, counterfactual, seasonal adjustment and sample. Effects in percent of the counterfactual.')
H.save(fig, 'fig04_spec_curve', s)
