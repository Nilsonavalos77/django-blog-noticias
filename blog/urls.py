from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # Vistas integradas para login/logout

urlpatterns = [
    path('', views.inicio, name='inicio'),  # Portada
    path('noticia/<int:pk>/', views.detalle_noticia, name='detalle_noticia'),  # Ver noticia
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),  # Login
    path('logout/', auth_views.LogoutView.as_view(next_page='inicio'), name='logout'),  # Logout
    path('registro/', views.registro, name='registro'),  # Registro de usuario
]
