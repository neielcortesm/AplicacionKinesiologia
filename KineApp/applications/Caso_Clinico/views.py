from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView

from .models import CasoClinico
from applications.Etapa.models import Etapa

from urllib.parse import urlparse, parse_qs
import re
import logging

logger = logging.getLogger(__name__)


class Inicio(TemplateView):
    template_name = 'Caso_Clinico/inicio.html'


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
