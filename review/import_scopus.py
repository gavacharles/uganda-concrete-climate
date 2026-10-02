"""Merge Scopus CSV exports with the OpenAlex union, then re-run the screens.

Export each Scopus search (S1..S4) as CSV with "Citation information" and
"Abstract & keywords" ticked, save as review/scopus/S1.csv ... S4.csv, then:

    .venv/bin/python review/import_scopus.py
    .venv/bin/python review/screen.py
    .venv/bin/python review/stage2_decisions.py

The OpenAlex union is kept untouched in results/union_openalex.csv, so this
script can be re-run. Scopus records outside the eligibility limits written into
the strings (1990 onward, English, article / review / conference paper / book
chapter) are removed before de-duplication and counted for the PRISMA flow.
Records are matched across databases on DOI or normalised title; matches get
database "both" and the union of search tags. New Scopus records are written to
results/scopus_only.csv.
"""
import json
import re
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent
RES = HERE / "results"
NAMES = {"S1": "S1_climate_deterioration", "S2": "S2_africa_tropical_durability",
         "S3": "S3_uganda_materials", "S4": "S4_uganda_exposure"}
DOC_TYPES = {"Article", "Review", "Conference paper", "Book chapter"}


def norm(t):
    return re.sub(r"[^a-z0-9]", "", str(t).lower())[:120]


def bare_doi(d):
    return str(d).lower().replace("https://doi.org/", "").strip()


def merge_tags(tags):
    return ";".join(sorted({t for s in tags for t in str(s).split(";") if t}))


def main():
    union = pd.read_csv(RES / "union_openalex.csv").fillna("")
    union["database"] = "openalex"
    counts = {"hits": {}, "ineligible": {}, "eligible": {}}
    frames = []
    for short, name in NAMES.items():
        f = HERE / "scopus" / f"{short}.csv"
        if not f.exists():
            print("missing", f)
            continue
        s = pd.read_csv(f).fillna("")
        counts["hits"][name] = len(s)
        ok = (pd.to_numeric(s["Year"], errors="coerce").between(1990, 2026)
              & s["Language of Original Document"].str.contains("English")
              & s["Document Type"].isin(DOC_TYPES))
        counts["ineligible"][name] = int((~ok).sum())
        s = s[ok]
        counts["eligible"][name] = len(s)
        frames.append(pd.DataFrame({
            "openalex_id": "", "doi": s["DOI"].map(lambda d: f"https://doi.org/{d.lower()}" if d else ""),
            "title": s["Title"], "year": s["Year"], "type": s["Document Type"],
            "source": s["Source title"], "first_author": s["Authors"].str.split(";").str[0],
            "cited_by": s["Cited by"], "abstract": s["Abstract"].replace("[No abstract available]", ""),
            "searches": name, "database": "scopus",
        }))
    sc = pd.concat(frames)
    sc["key"] = sc.title.map(norm)
    tags = sc.groupby("key").searches.agg(merge_tags)
    sc = sc.drop_duplicates("key").assign(searches=lambda d: d.key.map(tags))
    counts["scopus_unique"] = len(sc)

    union["key"] = union.title.map(norm)
    doi_key = {bare_doi(d): k for d, k in zip(union.doi, union.key) if bare_doi(d)}
    sc["match"] = [doi_key.get(bare_doi(d), k if k in set(union.key) else None) if bare_doi(d)
                   else (k if k in set(union.key) else None) for d, k in zip(sc.doi, sc.key)]
    hit = sc[sc.match.notna()]
    new = sc[sc.match.isna()].drop(columns=["match"])
    extra = hit.groupby("match").searches.agg(merge_tags)
    abs_sc = hit[hit.abstract != ""].drop_duplicates("match").set_index("match").abstract
    fill = (union.abstract == "") & union.key.isin(abs_sc.index)
    union.loc[fill, "abstract"] = union.key[fill].map(abs_sc)
    m = union.key.isin(extra.index)
    union.loc[m, "database"] = "both"
    union.loc[m, "searches"] = [merge_tags([a, extra[k]]) for a, k in zip(union.searches[m], union.key[m])]
    counts["scopus_in_openalex"] = int(hit.match.nunique())
    counts["scopus_new"] = len(new)
    counts["openalex_unique"] = len(union)

    new.drop(columns=["key"]).to_csv(RES / "scopus_only.csv", index=False)
    out = pd.concat([union, new]).drop(columns=["key"])
    out.to_csv(RES / "union.csv", index=False)
    counts["union_unique"] = len(out)
    (RES / "scopus_counts.json").write_text(json.dumps(counts, indent=2))
    print(json.dumps(counts, indent=2))


if __name__ == "__main__":
    main()
