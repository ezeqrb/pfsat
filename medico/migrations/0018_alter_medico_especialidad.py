# Generated by Django 3.2.14 on 2023-08-19 19:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medico', '0017_auto_20230813_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medico',
            name='especialidad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='medico.especialidad'),
        ),
    ]
