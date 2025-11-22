from django.urls import path
from . import views


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('list_all_casos/', views.ListAllCasos.as_view(), name='listAllCasos'),  
    path('list_casosByCategoria/', views.ListByCategoriaCasos.as_view(), name='listByCategoriaCasos'),
   # path('verCaso/<pk>', views.DetailCaso.as_view(), name='detalleCaso'),
]
