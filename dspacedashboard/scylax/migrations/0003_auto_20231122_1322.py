# Generated by Django 2.2.13 on 2023-11-22 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scylax', '0002_auto_20230823_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='id_lattes',
            field=models.BigIntegerField(verbose_name='ID Lattes'),
        ),
    ]
