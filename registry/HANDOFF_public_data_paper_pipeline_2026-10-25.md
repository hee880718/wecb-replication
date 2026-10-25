# HANDOFF — From public documents to a submitted paper: the complete pipeline behind "Where Export Controls Bind"
Written 25 October 2026, the day of submission. Purpose: a precise, reusable record of how the paper was built from public data alone, so that the same machinery can be re-applied to the WD paper ("The Reverse Ascent", World Development), the Russia sanctions-evasion paper and the planned JIE demand-engine paper.

---

## 0. Where things stand (identifiers to keep)

| Item | Value |
|---|---|
| Paper | Kyung, H. and S. Kim (2026), "Where Export Controls Bind: Law and Lead in the Semiconductor Supply Chain, 2018–2026", working paper v1, 25 Oct 2026, 32 pp. (LaTeX, TeX Gyre Pagella) |
| SSRN | Submitted 25 Oct 2026 as Content Type **Preprint**, licence **CC BY-NC-ND**, classifications ERN International Trade / PSN IPE: Trade Policy; co-author Sanghoon Kim added by his KIET e-mail (his SSRN profile still shows SUNY Buffalo — he must edit it to KIET); JEL codes could not be saved in the form (add later via Modify or support@ssrn.com); approval expected in 1–3 business days |
| RIPE | Taylor & Francis Submission Portal, **submission ID 263672777** (25 Oct 2026); confirmation to hee880718@gmail.com; queries to RRIP-peerreview@journals.tandf.co.uk with the ID in the subject; the paper may not be submitted elsewhere while under review; fallback after rejection: ISQ |
| Zenodo DOI 1 — replication package | **Concept DOI 10.5281/zenodo.23636445** (cite this; resolves to the latest version) · version 1.0 DOI 10.5281/zenodo.23636446 · created through the GitHub integration; every future GitHub release becomes a new Zenodo version automatically |
| GitHub | github.com/hee880718/wecb-replication — 193 files, release v1.0; manuscript, figures, code, processed data, registry · github.com/hee880718/wecb-disclosures — README, MANIFEST and a draft release v1 awaiting the 5.8 GB assets |
| Zenodo DOI 2 — public source documents | **10.5281/zenodo.23638441** (published 25 Oct 2026; 37 assets + README + MANIFEST, 5.84 GB, 15,644 files; CC BY 4.0 index, documents as issued). Inserted into the paper's acknowledgements and README; replication package re-released as v1.1 |
| ORCID | Heekwon Kyung 0009-0006-9916-2676 (KIET, Research Fellow since 2019-08) |
| Registry | registry/CANONICAL_REGISTRY_IO_v3_2026-10-07.csv — 107 rows, every row re-verified or re-run on 25 Oct 2026 |
| Tokens to revoke | GitHub fine-grained PATs `wecb-upload` (wecb-replication) and `wecb-disclosures` (researchworkbench1 + wecb-disclosures) |

---

## 1. Data acquisition — sources, methods, storage and the traps in each

Policy (set 21 Sep 2026): public data by default; small-cost paid sources acceptable; licensed market intelligence (Gartner, Counterpoint vendor-level, Omdia tables) excluded from paper and package entirely. Everything below is reconstructible from a public portal.

| Layer | Source | How it was pulled | Where it lives | Traps found |
|---|---|---|---|---|
| US-listed equipment and component suppliers (19 firms) and telecom/device peers (19 firms, ZTE/Huawei donors) | SEC EDGAR: 10-K, 10-Q, 20-F; XBRL companyfacts and frames APIs | Bulk downloader (EDGAR bulk script; `gh_release_upload.py` pattern); geographic-revenue tables parsed from 10-Q HTML; frames API for revenue series | `edgar_filings*.zip`, `edgar_addon`, `edgar_peers_cf` (companyfacts JSON) | Fiscal fourth quarters are reported only in the 10-K, so a 10-Q-only series misses one quarter per year (AMAT Oct, KLA/LRCX Jun quarters) — donors fell to 12 until recomputed; year-to-date figures must be differenced to quarterly; frames API has gaps; geographic revenue is by customer location (includes foreign-owned fabs in China) |
| Japanese toolmakers (TEL, SCREEN, DISCO, ULVAC, Advantest, Lasertec, Tokyo Seimitsu, JEOL) | EDINET 有価証券報告書, revenue by region | EDINET API; PDF + XBRL | `edinet_filings` | Fiscal years end March: FY2024 = Apr 2023–Mar 2024; plot at fiscal mid-year (fy − 0.25); the automated parser was unreliable for some firms → manual verification of China shares (TEL FY2024 44.4% confirmed) |
| Korean toolmakers (Wonik IPS, Jusung, Eugene Technology, TES, PSK) | OpenDART | API | `dart_filings` | KRW converted at annual average rates |
| Chinese listed firms (NAURA, AMEC, Piotech, Kingsemi, Changchuan, Jingce; SMIC, Hua Hong; JCET, TFMC, Huatian) | cninfo annual and quarterly reports; SSE STAR filings | PDF collection and table parsing | `cninfo_*`, `Supplements.Corporations.Records.1` | Units: 万元 / 亿元 / billions — a 10× error reached the paper (YMTC "187 bn" was 187 亿 = 18.7 bn) and was caught only on the final audit; quarterly cumulative figures; segment definitions change; values restated in later reports → the paper uses "as first reported" with a stated vintage rule |
| Huawei, ZTE | Annual reports (Huawei unlisted; ZTE listed) | PDF | `Supplements.Corporations.Records.1` | Huawei's regional table has an **Other** region, so the four named regions do not sum to total (2024 total 862,072, Other 18,846); the carrier segment is reported separately only to 2022; CNY, not USD |
| YMTC, CXMT | SSE STAR prospectuses, sponsor letters, audit reports (2026) | PDF (scanned audit report OCR'd) | `memory_ipo_docs`, `ymtc_prospectus*` | Shareholder tables: use the **signing-date register**, not earlier capital-contribution tables (both firms' holdings were wrong in the first draft; the subsidiary-level 31.72% was CXMT's own stake in a subsidiary); net income in 亿 |
| China customs, HS8 by origin, monthly | GACC statistics portal CSV batches (848620xx tool lines, 8542, 847130, 847131, 851714, 851762) | Four download batches | `GACC.*.zip`; combined `GACC_batch1_combined_hs8_monthly.csv.gz` | Customs record arrivals (lag shipments); the province field is the importer of record, not the plant; 84862090 (mixed) excluded; origin ≠ nationality (US toolmakers ship from Singapore/Malaysia) |
| Bilateral trade | BACI V202601 (CEPII) and UN Comtrade HS6 annual/monthly (self-hosted parquet warehouse hee880718/comtrade-wh) | BACI: streaming awk on a 189 MB gz (RAM 3.9 GB); Comtrade: parquet slabs | `figures/data/china_exports_baskets_v2_{baci,comtrade,mirror}.csv` | China and Russia do not report to Comtrade → mirror flows; China's returns record Hong Kong as destination while importers record China as origin, so US-bound effects differ by source; BACI may not be redistributed (derived aggregates only); basket definitions must be frozen before estimation (v2 re-specified once, in Oct 2026, and documented) |
| Rules and designations | Federal Register, Entity List (Consolidated Screening List CSV), METI order of 23 Jul 2023, Dutch Staatscourant 2023/18212 and Regulation BZ2404162 | Manual + CSV | `consolidated.csv`, `entitylist_panel_fixed.csv` | Announcement ≠ effective date (VEU revocation announced 29 Aug 2025, in force 31 Dec 2025); the timeline uses effective dates with exceptions flagged |
| Device trackers | Canalys, Omdia, IDC, Counterpoint press releases | Archived as short text files | `tracker_panel*.zip` | Copyright stays with the publishers; the handset material was dropped from the paper (too patchy) and survives only as provenance |
| Other customs statistics | Korea Customs Service HSK tables (parquet), Taiwan ITA exports of HS 8542 | Portal downloads | `hsk_*.parquet`, `taiwan.ita.*` | Used for satellite projects; not in the paper |

Storage: the raw originals live in the private release `researchworkbench1/supplements1` (37 assets, 5.83 GB). The tidy public copy is `wecb-disclosures` (release v1, assets named `NN_source_content_years.zip`, README and MANIFEST.csv listing all 15,644 files). The container cannot reach `uploads.github.com` or `zenodo.org`, so asset uploads must run from the PC (`disclosures_tidy.py --stage upload` / `--stage download`).

---

## 2. Data discipline — the error classes actually found, in the order to check them next time

Every one of these reached a draft of the paper and was removed by audit. For the WD paper, run this list first.

1. **Units.** 亿元 read as billions (10×); 万元 vs 亿元; USD thousands in panels; percent vs log points (the paper now states percent first and log points in parentheses). Rule: every table header carries the unit; every registry row carries the unit.
2. **Set definitions.** "Twelve foreign peers" was fifteen; "27 donors" was 26 donors plus the treated unit (27 placebo paths); the three-firm aggregate was the log of the sum in one run and the mean of logs in another. Rule: one script produces the number in the text, the table and the figure at once (`spec_curve_rerun.py` is the model); the peer set is listed by name in Appendix A.
3. **Stale values from earlier runs.** The 7 Oct battery and the 9/25 Oct clean runs coexisted in the manuscript (ASCM 0.73 vs 0.66; spec-curve +122%/98% vs +138%/93%; aggregate annual SDID +56% vs +116%; dynamic NAURA +0.40/+0.58/+0.91 vs +0.52/+0.64/+0.94). Rule: the registry `status` column marks `RETIRED`/`superseded`; an automated scan checks every number in the manuscript against the registry and the figure CSVs (zero misses before submission).
4. **Tables, holdings and fiscal years.** Shareholder tables from the wrong page; fiscal-year points plotted at the start rather than the midpoint; restated prior-year figures.
5. **Facts with an expiry date.** "No domestic immersion lithography tool" was true through 2025 and false in 2026 (SMIC testing a domestic scanner from Sep 2025; low-volume production in 2026). Rule: time-stamp every capability claim.
6. **Figure text collisions.** With fourteen figures laid out side by side, eleven had clipped or overlapping text; one script (`fig02_feed.py`) had been failing silently for days because of an apostrophe inside a single-quoted string, so its PNG was stale. Rule: `ast.parse` every figure script, check the regeneration log, and view all figures as a contact sheet before typesetting.
7. **Classification claims.** "Not listed" became "largely unlisted" after reading METI's 23 categories (sputtering may be partly covered). Rule: check the legal text, not secondary summaries.
8. **Reporting discipline (process).** Twice a fix was reported as applied when the edit had not reached the file. Rule: confirm every correction by re-reading the PDF text (`pdftotext | grep`) before reporting it.

---

## 3. Analysis toolkit (code/analysis/ in the replication package)

| Script | What it does | Headline outputs | Runtime |
|---|---|---|---|
| `clean_run_sdid.py` (+ `sdid2.py`) | Synthetic difference-in-differences (Arkhangelsky et al.) on the annual device panel (Huawei, ZTE segments; 29 donors) and the quarterly equipment panel (15 donors, seasonally adjusted); placebo ranks | Huawei −0.54 log (−42%, 1/30); ZTE consumer −0.63 (−47%, 1/30), carrier +0.01 (16/30); EQUIP3/NAURA/AMEC/ACMR +0.84/+0.96/+0.80/+0.94, all 1/16 | ~15 min |
| `spec_curve_rerun.py` | 112 specifications: 7 estimators (SDID, SC, ridge-augmented SC λ=1, two-factor IFE "GSC", soft-impute matrix completion, BJS imputation, TWFE) × 2 preparations (SA, trailing-4-quarter) × 2 counterfactuals (peers, own trend) × 4 units; ASCM and SDID placebo ranks; aggregate = mean of the three log series | vs peers median +138%, 93% > 0; vs own trend +16%, 73% > 0; ASCM 0.66/0.78/0.41/0.49 | ~8 min |
| `sdid2.py` (annual) | Annual SDID, 26 donors (14 SEC/EU incl. ASML, 8 Japanese, 4 Korean), pre 2017–22, post 2023–25 | NAURA +91%, AMEC +80%, ACMR +68%, aggregate +116%, all 1/27 | ~3 min |
| `compliance_tests.py` | Compliance-signature statistics on annual China shares (AMAT, KLA, Lam, TEL, SCREEN vs DISCO, ULVAC): level, post-2022 volatility, normalisation; all 21 assignments | +3.2 pp (p .429); +7.2 pp (1/21, p .048); −5.8 pp (3/21) | seconds |
| `ladder_v2_three_sources.py` | Trade-ladder tests for five baskets in BACI, China-reported and importer-reported data; 40 placebo destinations / 100 placebo alliances; Romano–Wolf step-down; allied-group sensitivity | US: smallest adjusted p 0.34; allies 0.079/0.069/0.366; narrower allied definitions weaker still | ~1 min |
| `hs8_shape_tests.py` | HS8 line-level level/volatility/normalisation tests, 126 assignments of four controlled lines among nine | p 0.51 / 0.63 / 0.94 | seconds |
| `make_F2alt.py` | Growth-rate change by firm for Figure 3c | NAURA −7, AMEC +3, ACM −18, Kingsemi −56, Changchuan −117, Jingce −11 pp | seconds |
| archived (registry rows) | Callaway–Sant'Anna event study of designation (8 firms, ATT −0.09 n.s.); conformal block permutation (p .054/.069); Honest DiD; placebo treatment date 2020 | Appendix B, D | — |

The package was verified by copying it to a fresh directory and running every script from there (`REPRODUCE.md` lists commands, expected outputs and runtimes). All paths are relative to the package root; the 41 MB GACC file is gzipped to pass GitHub's 25 MB web-upload limit.

---

## 4. Writing and typesetting pipeline

- **Master manuscript** is one Markdown file. Sections: 1 Introduction; 2 Theory, data and design (typology of legal vs technological chokepoints; propositions P1–P7; data layers; estimators; audit); 3 One regime, four responses; 4 Shielded substitution; 5 Where rules bind; 6 Discussion; Appendices A–F; 41 references.
- **Figures**: one script per figure (`figures/figNN_*.py` → PNG 300 dpi, vector PDF, data CSV) sharing `housestyle.py` (house red #6E0E18 titles, navy #1F3A5F, pink events, headline/subtitle/source layout; subtitle offset 0.058; panels 3–7% below the subtitle). Seven main figures, seven appendix figures (A1–A7, continuous numbering regardless of appendix letter).
- **Captions** in `captions_v7.py` (a Python dict evaluated by the builders — an apostrophe inside a single-quoted string breaks the whole build; validate with `eval` after every edit).
- **`gen_tex.py`**: pandoc → LaTeX, then: section numbering; references as a hanging-indent list on a new page; longtables converted to floats with captions; dashed rules between rows (arydshln), no dash before the bottom rule, `\arraystretch` 1.35; specific tables forced with `[H]` and narrower columns; figures 90% (main) / 84% (appendix) / 70% (A3, A7) width; `\Needspace` before section headings; `\clearpage` before References and Appendix A; preamble Pagella 12 pt, 1-inch margins, 1.15 spacing, `\emergencystretch` to kill overfull lines; running heads; `WP_ANON=1` swaps the author block and running head for the anonymised version.
- **Checks after every build**: `latexmk` error count 0; overfull hbox count 0; page scan for pages more than 30% blank; orphaned headings; PDF-text grep for the numbers just edited.
- **`build_wp_v7.py`**: self-contained HTML with base64 figures for quick reading.
- **Review format that worked**: a numbered list of page-referenced remarks (44 items) answered item by item; disagreements explained rather than silently ignored.

---

## 5. Submission playbook (order matters)

1. **Replication package → GitHub.** Build `repro/` (paper, figures, code/analysis, data/processed, data/raw, registry, README, REPRODUCE, licences, Zenodo metadata). Remove absolute paths, caches and withdrawn figures; gzip files above 25 MB. An empty repository rejects the Git Data API: create the first commit with the Contents API (README), then push the tree in one commit.
2. **Zenodo via the GitHub integration.** Log in with GitHub → account menu **GitHub** → toggle the repository ON (Sync now if absent) → **then** create the release (v1.0). The badge/DOI appears within minutes: a version DOI and a Concept DOI. Edit the record: resource type Dataset, creators with affiliations, description, CC BY 4.0 added alongside MIT, keywords. Later versions: push changes, create release v1.1 → Zenodo versions automatically; the Concept DOI never changes.
3. **DOI into the paper** (acknowledgements, data-availability statement), rebuild the PDF, update README and `zenodo_metadata.json`, commit to main (no new release needed).
4. **SSRN** (hq.ssrn.com/submissions): upload PDF → Preprint → title, abstract (fix hyphen/dash corruption from PDF extraction), keywords (JEL codes go in their own search-and-click field) → classifications (ERN International Trade; PSN IPE: Trade Policy) → authors by e-mail (masked display is normal; co-author confirms by e-mail) → Publication Details left empty (for the journal version later) → declaration of interest and funder statements → licence CC BY-NC-ND (keeps journal rights intact) → submit. Approval 1–3 business days; authors can be added later via Modify.
5. **RIPE** (Taylor & Francis Submission Portal, reached from the journal page's "Go to submission site" — not ScholarOne): four confirmations → Article → **two manuscripts** (with author details = the working-paper PDF; anonymous = the anonymised build) → title, **200-word abstract**, data set Yes with the DOI (100-character field) → declarations (ethics, AI policy with a declaration in the manuscript, no human participants, no third-party material) → keywords → authors with institution address entered manually (370 Sicheong-daero, Sejong 30147) and CRediT roles → ignore the open-access notice → preview PDF proof for anonymity → submit. The portal sends co-author verification e-mails.
6. **After submission**: record the ID; revoke tokens; when SSRN approves, add the SSRN URL to README and to the Zenodo record's related works.

---

## 6. Re-starting the WD paper ("The Reverse Ascent") with this machinery

**Current state (registry):** NBER-style LaTeX pipeline (TeX Gyre Termes) at v10r2; migration bundle WD_Migration_Bundle_v10r2_2026-07-11.zip; all 20 figures audited; econometric battery certified (demand premium +1.92, perm p .005; donut DiD k1 −4.85 / k2 −5.14; entry .199/.252; HQ premium +4.42; merchant +1.40); §5.3 re-anchored; **Gartner data abandoned, public-data reconstruction not yet done**; unverified appendix items A.1 (WFE workhorse share), A.3 (triple-difference ratio of ratios), E.4 (Table E3 chip-by-chip decomposition); title page, ORCID and e-mail fields pending.

**Plan:**
1. **Reconstruct every Gartner-dependent series from public data.** WFE and vendor revenue from the Chinese toolmakers' cninfo reports (NAURA 002371, AMEC 688012, Piotech 688072, Hwatsing 688120, Kingsemi 688037) and the SEC/EDINET/DART filings already in the package; industry totals from SEMI and WSTS public releases; device and server volumes from customs (HS 8471/8517/8528 by partner, BACI and Comtrade mirrors) and tracker press releases where unavoidable. The IO package's `figures/data/` panels (15-donor quarterly, 26-donor annual, localisation rate, HS8 lines, server origins) are directly reusable.
2. **Create CANONICAL_REGISTRY_WD_v1.csv** with the IO column structure (id, section, item, value, status, source, file, note); move every Gartner number to `RETIRED` rows; add the unit to every row.
3. **Audit in the order of §2** (units → set definitions → stale runs → table provenance → figure text → numeric scan to zero misses). Resolve A.1, A.3, E.4 or drop them.
4. **Typesetting.** Keep the NBER/Termes look but port `gen_tex.py`'s table rules, forced placements, anonymisation switch and page checks.
5. **Journal requirements.** World Development (Elsevier, Editorial Manager): check current word limit, Highlights, Declaration of Interests form, CRediT statement, Data Availability statement, and whether an SSRN preprint is acceptable (Elsevier allows preprints). Prepare: anonymised manuscript (confirm WD's review model), title page, highlights, cover letter.
6. **Deposit.** Build `wd-replication` with the same layout → GitHub → Zenodo integration → Concept DOI → insert → SSRN Preprint (CC BY-NC-ND) → journal. The public-document archive (`wecb-disclosures`, DOI 2 once issued) is shared between the two papers; cite its DOI in both.
7. **Effort estimate:** data reconstruction 2–3 sessions; registry and audit 2; manuscript re-integration 2; typesetting, package and submission 1.

---

## 7. Operating lessons from submission day

- Report a fix only after re-reading the PDF text; two "applied" edits had not reached the file.
- Validate figure scripts (`ast.parse`) and read regeneration logs; a silent failure left a stale figure in the paper for days.
- Network limits of the container: `api.github.com` and `github.com` work; `uploads.github.com` (release assets) and `zenodo.org` do not. Release assets and Zenodo uploads run from the PC with `disclosures_tidy.py`.
- Check co-author account states (SSRN affiliation, ORCID) before submission day.
- Enter submission systems through the journal page's button; publishers migrate platforms (T&F moved RIPE from ScholarOne to its own portal), so guessed URLs fail.
- Keep the SSRN working paper as the full master version and the journal submission as the derivative; both carry the same Concept DOI.
