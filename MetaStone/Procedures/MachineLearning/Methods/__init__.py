# coding=utf-8

"""
	Metagenomes -- __injt__.py

	Date:   06/04/2016
	Author: Madis Rumming <mrumming@cebitec.uni-bielefeld.de>
"""

__author__ = "Madis Rumming <mrumming@cebitec.uni-bielefeld.de>"
__copyright__ = "Copyright 2016, Computational Metagenomics, Faculty of Technology, Bielefeld University"

__version__ = "0.0.2"
__maintainer__ = "Madis Rumming"
__email__ = "mrumming@cebitec.uni-bielefeld.de"
__status__ = "Development"

import abc


class ClassifierModel(object, metaclass=abc.ABCMeta):
    """ Base class for Ensemble models for training and classification """

    @abc.abstractclassmethod
    def train(self, dataframe, metadata_label, *args, **kwargs):
        """ Train model from sets of TPs and FPs

                :param dataframe: data frame with training data (pfams) and metadata to classify
                :type dataframe: pandas.DataFrame
                :param metadata_label: Column label to classify
                :type metadata_label: str
        """
        pass

    @abc.abstractmethod
    def classify(self, dataframe, metadata_label, *args, **kwargs):
        """ Classify a set of instances after training

        :param dataframe: data frame with instances.
        :type dataframe: pandas.DataFrame
        :param metadata_label: the feature columns to use
        :type metadata_label: str

        :return: data frame with added column "ptag" which gives the classification
        :rtype: pandas.DataFrame
        """
        return dataframe

    def can_predict(self):
        """ Override to enable prediction (means classify will return ptag and qual columns)
        """
        return False

    def supports_multilabel(self):
        """
        Override to enable multilabel training, classification and cross validation.
        :return: Multilabel support or not as boolean value
        :rtype: bool
        """
        return False

    @abc.abstractclassmethod
    def cross_validate(self, dataframe, metadata_label, *args, **kwargs):
        """
        Performs cross validation on the input data against the trained model.
        Returns an array of scores dependent on 'cv', specifying the number
        of folds of the StratifiedKFold (target variable is binary or multiclass),
        otherwise number of folds in KFold.
        """
        pass

    @abc.abstractclassmethod
    def cross_validate_stratifiedkfold(self, dataframe, metadata_label, multilabel, binary, n_folds, completeness, **kwargs):
        """

        :param kwargs: Supported are: 'n_folds' for specifying the folds
        :return:
        """
        pass

    @abc.abstractmethod
    def save(self, filename):
        """ Save to file """
        pass

    @abc.abstractmethod
    def load(self, filename):
        """ Load from file """
        pass

    @abc.abstractmethod
    def plots(self, prefix, featurenames):
        """ Make diagnostic plots (optional)
        """
        pass

    # model factory
    _models = {}

    @classmethod
    def register(cls, mname, mclass):
        cls._models[mname] = mclass

    @classmethod
    def create(cls, mname):
        """
        :rtype: ClassifierModel
        """
        return cls._models[mname]()

    @classmethod
    def names(cls):
        return cls._models.keys()

from MetaStone.Procedures.MachineLearning.Methods.BaseMethods import KNeighbors
from MetaStone.Procedures.MachineLearning.Methods.BaseMethods import Decisiontree
from MetaStone.Procedures.MachineLearning.Methods.BaseMethods import Nbayes
from MetaStone.Procedures.MachineLearning.Methods.BaseMethods import Nbayesmultinomial
from MetaStone.Procedures.MachineLearning.Methods.BaseMethods import Nbayespca
from MetaStone.Procedures.MachineLearning.Methods.BaseMethods import Svc
from MetaStone.Procedures.MachineLearning.Methods.EnsembleMethods import Adaboost
from MetaStone.Procedures.MachineLearning.Methods.EnsembleMethods import Gbc
from MetaStone.Procedures.MachineLearning.Methods.EnsembleMethods import Rf
from MetaStone.Procedures.MachineLearning.Methods.EnsembleMethods import Rfcca
from MetaStone.Procedures.MachineLearning.Methods.EnsembleMethods import Rfpca
