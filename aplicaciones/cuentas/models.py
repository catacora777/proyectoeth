from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Perfil(models.Model):
    TIPOS_USUARIO = [
        ('adoptante', 'Adoptante'),
        ('rescatista', 'Rescatista'),
        ('voluntario', 'Voluntario'),
        ('colaborador', 'Colaborador'),
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil', verbose_name='Usuario')
    telefono = models.CharField(max_length=20, blank=True, verbose_name='Teléfono')
    direccion = models.CharField(max_length=255, blank=True, verbose_name='Dirección')
    ciudad = models.CharField(max_length=100, blank=True, verbose_name='Ciudad')
    documento_identidad = models.CharField(max_length=30, blank=True, verbose_name='Documento de identidad')
    foto = models.ImageField(upload_to='perfiles/', blank=True, null=True, verbose_name='Foto de perfil')
    tipo_usuario = models.CharField(max_length=20, choices=TIPOS_USUARIO, default='adoptante', verbose_name='Tipo de usuario')
    bio = models.TextField(max_length=500, blank=True, verbose_name='Sobre mí')
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

    def __str__(self):
        return f'Perfil de {self.usuario.username}'


@receiver(post_save, sender=User)
def crear_perfil_al_crear_usuario(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.get_or_create(usuario=instance)


@receiver(post_save, sender=User)
def guardar_perfil_de_usuario(sender, instance, **kwargs):
    if hasattr(instance, 'perfil'):
        instance.perfil.save()
