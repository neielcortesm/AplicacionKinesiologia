from django.db import models

# Create your models here.


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='img/', blank=True, null=True)  # Cambiado a 'img/'
    def __str__(self):
        return self.nombre