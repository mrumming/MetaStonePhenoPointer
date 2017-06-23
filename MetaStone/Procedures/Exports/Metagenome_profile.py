from MetaStone.models import User_Metagenome, EcosystemRelatedCharacteristics, SpeciesRelatedCharacteristics, \
    SequencingCharacteristics, SamplingSiteCharacteristics, InferredSpeciesRelatedCharacteristics
from MetaStone.EnumFields.DatabaseModels.Genome import EcosystemCategories, SamplingSiteCategories, \
    SequencingCategories, SpeciesCategories
import json
import random


class GenericExporter(object):
    def __init__(self, u_metagenome_id, export_format='json', fp=None, fill_random_mockdata=False):
        """

        :param u_metagenome: User_Metagenome
        :param export_format: str
        :param fp: filehandle-like object with write() method
        """
        self.u_metagenome_id = u_metagenome_id
        self.export_format = export_format
        self.fp = fp
        self.fill_random_mockdata = fill_random_mockdata

    def export(self):
        outDict = {}
        uMeta = User_Metagenome.objects.get(pk=self.u_metagenome_id)
        outDict["metagenomes"] = {}
        outDict["metagenomes"][uMeta.metagenome_name] = {}

        outDict["metagenomes"][uMeta.metagenome_name]["name"] = uMeta.metagenome_name
        outDict["metagenomes"][uMeta.metagenome_name]["profile_type"] = uMeta.profile_type

        outDict["metagenomes"][uMeta.metagenome_name]["samples"] = {}

        genome_ids = set()
        print(uMeta.metagenome_name)

        for sample in uMeta.user_metagenome_sample_set.all():
            sample_dict = {}
            for genome in sample.user_metagenome_sample_genome_set.all():
                genome_ids.add(genome.genome.taxon_oid)
                if genome.abundance.__float__().is_integer():
                    sample_dict[genome.genome.taxon_oid] = genome.abundance.__int__()
                else:
                    sample_dict[genome.genome.taxon_oid] = genome.abundance.__float__()
            outDict["metagenomes"][uMeta.metagenome_name]["samples"][sample.sample_name] = sample_dict

        outDict["genomes"] = {}
        for taxon_oid in genome_ids:
            if not taxon_oid == 0:
                genome_dict = {}

                eco = EcosystemRelatedCharacteristics.objects.get(pk=taxon_oid)
                genome_dict["Ecosystem related characteristics"] = {}
                for key in eco.img_name.keys():
                    if self.fill_random_mockdata:
                        if eco.img_name[key] == "relevance":
                            genome_dict["Ecosystem related characteristics"][key] = [
                                eval("eco.%s" % (eco.img_name[key])),
                                EcosystemCategories.RELEVANCE[
                                    random.randint(0, len(
                                        EcosystemCategories.RELEVANCE) - 1)][
                                    1]]
                        elif eco.img_name[key] == "ecosystem":
                            genome_dict["Ecosystem related characteristics"][key] = [
                                eval("eco.%s" % (eco.img_name[key])),
                                EcosystemCategories.ECOSYSTEM[
                                    random.randint(0, len(
                                        EcosystemCategories.ECOSYSTEM) - 1)][
                                    1]]
                        elif eco.img_name[key] == "specific_ecosystem":
                            genome_dict["Ecosystem related characteristics"][key] = [
                                eval("eco.%s" % (eco.img_name[key])),
                                EcosystemCategories.SPECIFIC_ECOSYSTEM[
                                    random.randint(0, len(
                                        EcosystemCategories.SPECIFIC_ECOSYSTEM) - 1)][
                                    1]]
                        elif eco.img_name[key] == "ecosystem_category":
                            genome_dict["Ecosystem related characteristics"][key] = [
                                eval("eco.%s" % (eco.img_name[key])),
                                EcosystemCategories.ECOSYSTEM_CATEGORY[
                                    random.randint(0, len(
                                        EcosystemCategories.ECOSYSTEM_CATEGORY) - 1)][
                                    1]]
                        elif eco.img_name[key] == "ecosystem_type":
                            genome_dict["Ecosystem related characteristics"][key] = [
                                eval("eco.%s" % (eco.img_name[key])),
                                EcosystemCategories.ECOSYSTEM_TYPE[
                                    random.randint(0, len(
                                        EcosystemCategories.ECOSYSTEM_TYPE) - 1)][
                                    1]]
                        else:
                            genome_dict["Ecosystem related characteristics"][key] = [
                                eval("eco.%s" % (eco.img_name[key])),
                                EcosystemCategories.ECOSYSTEM_SUBTYE[
                                    random.randint(0, len(
                                        EcosystemCategories.ECOSYSTEM_SUBTYE) - 1)][
                                    1]]
                    else:
                        genome_dict["Ecosystem related characteristics"][key] = [eval("eco.%s" % (eco.img_name[key])),
                                                                                 ""]

                samp = SamplingSiteCharacteristics.objects.get(pk=taxon_oid)
                genome_dict["Sampling site related characteristics"] = {}
                for key in samp.img_name.keys():
                    if self.fill_random_mockdata:
                        if samp.img_name[key] == "habitat":
                            genome_dict["Sampling site related characteristics"][key] = [
                                eval("samp.%s" % (samp.img_name[key])),
                                SamplingSiteCategories.HABITAT[
                                    random.randint(0, len(
                                        SamplingSiteCategories.HABITAT) - 1)][
                                    1]
                            ]
                        elif samp.img_name[key] == "sample_body_site":
                            genome_dict["Sampling site related characteristics"][key] = [
                                eval("samp.%s" % (samp.img_name[key])),
                                SamplingSiteCategories.SAMPLE_BODY_SITE[
                                    random.randint(0, len(
                                        SamplingSiteCategories.SAMPLE_BODY_SITE) - 1)][
                                    1]
                            ]
                        else:
                            genome_dict["Sampling site related characteristics"][key] = [
                                eval("samp.%s" % (samp.img_name[key])),
                                SamplingSiteCategories.SAMPLE_BODY_SUB_SITE[
                                    random.randint(0, len(
                                        SamplingSiteCategories.SAMPLE_BODY_SUB_SITE) - 1)][
                                    1]
                            ]
                    else:
                        genome_dict["Sampling site related characteristics"][key] = [
                            eval("samp.%s" % (samp.img_name[key])),
                            ""]

                seq = SequencingCharacteristics.objects.get(pk=taxon_oid)
                genome_dict["Sequencing related characteristics"] = {}
                for key in seq.img_name.keys():
                    if self.fill_random_mockdata:
                        if seq.img_name[key] == "sequencing_method":
                            genome_dict["Sequencing related characteristics"][key] = [
                                eval("seq.%s" % (seq.img_name[key])),
                                SequencingCategories.SEQUENCING_METHOD[
                                    random.randint(0, len(
                                        SequencingCategories.SEQUENCING_METHOD) - 1)][
                                    1]
                            ]
                        elif seq.img_name[key] == "status":
                            genome_dict["Sequencing related characteristics"][key] = [
                                eval("seq.%s" % (seq.img_name[key])),
                                SequencingCategories.STATUS[
                                    random.randint(0, len(
                                        SequencingCategories.STATUS) - 1)][
                                    1]
                            ]
                        elif seq.img_name[key] == "type_strain":
                            genome_dict["Sequencing related characteristics"][key] = [
                                eval("seq.%s" % (seq.img_name[key])),
                                SequencingCategories.TYPESTRAIN[
                                    random.randint(0, len(
                                        SequencingCategories.TYPESTRAIN) - 1)][
                                    1]
                            ]
                        else:
                            genome_dict["Sequencing related characteristics"][key] = [
                                eval("seq.%s" % (seq.img_name[key])),
                                SequencingCategories.UNCULTUREDTYPE[
                                    random.randint(0, len(
                                        SequencingCategories.UNCULTUREDTYPE) - 1)][
                                    1]
                            ]
                    else:
                        genome_dict["Sequencing related characteristics"][key] = [eval("seq.%s" % (seq.img_name[key])),
                                                                                  ""]

                spec = SpeciesRelatedCharacteristics.objects.get(pk=taxon_oid)
                pred_spec = InferredSpeciesRelatedCharacteristics.objects.get(pk=taxon_oid)
                # inf_spec = InferredSpeciesRelatedCharacteristics.objects.get(pk=taxon_oid)
                genome_dict["Species related characteristics"] = {}
                for key in spec.img_name.keys():
                    if self.fill_random_mockdata:
                        if spec.img_name[key] == "biotic_relationships":
                            genome_dict["Species related characteristics"][key] = [
                                eval("spec.%s" % (spec.img_name[key])),
                                SpeciesCategories.BIOTICRELATIONSHIPS[
                                    random.randint(0, len(
                                        SpeciesCategories.BIOTICRELATIONSHIPS) - 1)][
                                    1]
                            ]
                        elif spec.img_name[key] == "cell_arrangement":
                            genome_dict["Species related characteristics"][key] = [
                                eval("spec.%s" % (spec.img_name[key])),
                                SpeciesCategories.CELLARRANGEMENT[
                                    random.randint(0, len(
                                        SpeciesCategories.CELLARRANGEMENT) - 1)][
                                    1]
                            ]
                        elif spec.img_name[key] == "cell_shape":
                            genome_dict["Species related characteristics"][key] = [
                                eval("spec.%s" % (spec.img_name[key])),
                                SpeciesCategories.CELLSHAPE[
                                    random.randint(0, len(
                                        SpeciesCategories.CELLSHAPE) - 1)][
                                    1]
                            ]
                        elif spec.img_name[key] == "diseases":
                            genome_dict["Species related characteristics"][key] = [
                                eval("spec.%s" % (spec.img_name[key])),
                                SpeciesCategories.DISEASES[
                                    random.randint(0, len(
                                        SpeciesCategories.DISEASES) - 1)][
                                    1]
                            ]
                        elif spec.img_name[key] == "energy_source":
                            genome_dict["Species related characteristics"][key] = [
                                eval("spec.%s" % (spec.img_name[key])),
                                SpeciesCategories.ENERGYSOURCE[
                                    random.randint(0, len(
                                        SpeciesCategories.ENERGYSOURCE) - 1)][
                                    1]
                            ]
                        elif spec.img_name[key] == "gram_staining":
                            genome_dict["Species related characteristics"][key] = [
                                eval("spec.%s" % (spec.img_name[key])),
                                SpeciesCategories.GRAMSTAINING[
                                    random.randint(0, len(
                                        SpeciesCategories.GRAMSTAINING) - 1)][
                                    1]
                            ]
                        elif spec.img_name[key] == "metabolism":
                            genome_dict["Species related characteristics"][key] = [
                                eval("spec.%s" % (spec.img_name[key])),
                                SpeciesCategories.METABOLISM[
                                    random.randint(0, len(
                                        SpeciesCategories.METABOLISM) - 1)][
                                    1]
                            ]
                        elif spec.img_name[key] == "motility":
                            genome_dict["Species related characteristics"][key] = [
                                eval("spec.%s" % (spec.img_name[key])),
                                SpeciesCategories.MOTILITY[
                                    random.randint(0, len(
                                        SpeciesCategories.MOTILITY) - 1)][
                                    1]
                            ]
                        elif spec.img_name[key] == "oxygen_requirement":
                            genome_dict["Species related characteristics"][key] = [
                                eval("spec.%s" % (spec.img_name[key])),
                                SpeciesCategories.OXYGENREQUIREMENT[
                                    random.randint(0, len(
                                        SpeciesCategories.OXYGENREQUIREMENT) - 1)][
                                    1]
                            ]
                        elif spec.img_name[key] == "phenotype":
                            genome_dict["Species related characteristics"][key] = [
                                eval("spec.%s" % (spec.img_name[key])),
                                SpeciesCategories.PHENOTYPE[
                                    random.randint(0, len(
                                        SpeciesCategories.PHENOTYPE) - 1)][
                                    1]
                            ]
                        elif spec.img_name[key] == "sporulation":
                            genome_dict["Species related characteristics"][key] = [
                                eval("spec.%s" % (spec.img_name[key])),
                                SpeciesCategories.SPRORULATION[
                                    random.randint(0, len(
                                        SpeciesCategories.SPRORULATION) - 1)][
                                    1]
                            ]
                        elif spec.img_name[key] == "salinity":
                            genome_dict["Species related characteristics"][key] = [
                                eval("spec.%s" % (spec.img_name[key])),
                                SpeciesCategories.SALINITY[
                                    random.randint(0, len(
                                        SpeciesCategories.SALINITY) - 1)][
                                    1]
                            ]
                        else:
                            genome_dict["Species related characteristics"][key] = [
                                eval("spec.%s" % (spec.img_name[key])),
                                SpeciesCategories.TEMPERATURERANGE[
                                    random.randint(0, len(
                                        SpeciesCategories.TEMPERATURERANGE) - 1)][
                                    1]
                            ]
                    else:
                        # genome_dict["Species related characteristics"][key] = [eval("spec.%s" % (spec.img_name[key])),
                        #                                                       eval("inf_spec.%s" % (inf_spec.img_name[key]))]
                        genome_dict["Species related characteristics"][key] = [eval("spec.%s" % (spec.img_name[key])),
                                                                               eval("pred_spec.%s" % (
                                                                               pred_spec.img_name[key]))]
            else:
                genome_dict = {}
                genome_dict["Ecosystem related characteristics"] = {}
                genome_dict["Sampling site related characteristics"] = {}
                genome_dict["Sequencing related characteristics"] = {}
                genome_dict["Species related characteristics"] = {}
                for key in EcosystemRelatedCharacteristics.img_name.keys():
                    genome_dict["Ecosystem related characteristics"][key] = ["Undetermined", "Undetermined"]
                for key in SamplingSiteCharacteristics.img_name.keys():
                    genome_dict["Sampling site related characteristics"][key] = ["Undetermined", "Undetermined"]
                for key in SequencingCharacteristics.img_name.keys():
                    genome_dict["Sequencing related characteristics"][key] = ["Undetermined", "Undetermined"]
                for key in SpeciesRelatedCharacteristics.img_name.keys():
                    genome_dict["Species related characteristics"][key] = ["Undetermined", "Undetermined"]

            outDict["genomes"][taxon_oid] = genome_dict

        if self.export_format == "json" and self.fp:
            outfile = open(self.fp, "w")
            json.dump(outDict, outfile)
            outfile.close()
        elif self.export_format == "json":
            return json.dumps(outDict)
        elif self.export_format == "dict":
            return outDict
        else:
            return outDict
