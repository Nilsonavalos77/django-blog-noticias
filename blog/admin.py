from django.contrib import admin
from .models import Categoria, Noticia, Comentario

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')

@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'autor', 'fecha_publicacion', 'categoria', 'destacada')
    list_filter = ('categoria', 'fecha_publicacion', 'destacada')
    search_fields = ('titulo', 'contenido')

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'noticia', 'autor', 'fecha')
    search_fields = ('texto',)
    list_filter = ('fecha',)
