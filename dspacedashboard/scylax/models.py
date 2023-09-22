from lxml import etree

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

    @property
    def department_count(self):
        return Department.objects.filter(
            authors__in=self.authors.all()
        ).distinct().count()

    def to_xml(self):
        root = etree.Element('dublin_core', schema='dc')

        dc_type = etree.Element('dcvalue', element="type", qualifier="none")
        dc_type.text = 'article'
        root.append(dc_type)

        date = etree.Element('dcvalue', element="date", qualifier="issued")
        date.text = str(self.year.year)
        root.append(date)

        title = etree.Element('dcvalue', element="title", qualifier="none", language="pt_BR")
        title.text = self.title
        root.append(title)

        dc_issn = etree.Element('dcvalue', element="identifier", qualifier="issn")
        dc_issn.text = self.issn
        root.append(dc_issn)

        for author in self.authors.all():
            dc_author = etree.Element('dcvalue', element="contributor", qualifier="author", language="pt_BR")
            dc_author_lattes = etree.Element('dcvalue', element="contributor", qualifier="authorLattes", language="pt_BR")
            
            dc_author.text = author.name
            dc_author_lattes.text = f'http://lattes.cnpq.br/{author.id_lattes}'
            
            root.append(dc_author)
            root.append(dc_author_lattes)

        return etree.tostring(root, pretty_print=True)