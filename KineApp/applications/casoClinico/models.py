from django.db import models


# Create your models here.
class Caso(models.Model):
    Descripción=models.CharField('Descripción', max_length=300, null=False, default="")
    categoria = models.ForeignKey('Categoria.Categoria', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)+'-'+self.Descripción+'-'+str(self.categoria)
    

