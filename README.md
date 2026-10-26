# Where Export Controls Bind — reproducibility package v1 (2026-10-25)

[![DOI](https://zenodo.org/badge/1432913073.svg)](https://doi.org/10.5281/zenodo.23636445)

Archived on Zenodo: concept DOI 10.5281/zenodo.23636445 (all versions); version 1.0 DOI 10.5281/zenodo.23636446. Cite as: Kyung, H. and S. Kim (2026). Where Export Controls Bind — replication package v1.0. Zenodo. https://doi.org/10.5281/zenodo.23636446
Kyung & Kim, KIET. Every number and figure in `paper/WP_WhereExportControlsBind_v8.md` can be re-derived from this package.

## Layout
- `paper/` — manuscript: Markdown source (`WP_WhereExportControlsBind_v8.md`), LaTeX source and generator (`WP_WhereExportControlsBind_v8.tex`, `gen_tex.py`), typeset PDF, built HTML, captions, HTML build script (`python build_wp_v7.py`), SSRN submission fields.
- `figures/` — one script per figure (`figNN_*.py`) writing PNG/PDF/CSV; `figures/data/` holds every processed input the scripts read; shared style in `housestyle.py`.
- `code/build/` — `gacc_hs8_derivations.py` (rebuilds the GACC-derived inputs in `figures/data` from the monthly HS8 file). `code/analysis/` — `clean_run_sdid.py` (Huawei, ZTE and quarterly SDID; registry K1v2, K2v2, F8); `spec_curve_rerun.py` (the 112-specification curve, ASCM and SDID with placebo ranks, Appendix B and Figure 4); `sdid2.py` (annual SDID, 26 donors; `python sdid2.py` prints NAURA, AMEC, ACM Research, the three-firm aggregate, SMIC and Hua Hong); `compliance_tests.py` (W3a–c); `ladder_v2_three_sources.py` (three-source ladder tests with Romano–Wolf; allied-group sensitivity in `figures/data/ladder_v2_allies_sensitivity.csv`); `hs8_shape_tests.py` (HS8 shape tests, Appendix C); `make_F2alt.py` (F2a).
- `data/processed/` — panels and extracted series; `data/raw/` — redistributable originals (YMTC/CXMT STAR filings; archived tracker press releases). The full archive of public source documents (37 assets, 5.8 GB, 15,644 files: cninfo, SEC EDGAR, EDINET, OpenDART, SSE prospectuses, GACC customs, customs statistics, press releases) is a separate Zenodo record, DOI 10.5281/zenodo.23638441 (index at github.com/hee880718/wecb-disclosures). Large third-party originals (BACI, UN Comtrade) are listed in `data/RAW_SOURCES.md`.
- `registry/` — CANONICAL_REGISTRY (every value: status, source, file), page-by-page audits, roadmap.

## Provenance (original source → processed file)
| Input | Original public source | Processed file |
|---|---|---|
| US/EU toolmakers' revenue, China share | SEC EDGAR 10-K/10-Q geographic revenue tables, XBRL frames | us3_china_revenue.csv; EDGAR_controls_revenue_frames_19firms.csv |
| Japanese toolmakers | EDINET 有価証券報告書, revenue by region | edinet_china_share_v3.csv; edinet_revenue_annual.csv |
| Korean toolmakers | OpenDART annual reports | dart_revenue_annual.csv |
| Chinese toolmakers, SMIC, Hua Hong | cninfo reports; SMIC and Hua Hong IR | cn6_quarterly_cny_v3.csv; cn6_revenue_annual.csv; CN_equipment_annual_parsed_*.csv; quarterly_panel_local_v5.csv |
| Huawei segments and regions | Huawei annual reports 2018–2025 | huawei_segments_from_AR.csv; figures/data/huawei_regions.csv |
| ZTE segments | ZTE annual reports | telecom_device_panel_logUSD_v2.csv |
| YMTC, CXMT | SSE STAR filings 2026 (`data/raw/ymtc_cxmt_filings`: YMTC application of 21 Aug 2026 with sponsor and audit reports; CXMT prospectus of 22 Jul 2026) | registry G1–G3, Q4–Q7; Appendix E |
| China customs HS8 by origin, monthly | GACC statistics portal, imports, HS 848620xx | gacc_848620_hs8.csv; figures/data/gacc_*, etch_imports_origin_* |
| Bilateral trade | BACI V202601 (CEPII); UN Comtrade HS6 annual warehouse (github.com/hee880718/comtrade-wh) | figures/data/china_exports_baskets_v2_*.csv; us_imports_847150_by_origin.csv |
| Rules and designations | Federal Register, Entity List, METI, Staatscourant | entitylist_panel_fixed.csv; Figure 1 |

## Reproduce
See `REPRODUCE.md` for the script-by-script list with expected outputs and runtimes. `pip install pandas numpy scipy matplotlib`; run any `figures/figNN_*.py` or `code/analysis/*.py` from its own directory. Retired and corrected values are listed in Appendix F of the paper and in the `status` column of the registry. Every number in the paper is re-derived from the processed panels by the scripts in this package (four audit rounds; see `registry/`); the step from the original documents to the processed panels is scripted where `data/PROVENANCE.md` says so and otherwise consists of document extraction audited by hand against the originals, which are archived in Zenodo record 10.5281/zenodo.23638441.

## Redistribution
Code: MIT (LICENSE-CODE.txt). Processed data and figures: CC BY 4.0 (LICENSE-DATA.txt). `data/raw/ymtc_cxmt_filings` are public regulatory filings from the Shanghai Stock Exchange and cninfo, reproduced for research; `data/raw/tracker_press_releases` holds only a manifest (file names, sizes, SHA-256, publisher) of the archived press releases; the texts themselves remain the property of their publishers and are not redistributed here. BACI (CEPII) and UN Comtrade originals are not bundled; the basket aggregates derived from them are.
