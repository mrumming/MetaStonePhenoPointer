import gzip
import os

from django.db import transaction

from MetaStone.Procedures.Imports import UploadModel


class PfamToGenomeUploader(UploadModel):
    base_identifier = "taxon_oid"

    def __parse_file__(self, filehandle):
        header = filehandle.readline()
        header = header.strip().split(self.delim)

        base_index = header.index(self.base_identifier)

        ind_ = {}
        for i in range(len(header[1:])):
            ind_[i] = header[i]

        entries = {}
        for line in filehandle:
            line = line.strip().split(self.delim)
            entry = {}
            for i in ind_.keys():
                if not line[i].strip() == "0":
                    entry[ind_[i]] = line[i].strip()
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

            entries = self.__parse_file__(infile)
            infile.close()

        ind = 0
        for entry in entries.keys():
            if ind % 250 == 0:
                print("%i more to go..." % (len(entries) - ind))
            ind += 1

            dbobj = self.dbobject.create(entry)
            if dbobj:
                dbobj.pfams = entries[entry]
                dbobj.save()


UploadModel.register("pfam_to_genome", PfamToGenomeUploader)
