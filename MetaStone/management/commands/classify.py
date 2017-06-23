# coding=utf-8

"""
    Metagenomes -- classify

    Date:   10/05/2017 
    Author: Madis Rumming <mrumming@cebitec.uni-bielefeld.de>
"""

__author__ = "Madis Rumming <mrumming@cebitec.uni-bielefeld.de>"
__copyright__ = "Copyright 2017, Computational Metagenomics, Faculty of Technology, Bielefeld University"

__version__ = "0.1"
__maintainer__ = "Madis Rumming"
__email__ = "mrumming@cebitec.uni-bielefeld.de"
__status__ = "Development"

from django.core.management.base import BaseCommand

from MetaStone.Procedures.MachineLearning.Tools import Pipelines

from django.conf import settings
import subprocess
import os
import sys


class Command(BaseCommand):
    help = "Classifies a (set of) genome(s) for expressed phenotypes and microbial traits."

    def add_arguments(self, parser):
        parser.add_argument("input_base_path", type=str)
        parser.add_argument("input_suffix", type=str)
        parser.add_argument("--fastaasinput", action="store_true", dest="fasta", default=False,
                            help="Perform pfam_scan priot to characterization. Needed, if input is fasta and not pfam profiles.")
        parser.add_argument("outfile", type=str)
        parser.add_argument("--tmpdir", dest="tmpdir", type=str, default="",
                            help="Path to save temporary files and directories (used when performing prodigal/pfam_scan). Default: input base path.",
                            required=False)

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Starting CLassification."))
        prod_path = ""
        pfam_path = ""
        in_path = options["input_base_path"]
        in_suffix = options["input_suffix"]
        outfile_path = os.path.join(os.path.abspath(options["input_base_path"]), options["outfile"])
        if options["fasta"]:
            self.stdout.write(self.style.WARNING("Checking and creating tmp dirs."))
            if options["tmpdir"]:
                if os.path.isabs(options["tmpdir"]):
                    if os.path.exists(os.path.abspath(options["tmpdir"])):
                        if os.path.exists(os.path.join(os.path.abspath(options["tmpdir"]), "PRODIGAL")):
                            self.stdout.write(
                                self.style.ERROR("Directory PRODIGAL alreade exists in tmp dir. Exiting."))
                            sys.exit(1)
                        elif os.path.exists(os.path.join(os.path.abspath(options["tmpdir"]), "PFAM")):
                            self.stdout.write(
                                self.style.ERROR("Directory PFAM alreade exists in tmp dir. Exiting."))
                            sys.exit(1)
                        else:
                            os.mkdir(os.path.join(os.path.abspath(options["tmpdir"]), "PRODIGAL"))
                            os.mkdir(os.path.join(os.path.abspath(options["tmpdir"]), "PFAM"))
                    else:
                        os.makedirs(os.path.join(os.path.abspath(options["tmpdir"]), "PRODIGAL"))
                        os.mkdir(os.path.join(os.path.abspath(options["tmpdir"]), "PFAM"))
                    prod_path = os.path.join(os.path.abspath(options["tmpdir"]), "PRODIGAL")
                    pfam_path = os.path.join(os.path.abspath(options["tmpdir"]), "PFAM")
                else:
                    if os.path.exists(os.path.join(os.path.abspath(options["input_base_path"]), options["tmpdir"])):
                        if os.path.exists(os.path.join(os.path.abspath(options["input_base_path"]), options["tmpdir"],
                                                       "PRODIGAL")):
                            self.stdout.write(
                                self.style.ERROR("Directory PRODIGAL alreade exists in tmp dir. Exiting."))
                            sys.exit(1)
                        elif os.path.exists(
                                os.path.join(os.path.abspath(options["input_base_path"]), options["tmpdir"], "PFAM")):
                            self.stdout.write(
                                self.style.ERROR("Directory PFAM alreade exists in tmp dir. Exiting."))
                            sys.exit(1)
                        else:
                            os.mkdir(os.path.join(os.path.abspath(options["input_base_path"]), options["tmpdir"],
                                                  "PRODIGAL"))
                            os.mkdir(
                                os.path.join(os.path.abspath(options["input_base_path"]), options["tmpdir"], "PFAM"))
                    else:
                        os.makedirs(
                            os.path.join(os.path.abspath(options["input_base_path"]), options["tmpdir"], "PRODIGAL"))
                        os.mkdir(os.path.join(os.path.abspath(options["input_base_path"]), options["tmpdir"], "PFAM"))
                    prod_path = os.path.join(os.path.abspath(options["input_base_path"]), options["tmpdir"], "PRODIGAL")
                    pfam_path = os.path.join(os.path.abspath(options["input_base_path"]), options["tmpdir"], "PFAM")
            else:
                if os.path.exists(os.path.abspath(options["input_base_path"])):
                    if os.path.exists(os.path.join(os.path.abspath(options["input_base_path"]), "PRODIGAL")):
                        self.stdout.write(
                            self.style.ERROR("Directory PRODIGAL alreade exists in input base path. Exiting."))
                        sys.exit(1)
                    elif os.path.exists(os.path.join(os.path.abspath(options["input_base_path"]), "PFAM")):
                        self.stdout.write(
                            self.style.ERROR("Directory PFAM alreade exists in input base path. Exiting."))
                        sys.exit(1)
                    else:
                        os.mkdir(os.path.join(os.path.abspath(options["input_base_path"]), "PRODIGAL"))
                        os.mkdir(os.path.join(os.path.abspath(options["input_base_path"]), "PFAM"))
                        prod_path = os.path.join(os.path.abspath(options["input_base_path"]), "PRODIGAL")
                        pfam_path = os.path.join(os.path.abspath(options["input_base_path"]), "PFAM")
                else:
                    self.stdout.write(
                        self.style.ERROR("Specified input directory does not exist."))
                    sys.exit(1)

            self.stdout.write(self.style.SUCCESS("PRODIGAL output dir created as specified in %s" % (prod_path)))
            self.stdout.write(self.style.SUCCESS("PFAM output dir created as specified in %s" % (pfam_path)))

            self.stdout.write(self.style.WARNING("Starting PRODIGAL..."))
            fasta_files = os.listdir(os.path.abspath(options["input_base_path"]))
            fasta_files = list(filter(lambda x: x.endswith(options["input_suffix"]), fasta_files))
            prodigal_CMD = "%s -f gff" % (settings.PRODIGAL_PATH)
            pfam_CMD = "%s -cpu %i -dir %s" % (settings.PFAMSCAN_PATH, settings.PFAMSCAN_CPUS, settings.PFAM29_DIR)
            "-fasta $FILEBASE.$SGE_TASK_ID -outfile pfam_scan/$FILEBASE.$SGE_TASK_ID.pfam_scan.out"

            self.stdout.write(self.style.WARNING("Executing prodigal..."))
            for fasta_f in fasta_files:
                fasta_f = os.path.join(os.path.abspath(options["input_base_path"]), fasta_f)
                cmd_run = "%s -i %s -a %s -o %s" % (
                prodigal_CMD, fasta_f, os.path.join(prod_path, "%s.faa" % (".".join(fasta_f.split("/")[-1].split(".")[:-1]))),
                os.path.join(prod_path, "%s.gff" % (".".join(fasta_f.split("/")[-1].split(".")[:-1]))))
                print(cmd_run)
                ret_val = subprocess.check_output(cmd_run, shell=True, universal_newlines=True)

            faa_files = os.listdir(prod_path)
            faa_files = list(filter(lambda x: x.endswith(".faa"), faa_files))


            self.stdout.write(self.style.WARNING("Executing pfam_scan..."))
            for faa_f in faa_files:
                faa_f = os.path.join(prod_path, faa_f)
                cmd_run = "%s -fasta %s -outfile %s" % (pfam_CMD, faa_f, os.path.join(pfam_path, "%s.pfams.out" % (".".join(faa_f.split("/")[-1].split(".")[:-1]))))
                print(cmd_run)
                ret_val = subprocess.check_output(cmd_run, shell=True, universal_newlines=True)


            in_path = pfam_path
            in_suffix = ".pfams.out"


        self.stdout.write(self.style.WARNING("Starting classification."))
        self.stdout.write(self.style.WARNING(
           Pipelines.classify_external_genomes_pfam(pfam_base_path=in_path,
                                                    suffix=in_suffix, outfile_path=outfile_path)))
        self.stdout.write(self.style.SUCCESS("Classification succesfully ended."))
