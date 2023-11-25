from django import forms
from datetime import date
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.core.exceptions import ValidationError


#PARA EL LOGIN
class AuthenticationuseUserForm(AuthenticationForm):
    class Meta:
        model=User
        fields=['email','password']

    
#CREACIÓN DE USUARUIOS
class createUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','first_name','last_name','password1','password2']    

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = ExtendedData
        fields = "__all__"
        widgets = {
            'direccion': forms.TextInput(attrs={'required': False}),
            'cp': forms.TextInput(attrs={'required': False}),
            'calidad': forms.NumberInput(attrs={'required': False}),
        }


#AGREGAR VEHÍCULO
class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculos
        fields = ['tipo', 'modelo', 'año']


#EDITAR USUARIOS
class UserEditForm(forms.ModelForm):
    telefono = forms.CharField(max_length=10, required=False)

    class Meta:
        model = User
        fields = ['email', 'telefono']

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        if self.instance:
            extended_data = ExtendedData.objects.filter(user=self.instance).first()
            if extended_data:
                self.fields['telefono'].initial = extended_data.telefono


#EDITAR TALLERES 
class UpdateUserForm(UserChangeForm):
    telefono = forms.CharField(
        max_length=10,
        required=True,  
        widget=forms.TextInput(attrs={'autocomplete': 'off', 'title': 'Ingresa un número de teléfono válido de 10 dígitos (solo números).'}),
    )
    direccion = forms.CharField(
        max_length=128,
        required=True,  
        widget=forms.TextInput(attrs={'autocomplete': 'off', 'title': 'Ingresa tu dirección.'}),
    )
    cp = forms.CharField(
        max_length=5,
        required=True, 
        widget=forms.TextInput(attrs={'autocomplete': 'off', 'title': 'Ingresa un código postal válido de 5 dígitos (solo números).'}),
    )

    descripcion= forms.CharField(
        max_length=5000,
        required=True
    )

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        if not telefono.isdigit() or len(telefono) != 10:
            raise ValidationError('El teléfono debe tener 10 dígitos.')
        return telefono

    def clean_cp(self):
        cp = self.cleaned_data['cp']
        if not cp.isdigit() or len(cp) != 5:
            raise ValidationError('El código postal debe tener 5 dígitos.')
        return cp

    class Meta:
        model = User
        fields = ('email',)

class ExtendedDataForm(forms.ModelForm):
    class Meta:
        model = ExtendedData
        fields = ('telefono', 'direccion', 'cp','descripcion')


class ServiceForm(forms.ModelForm):
    service_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.TextInput(attrs={'placeholder': '$'})
    )

    class Meta:
        model = Service
        fields = ['service_name', 'service_time', 'service_price']

