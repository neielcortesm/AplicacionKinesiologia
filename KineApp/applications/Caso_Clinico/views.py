from django.shortcuts import render

from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    )
from .models import *


class Home(TemplateView):
    template_name = 'Caso_Clinico/home.html'


class ListAllCasos(ListView):
    template_name = 'Caso_Clinico/list_all_casos.html'
    model = CasoClinico
    context_object_name = 'ListAllCasos'
   # def get_queryset(self):
     #   palabra_clave = self.request.GET.get("kword", '')
      #  lista= CasoClinico.objects.filter(
      #  nombre= palabra_clave
      #  )
     #   return lista




class ListByCategoriaCasos(ListView):
    template_name = 'Caso_Clinico/list_casosByCategoria.html'
    model = CasoClinico
    context_object_name = 'ListByCategoriaCasos'
    queryset = CasoClinico.objects.filter(
        categoria__nombre= 'muscular'
        )
   
class DetailCaso(DetailView):
    template_name = 'Caso_Clinico/detalle_caso.html'
    model = CasoClinico
    context_object_name = 'DetailCaso'

