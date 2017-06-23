# coding=utf-8

"""
    Metagenomes -- rfcca

    Date:   16/06/2016 
    Author: Madis Rumming <mrumming@cebitec.uni-bielefeld.de>
"""

__author__ = "Madis Rumming <mrumming@cebitec.uni-bielefeld.de>"
__copyright__ = "Copyright 2016, Computational Metagenomics, Faculty of Technology, Bielefeld University"

__version__ = "0.1"
__maintainer__ = "Madis Rumming"
__email__ = "mrumming@cebitec.uni-bielefeld.de"
__status__ = "Development"

import numpy as np
import pandas
from sklearn import cross_validation
from sklearn import metrics
from sklearn import preprocessing
from sklearn.cross_decomposition import CCA
from sklearn.ensemble import RandomForestClassifier

from MetaStone.Procedures.MachineLearning.Methods import ClassifierModel
from MetaStone.Procedures.MachineLearning.Tools import IO


class RFCCA(ClassifierModel):
    def __init__(self):
        self.classifier = None
        self.cca = None
        self.pfams = []
        self.labels = []
        self.label_encoder = None

    def train(self, dataframe, metadata_label, *args, **kwargs):
        """ Train model from sets of TPs and FPs

                :param dataframe: data frame with training data (pfams) and metadata to classify
                :type dataframe: pandas.DataFrame
                :param metadata_label: Column label to classify
                :type metadata_label: str
        """

        self.pfams = list(filter(lambda s: s.startswith("pf"), dataframe.columns))
        self.labels = list(filter(lambda s: not s.startswith("pf"), dataframe.columns))

        if not kwargs:
            kwargs = {"n_jobs": 40,
                      "n_estimators": 200}

        if not "n_estimators" in kwargs:
            kwargs["n_estimators"] = 200

        if not "n_jobs" in kwargs:
            kwargs["n_jobs"] = 40

        if not "criterion" in kwargs:
            kwargs["criterion"] = "entropy"

        to_remove = []
        for key in kwargs.keys():
            if key.startswith("pre_"):
                to_remove.append(key)

        pre_kwargs = {}
        for key in to_remove:
            pre_kwargs[key[4:]] = kwargs.pop(key)




        self.classifier = RandomForestClassifier(**kwargs)
        self.cca = CCA(**pre_kwargs)

        if len(self.labels) == 1:
            print("One label")
            print(self.labels)

            self.label_encoder = preprocessing.LabelEncoder()
            self.label_encoder.fit(dataframe[self.labels].values)

            self.cca.fit(dataframe[self.pfams].values, self.label_encoder.transform(dataframe[self.labels].values))
            self.classifier.fit(self.cca.transform(dataframe[self.pfams].values),
                                self.label_encoder.transform(dataframe[self.labels].values))

        else:
            print("Moere labels")

            print(max(dataframe[self.pfams].values[0]))
            print(min(dataframe[self.pfams].values[0]))

            self.cca.fit(dataframe[self.pfams].values, dataframe[self.labels].values)
            self.classifier.fit(self.cca.transform(dataframe[self.pfams].values), dataframe[self.labels].values)

    def classify(self, dataframe, metadata_label, *args, **kwargs):
        """ Classify a set of instances after training

        :param dataframe: data frame with instances.
        :type dataframe: pandas.DataFrame
        :param metadata_label: the feature columns to use
        :type metadata_label: str

        :return: data frame with added column "ptag" which gives the classification
        :rtype: pandas.DataFrame
        """

        if "n_jobs" in kwargs:
            self.classifier.n_jobs = kwargs["n_jobs"]
        else:
            self.classifier.n_jobs = 40

        # dataframe.fillna(.0, inplace=True)

        preds = self.classifier.predict(self.cca.transform(dataframe[self.pfams].values))

        if len(self.labels) > 1:
            ret_vals = []
            for i in range(len(preds[0])):
                if not preds[0][i] == 0.:
                    ret_vals.append(self.labels[i])
            return "[%s]" % (", ".join(ret_vals))
        else:
            return self.label_encoder.inverse_transform(preds)

    def can_predict(self):
        return True

    def supports_multilabel(self):
        return True

    def cross_validate(self, dataframe, metadata_label, *args, **kwargs):

        # dataframe.fillna(.0, inplace=True)

        pfams = list(dataframe.columns)
        del (pfams[pfams.index(metadata_label)])

        if not kwargs:
            kwargs = {"n_jobs": 40,
                      "cv": 3,
                      "scoring": "accuracy"}
        if not "cv" in kwargs:
            kwargs["cv"] = 3
        if not "n_jobs" in kwargs:
            kwargs["n_jobs"] = 40
        if not "scoring" in kwargs:
            kwargs["scoring"] = "accuracy"

        return cross_validation.cross_val_score(self.classifier, dataframe[pfams].values,
                                                dataframe[metadata_label].values,
                                                n_jobs=kwargs["n_jobs"], cv=kwargs["cv"], scoring=kwargs["scoring"])

    def cross_validate_stratifiedkfold(self, dataframe, metadata_label, multilabel=False, binary=False, n_folds=3., completeness=1.,  **kwargs):
        cross_kwargs = {}
        if not cross_kwargs:
            cross_kwargs = {'n_folds': n_folds, 'shuffle': False, 'random_state': None}
        if not 'n_folds' in cross_kwargs:
            cross_kwargs['n_folds'] = n_folds
        if not 'shuffle' in cross_kwargs:
            cross_kwargs['shuffle'] = False
        if not 'random_state' in cross_kwargs:
            cross_kwargs['random_state'] = None

        # kwargs['random_state'] = 1371
        # Index: fold# --> Value: {Key: scoring_method, Value: score}
        scores = []

        if multilabel:
            skf = cross_validation.KFold(dataframe.shape[0], **cross_kwargs)
        else:
            skf = cross_validation.StratifiedKFold(dataframe[metadata_label].values, **cross_kwargs)

        for i, (train, test) in enumerate(skf):
            score_ = {}
            self.train(dataframe.iloc[train], metadata_label)
            if multilabel:
                preds = self.classifier.predict(self.cca.transform(dataframe.iloc[test][self.pfams].values))
            else:
                preds = self.classify(dataframe.iloc[test], metadata_label)

            if multilabel:
                score_["Accuracy"] = metrics.accuracy_score(dataframe.iloc[test][self.labels].values, preds)

                score_["AUPRC"] = metrics.average_precision_score(dataframe.iloc[test][self.labels].values, preds,
                                                                  "samples")
                score_["ROC AUC"] = metrics.roc_auc_score(dataframe.iloc[test][self.labels].values, preds,
                                                          "samples")
                score_["Precision"] = metrics.precision_score(dataframe.iloc[test][self.labels].values, preds,
                                                              average="samples")
                score_["Recall"] = metrics.recall_score(dataframe.iloc[test][self.labels].values, preds,
                                                        average="samples")
                score_["f1"] = metrics.f1_score(dataframe.iloc[test][self.labels].values, preds,
                                                average="samples")
            else:
                score_["Accuracy"] = metrics.accuracy_score(dataframe.iloc[test][metadata_label].values, preds)
                #if binary:
                #    score_["Precision"] = metrics.precision_score(dataframe.iloc[test][metadata_label].values, preds,
                #                                                  average="binary", pos_label=None)
                #    score_["Recall"] = metrics.recall_score(dataframe.iloc[test][metadata_label].values, preds,
                #                                            average="binary", pos_label=None)
                #    score_["f1"] = metrics.f1_score(dataframe.iloc[test][metadata_label].values, preds,
                #                                    average="binary", pos_label=None)
                #else:
                score_["Precision"] = metrics.precision_score(dataframe.iloc[test][metadata_label].values, preds,
                                                              average="weighted")
                score_["Recall"] = metrics.recall_score(dataframe.iloc[test][metadata_label].values, preds,
                                                        average="weighted")
                score_["f1"] = metrics.f1_score(dataframe.iloc[test][metadata_label].values, preds,
                                                average="weighted")
            scores.append(score_)

        return scores

    def save(self, filename):
        """ Save to file """
        if filename.endswith(".json"):
            IO.write_classifier_pickle(self.classifier, filename[:-4] + ".pkld")
            IO.write_classifier_pickle(self.cca, filename[:-4] + ".pkld.pca")
        else:
            IO.write_classifier_pickle(self.classifier, filename)
            IO.write_classifier_pickle(self.cca, filename + ".pca")

    def load(self, filename):
        """ Load from file """
        self.classifier = IO.read_pickled_classifier(filename)
        self.cca = IO.read_pickled_classifier(filename + ".pca")

    def plots(self, prefix, featurenames):
        """ Make diagnostic plots """
        importances = self.classifier.feature_importances_
        std = np.std([tree.feature_importances_ for tree in self.classifier.estimators_],
                     axis=0)
        indices = np.argsort(importances)[::-1]

        # Print the feature ranking
        print("Feature ranking:")

        for f in range(0, len(indices)):
            print("%d. feature %d:%s (%f +- %f)" % (f + 1, indices[f],
                                                    featurenames[indices[f]],
                                                    importances[indices[f]],
                                                    std[indices[f]]))


ClassifierModel.register("rfcca", RFCCA)
