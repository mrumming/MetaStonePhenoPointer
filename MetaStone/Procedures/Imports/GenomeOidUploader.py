from MetaStone.Procedures.Imports import UploadModel
from MetaStone.models import Genome


class GenomeOIDUploader(UploadModel):
    base_identifier = "taxon_oid"

    #Need for distinction of pgenus and pspecies
    def __post_process__(selfs, entries):

        test_it = next(iter(entries.values()))
        if not "Genus" in test_it or not "Species" in test_it:
            return entries

        for entry in entries.keys():
            if entries[entry]["Species"].startswith(entries[entry]["Genus"]):
                entries[entry]["Species"] = entries[entry]["Species"].replace("%s " % (entries[entry]["Genus"]), "")

        # Initiate mock genome for undetermined genomes during metadata enrichment of communty profiles.
        if not Genome.objects.filter(taxon_oid=0).exists():
            g = Genome.create(0)
            g.taxon_name = "Undetermined"
            g.save()

        return entries

UploadModel.register("genome_oid", GenomeOIDUploader)
