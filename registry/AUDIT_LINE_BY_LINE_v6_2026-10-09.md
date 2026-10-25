# Line-by-line audit of WP v6 — numbers, methods, figures (2026-10-09)
Status codes: **OK** = recomputed/verified against source this round or in AUD1–3; **CHK** = consistent with registry but source re-read recommended before SSRN; **FIX** = must change.

## A. Numbers in the text
| § | Claim | Registry | Source | Method | Status / action |
|---|---|---|---|---|---|
| 1,3.1 | Huawei group −39% (1/34, p=.029); 2021–23 −41% | K1v2 | 36 peers, EDGAR/ARs | SDID, placebo rank | OK. Note p is one-sided rank; state "rank p" explicitly in text |
| 3.1 | consumer −0.73, carrier −0.06, enterprise +0.21; DiD −0.67 | D1 | Huawei AR 2019–22 | within-firm log diff | OK (verified this session) |
| 3.1 | overseas 98→64 B$; consumer 136→70 | K1v2 | Huawei AR, CNY→USD | annual avg FX | CHK: confirm FX rates used (6.91/6.45) and that "consumer 136" is USD not CNY |
| 3.1 | TSMC China −30% (2021), share 19→10% | verified 20-F | TSMC 20-F | arithmetic | OK |
| 3.2 | overseas 74 B$ (2025); China 136→165 | K1v2 | Huawei AR 2025 | FX | CHK FX 2025 |
| 3.2 | consumer 214→344 bn CNY (+61%, −26% vs 2019) | K4 | Huawei AR 2023/2025 | arithmetic | OK |
| 3.3 | ZTE 2Q18 −59%; handsets −52% (1/30); carrier +2% (16/30) | K2v2 | ZTE reports, 30 peers | SDID placebo | OK; two-sidedness note |
| 3.4 | DUV imports ×5 (2019→2024); ASP 17→47 M$; EUV absent | F-series | GACC HS8 litho | sums, unit values | CHK: recompute ×5 with final HS8 file (84862039 NL origin 2019 1.08 → 2024 9.53 ≈ ×8.8 for allied; "fivefold" refers to total litho imports — confirm which basket) **FIX wording to match basket** |
| 3.4 | last-train +103% (NL), +36% (JP); monthly 0.1–0.2 → 1.32 B$ | U-series | GACC monthly | pre-effect window | OK (AUD2) |
| 3.5 | domestic WFE share 10→30%; litho 0 | F1b | cninfo + GACC | share | CHK Piotech 2022 inclusion break (~1.4pp) — caption |
| 3.5 | YMTC NAND 141→567; CXMT 91→618 | verified | prospectuses | — | OK |
| 3.6 | Fisher .004/.031; conservative .012/.054 | J1v2 | — | Fisher, ρ=.4 | OK; add note that ρ=.4 is assumed, not estimated |
| 4.1 | index 830 / 1,293 / 162; growth 40–69 → 31–39%; peers 0% | F2a | quarterly_panel_v5 | sums, log-linear fit | OK (this session) |
| 4.1 | NAURA +0.73 (1/16), AMEC +0.78; own-trend +0.23, +0.16 | F8/F13 | 15 donors | ASCM ridge | OK; **FIX**: body says "fifth or sixth of sixteen" — registry F13 says NAURA 5/16, AMEC 6/16: consistent |
| 4.1 | spec curve 98%/75%, medians +122/+11 | F9 | 112 specs | — | OK |
| 4.1 | Honest DiD M̄≈0; AMEC .4–.8 | methods audit | — | Rambachan–Roth | CHK: re-run with final panel v5 (was run on v3?) |
| 4.2 | growth change −7/+3/−18 vs −56/−117/−11 | session | annual reports | mean growth diff | CHK: Changchuan uses one year only; say so (done). AMEC "−3 (a slight rise)": sign convention must be unambiguous → **FIX** wording ("growth rose 3 points") |
| 4.2 | NAURA dynamics +0.40/+0.58/+0.91 | registry | — | ASCM by year | OK |
| 4.3 | second wave +0.46→+0.71 (Δ+0.24, 2/16); AMEC +0.77→+1.20 (1/16) | W2a | — | peer-path gaps | OK; note 2025 overlap (done) |
| 4.4 | CXMT 26.99/15.24; YMTC 28.56/12.88/12.24/9.96; ROE path; R&D 23→3.75; revenue 187→632 | G1–G3 | prospectuses | — | OK; **CHK** "Beijing E-Town 31.72%" belongs to which table (pre-/post-money) — keep out of body (it is) |
| 5.1 | US-bound −34–−68%; RI servers .024, network .049; RW 0/10; allied n.s. | L1-RI, L2-RI, RW | Comtrade/BACI | RI, RW | OK |
| 5.2 | HS8 p=.63/.30/.94; litho allied 1.1→10.0 | A1, A2 | GACC HS8 | shape tests, 126 perms | OK; **CHK** classification of 84862029 as controlled (assumption; sensitivity: move to uncontrolled) |
| 5.3 | AMAT 34,17,45,27; TEL 24,44,34; SCREEN 26,42,38; DISCO/ULVAC flat | J1-TEL etc. | 10-Q/有報 | — | OK; note fiscal-year ends differ (AMAT Oct, KLAC/LRCX Jun) — add footnote |
| 5.3 | level +4.6 (p=.24); volatility +7.2 (1/21, p=.048); normalization −5.8 (3/21) | W3a–c | 10-K/有報 annual | permutation (21) | OK; p floor 1/21 stated |
| 5.3 | 10-K mentions 0→1–3.6; slope −0.80 (p=.31) | registry | 10-K text | OLS | OK |
| 5.3 | etch US 29→5%, SG+MY 12→31%; Dec-24: US −29%, JP −10%, SG+MY +41%, NL −32% (2026 ann.) | W2b | GACC HS8 | sums | OK |
| 5.3 | Hubei US-firm-origin −66% vs 0; rank 2→15 | registry | GACC provincial | — | CHK attribution by importer of record (footnote) |
| 5.4 | CS ATT −0.09 [−0.33,+0.22], p≈.53; cohorts −0.35/−0.18/+0.21 | CS1 | 8 firms | Callaway–Sant'Anna | OK; was −0.73 before Inspur fix (disclosed) |
| 2.6 | ASML ratio 0.86–1.01 (7 yrs); corr 0.92 vs 0.38 | verified | ASML AR, GACC | — | OK |

## B. Methods — consistency checks to state in text
1. **Direction of p-values**: placebo-rank p (one-sided) in §3; permutation |stat| (two-sided) in §5.3 and HS8 tests. State both explicitly.
2. **Seasonal adjustment**: quarter-specific pre-period means; fine, but document in Appendix B.
3. **Ridge penalty λ** in ASCM: fixed at 1 — report and run λ sensitivity (0.1, 10).
4. **Donor pools**: 33 (annual industry) / 15 (quarterly toolmakers) / 12 (annual index) — three different pools appear; list them in Appendix B with firm names.
5. **Currency**: annual-average CNY and KRW rates; list rates in Appendix A.
6. **Fisher ρ=.4**: assumed; add a line showing p for ρ ∈ {0, .2, .4, .6}.
7. **Second wave**: 2025 overlapping treatments — stated.
8. **HS8 classification**: ex ante by control-list reading; one line (84862029) ambiguous — sensitivity to be reported.
9. **Compliance permutation**: fiscal years not calendar-aligned across US/JP vendors — footnote.

## C. Figures
| Figure | Check |
|---|---|
| F1 quartet v4 | panel c color semantics (post-2023 red) → change to single navy; caption Piotech break |
| F2alt | OK; panel c Changchuan one-year note |
| F3 placebo clouds | p two-sided vs text — align |
| F4 spec curve | add explicit "n clipped above 400%" on axis |
| F5 (F7 compliance) | OK; fiscal-year note |
| A1 HS8 | OK |
| A2 permutation | OK |
| A3 estimators/second wave | SDID bars use registry %→log conversions; recheck AMEC SDID +119% = +0.78 log (OK) |
| A4–A8 old style | content OK; **restyle to house palette** before SSRN |
| A9 dumbbell | placebo band is approximate → **recompute from placebo file** |

## D. Items to FIX before SSRN v1
1. §3.4 "fivefold" — specify basket (total lithography imports vs Dutch-origin 84862039) and recompute.
2. §4.2 AMEC sign wording.
3. One-/two-sided p statement in §2.7.
4. Fiscal-year footnote (§5.3).
5. 84862029 sensitivity (Appendix C).
6. F1c colors; F3 p alignment; F4 clip label; A9 band.
7. Restyle A4–A8.
8. Honest DiD re-run on panel v5; ASCM λ sensitivity; Fisher ρ grid.
