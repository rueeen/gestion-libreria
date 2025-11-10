from django.shortcuts import render, redirect, get_object_or_404
from .models import Libro, Categoria
from .forms import LibroForm, CategoriaForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'catalogo/base.html')

# ----------------- Vistas Libro -----------------
@login_required
def libro_list(request):
    print(request.user.perfilusuario.rol)
    listado_libros = Libro.objects.all() # -> select * from Libro
    return render(request, 'catalogo/libro/libro_list.html', {'listado_libros': listado_libros})

@login_required
def libro_form(request):
    if request.user.perfilusuario.rol.nombre != "Bibliotecario":
        return render(request, 'catalogo/error_401.html')
    
    form = LibroForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, 'Libro creada!')
            return redirect('libro-list')
        else:
            messages.error(request, 'Error')

    return render(request, 'catalogo/libro/libro_form.html', {'form': form})

@login_required
def libro_delete(request, id):
    libro = get_object_or_404(Libro, id=id)
    print(libro)
    if request.method == "POST":
        libro.delete()
        return redirect('libro-list')
    return render(request, 'catalogo/libro/libro_delete.html')

@login_required
def libro_update(request, id):
    libro = get_object_or_404(Libro, id=id)
    form = LibroForm(request.POST or None, instance=libro)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('libro-list')
    return render(request, 'catalogo/libro/libro_form.html', {'form':form})

# ----------------- Vistas Categoria -----------------
@login_required
def categoria_list(request):
    return render(request, 'catalogo/categorias/categoria_list.html', {'listado_categorias': Categoria.objects.all()})

@login_required
def categoria_create(request):
    form = CategoriaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, 'Categoria creada!')
        return redirect('categoria-list')
    return render(request, 'catalogo/categorias/categoria_form.html', {'form': form})

@login_required
def categoria_delete(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == "POST":
        categoria.delete()
        messages.success(request, 'Categoria eliminada!')
        return redirect('categoria-list')
    return render(request, 'catalogo/categorias/categoria_delete.html')

@login_required
def categoria_update(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    form = CategoriaForm(request.POST or None, instance=categoria)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('categoria-list')
    return render(request, 'catalogo/categorias/categoria_form.html', {'form':form})

def error_401(request):
    return render(request, 'catalogo/error_401.html')