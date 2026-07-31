from django.urls import path

from . import views

app_name = 'mascotas'

urlpatterns = [
    path('', views.listado_mascotas, name='listado_mascotas'),
    path('perdidos/', views.listado_perdidos, name='listado_perdidos'),
    path('rescatados/', views.listado_rescatados, name='listado_rescatados'),
    path('registrar/', views.registrar_mascota, name='registrar_mascota'),
    path('perdidos/reportar/', views.reportar_perdida, name='reportar_perdida'),
    path('rescatados/reportar/', views.reportar_rescate, name='reportar_rescate'),
    path('mis-mascotas/', views.mis_mascotas, name='mis_mascotas'),
    path('<int:mascota_id>/', views.detalle_mascota, name='detalle_mascota'),
    path('<int:mascota_id>/editar/', views.editar_mascota, name='editar_mascota'),
    path('<int:mascota_id>/eliminar/', views.eliminar_mascota, name='eliminar_mascota'),
    path('<int:mascota_id>/solicitar-adopcion/', views.solicitar_adopcion, name='solicitar_adopcion'),
]
