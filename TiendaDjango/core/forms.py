from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'categoria']

# ————— Formulario de registro con dirección opcional —————
class CustomUserCreationForm(UserCreationForm):
    direccion = forms.CharField(
        max_length=255,
        required=False,
        label="Dirección (opcional)"
    )
    class Meta(UserCreationForm.Meta):
        model  = User
        fields = UserCreationForm.Meta.fields + ('direccion',)

    def save(self, commit=True):
        user = super().save(commit)
        # Guardar la dirección en el perfil
        direccion = self.cleaned_data.get('direccion', '')
        user.profile.direccion = direccion
        user.profile.save()
        return user

# ————— Formulario para cambiar/agregar dirección —————
class AddressForm(forms.Form):
    direccion = forms.CharField(
        max_length=255,
        required=True,
        label="Dirección de envío"
    )