from django.contrib import admin
from .models import *
# Register your models here.
class CasoAdmin(admin.ModelAdmin):
    list_display=(
       'nombre', 
       'categoria',
       'docente',
    )
    search_fields=('nombre',)
admin.site.register(CasoClinico, CasoAdmin)
admin.site.register(InscripcionCaso)