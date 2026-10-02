"""PRISMA 2020 flow for the Scopus-only review (Paper A) -> figures/prisma_flow_scopus.png."""
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).parent))
from prisma_figure import LABEL, THEME, arrow, box, fmt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
P = json.loads((ROOT / "review" / "results" / "prisma_scopus.json").read_text())


def main():
    fig, ax = plt.subplots(figsize=(9, 8.6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0.04, 1)
    ax.axis("off")
    for name, lo, hi in (("Identification", 0.80, 0.995), ("Screening", 0.30, 0.78), ("Included", 0.04, 0.28)):
        ax.add_patch(FancyBboxPatch((0.0, lo + 0.005), 0.035, hi - lo - 0.01, boxstyle="round,pad=0,rounding_size=0.01",
                                    fc="#9ec5f4", ec="none"))
        ax.text(0.0175, (lo + hi) / 2, name, rotation=90, ha="center", va="center", size=10, weight="bold")
    lx, rx = 0.05, 0.56
    box(ax, lx, 0.835, 0.48, 0.155, f"Records identified from Scopus (n = {fmt(P['identified_total'])})\n" +
        "\n".join(f"{LABEL[k]}: {fmt(v)}" for k, v in P["identified_by_search"].items()))
    rem = P["removed_outside_limits"] + P["removed_duplicates"]
    box(ax, rx, 0.835, 0.43, 0.155, f"Removed before screening (n = {fmt(rem)})\n"
        f"Outside limits (pre-1990, non-English,\n  non-research item type): {fmt(P['removed_outside_limits'])}\n"
        f"Duplicates across search strings: {fmt(P['removed_duplicates'])}")
    arrow(ax, lx + 0.48, 0.912, rx, 0.912)
    box(ax, lx, 0.62, 0.48, 0.12, f"Screened, stage 1 (n = {fmt(P['screened'])})\n"
        "Search-specific inclusion rules applied to title and abstract")
    arrow(ax, lx + 0.24, 0.835, lx + 0.24, 0.74)
    ex1 = P["excluded_stage1"] + P["excluded_corrupted_metadata"]
    box(ax, rx, 0.62, 0.43, 0.12, f"Records excluded (n = {fmt(ex1)})\n"
        f"Outside topic of the search's inclusion rule: {fmt(P['excluded_stage1'])}\n"
        f"Corrupted abstract metadata: {fmt(P['excluded_corrupted_metadata'])}")
    arrow(ax, lx + 0.48, 0.68, rx, 0.68)
    box(ax, lx, 0.38, 0.48, 0.12, f"Assessed for eligibility, stage 2 (n = {fmt(P['assessed_stage2'])})\n"
        "Manual title/abstract review against the\nfour synthesis themes")
    arrow(ax, lx + 0.24, 0.62, lx + 0.24, 0.50)
    box(ax, rx, 0.38, 0.43, 0.12, f"Records excluded (n = {fmt(P['excluded_stage2'])})\n"
        "Off-topic: mix design without climate or field\n  context, chloride-only marine, freeze–thaw,\n"
        "  seismic, pavements, non-built land use")
    arrow(ax, lx + 0.48, 0.44, rx, 0.44)
    box(ax, lx, 0.07, 0.48, 0.18, f"Studies included in the review (n = {fmt(P['included'])})\n" +
        "\n".join(f"{THEME[k]}: {v}" for k, v in P["included_by_theme"].items()), fc="#eef5fb")
    arrow(ax, lx + 0.24, 0.38, lx + 0.24, 0.25)
    out = ROOT / "figures" / "prisma_flow_scopus.png"
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
    print("wrote", out)


if __name__ == "__main__":
    main()
