# coding=utf-8

"""
	Metagenomes -- IO.py

	Date:   06/04/2016
	Author: Madis Rumming <mrumming@cebitec.uni-bielefeld.de>
"""

__author__ = "Madis Rumming <mrumming@cebitec.uni-bielefeld.de>"
__copyright__ = "Copyright 2016, Computational Metagenomics, Faculty of Technology, Bielefeld University"

__version__ = "0.0.2"
__maintainer__ = "Madis Rumming"
__email__ = "mrumming@cebitec.uni-bielefeld.de"
__status__ = "Development"

import json
import pickle
import gzip
import os

def dict_for_tree(tree):
    """ Make dictionary for tree """
    tree_dict = {}
    for i in range(tree.node_count):
        tree_dict[i] = [int(tree.children_left[i]), int(tree.children_right[i])]
    node_features = tree.feature
    node_thresholds = tree.threshold
    node_count = tree.node_count

    decision_dict = {}
    for i in range(node_count):
        if tree_dict[i][0] == -1:
            node_features[i] = -1
            node_thresholds[i] = -1

        decision_dict[i] = [int(node_features[i]), float(node_thresholds[i])]
    node_values = tree.value

    node_values = node_values.tolist()
    node_values = [i[0] for i in node_values]
    node_values_dict = {}
    for i in range(len(node_values)):
        node_values_dict[i] = node_values[i]
    all_data = {'tree': tree_dict, 'decisions': decision_dict, 'node_votes': node_values_dict}
    return all_data


def read_pickled_classifier(pickle_fn):
    """ Read classifier from pickle file """
    with open(pickle_fn, 'rb') as fid:
        classifier = pickle.load(fid)
    return classifier


def write_classifier_pickle(classifier, pickle_fn):
    """ store classifier in pickle file """
    with open(pickle_fn, 'wb') as fid:
        pickle.dump(classifier, fid)




"""
Due to a bug in OSX (known since 2011 and before) in fwrite and fread, this work-around circumvents it by limiting the
amount of data being wrote to the filesystem.
"""
def special_pickle_load(filepath):
    max_bytes = 2**31-1
    bytes_in = bytearray(0)
    in_size = os.path.getsize(filepath)
    if filepath.endswith(".gz"):
        with gzip.open(filepath, "rb") as infile:
            b_read = infile.read(max_bytes)
            while b_read:
                bytes_in += b_read
                b_read = infile.read(max_bytes)
    else:
        with open(filepath, "rb") as infile:
            for _ in range(0, in_size, max_bytes):
                bytes_in += infile.read(max_bytes)

    return pickle.loads(bytes_in)

def special_pickle_dump(obj, filepath, as_gzip=True):
    max_bytes = 2**31-1
    bytes_out = pickle.dumps(obj)
    if as_gzip:
        with gzip.open(filepath, "wb") as outfile:
            for i in range(0, len(bytes_out), max_bytes):
                outfile.write(bytes_out[i:i+max_bytes])
    else:
        with open(filepath, "wb") as outfile:
            for i in range(0, len(bytes_out), max_bytes):
                outfile.write(bytes_out[i:i+max_bytes])
