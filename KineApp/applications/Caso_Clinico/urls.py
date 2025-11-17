from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('list_all_casos/', views.ListAllCasos.as_view(), name='listAllCasos'),   
]
