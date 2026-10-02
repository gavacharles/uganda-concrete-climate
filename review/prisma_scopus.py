"""Scopus-only PRISMA counts and included studies (the review as reported in Paper A).

Uses the screening decisions already made (screen.py, stage2_decisions.py) but restricts the records
to those retrieved by Scopus, de-duplicated on normalised title.
Outputs: results/prisma_scopus.json, results/included_scopus.csv
"""
import json
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import stage2_decisions as s2  # noqa: E402

RES = HERE / "results"


def norm(t):
    return pd.Series(t).str.lower().str.replace(r"[^a-z0-9]", "", regex=True).str[:120]


def decide(t):
    tl = t.lower()
    if any(k.lower() in tl for k in s2.FLAGGED):
        return "flagged"
    for k, v in s2.INCLUDE.items():
        if k.lower() in tl:
            return v
    return "exclude"


def main():
    a = pd.read_csv(RES / "screen_stage1_all.csv").fillna("")
    sc = a[a.database.isin(["scopus", "both"])].copy()
    sc = sc[~norm(sc.title).duplicated().to_numpy()]
    cnt = json.loads((RES / "scopus_counts.json").read_text())
    inc1 = sc[sc.stage1 == "include"].copy()
    inc1["decision"] = inc1.title.apply(decide)
    keep = inc1[~inc1.decision.isin(["exclude", "flagged"])]
    fin = keep[~norm(keep.title).str[:80].duplicated().to_numpy()]
    p = {
        "identified_by_search": cnt["hits"], "identified_total": int(sum(cnt["hits"].values())),
        "removed_outside_limits": int(sum(cnt["ineligible"].values())),
        "removed_duplicates": int(sum(cnt["eligible"].values()) - len(sc)),
        "screened": int(len(sc)),
        "excluded_corrupted_metadata": int((sc.stage1_reason == "corrupted abstract metadata").sum()),
        "excluded_stage1": int(((sc.stage1 == "exclude") & (sc.stage1_reason != "corrupted abstract metadata")).sum()),
        "assessed_stage2": int(len(inc1)), "flagged_integrity": int((inc1.decision == "flagged").sum()),
        "excluded_stage2": int((inc1.decision == "exclude").sum()),
        "duplicates_in_included": int(len(keep) - len(fin)), "included": int(len(fin)),
        "included_by_theme": fin.decision.value_counts().sort_index().to_dict(),
    }
    (RES / "prisma_scopus.json").write_text(json.dumps(p, indent=2))
    fin.rename(columns={"decision": "theme"})[["theme", "year", "first_author", "title", "source", "doi"]].sort_values(
        ["theme", "year"]).to_csv(RES / "included_scopus.csv", index=False)
    print(json.dumps(p, indent=2))


if __name__ == "__main__":
    main()
