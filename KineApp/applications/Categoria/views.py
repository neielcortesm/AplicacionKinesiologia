from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView
from applications.Categoria.models import Categoria


