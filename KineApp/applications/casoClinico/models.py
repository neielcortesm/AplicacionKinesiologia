from django.db import models


# Create your models here.
class Caso(models.Model):
    Descripción=models.CharField('Descripción', max_length=300, null=False, default="Descripción no disponible")
   

    def __str__(self):
        return str(self.id)+'-'+self.nombre+'-'+self.apellido
    

