from django.conf import settings
from django.db import models


class Mascota(models.Model):
    ESPECIES = [
        ('perro', 'Perro'),
        ('gato', 'Gato'),
        ('otro', 'Otro'),
    ]
    TAMANOS = [
        ('pequeno', 'Pequeño'),
        ('mediano', 'Mediano'),
        ('grande', 'Grande'),
    ]
    SEXOS = [
        ('macho', 'Macho'),
        ('hembra', 'Hembra'),
    ]
    RANGOS_EDAD = [
        ('cachorro', 'Cachorro'),
        ('joven', 'Joven'),
        ('adulto', 'Adulto'),
    ]
    ESTADOS = [
        ('rescatado', 'Rescatado'),
        ('en_adopcion', 'En adopción'),
        ('adoptado', 'Adoptado'),
    ]

    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    especie = models.CharField(max_length=20, choices=ESPECIES, verbose_name='Especie')
    raza = models.CharField(max_length=100, blank=True, verbose_name='Raza')
    edad = models.CharField(max_length=20, choices=RANGOS_EDAD, verbose_name='Edad')
    tamano = models.CharField(max_length=20, choices=TAMANOS, verbose_name='Tamaño')
    sexo = models.CharField(max_length=20, choices=SEXOS, verbose_name='Sexo')
    color = models.CharField(max_length=100, blank=True, verbose_name='Color')
    descripcion = models.TextField(verbose_name='Descripción')
    ciudad = models.CharField(max_length=100, blank=True, verbose_name='Ciudad')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='rescatado', verbose_name='Estado')
    foto_principal = models.ImageField(upload_to='mascotas/', blank=True, null=True, verbose_name='Foto principal')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mascotas', verbose_name='Usuario')
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')

    class Meta:
        verbose_name = 'Mascota'
        verbose_name_plural = 'Mascotas'
        ordering = ['-fecha_registro']

    def __str__(self):
        return f'{self.nombre} ({self.get_especie_display()})'


class FotoMascota(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='fotos', verbose_name='Mascota')
    imagen = models.ImageField(upload_to='mascotas/', verbose_name='Imagen')
    orden = models.PositiveIntegerField(default=0, verbose_name='Orden')

    class Meta:
        verbose_name = 'Foto de mascota'
        verbose_name_plural = 'Fotos de mascotas'
        ordering = ['orden', 'id']

    def __str__(self):
        return f'Foto de {self.mascota.nombre}'


class ReportePerdido(models.Model):
    ESPECIES = Mascota.ESPECIES
    ESTADOS = [
        ('perdido', 'Perdido'),
        ('encontrado', 'Encontrado'),
    ]

    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    especie = models.CharField(max_length=20, choices=ESPECIES, verbose_name='Especie')
    raza = models.CharField(max_length=100, blank=True, verbose_name='Raza')
    color = models.CharField(max_length=100, blank=True, verbose_name='Color')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    foto = models.ImageField(upload_to='mascotas/perdidos/', blank=True, null=True, verbose_name='Foto')
    ultima_ubicacion = models.CharField(max_length=255, verbose_name='Última ubicación')
    ciudad = models.CharField(max_length=100, blank=True, verbose_name='Ciudad')
    latitud = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name='Latitud')
    longitud = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name='Longitud')
    fecha_perdida = models.DateField(verbose_name='Fecha de pérdida')
    recompensa = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Recompensa (Bs)')
    contacto = models.CharField(max_length=100, blank=True, verbose_name='Contacto extra')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='perdido', verbose_name='Estado')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reportes_perdidos', verbose_name='Usuario')
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')

    class Meta:
        verbose_name = 'Reporte de mascota perdida'
        verbose_name_plural = 'Reportes de mascotas perdidas'
        ordering = ['-fecha_registro']

    def __str__(self):
        return f'{self.nombre} - perdido el {self.fecha_perdida}'


class ReporteRescatado(models.Model):
    ESPECIES = Mascota.ESPECIES
    ESTADOS = [
        ('rescatado', 'Rescatado'),
        ('en_hogar', 'En hogar temporal'),
    ]

    especie = models.CharField(max_length=20, choices=ESPECIES, verbose_name='Especie')
    color = models.CharField(max_length=100, blank=True, verbose_name='Color')
    descripcion = models.TextField(verbose_name='Descripción')
    foto = models.ImageField(upload_to='mascotas/rescatados/', blank=True, null=True, verbose_name='Foto')
    ciudad = models.CharField(max_length=100, blank=True, verbose_name='Ciudad')
    ubicacion = models.CharField(max_length=255, verbose_name='Dónde fue encontrado')
    fecha_rescate = models.DateField(verbose_name='Fecha del rescate')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='rescatado', verbose_name='Estado')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reportes_rescatados', verbose_name='Usuario')
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')

    class Meta:
        verbose_name = 'Reporte de animal rescatado'
        verbose_name_plural = 'Reportes de animales rescatados'
        ordering = ['-fecha_registro']

    def __str__(self):
        return f'{self.get_especie_display()} rescatado en {self.ciudad}'


class SolicitudAdopcion(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='solicitudes_adopcion', verbose_name='Solicitante')
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='solicitudes', verbose_name='Mascota')
    mensaje = models.TextField(verbose_name='¿Por qué quieres adoptar?')
    experiencia = models.TextField(blank=True, verbose_name='Experiencia con mascotas')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente', verbose_name='Estado')
    fecha_solicitud = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de solicitud')

    class Meta:
        verbose_name = 'Solicitud de adopción'
        verbose_name_plural = 'Solicitudes de adopción'
        ordering = ['-fecha_solicitud']

    def __str__(self):
        return f'{self.usuario.username} -> {self.mascota.nombre} ({self.get_estado_display()})'
