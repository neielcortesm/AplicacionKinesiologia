from django.urls import path
from . import views

urlpatterns = [
    # AK-82: ver las 3 subcategorías
    path('<int:examen_id>/subcategorias/',
         views.pagina_5_subcategorias,
         name='pagina_5_subcategorias'),

    # AK-83: ver las preguntas de una subcategoría
    path('<int:examen_id>/subcategorias/<str:subcategoria_key>/',
         views.preguntas_por_subcategoria,
         name='preguntas_por_subcategoria'),

    # AK-85: guardar preguntas seleccionadas al hacer clic en Aceptar
    path('<int:examen_id>/subcategorias/<str:subcategoria_key>/guardar/',
         views.guardar_preguntas_seleccionadas,
         name='guardar_preguntas_seleccionadas'),
]