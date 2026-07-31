from django.contrib import admin

from .models import FotoMascota, Mascota, ReportePerdido, ReporteRescatado, SolicitudAdopcion


class FotoMascotaInline(admin.TabularInline):
    model = FotoMascota
    extra = 1


class SolicitudAdopcionInline(admin.TabularInline):
    model = SolicitudAdopcion
    extra = 0
    readonly_fields = ('mensaje', 'experiencia', 'fecha_solicitud')


@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'especie', 'raza', 'edad', 'tamano', 'sexo', 'estado', 'ciudad', 'usuario', 'fecha_registro')
    list_filter = ('especie', 'edad', 'tamano', 'sexo', 'estado', 'ciudad')
    search_fields = ('nombre', 'raza', 'color', 'descripcion', 'ciudad', 'usuario__username')
    inlines = [FotoMascotaInline, SolicitudAdopcionInline]


@admin.register(FotoMascota)
class FotoMascotaAdmin(admin.ModelAdmin):
    list_display = ('mascota', 'imagen', 'orden')
    list_filter = ('mascota',)
    search_fields = ('mascota__nombre',)


@admin.register(ReportePerdido)
class ReportePerdidoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'especie', 'raza', 'ciudad', 'fecha_perdida', 'estado', 'usuario', 'fecha_registro')
    list_filter = ('especie', 'estado', 'ciudad')
    search_fields = ('nombre', 'raza', 'color', 'ultima_ubicacion', 'usuario__username')


@admin.register(ReporteRescatado)
class ReporteRescatadoAdmin(admin.ModelAdmin):
    list_display = ('especie', 'color', 'ciudad', 'fecha_rescate', 'estado', 'usuario', 'fecha_registro')
    list_filter = ('especie', 'estado', 'ciudad')
    search_fields = ('color', 'descripcion', 'ubicacion', 'usuario__username')


@admin.register(SolicitudAdopcion)
class SolicitudAdopcionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'mascota', 'estado', 'fecha_solicitud')
    list_filter = ('estado', 'fecha_solicitud')
    search_fields = ('usuario__username', 'mascota__nombre', 'mensaje')
    readonly_fields = ('usuario', 'mascota', 'mensaje', 'experiencia', 'fecha_solicitud')
