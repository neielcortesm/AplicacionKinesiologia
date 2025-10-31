from django.db import models
from django.db import models

class Estudiante(models.Model):
    nombre = models.CharField('Nombre', max_length=100, null=False)
    apellido = models.CharField('Apellido', max_length=100, null=False)
    correo = models.EmailField('Correo', max_length=100, unique=True, null=False)
    contrasena = models.CharField('Contraseña', max_length=100, null=False)
    estado = models.BooleanField('Activo', default=True)

    def _str_(self):
        return str(self.id)+'-'+self.nombre + '-' + self.apellido+'-'+self.correo

class Docente(models.Model):
    nombre = models.CharField('Nombre', max_length=100, null=False)
    apellido = models.CharField('Apellido', max_length=100, null=False)
    correo = models.EmailField('Correo', max_length=100, unique=True, null=False)
    contrasena = models.CharField('Contraseña', max_length=100, null=False)
    estado = models.BooleanField('Activo', default=True)

    def _str_(self):
        return str(self.id)+'-'+self.nombre + '-' + self.apellido+'-'+self.correo

class Administrador(models.Model):
    nombre = models.CharField('Nombre', max_length=100, null=False)
    apellido = models.CharField('Apellido', max_length=100, null=False)
    correo = models.EmailField('Correo', max_length=100, unique=True, null=False)
    contrasena = models.CharField('Contraseña', max_length=100, null=False)
    estado = models.BooleanField('Activo', default=True)

    def _str_(self):
        return str(self.id)+'-'+self.nombre + '-' + self.apellido+'-'+self.correo