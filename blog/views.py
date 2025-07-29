from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required  # ✅ Decorador para staff
from django.db.models import Q
from django.http import HttpResponseForbidden
from .models import Noticia, Comentario, Categoria
from .forms import NoticiaForm, ComentarioForm, CustomUserCreationForm


# ✅ Vista principal de inicio con búsqueda y filtro por categoría
def inicio(request):
    query = request.GET.get('q')
    categoria_id = request.GET.get('categoria')
    categorias = Categoria.objects.all()

    if query:
        noticias = Noticia.objects.filter(
            Q(titulo__icontains=query) | Q(resumen__icontains=query)
        ).order_by('-fecha_publicacion')
    elif categoria_id:
        noticias = Noticia.objects.filter(categoria__id=categoria_id).order_by('-fecha_publicacion')
    else:
        noticias = Noticia.objects.order_by('-fecha_publicacion')

    noticias_destacadas = Noticia.objects.filter(destacada=True).order_by('-fecha_publicacion')[:3]

    return render(request, 'inicio.html', {
        'noticias': noticias,
        'noticias_destacadas': noticias_destacadas,
        'query': query,
        'categorias': categorias,
        'categoria_actual': int(categoria_id) if categoria_id else None,
    })


# ✅ Página estática "Acerca de"
def acerca_de(request):
    return render(request, 'acerca_de.html')


# ✅ Vista para mostrar detalle de una noticia
def detalle_noticia(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    comentarios = noticia.comentarios.all()
    return render(request, 'detalle_noticia.html', {'noticia': noticia, 'comentarios': comentarios})


# ✅ Registro de usuarios con formulario personalizado
def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('inicio')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registro.html', {'form': form})


# ✅ Función auxiliar para verificar si es admin (staff)
def es_admin(user):
    return user.is_staff


# ✅ Crear noticia - solo para usuarios administradores (staff)
@staff_member_required
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


@login_required
def editar_noticia(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)

    # Permitir solo al autor o staff editar
    if not (request.user.is_staff or noticia.autor == request.user):
        return HttpResponseForbidden("No tienes permiso para editar esta noticia.")

    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES, instance=noticia)
        if form.is_valid():
            form.save()
            return redirect('detalle_noticia', pk=noticia.pk)
    else:
        form = NoticiaForm(instance=noticia)

    comentarios = noticia.comentarios.all()  # 🔁 Obtener comentarios asociados

    return render(request, 'crear_noticia.html', {
        'form': form,
        'noticia': noticia,
        'comentarios': comentarios  # 👈 se los pasás al template
    })


# ✅ Eliminar noticia - solo para admins
@user_passes_test(es_admin)
def eliminar_noticia(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    if request.method == 'POST':
        noticia.delete()
        return redirect('inicio')
    return render(request, 'eliminar_noticia.html', {'noticia': noticia})


# ✅ Agregar comentario - solo usuarios logueados
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


# ✅ Editar comentario - solo autor o admin
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


# ✅ Eliminar comentario - solo autor o admin
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
