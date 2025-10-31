from django.db import models

# --- MODELO ETAPA ---
class Etapa(models.Model):
    fase = models.CharField('Fase Etapa', max_length=100, null=False)
    descripcion = models.TextField('Descripción Etapa', null=True, max_length=200)
    video_url = models.URLField('Video', null=False, help_text="Ingresa el enlace del video de Youtube.")

    def __str__(self):
        return f"{self.id} - {self.fase}"


# --- MODELO PREGUNTA ---
class Pregunta(models.Model):
    texto_pregunta = models.TextField()
    respuesta_correcta = models.TextField(blank=True, null=True)

    # 🔑 Aquí agregas la llave foránea hacia Etapa
    etapa = models.ForeignKey('Etapa', on_delete=models.CASCADE, related_name='preguntas')

    def __str__(self):
        return f"{self.id} - {self.texto_pregunta}"
