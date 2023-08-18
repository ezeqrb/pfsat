from django.urls import path
from paciente import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('paciente-signup', views.paciente_signup_view,name='paciente-signup'),
    path('paciente-dashboard', views.paciente_dashboard_view,name='paciente-dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)