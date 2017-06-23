# coding=utf-8

"""
    Metagenomes -- infermissingannotationsindb

    Date:   31/05/2017 
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



    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Starting Training."))
        self.stdout.write(self.style.WARNING(Pipelines.infer_genomes_from_db()))
        self.stdout.write(self.style.SUCCESS("Training ended."))