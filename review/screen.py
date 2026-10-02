"""Rule-based title/abstract screen (stage 1) of the OpenAlex union.

Each search has its own inclusion rule; records failing it are excluded with a
reason so the PRISMA counts can be reported. Survivors go to manual screening
(review/results/screen_stage1_included.csv).
"""
import re
from pathlib import Path

import pandas as pd

RES = Path(__file__).parent / "results"


def has(text, pattern):
    return re.search(pattern, text, flags=re.I) is not None


def rule(r):
    t, a = str(r["title"]), str(r["abstract"])
    ta = f"{t} {a}"
    s = r["searches"]
    reasons = []
    if has(a, r"Svalbard|Tokelau"):  # scraped country drop-down lists in some publisher abstracts
        return "exclude", "corrupted abstract metadata"
    if "S1" in s:
        clim = r"climate change|changing climate|future climate|climate scenario|emission scenario|RCP ?\d|SSP ?\d|CMIP|global warming(?! potential)|CO2 concentration"
        if (has(ta, r"corrosion|service.life|durabilit|deteriorat|carbonation depth|carbonation front")
                and (has(t, clim) or (has(a, clim) and has(t, r"corrosion|carbonation|service.life|durabilit|deteriorat")))
                and not has(t, r"sequestrat|uptake|capture|mineraliz|accelerated carbonation curing|LCA|life.cycle assessment|emission reduction|recycled|asphalt|timber|geopolymer")):
            return "include", "S1"
        reasons.append("S1: not climate-driven deterioration")
    if "S2" in s:
        if (has(ta, r"carbonation|corrosion|durabilit|service life")
                and has(ta, r"Africa|Uganda|Kenya|Tanzania|Rwanda|Ethiopia|Zambia|Malawi|Nigeria|Ghana|Kampala|Nairobi|tropic")
                and not has(t, r"sequestrat|uptake|capture")):
            return "include", "S2"
        reasons.append("S2: not African/tropical durability")
    if "S3" in s:
        if has(t, r"concrete|cement|collapse|structural|building material|masonry|brick|aggregate|reinforc") \
                and has(ta, r"Uganda|Kampala"):
            return "include", "S3"
        reasons.append("S3: not construction materials")
    if "S4" in s:
        if has(t, r"urban|built.up|building|settlement|land.use|land cover|sprawl") and has(ta, r"Kampala|Uganda") \
                and not has(t, r"health|malaria|HIV|sanitation|water supply|refugee|school|nutrition|child"):
            return "include", "S4"
        reasons.append("S4: not built-environment growth")
    return "exclude", "; ".join(reasons)


def main():
    df = pd.read_csv(RES / "union.csv").fillna({"title": "", "abstract": ""})
    df[["stage1", "stage1_reason"]] = df.apply(lambda r: pd.Series(rule(r)), axis=1)
    df.to_csv(RES / "screen_stage1_all.csv", index=False)
    inc = df[df.stage1 == "include"].sort_values(["stage1_reason", "cited_by"], ascending=[True, False])
    inc[["stage1_reason", "year", "first_author", "title", "source", "doi", "cited_by"]].to_csv(
        RES / "screen_stage1_included.csv", index=False)
    print(df.stage1.value_counts())
    print(inc.stage1_reason.value_counts())


if __name__ == "__main__":
    main()
