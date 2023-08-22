from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from medico.models import Medico,Tratamiento
from paciente.forms import GroupForm, UserFormView, PerfilForm as PerfilFormM
from paciente.models import Paciente
from paciente.forms import GroupForm, UserFormView, PerfilForm as PerfilFormP
from django.contrib.auth.models import User, Group
from django.contrib import messages

def index_view(request):
    return render(request,'sat/public/index.html')

def es_admin(user):
    return user.groups.filter(name='ADMIN').exists()

def es_medico(user):
    return user.groups.filter(name='MEDICO').exists()

def es_paciente(user):
    return user.groups.filter(name='PACIENTE').exists()

def login_view(request):
    return redirect('index')

def afterlogin_view(request):
    if es_paciente(request.user):
        solicitud = Paciente.objects.filter(user_id=request.user.id,status=True)
        if solicitud:
            return redirect('paciente/paciente-dashboard')
        else:
            return render(request,'sat/private/user_wait_for_approval.html')
    elif es_medico(request.user):
        solicitud = Medico.objects.filter(user_id=request.user.id,status=True)
        if solicitud:
            return redirect('medico/medico-dashboard')
        else:
            return render(request,'sat/private/user_wait_for_approval.html')
    elif request.user.is_staff: 
        return redirect('admin-dashboard')
    else:
        return render(request,'sat/private/user_wait_for_approval.html')

def mi_perfil_view(request):
    if request.user.is_authenticated:
        try:
            usuario = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            return render(request,'error/404.html')
        
        userform = UserFormView(instance=usuario)
        if es_paciente(usuario):
            paciente = Paciente.objects.get(user=usuario.id)
            usuarioform = PerfilFormP(request.POST or None,request.FILES or None,instance=paciente)
        elif es_medico(usuario):
            medico = Medico.objects.get(user=usuario.id)
            usuarioform = PerfilFormM(request.POST or None,request.FILES or None,instance=medico)
        else:
            usuarioform = None

        if request.method == 'POST':
            if usuarioform and usuarioform.is_valid():
                if request.FILES.get("imagen") is None and request.POST.get("imagen-clear"):
                    if es_paciente(usuario):
                        paciente.imagen.delete()
                        paciente.save()
                    else:
                        medico.imagen.delete()
                        medico.save()
                    usuarioform.save()
                    messages.success(request,"Imagen eliminada con éxito!")
                elif request.FILES.get("imagen"):
                    usuarioform.save()
                    messages.success(request,"Imagen agregada con éxito!")
                else:
                    messages.info(request,"No se efectuaron cambios!")
                return redirect('mi-perfil')
            else:
                messages.error(request,"Error con la foto de perfil!")
                
        if es_paciente(usuario):
            form = {'userForm':userform,'usuarioForm':usuarioform,'usuario':paciente}
        elif es_medico(usuario):
            form = {'userForm':userform,'usuarioForm':usuarioform,'usuario':medico}
        else:
            form = {'userForm':userform}
        return render(request,'sat/private/mi-perfil.html',{'form':form})
    else:
        messages.error(request,'Permiso denegado: Debe iniciar sesión!')
        return redirect('index')

@login_required(login_url='/admin')
def admin_dashboard_view(request):
    if request.user.is_staff:
        pacientes_pendientes = Paciente.objects.all().filter(status=False)
        medicos = Medico.objects.all()
        usuarios = {'pacientes':pacientes_pendientes,'medicos':medicos}
        return render(request,'sat/private/admin-dashboard.html',{'usuarios':usuarios})
    else:
        messages.error(request,'Permiso denegado!')
        return redirect('afterlogin')

@login_required(login_url='/admin')
def approve_user_view(request,user_id):
    if request.user.is_staff or es_medico(request.user):
        try:
            usuario = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return render(request,'error/404.html')
        
        if es_medico(usuario):
            user = Medico.objects.get(user_id=user_id)
        else:
            user = Paciente.objects.get(user_id=user_id)
        user.status=True
        user.save()
        messages.success(request,'Solicitud aprobada!')
        return redirect('admin-dashboard')
    else:
        messages.error(request,'Permiso denegado!')
        return redirect('afterlogin')

@login_required(login_url='/admin')
def reject_user_view(request,user_id):
    if request.user.is_staff or es_medico(request.user):
        try:
            usuario = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return render(request,'error/404.html')
        
        if es_medico(usuario):
            user = Medico.objects.get(user_id=user_id)
        else:
            user = Paciente.objects.get(user_id=user_id)
        
        usuario.delete()
        user.delete()
        messages.success(request,'Solicitud rechazada!')
        return redirect('admin-dashboard')
    else:
        messages.error(request,'Permiso denegado!')
        return redirect('afterlogin')

''' CRUD usuarios '''

@login_required(login_url="/admin")
def list_usuarios(request):
    if request.user.is_staff:
        usuarios = User.objects.all().order_by('username')
        grupos = []
        for usuario in usuarios:
            if es_paciente(usuario):
                grupos.append("PACIENTE")
            elif es_medico(usuario):
                grupos.append("MEDICO")
            elif es_admin(usuario):
                grupos.append("ADMIN")
            else:
                grupos.append("---")
        usuarios_grupos = zip(usuarios, grupos)
        return render(request,'sat/private/manejo-usuario/list-usuarios.html',{'usuarios':usuarios_grupos})
    else:
        messages.error(request,'Permiso denegado!')
        return redirect('afterlogin')

@login_required(login_url="/admin")
def groups_usuarios(request):
    if request.user.is_staff:
        grupos = Group.objects.all().order_by('name')
        grupos_nusuarios = []
        for grupo in grupos:
            nusuarios = grupo.user_set.count()
            grupos_nusuarios.append((grupo, nusuarios))
        return render(request,'sat/private/manejo-usuario/groups-usuarios.html',{'grupos':grupos_nusuarios})
    else:
        messages.error(request,'Permiso denegado!')
        return redirect('afterlogin')

@login_required(login_url="/admin")
def add_group(request):
    if request.user.is_staff:
        if request.method=='POST':
            nombre = request.POST['nombre']
            nombre = nombre.upper()
            nuevo_grupo = Group.objects.create(name=nombre)
            messages.success(request,f'Grupo {nuevo_grupo} creado con éxito!')
        else:
            messages.error(request,'Error al crear el grupo!')
        return redirect('groups_usuarios')
    else:
        messages.error(request,'Permiso denegado!')
        return redirect('afterlogin')

@login_required(login_url="/admin")
def edit_group(request,grupo_id):
    if request.user.is_staff:
        try:
            grupo = Group.objects.get(pk=grupo_id)
        except Group.DoesNotExist:
            render(request,"error/404.html")

        if request.method == 'POST':
            grupoForm = GroupForm(request.POST, instance=grupo)
            if grupoForm.is_valid():
                grupoForm.name = request.POST["name"]
                grupoForm.save()
                messages.success(request,'Grupo editado con éxito!')
            else:
                for field, errors in grupoForm.errors.items():
                    print(f"Campo '{field}': {', '.join(errors)}")
                messages.error(request,'Error al editar Grupo!')
        return redirect(groups_usuarios)
    else:
        messages.error(request,'Permiso denegado!')
        return redirect('afterlogin')

@login_required(login_url="/admin")
def asignar_admin_group(request):
    if request.user.is_staff:
        try:
            admin_group = Group.objects.filter(name='ADMIN').first()
            usuarios = User.objects.filter(is_staff=True)
        except Group.DoesNotExist:
            render(request,"error/404.html")
        except User.DoesNotExist:
            render(request,"error/404.html")
        
        if usuarios:
            for usuario in usuarios:
                admin_group.user_set.add(usuario)
            messages.success(request,'Grupo ADMIN asignado!')
        else:
            messages.error(request,'No hay usuarios ADMIN!')
        return redirect(groups_usuarios)
    else:
        messages.error(request,'Permiso denegado!')
        return redirect('afterlogin')

''' CRUD tratamiento '''

@login_required(login_url="/medico-login")
def add_tratamiento(request,id_paciente):
    if request.user.is_staff or es_medico(request.user):
        if request.method=='POST':
            id_medico = request.POST['id_medico']
            nv_tratamiento,created = Tratamiento.objects.get_or_create(medico_id=id_medico,paciente_id=id_paciente)
            if created:
                messages.success(request,'Paciente asignado con éxito')
            else:
                messages.info(request,'Relación existente!')
            if request.user.is_staff:
                return redirect('admin-dashboard')
            else:
                return redirect('list_pacientes')
    else:
        messages.error(request,'Permiso denegado!')
        return redirect('afterlogin')