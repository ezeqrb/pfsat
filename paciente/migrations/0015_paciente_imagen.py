# Generated by Django 3.2.14 on 2023-08-04 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paciente', '0014_merge_20230803_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='imagen',
            field=models.ImageField(blank=True, max_length=200, null=True, upload_to='perfil/', verbose_name='Imagen de Perfil'),
        ),
    ]
