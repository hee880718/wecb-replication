"""Appendix Fig A3 — feed estimates by estimator and counterfactual; second-wave gap paths. Values from the canonical registry (F8, F13, W2a)."""
import housestyle as H, matplotlib.pyplot as plt, pandas as pd, numpy as np
H.setup()
est = pd.DataFrame([('NAURA', 0.96, 0.66, 0.27), ('AMEC', 0.80, 0.78, 0.11), ('ACM Research', 0.94, 0.41, -0.23), ('Three-firm aggregate', 0.85, 0.49, -0.03)], columns=['unit', 'sdid_peers', 'ascm_peers', 'ascm_own'])   # clean run 2026-10-25 (spec_curve_rerun.py)
wave = pd.DataFrame([('Three-firm aggregate', 0.28, 0.46, 0.71), ('NAURA', 0.52, 0.64, 0.94), ('AMEC', 0.50, 0.77, 1.20), ('ACM Research', 0.25, 0.48, 0.58)], columns=['unit', 'y2023', 'y2024', 'y2025'])
fig, ax = plt.subplots(1, 2, figsize=(8.27, 3.8)); fig.subplots_adjust(top=0.71, bottom=0.17, left=0.19, right=0.9, wspace=0.55)
a = ax[0]; H.ax_clean(a, grid='x'); ys = np.arange(len(est))[::-1]
for y, (_, r) in zip(ys, est.iterrows()):
    a.plot([r.ascm_own, r.ascm_peers], [y, y], color=H.C['light'], lw=3, zorder=1) if pd.notna(r.ascm_own) else None
    a.scatter(r.sdid_peers, y + 0.18, color=H.C['grey'], s=36, zorder=3); a.scatter(r.ascm_peers, y, color=H.C['red'], s=36, zorder=3)
    if pd.notna(r.ascm_own): a.scatter(r.ascm_own, y - 0.18, color=H.C['navy'], s=36, zorder=3)
a.axvline(0, color='#444', lw=0.7); a.set_yticks(ys); a.set_yticklabels(est.unit, fontsize=7.2); a.set_xlim(-0.5, 1.1); a.set_xlabel('Effect on quarterly revenue, log points', fontsize=7); a.tick_params(axis='x', labelsize=7)
a.text(0, 1.03, 'grey: SDID vs peers · red: augmented SC vs peers\nnavy: augmented SC vs own trend', transform=a.transAxes, fontsize=5.9, color=H.C['sub'])
a.set_title('a. Two counterfactuals, three estimators', loc='left', fontsize=8.6, weight='bold', color=H.C['ink'], pad=14)
b = ax[1]; H.ax_clean(b)
for _, r in wave.iterrows():
    col = H.C['red'] if r.unit in ('NAURA', 'AMEC') else H.C['grey']; b.plot([2023, 2024, 2025], [r.y2023, r.y2024, r.y2025], marker='o', ms=3.4, lw=1.7, color=col); b.text(2025.08, r.y2025, r.unit, fontsize=6.4, va='center', color=H.C['ink'])
b.axvline(2024.92, color=H.C['pink'], lw=0.9); b.text(2024.88, 0.03, 'Dec-2024\ndesignation', transform=b.get_xaxis_transform(), fontsize=6.0, color=H.C['sub'], ha='right', va='bottom')
b.set_xlim(2022.8, 2026.4); b.set_xticks([2023, 2024, 2025]); b.set_xticklabels(["'23", "'24", "'25"], fontsize=7); b.set_ylim(0, 1.35); b.set_ylabel('Gap vs foreign-peer synthetic control, log points', fontsize=7); b.tick_params(axis='y', labelsize=7)
b.set_title('b. Gap over peers, by year', loc='left', fontsize=8.6, weight='bold', color=H.C['ink'], pad=14)
H.headline(fig, 'The counterfactual decides the size of the feed; the list did not change it', 'Left: large against foreign peers under either estimator, small against each firm\'s own pre-2022 trend. Right: the gap over peers rose further in 2025, after the December 2024 designations (aggregate +0.24, rank 2 of 16; AMEC +0.42, rank 1 of 16).')
H.source(fig, 'Source: seasonally adjusted quarterly revenue panel, 2017Q1–2025Q4, 15 foreign donors; placebo ranks in Appendix B. Values from the clean re-run of 25 October 2026 (spec_curve_rerun.py; yearly gaps from the quarterly gap paths of Appendix Figure A2).')
H.save(fig, 'figA3_estimators', pd.concat([est.assign(table='estimators'), wave.assign(table='second_wave')]))
