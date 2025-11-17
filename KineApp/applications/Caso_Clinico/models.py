from django.db import models

class CasoClinico(models.Model):
    nombre = models.CharField(max_length=200)
    descripción = models.CharField('Descripción', max_length=300, null=False, default="")
    categoria = models.ForeignKey('Categoria.Categoria', on_delete=models.CASCADE)
    paciente = models.ForeignKey('Paciente.FichaPaciente', on_delete=models.CASCADE, null=True, blank=True)
    docente = models.ForeignKey('Perfil.Docente', on_delete=models.CASCADE, null=True, blank=True)
    puntaje_total = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.descripción} - {self.categoria}"
