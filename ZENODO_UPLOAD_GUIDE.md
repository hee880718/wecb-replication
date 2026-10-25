# Deposit guide (v1, 2026-10-21)
## A. Replication package (this folder) — DOI 1
1. https://github.com/new → repository `wecb-replication` (public, or private until review) → upload this folder's contents.
2. https://zenodo.org/account/settings/github/ → toggle `wecb-replication` ON.
3. GitHub → Releases → Draft a new release → tag v1.0 → Publish. Zenodo archives it and mints a DOI within minutes.
4. https://zenodo.org/me/uploads → open the record → Edit → fill from zenodo_metadata.json → Publish.
5. Insert DOI 1 into the paper (Acknowledgements) and SSRN's Data and code field.
## B. Source documents (~6 GB public filings) — DOI 2
Upload the supplements1 release zips (ASML, cninfo, EDGAR, EDINET, DART, EU IR, TEL, Hua Hong, YMTC prospectus, GACC, HSK) to a second Zenodo record: title 'Source documents for Where Export Controls Bind', upload_type dataset, licence 'other-pd', related identifier DOI 1 (isSupplementTo).
## C. Not redistributed
BACI V202601 (CEPII), UN Comtrade HS6 parquet (github.com/hee880718/comtrade-wh), Huawei annual reports (huawei.com): links and build steps in README.md.
