# coding=utf-8

"""
    Metagenomes -- xcross.py

    Date:   03/04/2017 
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


class Command(BaseCommand):
    help = "Execute crossvalidation with given setup-ini file and optional logging file."

    def add_arguments(self, parser):
        parser.add_argument("ini_path", nargs=1, type=str)
        parser.add_argument("logging_path", type=str, default="xcross.log")

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Starting XCROSS."))
        self.stdout.write(self.style.WARNING(Pipelines.xcross(ini_file=options["ini_path"][0], logging=options["logging_path"])))
        self.stdout.write(self.style.SUCCESS("Successfully ended, output files are written unless log file is not empty."))