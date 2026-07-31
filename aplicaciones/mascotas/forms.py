from django import forms

from .models import Mascota, ReportePerdido, ReporteRescatado, SolicitudAdopcion


class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['nombre', 'especie', 'raza', 'edad', 'tamano', 'sexo', 'color', 'ciudad', 'descripcion', 'estado', 'foto_principal']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la mascota'}),
            'especie': forms.Select(attrs={'class': 'form-select'}),
            'raza': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Labrador'}),
            'edad': forms.Select(attrs={'class': 'form-select'}),
            'tamano': forms.Select(attrs={'class': 'form-select'}),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: blanco con manchas'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ciudad o zona'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Cuéntanos su historia y personalidad'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'foto_principal': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class ReportePerdidoForm(forms.ModelForm):
    class Meta:
        model = ReportePerdido
        fields = ['nombre', 'especie', 'raza', 'color', 'descripcion', 'foto', 'ultima_ubicacion', 'ciudad', 'latitud', 'longitud', 'fecha_perdida', 'recompensa', 'contacto']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la mascota'}),
            'especie': forms.Select(attrs={'class': 'form-select'}),
            'raza': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Señas particulares'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'ultima_ubicacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Plaza principal, zona norte'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'latitud': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_latitud', 'step': 'any'}),
            'longitud': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_longitud', 'step': 'any'}),
            'fecha_perdida': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'recompensa': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'contacto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono adicional (opcional)'}),
        }


class ReporteRescatadoForm(forms.ModelForm):
    class Meta:
        model = ReporteRescatado
        fields = ['especie', 'color', 'descripcion', 'foto', 'ciudad', 'ubicacion', 'fecha_rescate', 'estado']
        widgets = {
            'especie': forms.Select(attrs={'class': 'form-select'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe su estado al ser encontrado'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: calle Comercio, entre 1 y 2'}),
            'fecha_rescate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }


class SolicitudAdopcionForm(forms.ModelForm):
    class Meta:
        model = SolicitudAdopcion
        fields = ['mensaje', 'experiencia']
        widgets = {
            'mensaje': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Cuéntanos por qué quieres darle un hogar'}),
            'experiencia': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '¿Ya has tenido mascotas antes? (opcional)'}),
        }
