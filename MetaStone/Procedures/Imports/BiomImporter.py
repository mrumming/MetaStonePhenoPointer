import os

import biom
from django.db import transaction

from MetaStone.Procedures.Helper import DbToolkit, PandasToolkit
from MetaStone.Procedures.Imports import UploadModel
from MetaStone.models import User_Metagenome_Sample
from MetaStone.models import User_Metagenome_Sample_Genome
from MetaStone.models import Genome


class BiomImporter(UploadModel):
    def __process_sample__(self, u_sample, sample_id, b_, df, observations):

        """

        :param u_sample: User_Metagenome_Sample -- sample model to work on
        :param sample_id: str -- sample ID
        :param b_: biom.table.Table -- embedded data and metadata
        :param df: SpareseDataFrame from pandas -- counts per OTU and sample
        """

        # TESTING:: COUNTS ONLY

        # sum_hits = 0
        # total = 0
        # for observation in b_.ids('observation'):
        #     sum_hits += DbToolkit.match_str_to_genome_name(True, "none", "",
        #                                                    *b_.metadata(observation, 'observation')['taxonomy'])
        #     total += 1
        #
        # print("Sample: %s with %i of %i possible hits." % (sample_id, sum_hits, total))
        #
        # pass

        for observation in observations.keys():
            if df[sample_id][observation] > .0:
                u_sample_genome = User_Metagenome_Sample_Genome(metagenome_sample=u_sample,
                                                                abundance=df[sample_id][observation],
                                                                genome=observations[observation][0])
                u_sample_genome.save()

    @transaction.atomic
    def process(self):
        # start_time = time.time()
        if not os.path.exists(self.filepath):
            raise IOError("%s could be found on server." % (self.filepath))
        else:
            b_ = biom.load_table(self.filepath)
            samples = {}
            for b_key in b_.ids():
                ums = User_Metagenome_Sample(metagenome=self.dbobject, sample_name=b_key)
                ums.save()
                samples[b_key] = ums

        df = PandasToolkit.biom_to_pandas(b_)
        ###
        # UNCOMMENT IF FINISHED
        ###
        obs_to_genome = {}
        for observation in b_.ids('observation'):
            dbhit = DbToolkit.match_str_to_genome_name(True, "none", "",
                                                       *b_.metadata(observation, 'observation')['taxonomy'])
            if dbhit:
                obs_to_genome[observation] = dbhit
            else:
                obs_to_genome[observation] = Genome.objects.filter(pk=0)
        #print(len(obs_to_genome))
        ###

        # Iterate over every sample and store data to data base
        for key in samples.keys():
            self.__process_sample__(samples[key], key, b_, df, obs_to_genome)

            # end_time = time.time()

            # print("Running time: %i seconds" % (int(end_time-start_time)))


UploadModel.register("biom", BiomImporter)


# TODO: Generic biom file processor for performing parsng without persisting and delivering back the mappable genomes as a dictiobnary
#TODO: Add UNMAPPABLE as dummy
