from django.contrib import admin
from .models import Categoria, Producto, Carrito, CarritoProducto, Pedido, DetallePedido

admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Carrito)
admin.site.register(CarritoProducto)
admin.site.register(Pedido)
admin.site.register(DetallePedido)


class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre','precio','stock','imagen')