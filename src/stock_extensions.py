"""National-scale extensions: model spread of the stock trajectories, and new construction 2020-2049.

stock_by_model.csv   share of today's RC stock past initiation, run separately for each climate model
                     (specified concrete, blended cement), 2030-2100 every 10 years.
new_construction.csv RC buildings cast 2020-2049 at each cell's 2000-2009 construction rate (GHS-OBAT
                     epoch 4, buildings >= 4.5 m), past initiation by year: concrete as built, as specified,
                     and as specified with 8 mm extra cover.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from carbonation import SPECS, Exposure, Samples, depth_variable_start_mm  # noqa: E402
from run_stock import (CASES, EPOCHS, ROOT, YEARS, available_models, cell_series,  # noqa: E402
                       co2_full, load_grids)

OUT = ROOT / "results"
REPORT = np.arange(2030, 2101, 10)
N_MODEL = 5_000
N_NEW = 20_000
EXTRA_COVER = 8.0


def main():
    models = available_models()
    print("models:", models, flush=True)
    grids = load_grids(models)
    stock = pd.read_csv(ROOT / "data" / "processed" / "stock_grid.csv")
    rc = stock[stock.hclass.isin(["2", "3+"])]
    cells = rc[rc.epoch.between(1, 5)].groupby(["glat", "glon", "epoch"]).agg(
        n=("n", "sum"), floor_m2=("floor_m2", "sum")).reset_index()
    new = rc[rc.epoch == 4].groupby(["glat", "glon"]).agg(n=("n", "sum"), floor_m2=("floor_m2", "sum"))
    new = new.assign(rate=new.n / 10.0, floor_per=new.floor_m2 / new.n)
    elev = pd.read_csv(ROOT / "data" / "processed" / "cell_elevation.csv").set_index(["glat", "glon"]).elev_m
    co2 = {c: co2_full(s, f) for c, s, f in CASES}
    rng = np.random.default_rng(11)
    by_model, newc = [], []
    for i, ((glat, glon), g) in enumerate(cells.groupby(["glat", "glon"])):
        z = float(elev.loc[(glat, glon)])
        series = {c: cell_series(grids, models, s, glat, glon, f) for c, s, f in CASES}
        # 1) separate run per climate model, today's stock, specified blended concrete
        p = Samples(N_MODEL, rng).draw(SPECS["design_blended"])
        for _, r in g.iterrows():
            lo, hi = EPOCHS[int(r.epoch)]
            cast = rng.integers(lo, hi + 1, N_MODEL)
            for case, _, _ in CASES:
                T, H = series[case]
                for mi, m in enumerate(models):
                    d = depth_variable_start_mm(p, YEARS, np.broadcast_to(T[mi], (N_MODEL, len(YEARS))),
                                                np.broadcast_to(H[mi], (N_MODEL, len(YEARS))), co2[case], z,
                                                cast, Exposure())
                    pin = (d[:, np.isin(YEARS, REPORT)] >= p["cover_mm"][:, None]).mean(axis=0)
                    for y, pi in zip(REPORT, pin):
                        by_model.append((m, case, y, r.n * pi, r.n))
        # 2) new construction 2020-2049
        if (glat, glon) in new.index:
            nr = new.loc[(glat, glon)]
            cast = rng.integers(2020, 2050, N_NEW)
            midx = rng.integers(0, len(models), N_NEW)
            built = np.array([(cast <= y).mean() for y in REPORT])
            for spec_key in ("asbuilt_blended", "design_blended"):
                p = Samples(N_NEW, rng).draw(SPECS[spec_key])
                for case, _, _ in CASES:
                    T, H = series[case]
                    d = depth_variable_start_mm(p, YEARS, T[midx], H[midx], co2[case], z, cast, Exposure())
                    dr = d[:, np.isin(YEARS, REPORT)]
                    variants = {spec_key: 0.0} if spec_key.startswith("asbuilt") else \
                        {spec_key: 0.0, f"{spec_key}_plus{EXTRA_COVER:.0f}mm": EXTRA_COVER}
                    for vname, dc in variants.items():
                        pin = (dr >= (p["cover_mm"] + dc)[:, None]).mean(axis=0)
                        for y, pi, b in zip(REPORT, pin, built):
                            total = nr.rate * 30
                            newc.append((glat, glon, vname, case, y, total * b, total * pi,
                                         total * pi * nr.floor_per))
        if i % 25 == 0:
            print(i, flush=True)
    bm = pd.DataFrame(by_model, columns=["model", "case", "year", "n_initiated", "n_buildings"])
    bm = bm.groupby(["model", "case", "year"]).sum().reset_index()
    bm["share_initiated"] = bm.n_initiated / bm.n_buildings
    bm.to_csv(OUT / "stock_by_model.csv", index=False)
    nc = pd.DataFrame(newc, columns=["glat", "glon", "variant", "case", "year", "n_built", "n_initiated",
                                     "floor_initiated_m2"])
    nc.to_csv(OUT / "new_construction_cells.csv", index=False)
    s = nc.groupby(["variant", "case", "year"])[["n_built", "n_initiated", "floor_initiated_m2"]].sum().reset_index()
    s["share_of_built"] = s.n_initiated / s.n_built
    s.to_csv(OUT / "new_construction.csv", index=False)
    print(bm.pivot_table(index=["case", "year"], values="share_initiated", aggfunc=["min", "mean", "max"]).round(3))
    print(s[s.year.isin([2050, 2100])].round(3).to_string())


if __name__ == "__main__":
    main()
