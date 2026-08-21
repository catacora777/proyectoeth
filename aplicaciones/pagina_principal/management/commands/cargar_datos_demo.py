from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from aplicaciones.mascotas.models import Mascota, ReportePerdido, ReporteRescatado
from aplicaciones.servicios.models import Servicio


class Command(BaseCommand):
    help = 'Carga datos de ejemplo (servicios, mascotas, perdidos, rescatados) para demostración.'

    def add_arguments(self, parser):
        parser.add_argument('--reiniciar', action='store_true', help='Borra los datos de ejemplo existentes y los vuelve a cargar.')

    def handle(self, *args, **options):
        if options['reiniciar']:
            ReporteRescatado.objects.all().delete()
            ReportePerdido.objects.all().delete()
            Mascota.objects.all().delete()
            Servicio.objects.all().delete()

        usuario, creado = User.objects.get_or_create(
            username='admin',
            defaults={
                'is_superuser': True,
                'is_staff': True,
                'is_active': True,
                'email': 'admin@huellitas.org',
            },
        )
        if creado:
            usuario.set_password('admin123')
            usuario.save()
            self.stdout.write(self.style.SUCCESS('Usuario admin creado.'))
        else:
            self.stdout.write('Usuario admin ya existía.')

        self._cargar_servicios()
        self._cargar_mascotas(usuario)
        self._cargar_perdidos(usuario)
        self._cargar_rescatados(usuario)

        self.stdout.write(self.style.SUCCESS(
            f'Resumen -> Servicios: {Servicio.objects.count()}, '
            f'Mascotas: {Mascota.objects.count()}, '
            f'Perdidos: {ReportePerdido.objects.count()}, '
            f'Rescatados: {ReporteRescatado.objects.count()}'
        ))

    def _cargar_servicios(self):
        if Servicio.objects.exists():
            self.stdout.write('Servicios ya existían; se omiten.')
            return
        datos = [
            ('veterinaria', 'Consulta general', 'Atención médica completa para tu mascota: revisión, diagnóstico y recomendaciones.', 50, 30),
            ('veterinaria', 'Vacunación', 'Aplicación del esquema completo de vacunas según la edad y especie.', 80, 20),
            ('veterinaria', 'Esterilización', 'Cirugía de esterilización segura con seguimiento post-operatorio.', 350, 90),
            ('veterinaria', 'Desparasitación', 'Control de parásitos internos y externos para cachorros y adultos.', 60, 15),
            ('peluqueria', 'Baño y corte', 'Baño, secado, corte de pelo y uñas con productos hipoalergénicos.', 60, 60),
            ('peluqueria', 'Solo baño', 'Baño con shampoo neutro, secado y cepillado.', 40, 45),
            ('peluqueria', 'Corte higiénico', 'Recorte de pelo en zonas sensibles para mantener la higiene.', 45, 30),
            ('guarderia', 'Día completo', 'Cuidado, alimentación y juegos durante todo el día.', 90, 480),
            ('guarderia', 'Medio día', 'Cuidado y atención durante la mañana o la tarde.', 50, 240),
            ('guarderia', 'Guardería nocturna', 'Estadía nocturna con supervisión y alimentación incluida.', 80, 720),
        ]
        for tipo, nombre, descripcion, precio, duracion in datos:
            Servicio.objects.create(tipo=tipo, nombre=nombre, descripcion=descripcion, precio=precio, duracion_minutos=duracion)
        self.stdout.write(self.style.SUCCESS(f'Se cargaron {Servicio.objects.count()} servicios.'))

    def _cargar_mascotas(self, usuario):
        if Mascota.objects.exists():
            self.stdout.write('Mascotas ya existían; se omiten.')
            return
        datos = [
            dict(nombre='Luna', especie='perro', raza='Labrador', edad='joven', tamano='grande', sexo='hembra', color='blanca', ciudad='La Paz', descripcion='Luna es una perra juguetona y cariñosa que busca un hogar con patio. Sabe sentarse y dar la patita.', estado='en_adopcion'),
            dict(nombre='Rocky', especie='perro', raza='Mestizo', edad='adulto', tamano='mediano', sexo='macho', color='marrón', ciudad='El Alto', descripcion='Rocky es tranquilo y leal. Ideal para personas mayores o vida en departamento.', estado='en_adopcion'),
            dict(nombre='Michi', especie='gato', raza='', edad='cachorro', tamano='pequeno', sexo='macho', color='naranja', ciudad='Cochabamba', descripcion='Gatito juguetón de 3 meses, muy sociable y ya usa la caja de arena.', estado='en_adopcion'),
            dict(nombre='Canela', especie='gato', raza='Siamés', edad='adulto', tamano='pequeno', sexo='hembra', color='crema', ciudad='Santa Cruz', descripcion='Canela es cariñosa y le encanta estar en el regazo. Vacunada y esterilizada.', estado='en_adopcion'),
        ]
        for mascota in datos:
            Mascota.objects.create(usuario=usuario, **mascota)
        self.stdout.write(self.style.SUCCESS(f'Se cargaron {Mascota.objects.count()} mascotas.'))

    def _cargar_perdidos(self, usuario):
        if ReportePerdido.objects.exists():
            self.stdout.write('Perdidos ya existían; se omiten.')
            return
        datos = [
            dict(nombre='Toby', especie='perro', raza='Beagle', color='tricolor', descripcion='Collar azul, muy amigable. Se perdió cerca del parque.', ultima_ubicacion='Parque Urbano Central', ciudad='La Paz', latitud='-16.499100', longitud='-68.150000', fecha_perdida='2026-08-10', contacto='71234567'),
            dict(nombre='Nina', especie='gato', raza='', color='gris', descripcion='Ojos verdes, temerosa. Responde al nombre.', ultima_ubicacion='Zona Sopocachi', ciudad='La Paz', latitud='-16.502000', longitud='-68.128000', fecha_perdida='2026-08-12', recompensa=150, contacto='72345678'),
            dict(nombre='Max', especie='perro', raza='Poodle', color='blanco', descripcion='Corte de león, usa chapita dorada.', ultima_ubicacion='Zona Sur, calle 10', ciudad='La Paz', latitud='-16.538000', longitud='-68.070000', fecha_perdida='2026-08-14', recompensa=300, contacto='73456789'),
        ]
        for perdido in datos:
            ReportePerdido.objects.create(usuario=usuario, **perdido)
        self.stdout.write(self.style.SUCCESS(f'Se cargaron {ReportePerdido.objects.count()} reportes de perdidos.'))

    def _cargar_rescatados(self, usuario):
        if ReporteRescatado.objects.exists():
            self.stdout.write('Rescatados ya existían; se omiten.')
            return
        datos = [
            dict(especie='perro', color='negro', descripcion='Encontrado en la carretera con una herida en la pata, ya atendido por el veterinario.', ciudad='El Alto', ubicacion='Av. Juan Pablo II', fecha_rescate='2026-08-09', estado='rescatado'),
            dict(especie='gato', color='blanco y negro', descripcion='Cachorro abandonado en una caja, deshidratado pero ya recuperándose.', ciudad='La Paz', ubicacion='Calle Comercio', fecha_rescate='2026-08-11', estado='en_hogar'),
            dict(especie='perro', color='café', descripcion='Perro adulto deambulando solo, se busca a su familia o un hogar temporal.', ciudad='Cochabamba', ubicacion='Plaza 14 de Septiembre', fecha_rescate='2026-08-13', estado='rescatado'),
        ]
        for rescatado in datos:
            ReporteRescatado.objects.create(usuario=usuario, **rescatado)
        self.stdout.write(self.style.SUCCESS(f'Se cargaron {ReporteRescatado.objects.count()} reportes de rescatados.'))