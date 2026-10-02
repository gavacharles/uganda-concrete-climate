"""PRISMA 2020 flow diagram from review/results/prisma.json -> figures/prisma_flow.png."""
import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
P = json.loads((ROOT / "review" / "results" / "prisma.json").read_text())
LABEL = {"S1_climate_deterioration": "S1 Climate × deterioration", "S2_africa_tropical_durability": "S2 Africa/tropics",
         "S3_uganda_materials": "S3 Uganda materials", "S4_uganda_exposure": "S4 Uganda exposure"}
THEME = {"T1": "T1 climate–carbonation modelling", "T2": "T2 tropical/African durability",
         "T3": "T3 Ugandan materials & quality", "T4": "T4 growth, exposure, urban climate"}


def fmt(n):
    return f"{n:,}"


def box(ax, x, y, w, h, text, fc="#ffffff", bold_first=True, size=8.6):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.004,rounding_size=0.008",
                                fc=fc, ec="#333333", lw=0.9))
    lines = text.split("\n")
    ax.text(x + 0.012, y + h - 0.012, lines[0], ha="left", va="top", size=size,
            weight="bold" if bold_first else "normal")
    if len(lines) > 1:
        ax.text(x + 0.012, y + h - 0.040, "\n".join(lines[1:]), ha="left", va="top", size=size - 0.4,
                linespacing=1.35)


def arrow(ax, x0, y0, x1, y1):
    ax.annotate("", (x1, y1), (x0, y0), arrowprops=dict(arrowstyle="-|>", lw=0.9, color="#333333"))


def main():
    fig, ax = plt.subplots(figsize=(10, 9.5))
    ax.set_xlim(0, 1)
    ax.set_ylim(0.04, 1)
    ax.axis("off")
    stages = [("Identification", 0.80, 0.995), ("Screening", 0.30, 0.78), ("Included", 0.04, 0.28)]
    for name, lo, hi in stages:
        ax.add_patch(FancyBboxPatch((0.0, lo + 0.005), 0.035, hi - lo - 0.01, boxstyle="round,pad=0,rounding_size=0.01",
                                    fc="#9ec5e8", ec="none"))
        ax.text(0.0175, (lo + hi) / 2, name, rotation=90, ha="center", va="center", size=10, weight="bold")

    oa, sc = P["identified"]["openalex"], P["identified"]["scopus"]
    t_oa, t_sc = P["identified_total"]["openalex"], P["identified_total"]["scopus"]
    lw, lx, rx = 0.43, 0.05, 0.56
    box(ax, lx, 0.835, 0.235, 0.155, f"OpenAlex (n = {fmt(t_oa)})\n" + "\n".join(f"{LABEL[k]}: {fmt(v)}" for k, v in oa.items()), size=8.2)
    box(ax, lx + 0.245, 0.835, 0.235, 0.155, f"Scopus (n = {fmt(t_sc)})\n" + "\n".join(f"{LABEL[k]}: {fmt(v)}" for k, v in sc.items()), size=8.2)
    dup = P["duplicates_within_openalex"] + P["duplicates_within_scopus"] + P["duplicates_across_databases"]
    removed = dup + P["scopus_ineligible_type_year_language"]
    box(ax, rx, 0.835, 0.43, 0.155,
        f"Records removed before screening (n = {fmt(removed)})\n"
        f"Outside limits (pre-1990, non-English, non-research\n  item type; Scopus): {fmt(P['scopus_ineligible_type_year_language'])}\n"
        f"Duplicates within OpenAlex: {fmt(P['duplicates_within_openalex'])}\n"
        f"Duplicates within Scopus (across strings): {fmt(P['duplicates_within_scopus'])}\n"
        f"Duplicates across databases (DOI/title): {fmt(P['duplicates_across_databases'])}")
    arrow(ax, lx + 0.48, 0.912, rx, 0.912)

    db = P["records_by_database"]
    box(ax, lx, 0.62, lw + 0.05, 0.12,
        f"Records screened, title/abstract stage 1 (n = {fmt(P['records_screened'])})\n"
        f"OpenAlex only {fmt(db.get('openalex', 0))} · Scopus only {fmt(db.get('scopus', 0))} · both {fmt(db.get('both', 0))}\n"
        "Search-specific inclusion rules applied to title and abstract")
    arrow(ax, lx + 0.24, 0.835, lx + 0.24, 0.74)
    ex1 = P["excluded_corrupted_metadata"] + P["excluded_stage1_rules"]
    box(ax, rx, 0.62, 0.43, 0.12,
        f"Records excluded (n = {fmt(ex1)})\n"
        f"Outside topic of the search's inclusion rule: {fmt(P['excluded_stage1_rules'])}\n"
        f"Corrupted abstract metadata: {fmt(P['excluded_corrupted_metadata'])}")
    arrow(ax, lx + 0.48, 0.68, rx, 0.68)

    box(ax, lx, 0.38, lw + 0.05, 0.12,
        f"Records assessed for eligibility, stage 2 (n = {fmt(P['screened_stage2'])})\n"
        "Manual title/abstract review against the\nfour synthesis themes")
    arrow(ax, lx + 0.24, 0.62, lx + 0.24, 0.50)
    ex2 = P["excluded_stage2"] + P["flagged_integrity"] + P["duplicates_in_included"]
    box(ax, rx, 0.36, 0.43, 0.16,
        f"Records excluded (n = {fmt(ex2)})\n"
        f"Off-topic: material/mix-design without climate or\n  field context, chloride-only marine, freeze–thaw,\n  seismic, pavements, non-built land use: {fmt(P['excluded_stage2'])}\n"
        f"Integrity concerns (suspect repository records): {fmt(P['flagged_integrity'])}\n"
        f"Residual duplicates: {fmt(P['duplicates_in_included'])}")
    arrow(ax, lx + 0.48, 0.44, rx, 0.44)

    th = P["included_by_theme"]
    idb = P["included_by_database"]
    box(ax, lx, 0.06, lw + 0.05, 0.19,
        f"Studies included in the review (n = {fmt(P['included'])})\n" +
        "\n".join(f"{THEME[k]}: {v}" for k, v in th.items()) +
        f"\n\nFound in both databases {idb.get('both', 0)} · OpenAlex only {idb.get('openalex', 0)} ·"
        f" Scopus only {idb.get('scopus', 0)}", fc="#eef5fb")
    arrow(ax, lx + 0.24, 0.38, lx + 0.24, 0.24)

    out = ROOT / "figures" / "prisma_flow.png"
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
    print("wrote", out)


if __name__ == "__main__":
    main()
