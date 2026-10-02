# Uganda climate–concrete paper: everything in one place

## 1. Documents (live, editable online)

| Document | Link | Shortcut in this folder |
| --- | --- | --- |
| Manuscript draft | [open](https://claude.ai/code/artifact/ecead7f2-5c83-429f-a4c0-5b1e5691670c) | `documents/Manuscript Draft.webloc` |
| Literature review + systematic review (PRISMA, Scopus strings) | [open](https://claude.ai/code/artifact/d89db0d2-a666-49a9-addc-b0d8672f07d1) | `documents/Literature Review and Systematic Review.webloc` |
| SHM concept note (to pass to the collaborator) | [open](https://claude.ai/code/artifact/0bdb6454-b173-48ed-bcc2-deb3df907498) | `documents/SHM Concept Note (for collaborator).webloc` |

To get Word or PDF copies, open a document and use its export option. They are live documents, so exported copies won't update.

## 2. Figures — `figures/` (redraw with `src/figures.py`)

| File | What it shows |
| --- | --- |
| `prisma_flow.png` | PRISMA 2020 flow, OpenAlex + Scopus: 6,367 records, 5,574 screened, 188 studies included |
| `fig1_framework.png` | Assessment framework |
| `fig2_climate.png` | Warming at six cities to 2100, ensemble mean and model range |
| `fig3_site_pinit.png` | Corrosion-initiation probability at six cities, 2000–2100 |
| `fig4_quality_vs_climate.png` | Concrete quality versus climate: probability by 2100 by concrete class |
| `fig5_stock_trajectory.png` | Share of Uganda's RC buildings past initiation, 2030–2100 |
| `fig6_stock_map.png` | Map: share past initiation by 2100 and the climate increase |
| `fig7_adaptation.png` | Extra cover that offsets climate change, by city |
| `fig8_sensitivity.png` | Which inputs matter most (tornado), Kampala and Arua |
| `fig9_cracking.png` | Probability of cover cracking at six cities |
| `fig10_new_construction.png` | Buildings built 2020–2049: as built, as specified, +8 mm cover |
| `fig11_growth.png` | Growth of the building stock by decade (maps) |
| `fig12_urban_heat.png` | Urban heat island effect at six cities |
| `fig13_machine_learning.png` | ML: surrogate importance, storeys check, national RC count, measured vs fib |
| `fig14_rain_extremes.png` | Rainfall extremes and wetting–drying change (manuscript Figure S5) |

## 3. Results — `results/`

| File | Contents |
| --- | --- |
| `site_pinit.csv` | Corrosion-initiation probability and mean carbonation depth for 6 cities × 2 climate baselines × 3 concrete classes × 3 scenarios × casting years 1980–2050, every year to 2100 |
| `site_climate.csv` | Annual temperature, humidity and rain days per model and scenario at each city |
| `site_run_log.txt` | Printed summary tables from the site run |
| `stock_summary.csv`, `stock_cells.csv` | National building-stock exposure (8 models) |
| `adaptation.csv` | Extra cover and cover for P ≤ 0.10, by city, concrete class and scenario |

## 4. Systematic review — `review/`

- `scopus/S1.csv`–`S4.csv`: Scopus exports (run 1 Oct 2026); `scopus/README.md` has the strings
- `results/included_final.csv`: the 188 included studies from database searches, with DOIs, themes and database
- `prisma_figure.py`: redraws `figures/prisma_flow.png` from `results/prisma.json`
- `results/prisma.json`: PRISMA counts
- `results/union.csv`: all 5,574 de-duplicated records with screening decisions in `screen_stage1_all.csv`

## 5. Literature PDFs — `literature/`

- Caleb et al. (2023), building collapse in Kampala (KJSET)
- Ministry of Works and Transport (2013), Standard Specifications for Building Works (cement, curing and cover clauses)
- GHS-OBAT technical report (building age and height data)

Also here: Ekolu 2020 (CO₂), Ekolu & Solomon 2022, Buregyeya 2018, Dimova 2025, Pinheiro Teodoro 2026, Bastidas-Arteaga 2022, Val 2025. Still missing: Ekolu 2020 Kampala chapter, fib Bulletin 34, Stewart 2011/2012, Talukdar 2012.

## 6. Data and code

- `data/processed/`: CO₂ pathways, ERA5 at the 6 cities, building stock aggregated to the climate grid, grid-cell elevations, and annual climate grids (`nex_annual_v2/`)
- `data/raw/`: large downloads (GHS-OBAT 2 GB, Meinshausen supplement)
- `src/`: the analysis scripts; `README.md` lists the pipeline order

## Status (2 Oct 2026)

- [x] Systematic review: OpenAlex + Scopus, PRISMA diagram and search strings (Literature Review doc)
- [x] Blended-cement factor calibrated (2.6–4.4) from Ekolu & Solomon 2022 and Buregyeya 2018
- [x] City, national stock and adaptation runs with all 8 models; figures 2–7
- [x] Manuscript: all sections drafted, including Results, Discussion, Conclusions, Abstract
- [x] Extensions: sensitivity, rain exposure, cracking, model spread, new construction, cost-effectiveness (Sections 4.6, 5.6–5.10)
- [x] Growth map, urban heat, three ML analyses (Sections 4.7, 5.11–5.13)
- [x] Rainfall extremes: Supplementary S10 (Figure S5)
- [x] Trim: main text 9 figures + 5 tables; further analyses moved to Supplementary S2–S10; abstract ~240 words
- [ ] Check the propagation parameters (DuraCrete 2000, Alonso et al. 1998) against the full texts
- [ ] Ugandan unit costs (concrete per m³, patch repair per m²) to turn Table 7 into money
- [ ] Remaining paywalled papers (Ekolu 2020 Kampala chapter, fib Bulletin 34, Stewart 2011/2012)
- [ ] Choose the target journal and format references
- Decided: no field survey; UNMA humidity data and US EAS 18-1 not obtainable
