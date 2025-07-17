# Importa la función path para definir rutas
from django.urls import path

# Importa las vistas personalizadas que creaste en views.py
from . import views

# Importa las vistas de autenticación integradas de Django (login, logout)
from django.contrib.auth import views as auth_views

# Lista de rutas disponibles en la aplicación
urlpatterns = [
    # Ruta para la página principal (portada de noticias)
    path('', views.inicio, name='inicio'),

    # Ruta para ver el detalle de una noticia según su ID (pk = primary key)
    path('noticia/<int:pk>/', views.detalle_noticia, name='detalle_noticia'),

    # Ruta para iniciar sesión (usa la vista incorporada de Django y un template personalizado)
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    # Ruta para cerrar sesión (redirecciona a 'inicio' después de salir)
    path('logout/', auth_views.LogoutView.as_view(next_page='inicio'), name='logout'),

    # Ruta para que un usuario se registre en el sitio (usa tu vista personalizada)
    path('registro/', views.registro, name='registro'),
]
