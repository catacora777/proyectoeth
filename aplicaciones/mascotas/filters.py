import django_filters
from django.db import models

from .models import Mascota


class MascotaFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='filtrar_busqueda', label='Buscar')
    ciudad = django_filters.CharFilter(lookup_expr='icontains', label='Ciudad')

    class Meta:
        model = Mascota
        fields = ['especie', 'estado', 'tamano', 'edad']

    def filtrar_busqueda(self, queryset, nombre, valor):
        return queryset.filter(
            models.Q(nombre__icontains=valor) |
            models.Q(raza__icontains=valor) |
            models.Q(color__icontains=valor) |
            models.Q(descripcion__icontains=valor)
        )
