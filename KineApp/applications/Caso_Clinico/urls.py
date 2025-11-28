from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('inicio/', views.Inicio.as_view(), name='Inicio'),
    path('', views.Inicio.as_view(), name='Inicio'),
    path('list_all_casos/', views.ListAllCasos.as_view(), name='listAllCasos'),  
    path('list_casosByCategoria/', views.ListByCategoriaCasos.as_view(), name='listByCategoriaCasos'),
    path('verCaso/<pk>', views.DetailCaso.as_view(), name='detalleCaso'),
    path('video_caso/<int:pk>', views.VideoCaso.as_view(), name='videoCaso'),
     path('inicio/', login_required(views.Inicio.as_view(), login_url='Aestudiante:login'), name='Inicio'),
]
