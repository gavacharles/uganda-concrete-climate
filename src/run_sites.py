"""Site-level corrosion-initiation probabilities for each scenario, concrete class and casting year.

Reads the annual NEX-GDDP-CMIP6 grids (src/fetch_nex_gddp.py) and the CO2 pathways,
builds per-model annual series at each site (nearest grid cell), and runs the
probabilistic carbonation model. Climate model is sampled per realisation.

Usage: .venv/bin/python src/run_sites.py [site ...]   (default: all sites)
Outputs: results/site_pinit.csv, results/site_climate.csv
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

sys.path.insert(0, str(Path(__file__).parent))
from carbonation import SPECS, Exposure, Samples, carbonation_depth_mm  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
NEX = ROOT / "data" / "processed" / "nex_annual_v2"
OUT = ROOT / "results"
OUT.mkdir(exist_ok=True)

SITES = {  # lat, lon, elevation (m, Open-Meteo/SRTM)
    "Kampala": (0.3476, 32.5825, 1174), "Mbale": (1.0821, 34.1750, 1121),
    "Gulu": (2.7746, 32.2990, 1099), "Arua": (3.0201, 30.9111, 1215),
    "Mbarara": (-0.6072, 30.6545, 1446), "Kasese": (0.1833, 30.0833, 990),
}
MODELS = ["ACCESS-CM2", "EC-Earth3", "MPI-ESM1-2-HR", "MRI-ESM2-0", "NorESM2-MM",
          "UKESM1-0-LL", "GFDL-ESM4", "MIROC6"]
YEARS = np.arange(1980, 2101)
CAST_YEARS = [1980, 1990, 2000, 2010, 2020, 2030, 2040, 2050]
N = 100_000


def site_series(site):
    """Annual tas, hurs, rain-day fraction per model and scenario at the site's grid cell."""
    lat, lon, _ = SITES[site]
    rows = []
    for m in MODELS:
        for scen in ("ssp245", "ssp585"):
            for y in YEARS:
                per = "historical" if y < 2015 else scen
                rec = {"model": m, "scenario": scen, "year": y}
                ok = True
                for var, key in (("tas", "tas_mean"), ("hurs", "hurs_mean"), ("pr", "pr_days_2p5")):
                    f = NEX / f"{m}_{per}_{var}_{y}.nc"
                    if not f.exists():
                        if var == "pr":  # rainfall only matters for rain-exposed members
                            rec[var] = np.nan
                            continue
                        ok = False
                        break
                    with xr.open_dataset(f) as ds:
                        rec[var] = float(ds[key].sel(lat=lat, lon=lon, method="nearest"))
                if ok:
                    rows.append(rec)
    df = pd.DataFrame(rows)
    df["tow"] = df["pr"] / 365.0
    return df


def complete_models(df):
    need = len(YEARS)
    c = df.groupby(["model", "scenario"]).year.nunique().unstack()
    return [m for m in c.index if (c.loc[m] == need).all()]


def climate_arrays(df, models, scen, model_idx, frozen, era5_base=None):
    """(n, years) arrays of T and RH for the sampled model of each realisation.

    era5_base=None uses the downscaled values as they are ("raw"). Otherwise (tas, hurs)
    1995-2014 ERA5 means: the delta-change method adds each model's anomaly relative to its
    own 1995-2014 mean to the ERA5 baseline.
    """
    T = np.empty((len(models), len(YEARS)))
    H = np.empty_like(T)
    base = (YEARS >= 1995) & (YEARS <= 2014)
    for i, m in enumerate(models):
        s = df[(df.model == m) & (df.scenario == scen)].set_index("year").reindex(YEARS)
        t, h = s.tas.to_numpy(), s.hurs.to_numpy()
        if era5_base is not None:
            t = era5_base[0] + (t - t[base].mean())
            h = np.clip(era5_base[1] + (h - h[base].mean()), 1.0, 99.0)
        if frozen:  # no climate change after 2014: hold the 1995-2014 mean
            t = np.where(YEARS > 2014, t[base].mean(), t)
            h = np.where(YEARS > 2014, h[base].mean(), h)
        T[i], H[i] = t, h
    return T[model_idx], H[model_idx]


def co2_series(scen, frozen):
    co2 = pd.read_csv(ROOT / "data" / "processed" / "co2_meinshausen2020.csv")
    hist = co2[co2.scenario == "historical"].set_index("year").co2_ppm
    fut = co2[co2.scenario == scen].set_index("year").co2_ppm
    s = pd.concat([hist[hist.index < 2015], fut]).reindex(YEARS)
    if frozen:
        s[s.index > 2014] = s.loc[2014]
    return s.to_numpy()


def run_site(site):
    df = site_series(site)
    models = complete_models(df)
    if not models:
        print(site, "no complete models yet")
        return None, df
    elev = SITES[site][2]
    era5 = pd.read_csv(ROOT / "data" / "processed" / "era5_sites_annual.csv")
    e = era5[(era5.site == site) & era5.year.between(1995, 2014)]
    baselines = {"raw": None, "era5_delta": (e.tas.mean(), e.hurs.mean())}
    out = []
    for bl, eb in baselines.items():
        for spec_key, spec in SPECS.items():
            rng = np.random.default_rng(42)
            p = Samples(N, rng).draw(spec)
            model_idx = rng.integers(0, len(models), N)
            for case, scen, frozen in (("no_change", "ssp245", True), ("SSP2-4.5", "ssp245", False),
                                       ("SSP5-8.5", "ssp585", False)):
                T, H = climate_arrays(df, models, scen, model_idx, frozen, eb)
                C = co2_series(scen, frozen)
                for cy in CAST_YEARS:
                    k = YEARS >= cy
                    d = carbonation_depth_mm(p, YEARS[k], T[:, k], H[:, k], C[k], elev, Exposure())
                    pin = (d >= p["cover_mm"][:, None]).mean(axis=0)
                    for yr, pi, dm in zip(YEARS[k], pin, d.mean(axis=0)):
                        out.append((site, bl, spec_key, case, cy, yr, pi, dm))
    res = pd.DataFrame(out, columns=["site", "baseline", "concrete", "case", "cast_year", "year",
                                     "p_init", "mean_depth_mm"])
    res["n_models"] = len(models)
    return res, df


def main(sites):
    allres, allclim = [], []
    for s in sites:
        res, clim = run_site(s)
        clim["site"] = s
        allclim.append(clim)
        if res is not None:
            allres.append(res)
            r = res[(res.year.isin([2050, 2100])) & (res.cast_year == 2000)]
            print(s, f"({res.n_models.iat[0]} models)")
            print(r.pivot_table(index=["baseline", "concrete", "case"], columns="year", values="p_init").round(3))
    if allres:
        pd.concat(allres).to_csv(OUT / "site_pinit.csv", index=False)
    pd.concat(allclim).to_csv(OUT / "site_climate.csv", index=False)


if __name__ == "__main__":
    main(sys.argv[1:] or list(SITES))
