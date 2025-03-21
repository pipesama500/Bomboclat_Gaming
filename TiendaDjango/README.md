# Ejecución del programa
## Requisitos Previos
- Python 3.9 o superior
- Django 4.1.11
- ReportLab (para generar facturas en PDF)
## Como ejecutar el proyecto
1. **Clonar el repositorio**
```
git clone https://github.com/pipesama500/Bomboclat_Gaming.git
cd Bomboclat_Gaming
cd TiendaDjango
```
2. **Configurar las migracionas**
```
python manage.py makemigrations
python manage.py migrate
```
3. **Crear un Superusuario (Administrador)**
```
python manage.py createsuperuser
```
4. **Ejecutar el servidor**
```
python manage.py runserver
```
5. **Acceder a la app**  
Accede a la app en: http://127.0.0.1:8000/
### Rutas principales
## Rutas Principales de la Aplicación

| Funcionalidad               | Ruta                                    | Descripción                                        |
|-----------------------------|-----------------------------------------|----------------------------------------------------|
| Página de Inicio            | `/`                                     | Vista principal con productos disponibles.         |
| Registro de Usuario         | `/registro/`                            | Formulario para crear cuenta de usuario.           |
| Inicio de Sesión            | `/login/`                               | Formulario de autenticación.                       |
| Carrito de Compras          | `/carrito/`                             | Visualizar y gestionar los productos del carrito.  |
| Confirmación de Pedido      | `/pedido-exitoso/<int:pedido_id>/`      | Resumen de compra exitosa.                         |
| Descarga de Factura en PDF  | `/pedido-exitoso/<int:pedido_id>/factura/` | Descarga de factura del pedido en formato PDF.     |
| Gestión de Productos (Admin)| `/admin-core/gestion-productos/`        | Administración de productos.                       |
| Gestión de Pedidos (Admin)  | `/admin-core/gestion-pedidos/`          | Administración y control de pedidos.               |
| Panel de Administración     | `/admin/`                               | Panel de administración predeterminado de Django.  |  

## Credenciales de prueba  
- Usuario administrador  
  -  Usuario: admin
  -  Contraseña: pipelon1234
- Cliente 
  -  Usuario: casoprueba
  -  Contraseña: contraseña12345
