from django.urls import path
from medico import views as viewsM
from paciente import views as viewsP
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('medico-signup', viewsM.medico_signup_view,name='medico-signup'),
    path('medico-dashboard', viewsM.medico_dashboard_view,name='medico-dashboard'),

    # Manejo de Paciente
    path('list_pacientes', viewsP.list_pacientes,name='list_pacientes'),
    path('edit_paciente/<int:paciente_id>', viewsP.edit_paciente,name='edit_paciente'),
    path('add_paciente', viewsP.add_paciente,name='add_paciente'),
    path('delete_paciente/<int:paciente_id>', viewsP.delete_paciente,name='delete_paciente'),

    # Manejo de Obra Social
    path('add_obraSocial', viewsP.add_obraSocial,name='add_obraSocial'),
    path('edit_obraSocial/<int:obraSocial_id>', viewsP.edit_obraSocial,name='edit_obraSocial'),

    # Manejo de Especialidad
    path('add_especialidad', viewsM.add_especialidad,name='add_especialidad'),
    path('edit_especialidad/<int:especialidad_id>', viewsM.edit_especialidad,name='edit_especialidad'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)