from django.db import models
from django.contrib.auth.models import User

#USUARIOS
class ExtendedData(models.Model):
    telefono = models.CharField(max_length=10, null=True,blank=True)
    direccion = models.CharField(max_length=128, null=True,blank=True)
    cp = models.CharField(max_length=5, null=True,blank=True)
    calidad = models.IntegerField(default=0,blank=True,null=True)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE,blank=True)
    descripcion = models.CharField(max_length=300, null=True,blank=True)


#Vehículos
class Vehiculos(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    TIPOS_CHOICES = [
        ('carro', 'Carro'),
        ('bicicleta', 'Bicicleta'),
        ('moto', 'Moto'),
    ]
    tipo = models.CharField(max_length=10, choices=TIPOS_CHOICES)
    modelo = models.CharField(max_length=10, null=True, blank=True)
    año = models.IntegerField(default=0, blank=True, null=True)

#Servicios
class Service(models.Model):
    SERVICE_CHOICES = [
        ('Mantenimiento', 'Mantenimiento'),
        ('Cambio de aceite', 'Cambio de aceite'),
        ('Frenos', 'Frenos'),
        ('Suspensión', 'Suspensión'),
    ]

    TIME_CHOICES = [
        ('1', '1 hora'),
        ('2', '2 horas'),
        ('3', '3 horas'),
        ('4', '4 horas'),
        ('5', '5 horas'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    service_time = models.CharField(max_length=1, choices=TIME_CHOICES)
    service_price = models.DecimalField(max_digits=10, decimal_places=2)

#OPINIONES
class Opinion(models.Model):
    id_taller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='opinions')
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    opinion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    #variable sentimiento
    sentimiento = models.CharField(max_length=10, blank=True, null=True, choices=(
        ('alegre', 'Alegre'),
        ('triste', 'Triste'),
        ('neutro', 'Neutro'),
        ('enojado', 'Enojado')
    ))
    class Meta:
        unique_together = ['id_taller', 'id_usuario']

#RESERVAR CITA
class ReservaCita(models.Model):
    taller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservas_como_taller')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservas_como_usuario')
    fecha = models.DateField()
    hora_entrega = models.TimeField()
    vehiculo = models.ForeignKey(Vehiculos, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Service, on_delete=models.CASCADE)
    ESTATUS_CHOICES = (
        ('Agendada', 'agendada'),
        ('Cancelada', 'cancelada'),
        ('En espera de entrega de vehículo', 'en espera de entrega de vehículo'),
        ('En progreso', 'en progreso'),
        ('En espera de recogida de vehículo', 'en espera de recogida de vehículo'),
        ('Terminada', 'terminada'),
    )

    estatus = models.CharField(max_length=50, choices=ESTATUS_CHOICES, default='Agendada')

    def __str__(self):
        return f'Reserva para {self.taller.username} - {self.usuario.username}'
    
