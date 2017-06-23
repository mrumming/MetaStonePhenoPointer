# coding=utf-8

"""
    Metagenomes -- pandas.py

    Date:   21/04/2017 
    Author: Madis Rumming <mrumming@cebitec.uni-bielefeld.de>
"""

__author__ = "Madis Rumming <mrumming@cebitec.uni-bielefeld.de>"
__copyright__ = "Copyright 2017, Computational Metagenomics, Faculty of Technology, Bielefeld University"

__version__ = "0.1"
__maintainer__ = "Madis Rumming"
__email__ = "mrumming@cebitec.uni-bielefeld.de"
__status__ = "Development"

import gzip
import pickle

from django.core.management.base import BaseCommand

from MetaStone.Procedures.MachineLearning.Tools import Transformer


class Command(BaseCommand):
    help = "Exports genome related metadata to a file as pickled gzip."

    def add_arguments(self, parser):
        parser.add_argument("outfile_name", type=str, help="Name of the output file, will be extended with '.pck.gz'")
        parser.add_argument("dbmodel", type=str, help="Data base model to get the data from")
        parser.add_argument("table_field", type=str, help="Model field to export")
        parser.add_argument("existence_only", type=bool,
                            help="Set to True, if no exact abundance of pfams is desired, but only True/False.")
        parser.add_argument("lineage", type=str, help="Valid values: bacteria, archaea, both")
        parser.add_argument("multilabel_style", type=bool,
                            help="Set to True, if the underlying is not binary or multiclass")
        parser.add_argument("nonempty_only", type=bool,
                            help="Set to True for exporting entities, where the desired table field contains data.")

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Starting export as pandas pickle.gzip."))

        df = Transformer.genomes_characteristics_to_dict(options["dbmodel"], options["table_field"],
                                                         existence_only=options["existence_only"],
                                                         lineage=options["lineage"], ret_as_dict=False,
                                                         multilabel_style=options["multilabel_style"],
                                                         nonempty_only=options["nonempty_only"])
        outfile = gzip.open("%s.pck.gz" % (options["outfile_name"]), "wb")
        pickle.dump(df, outfile)
        outfile.close()

        self.stdout.write(self.style.SUCCESS("Good bye!"))
