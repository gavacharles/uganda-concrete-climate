"""Re-weight the stock results with ML building counts (ml_buildings.py) instead of the height proxy.

The probability of initiation per cell, epoch, concrete class and scenario (results/stock_cells.csv)
is kept; only the number of RC buildings per cell and epoch changes. Output: results/stock_summary_ml.csv
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
s = pd.read_csv(ROOT / "results" / "stock_cells.csv")
ml = pd.read_csv(ROOT / "results" / "ml_buildings_cells.csv")
ml = ml[ml.epoch.between(1, 5)][["glat", "glon", "epoch", "ml_multi"]]
m = s.merge(ml, on=["glat", "glon", "epoch"], how="left").fillna({"ml_multi": 0.0})
m["n_init_ml"] = m.ml_multi * m.p_init
out = m.groupby(["concrete", "case", "year"]).agg(n_buildings_ml=("ml_multi", "sum"), n_initiated_ml=("n_init_ml", "sum"),
                                                  n_buildings_proxy=("n_buildings", "sum"),
                                                  n_initiated_proxy=("n_initiated", "sum")).reset_index()
out["share_ml"] = out.n_initiated_ml / out.n_buildings_ml
out["share_proxy"] = out.n_initiated_proxy / out.n_buildings_proxy
out.to_csv(ROOT / "results" / "stock_summary_ml.csv", index=False)
print(out[out.year.isin([2030, 2050, 2100])].round(3).to_string())
# epoch coverage: ML buildings in cells that the proxy run did not include
cov = ml.merge(s[["glat", "glon", "epoch"]].drop_duplicates(), how="left", indicator=True)
print("ML multi-storey buildings outside proxy cells/epochs:", round(cov[cov._merge == "left_only"].ml_multi.sum()))
