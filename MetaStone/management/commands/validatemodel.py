# coding=utf-8

"""
    Metagenomes -- validatemodel

    Date:   18/05/2017 
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
    help = "Trains a final model based on an INI configuration file."

    def add_arguments(self, parser):
        parser.add_argument("model_path", type=str)
        parser.add_argument("validation_df", type=str)
        parser.add_argument("output_path", type=str)

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Starting Validation."))
        self.stdout.write(self.style.WARNING(Pipelines.validatemodel(modeltotest_path=options["model_path"], validation_df_path=options["validation_df"], scores_path=options["output_path"])))
        self.stdout.write(self.style.SUCCESS("Validation ended."))