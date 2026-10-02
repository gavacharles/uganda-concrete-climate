"""Manuscript figures 2-7 from the results files.

fig3_site_pinit.png        P_i(t) at six cities, specified blended concrete cast 2000
fig2_climate.png           warming at six cities, ensemble mean and model range
fig4_quality_vs_climate.png  P_i(2100) by concrete class and scenario at six cities
fig6_stock_map.png         share of RC buildings past initiation by 2100, and the climate increment
fig5_stock_trajectory.png  national share of RC buildings past initiation, 2030-2100
fig7_adaptation.png        extra cover that offsets the climate effect, by city
fig8_sensitivity.png       one-at-a-time sensitivity of P_i(2100) at Kampala and Arua
fig9_cracking.png          P(cover cracking) at six cities
fig10_new_construction.png RC buildings built 2020-2049: share past initiation, with and without extra cover

Palette: reference data-viz palette, categorical slots 1-2 for scenarios, neutral grey
for the no-change reference; sequential blue and orange ramps for the maps.
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.patches import Patch, Polygon

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
FIG = ROOT / "figures"

INK, INK2, MUTED, GRID = "#0b0b0b", "#52514e", "#8a8984", "#e4e3df"
CASE_COLOR = {"no_change": MUTED, "SSP2-4.5": "#2a78d6", "SSP5-8.5": "#eb6834"}
CASE_LABEL = {"no_change": "No climate change", "SSP2-4.5": "SSP2-4.5", "SSP5-8.5": "SSP5-8.5"}
CASE_STYLE = {"no_change": (0, (4, 2)), "SSP2-4.5": "-", "SSP5-8.5": "-"}
CONCRETE = {"design_CEM_I": "Specified, CEM I", "design_blended": "Specified, blended cement",
            "asbuilt_blended": "As built, blended cement"}
SITES = ["Kampala", "Mbale", "Gulu", "Arua", "Mbarara", "Kasese"]
SITE_LL = {"Kampala": (0.35, 32.58), "Mbale": (1.08, 34.18), "Gulu": (2.77, 32.30), "Arua": (3.02, 30.91),
           "Mbarara": (-0.61, 30.65), "Kasese": (0.18, 30.08)}
BLUE = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
ORANGE = ["#fde4d7", "#f9c3a7", "#f49d74", "#eb6834", "#c94f1f", "#9c3b15", "#6e290e"]

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 8.5, "axes.edgecolor": MUTED, "axes.labelcolor": INK2,
    "axes.linewidth": 0.6, "xtick.color": INK2, "ytick.color": INK2, "xtick.major.width": 0.6,
    "ytick.major.width": 0.6, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
    "axes.spines.top": False, "axes.spines.right": False, "axes.titlesize": 9, "axes.titleweight": "bold",
    "axes.titlecolor": INK, "axes.titlelocation": "left", "legend.frameon": False, "savefig.dpi": 300,
    "savefig.bbox": "tight", "savefig.facecolor": "white", "lines.solid_capstyle": "round", "axes.axisbelow": True,
})


def end_labels(ax, x, items, gap=0.07, fmt="{:.0%}"):
    """Direct end-of-line labels, nudged apart vertically so they never overlap."""
    items = sorted(items, key=lambda t: t[0])
    if items[-1][0] - items[0][0] < 0.03:  # near-identical values: one range label
        lo, hi = items[0][0], items[-1][0]
        txt = fmt.format(lo) if round(lo, 2) == round(hi, 2) else f"{fmt.format(lo)}–{fmt.format(hi)}"
        ax.text(x, hi, txt, color=INK2, fontsize=7.5, va="center")
        return
    ys = []
    for v, _ in items:
        ys.append(max(v, ys[-1] + gap) if ys else v)
    top = ax.get_ylim()[1] + 0.02
    if ys and ys[-1] > top:
        shift = ys[-1] - top
        ys = [y - shift for y in ys]
        for i in range(len(ys) - 2, -1, -1):
            ys[i] = min(ys[i], ys[i + 1] - gap)
    for (v, txt), y in zip(items, ys):
        ax.text(x, y, txt if txt else fmt.format(v), color=INK2, fontsize=7.5, va="center")


def legend_top(fig, cases=("no_change", "SSP2-4.5", "SSP5-8.5"), y=1.0, extra=()):
    h = [plt.Line2D([], [], color=CASE_COLOR[c], lw=2, ls=CASE_STYLE[c]) for c in cases] + [e[0] for e in extra]
    lab = [CASE_LABEL[c] for c in cases] + [e[1] for e in extra]
    fig.legend(h, lab, loc="lower center", bbox_to_anchor=(0.5, y), ncol=len(lab), fontsize=8.5,
               handlelength=2.4, columnspacing=1.6)


def fig2():
    d = pd.read_csv(RES / "site_pinit.csv")
    d = d[(d.baseline == "era5_delta") & (d.concrete == "design_blended") & (d.cast_year == 2000)]
    fig, axes = plt.subplots(2, 3, figsize=(7.2, 4.4), sharex=True, sharey=True)
    for ax, s in zip(axes.flat, SITES):
        ends = []
        ax.set_ylim(0, 1)
        for c in CASE_COLOR:
            g = d[(d.site == s) & (d.case == c)]
            ax.plot(g.year, g.p_init, color=CASE_COLOR[c], lw=1.6, ls=CASE_STYLE[c])
            ends.append((g[g.year == 2100].p_init.iat[0], None))
        end_labels(ax, 2102, ends)
        ax.set_title(s)
        ax.set_xlim(2000, 2100)
        ax.set_xticks([2000, 2050, 2100])
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
    for ax in axes[:, 0]:
        ax.set_ylabel("P(corrosion initiation)")
    legend_top(fig, y=0.99)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(FIG / "fig3_site_pinit.png")


def fig3():
    c = pd.read_csv(RES / "site_climate.csv")
    c = c.dropna(subset=["tas", "hurs"])
    full = c.groupby(["model", "scenario"]).year.nunique().unstack().min(axis=1)
    c = c[c.model.isin(full[full == 121].index)]  # only models with complete 1980-2100 series
    fig, axes = plt.subplots(2, 3, figsize=(7.2, 4.4), sharex=True, sharey=True)
    for ax, s in zip(axes.flat, SITES):
        for scen, case in (("ssp245", "SSP2-4.5"), ("ssp585", "SSP5-8.5")):
            g = c[(c.site == s) & (c.scenario == scen)]
            base = g[g.year.between(1995, 2014)].groupby("model").tas.mean()
            g = g.assign(anom=g.tas - g.model.map(base))
            sm = g.pivot_table(index="year", columns="model", values="anom").rolling(11, center=True,
                                                                                      min_periods=6).mean()
            ax.fill_between(sm.index, sm.min(axis=1), sm.max(axis=1), color=CASE_COLOR[case], alpha=0.15, lw=0)
            ax.plot(sm.index, sm.mean(axis=1), color=CASE_COLOR[case], lw=1.6)
            em = g.groupby("year").anom.mean()
            ax.text(2102, sm.mean(axis=1).dropna().iat[-1], f"+{em.loc[2081:2100].mean():.1f}",
                    color=INK2, fontsize=7.5, va="center")
        ax.axhline(0, color=MUTED, lw=0.6)
        ax.set_title(s)
        ax.set_xlim(1980, 2100)
        ax.set_xticks([1980, 2020, 2060, 2100])
    for ax in axes[:, 0]:
        ax.set_ylabel("Warming vs 1995–2014 (°C)")
    n = c.model.nunique()
    legend_top(fig, cases=("SSP2-4.5", "SSP5-8.5"), y=0.99,
               extra=((Patch(color=MUTED, alpha=0.3, lw=0), f"Shading: range of {n} models"),))
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(FIG / "fig2_climate.png")


def fig4():
    d = pd.read_csv(RES / "site_pinit.csv")
    d = d[(d.baseline == "era5_delta") & (d.cast_year == 2000) & (d.year == 2100)]
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.9), sharey=True)
    y = np.arange(len(SITES))[::-1]
    for ax, (k, lab) in zip(axes, CONCRETE.items()):
        g = d[d.concrete == k].pivot_table(index="site", columns="case", values="p_init").reindex(SITES)
        ax.hlines(y, g.min(axis=1), g.max(axis=1), color=GRID, lw=3, zorder=1)
        for c in CASE_COLOR:
            ax.scatter(g[c], y, s=34, color=CASE_COLOR[c], edgecolor="white", linewidth=1.2, zorder=3,
                       marker="D" if c == "no_change" else "o")
        ax.set_title(lab, fontsize=8.5)
        ax.set_xlim(-0.02, 1.02)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
        ax.set_xlabel("P(initiation) by 2100")
        ax.grid(axis="y", visible=False)
    axes[0].set_yticks(y)
    axes[0].set_yticklabels(SITES)
    h = [plt.Line2D([], [], color=CASE_COLOR[c], marker="D" if c == "no_change" else "o", ls="",
                    markersize=6, markeredgecolor="white") for c in CASE_COLOR]
    fig.legend(h, [CASE_LABEL[c] for c in CASE_COLOR], loc="lower center", bbox_to_anchor=(0.5, 0.98), ncol=3)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(FIG / "fig4_quality_vs_climate.png")


def draw_outline(ax):
    reg = json.loads((ROOT / "data" / "processed" / "uganda_region.geojson").read_text())
    lakes = json.loads((ROOT / "data" / "processed" / "uganda_lakes.geojson").read_text())

    def polys(geom):
        cs = geom["coordinates"]
        return cs if geom["type"] == "MultiPolygon" else [cs]

    for f in reg["features"]:
        uga = f["properties"].get("ADM0_A3") == "UGA"
        for p in polys(f["geometry"]):
            ax.add_patch(Polygon(p[0], closed=True, fill=False, ec=INK2 if uga else GRID,
                                 lw=0.9 if uga else 0.6, zorder=4))
    for f in lakes["features"]:
        for p in polys(f["geometry"]):
            ax.add_patch(Polygon(p[0], closed=True, fc="#eef3f8", ec="#b9c7d6", lw=0.4, zorder=3))


def fig5():
    s = pd.read_csv(RES / "stock_cells.csv")
    s = s[(s.concrete == "design_blended") & (s.year == 2100)]
    g = s.groupby(["glat", "glon", "case"])[["n_initiated", "n_buildings"]].sum().reset_index()
    g["share"] = g.n_initiated / g.n_buildings
    w = g.pivot_table(index=["glat", "glon"], columns="case", values="share").reset_index()
    nb = g[g.case == "SSP5-8.5"].set_index(["glat", "glon"]).n_buildings
    w["n"] = [nb.loc[(a, b)] for a, b in zip(w.glat, w.glon)]
    w = w[w.n >= 20]
    w["inc"] = (w["SSP5-8.5"] - w["no_change"]) * 100
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.9))
    panels = (("SSP5-8.5", "a  Share past initiation by 2100, SSP5-8.5", BLUE,
               [0, .2, .3, .4, .5, .6, .7, 1.0], lambda v: f"{v:.0%}"),
              ("inc", "b  Increase due to climate change (points)", ORANGE,
               [0, 10, 15, 20, 25, 30, 35, 60], lambda v: f"{v:.0f}"))
    for ax, (col, title, ramp, bounds, fmt) in zip(axes, panels):
        cmap, norm = ListedColormap(ramp), BoundaryNorm(bounds, len(ramp))
        for _, r in w.iterrows():
            ax.add_patch(plt.Rectangle((r.glon - 0.125, r.glat - 0.125), 0.25, 0.25,
                                       fc=cmap(norm(r[col])), ec="white", lw=0.4, zorder=2))
        draw_outline(ax)
        for nm, (la, lo) in SITE_LL.items():
            ax.plot(lo, la, "o", ms=3.5, mfc=INK, mec="white", mew=0.8, zorder=5)
            ax.text(lo + 0.12, la + 0.1, nm, fontsize=7, color=INK, zorder=5,
                    path_effects=[__import__("matplotlib.patheffects", fromlist=["x"]).withStroke(
                        linewidth=2, foreground="white")])
        ax.set_xlim(29.4, 35.2)
        ax.set_ylim(-1.6, 4.4)
        ax.set_aspect("equal")
        ax.grid(False)
        ax.set_xticks([30, 32, 34])
        ax.set_yticks([-1, 0, 1, 2, 3, 4])
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0f}°E"))
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{abs(v):.0f}°" + ("" if v == 0 else "N" if v > 0 else "S")))
        ax.set_title(title, fontsize=8.5)
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        cb = fig.colorbar(sm, ax=ax, orientation="horizontal", fraction=0.05, pad=0.09, ticks=bounds)
        cb.ax.set_xticklabels([fmt(b) for b in bounds], fontsize=7)
        cb.outline.set_visible(False)
    fig.tight_layout()
    fig.savefig(FIG / "fig6_stock_map.png")


def fig6():
    s = pd.read_csv(RES / "stock_summary.csv")
    bm = pd.read_csv(RES / "stock_by_model.csv") if (RES / "stock_by_model.csv").exists() else None
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.8), sharey=True)
    for ax, (k, lab) in zip(axes, CONCRETE.items()):
        ends = []
        ax.set_ylim(0, 1)
        if bm is not None and k == "design_blended":
            for c in ("SSP2-4.5", "SSP5-8.5", "no_change"):
                b = bm[bm.case == c].groupby("year").share_initiated.agg(["min", "max"])
                ax.fill_between(b.index, b["min"], b["max"], color=CASE_COLOR[c], alpha=0.16, lw=0)
        for c in CASE_COLOR:
            g = s[(s.concrete == k) & (s.case == c)].sort_values("year")
            ax.plot(g.year, g.share_initiated, color=CASE_COLOR[c], lw=1.6, ls=CASE_STYLE[c],
                    marker="o", ms=4, mec="white", mew=0.8)
            ends.append((g.share_initiated.iat[-1], None))
        end_labels(ax, 2103, ends)
        ax.set_title(lab, fontsize=8.5)
        ax.set_xticks([2030, 2050, 2070, 2100])
        ax.set_xlim(2025, 2100)
        ax.set_ylim(0, 1)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
    axes[0].set_ylabel("RC buildings past initiation")
    legend_top(fig, y=0.98)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(FIG / "fig5_stock_trajectory.png")


def fig7():
    a = pd.read_csv(RES / "adaptation.csv")
    a = a[(a.baseline == "era5_delta") & (a.concrete == "design_blended") & (a.case != "no_change")]
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.9), sharey=True, sharex=True)
    y = np.arange(len(SITES))[::-1]
    xmax = np.ceil(a.dc_offset_mm.max() / 2.5 + 0.6) * 2.5
    for ax, yr, title in zip(axes, (2075, 2100), ("a  50-year design life (2025–2075)", "b  To 2100")):
        g = a[a.year == yr].pivot_table(index="site", columns="case", values="dc_offset_mm").reindex(SITES)
        for j, c in enumerate(("SSP2-4.5", "SSP5-8.5")):
            yy = y + (0.19 if j == 0 else -0.19)
            ax.barh(yy, g[c], height=0.36, color=CASE_COLOR[c], edgecolor="white", linewidth=1)
            for v, q in zip(g[c], yy):
                ax.text(v + 0.3, q, f"{v:.1f}", fontsize=7, color=INK2, va="center")
        ax.set_title(title, fontsize=8.5)
        ax.set_xlabel("Extra cover to offset climate change (mm)")
        ax.grid(axis="y", visible=False)
        ax.set_xlim(0, xmax)
        ax.set_xticks(np.arange(0, xmax + 0.1, 5))
    axes[0].set_yticks(y)
    axes[0].set_yticklabels(SITES)
    fig.legend([Patch(color=CASE_COLOR[c]) for c in ("SSP2-4.5", "SSP5-8.5")], ["SSP2-4.5", "SSP5-8.5"],
               loc="lower center", bbox_to_anchor=(0.5, 0.97), ncol=2)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(FIG / "fig7_adaptation.png")


def fig8():
    s = pd.read_csv(RES / "sensitivity.csv")
    s = s[s.concrete == "design_blended"]
    fig, axes = plt.subplots(2, 1, figsize=(7.2, 5.8), sharex=True)
    for ax, site in zip(axes, ("Kampala", "Arua")):
        g = s[s.site == site].copy()
        g["lo"] = g[["p_low", "p_high"]].min(axis=1)
        g["hi"] = g[["p_low", "p_high"]].max(axis=1)
        base = g.p_base.iat[0]
        g["lo"] = np.minimum(g.lo, base)
        g["hi"] = np.maximum(g.hi, base)
        g = g.assign(rng=g.hi - g.lo).sort_values("rng")
        y = np.arange(len(g))
        ax.barh(y, g.hi - g.lo, left=g.lo, height=0.6, color="#2a78d6", edgecolor="white", linewidth=1)
        ax.axvline(base, color=INK, lw=1)
        for yy, lo, hi in zip(y, g.lo, g.hi):
            if abs(lo - base) > 0.005:
                ax.text(lo - 0.01, yy, f"{lo:.0%}", ha="right", va="center", fontsize=7, color=INK2)
            if abs(hi - base) > 0.005:
                ax.text(hi + 0.01, yy, f"{hi:.0%}", ha="left", va="center", fontsize=7, color=INK2)
        ax.set_yticks(y)
        ax.set_yticklabels(g.factor, fontsize=7.2)
        ax.set_title(f"{site} (central case {base:.0%})", fontsize=8.5)
        ax.set_xlim(0, 1.06)
        ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
        ax.grid(axis="y", visible=False)
    axes[1].set_xlabel("P(initiation) by 2100, specified concrete with blended cement, cast 2000")
    fig.tight_layout(h_pad=1.5)
    fig.savefig(FIG / "fig8_sensitivity.png")


def fig9():
    d = pd.read_csv(RES / "propagation.csv")
    d = d[(d.concrete == "design_blended") & (d.cast_year == 2000)]
    fig, axes = plt.subplots(2, 3, figsize=(7.2, 4.4), sharex=True, sharey=True)
    for ax, s in zip(axes.flat, SITES):
        ends = []
        ax.set_ylim(0, 1)
        for c in CASE_COLOR:
            g = d[(d.site == s) & (d.case == c)]
            ax.plot(g.year, g.p_crack, color=CASE_COLOR[c], lw=1.6, ls=CASE_STYLE[c])
            ends.append((g[g.year == 2100].p_crack.iat[0], None))
        end_labels(ax, 2102, ends)
        ax.set_title(s)
        ax.set_xlim(2000, 2100)
        ax.set_xticks([2000, 2050, 2100])
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
    for ax in axes[:, 0]:
        ax.set_ylabel("P(cover cracking)")
    legend_top(fig, y=0.99)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(FIG / "fig9_cracking.png")


def fig10():
    n = pd.read_csv(RES / "new_construction.csv")
    variants = (("asbuilt_blended", "As built"), ("design_blended", "As specified"),
                ("design_blended_plus8mm", "As specified + 8 mm cover"))
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.8), sharey=True)
    for ax, (v, lab) in zip(axes, variants):
        ends = []
        ax.set_ylim(0, 1)
        for c in CASE_COLOR:
            g = n[(n.variant == v) & (n.case == c)].sort_values("year")
            ax.plot(g.year, g.share_of_built, color=CASE_COLOR[c], lw=1.6, ls=CASE_STYLE[c],
                    marker="o", ms=3.5, mec="white", mew=0.8)
            ends.append((g.share_of_built.iat[-1], None))
        end_labels(ax, 2103, ends)
        ax.set_title(lab, fontsize=8.5)
        ax.set_xlim(2030, 2100)
        ax.set_xticks([2030, 2050, 2070, 2100])
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
    axes[0].set_ylabel("New RC buildings past initiation")
    legend_top(fig, y=0.98)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(FIG / "fig10_new_construction.png")


def fig11():
    """Outward growth of the building stock by construction epoch (GHS-OBAT)."""
    s = pd.read_csv(ROOT / "data" / "processed" / "stock_grid.csv")
    g = s.groupby(["glat", "glon", "epoch"]).n.sum().unstack(fill_value=0)
    area = (0.25 * 111.32) ** 2 * np.cos(np.radians(g.index.get_level_values(0)))
    dens = g.div(area, axis=0)
    labels = {1: "Before 1980", 2: "1980–1990", 3: "1990–2000", 4: "2000–2010", 5: "2010–2020"}
    bounds = [0, 1, 5, 10, 25, 50, 100, 700]
    cmap, norm = ListedColormap(BLUE), BoundaryNorm(bounds, len(BLUE))
    fig, axes = plt.subplots(2, 3, figsize=(7.2, 6.4))
    for ax, (ep, lab) in zip(axes.flat, labels.items()):
        for (la, lo), v in dens[ep].items():
            if v > 0:
                ax.add_patch(plt.Rectangle((lo - 0.125, la - 0.125), 0.25, 0.25, fc=cmap(norm(v)), ec="white",
                                           lw=0.3, zorder=2))
        draw_outline(ax)
        ax.plot(32.58, 0.35, "o", ms=2.5, mfc=INK, mec="white", mew=0.6, zorder=5)
        ax.set_xlim(29.4, 35.2)
        ax.set_ylim(-1.6, 4.4)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_visible(False)
        ax.grid(False)
        ax.set_title(f"{lab}  ({g[ep].sum() / 1e6:.1f} M)", fontsize=8.5)
    ax = axes.flat[5]
    tot = g[[1, 2, 3, 4, 5]].sum() / 1e6
    kla = g.loc[[i for i in g.index if 0.0 < i[0] < 0.75 and 32.25 < i[1] < 33.0], [1, 2, 3, 4, 5]].sum() / 1e6
    x = np.arange(5)
    ax.bar(x, tot - kla, color="#2a78d6", edgecolor="white", linewidth=1, label="Rest of Uganda")
    ax.bar(x, kla, bottom=tot - kla, color="#eb6834", edgecolor="white", linewidth=1, label="Kampala area")
    ax.set_xticks(x)
    ax.set_xticklabels(["<1980", "80s", "90s", "00s", "10s"], fontsize=7.5)
    ax.set_ylabel("Buildings (millions)")
    ax.set_title("New buildings by epoch", fontsize=8.5)
    ax.grid(axis="x", visible=False)
    ax.legend(fontsize=7, loc="upper left")
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    cb = fig.colorbar(sm, ax=axes[:, :], orientation="horizontal", fraction=0.035, pad=0.04, ticks=bounds,
                      shrink=0.6)
    cb.ax.set_xticklabels([str(b) for b in bounds], fontsize=7)
    cb.set_label("New buildings per km² in the epoch (all heights)", fontsize=8, color=INK2)
    cb.outline.set_visible(False)
    fig.savefig(FIG / "fig11_growth.png")


def fig12():
    """Urban heat island sensitivity."""
    u = pd.read_csv(RES / "urban_heat.csv")
    u = u[u.concrete == "design_blended"]
    cols = {"no_change": "p_no_change", "SSP2-4.5": "p_ssp245", "SSP5-8.5": "p_ssp585"}
    fig, axes = plt.subplots(2, 3, figsize=(7.2, 4.4), sharex=True, sharey=True)
    for ax, s in zip(axes.flat, SITES):
        g = u[u.site == s].sort_values("uhi_degC")
        ax.set_ylim(0, 1)
        ends = []
        for c, col in cols.items():
            ax.plot(g.uhi_degC, g[col], color=CASE_COLOR[c], lw=1.6, ls=CASE_STYLE[c], marker="o", ms=4,
                    mec="white", mew=0.8)
            ends.append((g[col].iat[-1], None))
        end_labels(ax, 3.12, ends)
        ax.set_title(s)
        ax.set_xlim(0, 3)
        ax.set_xticks([0, 1, 2, 3])
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
    for ax in axes[:, 0]:
        ax.set_ylabel("P(initiation) by 2100")
    for ax in axes[1]:
        ax.set_xlabel("Urban heat island (°C)")
    legend_top(fig, y=0.99)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(FIG / "fig12_urban_heat.png")


def fig13():
    """Machine-learning results: surrogate importance, building storeys by epoch, national counts, fib check."""
    fig, axes = plt.subplots(2, 2, figsize=(7.2, 5.8))
    imp = pd.read_csv(RES / "ml_surrogate_importance.csv").sort_values("importance")
    imp = imp[imp.importance > 0.001]
    ax = axes[0, 0]
    ax.barh(imp.label, imp.importance, color="#2a78d6", height=0.6, edgecolor="white")
    ax.set_xlabel("Drop in AUC when permuted")
    ax.set_title("a  Surrogate model: input importance", fontsize=8.5)
    ax.tick_params(axis="y", labelsize=7)
    ax.grid(axis="y", visible=False)
    chk = pd.read_csv(RES / "ml_buildings_epoch_check.csv")
    chk = chk[chk.epoch.between(1, 5)]
    x = np.arange(len(chk))
    ticks = ["<1980", "1980s", "1990s", "2000s", "2010s"]
    ax = axes[0, 1]
    ax.bar(x - 0.2, chk.ghs_tall_share, 0.38, color=MUTED, edgecolor="white", label="Height proxy (\u2265 4.5 m)")
    ax.bar(x + 0.2, chk.osm_multi_share, 0.38, color="#eb6834", edgecolor="white", label="OSM storeys (\u2265 2)")
    ax.set_xticks(x)
    ax.set_xticklabels(ticks, fontsize=7.5)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
    ax.set_ylim(0, 1.3)
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_title("b  Kampala: share multi-storey, by epoch", fontsize=8.5)
    ax.legend(fontsize=7, loc="upper center", ncol=2, handlelength=1.2)
    ax.grid(axis="x", visible=False)
    cells = pd.read_csv(RES / "ml_buildings_cells.csv")
    e = cells[cells.epoch.between(1, 5)].groupby("epoch")[["ghs_tall", "ml_multi"]].sum() / 1e3
    ax = axes[1, 0]
    ax.bar(x - 0.2, e.ghs_tall, 0.38, color=MUTED, edgecolor="white", label="Height proxy")
    ax.bar(x + 0.2, e.ml_multi, 0.38, color="#eb6834", edgecolor="white", label="ML estimate")
    ax.set_xticks(x)
    ax.set_xticklabels(ticks, fontsize=7.5)
    ax.set_ylabel("Buildings (thousands)")
    ax.set_title("c  Uganda: multi-storey buildings", fontsize=8.5)
    ax.legend(fontsize=7, loc="upper right")
    ax.grid(axis="x", visible=False)
    nat = pd.read_csv(RES / "ml_carbonation_natural.csv")
    pc = nat[(nat.fa_frac == 0) & (nat.k_obs > 0)]
    ax = axes[1, 1]
    ax.scatter(pc.k_fib, pc.k_obs, s=9, color="#2a78d6", alpha=0.6, edgecolor="none")
    lim = [0.3, 40]
    ax.plot(lim, lim, color=INK, lw=0.8)
    ax.plot(lim, [2 * v for v in lim], color=MUTED, lw=0.6, ls=(0, (3, 2)))
    ax.plot(lim, [v / 2 for v in lim], color=MUTED, lw=0.6, ls=(0, (3, 2)))
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(lim)
    ax.set_ylim(lim)
    ax.set_xlabel("fib model k (mm/\u221ayr)")
    ax.set_ylabel("Measured k (mm/\u221ayr)")
    ax.set_title("d  Measured vs fib, CEM I, natural", fontsize=8.5)
    for axis in (ax.xaxis, ax.yaxis):
        axis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:g}"))
    fig.tight_layout(h_pad=1.6, w_pad=1.4)
    fig.savefig(FIG / "fig13_machine_learning.png")


def fig_carbonation_check():
    """Paper A, Figure S3: measured natural carbonation of Portland cement concrete against the fib model."""
    nat = pd.read_csv(RES / "ml_carbonation_natural.csv")
    pc = nat[(nat.fa_frac == 0) & (nat.k_obs > 0)]
    fig, ax = plt.subplots(figsize=(3.6, 3.4))
    ax.scatter(pc.k_fib, pc.k_obs, s=10, color="#2a78d6", alpha=0.6, edgecolor="none")
    lim = [0.3, 40]
    ax.plot(lim, lim, color=INK, lw=0.8)
    for f in (2, 0.5):
        ax.plot(lim, [f * v for v in lim], color=MUTED, lw=0.6, ls=(0, (3, 2)))
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(lim)
    ax.set_ylim(lim)
    for axis in (ax.xaxis, ax.yaxis):
        axis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:g}"))
    ax.set_xlabel("fib model k (mm/\u221ayr)")
    ax.set_ylabel("Measured k (mm/\u221ayr)")
    fig.tight_layout()
    fig.savefig(FIG / "figS3_carbonation_check.png")


def figB2_buildings():
    """Paper B Figure 2: label bias by town, and multi-storey counts by epoch (proxy vs ML)."""
    lb = pd.read_csv(RES / "ml_buildings_label_bias.csv", index_col=0).dropna(subset=["tagged_multi_share"])
    lb = lb[lb.n_tagged >= 9].sort_values("predicted_share_all_buildings")
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.4), gridspec_kw={"width_ratios": [1.15, 1]})
    ax = axes[0]
    y = np.arange(len(lb))
    ax.hlines(y, lb[["predicted_share_all_buildings", "tagged_multi_share"]].min(axis=1),
              lb[["predicted_share_all_buildings", "tagged_multi_share"]].max(axis=1), color=GRID, lw=3, zorder=1)
    ax.scatter(lb.predicted_share_all_buildings, y, s=30, color="#2a78d6", edgecolor="white", zorder=3,
               label="Predicted, all buildings")
    ax.scatter(lb.tagged_multi_share, y, s=30, color="#eb6834", marker="D", edgecolor="white", zorder=3,
               label="OSM-tagged buildings")
    ax.set_yticks(y)
    ax.set_yticklabels([f"{t} ({int(n)})" for t, n in zip(lb.index, lb.n_tagged)], fontsize=7)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
    ax.set_xlim(0, 0.85)
    ax.set_xlabel("Share with two or more storeys (within 8 km)")
    ax.set_title("a  Tagged versus predicted, by town", fontsize=8.5)
    ax.legend(fontsize=7, loc="lower right")
    ax.grid(axis="y", visible=False)
    cells = pd.read_csv(RES / "ml_buildings_cells.csv")
    e = cells[cells.epoch.between(1, 5)].groupby("epoch")[["ghs_tall", "ml_multi"]].sum() / 1e3
    ax = axes[1]
    x = np.arange(len(e))
    ax.bar(x - 0.2, e.ghs_tall, 0.38, color=MUTED, edgecolor="white", label="Height proxy (\u2265 4.5 m)")
    ax.bar(x + 0.2, e.ml_multi, 0.38, color="#eb6834", edgecolor="white", label="ML estimate")
    ax.set_xticks(x)
    ax.set_xticklabels(["<1980", "1980s", "1990s", "2000s", "2010s"], fontsize=7.5)
    ax.set_ylabel("Multi-storey buildings (thousands)")
    ax.set_title("b  Uganda: multi-storey buildings by epoch", fontsize=8.5)
    ax.legend(fontsize=7, loc="upper right")
    ax.grid(axis="x", visible=False)
    fig.tight_layout(w_pad=1.5)
    fig.savefig(FIG / "figB2_buildings_ml.png")


def figB4_observed_uhi():
    """Paper B Figure 4: observed surface heat islands and their effect on initiation."""
    c = pd.read_csv(RES / "suhi_cities.csv").set_index("site").reindex(SITES)
    u = pd.read_csv(RES / "uhi_observed_pinit.csv")
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0))
    ax = axes[0]
    y = np.arange(len(SITES))[::-1]
    ax.barh(y + 0.19, c.suhi_day, 0.36, color="#eb6834", edgecolor="white", label="Day (13:30)")
    ax.barh(y - 0.19, c.suhi_night, 0.36, color="#2a78d6", edgecolor="white", label="Night (01:30)")
    for v, q in zip(c.suhi_day, y + 0.19):
        ax.text(v + 0.1, q, f"{v:.1f}", fontsize=7, color=INK2, va="center")
    for v, q in zip(c.suhi_night, y - 0.19):
        ax.text(v + 0.1, q, f"{v:.1f}", fontsize=7, color=INK2, va="center")
    ax.set_yticks(y)
    ax.set_yticklabels(SITES)
    ax.set_xlabel("Surface heat island, urban core (\u00b0C)")
    ax.set_title("a  Observed heat island, 2020\u20132021", fontsize=8.5)
    ax.set_xlim(0, 8.5)
    ax.legend(fontsize=7, loc="center right")
    ax.grid(axis="y", visible=False)
    ax = axes[1]
    est = {"none": ("No heat island", "D", MUTED), "low (0.5 x night SUHI)": ("Low estimate", "o", "#9ec5f4"),
           "central (1.0 x night SUHI)": ("Central estimate", "o", "#2a78d6")}
    g = u[u.case == "SSP5-8.5"].pivot_table(index="site", columns="uhi_estimate", values="p_init_2100").reindex(SITES)
    g0 = u[u.case == "no_change"].pivot_table(index="site", columns="uhi_estimate", values="p_init_2100").reindex(SITES)
    for k, (lab, mk, col) in est.items():
        ax.scatter(g0[k], y + 0.15, marker=mk, s=26, color=col, edgecolor="white", zorder=3, label=lab)
        ax.scatter(g[k], y - 0.15, marker=mk, s=26, color=col, edgecolor="#eb6834", linewidth=1, zorder=3)
    ax.set_yticks(y)
    ax.set_yticklabels(SITES)
    ax.set_xlim(0.3, 1.0)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
    ax.set_xlabel("P(initiation) by 2100")
    ax.set_title("b  Upper row: no climate change;\n    lower row (orange edge): SSP5-8.5", fontsize=8)
    ax.legend(fontsize=7, loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=3, handletextpad=0.3,
              columnspacing=1.0)
    ax.grid(axis="y", visible=False)
    fig.tight_layout(w_pad=1.5)
    fig.savefig(FIG / "figB4_observed_uhi.png")


if __name__ == "__main__":
    for f in (fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10, fig11, fig12, fig13):
        try:
            f()
            print("ok", f.__name__)
        except FileNotFoundError as e:
            print("skip", f.__name__, e)
