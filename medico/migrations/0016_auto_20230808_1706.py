# Generated by Django 3.2.14 on 2023-08-08 20:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0007_form_state'),
        ('medico', '0015_alter_tratamiento_fechaalta'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicoCreaEncuesta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now=True)),
                ('encuesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.form')),
                ('medico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medico.medico')),
            ],
        ),
        migrations.AddField(
            model_name='medico',
            name='encuestas',
            field=models.ManyToManyField(through='medico.MedicoCreaEncuesta', to='index.Form'),
        ),
    ]
