from django.db import models
from django.contrib.auth.models import User

class CasoClinico(models.Model):
    nombre = models.CharField(max_length=200)
    descripción = models.CharField('Descripción', max_length=300, null=False, default="")
    categoria = models.ForeignKey('Categoria.Categoria', on_delete=models.CASCADE)
    paciente = models.ForeignKey('Paciente.FichaPaciente', on_delete=models.CASCADE, null=True, blank=True)
    docente = models.ForeignKey('Perfil.Docente', on_delete=models.CASCADE, null=True, blank=True)
    puntaje_total = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    video_motivo = models.URLField('Video motivo de consulta', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.descripción}"
    

class InscripcionCaso(models.Model):
    estudiante = models.ForeignKey(User, on_delete=models.CASCADE)
    caso = models.ForeignKey(CasoClinico, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('estudiante', 'caso')  

    def __str__(self):
        return f"{self.estudiante.username} inscrito en {self.caso.nombre}"