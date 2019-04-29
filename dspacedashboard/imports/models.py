from django.db import models

from dspacedashboard.core.models import BaseModel
from dspacedashboard.accounts.models import User

class Collection(BaseModel):
    name = models.CharField(verbose_name='Nome', max_length=255)
    handle = models.CharField(verbose_name='Nome', max_length=30)

    def __str__(self):
        return f'{self.handle} - {self.name}'

class FileImport(BaseModel):
    user = models.ForeignKey(User, verbose_name='Usuário de importação', on_delete=models.PROTECT)
    collection = models.ForeignKey(Collection, verbose_name='Coleção de destino', on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.created_at} - {self.collection.name}'