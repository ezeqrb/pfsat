# Generated by Django 3.2.14 on 2023-07-25 13:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ObraSocial',
            fields=[
                ('nombre', models.TextField(max_length=100, primary_key=True, serialize=False, verbose_name='nombre de obra social')),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaNacimiento', models.DateField(verbose_name='fecha de nacimiento')),
                ('sexo', models.CharField(choices=[('f', 'femenino'), ('m', 'masculino'), ('o', 'otro')], max_length=1, verbose_name='sexo')),
                ('dni', models.IntegerField(verbose_name='dni')),
                ('direccion', models.TextField(blank=True, max_length=100, null=True, verbose_name='direccion')),
                ('telefono', models.TextField(blank=True, max_length=30, null=True, verbose_name='telefono')),
                ('tipo_usuario', models.CharField(choices=[('p', 'paciente'), ('m', 'medico'), ('a', 'administrador')], max_length=1, verbose_name='tipo de usuario')),
                ('numeroObraSocial', models.TextField(max_length=30, verbose_name='numero de obra social')),
                ('baja', models.BooleanField(default=0, verbose_name='baja')),
                ('altura_m', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True, verbose_name='Altura')),
                ('peso_kg', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Peso')),
                ('obraSocial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paciente.obrasocial')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
