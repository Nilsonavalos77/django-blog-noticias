from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q  # Para búsquedas complejas con OR
from .models import Noticia, Comentario, Categoria
from .forms import NoticiaForm, ComentarioForm
from .forms import CustomUserCreationForm  # importa el formulario personalizado

# ✅ Vista de inicio con búsqueda, noticias destacadas y filtro por categoría
def inicio(request):
    query = request.GET.get('q')  # Captura el texto ingresado en el buscador
    categoria_id = request.GET.get('categoria')  # Captura el ID de categoría seleccionada
    categorias = Categoria.objects.all()  # Trae todas las categorías para mostrar como botones

    # Filtro principal según búsqueda o categoría
    if query:
        noticias = Noticia.objects.filter(
            Q(titulo__icontains=query) | Q(resumen__icontains=query)
        ).order_by('-fecha_publicacion')
    elif categoria_id:
        noticias = Noticia.objects.filter(categoria__id=categoria_id).order_by('-fecha_publicacion')
    else:
        noticias = Noticia.objects.order_by('-fecha_publicacion')

    # Noticias destacadas para la barra lateral (máx 3)
    noticias_destacadas = Noticia.objects.filter(destacada=True).order_by('-fecha_publicacion')[:3]

    # Renderiza la plantilla con todas las variables
    return render(request, 'inicio.html', {
        'noticias': noticias,
        'noticias_destacadas': noticias_destacadas,
        'query': query,
        'categorias': categorias,
        'categoria_actual': int(categoria_id) if categoria_id else None,
    })

# ✅ Página "Acerca de"
def acerca_de(request):
    return render(request, 'acerca_de.html')

# ✅ Vista de detalle de noticia
def detalle_noticia(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    comentarios = noticia.comentarios.all()
    return render(request, 'detalle_noticia.html', {'noticia': noticia, 'comentarios': comentarios})

# ✅ Vista de registro de usuario
def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        print(form.fields.keys())  # Depuración
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('inicio')
    else:
        form = CustomUserCreationForm()
        print(form.fields.keys())  # Depuración
    return render(request, 'registro.html', {'form': form})

# ✅ Verifica si el usuario es admin
def es_admin(user):
    return user.is_staff

# ✅ Crear noticia (solo admins)
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

# ✅ Editar noticia (solo admins)
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

# ✅ Eliminar noticia (solo admins)
@user_passes_test(es_admin)
def eliminar_noticia(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    if request.method == 'POST':
        noticia.delete()
        return redirect('inicio')
    return render(request, 'eliminar_noticia.html', {'noticia': noticia})

# ✅ Agregar comentario (solo usuarios logueados)
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

# ✅ Editar comentario (solo autor o admin)
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

# ✅ Eliminar comentario (solo autor o admin)
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
