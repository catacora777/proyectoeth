from django.contrib import admin

from .models import Cita, Servicio


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'precio', 'duracion_minutos', 'activo', 'fecha_registro')
    list_filter = ('tipo', 'activo')
    search_fields = ('nombre', 'descripcion')


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'servicio', 'mascota', 'fecha', 'hora', 'estado', 'fecha_registro')
    list_filter = ('estado', 'fecha', 'servicio__tipo')
    search_fields = ('usuario__username', 'usuario__email', 'servicio__nombre', 'mascota__nombre')
    readonly_fields = ('usuario', 'servicio', 'mascota', 'fecha', 'hora', 'notas', 'fecha_registro')
    list_editable = ('estado',)