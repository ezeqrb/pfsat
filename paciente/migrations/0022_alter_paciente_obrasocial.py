# Generated by Django 3.2.14 on 2023-08-19 19:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('paciente', '0021_auto_20230813_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='obraSocial',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='paciente.obrasocial', verbose_name='Obra Social'),
        ),
    ]
