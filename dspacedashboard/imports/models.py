from django.db import models
from django.db.models import Q

from dspacedashboard.core.models import BaseModel
from dspacedashboard.accounts.models import User

class FileImportManager(models.Manager):
	def search(self, query):
		return self.filter(
            Q(pk__icontains=query) |
            Q(user__name__icontains=query) |
            Q(collection__name__icontains=query) | 
            Q(collection__handle__icontains=query)
        )

class Collection(BaseModel):
    name = models.CharField(verbose_name='Nome', max_length=255)
    handle = models.CharField(verbose_name='Nome', max_length=30)

    def __str__(self):
        return f'{self.handle} - {self.name}'

    class Meta:
        verbose_name = 'Coleção'
        verbose_name_plural = 'Coleções'

class FileImport(BaseModel):
    user = models.ForeignKey(User, verbose_name='Usuário de importação', on_delete=models.PROTECT)
    collection = models.ForeignKey(Collection, verbose_name='Coleção de destino', on_delete=models.PROTECT)

    objects = FileImportManager()

    def __str__(self):
        return f'{self.created_at} - {self.collection.name}'

    class Meta:
        verbose_name = 'Importação'
        verbose_name_plural = 'Importações'
        ordering = ('-created_at', )