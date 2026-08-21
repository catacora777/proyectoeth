from django.apps import AppConfig


class SeguimientoConfig(AppConfig):
    name = 'aplicaciones.seguimiento'

    def ready(self):
        import aplicaciones.seguimiento.signals
