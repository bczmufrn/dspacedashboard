# Generated by Django 2.2.13 on 2023-08-23 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scylax', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='id_lattes',
            field=models.PositiveIntegerField(verbose_name='ID Lattes'),
        ),
    ]
