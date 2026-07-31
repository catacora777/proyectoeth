from django.urls import path
from . import views

app_name = 'pagina_principal'

urlpatterns = [
    path('', views.inicio, name='inicio'),
]
