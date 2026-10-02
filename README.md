# Climate change and carbonation-induced corrosion risk of Uganda's reinforced concrete building stock

Code, processed data and results for two companion papers:

- **Paper A** — climate change and carbonation-induced corrosion risk of Uganda's RC building stock
  (CMIP6 projections, probabilistic fib carbonation model, building-age data, adaptation).
- **Paper B** — exposure of the building stock: growth, neighbourhood-height bias in multi-storey
  counts (machine learning on OpenStreetMap labels), urban heat island, rainfall extremes.

## Which script supports which paper

| Step | Script | Output | Paper |
| --- | --- | --- | --- |
| Systematic review, Scopus (as reported) | `review/import_scopus.py` → `review/screen.py` → `review/stage2_decisions.py` → `review/prisma_scopus.py` | `review/results/prisma_scopus.json`, `included_scopus.csv`, `figures/prisma_flow_scopus.png` | A |
| CO₂ pathways | extracted from Meinshausen et al. (2020) | `data/processed/co2_meinshausen2020.csv` | A, B |
| Climate projections | `src/fetch_nex_gddp.py` (NEX-GDDP-CMIP6, 8 models, 1980–2100) | `data/processed/nex_annual_v2/` (not versioned) | A, B |
| ERA5 check | `src/fetch_era5_sites.py` | `data/processed/era5_sites_annual.csv` | A |
| Building stock | `src/aggregate_stock.py` (GHS-OBAT) + `src/fetch_cell_elevation.py` | `data/processed/stock_grid.csv`, `cell_elevation.csv` | A, B |
| Carbonation model | `src/carbonation.py` (`python src/carbonation.py` runs the fib reference check) | — | A |
| City results | `src/run_sites.py` | `results/site_pinit.csv`, `site_climate.csv` | A |
| Stock results | `src/run_stock.py` | `results/stock_cells.csv`, `stock_summary.csv` | A |
| Adaptation | `src/adaptation.py` | `results/adaptation.csv` | A |
| Sensitivity, rain exposure, cracking, cost-effectiveness | `src/site_extensions.py` | `results/sensitivity.csv`, `rain_exposure.csv`, `propagation.csv`, `cost_benefit.csv` | A |
| Model spread, new construction 2020–2049 | `src/stock_extensions.py` | `results/stock_by_model.csv`, `new_construction.csv` | A |
| Check against measured carbonation | `src/ml_carbonation_check.py` | `results/ml_carbonation_*.csv` | A |
| Urban heat island | `src/urban_heat.py` | `results/urban_heat.csv` | B |
| Multi-storey classifier (OSM labels) | `src/osm_levels.py` → `src/ml_buildings.py` → `src/ml_reweight.py` | `results/ml_buildings_*.csv`, `stock_summary_ml.csv` | B |
| Surrogate of the carbonation model | `src/ml_surrogate.py` | `results/ml_surrogate_*.csv` | B |
| Rainfall extremes | `src/fetch_rain_extremes.py` → `src/rain_extremes_analysis.py` | `results/rain_extremes_*.csv` | B |
| Observed urban heat island (MODIS Aqua LST 2020–2021, Copernicus DEM) | `src/fetch_modis_lst.py` + `src/building_density.py` → `src/observed_uhi.py` | `results/suhi_cities.csv`, `suhi_cells.csv`, `uhi_observed_pinit.csv` | B |
| Classifier checks (geographic transfer, label bias) | `src/ml_buildings.py` | `results/ml_buildings_transfer.csv`, `ml_buildings_label_bias.csv` | B |
| Building-level risk, Greater Kampala | `src/kampala_building_risk.py` | `results/kampala_building_risk_*.csv`, `figures/figB5_kampala_risk.png` | B |
| Word manuscripts | `src/build_docx.py` | `manuscripts/Paper*_manuscript.docx` | A, B |
| Figures | `src/figures.py`, `review/prisma_figure_scopus.py` | `figures/` | A, B |
| Re-run all analyses | `src/run_all.sh` | — | A |

`review/search_openalex.py` and `review/prisma_figure.py` belong to an earlier exploratory search and are kept for the record; Paper A reports the Scopus search only.

### Figure files and paper numbering

| File | Paper A | Paper B |
| --- | --- | --- |
| `fig1_framework.png` … `fig8_sensitivity.png` | Figures 1–8 | — |
| `prisma_flow_scopus.png` | Figure S1 | — |
| `fig9_cracking.png` | Figure S2 | — |
| `fig10_new_construction.png` | Figure S3 | — |
| `figS3_carbonation_check.png` | Figure S4 | — |
| `fig11_growth.png` | — | Figure 1 |
| `figB2_buildings_ml.png` | — | Figure 2 |
| `figB4_observed_uhi.png` | — | Figure 3 |
| `fig12_urban_heat.png` | — | Figure 4 |
| `figB5_kampala_risk.png` | — | Figure 5 |
| `fig14_rain_extremes.png` | — | Figure 6 |

## Reproducing

```sh
python3 -m venv .venv
.venv/bin/pip install numpy pandas scipy xarray netCDF4 requests matplotlib openpyxl pypdf scikit-learn osmium \
    pystac-client planetary-computer rasterio shapely mercantile joblib python-docx pypandoc_binary
.venv/bin/python src/fetch_nex_gddp.py          # climate data (several hours)
.venv/bin/python src/aggregate_stock.py         # needs the GHS-OBAT Uganda CSV in data/raw/ghs_obat_uga/
./src/run_all.sh                                # cities, adaptation, stock, figures
```

## Data not included, and why

| Data | Source | Reason |
| --- | --- | --- |
| NEX-GDDP-CMIP6 daily data | NASA NCCS THREDDS | Large; fetched by `src/fetch_nex_gddp.py` and `src/fetch_rain_extremes.py` |
| GHS-OBAT Uganda (2 GB) | European Commission JRC | Large; download from the GHSL website |
| Scopus exports and screening tables with abstracts | Elsevier Scopus | Scopus terms do not allow redistribution; the search strings are in `review/scopus/README.md` |
| OpenStreetMap building levels | Geofabrik extract | ODbL; regenerate with `src/osm_levels.py` |
| Carbonation test database | Mendeley Data, doi:10.17632/rchp48n97y.2 (CC BY 4.0) | Downloaded by the user; see `src/ml_carbonation_check.py` |
| Literature PDFs | Publishers | Copyright |

Included processed data derive from GHS-OBAT (CC BY 4.0), ERA5 (Copernicus licence), Meinshausen et al. (2020) and Natural Earth (public domain).

## Key assumptions

- Blended-cement multiplier on R⁻¹_ACC,0 is 2.6–4.4, calibrated from Ekolu & Solomon (2022) and Buregyeya et al. (2018).
- As-built cover N(22, 8) mm and w/c 0.55–0.70 are literature-informed; no Ugandan field data exist.
- RC frames = buildings in neighbourhoods of mean height ≥ 4.5 m (GHS-BUILT-H, 100 m); this overstates the multi-storey stock about four-fold (Paper B), so building counts are upper bounds.
- Corrosion-propagation parameters (DuraCrete 2000; Alonso et al. 1998) are indicative.
