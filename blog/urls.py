# Importaciones necesarias
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # Importa tus vistas personalizadas

# Lista de rutas disponibles en la aplicación
urlpatterns = [
    # Página principal: muestra listado de noticias
    path('', views.inicio, name='inicio'),

    # Detalle de una noticia según su ID
    path('noticia/<int:pk>/', views.detalle_noticia, name='detalle_noticia'),

    # Agregar comentario a una noticia específica
    path('noticia/<int:pk>/comentario/', views.agregar_comentario, name='agregar_comentario'),

    # Página de login, utilizando el template personalizado 'login.html'
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    # Logout: cierra sesión y redirige a la página de inicio
    path('logout/', auth_views.LogoutView.as_view(next_page='inicio'), name='logout'),

    # Registro de nuevo usuario
    path('registro/', views.registro, name='registro'),

    # Crear nueva noticia (reservado para usuarios con permisos)
    path('crear_noticia/', views.crear_noticia, name='crear_noticia'),

    # Página "Acerca de"
    path('acerca-de/', views.acerca_de, name='acerca_de'),
]
