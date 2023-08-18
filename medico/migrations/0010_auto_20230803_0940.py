# Generated by Django 3.2.14 on 2023-08-03 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medico', '0009_auto_20230802_1917'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='medico',
            options={'verbose_name': 'Médico', 'verbose_name_plural': 'Médicos'},
        ),
        migrations.AddField(
            model_name='medico',
            name='status',
            field=models.BooleanField(default=False, verbose_name='Estado'),
        ),
    ]
