"""Appendix Fig A6 — lifted: ZTE's consumer and carrier segments after the 2018 denial order and settlement."""
import housestyle as H, matplotlib.pyplot as plt, pandas as pd, numpy as np, os
H.setup(); D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data'); d = pd.read_csv(f'{D}/telecom_device_panel_logUSD_v2.csv', index_col=0); yrs = [int(c) for c in d.columns]
cons = np.exp(d.loc['TR:ZTE_consumer'].values) / 1000; carr = np.exp(d.loc['TR:ZTE_carrier'].values) / 1000   # USD bn
fig, ax = plt.subplots(1, 2, figsize=(8.27, 3.8)); fig.subplots_adjust(top=0.72, bottom=0.18, left=0.08, right=0.98, wspace=0.35)
a = ax[0]; H.ax_clean(a); a.plot(yrs, carr, color=H.C['navy'], lw=1.9, marker='o', ms=3); a.plot(yrs, cons, color=H.C['red'], lw=1.9, marker='o', ms=3)
a.axvspan(2018.25, 2018.55, color=H.C['pink'], alpha=0.5, lw=0); a.text(2018.4, 0.97, 'denial order → settlement', transform=a.get_xaxis_transform(), fontsize=6.2, color=H.C['sub'], rotation=90, va='top', ha='right')
a.text(yrs[-1] + 0.15, carr[-1], 'carrier networks', fontsize=6.8, color=H.C['navy'], va='center'); a.text(yrs[-1] + 0.15, cons[-1], 'consumer (handsets)', fontsize=6.8, color=H.C['red'], va='center')
a.set_xlim(2014.6, 2028.6); a.set_ylabel('Segment revenue, USD bn', fontsize=7); a.set_xticks(range(2015, 2026, 2)); a.set_xticklabels([f"'{str(y)[2:]}" for y in range(2015, 2026, 2)], fontsize=7); a.tick_params(axis='y', labelsize=7); a.set_ylim(0, 13)
a.set_title('a. Revenue by segment', loc='left', fontsize=8.6, weight='bold', color=H.C['ink'])
b = ax[1]; H.ax_clean(b, grid='x'); eff = [('Consumer (handsets)', -47, '1 of 30', H.C['red']), ('Carrier networks', 1, '16 of 30', H.C['navy'])]
for i, (nm, v, rk, c) in enumerate(eff[::-1]): b.barh(i, v, color=c, height=0.5); b.text(4, i, f'{v:+d}%   rank {rk}', va='center', ha='left', fontsize=7, color=H.C['ink'])
b.axvline(0, color='#444', lw=0.7); b.set_yticks([0, 1]); b.set_yticklabels([e[0] for e in eff[::-1]], fontsize=7); b.set_xlim(-70, 45); b.set_xlabel('Synthetic DiD effect vs 29 peers, 2019–23, %\n(rank among 30 placebo paths)', fontsize=7); b.tick_params(axis='x', labelsize=7)
b.set_title('b. Effect against peers, by segment', loc='left', fontsize=8.6, weight='bold', color=H.C['ink'])
H.headline(fig, 'Lifted: the carrier business came back, the handset business did not', "ZTE's access was cut in April 2018 and restored in July. Carrier revenue recovered fully against peers; handset revenue fell by nearly half against peers and in level regained only nine-tenths of its 2017 size by 2025. Customers who could switch did not switch back.")
H.source(fig, 'Sources: ZTE annual reports (segment revenue, CNY converted at annual average rates; panel telecom_device_panel_logUSD_v2); effects from the clean run of 9 October 2026 (synthetic difference-in-differences against 29 listed peers with complete 2015–2023 data, pre-period 2015–17, post-period 2019–23; rank among the 30 placebo paths).')
H.save(fig, 'figA6_lifted', pd.DataFrame({'year': yrs, 'consumer_usd_bn': cons, 'carrier_usd_bn': carr}))
print("consumer 2017→2019→2025:", round(cons[2], 2), round(cons[4], 2), round(cons[-1], 2), "· carrier:", round(carr[2], 2), round(carr[4], 2), round(carr[-1], 2))
