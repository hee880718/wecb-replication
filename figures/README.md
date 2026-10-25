# figures_v2 — paper figure system (LaTeX-ready)
- One script per figure: `figNN_<name>.py` → writes `figNN_<name>.png` (300 dpi), `.pdf` (vector, Type 42 fonts), `.csv` (data behind the figure).
- Shared rules in `housestyle.py`: palette (red = treated/Chinese, navy = foreign/control, grey = placebo/untreated, pink = events), event lines, headline/subtitle/source helpers, full/half sizes.
- Inputs live in `data/` (exported from the analysis folder; never hand-typed). Re-run any script to regenerate after a data change.
- Title = conclusion sentence (used as figure headline in the WP HTML; in LaTeX the headline moves into the caption and the figure is exported with `notitle=True` if added).
- Status: fig00 (typology) done. To migrate: F1 quartet, F2alt feed, F3 placebo, F4 spec curve, F7 compliance, A1–A3, A4–A8 (restyle), A9.
