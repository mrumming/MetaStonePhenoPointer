from django.db import transaction

from MetaStone.EnumFields.DatabaseModels.Internal import DbModelMapping
from MetaStone.Procedures.Imports import UploadModel
from MetaStone.models import AdminFileUpload, DirectInferredSpeciesRelatedCharacteristics, Genome, GenomeLineage, \
    DirectInferredSamplingSiteCharacteristics, DirectInferredEcosystemRelatedCharacteristics


def process_all_imports(*args):
    # Select all uploads, that have not been processed yet
    """

    :param args: Tasks, to be performed as Tablenames as defined in MetaStone.EnumFields.DatabaseModels.Internal.Uploads.TABLE_NAME
    :type args: tuple
    """
    tasks = AdminFileUpload.objects.filter(status="uploaded")

    for task in tasks:
        task.status = "processing"
        task.save()
        if not args:
            for subtask in DbModelMapping.TASKS[task.db_model]:
                up_ = UploadModel.create(mname=DbModelMapping.TASK_FACTORY_ID[task.db_model],
                                         filepath=task.file_content.path, dbobj=subtask)
                up_.process()
        else:
            for arg in args:
                for subtask in DbModelMapping.TASKS[arg]:
                    up_ = UploadModel.create(mname=DbModelMapping.TASK_FACTORY_ID[task.db_model],
                                             filepath=task.file_content.path, dbobj=subtask)
                    up_.process()
        task.status = "finished"
        task.save()


@transaction.atomic
def _storeInferred_(data, dbObj):
    # to_store[ATTRIBUTE][TAX_LEVEL] = [[GENOMES_AFFECTTED_TO_STORE]}, [GENOMES_TO_INFER_FROM]]

    for hstore_name in data:
        for tax_level in data[hstore_name]:
            properties = {}
            for genome in data[hstore_name][tax_level][1]:
                characteristic = eval('genome.%s.%s' % (dbObj.eval_basename, dbObj.eval_subnames[hstore_name]))
                if characteristic in properties:
                    properties[characteristic] += 1
                else:
                    properties[characteristic] = 1

            for genome in data[hstore_name][tax_level][0]:
                if dbObj.objects.filter(genome=genome.taxon_oid).filter(taxonomy_level=tax_level).exists():
                    dbObj_ = dbObj.objects.filter(genome=genome.taxon_oid).filter(taxonomy_level=tax_level).first()
                    exec('dbObj_.%s = {}' % (hstore_name))
                    for characteristic, count in properties.items():
                        exec('dbObj_.%s["%s"] = "%f"' % (
                            hstore_name, characteristic, count / data[hstore_name][tax_level][1].count()))
                    dbObj_.save()

                else:
                    dbObj_ = dbObj.create(genome.taxon_oid)
                    dbObj_.taxonomy_level = tax_level

                    exec('dbObj_.%s = {}' % (hstore_name))
                    for characteristic, count in properties.items():
                        exec('dbObj_.%s["%s"] = "%f"' % (
                            hstore_name, characteristic, count / data[hstore_name][tax_level][1].count()))
                    dbObj_.save()


def compute_inferred_genome_characteristics():
    datasets = GenomeLineage.objects.values('pspecies').exclude(pspecies="unclassified").distinct().count()

    print("%i datasets to process..." % (datasets))

    counter = 0
    for pspecies in GenomeLineage.objects.values('pspecies').exclude(pspecies="unclassified").distinct():
        counter += 1
        if counter % 100 == 0:
            print("Still to process: %i" % (datasets - counter))
        for pgenus in GenomeLineage.objects.filter(pspecies=pspecies['pspecies']).values('pgenus').exclude(
                pgenus="unclassified").distinct():
            for pfamily in GenomeLineage.objects.filter(pspecies=pspecies['pspecies']).filter(
                    pgenus=pgenus['pgenus']).values('pfamily').exclude(pfamily="unclassified").distinct():
                for porder in GenomeLineage.objects.filter(pspecies=pspecies['pspecies']).filter(
                        pgenus=pgenus['pgenus']).filter(pfamily=pfamily['pfamily']).values('porder').exclude(
                    porder='unclassified').distinct():
                    for pclass in GenomeLineage.objects.filter(pspecies=pspecies['pspecies']).filter(
                            pgenus=pgenus['pgenus']).filter(pfamily=pfamily['pfamily']).filter(
                        porder=porder['porder']).values("pclass").exclude(pclass="unclassified").distinct():
                        for characteristic in [DirectInferredEcosystemRelatedCharacteristics,
                                               DirectInferredSamplingSiteCharacteristics,
                                               DirectInferredSpeciesRelatedCharacteristics]:
                            to_store = {}
                            for hstore_name, orig_name in characteristic.eval_subnames.items():

                                genomes = Genome.objects.filter(genomelineage__pspecies=pspecies['pspecies']).filter(
                                    genomelineage__pgenus=pgenus['pgenus']).filter(
                                    genomelineage__pfamily=pfamily['pfamily']).filter(
                                    genomelineage__porder=porder['porder']).filter(
                                    genomelineage__pclass=pclass['pclass']).exclude(
                                    genomelineage__pphylum="unclassified").exclude(
                                    genomelineage__pdomain="unclassified")
                                if eval('genomes.filter(%s__%s="")' % (characteristic.eval_basename, orig_name)):
                                    if eval('genomes.exclude(%s__%s="")' % (characteristic.eval_basename, orig_name)):
                                        to_store[hstore_name] = {}
                                        to_store[hstore_name]["pspecies"] = [eval(
                                            'genomes.filter(%s__%s="")' % (characteristic.eval_basename, orig_name)),
                                            eval('genomes.exclude(%s__%s="")' % (
                                                characteristic.eval_basename, orig_name))]
                                    else:
                                        genomes_0 = Genome.objects.filter(
                                            genomelineage__pgenus=pgenus['pgenus']).filter(
                                            genomelineage__pfamily=pfamily['pfamily']).filter(
                                            genomelineage__porder=porder['porder']).filter(
                                            genomelineage__pclass=pclass['pclass']).exclude(
                                            genomelineage__pphylum="unclassified").exclude(
                                            genomelineage__pdomain="unclassified")
                                        if eval('genomes_0.exclude(%s__%s="")' % (
                                                characteristic.eval_basename, orig_name)):
                                            to_store[hstore_name] = {}
                                            to_store[hstore_name]["pgenus"] = [eval('genomes.filter(%s__%s="")' % (
                                                characteristic.eval_basename, orig_name)), eval(
                                                'genomes_0.exclude(%s__%s="")' % (
                                                    characteristic.eval_basename, orig_name))]
                                        else:
                                            genomes_1 = Genome.objects.filter(
                                                genomelineage__pfamily=pfamily['pfamily']).filter(
                                                genomelineage__porder=porder['porder']).filter(
                                                genomelineage__pclass=pclass['pclass']).exclude(
                                                genomelineage__pphylum="unclassified").exclude(
                                                genomelineage__pdomain="unclassified")
                                            if eval('genomes_1.exclude(%s__%s="")' % (
                                                    characteristic.eval_basename, orig_name)):
                                                to_store[hstore_name] = {}
                                                to_store[hstore_name]["pfamily"] = [eval(
                                                    'genomes.filter(%s__%s="")' % (
                                                        characteristic.eval_basename, orig_name)), eval(
                                                    'genomes_1.exclude(%s__%s="")' % (
                                                        characteristic.eval_basename, orig_name))]
                                            else:
                                                genomes_2 = Genome.objects.filter(
                                                    genomelineage__porder=porder['porder']).filter(
                                                    genomelineage__pclass=pclass['pclass']).exclude(
                                                    genomelineage__pphylum="unclassified").exclude(
                                                    genomelineage__pdomain="unclassified")
                                                if eval('genomes_2.exclude(%s__%s="")' % (
                                                        characteristic.eval_basename, orig_name)):
                                                    to_store[hstore_name] = {}
                                                    to_store[hstore_name]["porder"] = [eval(
                                                        'genomes.filter(%s__%s="")' % (
                                                            characteristic.eval_basename, orig_name)), eval(
                                                        'genomes_2.exclude(%s__%s="")' % (
                                                            characteristic.eval_basename, orig_name))]
                                                else:
                                                    genomes_3 = Genome.objects.filter(
                                                        genomelineage__pclass=pclass['pclass']).exclude(
                                                        genomelineage__pphylum="unclassified").exclude(
                                                        genomelineage__pdomain="unclassified")
                                                    if eval('genomes_3.exclude(%s__%s="")' % (
                                                            characteristic.eval_basename, orig_name)):
                                                        to_store[hstore_name] = {}
                                                        to_store[hstore_name]["pclass"] = [eval(
                                                            'genomes.filter(%s__%s="")' % (
                                                                characteristic.eval_basename, orig_name)), eval(
                                                            'genomes_3.exclude(%s__%s="")' % (
                                                                characteristic.eval_basename, orig_name))]
                            # Store everything into database
                            if (to_store):
                                _storeInferred_(to_store, characteristic)
