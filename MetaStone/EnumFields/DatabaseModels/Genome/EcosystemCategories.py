RELEVANCE = (("ComparativeAnalysis", "Comparative analysis"), ("FoodIndustry", "Food industry"),
             ("AcetateProduction", "Acetate production"), ("PlantSymbiont", "Plant Symbiont"),
             ("ColdAdaptation", "Cold adaptation"), ("VaccineDevelopment", "Vaccine development"),
             ("seqMethod1000Genomes", "1000 Genomes"), ("BiodegradationOfPollutants", "Biodegradation of pollutants"),
             ("SulfurCycle", "Sulfur cycle"), ("HumanMicrobiome", "Human Microbiome"), ("Pathogen", "Pathogen"),
             ("NitrogenFixation", "Nitrogen fixation"), ("Aquaculture", "Aquaculture"),
             ("BacterialPathogen", "Bacterial Pathogen"), ("Bioleaching", "Bioleaching"),
             ("MicrobialDarkMatter", "Microbial Dark Matter"), ("Biotechnological", "Biotechnological"),
             ("Biofuels", "Biofuels"), ("GebaKmg", "GEBA-KMG"), ("PetroleumProduction", "Petroleum production"),
             ("OpportunisticPathogen", "Opportunistic Pathogen"), ("WastewaterTreatment", "Wastewater treatment"),
             ("AntibioticProduction", "Antibiotic production"), ("FrogPathogen", "Frog Pathogen"),
             ("PoultryPathogen", "Poultry Pathogen"), ("EnergyProduction", "Energy production"), ("Medical", "Medical"),
             ("Ebpr", "EBPR"), ("GebaSingleCells", "GEBA-Single Cells"), ("Biohydrogen", "Biohydrogen"),
             ("RootNodulatingBacteriaRnb", "Root Nodulating Bacteria (RNB)"), ("Biodefense", "Biodefense"),
             ("Fermentation", "Fermentation"), ("Biogeochemical", "Biogeochemical"),
             ("NosocomialPathogen", "Nosocomial Pathogen"), ("ModelOrganism", "Model Organism"),
             ("HumanOralMicrobiomeProjectHomp", "Human Oral Microbiome Project (HOMP)"),
             ("HumanMicrobiomeProjectHmp", "Human Microbiome Project (HMP)"), ("Bioenergy", "Bioenergy"),
             ("HumanPathogen", "Human Pathogen"), ("HumanCommensal", "Human commensal"),
             ("MammalPathogen", "Mammal Pathogen"), ("NaturalAttenuation", "Natural Attenuation"),
             ("Agricultural", "Agricultural"), ("NematodePathogen", "Nematode pathogen"), ("Geba", "GEBA"),
             ("OilIndustry", "Oil industry"), ("CommercialInoculant", "Commercial inoculant"),
             ("Ecological", "Ecological"), ("SwinePathogen", "Swine Pathogen"),
             ("MarineMicrobialInitiativeMmi", "Marine Microbial Initiative (MMI)"), ("Unknown", "Unknown"),
             ("AnimalPathogen", "Animal Pathogen"), ("FishPathogen", "Fish Pathogen"),
             ("PlantPathogen", "Plant Pathogen"), ("Biothreat", "Biothreat"), ("ClimateChange", "Climate change"),
             ("TreeOfLife", "Tree of Life"), ("Biocontrol", "Biocontrol"), ("OceanCarbonCycle", "Ocean carbon cycle"),
             ("HumanGutMicrobiomeInitiativeHgmi", "Human Gut Microbiome Initiative (HGMI)"),
             ("Bioremediation", "Bioremediation"), ("Bioreactors", "Bioreactors"),
             ("InsectPathogen", "Insect Pathogen"), ("CattlePathogen", "Cattle Pathogen"), ("Industrial", "Industrial"),
             ("PestControl", "Pest control"), ("Biocatalysis", "Biocatalysis"),
             ("BiopolymerProduction", "Biopolymer production"), ("Environmental", "Environmental"),
             ("Evolution", "Evolution"))

ECOSYSTEM = (("Unknown", "Unknown"), ("Environmental", "Environmental"), ("HostAssociated", "Host-associated"),
             ("Engineered", "Engineered"))

ECOSYSTEM_CATEGORY = (
    ("IndustrialProduction", "Industrial production"), ("Biotransformation", "Biotransformation"),
    ("Unknown", "Unknown"),
    ("Insecta", "Insecta"), ("Mammals", "Mammals"), ("Aquatic", "Aquatic"), ("Wastewater", "Wastewater"),
    ("Fish", "Fish"),
    ("Birds", "Birds"), ("Reptilia", "Reptilia"), ("FoodProduction", "Food production"),
    ("LabSynthesis", "Lab synthesis"),
    ("Air", "Air"), ("Terrestrial", "Terrestrial"), ("Plants", "Plants"), ("Fungi", "Fungi"), ("Amphibia", "Amphibia"),
    ("Unclassified", "Unclassified"), ("Algae", "Algae"), ("Cnidaria", "Cnidaria"), ("Human", "Human"),
    ("BuiltEnvironment", "Built environment"), ("Porifera", "Porifera"), ("SolidWaste", "Solid waste"),
    ("Animal", "Animal"), ("Bioremediation", "Bioremediation"), ("Arthropoda", "Arthropoda"), ("Mollusca", "Mollusca"))

ECOSYSTEM_TYPE = (("DairyProducts", "Dairy products"), ("Unknown", "Unknown"), ("NervousSystem", "Nervous system"),
                  ("ExcretorySystem", "Excretory system"), ("Milk", "Milk"), ("DigestiveSystem", "Digestive system"),
                  ("IndustrialWastewater", "Industrial wastewater"), ("Phylloplane", "Phylloplane"),
                  ("Marine", "Marine"), ("ActivatedSludge", "Activated Sludge"), ("Rhizoplane", "Rhizoplane"),
                  ("AgriculturalField", "Agricultural field"), ("Aquaculture", "Aquaculture"),
                  ("CirculatorySystem", "Circulatory system"), ("Freshwater", "Freshwater"), ("Geologic", "Geologic"),
                  ("ReproductiveSystem", "Reproductive system"), ("ThermalSprings", "Thermal springs"),
                  ("Unclassified", "Unclassified"), ("NonMarineSalineAndAlkaline", "Non-marine Saline and Alkaline"),
                  ("SilageFermentation", "Silage fermentation"), ("Skin", "Skin"), ("OilReservoir", "Oil reservoir"),
                  ("Soil", "Soil"), ("Landfill", "Landfill"), ("Composting", "Composting"),
                  ("SolidAnimalWaste", "Solid animal waste"), ("Sediment", "Sediment"),
                  ("RespiratorySystem", "Respiratory system"), ("Metal", "Metal"),
                  ("EngineeredProduct", "Engineered product"))

ECOSYSTEM_SUBTYE = (
    ("Unknown", "Unknown"), ("Urethra", "Urethra"), ("Petrochemical", "Petrochemical"), ("NeriticZone", "Neritic zone"),
    ("Wetlands", "Wetlands"), ("DrinkingWater", "Drinking water"), ("Nasopharyngeal", "Nasopharyngeal"),
    ("Lotic", "Lotic"),
    ("Lentic", "Lentic"), ("Blood", "Blood"), ("PulmonarySystem", "Pulmonary system"), ("Vagina", "Vagina"),
    ("Glands", "Glands"), ("Unclassified", "Unclassified"), ("LandfillLeachate", "Landfill leachate"),
    ("Groundwater", "Groundwater"), ("Foregut", "Foregut"), ("Mine", "Mine"), ("Fecal", "Fecal"),
    ("HydrothermalVents", "Hydrothermal vents"), ("Oceanic", "Oceanic"), ("MineWater", "Mine water"),
    ("AgriculturalWastewater", "Agricultural wastewater"), ("Ponds", "Ponds"), ("Oral", "Oral"), ("Clay", "Clay"),
    ("Sediment", "Sediment"), ("LargeIntestine", "Large intestine"), ("Hypersaline", "Hypersaline"),
    ("CerebrospinalFluid", "Cerebrospinal fluid"), ("IntertidalZone", "Intertidal zone"))

SPECIFIC_ECOSYSTEM = (
    ("Unknown", "Unknown"), ("OilContaminated", "Oil-contaminated"), ("SaltMarsh", "Salt marsh"), ("Saliva", "Saliva"),
    ("Sputum", "Sputum"), ("Desert", "Desert"), ("AgriculturalLand", "Agricultural land"),
    ("ForestSoil", "Forest soil"),
    ("Beach", "Beach"), ("Unclassified", "Unclassified"), ("Grasslands", "Grasslands"), ("Fecal", "Fecal"),
    ("Contaminated", "Contaminated"), ("Marsh", "Marsh"), ("Urine", "Urine"), ("MangroveSwamp", "Mangrove swamp"),
    ("Permafrost", "Permafrost"), ("Trachea", "Trachea"), ("Estuary", "Estuary"), ("Rumen", "Rumen"),
    ("Sediment", "Sediment"))
