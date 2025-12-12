# applications/Pregunta/models.py
from django.db import models
from applications.Caso_Clinico.models import CasoClinico

class Pregunta(models.Model):
    ETAPAS = [
        ('amnesis', 'Entrevista clínica (Amnesis)'),
        ('examen_fisico', 'Examen físico'),
        ('examen_final', 'Examen final'),
    ]

    CATEGORIAS = [
        ('sintoma', 'Sintoma'),
        ('trabajo', 'Trabajo'),
        ('actividades', 'Actividades'),
    ]

    caso = models.ForeignKey(CasoClinico, on_delete=models.CASCADE, related_name='preguntas')

    etapa = models.CharField(max_length=20, choices=ETAPAS)  # ← en vez de modelo Etapa
    subcategoria = models.CharField(max_length=20, choices=CATEGORIAS)

    texto = models.TextField()
    es_correcta = models.BooleanField(default=False)

    # video solo para las correctas (sobre todo en amnesis)
    video_respuesta = models.URLField('Video respuesta', null=True, blank=True)

    def __str__(self):
        return f"{self.get_etapa_display()} - {self.texto[:40]}"
    class Meta:
        verbose_name = "Pregunta"
        verbose_name_plural = "Preguntas"