from django import forms
from .models import Paciente,ObraSocial
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ('imagen',)
        widgets = {
            'imagen': forms.ClearableFileInput(attrs={'class':'form-control'}),
        }

class UserForm(UserCreationForm):
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la contraseña'}),
        help_text="La contraseña debe contener al menos 8 caracteres y no puede ser demasiado común."
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme la contraseña'}),
        help_text="Ingrese la misma contraseña para confirmar."
    )
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password1','password2']
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese el nombre','required':'required'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Ingrese el apellido','required':'required'}),
            'username': forms.TextInput(attrs={'class':'form-control','placeholder':'Usuario recomendado: nombre.apellido','required':'required'}),
            'email': forms.EmailInput(attrs={'class':'form-control','placeholder':'Ingrese el correo electrónico','required':'required'}),
        }

class UserFormView(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control','readonly': 'readonly'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}),
            'username': forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}),
            'email': forms.TextInput(attrs={'class':'form-control','readonly': 'readonly'}),
        }

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']

class PacienteFormSignUp(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['dni','fechaNacimiento','sexo']
        widgets = {
            'dni': forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese el DNI'}),
            'fechaNacimiento': forms.DateInput(attrs={'class': 'form-control','type':'date'}),
            'sexo': forms.Select(attrs={'class':'form-control'}),
        }

# para los campos de DecimalField: altura_m y peso_kg
class DecimalInput(forms.TextInput):
    def format_value(self, value):
        if isinstance(value, float):
            return '{:.2f}'.format(value)
        return super().format_value(value)
    
class PacienteFormAdd(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['dni','fechaNacimiento','sexo','direccion','telefono','obraSocial','numeroObraSocial','altura_m','peso_kg','descripcion']
        widgets = {
            'dni': forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese el DNI'}),
            'fechaNacimiento': forms.DateInput(attrs={'class': 'form-control','type':'date'}),
            'sexo': forms.Select(attrs={'class':'form-control'}),
            'direccion': forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese la dirección'}),
            'telefono': forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese el teléfono'}),
            'obraSocial': forms.Select(attrs={'class':'form-control'}),
            'numeroObraSocial': forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese el número de la obra social'}),
            'altura_m': DecimalInput(attrs={'class': 'form-control','placeholder':'Ingrese la altura en metros'}),
            'peso_kg': DecimalInput(attrs={'class': 'form-control','placeholder':'Ingrese el peso en kilogramos'}),
            'descripcion': forms.Textarea(attrs={'cols': 80, 'rows': 5,'class':'form-control','placeholder':'Ingrese una descripción'}),
        }
    
class PacienteFormEdit(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['direccion','telefono','obraSocial','numeroObraSocial','altura_m','peso_kg','descripcion']
        widgets = {
            'direccion': forms.TextInput(attrs={'class':'form-control'}),
            'telefono': forms.TextInput(attrs={'class':'form-control'}),
            'obraSocial': forms.Select(attrs={'class':'form-control'}),
            'numeroObraSocial': forms.TextInput(attrs={'class':'form-control'}),
            'altura_m': DecimalInput(attrs={'class': 'form-control'}),
            'peso_kg': DecimalInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'cols': 80, 'rows': 5,'class':'form-control'}),
        }

class ObraSocialForm(forms.ModelForm):
    class Meta:
        model = ObraSocial
        fields = ['nombre']
