# Page-by-page audit of WP v7 (2026-10-09)
V = verified against original source this session or in AUD1–3 and reproduced from data in figures_v2/data; R = registry value from an earlier session (reproducible from the replication package, not re-run today); F = fixed today (old value retired); C = check before SSRN.

## Abstract / §1
| Claim | Status |
|---|---|
| −39% vs peers (1/34, p=.029) | R (K1v2) |
| consumer −0.67 log vs carrier | V (Huawei AR 2019–22) |
| 30–40%/yr growth; own trend not exceeded; 830 vs 162 vs 1,293 | V (fig02 data) |
| lithography ×5; allied-origin ×9.2; domestic 0 | V (GACC) |
| faint, source-dependent trade trace; RW min .34 (US) / .07 (allies) | V (ladder_v2_three_sources_RW) |
| compliance cycle 1/21 p=.048 | V (figA2 data) |
| designation −0.09 n.s. | R (CS1) |
| Fisher .004/.031 | R (J1v2) |
| etch origin US 43→5%, SG+MY 13→43% | F (was 29→5 / 12→31) |

## §2 Theory, data, design
| Claim | Status |
|---|---|
| source counts (63/36/19/9/47+7) | R |
| ASML ratio 0.86–1.01 (7 yrs) | R — C: the only file in container (asml_china_20F.csv) is a broken parse; re-derive from ASML ARs before SSRN |
| corr 0.92 vs 0.38 | R — C: recompute with current GACC file |
| p floors 1/34, 1/16 | V |
| GACC file = imports only, monthly not cumulative, 2024 total $35.1bn | V (checked today) |

## §3 Four responses
| Claim | Status |
|---|---|
| overseas 352→224→265 bn CNY; China 507→413→616 | F/V (was 98/64/74 B$) |
| consumer 467→243→214→344; carrier 297→281→284 | V |
| TSMC China −30% (2021), share 19→10% | R (20-F verified earlier; file not in container) |
| ZTE −59% 2Q18; handset −52% (1/30); carrier +2% (16/30); level 2.2→4.7 B$ | R + V (Z1) |
| litho ×5.0 total, NL ×11.6; NL unit value 20→37→51 M$ | F/V (was 17→47) |
| last-train +103% (NL), +36% (JP); monthly 0.1–0.2→1.32 B$ | R (AUD2) — C: recheck with monthly file (2023-09 = 1.30 B$ confirms the 1.3 peak) |
| domestic share 10.2→29.7% | V |
| YMTC NAND 141→567; CXMT 91→618 | V (prospectus) |

## §4 Feed
| Claim | Status |
|---|---|
| +0.73 (1/16), +0.78; own +0.23, +0.16 (5–6/16) | R (F8, F13) |
| spec curve 98%/75%, +122/+11 | V (fig04 data) |
| growth change −7/+3/−18 vs −56/−117/−11 | V (fig02 data; Changchuan one year) |
| dynamics +0.40/+0.58/+0.91 (annual) | R; quarterly end-values differ (A5) — stated |
| second wave +0.24 (2/16), AMEC +0.42 (1/16) | R (W2a) |
| CXMT 26.99/15.24; YMTC 28.56/12.88/12.24/9.96/9.25; ROE path; R&D ratio | V (prospectus) — C: CXMT table membership |

## §5 Firms not flows
| Claim | Status |
|---|---|
| three-source ladder, RW-adjusted | V |
| server mirror gap 1.11/1.16 vs 1.37/0.56; US imports Mexico 25→81, Taiwan 3→70 | V |
| HS8 shape tests p .63/.30/.94; litho allied 1.1→10.0 | V |
| AMAT quarterly 34→17→45→27 (2022–26); TEL FY23–26 24/44/42/34; SCREEN 20/39/42/38 | F/V (sequences realigned to full fiscal years) |
| level +3.2 (p=.43) [F: was +4.6/.24, loose windows]; volatility +7.2 (1/21); normalization −5.8 (3/21) | V |
| 10-K mentions 0→1–3.6; slope −0.80 (p=.31) | R |
| Dec-24 origin shifts US −29%, JP −10%, SG+MY +41%; NL −32% (2026 ann.) | R (W2b) — C: 2026 now Jan–Aug; recompute |
| Hubei −66% vs 0; rank 2→15 | R |
| CS DiD −0.09 [−0.33, +0.22]; cohorts | R (CS1) |

## Figures (15)
All drawn from figures_v2/data CSVs or registry rows cited in the script header; PDF+PNG+CSV present. C: G1 timeline dates vs Appendix A gazette citations; A4 CXMT holders table.

## Open C-items before SSRN v1
1. ASML ratio and 0.92/0.38 correlation — re-derive from current files.
2. 2026 annualized NL figure (−32%) — recompute as Jan–Aug.
3. G1 dates ↔ gazette citations.
4. CXMT shareholder table membership.
5. Fiscal-year footnote in §5.3.
6. [verify] ×4 citations.


## Second pass (2026-10-09, automated recomputation)
Recomputed from figures_v2/data: Huawei regions/segments, within-firm DiD, feed index and growth, spec-curve shares and medians, compliance three statistics, TEL/SCREEN/AMAT sequences, RW minima, server origin table, etch origin shares, domestic share, allied litho multiple. Discrepancies found and fixed: compliance level DiD (+4.6→+3.2, p .24→.43), TEL/SCREEN sequence selection, AMAT period wording. Items requiring a clean run of the replication package before SSRN: K1v2, K2v2, J1v2, F8, F13, W2a, CS1, 10-K exposure, Hubei plant, TSMC, last-train, ASML ratio, 0.92/0.38 correlation, YMTC NAND segment.

## Third pass — clean run (2026-10-09)
Re-run with sdid2.sdid on the panels in the replication package:
- Huawei group SDID: −0.54 log (−42%), rank 1/30, p=.033 (29 complete donors; earlier −39%/1/34 on a 33-donor panel superseded) → text, abstract, Figure 1 key line updated.
- ZTE consumer −47% (1/30), carrier +1% (16/30) (earlier −52%/+2% superseded) → §3.3, Appendix Figure A6 updated.
- Quarterly SA SDID (15 donors): aggregate +0.84, NAURA +0.96, AMEC +0.80, ACMR +0.94, all rank 1/16 → Appendix B table, Appendix Figure A3 updated.
- Fisher with floors (.033, .033, .063): p=.004 → §3.6 updated.
- Verified unchanged: exposure slope −0.80; CS ATT ≈ −0.09; monthly NL peak 1.3 bn.
Still flagged: conformal inference (removed from text pending re-run); instruments appendix (sign conflict with archived product regression; marked under re-verification); last-train magnitude stated as levels; [verify] citations ×8.
