import datetime

from django import forms

from .models import Cita, Servicio


class CitaForm(forms.ModelForm):
    def __init__(self, *args, usuario=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['servicio'].queryset = Servicio.objects.filter(activo=True)
        if usuario:
            self.fields['mascota'].queryset = usuario.mascotas.all()

    class Meta:
        model = Cita
        fields = ['servicio', 'mascota', 'fecha', 'hora', 'notas']
        widgets = {
            'servicio': forms.Select(attrs={'class': 'form-select'}),
            'mascota': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'min': datetime.date.today().isoformat()}),
            'hora': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Comentarios adicionales (opcional)'}),
        }