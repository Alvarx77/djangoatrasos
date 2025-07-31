from django.urls import path
from . import views
from .views import home

urlpatterns = [
    path('', home, name='home'),
    path('cargar_excel/', views.cargar_excel_sige, name='cargar_excel'),
    path('alumnos/', views.lista_alumnos, name='lista_alumnos'),
    path('alertas/', views.alertas_atrasos, name='alertas_atrasos'),
    path('dashboard/', views.dashboard_admin, name='dashboard_admin'),
    path('estadisticas/', views.estadisticas, name='ver_estadisticas'),
    path('exportar-excel/', views.exportar_excel, name='exportar_excel'),
    path('opciones-admin/', views.opciones_admin, name='opciones_admin'),
    path('iniciar-nuevo-anio/', views.iniciar_nuevo_anio, name='iniciar_nuevo_anio'),
    path('alumnos/agregar/', views.agregar_alumno, name='agregar_alumno'),
    path('alumnos/editar/<int:alumno_id>/', views.editar_alumno, name='editar_alumno'),
    path('alumnos/eliminar/<int:alumno_id>/', views.confirmar_eliminar_alumno, name='eliminar_alumno'),
    path('eliminar-base/', views.eliminar_base, name='eliminar_base'),
    path('seguimiento/', views.seguimiento, name='seguimiento'),
    path('seguimiento_individual/<int:alumno_id>/<int:semana>/<int:anio>/', views.seguimiento_individual, name='seguimiento_individual')








]

