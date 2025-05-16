from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Producto, Profile

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'categoria','imagen']

# ————— Formulario de registro con dirección opcional —————
class CustomUserCreationForm(UserCreationForm):
    direccion = forms.CharField(max_length=255, required=False, label="Dirección (opcional)")
    pais      = forms.CharField(max_length=100, required=False, label="País (opcional)")
    municipio = forms.CharField(max_length=100, required=False, label="Municipio (opcional)")
    ciudad    = forms.CharField(max_length=100, required=False, label="Ciudad (opcional)")
    
    class Meta(UserCreationForm.Meta):
        model  = User
        fields = UserCreationForm.Meta.fields + (
            'direccion',
            'pais',
            'municipio',
            'ciudad',
        )
    def save(self, commit=True):
        user = super().save(commit)
        # Guardar la dirección en el perfil
        profile = user.profile
        profile.direccion  = self.cleaned_data.get('direccion', '')
        profile.pais       = self.cleaned_data.get('pais', '')
        profile.municipio  = self.cleaned_data.get('municipio', '')
        profile.ciudad     = self.cleaned_data.get('ciudad', '')
        profile.save()
        return user

# ————— Formulario para cambiar/agregar dirección —————
class ProfileForm(forms.ModelForm):
    class Meta:
        model  = Profile
        fields = ['direccion', 'pais', 'municipio', 'ciudad']
        labels = {
            'direccion': 'Dirección de envío',
            'pais':      'País',
            'municipio': 'Municipio',
            'ciudad':    'Ciudad',
        }
        widgets = {
            'direccion': forms.TextInput(attrs={'placeholder': 'Calle, número, etc.'}),
            'pais':      forms.TextInput(attrs={'placeholder': 'Ej. Colombia'}),
            'municipio': forms.TextInput(attrs={'placeholder': 'Ej. Medellín'}),
            'ciudad':    forms.TextInput(attrs={'placeholder': 'Ej. Envigado'}),
        }