from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender='mascotas.SolicitudAdopcion')
def crear_seguimiento_al_aprobar(sender, instance, created, **kwargs):
    if instance.estado == 'aprobada':
        from .models import Seguimiento
        Seguimiento.objects.get_or_create(
            solicitud=instance,
            defaults={
                'mascota': instance.mascota,
                'adoptante': instance.usuario,
            },
        )
