from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.urls import reverse
from django.db.models import F

from django.http import JsonResponse

from django.utils import timezone
from django.contrib.auth.models import User

from pathlib import Path
from .forms import *
from .models import *

from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

# Create your views here.

############################################################LOGIN############################################################
# VISTA PARA EL LOGIN
def home_login(request):
    error_message = ""  
    print(Path(__file__).resolve().parent.parent)
    if request.method == 'POST':
        correo = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')

        if correo and contrasena:
            user = authenticate(request, username=correo, password=contrasena)

            if user is not None:
                try:
                    usuario_extendido = user.extendeddata
                    if usuario_extendido.cp:
                        login(request, user)
                        return redirect('tanalitica')
                    else:
                        login(request, user)
                        return redirect('ctalleres')
                except ExtendedData.DoesNotExist:
                    pass
            else:
                error_message = 'Usuario o contraseña incorrecto'  

        if not correo or not contrasena:
            error_message = 'Por favor, complete todos los campos'

    return render(request, 'registration/login.html', {'error_message': error_message})


#PINTAR PÁGINA DE SI ERES TALLER O CLIENTE
def register_option(request):
    return render(request,'registeroption.html')

#VISTA PARA REGISTRAR TALLER
def taller(request):
    error_message = ""
    if request.method == 'POST':
        user_form = createUserForm(request.POST)
        user_profile_form = UserProfileForm(request.POST)
        print(user_form.errors)
        print(user_profile_form.errors)
        if user_form.is_valid() and user_profile_form.is_valid():
            user = user_form.save() 
            profile = user_profile_form.save(commit=False)  
            profile.user = user
            profile.save()
            return redirect('login')
        else:
            error_message = "El usuario que ingresó ya existe intente con otro"
    else:
        user_form = createUserForm()
        user_profile_form = UserProfileForm()

    data_context = {'user_form': user_form, 'user_profile_form': user_profile_form, 'error_message': error_message}
    return render(request, 'taller.html', data_context)

#VISTA PARA REGISTRAR CLIENTE
def cliente(request):
    error_message = ""
    user_form = createUserForm()
    user_profile_form = UserProfileForm()
    data_context = {'user_form': user_form, 'user_profile_form': user_profile_form}
    
    if request.method == 'POST':
        user_form = createUserForm(request.POST)
        user_profile_form = UserProfileForm(request.POST)
        print(user_form.errors)
        print(user_profile_form.errors)
        
        if user_form.is_valid() and user_profile_form.is_valid():
            user = user_form.save() 
            profile = ExtendedData()
            profile.telefono = request.POST['telefono']
            profile.user = user
            profile.save()
            return redirect('login')
        else:
            error_message = "El usuario que ingresó ya existe intente con otro."

    data_context['error_message'] = error_message
    return render(request, 'cliente.html', data_context)

#RECUPERAR COMNTRASEÑA

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

############################################################LOGIN############################################################



############################################################CLIENTES############################################################

#LISTA DE TALLERES
@login_required
def clientes_talleres(request):
    talleres = ExtendedData.objects.exclude(cp__isnull=True).exclude(cp__exact='')
    return render(request, 'clientes_talleres.html', {'talleres': talleres})

#LISTA DE CITAS
@login_required
def clientes_calendario(request):
    citas = ReservaCita.objects.filter(usuario=request.user).annotate(taller_name=F('taller__username'))
    return render(request, 'clientes_calendario.html', {'citas': citas})

#EDITAR PERFIL
@login_required
def clientes_edit(request):
    user = request.user
    extended_data, created = ExtendedData.objects.get_or_create(user=user)
    show_alert = False  
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            correo = form.cleaned_data['email']
            telefono = form.cleaned_data['telefono']
            if created:
                extended_data = ExtendedData.objects.create(user=user, telefono=telefono)
            else:
                extended_data.telefono = telefono
                extended_data.save()
            user.email = correo
            user.save()
            messages.success(request, 'Perfil actualizado correctamente') 
            show_alert = True
    else:
        initial_data = {'telefono': extended_data.telefono} if extended_data else None
        form = UserEditForm(instance=user, initial=initial_data)
    return render(request, 'clientes_edit.html', {'form': form, 'extended_data': extended_data, 'user': user, 'show_alert': show_alert})

#Lista vehículos
@login_required
def clientes_vehiculos(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            vehiculo = form.save(commit=False)
            vehiculo.usuario = request.user
            vehiculo.save()
            return redirect('cvehiculos')
    else:
        form = VehiculoForm()

    vehiculos = Vehiculos.objects.filter(usuario=request.user)

    # Verifica si hay un parámetro "vehicle_deleted" en la URL
    if request.GET.get("vehicle_deleted") == "true":
        messages.success(request, "Vehículo eliminado.")

    return render(request, 'clientes_vehiculos.html', {'form': form, 'vehiculos': vehiculos})

# Eliminación de vehículos
@login_required
def eliminar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculos, pk=vehiculo_id)

    if request.method == "POST":
        vehiculo.delete()
        messages.success(request, "Vehículo eliminado.")

    return redirect('cvehiculos')

#EDITAR VEHÍCULO
@login_required
def actualizar_vehiculo(request, vehiculo_id):
    vehiculo = Vehiculos.objects.get(id=vehiculo_id)

    if request.method == 'POST':
        form = VehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            form.save()
            return redirect('cvehiculos') 
    else:
        form = VehiculoForm(instance=vehiculo)

    return render(request, 'editar_vehiculo.html', {'form': form})


def editar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculos, id=vehiculo_id)
    if request.method == 'POST':
        form = VehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            form.save()
            return redirect('cvehiculos')
    else:
        form = VehiculoForm(instance=vehiculo)

    return render(request, 'nombre_del_template_editar_vehiculo.html', {'form': form})

#PERFIL DE TALLERES
@login_required
def agendar_citas(request, taller_name):
        taller = get_object_or_404(ExtendedData, user__username=taller_name)
        servicios = Service.objects.filter(user=taller.user)
        if request.method == 'POST':
            # Procesa el formulario de creación de opiniones
            try:
                id_taller = User.objects.get(username=taller_name)
                opinion_text = request.POST.get('opinion')
                id_usuario = request.user
                opinion = Opinion(id_taller=id_taller, id_usuario=id_usuario, opinion=opinion_text)
                opinion.save()
                # Realiza el análisis de sentimiento
                credential = AzureKeyCredential("6e222a611092490ca0462c4a0a436616")
                endpoint = "https://lenguajedsccacg.cognitiveservices.azure.com/"
                text_analytics_client = TextAnalyticsClient(endpoint,credential)
                documents = [opinion_text]
                response = text_analytics_client.analyze_sentiment(documents, language="es")
                result = response[0]
                # Después de obtener el resultado del análisis de sentimiento
                sentimiento_mapping = {
                    'positive': 'alegre',
                    'negative': 'triste',
                    'neutral': 'neutro'
                }
                opinion.sentimiento = sentimiento_mapping.get(result.sentiment)
                opinion.save()
                # Guarda el sentimiento en la opinión
                # opinion.sentimiento = result.sentiment
                # opinion.save()
                print("Opinión guardada exitosamente.")
            except Exception as e:
                print("Error al guardar la opinión:", str(e))
        opiniones = Opinion.objects.filter(id_taller=taller.user)
        return render(request, 'citas.html', {'taller': taller, 'servicios': servicios, 'opiniones': opiniones, 'taller_name': taller_name,})

#CONTABILIZAR SENTIMIENTOS
def contar_sentimientos(user):
    opiniones = Opinion.objects.filter(id_taller=user.taller.id)  # Asume que cada usuario tiene un taller relacionado

    total_alegre = opiniones.filter(sentimiento='alegre').count()
    total_triste = opiniones.filter(sentimiento='triste').count()
    total_neutro = opiniones.filter(sentimiento='neutro').count()
    total_comentarios = opiniones.count()
    print(total_alegre)
    print(total_neutro)
    print(total_triste)


    return {
        'alegre': total_alegre,
        'triste': total_triste,
        'neutro': total_neutro,
        'total_comentarios': total_comentarios
    }



def top_comentarios(request, taller):
    # Recuperar opiniones filtradas por el taller
    opiniones = Opinion.objects.filter(id_taller=taller)

    # Obtener top 3 comentarios por sentimiento y ordenados por fecha de creación
    top_comentarios = {
        'alegre': list(opiniones.filter(sentimiento='alegre').order_by('-fecha_creacion')[:3]),
        'triste': list(opiniones.filter(sentimiento='triste').order_by('-fecha_creacion')[:3]),
        'neutro': list(opiniones.filter(sentimiento='neutro').order_by('-fecha_creacion')[:3])
    }

    # Contar sentimientos (asumiendo que tienes una función llamada contar_sentimientos)
    conteo_sentimientos = contar_sentimientos(taller.user)

    # Imprimir el conteo de sentimientos
    print(conteo_sentimientos)

    # Renderizar la plantilla con los datos
    return render(request, 'taller_analitica.html',
                  {'conteo_sentimientos': conteo_sentimientos, 
                   'top_3_comentarios': top_comentarios})




#RESERVAR LA CITA
@login_required
def reservar_cita(request, taller_name):
    taller = get_object_or_404(ExtendedData, user__username=taller_name)  
    
    if request.method == 'POST':
        fecha_entrega = request.POST.get('fecha_entrega')
        hora_entrega = request.POST.get('hora_entrega')
        servicio_id = request.POST.get('servicio')
        vehiculo_id = request.POST.get('vehiculo') 
        vehiculo_id = int(vehiculo_id)
        
        vehiculo = Vehiculos.objects.get(id=vehiculo_id)
        

        ReservaCita.objects.create(
            taller=taller.user,
            usuario=request.user,
            fecha=fecha_entrega,
            hora_entrega=hora_entrega,
            vehiculo=vehiculo,
            servicio_id=servicio_id  
        )
        

        return redirect('ccalendario')
    else:
        servicios = Service.objects.filter(user=taller.user)
        vehiculos = Vehiculos.objects.filter(usuario=request.user)
        return render(request, 'clientes_reserva.html', {'taller': taller, 'servicios': servicios, 'vehiculos': vehiculos})

#CANCELAR CITA
@login_required
def cancelar_cita(request, reserva_id):
    reserva = get_object_or_404(ReservaCita, id=reserva_id)
    print(reserva_id)

    if request.user == reserva.usuario:
        reserva.estatus = 'Cancelada'
        reserva.save()

    return redirect('ccalendario')  

#Eliminar opinión
@login_required
def eliminar_opinion(request, opinion_id):
    opinion = get_object_or_404(Opinion, id=opinion_id)

    if request.user == opinion.id_usuario:
        opinion.delete()

    taller_name = opinion.id_taller.username

    return redirect(reverse('agendar_citas', args=[taller_name]))

#EDITAR OPINION
@login_required
def editar_opinion(request, opinion_id):
    opinion = get_object_or_404(Opinion, id=opinion_id)
    
    if request.user != opinion.id_usuario:
        return redirect('página_de_error_o_permisos_inadecuados')

    if request.method == 'POST':
        nuevo_texto = request.POST['nuevo_texto']
        opinion.opinion = nuevo_texto
        opinion.save()
        return redirect('agendar_citas', taller_name=opinion.id_taller.username)  

    return render(request, 'editar_opinion.html', {'opinion': opinion})

    return redirect('agendar_citas', taller_name=opinion.id_taller.username)


############################################################CLIENTES############################################################




####################TALLERES####################
def talleres_edit(request):
    user = request.user
    extended_data, created = ExtendedData.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=user)
        extended_data_form = ExtendedDataForm(request.POST, instance=extended_data)

        if user_form.is_valid() and extended_data_form.is_valid():
            user_form.save()
            extended_data_form.save()
            return redirect('tperfil')
            
    else:
        user_form = UpdateUserForm(instance=user)
        extended_data_form = ExtendedDataForm(instance=extended_data)
        print("soy1")

    return render(request, 'taller_edit.html', {'user_form': user_form, 'extended_data_form': extended_data_form})




@login_required
def talleres_notificacion(request):
    return render(request,'taller_notificacion.html')

@login_required
def talleres_servicios(request):
    error_message = None  
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            servicio = form.save(commit=False)
            servicio.user = request.user
            existing_service = Service.objects.filter(
                user=request.user,
                service_name=servicio.service_name
            ).first()
            if existing_service:
                error_message = "Este servicio ya existe."
            else:
                servicio.save()
                return redirect('tservicios')
    else:
        form = ServiceForm()
    
    servicios = Service.objects.filter(user=request.user)
    return render(request, 'taller_servicios.html', {'form': form, 'servicios': servicios, 'error_message': error_message}) 




@login_required
def talleres_citas(request):
    taller_autenticado = request.user

    citas = ReservaCita.objects.filter(taller=taller_autenticado)
    
    usuarios = [cita.usuario for cita in citas]

    return render(request, 'taller_citas.html', {'citas': citas, 'usuarios': usuarios})

@csrf_exempt
@login_required
def cambiar_estado_cita(request, cita_id, nuevo_estado):
    try:
        cita = get_object_or_404(ReservaCita, id=cita_id)
        cita.estatus = nuevo_estado
        cita.save()
        return JsonResponse({'success': True, 'nuevo_estado': nuevo_estado})
    except ReservaCita.DoesNotExist:
        return JsonResponse({'success': False, 'mensaje': 'Cita no encontrada'})












# @login_required
# def talleres_analitica(request):
#     # Obtener el id del taller del usuario logueado (en este caso, el propio usuario)
#     id_taller_usuario = request.user.id
#     opiniones = Opinion.objects.filter(id_taller=id_taller_usuario)  # Asume que cada usuario tiene un taller relacionado
#     total_alegre = opiniones.filter(sentimiento='alegre').count()
#     total_triste = opiniones.filter(sentimiento='triste').count()
#     total_neutro = opiniones.filter(sentimiento='neutro').count()
#     total_comentarios = opiniones.count()
#     print(total_alegre)
#     print(total_neutro)
#     print(total_triste)
#     context = {'happy':total_alegre,'mid':total_neutro,'sad':total_triste}


#     return render(request,'taller_analitica.html',context)


@login_required
def talleres_analitica(request):
    # Obtener el id del taller del usuario logueado
    id_taller_usuario = request.user.id
    opiniones = Opinion.objects.filter(id_taller=id_taller_usuario)
    
    total_alegre = opiniones.filter(sentimiento='alegre').count()
    total_triste = opiniones.filter(sentimiento='triste').count()
    total_neutro = opiniones.filter(sentimiento='neutro').count()
    total_comentarios = opiniones.count()

    # Obtener top 3 comentarios por sentimiento
    top_3_alegre = opiniones.filter(sentimiento='alegre').order_by('-fecha_creacion')[:3]
    top_3_triste = opiniones.filter(sentimiento='triste').order_by('-fecha_creacion')[:3]
    top_3_neutro = opiniones.filter(sentimiento='neutro').order_by('-fecha_creacion')[:3]

    context = {
        'happy': total_alegre,
        'mid': total_triste,
        'sad': total_neutro,
        'conteo_sentimientos': {
            'total': total_comentarios
        },
        'top_3_comentarios': {
            'alegre': top_3_alegre,
            'triste': top_3_triste,
            'neutro': top_3_neutro
        }
    }

    return render(request, 'taller_analitica.html', context)


def editar_servicio(request, servicio_id):
    servicio = get_object_or_404(Service, id=servicio_id)

    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
            return redirect('tservicios')

    form = ServiceForm(instance=servicio)
    return render(request, 'editar_servicio.html', {'form': form, 'servicio': servicio})

def eliminar_servicio(request, servicio_id):
    servicio = get_object_or_404(Service, id=servicio_id)
    servicio.delete()
    return redirect('tservicios')






# @login_required
# def talleres_analitica(request):
#     opiniones = Opinion.objects.filter(id_taller=1)  # Asume que cada usuario tiene un taller relacionado

#     total_alegre = opiniones.filter(sentimiento='alegre').count()
#     total_triste = opiniones.filter(sentimiento='triste').count()
#     total_neutro = opiniones.filter(sentimiento='neutro').count()
#     total_comentarios = opiniones.count()
#     print(total_alegre)
#     print(total_neutro)
#     print(total_triste)
#     context = {'happy':total_alegre,'mid':total_neutro,'sad':total_triste}


#     return render(request,'taller_analitica.html',context)

