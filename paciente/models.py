from django.db import models
from django.contrib.auth.models import User
from datetime import date
from index.models import Form

class Persona(models.Model):
    SEXO = [
        ('','--- Seleccione ---'),
        ('f','Femenino'),
        ('m','Masculino'),
        ('o','Otro')
    ]

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    imagen = models.ImageField(verbose_name='Imagen de Perfil',max_length=200,upload_to='usuarios-perfil/',null=True,blank=True)
    fechaNacimiento = models.DateField(verbose_name='Fecha de Nacimiento')
    sexo = models.CharField(max_length=1,verbose_name='Sexo',choices=SEXO)
    dni = models.CharField(max_length=15,verbose_name='DNI')
    direccion = models.CharField(max_length=100,verbose_name='Dirección',null=True,blank=True)
    telefono = models.CharField(max_length=30,verbose_name='Teléfono',null=True,blank=True)
    status = models.BooleanField(verbose_name='Estado',default=False)
    
    @property
    def get_edad(self):
        fecha_actual = date.today()
        edad = fecha_actual.year - self.fechaNacimiento.year - ((fecha_actual.month, fecha_actual.day) < (self.fechaNacimiento.month, self.fechaNacimiento.day))
        return edad

    @property
    def get_username(self):
        return self.user.first_name + "." + self.user.last_name
    
    @property
    def get_fullname(self):
        return self.user.first_name.capitalize() + " " + self.user.last_name.capitalize()
    
    @property
    def get_instance(self):
        return self
    
    def delete(self,using=None,keep_parents=False):
        if self.imagen:
            self.imagen.storage.delete(self.imagen.name) # borrado físico de la imagen
        super().delete()

    def __str__(self):
        return f"{self.get_fullname}"# - {self.dni}

    class Meta:
        abstract = True
        ordering = ['dni']

class ObraSocial(models.Model):
    nombre = models.TextField(max_length=100,verbose_name='Nombre de obra social',primary_key=True)

    class Meta:
        verbose_name = 'Obra Social'
        verbose_name_plural = 'Obras Sociales'

    def __str__(self):
        return self.nombre

class Paciente(Persona):
    obraSocial = models.ForeignKey(ObraSocial,on_delete=models.CASCADE,default='A completar',verbose_name='Obra Social')
    numeroObraSocial = models.CharField(max_length=30,verbose_name='Nº de obra social',null=True,blank=True)
    baja = models.BooleanField(verbose_name='Baja',default=False)
    descripcion = models.TextField(max_length=250,verbose_name="Descripción",null=True,blank=True)
    altura_m = models.DecimalField(max_digits=3,decimal_places=2,verbose_name="Altura [m]",null=True,blank=True)
    peso_kg = models.DecimalField(max_digits=5,decimal_places=2,verbose_name="Peso [kg]",null=True,blank=True)
    encuestas = models.ManyToManyField(Form,through='PacienteRealizaEncuesta') 

    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'

    # baja lógica
    def soft_delete(self):
        self.baja = True
        super().save()

    # alta lógica
    def restore(self):
        self.baja = False
        super().save()

class PacienteRealizaEncuesta(models.Model):
    ESTADOS = [
        ('','--- Seleccione ---'),
        ('b','borrador'),
        ('p','publicada')
    ]
    paciente = models.ForeignKey(Paciente,on_delete=models.CASCADE)
    encuesta = models.ForeignKey(Form,on_delete=models.CASCADE)
    fechaCreacion = models.DateTimeField(auto_now_add = True)
    fechaModificacion = models.DateTimeField(auto_now = True)
    estado = models.CharField(max_length=1,choices=ESTADOS,default='b')

    class Meta:
        verbose_name = 'Paciente Realiza Encuesta'
        verbose_name_plural = 'Pacientes Realizan Encuestas'

    def __str__(self):
        return f"{self.paciente.get_fullname}"