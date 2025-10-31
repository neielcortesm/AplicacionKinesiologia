from django.db import models


# Create your models here.
class Caso(models.Model):
    
    Descripción=models.CharField('Descripción', max_length=300, null=False, default="")
    categoria = models.ForeignKey('Categoria.Categoria', on_delete=models.CASCADE)
    etapa=models.ForeignKey('Etapa.Etapa', on_delete=models.CASCADE)
    paciente = models.ForeignKey('Paciente.FichaPaciente', on_delete=models.CASCADE, null=True, blank=True)
    docente = models.ForeignKey('Perfil.Docente', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.id)+'-'+self.Descripción+str(self.categoria)
    

