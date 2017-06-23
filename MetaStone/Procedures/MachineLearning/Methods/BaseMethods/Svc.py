# coding=utf-8

"""
    Metagenomes -- svc

    Date:   02/05/2016 
    Author: Madis Rumming <mrumming@cebitec.uni-bielefeld.de>
"""

__author__ = "Madis Rumming <mrumming@cebitec.uni-bielefeld.de>"
__copyright__ = "Copyright 2016, Computational Metagenomics, Faculty of Technology, Bielefeld University"

__version__ = "0.0.2"
__maintainer__ = "Madis Rumming"
__email__ = "mrumming@cebitec.uni-bielefeld.de"
__status__ = "Development"

import numpy as np
import pandas
from sklearn import cross_validation
from sklearn import metrics
from sklearn.svm import SVC

import MetaStone.Procedures.MachineLearning.Tools.IO as io
from MetaStone.Procedures.MachineLearning.Methods import ClassifierModel


class Svc(ClassifierModel):
    def __init__(self):
        self.classifier = None
        self.pfams = []

    def train(self, dataframe, metadata_label, *args, **kwargs):
        """ Train model from sets of TPs and FPs

                :param dataframe: data frame with training data (pfams) and metadata to classify
                :type dataframe: pandas.DataFrame
                :param metadata_label: Column label to classify
                :type metadata_label: str
        """
        # dataframe.fillna(.0, inplace=True)

        pfams = list(filter(lambda s: not s.startswith(metadata_label), dataframe.columns))
        metadata_labels = list(filter(lambda s: s.startswith(metadata_label), dataframe.columns))

        if not kwargs:
            kwargs = {"kernel": "rbf"}
        elif not "kernel" in kwargs:
            kwargs["kernel"] = "rbf"

        # self.classifier = AdaBoostClassifier(
        #    base_estimator=RandomForestClassifier(n_jobs=40, n_estimators=100, criterion="entropy"), **kwargs)
        self.classifier = SVC(**kwargs)
        self.classifier.fit(dataframe[pfams].values, dataframe[metadata_label].values)
        self.pfams = pfams

    def classify(self, dataframe, metadata_label, *args, **kwargs):
        """ Classify a set of instances after training

        :param dataframe: data frame with instances.
        :type dataframe: pandas.DataFrame
        :param metadata_label: the feature columns to use
        :type metadata_label: str

        :return: data frame with added column "ptag" which gives the classification
        :rtype: pandas.DataFrame
        """

        # dataframe.fillna(.0, inplace=True)


        preds = self.classifier.predict(dataframe[self.pfams].values)

        dataframe[metadata_label + "_ptag"] = preds

        cprobs = self.classifier.predict_proba(dataframe[self.pfams].values)

        return dataframe

    def can_predict(self):
        return True

    def cross_validate(self, dataframe, metadata_label, *args, **kwargs):

        # dataframe.fillna(.0, inplace=True)


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

        return cross_validation.cross_val_score(self.classifier, dataframe[self.pfams].values,
                                                dataframe[metadata_label].values,
                                                n_jobs=kwargs["n_jobs"], cv=kwargs["cv"], scoring=kwargs["scoring"])

    def cross_validate_stratifiedkfold(self, dataframe, metadata_label, multilabel=False, binary=False, n_folds=3,
                                       completeness=1., **kwargs):

        cross_kwargs = {}
        if not cross_kwargs:
            cross_kwargs = {'n_folds': n_folds, 'shuffle': False, 'random_state': None}
        if not 'n_folds' in cross_kwargs:
            cross_kwargs['n_folds'] = n_folds
        if not 'shuffle' in cross_kwargs:
            cross_kwargs['shuffle'] = False
        if not 'random_state' in cross_kwargs:
            cross_kwargs['random_state'] = None

        # Index: fold# --> Value: {Key: scoring_method, Value: score}
        scores = []

        skf = cross_validation.StratifiedKFold(dataframe[metadata_label].values, **cross_kwargs)

        for i, (train, test) in enumerate(skf):
            score_ = {}
            self.train(dataframe.iloc[train], metadata_label, **kwargs)

            if completeness == 1.:
                print("COMPLETE")
                preds = self.classifier.predict(dataframe.iloc[test][self.pfams].values)
            else:
                print("PARTIAL")
                df_cp = dataframe.iloc[test][self.pfams].values
                for shap in range(df_cp.shape[0]):
                    for choi in np.random.choice(df_cp[shap].nonzero()[0],
                                                 int(np.count_nonzero(df_cp[shap]) * (1 - completeness)),
                                                 replace=False):
                        df_cp[shap][choi] = .0
                preds = self.classifier.predict(df_cp)

            score_["Accuracy"] = metrics.accuracy_score(dataframe.iloc[test][metadata_label].values, preds)
            #if binary:
            #    score_["Precision"] = metrics.precision_score(dataframe.iloc[test][metadata_label].values, preds,
            #                                                  average="binary", pos_label=None)
            #    score_["Recall"] = metrics.recall_score(dataframe.iloc[test][metadata_label].values, preds,
            #                                            average="binary", pos_label=None)
            #    score_["f1"] = metrics.f1_score(dataframe.iloc[test][metadata_label].values, preds, average="binary",
            #                                    pos_label=None)
            #else:
            score_["Precision"] = metrics.precision_score(dataframe.iloc[test][metadata_label].values, preds,
                                                          average="weighted")
            score_["Recall"] = metrics.recall_score(dataframe.iloc[test][metadata_label].values, preds,
                                                    average="weighted")
            score_["f1"] = metrics.f1_score(dataframe.iloc[test][metadata_label].values, preds, average="weighted")
            scores.append(score_)

        return scores

    def save(self, filename):
        """ Save to file """
        if filename.endswith(".json"):
            io.write_classifier_json(self.classifier, filename)
        else:
            io.write_classifier_pickle(self.classifier, filename)

        io.write_classifier_pickle(self.pfams, "features_" + filename)

    def load(self, filename):
        """ Load from file """
        self.classifier = io.read_pickled_classifier(filename)

        self.pfams = io.read_pickled_classifier("features_" + filename)

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


ClassifierModel.register("svc", Svc)
