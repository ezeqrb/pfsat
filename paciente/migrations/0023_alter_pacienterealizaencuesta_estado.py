# Generated by Django 3.2.14 on 2023-08-22 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paciente', '0022_alter_paciente_obrasocial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pacienterealizaencuesta',
            name='estado',
            field=models.CharField(choices=[('', '--- Seleccione ---'), ('r', 'reasignada'), ('b', 'borrador'), ('p', 'publicada')], default='b', max_length=1),
        ),
    ]
