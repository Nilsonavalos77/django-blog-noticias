from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Noticia, Comentario

# Vista para mostrar la portada con todas las noticias
def inicio(request):
    noticias = Noticia.objects.order_by('-fecha_publicacion')  # Ordenar por más recientes
    return render(request, 'inicio.html', {'noticias': noticias})

# Vista para ver el detalle de una noticia específica
def detalle_noticia(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)  # Buscar la noticia por su ID
    comentarios = noticia.comentarios.all()  # Obtener comentarios relacionados
    return render(request, 'detalle_noticia.html', {'noticia': noticia, 'comentarios': comentarios})

# Vista para registrar un nuevo usuario
def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)  # Crea el formulario con los datos enviados
        if form.is_valid():
            usuario = form.save()  # Guarda el nuevo usuario
            login(request, usuario)  # Inicia sesión automáticamente
            return redirect('inicio')  # Redirige a la portada
    else:
        form = UserCreationForm()  # Formulario vacío
    return render(request, 'registro.html', {'form': form})  # Mostrar el formulario
