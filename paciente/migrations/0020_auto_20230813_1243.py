# Generated by Django 3.2.14 on 2023-08-13 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paciente', '0019_merge_20230813_1021'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='obrasocial',
            options={'verbose_name': 'Obra Social', 'verbose_name_plural': 'Obras Sociales'},
        ),
        migrations.AlterModelOptions(
            name='pacienterealizaencuesta',
            options={'verbose_name': 'Paciente Realiza Encuesta', 'verbose_name_plural': 'Pacientes Realizan Encuestas'},
        ),
    ]
