from django.db import models

# Create your models here.
# CATEGORÍAS

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.id) + '-'+ self.nombre
    