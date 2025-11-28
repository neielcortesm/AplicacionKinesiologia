from django.urls import path
from .views import (List_categorias)


path('categorias/', List_categorias.as_view(), name='categorias_list'),