from django.db import models
from applications.Caso_Clinico.models import CasoClinico

# Create your models here.
class ExamenFinal(models.Model):
    tratamiento = models.TextField('Tratamiento', null=True, max_length=200)
    puntaje_total = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    caso = models.OneToOneField(CasoClinico, on_delete=models.CASCADE, related_name='examen_final')

    class Meta:
        verbose_name='Examen Final'
        verbose_name_plural="Exámenes Finales"
        ordering=['caso']

    def __str__(self):
        return f"{self.id} - {self.tratamiento[:30]} "
    
class PreguntaExamenFinal(models.Model):
    texto = models.TextField()
    examen_final = models.ForeignKey(ExamenFinal, on_delete=models.CASCADE, related_name='preguntas')

    class Meta:
        verbose_name='Pregunta examen final'
        verbose_name_plural="Preguntas examen final"
        ordering=['texto']

    def __str__(self):
        return self.texto