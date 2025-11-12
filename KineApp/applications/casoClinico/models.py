from django.db import models


# Create your models here.
class Caso(models.Model):
    Descripción=models.CharField('Descripción', max_length=300, null=False, default="")
    categoria = models.ForeignKey('Categoria.Categoria', on_delete=models.CASCADE)

    estudiantes = models.ManyToManyField(
        'Perfil.Estudiante',         # nombre de la app + modelo
        related_name='casos_clinicos',  # para acceder desde el estudiante
        blank=True
    )

    def __str__(self):
        return str(self.id)+'-'+self.Descripción+'-'+str(self.categoria)
    

