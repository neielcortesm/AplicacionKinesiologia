from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from . import views
from .views import ListAllCasos, DetailCaso, EtapaInicialView, respuesta_pregunta
from .views import ExamenFisicoView, ExamenFinalView
from .views import ListCategoriasView
from .views import InscribirCasoView
from .views import inscripciones_por_caso
from django.urls import path, include

urlpatterns = [
    path('', login_required(views.Inicio.as_view(), login_url='Aestudiante:login'), name='Inicio'),
    path('inicio/', login_required(views.Inicio.as_view(), login_url='Aestudiante:login'), name='Inicio'),

    path('list_all_casos/', ListAllCasos.as_view(), name='listAllCasos'),
    path('list_casosByCategoria/', views.ListByCategoriaCasos.as_view(), name='listByCategoriaCasos'),

    path('detalle/<int:pk>/', DetailCaso.as_view(), name='detalleCaso'),
    path('inscribir/<int:pk>/', views.InscribirCasoView.as_view(), name='inscribirse_caso'),

    path('etapa_inicial/<int:pk>/', EtapaInicialView.as_view(), name='etapa_inicial'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('etapa_inicial/<int:pk>/', EtapaInicialView.as_view(), name='etapa_inicial'),
    path(
        'respuesta/<int:caso_id>/<int:pregunta_id>/<str:subcategoria_key>/',
        respuesta_pregunta,
        name='respuesta_pregunta'
    ),
]

urlpatterns += [
    path('examen_fisico/<int:pk>/', ExamenFisicoView.as_view(), name='examen_fisico'),
    path('examen_final/<int:pk>/', ExamenFinalView.as_view(), name='examen_final'),
]
urlpatterns += [
    path('list_categorias/', ListCategoriasView.as_view(), name='list_categorias'),
]
# urls.py del app de casos

urlpatterns += [
    path('caso/<int:pk>/inscribir/', InscribirCasoView.as_view(), name='inscribir_caso'),
]


urlpatterns += [
    path('perfil/', include('applications.Perfil.urls')),
    path('docente/inscripciones/', inscripciones_por_caso, name='inscripciones_por_caso'),
]
