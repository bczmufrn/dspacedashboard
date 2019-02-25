from django.db import models
from django.contrib.auth.models import User

from dspacedashboard.core.models import Basemodel

class FileImport(Basemodel):
    user = models.ForeignKey(User, verbose_name='Usuário de importação', on_delete=models.PROTECT)

    collection = models.CharField('Handle da coleção', max_length=30)
    dspace_simple_archive = models.FileField(verbose_name='Arquivo', upload_to='imports', blank=True, null=True)