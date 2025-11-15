from django.db import models
from applications.Caso_Clinico.models import CasoClinico

# Create your models here.
class ExamenFinal(models.Model):
    nombre = models.CharField('Nombre Examen', max_length=100, null=False)
    fecha = models.DateField(auto_now_add=True)
    puntaje_total = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    resultado_final = models.CharField(max_length=50, null=True, blank=True)
    descripcion = models.TextField('Descripción Examen', null=True, max_length=200)
    caso = models.OneToOneField(CasoClinico, on_delete=models.CASCADE, related_name='examen_final')

    class Meta:
        verbose_name='Examen Final'
        verbose_name_plural="Exámenes Finales"
        ordering=['nombre','caso']

    def __str__(self):
        return f"{self.id} - {self.nombre}"
    
class PreguntaExamenFinal(models.Model):
    CATEGORIAS = [
        ('sintoma', 'Síntoma'),
        ('trabajo', 'Trabajo'),
        ('actividades', 'Actividades'),
    ]
    texto = models.TextField()
    subcategoria = models.CharField(max_length=20, choices=CATEGORIAS)
    examen_final = models.ForeignKey(ExamenFinal, on_delete=models.CASCADE, related_name='preguntas')

    class Meta:
        verbose_name='Pregunta examen final'
        verbose_name_plural="Preguntas examen final"
        ordering=['texto','subcategoria']

    def __str__(self):
        return self.texto