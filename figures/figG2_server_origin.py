"""Fig G2 — US imports of processing units (HS 847150) by origin: the AI-server boom went to Mexico and Taiwan."""
import housestyle as H, matplotlib.pyplot as plt, pandas as pd, numpy as np, os
H.setup(); D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data'); u = pd.read_csv(f'{D}/us_imports_847150_by_origin.csv', index_col=0); u.columns = u.columns.astype(int)
order = ['Mexico', 'Taiwan', 'Thailand', 'China', 'Other']; cols = {'Mexico': H.C['navy'], 'Taiwan': '#7A8CA8', 'Thailand': H.C['light'], 'China': H.C['red'], 'Other': '#CFD4DA'}; u.loc['Other'] = u.loc['World'] - u.loc[['Mexico', 'Taiwan', 'Thailand', 'China']].sum()
fig, ax = plt.subplots(figsize=(8.27, 3.9)); fig.subplots_adjust(top=0.72, bottom=0.16, left=0.08, right=0.86); H.ax_clean(ax); yrs = list(u.columns); x = np.arange(len(yrs)); bottom = np.zeros(len(yrs))
for o in order: ax.bar(x, u.loc[o].values, bottom=bottom, color=cols[o], width=0.6); bottom += u.loc[o].values
for i, y in enumerate(yrs): ax.text(i, bottom[i] + 3, f'{bottom[i]:.0f}', ha='center', fontsize=7, color=H.C['ink'])
for o, yy in [('Mexico', u.loc['Mexico', 2025] / 2), ('Taiwan', u.loc['Mexico', 2025] + u.loc['Taiwan', 2025] / 2), ('China', u.loc[['Mexico', 'Taiwan', 'Thailand'], 2025].sum() + 1)]: ax.text(len(yrs) - 0.62, yy, f"{o}  {u.loc[o, 2025]:.1f}", fontsize=6.8, va='center', color=H.C['ink'])
ax.set_xticks(x); ax.set_xticklabels(yrs, fontsize=7.5); ax.set_ylabel('US imports, USD bn', fontsize=7.5); ax.tick_params(axis='y', labelsize=7); ax.set_ylim(0, 185)
ax.text(0.02, 0.97, 'navy: Mexico   blue-grey: Taiwan   light: Thailand   red: China   grey: other', transform=ax.transAxes, fontsize=6.3, color=H.C['sub'], va='top')
H.headline(fig, 'The AI-server boom went to Mexico and Taiwan; China was never a large source', 'United States imports of processing units (HS 847150) rose from 31 to 165 billion dollars between 2019 and 2025. Imports of Chinese origin fell from 1.4 to 0.4 billion — a 4 percent share shrinking to 0.3 percent — while Mexico and Taiwan supplied the increase.')
H.source(fig, 'Source: UN Comtrade, United States as reporter, imports by partner, HS 847150 (processing units), annual; years shown: 2019, 2022, 2024, 2025. Other includes Malaysia and Viet Nam. Mexican and Taiwanese shipments are largely assembled by Taiwanese electronics manufacturing services firms.')
H.save(fig, 'figG2_server_origin', u.reset_index())
