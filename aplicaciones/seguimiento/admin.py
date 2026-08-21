from django.contrib import admin

from .models import Alerta, ListaVerificacion, Seguimiento, Visita


class VisitaInline(admin.TabularInline):
    model = Visita
    extra = 0


class AlertaInline(admin.TabularInline):
    model = Alerta
    extra = 0
    readonly_fields = ('fecha_creacion',)


class ListaVerificacionInline(admin.StackedInline):
    model = ListaVerificacion
    extra = 0


@admin.register(Seguimiento)
class SeguimientoAdmin(admin.ModelAdmin):
    list_display = ('mascota', 'adoptante', 'estado', 'fecha_inicio', 'fecha_creacion')
    list_filter = ('estado', 'fecha_inicio')
    search_fields = ('mascota__nombre', 'adoptante__username')
    inlines = [VisitaInline, AlertaInline]


@admin.register(Visita)
class VisitaAdmin(admin.ModelAdmin):
    list_display = ('seguimiento', 'tipo', 'estado', 'fecha_programada', 'responsable')
    list_filter = ('estado', 'tipo')
    search_fields = ('seguimiento__mascota__nombre', 'responsable__username')
    inlines = [ListaVerificacionInline]


@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ('seguimiento', 'tipo', 'prioridad', 'leida', 'fecha_creacion')
    list_filter = ('tipo', 'prioridad', 'leida')
    search_fields = ('seguimiento__mascota__nombre', 'mensaje')
