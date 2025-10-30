from django.db import models

# Create your models here.
# FICHA PACIENTE

class FichaPaciente(models.Model):
    nombre_paciente = models.CharField(max_length=100)
    edad = models.IntegerField()
    diagnostico = models.TextField()
    fecha_evaluacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.id) + '-'+ self.nombre_paciente+' '+ str(self.fecha_evaluacion)
    