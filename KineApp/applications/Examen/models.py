from django.db import models

# --- MODELO EXAMEN FINAL ---
class ExamenFinal(models.Model):
    nombre = models.CharField('Nombre Examen', max_length=100, null=False)
    fecha = models.DateField(auto_now_add=True)
    puntaje_total = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    resultado_final = models.CharField(max_length=50, null=True, blank=True)
    descripcion = models.TextField('Descripción Examen', null=True, max_length=200)

   
    caso = models.OneToOneField(
        'casoClinico.Caso',
        on_delete=models.CASCADE,
        related_name='examen_final'
    )

    def __str__(self):
        return f"{self.id} - {self.nombre}"


# --- MODELO PREGUNTAS DEL EXAMEN FINAL ---
class Preguntas_Examen_Final(models.Model):
   
    texto_pregunta_exf = models.TextField('Pregunta', null=False)
    
   
    resultado_corregido_exf = models.CharField('Respuesta', max_length=50, null=True, blank=True)


    examen_final = models.ForeignKey(
        ExamenFinal,
        on_delete=models.CASCADE,        # Si eliminas el examen, se eliminan sus preguntas
        related_name='preguntas_exf'     # Acceso rápido desde ExamenFinal → preguntas_exf.all()
    )

    def __str__(self):
        return f"{self.id} - {self.texto_pregunta_exf}"
