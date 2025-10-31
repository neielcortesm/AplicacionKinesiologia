from django.db import models

class PreguntaDeEstudiante(models.Model):
    id_preguntas_ingresa = models.AutoField(primary_key=True)
    id_estudiante = models.IntegerField()  # FK lógica (puedes cambiarlo por ForeignKey si tienes el modelo Estudiante)
    id_caso_clinico = models.IntegerField()  # FK lógica (igual, puedes enlazarlo a un modelo CasoClinico)
    texto_pregunta = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2)
    retroalimentacion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "pregunta_de_estudiante"
        verbose_name = "Pregunta de Estudiante"
        verbose_name_plural = "Preguntas de Estudiantes"
        ordering = ["-fecha_envio"]

    def __str__(self):
        return f"Pregunta {self.id_preguntas_ingresa} (Estudiante {self.id_estudiante})"