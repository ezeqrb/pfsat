# Generated by Django 3.2.14 on 2023-07-25 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paciente', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paciente',
            name='tipo_usuario',
        ),
    ]