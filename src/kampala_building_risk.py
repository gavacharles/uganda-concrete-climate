"""Building-level corrosion-initiation risk for Greater Kampala.

Each footprint carries (i) the classifier's probability of having two or more storeys
(data/processed/kampala_buildings_pred.csv.gz) and (ii) the local night-time surface heat island of its
0.01 deg pixel (data/processed/suhi_uganda.nc). The probability of corrosion initiation by 2100 is taken
from the physical model at the Kampala site (ERA5-adjusted climate), for the building's construction
epoch and a local air-temperature heat island of 1.0 x night SUHI (central estimate), with relative humidity
lowered at constant vapour pressure. The model is evaluated on a grid of heat-island values and
interpolated per building. Expected multi-storey buildings past initiation = p_multi x P_init.

Outputs: results/kampala_building_risk_pixels.csv (per 0.01 deg pixel), results/kampala_building_risk_summary.csv,
figures/figB5_kampala_risk.png
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

sys.path.insert(0, str(Path(__file__).parent))
from carbonation import SPECS, Exposure, Samples, depth_variable_start_mm  # noqa: E402
from run_sites import ROOT, YEARS  # noqa: E402
from site_extensions import CASES, Site  # noqa: E402
from urban_heat import es  # noqa: E402

EPOCHS = {1: (1960, 1979), 2: (1980, 1989), 3: (1990, 1999), 4: (2000, 2009), 5: (2010, 2019)}
DT_GRID = np.arange(0.0, 4.01, 0.25)
N = 20_000
FACTOR = 1.0


def lookup(site):
    """P_init(2100) by concrete class, case, epoch and heat island (degC)."""
    rows = []
    for spec_key in ("design_blended", "asbuilt_blended"):
        for case in ("no_change", "SSP5-8.5"):
            for ep, (lo, hi) in EPOCHS.items():
                rng = np.random.default_rng(7)
                p = Samples(N, rng).draw(SPECS[spec_key])
                midx = rng.integers(0, len(site.models), N)
                cast = rng.integers(lo, hi + 1, N)
                T, H, C, _ = site.climate(case, "era5_delta", midx)
                # extend the 1980-2100 series back to 1960 with the 1980s mean, as in run_stock.py
                yrs = np.arange(1960, 2101)
                pre = yrs < YEARS[0]
                T = np.concatenate([np.repeat(T[:, :10].mean(axis=1, keepdims=True), pre.sum(), axis=1), T], axis=1)
                H = np.concatenate([np.repeat(H[:, :10].mean(axis=1, keepdims=True), pre.sum(), axis=1), H], axis=1)
                C = np.concatenate([np.full(pre.sum(), C[:10].mean()), C])
                for dT in DT_GRID:
                    Hd = np.clip(H * es(T) / es(T + dT), 1.0, 99.0)
                    d = depth_variable_start_mm(p, yrs, T + dT, Hd, C, site.elev, cast, Exposure())
                    rows.append((spec_key, case, ep, dT, float((d[:, -1] >= p["cover_mm"]).mean())))
        print("lookup", spec_key, flush=True)
    return pd.DataFrame(rows, columns=["concrete", "case", "epoch", "dT", "p_init"])


def main():
    era5 = pd.read_csv(ROOT / "data" / "processed" / "era5_sites_annual.csv")
    site = Site("Kampala", era5)
    lut = lookup(site)
    lut.to_csv(ROOT / "results" / "kampala_pinit_lookup.csv", index=False)
    b = pd.read_csv(ROOT / "data" / "processed" / "kampala_buildings_pred.csv.gz")
    b = b[b.epoch.between(1, 5)].copy()
    s = xr.open_dataset(ROOT / "data" / "processed" / "suhi_uganda.nc")
    sn = s.suhi_night.sel(lat=xr.DataArray(b.lat.to_numpy()), lon=xr.DataArray(b.lon.to_numpy()), method="nearest")
    b["suhi_night"] = np.nan_to_num(sn.to_numpy(), nan=0.0)
    b["dT"] = np.clip(b.suhi_night * FACTOR, 0, DT_GRID[-1])
    out = {}
    for (spec, case), g in lut.groupby(["concrete", "case"]):
        p_uhi = np.zeros(len(b))
        p_no = np.zeros(len(b))
        for ep in EPOCHS:
            m = (b.epoch == ep).to_numpy()
            gg = g[g.epoch == ep].sort_values("dT")
            p_uhi[m] = np.interp(b.dT.to_numpy()[m], gg.dT, gg.p_init)
            p_no[m] = gg.p_init.iloc[0]
        out[(spec, case)] = (p_uhi, p_no)
        b[f"exp_{spec}_{case}_uhi"] = b.p_multi * p_uhi
        b[f"exp_{spec}_{case}_nouhi"] = b.p_multi * p_no
    b["pi"] = ((0.60 - b.lat) / 0.01).astype(int)
    b["pj"] = ((b.lon - 32.35) / 0.01).astype(int)
    cols = [c for c in b.columns if c.startswith("exp_")] + ["p_multi"]
    px = b.groupby(["pi", "pj"])[cols].sum().join(b.groupby(["pi", "pj"]).size().rename("buildings"))
    px = px.join(b.groupby(["pi", "pj"]).suhi_night.mean())
    px.reset_index().to_csv(ROOT / "results" / "kampala_building_risk_pixels.csv", index=False)
    summ = pd.DataFrame([{"quantity": c, "total": float(b[c].sum())} for c in cols] +
                        [{"quantity": "buildings", "total": float(len(b))},
                         {"quantity": "mean_night_suhi_weighted_by_p_multi",
                          "total": float(np.average(b.suhi_night, weights=b.p_multi))}])
    summ.to_csv(ROOT / "results" / "kampala_building_risk_summary.csv", index=False)
    print(summ.round(1).to_string(), flush=True)
    figure(px)


def figure(px):
    import matplotlib.pyplot as plt
    from matplotlib.colors import BoundaryNorm, ListedColormap

    from figures import BLUE, INK2, ORANGE, draw_outline

    km2 = (0.01 * 111.32) ** 2
    ny, nx = 50, 50
    grids = {}
    for col in ("suhi_night", "exp_design_blended_SSP5-8.5_uhi", "uhi_increase"):
        g = np.full((ny, nx), np.nan)
        if col == "uhi_increase":
            v = px["exp_design_blended_SSP5-8.5_uhi"] - px["exp_design_blended_SSP5-8.5_nouhi"]
        else:
            v = px[col] / (km2 if col.startswith("exp") else 1)
        for (i, j), val in v.items():
            if 0 <= i < ny and 0 <= j < nx:
                g[i, j] = val / (km2 if col == "uhi_increase" else 1)
        grids[col] = g
    panels = (("suhi_night", "a  Night-time heat island\n    (\u00b0C)", ["#f0efec"] + ORANGE[1:6],
               [0, 0.25, 0.5, 1, 1.5, 2, 3]),
              ("exp_design_blended_SSP5-8.5_uhi", "b  Past initiation by 2100\n    (per km\u00b2)",
               BLUE, [0, 5, 10, 25, 50, 100, 200, 400]),
              ("uhi_increase", "c  Added by the heat island\n    (per km\u00b2)", ORANGE[:7], [0, 1, 2, 5, 10, 20, 40, 80]))
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 3.4))
    for ax, (col, title, ramp, bounds) in zip(axes, panels):
        cmap, norm = ListedColormap(ramp), BoundaryNorm(bounds, len(ramp))
        ax.imshow(np.clip(grids[col], bounds[0], bounds[-1] - 1e-6), extent=(32.35, 32.85, 0.10, 0.60), cmap=cmap,
                  norm=norm, interpolation="nearest", zorder=1)
        draw_outline(ax)
        ax.plot(32.582, 0.347, "o", ms=3, mfc="#0b0b0b", mec="white", zorder=5)
        ax.set_xlim(32.35, 32.85)
        ax.set_ylim(0.10, 0.60)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)
        for sp in ax.spines.values():
            sp.set_visible(False)
        ax.set_title(title, fontsize=7.5, loc="left")
        cb = fig.colorbar(plt.cm.ScalarMappable(cmap=cmap, norm=norm), ax=ax, orientation="horizontal", fraction=0.05,
                          pad=0.03, ticks=bounds)
        cb.ax.set_xticklabels([f"{t:g}" for t in bounds])
        cb.ax.tick_params(labelsize=6.5)
        cb.outline.set_visible(False)
    fig.text(0.5, 0.01, "Greater Kampala, 0.01° pixels. Specified concrete with blended cement; air heat island = "
             "night-time surface heat island. Dot: city centre.", ha="center", fontsize=7, color=INK2)
    fig.savefig(ROOT / "figures" / "figB5_kampala_risk.png")


if __name__ == "__main__":
    main()
