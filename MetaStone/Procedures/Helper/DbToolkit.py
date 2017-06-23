from MetaStone.models import Genome

prefix_type_n_style = {"greengenes": r'^[kpcofgs]__(.*)', "none": r'(.*)'}


def match_str_to_genome_name(exact, prefixed, genome_name, *args):
    """

    :param exact: True, if only exact name matching is desired, False otherwise
    :type exact: bool
    :param prefixed: prefixstyle ("greengenes": r'^[kpcofgs]__(.*)', "none": r'(.*)' )
    :type prefixed: str
    :param genome_name: full genome name to be mapped onto db
    :type genome_name: str
    :param args: optional list of prefixstyled genome name parts
    :type args: tuple
    """
    # print(genome_name)


    if not genome_name:
        try:
            if len(args[0]) >= 2:
                genome_name = "%s %s" % (args[-2].strip()[3:], args[-1].strip()[3:])

        except:
            return None
    # if exact:
    #     if genome_name:
    #         # genomes = Genome.objects.filter(taxon_name=genome_name)
    #
    #         genomes = Genome.objects.filter(genomelineage__pgenus=args[-2].strip()[3:]).filter(
    #             genomelineage__pspecies=args[-1].strip()[3:])
    #         ###
    #         # UNCOMMENT IF DONE!
    #         # return genomes
    #         ###
    #
    #
    #         if (len(genomes) >= 1):
    #             return 1
    #         else:
    #             return 0
    #     else:
    #         return 0
    # else:
    #     return None

    if exact:
        if genome_name:
            genomes = Genome.objects.filter(taxon_name=genome_name)

            if genomes:
                return genomes

            genomes = Genome.objects.filter(genomelineage__pgenus=args[-2].strip()[3:]).filter(
                genomelineage__pspecies=args[-1].strip()[3:])
            return genomes


        else:
            return None
    else:
        return None
