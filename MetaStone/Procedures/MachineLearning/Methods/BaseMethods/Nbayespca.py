# coding=utf-8

"""
	Metagenomes -- nbayespca

	Date:   07/04/2016
	Author: Madis Rumming <mrumming@cebitec.uni-bielefeld.de>
"""

__author__ = "Madis Rumming <mrumming@cebitec.uni-bielefeld.de>"
__copyright__ = "Copyright 2016, Computational Metagenomics, Faculty of Technology, Bielefeld University"

__version__ = "0.0.2"
__maintainer__ = "Madis Rumming"
__email__ = "mrumming@cebitec.uni-bielefeld.de"
__status__ = "Development"

# coding=utf-8

import pandas
from sklearn import cross_validation
from sklearn.decomposition import PCA
from sklearn.naive_bayes import GaussianNB

from MetaStone.Procedures.MachineLearning.Methods import ClassifierModel
from MetaStone.Procedures.MachineLearning.Tools import IO


class NBGaussianPCA(ClassifierModel):
    def __init__(self):
        self.classifier = None
        self.pca = None

    def train(self, dataframe, metadata_label, *args, **kwargs):
        """ Train model from sets of TPs and FPs

                :param dataframe: data frame with training data (pfams) and metadata to classify
                :type dataframe: pandas.DataFrame
                :param metadata_label: Column label to classify
                :type metadata_label: str
        """
        # dataframe.fillna(.0, inplace=True)

        pfams = list(dataframe.columns)
        del (pfams[pfams.index(metadata_label)])

        to_remove = []
        for key in kwargs.keys():
            if key.startswith("pre_"):
                to_remove.append(key)

        pre_kwargs = {}
        for key in to_remove:
            pre_kwargs[key[4:]] = kwargs.pop(key)

        self.classifier = GaussianNB()
        self.pca = PCA(**pre_kwargs)

        self.classifier.fit(self.pca.fit_transform(dataframe[pfams].values), dataframe[metadata_label].values)

    def classify(self, dataframe, metadata_label, *args, **kwargs):
        """ Classify a set of instances after training

        :param dataframe: data frame with instances.
        :type dataframe: pandas.DataFrame
        :param metadata_label: the feature columns to use
        :type metadata_label: str

        :return: data frame with added column "ptag" which gives the classification
        :rtype: pandas.DataFrame
        """

        # if "n_jobs" in kwargs:
        #    self.classifier.n_jobs = kwargs["n_jobs"]
        # else:
        #    self.classifier.n_jobs = 40

        # dataframe.fillna(.0, inplace=True)

        pfams = list(dataframe.columns)
        if metadata_label in pfams:
            del (pfams[pfams.index(metadata_label)])

        ivals = self.pca.transform(dataframe[pfams].values)
        preds = self.classifier.predict(ivals)

        dataframe[metadata_label + "_ptag"] = preds

        cprobs = self.classifier.predict_proba(dataframe[pfams].values)
        # tpcol = np.where(self.classifier.classes_ == "TP")[0][0]
        # instances["qual"] = cprobs[:, tpcol]

        return dataframe

    def can_predict(self):
        return True

    def cross_validate(self, dataframe, metadata_label, *args, **kwargs):

        # dataframe.fillna(.0, inplace=True)

        pfams = list(dataframe.columns)
        del (pfams[pfams.index(metadata_label)])

        if not kwargs:
            kwargs = {"cv": 3,
                      "scoring": "accuracy"}
        if not "cv" in kwargs:
            kwargs["cv"] = 3
        if not "scoring" in kwargs:
            kwargs["scoring"] = "accuracy"

        return cross_validation.cross_val_score(self.classifier, dataframe[pfams].values,
                                                dataframe[metadata_label].values, cv=kwargs["cv"],
                                                scoring=kwargs["scoring"])

    def save(self, filename):
        """ Save to file """
        if filename.endswith(".json"):
            IO.write_classifier_pickle(self.classifier, filename[:-4] + ".pkld")
        else:
            IO.write_classifier_pickle(self.classifier, filename)

    def load(self, filename):
        """ Load from file """
        self.classifier = IO.read_pickled_classifier(filename)

    def plots(self, prefix, featurenames):
        """ Make diagnostic plots
        importances = self.clf.feature_importances_
        std = np.std([tree.feature_importances_ for tree in self.clf.estimators_],
                      axis=0)
        indices = np.argsort(importances)[::-1]

        # Print the feature ranking
        print "Feature ranking:"

        for f in xrange(0, len(indices)):
            print "%d. feature %d:%s (%f +- %f)" % (f + 1, indices[f],
                                                    featurenames[indices[f]],
                                                    importances[indices[f]],
                                                    std[indices[f]])"""
        pass


ClassifierModel.register("nbayespca", NBGaussianPCA)
