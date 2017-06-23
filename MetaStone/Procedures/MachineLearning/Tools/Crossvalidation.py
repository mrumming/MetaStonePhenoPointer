# coding=utf-8

"""
    Metagenomes -- Crossvalidation.py

    Date:   06/04/2016
    Author: Madis Rumming <mrumming@cebitec.uni-bielefeld.de>
"""

__author__ = "Madis Rumming <mrumming@cebitec.uni-bielefeld.de>"
__copyright__ = "Copyright 2016, Computational Metagenomics, Faculty of Technology, Bielefeld University"

__version__ = "0.0.2"
__maintainer__ = "Madis Rumming"
__email__ = "mrumming@cebitec.uni-bielefeld.de"
__status__ = "Development"

import os
import time

from numpy import mean, std
from pandas import DataFrame
from sklearn import cross_validation
from sklearn import metrics

from MetaStone.Procedures.MachineLearning.Methods import ClassifierModel
from MetaStone.Procedures.MachineLearning.Tools import IO
from MetaStone.Procedures.MachineLearning.Tools import Transformer


def test_all_classifiers(dataframe_path="", dataframe_multilabel_path="", output_filename="classifier_stats.csv",
                         trainset_fraction_fold=3., binary=False, classifier_to_test="", kwargs_to_pass={},
                         completeness=1.):
    """
    Performs cross validation on pre-built dataframes multiclass and/or multilabel and writes as output different scores
    per classifier.

    :param dataframe_path:
    :type dataframe_path: str
    :param dataframe_multilabel_path:
    :type dataframe_multilabel_path: str
    :param output_filename:
    :type output_filename: str
    :param trainset_fraction_fold: If < 1., simple split is performed with no further iterations. >= 1. uses (stratified)KFold approach
    :type trainset_fraction_fold: float
    :return:
    """

    scores_multiclass = {}
    scores_multilabel = {}

    if not classifier_to_test:
        for classifier in ClassifierModel.names():
            if dataframe_path:
                print(classifier)
                scores_ = performcrossvalidation(classifier=classifier, dataframe_path=dataframe_path,
                                                 trainset_fraction_fold=trainset_fraction_fold, binary=binary,
                                                 completeness=completeness)
                if scores_:
                    scores_multiclass[classifier] = scores_
            if dataframe_multilabel_path:
                print(classifier)
                scores_ = performcrossvalidation(classifier=classifier, dataframe_path=dataframe_multilabel_path,
                                                 trainset_fraction_fold=trainset_fraction_fold, multilabel=True,
                                                 binary=binary, completeness=completeness)
                if scores_:
                    scores_multilabel[classifier] = scores_
    else:
        if dataframe_path:
            print("Specified: %s" % (classifier_to_test))
            scores_ = performcrossvalidation(classifier=classifier_to_test, dataframe_path=dataframe_path,
                                             trainset_fraction_fold=trainset_fraction_fold, binary=binary,
                                             kwargs_to_pass=kwargs_to_pass, completeness=completeness)
            if scores_:
                scores_multiclass[classifier_to_test] = scores_
        if dataframe_multilabel_path:
            print("Specified: %s" % (classifier_to_test))
            scores_ = performcrossvalidation(classifier=classifier_to_test, dataframe_path=dataframe_multilabel_path,
                                             trainset_fraction_fold=trainset_fraction_fold, multilabel=True,
                                             binary=binary, kwargs_to_pass=kwargs_to_pass, completeness=completeness)
            if scores_:
                scores_multilabel[classifier_to_test] = scores_

    outfile = open(output_filename, "w")

    snippet = open("snippet", "w")
    snippet.write("dpoints = np.array([\n")

    classifiers_multiclass = []
    scoring_methods_multiclass = []
    classifiers_multilabel = []
    scoring_methods_multilabel = []

    if scores_multiclass:
        classifiers_multiclass = list(scores_multiclass.keys())
        if trainset_fraction_fold >= .1:
            scoring_methods_multiclass = list(scores_multiclass[classifiers_multiclass[0]][0].keys())
    if scores_multilabel:
        classifiers_multilabel = list(scores_multilabel.keys())
        if trainset_fraction_fold >= .1:
            scoring_methods_multilabel = list(scores_multilabel[classifiers_multilabel[0]][0].keys())

    if scores_multiclass:
        mean_values_multiclass = [[] for i in range(len(classifiers_multiclass) * len(scoring_methods_multiclass))]

        outfile.write("sep=\t\n")
        if binary:
            outfile.write(
                "BINARY PROBLEM%s\n" % (len(scoring_methods_multiclass) * len(classifiers_multiclass) * "\t"))
        else:
            outfile.write(
                "MULTICLASS PROBLEM%s\n" % (len(scoring_methods_multiclass) * len(classifiers_multiclass) * "\t"))
        outfile.write(
            "\t%s\n" % (
                "".join(["%s%s" % (s, len(scoring_methods_multiclass) * "\t") for s in classifiers_multiclass])))
        outfile.write("\t%s\n" % ("\t".join(len(classifiers_multiclass) * scoring_methods_multiclass)))
        if trainset_fraction_fold < 1.:
            pass
        else:
            for iteration in range(int(trainset_fraction_fold)):
                counter = 0
                outfile.write("Iteration %i\t" % (iteration))
                l_ = []
                for classifier in classifiers_multiclass:
                    for scoring in scoring_methods_multiclass:
                        l_.append("%.4f" % (scores_multiclass[classifier][iteration][scoring]))
                        mean_values_multiclass[counter].append(scores_multiclass[classifier][iteration][scoring])
                        counter += 1
                outfile.write("%s\n" % ("\t".join(l_)))

        mean_values_ = list(map(lambda x: "%.4f" % (mean(x)), mean_values_multiclass))
        std_values_ = list(map(lambda x: "%.4f" % (std(x)), mean_values_multiclass))
        std_values_snipptet_ = list(map(lambda x: "%.4f" % (std(x) / 2), mean_values_multiclass))

        outfile.write("\nMean\t%s\n" % ("\t".join(mean_values_)))
        outfile.write("STD deviation\t%s\n" % ("\t".join(std_values_)))

        counter = 0
        for classifier in classifiers_multiclass:
            for scoring in scoring_methods_multiclass:
                snippet.write("['%s', '%s', %s, %s],\n" % (
                    classifier, scoring, mean_values_[counter], std_values_snipptet_[counter]))
                counter += 1
        snippet.write("])\n")
        snippet.close()

        # for classifier, testsets in scores_multiclass.items():
        #    outfile.write("%s\n" % (classifier))
        #    if trainset_fraction_fold < 1.:
        #        for testset, summary in testsets.items():
        #            outfile.write("%s\n" % (testset))
        #            outfile.write(summary)
        #    else:
        #        for i, scoring in enumerate(testsets):
        #            outfile.write("Iteration: %i\n" % (i + 1))
        #            for scoring_method, scores in scoring.items():
        #                outfile.write("%s\n" % (scoring_method))
        #                if isinstance(scores, float64):
        #                    outfile.write("%.4f\n" % (scores))
        #                else:
        #                    outfile.write("%s\n" % ("\t".join(["%.4f" % score for score in scores])))
        #                outfile.write("\n")
    if scores_multilabel:
        mean_values_multilabel = [[] for i in range(len(classifiers_multilabel) * len(scoring_methods_multilabel))]

        outfile.write("sep=\t\n")
        outfile.write(
            "MULTILABELCLASS PROBLEM%s\n" % (len(scoring_methods_multilabel) * len(classifiers_multilabel) * "\t"))
        outfile.write(
            "\t%s\n" % (
                "".join(["%s%s" % (s, len(scoring_methods_multilabel) * "\t") for s in classifiers_multilabel])))
        outfile.write("\t%s\n" % ("\t".join(len(classifiers_multilabel) * scoring_methods_multilabel)))
        if trainset_fraction_fold < 1.:
            pass
        else:
            for iteration in range(int(trainset_fraction_fold)):
                counter = 0
                outfile.write("Iteration %i\t" % (iteration))
                l_ = []
                for classifier in classifiers_multilabel:
                    for scoring in scoring_methods_multilabel:
                        l_.append("%.4f" % (scores_multilabel[classifier][iteration][scoring]))
                        mean_values_multilabel[counter].append(scores_multilabel[classifier][iteration][scoring])
                        counter += 1
                outfile.write("%s\n" % ("\t".join(l_)))

        outfile.write("\nMean\t%s\n" % ("\t".join(map(lambda x: "%.4f" % (mean(x)), mean_values_multilabel))))
    # outfile.write("MULTILABEL PROBLEM\n")
    #    for classifier, testsets in scores_multilabel.items():
    #        outfile.write("%s\n" % (classifier))
    #        if trainset_fraction_fold < 1.:
    #            for testset, summary in testsets.items():
    #                outfile.write("%s\n" % (testset))
    #                outfile.write(summary)
    #        else:
    #            for i, scoring in enumerate(testsets):
    #                outfile.write("Iteration: %i\n" % (i + 1))
    #                for scoring_method, scores in scoring.items():
    #                    outfile.write("%s\n" % (scoring_method))
    #                    if isinstance(scores, float64):
    #                        outfile.write("%.4f\n" % (scores))
    #                    else:
    #                        outfile.write("%s\n" % ("\t".join(["%.4f" % score for score in scores])))
    #                    outfile.write("\n")


    outfile.close()


def performcrossvalidation(classifier="rf", characteristic="", subcharacteristic="", seed=1337,
                           trainset_fraction_fold=3.,
                           existence_only=False, dataframe_path="", multilabel=False, binary=False, kwargs_to_pass={},
                           completeness=1.):
    clf = ClassifierModel.create(classifier)
    if multilabel:
        if not clf.supports_multilabel():
            return None

    # Gather training data set
    start_time = time.time()

    if dataframe_path:
        df = IO.special_pickle_load(dataframe_path)
    else:
        t_dict = {}

        df = DataFrame.from_dict(Transformer.genomes_characteristics_to_dict(characteristic, subcharacteristic,
                                                                             existence_only=existence_only),
                                 orient="index")
# REWORK THIS! AUTOMATED PANDAS DATAFRAME GENERTION ALREADY IMPLEMENTED
        if existence_only:
            df.fillna(False, inplace=True)
        else:
            df.fillna(.0, inplace=True)

    # df = Transformer.genomes_characteristics_to_pandas(characteristic, subcharacteristic)

    m, s = divmod(time.time() - start_time, 60)
    h, m = divmod(m, 60)
    print("Elapsed time for gathering data frame: %d:%02d:%02d" % (h, m, s))

    scores_classification = {}

    if trainset_fraction_fold < 1.:
        # TODO: ADD COMPLETENESS
        start_time_ = time.time()
        # Split data set into training and validation data sets
        df_train, df_test = cross_validation.train_test_split(df, train_size=trainset_fraction_fold, random_state=seed)
        m, s = divmod(time.time() - start_time_, 60)
        h, m = divmod(m, 60)
        print("Elapsed time for splitting into train-test set: %d:%02d:%02d" % (h, m, s))

        # Perform cross-validation
        start_time_ = time.time()

        clf.train(df_train, "t_level", kwargs_to_pass)
        m, s = divmod(time.time() - start_time_, 60)
        h, m = divmod(m, 60)
        print("Elapsed time for training: %d:%02d:%02d" % (h, m, s))

        start_time_ = time.time()

        clf.classify(df_test, "t_level")
        clf.classify(df_train, "t_level")

        scores_classification["test_data"] = metrics.classification_report(df_test["t_level"], df_test["t_level_ptag"])
        scores_classification["training_data"] = metrics.classification_report(df_train["t_level"],
                                                                               df_train["t_level_ptag"])

        m, s = divmod(time.time() - start_time_, 60)
        h, m = divmod(m, 60)
        print("Elapsed time for cross validation: %d:%02d:%02d" % (h, m, s))
    else:
        if multilabel:
            start_time_ = time.time()

            scores_classification = clf.cross_validate_stratifiedkfold(df, "t_level", n_folds=trainset_fraction_fold,
                                                                       multilabel=multilabel, binary=binary, completeness=completeness,
                                                                       **kwargs_to_pass)

            m, s = divmod(time.time() - start_time_, 60)
            h, m = divmod(m, 60)
            print("Elapsed time for stratified k-fold cross validation: %d:%02d:%02d" % (h, m, s))
        else:
            start_time_ = time.time()
            scores_classification = clf.cross_validate_stratifiedkfold(df, "t_level", n_folds=trainset_fraction_fold,
                                                                       multilabel=multilabel, binary=binary, completeness=completeness,
                                                                       **kwargs_to_pass)
            m, s = divmod(time.time() - start_time_, 60)
            h, m = divmod(m, 60)
            print("Elapsed time for stratified k-fold cross validation: %d:%02d:%02d" % (h, m, s))

    m, s = divmod(time.time() - start_time, 60)
    h, m = divmod(m, 60)
    print("Elapsed total time: %d:%02d:%02d" % (h, m, s))
    del(clf)
    del(df)

    return scores_classification


def compare_results(search_dir=""):
    files = os.listdir(search_dir)
    files = list(filter(lambda s: s.endswith(".csv"), files))
