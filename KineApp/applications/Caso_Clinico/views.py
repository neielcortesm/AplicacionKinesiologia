from urllib.parse import urlparse, parse_qs
import re
import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, View
from django.contrib import messages
from applications.Pregunta.models import Pregunta, IntentoEtapa
from .models import CasoClinico, InscripcionCaso
from applications.Categoria.models import Categoria
from applications.Caso_Clinico.models import CasoClinico
from applications.Examen.models import ExamenFinal  # ajusta la ruta real
from django.db.models import Prefetch
from django.contrib.auth import get_user_model
from applications.Perfil.views import docente_login_required   # tu decorador
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
    login_url = "Aestudiante:login"      # importante
    redirect_field_name = "next"
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
    login_url = "Aestudiante:login"      # importante
    redirect_field_name = "next"

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

        # 5. Crear inscripción
        InscripcionCaso.objects.create(
            estudiante=request.user,
            caso=caso,
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

class EtapaInicialView(LoginRequiredMixin, TemplateView):
    template_name = 'Caso_Clinico/etapa_inicial.html'
    login_url = "Aestudiante:login"      # importante
    redirect_field_name = "next"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        caso = get_object_or_404(CasoClinico, pk=self.kwargs['pk'])
        context['caso'] = caso

        video_id_motivo = get_video_id(caso.video_motivo) if getattr(caso, 'video_motivo', None) else None
        embed_motivo = f"https://www.youtube.com/embed/{video_id_motivo}" if video_id_motivo else None
        context['video_motivo'] = embed_motivo

        # subcategorías SIN maniobras
        context['subcategorias'] = [
            (key, nombre)
            for key, nombre in Pregunta.CATEGORIAS
            if key != 'maniobras'
        ]

        subcat = self.request.GET.get('subcategoria')
        if subcat:
            key = f"acertadas_{caso.id}_{subcat}"
            acertadas = self.request.session.get(key, [])

            preguntas = Pregunta.objects.filter(
                caso=caso,
                etapa='anamnesis',
                subcategoria=subcat
            ).exclude(id__in=acertadas).order_by('id')

            correctas_pendientes = Pregunta.objects.filter(
                caso=caso,
                etapa='anamnesis',
                subcategoria=subcat,
                es_correcta=True
            ).exclude(id__in=acertadas)

            labels = dict(Pregunta.CATEGORIAS)
            context['preguntas'] = preguntas
            context['subcategoria_key'] = subcat
            context['subcategoria_nombre'] = labels.get(subcat, subcat)

            if not correctas_pendientes.exists():
                orden = ['sintoma', 'trabajo', 'actividades']

                if subcat == 'actividades':
                    context['mostrar_examen_fisico'] = True
                else:
                    try:
                        idx = orden.index(subcat)
                        siguiente = orden[idx + 1] if idx + 1 < len(orden) else None
                    except (ValueError, IndexError):
                        siguiente = None
                    context['siguiente_subcategoria'] = siguiente

        return context



    def post(self, request, *args, **kwargs):
        caso = get_object_or_404(CasoClinico, pk=kwargs['pk'])
        subcat = request.GET.get('subcategoria')

        pregunta_id = request.POST.get('pregunta')
        if not pregunta_id:
            messages.error(request, "Debes seleccionar una pregunta.")
            return redirect(f"{request.path}?subcategoria={subcat}" if subcat else request.path)

        pregunta = get_object_or_404(
            Pregunta,
            id=pregunta_id,
            caso=caso,
            etapa='anamnesis',
            subcategoria=subcat
        )

        if pregunta.es_correcta and pregunta.video_respuesta:
            IntentoEtapa.objects.create(
                estudiante=request.user,
                caso=caso,
                etapa='anamnesis',
                pregunta=pregunta,
                es_correcto=True,
            )
            key = f"acertadas_{caso.id}_{subcat}"
            acertadas = request.session.get(key, [])
            if pregunta.id not in acertadas:
                acertadas.append(pregunta.id)
                request.session[key] = acertadas
                request.session.modified = True

            return redirect(
                'respuesta_pregunta',
                caso_id=caso.id,
                pregunta_id=pregunta.id,
                subcategoria_key=subcat
            )
        else:
            IntentoEtapa.objects.create(
                estudiante=request.user,
                caso=caso,
                etapa='anamnesis',
                pregunta=pregunta,
                es_correcto=False,
            )
            messages.error(request, "La pregunta seleccionada no es correcta. Intenta nuevamente.")
            return redirect(f"{request.path}?subcategoria={subcat}" if subcat else request.path)



def respuesta_pregunta(request, caso_id, pregunta_id, subcategoria_key):
    caso = get_object_or_404(CasoClinico, id=caso_id)
    pregunta = get_object_or_404(Pregunta, id=pregunta_id, caso=caso)

    # video de la respuesta
    video_id = get_video_id(pregunta.video_respuesta) if pregunta.video_respuesta else None
    embed_url = f"https://www.youtube.com/embed/{video_id}" if video_id else None

    # AQUÍ se define la clave de sesión y se obtienen las acertadas
    key = f"acertadas_{caso.id}_{subcategoria_key}"
    acertadas = request.session.get(key, [])

    # AQUÍ se calcula 'pendientes' (las preguntas que faltan de esa subcategoría)
    pendientes = Pregunta.objects.filter(
        caso=caso,
        etapa='anamnesis',
        subcategoria=subcategoria_key
    ).exclude(id__in=acertadas).order_by('id')

    # Si ya no quedan preguntas pendientes, pasar a la siguiente subcategoría (ejemplo: trabajo)
    if not pendientes.exists():
        # cambia 'trabajo' por la subcategoría que quieras seguir
        siguiente = 'trabajo'
        return redirect(f"{reverse('etapa_inicial', args=[caso.id])}?subcategoria={siguiente}")

    labels = dict(Pregunta.CATEGORIAS)
    subcategoria_nombre = labels.get(subcategoria_key, subcategoria_key)

    context = {
        'caso': caso,
        'pregunta': pregunta,
        'video_respuesta': embed_url,
        'preguntas': pendientes,           # aquí mandas 'pendientes' al template
        'subcategoria_key': subcategoria_key,
        'subcategoria_nombre': subcategoria_nombre,
    }
    return render(request, 'Caso_Clinico/respuesta_pregunta.html', context)


class ExamenFisicoView(LoginRequiredMixin, TemplateView):
    template_name = 'Caso_Clinico/examen_fisico.html'
    login_url = "Aestudiante:login"      # importante
    redirect_field_name = "next"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        caso = get_object_or_404(CasoClinico, pk=self.kwargs['pk'])
        context['caso'] = caso

        # todas las preguntas de examen físico de este caso
        maniobras = Pregunta.objects.filter(
            caso=caso,
            etapa='examen_fisico'
        ).order_by('id')

        context['maniobras'] = maniobras
        return context

    def post(self, request, *args, **kwargs):
        caso = get_object_or_404(CasoClinico, pk=kwargs['pk'])

        seleccionadas_ids = request.POST.getlist('maniobras')  # lista de strings
        seleccionadas_ids = [int(i) for i in seleccionadas_ids]

        correctas_ids = list(
            Pregunta.objects.filter(
                caso=caso,
                etapa='examen_fisico',
                es_correcta=True
            ).values_list('id', flat=True)
        )

        set_sel = set(seleccionadas_ids)
        set_cor = set(correctas_ids)

        paso = set_sel == set_cor and len(set_cor) > 0
        IntentoEtapa.objects.create(
            estudiante=request.user,
            caso=caso,
            etapa='examen_fisico',
            pregunta=None,          # aquí es global a la etapa
            es_correcto=paso,
        )
        context = self.get_context_data(pk=caso.id)
        context['seleccionadas'] = seleccionadas_ids
        context['paso_examen_final'] = paso
        return render(request, self.template_name, context)


class ExamenFinalView(LoginRequiredMixin, TemplateView):
    template_name = 'Caso_Clinico/examen_final.html'
    login_url = "Aestudiante:login"      # importante
    redirect_field_name = "next"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        caso = get_object_or_404(CasoClinico, pk=self.kwargs['pk'])
        context['caso'] = caso

        if self.request.user.is_authenticated:
            errores_anamnesis = IntentoEtapa.objects.filter(
                estudiante=self.request.user,
                caso=caso,
                etapa='anamnesis',
                es_correcto=False
            ).count()
        else:
            errores_anamnesis = None


        errores_examen_fisico = IntentoEtapa.objects.filter(
            estudiante=self.request.user,
            caso=caso,
            etapa='examen_fisico',
            es_correcto=False
        ).count()
        # examen ideal (profesora)
        examen = ExamenFinal.objects.filter(caso=caso).first()
        context['examen'] = examen
        context['errores_anamnesis'] = errores_anamnesis
        context['errores_examen_fisico'] = errores_examen_fisico
        return context

    def post(self, request, *args, **kwargs):
        caso = get_object_or_404(CasoClinico, pk=kwargs['pk'])
        respuesta_alumno = request.POST.get('tratamiento_alumno', '').strip()

        examen = ExamenFinal.objects.filter(caso=caso).first()

        context = {
            'caso': caso,
            'examen': examen,
            'respuesta_alumno': respuesta_alumno,
            'mostrar_resultado': True,  # bandera para abrir modal o mostrar bloque
        }
        return render(request, self.template_name, context)

class ListCategoriasView(ListView):
    template_name = "Categoria/list_categorias.html"
    model = Categoria
    context_object_name = "categorias"

    def get_queryset(self):
        return Categoria.objects.all().order_by("nombre")
    
# applications/Caso_Clinico/views.py


User = get_user_model()

@docente_login_required
def inscripciones_por_caso(request):
    # obtener todos los casos para el filtro
    casos = CasoClinico.objects.all().order_by('nombre')

    caso_id = request.GET.get('caso')  # id seleccionado en el filtro
    inscripciones = InscripcionCaso.objects.select_related('estudiante', 'caso').order_by('-fecha')

    if caso_id:
        inscripciones = inscripciones.filter(caso_id=caso_id)

    context = {
        'casos': casos,
        'inscripciones': inscripciones,
        'caso_seleccionado': int(caso_id) if caso_id else None,
    }
    return render(request, 'docente/inscripciones_por_caso.html', context)

