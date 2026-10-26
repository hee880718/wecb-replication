"""Build the GACC-derived inputs in figures/data from the monthly HS8-by-origin file data/processed/GACC_batch1_combined_hs8_monthly.csv.gz.
Outputs: gacc_hs8_by_line.csv (annual by HS8 x allied flag), gacc_litho_allied.csv (84862039 from US+JP+NL, annual USD bn),
etch_imports_origin_share.csv / etch_imports_origin_usd_bn.csv (84862041 by origin group), nl_litho_monthly.csv (84862039 from the Netherlands, monthly).
Run from this directory: python gacc_hs8_derivations.py"""
import pandas as pd, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')); OUT = os.path.join(ROOT, 'figures', 'data')
w = pd.read_csv(os.path.join(ROOT, 'data', 'processed', 'GACC_batch1_combined_hs8_monthly.csv.gz'), low_memory=False)
w['usd'] = pd.to_numeric(w['usd'], errors='coerce'); w['hs8'] = w['Commodity code'].astype(str).str[:8]; w['ym'] = w['Date of data'].astype(str); w['year'] = w.ym.str[:4].astype(int)
ALLIED = ['United States', 'Japan', 'Netherlands']; w['allied'] = w['Trading partner'].isin(ALLIED)
lines = ['84862010', '84862021', '84862022', '84862029', '84862031', '84862039', '84862041', '84862049', '84862050']
by_line = w[w.hs8.isin(lines) & w.year.between(2019, 2026)].groupby(['hs8', 'allied', 'year'], as_index=False).usd.sum(); by_line.to_csv(os.path.join(OUT, 'gacc_hs8_by_line.csv'), index=False)
litho = w[(w.hs8 == '84862039') & w.allied & w.year.between(2019, 2025)].groupby('year').usd.sum() / 1e9; litho.rename('usd_bn').to_csv(os.path.join(OUT, 'gacc_litho_allied.csv'))
e = w[(w.hs8 == '84862041') & w.year.between(2019, 2026)]; tot = e.groupby('year').usd.sum(); grp = {'US': ['United States'], 'SG+MY': ['Singapore', 'Malaysia'], 'JP': ['Japan'], 'KR': [p for p in e['Trading partner'].unique() if 'Korea' in str(p)]}
val = pd.DataFrame({k: e[e['Trading partner'].isin(v)].groupby('year').usd.sum() for k, v in grp.items()}).reindex(tot.index).fillna(0); val['Other'] = tot - val.sum(axis=1)
(val / 1e9).round(4).to_csv(os.path.join(OUT, 'etch_imports_origin_usd_bn.csv')); (100 * val.div(tot, axis=0)).round(3).to_csv(os.path.join(OUT, 'etch_imports_origin_share.csv'))
nl = w[(w.hs8 == '84862039') & (w['Trading partner'] == 'Netherlands')].groupby('ym').usd.sum() / 1e6; nl.rename('usd_m').to_csv(os.path.join(OUT, 'nl_litho_monthly.csv'))
print('wrote gacc_hs8_by_line.csv, gacc_litho_allied.csv, etch_imports_origin_usd_bn.csv, etch_imports_origin_share.csv, nl_litho_monthly.csv')
