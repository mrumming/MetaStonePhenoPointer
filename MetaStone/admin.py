from django.contrib import admin

from .models import Genome, GenomeLineage, AdminFileUpload, User_Metagenome, User_Metagenome_Sample, User_Metagenome_Sample_Genome

admin.site.register(Genome)
admin.site.register(GenomeLineage)
admin.site.register(AdminFileUpload)
admin.site.register(User_Metagenome)
admin.site.register(User_Metagenome_Sample)
admin.site.register(User_Metagenome_Sample_Genome)
