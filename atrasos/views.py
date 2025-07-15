from django.shortcuts import render, get_object_or_404, redirect
from .models import Atraso  # ✅ Correcto
from alumnos.models import Alumno, Curso
from django.utils import timezone
from django.contrib import messages
from django.utils.timezone import localtime
from datetime import datetime, time, timedelta
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils.dateparse import parse_date
from atrasos.models import Atraso
from alumnos.models import Alumno, Curso
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.messages import get_messages


def logout_view(request):
    logout(request)

    # Elimina todos los mensajes que quedaron en la sesión
    list(get_messages(request))

    return redirect('/?logout=1')



@login_required
def registrar_atraso(request):
    alumnos = Alumno.objects.select_related('curso').all().order_by('nombre_completo')
    cursos = Curso.objects.all().order_by('nombre')
    hora_actual = localtime().strftime('%H:%M')
    errores = []

    if request.method == 'POST':
        alumno_id = request.POST.get('alumno')
        hora_str = request.POST.get('hora_llegada')
        estado = request.POST.get('estado')
        comentario = request.POST.get('comentario')

        if not alumno_id or not hora_str:
            errores.append("Debe seleccionar un alumno y una hora de llegada.")
        else:
            try:
                alumno = Alumno.objects.get(id=alumno_id)
                usar_tolerancia = request.POST.get('usar_tolerancia') == 'on'
                minutos_tolerancia = int(request.POST.get('minutos_tolerancia') or 0)

                fecha_actual = localtime().date()
                hora_entrada = datetime.combine(fecha_actual, time(8, 0))
                if usar_tolerancia:
                    hora_entrada += timedelta(minutes=minutos_tolerancia)

                hora_llegada_dt = datetime.combine(fecha_actual, datetime.strptime(hora_str, '%H:%M').time())

                # Si la hora es menor o igual a la hora de entrada, no se considera atraso
                if hora_llegada_dt <= hora_entrada:
                    errores.append("⏰ El alumno llegó a tiempo. No se considera atraso.")

                # Verificar si ya existe un atraso registrado hoy
                elif Atraso.objects.filter(alumno=alumno, fecha=fecha_actual).exists():
                    errores.append("⚠️ Este alumno ya tiene un atraso registrado hoy.")

                else:
                    minutos_tarde = max(int((hora_llegada_dt - hora_entrada).total_seconds() // 60), 0)

                    Atraso.objects.create(
                        alumno=alumno,
                        fecha=fecha_actual,
                        hora_llegada=hora_llegada_dt.time(),
                        minutos_tarde=minutos_tarde,
                        estado=estado,
                        comentario=comentario,
                        registrado_por=request.user  # <- este campo nuevo
                    )

                    messages.success(request, "✅ Atraso registrado correctamente.")
                    return redirect('listar_atrasos')

            except Alumno.DoesNotExist:
                errores.append("El alumno seleccionado no existe.")
            except ValueError:
                errores.append("La hora ingresada no es válida. Formato esperado: HH:MM.")

    return render(request, 'atrasos/registrar.html', {
        'alumnos': alumnos,
        'cursos': cursos,
        'hora_actual': hora_actual,
        'errores': errores
    })



@login_required
def listar_atrasos(request):
    nombre_filtro = request.GET.get('nombre')
    curso_filtro = request.GET.get('curso')
    fecha_filtro = request.GET.get('fecha')  # nuevo

    atrasos = Atraso.objects.select_related('alumno', 'alumno__curso').order_by('-fecha', '-hora_llegada')

    if nombre_filtro:
        atrasos = atrasos.filter(alumno__id=nombre_filtro)

    if curso_filtro:
        atrasos = atrasos.filter(alumno__curso__id=curso_filtro)

    if fecha_filtro:
        try:
            fecha_obj = parse_date(fecha_filtro)
            if fecha_obj:
                atrasos = atrasos.filter(fecha=fecha_obj)
        except:
            pass  # en caso de formato inválido

    # Paginación (10 registros por página)
    paginator = Paginator(atrasos, 10)
    page_number = request.GET.get('page')
    atrasos_page = paginator.get_page(page_number)

    alumnos = Alumno.objects.select_related('curso').order_by('nombre_completo')
    cursos = Curso.objects.all().order_by('nombre')

    context = {
        'atrasos': atrasos_page,
        'alumnos': alumnos,
        'cursos': cursos,
        'nombre_seleccionado': nombre_filtro,
        'curso_seleccionado': curso_filtro,
        'fecha_seleccionada': fecha_filtro,  # para mantener el valor del input
    }

    return render(request, 'atrasos/listar.html', context)

@login_required
def editar_atraso(request, atraso_id):
    atraso = get_object_or_404(Atraso, id=atraso_id)
    alumnos = Alumno.objects.select_related('curso').order_by('nombre_completo')
    cursos = Curso.objects.all().order_by('nombre')

    if request.method == 'POST':
        alumno_id = request.POST['alumno']
        hora_str = request.POST['hora_llegada']
        estado = request.POST['estado']
        comentario = request.POST['comentario']
        usar_tolerancia = request.POST.get('usar_tolerancia') == 'on'
        minutos_tolerancia = int(request.POST.get('minutos_tolerancia') or 0)

        alumno = Alumno.objects.get(id=alumno_id)
        hora_entrada = datetime.combine(localtime().date(), time(8, 0))

        if usar_tolerancia:
            hora_entrada += timedelta(minutes=minutos_tolerancia)

        hora_llegada_dt = datetime.combine(localtime().date(), datetime.strptime(hora_str, '%H:%M').time())
        minutos_tarde = max(int((hora_llegada_dt - hora_entrada).total_seconds() // 60), 0)

        # Actualiza los campos
        atraso.alumno = alumno
        atraso.hora_llegada = hora_llegada_dt.time()
        atraso.minutos_tarde = minutos_tarde
        atraso.estado = estado
        atraso.comentario = comentario
        atraso.save()

        messages.success(request, "Atraso actualizado correctamente.")
        return redirect('listar_atrasos')

    context = {
        'atraso': atraso,
        'alumnos': alumnos,
        'cursos': cursos,
    }
    return render(request, 'atrasos/editar.html', context)


@login_required
def eliminar_atraso(request, atraso_id):
    atraso = get_object_or_404(Atraso, id=atraso_id)

    if request.method == 'POST':
        atraso.delete()
        messages.success(request, "El atraso fue eliminado correctamente.")

    return redirect('listar_atrasos')
