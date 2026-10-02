"""Reproducible systematic search on OpenAlex (open proxy for Scopus).

Runs the four search strings defined in SEARCHES against titles and abstracts,
1990-2026, articles/reviews/chapters/proceedings, and writes one CSV per search
plus a de-duplicated union with a first-pass relevance screen.
"""
import csv
import json
import time
from pathlib import Path

import requests

OUT = Path(__file__).parent / "results"
OUT.mkdir(exist_ok=True)

DETERIORATION = ('(carbonation OR "reinforcement corrosion" OR "steel corrosion" OR "rebar corrosion" '
                 'OR "corrosion initiation" OR "concrete durability" OR "service life")')
CLIMATE = ('("climate change" OR "global warming" OR "changing climate" OR "climate projection" '
           'OR "CO2 concentration" OR "carbon dioxide concentration" OR RCP OR SSP OR CMIP)')
AFRICA = ('(Africa OR "sub-Saharan" OR Uganda OR Kenya OR Tanzania OR Rwanda OR Ethiopia OR Zambia '
          'OR Malawi OR Nigeria OR Ghana OR Kampala OR Nairobi OR "East Africa" OR tropical OR tropics)')

SEARCHES = {
    "S1_climate_deterioration": f"concrete AND {DETERIORATION} AND {CLIMATE}",
    "S2_africa_tropical_durability": f"concrete AND {DETERIORATION} AND {AFRICA}",
    "S3_uganda_materials": ('Uganda AND (concrete OR cement OR "building collapse" OR "structural failure" '
                            'OR "construction quality" OR "building materials" OR masonry)'),
    "S4_uganda_exposure": ('(Uganda OR Kampala) AND ("urban expansion" OR "urban growth" OR "built-up" '
                           'OR "building stock" OR "exposure model" OR "building footprint" OR "settlement")'),
}

BASE = "https://api.openalex.org/works"
FILTER = "from_publication_date:1990-01-01,type:article|review|book-chapter|proceedings-article"


def run(name, query):
    rows, cursor = [], "*"
    while cursor:
        r = requests.get(BASE, params={
            "filter": f"title_and_abstract.search:{query},{FILTER}",
            "per-page": 200, "cursor": cursor,
            "select": "id,doi,title,publication_year,type,primary_location,authorships,cited_by_count,abstract_inverted_index",
            "mailto": "research@example.org",
        }, timeout=60)
        r.raise_for_status()
        js = r.json()
        for w in js["results"]:
            inv = w.get("abstract_inverted_index") or {}
            abstract = " ".join(k for _, k in sorted((p, k) for k, v in inv.items() for p in v))
            src = ((w.get("primary_location") or {}).get("source") or {}).get("display_name")
            rows.append({
                "search": name, "openalex_id": w["id"], "doi": w.get("doi") or "",
                "title": w.get("title") or "", "year": w.get("publication_year"),
                "type": w.get("type"), "source": src or "",
                "first_author": (w["authorships"][0]["author"]["display_name"] if w["authorships"] else ""),
                "cited_by": w.get("cited_by_count", 0), "abstract": abstract,
            })
        cursor = js["meta"].get("next_cursor")
        if len(rows) >= 2000:
            break
        time.sleep(0.2)
    return rows, js["meta"]["count"]


def main():
    counts, union = {}, {}
    for name, q in SEARCHES.items():
        rows, n = run(name, q)
        counts[name] = n
        with open(OUT / f"{name}.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=rows[0].keys())
            w.writeheader()
            w.writerows(rows)
        for r in rows:
            key = r["doi"].lower() or r["openalex_id"]
            union.setdefault(key, {**r, "searches": set()})["searches"].add(name)
        print(name, n)
    with open(OUT / "union.csv", "w", newline="") as f:
        fields = [k for k in next(iter(union.values())).keys() if k != "search"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in union.values():
            r = {k: v for k, v in r.items() if k != "search"}
            r["searches"] = ";".join(sorted(r["searches"]))
            w.writerow(r)
    (OUT / "counts.json").write_text(json.dumps({**counts, "union_unique": len(union)}, indent=2))
    print("union", len(union))


if __name__ == "__main__":
    main()
