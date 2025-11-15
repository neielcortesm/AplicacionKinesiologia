from django.contrib import admin
from .models import *
# Register your models here.

class ExamenFAdmin(admin.ModelAdmin):
    list_display=(
       'nombre', 
       'caso',
    )
    search_fields=('nombre',)

class PreguntaEFAdmin(admin.ModelAdmin):
    list_display=(
       'texto', 
       'subcategoria',
       'examen_final',
    )
    search_fields=('texto',)
admin.site.register(ExamenFinal, ExamenFAdmin)
admin.site.register(PreguntaExamenFinal, PreguntaEFAdmin)
