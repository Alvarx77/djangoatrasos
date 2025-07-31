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


from alumnos.models import Alumno  # Ajusta si estás en otra app

class Seguimiento(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    semana = models.IntegerField()
    anio = models.IntegerField()
    acuerdo_con_apoderado = models.BooleanField(default=False)
    compromiso_alumno = models.BooleanField(default=False)
    incumplido = models.BooleanField(default=False)
    veces_incumplido = models.IntegerField(default=0)
    observaciones = models.TextField(blank=True)

    class Meta:
        unique_together = ('alumno', 'semana', 'anio')

    def __str__(self):
        return f"{self.alumno} - Semana {self.semana}/{self.anio}"