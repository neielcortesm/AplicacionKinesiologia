from django.contrib import admin
from .models import *
# Register your models here.

class ExamenFAdmin(admin.ModelAdmin):
    list_display=(
       'caso',
    )
    search_fields=('caso',)

class PreguntaEFAdmin(admin.ModelAdmin):
    list_display=(
       'texto', 
       'examen_final',
    )
    search_fields=('texto',)
admin.site.register(ExamenFinal, ExamenFAdmin)
admin.site.register(PreguntaExamenFinal, PreguntaEFAdmin)
