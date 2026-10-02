# Paper B: Exposure of Uganda's Building Stock to Climate-Driven Concrete Deterioration

## Abstract

To be written when the building-level map, observed urban heat and independent classifier check are in. Planned headline findings: open neighbourhood-height data overstate Uganda's multi-storey stock about four-fold; a 1 °C urban heat island, with its drier air, raises corrosion-initiation probability as much as SSP5-8.5; the wettest day of the year intensifies by 22–40% while wetting–drying cycles barely change; and new building since 2000 has spread across the country rather than concentrating in Kampala.

## 1. Introduction

Assessments of climate-driven deterioration of reinforced concrete (RC) usually take two inputs as given: how many buildings are exposed, and what climate they experience. Both are uncertain in fast-growing tropical countries. Building inventories rarely exist, so exposure models rely on open gridded data such as the Global Human Settlement Layer (GHSL) and its footprint-level derivative GHS-OBAT \[Florio et al., 2025\], whose heights and construction epochs are neighbourhood values. Climate inputs come from regional projections that do not resolve urban heat islands, which in East African cities add local warming on top of regional trends.

The companion study (Paper A) estimated carbonation-induced corrosion risk for Uganda's RC stock under CMIP6 scenarios. This paper examines the exposure side of that estimate. Its objectives are to:

1. map how and where Uganda's building stock has grown since before 1980;
2. test whether neighbourhood-height data identify multi-storey (RC-frame) buildings, using OpenStreetMap storey counts and a machine-learning classifier;
3. quantify how an urban heat island, through both warming and drying, changes carbonation risk; and
4. assess projected changes in rainfall extremes and wetting–drying cycles over the building stock.

## 2. Data and methods

### 2.1 Building stock and growth

GHS-OBAT gives every building footprint in Uganda (22.5 million) a construction epoch, a height and a use \[Florio et al., 2025\]. Height is the GHS-BUILT-H average building height of the surrounding 100 m cell in 2018. The epoch is the earliest decade by which at least half of the cell's present built-up surface existed (GHS-AGE), so infill and replacement inside older neighbourhoods are dated to the earlier epoch. Buildings were aggregated to a 0.25° grid by epoch to map outward growth, expressed as new buildings per km².

### 2.2 Multi-storey buildings from OpenStreetMap and machine learning

OpenStreetMap buildings with a storey count (building:levels) were extracted from the Uganda extract and matched to the nearest GHS-OBAT footprint within about 10 m: 104,014 matches, of which 1,811 have two or more storeys. A gradient-boosting classifier predicts the probability that a building has two or more storeys from footprint area, perimeter and shape factor, use, GHS-OBAT neighbourhood height and epoch, building density and mean footprint size in about 220 m bins, and distance to the nearest of 16 towns. It was evaluated by five-fold cross-validation blocked by 0.05° tiles and applied to all footprints.

### 2.3 Urban heat island

A constant urban air-temperature excess of 1, 2 or 3 °C was added to the ERA5-adjusted climate at six cities, with relative humidity lowered at constant vapour pressure, RH′ = RH · e\_s(T)/e\_s(T + ΔT). Corrosion-initiation probability was then computed with the probabilistic carbonation model of Paper A for specified concrete with blended cement.

### 2.4 Rainfall extremes and wetting–drying cycles

Daily precipitation from eight NEX-GDDP-CMIP6 models (SSP2-4.5 and SSP5-8.5) was reduced to annual indices: wettest day, wettest five days, days with at least 20 mm and 50 mm, wet days, wetting events (a wet day after a dry day) and longest dry spell. Changes between 1995–2014 and 2081–2100 are reported as ensemble-mean relative changes with model agreement, because 0.25° data understate local extremes.

### 2.5 Surrogate model

A gradient-boosting classifier trained on 1.08 million Monte Carlo realisations of the carbonation model reproduces initiation by 2100 (held-out AUC 0.975; 0.970–0.976 when a city is left out). It will be used to map risk building by building in Kampala (to do).

## 3. Results

### 3.1 Growth of the building stock

Uganda's building stock has spread outward across the whole country rather than concentrating in Kampala (Figure 1). Buildings in newly built-up areas rose from 2.4 million in each of the 1980s and 1990s to 5.5 million in the 2000s and 6.5 million in the 2010s. The Kampala area held 17–21% of the buildings dated before 2000 but only 12% in the 2000s and 5% in the 2010s. The densest outward growth before 2000 was around Kampala, at up to 640 buildings per km²; in the 2010s it was spread across the south-west, the east and the Kampala belt, at up to about 100 per km².

&#91;image: Figure 1. Growth of the building stock\]

*Figure 1. Buildings per km² in areas that became built-up in each epoch (GHS-OBAT, all heights), and national totals by epoch. Dot: Kampala.*

### 3.2 Neighbourhood heights overstate the multi-storey stock

Among OpenStreetMap-labelled buildings in the Kampala area, 5–16% have two or more storeys in each epoch, against 69–99% flagged by the 4.5 m neighbourhood-height proxy (Figure 2b). The multi-storey share rises from 5% before 1980 to 14–16% in the 2000s and 2010s, so recent construction is not less multi-storey; the low proxy count for the 2010s reflects the 2018 height data. The classifier separates multi-storey buildings well (cross-validated AUC 0.87–0.99, median 0.98; average precision 0.29–0.64 at a prevalence of 1–3%). Applied nationally, it gives about 0.62 million multi-storey buildings, against 2.42 million from the proxy (Figure 2c).

Re-weighting Paper A's stock results with these counts changes the share past corrosion initiation little (46–72% by 2100, against 50–76%) but cuts the number of buildings affected by climate change about four-fold, to 90,000–152,000.

&#91;image: Figure 2. Machine-learning results\]

*Figure 2. (a) Input importance in the surrogate model. (b) Share of buildings with two or more storeys by epoch in the Kampala area: height proxy versus OpenStreetMap labels. (c) Multi-storey buildings in Uganda by epoch: height proxy versus machine-learning estimate. (d) Measured natural carbonation coefficients of Portland cement concrete against the fib model (reported in Paper A; to be dropped from this figure).*

### 3.3 Urban heat island

Urban warming has a large effect because it also dries the air (Figure 3). With a 1 °C heat island, the probability of initiation by 2100 without climate change rises by 5–24 percentage points, most in the humid cities: in Kampala from 37% to 61%, and to 85% at 3 °C. This is comparable to the effect of SSP5-8.5 alone. At constant vapour pressure, 1 °C lowers relative humidity by about 5 points, and carbonation is very sensitive to humidity at 75–85%. Combined with SSP5-8.5, a 1 °C heat island raises the extra cover needed over 50 years from 5–8 mm to 10–13 mm, and a 3 °C one to 15–24 mm.

&#91;image: Figure 3. Urban heat island\]

*Figure 3. Probability of corrosion initiation by 2100 for specified concrete with blended cement cast in 2000, against a constant urban heat island, with relative humidity lowered at constant vapour pressure.*

### 3.4 Rainfall extremes and wetting–drying cycles

Heavy rainfall intensifies everywhere, while wetting–drying cycles hardly change (Figure 4). By 2081–2100 the wettest day of the year is 22% heavier under SSP2-4.5 and 40% heavier under SSP5-8.5, averaged over the RC stock, and at least six of eight models agree on an increase in every grid cell. Days with at least 20 mm become two to four times more frequent, from a small base. Wetting events change by no more than about 10% anywhere, with weak model agreement, and dry spells shorten by 10–30% in the north-east. Every RC building lies in a cell where the wettest day intensifies by more than 20% under SSP5-8.5.

&#91;image: Figure 4. Rainfall extremes\]

*Figure 4. Change in rainfall indices, 2081–2100 relative to 1995–2014, under SSP5-8.5 (eight-model mean; land cells with buildings). Hatching: fewer than six of eight models agree on the sign.*

### 3.5 Building-level risk in Kampala (to do)

The surrogate model will be applied to each footprint in Kampala, combining the classifier's multi-storey probability with corrosion-initiation probability, to map where risk concentrates within the city.

### 3.6 Observed urban heat (to do)

MODIS land-surface temperature will give an urban–rural difference for each grid cell, replacing the fixed 1–3 °C offsets of Section 3.3.

## 4. Discussion (outline)

- **Exposure data.** Neighbourhood-level heights and epochs are useful for growth and age, but counting multi-storey buildings from them overstates the RC stock about four-fold; risk shares are robust, building counts are not. Relevance for every user of GHSL or GHS-OBAT in exposure modelling.
- **Limits of the labels.** OpenStreetMap storey counts are concentrated in Kampala and may under-record upper storeys; the classifier is therefore best treated as a lower bound and needs an independent check.
- **Urban heat.** Design climates for city centres should include the heat island and its drying effect; regional projections alone understate carbonation risk in humid tropical cities.
- **Rainfall.** Heavier rainfall is a flood, scour and foundation hazard for the growing stock, separate from carbonation; wetting–drying cycles give no reason to expect faster corrosion.
- **Growth.** New building has dispersed across the country since 2000, so exposure and building control can no longer focus on Kampala alone.

## 5. Conclusions

To be written after the remaining analyses.

## References

Shared with Paper A, plus: Florio et al. (2025) GHS-OBAT; OpenStreetMap contributors (2026); Thrasher et al. (2022) NEX-GDDP-CMIP6; urban heat island literature for East African cities (to add).
