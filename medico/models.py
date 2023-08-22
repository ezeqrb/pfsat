from django.db import models
from paciente.models import Persona,Paciente
from index.models import Form

class Especialidad(models.Model):
    nombre = models.CharField(max_length=100,verbose_name='Especialidad',primary_key=True)
    
    class Meta:
        verbose_name = 'Especialidad'
        verbose_name_plural = 'Especialidades'

    def __str__(self):
        return self.nombre

class Medico(Persona):
    especialidad = models.ForeignKey(Especialidad,on_delete=models.CASCADE,null=True,blank=True)
    matricula = models.CharField(max_length=15,verbose_name='Matrícula',null=True,blank=True)
    pacientes = models.ManyToManyField(Paciente,through='Tratamiento') 
    encuestas = models.ManyToManyField(Form,through='MedicoCreaEncuesta') 

    class Meta:
        verbose_name = 'Médico'
        verbose_name_plural = 'Médicos'

class Tratamiento(models.Model):
    fechaAlta = models.DateField(auto_now=True,verbose_name='Fecha de Creación')
    paciente = models.ForeignKey(Paciente,on_delete=models.CASCADE,verbose_name='Paciente')
    medico = models.ForeignKey(Medico,on_delete=models.CASCADE,verbose_name='Médico')

    class Meta:
        verbose_name = 'Tratamiento'
        verbose_name_plural = 'Tratamientos'

    def __str__(self):
        return f"{self.paciente.get_fullname} es paciente de {self.medico.get_fullname}"
    
class MedicoCreaEncuesta(models.Model):
    medico = models.ForeignKey(Medico,on_delete=models.CASCADE)
    encuesta = models.ForeignKey(Form,on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Medico Crea Encuesta'
        verbose_name_plural = 'Medicos Crean Encuestas'

    def __str__(self):
        return f"{self.medico.get_fullname}"
