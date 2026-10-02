"""ERA5 daily temperature and relative humidity at the six sites (Open-Meteo archive API), 1981-2014.

Used to check the NEX-GDDP-CMIP6 historical runs. Output: data/processed/era5_sites_annual.csv
"""
import sys
import time
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).parent))
from run_sites import SITES  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def main():
    rows = []
    for site, (lat, lon, _) in SITES.items():
        for attempt in range(6):  # free API is rate limited per minute
            r = requests.get("https://archive-api.open-meteo.com/v1/archive", params={
                "latitude": lat, "longitude": lon, "start_date": "1981-01-01", "end_date": "2014-12-31",
                "daily": "temperature_2m_mean,relative_humidity_2m_mean,precipitation_sum",
                "models": "era5", "timezone": "Africa/Kampala"}, timeout=300)
            if r.status_code != 429:
                break
            time.sleep(65)
        r.raise_for_status()
        time.sleep(20)
        d = pd.DataFrame(r.json()["daily"])
        d["year"] = pd.to_datetime(d.time).dt.year
        a = d.groupby("year").agg(tas=("temperature_2m_mean", "mean"), hurs=("relative_humidity_2m_mean", "mean"),
                                  pr_total=("precipitation_sum", "sum"),
                                  pr_days=("precipitation_sum", lambda s: (s >= 2.5).sum())).reset_index()
        a["site"] = site
        rows.append(a)
        print(site, a[["tas", "hurs", "pr_total", "pr_days"]].mean().round(1).to_dict())
    pd.concat(rows).to_csv(ROOT / "data" / "processed" / "era5_sites_annual.csv", index=False)


if __name__ == "__main__":
    main()
