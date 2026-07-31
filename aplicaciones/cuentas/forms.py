from django import forms

from .models import Perfil


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['telefono', 'direccion', 'ciudad', 'documento_identidad', 'foto', 'bio', 'tipo_usuario']
        widgets = {
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 70012345'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu dirección'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu ciudad'}),
            'documento_identidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CI o pasaporte'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Cuéntanos sobre ti'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'tipo_usuario': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
            'ciudad': 'Ciudad',
            'documento_identidad': 'Documento de identidad',
            'foto': 'Foto de perfil',
            'bio': 'Sobre mí',
            'tipo_usuario': 'Tipo de usuario',
        }
