from django.db import models

from dspacedashboard.core.models import BaseModel

class AcademicCenter(BaseModel):
    id_scylax = models.PositiveIntegerField('ID no scylax', unique=True)
    name = models.CharField('Nome', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Centro'
        verbose_name_plural = 'Centros'


class Department(BaseModel):
    id_scylax = models.PositiveIntegerField('ID no scylax', unique=True)
    name = models.CharField('Nome', max_length=255)
    academic_center = models.ForeignKey(
        AcademicCenter, 
        on_delete=models.PROTECT,
        verbose_name='Centro',
        null=True, 
        blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'


class Author(BaseModel):
    id_lattes = models.PositiveIntegerField('ID Lattes')
    name = models.CharField('Nome', max_length=512)
    departments = models.ManyToManyField(
        Department, 
        verbose_name='Departamentos',
        related_name='authors'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'


class Article(BaseModel):
    id_scylax = models.PositiveIntegerField('ID no scylax', unique=True)
    title = models.CharField('Título', max_length=2048)
    year = models.DateField('Ano de publicação')
    issn = models.CharField('ISSN', max_length=255)
    exported = models.BooleanField('Já exportado', default=False)
    authors = models.ManyToManyField(Author, verbose_name='Autores', related_name='articles')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Artigo'
        verbose_name_plural = 'Artigos'