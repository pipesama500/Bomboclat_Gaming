import io
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.http import FileResponse, JsonResponse
from django.utils.translation import gettext_lazy as _
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from .models import Producto, Carrito, CarritoProducto, Pedido, DetallePedido, Categoria
from .forms import ProductoForm, CustomUserCreationForm, ProfileForm

def home(request):
    categoria_id = request.GET.get('categoria')  # Filtrar por categoría
    busqueda = request.GET.get('buscar')         # Buscar por nombre

    # Filtrar los productos
    productos = Producto.objects.all()

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    if busqueda:
        productos = productos.filter(nombre__icontains=busqueda)

    categorias = Categoria.objects.all()  # Para mostrar todas las categorías disponibles
    return render(request, 'core/home.html', {'productos': productos, 'categorias': categorias})

def producto_detalle(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'core/producto_detalle.html', {'producto': producto})

@login_required
def agregar_al_carrito(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)

    item, creado = CarritoProducto.objects.get_or_create(carrito=carrito, producto=producto)
    if not creado:
        item.cantidad += 1
        item.save()

    return redirect('ver_carrito')

@login_required
def ver_carrito(request):
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.carritoproducto_set.all()
    total = carrito.calcular_total()

    return render(request, 'core/carrito.html', {'items': items, 'total': total})

@login_required
def eliminar_del_carrito(request, producto_id):
    carrito = Carrito.objects.get(usuario=request.user)
    item = CarritoProducto.objects.filter(carrito=carrito, producto_id=producto_id).first()

    if item:
        if item.cantidad > 1:
            item.cantidad -= 1
            item.save()
        else:
            item.delete()

    return redirect('ver_carrito')

@login_required
def vaciar_carrito(request):
    carrito = Carrito.objects.get(usuario=request.user)
    carrito.carritoproducto_set.all().delete()  # Elimina todos los productos del carrito
    return redirect('ver_carrito')

@login_required
def finalizar_compra(request):
    carrito = Carrito.objects.get(usuario=request.user)
    items   = carrito.carritoproducto_set.all()

    if not items:
        return redirect('ver_carrito')

    if request.method == 'POST':
       metodo_envio = request.POST.get('metodo_envio')
       perfil       = request.user.profile
       # Si elige domicilio pero no tiene dirección, forzamos actualizar primero
       if metodo_envio == 'Domicilio' and not perfil.direccion:
           return redirect(f"{reverse('actualizar_direccion')}?next=finalizar_compra")

       direccion_envio = perfil.direccion if metodo_envio == 'Domicilio' else ''
       pedido = Pedido.objects.create(
           usuario=request.user,
           total=carrito.calcular_total(),
           metodo_envio=metodo_envio,
           direccion_envio=direccion_envio
       )

       for item in items:
           DetallePedido.objects.create(
               pedido   = pedido,
               producto = item.producto,
               cantidad = item.cantidad,
               subtotal = item.subtotal()
           )

       carrito.carritoproducto_set.all().delete()
       return redirect('pedido_exitoso', pedido.id)

    # Si no es POST, devolvemos al carrito
    return redirect('ver_carrito')

@login_required
def pedido_exitoso(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)
    return render(request, 'core/pedido_exitoso.html', {'pedido': pedido})

@login_required
def generar_factura_pdf(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    detalles = DetallePedido.objects.filter(pedido=pedido)

    # Crear un buffer de BytesIO para el PDF
    buffer = io.BytesIO()

    # Creamos el lienzo del PDF
    c = canvas.Canvas(buffer, pagesize=A4)
    c.setFont("Helvetica", 12)
    # marcamos las partes estáticas para traducción y combinamos con dinámicos
    titulo = _("Factura del Pedido")
    fecha_lbl = _("Fecha de creación")
    estado_lbl = _("Estado del Pedido")

    c.drawString(100, 800, f"{titulo} #{pedido.id}")
    c.drawString(100, 780, f"{fecha_lbl}: {pedido.fecha.strftime('%Y-%m-%d')}")
    c.drawString(100, 760, f"{estado_lbl}: {pedido.estado}")

    y = 720
    detalle_lbl = _("Detalles de los Productos")
    c.drawString(100, y, f"{detalle_lbl}:")    
    y -= 20
    c.drawString(100, y, "Producto      | Cantidad | Precio Unitario | Subtotal")
    cabecera = _("Producto      | Cantidad | Precio Unitario | Subtotal")
    c.drawString(100, y, cabecera)    
    y -= 20

    total = 0
    for detalle in detalles:
        producto = detalle.producto.nombre
        cantidad = detalle.cantidad
        precio = detalle.producto.precio
        subtotal = precio * cantidad
        total += subtotal

        c.drawString(100, y, f"{producto} | {cantidad} | ${precio:.2f} | ${subtotal:.2f}")
        y -= 20

    total_lbl = _("Total a Pagar")
    c.drawString(100, y - 20, f"{total_lbl}: ${total:.2f}")    
    c.showPage()
    c.save()

    # Configuramos la respuesta del PDF desde el buffer
    buffer.seek(0)
    response = FileResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="factura_pedido_{pedido_id}.pdf"'

    return response

@login_required
def mis_pedidos(request):
    """
    Muestra al usuario autenticado la lista de sus propios pedidos,
    con estado y enlace para descargar la factura en PDF.
    """
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'core/mis_pedidos.html', {
        'pedidos': pedidos
    })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'auth_core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def registro_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()  # Guarda el usuario correctamente
            login(request, usuario)  # Inicia sesión automáticamente
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'auth_core/registro.html', {'form': form})

@login_required
def actualizar_direccion(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            # tras guardar, volvemos al flujo de compra o donde venga 'next'
            next_url = request.GET.get('next') or 'ver_carrito'
            return redirect(next_url)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'core/actualizar_direccion.html', {'form': form})


@staff_member_required
def admin_pedidos(request):
    # Obtener filtro de estado
    estado_filtro = request.GET.get('estado')

    # Filtrar pedidos según el estado seleccionado
    if estado_filtro:
        pedidos = Pedido.objects.filter(estado=estado_filtro)
    else:
        pedidos = Pedido.objects.all()

    # Conteo de estados para mostrar resumen
    pendientes = Pedido.objects.filter(estado='Pendiente').count()
    enviados = Pedido.objects.filter(estado='Enviado').count()
    finalizados = Pedido.objects.filter(estado='Finalizado').count()

    return render(request, 'admin_core/admin_pedidos.html', {
        'pedidos': pedidos,
        'pendientes': pendientes,
        'enviados': enviados,
        'finalizados': finalizados,
        'estado_filtro': estado_filtro  # Mantener el filtro seleccionado
    })

@staff_member_required
def actualizar_estado(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)

    # Si el pedido está finalizado, no se puede editar
    if pedido.estado == 'Finalizado':
        return redirect('admin_pedidos')

    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado == 'Enviado' and pedido.estado not in ['Enviado', 'Finalizado']:
            for detalle in pedido.detallepedido_set.all():
                detalle.producto.stock -= detalle.cantidad
                detalle.producto.save()

        pedido.estado = nuevo_estado
        pedido.save()
        return redirect('admin_pedidos')

    return render(request, 'admin_core/actualizar_estado.html', {'pedido': pedido})

@staff_member_required
def admin_productos(request):
    productos = Producto.objects.all()
    return render(request, 'admin_core/admin_productos.html', {'productos': productos})

@staff_member_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_productos')
    else:
        form = ProductoForm()

    return render(request, 'admin_core/crear_producto.html', {'form': form})

@staff_member_required
def editar_producto(request, producto_id):
    # 1) Traigo el producto o 404
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        # 2) Incluyo request.FILES para procesar el ImageField
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('admin_productos')
    else:
        form = ProductoForm(instance=producto)

    return render(request,
                  'admin_core/editar_producto.html',
                  {
                      'form': form,
                      'producto': producto,
                  })

@staff_member_required
def eliminar_producto(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    producto.delete()
    return redirect('admin_productos')

def productos_json(request):
    """
    Servicio web que devuelve un JSON con todos los productos
    cuyo stock > 0, e incluye un campo 'url' apuntando
    a la vista de detalle de cada producto.
    """
    qs = Producto.objects.filter(stock__gt=0)
    data = []
    for p in qs:
        data.append({
            'id':      p.id,
            'nombre':  p.nombre,
            'precio':  float(p.precio),  # o str(p.precio) si prefieres texto
            'stock':   p.stock,
            'url':     request.build_absolute_uri(
                           reverse('producto_detalle', args=[p.id])
                       )
        })
    return JsonResponse({'productos': data})