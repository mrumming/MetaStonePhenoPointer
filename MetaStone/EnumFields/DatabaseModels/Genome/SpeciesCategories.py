CELLSHAPE = (
    ("CoccusShaped", "Coccus-shaped"), ("PleomorphicShaped", "Pleomorphic-shaped"), ("CurvedShaped", "Curved-shaped"),
    ("OvalShaped", "Oval-shaped"), ("Unknown", "Unknown"), ("HelicalShaped", "Helical-shaped"),
    ("Triangular", "Triangular"), ("OvoidShaped", "Ovoid-shaped"), ("Coccoid", "Coccoid"),
    ("IrregularShaped", "Irregular-shaped"), ("RodShaped", "Rod-shaped"), ("DiscShaped", "Disc-shaped"),
    ("BeanShaped", "Bean-shaped"), ("SpiralShaped", "Spiral-shaped"), ("VibrioShaped", "Vibrio-shaped"),
    ("SphereShaped", "Sphere-shaped"), ("FilamentShaped", "Filament-shaped"), ("FlaskShaped", "Flask-shaped"))

CELLARRANGEMENT = (("Chains", "Chains"), ("Singles", "Singles"), ("Filaments", "Filaments"), ("Unknown", "Unknown"),
                   ("IrregularColonies", "Irregular  colonies"), ("Clusters", "Clusters"), ("Pairs", "Pairs"),
                   ("VShapedForms", "V-shaped forms"), ("Tetrads", "Tetrads"))

BIOTICRELATIONSHIPS = (("Symbiotic", "Symbiotic"), ("Unknown", "Unknown"), ("FreeLiving", "Free living"))

GRAMSTAINING = (("Unknown", "Unknown"), ("Gram", "Gram-"), ("GramPLUS", "Gram+"))

ENERGYSOURCE = (
    ("Chemoorganotroph", "Chemoorganotroph"), ("Photosynthetic", "Photosynthetic"), ("Methylotroph", "Methylotroph"),
    ("Chemoheterotroph", "Chemoheterotroph"), ("Photoautotroph", "Photoautotroph"),
    ("Carboxydotroph", "Carboxydotroph"),
    ("Phototroph", "Phototroph"), ("Unknown", "Unknown"), ("Photoheterotroph", "Photoheterotroph"),
    ("Autotroph", "Autotroph"), ("Lithotroph", "Lithotroph"), ("Mixotroph", "Mixotroph"),
    ("Chemolithotroph", "Chemolithotroph"), ("Chemolithoautotroph", "Chemolithoautotroph"),
    ("Lithoheterotroph", "Lithoheterotroph"), ("Organoheterotroph", "Organoheterotroph"),
    ("Chemoorganoheterotroph", "Chemoorganoheterotroph"), ("Heterotroph", "Heterotroph"))

DISEASES = (("Brucellosis", "Brucellosis"), ("Anemia", "Anemia"), ("OtitisMedia", "Otitis media"),
            ("Salmonellosis", "Salmonellosis"), ("SoftRot", "Soft rot"), ("LymeDisease", "Lyme disease"),
            ("ChronicGranulomatous", "Chronic granulomatous"), ("Colitis", "Colitis"),
            ("OpportunisticInfection", "Opportunistic infection"), ("Meningitis", "Meningitis"),
            ("Dysenteria", "Dysenteria"), ("Legionellosis", "Legionellosis"), ("GlasserSDisease", "Glasser's disease"),
            ("Monoarthritis", "Monoarthritis"), ("DeathOfCoralReefs", "Death of coral reefs"),
            ("Bacteremia", "Bacteremia"), ("AcrodermatitisChronicaAtrophicans", "Acrodermatitis chronica atrophicans"),
            ("BubonicAndPneumonicPlague", "Bubonic and Pneumonic plague"), ("FoodPoisoning", "Food poisoning"),
            ("CysticFibrosis", "Cystic Fibrosis"), ("Cholera", "Cholera"), ("Cystitis", "Cystitis"),
            ("CepaciaSyndrome", "Cepacia syndrome"), ("Actinomycosis", "Actinomycosis"),
            ("SexuallyTransmittedDisease", "Sexually transmitted disease"), ("Sinusitis", "Sinusitis"),
            ("Leptospirosis", "Leptospirosis"), ("Abscesses", "Abscesses"), ("SystemicDisease", "Systemic disease"),
            ("UrinaryInfection", "Urinary infection"), ("RickettsialPox", "Rickettsial pox"),
            ("EpizooticBovineAbortion", "Epizootic bovine abortion"), ("Tuberculosis", "Tuberculosis"),
            ("Pneumonia", "Pneumonia"), ("UrogenitalInfection", "Urogenital infection"),
            ("CitrusCanker", "Citrus canker"), ("Abortion", "Abortion"), ("WoundInfection", "Wound infection"),
            ("WiltingDisease", "Wilting disease"), ("Anthrax", "Anthrax"), ("LeafScaldDisease", "Leaf scald disease"),
            ("PlantRot", "Plant rot"), ("SuppurativePleuritis", "Suppurative pleuritis"), ("Bronchitis", "Bronchitis"),
            ("HemorrhagicColitis", "Hemorrhagic colitis"), ("AmericanFoulbrood", "American foulbrood"),
            ("PulmonaryInfection", "Pulmonary infection"), ("DentalCaries", "Dental caries"),
            ("GillDisease", "Gill disease"), ("Periodontitis", "Periodontitis"),
            ("GastrointestinalDisease", "Gastrointestinal disease"), ("Bartonellosis", "Bartonellosis"),
            ("BloodInfection", "Blood infection"), ("Anaplasmosis", "Anaplasmosis"),
            ("NecrotizingFasciitis", "Necrotizing fasciitis"), ("Syphilis", "Syphilis"),
            ("Endocarditis", "Endocarditis"), ("Listeriosis", "Listeriosis"),
            ("NosocomialInfection", "Nosocomial infection"), ("DentalPlaque", "Dental plaque"),
            ("Septicemia", "Septicemia"), ("ParatyphoidFever", "Paratyphoid fever"), ("Mastitis", "Mastitis"),
            ("TickBorneRelapsingFever", "Tick-borne relapsing fever"),
            ("UrinaryTractInfection", "Urinary tract infection"), ("Sepsis", "Sepsis"), ("Gingivitis", "Gingivitis"),
            ("Acne", "Acne"), ("Tracheobronchitis", "Tracheobronchitis"), ("Pyelonephritis", "Pyelonephritis"),
            ("NecrotizingEnterocolitis", "Necrotizing enterocolitis"), ("Endophthalmitis", "Endophthalmitis"),
            ("Arthritis", "Arthritis"), ("None", "None"), ("Diarrhea", "Diarrhea"), ("QFever", "Q fever"),
            ("PeriodontalInfection", "Periodontal infection"), ("Endometritis", "Endometritis"),
            ("BovineAnaplasmosis", "Bovine anaplasmosis"), ("ChronicBronchitis", "Chronic bronchitis"),
            ("Unknown", "Unknown"), ("Peritonitis", "Peritonitis"), ("Gastroenteritis", "Gastroenteritis"),
            ("Cholecystitis", "Cholecystitis"), ("SottoDisease", "Sotto disease"),
            ("Enterohaemorrhagic", "Enterohaemorrhagic"), ("RespiratoryInfection", "Respiratory infection"))

METABOLISM = (
    ("Unknown", "Unknown"), ("DegradesCrudeOil", "Degrades crude oil"), ("HydrogenProduction", "Hydrogen production"),
    ("AmmoniaOxidizer", "Ammonia-oxidizer"), ("AminoacidDegrading", "Aminoacid degrading"),
    ("CelluloseDegrader", "Cellulose degrader"), ("AcetateOxidizer", "Acetate oxidizer"),
    ("DinitrogenFixing", "Dinitrogen-fixing"), ("Acetogen", "Acetogen"), ("IronReducer", "Iron reducer"),
    ("MethaneOxidation", "Methane oxidation"), ("Denitrifying", "Denitrifying"),
    ("PolymerDegrader", "Polymer degrader"),
    ("HydrocarbonOxidizing", "Hydrocarbon-oxidizing"), ("MethanolDegrading", "Methanol degrading"),
    ("NitrogenFixerAnaerobic", "Nitrogen fixer- anaerobic"), ("AcetateProducer", "Acetate producer"),
    ("SurfactantDegrading", "Surfactant-degrading"), ("BiomassDegrader", "Biomass degrader"),
    ("FattyAcidOxidizer", "Fatty-acid-oxidizer"), ("Hydrogenotrophic", "Hydrogenotrophic"),
    ("HydrogenMetabolizer", "Hydrogen metabolizer"), ("Methanogen", "Methanogen"), ("Syntrophic", "Syntrophic"),
    ("Homofermentative", "Homofermentative"), ("SulfateReducer", "Sulfate reducer"),
    ("NitrogenFixation", "Nitrogen fixation"), ("MannanLysing", "Mannan lysing"),
    ("SuccinicAcidProduction", "Succinic acid production"), ("AcidProducing", "Acid-producing"),
    ("SulfurMetabolizing", "Sulfur metabolizing"), ("Haloalkalophile", "Haloalkalophile"), ("Nitrifying", "Nitrifying"),
    ("IronOxidizer", "Iron oxidizer"), ("NitrogenFixerAerobic", "Nitrogen fixer- aerobic"),
    ("NitrateReducer", "Nitrate reducer"), ("XylanDegrader", "Xylan degrader"),
    ("EthanolProduction", "Ethanol production"),
    ("Methylotrophic", "Methylotrophic"), ("ChlorateReducer", "Chlorate-reducer"),
    ("DegradesAromaticHydrocarbons", "Degrades aromatic hydrocarbons"), ("LactoseFermenting", "Lactose fermenting"))

MOTILITY = (("Unknown", "Unknown"), ("Nonmotile", "Nonmotile"), ("Chemotactic", "Chemotactic"), ("Motile", "Motile"))

OXYGENREQUIREMENT = (
    ("Aerobe", "Aerobe"), ("ObligateAerobe", "Obligate aerobe"), ("Unknown", "Unknown"), ("Facultative", "Facultative"),
    ("Microaerophilic", "Microaerophilic"), ("Anaerobe", "Anaerobe"), ("ObligateAnaerobe", "Obligate anaerobe"))

PHENOTYPE = (
    ("NematodeParasite", "Nematode parasite"), ("Nontyphoidal", "Nontyphoidal"), ("Luminescent", "Luminescent"),
    ("Unknown", "Unknown"), ("VancomycinResistant", "Vancomycin resistant"), ("Probiotic", "Probiotic"),
    ("Alkalitolerant", "Alkalitolerant"), ("ProteaseProduction", "Protease production"),
    ("BetaHemolytic", "Beta-hemolytic"), ("Parasite", "Parasite"), ("NitrogenCycle", "Nitrogen cycle"),
    ("MeticillinResistant", "Meticillin resistant"), ("MdrMultiDrugResistant", "MDR (Multi-drug resistant)"),
    ("Intracellular", "Intracellular"), ("Anoxygenic", "Anoxygenic"), ("RadiationResistant", "Radiation resistant"),
    ("IntracellularPathogen", "Intracellular pathogen"), ("AceticAcid", "Acetic-acid"),
    ("Enteropathogenic", "Enteropathogenic"), ("Bioluminescent", "Bioluminescent"), ("Pathogen", "Pathogen"),
    ("Acidophile", "Acidophile"), ("AntimicrobialActivities", "Antimicrobial activities"), ("Biofilm", "Biofilm"),
    ("Enterohemorrhagic", "Enterohemorrhagic"), ("Gliding", "Gliding"), ("NonHaemolytic", "Non-Haemolytic"),
    ("CatalaseNegative", "Catalase negative"), ("OpportunisticPathogen", "Opportunistic Pathogen"),
    ("PinkColored", "Pink-colored"), ("Symbiotic", "Symbiotic"), ("Neutrophilic", "Neutrophilic"),
    ("Symbiont", "Symbiont"),
    ("NonPathogen", "Non-Pathogen"), ("InsectParasite", "Insect Parasite"), ("Alkaliphile", "Alkaliphile"),
    ("AlphaHemolytic", "Alpha-hemolytic"), ("ObligateParasite", "Obligate parasite"),
    ("CatalasePositive", "Catalase positive"), ("SlowGrowing", "Slow growing"))

SPRORULATION = (("Sporulating", "Sporulating"), ("Nonsporulating", "Nonsporulating"), ("Unknown", "Unknown"))

SALINITY = (
    ("Unknown", "Unknown"), ("Euryhaline", "Euryhaline"), ("Halotolerant", "Halotolerant"), ("Halophile", "Halophile"),
    ("Stenohaline", "Stenohaline"))

TEMPERATURERANGE = (
    ("Thermotolerant", "Thermotolerant"), ("Hyperthermophile", "Hyperthermophile"), ("Unknown", "Unknown"),
    ("Thermophile", "Thermophile"), ("Mesophile", "Mesophile"), ("Psychrotolerant", "Psychrotolerant"),
    ("Psychrotrophic", "Psychrotrophic"), ("Psychrophile", "Psychrophile"))
