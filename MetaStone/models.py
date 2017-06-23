from django.contrib.auth.models import User
from django.contrib.postgres.fields import HStoreField
from django.db import models

from MetaStone.EnumFields.DatabaseModels.Genome import EcosystemCategories, SpeciesCategories, SequencingCategories
from MetaStone.EnumFields.DatabaseModels.Genome import SamplingSiteCategories, Conglomeration
from MetaStone.EnumFields.DatabaseModels.Internal import Uploads
from MetaStone.EnumFields.DatabaseModels.Metagenome import Gold
from MetaStone.EnumFields.DatabaseModels.UserMetagenome import Project


###
# Maybe needed, if hstore does not work out of the box
#
# https://docs.djangoproject.com/en/1.9/ref/contrib/postgres/fields/#hstorefield
###


class Genome(models.Model):
    taxon_name = models.CharField(max_length=255)
    taxon_oid = models.BigIntegerField(primary_key=True)

    def __str__(self):
        return self.taxon_name

    img_name = {"taxon_name": "taxon_name"}
    alt_img_name = {"Genome Name / Sample Name": "taxon_name"}

    @classmethod
    def create(cls, taxon_oid):
        genome = cls(taxon_oid=taxon_oid)
        return genome


class User_Metagenome(models.Model):
    # MAYBE CHANGE IT?!?!?!
    profile_type = models.CharField(choices=Project.METAGENOME_TYPE, default="undefined", max_length=9)
    abundance_type_stored = models.CharField(choices=Project.ABUNDANCE_TYPE, default="absolute", max_length=8)

    abundance_type = models.CharField(choices=Project.ABUNDANCE_TYPE, default="absolute", max_length=8)
    file_type = models.CharField(choices=Project.FILE_TYPE, default="undefined", max_length=9)
    file_path = models.FileField(upload_to='uploads/user_metagenome/')

    metagenome_name = models.CharField(max_length=256)


class User_Metagenome_Sample(models.Model):
    metagenome = models.ForeignKey(User_Metagenome)

    sample_name = models.CharField(max_length=256)

    total_count = models.IntegerField(default=0)

    # sample_metadata = ""


class User_Metagenome_Sample_Genome(models.Model):
    genome = models.ForeignKey(Genome)
    abundance = models.DecimalField(max_digits=10, decimal_places=4)

    genomename_raw = models.CharField(max_length=256)

    metagenome_sample = models.ForeignKey(User_Metagenome_Sample)


class User_Mims(models.Model):
    u_metagenome = models.OneToOneField(User_Metagenome)


class IMG_Metagenome(models.Model):
    taxon_oid = models.BigIntegerField(primary_key=True)
    profile_type = models.CharField(choices=Project.METAGENOME_TYPE, default="undefined", max_length=9)
    abundance_type = models.CharField(choices=Project.ABUNDANCE_TYPE, default="absolute", max_length=8)


class IMG_MetagenomeIdMapping(models.Model):
    metagenome = models.OneToOneField(IMG_Metagenome)

    jgi_projectid = models.IntegerField()
    ncbi_projectid = models.IntegerField()

    img_submission = models.IntegerField()


class IMG_MetagenomeGold(models.Model):
    metagenome = models.OneToOneField(IMG_Metagenome)

    gold_studyid = models.CharField(max_length=50)
    gold_projectid = models.CharField(max_length=50)
    gold_analysis_projectid = models.CharField(max_length=50)

    gold_analysis_project_type = models.CharField(max_length=19, choices=Gold.GOLD_ANALYSIS_PROJECT_TYPE)


class GenomeIdMapping(models.Model):
    genome = models.OneToOneField(Genome, on_delete=models.CASCADE, primary_key=True)

    gold_projectid = models.CharField(max_length=50)
    ncbi_taxonid = models.CharField(max_length=50)

    img_name = {"NCBI Taxon ID": "ncbi_taxonid", "GOLD Project ID": "gold_projectid"}

    alt_img_name = {"GOLD Sequencing Project ID": "gold_projectid"}

    @classmethod
    def create(cls, taxon_oid):
        try:
            gidmap = cls(genome=Genome.objects.get(pk=taxon_oid))
        except Genome.DoesNotExist:
            return None
        else:
            return gidmap


class GenomeLineage(models.Model):
    genome = models.OneToOneField(Genome, on_delete=models.CASCADE, primary_key=True)

    pdomain = models.CharField(max_length=255)
    pphylum = models.CharField(max_length=255)
    pclass = models.CharField(max_length=255)
    porder = models.CharField(max_length=255)
    pfamily = models.CharField(max_length=255)
    pgenus = models.CharField(max_length=255)
    pspecies = models.CharField(max_length=255)
    pstrain = models.CharField(max_length=255)

    def __str__(self):
        return self.pclass + "[...]" + self.pgenus + "[...]" + self.pspecies

    img_name = {"Domain": "pdomain", "Class": "pclass", "Family": "pfamily", "Genus": "pgenus", "Order": "porder",
                "Phylum": "pphylum", "Species": "pspecies", "Strain": "pstrain"}

    @classmethod
    def create(cls, taxon_oid):
        try:
            lineage = cls(genome=Genome.objects.get(pk=taxon_oid))
        except Genome.DoesNotExist:
            return None
        else:
            return lineage


class EcosystemRelatedCharacteristics(models.Model):
    genome = models.OneToOneField(Genome, on_delete=models.CASCADE, primary_key=True)

    relevance = models.CharField(choices=EcosystemCategories.RELEVANCE, default="Unknown", max_length=255)
    ecosystem = models.CharField(choices=EcosystemCategories.ECOSYSTEM, default="Unknown", max_length=255)
    specific_ecosystem = models.CharField(choices=EcosystemCategories.SPECIFIC_ECOSYSTEM, default="Unknown",
                                          max_length=255)
    ecosystem_category = models.CharField(choices=EcosystemCategories.ECOSYSTEM_CATEGORY, default="Unknown",
                                          max_length=255)
    ecosystem_type = models.CharField(choices=EcosystemCategories.ECOSYSTEM_TYPE, default="Unknown", max_length=255)
    ecosystem_subtype = models.CharField(choices=EcosystemCategories.ECOSYSTEM_SUBTYE, default="Unknown",
                                         max_length=255)

    img_name = {"Relevance": "relevance", "Ecosystem": "ecosystem", "Specific Ecosystem": "specific_ecosystem",
                "Ecosystem Category": "ecosystem_category", "Ecosystem Type": "ecosystem_type",
                "Ecosystem Subtype": "ecosystem_subtype"}

    non_distinct = ["relevance"]

    ml_inferred_available = False

    @classmethod
    def create(cls, taxon_oid):
        try:
            eco = cls(genome=Genome.objects.get(pk=taxon_oid))
        except Genome.DoesNotExist:
            return None
        else:
            return eco


class DirectInferredEcosystemRelatedCharacteristics(models.Model):
    genome = models.ForeignKey(Genome, on_delete=models.CASCADE)

    relevance_hstore = HStoreField(null=True, blank=True)
    ecosystem_hstore = HStoreField(null=True, blank=True)
    specific_ecosystem_hstore = HStoreField(null=True, blank=True)
    ecosystem_category_hstore = HStoreField(null=True, blank=True)
    ecosystem_type_hstore = HStoreField(null=True, blank=True)
    ecosystem_subtype_hstore = HStoreField(null=True, blank=True)

    taxonomy_level = models.CharField(choices=Conglomeration.TAXONOMIC_LEVELS, default="pdomain", max_length=8)

    eval_basename = "ecosystemrelatedcharacteristics"

    img_name = {"Relevance": "relevance_hstore", "Ecosystem": "ecosystem_hstore",
                "Specific Ecosystem": "specific_ecosystem_hstore",
                "Ecosystem Category": "ecosystem_category_hstore", "Ecosystem Type": "ecosystem_type_hstore",
                "Ecosystem Subtype": "ecosystem_subtype_hstore"}

    eval_subnames = {"relevance_hstore": "relevance", "ecosystem_hstore": "ecosystem",
                     "specific_ecosystem_hstore": "specific_ecosystem",
                     "ecosystem_category_hstore": "ecosystem_category", "ecosystem_type_hstore": "ecosystem_type",
                     "ecosystem_subtype_hstore": "ecosystem_subtype"}

    non_distinct = ["relevance_hstore"]

    @classmethod
    def create(cls, taxon_oid):
        try:
            inf = cls(genome=Genome.objects.get(pk=taxon_oid))
        except Genome.DoesNotExist:
            return None
        else:
            return inf


class SpeciesRelatedCharacteristics(models.Model):
    genome = models.OneToOneField(Genome, on_delete=models.CASCADE, primary_key=True)

    biotic_relationships = models.CharField(choices=SpeciesCategories.BIOTICRELATIONSHIPS, default="Unknown",
                                            max_length=255)
    cell_arrangement = models.CharField(choices=SpeciesCategories.CELLARRANGEMENT, default="Unknown", max_length=255)
    cell_shape = models.CharField(choices=SpeciesCategories.CELLSHAPE, default="Unknown", max_length=255)
    diseases = models.CharField(choices=SpeciesCategories.DISEASES, default="Unknown", max_length=255)
    energy_source = models.CharField(choices=SpeciesCategories.ENERGYSOURCE, default="Unknown", max_length=255)
    gram_staining = models.CharField(choices=SpeciesCategories.GRAMSTAINING, default="Unknown", max_length=255)
    metabolism = models.CharField(choices=SpeciesCategories.METABOLISM, default="Unknown", max_length=255)
    motility = models.CharField(choices=SpeciesCategories.MOTILITY, default="Unknown", max_length=255)
    oxygen_requirement = models.CharField(choices=SpeciesCategories.OXYGENREQUIREMENT, default="Unknown",
                                          max_length=255)
    phenotype = models.CharField(choices=SpeciesCategories.PHENOTYPE, default="Unknown", max_length=255)
    sporulation = models.CharField(choices=SpeciesCategories.SPRORULATION, default="Unknown", max_length=255)
    salinity = models.CharField(choices=SpeciesCategories.SALINITY, default="Unknown", max_length=255)
    temperature_range = models.CharField(choices=SpeciesCategories.TEMPERATURERANGE, default="Unknown", max_length=255)

    img_name = {"Biotic Relationships": "biotic_relationships", "Cell Arrangement": "cell_arrangement",
                "Cell Shape": "cell_shape", "Diseases": "diseases", "Energy Source": "energy_source",
                "Gram Staining": "gram_staining", "Metabolism": "metabolism", "Motility": "motility",
                "Oxygen Requirement": "oxygen_requirement", "Phenotype": "phenotype", "Sporulation": "sporulation",
                "Salinity": "salinity", "Temperature Range": "temperature_range"}

    non_distinct = ["phenotype", "energy_source", "metabolism", "diseases", "cell_arrangement"]

    ml_inferred_available = True

    @classmethod
    def create(cls, taxon_oid):
        try:
            spec = cls(genome=Genome.objects.get(pk=taxon_oid))
        except Genome.DoesNotExist:
            return None
        else:
            return spec


class InferredSpeciesRelatedCharacteristics(models.Model):
    genome = models.OneToOneField(Genome, on_delete=models.CASCADE, primary_key=True)

    biotic_relationships = models.CharField(choices=SpeciesCategories.BIOTICRELATIONSHIPS, default="Unknown",
                                            max_length=255)

    cell_arrangement = models.CharField(choices=SpeciesCategories.CELLARRANGEMENT, default="Unknown", max_length=255)
    cell_shape = models.CharField(choices=SpeciesCategories.CELLSHAPE, default="Unknown", max_length=255)
    diseases = models.CharField(choices=SpeciesCategories.DISEASES, default="Unknown", max_length=255)
    energy_source = models.CharField(choices=SpeciesCategories.ENERGYSOURCE, default="Unknown", max_length=255)
    gram_staining = models.CharField(choices=SpeciesCategories.GRAMSTAINING, default="Unknown", max_length=255)
    metabolism = models.CharField(choices=SpeciesCategories.METABOLISM, default="Unknown", max_length=255)
    motility = models.CharField(choices=SpeciesCategories.MOTILITY, default="Unknown", max_length=255)
    oxygen_requirement = models.CharField(choices=SpeciesCategories.OXYGENREQUIREMENT, default="Unknown",
                                          max_length=255)
    phenotype = models.CharField(choices=SpeciesCategories.PHENOTYPE, default="Unknown", max_length=255)
    sporulation = models.CharField(choices=SpeciesCategories.SPRORULATION, default="Unknown", max_length=255)
    salinity = models.CharField(choices=SpeciesCategories.SALINITY, default="Unknown", max_length=255)
    temperature_range = models.CharField(choices=SpeciesCategories.TEMPERATURERANGE, default="Unknown", max_length=255)

    img_name = {"Biotic Relationships": "biotic_relationships", "Cell Arrangement": "cell_arrangement",
                "Cell Shape": "cell_shape", "Diseases": "diseases", "Energy Source": "energy_source",
                "Gram Staining": "gram_staining", "Metabolism": "metabolism", "Motility": "motility",
                "Oxygen Requirement": "oxygen_requirement", "Phenotype": "phenotype", "Sporulation": "sporulation",
                "Salinity": "salinity", "Temperature Range": "temperature_range"}

    non_distinct = ["phenotype", "energy_source", "metabolism", "diseases", "cell_arrangement"]

    @classmethod
    def create(cls, taxon_oid):
        try:
            inf_spec = cls(genome=Genome.objects.get(pk=taxon_oid))
        except Genome.DoesNotExist:
            return None
        else:
            return inf_spec


class DirectInferredSpeciesRelatedCharacteristics(models.Model):
    genome = models.ForeignKey(Genome, on_delete=models.CASCADE)

    biotic_relationships_hstore = HStoreField(null=True, blank=True)
    cell_arrangement_hstore = HStoreField(null=True, blank=True)
    cell_shape_hstore = HStoreField(null=True, blank=True)

    ###
    # TODO: Split before inferring
    ###
    # diseases_hstore = HStoreField()
    ###

    diseases_hstore = HStoreField(null=True, blank=True)
    energy_source_hstore = HStoreField(null=True, blank=True)
    gram_staining_hstore = HStoreField(null=True, blank=True)
    metabolism_hstore = HStoreField(null=True, blank=True)
    motility_hstore = HStoreField(null=True, blank=True)
    oxygen_requirement_hstore = HStoreField(null=True, blank=True)
    phenotype_hstore = HStoreField(null=True, blank=True)
    sporulation_hstore = HStoreField(null=True, blank=True)
    salinity_hstore = HStoreField(null=True, blank=True)
    temperature_range_hstore = HStoreField(null=True, blank=True)

    taxonomy_level = models.CharField(choices=Conglomeration.TAXONOMIC_LEVELS, default="pdomain", max_length=8)

    eval_basename = "speciesrelatedcharacteristics"

    img_name = {"Biotic Relationships": "biotic_relationships_hstore", "Cell Arrangement": "cell_arrangement_hstore",
                "Cell Shape": "cell_shape_hstore", "Energy Source": "energy_source_hstore",
                "Gram Staining": "gram_staining_hstore", "Metabolism": "metabolism_hstore",
                "Motility": "motility_hstore",
                "Oxygen Requirement": "oxygen_requirement_hstore", "Phenotype": "phenotype_hstore",
                "Sporulation": "sporulation_hstore",
                "Salinity": "salinity_hstore", "Temperature Range": "temperature_range_hstore",
                "Diseases": "diseases_hstore"}

    eval_subnames = {"biotic_relationships_hstore": "biotic_relationships",
                     "cell_arrangement_hstore": "cell_arrangement",
                     "cell_shape_hstore": "cell_shape", "energy_source_hstore": "energy_source",
                     "gram_staining_hstore": "gram_staining", "metabolism_hstore": "metabolism",
                     "motility_hstore": "metabolism",
                     "oxygen_requirement_hstore": "oxygen_requirement", "phenotype_hstore": "phenotype",
                     "sporulation_hstore": "sporulation",
                     "salinity_hstore": "salinity", "temperature_range_hstore": "temperature_range"}

    non_distinct = ["phenotype_hstore", "energy_source_hstore", "metabolism_hstore",
                    "cell_arrangement_hstore", "diseases_hstore"]

    @classmethod
    def create(cls, taxon_oid):
        try:
            inf = cls(genome=Genome.objects.get(pk=taxon_oid))
        except Genome.DoesNotExist:
            return None
        else:
            return inf


class SamplingSiteCharacteristics(models.Model):
    genome = models.OneToOneField(Genome, on_delete=models.CASCADE, primary_key=True)

    habitat = models.CharField(choices=SamplingSiteCategories.HABITAT, default="Unknown", max_length=255)
    sample_body_site = models.CharField(choices=SamplingSiteCategories.SAMPLE_BODY_SITE, default="Unknown",
                                        max_length=255)
    sample_body_sub_site = models.CharField(choices=SamplingSiteCategories.SAMPLE_BODY_SUB_SITE, default="Unknown",
                                            max_length=255)

    img_name = {"Habitat": "habitat", "Sample Body Site": "sample_body_site",
                "Sample Body Subsite": "sample_body_sub_site"}

    non_distinct = ["sample_body_site", "habitat"]

    ml_inferred_available = False

    @classmethod
    def create(cls, taxon_oid):
        try:
            samp = cls(genome=Genome.objects.get(pk=taxon_oid))
        except Genome.DoesNotExist:
            return None
        else:
            return samp


class DirectInferredSamplingSiteCharacteristics(models.Model):
    genome = models.ForeignKey(Genome, on_delete=models.CASCADE)

    habitat_hstore = HStoreField(null=True, blank=True)
    sample_body_site_hstore = HStoreField(null=True, blank=True)
    sample_body_sub_site_hstore = HStoreField(null=True, blank=True)

    taxonomy_level = models.CharField(choices=Conglomeration.TAXONOMIC_LEVELS, default="pdomain", max_length=8)

    eval_basename = "samplingsitecharacteristics"

    img_name = {"Habitat": "habitat_hstore", "Sample Body Site": "sample_body_site_hstore",
                "Sample Body Subsite": "sample_body_sub_site_hstore"}

    eval_subnames = {"habitat_hstore": "habitat", "sample_body_site_hstore": "sample_body_site",
                     "sample_body_sub_site_hstore": "sample_body_sub_site"}

    non_distinct = ["sample_body_site_hstore", "habitat_hstore"]

    @classmethod
    def create(cls, taxon_oid):
        try:
            inf = cls(genome=Genome.objects.get(pk=taxon_oid))
        except Genome.DoesNotExist:
            return None
        else:
            return inf


class SequencingCharacteristics(models.Model):
    ###
    # No inferred data here => Meaningless ;)
    ###
    genome = models.OneToOneField(Genome, on_delete=models.CASCADE, primary_key=True)

    sequencing_method = models.CharField(choices=SequencingCategories.SEQUENCING_METHOD, default="Unknown",
                                         max_length=255)
    status = models.CharField(choices=SequencingCategories.STATUS, default="Unknown", max_length=255)
    type_strain = models.CharField(choices=SequencingCategories.TYPESTRAIN, default="Unknown", max_length=255)
    uncultured_type = models.CharField(choices=SequencingCategories.UNCULTUREDTYPE, default="Unknown", max_length=255)

    img_name = {"Sequencing Method": "sequencing_method", "Status": "status", "Type Strain": "type_strain",
                "Uncultured Type": "uncultured_type"}

    non_distinct = ["sequencing_method"]

    ml_inferred_available = False

    @classmethod
    def create(cls, taxon_oid):
        try:
            seq = cls(genome=Genome.objects.get(pk=taxon_oid))
        except Genome.DoesNotExist:
            return None
        else:
            return seq


class Pfam(models.Model):
    func_id = models.CharField(max_length=11, primary_key=True)
    func_name_shrt = models.CharField(max_length=50)
    func_name_full_length = models.CharField(max_length=255)

    img_name = {"func_name_shrt": "func_name_shrt", "func_name_long": "func_name_full_length"}

    @classmethod
    def create(cls, func_id):
        return cls(func_id=func_id)


class Pfam2Genome(models.Model):
    # TODO: SPECIAL IMPORTER NEEDED
    genome = models.OneToOneField(Genome, on_delete=models.CASCADE, primary_key=True)
    pfams = HStoreField(null=True, blank=True)

    @classmethod
    def create(cls, taxon_oid):
        try:
            p2g = cls(genome=Genome.objects.get(pk=taxon_oid))
        except Genome.DoesNotExist:
            return None
        else:
            return p2g


class AdminFileUpload(models.Model):
    db_model = models.CharField(max_length=16, choices=Uploads.TABLE_NAME, default="None")
    status = models.CharField(max_length=10, choices=Uploads.STATUS, default='uploaded')

    ###
    # Substeps in importing
    ###

    file_content = models.FileField(upload_to='uploads/')
    upload_date = models.DateTimeField('Uploaded on')

    def __str__(self):
        return "On " + self.upload_date.date().__str__() + ": " + self.db_model + "with status " + self.status
