from django.db import models
from applications.Caso_Clinico.models import CasoClinico
# entrevista clinica, amnesis
#examen fisico
#examen final
#preguntas
#subcategorias
    #sintomas, #actividades recreativas, ##ocupacion, trabajo
class Etapa(models.Model):
    ETAPAS = [
        ('Amnesis', 'Entrevista Clínica (Amnesis)'),
        ('examen_fisico', 'Exámen Físico'),
        ('examen_final', 'Exámen Final'),
    ]
    nombre = models.CharField(max_length=30, choices=ETAPAS, unique=True)
    descripcion = models.TextField('Descripción Etapa', null=True, max_length=200)
    video_url = models.URLField('Video', null=True, help_text="Ingresa el enlace del video de Youtube.")
    caso = models.ForeignKey(CasoClinico, on_delete=models.CASCADE, related_name='etapas')

    def __str__(self):
        return dict(self.ETAPAS).get(self.nombre, 'Desconocido')
    