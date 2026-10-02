"""Buildings per 0.01 deg pixel over Uganda from GHS-OBAT -> data/processed/building_density_001.nc
(count of all footprints and their total area; same grid as fetch_modis_lst.py)."""
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data" / "raw" / "ghs_obat_uga" / "GHS_OBAT_CSV_UGA_E2020_R2024A_V1_0.csv"
W, S, E, N, RES = 29.5, -1.6, 35.1, 4.3, 0.01
NX, NY = int(round((E - W) / RES)), int(round((N - S) / RES))

count = np.zeros((NY, NX))
area = np.zeros((NY, NX))
for c in pd.read_csv(SRC, usecols=["lon", "lat", "area"], chunksize=2_000_000):
    i = np.floor((N - c.lat.to_numpy()) / RES).astype(int)
    j = np.floor((c.lon.to_numpy() - W) / RES).astype(int)
    ok = (i >= 0) & (i < NY) & (j >= 0) & (j < NX)
    np.add.at(count, (i[ok], j[ok]), 1)
    np.add.at(area, (i[ok], j[ok]), c.area.to_numpy()[ok])
lat = N - RES * (np.arange(NY) + 0.5)
lon = W + RES * (np.arange(NX) + 0.5)
km2 = (RES * 111.32) ** 2 * np.cos(np.radians(lat))[:, None]
xr.Dataset({"buildings": (("lat", "lon"), count), "built_m2": (("lat", "lon"), area),
            "density_km2": (("lat", "lon"), count / km2)}, coords={"lat": lat, "lon": lon}).to_netcdf(
    ROOT / "data" / "processed" / "building_density_001.nc")
print("buildings", int(count.sum()), "pixels with >=1000/km2:", int((count / km2 >= 1000).sum()))
