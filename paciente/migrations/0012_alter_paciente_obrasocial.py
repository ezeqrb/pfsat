# Generated by Django 3.2.14 on 2023-08-03 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('paciente', '0011_paciente_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='obraSocial',
            field=models.ForeignKey(default='Prueba', on_delete=django.db.models.deletion.CASCADE, to='paciente.obrasocial', verbose_name='Obra Social'),
        ),
    ]