from django.conf import settings
from django.db import models

from aplicaciones.mascotas.models import Mascota


class Servicio(models.Model):
    TIPOS = [
        ('veterinaria', 'Veterinaria'),
        ('peluqueria', 'Peluquería'),
        ('guarderia', 'Guardería'),
    ]

    tipo = models.CharField(max_length=20, choices=TIPOS, verbose_name='Tipo')
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    descripcion = models.TextField(verbose_name='Descripción')
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio (Bs)')
    duracion_minutos = models.PositiveIntegerField(verbose_name='Duración (minutos)')
    foto = models.ImageField(upload_to='servicios/', blank=True, null=True, verbose_name='Foto')
    activo = models.BooleanField(default=True, verbose_name='Activo')
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')

    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        ordering = ['tipo', 'nombre']

    def __str__(self):
        return f'{self.nombre} ({self.get_tipo_display()})'


class Cita(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='citas', verbose_name='Usuario')
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='citas', verbose_name='Servicio')
    mascota = models.ForeignKey(Mascota, on_delete=models.SET_NULL, null=True, blank=True, related_name='citas', verbose_name='Mascota')
    fecha = models.DateField(verbose_name='Fecha')
    hora = models.TimeField(verbose_name='Hora')
    notas = models.TextField(blank=True, verbose_name='Notas')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente', verbose_name='Estado')
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')

    class Meta:
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'
        ordering = ['-fecha', '-hora']

    def __str__(self):
        mascota = f' - {self.mascota.nombre}' if self.mascota else ''
        return f'{self.usuario.username}: {self.servicio.nombre}{mascota} el {self.fecha} {self.hora}'