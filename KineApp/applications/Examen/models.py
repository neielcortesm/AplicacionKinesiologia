from django.db import models

# Create your models here.
class ExamenFinal(models.Model):
    nombre = models.CharField('Nombre Examen',max_length=100, null=False)    
   # id_etapa = models.IntegerField()  # Puedes cambiarlo a ForeignKey('Etapa', on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    puntaje_total = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    resultado_final = models.CharField(max_length=50, null=True, blank=True)
    valor_uf = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    descripcion = models.TextField('Descripción Examen', null=True, max_length=200)

   # class Meta:
      #  db_table = "Examen_Final"

    def __str__(self):
        return str(self.id) + '-'+ self.nombre


