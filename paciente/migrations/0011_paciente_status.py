# Generated by Django 3.2.14 on 2023-08-03 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paciente', '0010_auto_20230802_1917'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='status',
            field=models.BooleanField(default=False, verbose_name='Estado'),
        ),
    ]