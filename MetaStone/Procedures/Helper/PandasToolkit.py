import numpy
from pandas import SparseSeries, SparseDataFrame


def biom_to_pandas(biom_otu):
    """
    Convert data from biom to SparseDataFrame (pandas) for easy access
    :param biom_otu: Table
    :rtype: DataFrame
    """
    tmp_m = biom_otu.matrix_data
    df = [SparseSeries(tmp_m[i].toarray().ravel()) for i in numpy.arange(tmp_m.shape[0])]
    return (SparseDataFrame(df, index=biom_otu.ids('observation'), columns=biom_otu.ids('sample')).to_dense())
