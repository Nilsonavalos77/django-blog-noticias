from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Noticia, Comentario
from .forms import NoticiaForm, ComentarioForm  # Formularios que vamos a crear

# Vista para mostrar la portada con todas las noticias (acceso libre)
def inicio(request):
    noticias = Noticia.objects.order_by('-fecha_publicacion')
    return render(request, 'inicio.html', {'noticias': noticias})

# Vista para ver el detalle de una noticia (acceso libre)
def detalle_noticia(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    comentarios = noticia.comentarios.all()
    return render(request, 'detalle_noticia.html', {'noticia': noticia, 'comentarios': comentarios})

# Vista para registrar un nuevo usuario (acceso libre)
def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('inicio')
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'form': form})

# Check si es admin (staff)
def es_admin(user):
    return user.is_staff

# Crear noticia (solo admin)
@user_passes_test(es_admin)
def crear_noticia(request):
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            noticia = form.save(commit=False)
            noticia.autor = request.user
            noticia.save()
            return redirect('detalle_noticia', pk=noticia.pk)
    else:
        form = NoticiaForm()
    return render(request, 'crear_noticia.html', {'form': form})

# Editar noticia (solo admin)
@user_passes_test(es_admin)
def editar_noticia(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES, instance=noticia)
        if form.is_valid():
            form.save()
            return redirect('detalle_noticia', pk=noticia.pk)
    else:
        form = NoticiaForm(instance=noticia)
    return render(request, 'crear_noticia.html', {'form': form})

# Eliminar noticia (solo admin)
@user_passes_test(es_admin)
def eliminar_noticia(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    if request.method == 'POST':
        noticia.delete()
        return redirect('inicio')
    return render(request, 'eliminar_noticia.html', {'noticia': noticia})

# Agregar comentario (solo usuario logueado)
@login_required
def agregar_comentario(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.autor = request.user
            comentario.noticia = noticia
            comentario.save()
            return redirect('detalle_noticia', pk=pk)
    else:
        form = ComentarioForm()
    return render(request, 'agregar_comentario.html', {'form': form, 'noticia': noticia})

# Editar comentario (solo autor o admin)
@login_required
def editar_comentario(request, pk):
    comentario = get_object_or_404(Comentario, pk=pk)
    if request.user != comentario.autor and not request.user.is_staff:
        return redirect('detalle_noticia', pk=comentario.noticia.pk)
    if request.method == 'POST':
        form = ComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            return redirect('detalle_noticia', pk=comentario.noticia.pk)
    else:
        form = ComentarioForm(instance=comentario)
    return render(request, 'editar_comentario.html', {'form': form, 'comentario': comentario})

# Eliminar comentario (solo autor o admin)
@login_required
def eliminar_comentario(request, pk):
    comentario = get_object_or_404(Comentario, pk=pk)
    if request.user != comentario.autor and not request.user.is_staff:
        return redirect('detalle_noticia', pk=comentario.noticia.pk)
    if request.method == 'POST':
        noticia_pk = comentario.noticia.pk
        comentario.delete()
        return redirect('detalle_noticia', pk=noticia_pk)
    return render(request, 'eliminar_comentario.html', {'comentario': comentario})
