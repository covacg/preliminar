"""
URL configuration for mechanicsrevolution project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    #URLS HOME
    # path('', views.home_login, name='principal'),
    path('', views.home_login, name='login'),
    path('registeroption',views.register_option, name='registeroption'),
    path('taller',views.taller,name='taller'),
    path('cliente',views.cliente, name='cliente'),
    path('login/registration/login.html', views.home_login, name='login'),   

    #URLS CLIENTES
    path('calendario', views.clientes_calendario, name='ccalendario'),
    path('talleres',views.clientes_talleres, name='ctalleres'),
        path('eliminar_opinion/<int:opinion_id>/', views.eliminar_opinion, name='eliminar_opinion'),
        path('reservar/<str:taller_name>/', views.reservar_cita, name='reservar_cita'),
        path('editar_opinion/<int:opinion_id>/', views.editar_opinion, name='editar_opinion'),
    path('vehiculos',views.clientes_vehiculos, name='cvehiculos'),
        path('eliminar_vehiculo/<int:vehiculo_id>/', views.eliminar_vehiculo, name='eliminar_vehiculo'),  
        path('edit',views.clientes_edit, name='cperfil'),
    path('cancelar_cita/<int:reserva_id>/', views.cancelar_cita, name='cancelar_cita'),


    #URLS TALLERES
    path('analitica', views.talleres_analitica, name='tanalitica'),
    path('citas',views.talleres_citas, name='tcalendario'),
    path('servicios',views.talleres_servicios, name='tservicios'),
    path('notificacion',views.talleres_notificacion, name='tnotificaciones'),
    path('perfil',views.talleres_edit, name='tperfil'),
    path('agendar/<str:taller_name>/', views.agendar_citas, name='agendar_citas'),
    path('editar_servicio/<int:servicio_id>/', views.editar_servicio, name='editar_servicio'),
    path('eliminar_servicio/<int:servicio_id>/', views.eliminar_servicio, name='eliminar_servicio'),



    
    path('cambiar_estado_cita/<int:cita_id>/<str:nuevo_estado>/', views.cambiar_estado_cita, name='cambiar_estado_cita'),

    
    
    path('actualizar_vehiculo/<int:vehiculo_id>/', views.actualizar_vehiculo, name='actualizar_vehiculo'),
    path('reservar/<str:taller_name>/', views.reservar_cita, name='reservar_cita'),


    #URLS PASSWORD RESET
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    #path('login/', auth_views.LoginView.as_view(), name='login'),

]
    