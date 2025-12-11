from django.db import models
from applications.Caso_Clinico.models import CasoClinico
# entrevista clinica, amnesis
#examen fisico
#examen final
#preguntas
#subcategorias
    #sintomas, #actividades recreativas, ##ocupacion, trabajo
from applications.Etapa.models import Etapa
# Create your models here.
class Pregunta(models.Model):
    CATEGORIAS = [
        ('sintomas', 'Síntomas'),
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

    