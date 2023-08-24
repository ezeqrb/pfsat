from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from paciente.forms import UserForm, UserFormView
from paciente.models import Paciente
from .models import Medico, Especialidad
from .forms import MedicoFormSignUp, MedicoFormAdd, MedicoFormEdit, EspecialidadForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from sat.views import es_paciente
from unidecode import unidecode
import re

def medico_login_view(request):
    ''' Autenticación '''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not es_paciente(user):   #solo los médicos pueden ser admin
                form = login(request, user)
                nxt = request.GET.get("next",None)
                if nxt is None:
                    return redirect('afterlogin')
                else:
                    return redirect(nxt)
            else:
                messages.error(request, f'Login válido solamente para médicos!')
        else:
            messages.error(request, f'Usuario o contraseña incorrecta... Vuelva a intentar!')
    form = AuthenticationForm()
    return render(request,'medico/medico-login.html', {'form': form})

def medico_signup_view(request):
    userForm = UserForm()
    medicoForm = MedicoFormSignUp()
    form = {'userForm':userForm,'usuarioForm':medicoForm}
    if request.method=='POST':
        userForm = UserForm(request.POST)
        medicoForm = MedicoFormSignUp(request.POST)
        if userForm.is_valid() and medicoForm.is_valid():
            # Usuario
            if User.objects.filter(email=request.POST['email']):
                messages.error(request,'Correo electrónico inválido: ya fue utilizado en otra cuenta!')
                return redirect('medico-signup')
            user = userForm.save(commit=False)
            user.first_name = request.POST['first_name'].capitalize()
            user.last_name = request.POST['last_name'].capitalize()
            #nombre_usuario = request.POST['first_name'].lower() + "." + request.POST['last_name'].lower()
            #nombre_usuario = re.sub(r'\s+', '', nombre_usuario) #nombre sin espacios
            #user.username = unidecode(nombre_usuario) #nombre sin caracteres especiales
            user.set_password(request.POST['password1'])
            user.save()
            # Médico
            medico = medicoForm.save(commit=False)
            medico.user = user
            medico.save()
            # Grupo de usuario
            my_medico_group = Group.objects.get_or_create(name='MEDICO')
            my_medico_group[0].user_set.add(user)
            messages.success(request,'Usuario creado con éxito!')
            return redirect('medico-login')
        else:
            for field, errors in userForm.errors.items():
                print(f"Campo '{field}': {', '.join(errors)}")
            for field, errors in medicoForm.errors.items():
                print(f"Campo '{field}': {', '.join(errors)}")
            messages.error(request,f"{', '.join(errors)}")
    return render(request,'medico/medico-signup.html',{'form':form})

@login_required(login_url="/medico-login")
def medico_dashboard_view(request):
    try:
        medico = Medico.objects.get(user_id=request.user.id)
    except Medico.DoesNotExist:
        return render(request,'error/404.html')
    
    pacientes = Paciente.objects.filter(tratamiento__medico=medico.id).distinct()
    solicitudes_pendientes = []
    for paciente in pacientes:
        if paciente.status == False: # paciente en espera
            solicitudes_pendientes.append(paciente)

    return render(request,'medico/medico-dashboard.html',{'pacientes':solicitudes_pendientes})

''' CRUD MÉDICO '''

@login_required(login_url="/medico-login")
def list_medicos(request):
    if request.user.is_staff:
        medicos = Medico.objects.filter(status=True).order_by('dni')
        return render(request,'sat/private/manejo-medico/list-medicos.html',{'medicos':medicos})
    else:
        messages.error(request,'Permiso denegado!')
        return redirect('afterlogin')

@login_required(login_url="/medico-login")
def add_medico(request):
    if request.user.is_staff:
        userform = UserForm()
        medicoform = MedicoFormAdd()
        form = {'userForm':userform,'usuarioForm':medicoform}
        if request.method=='POST':
            userform = UserForm(request.POST)
            medicoform = MedicoFormAdd(request.POST)
            if userform.is_valid() and medicoform.is_valid():
                # Usuario
                if User.objects.filter(email=request.POST['email']):
                    messages.error(request,'Correo electrónico inválido: ya fue utilizado en otra cuenta!')
                    return redirect('add_medico')
                user = userform.save(commit=False)
                user.first_name = request.POST['first_name'].capitalize()
                user.last_name = request.POST['last_name'].capitalize()
                user.set_password(request.POST['password1'])
                user.save()
                # Médico
                medico = medicoform.save(commit=False)
                medico.user = user
                medico.status = True #por este medio, no se envía la solicitud
                # Especialidad
                especialidad = request.POST.get('especialidad')
                if especialidad:
                    esp, created = Especialidad.objects.get_or_create(nombre=especialidad)
                    medico.especialidad = esp
                medico.save()
                medico_group = Group.objects.get_or_create(name='MEDICO')
                medico_group[0].user_set.add(user)
                messages.success(request,'Médico creado con éxito!')
                return redirect('list_medicos')
            else:
                for field, errors in medicoform.errors.items():
                    print(f"Campo '{field}': {', '.join(errors)}")
                messages.error(request,f"{', '.join(errors)}")
        Especialidades = Especialidad.objects.all()
        return render(request,'sat/private/manejo-medico/add-medico.html',{'form': form,'Especialidades':Especialidades})
    else:
        messages.error(request,'Permiso denegado!')
        return redirect('afterlogin')

@login_required(login_url="/medico-login")
def edit_medico(request,medico_id):
    if request.user.is_staff:
        try:
            medico = Medico.objects.get(pk=medico_id)
            usuario = User.objects.get(pk=medico.user.id)
        except Medico.DoesNotExist:
            return render(request,'error/404.html')
        except User.DoesNotExist:
            return render(request,'error/404.html')

        if (medico.status == True):
            if(request.method=='POST'):
                medicoForm = MedicoFormEdit(request.POST,instance=medico)
                if medicoForm.is_valid():
                    # Médico
                    medico = medicoForm.save()
                    # Especialidad
                    nv_especialidad = request.POST.get('especialidad')
                    if nv_especialidad:
                        esp, created = Especialidad.objects.get_or_create(nombre=nv_especialidad)
                        medico.especialidad = esp
                    medico.save()
                    messages.success(request,'Médico modificado con éxito!')
                    return redirect('list_medicos')
                else:
                    for field, errors in medicoForm.errors.items():
                        print(f"Campo '{field}': {', '.join(errors)}")
                    messages.error(request,f"{', '.join(errors)}")
            else:
                medicoForm = MedicoFormEdit(instance=medico)
            especialidades = Especialidad.objects.all()
            userForm = UserFormView(instance=usuario)
            form = {'userForm':userForm,'usuarioForm':medicoForm}
            return render(request,'sat/private/manejo-medico/edit-medico.html',{'form':form,'medico':medico,'elementos':especialidades})
        else:
            messages.info(request,'Médico en lista de espera!')
            return redirect('afterlogin')
    else:
        messages.error(request,'Permiso denegado!')
        return redirect('afterlogin')

@login_required(login_url="/medico-login")
def delete_medico(request,medico_id):
    if request.user.is_staff:
        try:
            medico = Medico.objects.get(id = medico_id)
            usuario = User.objects.get(id = medico.user.id)
        except Medico.DoesNotExist:
            return render(request,'error/404.html')
        except User.DoesNotExist:
            return render(request,'error/404.html')
        
        usuario.delete()
        medico.delete()
        messages.success(request,'Médico eliminado con éxito!')
        return redirect('list_medicos')
    else:
        messages.error(request,'Permiso denegado!')
        return redirect('afterlogin')

''' CRUD Especialidad '''

def add_especialidad(request):
    if request.method=='POST':
        nombre = request.POST['nombreEsp']
        nombre = unidecode(nombre) #sin acentos
        inst, nv = Especialidad.objects.get_or_create(
            nombre__iexact=nombre,
            defaults={
                'nombre': nombre.capitalize()
            }
        )
        if nv: 
            messages.success(request,'Especialidad creada con éxito!')
        else:
            messages.info(request,'Especialidad ya existente!')
    else:
        messages.error(request,'Error al crear la Especialidad!')
    return redirect('list_medicos')

def edit_especialidad(request,especialidad_id):
    try:
        esp = Especialidad.objects.get(pk=especialidad_id)
    except Especialidad.DoesNotExist:
        render(request,"error/404.html")

    if request.method == 'POST':
        espform = EspecialidadForm(request.POST, instance=esp)
        if espform.is_valid():
            espform.nombre = request.POST["nombreEsp"]
            espform.save()
            messages.success(request,'Especialidad editada con éxito!')
        else:
            for field, errors in espform.errors.items():
                print(f"Campo '{field}': {', '.join(errors)}")
            messages.error(request,'Error al editar Grupo!')
    return redirect('list_medicos')