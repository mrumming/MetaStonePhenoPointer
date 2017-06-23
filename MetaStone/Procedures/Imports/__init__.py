import abc
import gzip
import os

from django.db import transaction


class UploadModel(object, metaclass=abc.ABCMeta):
    delim = "\t"

    def __init__(self, filepath, dbobject):
        self.filepath = filepath
        self.dbobject = dbobject

    def __post_process__(selfs, entries):
        return entries

    def __parse_file__(self, filehandle, keys):

        header = filehandle.readline()
        header = header.strip().split(self.delim)

        base_index = header.index(self.base_identifier)

        ind_ = {}
        for key in keys:
            if not key in header:
                print("Possible renaming of %s" % (key))
            ind_[header.index(key)] = key

        entries = {}
        for line in filehandle:
            line = line.strip().split(self.delim)
            entry = {}
            for i in ind_.keys():
                entry[ind_[i]] = line[i]
            entries[line[base_index]] = entry

        entries = self.__post_process__(entries)

        return entries

    @transaction.atomic
    def process(self):
        if not os.path.exists(self.filepath):
            raise IOError("%s could be found on server." % (self.filepath))
        else:
            if self.filepath.endswith(".gz"):
                infile = gzip.open(os.path.abspath(self.filepath), 'rt')
            else:
                infile = open(os.path.abspath(self.filepath))
            try:
                entries = self.__parse_file__(infile, self.dbobject.img_name.keys())
            except ValueError:
                infile.seek(0)
                entries = self.__parse_file__(infile, self.dbobject.alt_img_name.keys())
                self.dbobject.img_name = self.dbobject.alt_img_name
            infile.close()

        ind = 0
        for entry in entries.keys():
            if ind % 250 == 0:
                print("%i more to go..." % (len(entries) - ind))
            ind += 1

            dbobj = self.dbobject.create(entry)
            if dbobj:
                for key in dbobj.img_name.keys():
                    setattr(dbobj, dbobj.img_name[key],
                            entries[entry][key].translate(str.maketrans({"'": "\\'", '"': '\\"'})))
                dbobj.save()

    ######
    # model factory -> See bottom of this for members
    ###
    #
    #
    _models = {}

    #
    @classmethod
    def register(cls, mname, mclass):
        cls._models[mname] = mclass

    #
    @classmethod
    def create(cls, mname, filepath, dbobj):
        """
        :argument filepath: Path to input file
        :rtype: UploadModel
        """
        # noinspection PyCallingNonCallable
        return cls._models[mname](filepath, dbobj)

    #
    @classmethod
    def names(cls):
        return list(cls._models.keys())
        #
        ######


######
# self-registration of implementing class into factory through register()-call after import
###
#
#
from MetaStone.Procedures.Imports import GenomeOidUploader
from MetaStone.Procedures.Imports import PfamToGenomeUploader
from MetaStone.Procedures.Imports import BiomImporter
from MetaStone.Procedures.Imports import PfamAClansUploader
#
######
