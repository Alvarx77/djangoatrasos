from django import forms
from .models import Alumno, Seguimiento

class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ['nombre_completo', 'curso']


class SeguimientoForm(forms.ModelForm):
    class Meta:
        model = Seguimiento
        fields = ['acuerdo_con_apoderado', 'compromiso_alumno', 'observaciones']
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 2}),
        }