###
# This file necessary due to cross importing errors if put to ./Uploads.py
###

from MetaStone.models import Genome, GenomeIdMapping, GenomeLineage, EcosystemRelatedCharacteristics, \
    SamplingSiteCharacteristics, SequencingCharacteristics, SpeciesRelatedCharacteristics, \
    InferredSpeciesRelatedCharacteristics, Pfam, Pfam2Genome

TASKS = {"Genomes": [Genome], "Genome_Lineage": [GenomeLineage], "Genome_Metadata":
    [GenomeIdMapping, EcosystemRelatedCharacteristics,
     SamplingSiteCharacteristics,
     SequencingCharacteristics,
     SpeciesRelatedCharacteristics], "Pfam": [Pfam], "Pfam2Genome": [Pfam2Genome],
         "ALL": [Genome, GenomeLineage, GenomeIdMapping, EcosystemRelatedCharacteristics, SamplingSiteCharacteristics,
                 SequencingCharacteristics, SpeciesRelatedCharacteristics]}

TASK_FACTORY_ID = {"Genomes": "genome_oid", "Genome_Lineage": "genome_oid", "Genome_Metadata": "genome_oid",
                   "Pfam": "pfam_clans", "Pfam2Genome": "pfam_to_genome", "ALL": "genome_oid"}

# Possible since all phenotype information fields from IMG/GOLD are unique on their own and form a set with distinctive
# keys
IMG_MODELS = [EcosystemRelatedCharacteristics, SamplingSiteCharacteristics, SequencingCharacteristics,
              SpeciesRelatedCharacteristics]

FIELDS_TO_MODEL = {name_: model for model in IMG_MODELS for name_ in model.img_name.values()}

MODEL_TO_INFERRED = {SpeciesRelatedCharacteristics: InferredSpeciesRelatedCharacteristics}
