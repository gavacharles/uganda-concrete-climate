"""Observed surface urban heat island (SUHI) from MODIS land-surface temperature, and its effect on carbonation.

1. SUHI per 0.01 deg pixel: for each 0.25 deg cell, rural land pixels (< 20 buildings/km2, no lakes) in the
   surrounding 3 x 3 cells give an elevation-dependent reference LST = a + b * z (least squares); SUHI is the
   pixel LST minus the reference at its own elevation. Done separately for day (13:30) and night (01:30).
2. City values: mean SUHI over urban-core pixels (>= 1,000 buildings/km2) within 10 km of each city centre.
3. Effect on corrosion initiation: surface and air heat islands differ; the daily-mean air-temperature heat
   island is taken as 0.5-1.0 times the night-time SUHI (low and central estimates), with relative humidity
   lowered at constant vapour pressure as in src/urban_heat.py.

Outputs: data/processed/suhi_uganda.nc, results/suhi_cities.csv, results/suhi_cells.csv, results/uhi_observed_pinit.csv
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr
from rasterio.features import rasterize
from rasterio.transform import from_origin
from shapely.geometry import shape

sys.path.insert(0, str(Path(__file__).parent))
from carbonation import SPECS  # noqa: E402
from run_sites import ROOT, SITES  # noqa: E402
from site_extensions import CASES, Site  # noqa: E402
from urban_heat import depths  # noqa: E402

PROC = ROOT / "data" / "processed"
URBAN, RURAL = 1000.0, 20.0
FACTORS = {"low (0.5 x night SUHI)": 0.5, "central (1.0 x night SUHI)": 1.0}


def lake_mask(lat, lon):
    lakes = json.loads((PROC / "uganda_lakes.geojson").read_text())
    tr = from_origin(lon[0] - 0.005, lat[0] + 0.005, 0.01, 0.01)
    return rasterize([(shape(f["geometry"]), 1) for f in lakes["features"]], out_shape=(len(lat), len(lon)),
                     transform=tr, fill=0).astype(bool)


def suhi(lst, z, dens, land):
    out = np.full_like(lst, np.nan)
    ny, nx = lst.shape
    b = 25  # pixels per 0.25 deg cell
    rural = land & (dens < RURAL) & np.isfinite(lst) & np.isfinite(z)
    for i0 in range(0, ny, b):
        for j0 in range(0, nx, b):
            ri = slice(max(i0 - b, 0), min(i0 + 2 * b, ny))
            rj = slice(max(j0 - b, 0), min(j0 + 2 * b, nx))
            m = rural[ri, rj]
            if m.sum() < 50:
                continue
            zz, tt = z[ri, rj][m], lst[ri, rj][m]
            A = np.c_[np.ones_like(zz), zz]
            coef, *_ = np.linalg.lstsq(A, tt, rcond=None)
            ci, cj = slice(i0, min(i0 + b, ny)), slice(j0, min(j0 + b, nx))
            out[ci, cj] = lst[ci, cj] - (coef[0] + coef[1] * z[ci, cj])
    return np.where(land, out, np.nan)


def main():
    m = xr.open_dataset(PROC / "modis_lst_uganda_2020_2021.nc")
    d = xr.open_dataset(PROC / "building_density_001.nc")
    lat, lon = m.lat.to_numpy(), m.lon.to_numpy()
    assert np.allclose(lat, d.lat) and np.allclose(lon, d.lon)
    dens = d.density_km2.to_numpy()
    land = ~lake_mask(lat, lon)
    z = m.elevation.to_numpy()
    sd = suhi(m.lst_day.to_numpy(), z, dens, land)
    sn = suhi(m.lst_night.to_numpy(), z, dens, land)
    xr.Dataset({"suhi_day": (("lat", "lon"), sd), "suhi_night": (("lat", "lon"), sn),
                "density_km2": (("lat", "lon"), dens)}, coords={"lat": lat, "lon": lon}).to_netcdf(PROC / "suhi_uganda.nc")

    LA, LO = np.meshgrid(lat, lon, indexing="ij")
    urban = (dens >= URBAN) & land
    rows = []
    for name, (la, lo, _) in SITES.items():
        dkm = np.hypot(LA - la, (LO - lo) * np.cos(np.radians(la))) * 111.32
        core = urban & (dkm <= 10)
        rows.append((name, int(core.sum()), float(np.nanmean(sd[core])) if core.any() else np.nan,
                     float(np.nanmean(sn[core])) if core.any() else np.nan))
    cities = pd.DataFrame(rows, columns=["site", "urban_pixels", "suhi_day", "suhi_night"])
    cities.to_csv(ROOT / "results" / "suhi_cities.csv", index=False)
    print(cities.round(2), flush=True)

    # building-weighted SUHI per 0.25 deg cell (for maps and the stock)
    gl = (np.floor(LA / 0.25) + 0.5) * 0.25
    go = (np.floor(LO / 0.25) + 0.5) * 0.25
    w = d.buildings.to_numpy()
    ok = np.isfinite(sn) & (w > 0)
    df = pd.DataFrame({"glat": gl[ok], "glon": go[ok], "w": w[ok], "sn": sn[ok] * w[ok], "sd": np.nan_to_num(sd[ok]) * w[ok]})
    cells = df.groupby(["glat", "glon"]).sum()
    cells = pd.DataFrame({"buildings": cells.w, "suhi_night_bw": cells.sn / cells.w, "suhi_day_bw": cells.sd / cells.w})
    cells.reset_index().to_csv(ROOT / "results" / "suhi_cells.csv", index=False)

    # corrosion initiation with the observed heat island
    era5 = pd.read_csv(PROC / "era5_sites_annual.csv")
    out = []
    for _, c in cities.iterrows():
        if not np.isfinite(c.suhi_night):
            continue
        s = Site(c.site, era5)
        for label, f in [("none", 0.0)] + list(FACTORS.items()):
            dT = max(c.suhi_night, 0.0) * f
            for case in CASES:
                p, dd, _ = depths(s, SPECS["design_blended"], case, dT, 2000)
                out.append((c.site, label, dT, case, float((dd[:, -1] >= p["cover_mm"]).mean())))
        print("pinit", c.site, flush=True)
    res = pd.DataFrame(out, columns=["site", "uhi_estimate", "delta_t_air", "case", "p_init_2100"])
    res.to_csv(ROOT / "results" / "uhi_observed_pinit.csv", index=False)
    print(res.pivot_table(index=["site", "uhi_estimate"], columns="case", values="p_init_2100").round(2))


if __name__ == "__main__":
    main()
