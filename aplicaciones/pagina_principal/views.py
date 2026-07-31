from django.shortcuts import render

from aplicaciones.mascotas.models import Mascota, ReportePerdido


def inicio(request):
    mascotas_recientes = Mascota.objects.filter(estado='en_adopcion')[:6]
    perdidos_recientes = ReportePerdido.objects.filter(estado='perdido')[:3]
    return render(request, 'aplicaciones/pagina_principal/inicio.html', {
        'mascotas_recientes': mascotas_recientes,
        'perdidos_recientes': perdidos_recientes,
    })
