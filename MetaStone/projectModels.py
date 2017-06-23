from django.db import models


class stuff(models.Model):
    taxon_name = models.CharField(max_length=255)
    taxon_oid = models.BigIntegerField()