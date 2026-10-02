"""Elevation (m) at the centre of each 0.25 deg grid cell with buildings (Open-Meteo, SRTM-based)."""
import time
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]


def main():
    cells = pd.read_csv(ROOT / "data" / "processed" / "stock_grid.csv")[["glat", "glon"]].drop_duplicates()
    out = []
    for i in range(0, len(cells), 100):
        c = cells.iloc[i:i + 100]
        for attempt in range(5):
            r = requests.get("https://api.open-meteo.com/v1/elevation", params={
                "latitude": ",".join(map(str, c.glat)), "longitude": ",".join(map(str, c.glon))}, timeout=60)
            if r.status_code != 429:
                break
            time.sleep(60)
        r.raise_for_status()
        out.append(c.assign(elev_m=r.json()["elevation"]))
        time.sleep(2)
    pd.concat(out).to_csv(ROOT / "data" / "processed" / "cell_elevation.csv", index=False)
    print(len(cells), "cells")


if __name__ == "__main__":
    main()
