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
    

class Pregunta(models.Model):
    #id_pregunta = models.AutoField(primary_key=True)
    #pregunta_caso = models.ForeignKey(PreguntaCasoClinico, on_delete=models.CASCADE, related_name="preguntas")
    texto_pregunta = models.TextField()
    respuesta_correcta = models.TextField(blank=True, null=True)

    # 🔑 Aquí agregas la llave foránea hacia Etapa
    etapa = models.ForeignKey('Etapa', on_delete=models.CASCADE, related_name='preguntas')

    def __str__(self):
        return str(self.id) + '-'+ self.texto_pregunta