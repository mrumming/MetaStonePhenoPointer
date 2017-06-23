# coding=utf-8

"""
    Metagenomes -- Transformer.py

        This class contains methods and data structures for conversion from django models to numpy forth and back for
    ML-purposes.

    Date:   06/04/2016
    Author: Madis Rumming <mrumming@cebitec.uni-bielefeld.de>
"""

__author__ = "Madis Rumming <mrumming@cebitec.uni-bielefeld.de>"
__copyright__ = "Copyright 2016, Computational Metagenomics, Faculty of Technology, Bielefeld University"

__version__ = "0.1"
__maintainer__ = "Madis Rumming"
__email__ = "mrumming@cebitec.uni-bielefeld.de"
__status__ = "Development"

import os

from pandas import DataFrame

from MetaStone.Procedures.MachineLearning.Methods import ClassifierModel
from MetaStone.Procedures.MachineLearning.Tools import IO
from MetaStone.models import Pfam


def classify_single_genome(df_trainingpath="", to_classify=None, classifier="rf", ):
    clf = ClassifierModel.create(classifier)

    df_train = IO.special_pickle_load(df_trainingpath)

    clf.train(df_train, "t_level")

    if isinstance(to_classify, DataFrame):
        print(clf.classify(to_classify, "nope"))
    else:
        for key in to_classify.keys():
            print("%s - %s" % (key, clf.classify(to_classify[key], "nope")))


def pfamout_to_dict(inputpath="", existence_only=False, ret_as_dict=False, org_name="NONE_SPECIFIED"):
    if not os.path.exists(os.path.abspath(inputpath)):
        return None

    infile = open(os.path.abspath(inputpath))
    pfams = Pfam.objects.all()
    t_dict = {}

    for pfam in pfams:
        if existence_only:
            t_dict[pfam.func_id] = False
        else:
            t_dict[pfam.func_id] = 0

    for line in infile:
        if not line.startswith("#"):
            break

    for line in infile:
        line = line.strip()
        if "PF" in line:
            line = line[line.index("PF") + 2:line.index("PF") + 7]
            line = "pfam%s" % (line)
            if line in t_dict:
                if existence_only:
                    t_dict[line] = True
                else:
                    t_dict[line] += 1.

    infile.close()

    if ret_as_dict:
        return {org_name: t_dict}
    else:
        return DataFrame.from_dict({org_name: t_dict}, orient="index")


###
# DO NOT APPEND TO MUCH DATA FRAMES! NOT PERFORMANT!
###
def genomes_characteristics_to_dict(dbobj, table_field, existence_only=False, lineage="both", ret_as_dict=False,
                                    multilabel_style=False, nonempty_only=True):
    """

    :param dbobj:
    :type dbobj: str
    :param table_field:
    :type table_field: str
    :param existence_only:
    :type existence_only: bool
    :param lineage:
    :type lineage: str
    :param ret_as_dict:
    :type ret_as_dict: bool
    :return:
    :rtype: dict
    """

    if nonempty_only:
        if lineage == "both":
            pfams = eval(
                'Pfam2Genome.objects.exclude(genome__%s__%s="").exclude(genome__%s__%s="Undefined").exclude(genome__%s__%s="undefined").exclude(genome__%s__%s__isnull=True)' % (
                    dbobj.lower(), table_field.lower(), dbobj.lower(), table_field.lower(), dbobj.lower(),
                    table_field.lower(), dbobj.lower(), table_field.lower()))
        elif lineage == "bacteria":
            pfams = eval(
                'Pfam2Genome.objects.exclude(genome__%s__%s="").exclude(genome__%s__%s="Undefined").exclude(genome__%s__%s="undefined").exclude(genome__%s__%s__isnull=True).exclude(genome__genomelineage__pdomain="Archaea")' % (
                    dbobj.lower(), table_field.lower(), dbobj.lower(), table_field.lower(), dbobj.lower(),
                    table_field.lower(), dbobj.lower(), table_field.lower()))
        else:
            pfams = eval(
                'Pfam2Genome.objects.exclude(genome__%s__%s="").exclude(genome__%s__%s="Undefined").exclude(genome__%s__%s="undefined").exclude(genome__%s__%s__isnull=True).exclude(genome__genomelineage__pdomain="Bacteria")' % (
                    dbobj.lower(), table_field.lower(), dbobj.lower(), table_field.lower(), dbobj.lower(),
                    table_field.lower(), dbobj.lower(), table_field.lower()))
    else:
        if lineage == "both":
            pfams = eval('Pfam2Genome.objects.filter(genome__%s__%s="")' % (dbobj.lower(), table_field.lower()))
        elif lineage == "bacteria":
            pfams = eval(
                'Pfam2Genome.objects.filter(genome__%s__%s="").exclude(genome__genomelineage__pdomain="Archaea")' % (
                    dbobj.lower(),
                    table_field.lower()))
        else:
            pfams = eval(
                'Pfam2Genome.objects.filter(genome__%s__%s="").exclude(genome__genomelineage__pdomain="Bacteria")' % (
                    dbobj.lower(),
                    table_field.lower()))

    t_dict = {}

    t_level_labels = set()

    for pfam in pfams:
        # Fill in features --> PFAMS
        if existence_only:
            t_dict[pfam.genome.taxon_oid] = {}
            for key in pfam.pfams.keys():
                t_dict[pfam.genome.taxon_oid][key] = True
        else:
            t_dict[pfam.genome.taxon_oid] = {k: float(v) for k, v in pfam.pfams.items()}

        # Fill in label --> THING TO PREDICT/TRAIN ON
        ttt = eval('%s.objects.get(pk=pfam.genome).%s' % (dbobj, table_field))
        if multilabel_style:
            ttt = ttt.split(",")
            for ttt_ in ttt:
                ttt_ = ttt_.strip()
                while "  " in ttt_:
                    ttt_ = ttt_.replace("  ", " ")
                ttt_.replace(" ", "_")
                t_dict[pfam.genome.taxon_oid]["t_level_%s" % (ttt_)] = True
                t_level_labels.add("t_level_%s" % (ttt_))
        else:
            t_dict[pfam.genome.taxon_oid]["t_level"] = ttt

    if ret_as_dict:
        return t_dict
    else:
        if multilabel_style:
            df = DataFrame.from_dict(t_dict, orient="index")
            df.fillna(value={t_level_label: False for t_level_label in t_level_labels}, inplace=True)
            df.fillna(.0, inplace=True)
            return df.drop("taxon_oid", axis=1)
        elif existence_only:
            return DataFrame.from_dict(t_dict, orient="index").fillna(False).drop("taxon_oid", axis=1)
        else:
            return DataFrame.from_dict(t_dict, orient="index").fillna(.0).drop("taxon_oid", axis=1)
