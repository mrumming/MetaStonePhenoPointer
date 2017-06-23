# coding=utf-8

"""
    Metagenomes -- Pipelines

    Date:   30/05/2016 
    Author: Madis Rumming <mrumming@cebitec.uni-bielefeld.de>
"""

__author__ = "Madis Rumming <mrumming@cebitec.uni-bielefeld.de>"
__copyright__ = "Copyright 2016, Computational Metagenomics, Faculty of Technology, Bielefeld University"

__version__ = "0.1"
__maintainer__ = "Madis Rumming"
__email__ = "mrumming@cebitec.uni-bielefeld.de"
__status__ = "Development"

import configparser
import copy
import os
import matplotlib.pyplot as plt
import itertools
import numpy as np
from collections import namedtuple


from MetaStone.EnumFields.DatabaseModels.Internal import DbModelMapping
from MetaStone.Procedures.MachineLearning.Methods import ClassifierModel
from MetaStone.Procedures.MachineLearning.Tools import Crossvalidation
from MetaStone.Procedures.MachineLearning.Tools import IO
from MetaStone.Procedures.MachineLearning.Tools import Transformer
from MetaStone.models import InferredSpeciesRelatedCharacteristics, SpeciesRelatedCharacteristics, Genome, Pfam2Genome
from sklearn import metrics
from pandas import DataFrame



def classify_external_genomes_pfam(pfam_base_path="", suffix=".pfams.out", outfile_path=""):
    classifiers = {}
    classifiers["Biotic Relationships"] = "classifiers/biotic_relationships.pck.gz"
    classifiers["Cell Arrangement"] = "classifiers/cell_arrangement.pck.gz"
    classifiers["Cell Shape"] = "classifiers/cell_shape.pck.gz"
    classifiers["Diseases"] = "classifiers/diseases.pck.gz"
    classifiers["Energy Source"] = "classifiers/energy_source.pck.gz"
    classifiers["Gram Staining"] = "classifiers/gram_staining.pck.gz"
    classifiers["Metabolism"] = "classifiers/metabolism.pck.gz"
    classifiers["Motility"] = "classifiers/motility.pck.gz"
    classifiers["Oxygen Requirement"] = "classifiers/oxygen_requirement.pck.gz"
    classifiers["Phenotype"] = "classifiers/phenotype.pck.gz"
    classifiers["Salinity"] = "classifiers/salinity.pck.gz"
    classifiers["Sporulation"] = "classifiers/sporulation.pck.gz"
    classifiers["Temperature Range"] = "classifiers/temperature_range.pck.gz"

    pfam_files = os.listdir(pfam_base_path)
    pfam_files = list(filter(lambda s: s.endswith(suffix), pfam_files))

    to_classify = {}



    for pfam_file in pfam_files:
        to_classify[pfam_file] = Transformer.pfamout_to_dict(inputpath=os.path.join(pfam_base_path, pfam_file))

    predictions = {}

    for model_key in classifiers.keys():
        print(model_key)
        clf = IO.special_pickle_load(classifiers[model_key])
        predictions[model_key] = {}
        for genome_key in to_classify.keys():
            df = to_classify[genome_key]

            for pf in clf.pfams:
                if not pf in df:
                    df[pf] = .0

            multilabel = (len(clf.labels) > 1)

            if multilabel:
                preds = clf.classifier.predict(df[clf.pfams].values)
                cur_pred_as_labels = []
                for j in range(len(clf.labels)):
                    if preds[0][j]:
                        cur_pred_as_labels.append(clf.labels[j].split("_")[-1])
                predictions[model_key][genome_key] = ", ".join(cur_pred_as_labels)
            else:
                predictions[model_key][genome_key] = clf.classify(df, "t_level")[0]

    outfile = open(outfile_path, "w")

    for genome_key in to_classify.keys():
        outfile.write("Organism identifier:\t%s\n" % (genome_key))
        for model_key in classifiers.keys():
            outfile.write("%s\t%s\n" % (model_key, predictions[model_key][genome_key]))
        outfile.write("\t\n\t\n")

    outfile.close()

    return("Outputfile written as %s." % (outfile_path))



def _parse_classifier_ini_(ini_file=""):
    """
    Parses ini-File, performs checks for designated file paths, classifier params and defined dependencies.

    :param ini_file: Path to ini-style setup file
    :type ini_file: str
    :return: Mapping of parsed setup file
    :rtype: namedtuple
    """
    return_object = namedtuple("classifier_setup", ["cp", "classifiers", "classifier_names", "dataframe_packages"])

    if not os.path.exists(os.path.abspath(ini_file)):
        return "Path for ini-file %s does not exist." % (ini_file)

    cp = configparser.ConfigParser()
    cp.optionxform = str
    with open(ini_file) as fp:
        cp.read_file(fp)

    if not cp.has_section("setup"):
        return "Missing section %s" % ("setup")

    if not cp.has_option("setup", "classifier"):
        return "Missing option %s in section %s" % ("classification", "setup")

    classifiers = {k: [] for k in cp.get("setup", "classifier").split(",")}

    errors = []
    for classifier in classifiers.keys():
        if not cp.has_section(classifier):
            errors.append(classifier)
    if errors:
        return "Missing sections: %s" % (",".join(errors))

    classifier_names = {}

    for classifier in classifiers.keys():
        if not cp.has_option(classifier, "name"):
            return "Missing option %s in section %s." % ("name", classifier)
        else:
            if not cp.get(classifier, "name") in ClassifierModel.names():
                return "Unknown classifier %s in section %s." % (cp.get(classifier, "name"), classifier)
            else:
                classifier_names[classifier] = cp.get(classifier, "name")

    if not os.path.exists(os.path.join(os.path.abspath("."), cp.get("setup", "dataframe_base_dir"))):
        return "Specified dataframe base dir %s does not exist." % (cp.get("setup", "dataframe_base_dir"))

    dataframe_packages = {k: [] for k in cp.get("setup", "dataframe_package").split(",")}

    for dataframe_package in dataframe_packages.keys():
        if not cp.has_section(dataframe_package):
            errors.append("Missing section %s" % (dataframe_package))
    if errors:
        return "\n".join(errors)

    for dataframe_package in dataframe_packages.keys():
        if not os.path.exists(
                os.path.join(os.path.abspath("."), cp.get("setup", "dataframe_base_dir"),
                             cp.get(dataframe_package, "subdir"))):
            errors.append("Specified dataframe package '%s' under base dir %s does not exist." % (
                cp.get(dataframe_package, "subdir"), cp.get("setup", "dataframe_base_dir")))
        if not cp.has_option(dataframe_package, "dataframes"):
            errors.append("Missing option %s in section %s." % ("dataframes", dataframe_package))
        else:
            for dataframe in cp.get(dataframe_package, "dataframes").split(","):
                if not os.path.exists(
                        os.path.join(os.path.abspath("."), cp.get("setup", "dataframe_base_dir"),
                                     cp.get(dataframe_package, "subdir"),
                                     "%s%s" % (dataframe, cp.get("setup", "dataframe_suffix")))):
                    errors.append("Speciefied dataframe %s%s under package %s in %s does not exist." % (
                        dataframe, cp.get("setup", "dataframe_suffix"), cp.get(dataframe_package, "subdir"),
                        cp.get("setup", "dataframe_base_dir")))
                else:
                    dataframe_packages[dataframe_package].append(dataframe)

    if errors:
        return "\n".join(errors)

    for classifier in classifiers.keys():
        kwargs = []
        kwargs_base = {}
        options_dict = {}
        start_option = ""
        for option in cp.options(classifier):
            if not (option.endswith("_type") or option == "name"):
                if "," in cp.get(classifier, option):
                    l_ = []
                    for entry in cp.get(classifier, option).split(","):
                        if cp.get(classifier, "%s_type" % (option)) == "int":
                            l_.append(int(entry))
                        elif cp.get(classifier, "%s_type" % (option)) == "float":
                            l_.append(float(entry))
                        elif cp.get(classifier, "%s_type" % (option)) == "bool":
                            if entry.lower() == "true":
                                l_.append(True)
                            else:
                                l_.append(False)
                        else:
                            l_.append(entry)
                    options_dict[option] = l_
                else:
                    if cp.get(classifier, "%s_type" % (option)) == "int":
                        kwargs_base[option] = int(cp.get(classifier, option))
                    elif cp.get(classifier, "%s_type" % (option)) == "float":
                        kwargs_base[option] = float(cp.get(classifier, option))
                    elif cp.get(classifier, "%s_type" % (option)) == "bool":
                        kwargs_base[option] = cp.getboolean(classifier, option)
                    else:
                        kwargs_base[option] = cp.get(classifier, option)
        kwargs.append(kwargs_base)

        for option in options_dict.keys():
            kwargs_ = []
            for entry in options_dict[option]:
                for partial_kwargs in kwargs:
                    worker_dict = copy.deepcopy(partial_kwargs)
                    worker_dict[option] = entry
                    kwargs_.append(worker_dict)
            kwargs = kwargs_
        classifiers[classifier] = kwargs

    return return_object(cp, classifiers, classifier_names, dataframe_packages)


def infer_genomes_from_db():
    """


    :param ini_file: Path to setup file
    :type ini_file: str
    :param store_into_db: Indicates whether to store the predicted values to the RDBMS or not
    :type store_into_db: bool
    """
    classifiers = {}
    #classifiers["Biotic Relationships"] = "classifiers/biotic_relationships.pck.gz"
    classifiers["Cell Arrangement"] = "classifiers/cell_arrangement.pck.gz"
    classifiers["Cell Shape"] = "classifiers/cell_shape.pck.gz"
    classifiers["Diseases"] = "classifiers/diseases.pck.gz"
    #classifiers["Energy Source"] = "classifiers/energy_source.pck.gz"
    #classifiers["Gram Staining"] = "classifiers/gram_staining.pck.gz"
    #classifiers["Metabolism"] = "classifiers/metabolism.pck.gz"
    #classifiers["Motility"] = "classifiers/motility.pck.gz"
    #classifiers["Oxygen Requirement"] = "classifiers/oxygen_requirement.pck.gz"
    classifiers["Phenotype"] = "classifiers/phenotype.pck.gz"
    classifiers["Salinity"] = "classifiers/salinity.pck.gz"
    #classifiers["Sporulation"] = "classifiers/sporulation.pck.gz"
    #classifiers["Temperature Range"] = "classifiers/temperature_range.pck.gz"

    multi = ["Phenotype", "Metabolism", "Diseases", "Energy Source", "Cell Arrangement"]



    pfams = Pfam2Genome.objects.all()
    t_dict = {}

    print("dicting")
    for pfam in pfams:
        # Fill in features --> PFAMS
        t_ = {}
        t_dict[pfam.genome.taxon_oid] =  {k: float(v) for k, v in pfam.pfams.items()}
        t_dict[pfam.genome.taxon_oid]["t_level"] = ""
    print("pre")
    t_dict = DataFrame.from_dict(t_dict, orient="index").fillna(.0).drop("taxon_oid", axis=1)
    print("post")
        # Fill in label --> THING TO PREDICT/TRAIN ON
        #if multilabel_style:
        #    ttt = ttt.split(",")
        #    for ttt_ in ttt:
        #        ttt_ = ttt_.strip()
        #        while "  " in ttt_:
        #            ttt_ = ttt_.replace("  ", " ")
        #        ttt_.replace(" ", "_")
        #        t_dict[pfam.genome.taxon_oid]["t_level_%s" % (ttt_)] = True
        #        t_level_labels.add("t_level_%s" % (ttt_))
        #else:
        #    t_dict[pfam.genome.taxon_oid]["t_level"] = ttt


    for category in classifiers.keys():
        clf = IO.special_pickle_load(classifiers[category])
        for genome in Genome.objects.all():
            try:
                dbobj = InferredSpeciesRelatedCharacteristics.objects.get(pk=genome.taxon_oid)
                if eval("SpeciesRelatedCharacteristics.objects.get(pk=%s).%s" % (genome.taxon_oid, InferredSpeciesRelatedCharacteristics.img_name[category])):
                    setattr(dbobj, dbobj.img_name[category], eval("SpeciesRelatedCharacteristics.objects.get(pk=%s).%s" % (genome.taxon_oid, InferredSpeciesRelatedCharacteristics.img_name[category])))
                    dbobj.save()
                else:
                    try:
                        for pf in clf.pfams:
                            if not pf in t_dict:
                                t_dict[pf] = .0

                        if category in multi:
                            preds = clf.classifier.predict(t_dict.loc[genome.taxon_oid][clf.pfams].values)
                            cur_pred_as_labels = []
                            for j in range(len(clf.labels)):
                                if preds[0][j]:
                                    cur_pred_as_labels.append(clf.labels[j].split("_")[-1])
                            pred = ", ".join(sorted(cur_pred_as_labels))
                        else:
                            pred = clf.classify(t_dict.loc[genome.taxon_oid], "t_level")[0]

                        setattr(dbobj, dbobj.img_name[category], pred)
                    except:
                        pass
                    dbobj.save()
            except:
                dbobj = InferredSpeciesRelatedCharacteristics.create(genome.taxon_oid)
                if eval("SpeciesRelatedCharacteristics.objects.get(pk=%s).%s" % (genome.taxon_oid, InferredSpeciesRelatedCharacteristics.img_name[category])):
                    setattr(dbobj, dbobj.img_name[category],
                            eval("SpeciesRelatedCharacteristics.objects.get(pk=%s).%s" % (genome.taxon_oid, InferredSpeciesRelatedCharacteristics.img_name[category])))
                    dbobj.save()
                else:
                    try:
                        for pf in clf.pfams:
                            if not pf in t_dict:
                                t_dict[pf] = .0

                        if category in multi:
                            preds = clf.classifier.predict(t_dict.loc[genome.taxon_oid][clf.pfams].values)
                            cur_pred_as_labels = []
                            for j in range(len(clf.labels)):
                                if preds[0][j]:
                                    cur_pred_as_labels.append(clf.labels[j].split("_")[-1])
                            pred = ", ".join(sorted(cur_pred_as_labels))
                        else:
                            pred = clf.classify(t_dict.loc[genome.taxon_oid], "t_level")[0]

                        setattr(dbobj, dbobj.img_name[category], pred)
                    except:
                        pass
                    dbobj.save()


    return("Done")


def xcross(ini_file="", logging=None):
    """
    Performs cross-validation of different machine learners based an k-fold stratified cross-validation with different
    parameters on different input data sets.

    :param ini_file: Path to setup file with dataframes, classifiers and parameters to crossvalidate
    :type ini_file: str
    :param logging: Path to file containing log entries. If not desired, the set to None
    :type logging: str
    :return:
    """
    classifier_setup = _parse_classifier_ini_(ini_file=ini_file)

    # If any error occured, return detailed description as str, otherwise proceed.
    if isinstance(classifier_setup, str):
        return classifier_setup

    if logging:
        logging_file = open(logging, "w")

    for classifier, kwargs_list in classifier_setup.classifiers.items():
        for kwargs in kwargs_list:
            for dataframe_package, dataframes in classifier_setup.dataframe_packages.items():
                for dataframe in dataframes:
                    for completeness in classifier_setup.cp.get("setup", "completeness", fallback="100").split(","):
                        completeness = float(completeness) / 100.
                       # try:
                        if classifier_setup.cp.get(dataframe_package, "type") == "multilabel":
                            Crossvalidation.test_all_classifiers(
                                dataframe_multilabel_path=os.path.join(os.path.abspath("."),
                                                                       classifier_setup.cp.get("setup",
                                                                                               "dataframe_base_dir"),
                                                                       classifier_setup.cp.get(dataframe_package,
                                                                                               "subdir"),
                                                                       "%s%s" % (dataframe,
                                                                                 classifier_setup.cp.get(
                                                                                     "setup",
                                                                                     "dataframe_suffix"))),
                                output_filename="classifierstats_%s_%s_%s.%i.csv" % (
                                    dataframe, classifier_setup.classifier_names[classifier], "_".join(
                                        ["%s-%s" % (k, v) for k, v in kwargs.items()]), int(completeness * 100.)),
                                trainset_fraction_fold=float(
                                    classifier_setup.cp.get("setup", "classifier_kfold")), binary=False,
                                classifier_to_test=classifier_setup.classifier_names[classifier],
                                kwargs_to_pass=kwargs, completeness=completeness)
                        elif classifier_setup.cp.get(dataframe_package, "type") == "binary":
                            Crossvalidation.test_all_classifiers(
                                dataframe_path=os.path.join(os.path.abspath("."),
                                                            classifier_setup.cp.get("setup", "dataframe_base_dir"),
                                                            classifier_setup.cp.get(dataframe_package, "subdir"),
                                                            "%s%s" % (dataframe, classifier_setup.cp.get("setup",
                                                                                                         "dataframe_suffix"))),
                                output_filename="classifierstats_%s_%s_%s.%i.csv" % (
                                    dataframe, classifier_setup.classifier_names[classifier], "_".join(
                                        ["%s-%s" % (k, v) for k, v in kwargs.items()]), int(completeness * 100.)),
                                trainset_fraction_fold=float(classifier_setup.cp.get("setup", "classifier_kfold")),
                                binary=True,
                                classifier_to_test=classifier_setup.classifier_names[classifier],
                                kwargs_to_pass=kwargs, completeness=completeness)
                        else:
                            Crossvalidation.test_all_classifiers(
                                dataframe_path=os.path.join(os.path.abspath("."),
                                                            classifier_setup.cp.get("setup", "dataframe_base_dir"),
                                                            classifier_setup.cp.get(dataframe_package, "subdir"),
                                                            "%s%s" % (dataframe, classifier_setup.cp.get("setup",
                                                                                                         "dataframe_suffix"))),
                                output_filename="classifierstats_%s_%s_%s.%i.csv" % (
                                    dataframe, classifier_setup.classifier_names[classifier], "_".join(
                                        ["%s-%s" % (k, v) for k, v in kwargs.items()]), int(completeness * 100.)),
                                trainset_fraction_fold=float(classifier_setup.cp.get("setup", "classifier_kfold")),
                                binary=False,
                                classifier_to_test=classifier_setup.classifier_names[classifier],
                                kwargs_to_pass=kwargs, completeness=completeness)
                                ##TODO: AENDERN
                        #except:
                        #    if logging:
                        #        logging_file.write("Error occured for %s-typed dataframe %s.\n" % (
                        #            classifier_setup.cp.get(dataframe_package, "type"), dataframe))
                        #        logging_file.write("Classifier: %s\n" % (classifier_setup.classifier_names[classifier]))
                        #        logging_file.write("Genome completeness: %i"\n % (int(completeness * 100.)))
                        #        logging_file.write(
                        #            "Params: %s\n" % ("; ".join(["%s-%s" % (k, v) for k, v in kwargs.items()])))
                        #    else:
                        #        print("Error occured for %s-typed dataframe %s, completeness: %i." % (
                        #            classifier_setup.cp.get(dataframe_package, "type"), dataframe,
                        #            int(completeness * 100.)))

    if logging:
        logging_file.close()

    return ("Everyhing fine.")


def trainfinalmodel(ini_file, out_path):
    """
    Train final classification model for given INI configuration and serialize object as gzipp'ed pickle.
    :param ini_file: Path to input INI
    :type ini_file: str
    :param out_path: Filename to pickle as
    :type out_path: str
    :return: Statusstring
    """
    classifier_setup = _parse_classifier_ini_(ini_file=ini_file)

    # If any error occured, return detailed description as str, otherwise proceed.
    if isinstance(classifier_setup, str):
        return classifier_setup

    for classifier, kwargs_list in classifier_setup.classifiers.items():
        for kwargs in kwargs_list:
            for dataframe_package, dataframes in classifier_setup.dataframe_packages.items():
                for dataframe in dataframes:
                    clf = ClassifierModel.create(classifier_setup.classifier_names[classifier])

                    df = IO.special_pickle_load(os.path.join(os.path.abspath("."),
                                                             classifier_setup.cp.get("setup", "dataframe_base_dir"),
                                                             classifier_setup.cp.get(dataframe_package, "subdir"),
                                                             "%s%s" % (dataframe, classifier_setup.cp.get("setup",
                                                                                                          "dataframe_suffix"))))
                    clf.train(df, "t_level", **kwargs)

                    IO.special_pickle_dump(clf, out_path, as_gzip=True)

    return ("Everything fine!")


def validatemodel(modeltotest_path, validation_df_path, scores_path):
    """
    Validate a pre-trained classification model against a validation set
    :param modeltotest_path: Path to model to load
    :type modeltotest_path: str
    :param validation_df_path: Path to validation data frame to load
    :type validation_df_path: str
    :param scores_path: Filename of scoring statistics output file
    :type scores_path: str
    :return: 
    """
    clf = IO.special_pickle_load(modeltotest_path)
    df = IO.special_pickle_load(validation_df_path)

    # check for missing pfams and add these with .0 as values
    pfams = clf.pfams
    for pf in pfams:
        if not pf in df:
            df[pf] = .0

    multilabel = (len(clf.labels) > 1)

    if multilabel:
        preds = clf.classifier.predict(df[clf.pfams].values)
    else:
        preds = clf.classify(df, "t_level")

    scores = {}

    for tl in clf.labels:
        if not tl in df:
            df[tl] = False

    if multilabel:
        scores["Accuracy"] = metrics.accuracy_score(df[clf.labels].values, preds)

        # scores["AUPRC"] = metrics.average_precision_score(df[clf.labels].values, preds,
        #                                                 "samples")
        # scores["ROC AUC"] = metrics.roc_auc_score(df[clf.labels].values, preds,
        #                                        "samples")
        scores["Precision"] = metrics.precision_score(df[clf.labels].values, preds,
                                                      average="samples")
        scores["Recall"] = metrics.recall_score(df[clf.labels].values, preds,
                                                average="samples")
        scores["f1"] = metrics.f1_score(df[clf.labels].values, preds,
                                        average="samples")


        pred_dict = {}
        for i in range(len(preds)):
            given = []
            predicted = []
            for j in range(len(clf.labels)):
                if df[clf.labels[j]].iloc[i]:
                    given.append(clf.labels[j])
                if preds[i][j]:
                    predicted.append(clf.labels[j])
            #print("%s --> %s" % (", ".join(given), ", ".join(predicted)))

            given = ", ".join(given).replace("t_level_", "")
            predicted = "}, \\textcolor{red}{".join(predicted).replace("t_level_", "")

            if given in pred_dict:
                if predicted in pred_dict[given]:
                    pred_dict[given][predicted] += 1
                else:
                    pred_dict[given][predicted] = 1
            else:
                pred_dict[given] = {predicted: 1}

        for key in pred_dict.keys():
            for skey in pred_dict[key].keys():
                print("\\item[%i %s] %s}" % (pred_dict[key][skey], key, skey))

    else:
        scores["Accuracy"] = metrics.accuracy_score(df[clf.labels].values, preds)
        scores["Precision"] = metrics.precision_score(df[clf.labels].values, preds,
                                                      average="weighted")
        scores["Recall"] = metrics.recall_score(df[clf.labels].values, preds,
                                                average="weighted")
        scores["f1"] = metrics.f1_score(df[clf.labels].values, preds,
                                        average="weighted")

        l_ =  set([x[0] for x in df[clf.labels].values.tolist()]      )
        l_.union(set([x[0] for x in preds.tolist()]      ))
        cnf = metrics.confusion_matrix(df[clf.labels].values, preds, labels=list(l_))



        def plot_confusion_matrix(cm, classes,
                                  normalize=False,
                                  title='Confusion matrix',
                                  cmap=plt.cm.Blues):
            """
            This function prints and plots the confusion matrix.
            Normalization can be applied by setting `normalize=True`.
            """
            plt.imshow(cm, interpolation='nearest', cmap=cmap)
            plt.title(title)
            plt.colorbar()
            tick_marks = np.arange(len(classes))
            plt.xticks(tick_marks, classes, rotation=90)
            plt.yticks(tick_marks, classes)

            if normalize:
                cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
                print("Normalized confusion matrix")
            else:
                print('Confusion matrix, without normalization')

            print(cm)

            thresh = cm.max() / 2.
            for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
                plt.text(j, i, cm[i, j],
                         horizontalalignment="center",
                         color="white" if cm[i, j] > thresh else "black")

            plt.tight_layout()
            plt.ylabel('True label')
            plt.xlabel('Predicted label')

        # Compute confusion matrix
        np.set_printoptions(precision=2)

        # Plot non-normalized confusion matrix
        plt.figure()
        plot_confusion_matrix(cnf, classes=l_,
                              title='Confusion matrix, without normalization')

        # Plot normalized confusion matrix
        #plt.figure()
        #plot_confusion_matrix(cnf, classes=l_, normalize=True,
        #                      title='Normalized confusion matrix')

        plt.show()


    # print(preds)
    # print(df["t_level"])
    print(scores)

    return ()


def select_best_classifier_from_stats(search_dir="", is_single_dir=False, output_filename="summary.csv"):
    if not os.path.exists(os.path.abspath(search_dir)):
        return "Designated search dir %s does not exist." % (search_dir)

    if is_single_dir:
        dirs = [os.path.abspath(search_dir)]
    else:
        # Check every input whether it is a single directory and contains some files
        dirs = os.listdir(os.path.abspath(search_dir))
        dirs = list(filter(lambda s: os.path.isdir(os.path.join(os.path.abspath(search_dir), s)), dirs))
        dirs = [os.path.join(os.path.abspath(search_dir), s) for s in dirs]
        dirs = list(filter(lambda s: not len(os.listdir(s)) == 0, dirs))

    per_dataframe_score = {}

    dataframe_scores_total = {}
    scores__ = []
    for subdir in dirs:

        files = os.listdir(os.path.abspath(subdir))
        # Filter for parsable csv files
        files = list(filter(lambda s: s.endswith(".csv"), files))

        # dataframe = files[0][files[0].index("_") + 1:files[0].index("_", files[0].index("both"))]
        classifier = files[0][files[0].index("_", files[0].index("both")) + 1: files[0].index("_", files[0].index("_",
                                                                                                                  files[
                                                                                                                      0].index(
                                                                                                                      "both")) + 1)]
        # search_index = files[0][files[0].index("_", files[0].index("_", files[0].index("both"))+1)]+1

        infile = open(os.path.join(subdir, files[0]))

        infile.readline()
        infile.readline()
        infile.readline()

        scores_ = infile.readline()
        scores_ = scores_.strip().split("\t")
        scores__ = scores_

        dataframe_scores = {}

        infile.close()

        for file_ in files:
            infile = open(os.path.join(subdir, file_))

            infile.readline()
            infile.readline()
            infile.readline()

            header = infile.readline()
            header = header.strip().split("\t")

            dataframe = file_[file_.index("_") + 1:file_.index("_", file_.index("both"))]

            for line in infile:
                if line.startswith("Mean"):
                    line = line.strip().split("\t")
                    if dataframe in dataframe_scores:
                        for entry in scores_:
                            if float(line[header.index(entry) + 1]) >= dataframe_scores[dataframe][entry][0]:
                                if float(line[header.index(entry) + 1]) == dataframe_scores[dataframe][entry][0]:
                                    dataframe_scores[dataframe][entry][1].append(file_)
                                else:
                                    dataframe_scores[dataframe][entry][0] = float(line[header.index(entry) + 1])
                                    dataframe_scores[dataframe][entry][1] = [file_]
                    else:
                        scores = {k: [0., []] for k in scores_}
                        for entry in scores_:
                            if float(line[header.index(entry) + 1]) >= scores[entry][0]:
                                if float(line[header.index(entry) + 1]) == scores[entry][0]:
                                    scores[entry][0] = float(line[header.index(entry) + 1])
                                    scores[entry][1].append(file_)
                        dataframe_scores[dataframe] = scores

                    if dataframe in per_dataframe_score:
                        for entry in scores_:
                            if float(line[header.index(entry) + 1]) >= per_dataframe_score[dataframe][entry][0]:
                                if float(line[header.index(entry) + 1]) == per_dataframe_score[dataframe][entry][0]:
                                    per_dataframe_score[dataframe][entry][1].append(file_)
                                else:
                                    per_dataframe_score[dataframe][entry][0] = float(line[header.index(entry) + 1])
                                    per_dataframe_score[dataframe][entry][1] = [file_]
                    else:
                        scores = {k: [0., []] for k in scores_}
                        for entry in scores_:
                            scores[entry][0] = float(line[header.index(entry) + 1])
                            scores[entry][1] = [file_]
                        per_dataframe_score[dataframe] = scores

                    break
            infile.close()
        dataframe_scores_total[classifier] = dataframe_scores

    outfile = open(os.path.join(os.path.abspath(search_dir), output_filename), "w")
    outfile.write("sep=\t\n")

    for classifier_ in dataframe_scores_total.keys():
        outfile.write("Classififier: %s\n" % (classifier_))
        for dataframe in dataframe_scores_total[classifier_].keys():
            outfile.write("%s\n" % (dataframe))
            outfile.write("%s\n" % ("\t".join(scores__)))
            outfile.write(
                "%s\n" % ("\t".join([str(dataframe_scores_total[classifier_][dataframe][s][0]) for s in scores__])))
            outfile.write("%s\n" % (
                "\t".join([", ".join(dataframe_scores_total[classifier_][dataframe][s][1]) for s in scores__])))
        outfile.write("\n")

    outfile.close()

    outfile = open(os.path.join(os.path.abspath(search_dir), "dataframes_%s" % (output_filename)), "w")
    outfile.write("sep=\t\n")

    # Select best setup per dataframe
    for dataframe in per_dataframe_score.keys():
        outfile.write("%s\n" % (dataframe))
        outfile.write("%s\n" % ("\t".join(scores__)))
        outfile.write("%s\n" % ("\t".join([str(per_dataframe_score[dataframe][s][0]) for s in scores__])))
        outfile.write("%s\n" % ("\t".join([", ".join(per_dataframe_score[dataframe][s][1]) for s in scores__])))
        start_set = set(per_dataframe_score[dataframe][scores__[0]][1])
        for s in scores__[1:]:
            start_set = start_set.intersection(set(per_dataframe_score[dataframe][s][1]))
        if start_set:
            outfile.write("Best classifiers with params:\n")
            outfile.write("%s\n" % ("\n".join(start_set)))
            print("%s: %s\n" % (dataframe, ", ".join(start_set)))
        else:
            outfile.write("None best found.\n")
            print("%s: None best found." % (dataframe))
        outfile.write("\n\n")
    outfile.close()
