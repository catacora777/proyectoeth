from django.urls import path

from . import views

app_name = 'cuentas'

urlpatterns = [
    path('', views.mi_perfil, name='mi_perfil'),
    path('editar/', views.editar_perfil, name='editar_perfil'),
    path('<str:username>/', views.perfil_publico, name='perfil_publico'),
]
