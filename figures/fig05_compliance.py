"""Fig 5 — compliance signature: small multiples of China revenue share, controlled vs uncontrolled vendors."""
import housestyle as H, matplotlib.pyplot as plt, pandas as pd, os
H.setup(); D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
us = pd.read_csv(f'{D}/us_china_share.csv'); us['d'] = pd.to_datetime(us.report_date); us = us[us.form == '10-Q']; jp = pd.read_csv(f'{D}/japan_china_share.csv')
panels = [('AMAT', 'US · etch, deposition', 'q', True), ('KLAC', 'US · inspection', 'q', True), ('TEL', 'Japan · front-end', 'a', True), ('SCREEN', 'Japan · cleaning', 'a', True), ('DISCO', 'Japan · dicing', 'a', False), ('ULVAC', 'Japan · sputtering', 'a', False)]
fig, axes = plt.subplots(2, 3, figsize=(8.27, 5.2), sharey=True); fig.subplots_adjust(top=0.70, bottom=0.14, left=0.08, right=0.98, hspace=0.6, wspace=0.12)
for ax, (f, lab, kind, ctrl) in zip(axes.ravel(), panels):
    H.ax_clean(ax); col = H.C['red'] if ctrl else H.C['grey']
    if kind == 'q': s = us[(us.firm == f) & (us.d >= '2017-01-01')].sort_values('d'); ax.plot(s.d.dt.year + (s.d.dt.month - 1) / 12, 100 * s.share, color=col, lw=1.7, marker='.', ms=3)
    else: s = jp[jp.firm == f].sort_values('fy'); ax.plot(s.fy - 0.25, 100 * s.share, color=col, lw=1.7, marker='o', ms=3.2); ax.axvline(2023.55, color=H.C['navy'], lw=0.8, ls='--')
    for e in (2022.8, 2024.9): ax.axvline(e, color=H.C['pink'], lw=0.9)
    ax.set_xlim(2016.8, 2026.8); ax.set_ylim(0, 52); ax.set_title(f"{f.replace('KLAC', 'KLA')}\n{lab}" + ('' if ctrl else ' · largely unlisted'), loc='left', fontsize=8, weight='bold', color=H.C['ink'] if ctrl else H.C['sub']); ax.set_xticks([2018, 2020, 2022, 2024, 2026]); ax.set_xticklabels(["'18", "'20", "'22", "'24", "'26"], fontsize=7); ax.tick_params(axis='y', labelsize=7)
axes[0, 0].set_ylabel('China share of revenue, %', fontsize=7.5); axes[1, 0].set_ylabel('China share of revenue, %', fontsize=7.5)
axes[0, 0].text(2022.9, 49, 'US Oct-22', fontsize=6, color=H.C['sub']); axes[0, 0].text(2025.0, 49, 'US Dec-24', fontsize=6, color=H.C['sub']); axes[0, 2].text(2023.65, 3, 'Japan Jul-23', fontsize=6, color=H.C['navy'], rotation=90, va='bottom')
H.headline(fig, 'The rule is visible in the books of the vendors it named', 'Toolmakers whose products were listed show the same cycle after 2022 — drop, overshoot, normalization — on both sides of the Pacific. Two Japanese toolmakers whose main products (dicing saws; general-purpose sputtering) fall largely outside the listed categories do not. The level of the controlled vendors\' China share did not fall; its volatility rose (rank 1 of 21 assignments).')
H.source(fig, 'Sources: SEC 10-Q geographic revenue by customer location (AMAT, KLA; quarterly, plotted at quarter end; fiscal fourth quarters are reported only in the 10-K and are not plotted); EDINET annual securities reports, revenue by region (TEL, SCREEN, DISCO, ULVAC; fiscal years ending March, each plotted at the fiscal mid-year, i.e. October of the preceding calendar year). Pink: US rules of October 2022 and December 2024; dashed navy: Japan\'s controls in force July 2023.')
H.save(fig, 'fig05_compliance', pd.concat([us[['firm', 'report_date', 'share']].rename(columns={'report_date': 'period'}), jp.rename(columns={'fy': 'period'})]))
