from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PerfilForm


@login_required
def mi_perfil(request):
    perfil = request.user.perfil
    return render(request, 'aplicaciones/cuentas/mi_perfil.html', {'perfil': perfil})


@login_required
def editar_perfil(request):
    perfil = request.user.perfil
    if request.method == 'POST':
        formulario = PerfilForm(request.POST, request.FILES, instance=perfil)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Tu perfil se actualizó correctamente.')
            return redirect('cuentas:mi_perfil')
    else:
        formulario = PerfilForm(instance=perfil)
    return render(request, 'aplicaciones/cuentas/editar_perfil.html', {'formulario': formulario})


def perfil_publico(request, username):
    usuario = get_object_or_404(User, username=username)
    perfil = usuario.perfil
    mascotas = usuario.mascotas.filter(estado='en_adopcion')
    return render(request, 'aplicaciones/cuentas/perfil_publico.html', {
        'perfil': perfil,
        'usuario_visible': usuario,
        'mascotas': mascotas,
    })
