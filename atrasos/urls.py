from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar_atraso, name='registrar_atraso'),
    path('listar/', views.listar_atrasos, name='listar_atrasos'),
    path('editar/<int:atraso_id>/', views.editar_atraso, name='editar_atraso'),
    path('eliminar/<int:atraso_id>/', views.eliminar_atraso, name='eliminar_atraso'),
    
]
