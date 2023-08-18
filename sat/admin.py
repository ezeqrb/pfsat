from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from paciente.models import Paciente, ObraSocial, PacienteRealizaEncuesta
from medico.models import Medico, Especialidad, MedicoCreaEncuesta, Tratamiento
from index.models import Form, Questions, Choices, Answer, Responses

class PacienteAdmin(admin.ModelAdmin):
    list_display = ('dni','user','obraSocial','status',)
    list_display_links = ('user',)
    ordering = ('dni','user',)
    search_fields = ['dni','user','obraSocial']
    list_filter = ('obraSocial','baja','status',)
    list_per_page = 10

class MedicoAdmin(admin.ModelAdmin):
    list_display = ('dni','user','especialidad','status',)
    list_display_links = ('user',)
    ordering = ('dni','user',)
    search_fields = ['dni','user','especialidad']
    list_filter = ('especialidad','status',)
    list_per_page = 10
    
class FormAdmin(admin.ModelAdmin):
    list_display = ('title','code','status')
    list_display_links = ('title',)
    ordering = ('title',)
    search_fields = ['title','status']
    list_filter = ('status','is_quiz','edit_after_submit','allow_view_score',)
    list_per_page = 10

class PacienteRealizaEncuestaAdmin(admin.ModelAdmin):
    list_display = ('paciente','encuesta','fechaModificacion')
    ordering = ('paciente',)
    list_filter = ('encuesta','paciente')
    list_per_page = 10

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'paciente':
            kwargs['queryset'] = Paciente.objects.filter(baja=False,status=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class MedicoCreaEncuestaAdmin(admin.ModelAdmin):
    list_display = ('medico','encuesta','fecha')
    ordering = ('encuesta',)
    list_filter = ('medico',)
    list_per_page = 10

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'medico':
            kwargs['queryset'] = Medico.objects.filter(status=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# Register your models here.
admin.site.register(Paciente,PacienteAdmin)
admin.site.register(ObraSocial)
admin.site.register(PacienteRealizaEncuesta,PacienteRealizaEncuestaAdmin)
admin.site.register(Medico,MedicoAdmin)
admin.site.register(Especialidad)
admin.site.register(MedicoCreaEncuesta,MedicoCreaEncuestaAdmin)
admin.site.register(Tratamiento)
admin.site.register(Form,FormAdmin)
admin.site.register(Questions)
admin.site.register(Choices)
admin.site.register(Answer)
admin.site.register(Responses)