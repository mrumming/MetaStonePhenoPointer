# coding=utf-8

"""
    Metagenomes -- KNeighbors

    Date:   05/07/2016 
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
from sklearn.neighbors import KNeighborsClassifier

import MetaStone.Procedures.MachineLearning.Tools.IO as io
from MetaStone.Procedures.MachineLearning.Methods import ClassifierModel


class KN(ClassifierModel):
    def __init__(self):
        self.classifier = None
        self.pfams = []
        self.labels = []

    def train(self, dataframe, metadata_label, *args, **kwargs):
        """ Train model from sets of TPs and FPs

                :param dataframe: data frame with training data (pfams) and metadata to classify
                :type dataframe: pandas.DataFrame
                :param metadata_label: Column label to classify
                :type metadata_label: str
        """
        # dataframe.fillna(.0, inplace=True)

        self.pfams = list(filter(lambda s: not s.startswith(metadata_label), dataframe.columns))
        self.labels = list(filter(lambda s: s.startswith(metadata_label), dataframe.columns))

        if not kwargs:
            kwargs = {"n_jobs": 40,
                      "n_neighbors": 5,
                      "algorithm": "auto",
                      "leaf_size": 30}

        if not "n_jobs" in kwargs:
            kwargs["n_jobs"] = 40

        if not "n_neighbors" in kwargs:
            kwargs["n_neighbors"] = 5

        if not "algorithm" in kwargs:
            kwargs["algorithm"] = "auto"

        if not "leaf_size" in kwargs:
            kwargs["leaf_size"] = 30

        self.classifier = KNeighborsClassifier(**kwargs)
        if len(self.labels) == 1:
            print("One label")
            print(self.labels)
            self.classifier.fit(dataframe[self.pfams].values, dataframe[metadata_label].values)

        else:
            print("Moere labels")
            self.classifier.fit(dataframe[self.pfams].values, dataframe[self.labels].values)

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

        # metadata_labels = list(filter(lambda s: s.startswith(metadata_label), dataframe.columns))

        preds = self.classifier.predict(dataframe[self.pfams].values)

        if len(self.labels) > 1:
            ret_vals = []
            for i in range(len(preds)):
                if not preds[i][i] == 0.:
                    ret_vals.append(self.labels[i])
            return "[%s]" % (", ".join(ret_vals))
        else:
            return preds

            # TODO: REWORK
            # dataframe[metadata_label + "_ptag"] = preds

            # cprobs = self.classifier.predict_proba(dataframe[self.pfams].values)
            # tpcol = np.where(self.classifier.classes_ == "TP")[0][0]
            # instances["qual"] = cprobs[:, tpcol]

    def can_predict(self):
        return True

    def supports_multilabel(self):
        return True

    def cross_validate(self, dataframe, metadata_label, *args, **kwargs):

        # dataframe.fillna(.0, inplace=True)


        if not kwargs:
            kwargs = {"n_jobs": 40,
                      "cv": 3,
                      "scoring": "accuracy",
                      "seed": 1337}
        if not "cv" in kwargs:
            kwargs["cv"] = 3
        if not "n_jobs" in kwargs:
            kwargs["n_jobs"] = 40
        if not "scoring" in kwargs:
            kwargs["scoring"] = "accuracy"
        if not "seed" in kwargs:
            kwargs["seed"] = 1337

        return cross_validation.cross_val_score(self.classifier, dataframe[self.pfams].values,
                                                dataframe[metadata_label].values,
                                                **kwargs)

    def cross_validate_stratifiedkfold(self, dataframe, metadata_label, multilabel=False, binary=False, n_folds=3.,
                                       completeness=1.,
                                       **kwargs):

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

        if multilabel:
            skf = cross_validation.KFold(dataframe.shape[0], **cross_kwargs)
        else:
            skf = cross_validation.StratifiedKFold(dataframe[metadata_label].values, **cross_kwargs)

        for i, (train, test) in enumerate(skf):
            score_ = {}
            self.train(dataframe.iloc[train], metadata_label, **kwargs)

            if completeness == 1.:
                print("COMPLETE")
                preds = self.classifier.predict(dataframe.iloc[test][self.pfams].values)
            elif completeness < 1.:
                print("PARTIAL")
                df_cp = dataframe.iloc[test][self.pfams].values
                for shap in range(df_cp.shape[0]):
                    try:
                        for choi in np.random.choice(df_cp[shap].nonzero()[0],
                                                     int(np.count_nonzero(df_cp[shap]) * (1 - completeness)),
                                                     replace=False):
                            df_cp[shap][choi] = .0
                    except:
                        pass
                preds = self.classifier.predict(df_cp)
            else:
                print("CONTAMINATED")
                df_cp = dataframe.iloc[test][self.pfams].values
                for shap in range(df_cp.shape[0]):
                    try:
                        for choi in np.random.choice([x for x in range(df_cp.shape[1])],
                                                     int(df_cp.shape[1] * (completeness - 1)),
                                                     replace=False):

                            df_cp[shap][choi] = float(np.random.randint(1,11))
                    except:
                        pass  # DO NOTHING INTENTIONALLY! :)
                preds = self.classifier.predict(df_cp)

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
                # if binary:
                #    score_["Precision"] = metrics.precision_score(dataframe.iloc[test][metadata_label].values, preds,
                #                                                  average="binary", pos_label=None)
                #    score_["Recall"] = metrics.recall_score(dataframe.iloc[test][metadata_label].values, preds,
                #                                            average="binary", pos_label=None)
                #    score_["f1"] = metrics.f1_score(dataframe.iloc[test][metadata_label].values, preds,
                #                                    average="binary", pos_label=None)
                # else:
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


ClassifierModel.register("kn", KN)
