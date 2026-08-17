from django.urls import path

from . import views

app_name = 'servicios'

urlpatterns = [
    path('', views.listado_servicios, name='listado_servicios'),
    path('mis-citas/', views.mis_citas, name='mis_citas'),
    path('<int:servicio_id>/', views.detalle_servicio, name='detalle_servicio'),
    path('<int:servicio_id>/agendar/', views.agendar_cita, name='agendar_cita'),
    path('citas/<int:cita_id>/cancelar/', views.cancelar_cita, name='cancelar_cita'),
]