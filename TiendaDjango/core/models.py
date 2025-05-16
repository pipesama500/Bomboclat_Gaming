from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

class Categoria(models.Model):
    nombre = models.CharField(
        _('Nombre de categoría'),
        max_length=100
    )

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(
        _('Nombre'),
        max_length=200
    )
    descripcion = models.TextField(
        _('Descripción')
    )
    precio = models.DecimalField(
        _('Precio'),
        max_digits=10, decimal_places=2
    )
    stock = models.PositiveIntegerField(
        _('Stock')
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        verbose_name=_('Categoría')
    )
    imagen = models.ImageField(
        _('Imagen'),
        upload_to='productos/', blank=True, null=True
    )
    
    def __str__(self):
        return self.nombre
    
class Carrito(models.Model):
    usuario = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE,
        verbose_name=_('Usuario')
    )
    productos = models.ManyToManyField(
        Producto,
        through='CarritoProducto',
        verbose_name=_('Productos')
    )

    def calcular_total(self):
        return sum(item.subtotal() for item in self.carritoproducto_set.all())

    def __str__(self):
        return f"{_('Carrito de')} {self.usuario.username}"

class CarritoProducto(models.Model):
    carrito = models.ForeignKey(
        Carrito, on_delete=models.CASCADE,
        verbose_name=_('Carrito')
    )
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE,
        verbose_name=_('Producto')
    )
    cantidad = models.PositiveIntegerField(
        _('Cantidad'), default=1
    )

    def subtotal(self):
        return self.producto.precio * self.cantidad

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} {_('en el carrito de')} {self.carrito.usuario.username}"

class Pedido(models.Model):
    usuario = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE,
        verbose_name=_('Usuario')
    )
    fecha = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Fecha')
    )
    total = models.DecimalField(
        _('Total'),
        max_digits=10, decimal_places=2, default=0
    )
    # ————— Campos de envío —————
    METODOS_ENVIO = [
        ('Tienda',    _('Recoger en tienda')),
        ('Domicilio', _('Envío a domicilio')),
    ]
    metodo_envio = models.CharField(
        _('Método de envío'),
        max_length=10, choices=METODOS_ENVIO, default='Tienda'
    )
    direccion_envio = models.CharField(
        _('Dirección de envío'),
        max_length=255, blank=True
    )
    ESTADOS = [
        ('Pendiente', _('Pendiente')),
        ('Enviado',   _('Enviado')),
        ('Cancelado', _('Cancelado')),
    ]
    estado = models.CharField(
        _('Estado'),
        max_length=10, choices=ESTADOS, default='Pendiente'
    )

    def __str__(self):
        return f"{_('Pedido')} {self.id} - {self.usuario.username}"

class Profile(models.Model):
    user      = models.OneToOneField(
        User, on_delete=models.CASCADE,
        verbose_name=_('Usuario')
    )
    direccion = models.CharField(
        _('Dirección de envío'),
        max_length=255, blank=True
    )
    pais      = models.CharField(
        _('País'),
        max_length=100, blank=True
    )
    municipio = models.CharField(
        _('Municipio'),
        max_length=100, blank=True
    )
    ciudad    = models.CharField(
        _('Ciudad'),
        max_length=100, blank=True
    )

    def __str__(self):
        return f"{_('Perfil de')} {self.user.username}"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    Profile.objects.get_or_create(user=instance)

class DetallePedido(models.Model):
    pedido = models.ForeignKey(
        Pedido, on_delete=models.CASCADE,
        verbose_name=_('Pedido')
    )
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE,
        verbose_name=_('Producto')
    )
    cantidad = models.PositiveIntegerField(
        _('Cantidad')
    )
    subtotal = models.DecimalField(
        _('Subtotal'),
        max_digits=10, decimal_places=2
    )

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} {_('en Pedido')} {self.pedido.id}"
