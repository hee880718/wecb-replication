"""Appendix Fig A7 — origin is not nationality: China's dry-etch imports by origin, 2019–2026."""
import housestyle as H, matplotlib.pyplot as plt, pandas as pd, os
H.setup(); D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data'); sh = pd.read_csv(f'{D}/etch_imports_origin_share.csv', index_col=0); usd = pd.read_csv(f'{D}/etch_imports_origin_usd_bn.csv', index_col=0)
order = ['US', 'SG+MY', 'JP', 'KR', 'Other']; cols = {'US': H.C['red'], 'SG+MY': H.C['pink'], 'JP': H.C['navy'], 'KR': '#7A8CA8', 'Other': H.C['light']}
fig, ax = plt.subplots(1, 2, figsize=(8.27, 3.8)); fig.subplots_adjust(top=0.70, bottom=0.18, left=0.08, right=0.98, wspace=0.3)
a = ax[0]; H.ax_clean(a); bottom = pd.Series(0.0, index=sh.index)
for o in order: a.bar(sh.index, sh[o], bottom=bottom, color=cols[o], width=0.7, label=o); bottom += sh[o]
a.text(0.02, 0.97, 'red: United States   pink: Singapore + Malaysia   navy: Japan   light: Korea, other', transform=a.transAxes, fontsize=6.0, color=H.C['sub'], va='top')
a.set_xlim(2018.3, 2026.8); a.set_ylim(0, 108); a.set_ylabel('Share of China\'s dry-etch tool imports, %', fontsize=7); a.set_xticks(range(2019, 2027)); a.set_xticklabels([f"'{str(y)[2:]}" + ('\n(Jan–Aug)' if y == 2026 else '') for y in range(2019, 2027)], fontsize=6.5); a.tick_params(axis='y', labelsize=7); a.axvline(2022.8, color='#444', lw=0.8, ls=':')
a.set_title('a. Shares by origin', loc='left', fontsize=8.6, weight='bold', color=H.C['ink'])
b = ax[1]; H.ax_clean(b)
for o in ['US', 'SG+MY', 'JP']: b.plot(usd.index, usd[o], color=cols[o] if o != 'SG+MY' else '#C9736A', lw=1.9, marker='o', ms=3); b.text(usd.index[-1] + 0.15, usd[o].iloc[-1], {'US': 'United States', 'SG+MY': 'Singapore +\nMalaysia', 'JP': 'Japan'}[o], fontsize=6.3, va='center', color=H.C['ink'])
b.axvline(2022.8, color='#444', lw=0.8, ls=':'); b.text(2022.9, 0.97, 'US rule', transform=b.get_xaxis_transform(), fontsize=6.2, color=H.C['sub'], rotation=90, va='top'); b.set_xlim(2018.8, 2028.3); b.set_ylabel('Imports, USD bn', fontsize=7); b.set_xticks(range(2019, 2027)); b.set_xticklabels([f"'{str(y)[2:]}" + ('\n(Jan–Aug)' if y == 2026 else '') for y in range(2019, 2027)], fontsize=6.5); b.tick_params(axis='y', labelsize=7)
b.set_title('b. Values by origin', loc='left', fontsize=8.6, weight='bold', color=H.C['ink'])
H.headline(fig, 'Origin is not nationality: the same American toolmakers, shipped from Asia', "China's imports of dry-etch tools of United States origin fell from 43 percent of the total in 2019 to 5 percent in 2025, while imports from the same firms' Singapore and Malaysian plants rose from 13 to 43 percent; the origin of a shipment says little about who made it.")
H.source(fig, 'Source: GACC HS 84862041 (dry plasma etch) imports by country of origin, annual sums; 2026 is January–August. US, Singapore + Malaysia, Japan and Korea shown; other origins in grey. Customs record the country of origin, not the shipper; the main etch plants in Singapore and Malaysia belong to Applied Materials and Lam Research.')
H.save(fig, 'figA7_origin', sh.reset_index())
