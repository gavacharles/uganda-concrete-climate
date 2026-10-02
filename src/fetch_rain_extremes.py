"""Daily rainfall indices from NEX-GDDP-CMIP6 over Uganda (8 models, 1980-2100).

For each model, scenario and year, daily pr is reduced to annual grids:
  rx1day     maximum 1-day rainfall (mm)
  rx5day     maximum 5-day rainfall (mm)
  r20mm      days with >= 20 mm (heavy rain)
  r50mm      days with >= 50 mm (very heavy rain; flash-flood relevant)
  wet_days   days with >= 1 mm
  wd_cycles  wetting events: a wet day (>= 1 mm) following a dry day (< 1 mm)
  cdd        longest run of dry days (< 1 mm)
Output: data/processed/nex_rain_v1/{model}_{scenario}_pr_{year}.nc
"""
import io
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import requests
import xarray as xr

sys.path.insert(0, str(Path(__file__).parent))
from fetch_nex_gddp import BASE, BOX, MODELS, PERIODS  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "processed" / "nex_rain_v1"
OUT.mkdir(parents=True, exist_ok=True)


def longest_run(mask):
    """Longest run of True along axis 0 of a (time, lat, lon) boolean array."""
    run = np.zeros(mask.shape[1:], dtype=int)
    best = np.zeros_like(run)
    for t in range(mask.shape[0]):
        run = np.where(mask[t], run + 1, 0)
        best = np.maximum(best, run)
    return best


def reduce(ds):
    mm = (ds["pr"] * 86400.0).transpose("time", "lat", "lon")
    a = mm.to_numpy()
    wet = a >= 1.0
    r5 = np.lib.stride_tricks.sliding_window_view(a, 5, axis=0).sum(axis=-1)
    dims, co = ("lat", "lon"), {"lat": mm.lat, "lon": mm.lon}
    return xr.Dataset({
        "rx1day": (dims, a.max(axis=0)), "rx5day": (dims, r5.max(axis=0)),
        "r20mm": (dims, (a >= 20).sum(axis=0)), "r50mm": (dims, (a >= 50).sum(axis=0)),
        "wet_days": (dims, wet.sum(axis=0)), "wd_cycles": (dims, (wet[1:] & ~wet[:-1]).sum(axis=0)),
        "cdd": (dims, longest_run(~wet)),
    }, coords=co)


def fetch(model, scen, year):
    out = OUT / f"{model}_{scen}_pr_{year}.nc"
    if out.exists():
        return "skip"
    member = MODELS[model]
    params = {"var": "pr", **BOX, "horizStride": 1, "temporal": "all", "accept": "netcdf3", "addLatLon": "true"}
    last = None
    for grid in ("gn", "gr", "gr1"):
        for suffix in ("_v2.0", "_v1.1", "_v1.2", ""):
            url = f"{BASE}/{model}/{scen}/{member}/pr/pr_day_{model}_{scen}_{member}_{grid}_{year}{suffix}.nc"
            for attempt in range(4):
                try:
                    r = requests.get(url, params=params, timeout=180)
                    if r.status_code == 404 or b"FileNotFound" in r.content[:200]:
                        break
                    r.raise_for_status()
                    ds = xr.open_dataset(io.BytesIO(r.content), engine="scipy")
                    reduce(ds).assign_attrs(model=model, scenario=scen, year=year, source=url).to_netcdf(out)
                    return "ok"
                except Exception as e:  # network hiccups: back off and retry
                    last = e
                    time.sleep(3 * (attempt + 1))
    return f"fail {last}"


def main(workers=6):
    jobs = [(m, s, y) for m in MODELS for s, yrs in PERIODS.items() for y in yrs]
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
    print("finished", done, flush=True)


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 6)
