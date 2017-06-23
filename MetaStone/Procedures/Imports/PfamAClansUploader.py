from MetaStone.Procedures.Imports import UploadModel


class PfamAClansUploader(UploadModel):
    base_identifier = "func_id"

    def __parse_file__(self, filehandle, keys):

        header = ["func_id", "None1", "None2", "func_name_shrt", "func_name_long"]

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
            entries["pfam%s" % (line[base_index][2:])] = entry

        entries = self.__post_process__(entries)

        return entries


UploadModel.register("pfam_clans", PfamAClansUploader)
