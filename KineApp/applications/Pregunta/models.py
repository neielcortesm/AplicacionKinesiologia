# applications/Pregunta/models.py
from django.db import models
from applications.Caso_Clinico.models import CasoClinico
from django.contrib.auth import get_user_model
from applications.Caso_Clinico.models import CasoClinico
class Pregunta(models.Model):
    ETAPAS = [
        ('anamnesis', 'Entrevista clínica (Anamnesis)'),
        ('examen_fisico', 'Examen físico'),
        ('examen_final', 'Examen final'),
    ]

    CATEGORIAS = [
        ('sintoma', 'Sintoma'),
        ('trabajo', 'Trabajo'),
        ('actividades', 'Actividades'),
        ('maniobras', 'Maniobras'),  # ← NUEVA subcategoría

    ]

    caso = models.ForeignKey(CasoClinico, on_delete=models.CASCADE, related_name='preguntas')

    etapa = models.CharField(max_length=20, choices=ETAPAS)  # ← en vez de modelo Etapa
    subcategoria = models.CharField(max_length=20, choices=CATEGORIAS)

    texto = models.TextField()
    es_correcta = models.BooleanField(default=False)

    # video solo para las correctas (sobre todo en amnesis)
    video_respuesta = models.URLField('Video respuesta', null=True, blank=True)

    def __str__(self):
        return f"{self.texto} - {self.caso} -{self.get_subcategoria_display()} -  {self.get_etapa_display()} "
    class Meta:
        verbose_name = "Pregunta"
        verbose_name_plural = "Preguntas"



User = get_user_model()

class IntentoEtapa(models.Model):
    ETAPAS = [
        ('anamnesis', 'Anamnesis'),
        ('examen_fisico', 'Examen físico'),
        ('examen_final', 'Examen final'),
    ]

    estudiante = models.ForeignKey(User, on_delete=models.CASCADE)
    caso = models.ForeignKey(CasoClinico, on_delete=models.CASCADE)
    etapa = models.CharField(max_length=20, choices=ETAPAS)
    pregunta = models.ForeignKey('Pregunta', on_delete=models.SET_NULL, null=True, blank=True)
    es_correcto = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Intento de etapa"
        verbose_name_plural = "Intentos de etapas"

    def __str__(self):
        return f"{self.estudiante} - {self.caso} - {self.etapa} - {'OK' if self.es_correcto else 'Error'}"

