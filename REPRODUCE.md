# Reproduce every number in the paper (tested 25 October 2026 from a fresh copy of this package)

Requirements: Python 3.10+ with `pandas numpy scipy matplotlib requests`; for the PDF, pandoc and XeLaTeX (TeX Gyre Pagella).
Run each script from its own directory.

| Script (directory) | Produces | Expected output (abridged) | Runtime |
|---|---|---|---|
| `code/analysis/clean_run_sdid.py` | Huawei, ZTE and quarterly SDID with placebo ranks (§3.1–3.3, Appendix B) | EQUIP3 +0.84 (1/16), NAURA +0.96, AMEC +0.80, ACMR +0.94; Huawei −0.54 (−42%, 1/30); ZTE consumer −0.63 (−47%, 1/30), carrier +0.01 (16/30) | ~15 min |
| `code/analysis/spec_curve_rerun.py` | `figures/data/spec_curve_feed.csv`, `spec_curve_ranks.csv` (Figure 4, Appendix B) | vs peers median +138%, 93% > 0; vs own trend +16%, 73% > 0; ASCM 0.66/0.78/0.41/0.49 | ~8 min |
| `code/analysis/sdid2.py` (import; see `clean_run_sdid.py`) | annual SDID, 26 donors | NAURA +91%, AMEC +80%, ACMR +68%, aggregate +116% (all 1/27) | ~3 min |
| `code/analysis/compliance_tests.py` | §5.3, Appendix D | +3.2 pp (p = 0.429); +7.2 pp (1/21, p = 0.048); −5.8 pp (3/21) | seconds |
| `code/analysis/ladder_v2_three_sources.py` | `figures/data/ladder_v2_three_sources_RW.csv` (§5.1, Figure 5) | US smallest RW p 0.34; allies 0.079 / 0.069 / 0.366 | ~1 min |
| `code/analysis/hs8_shape_tests.py` | §5.2, Appendix C | +0.28 (p 0.51), +0.20 (p 0.63), +0.03 (p 0.94) | seconds |
| `code/analysis/make_F2alt.py` | `figures/data/` inputs of Figure 3 | growth change NAURA −7, AMEC +3, ACM −18, Kingsemi −56, Changchuan −117, Jingce −11 | seconds |
| `figures/figNN_*.py` (14 scripts) | PNG, PDF and CSV of every figure | — | seconds each |
| `paper/build_wp_v7.py` | `paper/WP_WhereExportControlsBind_v8.html` | — | seconds |
| `paper/gen_tex.py` then `latexmk -xelatex wp.tex` (in `paper/`) | typeset PDF (32 pages) | — | ~1 min |

Values are traced in `registry/CANONICAL_REGISTRY_IO_v3_2026-10-07.csv` (status, source, file) and corrections in Appendix F of the paper.
