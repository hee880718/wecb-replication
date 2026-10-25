"""Fig G1 — the policy timeline: decrees by jurisdiction, 2018–2025."""
import housestyle as H, matplotlib.pyplot as plt, pandas as pd
H.setup()
ev = pd.DataFrame([('2018-04', 'US', 'ZTE denial order'), ('2018-07', 'US', 'ZTE denial lifted'), ('2019-05', 'US', 'Huawei on Entity List'), ('2020-05', 'US', 'FDPR: Huawei designs'), ('2020-08', 'US', 'FDPR: all Huawei chips'), ('2020-12', 'US', 'SMIC on Entity List'), ('2022-10', 'US', 'Oct-2022 rule'), ('2022-12', 'US', 'YMTC on Entity List'), ('2023-07', 'JP', 'Japan: 23 tool categories'), ('2023-09', 'NL', 'Netherlands: DUV immersion'), ('2023-10', 'US', 'Rule update'), ('2024-09', 'NL', 'Netherlands: 1970i/1980i'), ('2024-12', 'US', 'Dec-2024 rule'), ('2025-01', 'US', 'AI diffusion rule'), ('2025-05', 'US', 'AI rule rescinded'), ('2025-08', 'US', 'VEU revocation\n(in force Dec 2025)')], columns=['date', 'jur', 'label'])
ev['x'] = ev.date.str[:4].astype(int) + (ev.date.str[5:7].astype(int) - 1) / 12; rows = {'US': 2.4, 'JP': 1, 'NL': 0}; col = {'US': H.C['red'], 'JP': H.C['navy'], 'NL': '#7A8CA8'}
fig, ax = plt.subplots(figsize=(8.27, 3.4)); fig.subplots_adjust(top=0.74, bottom=0.14, left=0.08, right=0.98); ax.tick_params(length=0); ax.set_axisbelow(True)
for j, y in rows.items(): ax.axhline(y, color=H.C['light'], lw=0.8); ax.text(2017.75, y, {'US': 'United States', 'JP': 'Japan', 'NL': 'Netherlands'}[j], fontsize=7.5, ha='right', va='center', color=H.C['ink'])
flip = {'US': [1, -1, 2, -2] * 4, 'JP': [1], 'NL': [1, -1]}; cnt = {k: 0 for k in rows}
for _, r in ev.iterrows():
    y = rows[r.jur]; f = flip[r.jur][cnt[r.jur] % len(flip[r.jur])]; cnt[r.jur] += 1; ax.scatter(r.x, y, s=30, color=col[r.jur], zorder=3); off = 0.18 * f; ax.plot([r.x, r.x], [y, y + off], color=H.C['light'], lw=0.6, zorder=1); ax.text(r.x + (0.06 if 'VEU' in r.label else 0), y + off + (0.03 if f > 0 else -0.03) - (0.16 if 'VEU' in r.label else 0), r.label, fontsize=5.8, ha='left' if 'VEU' in r.label else 'center', va='bottom' if f > 0 else 'top', color=H.C['ink'])
ax.set_ylim(-0.75, 3.35); ax.set_xlim(2017.6, 2027.0); ax.set_yticks([]); ax.set_xticks(range(2018, 2027)); ax.set_xticklabels(range(2018, 2027), fontsize=7.5)
for s in ('left', 'top', 'right'): ax.spines[s].set_visible(False)
H.headline(fig, 'The rules, 2018–2025', 'Red: United States; navy: Japan; blue-grey: Netherlands. Each point is the date the measure took effect, as used for treatment timing in the paper, except the VEU revocation (announced August 2025, in force 31 December 2025); publication references are in Appendix A.')
H.source(fig, 'Sources: Federal Register; METI; Staatscourant; Entity List. The paper treats October 2022 as the first wave and December 2024 as the second; Japanese and Dutch controls took effect in July and September 2023.')
H.save(fig, 'figG1_timeline', ev)
