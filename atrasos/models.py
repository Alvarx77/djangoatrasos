from django.db import models
from django.contrib.auth.models import User
from alumnos.models import Alumno

class Atraso(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('justificado', 'Justificado'),
        ('no_justificado', 'No Justificado'),
    ]

    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='atrasos')
    fecha = models.DateField()
    hora_llegada = models.TimeField()
    minutos_tarde = models.PositiveIntegerField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    comentario = models.TextField(blank=True)
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Registrado por")

    class Meta:
        ordering = ['-fecha', 'alumno__nombre_completo']
        verbose_name = "Atraso"
        verbose_name_plural = "Atrasos"
        unique_together = ('alumno', 'fecha')  # Evita registros duplicados del mismo alumno el mismo día

    def __str__(self):
        return f"{self.alumno.nombre_completo} - {self.fecha.strftime('%d/%m/%Y')}"
