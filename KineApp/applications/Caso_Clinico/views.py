from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    ListView, 
    )
from .models import *

class Home(TemplateView):
    template_name = 'Caso_Clinico/home.html'

class ListAllCasos(ListView):
    template_name = 'Caso_Clinico/list_all_casos.html'
    model = CasoClinico
    context_object_name = 'ListAllCasos'
