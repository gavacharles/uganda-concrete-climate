"""ML case 3: independent check of the carbonation model against measured data.

Data: Database for accelerated and natural carbonation in fly ash concrete (Mendeley Data,
doi:10.17632/rchp48n97y.2, CC BY 4.0), 831 tests from 18 published sources. Only natural exposure
(CO2 <= 0.1 %) is used. The target is the carbonation coefficient k = depth / sqrt(years).

1. fib check: for each natural-exposure test, the fib model (CEM I resistance from w/b, k_t = 1.25,
   eps_t = 1e-11, curing and humidity functions, sheltered) predicts k; compared with measured k for
   plain Portland cement mixes.
2. Implied blended-cement factor: for fly-ash mixes, the multiplier on R_inv that reproduces the
   measured k, by fly-ash content, compared with the 2.6-4.4 used for Ugandan pozzolanic cements.
3. ML model: gradient boosting of k on mix and exposure variables, validated by leaving out each
   source study in turn (grouped cross-validation).

Outputs: results/ml_carbonation_fib_check.csv, ml_carbonation_blend.csv, ml_carbonation_cv.csv
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import GroupKFold

sys.path.insert(0, str(Path(__file__).parent))
from carbonation import M_CO2, R_GAS, k_e, rinv_mean_cem1  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SEC = 365.25 * 24 * 3600
FEATS = ["fa_frac", "binder", "wb", "curing_days", "temp", "rh", "co2_pct"]


def load():
    raw = pd.read_csv(ROOT / "data" / "raw" / "carbonation_db" / "mendeley_rchp48n97y_v2.csv", encoding="latin1",
                      header=None, skiprows=1)
    names = ["source", "sn", "mix", "c_cao", "c_sio2", "c_fe2o3", "c_al2o3", "fa_cao", "fa_sio2", "fa_fe2o3",
             "fa_al2o3", "fly_ash", "cement", "water", "wc", "curing_days", "curing_rh", "temp", "rh", "co2_pct",
             "duration_days", "depth_mm"]
    d = raw.iloc[:, :22]
    d.columns = names
    d["source"] = d.source.ffill()
    for c in names[3:]:
        d[c] = pd.to_numeric(d[c], errors="coerce")
    d = d.dropna(subset=["cement", "water", "duration_days", "depth_mm", "rh", "temp", "co2_pct"])
    d["binder"] = d.cement + d.fly_ash.fillna(0)
    d["fa_frac"] = d.fly_ash.fillna(0) / d.binder
    d["wb"] = d.water / d.binder
    d["years"] = d.duration_days / 365.25
    d["k_obs"] = d.depth_mm / np.sqrt(d.years)
    return d


def fib_k(d, mult=1.0):
    """Mean fib carbonation coefficient (mm / sqrt(yr)) for the test conditions, sheltered, sea level."""
    cs = d.co2_pct / 100 * M_CO2 * 101325 / (R_GAS * (d.temp + 273.15))  # kg/m3
    kc = (np.maximum(d.curing_days, 1) / 7.0) ** -0.567
    rinv = rinv_mean_cem1(d.wb.to_numpy()) * 1e-11 * mult
    return np.sqrt(2 * k_e(d.rh) * kc * (1.25 * rinv + 1e-11) * cs * SEC) * 1000


def main():
    d = load()
    nat = d[(d.co2_pct <= 0.1) & (d.years >= 0.25)].copy()
    print("natural tests", len(nat), "sources", nat.source.nunique(), flush=True)
    nat["k_fib"] = fib_k(nat)

    # 1. fib check on plain Portland cement mixes
    pc = nat[nat.fa_frac == 0]
    ratio = (pc.k_obs / pc.k_fib).replace([np.inf, -np.inf], np.nan).dropna()
    fib = pd.DataFrame([{
        "n": len(pc), "sources": pc.source.nunique(), "median_obs_over_fib": ratio.median(),
        "p25": ratio.quantile(0.25), "p75": ratio.quantile(0.75),
        "share_within_factor_2": float(((ratio > 0.5) & (ratio < 2)).mean()),
        "r2_log": r2_score(np.log1p(pc.k_obs), np.log1p(pc.k_fib))}])
    fib.to_csv(ROOT / "results" / "ml_carbonation_fib_check.csv", index=False)
    print(fib.round(3).T, flush=True)

    # 2. implied blended-cement multiplier for fly-ash mixes (relative to the fib CEM I value, with a
    #    source-specific correction from that source's own Portland mixes where available)
    fa = nat[(nat.fa_frac > 0) & (nat.k_obs > 0)].copy()
    cs = fa.co2_pct / 100 * M_CO2 * 101325 / (R_GAS * (fa.temp + 273.15))
    kc = (np.maximum(fa.curing_days, 1) / 7.0) ** -0.567
    need = ((fa.k_obs / 1000) ** 2 / (2 * k_e(fa.rh) * kc * cs * SEC) - 1e-11) / 1.25
    fa["mult_raw"] = need / (rinv_mean_cem1(fa.wb.to_numpy()) * 1e-11)
    corr = (pc.assign(r=(pc.k_obs / pc.k_fib) ** 2).groupby("source").r.median())
    fa["mult_adj"] = fa.mult_raw / fa.source.map(corr)
    fa["fa_bin"] = pd.cut(fa.fa_frac, [0, 0.2, 0.3, 0.4, 1.0], labels=["<20%", "20-30%", "30-40%", ">40%"])
    blend = fa.groupby("fa_bin", observed=True).agg(
        n=("mult_raw", "size"), median_mult=("mult_raw", "median"),
        p25=("mult_raw", lambda x: x.quantile(0.25)), p75=("mult_raw", lambda x: x.quantile(0.75)),
        median_mult_source_adjusted=("mult_adj", "median"), n_adjusted=("mult_adj", lambda x: int(x.notna().sum())))
    blend.to_csv(ROOT / "results" / "ml_carbonation_blend.csv")
    print(blend.round(2), flush=True)

    # 3. ML model of k, leave-source-out validation
    X, y, g = nat[FEATS], nat.k_obs, nat.source
    pred = np.full(len(nat), np.nan)
    nfold = min(nat.source.nunique(), 10)
    for tr, te in GroupKFold(nfold).split(X, y, g):
        m = HistGradientBoostingRegressor(max_iter=300, learning_rate=0.05, min_samples_leaf=10,
                                          random_state=0).fit(X.iloc[tr], y.iloc[tr])
        pred[te] = m.predict(X.iloc[te])
    cv = pd.DataFrame([
        {"model": "ML, leave-source-out", "r2": r2_score(y, pred), "mae_mm_per_sqrt_yr": mean_absolute_error(y, pred)},
        {"model": "fib (CEM I resistance, all mixes)", "r2": r2_score(y, nat.k_fib),
         "mae_mm_per_sqrt_yr": mean_absolute_error(y, nat.k_fib)},
        {"model": "fib x source-free FA factor", "r2": np.nan, "mae_mm_per_sqrt_yr": np.nan}])
    # fib with a single fly-ash multiplier from the 20-40 % bins applied to FA mixes
    mfa = float(fa[(fa.fa_frac > 0.2) & (fa.fa_frac <= 0.4)].mult_raw.median())
    kf = np.where(nat.fa_frac > 0, fib_k(nat, mfa), nat.k_fib)
    cv.loc[2] = ["fib with fitted fly-ash factor %.1f" % mfa, r2_score(y, kf), mean_absolute_error(y, kf)]
    cv.to_csv(ROOT / "results" / "ml_carbonation_cv.csv", index=False)
    print(cv.round(3), flush=True)
    nat.assign(k_ml_cv=pred).to_csv(ROOT / "results" / "ml_carbonation_natural.csv", index=False)


if __name__ == "__main__":
    main()
