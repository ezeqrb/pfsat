from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from .forms import UserForm, UserFormView, PacienteFormSignUp, PacienteFormAdd, PacienteFormEdit, ObraSocialForm
from .models import Paciente, ObraSocial
from medico.models import Medico,Tratamiento
from sat.views import es_paciente,es_medico
from unidecode import unidecode

def paciente_login_view(request):
    ''' Autenticación '''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if es_paciente(user):
                form = login(request, user)
                print(form)
                nxt = request.GET.get("next",None)
                if nxt is None:
                    return redirect('afterlogin')
                else:
                    return redirect(nxt)
            else:
                messages.error(request, f'Login válido solamente para pacientes!')
        else:
            messages.error(request, f'Usuario o contraseña incorrecta... Vuelva a intentar!')
    form = AuthenticationForm()
    return render(request,'paciente/paciente-login.html', {'form': form})

def paciente_signup_view(request):
    userform = UserForm()
    pacienteform = PacienteFormSignUp()
    form = {'userForm':userform,'usuarioForm':pacienteform}
    if request.method=='POST':
        userform = UserForm(request.POST)
        pacienteform = PacienteFormSignUp(request.POST)
        if userform.is_valid() and pacienteform.is_valid():
            # Usuario
            if User.objects.filter(email=request.POST['email']):
                messages.error(request,'Correo electrónico inválido: ya fue utilizado en otra cuenta!')
                return redirect('paciente-signup')
            user = userform.save(commit=False)
            user.first_name = request.POST['first_name'].capitalize()
            user.last_name = request.POST['last_name'].capitalize()
            #nombre_usuario = request.POST['first_name'].lower() + "." + request.POST['last_name'].lower()
            #nombre_usuario = re.sub(r'\s+', '', nombre_usuario) #nombre sin espacios
            #user.username = unidecode(nombre_usuario) #nombre sin caracteres especiales
            user.set_password(request.POST['password1'])
            user.save()
            # Paciente
            paciente = pacienteform.save(commit=False)
            paciente.user = user
            paciente.save()
            # Grupo de usuario
            my_paciente_group = Group.objects.get_or_create(name='PACIENTE')
            my_paciente_group[0].user_set.add(user)
            # Tratamiento: funciona en el caso de que el médico exista en la bbdd!
            try:
                user_mp = User.objects.get(username='gustavo.giunta')
                medico_mp = Medico.objects.get(user_id=user_mp.id)
                nv_tratamiento, created = Tratamiento.objects.get_or_create(medico_id=medico_mp.id,paciente_id=paciente.id)#por defecto, se asocia al paciente con el médico
            except:
                print("Falta asignar médico!")
            messages.success(request,'Usuario creado con éxito!')
            return redirect('paciente-login')
        else:
            for field, errors in userform.errors.items():
                print(f"Campo '{field}': {', '.join(errors)}")
            for field, errors in pacienteform.errors.items():
                print(f"Campo '{field}': {', '.join(errors)}")
            messages.error(request,f"{', '.join(errors)}")
    return render(request,'paciente/paciente-signup.html',{'form': form})

@login_required(login_url="/paciente-login")
def paciente_dashboard_view(request):
    return render(request,'paciente/paciente-dashboard.html')

''' CRUD PACIENTE '''

@login_required(login_url="/medico-login")
def list_pacientes(request):
    medicos_activos = Medico.objects.filter(status=True)
    if request.user.is_staff: #los admin pueden ver a todos los pacientes
        pacientes = Paciente.objects.filter(baja=False,status=True).order_by('dni')
    else: #los médicos solamente pueden ver a sus pacientes
        try:
            medico = Medico.objects.get(user_id=request.user.id)
        except Medico.DoesNotExist:
            return render(request,'error/404.html')
        pacientes = Paciente.objects.filter(tratamiento__medico=medico.id,status=True,baja=False).distinct()
    return render(request,'medico/manejo-paciente/list-pacientes.html',{'pacientes':pacientes,'medicos':medicos_activos})

@login_required(login_url="/medico-login")
def add_paciente(request):
    userform = UserForm()
    pacienteform = PacienteFormAdd()
    form = {'userForm':userform,'usuarioForm':pacienteform}
    if request.method=='POST':
        userform = UserForm(request.POST)
        pacienteform = PacienteFormAdd(request.POST)
        if userform.is_valid() and pacienteform.is_valid():
            # Usuario
            if User.objects.filter(email=request.POST['email']):
                messages.error(request,'Correo electrónico inválido: ya fue utilizado en otra cuenta!')
                return redirect('add_paciente')
            user = userform.save(commit=False)
            user.first_name = request.POST['first_name'].capitalize()
            user.last_name = request.POST['last_name'].capitalize()
            user.set_password(request.POST['password1'])
            user.save()
            # Paciente
            paciente = pacienteform.save(commit=False)
            paciente.user = user
            paciente.status = True #por este medio, no se envía la solicitud
            # Obra Social
            obraSocial = request.POST.get('obraSocial')
            if obraSocial:
                obra_social, created = ObraSocial.objects.get_or_create(nombre=obraSocial)
                paciente.obraSocial = obra_social
            paciente.save()
            my_paciente_group = Group.objects.get_or_create(name='PACIENTE')
            my_paciente_group[0].user_set.add(user)
            # Tratamiento: Relación Médico-Paciente
            if es_medico(request.user): #si el médico agrega un paciente, se crea la relación automáticamente
                medico = Medico.objects.get(user_id=request.user.id)
                nv_tratamiento = Tratamiento.objects.get_or_create(medico_id=medico.id,paciente_id=paciente.id)
            # si el admin crea un paciente, le debe asociar un médico
            messages.success(request,'Paciente creado con éxito!')
            return redirect('list_pacientes')
        else:
            for field, errors in userform.errors.items():
                print(f"Campo '{field}': {', '.join(errors)}")
            for field, errors in pacienteform.errors.items():
                print(f"Campo '{field}': {', '.join(errors)}")
            messages.error(request,f"{', '.join(errors)}")
    ObrasSociales = ObraSocial.objects.all()
    return render(request,'medico/manejo-paciente/add-paciente.html',{'form': form,'ObrasSociales':ObrasSociales})

@login_required(login_url="/medico-login")
def edit_paciente(request,paciente_id):
    try:
        paciente = Paciente.objects.get(pk=paciente_id)
        usuario = User.objects.get(pk=paciente.user.id)
    except Paciente.DoesNotExist:
        return render(request,'error/404.html')
    except User.DoesNotExist:
        return render(request,'error/404.html')

    if(paciente.status == True):
        if(request.method=='POST'):
            pacienteForm = PacienteFormEdit(request.POST,instance=paciente)
            if pacienteForm.is_valid():
                # Paciente
                paciente = pacienteForm.save()
                # Obra Social
                obraSocial = request.POST.get('obraSocial')
                if obraSocial:
                    obra_social, created = ObraSocial.objects.get_or_create(nombre=obraSocial)
                    paciente.obraSocial = obra_social
                paciente.save()
                messages.success(request,'Paciente modificado con éxito!')
                return redirect('list_pacientes')
            else:
                for field, errors in pacienteForm.errors.items():
                    print(f"Campo '{field}': {', '.join(errors)}")
                messages.error(request,f"{', '.join(errors)}")
        else:
            pacienteForm = PacienteFormEdit(instance=paciente)
        ObrasSociales = ObraSocial.objects.all()
        userForm = UserFormView(instance=usuario)
        form = {'userForm':userForm,'usuarioForm':pacienteForm}
        return render(request,'medico/manejo-paciente/edit-paciente.html',{'form':form,'paciente':paciente,'elementos':ObrasSociales})
    else:
        messages.info(request,'Paciente en lista de espera!')
        return redirect('afterlogin')

@login_required(login_url="/medico-login")
def delete_logico_paciente(request,paciente_id):
    try:
        paciente = Paciente.objects.get(pk=paciente_id)
    except Paciente.DoesNotExist:
        return render(request,'error/404.html')
    
    paciente.soft_delete() #baja = True o paciente.delete()
    return redirect('list_pacientes')

@login_required(login_url="/medico-login")
def delete_paciente(request,paciente_id):
    try:
        paciente = Paciente.objects.get(pk=paciente_id)
        usuario = User.objects.get(pk=paciente.user.id)
    except Paciente.DoesNotExist:
        return render(request,'error/404.html')
    except User.DoesNotExist:
        return render(request,'error/404.html')
    
    
    paciente.delete()
    usuario.delete()
    messages.success(request,'Paciente eliminado con éxito!')
    return redirect('list_pacientes')

''' CRUD Obra Social '''

def add_obraSocial(request):
    if request.method=='POST':
        nombre = request.POST['nombreOS']
        nombre = unidecode(nombre) #sin acentos
        inst, nv = ObraSocial.objects.get_or_create(
            nombre__iexact=nombre,
            defaults={
                'nombre': nombre.capitalize()
            }
        )
        if nv: 
            messages.success(request,'Obra Social creada con éxito!')
        else:
            messages.info(request,'Obra Social ya existente!')
    else:
        messages.error(request,'Error al crear la Obra Social!')
    return redirect('list_pacientes')

def edit_obraSocial(request,obraSocial_id):
    try:
        obraSocial = ObraSocial.objects.get(pk=obraSocial_id)
    except ObraSocial.DoesNotExist:
        render(request,"error/404.html")

    if request.method == 'POST':
        osform = ObraSocialForm(request.POST, instance=obraSocial)
        if osform.is_valid():
            osform.nombre = request.POST["nombreOS"]
            osform.save()
            messages.success(request,'Obra Social editada con éxito!')
        else:
            for field, errors in osform.errors.items():
                print(f"Campo '{field}': {', '.join(errors)}")
            messages.error(request,'Error al editar Grupo!')
    return redirect('list_pacientes')