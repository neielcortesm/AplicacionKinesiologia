from django.db import models

# Create your models here.

class Estudiante(models.Model):
    nombre = models.CharField('Nombre', max_length=100, null=False)
    apellido = models.CharField('Apellido', max_length=100, null=False)
    correo = models.EmailField('Correo', max_length=100, unique=True, null=False)
    contrasena = models.CharField('Contraseña', max_length=100, null=False)
    estado = models.BooleanField('Activo', default=True)


    def __str__(self):
        return str(self.id)+'-'+self.nombre + '-' + self.apellido+'-'+self.correo


class Docente(models.Model):
    nombre = models.CharField('Nombre', max_length=100, null=False)
    apellido = models.CharField('Apellido', max_length=100, null=False)
    correo = models.EmailField('Correo', max_length=100, unique=True, null=False)
    contrasena = models.CharField('Contraseña', max_length=100, null=False)
    estado = models.BooleanField('Activo', default=True)


    def __str__(self):
        return str(self.id)+'-'+self.nombre + '-' + self.apellido+'-'+self.correo


class Administrador(models.Model):
    nombre = models.CharField('Nombre', max_length=100, null=False)
    apellido = models.CharField('Apellido', max_length=100, null=False)
    correo = models.EmailField('Correo', max_length=100, unique=True, null=False)
    contrasena = models.CharField('Contraseña', max_length=100, null=False)
    estado = models.BooleanField('Activo', default=True)

    class Meta:
        verbose_name='Administrador'
        verbose_name_plural="Administradores"
        ordering=['nombre','apellido']

    def __str__(self):
        return str(self.id)+'-'+self.nombre + '-' + self.apellido+'-'+self.correo