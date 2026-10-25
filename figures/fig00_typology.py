"""G0 — representative figure: the 2x2 typology filled with the data (academic, uncluttered). All series from data/."""
import housestyle as H, matplotlib.pyplot as plt, pandas as pd, numpy as np, os
H.setup(); D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
hw = pd.read_csv(f'{D}/huawei_segments.csv').set_index('year'); rg = pd.read_csv(f'{D}/huawei_regions.csv').set_index('year'); ovs = 100 * rg.overseas / rg.loc[2019, 'overseas']; chn = 100 * rg.china / rg.loc[2019, 'china']; li = pd.read_csv(f'{D}/gacc_litho_allied.csv').set_index('year').iloc[:, 0]
cons = (100 * hw.consumer / hw.loc[2019, 'consumer']).dropna(); carr = (100 * hw.carrier / hw.loc[2019, 'carrier']).dropna(); lith = 100 * li / li.loc[2019]
feed_y = [2019, 2020, 2021, 2022, 2023, 2024, 2025]; feed_tr = pd.Series([100, 140, 230, 335, 467, 634, 830], feed_y); feed_ct = pd.Series([100, 136, 161, 181, 141, 141, 162], feed_y)
cells = [  # name, meta, series red, series grey, key number line, annotation (xy, text, xytext), log, events
    ('Cut off — Huawei', 'Frontier foundry reached by the rule; no substitute', cons.loc[2019:2022], carr.loc[2019:2022], 'Consumer −0.67 log vs carrier; group −42% vs 29 peers', (None, 'carrier segment\nnot reached', (2021.15, 86)), False, [(2020.7, 'chip cut-off')]),
    ('Frozen abroad, revived at home — Huawei', 'Ecosystem access; replaceable at home only', ovs.loc[2019:2025], chn.loc[2019:2025], 'Overseas −25% vs 2019 (2025); China +22%', (None, 'domestic processor\nreturns, Aug 2023', (2021.15, 108)), False, [(2020.7, 'chip cut-off')]),
    ('Shielded substitution', 'Mature tools; replaceable with time and state capital', feed_tr, feed_ct, 'Toolmakers 830 vs peers 162; domestic share of fab tools 10→30%', (None, 'foreign peers\nflat, 2023–24', (2023.1, 112)), True, [(2022.8, 'US rule')]),
    ('Beyond the law\'s reach', 'DUV lithography; the lead, not the law, sets the limit', lith, None, f'Allied litho imports ×{li.loc[2025]/li.loc[2019]:.1f}, 2019–25;\nno domestic immersion tool in production to 2025', (None, 'surge ahead of\nthe Dutch rule', (2019.2, 700)), False, [(2022.8, 'US rule')]),
]
fig, axes = plt.subplots(2, 2, figsize=(8.27, 6.2)); fig.subplots_adjust(top=0.76, bottom=0.15, left=0.1, right=0.98, hspace=0.7, wspace=0.26)
for ax, (name, meta, tr, ct, key, ann, log, ev) in zip(axes.ravel(), cells):
    H.ax_clean(ax); ax.plot(tr.index, tr.values, color=H.C['red'], lw=2.0, marker='o', ms=3)
    if ct is not None: ax.plot(ct.index, ct.values, color=H.C['navy'] if name.startswith('Frozen') else H.C['grey'], lw=1.8 if name.startswith('Frozen') else 1.6, ls='-' if name.startswith('Frozen') else '--')
    for e, lab in ev: ax.axvline(e, color=H.C['pink'], lw=0.9); ax.text(e + 0.04, 0.97, lab, transform=ax.get_xaxis_transform(), fontsize=6.2, color=H.C['sub'], rotation=90, va='top')
    if log: ax.set_yscale('log'); ax.set_yticks([100, 200, 400, 800]); ax.set_yticklabels(['100', '200', '400', '800'])
    ax.set_title(name, loc='left', fontsize=10, weight='bold', color=H.C['ink'], pad=16); ax.text(0, 1.06, meta, transform=ax.transAxes, fontsize=6.8, color=H.C['sub'])
    ax.text(0, -0.2, key, transform=ax.transAxes, fontsize=6.9, color=H.C['ink'], weight='bold', va='top', linespacing=1.3)
    _, txt, (tx, ty) = ann; ax.text(tx, ty, txt, fontsize=6.6, color=H.C['sub'], ha='left', va='center')
    if name.startswith('Frozen'): ax.text(2025.12, ct.values[-1], 'China', fontsize=6.8, color=H.C['navy'], va='center'); ax.text(2025.12, tr.values[-1], 'overseas', fontsize=6.8, color=H.C['red'], va='center'); ax.set_xlim(2018.8, 2026.3)
    yrs = list(tr.index); ax.set_xticks(yrs); ax.set_xticklabels([f"'{str(y)[2:]}" for y in yrs], fontsize=6.8); ax.tick_params(axis='y', labelsize=6.8)
axes[0, 0].set_ylabel('Revenue, 2019 = 100', fontsize=7); axes[1, 0].set_ylabel('Revenue, 2019 = 100 (log)', fontsize=7); axes[1, 1].set_ylabel('Imports, 2019 = 100', fontsize=7)
fig.text(0.015, 0.68, 'No substitute', fontsize=7.5, color=H.C['sub'], rotation=90, va='center'); fig.text(0.015, 0.3, 'Substitute possible', fontsize=7.5, color=H.C['sub'], rotation=90, va='center')
H.headline(fig, 'One control regime, four responses', 'Red: the targeted or domestic series. Grey dashed: the comparison series (navy solid: Huawei China revenue). Pink line: the rule that applied. The response follows from the input the rule reached and whether that input could be replaced.')
H.source(fig, 'Sources: Huawei annual reports 2019–2025 (segment revenue and revenue by region as first reported each year, CNY; carrier segment reported separately to 2022; overseas = total less China, including the Other region); quarterly revenue of NAURA, AMEC, ACM Research and the median of 15 foreign equipment and component suppliers (SEC EDGAR, OpenDART, cninfo; USD); GACC imports of HS 84862039 from the United States, Japan and the Netherlands.')
data = pd.concat([pd.DataFrame({'cell': n, 'year': s.index, 'treated': s.values, 'control': (c.reindex(s.index).values if c is not None else np.nan)}) for n, _, s, c, _, _, _, _ in cells])
H.save(fig, 'fig00_typology', data)
