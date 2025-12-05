from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView
from applications.Categoria.models import Categoria


# Create your views here.
class List_categorias(LoginRequiredMixin, ListView):
    template_name = "Caso_Clinico/list_categorias.html"   # <- plantilla correcta
    model = Categoria
    context_object_name = "categorias"
    login_url = "login"
    ordering = ["nombre"]