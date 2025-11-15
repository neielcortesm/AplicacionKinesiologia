from django.contrib import admin
from .models import FichaPaciente


class FichaPacienteAdmin(admin.ModelAdmin):
    list_display=(
       'nombre', 
       'edad',
       'prevision',
    )
    search_fields=('nombre',)
admin.site.register(FichaPaciente, FichaPacienteAdmin)
# Register your models here.
