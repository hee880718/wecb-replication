"""WECB disclosures: inventory, manifest, README and tidy re-upload of the 6.3 GB supplements1 release.

Run inside the Claude container or on Windows:  python disclosures_tidy.py --token <PAT> [--stage inventory|upload]
Token: fine-grained PAT, Contents: Read and write on hee880718/researchworkbench1 (source) and on the new
public repository hee880718/wecb-disclosures (destination; create it empty on github.com first).

Stage "inventory" (fast, ~20 min for 6.3 GB on a good link): streams every asset of release `supplements1`,
reads the zip directory without extracting, classifies the contents by firm/source/year, writes
MANIFEST.csv (one row per file inside the zips) and README.md, and deletes each download after inspection
(the container keeps one asset at a time; disk need < 2.5 GB).
Stage "upload": re-uploads every asset, plus README.md and MANIFEST.csv, to release `v1` of wecb-disclosures,
with tidy names (<firm-or-source>_<content>_partNN.zip) taken from MANIFEST_names.csv. Resumable: assets already
present in the destination release are skipped.
"""
import argparse, csv, io, json, os, re, sys, time, zipfile, requests

SRC = "hee880718/researchworkbench1"; SRC_TAG = "supplements1"
DST = "hee880718/wecb-disclosures"; DST_TAG = "v1"
API = "https://api.github.com"
FIRM_HINTS = {"zte": "ZTE", "huawei": "Huawei", "smic": "SMIC", "huahong": "Hua Hong", "hua_hong": "Hua Hong", "naura": "NAURA", "北方华创": "NAURA",
              "amec": "AMEC", "中微": "AMEC", "piotech": "Piotech", "拓荆": "Piotech", "jcet": "JCET", "长电": "JCET", "tfmc": "TFMC", "通富": "TFMC",
              "huatian": "Huatian", "华天": "Huatian", "edgar": "SEC EDGAR (19 US-listed equipment firms)", "ita": "Taiwan ITA export statistics",
              "counterpoint": "Counterpoint", "ymtc": "YMTC", "长江存储": "YMTC", "cxmt": "CXMT", "长鑫": "CXMT", "edinet": "EDINET", "dart": "OpenDART",
              "gacc": "GACC customs", "comtrade": "UN Comtrade", "baci": "BACI"}

def hdr(tok): return {"Authorization": f"Bearer {tok}", "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}

def release(repo, tag, tok, create=False):
    r = requests.get(f"{API}/repos/{repo}/releases/tags/{tag}", headers=hdr(tok))
    if r.status_code == 404 and create:
        r = requests.post(f"{API}/repos/{repo}/releases", headers=hdr(tok), json={"tag_name": tag, "name": f"Corporate disclosures and trade statistics — {tag}", "body": "See README.md and MANIFEST.csv in this release.", "draft": False, "prerelease": False})
    r.raise_for_status(); return r.json()

def classify(name):
    low = name.lower()
    for k, v in FIRM_HINTS.items():
        if k in low: return v
    return "other"

def years(name):
    ys = sorted(set(re.findall(r"(?<!\d)(20[0-2]\d)(?!\d)", name))); return (ys[0] + ("–" + ys[-1] if len(ys) > 1 else "")) if ys else ""

def inventory(tok):
    rel = release(SRC, SRC_TAG, tok); rows, names = [], []
    print(f"source release {SRC_TAG}: {len(rel['assets'])} assets, {sum(a['size'] for a in rel['assets'])/1e9:.2f} GB")
    for a in rel["assets"]:
        fn = a["name"]; print(f"  {fn}  {a['size']/1e6:.0f} MB ... ", end="", flush=True)
        with requests.get(a["url"], headers={**hdr(tok), "Accept": "application/octet-stream"}, stream=True) as r:
            r.raise_for_status()
            with open(fn, "wb") as f:
                for chunk in r.iter_content(1 << 22): f.write(chunk)
        try:
            with zipfile.ZipFile(fn) as z:
                members = [m for m in z.infolist() if not m.is_dir()]
                for m in members:
                    rows.append({"asset": fn, "file": m.filename, "bytes": m.file_size, "firm_or_source": classify(m.filename), "years": years(m.filename)})
                firms = sorted({classify(m.filename) for m in members} - {"other"}); n = len(members)
        except zipfile.BadZipFile:
            rows.append({"asset": fn, "file": fn, "bytes": a["size"], "firm_or_source": classify(fn), "years": years(fn)}); firms, n = [classify(fn)], 1
        os.remove(fn); print(f"{n} files; {', '.join(firms) or 'unclassified'}")
        names.append({"asset": fn, "bytes": a["size"], "n_files": n, "contents": "; ".join(firms), "tidy_name": fn})
    with open("MANIFEST.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["asset", "file", "bytes", "firm_or_source", "years"]); w.writeheader(); w.writerows(rows)
    with open("MANIFEST_names.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["asset", "bytes", "n_files", "contents", "tidy_name"]); w.writeheader(); w.writerows(names)
    write_readme(names, rows); print("wrote MANIFEST.csv, MANIFEST_names.csv, README.md — edit tidy_name in MANIFEST_names.csv if you want different asset names, then run --stage upload")

def write_readme(names, rows):
    by = {}
    for r in rows: by.setdefault(r["firm_or_source"], []).append(r)
    lines = ["# Where Export Controls Bind — corporate disclosures and trade statistics (supplement 2)", "",
             "Kyung & Kim (2026), KIET. Original public documents behind the processed panels of the replication package",
             "(Zenodo record 1 / github.com/hee880718/wecb-replication). Everything here was downloaded from public portals",
             "(SEC EDGAR, EDINET, OpenDART, cninfo, SSE, company investor-relations sites, GACC, Taiwan ITA) and is reproduced for",
             "research provenance; copyright remains with the issuers. Total size " + f"{sum(n['bytes'] for n in names)/1e9:.2f} GB in {len(names)} zip assets.", "",
             "## Assets", "", "| Asset | Size | Files | Contents |", "|---|---|---|---|"]
    for n in names: lines.append(f"| {n['tidy_name']} | {n['bytes']/1e6:.0f} MB | {n['n_files']} | {n['contents']} |")
    lines += ["", "## Contents by firm or source", ""]
    for k in sorted(by): ys = sorted({r['years'] for r in by[k] if r['years']}); lines.append(f"- **{k}** — {len(by[k])} files" + (f", years {ys[0]}…{ys[-1]}" if ys else ""))
    lines += ["", "`MANIFEST.csv` lists every file inside every asset (asset, path, bytes, firm or source, years).", "",
              "## How the paper uses these documents", "",
              "Revenue by segment and region (Huawei, ZTE), quarterly and annual revenue (NAURA, AMEC, Piotech, SMIC, Hua Hong, JCET, TFMC, Huatian),",
              "China share of revenue (SEC 10-K/10-Q, EDINET), YMTC and CXMT STAR Market filings, Taiwan ITA HS 8542 exports. The processed",
              "series derived from them, with extraction rules and audit log, are in the replication package.", "",
              "License: documents as issued by their publishers; this index (README, MANIFEST) CC BY 4.0."]
    open("README.md", "w", encoding="utf-8").write("\n".join(lines))

def upload(tok):
    dst = release(DST, DST_TAG, tok, create=True); have = {a["name"] for a in dst["assets"]}; up_url = dst["upload_url"].split("{")[0]
    names = list(csv.DictReader(open("MANIFEST_names.csv", encoding="utf-8"))); src = release(SRC, SRC_TAG, tok); src_assets = {a["name"]: a for a in src["assets"]}
    for extra in ("README.md", "MANIFEST.csv"):
        if extra not in have:
            r = requests.post(f"{up_url}?name={extra}", headers={**hdr(tok), "Content-Type": "application/octet-stream"}, data=open(extra, "rb")); r.raise_for_status(); print("uploaded", extra)
    for n in names:
        tidy = n["tidy_name"]
        if tidy in have: print("skip (present)", tidy); continue
        a = src_assets[n["asset"]]; print(f"{n['asset']} → {tidy} ({a['size']/1e6:.0f} MB)"); 
        with requests.get(a["url"], headers={**hdr(tok), "Accept": "application/octet-stream"}, stream=True) as r:
            r.raise_for_status()
            with open(tidy, "wb") as f:
                for chunk in r.iter_content(1 << 22): f.write(chunk)
        for attempt in range(3):
            with open(tidy, "rb") as f:
                r = requests.post(f"{up_url}?name={tidy}", headers={**hdr(tok), "Content-Type": "application/zip"}, data=f, timeout=3600)
            if r.status_code in (200, 201): break
            print("  retry", attempt + 1, r.status_code, r.text[:120]); time.sleep(10)
        os.remove(tidy); print("  done")
    print("upload complete:", f"https://github.com/{DST}/releases/tag/{DST_TAG}")

if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("--token", required=True); p.add_argument("--stage", default="inventory", choices=["inventory", "upload"]); a = p.parse_args()
    inventory(a.token) if a.stage == "inventory" else upload(a.token)
