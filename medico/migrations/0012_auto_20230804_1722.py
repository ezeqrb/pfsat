# Generated by Django 3.2.14 on 2023-08-04 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medico', '0011_merge_0009_auto_20230803_1022_0010_auto_20230803_0940'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='medico',
            options={'verbose_name': 'Médico', 'verbose_name_plural': 'Médicos'},
        ),
        migrations.AddField(
            model_name='medico',
            name='imagen',
            field=models.ImageField(blank=True, max_length=200, null=True, upload_to='perfil/', verbose_name='Imagen de Perfil'),
        ),
    ]
