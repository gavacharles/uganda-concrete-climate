"""Stage-2 (manual title/abstract) decisions and PRISMA counts.

INCLUDE maps a distinctive title fragment to the synthesis theme. Records that
passed stage 1 but are not listed here were excluded at stage 2 (off-topic:
mix-design/material studies without climate or field context, chloride-only
marine studies, non-built-environment land-use studies, etc.). FLAGGED records
are excluded for integrity reasons and reported separately.
"""
import json
from pathlib import Path

import pandas as pd

RES = Path(__file__).parent / "results"

# theme codes: T1 climate-carbonation modelling, T2 tropical/African durability evidence,
# T3 Ugandan materials & construction quality, T4 Uganda growth/exposure/urban climate
INCLUDE = {
    # T1 climate change x carbonation/corrosion modelling
    "Climate change impact and risks of concrete infrastructure deterioration": "T1",
    "Climate change adaptation for corrosion control of concrete infrastructure": "T1",
    "Influence of global warming on durability of corroding RC structures": "T1",
    "Impact of climate change on corrosion and damage to concrete infrastructure in Australia": "T1",
    "Climate change and corrosion damage risks for reinforced concrete infrastructure in China": "T1",
    "Durability demands related to carbonation induced corrosion for Finnish concrete buildings": "T1",
    "Economic assessment of climate adaptation strategies for existing reinforced concrete": "T1",
    "Development of a service lifespan model": "T1",
    "Carbonation depth predictions in concrete bridges under changing climate": "T1",
    "Spatial time-dependent reliability analysis of corrosion damage to RC structures with climate change": "T1",
    "Durability assessment of reinforced concrete structures considering global warming": "T1",
    "Multi-region lifetime assessment of reinforced concrete structures": "T1",
    "Effects of climate variations and global warming on the durability of RC structures subjected to carbonation": "T1",
    "Carbonation depth predictions in concrete structures under changing climate condition in China": "T1",
    "Model Refinement and Represent": "T1",
    "Impact of climate change on the service life of concrete structures": "T1",
    "Climate Change Impacts on the Risk Assessment of Concrete Civil Infrastructures": "T1",
    "Polynomial chaos expansion for lifetime assessment": "T1",
    "Durability of RC Structures against Carbonation-Induced Corrosion under the Impact of Climate Change": "T1",
    "Remaining Life of Ageing RC Infrastructure for Sustainable development": "T1",
    "Life-cycle cost assessment of climate change adaptation measures to minimise carbonation": "T1",
    "Corrosion of Concrete and Steel Structures in a Changing Climate": "T1",
    "Probabilistic approach to the sustainability assessment of reinforced concrete structures in conditions of cli": "T1",
    "Climate change-induced carbonation of concrete infrastructure": "T1",
    "Influence of Climate Change on Probability of Carbonation-Induced Corrosion Initiation": "T1",
    "Probabilistic cost-benefit analysis of climate change adaptation strategies for new RC": "T1",
    "Effect of Climate Change on Service Life of High Volume Fly Ash Concrete Subjected to Carbonation": "T1",
    "Time-Dependent Reliability-Based Service Life Assessment of RC Bridges Subjected to Carbonation": "T1",
    "Europe's reinforced concrete structures: Corrosion rates in a changing climate": "T1",
    "Effects of Crack and Climate Change on Service Life of Concrete Subjected to Carbonation": "T1",
    "INVESTIGATING THE CORROSION INITIATION PROCESS IN REINFORCED CONCRETE STRUCTURES UNDER THE IMPACT OF CLIMATE": "T1",
    "Climate Change Effects on Carbonation Process: A Scenario-Based Study": "T1",
    "Impact of carbonation on reinforced concrete structures, considering the increase of CO2": "T1",
    "Reliability-based durability requirements for RC structures made of low-carbon concretes": "T1",
    "Climate change effects on structural reliability in the Carpathian region": "T1",
    "Prediction of corrosion rates in view of climate change with rising temperatures": "T1",
    "Spatial Time Dependent Reliability Analysis of Carbonation with Climate Change": "T1",
    "Evaluation of carbonation service life of slag blended concrete considering climate changes": "T1",
    "Climate change effect on deterioration of concrete structures in Finland": "T1",
    "Influence of climate change on reliability of RC structure under carbonization": "T1",
    "The Impact of Climate Change and Carbonation on the Durability of Concrete Structures in Afghanistan": "T1",
    "Lifetime Assessment of European Reinforced Concrete Structures Subjected to Climate Change": "T1",
    "Climate Change Impacts on Reinforced Concrete Structures: A Bibliometric Analysis": "T1",
    "Deterioration of concrete structures in Australia under a changing climate": "T1",
    "Reliability-Based Assessment of the Effect of Climatic Conditions and CO2 Emissions": "T1",
    "The effect of climate change and low CO2-binders on the service life of concrete structures": "T1",
    "Assessment of the potential loss of durability of reinforced concrete under climate change": "T1",
    "Rethinking concrete durability for low-carbon concretes through climate-informed corrosion modelling": "T1",
    "WHY THE IMPACT OF CLIMATIC CHANGE ON CONCRETE DURABILITY CANNOT BE PREDICTED AT PRESENT": "T1",
    "Climate change impact on RC structures subjected to chloride ingress and carbonation": "T1",
    "Climate change induced carbonation and corrosion of EU building stock": "T1",
    "Climate change effects on the structural reliability of reinforced concrete building in Veneto": "T1",
    "Future climate scenarios and their impact on carbonation of reinforced concrete structures in Brazil": "T1",
    "Influence of CO_2 Emission and Climate Change on Initiation Corrosion Time": "T1",
    "Climate-Responsive Modelling of Carbonation and Strength Degradation": "T1",
    "Influence of climate change on concrete durability in Yucatan": "T1",
    # T2 tropical / African durability evidence
    "Carbonation of concrete in the tropical environment of Singapore": "T2",
    "The carbonation of concrete structures in the tropical environment of singapore": "T2",
    "Carbonation of concrete bridge structures in three South African localities": "T2",
    "Service life design and modelling of concrete structures": "T2",
    "Concrete Carbonation in Ibero-American Countries DURACON": "T2",
    "A Case Study on Practical Prediction of Natural Carbonation": "T2",
    "Concrete durability standards: International trends and the South African context": "T2",
    "Carbonation-Induced Corrosion in Urban Concrete Structures": "T2",
    "Concrete carbonation in tropical urban and urban/marine environments after 20 years": "T2",
    "Natural carbonation of concretes with supplementary cementitious materials in a Brazilian tropical": "T2",
    "Synergistic impact of temperature and pore saturation on corrosion in carbonated reinforced concrete": "T2",
    "Service life and durability design of RC structures: general considerations and selected Southern Af": "T2",
    "A practical carbonation model for service life design of reinforced concrete structures": "T2",
    "Assessment of Concrete Durability in Buildings: the Effects of the Quality of Cements": "T2",
    "Severity of Rain-Induced Wetting": "T2",
    "DETERMINATION OF REFERENCE SERVICE LIFE FOR REINFORCED CONCRETE MULTISTOREY RESIDENTIAL BUILDINGS": "T2",
    "Non-Destructive Testing Techniques for Corrosion Assessment in Reinforced Concrete Structures in Ken": "T2",
    "Carbonation of Bridge Deterioration in High Rainfall Tropical Region": "T2",
    "Effect of Selected Cement Brands on the Service Life of Reinforced Concrete": "T2",
    "Probabilistic service life design and analysis": "T2",
    "The natural carbonation prediction (NCP) model and methodology": "T2",
    "Validation of NCP model": "T2",
    "Experimental justification of the NCP model": "T2",
    "Control of concrete cover depth of reinforced concrete structures for durability": "T2",
    "An assessment of a practical implementation of the deemed-to-satisfy durability design": "T2",
    "Use of durability indexes in probabilistic modelling for durability design": "T2",
    "The Effect of a Hot Humid Climate on Corrosion of Reinforced Concrete": "T2",
    "The evolution of performance-based specifications based on the durability index approach": "T2",
    "DURABILITY DESIGN FOR INDONESIAN CLIMATE": "T2",
    # T3 Ugandan materials and construction quality
    "Impact of environmental exposure on concrete strength in highway bridges in Uganda": "T3",
    "Pozzolanic and hydration properties of kamafugites": "T3",
    "THE EFFECT OF CONCRETE EXPANSION AT OWEN FALLS POWER STATION": "T3",
    "Forensic Investigations of Concrete Degradation: Case Study of a Hydropower Project": "T3",
    "Research on Development of Alternative Cements Based on Lime Pozzolanas in Uganda": "T3",
    "Standardisation of construction and building materials in Uganda": "T3",
    "Pozzolans as a binder for affordable building materials in Uganda": "T3",
    "Factors that led to an increase of building collapses during the COVID-19": "T3",
    "Investigating Implementation Strategies towards Elimination of Structural Failure": "T3",
    "The Concrete Reinforcing Value of Recycled Steel Bars in Uganda": "T3",
    "Compliance of Reinforced Concrete Buildings in Fort Portal": "T3",
    "Assessing the Effect of Water from Different Sources on the Strength of Concrete": "T3",
    "Pozzolanic cements in Uganda": "T3",
    "Evaluating the performance of indigenous volcanic scoria rocks from Uganda": "T3",
    "Factor Analysis for In Situ Reinforced Concrete Beam Production": "T3",
    # T4 growth, exposure and urban climate
    "Urban growth of Kampala, Uganda: Pattern analysis and scenario development": "T4",
    "Adapting urban areas in Africa to climate change: the case of Kampala": "T4",
    "Urban Informality and Vulnerability: A Case Study in Kampala": "T4",
    "How urbanisation alters the intensity of the urban heat island in a tropical African city": "T4",
    "Developing a cellular automata model of urban growth to inform spatial policy for flood": "T4",
    "Will urban farming survive the growth of African cities": "T4",
    "Patterns of Urban Sprawl and Agricultural Land Loss in Sub-Saharan Africa": "T4",
    "Lack of vegetation exacerbates exposure to dangerous heat in dense settlements": "T4",
    "ASSURE: a model for the simulation of urban expansion": "T4",
    "Tropical surface urban heat islands in east Africa": "T4",
    "Spatial assessment of urban sprawl in Arua Municipality": "T4",
    "Spatiotemporal dynamics of urban climate during the wet-dry season transition": "T4",
    "Sprawl and the City. House Types in the Formal and Informal Settlements of Kampala": "T4",
    "Simulating Spatial Patterns of Urban Growth in Kampala, Uganda, and Its Impact on Flood": "T4",
    "Constraints to Urban Planning and Management of Secondary Towns in Uganda": "T4",
    # added after the Scopus merge (1 Oct 2026)
    "Effect of global climatic change on carbonation progress of concrete": "T1",
    "Climate change, deterioration and time-dependent reliability of concrete structures": "T1",
    "Climate change and its influences on spatial time-dependent reliability of pretensioned prestressed": "T1",
    "Deterioration of concrete structures in Australia under changing environment": "T1",
    "global climate change on the lifespan of concrete structures in Mumbai": "T1",
    "Carbonation in concrete infrastructure in the context of global climate change: Part 2": "T1",
    "Synthetic climate modeling for estimating the impact of global warming on construction materials": "T1",
    "Is climate change a concern?": "T1",
    "Models for reliability assessment of reinforced concrete structures in corrosive environments in conditions of a changing climate": "T1",
    "Urban scale mapping of concrete degradation from projected climate change": "T1",
    "Probabilistic optimization of the concrete cover for structures exposed to chlorination and carbonation": "T1",
    "Assessing climate impact on reinforced concrete durability with a multi-physics model": "T1",
    "carbonation-induced corrosion in Reinforced Concrete Structures in Malta": "T1",
    "Research on prediction of the initiation time of carbonated induced steel corrosion": "T1",
    "Effect of global warming on the proportional design of low CO2 slag-blended concrete": "T1",
    "Impact of climate change on proportional design of fly": "T1",
    "Carbonation of concrete in a climate change context": "T1",
    "Service life predictions for RC bridges under time-varying climate conditions": "T1",
    "Impacts of climate change on optimal mixture design of blended concrete considering carbonation": "T1",
    "Consideration of climate change-induced corrosion by structural codes": "T1",
    "Degradation of Concrete Structures from the Climate Change Perspective": "T1",
    "Impact of climate change on the carbonation in concrete due to carbon dioxide ingress": "T1",
    "Impact of climate change on the durability of heritage buildings with structural concrete": "T1",
    "Stochastic Carbon Dioxide Forecasting Model for Concrete Durability": "T1",
    "Reliability Analysis for Service Life of Concrete Structures Subject to Various Carbon Dioxide Concentrations": "T1",
    "impact of microclimate change on the corrosion performance of a bridge subjected to carbonation": "T1",
    "3D probabilistic satisfaction surface diagram for evaluation of concrete carbonation": "T1",
    "Resilient maintenance of carbonation-affected concrete infrastructure": "T1",
    "The Impact of Climate Change Scenarios on The Time-Dependent Capacity of Reinforced Concrete": "T1",
    "Durability Deterioration of Reinforced Concrete Structures: A Framework Considering Climate": "T1",
    "Climate Change on Carbonation-Induced Corrosion in Reinforced Concrete in Multiple Regions of Vietnam": "T1",
    "Climate-adaptive optimization of low-carbon slag": "T1",
    "Implications of global CO2 emissions on natural carbonation and service lifespan": "T1",
    "Carbonation model for concretes with fly ash, slag, and limestone calcined clay": "T2",
    "A worldwide survey of concrete service life in various climate zones": "T2",
    "Carbonation in the tropics. A typical case of the Estadio Pachencho Romero": "T2",
    "Performance specifications for concrete using the durability index approach": "T2",
    "Carbonation-induced corrosion in buildings under tropical environments": "T2",
    "development towards a performance specification in South Africa": "T2",
    "A framework for use of durability indexes in performance-based design": "T2",
    "Durability design in the African concrete code": "T2",
    "Performance-based durability testing, design and specification in South Africa": "T2",
    "Poor quality concrete: A major challenge in the building construction industry in Nigeria": "T2",
    "durability indexes in the deemed-to-satisfy approach and the full-prob": "T2",
    "Robustness improvement of fresh concrete and mortar performance for challenging casting environments": "T2",
    "Practical implementation of the durability index performance-based design approach": "T2",
    "Challenges and opportunities in tropical concreting": "T2",
    "compressive strength and rebar parameters of reinforced concrete in buildings in Nairobi": "T2",
    "Suitability of Nigerian Portland-limestone cement grades": "T2",
    "towards the rationalization of guidelines": "T2",
    "Simulation of moisture ingress in concrete subjected to intermittent rainfall": "T2",
    "Performance-based concrete durability design and specification in south africa": "T2",
    "Diameter inconsistency, strength and corrosion characteristics of locally-produced": "T2",
    "influence of cover depth and concrete quality on time to cover cracking due to carbonation": "T2",
    "Corrosion of steel reinforcements in concretes of non-coastal areas": "T2",
    "Corrosion induced cracking in concrete exposed to a South Africa inland environment": "T2",
    "initial moist curing on carbonation of concrete in a semi-arid": "T2",
    "Field investigation of slab deterioration due to carbonation in a concrete building": "T2",
    "Materials and technology solutions to tackle the challenges in daily concrete construction": "T2",
    "Model for natural carbonation prediction (NCP): Practical application worldwide": "T2",
    "Service life design for inland concrete structures in Africa: Kampala case study": "T2",
    "An assessment of some physical properties of different brands of cement in Nigeria": "T2",
    "Use of natural pozzolans in high-performance concrete for the Mombasa": "T2",
    "Service-life and Sustainability of Concrete Structure in Tropical Condition": "T2",
    "Carbonation of Granite Fines Concrete in the Tropical Environment": "T2",
    "Climate-driven building pathology in tropical and coastal environments": "T2",
    "Investigation of Existing Building Condition for Maintenance": "T2",
    "Perception of professionals on causes of structural cracks in concrete buildings": "T2",
    "Assessing the Suitability of Tanzanian Kaolinite Clay": "T2",
    "Calcination of Carbonatites and Kamafugites on Their Pozzolanic Performance": "T3",
    "Sustainable urban development: Managing City development in Uganda": "T4",
    "Surface Urban Heat Island (SUHI) Using Landsat: Application on African Cities": "T4",
    "Urban expansion and its effects on land surface temperature and vegetation in three east African cities": "T4",
}

FLAGGED = {
    "Structural Integrity Assessment of Aging Infrastructure in Uganda":
        "18 near-identical Zenodo records, back-dated 2002-2013 (before Zenodo existed), implausible author attribution",
    "Assessment of Structural Integrity in Aging Infrastructure in Uganda":
        "same suspect series as above",
    "Durability of Portland Cement Concrete Under the Humid Tropical Climate of Juba":
        "multiple duplicate Zenodo uploads, not peer reviewed; noted but not synthesised",
}


def main():
    s1 = pd.read_csv(RES / "screen_stage1_all.csv").fillna("")
    inc1 = s1[s1.stage1 == "include"].copy()

    def decide(title):
        for k, v in FLAGGED.items():
            if k.lower() in title.lower():
                return "flagged", v
        for k, v in INCLUDE.items():
            if k.lower() in title.lower():
                return "include", v
        return "exclude", "stage 2: off-topic on title/abstract"

    inc1[["stage2", "theme"]] = inc1.title.apply(lambda t: pd.Series(decide(t)))
    final = inc1[inc1.stage2 == "include"]
    final = final[~final.title.str.lower().str.replace(r"[^a-z0-9]", "", regex=True).str[:80].duplicated()]
    final = final.sort_values(["theme", "year"])
    final[["theme", "year", "first_author", "title", "source", "doi", "cited_by", "searches", "database"]].to_csv(
        RES / "included_final.csv", index=False)
    missing = [k for k in INCLUDE if not final.title.str.lower().str.contains(k.lower(), regex=False).any()]
    oa = json.loads((RES / "counts.json").read_text())
    sc = json.loads((RES / "scopus_counts.json").read_text())
    oa_hits = {k: v for k, v in oa.items() if k.startswith("S")}
    prisma = {
        "identified": {"openalex": oa_hits, "scopus": sc["hits"]},
        "identified_total": {"openalex": int(sum(oa_hits.values())), "scopus": int(sum(sc["hits"].values()))},
        "scopus_ineligible_type_year_language": int(sum(sc["ineligible"].values())),
        "duplicates_within_openalex": int(sum(oa_hits.values()) - oa["union_unique"]),
        "duplicates_within_scopus": int(sum(sc["eligible"].values()) - sc["scopus_unique"]),
        "duplicates_across_databases": sc["scopus_in_openalex"],
        "records_screened": int(len(s1)),
        "records_by_database": s1.database.value_counts().to_dict(),
        "excluded_corrupted_metadata": int((s1.stage1_reason == "corrupted abstract metadata").sum()),
        "excluded_stage1_rules": int(((s1.stage1 == "exclude") & (s1.stage1_reason != "corrupted abstract metadata")).sum()),
        "screened_stage2": int(len(inc1)),
        "flagged_integrity": int((inc1.stage2 == "flagged").sum()),
        "excluded_stage2": int((inc1.stage2 == "exclude").sum()),
        "duplicates_in_included": int((inc1.stage2 == "include").sum() - len(final)),
        "included": int(len(final)),
        "included_by_theme": final.theme.value_counts().sort_index().to_dict(),
        "included_by_database": final.database.value_counts().to_dict(),
        "unmatched_include_keys": missing,
    }
    (RES / "prisma.json").write_text(json.dumps(prisma, indent=2))
    print(json.dumps(prisma, indent=2))


if __name__ == "__main__":
    main()
