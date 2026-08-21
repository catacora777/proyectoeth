import datetime

from django import forms

from .models import Alerta, ListaVerificacion, Visita


class VisitaForm(forms.ModelForm):
    class Meta:
        model = Visita
        fields = ['tipo', 'fecha_programada', 'notas']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'fecha_programada': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ListaVerificacionForm(forms.ModelForm):
    class Meta:
        model = ListaVerificacion
        fields = ['condicion_vivienda', 'alimentacion_adecuada', 'agua_disponible', 'atencion_veterinaria', 'identificacion_mascota', 'socializacion', 'comportamiento', 'observaciones', 'aprobado']
        widgets = {
            'condicion_vivienda': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'alimentacion_adecuada': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'agua_disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'atencion_veterinaria': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'identificacion_mascota': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'socializacion': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'comportamiento': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'aprobado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class AlertaForm(forms.ModelForm):
    class Meta:
        model = Alerta
        fields = ['tipo', 'prioridad', 'mensaje']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'prioridad': forms.Select(attrs={'class': 'form-select'}),
            'mensaje': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
