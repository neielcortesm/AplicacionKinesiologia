from django.db import models
from applications.Etapa.models import Etapa
# Create your models here.
class Pregunta(models.Model):
    CATEGORIAS = [
        ('sintoma', 'Síntoma'),
        ('trabajo', 'Trabajo'),
        ('actividades', 'Actividades'),
    ]
    texto = models.TextField()
    subcategoria = models.CharField(max_length=20, choices=CATEGORIAS)
    etapa = models.ForeignKey(Etapa, on_delete=models.CASCADE,
    related_name='preguntas')
    es_correcta = models.BooleanField(default=False)
    def __str__(self):
        return self.texto

