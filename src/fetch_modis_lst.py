"""MODIS Aqua land-surface temperature (MYD11A2 v061, 8-day, 1 km) for Uganda, 2020-2021, from the
Microsoft Planetary Computer, averaged onto a 0.01 deg grid; plus the Copernicus 90 m DEM on the same grid.

Aqua overpasses at about 13:30 and 01:30 local time; the night pass is close to the time of maximum
urban heat island. Pixels flagged as fill (0) are skipped; 8-day composites are already clear-sky.
Output: data/processed/modis_lst_uganda_2020_2021.nc (lst_day, lst_night in degC, n_day, n_night, elevation)
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
import planetary_computer as pc
import pystac_client
import rasterio
import xarray as xr
from rasterio.warp import Resampling, reproject
from rasterio.transform import from_origin

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "processed" / "modis_lst_uganda_2020_2021.nc"
W, S, E, N = 29.5, -1.6, 35.1, 4.3
RES = 0.01
NX, NY = int(round((E - W) / RES)), int(round((N - S) / RES))
DST = from_origin(W, N, RES, RES)


def to_grid(href, scale=1.0, nodata=0, resampling=Resampling.average):
    out = np.full((NY, NX), np.nan, dtype="float32")
    with rasterio.open(href) as src:
        reproject(rasterio.band(src, 1), out, src_nodata=nodata, dst_transform=DST, dst_crs="EPSG:4326",
                  dst_nodata=np.nan, resampling=resampling)
    return out * scale


def lst(item, var):
    a = to_grid(pc.sign(item.assets[var].href))
    return a * 0.02 - 273.15  # MODIS LST scale factor 0.02 K


def main():
    cat = pystac_client.Client.open("https://planetarycomputer.microsoft.com/api/stac/v1", modifier=pc.sign_inplace)
    items = [it for it in cat.search(collections=["modis-11A2-061"], bbox=[W, S, E, N],
                                     datetime="2020-01-01/2021-12-31").items() if it.id.startswith("MYD11A2")]
    print("items", len(items), flush=True)
    acc = {v: [np.zeros((NY, NX)), np.zeros((NY, NX))] for v in ("LST_Day_1km", "LST_Night_1km")}

    def job(args):
        it, var = args
        for attempt in range(4):
            try:
                return var, lst(it, var)
            except Exception as e:  # transient network errors
                err = e
        print("fail", it.id, var, err, flush=True)
        return var, None

    jobs = [(it, v) for it in items for v in acc]
    with ThreadPoolExecutor(8) as ex:
        for i, (var, a) in enumerate(ex.map(job, jobs)):
            if a is not None:
                ok = np.isfinite(a)
                acc[var][0][ok] += a[ok]
                acc[var][1][ok] += 1
            if i % 50 == 0:
                print(i, "/", len(jobs), flush=True)
    dem_items = list(cat.search(collections=["cop-dem-glo-90"], bbox=[W, S, E, N]).items())
    z_sum, z_n = np.zeros((NY, NX)), np.zeros((NY, NX))
    for it in dem_items:
        a = to_grid(pc.sign(it.assets["data"].href), nodata=None)
        ok = np.isfinite(a)
        z_sum[ok] += a[ok]
        z_n[ok] += 1
    lat = N - RES * (np.arange(NY) + 0.5)
    lon = W + RES * (np.arange(NX) + 0.5)
    ds = xr.Dataset({
        "lst_day": (("lat", "lon"), np.where(acc["LST_Day_1km"][1] > 0, acc["LST_Day_1km"][0] / np.maximum(acc["LST_Day_1km"][1], 1), np.nan)),
        "lst_night": (("lat", "lon"), np.where(acc["LST_Night_1km"][1] > 0, acc["LST_Night_1km"][0] / np.maximum(acc["LST_Night_1km"][1], 1), np.nan)),
        "n_day": (("lat", "lon"), acc["LST_Day_1km"][1]), "n_night": (("lat", "lon"), acc["LST_Night_1km"][1]),
        "elevation": (("lat", "lon"), np.where(z_n > 0, z_sum / np.maximum(z_n, 1), np.nan)),
    }, coords={"lat": lat, "lon": lon}, attrs={"source": "MYD11A2 v061 (Planetary Computer), Copernicus DEM GLO-90",
                                               "period": "2020-2021"})
    ds.to_netcdf(OUT)
    print("wrote", OUT, flush=True)


if __name__ == "__main__":
    main()
