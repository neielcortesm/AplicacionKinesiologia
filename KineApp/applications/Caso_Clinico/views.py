from urllib.parse import urlparse, parse_qs
import re
import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView

from .models import CasoClinico               # ✅ SOLO CasoClinico aquí
from applications.Pregunta.models import Pregunta  # ✅ Pregunta desde su app real
from applications.Etapa.models import Etapa

logger = logging.getLogger(__name__)



# =========================
#   VISTAS PRINCIPALES
# =========================
class Inicio(LoginRequiredMixin, TemplateView):  # usa tu clase base real
    template_name = "Caso_Clinico/inicio.html"
    login_url = reverse_lazy('Aestudiante:login')   # a dónde manda si no está logueado
    redirect_field_name = 'next'


class ListAllCasos(ListView):
    template_name = 'Caso_Clinico/list_all_casos.html'
    model = CasoClinico
    context_object_name = 'ListAllCasos'

    # Si quieres filtrar por palabra clave, descomenta y ajusta:
    # def get_queryset(self):
    #     palabra_clave = self.request.GET.get("kword", '').strip()
    #     if palabra_clave:
    #         return CasoClinico.objects.filter(nombre__icontains=palabra_clave)
    #     return super().get_queryset()


class ListByCategoriaCasos(ListView):
    template_name = 'Caso_Clinico/list_casosByCategoria.html'
    model = CasoClinico
    context_object_name = 'ListByCategoriaCasos'
    # Ajusta la categoría aquí si necesitas que sea dinámica
    queryset = CasoClinico.objects.filter(categoria__nombre='muscular')


class DetailCaso(DetailView):
    template_name = 'Caso_Clinico/detalle_caso.html'
    model = CasoClinico
    context_object_name = 'DetailCaso'


# =========================
#   UTILIDADES
# =========================
def get_video_id(url: str):
    """
    Extrae el ID de YouTube (11 caracteres) desde múltiples formatos:
    - https://www.youtube.com/watch?v=ID
    - https://youtu.be/ID
    - https://www.youtube.com/embed/ID
    - https://www.youtube.com/shorts/ID
    Limpia parámetros extra y valida longitud.
    """
    if not url:
        return None

    try:
        parsed = urlparse(url)
        host = (parsed.netloc or '').lower()
        path = parsed.path or ''

        # 1) https://www.youtube.com/watch?v=ID
        if 'youtube.com' in host:
            qs = parse_qs(parsed.query or '')
            if 'v' in qs and qs['v']:
                vid = qs['v'][0]
                return vid if re.fullmatch(r'[A-Za-z0-9_-]{11}', vid) else None

            # 2) https://www.youtube.com/embed/ID
            m = re.search(r'/embed/([A-Za-z0-9_-]{11})', path)
            if m:
                return m.group(1)

            # 3) https://www.youtube.com/shorts/ID
            m = re.search(r'/shorts/([A-Za-z0-9_-]{11})', path)
            if m:
                return m.group(1)

        # 4) https://youtu.be/ID
        if 'youtu.be' in host:
            m = re.search(r'/([A-Za-z0-9_-]{11})', path)
            if m:
                return m.group(1)

    except Exception as e:
        logger.exception("Error extrayendo video_id desde URL '%s': %s", url, e)

    return None


# =========================
#   VISTA DE VIDEO
# =========================
class VideoCaso(TemplateView):
    template_name = 'Caso_Clinico/video_caso.html'
    # model/context_object_name no son necesarios en TemplateView, pero no molestan
    model = CasoClinico
    context_object_name = 'VideoCaso'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtén la Etapa por PK desde la URL
        etapa = get_object_or_404(Etapa, pk=self.kwargs['pk'])
        context['etapa'] = etapa

        # Extrae el ID del video
        video_id = get_video_id(etapa.video_url)
        context['video_id'] = video_id

        # Logs útiles para depurar en consola
        logger.info("URL recibida de etapa (%s): %s", etapa.pk, etapa.video_url)
        logger.info("VIDEO ID extraído: %s", video_id)

        return context


# =========================
#   EVALUACIONES
# =========================
def evaluar_preguntas(request):
    preguntas = Pregunta.objects.all().order_by("id")
    resultado = None
    seleccionadas = []
    faltantes = []
    sobrantes = []

    if request.method == "POST":
        seleccionadas = request.POST.getlist("preguntas_seleccionadas")
        seleccionadas_ids = [int(i) for i in seleccionadas]

        correctas_ids = list(
            Pregunta.objects.filter(es_correcta=True).values_list("id", flat=True)
        )

        set_sel = set(seleccionadas_ids)
        set_cor = set(correctas_ids)

        faltantes_ids = set_cor - set_sel
        sobrantes_ids = set_sel - set_cor

        if set_sel == set_cor and len(set_cor) > 0:
            resultado = "✅ Tu selección coincide con las respuestas correctas."
        else:
            resultado = "⚠️ Tu selección aún no coincide con todas las respuestas correctas."

        faltantes = Pregunta.objects.filter(id__in=faltantes_ids)
        sobrantes = Pregunta.objects.filter(id__in=sobrantes_ids)

    context = {
        "preguntas": preguntas,
        "resultado": resultado,
        "faltantes": faltantes,
        "sobrantes": sobrantes,
        "seleccionadas": seleccionadas,
    }
    return render(request, "Caso_Clinico/evaluar_preguntas.html", context)


def comentarios_preguntas(request):
    preguntas = Pregunta.objects.all().order_by("id")

    seleccionadas = []
    correctas_sel = []
    incorrectas_sel = []

    if request.method == "POST":
        seleccionadas = request.POST.getlist("preguntas_seleccionadas")
        seleccionadas_ids = [int(i) for i in seleccionadas]

        correctas_ids = list(
            Pregunta.objects.filter(es_correcta=True).values_list("id", flat=True)
        )

        ids_correctas_sel = set(seleccionadas_ids) & set(correctas_ids)
        ids_incorrectas_sel = set(seleccionadas_ids) - set(correctas_ids)

        correctas_sel = Pregunta.objects.filter(id__in=ids_correctas_sel)
        incorrectas_sel = Pregunta.objects.filter(id__in=ids_incorrectas_sel)

    context = {
        "preguntas": preguntas,
        "seleccionadas": seleccionadas,
        "correctas_sel": correctas_sel,
        "incorrectas_sel": incorrectas_sel,
    }
    return render(request, "Caso_Clinico/comentarios_preguntas.html", context)


def verificar_avance_etapa(request):
    # Solo permite avanzar si la selección es exactamente igual al conjunto de preguntas correctas
    preguntas = Pregunta.objects.all().order_by("id")
    seleccionadas = []
    puede_avanzar = False
    mensaje = None

    if request.method == "POST":
        seleccionadas = request.POST.getlist("preguntas_seleccionadas")
        seleccionadas_ids = [int(i) for i in seleccionadas]

        correctas_ids = list(
            Pregunta.objects.filter(es_correcta=True).values_list("id", flat=True)
        )

        if set(seleccionadas_ids) == set(correctas_ids) and len(correctas_ids) > 0:
            puede_avanzar = True
            mensaje = "✅ Cumples los criterios. Puedes avanzar a la siguiente etapa."
        else:
            mensaje = "⛔ Aún no puedes avanzar. Debes seleccionar exactamente todas las respuestas correctas."

    context = {
        "preguntas": preguntas,
        "seleccionadas": seleccionadas,
        "puede_avanzar": puede_avanzar,
        "mensaje": mensaje,
    }
    return render(request, "Caso_Clinico/verificar_avance_etapa.html", context)


def siguiente_etapa(request):
    # Pantalla simple de la etapa siguiente (puedes mejorarla después)
    return render(request, "Caso_Clinico/siguiente_etapa.html")
