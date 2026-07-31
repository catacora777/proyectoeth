from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .filters import MascotaFilter
from .forms import MascotaForm, ReportePerdidoForm, ReporteRescatadoForm, SolicitudAdopcionForm
from .models import Mascota, ReportePerdido, ReporteRescatado


def listado_mascotas(request):
    filtro = MascotaFilter(request.GET, queryset=Mascota.objects.filter(estado='en_adopcion'))
    return render(request, 'aplicaciones/mascotas/listado_mascotas.html', {'filtro': filtro})


def detalle_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    return render(request, 'aplicaciones/mascotas/detalle_mascota.html', {'mascota': mascota})


@login_required
def registrar_mascota(request):
    if request.method == 'POST':
        formulario = MascotaForm(request.POST, request.FILES)
        if formulario.is_valid():
            mascota = formulario.save(commit=False)
            mascota.usuario = request.user
            mascota.save()
            messages.success(request, 'Tu mascota se registró correctamente.')
            return redirect('mascotas:detalle_mascota', mascota_id=mascota.id)
    else:
        formulario = MascotaForm()
    return render(request, 'aplicaciones/mascotas/formulario_mascota.html', {'formulario': formulario, 'titulo': 'Registrar mascota'})


@login_required
def editar_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id, usuario=request.user)
    if request.method == 'POST':
        formulario = MascotaForm(request.POST, request.FILES, instance=mascota)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'La mascota se actualizó correctamente.')
            return redirect('mascotas:detalle_mascota', mascota_id=mascota.id)
    else:
        formulario = MascotaForm(instance=mascota)
    return render(request, 'aplicaciones/mascotas/formulario_mascota.html', {'formulario': formulario, 'titulo': 'Editar mascota'})


@login_required
def eliminar_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id, usuario=request.user)
    if request.method == 'POST':
        mascota.delete()
        messages.success(request, 'La mascota se eliminó correctamente.')
        return redirect('mascotas:listado_mascotas')
    return render(request, 'aplicaciones/mascotas/confirmar_eliminar_mascota.html', {'mascota': mascota})


@login_required
def solicitar_adopcion(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    if mascota.usuario == request.user:
        messages.warning(request, 'No puedes solicitar la adopción de tu propia mascota.')
        return redirect('mascotas:detalle_mascota', mascota_id=mascota.id)
    if mascota.estado != 'en_adopcion':
        messages.warning(request, 'Esta mascota no está disponible para adopción.')
        return redirect('mascotas:detalle_mascota', mascota_id=mascota.id)
    if mascota.solicitudes.filter(usuario=request.user).exists():
        messages.info(request, 'Ya enviaste una solicitud para esta mascota.')
        return redirect('mascotas:detalle_mascota', mascota_id=mascota.id)
    if request.method == 'POST':
        formulario = SolicitudAdopcionForm(request.POST)
        if formulario.is_valid():
            solicitud = formulario.save(commit=False)
            solicitud.usuario = request.user
            solicitud.mascota = mascota
            solicitud.save()
            messages.success(request, 'Tu solicitud de adopción se envió correctamente.')
            return redirect('mascotas:detalle_mascota', mascota_id=mascota.id)
    else:
        formulario = SolicitudAdopcionForm()
    return render(request, 'aplicaciones/mascotas/solicitud_adopcion.html', {'formulario': formulario, 'mascota': mascota})


@login_required
def mis_mascotas(request):
    mascotas = Mascota.objects.filter(usuario=request.user)
    return render(request, 'aplicaciones/mascotas/mis_mascotas.html', {'mascotas': mascotas})


def listado_perdidos(request):
    perdidos = ReportePerdido.objects.filter(estado='perdido')
    return render(request, 'aplicaciones/mascotas/listado_perdidos.html', {'perdidos': perdidos})


@login_required
def reportar_perdida(request):
    if request.method == 'POST':
        formulario = ReportePerdidoForm(request.POST, request.FILES)
        if formulario.is_valid():
            reporte = formulario.save(commit=False)
            reporte.usuario = request.user
            reporte.save()
            messages.success(request, 'El reporte de mascota perdida se publicó correctamente.')
            return redirect('mascotas:listado_perdidos')
    else:
        formulario = ReportePerdidoForm()
    return render(request, 'aplicaciones/mascotas/formulario_perdido.html', {'formulario': formulario})


def listado_rescatados(request):
    rescatados = ReporteRescatado.objects.all()
    return render(request, 'aplicaciones/mascotas/listado_rescatados.html', {'rescatados': rescatados})


@login_required
def reportar_rescate(request):
    if request.method == 'POST':
        formulario = ReporteRescatadoForm(request.POST, request.FILES)
        if formulario.is_valid():
            reporte = formulario.save(commit=False)
            reporte.usuario = request.user
            reporte.save()
            messages.success(request, 'El reporte de animal rescatado se publicó correctamente.')
            return redirect('mascotas:listado_rescatados')
    else:
        formulario = ReporteRescatadoForm()
    return render(request, 'aplicaciones/mascotas/formulario_rescatado.html', {'formulario': formulario})
