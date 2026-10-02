"""Download NEX-GDDP-CMIP6 daily tas/hurs/pr over Uganda and reduce to annual statistics.

One NCSS request per (model, scenario, variable, year) returns the Uganda box for
that year; it is reduced immediately to annual grids and the daily data dropped:
  tas -> annual mean (degC)
  hurs -> annual mean (%)
  pr  -> annual total (mm) and number of days with pr >= 2.5 mm (fib ToW definition)
Output: data/processed/nex_annual_v2/{model}_{scenario}_{var}_{year}.nc
"""
import io
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import requests
import xarray as xr

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "processed" / "nex_annual_v2"
OUT.mkdir(parents=True, exist_ok=True)

BASE = "https://ds.nccs.nasa.gov/thredds/ncss/grid/AMES/NEX/GDDP-CMIP6"
MODELS = {
    "ACCESS-CM2": "r1i1p1f1", "EC-Earth3": "r1i1p1f1", "MPI-ESM1-2-HR": "r1i1p1f1",
    "MRI-ESM2-0": "r1i1p1f1", "NorESM2-MM": "r1i1p1f1", "UKESM1-0-LL": "r1i1p1f2",
    "GFDL-ESM4": "r1i1p1f1", "MIROC6": "r1i1p1f1",
}
VARS = ["tas", "hurs", "pr"]
PERIODS = {"historical": range(1980, 2015), "ssp245": range(2015, 2101), "ssp585": range(2015, 2101)}
BOX = dict(north=4.4, south=-1.6, west=29.4, east=35.2)


def reduce(ds, var):
    da = ds[var]
    if var == "tas":
        return xr.Dataset({"tas_mean": (da - 273.15).mean("time")})
    if var == "hurs":
        return xr.Dataset({"hurs_mean": da.clip(0, 100).mean("time")})
    mm = da * 86400.0
    return xr.Dataset({"pr_total": mm.sum("time"), "pr_days_2p5": (mm >= 2.5).sum("time")})


def fetch(model, scen, var, year):
    out = OUT / f"{model}_{scen}_{var}_{year}.nc"
    if out.exists():
        return "skip"
    member = MODELS[model]
    params = {"var": var, **BOX, "horizStride": 1, "temporal": "all", "accept": "netcdf3", "addLatLon": "true"}
    last = None
    candidates = [(g, sfx) for g in ("gn", "gr", "gr1") for sfx in ("_v2.0", "_v1.1", "_v1.2", "")]
    for grid, suffix in candidates:  # EC-Earth3 uses gr, GFDL-ESM4 gr1
        url = f"{BASE}/{model}/{scen}/{member}/{var}/{var}_day_{model}_{scen}_{member}_{grid}_{year}{suffix}.nc"
        for attempt in range(4):
            try:
                r = requests.get(url, params=params, timeout=180)
                if r.status_code == 404 or b"FileNotFound" in r.content[:200]:
                    break
                r.raise_for_status()
                ds = xr.open_dataset(io.BytesIO(r.content), engine="scipy")
                red = reduce(ds, var).assign_attrs(model=model, scenario=scen, year=year, source=url)
                red.to_netcdf(out)
                return "ok"
            except Exception as e:  # network hiccups: back off and retry
                last = e
                time.sleep(3 * (attempt + 1))
    return f"fail {last}"


def main(workers=6):
    # temperature and humidity first (needed for the sheltered base case); rainfall last
    jobs = [(m, s, v, y) for v in VARS for m in MODELS for s, yrs in PERIODS.items() for y in yrs]
    done = 0
    with ProcessPoolExecutor(workers) as ex:
        futs = {ex.submit(fetch, *j): j for j in jobs}
        for f in as_completed(futs):
            done += 1
            res = f.result()
            if res.startswith("fail"):
                print("FAIL", futs[f], res, flush=True)
            if done % 100 == 0:
                print(f"{done}/{len(jobs)}", flush=True)
    print("finished", done)


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 6)
