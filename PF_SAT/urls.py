"""PF_SAT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth.views import LogoutView, PasswordChangeView
from sat import views as viewsS
from paciente import views as viewsP
from medico import views as viewsM
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    #path('administracion/', views.index_administracion, name='inicio_administracion'),
    path('admin/', admin.site.urls),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('medico/', include('medico.urls')),
    path('paciente/', include('paciente.urls')),
    path('', include('index.urls')),

    path('', viewsS.index_view, name='index'),
    path('paciente-login', viewsP.paciente_login_view,name='paciente-login'),
    path('medico-login', viewsM.medico_login_view,name='medico-login'),
    path('mi-perfil', viewsS.mi_perfil_view,name='mi-perfil'),
    #path('profile', viewsS.ProfileUpdate.as_view(template_name='sat/private/mi-perfil.html'), name='profile'),
    path('logout/', LogoutView.as_view(template_name='sat/public/index.html'), name='logout'),
    path('password_change/',PasswordChangeView.as_view(success_url='/'), name='password_change'),
    #path('password_change/', PasswordChangeView.as_view(template_name='sat/public/password_change.html', success_url='/'), name='password_change'), #NO FUNCIONA!
    path('afterlogin', viewsS.afterlogin_view,name='afterlogin'),
    path('admin-dashboard', viewsS.admin_dashboard_view,name='admin-dashboard'),

    # Manejo de Médicos
    path('admin-list_medicos', viewsM.list_medicos,name='list_medicos'),
    path('admin-edit_medico/<int:medico_id>', viewsM.edit_medico,name='edit_medico'),
    path('admin-add_medico', viewsM.add_medico,name='add_medico'),
    path('admin-delete_medico/<int:medico_id>', viewsM.delete_medico,name='delete_medico'),

    # Relación Médico-Paciente
    path('admin-add_tratamiento/<int:id_paciente>', viewsS.add_tratamiento,name='add_tratamiento'),

    # Manejo de Usuarios
    path('admin-list_usuarios', viewsS.list_usuarios,name='list_usuarios'),
    path('admin-groups_usuarios', viewsS.groups_usuarios,name='groups_usuarios'),
    path('admin-add_group', viewsS.add_group,name='add_group'),
    path('admin-edit_group/<int:grupo_id>', viewsS.edit_group,name='edit_group'),
    path('admin-asignar_admin_group', viewsS.asignar_admin_group,name='asignar_admin_group'),
    path('admin-approve_user_view/<int:user_id>', viewsS.approve_user_view,name='approve_user_view'),
    path('admin-reject_user_view/<int:user_id>', viewsS.reject_user_view,name='reject_user_view'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)