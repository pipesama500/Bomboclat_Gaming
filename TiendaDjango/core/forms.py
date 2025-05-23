from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import Producto, Profile

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'categoria', 'imagen']

# ————— Formulario de registro con dirección opcional —————
class CustomUserCreationForm(UserCreationForm):
    direccion = forms.CharField(
        max_length=255, required=False,
        label=_('Dirección (opcional)')
    )
    pais = forms.CharField(
        max_length=100, required=False,
        label=_('País (opcional)')
    )
    municipio = forms.CharField(
        max_length=100, required=False,
        label=_('Municipio (opcional)')
    )
    ciudad = forms.CharField(
        max_length=100, required=False,
        label=_('Ciudad (opcional)')
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            'direccion',
            'pais',
            'municipio',
            'ciudad',
        )

    def save(self, commit=True):
        user = super().save(commit)
        profile = user.profile
        profile.direccion = self.cleaned_data.get('direccion', '')
        profile.pais = self.cleaned_data.get('pais', '')
        profile.municipio = self.cleaned_data.get('municipio', '')
        profile.ciudad = self.cleaned_data.get('ciudad', '')
        profile.save()
        return user

# ————— Formulario para cambiar/agregar dirección —————
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['direccion', 'pais', 'municipio', 'ciudad']
        labels = {
            'direccion': _('Dirección de envío'),
            'pais': _('País'),
            'municipio': _('Municipio'),
            'ciudad': _('Ciudad'),
        }
        widgets = {
            'direccion': forms.TextInput(
                attrs={'placeholder': _('Calle, número, etc.')}  # placeholder traducible
            ),
            'pais': forms.TextInput(
                attrs={'placeholder': _('Ej. Colombia')}
            ),
            'municipio': forms.TextInput(
                attrs={'placeholder': _('Ej. Medellín')}
            ),
            'ciudad': forms.TextInput(
                attrs={'placeholder': _('Ej. Envigado')}
            ),
        }
