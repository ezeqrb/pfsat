from django import forms
from .models import Medico,Especialidad,Tratamiento

class TratamientoForm(forms.ModelForm):
    class Meta:
        model = Tratamiento
        fields = ['paciente','medico']
        widgets = {
            'paciente': forms.Select(attrs={'class':'form-control'}),
            'medico': forms.Select(attrs={'class':'form-control'}),
        }

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ('imagen',)
        widgets = {
            'imagen': forms.ClearableFileInput(attrs={'class':'form-control'}),
        }

class MedicoFormSignUp(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['dni','fechaNacimiento','sexo']
        widgets = {
            'dni': forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese el DNI'}),
            'fechaNacimiento': forms.DateInput(attrs={'class': 'form-control','type':'date'}),
            'sexo': forms.Select(attrs={'class':'form-control','placeholder':'-- Seleccione --'}),
        }

class MedicoFormAdd(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['dni','fechaNacimiento','sexo','direccion','telefono','especialidad','matricula']
        widgets = {
            'dni': forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese el DNI'}),
            'fechaNacimiento': forms.DateInput(attrs={'class': 'form-control','type':'date'}),
            'sexo': forms.Select(attrs={'class':'form-control'}),
            'direccion': forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese la dirección'}),
            'telefono': forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese el teléfono'}),
            'especialidad': forms.Select(attrs={'class':'form-control'}),
            'matricula': forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese la matrícula'}),
        }

class MedicoFormEdit(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['direccion','telefono','especialidad','matricula']
        widgets = {
            'direccion': forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese la dirección'}),
            'telefono': forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese el teléfono'}),
            'especialidad': forms.Select(attrs={'class':'form-control'}),
            'matricula': forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese la matrícula'}),
        }

class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = ['nombre']