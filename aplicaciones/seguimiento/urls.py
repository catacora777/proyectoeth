from django.urls import path

from . import views

app_name = 'seguimiento'

urlpatterns = [
    path('', views.listado_seguimientos, name='listado_seguimientos'),
    path('publico/', views.listado_seguimientos_publico, name='listado_seguimientos_publico'),
    path('alertas/', views.mis_alertas, name='mis_alertas'),
    path('alertas/<int:alerta_id>/leer/', views.marcar_alerta_leida, name='marcar_alerta_leida'),
    path('<int:seguimiento_id>/', views.detalle_seguimiento, name='detalle_seguimiento'),
    path('<int:seguimiento_id>/visita/nueva/', views.crear_visita, name='crear_visita'),
    path('visita/<int:visita_id>/realizar/', views.realizar_visita, name='realizar_visita'),
]
