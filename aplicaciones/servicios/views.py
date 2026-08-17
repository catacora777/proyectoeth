import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CitaForm
from .models import Cita, Servicio


def listado_servicios(request):
    servicios = Servicio.objects.filter(activo=True)
    return render(request, 'aplicaciones/servicios/listado_servicios.html', {'servicios': servicios})


def detalle_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id, activo=True)
    return render(request, 'aplicaciones/servicios/detalle_servicio.html', {'servicio': servicio})


@login_required
def agendar_cita(request, servicio_id=None):
    servicio = None
    if servicio_id:
        servicio = get_object_or_404(Servicio, id=servicio_id, activo=True)
    if request.method == 'POST':
        formulario = CitaForm(request.POST, usuario=request.user)
        if formulario.is_valid():
            cita = formulario.save(commit=False)
            cita.usuario = request.user
            if Cita.objects.filter(
                usuario=request.user,
                servicio=cita.servicio,
                mascota=cita.mascota,
                fecha=cita.fecha,
                hora=cita.hora,
                estado__in=['pendiente', 'confirmada'],
            ).exists():
                messages.warning(request, 'Ya tienes una cita con ese servicio, fecha y hora.')
                return render(request, 'aplicaciones/servicios/agendar_cita.html', {'formulario': formulario})
            cita.save()
            messages.success(request, 'Tu cita se agendó correctamente. Espera la confirmación.')
            return redirect('servicios:mis_citas')
    else:
        formulario = CitaForm(usuario=request.user)
        if servicio:
            formulario.fields['servicio'].initial = servicio.id
    return render(request, 'aplicaciones/servicios/agendar_cita.html', {'formulario': formulario, 'servicio': servicio})


@login_required
def mis_citas(request):
    citas = Cita.objects.filter(usuario=request.user)
    return render(request, 'aplicaciones/servicios/mis_citas.html', {'citas': citas})


@login_required
def cancelar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id, usuario=request.user)
    if cita.estado in ['pendiente', 'confirmada']:
        cita.estado = 'cancelada'
        cita.save()
        messages.success(request, 'Tu cita se canceló correctamente.')
    else:
        messages.warning(request, 'Esta cita ya no se puede cancelar.')
    return redirect('servicios:mis_citas')