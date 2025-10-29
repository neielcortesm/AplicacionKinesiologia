from django.db import models

# Create your models here.

class Etapa(models.Model):
    fase = models.CharField('Fase Etapa',max_length=100, null=False)
    descripcion = models.TextField('Descripción Etapa', null=True, max_length=200)
    video_url = models.URLField('Video', null=False, help_text="Ingresa el enlace del video de Youtube.")
    #foreign key
 #   caso= models.ForeignKey(Caso_Clinico, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + '-'+ self.fase
    