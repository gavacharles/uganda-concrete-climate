"""Site-level extensions: rain exposure, sensitivity, corrosion propagation and cost-benefit.

1. rain_exposure.csv   P_i(2100) for sheltered, vertical rain-exposed (p_SR = 0.25, after Val et al. 2025)
                       and horizontal rain-exposed (p_SR = 1) members, using projected rain days (>= 2.5 mm).
2. sensitivity.csv     one-at-a-time ranges of P_i(2100) at Kampala and Arua around a central case
                       (SSP2-4.5, ERA5-adjusted baseline, cast 2000).
3. propagation.csv     P(initiation) and P(cover cracking) by year for members cast in 2000 and 2025.
4. cost_benefit.csv    break-even repair-to-concrete cost ratio for extra cover, members cast in 2025.

Propagation (indicative; parameters flagged in the manuscript for checking against the full texts):
  corrosion rate at 20 degC, V20 ~ lognormal, mean 2.0 um/yr, CoV 0.5 (sheltered carbonated concrete, DuraCrete-type);
  temperature: V = V20 [1 + K (T - 20)], K = 0.025 below 20 degC and 0.073 above (Stewart et al. 2011);
  cover cracking when corrosion penetration reaches x0 = 7.53 + 9.32 c / phi (um), phi = 12 mm (Alonso et al. 1998).
"""
import sys
from dataclasses import replace
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from carbonation import SPECS, Exposure, Samples, carbonation_depth_mm  # noqa: E402
from run_sites import (ROOT, SITES, YEARS, climate_arrays, co2_series,  # noqa: E402
                       complete_models, site_series)

OUT = ROOT / "results"
N = 50_000
CASES = {"no_change": ("ssp245", True), "SSP2-4.5": ("ssp245", False), "SSP5-8.5": ("ssp585", False)}
PHI_MM = 12.0
V20_MEAN, V20_COV = 2.0, 0.5
DISCOUNT = (0.01, 0.03, 0.05)


def tow_array(df, models, scen, midx, frozen):
    """(n, years) fraction of days with >= 2.5 mm rain for the sampled model of each realisation."""
    out = np.empty((len(models), len(YEARS)))
    base = (YEARS >= 1995) & (YEARS <= 2014)
    for i, m in enumerate(models):
        t = df[(df.model == m) & (df.scenario == scen)].set_index("year").reindex(YEARS).tow.to_numpy()
        if frozen:
            t = np.where(YEARS > 2014, t[base].mean(), t)
        out[i] = t
    return out[midx]


class Site:
    """Climate inputs for one site, cached per baseline/scenario."""

    def __init__(self, name, era5):
        self.name = name
        self.df = site_series(name)
        self.models = complete_models(self.df)
        e = era5[(era5.site == name) & era5.year.between(1995, 2014)]
        self.bases = {"raw": None, "era5_delta": (e.tas.mean(), e.hurs.mean())}
        self.elev = SITES[name][2]

    def climate(self, case, baseline, midx):
        scen, frozen = CASES[case]
        T, H = climate_arrays(self.df, self.models, scen, midx, frozen, self.bases[baseline])
        return T, H, co2_series(scen, frozen), tow_array(self.df, self.models, scen, midx, frozen)


def depth(site, spec, case, baseline, cast, exposure=Exposure(), n=N, seed=42, model=None, elev=None):
    rng = np.random.default_rng(seed)
    p = Samples(n, rng).draw(spec)
    midx = rng.integers(0, len(site.models), n)
    if model is not None:
        midx[:] = site.models.index(model)
    T, H, C, W = site.climate(case, baseline, midx)
    k = YEARS >= cast
    d = carbonation_depth_mm(p, YEARS[k], T[:, k], H[:, k], C[k], site.elev if elev is None else elev,
                             exposure, tow=W[:, k])
    return p, d, T[:, k], YEARS[k], rng


def crack_prob(d, cover, T, rng):
    """P(initiation) and P(cover cracking) by year given depth paths and cover."""
    init = d >= cover[:, None]
    sig = np.sqrt(np.log(1 + V20_COV ** 2))
    v20 = rng.lognormal(np.log(V20_MEAN) - sig ** 2 / 2, sig, d.shape[0])
    K = np.where(T < 20, 0.025, 0.073)
    pen = np.cumsum(v20[:, None] * np.maximum(1 + K * (T - 20), 0) * init, axis=1)  # um
    x0 = 7.53 + 9.32 * cover / PHI_MM
    return init.mean(axis=0), (pen >= x0[:, None]).mean(axis=0)


def rain_exposure(sites):
    rows = []
    exps = {"sheltered": Exposure(), "vertical, rain-exposed": Exposure(sheltered=False, p_splash_rain=0.25),
            "horizontal, rain-exposed": Exposure(sheltered=False, p_splash_rain=1.0)}
    for s in sites:
        for spec_key, spec in SPECS.items():
            for case in CASES:
                for ex_name, ex in exps.items():
                    p, d, _, yrs, _ = depth(s, spec, case, "era5_delta", 2000, ex)
                    rows.append((s.name, spec_key, case, ex_name, float((d[:, -1] >= p["cover_mm"]).mean()),
                                 float(d[:, -1].mean())))
        print("rain", s.name, flush=True)
    return pd.DataFrame(rows, columns=["site", "concrete", "case", "exposure", "p_init_2100", "mean_depth_2100_mm"])


def p2100(site, spec, case="SSP2-4.5", baseline="era5_delta", exposure=Exposure(), model=None, elev=None):
    p, d, _, _, _ = depth(site, spec, case, baseline, 2000, exposure, model=model, elev=elev)
    return float((d[:, -1] >= p["cover_mm"]).mean())


def sensitivity(sites):
    rows = []
    for s in sites:
        for spec_key in ("design_blended", "asbuilt_blended"):
            sp = SPECS[spec_key]
            base = p2100(s, sp)
            cure = (3, 14) if spec_key.startswith("design") else (1, 7)
            per_model = [p2100(s, sp, model=m) for m in s.models]
            var = {
                "Emission scenario (no change / SSP5-8.5)": (p2100(s, sp, "no_change"), p2100(s, sp, "SSP5-8.5")),
                "Climate model (lowest / highest)": (min(per_model), max(per_model)),
                "Humidity baseline (raw downscaled)": (p2100(s, sp, baseline="raw"),) * 2,
                "Blended-cement factor (2.6 / 4.4)": (p2100(s, replace(sp, blend_factor_high=sp.blend_factor_low)),
                                                      p2100(s, replace(sp, blend_factor_low=sp.blend_factor_high))),
                f"w/c ({sp.wc_low:.2f} / {sp.wc_high:.2f})": (p2100(s, replace(sp, wc_high=sp.wc_low)),
                                                              p2100(s, replace(sp, wc_low=sp.wc_high))),
                "Mean cover (+5 / −5 mm)": (p2100(s, replace(sp, cover_mean_mm=sp.cover_mean_mm + 5)),
                                                p2100(s, replace(sp, cover_mean_mm=sp.cover_mean_mm - 5))),
                f"Curing ({cure[1]} / {cure[0]} days)": (
                    p2100(s, replace(sp, curing_days_low=cure[1], curing_days_high=cure[1])),
                    p2100(s, replace(sp, curing_days_low=cure[0], curing_days_high=cure[0]))),
                "Urban CO₂ factor (1.0 / 1.2)": (p2100(s, sp, exposure=Exposure(urban_co2_factor=1.0)),
                                                      p2100(s, sp, exposure=Exposure(urban_co2_factor=1.2))),
                "Activation energy (30 / 50 kJ/mol)": (p2100(s, sp, exposure=Exposure(activation_j=30000.0)),
                                                       p2100(s, sp, exposure=Exposure(activation_j=50000.0))),
                "Elevation correction off (sea level)": (p2100(s, sp, elev=0.0),) * 2,
            }
            for k, (lo, hi) in var.items():
                rows.append((s.name, spec_key, k, base, lo, hi))
        print("sens", s.name, flush=True)
    return pd.DataFrame(rows, columns=["site", "concrete", "factor", "p_base", "p_low", "p_high"])


def propagation(sites):
    rows = []
    for s in sites:
        for spec_key in ("design_CEM_I", "design_blended", "asbuilt_blended"):
            for case in CASES:
                for cast in (2000, 2025):
                    p, d, T, yrs, rng = depth(s, SPECS[spec_key], case, "era5_delta", cast)
                    pi, pc = crack_prob(d, p["cover_mm"], T, rng)
                    for y, a, b in zip(yrs, pi, pc):
                        if y % 5 == 0:
                            rows.append((s.name, spec_key, case, cast, y, a, b))
        print("prop", s.name, flush=True)
    return pd.DataFrame(rows, columns=["site", "concrete", "case", "cast_year", "year", "p_init", "p_crack"])


def cost_benefit(sites, dcs=(0, 2, 5, 8, 10, 15, 20), cast=2025):
    """Expected discounted cracking probability per m2 of surface vs extra cover.

    Break-even ratio R* = (extra concrete volume per m2) / (reduction in discounted P(crack)),
    i.e. adaptation pays off if patch-repair cost per m2 / in-place concrete cost per m3 exceeds R*.
    """
    rows = []
    for s in sites:
        spec = SPECS["design_blended"]
        for case in CASES:
            p, d, T, yrs, rng = depth(s, spec, case, "era5_delta", cast)
            state = rng.bit_generator.state
            for r in DISCOUNT:
                disc = (1 + r) ** -(yrs - cast)
                dd = {}
                for dc in dcs:
                    rng.bit_generator.state = state  # same corrosion-rate draws for every cover
                    _, pc = crack_prob(d, p["cover_mm"] + dc, T, rng)
                    dd[dc] = float(np.sum(np.diff(np.concatenate([[0.0], pc])) * disc))
                for dc in dcs:
                    gain = dd[0] - dd[dc]
                    rstar = (dc / 1000.0) / gain if dc > 0 and gain > 0 else np.nan
                    rows.append((s.name, case, r, dc, dd[dc], gain, rstar))
        print("cb", s.name, flush=True)
    return pd.DataFrame(rows, columns=["site", "case", "discount", "extra_cover_mm", "disc_p_crack",
                                       "reduction", "breakeven_ratio"])


def main():
    era5 = pd.read_csv(ROOT / "data" / "processed" / "era5_sites_annual.csv")
    sites = [Site(n, era5) for n in SITES]
    print("models", sites[0].models, flush=True)
    rain_exposure(sites).to_csv(OUT / "rain_exposure.csv", index=False)
    sensitivity([s for s in sites if s.name in ("Kampala", "Arua")]).to_csv(OUT / "sensitivity.csv", index=False)
    propagation(sites).to_csv(OUT / "propagation.csv", index=False)
    cost_benefit(sites).to_csv(OUT / "cost_benefit.csv", index=False)


if __name__ == "__main__":
    main()
