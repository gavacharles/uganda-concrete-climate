# Paper B

## Abstract

Assessments of climate-driven deterioration of reinforced concrete rely on open building data and regional climate projections, both of which are uncertain in fast-growing tropical countries. Using Uganda as a case, this study examines four exposure factors: growth of the building stock, the count of multi-storey (reinforced-concrete-frame) buildings, the urban heat island and rainfall extremes. Footprint-level construction epochs show that Uganda added 6.5 million buildings in the 2010s, only 5% of them in the Kampala area. A gradient-boosting classifier trained on 104,014 OpenStreetMap storey counts estimates about 0.62 million multi-storey buildings, against 2.42 million from a neighbourhood-height threshold; shares of the stock at risk of corrosion are robust to this four-fold difference, but building counts are not. MODIS land-surface temperature for 2020–2021 gives urban heat islands of 1.9–7.2 °C by day and 0.1–1.4 °C by night in six cities. Treating 0.5–1.0 times the night-time value as the air heat island, with the drier air it implies, raises the probability of carbonation-induced corrosion initiation by 2100 in Kampala from 36% to 48–58% without climate change, and adds 27,000–40,000 multi-storey buildings past initiation in Greater Kampala. The wettest day of the year intensifies by 22–40% by 2081–2100, while wetting–drying cycles barely change. Exposure models for tropical building stocks should report building counts with their uncertainty, and durability design for humid tropical cities should use urban rather than regional climate.

**Keywords:** exposure modelling; building stock; urban heat island; machine learning; OpenStreetMap; carbonation; Uganda

## 1. Introduction

Assessments of climate-driven deterioration of reinforced concrete (RC) usually take two inputs as given: how many buildings are exposed, and what climate they experience. Both are uncertain in fast-growing tropical countries. Building inventories rarely exist, so exposure models rely on open gridded data such as the Global Human Settlement Layer (GHSL) and its footprint-level derivative GHS-OBAT [Florio et al., 2025], whose heights and construction epochs are neighbourhood values. Climate inputs come from regional projections that do not resolve urban heat islands, which in East African cities add local warming on top of regional trends.

The companion study (Paper A) estimated carbonation-induced corrosion risk for Uganda's RC stock under CMIP6 scenarios. This paper examines the exposure side of that estimate. Its objectives are to:

1. map how and where Uganda's building stock has grown since before 1980;
2. test whether neighbourhood-height data identify multi-storey (RC-frame) buildings, using OpenStreetMap storey counts and a machine-learning classifier;
3. quantify how an urban heat island, through both warming and drying, changes carbonation risk; and
4. assess projected changes in rainfall extremes and wetting–drying cycles over the building stock.

Finally, it maps corrosion risk building by building in Greater Kampala, combining the classifier with the observed heat island.

## 2. Data and methods

### 2.1 Building stock and growth

GHS-OBAT gives every building footprint in Uganda (22.5 million) a construction epoch, a height and a use [Florio et al., 2025]. Height is the GHS-BUILT-H average building height of the surrounding 100 m cell in 2018. The epoch is the earliest decade by which at least half of the cell's present built-up surface existed (GHS-AGE), so infill and replacement inside older neighbourhoods are dated to the earlier epoch. Buildings were aggregated to a 0.25° grid by epoch to map outward growth, expressed as new buildings per km².

### 2.2 Multi-storey buildings from OpenStreetMap and machine learning

OpenStreetMap buildings with a storey count (building:levels) were extracted from the Uganda extract and matched to the nearest GHS-OBAT footprint within about 10 m: 104,014 matches, of which 1,811 have two or more storeys. A gradient-boosting classifier predicts the probability that a building has two or more storeys from footprint area, perimeter and shape factor, use, GHS-OBAT neighbourhood height and epoch, building density and mean footprint size in about 220 m bins, and distance to the nearest of 16 towns. The fitted model was applied to all footprints.

Three checks were made. (i) Five-fold cross-validation blocked by 0.05° tiles. (ii) A geographic transfer test: the model was trained on labels in the Kampala area only and tested on the 455 labelled buildings within 8 km of 15 other towns. (iii) A label-bias test: within 8 km of each town, the multi-storey share among tagged buildings was compared with the predicted share among all buildings. No open building-level height data for Uganda were available to serve as an independent reference; Microsoft's global building footprints carry no heights for Uganda.

### 2.3 Observed urban heat island

MODIS Aqua land-surface temperature (MYD11A2 v061, 8-day composites, 1 km) for 2020–2021 was averaged on a 0.01° grid for the day (13:30) and night (01:30) overpasses, with the Copernicus 90 m DEM on the same grid. Building density per pixel came from GHS-OBAT. For each 0.25° cell, rural land pixels (fewer than 20 buildings per km², lakes excluded) in the surrounding 3 × 3 cells define a reference temperature that varies linearly with elevation; the surface urban heat island (SUHI) of a pixel is its temperature minus the reference at its own elevation. City values average urban-core pixels (at least 1,000 buildings per km²) within 10 km of each centre.

Surface and air heat islands differ. The daily-mean air-temperature heat island was taken as 0.5–1.0 times the night-time SUHI (low and central estimates), a conservative choice because daytime SUHI is several times larger. Relative humidity was lowered at constant vapour pressure, RH′ = RH · e_s(T)/e_s(T + ΔT), and the probability of corrosion initiation was computed with the carbonation model of Paper A. A sensitivity analysis with fixed heat islands of 1–3 °C was also run.

### 2.4 Building-level risk in Greater Kampala

For each of 2.25 million footprints in Greater Kampala (0.10–0.60°N, 32.35–32.85°E), the classifier's multi-storey probability was combined with the probability of corrosion initiation by 2100 for the building's construction epoch and its pixel's heat island (central estimate). The latter came from the physical model at the Kampala site, evaluated on a grid of heat-island values from 0 to 4 °C and interpolated per building. The expected number of multi-storey buildings past initiation is the sum of the two probabilities' product.

### 2.5 Rainfall extremes and wetting–drying cycles

Daily precipitation from eight NEX-GDDP-CMIP6 models (SSP2-4.5 and SSP5-8.5) was reduced to annual indices: wettest day, wettest five days, days with at least 20 mm and 50 mm, wet days, wetting events (a wet day after a dry day) and longest dry spell. Changes between 1995–2014 and 2081–2100 are reported as ensemble-mean relative changes with model agreement, because 0.25° data understate local extremes.

## 3. Results

### 3.1 Growth of the building stock

Uganda's building stock has spread outward across the whole country rather than concentrating in Kampala (Figure 1). Buildings in newly built-up areas rose from 2.4 million in each of the 1980s and 1990s to 5.5 million in the 2000s and 6.5 million in the 2010s. The Kampala area held 17–21% of the buildings dated before 2000 but only 12% in the 2000s and 5% in the 2010s. The densest outward growth before 2000 was around Kampala, at up to 640 buildings per km²; in the 2010s it was spread across the south-west, the east and the Kampala belt, at up to about 100 per km².

[image: Figure 1. Growth of the building stock]

*Figure 1. Buildings per km² in areas that became built-up in each epoch (GHS-OBAT, all heights), and national totals by epoch. Dot: Kampala.*

### 3.2 Neighbourhood heights overstate the multi-storey stock

The neighbourhood-height proxy flags 2.42 million buildings as two or more storeys; the classifier estimates about 0.62 million (Figure 2b). The difference is largest for older epochs, where whole neighbourhoods of mixed buildings exceed the 4.5 m threshold. Unlike the proxy, the classifier does not show a collapse in multi-storey construction in the 2010s, which in the proxy reflects the 2018 height data.

The classifier separates multi-storey buildings well within its training area (spatially blocked AUC 0.87–0.99, median 0.98) but transfers less well. Trained on Kampala only and tested on 455 labelled buildings in 15 other towns, it reaches an AUC of 0.78 and an average precision of 0.45, against a base rate of 0.17. The labels themselves are biased, in opposite directions (Figure 2a). In Kampala, where most tags come from mapping of informal settlements, 3.7% of the 21,016 tagged buildings are multi-storey, against 13% predicted for all buildings within 8 km. In secondary towns, where mappers tagged prominent buildings, 20–79% of tagged buildings are multi-storey, against 4–15% predicted.

Re-weighting Paper A's stock results with the classifier's counts changes the share of the stock past corrosion initiation little (46–72% by 2100, against 50–76%) but cuts the number of buildings affected by climate change about four-fold, from 373,000–614,000 to 90,000–152,000.

[image: Figure 2. Multi-storey buildings]

*Figure 2. (a) Share of buildings with two or more storeys within 8 km of each town: OpenStreetMap-tagged buildings (number in brackets) against the classifier's prediction for all buildings. (b) Multi-storey buildings in Uganda by construction epoch: neighbourhood-height proxy against machine-learning estimate.*

### 3.3 Observed urban heat island

The observed surface heat island is large by day and modest at night (Figure 3a). Urban cores are 1.9–7.2 °C warmer than elevation-matched rural land at 13:30, with Kampala (7.2 °C) and Kasese (6.1 °C) highest, and 0.1–1.4 °C warmer at 01:30.

Even the conservative air heat island derived from the night-time value raises the probability of initiation noticeably (Figure 3b). In Kampala, for specified concrete with blended cement, the probability by 2100 rises from 36% to 48–58% without climate change and from 69% to 78–85% under SSP5-8.5. In Mbale, where the night-time heat island is only 0.1 °C, the change is 2–4 points; in the other cities it is 4–11 points. The fixed-offset analysis (Figure 4) shows why: a 1 °C heat island lowers relative humidity by about 5 points, and carbonation is very sensitive to humidity at 75–85%, so in humid Kampala 1 °C has an effect comparable to SSP5-8.5 alone.

[image: Figure 3. Observed urban heat island]

*Figure 3. (a) Surface urban heat island of urban cores (at least 1,000 buildings per km² within 10 km of the centre), MODIS Aqua 2020–2021, relative to elevation-matched rural land. (b) Probability of corrosion initiation by 2100 for specified concrete with blended cement cast in 2000, without and with the observed heat island (air heat island = 0.5 or 1.0 × night-time surface value).*

[image: Figure 4. Heat-island sensitivity]

*Figure 4. Probability of corrosion initiation by 2100 against a fixed urban heat island of 0–3 °C, with relative humidity lowered at constant vapour pressure.*

### 3.4 Building-level risk in Greater Kampala

Greater Kampala has 2.25 million footprints, of which about 340,000 are expected to be multi-storey. The night-time heat island reaches 1.5–2 °C in the city centre and fades within about 10 km (Figure 5a); weighted by multi-storey buildings, it averages 0.4 °C. If built as specified with blended cement, about 143,000 multi-storey buildings pass corrosion initiation by 2100 without climate change or heat island, and 245,000 under SSP5-8.5. The observed heat island adds a further 40,000 without climate change and 27,000 under SSP5-8.5, concentrated in the dense centre and along the main growth corridors (Figure 5b, c). If built as concrete typically is on site, almost all multi-storey buildings (about 336,000–340,000) pass initiation by 2100 in every case.

[image: Figure 5. Kampala building-level risk]

*Figure 5. Greater Kampala at 0.01°: (a) night-time surface heat island; (b) expected multi-storey buildings past corrosion initiation by 2100 under SSP5-8.5 with the heat island, per km²; (c) the part added by the heat island. Specified concrete with blended cement.*

### 3.5 Rainfall extremes and wetting–drying cycles

Heavy rainfall intensifies everywhere, while wetting–drying cycles hardly change (Figure 6). By 2081–2100 the wettest day of the year is 22% heavier under SSP2-4.5 and 40% heavier under SSP5-8.5, averaged over the RC stock, and at least six of eight models agree on an increase in every grid cell. Days with at least 20 mm become two to four times more frequent, from a small base. Wetting events change by no more than about 10% anywhere, with weak model agreement, and dry spells shorten by 10–30% in the north-east. Every RC building lies in a cell where the wettest day intensifies by more than 20% under SSP5-8.5.

[image: Figure 6. Rainfall extremes]

*Figure 6. Change in rainfall indices, 2081–2100 relative to 1995–2014, under SSP5-8.5 (eight-model mean; land cells with buildings). Hatching: fewer than six of eight models agree on the sign.*

## 4. Discussion

### 4.1 Counting exposed buildings

Open footprint data with neighbourhood attributes are good enough to describe how a building stock has grown and aged, but not to count multi-storey buildings. Applying a height threshold to a 100 m average height assigns the neighbourhood's height to every building in it, which overstates Uganda's multi-storey stock about four-fold. For risk assessment this matters in a specific way: the share of the stock at risk is robust, because it depends mainly on age and climate, but the number of buildings at risk is not. Studies that report counts of exposed buildings from GHSL-type data should therefore treat them as upper bounds.

The machine-learning estimate is better but not definitive. Its labels are scarce outside Kampala and biased in both directions, and it transfers to unseen towns with moderate skill (AUC 0.78). Building-level heights, from Google Open Buildings 2.5D, stereo imagery or a field sample, would allow a proper calibration. Until then, the proxy and the classifier bracket the plausible range.

### 4.2 Urban heat as a design climate

The urban heat island acts on carbonation through two channels: warmer air speeds the reaction, and the same vapour pressure in warmer air means lower relative humidity, which matters most in humid cities. Even a modest night-time surface heat island, scaled down conservatively, raises the probability of initiation in Kampala by 12–22 points and adds 27,000–40,000 multi-storey buildings past initiation by 2100. Regional climate projections, including bias-corrected downscaled ones, do not resolve this effect. Durability design for city centres in humid tropical climates should therefore use urban rather than regional temperature and humidity, or add an equivalent allowance to the cover.

The main uncertainty is the link between surface and air temperature. Daytime surface heat islands of up to 7 °C were not used directly; air-temperature measurements in Kampala's centre and outskirts would replace the 0.5–1.0 scaling.

### 4.3 Heavier rain

Heavier rainfall is a separate hazard for the growing stock. It acts through flooding, scour and foundation movement, particularly where new building spreads onto low-lying land and wetland margins, rather than through carbonation. For carbonation, wetter conditions slow the process on rain-exposed faces, and the near-constant number of wetting cycles gives no reason to expect faster corrosion from cycling.

### 4.4 Growth and building control

Since 2000, new building has dispersed across the country, with only 5–12% in the Kampala area. Durability regulation and building control focused on Kampala will therefore miss most new construction, even though Kampala still holds most multi-storey buildings and most of the heat-island effect.

### 4.5 Limitations

- Construction epochs date 100 m cells by their first built-up majority, so densification inside existing neighbourhoods is not captured.
- Multi-storey labels are scarce and biased; no independent building-level heights were available.
- Surface heat islands were converted to air heat islands with an assumed factor of 0.5–1.0, and the heat island was held constant in time, although it may grow with the city.
- Rainfall extremes are relative changes from 0.25° data and are not linked to a damage model.

## 5. Conclusions

1. Uganda's building stock grew from 2.4 million new buildings per decade in the 1980s and 1990s to 6.5 million in the 2010s, and growth has moved out of Kampala: only 5% of 2010s building was in the Kampala area.
2. Counting multi-storey buildings from neighbourhood heights overstates them about four-fold (2.42 million against about 0.62 million). Shares of the stock at risk are robust to this; building counts are not.
3. The observed urban heat island, through warming and drying, raises the probability of corrosion initiation in Kampala from 36% to 48–58% by 2100 without climate change, and adds 27,000–40,000 multi-storey buildings past initiation in Greater Kampala.
4. The wettest day of the year intensifies by 22–40% over the stock by 2081–2100, while wetting–drying cycles barely change; heavier rain is a flood and foundation hazard rather than a carbonation driver.

Exposure models for tropical building stocks should report building counts with their uncertainty, and durability design for humid tropical cities should use urban rather than regional climate.

## Data availability

All inputs are open: GHS-OBAT, NEX-GDDP-CMIP6, MODIS MYD11A2 and the Copernicus DEM (via the Microsoft Planetary Computer), and OpenStreetMap. Code and processed results are in the GitHub repository github.com/gavacharles/uganda-concrete-climate (to be made public and archived on Zenodo on submission). OpenStreetMap-derived data are regenerated by the code under the ODbL.

## References

Author-year list; convert to the target journal's style on submission. Entries marked † need their details checked.

- Companion study (Paper A, in preparation). Climate change and carbonation-induced corrosion risk of a rapidly growing concrete building stock: a probabilistic, building-age-aware assessment for Uganda.
- European Space Agency (2021). Copernicus Global Digital Elevation Model (GLO-90). https://doi.org/10.5270/ESA-c5d3d65
- Florio, P., et al. (2025). GHS-OBAT: global, open building attribute data reporting age, function, height and compactness at footprint level. *Data in Brief* 61, 111751. https://doi.org/10.1016/j.dib.2025.111751
- Meinshausen, M., et al. (2020). The shared socio-economic pathway (SSP) greenhouse gas concentrations and their extensions to 2500. *Geoscientific Model Development* 13, 3571–3605. https://doi.org/10.5194/gmd-13-3571-2020
- † Microsoft Open Source, McFarland, M., Emanuele, R., Morris, D., Augspurger, T. (2022). microsoft/PlanetaryComputer. Zenodo. https://doi.org/10.5281/zenodo.7261897
- Microsoft (2026). Global ML Building Footprints. https://github.com/microsoft/GlobalMLBuildingFootprints
- OpenStreetMap contributors (2026). OpenStreetMap data for Uganda, extract of 2 October 2026 (Geofabrik). Open Database Licence.
- Pedregosa, F., et al. (2011). Scikit-learn: machine learning in Python. *Journal of Machine Learning Research* 12, 2825–2830.
- Thrasher, B., et al. (2022). NASA Global Daily Downscaled Projections, CMIP6. *Scientific Data* 9, 262. https://doi.org/10.1038/s41597-022-01393-4
- Wan, Z., Hook, S., Hulley, G. (2021). MODIS/Aqua Land Surface Temperature/Emissivity 8-Day L3 Global 1km SIN Grid V061. NASA EOSDIS Land Processes DAAC. https://doi.org/10.5067/MODIS/MYD11A2.061
- † Urban heat island studies for East African cities, including Kampala, to add from the literature.
