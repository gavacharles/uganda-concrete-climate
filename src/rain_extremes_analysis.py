"""Projected change in rainfall extremes and wetting-drying cycles, and the RC stock exposed.

Reads data/processed/nex_rain_v1 (fetch_rain_extremes.py). For each 0.25 deg cell and model, the
2081-2100 mean of each index is compared with 1995-2014; the ensemble mean relative change and the
share of models agreeing on its sign are kept. Exposure: ML-estimated multi-storey buildings
(results/ml_buildings_cells.csv) per cell.

Downscaled 0.25 deg daily data under-represent local extremes (absolute rx1day is too low), so only
relative changes are used.

Outputs: results/rain_extremes_cells.csv, results/rain_extremes_summary.csv, figures/fig14_rain_extremes.png
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

sys.path.insert(0, str(Path(__file__).parent))
from fetch_nex_gddp import MODELS  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RAIN = ROOT / "data" / "processed" / "nex_rain_v1"
IDX = {"rx1day": "Wettest day (Rx1day)", "r20mm": "Heavy-rain days (≥ 20 mm)",
       "wd_cycles": "Wetting events (dry → wet)", "cdd": "Longest dry spell (CDD)"}


def period_mean(model, scen, years):
    arrs = []
    for y in years:
        per = "historical" if y < 2015 else scen
        f = RAIN / f"{model}_{per}_pr_{y}.nc"
        if not f.exists():
            return None
        with xr.open_dataset(f) as ds:
            arrs.append(ds[list(IDX)].load())
    return xr.concat(arrs, "year").mean("year")


def main():
    rows = []
    for scen in ("ssp245", "ssp585"):
        changes = []
        for m in MODELS:
            base = period_mean(m, scen, range(1995, 2015))
            fut = period_mean(m, scen, range(2081, 2101))
            if base is None or fut is None:
                print("incomplete", m, scen, flush=True)
                continue
            changes.append(((fut - base) / base.where(base > 0) * 100).expand_dims(model=[m]))
        ch = xr.concat(changes, "model")
        mean = ch.mean("model")
        agree = (np.sign(ch) == np.sign(mean)).mean("model")
        df = mean.to_dataframe().add_suffix("_pct").join(agree.to_dataframe().add_suffix("_agree")).reset_index()
        df["scenario"] = scen
        df["n_models"] = ch.sizes["model"]
        rows.append(df)
    cells = pd.concat(rows, ignore_index=True)
    cells["glat"] = (np.floor(cells.lat / 0.25) + 0.5) * 0.25
    cells["glon"] = (np.floor(cells.lon / 0.25) + 0.5) * 0.25
    ml = pd.read_csv(ROOT / "results" / "ml_buildings_cells.csv")
    expo = ml[ml.epoch.between(1, 5)].groupby(["glat", "glon"]).ml_multi.sum()
    cells = cells.merge(expo.rename("rc_buildings").reset_index(), on=["glat", "glon"], how="left").fillna(
        {"rc_buildings": 0})
    cells.to_csv(ROOT / "results" / "rain_extremes_cells.csv", index=False)
    summ = []
    for scen, g in cells.groupby("scenario"):
        w = g.rc_buildings
        for k in IDX:
            v = g[f"{k}_pct"]
            ok = v.notna() & (w > 0)
            summ.append((scen, k, float(np.average(v[ok], weights=w[ok])), float(v.median()),
                         float((g.loc[ok, f"{k}_agree"] >= 0.75).mean()),
                         float(w[ok & (v > 20)].sum() / w[ok].sum())))
    s = pd.DataFrame(summ, columns=["scenario", "index", "rc_weighted_change_pct", "median_cell_change_pct",
                                    "share_cells_75pct_model_agreement", "share_rc_where_change_gt20pct"])
    s.to_csv(ROOT / "results" / "rain_extremes_summary.csv", index=False)
    print(s.round(2).to_string())
    figure(cells)


def figure(cells):
    import matplotlib.pyplot as plt
    from matplotlib.colors import BoundaryNorm, ListedColormap

    sys.path.insert(0, str(Path(__file__).parent))
    from figures import BLUE, FIG, INK2, ORANGE, SITE_LL, draw_outline

    land = pd.read_csv(ROOT / "data" / "processed" / "stock_grid.csv")[["glat", "glon"]].drop_duplicates()
    g = cells[cells.scenario == "ssp585"].merge(land, on=["glat", "glon"])
    div = BLUE[1:4][::-1] + ["#f0efec"] + ORANGE[1:4]
    panels = {
        "rx1day": ("a  Wettest day of the year", ORANGE[:6], [0, 10, 20, 30, 40, 50, 60]),
        "r20mm": ("b  Days with \u2265 20 mm", ORANGE[:6], [0, 50, 100, 200, 300, 500, 1000]),
        "wd_cycles": ("c  Wetting events (dry \u2192 wet day)", div, [-15, -10, -5, -2, 2, 5, 10, 15]),
        "cdd": ("d  Longest dry spell", div, [-40, -20, -10, -5, 5, 10, 20, 40]),
    }
    fig, axes = plt.subplots(2, 2, figsize=(7.2, 7.4))
    for ax, (k, (title, ramp, bounds)) in zip(axes.flat, panels.items()):
        cmap, norm = ListedColormap(ramp), BoundaryNorm(bounds, len(ramp))
        for _, r in g.iterrows():
            v = r[f"{k}_pct"]
            if np.isfinite(v):
                v = np.clip(v, bounds[0] + 1e-6, bounds[-1] - 1e-6)
                ax.add_patch(plt.Rectangle((r.glon - 0.125, r.glat - 0.125), 0.25, 0.25, fc=cmap(norm(v)),
                                           ec="white", lw=0.3, zorder=2))
                if r[f"{k}_agree"] < 0.75:  # fewer than 6 of 8 models agree on the sign
                    ax.add_patch(plt.Rectangle((r.glon - 0.125, r.glat - 0.125), 0.25, 0.25, fill=False,
                                               hatch="////", ec="#8a8984", lw=0, zorder=2.5))
        draw_outline(ax)
        ax.plot(SITE_LL["Kampala"][1], SITE_LL["Kampala"][0], "o", ms=3, mfc="#0b0b0b", mec="white", zorder=5)
        ax.set_xlim(29.4, 35.2)
        ax.set_ylim(-1.6, 4.4)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_visible(False)
        ax.grid(False)
        ax.set_title(title, fontsize=8.5, loc="left")
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        cb = fig.colorbar(sm, ax=ax, orientation="horizontal", fraction=0.05, pad=0.03, ticks=bounds)
        cb.ax.tick_params(labelsize=7)
        cb.set_label("Change (%)", fontsize=7.5, color=INK2)
        cb.outline.set_visible(False)
    fig.subplots_adjust(hspace=0.32)
    fig.text(0.5, 0.005, "SSP5-8.5, 2081\u20132100 vs 1995\u20132014, eight-model mean. "
             "Hatched: fewer than 6 of 8 models agree on the sign.", ha="center", fontsize=7.5, color=INK2)
    fig.savefig(FIG / "fig14_rain_extremes.png")


if __name__ == "__main__":
    main()
