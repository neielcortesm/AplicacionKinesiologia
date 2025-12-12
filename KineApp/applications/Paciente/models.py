from datetime import date
from django.db import models

# Create your models here.
class FichaPaciente(models.Model):
    PREVISION_CHOICES = [
        ("fonasa", "Fonasa"),
        ("isapre", "Isapre"),
        ("particular", "Particular"),
    ]
    SEXO_CHOICES = [
        ("M", "Masculino"),
        ("F", "Femenino"),
        ("O", "Otro"),
    ]

    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=12)
    fecha_nacimiento = models.DateField()
    edad = models.IntegerField(null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    prevision = models.CharField(max_length=20, choices=PREVISION_CHOICES, null=True, blank=True)
    ocupacion = models.CharField(max_length=100, null=True, blank=True)
    habitos = models.TextField(null=True, blank=True)
    imagen = models.ImageField(upload_to='img/', blank=True, null=True)  # Cambiado a 'img/'


    def __str__(self):
        return f"{self.nombre}"
    def save(self, *args, **kwargs):
        # Calcula la edad automáticamente antes de guardar
        if self.fecha_nacimiento:
            hoy = date.today()
            self.edad = hoy.year - self.fecha_nacimiento.year - ((hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))
        super().save(*args, **kwargs)