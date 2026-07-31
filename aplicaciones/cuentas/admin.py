from django.contrib import admin
from django.contrib.auth.models import User

from .models import Perfil


class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'Perfil'


class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    inlines = [PerfilInline]


admin.site.unregister(User)
admin.site.register(User, UsuarioAdmin)


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'telefono', 'ciudad', 'tipo_usuario', 'fecha_registro')
    list_filter = ('tipo_usuario', 'ciudad')
    search_fields = ('usuario__username', 'usuario__email', 'telefono', 'ciudad', 'documento_identidad')
