from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Categoria, Producto, Carrito, CarritoProducto

class ProductoModelTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre='TestCat')
        self.producto = Producto.objects.create(
            nombre='Prod1',
            descripcion='Descripción de prueba',
            precio=9.99,
            stock=5,
            categoria=self.categoria
        )

    def test_str_devuelve_nombre(self):
        """El __str__ de Producto debe ser su nombre."""
        self.assertEqual(str(self.producto), 'Prod1')


class CarritoModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='usr', password='pwd')
        self.categoria = Categoria.objects.create(nombre='Cat')
        self.producto = Producto.objects.create(
            nombre='X',
            descripcion='D',
            precio=10.00,
            stock=10,
            categoria=self.categoria
        )
        self.carrito = Carrito.objects.create(usuario=self.user)
        CarritoProducto.objects.create(
            carrito=self.carrito,
            producto=self.producto,
            cantidad=2
        )

    def test_calcular_total(self):
        """calcular_total debe devolver precio * cantidad."""
        total = self.carrito.calcular_total()
        self.assertEqual(total, 20.00)


class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_status_and_template(self):
        """
        La vista 'home' debe responder con status 200
        y usar la plantilla core/home.html.
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home.html')
