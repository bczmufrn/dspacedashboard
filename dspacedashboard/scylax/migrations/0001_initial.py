# Generated by Django 2.2.13 on 2023-08-23 11:45

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicCenter',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('id_scylax', models.PositiveIntegerField(unique=True, verbose_name='ID no scylax')),
                ('name', models.CharField(max_length=255, verbose_name='Nome')),
            ],
            options={
                'verbose_name': 'Centro',
                'verbose_name_plural': 'Centros',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('id_scylax', models.PositiveIntegerField(unique=True, verbose_name='ID no scylax')),
                ('name', models.CharField(max_length=255, verbose_name='Nome')),
                ('academic_center', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='scylax.AcademicCenter', verbose_name='Centro')),
            ],
            options={
                'verbose_name': 'Departamento',
                'verbose_name_plural': 'Departamentos',
            },
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('id_lattes', models.PositiveIntegerField(unique=True, verbose_name='ID Lattes')),
                ('name', models.CharField(max_length=512, verbose_name='Nome')),
                ('departments', models.ManyToManyField(related_name='authors', to='scylax.Department', verbose_name='Departamentos')),
            ],
            options={
                'verbose_name': 'Autor',
                'verbose_name_plural': 'Autores',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('id_scylax', models.PositiveIntegerField(unique=True, verbose_name='ID no scylax')),
                ('title', models.CharField(max_length=2048, verbose_name='Título')),
                ('year', models.DateField(verbose_name='Ano de publicação')),
                ('issn', models.CharField(max_length=255, verbose_name='ISSN')),
                ('exported', models.BooleanField(default=False, verbose_name='Já exportado')),
                ('authors', models.ManyToManyField(related_name='articles', to='scylax.Author', verbose_name='Autores')),
            ],
            options={
                'verbose_name': 'Artigo',
                'verbose_name_plural': 'Artigos',
            },
        ),
    ]
