"""Urban heat island (UHI) sensitivity at the six cities.

A constant urban air-temperature excess dT (0, 1, 2, 3 degC) is added to every year of the
ERA5-adjusted climate. Relative humidity is lowered consistently, holding vapour pressure fixed:
RH' = RH * es(T) / es(T + dT), with es the Magnus saturation vapour pressure.
Outputs results/urban_heat.csv: P_i(2100) for members cast in 2000, and the extra cover that offsets
SSP5-8.5 over a 50-year life for members cast in 2025, by city, concrete class and dT.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from adaptation import solve  # noqa: E402
from carbonation import SPECS, Exposure, Samples, carbonation_depth_mm  # noqa: E402
from site_extensions import CASES, Site  # noqa: E402
from run_sites import ROOT, SITES, YEARS  # noqa: E402

N = 50_000
UHI = (0.0, 1.0, 2.0, 3.0)


def es(t):
    return 6.112 * np.exp(17.67 * t / (t + 243.5))


def depths(site, spec, case, dT, cast):
    rng = np.random.default_rng(42)
    p = Samples(N, rng).draw(spec)
    midx = rng.integers(0, len(site.models), N)
    T, H, C, _ = site.climate(case, "era5_delta", midx)
    H = np.clip(H * es(T) / es(T + dT), 1.0, 99.0)
    T = T + dT
    k = YEARS >= cast
    d = carbonation_depth_mm(p, YEARS[k], T[:, k], H[:, k], C[k], site.elev, Exposure())
    return p, d, YEARS[k]


def main():
    era5 = pd.read_csv(ROOT / "data" / "processed" / "era5_sites_annual.csv")
    rows = []
    for name in SITES:
        s = Site(name, era5)
        for spec_key in ("design_CEM_I", "design_blended", "asbuilt_blended"):
            spec = SPECS[spec_key]
            for dT in UHI:
                pis = {}
                for case in CASES:
                    p, d, _ = depths(s, spec, case, dT, 2000)
                    pis[case] = float((d[:, -1] >= p["cover_mm"]).mean())
                p0, d0, y0 = depths(s, spec, "no_change", 0.0, 2025)
                p5, d5, _ = depths(s, spec, "SSP5-8.5", dT, 2025)
                i = y0 == 2075
                ref = float((d0[:, i][:, 0] >= p0["cover_mm"]).mean())  # no climate change, no UHI
                dd = d5[:, i][:, 0]
                dc = solve(lambda x: float((dd >= p5["cover_mm"] + x).mean()) - ref)
                rows.append((name, spec_key, dT, pis["no_change"], pis["SSP2-4.5"], pis["SSP5-8.5"], dc))
        print(name, flush=True)
    out = pd.DataFrame(rows, columns=["site", "concrete", "uhi_degC", "p_no_change", "p_ssp245", "p_ssp585",
                                      "dc_offset_2075_ssp585_mm"])
    out.to_csv(ROOT / "results" / "urban_heat.csv", index=False)
    print(out[out.concrete == "design_blended"].round(3).to_string())


if __name__ == "__main__":
    main()
