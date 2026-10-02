"""Stock-level exposure: expected number and floor area of RC buildings past corrosion initiation.

For every 0.25 deg grid cell with buildings, each GHS-OBAT construction epoch is a cohort
whose casting years are drawn uniformly within the epoch. Buildings of two or more
storeys (GHS-BUILT-H height >= 4.5 m) are treated as RC frames. For each cell, epoch,
concrete class and climate case, the initiation probability P_i(t) is computed by Monte
Carlo; the expected count past initiation is n_buildings * P_i(t).

Outputs: results/stock_cells.csv (per cell) and results/stock_summary.csv (Uganda totals).
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from carbonation import SPECS, Exposure, Samples, depth_variable_start_mm  # noqa: E402
from run_sites import MODELS, NEX, co2_series  # noqa: E402

import xarray as xr  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results"
YEARS = np.arange(1960, 2101)
EPOCHS = {1: (1960, 1979), 2: (1980, 1989), 3: (1990, 1999), 4: (2000, 2009), 5: (2010, 2019)}
REPORT_YEARS = [2030, 2050, 2070, 2100]
N = 20_000
CASES = (("no_change", "ssp245", True), ("SSP2-4.5", "ssp245", False), ("SSP5-8.5", "ssp585", False))


def load_grids(models):
    """Dict (model, scen, var) -> DataArray (year, lat, lon) of annual means, 1980-2100."""
    grids = {}
    for m in models:
        for scen in ("ssp245", "ssp585"):
            for var, key in (("tas", "tas_mean"), ("hurs", "hurs_mean")):
                arrs = []
                for y in range(1980, 2101):
                    per = "historical" if y < 2015 else scen
                    with xr.open_dataset(NEX / f"{m}_{per}_{var}_{y}.nc") as ds:
                        arrs.append(ds[key].load().expand_dims(year=[y]))
                grids[(m, scen, var)] = xr.concat(arrs, "year")
    return grids


def available_models():
    ok = []
    for m in MODELS:
        need = [NEX / f"{m}_{'historical' if y < 2015 else s}_{v}_{y}.nc"
                for s in ("ssp245", "ssp585") for v in ("tas", "hurs") for y in range(1980, 2101)]
        if all(f.exists() for f in need):
            ok.append(m)
    return ok


def cell_series(grids, models, scen, lat, lon, frozen):
    """(n_models, len(YEARS)) temperature and RH at a cell; pre-1980 = 1980-1989 mean."""
    T = np.empty((len(models), len(YEARS)))
    H = np.empty_like(T)
    for i, m in enumerate(models):
        t = grids[(m, scen, "tas")].sel(lat=lat, lon=lon, method="nearest").to_numpy()
        h = grids[(m, scen, "hurs")].sel(lat=lat, lon=lon, method="nearest").to_numpy()
        yrs = np.arange(1980, 2101)
        if frozen:
            base = (yrs >= 1995) & (yrs <= 2014)
            t = np.where(yrs > 2014, t[base].mean(), t)
            h = np.where(yrs > 2014, h[base].mean(), h)
        pre = YEARS < 1980
        T[i] = np.concatenate([np.full(pre.sum(), t[:10].mean()), t])
        H[i] = np.concatenate([np.full(pre.sum(), h[:10].mean()), h])
    return T, H


def co2_full(scen, frozen):
    co2 = pd.read_csv(ROOT / "data" / "processed" / "co2_meinshausen2020.csv")
    hist = co2[co2.scenario == "historical"].set_index("year").co2_ppm
    fut = co2[co2.scenario == scen].set_index("year").co2_ppm
    s = pd.concat([hist[hist.index < 2015], fut]).reindex(YEARS)
    if frozen:
        s[s.index > 2014] = s.loc[2014]
    return s.to_numpy()


def main():
    models = available_models()
    print("models:", models)
    grids = load_grids(models)
    stock = pd.read_csv(ROOT / "data" / "processed" / "stock_grid.csv")
    rc = stock[stock.hclass.isin(["2", "3+"]) & stock.epoch.between(1, 5)]
    cells = rc.groupby(["glat", "glon", "epoch"]).agg(n=("n", "sum"), floor_m2=("floor_m2", "sum")).reset_index()
    elev = pd.read_csv(ROOT / "data" / "processed" / "cell_elevation.csv").set_index(["glat", "glon"]).elev_m
    co2 = {c: co2_full(s, f) for c, s, f in CASES}
    rng = np.random.default_rng(7)
    rows = []
    for (glat, glon), g in cells.groupby(["glat", "glon"]):
        z = float(elev.loc[(glat, glon)])
        series = {c: cell_series(grids, models, s, glat, glon, f) for c, s, f in CASES}
        for spec_key, spec in SPECS.items():
            p = Samples(N, rng).draw(spec)
            midx = rng.integers(0, len(models), N)
            for _, r in g.iterrows():
                lo, hi = EPOCHS[int(r.epoch)]
                cast = rng.integers(lo, hi + 1, N)
                for case, _, _ in CASES:
                    T, H = series[case]
                    d = depth_variable_start_mm(p, YEARS, T[midx], H[midx], co2[case], z, cast, Exposure())
                    for yr in REPORT_YEARS:
                        pi = float((d[:, YEARS == yr][:, 0] >= p["cover_mm"]).mean())
                        rows.append((glat, glon, int(r.epoch), spec_key, case, yr, pi,
                                     r.n * pi, r.floor_m2 * pi, r.n, r.floor_m2))
    res = pd.DataFrame(rows, columns=["glat", "glon", "epoch", "concrete", "case", "year", "p_init",
                                      "n_initiated", "floor_initiated_m2", "n_buildings", "floor_m2"])
    res["n_models"] = len(models)
    res.to_csv(OUT / "stock_cells.csv", index=False)
    summ = res.groupby(["concrete", "case", "year"]).agg(
        n_initiated=("n_initiated", "sum"), floor_initiated_m2=("floor_initiated_m2", "sum"),
        n_buildings=("n_buildings", "sum"), floor_m2=("floor_m2", "sum")).reset_index()
    summ["share_initiated"] = summ.n_initiated / summ.n_buildings
    summ.to_csv(OUT / "stock_summary.csv", index=False)
    print(summ.pivot_table(index=["concrete", "case"], columns="year", values="share_initiated").round(3))


if __name__ == "__main__":
    main()
