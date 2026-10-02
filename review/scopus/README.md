# Scopus searches

Paste each string into Scopus > Advanced document search, export all results as CSV
(tick Citation information + Abstract & keywords) and save here as `S1.csv` ... `S4.csv`.
Then run `review/import_scopus.py`, `review/screen.py`, `review/stage2_decisions.py`.

Record the search date and the hit count for each string (PRISMA requires both).

## S1 Climate change x concrete deterioration
```
TITLE-ABS-KEY ( concrete AND ( carbonation OR "reinforcement corrosion" OR "steel corrosion" OR "rebar corrosion" OR "corrosion initiation" OR "concrete durability" OR "service life" ) AND ( "climate change" OR "global warming" OR "changing climate" OR "future climate" OR "climate projection*" OR "CO2 concentration*" OR "carbon dioxide concentration*" OR "representative concentration pathway*" OR "shared socioeconomic pathway*" OR CMIP* ) ) AND PUBYEAR > 1989 AND ( LIMIT-TO ( DOCTYPE , "ar" ) OR LIMIT-TO ( DOCTYPE , "re" ) OR LIMIT-TO ( DOCTYPE , "cp" ) OR LIMIT-TO ( DOCTYPE , "ch" ) ) AND ( LIMIT-TO ( LANGUAGE , "English" ) )
```

## S2 African and tropical concrete durability
```
TITLE-ABS-KEY ( concrete AND ( carbonation OR "reinforcement corrosion" OR "steel corrosion" OR "corrosion initiation" OR "concrete durability" OR "service life" OR "cover depth" ) AND ( africa* OR "sub-saharan" OR uganda OR kenya OR tanzania OR rwanda OR ethiopia OR zambia OR malawi OR nigeria OR ghana OR "south africa" OR "south sudan" OR kampala OR nairobi OR tropic* ) ) AND PUBYEAR > 1989 AND ( LIMIT-TO ( LANGUAGE , "English" ) )
```

## S3 Ugandan construction materials and quality
```
TITLE-ABS-KEY ( ( uganda* OR kampala ) AND ( concrete OR cement* OR pozzolan* OR "building collapse*" OR "structural failure*" OR "construction quality" OR "building material*" OR masonry OR "reinforcing steel" OR rebar ) ) AND PUBYEAR > 1989
```

## S4 Uganda building growth, exposure and urban climate
```
TITLE-ABS-KEY ( ( uganda* OR kampala OR "east africa*" ) AND ( "urban expansion" OR "urban growth" OR "urban sprawl" OR "built-up" OR "building stock" OR "exposure model*" OR "building footprint*" OR "urban heat island*" OR "settlement growth" ) ) AND PUBYEAR > 1989
```
