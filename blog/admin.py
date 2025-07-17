from django.contrib import admin
from .models import Categoria, Noticia, Comentario

# Registro personalizado para el modelo Categoria
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')  # Muestra estas columnas en el panel admin

# Registro personalizado para el modelo Noticia
@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'autor', 'fecha_publicacion', 'categoria', 'destacada')  # Columnas visibles
    list_filter = ('categoria', 'fecha_publicacion', 'destacada')  # Filtros laterales
    search_fields = ('titulo', 'contenido')  # Habilita búsqueda por título o contenido

# Registro personalizado para el modelo Comentario
@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'noticia', 'autor', 'fecha')  # Columnas visibles
    search_fields = ('texto',)  # Permite buscar por contenido del comentario
    list_filter = ('fecha',)  # Permite filtrar por fecha

