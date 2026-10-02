# Paper A: Climate Change and Corrosion Risk of Uganda's Concrete Building Stock

Oct 1, 2026 · @Gavamukulya Charles

## Working notes (remove before submission)

**Working title:** Climate change and carbonation-induced corrosion risk of a rapidly growing concrete building stock: a probabilistic, building-age-aware assessment for Uganda.

**Target journals** (check quartile and scope before choosing): *Structural Safety*, *Engineering Structures*, *Sustainable Cities and Society*, *Journal of Building Engineering*, *Climate Risk Management*.

| Section | Status | Depends on |
| --- | --- | --- |
| Introduction | First draft | Systematic review |
| Background | Updated with Scopus + OpenAlex review (188 studies) | — |
| Study area and data | First draft | — |
| Methodology | First draft | — (blended-cement factor calibrated) |
| Results | Complete with all 8 models: cities, national stock, adaptation | — |
| Discussion, Conclusions | First draft | Results |
| Abstract | First draft | Results |

Analysis code lives in `~/uganda-concrete-climate` (local).

## Abstract

Climate change is expected to accelerate carbonation-induced corrosion of reinforced concrete (RC), but its effect has not been assessed for East Africa, where building stocks are growing fastest. This study couples eight downscaled CMIP6 models (SSP2-4.5, SSP5-8.5) with a probabilistic fib carbonation model that accounts for site elevation, a blended-cement factor calibrated for Uganda's pozzolanic cements, and footprint-level building-age data for Uganda's multi-storey stock. For concrete built to specification, the probability of corrosion initiation by 2100 at six cities rises from 37–83% without climate change to 56–92% under SSP2-4.5 and 69–97% under SSP5-8.5. Nationally, the share of the stock past initiation rises from 50% to 66–76%, adding up to 373,000–614,000 buildings (upper bounds, as counts rest on neighbourhood-height data); two-thirds are in the Kampala metropolitan area. Construction quality dominates, however: built as concrete typically is on site, 86% of the stock has passed initiation by 2030 regardless of climate. With blended cement, a 30 mm cover misses a 0.10 target probability at five of six cities even without climate change, and 5–8 mm of extra cover offsets the climate effect over a 50-year design life at low cost. Cover requirements in Uganda should depend on cement type and include a climate allowance, and building control should prioritise site checks of cover and curing.

**Keywords:** carbonation; reinforcement corrosion; climate change; CMIP6; reliability; building stock; Uganda; East Africa

## 1. Introduction

Corrosion of reinforcing steel is the most common cause of premature deterioration in reinforced concrete (RC) structures. In inland environments it is driven mainly by carbonation: atmospheric CO₂ diffuses into the concrete cover, lowers the pore-solution pH and depassivates the steel. The rate of this process depends on the CO₂ concentration, temperature and relative humidity, which climate change is altering. Probabilistic studies have shown that rising CO₂ and warming can raise carbonation-induced damage risk by up to about 16% by 2100 in Australia \[Stewart et al., 2011\]. Comparable increases have been reported for China \[Peng and Stewart, 2014\], Canada \[Talukdar et al., 2012\] and Europe \[Bastidas-Arteaga et al., 2022; Dimova et al., 2025\].

This body of work is concentrated in temperate and subtropical regions. Tropical evidence is recent and limited to a few countries, such as Brazil \[Pinheiro Teodoro et al., 2026\] and Vietnam \[Tran, 2021\]. In sub-Saharan Africa, service-life studies exist for Johannesburg and Durban \[Ekolu, 2020b\] and Lusaka \[Zulu and Miyazato, 2024\], and a deterministic service-life design study exists for Kampala \[Ekolu, 2020a\]. None of these combines downscaled climate projections, realistic as-built concrete quality and the size and age of the exposed building stock.

Uganda illustrates why that combination matters. Kampala's built-up area expanded rapidly from the late 1980s \[Vermeiren et al., 2012\], and its urban share of land rose from 7% in 1989 to 55% in 2015 \[Muchelo et al., 2024\]. Most of this new stock is RC frame construction. It is built largely with Portland-pozzolana and pozzolanic cements that use local volcanic materials \[Buregyeya et al., 2018\], which typically carbonate faster than plain Portland cement. Construction-quality problems are well documented, including poor workmanship, weak supervision and non-compliance with specifications \[Alinaitwe and Ekolu, 2014; Kakitahi et al., 2015; Alinaitwe, 2023\]. Meanwhile, CMIP6 projects warming of about 3.5 °C over central East Africa by the end of the century under high emissions \[Almazroui et al., 2020\].

The equatorial highland setting also differs physically from the settings studied so far. Uganda is warm but humid, which slows carbonation. Its main cities lie at 1,000–1,500 m elevation, where lower air pressure reduces the mass concentration of CO₂ at a given mole fraction. Whether warming dominates these effects, and by how much, has not been quantified.

This study addresses that gap. Its objectives are to:

1. quantify how projected changes in temperature, relative humidity and CO₂ under SSP2-4.5 and SSP5-8.5 alter the probability of carbonation-induced corrosion initiation across Uganda's climate zones;
2. compare concrete as specified with concrete as typically built, to separate the effect of climate from that of construction quality;
3. combine these results with building-age data to estimate the share of Uganda's RC building stock reaching corrosion initiation by 2050 and 2100; and
4. determine the additional cover or concrete quality needed to offset the climate effect.

The paper is organised as follows. Section 2 reviews prior work, drawing on a systematic search. Section 3 describes the study area and data. Section 4 presents the probabilistic model. Section 5 reports the results, Section 6 discusses their implications for design and policy, and Section 7 concludes.

## 2. Background

This review draws on a systematic search of Scopus covering four themes, run on 1 October 2026. The search identified 2,891 records, of which 2,745 were screened and 137 studies were included after two-stage screening. Search strings, eligibility criteria and the PRISMA flow are given in Supplementary Material S1.

### 2.1 Climate change and carbonation-induced corrosion

The standard approach couples an engineering carbonation model, usually the *fib* Model Code formulation \[fib, 2006\] or a diffusion-based variant \[Papadakis et al., 1991\], with time-varying CO₂, temperature and humidity from emission scenarios. Stewart et al. \[2011, 2012\] and Wang et al. \[2011\] established a reliability-based framework for Australia. It was later extended to China \[Peng and Stewart, 2014\], used for spatial reliability analysis \[Peng and Stewart, 2014b\], and used to show that 5–10 mm of extra cover offsets the climate effect cost-effectively. Talukdar et al. \[2012\] calibrated a carbonation model experimentally for Canadian cities. Bastidas-Arteaga and co-workers developed probabilistic and cost-benefit treatments \[Bastidas-Arteaga et al., 2013; Bastidas-Arteaga and Stewart, 2015\] and a multi-region method for handling climate data at different resolutions \[Bastidas-Arteaga et al., 2022\].

Recent work has moved from single sites to building stocks. Dimova et al. \[2025\] assessed the European RC building stock to 2100 and found that, without climate change, carbonation would not reach the cover by 2100, but it would under severe scenarios. Val et al. \[2025\] showed that low-carbon binders, which carbonate faster, make the climate effect more critical. Pinheiro Teodoro et al. \[2026\] applied bias-corrected downscaling at 0.2° resolution across Brazil. The field has grown rapidly since 2010, with 2,061 Scopus records to 2025 \[Cervantes et al., 2026\].

### 2.2 Carbonation in tropical and African settings

Long-term exposure programmes show high carbonation rates in tropical urban environments \[Troconis de Rincon et al., 2014; Antoni et al., 2024; Cascudo et al., 2025\]. Results from Singapore indicate that 28-day strength and w/c ratio are reliable predictors under natural tropical exposure \[Tam et al., 2008\]. In southern Africa, the durability-index approach links early-age tests to service life \[Alexander, 2018; Fotso Lele, 2023\]. Field measurements on South African bridges \[Alexander et al., 2007\] and cover-depth control studies \[Alexander et al., 2012\] support model calibration. Ekolu's natural carbonation prediction (NCP) model, calibrated on 553 measurements, handles blended cements explicitly \[Ekolu and Solomon, 2022; Ekolu, 2025\].

Two African studies apply climate projections. Ekolu \[2020b\] performed a reliability analysis for Johannesburg and Durban under rising CO₂. Zulu and Miyazato \[2024\] projected a 50–52% reduction in corrosion initiation time in Lusaka over 100 years, holding relative humidity constant. Ekolu \[2020a\] examined service-life design for Kampala and noted that carbonation is the governing mechanism there; its abstract gives no indication that climate projections were used.

### 2.3 Ugandan materials and construction quality

Ugandan cements are mostly Portland-pozzolana (CEM II/B-P) and pozzolanic (CEM IV) types blended with local volcanic materials. These include kamafugites and carbonatitic lavas whose pozzolanic reactivity is relatively low: at 20% replacement they reach 81–89% of the strength of CEM I after 180 days and gain no strength after 28 days \[Buregyeya et al., 2018; Balu-Tabaaro, 2014\]. Design strengths of 25–30 MPa are typical \[Ekolu, 2020a\]. As-built quality is variable: a distressed Kampala building averaged about 5 MPa by non-destructive testing \[Caleb et al., 2023\], and clay in fine aggregate measurably reduces strength \[Kwikiriza, 2018\]. Recycled rebar shows elevated yield strength \[Senfuka et al., 2013\]. Systemic causes of failure include poor workmanship, inadequate supervision and non-compliance \[Alinaitwe and Ekolu, 2014; Kakitahi et al., 2015\], and these worsened during the COVID-19 lockdowns \[Alinaitwe, 2023\]. No published field data on concrete cover or carbonation depth in Ugandan buildings were found.

### 2.4 Growth and exposure of the building stock

Kampala's growth has been mapped from Landsat imagery and modelled with scenario and cellular-automata approaches \[Vermeiren et al., 2012; Muchelo et al., 2024\]. Secondary towns such as Mbarara and Arua are also growing quickly. A uniform exposure model for Africa provides building typologies and stock projections to 2050 \[Paul et al., 2022\]. Open building-level data now provide construction epoch, height and use for each footprint \[Florio et al., 2025\], and annual building presence and height for 2016–2023 \[Google Open Buildings 2.5D Temporal\]. Urban heat islands in East African cities add local warming on top of regional trends \[Li et al., 2021\]. These data make a building-age-aware exposure analysis possible for the first time.

### 2.5 Research gap

No study has assessed climate-driven carbonation for East Africa's equatorial highland climates. None has combined downscaled projections that include humidity with the elevation effect on CO₂ concentration, the variable quality of as-built concrete and the age structure of a fast-growing building stock. This study addresses all four.

## 3. Study area and data

### 3.1 Study area and representative sites

Uganda lies on the equator between about 1.5°S and 4.2°N. Most of the population lives on a plateau at 900–1,500 m. The climate is tropical but moderated by altitude, with two rainy seasons in the south and a single long season in the north. Six cities were selected to represent the main climate zones and the fastest-growing urban centres.

| City | Region and climate | Latitude, longitude | Elevation (m) |
| --- | --- | --- | --- |
| Kampala | Central; humid, bimodal rainfall, Lake Victoria influence | 0.35°N, 32.58°E | 1,174 |
| Mbale | Eastern; humid, foot of Mt Elgon | 1.08°N, 34.18°E | 1,121 |
| Gulu | Northern; drier, unimodal rainfall | 2.77°N, 32.30°E | 1,099 |
| Arua | West Nile; drier, unimodal rainfall | 3.02°N, 30.91°E | 1,215 |
| Mbarara | South-western; cooler highland | 0.61°S, 30.65°E | 1,446 |
| Kasese | Western rift floor; hot, drier | 0.18°N, 30.08°E | 990 |

Table 1. Representative cities. Elevations are from the Open-Meteo elevation service (SRTM-based) at the city coordinates.

### 3.2 Climate data

Daily near-surface air temperature (tas), relative humidity (hurs) and precipitation (pr) were taken from NASA NEX-GDDP-CMIP6 \[Thrasher et al., 2022\]. This dataset is bias-corrected and statistically downscaled to 0.25° (about 28 km). Eight models were used: ACCESS-CM2, EC-Earth3, GFDL-ESM4, MIROC6, MPI-ESM1-2-HR, MRI-ESM2-0, NorESM2-MM and UKESM1-0-LL. They span low to high climate sensitivity and all provide humidity. The data cover the historical period (1980–2014) and two scenarios (2015–2100): SSP2-4.5 (intermediate) and SSP5-8.5 (high emissions). Daily data were reduced to annual mean temperature, annual mean relative humidity, and the annual number of days with at least 2.5 mm of rain, which is used to calculate time of wetness. A no-climate-change reference holds each model's 1995–2014 climate and the 2014 CO₂ concentration constant.

The downscaled data were checked against the ERA5 reanalysis \[Hersbach et al., 2020\] at the six cities for 1995–2014 (Section 5.1). Station records from the Uganda National Meteorological Authority could not be obtained, so ERA5 is the only independent reference.

### 3.3 Atmospheric CO₂

Global mean CO₂ mole fractions were taken from the CMIP6 concentration dataset \[Meinshausen et al., 2017, 2020\]. Values are 339 ppm in 1980 and 398 ppm in 2014, rising to 507 ppm (2050) and 603 ppm (2100) under SSP2-4.5, and to 563 ppm and 1,135 ppm under SSP5-8.5. Mole fractions were converted to mass concentration using the ideal gas law at each site's mean temperature and its pressure from the barometric formula. At Kampala's elevation, air pressure is about 13% lower than at sea level, so CO₂ mass concentration is lower by the same proportion. An urban enhancement factor of 1.10 accounts for local emissions \[after Stewart et al., 2011\].

### 3.4 Building stock data

The age and size of the building stock come from GHS-OBAT \[Florio et al., 2025\], which gives every building footprint in Uganda (22.5 million) a construction epoch (before 1980, 1980–1990, 1990–2000, 2000–2010, 2010–2020), a mean height from GHS-BUILT-H and a residential or non-residential use. Buildings with a mean height of at least 4.5 m (two or more storeys) are taken as likely RC frames; single-storey buildings are mostly load-bearing masonry and are excluded. This leaves 2.42 million buildings with 463 million m² of floor area, aggregated to the 0.25° climate grid (346 cells). Floor area is footprint area times the number of storeys, taken as height divided by 3 m.

Two properties of GHS-OBAT matter for this study \[Florio et al., 2025\]. Building height is the GHS-BUILT-H average height of the surrounding 100 m cell in 2018, not the height of the building itself, so the 4.5 m threshold identifies buildings in taller neighbourhoods and overstates the number of multi-storey buildings; a companion study estimates the overstatement at about four-fold \[Companion study, in preparation\]. Building counts are therefore upper bounds, and results are mainly reported as shares of the stock, which are robust to the count. The construction epoch is the earliest decade by which at least half of the cell's present built-up surface existed (GHS-AGE), so infill inside older neighbourhoods is dated to the earlier epoch.

## 4. Methodology

The assessment couples projected climate and CO₂ with a probabilistic carbonation model, then applies the results to the building stock by age (Figure 1). All code is open and reproducible (Data availability).

&#91;embedded content: Figure 1. Assessment framework\]

### 4.1 Carbonation model

Carbonation depth follows the *fib* Model Code formulation \[fib, 2006; fib, 2013\], extended to time-varying conditions. For a member cast in year t₀, the depth at time t is

```latex
x_c(t) = \sqrt{\int_{t_0}^{t} 2\, k_e(\tau)\, k_c\, k_T(\tau)\, \left(k_t R^{-1}_{ACC,0} + \varepsilon_t\right) C_S(\tau)\, d\tau} \; \cdot \; W(t - t_0)
```

The terms are as follows:

- k\_e is the humidity function ((1 − RH^5)/(1 − 0.65^5))^2.5, which is near zero in saturated concrete and peaks at moderate humidity.
- k\_c = (t\_c/7)^b\_c accounts for curing duration t\_c in days.
- k\_t and ε\_t convert accelerated-test results to natural conditions.
- R⁻¹\_ACC,0 is the inverse effective carbonation resistance of the concrete.
- C\_S is the CO₂ mass concentration at the surface.
- W is the weather function, which reduces carbonation in members wetted by rain.

Temperature enters through an Arrhenius factor on the diffusion rate, following Stewart et al. \[2011\]:

```latex
k_T(\tau) = \exp\left[\frac{E}{R}\left(\frac{1}{T_{ref}} - \frac{1}{T(\tau)}\right)\right], \quad E = 40\ \text{kJ/mol},\; T_{ref} = 293\ \text{K}
```

The integral is evaluated in annual steps using each year's mean temperature, mean humidity and CO₂. Corrosion is taken to initiate when x\_c reaches the cover depth. The probability of corrosion initiation at time t is P\_i(t) = P\[x\_c(t) ≥ c\].

The model was checked against the *fib* reference case (CEM I, w/c 0.50, 7-day curing, 65% RH, 20 °C, sheltered, 50 years). It gives a mean depth of 15.2 mm, consistent with a hand calculation at mean values (15.7 mm).

### 4.2 Input distributions

Two concrete classes are compared: concrete *as specified* in typical designs, and concrete *as built* under common site practice.

**Blended-cement factor.** The fib resistance values are for CEM I, so a multiplier is needed for the Portland-pozzolana (CEM II/B-P) and pozzolanic (CEM IV) cements used in Uganda. It was derived from two sources. In the natural carbonation prediction model, depth scales with concrete strength f as f^g, with g = −1.5 for CEM I and g = −1.4 for CEM II/B and CEM IV/A \[Ekolu and Solomon, 2022, Table 1\]. Ugandan kamafugite and carbonatite pozzolans reach 81–89% of the strength of CEM I at 20% replacement after 180 days, and gain no strength after 28 days \[Buregyeya et al., 2018\]. Taking 75–89% to cover the 21–35% pozzolan content of CEM II/B-P, and a CEM I cube strength of 25–30 MPa, blended concrete carbonates 1.6–2.1 times deeper than CEM I at equal w/c. Because depth scales with the square root of R⁻¹, this corresponds to a multiplier of 2.6–4.4 on R⁻¹\_ACC,0.

| Variable | As specified | As built | Basis |
| --- | --- | --- | --- |
| w/c ratio | Uniform 0.50–0.55 | Uniform 0.55–0.70 | Design strengths of 25–30 MPa \[Ekolu, 2020a\]; site batching and added water \[Kwikiriza, 2018; Caleb et al., 2023\] |
| R⁻¹\_ACC,0, CEM I (10⁻¹¹ m²/s per kg/m³) | Lognormal; mean from *fib* table by w/c; s = 0.69m^0.78 | Same | fib \[2006\] |
| Blended-cement multiplier on R⁻¹\_ACC,0 | 2.6–4.4 (log-uniform) | 2.6–4.4 (log-uniform) | **Calibrated (Section 4.2): carbonation depths 1.6–2.1 times CEM I at equal w/c \[Ekolu and Solomon, 2022; Buregyeya et al., 2018\]** |
| Cover (mm) | Normal, mean 30, sd 5 | Normal, mean 22, sd 8, minimum 5 | Design 25–30 mm (BS 8110, EN 1992); Uganda's specification requires cover as drawn within ±3 mm \[MoWT, 2013, cl. 1.4.27\]; shortfalls in African practice \[Alexander et al., 2012; Tutu et al., 2022\] |
| Curing t\_c (days) | 7 | Uniform 1–3 | Specified: at least 7 days moist curing \[MoWT, 2013, cl. 1.4.19\]; as built: assumed shortfall in site practice |
| b\_c | Normal(−0.567, 0.024) | Same | fib \[2006\] |
| k\_t | Normal(1.25, 0.35) | Same | fib \[2006\] |
| ε\_t | Normal(1.0, 0.15) × 10⁻¹¹ | Same | fib \[2006\] |
| Urban CO₂ factor | 1.10 | 1.10 | Stewart et al. \[2011\] |
| Exposure | Outdoor, sheltered from rain | Same | Governing case for external frames |

*Table 2. Input distributions for concrete as specified and as built.*

### 4.3 Uncertainty propagation

For each site, scenario, concrete class and casting year, 10⁵ Monte Carlo realisations are drawn. Each realisation is assigned one of the eight climate models at random with equal weight, so model spread is carried into P\_i(t). Casting years run from 1980 to 2050 in 10-year steps. The no-climate-change reference uses the same samples, so differences between scenarios are not affected by sampling noise.

### 4.4 Building stock coupling

For each grid cell and construction epoch, casting years are drawn uniformly within the epoch (1960–1979 for the oldest epoch), and climate before 1980 is held at the 1980–1989 mean. The probability of initiation P\_i(t) is computed from 2×10⁴ Monte Carlo realisations per cell, epoch, concrete class and scenario, using the raw downscaled climate of that cell. The expected number of buildings, and the floor area, past initiation by year t is the cell's count times P\_i(t), summed over epochs and cells. Buildings completed after 2020 are not included, so the stock results describe today's building stock.

### 4.5 Adaptation

Adaptation is assessed for new construction cast in 2025, at the end of a 50-year design working life (2075) and at 2100. Two quantities are found by bisection on the sampled depths, using the same realisations in every scenario. The first is the extra cover Δc that brings P\_i under a scenario back to its no-climate-change value. The second is the mean cover needed to keep P\_i at or below 0.10, the target probability used by Val et al. \[2025\], keeping the cover scatter of each concrete class.

### 4.6 Sensitivity and model spread

**Sensitivity.** At Kampala and Arua, each input was moved to the ends of a plausible range while the others kept their distributions, and P\_i(2100) was recomputed with the same random numbers. The central case is SSP2-4.5 on the ERA5-adjusted baseline for members cast in 2000. The ranges are: emission scenario (no change, SSP5-8.5); single climate models (lowest and highest); raw humidity baseline; blended-cement factor (2.6, 4.4); w/c at either end of its range; mean cover ±5 mm; curing 3 or 14 days (1 or 7 days for as-built concrete); urban CO₂ factor (1.0, 1.2); activation energy (30, 50 kJ/mol); and no elevation correction.

**Model spread in the stock.** The national run was repeated separately for each climate model, with 5,000 realisations per cell and epoch, to show the range across models.

## 5. Results

All results use the full ensemble of eight climate models.

### 5.1 Projected climate at the six cities

All six cities warm by 2.5–2.6 °C under SSP2-4.5 and 4.3–4.5 °C under SSP5-8.5 by 2081–2100, relative to 1981–2014 (ensemble means; model range 1.8–4.2 °C and 2.6–7.0 °C). Warming accelerates after 2050 under SSP5-8.5 (Figure 2). Changes in mean relative humidity are small, between −1.0 and +3.2 percentage points, so CO₂ and temperature drive the change in carbonation.

&#91;image: Figure 2. Projected warming at six Ugandan cities\]

*Figure 2. Annual mean temperature change relative to 1995–2014 at six cities (11-year running mean). Lines are ensemble means; shading spans the eight models. Labels give the 2081–2100 mean.*

The downscaled data differ from ERA5 in the historical period. NEX-GDDP-CMIP6 relative humidity is 12–14 points higher than ERA5 at Arua, Kasese and Mbarara, and temperature is 1.3–2.6 °C higher at Arua, Gulu, Kampala and Mbale (Table 3). City results are therefore given for two baselines: the downscaled values as they are ("raw") and a delta-change baseline that adds each model's projected change to the ERA5 1995–2014 climate.

| City | NEX tas (°C) | ERA5 tas (°C) | NEX RH (%) | ERA5 RH (%) | ΔT SSP2-4.5 (°C) | ΔT SSP5-8.5 (°C) |
| --- | --- | --- | --- | --- | --- | --- |
| Kampala | 23.2 | 21.8 | 80.6 | 81.8 | 2.5 | 4.3 |
| Mbale | 24.5 | 21.9 | 75.3 | 80.3 | 2.5 | 4.3 |
| Gulu | 24.9 | 23.5 | 77.7 | 71.2 | 2.6 | 4.3 |
| Arua | 24.0 | 22.7 | 81.0 | 67.0 | 2.6 | 4.5 |
| Mbarara | 20.6 | 20.6 | 84.6 | 72.5 | 2.5 | 4.4 |
| Kasese | 23.8 | 23.8 | 88.2 | 75.6 | 2.6 | 4.5 |

*Table 3. Historical values are 1981–2014 means; changes are 2081–2100 relative to 1981–2014 (ensemble mean).*

### 5.2 Corrosion initiation at the six cities

Climate change raises the probability of corrosion initiation at every city, under both baselines and for every concrete class. For specified concrete with blended cement cast in 2000, mean carbonation depth in 2100 is 12–18% greater under SSP2-4.5 and 23–37% greater under SSP5-8.5 than with no climate change. In Kampala the probability of initiation by 2100 rises from 37% to 56% (SSP2-4.5) and 69% (SSP5-8.5) on the ERA5-adjusted baseline (Figure 3, Table 4).

&#91;image: Figure 3. Corrosion-initiation probability at six cities\]

*Figure 3. Probability of corrosion initiation for specified concrete with blended cement cast in 2000, sheltered outdoor exposure, ERA5-adjusted baseline.*

The effect builds slowly. By 2050 the scenarios differ by at most 9 percentage points (Arua, 44% to 53%) and by 3 points in Kampala. Warming and CO₂ growth accelerate after mid-century, while carbonation depth grows with the square root of accumulated exposure.

| City | No change | SSP2-4.5 | SSP5-8.5 | No change (raw) | SSP2-4.5 (raw) | SSP5-8.5 (raw) |
| --- | --- | --- | --- | --- | --- | --- |
| Kampala | 37% | 56% | 69% | 44% | 63% | 75% |
| Mbale | 46% | 61% | 70% | 70% | 82% | 88% |
| Gulu | 79% | 89% | 94% | 63% | 77% | 84% |
| Arua | 83% | 92% | 97% | 44% | 63% | 74% |
| Mbarara | 67% | 83% | 92% | 15% | 31% | 46% |
| Kasese | 70% | 86% | 93% | 7% | 20% | 37% |

*Table 4. Probability of corrosion initiation by 2100; specified concrete with blended cement, cast in 2000. The first three columns use the ERA5-adjusted baseline.*

The ranking of cities depends on the humidity baseline. On the ERA5-adjusted baseline, the drier northern and western cities (Arua, Gulu, Kasese, Mbarara) carry the highest risk. On the raw baseline their much higher humidity suppresses carbonation, and Mbarara and Kasese become the lowest-risk cities. The increase due to climate change has the same direction and a similar size under both baselines: 14–32 percentage points by 2100 under SSP5-8.5.

### 5.3 Construction quality versus climate

Construction quality dominates (Figure 4). For concrete as typically built (w/c 0.55–0.70, 1–3 days of curing, mean cover 22 mm, blended cement), 91–99% of members cast in 2000 have initiated corrosion by 2050 at every city, with or without climate change. By then the gap between as-built and specified concrete is 46–83 percentage points, while climate change adds at most 9. Cement type is the second-largest factor. For specified concrete with CEM I, initiation by 2100 is 1–17% without climate change and 8–51% under SSP5-8.5, against 37–83% and 69–97% with blended cement.

&#91;image: Figure 4. Construction quality versus climate\]

*Figure 4. Probability of corrosion initiation by 2100 for members cast in 2000, by concrete class and scenario (ERA5-adjusted baseline).*

### 5.4 Building-stock exposure

The national run covers 2.42 million buildings of two or more storeys, with 463 million m² of floor area, in 346 grid cells. If they were built as specified with blended cement, 50% would pass corrosion initiation by 2100 without climate change, 66% under SSP2-4.5 and 76% under SSP5-8.5 (Figure 5). Climate change therefore adds about 373,000 buildings (72 million m²) under SSP2-4.5 and 614,000 buildings (118 million m²) under SSP5-8.5. The increase is small before mid-century: in 2050 the shares are 20%, 23% and 24%. Run separately, the eight climate models give 44–55% without climate change, 60–71% under SSP2-4.5 and 67–83% under SSP5-8.5 by 2100, so the climate increase exceeds the spread between models.

&#91;image: Figure 5. National building-stock trajectories\]

*Figure 5. Share of Uganda's RC buildings (two or more storeys, built before 2020) past corrosion initiation, by concrete class and scenario. Raw downscaled climate. Shading in the middle panel spans the eight climate models run separately.*

The concrete class matters more than the scenario. With CEM I the share past initiation by 2100 is 4% without climate change and 9–15% with it. If the stock was built as concrete typically is on site, 86% of buildings have already passed initiation by 2030, and 99% by 2100 under every scenario.

The climate increment varies from 10 to 38 percentage points between grid cells (median 25; Figure 6). It is largest in the Kampala–Lake Victoria belt and the south-west, and smallest in the east and north-east. The Kampala metropolitan area (nine grid cells) holds 62% of the RC stock and 66% of the extra buildings past initiation under SSP5-8.5.

&#91;image: Figure 6. Map of stock exposure\]

*Figure 6. (a) Share of RC buildings past corrosion initiation by 2100 under SSP5-8.5, and (b) increase over no climate change, for specified concrete with blended cement. Cells with fewer than 20 RC buildings are blank.*

### 5.5 Adaptation

Modest extra cover offsets the climate effect for new construction (Figure 7, Table 5). For specified blended concrete cast in 2025, 3.2–5.1 mm (SSP2-4.5) and 4.9–7.9 mm (SSP5-8.5) of extra cover restores the no-climate-change probability over a 50-year design life. To 2100 the figures rise to 4.4–6.9 mm and 8.6–13.8 mm. Kasese, Mbarara and Arua need the most; Mbale and Kampala the least.

&#91;image: Figure 7. Extra cover to offset climate change\]

*Figure 7. Extra cover that restores the no-climate-change probability of initiation, for specified concrete with blended cement cast in 2025 (ERA5-adjusted baseline).*

Meeting a target probability of 0.10 over 50 years needs a mean cover of 29–41 mm without climate change and 35–51 mm under SSP5-8.5, against the 30 mm assumed in design (Table 5). With CEM I, 21–30 mm meets the target even under SSP5-8.5. For concrete as typically built, the cover needed is 60–108 mm, which shows that cover alone cannot make up for poor concrete quality.

| City | Δc, SSP2-4.5 (mm) | Δc, SSP5-8.5 (mm) | Δc to 2100, SSP5-8.5 (mm) | Cover for P ≤ 0.10, no change (mm) | Cover for P ≤ 0.10, SSP5-8.5 (mm) |
| --- | --- | --- | --- | --- | --- |
| Kampala | 4.0 | 5.8 | 10.8 | 29 | 35 |
| Mbale | 3.2 | 4.9 | 8.6 | 31 | 36 |
| Gulu | 4.2 | 6.4 | 11.1 | 40 | 48 |
| Arua | 4.8 | 7.3 | 12.8 | 41 | 51 |
| Mbarara | 4.8 | 7.4 | 13.1 | 36 | 45 |
| Kasese | 5.1 | 7.9 | 13.8 | 37 | 46 |

*Table 5. Adaptation for specified concrete with blended cement cast in 2025, over a 50-year design life (2025–2075) unless stated; ERA5-adjusted baseline.*

### 5.6 Sensitivity

Construction-related inputs move the result as much as the emission scenario, or more (Figure 8). At Kampala, where the central probability of initiation by 2100 is 55%, curing for 3 rather than 14 days spans 31–81%, and ±5 mm of cover spans 35–75%. The emission scenario spans 36–69%, and the blended-cement factor 39–71%. The choice of climate model matters less (47–59%), as do the urban CO₂ factor (49–61%) and the activation energy (52–58%). Ignoring the elevation correction would raise the result to 64%.

At Arua, the humidity baseline dominates: the raw downscaled climate, 14 points more humid than ERA5, lowers the probability from 92% to 63%. The other inputs act within a narrower band because the probability is already near its upper limit.

&#91;image: Figure 8. Sensitivity of corrosion initiation\]

*Figure 8. Range of the probability of corrosion initiation by 2100 when each input is set to the ends of its range, others unchanged. Central case: specified concrete with blended cement cast in 2000, SSP2-4.5, ERA5-adjusted baseline (vertical line).*

### 5.7 Further results

Five further analyses are reported in the Supplementary Material. Their main findings are:

- **Rain exposure (S3).** Members exposed to rain carbonate far more slowly, so sheltered members govern; specified concrete on rain-exposed faces reaches at most 7% initiation by 2100.
- **Cover cracking (S4).** Cracking follows initiation by a median of 11–16 years, and climate change raises the probability of cracking by 2100 about as much as that of initiation.
- **New construction (S5).** Of about 1.3 million RC buildings expected by 2050 at recent construction rates, 60% pass initiation by 2100 under SSP5-8.5 if built as specified, and 32% with 8 mm of extra cover.
- **Cost-effectiveness (S6).** Extra cover pays for itself unless repairing 1 m² of cracked concrete costs less than 7–15% of the price of 1 m³ of in-place concrete.
- **Check against measured carbonation (S7).** Measured natural carbonation of Portland cement concrete is a median 1.6 times faster than the fib model predicts, so the probabilities here are likely conservative, and the blended-cement factor implied by fly-ash data brackets the 2.6–4.4 used here.

## 6. Discussion

### 6.1 Climate versus construction quality

In Uganda, construction quality decides whether reinforcement corrodes within a building's life, and climate change decides how much of the well-built stock follows. If the existing stock was built as concrete typically is on site, 86% of it has already passed corrosion initiation by 2030, whatever the climate. For this stock, carbonation-induced corrosion is a present problem, and climate change adds little because initiation is close to certain. For concrete built as specified, climate change matters: it raises the probability of initiation by 2100 by 14–32 percentage points at the six cities, and adds 15 (SSP2-4.5) to 25 (SSP5-8.5) percentage points to the share of the national stock past initiation. Even for specified concrete, the sensitivity analysis shows that curing and ±5 mm of cover move the result as much as the choice between no climate change and SSP5-8.5 (Figure 8). Site practice and climate change are therefore of similar weight for well-designed buildings, and site practice dominates for the rest.

The humid equatorial highland setting moderates the climate effect without removing it. Relative humidity of 75–88% lowers the carbonation rate, and the 13% lower CO₂ mass concentration at 1,000–1,500 m lowers it further. Neither changes much with time, however, because projected humidity changes are within ±3 points. The change comes from CO₂ and temperature. Between 2014 and 2100, CO₂ rises by a factor of 1.5 under SSP2-4.5 and 2.9 under SSP5-8.5, while 2.5–4.6 °C of warming raises the rate by roughly 15–30% through the Arrhenius term. CO₂ is therefore the main driver in both scenarios.

### 6.2 Regional differences

The ranking of cities depends more on the humidity baseline than on the emission scenario. On the ERA5-adjusted baseline, the drier northern and western cities (Arua, Gulu, Kasese, Mbarara) carry the highest risk. On the raw downscaled baseline, which is 12–14 points more humid at three of these cities, Mbarara and Kasese become the lowest-risk cities. The climate increment is similar under both baselines, so the conclusion that climate change raises risk everywhere is robust; the ranking of cities is not. Station humidity records, which could not be obtained for this study, would resolve it.

Exposure is concentrated where the stock is. The Kampala metropolitan area holds 62% of Uganda's RC buildings of two or more storeys and accounts for 66% of the extra buildings past initiation under SSP5-8.5. It is also where growth is fastest \[Vermeiren et al., 2012; Muchelo et al., 2024\], so the city's building control and design practice will largely determine national outcomes.

### 6.3 Implications for design and regulation

Three implications follow for design and regulation.

1. **Cover should depend on cement type.** Even without climate change, a 30 mm cover with blended cement does not meet a target probability of 0.10 over 50 years at five of the six cities; 31–41 mm is needed there. With CEM I, 30 mm suffices everywhere. Since most Ugandan cement is CEM II/B-P or CEM IV, durability provisions written for Portland cement understate the cover required.
2. **A climate allowance of 5–8 mm is justified for structures designed now.** This is the extra cover that offsets SSP5-8.5 over a 50-year life at every city studied, and it is close to the 5–10 mm found cost-effective in Australia \[Stewart et al., 2012\]. It is also cost-effective here unless repairing 1 m² of cracked concrete costs less than 7–15% of the price of 1 m³ of in-place concrete under SSP5-8.5 (Supplementary S6). The allowance applies to faces sheltered from rain, such as soffits and columns under eaves, which govern (Supplementary S3). For longer-lived structures, or design to 2100, the allowance rises to 9–14 mm.
3. **Enforcement matters more than either.** The as-built case needs 60–108 mm of cover, which is impractical; the remedy is achieving the specified w/c, curing and cover. The Ministry of Works specification already requires at least 7 days of moist curing and cover within ±3 mm of the drawings \[MoWT, 2013\]. Cover-meter checks and curing records at inspection, under the Building Control Act 2013, would address the largest single risk factor.

The rules adopted now matter most for the buildings still to be built. At recent rates, about 1.3 million RC buildings will be added by 2050, more than half the present stock; built as specified with 8 mm of extra cover, 32% of them pass initiation by 2100 under SSP5-8.5, against 60% without the extra cover and 95–99% if built as concrete typically is today. For existing buildings, inspection should start with buildings constructed before 2000 in the Kampala metropolitan area and the drier north and west, where the model gives the highest probabilities of initiation.

### 6.4 Comparison with other studies

The climate effect found here is at the lower end of published estimates, as expected for a humid climate.

| Study | Setting | Climate effect on carbonation |
| --- | --- | --- |
| This study | Six Ugandan cities, CMIP6, to 2100 | Depth +12–18% (SSP2-4.5), +23–37% (SSP5-8.5) |
| Dimova et al. \[2025\] | 27 EU capitals, 60 years to 2085 | Depth +25–45% (intermediate), +58–89% (high) |
| Ekolu \[2020b\] | Johannesburg and Durban, to 2100 | Depth up to +31% from rising CO₂ |
| Talukdar et al. \[2012\] | Canadian cities, A1FI, to 2100 | Depth up to +45% |
| Pinheiro Teodoro et al. \[2026\] | Brazil, 0.2° grid, SSP5-8.5 | Mean depth 42 mm by 2100 in the aggressive class; largest where humidity falls |
| Zulu and Miyazato \[2024\] | Lusaka, 100 years | Initiation time 50–52% shorter |

The main reason for the smaller increase is humidity. In Europe and much of Brazil, humidity falls as the climate warms, which speeds carbonation; in Uganda it hardly changes and stays high. The reference case also differs: the no-change case here holds CO₂ at its 2014 level, whereas several studies compare with 2000.

The adaptation results agree more closely with earlier work. The 4–14 mm of extra cover needed to 2100 brackets the 5–10 mm reported for Australia \[Stewart et al., 2012\]. The covers that meet a 0.10 target with blended cement (35–51 mm under SSP5-8.5) are similar to the 35–60 mm Val et al. \[2025\] found for fly-ash concrete in sheltered exposure in Dublin, Seoul and Dubai, although their design life was 100 years rather than 50.

### 6.5 Limitations

- **No Ugandan field data.** No published measurements of cover or carbonation depth in Ugandan buildings exist, so the as-built distributions come from regional literature. A phenolphthalein and cover-meter survey of buildings of known age would test them directly.
- **Blended-cement factor.** The calibrated range (2.6–4.4) rests on mortar strength tests at 20% replacement \[Buregyeya et al., 2018\] and a model calibrated on South African data \[Ekolu and Solomon, 2022\]. Natural carbonation data for Ugandan cements would narrow it.
- **Propagation.** Propagation to cover cracking uses indicative corrosion rates and a cracking criterion from the literature \[DuraCrete, 2000; Alonso et al., 1998; Stewart et al., 2011\], not calibrated for Uganda. Spalling and loss of structural capacity are not modelled.
- **Building-stock data.** GHS-OBAT heights and epochs are neighbourhood (100 m) values, not building values. Counting buildings of at least 4.5 m therefore overstates the multi-storey stock, by about four-fold according to a companion study, so building counts here are upper bounds while shares are robust. Buildings completed after 2020 are excluded. New construction to 2049 assumes each cell's 2000–2010 construction rate continues; the shares are insensitive to this, but the building counts are not.
- **Climate data.** The stock run uses the raw downscaled climate, which is more humid than ERA5 at several sites, so it may understate risk in the drier north and west. ERA5 was the only independent check, as station records were not available.
- **Exposure.** Only sheltered outdoor members are modelled. Indoor members carbonate faster at lower humidity, while members exposed to rain carbonate more slowly.

## 7. Conclusions

This study coupled eight downscaled CMIP6 models with a probabilistic carbonation model and footprint-level building-age data to assess carbonation-induced corrosion of Uganda's reinforced concrete building stock to 2100. The main findings are:

1. Climate change raises the probability of corrosion initiation at all six cities studied. For specified concrete with blended cement cast in 2000, the probability by 2100 rises from 37–83% without climate change to 56–92% under SSP2-4.5 and 69–97% under SSP5-8.5. Carbonation depth increases by 12–18% and 23–37% respectively. The effect is small before 2050.
2. Construction quality dominates. If the stock was built as concrete typically is on site, 86% of Uganda's RC buildings have passed corrosion initiation by 2030, whatever the climate.
3. If the stock was built as specified, the share past initiation by 2100 rises from 50% to 66% (SSP2-4.5) and 76% (SSP5-8.5): an extra 373,000–614,000 buildings with 72–118 million m² of floor area. These counts rest on neighbourhood-height data and are upper bounds; the shares are robust. Two-thirds of the increase falls in the Kampala metropolitan area.
4. Uganda's pozzolanic cements carbonate 1.6–2.1 times deeper than CEM I at equal w/c. With them, a 30 mm cover does not meet a 0.10 target probability over 50 years at five of the six cities, even without climate change.
5. For new construction, 5–8 mm of extra cover offsets the SSP5-8.5 climate effect over a 50-year design life, and 9–14 mm to 2100.

6) Members sheltered from rain govern: on rain-exposed faces the probability of initiation is at most 7% for specified concrete. Cover cracking follows initiation by a median of 11–16 years, and climate change raises the probability of cracking by 2100 as much as that of initiation.
7) For the 1.3 million RC buildings expected by 2050, 8 mm of extra cover reduces the share past initiation by 2100 under SSP5-8.5 from 60% to 32%. Extra cover is cost-effective unless repairing 1 m² of cracked concrete costs less than 7–15% of the price of 1 m³ of in-place concrete.
8) Curing and cover affect the result as much as the emission scenario, and the climate increase is larger than the spread between climate models.

9. Measured natural carbonation of Portland cement concrete is on average 1.6 times faster than the fib model predicts, so the probabilities reported here are likely conservative.

For design practice, cover requirements in Uganda should depend on cement type and include a climate allowance of about 5–8 mm, and building control should verify cover and curing on site, since these govern the outcome more than climate does. For research, the priorities are field measurements of cover and carbonation depth in Ugandan buildings of known age, natural carbonation data for Ugandan cements, and extension to the corrosion propagation stage, together with the structural health monitoring companion study.

## Data availability

All input data are open: NEX-GDDP-CMIP6, the CMIP6 greenhouse-gas concentrations, GHS-OBAT and Google Open Buildings. Analysis code, processed data and the systematic review records are in the GitHub repository github.com/gavacharles/uganda-concrete-climate (to be made public and archived on Zenodo on submission). Scopus records cannot be redistributed; the search strings are given in Supplementary S1.

## References

*Author-year list; convert to the target journal's style on submission. Entries marked † still need the full text checked.*

- *† Alexander, M.G. (2018). Service life design and modelling of concrete structures – background, developments, and implementation. (Venue to confirm from included\_final.csv.)*
- Alexander, M.G., Beushausen, H., Nganga, G. (2012). Control of concrete cover depth of reinforced concrete structures for durability. In *Concrete Repair, Rehabilitation and Retrofitting III*. https://doi.org/10.1201/b12750-70
- Alinaitwe, H.M. (2023). Factors that led to an increase of building collapses during the COVID-19 lockdown period in the Greater Kampala metropolitan area, Uganda. https://doi.org/10.1201/9781003278368-26
- Alinaitwe, H.M., Ekolu, S. (2014). Failure of structures in East Africa with focus on the causes of failures in the construction phase. In *Construction Materials and Structures*, IOS Press. https://doi.org/10.3233/978-1-61499-466-4-76
- Almazroui, M., et al. (2020). Projected change in temperature and precipitation over Africa from CMIP6. *Earth Systems and Environment* 4, 455–475. https://doi.org/10.1007/s41748-020-00161-x
- Bastidas-Arteaga, E., et al. (2022). Multi-region lifetime assessment of reinforced concrete structures subjected to carbonation and climate change. *Structures*. https://doi.org/10.1016/j.istruc.2022.09.061
- Buregyeya, A., et al. (2018). Pozzolanic and hydration properties of kamafugites and carbonatitic lavas as supplementary cementitious materials in Portland cement. *African Journal of Science, Technology, Innovation and Development*. https://doi.org/10.1080/20421338.2018.1527539
- Caleb, M., Olonade, K.A., Lawan, M.M. (2023). Evaluating the causes of building collapse in Kampala District, Uganda. *KIU Journal of Science, Engineering and Technology* 2(2), 1–20. https://doi.org/10.59568/KJSET-2023-2-2-01
- Cervantes, E., et al. (2026). Climate change impacts on reinforced concrete structures: a bibliometric analysis. *Structural Engineering International*. https://doi.org/10.1080/10168664.2026.2649216
- Dimova, S., et al. (2025). Lifetime assessment of European reinforced concrete structures subjected to climate change-induced carbonation. *ce/papers*. https://doi.org/10.1002/cepa.3341
- † Ekolu, S.O. (2020a). Service life design for inland concrete structures in Africa: Kampala case study. RILEM Bookseries 26, 132–136. https://doi.org/10.1007/978-3-030-43332-1\_26
- Ekolu, S.O. (2020b). Implications of global CO₂ emissions on natural carbonation and service lifespan of concrete infrastructures – reliability analysis. *Cement and Concrete Composites* 114, 103744. https://doi.org/10.1016/j.cemconcomp.2020.103744
- Ekolu, S., Solomon, F. (2022). A case study on practical prediction of natural carbonation for concretes containing supplementary cementitious materials. *KSCE Journal of Civil Engineering* 26(3), 1163–1176. https://doi.org/10.1007/s12205-021-1770-6
- Companion study (in preparation). Exposure of Uganda's building stock to climate-driven concrete deterioration: neighbourhood data, urban heat and rainfall extremes. (Paper B; replace with the full reference once submitted.)
- Mendeley Data (2022). Database for accelerated and natural carbonation in fly ash concrete. doi:10.17632/rchp48n97y.2 (CC BY 4.0).
- Alonso, C., Andrade, C., Rodriguez, J., Diez, J.M. (1998). Factors controlling cracking of concrete affected by reinforcement corrosion. *Materials and Structures* 31, 435–441. (Check details against the full text.)
- DuraCrete (2000). *Statistical quantification of the variables in the limit state functions*. Report BE95-1347/R9, The European Union – Brite EuRam III. (Check corrosion-rate values against the full text.)
- Hersbach, H., et al. (2020). The ERA5 global reanalysis. *Quarterly Journal of the Royal Meteorological Society* 146, 1999–2049. https://doi.org/10.1002/qj.3803
- Ministry of Works and Transport (MoWT) (2013). *Standard Specifications for Building Works*. Government of Uganda, Kampala.
- Republic of Uganda (2013). *Building Control Act, 2013*. Uganda Printing and Publishing Corporation, Entebbe.
- fib (2006). *Model Code for Service Life Design*. fib Bulletin 34. Fédération internationale du béton.
- Florio, P., et al. (2025). GHS-OBAT: global, open building attribute data reporting age, function, height and compactness at footprint level. *Data in Brief* 61, 111751. https://doi.org/10.1016/j.dib.2025.111751
- Kakitahi, J., Alinaitwe, H., Landin, A., Mudaaki, S. (2015). A study of non-compliance with quality requirements in Uganda. *Proc. ICE – Management, Procurement and Law* 168, 22–42. https://doi.org/10.1680/mpal.13.00042
- Meinshausen, M., et al. (2020). The shared socio-economic pathway (SSP) greenhouse gas concentrations and their extensions to 2500. *Geoscientific Model Development* 13, 3571–3605. https://doi.org/10.5194/gmd-13-3571-2020
- Muchelo, R., et al. (2024). Patterns of urban sprawl and agricultural land loss in sub-Saharan Africa: the cases of the Ugandan cities of Kampala and Mbarara. *Land* 13, 1056. https://doi.org/10.3390/land13071056
- Paul, N., Silva, V., Amo-Oduro, D. (2022). Development of a uniform exposure model for the African continent for use in disaster risk assessment. *International Journal of Disaster Risk Reduction* 71, 102823. https://doi.org/10.1016/j.ijdrr.2022.102823
- Peng, L., Stewart, M.G. (2014). Climate change and corrosion damage risks for reinforced concrete infrastructure in China. *Structure and Infrastructure Engineering* 12, 499–516. https://doi.org/10.1080/15732479.2013.858270
- Pinheiro Teodoro, C., et al. (2026). Future climate scenarios and their impact on carbonation of reinforced concrete structures in Brazil. *Case Studies in Construction Materials*. https://doi.org/10.1016/j.cscm.2026.e06125
- Stewart, M.G., Wang, X., Nguyen, M.N. (2011). Climate change impact and risks of concrete infrastructure deterioration. *Engineering Structures* 33, 1326–1337. https://doi.org/10.1016/j.engstruct.2011.01.010
- Stewart, M.G., Wang, X., Nguyen, M.N. (2012). Climate change adaptation for corrosion control of concrete infrastructure. *Structural Safety* 35, 29–39. https://doi.org/10.1016/j.strusafe.2011.10.002
- Talukdar, S., Banthia, N., Grace, J.R. (2012). Carbonation in concrete infrastructure in the context of global climate change – Part 1. *Cement and Concrete Composites* 34, 924–930. https://doi.org/10.1016/j.cemconcomp.2012.04.011
- Thrasher, B., et al. (2022). NASA Global Daily Downscaled Projections, CMIP6. *Scientific Data* 9, 262.
- Tutu, K.A., et al. (2022). Concrete quality issues in multistory building construction in Ghana: cases from Kumasi metropolis. *Case Studies in Construction Materials*. https://doi.org/10.1016/j.cscm.2022.e01425
- Val, D.V., et al. (2025). Reliability-based durability requirements for RC structures made of low-carbon concretes in climate change conditions. *Civil Engineering and Environmental Systems*. https://doi.org/10.1080/10286608.2025.2478008
- Vermeiren, K., et al. (2012). Urban growth of Kampala, Uganda: pattern analysis and scenario development. *Landscape and Urban Planning* 106, 199–206. https://doi.org/10.1016/j.landurbplan.2012.03.006
- Zulu, W.A., Miyazato, S. (2024). Predicting the impact of global warming on carbonation of reinforced concrete structures in Zambia and Japan. *Advances in Concrete Construction* 17(5), 245–255. https://doi.org/10.12989/acc.2024.17.5.245

*Remaining in-text citations (Wang et al. 2011; Bastidas-Arteaga et al. 2013, 2015; Peng and Stewart 2014b; Papadakis et al. 1991; Troconis de Rincon et al. 2014; Antoni et al. 2024; Cascudo et al. 2025; Tam et al. 2008; Alexander et al. 2007; Fotso Lele 2023; Ekolu 2025; Balu-Tabaaro 2014; Kwikiriza 2018; Senfuka et al. 2013; Li et al. 2021; Tran 2021; Meinshausen et al. 2017; fib 2013) are listed with DOIs in* `review/results/included_final.csv` *and will be added in full when the citation style is fixed.*

## Supplementary Material

The sections below support Sections 2 and 5.7 of the main text.

### S1 Systematic review

Four search strings were run in Scopus (TITLE-ABS-KEY, Advanced document search) on 1 October 2026. Records outside the limits written into the strings (before 1990, not English, or not an article, review, conference paper or book chapter) were removed after export, and records retrieved by more than one string were de-duplicated on title. Screening ran in two stages: search-specific topic rules on title and abstract, then manual title and abstract review against four themes. Included studies are: (T1) studies that model the effect of climate change on carbonation or corrosion of reinforced concrete; (T2) field or modelling evidence on carbonation and durability in tropical or African settings; (T3) Ugandan concrete, cement, steel and construction-quality studies; (T4) growth, exposure or urban climate of Uganda's built environment. Excluded: chloride-only marine studies, mix-design studies without climate or field context, freeze–thaw, seismic and pavement studies, and non-built-environment land-use studies. The search identified 2,891 records, of which 2,745 were screened and 137 included (Figure S1). Other sources cited in the main text, such as datasets, standards and studies outside the search results, are referenced individually and are not part of these counts.

| String | Concept blocks joined by AND | Scopus hits |
| --- | --- | --- |
| S1 Climate change × concrete deterioration | concrete AND deterioration mechanism AND climate change or CO₂ | 2,411 |
| S2 African and tropical concrete durability | concrete AND deterioration mechanism AND African country or tropics | 376 |
| S3 Ugandan construction materials and quality | Uganda AND material or construction quality | 18 |
| S4 Uganda building growth, exposure and urban climate | Uganda or East Africa AND urban growth, building stock or heat island | 86 |

```text
S1  TITLE-ABS-KEY ( concrete
      AND ( carbonation OR "reinforcement corrosion" OR "steel corrosion" OR "rebar corrosion"
            OR "corrosion initiation" OR "concrete durability" OR "service life" )
      AND ( "climate change" OR "global warming" OR "changing climate" OR "future climate"
            OR "climate projection*" OR "CO2 concentration*" OR "carbon dioxide concentration*"
            OR "representative concentration pathway*" OR "shared socioeconomic pathway*" OR CMIP* ) )
    AND PUBYEAR > 1989
    AND ( LIMIT-TO ( DOCTYPE , "ar" ) OR LIMIT-TO ( DOCTYPE , "re" ) OR LIMIT-TO ( DOCTYPE , "cp" )
          OR LIMIT-TO ( DOCTYPE , "ch" ) )
    AND ( LIMIT-TO ( LANGUAGE , "English" ) )

S2  TITLE-ABS-KEY ( concrete
      AND ( carbonation OR "reinforcement corrosion" OR "steel corrosion" OR "corrosion initiation"
            OR "concrete durability" OR "service life" OR "cover depth" )
      AND ( africa* OR "sub-saharan" OR uganda OR kenya OR tanzania OR rwanda OR ethiopia OR zambia
            OR malawi OR nigeria OR ghana OR "south africa" OR "south sudan" OR kampala OR nairobi OR tropic* ) )
    AND PUBYEAR > 1989 AND ( LIMIT-TO ( LANGUAGE , "English" ) )

S3  TITLE-ABS-KEY ( ( uganda* OR kampala )
      AND ( concrete OR cement* OR pozzolan* OR "building collapse*" OR "structural failure*"
            OR "construction quality" OR "building material*" OR masonry OR "reinforcing steel" OR rebar ) )
    AND PUBYEAR > 1989

S4  TITLE-ABS-KEY ( ( uganda* OR kampala OR "east africa*" )
      AND ( "urban expansion" OR "urban growth" OR "urban sprawl" OR "built-up" OR "building stock"
            OR "exposure model*" OR "building footprint*" OR "urban heat island*" OR "settlement growth" ) )
    AND PUBYEAR > 1989
```

&#91;image: Figure S0. PRISMA flow\]

*Figure S1. PRISMA 2020 flow of the Scopus search (searched 1 October 2026).*

### S2 Methods for the further analyses

**Exposure to rain.** Members exposed to rain were modelled with the fib weather function W = (t₀/t)^w, with w = (p\_SR · ToW)^b\_w / 2 \[fib, 2006\]. Time of wetness ToW is the fraction of days with at least 2.5 mm of rain in each model and scenario. Vertical faces use p\_SR = 0.25 \[after Val et al., 2025\] and horizontal surfaces p\_SR = 1.

**Propagation to cover cracking.** After initiation, corrosion penetration accumulates at a rate V = V₂₀\[1 + K(T − 20)\], with K = 0.025 below 20 °C and 0.073 above \[Stewart et al., 2011\]. V₂₀ is lognormal with mean 2.0 µm/yr and coefficient of variation 0.5, a value typical of sheltered carbonated concrete \[DuraCrete, 2000\]. The cover cracks when penetration reaches x₀ = 7.53 + 9.32 c/φ µm \[Alonso et al., 1998\], with bar diameter φ = 12 mm. These propagation parameters are indicative and were not calibrated for Uganda.

**New construction.** RC buildings completed from 2020 to 2049 were added at each grid cell's 2000–2010 construction rate (about 44,000 buildings a year nationally), with uniform casting years. The 2010–2020 epoch was not used because its share of tall buildings (1%) is implausibly low. Three variants were run: as built, as specified, and as specified with 8 mm of extra cover.

**Cost-effectiveness of extra cover.** For specified blended concrete cast in 2025, the expected discounted probability of cover cracking per m² of surface was computed for 0–20 mm of extra cover, with discount rates of 1%, 3% and 5%. Extra cover of Δc costs Δc × 1 m² of concrete. It pays for itself when the cost of repairing 1 m² of cracked surface, divided by the in-place cost of 1 m³ of concrete, exceeds a break-even ratio R\* = Δc / (reduction in discounted cracking probability). Expressing the result as a ratio avoids the need for Ugandan unit costs, which were not available.

**Check against measured carbonation.** An open database of 831 carbonation tests on Portland and fly-ash concretes from 18 published sources \[Mendeley Data, doi:10.17632/rchp48n97y.2\] was used. Its 454 natural-exposure tests (CO₂ ≤ 0.1%, four sources) were compared with the fib model through the carbonation coefficient k = depth/√t, and the multiplier on R⁻¹ that reproduces the measured k was back-calculated for the fly-ash mixes. A gradient-boosting model of k, validated by leaving out whole sources, was also fitted as a data-driven comparison.

### S3 Members exposed to rain

Members exposed to rain carbonate far more slowly than sheltered ones, so sheltered members govern (Table S1). For specified blended concrete under SSP5-8.5, the probability of initiation by 2100 falls from 69–96% when sheltered to 1–7% on vertical faces exposed to rain, and to zero on horizontal surfaces. As-built concrete on rain-exposed vertical faces still reaches 38–66%.

Climate change raises risk for rain-exposed members too. For as-built concrete on vertical faces, it adds 9–17 percentage points by 2100 under SSP5-8.5. The number of rain days changes little, by 0–11%, so wetter conditions do not offset the faster carbonation.

| City | Specified, sheltered | Specified, vertical, rain-exposed | As built, sheltered | As built, vertical, rain-exposed | As built, horizontal, rain-exposed |
| --- | --- | --- | --- | --- | --- |
| Kampala | 69% | 1% | 100% | 38% | 2% |
| Mbale | 70% | 1% | 100% | 39% | 3% |
| Gulu | 94% | 5% | 100% | 61% | 8% |
| Arua | 96% | 7% | 100% | 66% | 11% |
| Mbarara | 92% | 3% | 100% | 55% | 5% |
| Kasese | 93% | 3% | 100% | 56% | 5% |

*Table S1. Probability of corrosion initiation by 2100 under SSP5-8.5 by exposure, blended cement, cast in 2000, ERA5-adjusted baseline.*

### S4 Propagation to cover cracking

Cover cracking follows initiation by a median of 11–16 years at the cities' present and projected temperatures, with a 10–90% range of about 6–30 years. For specified blended concrete cast in 2000, the probability of cover cracking by 2100 rises from 27–74% without climate change to 43–86% under SSP2-4.5 and 52–91% under SSP5-8.5 (Figure S2). For members cast in 2025, the probability of cracking by 2075 roughly doubles or more under SSP5-8.5 at every city, from 3–25% to 9–46%. Because the corrosion rate also rises with temperature, warming acts on both stages.

&#91;image: Figure 9. Probability of cover cracking\]

*Figure S2. Probability of corrosion-induced cover cracking for specified concrete with blended cement cast in 2000 (ERA5-adjusted baseline). Propagation parameters are indicative (Section S2).*

### S5 New construction, 2020–2049

At the 2000–2010 construction rate, about 1.32 million RC buildings are added between 2020 and 2049. If they are built as concrete typically is on site, 52–61% of them pass initiation by 2050 and 95–99% by 2100 (Figure S3). Built as specified with blended cement, 23% pass initiation by 2100 without climate change, 43% under SSP2-4.5 and 60% under SSP5-8.5.

Eight millimetres of extra cover lowers these shares to 6%, 18% and 32%. Under SSP2-4.5 that is better than specified concrete without climate change (23%). Under SSP5-8.5 it is not, because 8 mm offsets the climate effect over 50 years but not to 2100 (Table 5).

&#91;image: Figure 10. New construction 2020–2049\]

*Figure S3. Share of RC buildings completed in 2020–2049 that are past corrosion initiation, for concrete as built, as specified, and as specified with 8 mm of extra cover (blended cement, raw downscaled climate).*

### S6 Cost-effectiveness of extra cover

Extra cover pays for itself at low repair costs (Table S2). With a 3% discount rate, 10 mm of extra cover is worth providing if repairing 1 m² of cracked surface costs more than 8–17% of the price of 1 m³ of in-place concrete under SSP5-8.5. Without climate change the threshold is higher, at 10–44%, so climate change roughly halves the repair cost needed to justify adaptation in Kampala and Mbale. At a 5% discount rate the thresholds rise to 15–44% under SSP5-8.5. A patch repair involves breaking out, cleaning the steel, reinstating concrete and providing access, so it is likely to cost more than these thresholds; Ugandan unit rates are needed to confirm this.

| City | R\*, 5 mm, no change | R\*, 5 mm, SSP5-8.5 | R\*, 10 mm, no change | R\*, 10 mm, SSP5-8.5 |
| --- | --- | --- | --- | --- |
| Kampala | 0.29 | 0.13 | 0.44 | 0.17 |
| Mbale | 0.21 | 0.12 | 0.30 | 0.15 |
| Gulu | 0.09 | 0.07 | 0.11 | 0.08 |
| Arua | 0.08 | 0.07 | 0.10 | 0.08 |
| Mbarara | 0.12 | 0.08 | 0.16 | 0.10 |
| Kasese | 0.10 | 0.08 | 0.14 | 0.09 |

*Table S2. Break-even ratio R\** (repair cost per m² ÷ in-place concrete cost per m³) above which extra cover is cost-effective; specified blended concrete cast in 2025, cracking to 2100, 3% discount rate.

### S7 Check against measured carbonation

**Measured natural carbonation is faster than the fib model predicts.** For 160 natural-exposure tests on Portland cement concrete, measured carbonation coefficients are a median 1.6 times the fib prediction (interquartile range 1.0–3.4; Figure S4). If this holds for Ugandan concrete, the probabilities in this paper are conservative. For fly-ash mixes, the multiplier on R⁻¹ that reproduces the measurements is 4.1 at 20–30% fly ash and 4.6 at 30–40% (2.3 and 3.8 after correcting each source by its own Portland mixes), which brackets the 2.6–4.4 used here. A purely data-driven model of the carbonation coefficient did not generalise to an unseen source (leave-source-out R² = −1.4), whereas the fib model with a fitted fly-ash factor had a mean absolute error of 2.1 mm/√yr. With only four independent sources of natural-exposure data, the physical model is the more reliable tool.

&#91;image: Figure S3. Measured versus fib carbonation\]

*Figure S4. Measured natural carbonation coefficients of Portland cement concrete (160 tests) against the fib model; dashed lines mark a factor of 2.*
