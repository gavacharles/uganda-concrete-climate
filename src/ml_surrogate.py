"""ML case 2: gradient-boosting surrogate of the probabilistic carbonation model.

Training data are Monte Carlo realisations from the physical model (six cities, three climate
cases, three concrete classes, members cast in 2000, ERA5-adjusted baseline). Each row holds the
sampled inputs and the realisation's mean climate; the label is corrosion initiation by 2100.

Outputs
  results/ml_surrogate_metrics.csv     held-out AUC and Brier score, and leave-one-city-out AUC
  results/ml_surrogate_importance.csv  permutation importance (drop in AUC) per input
  results/ml_surrogate_pdp.csv         partial dependence of P(initiation) on cover and on mean temperature
"""
import sys
import zlib
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.inspection import partial_dependence, permutation_importance
from sklearn.metrics import brier_score_loss, roc_auc_score

sys.path.insert(0, str(Path(__file__).parent))
from carbonation import SPECS, Exposure, Samples, carbonation_depth_mm, co2_kg_m3  # noqa: E402
from run_sites import ROOT, SITES, YEARS  # noqa: E402
from site_extensions import CASES, Site  # noqa: E402

N = 20_000
FEATURES = ["wc", "blend", "cover_mm", "curing_days", "kt", "eps", "temp_mean", "rh_mean", "co2_mass_mean",
            "elevation_m"]
LABELS = {"wc": "w/c ratio", "blend": "Blended-cement factor", "cover_mm": "Cover depth",
          "curing_days": "Curing duration", "kt": "Test-method factor k_t", "eps": "Error term ε_t",
          "temp_mean": "Mean temperature", "rh_mean": "Mean relative humidity",
          "co2_mass_mean": "Mean CO₂ concentration", "elevation_m": "Elevation"}


def build():
    era5 = pd.read_csv(ROOT / "data" / "processed" / "era5_sites_annual.csv")
    frames = []
    for name in SITES:
        s = Site(name, era5)
        for spec_key, spec in SPECS.items():
            for case in CASES:
                rng = np.random.default_rng(zlib.crc32(f"{name}|{spec_key}|{case}".encode()))
                p = Samples(N, rng).draw(spec)
                midx = rng.integers(0, len(s.models), N)
                T, H, C, _ = s.climate(case, "era5_delta", midx)
                k = YEARS >= 2000
                d = carbonation_depth_mm(p, YEARS[k], T[:, k], H[:, k], C[k], s.elev, Exposure())
                cs = co2_kg_m3(C[k][None, :], T[:, k], s.elev) * 1e3  # g/m3
                frames.append(pd.DataFrame({
                    "site": name, "concrete": spec_key, "case": case,
                    "wc": p["wc"], "blend": p["blend"], "cover_mm": p["cover_mm"], "curing_days": p["curing_days"],
                    "kt": p["kt"], "eps": p["eps"] * 1e11, "temp_mean": T[:, k].mean(axis=1),
                    "rh_mean": H[:, k].mean(axis=1), "co2_mass_mean": cs.mean(axis=1), "elevation_m": s.elev,
                    "initiated": (d[:, -1] >= p["cover_mm"]).astype(int)}))
        print("data", name, flush=True)
    return pd.concat(frames, ignore_index=True)


def main():
    df = build()
    rng = np.random.default_rng(0)
    test = rng.random(len(df)) < 0.2
    X, y = df[FEATURES], df.initiated
    model = HistGradientBoostingClassifier(max_iter=400, learning_rate=0.08, max_leaf_nodes=63,
                                           random_state=0).fit(X[~test], y[~test])
    pr = model.predict_proba(X[test])[:, 1]
    rows = [("all cities, 20% held out", roc_auc_score(y[test], pr), brier_score_loss(y[test], pr), int(test.sum()))]
    for name in SITES:  # spatial transfer: train without one city, test on it
        m = df.site == name
        mdl = HistGradientBoostingClassifier(max_iter=400, learning_rate=0.08, max_leaf_nodes=63,
                                             random_state=0).fit(X[~m], y[~m])
        q = mdl.predict_proba(X[m])[:, 1]
        rows.append((f"leave out {name}", roc_auc_score(y[m], q), brier_score_loss(y[m], q), int(m.sum())))
        print("loco", name, flush=True)
    pd.DataFrame(rows, columns=["test", "auc", "brier", "n"]).to_csv(ROOT / "results" / "ml_surrogate_metrics.csv",
                                                                    index=False)
    sub = rng.choice(np.flatnonzero(test), 60_000, replace=False)
    imp = permutation_importance(model, X.iloc[sub], y.iloc[sub], scoring="roc_auc", n_repeats=5, random_state=0)
    pd.DataFrame({"feature": FEATURES, "label": [LABELS[f] for f in FEATURES], "importance": imp.importances_mean,
                  "sd": imp.importances_std}).sort_values("importance", ascending=False).to_csv(
        ROOT / "results" / "ml_surrogate_importance.csv", index=False)
    pdp = []
    for f in ("cover_mm", "temp_mean"):
        r = partial_dependence(model, X.iloc[sub], [f], grid_resolution=40, kind="average")
        for v, a in zip(r["grid_values"][0], r["average"][0]):
            pdp.append((f, v, a))
    pd.DataFrame(pdp, columns=["feature", "value", "p_initiation"]).to_csv(ROOT / "results" / "ml_surrogate_pdp.csv",
                                                                          index=False)
    print(pd.read_csv(ROOT / "results" / "ml_surrogate_metrics.csv").round(3))
    print(pd.read_csv(ROOT / "results" / "ml_surrogate_importance.csv").round(4))


if __name__ == "__main__":
    main()
