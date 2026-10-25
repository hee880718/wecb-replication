"""Appendix Fig A4 — who paid: the memory makers' revenue, profit and state-linked shareholders (prospectuses)."""
import housestyle as H, matplotlib.pyplot as plt, pandas as pd, numpy as np
H.setup()
rev = pd.DataFrame({'year': ['2023', '2024', '2025', '1Q 2026'], 'YMTC': [18.74, 45.20, 63.18, 47.04], 'CXMT': [9.09, 24.18, 61.80, 50.80]})   # registry G3/Q6 (prospectus values in ¥100m, converted to CNY bn)
ni_cxmt = {'2023': -16.3, '1Q 2026': 24.8}; roe_ymtc = {'2023': -27.7, '2024': 8.2, '2025': 15.1, '1Q 2026': 28.0}
own = pd.DataFrame({'holder': ['Hubei Changsheng (Hubei state)', 'Xinfei Technology', 'National IC Fund I', 'National IC Fund II', 'Optics Valley Industrial Investment', 'Hubei Guoxin fund'], 'YMTC': [26.54, 25.35, 11.97, 11.38, 9.25, 5.90]})
own_c = pd.DataFrame({'holder': ['Qinghui Jidian (Hefei state)', 'Changxin Jicheng (Hefei state)', 'National IC Fund II', 'Hefei Jixin', 'Anhui Provincial Investment'], 'CXMT': [21.67, 11.71, 8.73, 8.37, 7.91]})
fig, ax = plt.subplots(1, 2, figsize=(8.27, 4.6), gridspec_kw={'width_ratios': [1, 1.15]}); fig.subplots_adjust(top=0.74, bottom=0.26, left=0.08, right=0.98, wspace=0.62)
a = ax[0]; H.ax_clean(a); x = np.arange(4); w = 0.36
a.bar(x - w/2, rev.YMTC, w, color=H.C['red']); a.bar(x + w/2, rev.CXMT, w, color=H.C['navy'])
for i, (y, c) in enumerate(zip(rev.YMTC, rev.CXMT)): a.text(i - w/2, y + 1, f'{y:.1f}', ha='center', fontsize=6.2, color=H.C['red']); a.text(i + w/2, c + 1, f'{c:.1f}', ha='center', fontsize=6.2, color=H.C['navy'])
a.set_xticks(x); a.set_xticklabels(rev.year, fontsize=7); a.set_ylabel('Revenue, CNY bn (1Q 2026 = quarter only)', fontsize=7); a.tick_params(axis='y', labelsize=7); a.set_ylim(0, 72)
a.text(0.02, 0.97, 'red: YMTC   navy: CXMT', transform=a.transAxes, fontsize=6.4, color=H.C['sub'], va='top')
a.text(0.0, -0.2, 'Attributable net income, CNY bn (2023 → 2024 → 2025 → 1Q 2026):\nYMTC  −19.2 → +6.8 → +14.2 → +33.4\nCXMT  −16.3 → −7.1 → +1.9 → +24.8\nYMTC weighted ROE −27.7% → 8.2% → 15.1% → 28.0%', transform=a.transAxes, fontsize=6.4, color=H.C['ink'], va='top', linespacing=1.5)
a.set_title('a. Revenue and profitability, 2023–1Q 2026', loc='left', fontsize=8.2, weight='bold', color=H.C['ink'])
b = ax[1]; H.ax_clean(b, grid='x'); hold = ['— YMTC —'] + list(own.holder) + ['— CXMT —'] + list(own_c.holder); vals = [np.nan] + list(own.YMTC) + [np.nan] + list(own_c.CXMT); cols = ['white'] + [H.C['red']] * len(own) + ['white'] + [H.C['navy']] * len(own_c)
ys = np.arange(len(hold))[::-1]; b.barh(ys, [v if pd.notna(v) else 0 for v in vals], color=cols, height=0.62)
for y, v in zip(ys, vals):
    if pd.notna(v): b.text(v + 0.6, y, f'{v:.1f}%', va='center', fontsize=6.4, color=H.C['ink'])
b.set_yticks(ys); b.set_yticklabels(hold, fontsize=6.4); b.set_xlim(0, 34); b.set_xlabel('Share of pre-listing equity, %', fontsize=7); b.tick_params(axis='x', labelsize=7)
b.set_title('b. State-linked shareholders', loc='left', fontsize=8.2, weight='bold', color=H.C['ink']); b.text(0.0, -0.2, 'YMTC: top four holders 75.2%, all state capital or national funds.\nCXMT: state-owned holders ≈ 54% (Hefei state capital ≈ 37%).', transform=b.transAxes, fontsize=6.4, color=H.C['ink'], va='top')
H.headline(fig, 'Who paid for the insulation: the memory makers and their shareholders', 'Both memory makers grew several-fold from 2023 to 2025 through designation (YMTC, 3.4×) and non-designation (CXMT, 6.8×) alike. Their losses in 2023 were carried by national and provincial funds that hold the majority of their equity; profitability arrived with the 2024–25 memory upcycle.')
H.source(fig, 'Sources: YMTC (Changcun Holdings) and CXMT (Changxin Technology) STAR Market prospectuses and sponsor letters, 2026; shareholdings from the pre-IPO tables (YMTC filing of 21 August 2026; CXMT prospectus of 27 May 2026, state-owned holders ≈ 54% in total). Revenue in CNY bn; 1Q 2026 is a single quarter.')
H.save(fig, 'figA4_memory_state', pd.concat([rev.melt(id_vars='year', var_name='firm', value_name='revenue_cny_bn'), own.rename(columns={'YMTC': 'share_pct'}).assign(firm='YMTC'), own_c.rename(columns={'CXMT': 'share_pct'}).assign(firm='CXMT')]))
