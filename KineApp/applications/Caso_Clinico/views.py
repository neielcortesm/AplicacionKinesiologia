from urllib.parse import urlparse, parse_qs
import re
import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from applications.Pregunta.models import Pregunta
from .models import CasoClinico, InscripcionCaso
from applications.Categoria.models import Categoria
from applications.Caso_Clinico.models import CasoClinico



# =========================

#   VISTAS PRINCIPALES
# =========================
class Inicio(LoginRequiredMixin, TemplateView):  # usa tu clase base real
    template_name = "Caso_Clinico/inicio.html"
    login_url = reverse_lazy('Aestudiante:login')   # a dónde manda si no está logueado
    redirect_field_name = 'next'

class ListAllCasos(LoginRequiredMixin, ListView):
    """
    Lista TODOS los casos clínicos.
    Incluye buscador por nombre del caso.
    Tiene paginación.
    """
    template_name = "Caso_Clinico/list_all_casos.html"
    model = CasoClinico
    context_object_name = "ListAllCasos"
    paginate_by = 10
    login_url = "login"

    def get_queryset(self):
        # Base de datos optimizada con select_related
        qs = CasoClinico.objects.select_related("categoria", "paciente").order_by("id")

        # Búsqueda por nombre
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(nombre__icontains=q)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Mantiene el valor del buscador en pantalla
        ctx["q"] = self.request.GET.get("q", "")
        return ctx
#class ListAllCasos(ListView):
 #   template_name = 'Caso_Clinico/list_all_casos.html'
  #  model = CasoClinico
   # context_object_name = 'ListAllCasos'

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

# ============================================================
#                    DETALLE DEL CASO
# ============================================================
class DetailCaso(LoginRequiredMixin, DetailView):
    """
    Vista detalle del caso clínico.
    Además muestra si el usuario YA está inscrito.
    """
    template_name = "Caso_Clinico/detalle_caso.html"
    model = CasoClinico
    context_object_name = "caso"
    login_url = "login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        caso = self.get_object()

        # Verificar si el usuario ya está inscrito en este caso
        context["inscrito"] = InscripcionCaso.objects.filter(
            estudiante=self.request.user,
            caso=caso
        ).exists()

        return context



# ============================================================
#                    INSCRIPCIÓN A CASO
# ============================================================
class InscribirCasoView(View):
    """
    Procesa la inscripción de un estudiante a un caso clínico.
    Recibe el formulario desde POST.
    """
    def post(self, request, pk):

        # 1. Usuario no logueado
        if not request.user.is_authenticated:
            messages.error(request, "Debes iniciar sesión para inscribirte.")
            return redirect("detalleCaso", pk=pk)

        # 2. Obtener el caso
        caso = CasoClinico.objects.get(pk=pk)

        # 3. Evitar inscripciones duplicadas
        if InscripcionCaso.objects.filter(
            estudiante=request.user,
            caso=caso
        ).exists():
            messages.warning(request, "Ya estás inscrito en este caso.")
            return redirect("detalleCaso", pk=pk)

        # 4. Datos del formulario
        motivo = request.POST.get("motivo")
        comentario = request.POST.get("comentario")

        # 5. Crear inscripción
        InscripcionCaso.objects.create(
            estudiante=request.user,
            caso=caso,
            motivo=motivo,
            comentario=comentario
        )

        # 6. Confirmación
        messages.success(request, "Inscripción realizada con éxito.")
        return redirect("detalleCaso", pk=pk)

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
class EtapaInicialView(TemplateView):
    template_name = 'Caso_Clinico/etapa_inicial.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        caso = get_object_or_404(CasoClinico, pk=self.kwargs['pk'])
        context['caso'] = caso

        video_id_motivo = get_video_id(caso.video_motivo) if caso.video_motivo else None
        embed_motivo = f"https://www.youtube.com/embed/{video_id_motivo}" if video_id_motivo else None
        context['video_motivo'] = embed_motivo

        context['subcategorias'] = Pregunta.CATEGORIAS

        subcat = self.request.GET.get('subcategoria')
        if subcat:
            preguntas = Pregunta.objects.filter(
                caso=caso,
                etapa='amnesis',
                subcategoria=subcat
            ).order_by('id')
            labels = dict(Pregunta.CATEGORIAS)
            context['preguntas'] = preguntas
            context['subcategoria_key'] = subcat
            context['subcategoria_nombre'] = labels.get(subcat, subcat)

        return context

    def post(self, request, *args, **kwargs):
        caso = get_object_or_404(CasoClinico, pk=kwargs['pk'])
        subcat = request.GET.get('subcategoria')

        pregunta_id = request.POST.get('pregunta')  # solo una
        if not pregunta_id:
            messages.error(request, "Debes seleccionar una pregunta.")
            return redirect(f"{request.path}?subcategoria={subcat}" if subcat else request.path)

        pregunta = get_object_or_404(
            Pregunta,
            id=pregunta_id,
            caso=caso,
            etapa='amnesis',
            subcategoria=subcat
        )

        if pregunta.es_correcta and pregunta.video_respuesta:
            # redirigir a la página de respuesta
            return redirect('respuesta_pregunta',
                            caso_id=caso.id,
                            pregunta_id=pregunta.id,
                            subcategoria_key=subcat)
        else:
            messages.error(request, "La pregunta seleccionada no es pertinente. ¡Intentalo de nuevo!")
            return redirect(f"{request.path}?subcategoria={subcat}" if subcat else request.path)


def respuesta_pregunta(request, caso_id, pregunta_id, subcategoria_key):
    caso = get_object_or_404(CasoClinico, id=caso_id)
    pregunta = get_object_or_404(Pregunta, id=pregunta_id, caso=caso)

    video_id = get_video_id(pregunta.video_respuesta) if pregunta.video_respuesta else None
    embed_url = f"https://www.youtube.com/embed/{video_id}" if video_id else None

    preguntas_misma_subcat = Pregunta.objects.filter(
        caso=caso,
        etapa='amnesis',
        subcategoria=subcategoria_key
    ).order_by('id')

    labels = dict(Pregunta.CATEGORIAS)
    subcategoria_nombre = labels.get(subcategoria_key, subcategoria_key)

    context = {
        'caso': caso,
        'pregunta': pregunta,
        'video_respuesta': embed_url,
        'preguntas': preguntas_misma_subcat,
        'subcategoria_key': subcategoria_key,
        'subcategoria_nombre': subcategoria_nombre,
    }
    return render(request, 'Caso_Clinico/respuesta_pregunta.html', context)