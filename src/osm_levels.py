"""Extract OSM buildings with a storey count (building:levels) in Uganda -> data/processed/osm_building_levels.csv."""
from pathlib import Path

import osmium
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


class H(osmium.SimpleHandler):
    def __init__(self):
        super().__init__()
        self.rows = []

    def way(self, w):
        t = w.tags
        if "building" in t and "building:levels" in t:
            try:
                lv = float(str(t["building:levels"]).split(";")[0].replace(",", "."))
                xs = [n.lon for n in w.nodes if n.location.valid()]
                ys = [n.lat for n in w.nodes if n.location.valid()]
                if xs:
                    self.rows.append((w.id, sum(ys) / len(ys), sum(xs) / len(xs), lv, t["building"]))
            except ValueError:
                pass


h = H()
h.apply_file(str(ROOT / "data" / "raw" / "osm" / "uganda-latest.osm.pbf"), locations=True)
df = pd.DataFrame(h.rows, columns=["osm_id", "lat", "lon", "levels", "building"])
df.to_csv(ROOT / "data" / "processed" / "osm_building_levels.csv", index=False)
print(len(df)); print(df.levels.describe()); print((df.levels >= 2).mean())
