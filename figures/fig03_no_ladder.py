"""Fig 3 — no clear ladder in trade: three sources × (US, allies), v2 baskets, placebo clouds + Romano–Wolf p."""
import housestyle as H, matplotlib.pyplot as plt, pandas as pd, numpy as np, os
H.setup(); D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data'); rng0 = np.random.default_rng(3)
SRC = [('BACI', 'china_exports_baskets_v2_baci.csv', 'BACI (reconciled)'), ('CN', 'china_exports_baskets_v2_comtrade.csv', "China's reported exports"), ('MIR', 'china_exports_baskets_v2_mirror.csv', "Importers' reported imports")]
G = ['WFE', 'SEMI', 'NETWORK', 'SERVER', 'CONSUMER']; L = ['tools', 'semi-\nconductors', 'network', 'servers', 'consumer']; ALLIES = [392, 410, 490, 528, 276, 826, 250, 380, 124, 36, 702]; PRE, POST = [2019, 2020, 2021], [2023, 2024]
RW = pd.read_csv(f'{D}/ladder_v2_three_sources_RW.csv').set_index(['source', 'basket'])
def gap(sub, dests):
    t = sub[sub.partner.isin(dests)].groupby('year').value_usd.sum().reindex(range(2019, 2025), fill_value=0); r = sub[~sub.partner.isin(dests)].groupby('year').value_usd.sum().reindex(range(2019, 2025), fill_value=0)
    return np.nan if t[POST].sum() <= 0 or t[PRE].sum() <= 0 else (np.log(t[POST].sum()) - np.log(t[PRE].sum())) - (np.log(r[POST].sum()) - np.log(r[PRE].sum()))
fig, axes = plt.subplots(2, 3, figsize=(8.27, 5.6), sharey='row'); fig.subplots_adjust(top=0.745, bottom=0.15, left=0.08, right=0.98, hspace=0.6, wspace=0.08); rows = []
for j, (key, fn, lab) in enumerate(SRC):
    df = pd.read_csv(f'{D}/{fn}'); df = df[df.partner != 0]; base = df[df.year.isin(PRE)].groupby('partner').value_usd.sum().sort_values(ascending=False); top40 = [p for p in base.index if p != 842][:40]; pool = [p for p in base.index[:70] if p != 842]
    rng = np.random.default_rng(7); draws = [list(rng.choice(pool, 11, replace=False)) for _ in range(100)]
    for i, (grp, dests, plac, ttl) in enumerate([('US', [842], [[d] for d in top40], 'to the United States'), ('Allies', ALLIES, draws, 'to eleven allies')]):
        ax = axes[i, j]; H.ax_clean(ax); ax.axhline(0, color='#444', lw=0.7)
        for k, g in enumerate(G):
            s = df[df.grp == g]; z = np.array([v for v in (gap(s, d) for d in plac) if pd.notna(v)]); a = gap(s, dests)
            ax.scatter(k + rng0.uniform(-0.22, 0.22, len(z)), z, s=7, color=H.C['grey'], alpha=0.5, lw=0, zorder=2); ax.scatter([k], [a], s=38, color=H.C['red'], zorder=4, edgecolor='white', lw=0.5)
            p = RW.loc[(key, g), 'allies_rw_p' if grp == 'Allies' else 'us_rw_p']; ax.text(k, -2.05, f'{p:.2f}', fontsize=6, color=H.C['ink'], ha='center', va='top'); rows.append({'source': key, 'group': grp, 'basket': g, 'actual_log': a, 'rw_p': p})
        ax.set_ylim(-2.3, 3.0); ax.set_xticks(range(5)); ax.set_xticklabels(L, fontsize=6.3); ax.set_xlim(-0.5, 4.5); ax.tick_params(axis='y', labelsize=6.8)
        if i == 0: ax.set_title(lab, loc='left', fontsize=8.4, weight='bold', color=H.C['ink'], pad=18); ax.text(0, 1.04, 'a. exports to the US, up to 40 placebo destinations', transform=ax.transAxes, fontsize=6.4, color=H.C['sub'])
        else: ax.text(0, 1.04, 'b. exports to eleven allies, 100 placebo alliances', transform=ax.transAxes, fontsize=6.4, color=H.C['sub'])
axes[0, 0].set_ylabel('Effect after Oct 2022, log points', fontsize=7); axes[1, 0].set_ylabel('Effect after Oct 2022, log points', fontsize=7)
H.headline(fig, 'No clear compliance ladder in bilateral trade — in any of three customs sources', "Red: actual effect on China's exports to the treated destinations relative to all others; grey: placebo destinations or random groups of eleven. Numbers below each basket: Romano–Wolf adjusted p. No basket is significant at 5 percent in any source.")
H.source(fig, 'Sources: BACI V202601; UN Comtrade (China as reporter; importing countries as reporters). Baskets v2 (Appendix A). Effect = change in log exports 2023–24 vs 2019–21 for the treated destination(s) minus the same change for all other destinations. One-sided (fall) randomization p-values with Romano–Wolf step-down across the five baskets. 7 of 2,100 placebo values lie beyond the axis range and are not shown.')
H.save(fig, 'fig03_no_ladder', pd.DataFrame(rows))
