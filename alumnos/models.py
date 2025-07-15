from django.db import models

class Curso(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Alumno(models.Model):
    nombre_completo = models.CharField(max_length=255)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return self.nombre_completo
