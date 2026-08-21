from django.conf import settings
from django.db import models
from django.utils import timezone


class Seguimiento(models.Model):
    ESTADOS = [
        ('activo', 'Activo'),
        ('finalizado', 'Finalizado'),
        ('alertado', 'Alertado'),
        ('cancelado', 'Cancelado'),
    ]

    solicitud = models.OneToOneField('mascotas.SolicitudAdopcion', on_delete=models.CASCADE, related_name='seguimiento', verbose_name='Solicitud de adopción')
    mascota = models.ForeignKey('mascotas.Mascota', on_delete=models.CASCADE, related_name='seguimientos', verbose_name='Mascota')
    adoptante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seguimientos', verbose_name='Adoptante')
    fecha_inicio = models.DateField(auto_now_add=True, verbose_name='Fecha de inicio')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='activo', verbose_name='Estado')
    observaciones_generales = models.TextField(blank=True, verbose_name='Observaciones generales')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    class Meta:
        verbose_name = 'Seguimiento post-adopción'
        verbose_name_plural = 'Seguimientos post-adopción'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f'{self.adoptante.username} -> {self.mascota.nombre} ({self.get_estado_display()})'


class Visita(models.Model):
    ESTADOS = [
        ('programada', 'Programada'),
        ('realizada', 'Realizada'),
        ('cancelada', 'Cancelada'),
        ('reprogramada', 'Reprogramada'),
    ]

    TIPOS = [
        ('presencial', 'Presencial'),
        ('virtual', 'Virtual'),
        ('telefonica', 'Telefónica'),
    ]

    seguimiento = models.ForeignKey(Seguimiento, on_delete=models.CASCADE, related_name='visitas', verbose_name='Seguimiento')
    responsable = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Responsable')
    tipo = models.CharField(max_length=20, choices=TIPOS, verbose_name='Tipo de visita')
    fecha_programada = models.DateTimeField(verbose_name='Fecha programada')
    fecha_realizada = models.DateTimeField(null=True, blank=True, verbose_name='Fecha realizada')
    notas = models.TextField(blank=True, verbose_name='Notas')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='programada', verbose_name='Estado')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')

    class Meta:
        verbose_name = 'Visita'
        verbose_name_plural = 'Visitas'
        ordering = ['fecha_programada']

    def __str__(self):
        return f'{self.seguimiento.mascota.nombre} - {self.get_tipo_display()} el {self.fecha_programada:%d/%m/%Y}'


class ListaVerificacion(models.Model):
    visita = models.OneToOneField(Visita, on_delete=models.CASCADE, related_name='lista_verificacion', verbose_name='Visita')
    condicion_vivienda = models.BooleanField(default=False, verbose_name='Condición de vivienda adecuada')
    alimentacion_adecuada = models.BooleanField(default=False, verbose_name='Alimentación adecuada')
    agua_disponible = models.BooleanField(default=False, verbose_name='Agua disponible')
    atencion_veterinaria = models.BooleanField(default=False, verbose_name='Atención veterinaria al día')
    identificacion_mascota = models.BooleanField(default=False, verbose_name='Identificación (collar/microchip)')
    socializacion = models.BooleanField(default=False, verbose_name='Socialización adecuada')
    comportamiento = models.BooleanField(default=False, verbose_name='Comportamiento sin signos de maltrato')
    observaciones = models.TextField(blank=True, verbose_name='Observaciones')
    aprobado = models.BooleanField(default=False, verbose_name='Aprobado')
    fecha_verificacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de verificación')

    class Meta:
        verbose_name = 'Lista de verificación'
        verbose_name_plural = 'Listas de verificación'

    def __str__(self):
        return f'Verificación de {self.visita}'

    def esta_aprobado(self):
        return all([
            self.condicion_vivienda,
            self.alimentacion_adecuada,
            self.agua_disponible,
            self.atencion_veterinaria,
            self.identificacion_mascota,
            self.socializacion,
            self.comportamiento,
        ]) and self.aprobado


class Alerta(models.Model):
    TIPOS = [
        ('visita_vencida', 'Visita vencida'),
        ('visita_proxima', 'Visita próxima'),
        ('checklist_no_aprobado', 'Checklist no aprobado'),
        ('maltrato_sospechoso', 'Maltrato sospechoso'),
        ('mascota_perdida', 'Mascota perdida'),
        ('otro', 'Otro'),
    ]

    PRIORIDADES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('critica', 'Crítica'),
    ]

    seguimiento = models.ForeignKey(Seguimiento, on_delete=models.CASCADE, related_name='alertas', verbose_name='Seguimiento')
    tipo = models.CharField(max_length=30, choices=TIPOS, verbose_name='Tipo')
    prioridad = models.CharField(max_length=20, choices=PRIORIDADES, default='media', verbose_name='Prioridad')
    mensaje = models.TextField(blank=True, verbose_name='Mensaje')
    leida = models.BooleanField(default=False, verbose_name='Leída')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    fecha_resuelta = models.DateTimeField(null=True, blank=True, verbose_name='Fecha resuelta')

    class Meta:
        verbose_name = 'Alerta'
        verbose_name_plural = 'Alertas'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f'{self.get_tipo_display()} - {self.seguimiento.mascota.nombre}'

    def marcar_leida(self):
        self.leida = True
        self.fecha_resuelta = timezone.now()
        self.save()
