"""Adaptation: extra cover needed for new construction under climate change.

For a member cast in 2025 at each site, two cover requirements are found for each
concrete class, baseline and scenario, at the end of a 50-year design working life
(2075) and at 2100:

  dc_offset   extra cover (mm) that brings P_i under the scenario back to its
              no-climate-change value (same concrete, same samples);
  cover_p10   mean cover (mm) needed to keep P_i <= 0.10, the target used by
              Val et al. (2025), with the cover scatter of that concrete class.

Cover enters only through the limit state, so both are found on the sampled depths
by bisection; common random numbers keep scenario differences free of sampling noise.

Output: results/adaptation.csv
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from carbonation import SPECS, Exposure, Samples, carbonation_depth_mm  # noqa: E402
from run_sites import (ROOT, SITES, YEARS, climate_arrays, co2_series,  # noqa: E402
                       complete_models, site_series)

CAST = 2025
CHECK_YEARS = (2075, 2100)
TARGET = 0.10
N = 100_000
CASES = (("no_change", "ssp245", True), ("SSP2-4.5", "ssp245", False), ("SSP5-8.5", "ssp585", False))


def p_init(depth, cover):
    return float((depth >= cover).mean())


def solve(f, lo=0.0, hi=150.0, tol=0.05):
    """Smallest x in [lo, hi] with f(x) <= 0 for decreasing f."""
    if f(lo) <= 0:
        return lo
    if f(hi) > 0:
        return np.nan
    while hi - lo > tol:
        mid = (lo + hi) / 2
        lo, hi = (lo, mid) if f(mid) <= 0 else (mid, hi)
    return hi


def run_site(site, era5):
    df = site_series(site)
    models = complete_models(df)
    e = era5[(era5.site == site) & era5.year.between(1995, 2014)]
    rows = []
    for bl, eb in (("raw", None), ("era5_delta", (e.tas.mean(), e.hurs.mean()))):
        for spec_key, spec in SPECS.items():
            rng = np.random.default_rng(42)
            p = Samples(N, rng).draw(spec)
            midx = rng.integers(0, len(models), N)
            k = YEARS >= CAST
            depth = {}
            for case, scen, frozen in CASES:
                T, H = climate_arrays(df, models, scen, midx, frozen, eb)
                d = carbonation_depth_mm(p, YEARS[k], T[:, k], H[:, k], co2_series(scen, frozen)[k],
                                         SITES[site][2], Exposure())
                depth[case] = {y: d[:, YEARS[k] == y][:, 0] for y in CHECK_YEARS}
            cover = p["cover_mm"]
            dev = cover - spec.cover_mean_mm  # cover scatter kept when the mean is moved
            for y in CHECK_YEARS:
                p0 = p_init(depth["no_change"][y], cover)
                for case, _, _ in CASES:
                    d = depth[case][y]
                    pc = p_init(d, cover)
                    dc = solve(lambda x: p_init(d, cover + x) - p0) if case != "no_change" else 0.0
                    c10 = solve(lambda c: p_init(d, np.maximum(c + dev, spec.cover_min_mm)) - TARGET, 0.0, 200.0)
                    rows.append((site, bl, spec_key, case, y, pc, p0, dc, c10, len(models)))
    return rows


def main():
    era5 = pd.read_csv(ROOT / "data" / "processed" / "era5_sites_annual.csv")
    rows = []
    for s in SITES:
        rows += run_site(s, era5)
        print(s, "done", flush=True)
    res = pd.DataFrame(rows, columns=["site", "baseline", "concrete", "case", "year", "p_init",
                                      "p_init_no_change", "dc_offset_mm", "cover_p10_mm", "n_models"])
    res.to_csv(ROOT / "results" / "adaptation.csv", index=False)
    show = res[(res.baseline == "era5_delta") & (res.concrete != "asbuilt_blended")]
    print(show.pivot_table(index=["concrete", "site"], columns=["year", "case"],
                           values=["dc_offset_mm", "cover_p10_mm"]).round(1).to_string())


if __name__ == "__main__":
    main()
