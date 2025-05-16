from django.urls import path
from . import views
from core.views import productos_json

urlpatterns = [

    
    #Urls cliente
    path('', views.home, name='home'),
    path('producto/<int:producto_id>/', views.producto_detalle, name='producto_detalle'),
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('eliminar/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    path('finalizar/', views.finalizar_compra, name='finalizar_compra'),
    path('pedido-exitoso/<int:pedido_id>/', views.pedido_exitoso, name='pedido_exitoso'),
    path('pedido-exitoso/<int:pedido_id>/factura/', views.generar_factura_pdf, name='generar_factura_pdf'),
    path('actualizar-direccion/', views.actualizar_direccion, name='actualizar_direccion'),
    path('mis-pedidos/', views.mis_pedidos, name='mis_pedidos'),

    #Urls autenticacion
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro_view, name='registro'),
    
    #Urls admin
    path('admin-core/pedidos/', views.admin_pedidos, name='admin_pedidos'),
    path('admin-core/pedidos/actualizar/<int:pedido_id>/', views.actualizar_estado, name='actualizar_estado'),
    path('admin-core/productos/', views.admin_productos, name='admin_productos'),
    path('admin-core/crear-producto/', views.crear_producto, name='crear_producto'),
    path('admin-core/editar-producto/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('admin-core/eliminar-producto/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),

    path('api/productos/', productos_json, name='productos_json'),
]

