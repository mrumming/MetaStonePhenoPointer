# coding=utf-8

"""
    Metagenomes -- enrich.py

    Date:   21/04/2017 
    Author: Madis Rumming <mrumming@cebitec.uni-bielefeld.de>
"""

__author__ = "Madis Rumming <mrumming@cebitec.uni-bielefeld.de>"
__copyright__ = "Copyright 2017, Computational Metagenomics, Faculty of Technology, Bielefeld University"

__version__ = "0.1"
__maintainer__ = "Madis Rumming"
__email__ = "mrumming@cebitec.uni-bielefeld.de"
__status__ = "Development"

import sys, os, json, biom

from MetaStone.models import User_Metagenome, Genome, EcosystemRelatedCharacteristics, SamplingSiteCharacteristics, \
    SequencingCharacteristics, SpeciesRelatedCharacteristics, InferredSpeciesRelatedCharacteristics
from MetaStone.Procedures.Exports import Metagenome_profile
from MetaStone.Procedures.Imports import UploadModel
from MetaStone.Procedures.Helper import PandasToolkit, DbToolkit

from django.core.management.base import BaseCommand
from django.core.files import File


class Command(BaseCommand):
    help = "Exports genome related metadata to a file as pickled gzip."

    def add_arguments(self, parser):
        parser.add_argument("--input", dest="input", type=str,
                            help="Path to input BIOM file to be enriched with metadata or metagenome ID to export (use --getfromdb switch).")
        parser.add_argument("--metagenomename", dest="mname", type=str, default="Community Profile",
                            help="Some meanungful short name for this community profile. Default: Coomunity Profile")
        parser.add_argument("--output_filename", dest="outfile_name", default="enriched_profile.json", type=str,
                            help="Output file name, will be stored in the same directory where input lies. Will be gzipped JSON. Default: enriched_profile.json")
        parser.add_argument("--storeindb", action="store_true", dest="storedb", default=False,
                            help="Optional, state to store community profile in DB (default: no persisting).")
        parser.add_argument("--getfromdb", action="store_true", dest="getfromdb", default=False,
                            help="Optional, state to get enriched community profile stored in DB.")

    def handle(self, *args, **options):

        if options["getfromdb"]:
            try:
                self.stdout.write(self.style.WARNING("Starting export of enriched community profile."))

                exp = Metagenome_profile.GenericExporter(int(options["input"]), fp=options["outfile_name"])
                exp.export()
            except:
                self.stdout.write(self.style.ERROR("Requested metagenome does not exist. Exiting..."))
                sys.exit(1)
        elif os.path.exists(options["input"]):
            if options["storedb"]:
                self.stdout.write(self.style.WARNING("Starting import of community profile and storing to DB."))

                um = User_Metagenome(profile_type="16s_rRNA", abundance_type="absolute",
                                     abundance_type_stored="absolute", metagenome_name=options["mname"])
                um.save()
                um.file_path.save(name="umeta%i.biom" % (um.id), content=File(open(options["input"], "rt")))

                bb = UploadModel.create("biom", um.file_path.path, um)
                bb.process()
                exp = Metagenome_profile.GenericExporter(um.id, fp=options["outfile_name"])
                exp.export()
                self.stdout.write(self.style.SUCCESS("Community enriched and stored with ID %i." % (um.id)))
            else:
                self.stdout.write(self.style.WARNING("Starting enrichment of community profile."))
                b_ = biom.load_table(options["input"])

                samples = {}
                for b_key in b_.ids():
                    samples[b_key] = {}

                df = PandasToolkit.biom_to_pandas(b_)

                obs_to_genome = {}
                genome_ids = set()
                for observation in b_.ids('observation'):
                    dbhit = DbToolkit.match_str_to_genome_name(True, "none", "",
                                                               *b_.metadata(observation, 'observation')['taxonomy'])
                    if dbhit:
                        obs_to_genome[observation] = dbhit[0].taxon_oid
                        genome_ids.add(dbhit[0].taxon_oid)
                    else:
                        obs_to_genome[observation] = Genome.objects.filter(pk=0)[0].taxon_oid
                        genome_ids.add(0)

                for key in samples.keys():
                    for observation in obs_to_genome.keys():
                        if df[key][observation] > .0:
                            samples[key][obs_to_genome[observation]] = df[key][observation]



                outDict = {}
                outDict["metagenomes"] = {}
                outDict["metagenomes"][options["mname"]] = {}

                outDict["metagenomes"][options["mname"]]["name"] = options["mname"]
                outDict["metagenomes"][options["mname"]]["profile_type"] = "16s_rRNA"

                outDict["metagenomes"][options["mname"]]["samples"] = {}



                for sample in samples.keys():
                    sample_dict = {}
                    for genome in samples[sample].keys():
                        #Gnahhh...
                        sample_dict[genome] = samples[sample][genome]
                    outDict["metagenomes"][options["mname"]]["samples"][sample] = sample_dict

                outDict["genomes"] = {}
                for taxon_oid in genome_ids:
                    if not taxon_oid == 0:
                        genome_dict = {}

                        eco = EcosystemRelatedCharacteristics.objects.get(pk=taxon_oid)
                        genome_dict["Ecosystem related characteristics"] = {}
                        for key in eco.img_name.keys():
                            genome_dict["Ecosystem related characteristics"][key] = [
                                eval("eco.%s" % (eco.img_name[key])), ""]

                        samp = SamplingSiteCharacteristics.objects.get(pk=taxon_oid)
                        genome_dict["Sampling site related characteristics"] = {}
                        for key in samp.img_name.keys():
                            genome_dict["Sampling site related characteristics"][key] = [
                                eval("samp.%s" % (samp.img_name[key])),
                                ""]

                        seq = SequencingCharacteristics.objects.get(pk=taxon_oid)
                        genome_dict["Sequencing related characteristics"] = {}
                        for key in seq.img_name.keys():
                            genome_dict["Sequencing related characteristics"][key] = [
                                eval("seq.%s" % (seq.img_name[key])), ""]

                        spec = SpeciesRelatedCharacteristics.objects.get(pk=taxon_oid)
                        pred_spec = InferredSpeciesRelatedCharacteristics.objects.get(pk=taxon_oid)
                        genome_dict["Species related characteristics"] = {}
                        for key in spec.img_name.keys():
                            genome_dict["Species related characteristics"][key] = [
                                eval("spec.%s" % (spec.img_name[key])),
                                eval("pred_spec.%s" % (pred_spec.img_name[key]))]
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



                outfile = open(options["outfile_name"], "w")
                json.dump(outDict, outfile)
                outfile.close()

        else:
            self.stdout.write(self.style.ERROR("Specified input file does not exist. Exiting..."))
            sys.exit(1)

        self.stdout.write(self.style.SUCCESS("Good bye!"))
