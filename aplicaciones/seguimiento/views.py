from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import AlertaForm, ListaVerificacionForm, VisitaForm
from .models import Alerta, ListaVerificacion, Seguimiento, Visita


def _es_voluntario_o_admin(usuario):
    return usuario.is_authenticated and (usuario.is_staff or usuario.groups.filter(name='voluntario').exists())


def _requerir_voluntario(vista):
    def envoltura(request, *args, **kwargs):
        if not _es_voluntario_o_admin(request.user):
            messages.warning(request, 'Acceso solo para voluntarios y administradores.')
            return redirect('pagina_principal:inicio')
        return vista(request, *args, **kwargs)
    return envoltura


@login_required
@_requerir_voluntario
def listado_seguimientos(request):
    seguimientos = Seguimiento.objects.select_related('adoptante', 'mascota').all()
    estado = request.GET.get('estado')
    if estado:
        seguimientos = seguimientos.filter(estado=estado)
    busqueda = request.GET.get('q')
    if busqueda:
        seguimientos = seguimientos.filter(models.Q(adoptante__username__icontains=busqueda) | models.Q(mascota__nombre__icontains=busqueda))
    return render(request, 'aplicaciones/seguimiento/listado_seguimientos.html', {'seguimientos': seguimientos, 'estado': estado, 'busqueda': busqueda})


@login_required
@_requerir_voluntario
def detalle_seguimiento(request, seguimiento_id):
    seguimiento = get_object_or_404(Seguimiento, id=seguimiento_id)
    visitas = seguimiento.visitas.select_related('responsable').all()
    alertas = seguimiento.alertas.filter(leida=False)
    return render(request, 'aplicaciones/seguimiento/detalle_seguimiento.html', {'seguimiento': seguimiento, 'visitas': visitas, 'alertas': alertas})


@login_required
@_requerir_voluntario
def crear_visita(request, seguimiento_id):
    seguimiento = get_object_or_404(Seguimiento, id=seguimiento_id)
    if request.method == 'POST':
        formulario = VisitaForm(request.POST)
        if formulario.is_valid():
            visita = formulario.save(commit=False)
            visita.seguimiento = seguimiento
            visita.responsable = request.user
            visita.save()
            messages.success(request, 'Visita programada correctamente.')
            return redirect('seguimiento:detalle_seguimiento', seguimiento_id=seguimiento.id)
    else:
        formulario = VisitaForm()
    return render(request, 'aplicaciones/seguimiento/formulario_visita.html', {'formulario': formulario, 'seguimiento': seguimiento})


@login_required
@_requerir_voluntario
def realizar_visita(request, visita_id):
    visita = get_object_or_404(Visita, id=visita_id)
    if visita.lista_verificacion if hasattr(visita, 'lista_verificacion') else False:
        lista = visita.lista_verificacion
    else:
        lista = None
    if request.method == 'POST':
        formulario = ListaVerificacionForm(request.POST, instance=lista)
        if formulario.is_valid():
            verificacion = formulario.save(commit=False)
            verificacion.visita = visita
            verificacion.save()
            visita.estado = 'realizada'
            visita.fecha_realizada = timezone.now()
            visita.save()
            if not verificacion.esta_aprobado():
                Alerta.objects.create(seguimiento=visita.seguimiento, tipo='checklist_no_aprobado', prioridad='alta', mensaje=f'Checklist no aprobado en visita del {visita.fecha_programada:%d/%m/%Y}.')
            messages.success(request, 'Visita registrada.')
            return redirect('seguimiento:detalle_seguimiento', seguimiento_id=visita.seguimiento.id)
    else:
        formulario = ListaVerificacionForm(instance=lista)
    return render(request, 'aplicaciones/seguimiento/formulario_verificacion.html', {'formulario': formulario, 'visita': visita})


@login_required
@_requerir_voluntario
def mis_alertas(request):
    alertas = Alerta.objects.filter(leida=False).select_related('seguimiento__mascota', 'seguimiento__adoptante').order_by('-fecha_creacion')
    return render(request, 'aplicaciones/seguimiento/listado_alertas.html', {'alertas': alertas})


@login_required
@_requerir_voluntario
def marcar_alerta_leida(request, alerta_id):
    alerta = get_object_or_404(Alerta, id=alerta_id)
    if request.method == 'POST':
        alerta.leida = True
        alerta.fecha_resuelta = timezone.now()
        alerta.save()
        messages.success(request, 'Alerta marcada como leída.')
    return redirect('seguimiento:mis_alertas')


def listado_seguimientos_publico(request):
    seguimientos = Seguimiento.objects.filter(estado='activo').select_related('adoptante', 'mascota')
    return render(request, 'aplicaciones/seguimiento/listado_publico.html', {'seguimientos': seguimientos})
