"""ML case 1: building-level probability of being multi-storey (two or more storeys, the RC-frame proxy).

Labels: OpenStreetMap buildings with a building:levels tag (data/processed/osm_building_levels.csv),
matched to the nearest GHS-OBAT footprint within ~10 m. Features: footprint area, perimeter, shape
factor, use, GHS-OBAT neighbourhood height and epoch, local building density and mean footprint in
~220 m bins, and distance to the nearest of 16 towns. Model: gradient boosting, evaluated with
spatially blocked cross-validation (0.05 deg tiles). The fitted model is applied to all 22.5 million
footprints to estimate multi-storey buildings per grid cell and epoch.

Outputs
  results/ml_buildings_cv.csv          AUC and average precision per fold
  results/ml_buildings_epoch_check.csv OSM-labelled multi-storey share by GHS-OBAT epoch (Kampala cells)
  results/ml_buildings_cells.csv       expected multi-storey buildings per 0.25 deg cell and epoch
  results/ml_buildings_transfer.csv    geographic transfer test: trained in Kampala, tested in other towns
  results/ml_buildings_label_bias.csv  multi-storey share among OSM-tagged buildings vs predicted share of all
                                       buildings, within 8 km of each town
  data/processed/kampala_buildings_pred.csv.gz  per-building predictions for Greater Kampala
"""
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.model_selection import GroupKFold

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data" / "raw" / "ghs_obat_uga" / "GHS_OBAT_CSV_UGA_E2020_R2024A_V1_0.csv"
COLS = ["lon", "lat", "height", "shapefactor", "use", "epoch", "area", "perimeter"]
BIN = 0.002
TOWNS = {"Kampala": (0.347, 32.582), "Entebbe": (0.056, 32.464), "Jinja": (0.424, 33.204),
         "Mukono": (0.353, 32.755), "Masaka": (-0.333, 31.734), "Mbarara": (-0.607, 30.655),
         "Fort Portal": (0.654, 30.275), "Kasese": (0.183, 30.083), "Hoima": (1.431, 31.352),
         "Arua": (3.020, 30.911), "Gulu": (2.775, 32.299), "Lira": (2.249, 32.900), "Soroti": (1.715, 33.611),
         "Mbale": (1.082, 34.175), "Tororo": (0.693, 34.181), "Kabale": (-1.249, 29.990)}
FEATS = ["log_area", "perimeter", "shapefactor", "use", "height", "epoch", "dens", "bin_mean_area", "dist_town_km"]


def chunks():
    for c in pd.read_csv(SRC, usecols=COLS, chunksize=2_000_000, dtype={"use": "float32"}):
        yield c


def bin_key(lat, lon):
    return (np.floor(lat / BIN).astype(np.int64) * 100_000 + np.floor(lon / BIN).astype(np.int64))


def add_features(c, bins, tree_towns):
    k = bin_key(c.lat.to_numpy(), c.lon.to_numpy())
    b = bins.reindex(k)
    c = c.assign(log_area=np.log1p(c.area), dens=b["n"].to_numpy(), bin_mean_area=b["mean_area"].to_numpy())
    d, _ = tree_towns.query(np.c_[c.lat.to_numpy(), c.lon.to_numpy() * np.cos(np.radians(c.lat.to_numpy()))])
    return c.assign(dist_town_km=d * 111.32)


def main():
    # pass 1: local density and mean footprint per ~220 m bin
    parts = []
    for c in chunks():
        parts.append(pd.DataFrame({"k": bin_key(c.lat.to_numpy(), c.lon.to_numpy()), "a": c.area.to_numpy()})
                     .groupby("k").a.agg(["size", "sum"]))
    bins = pd.concat(parts).groupby(level=0).sum()
    bins = pd.DataFrame({"n": bins["size"], "mean_area": bins["sum"] / bins["size"]})
    print("bins", len(bins), flush=True)
    tw = np.array([(la, lo * np.cos(np.radians(la))) for la, lo in TOWNS.values()])
    tree_towns = cKDTree(tw)

    # pass 2: match OSM labels to footprints
    osm = pd.read_csv(ROOT / "data" / "processed" / "osm_building_levels.csv")
    tree = cKDTree(np.c_[osm.lat, osm.lon])
    matched = []
    for c in chunks():
        d, i = tree.query(np.c_[c.lat, c.lon], distance_upper_bound=0.0001)
        m = np.isfinite(d)
        if m.any():
            sub = c[m].assign(osm_idx=i[m], dist=d[m])
            matched.append(sub)
    lab = pd.concat(matched).sort_values("dist").drop_duplicates("osm_idx")
    lab = lab.assign(levels=osm.levels.to_numpy()[lab.osm_idx], osm_building=osm.building.to_numpy()[lab.osm_idx])
    lab = add_features(lab, bins, tree_towns)
    lab["y"] = (lab.levels >= 2).astype(int)
    print("labelled", len(lab), "multi", lab.y.sum(), flush=True)

    # direct check: multi-storey share by epoch among OSM-labelled buildings in the Kampala cells
    kla = lab[(lab.lat.between(0.0, 0.75)) & (lab.lon.between(32.25, 33.0))]
    chk = kla.groupby("epoch").agg(n=("y", "size"), osm_multi_share=("y", "mean"),
                                   ghs_tall_share=("height", lambda h: float((h >= 4.5).mean())))
    chk.to_csv(ROOT / "results" / "ml_buildings_epoch_check.csv")
    print(chk, flush=True)

    # spatially blocked CV
    X, y = lab[FEATS], lab.y
    groups = (np.floor(lab.lat / 0.05) * 1000 + np.floor(lab.lon / 0.05)).astype(int)
    cv = []
    for f, (tr, te) in enumerate(GroupKFold(5).split(X, y, groups)):
        mdl = HistGradientBoostingClassifier(max_iter=300, learning_rate=0.06, class_weight="balanced",
                                             random_state=0).fit(X.iloc[tr], y.iloc[tr])
        p = mdl.predict_proba(X.iloc[te])[:, 1]
        if y.iloc[te].nunique() == 2:
            cv.append((f, roc_auc_score(y.iloc[te], p), average_precision_score(y.iloc[te], p),
                       float(y.iloc[te].mean()), len(te)))
    pd.DataFrame(cv, columns=["fold", "auc", "avg_precision", "prevalence", "n"]).to_csv(
        ROOT / "results" / "ml_buildings_cv.csv", index=False)
    print(pd.DataFrame(cv, columns=["fold", "auc", "ap", "prev", "n"]).round(3), flush=True)

    # geographic transfer: train on the Kampala area only, test on labels near the other towns
    town_ll = np.array(list(TOWNS.values()))
    dk = np.hypot(lab.lat.to_numpy()[:, None] - town_ll[None, :, 0],
                  (lab.lon.to_numpy()[:, None] - town_ll[None, :, 1]) * np.cos(np.radians(town_ll[None, :, 0]))) * 111.32
    near = dk.argmin(axis=1)
    within = dk.min(axis=1) <= 8.0
    in_kla = lab.lat.between(0.0, 0.75).to_numpy() & lab.lon.between(32.25, 33.0).to_numpy()
    names = np.array(list(TOWNS))
    test = within & ~in_kla & (names[near] != "Kampala")
    mk = HistGradientBoostingClassifier(max_iter=300, learning_rate=0.06, random_state=0).fit(X[in_kla], y[in_kla])
    pt = mk.predict_proba(X[test])[:, 1]
    tr = [("trained Kampala area, tested other towns", int(test.sum()), int(y[test].sum()),
           roc_auc_score(y[test], pt), average_precision_score(y[test], pt), float(y[test].mean()), float(pt.mean()))]
    pd.DataFrame(tr, columns=["test", "n", "n_multi", "auc", "avg_precision", "observed_share", "predicted_share"]
                 ).to_csv(ROOT / "results" / "ml_buildings_transfer.csv", index=False)
    print(pd.read_csv(ROOT / "results" / "ml_buildings_transfer.csv").round(3), flush=True)
    tagged = pd.DataFrame({"town": names[near][within], "y": y[within]}).groupby("town").y.agg(["size", "mean"])

    # final model (unweighted, so probabilities stay calibrated to label prevalence) and national prediction
    mdl = HistGradientBoostingClassifier(max_iter=300, learning_rate=0.06, random_state=0).fit(X, y)
    out, kla_rows, town_sum = [], [], {}
    for c in chunks():
        c = add_features(c, bins, tree_towns)
        p = mdl.predict_proba(c[FEATS])[:, 1]
        kb = c.lat.between(0.10, 0.60) & c.lon.between(32.35, 32.85)
        kla_rows.append(c.loc[kb, ["lat", "lon", "epoch", "area", "use", "height"]].assign(p_multi=p[kb.to_numpy()]))
        dt = np.hypot(c.lat.to_numpy()[:, None] - town_ll[None, :, 0],
                      (c.lon.to_numpy()[:, None] - town_ll[None, :, 1]) * np.cos(np.radians(town_ll[None, :, 0]))) * 111.32
        w8 = dt.min(axis=1) <= 8.0
        for t, g in pd.DataFrame({"t": names[dt.argmin(axis=1)][w8], "p": p[w8]}).groupby("t").p:
            a = town_sum.setdefault(t, [0.0, 0])
            a[0] += g.sum()
            a[1] += len(g)
        g = pd.DataFrame({"glat": (np.floor(c.lat / 0.25) + 0.5) * 0.25, "glon": (np.floor(c.lon / 0.25) + 0.5) * 0.25,
                          "epoch": c.epoch, "p": p, "ghs_tall": (c.height >= 4.5).astype(float)})
        out.append(g.groupby(["glat", "glon", "epoch"]).agg(n=("p", "size"), ml_multi=("p", "sum"),
                                                            ghs_tall=("ghs_tall", "sum")))
        print("pred chunk", flush=True)
    pd.concat(kla_rows).to_csv(ROOT / "data" / "processed" / "kampala_buildings_pred.csv.gz", index=False)
    lb = pd.DataFrame({t: {"predicted_share_all_buildings": v[0] / v[1], "n_buildings": v[1]}
                       for t, v in town_sum.items()}).T
    lb = lb.join(tagged.rename(columns={"size": "n_tagged", "mean": "tagged_multi_share"}), how="left")
    lb.to_csv(ROOT / "results" / "ml_buildings_label_bias.csv")
    print(lb.round(3), flush=True)
    import joblib
    joblib.dump(mdl, ROOT / "results" / "ml_buildings_model.joblib")
    cells = pd.concat(out).groupby(level=[0, 1, 2]).sum().reset_index()
    cells.to_csv(ROOT / "results" / "ml_buildings_cells.csv", index=False)
    print(cells.groupby("epoch")[["n", "ml_multi", "ghs_tall"]].sum().round(0))


if __name__ == "__main__":
    main()
