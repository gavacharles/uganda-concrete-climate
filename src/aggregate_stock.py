"""Aggregate GHS-OBAT Uganda building footprints to the 0.25 deg NEX-GDDP grid.

Groups: grid cell x construction epoch (0-5) x height class x use.
Height class from GHS-BUILT-H mean height: '1' (<4.5 m, one storey), '2' (4.5-7.5 m),
'3+' (>=7.5 m), 'na' (no height). Storeys = max(1, round(height / 3)).
Output: data/processed/stock_grid.csv
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data" / "raw" / "ghs_obat_uga" / "GHS_OBAT_CSV_UGA_E2020_R2024A_V1_0.csv"
OUT = ROOT / "data" / "processed" / "stock_grid.csv"


def main():
    parts = []
    for chunk in pd.read_csv(SRC, usecols=["lon", "lat", "adm1", "height", "use", "epoch", "area"],
                             chunksize=2_000_000):
        c = chunk
        c["glat"] = (np.floor(c.lat / 0.25) + 0.5) * 0.25
        c["glon"] = (np.floor(c.lon / 0.25) + 0.5) * 0.25
        h = c.height
        c["hclass"] = np.select([h.isna(), h < 4.5, h < 7.5], ["na", "1", "2"], "3+")
        storeys = np.maximum(1, np.round(h.fillna(3.0) / 3.0))
        c["floor_area"] = c.area * storeys
        g = c.groupby(["glat", "glon", "epoch", "hclass", "use"]).agg(
            n=("area", "size"), footprint_m2=("area", "sum"), floor_m2=("floor_area", "sum"))
        parts.append(g)
        print(len(parts), flush=True)
    stock = pd.concat(parts).groupby(level=[0, 1, 2, 3, 4]).sum().reset_index()
    stock.to_csv(OUT, index=False)
    print(stock.groupby("epoch").n.sum(), stock.groupby("hclass").n.sum(), sep="\n")


if __name__ == "__main__":
    main()
