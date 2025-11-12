from transbank.common.options import WebpayOptions
from transbank.common.integration_type import IntegrationType
from transbank.webpay.webpay_plus.transaction import Transaction
from .models import Carrito, ItemCarrito, Pedido, Libro, Categoria
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LibroForm, CategoriaForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Libreria para hacer búsquedas y filtros más avanzados en las consultas (QuerySets)
from django.db.models import Q


def home(request):
    return render(request, 'catalogo/base.html')

# ----------------- Vistas Libro -----------------


@login_required
def libro_list(request):
    query = request.GET.get('q', '')
    categorias_seleccionadas = request.GET.getlist('categoria')
    listado_libros = Libro.objects.all()

    # Buscador
    if query:
        listado_libros = listado_libros.filter(
            Q(titulo__icontains=query) | Q(descripcion__icontains=query)
        )

    # Filtro múltiple de categorías
    if categorias_seleccionadas:
        listado_libros = listado_libros.filter(
            categoria__id__in=categorias_seleccionadas).distinct()

    categorias = Categoria.objects.all()

    contexto = {
        'listado_libros': listado_libros,
        'categorias': categorias,
        'query': query,
        'categorias_seleccionadas': [int(c) for c in categorias_seleccionadas],
    }
    return render(request, 'catalogo/libro/libro_list.html', contexto)


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
    return render(request, 'catalogo/libro/libro_form.html', {'form': form})

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
    return render(request, 'catalogo/categorias/categoria_form.html', {'form': form})


def error_401(request):
    return render(request, 'catalogo/error_401.html')


# ----------------- Vistas Carrito -----------------

@login_required
def agregar_al_carrito(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    perfil = request.user.perfilusuario
    carrito, _ = Carrito.objects.get_or_create(usuario=perfil)
    item, creado = ItemCarrito.objects.get_or_create(
        carrito=carrito, libro=libro)
    if not creado:
        item.cantidad += 1
        item.save()
    return redirect('ver_carrito')


@login_required
def ver_carrito(request):
    perfil = request.user.perfilusuario
    carrito, _ = Carrito.objects.get_or_create(usuario=perfil)
    items = carrito.itemcarrito_set.all()
    total = carrito.total()
    return render(request, 'catalogo/carrito/ver_carrito.html', {
        'carrito': carrito,
        'items': items,
        'total': total,
    })


@login_required
def eliminar_item(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id,
                             carrito__usuario=request.user.perfilusuario)
    item.delete()
    return redirect('ver_carrito')


@login_required
def confirmar_pedido(request):
    perfil = request.user.perfilusuario
    carrito = get_object_or_404(Carrito, usuario=perfil)
    items = carrito.itemcarrito_set.all()
    if not items:
        return redirect('ver_carrito')
    total = carrito.total()
    pedido = Pedido.objects.create(usuario=perfil, total=total)
    items.delete()  # limpia el carrito
    return render(request, 'catalogo/carrito/confirmar_pedido.html', {'pedido': pedido})


@login_required
def incrementar_item(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id,
                             carrito__usuario=request.user.perfilusuario)
    item.cantidad += 1
    item.save()
    return redirect('ver_carrito')


@login_required
def disminuir_item(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id,
                             carrito__usuario=request.user.perfilusuario)
    if item.cantidad > 1:
        item.cantidad -= 1
        item.save()
    else:
        item.delete()  # elimina el ítem si llega a 0
    return redirect('ver_carrito')


# ----------------- Vistas Pago -----------------

@login_required
def iniciar_pago(request):
    perfil = request.user.perfilusuario
    carrito = get_object_or_404(Carrito, usuario=perfil)
    total = carrito.total()

    buy_order = f"orden-{perfil.id}-{carrito.id}"
    session_id = str(perfil.id)
    return_url = request.build_absolute_uri('/carrito/pago-exitoso/')

    try:
        # Configurar transacción con ambiente de integración (sandbox)
        options = WebpayOptions(
            commerce_code="597055555532",  # código de comercio de pruebas
            api_key="579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C",
            integration_type=IntegrationType.TEST
        )

        tx = Transaction(options)

        response = tx.create(
            buy_order=buy_order,
            session_id=session_id,
            amount=total,
            return_url=return_url
        )

        request.session['buy_order'] = buy_order
        return redirect(f"{response['url']}?token_ws={response['token']}")

    except Exception as e:
        messages.error(request, f"Error al iniciar el pago: {e}")
        return redirect('ver_carrito')


@login_required
def pago_exitoso(request):
    token = request.GET.get("token_ws")
    if not token:
        messages.error(request, "No se recibió el token de Webpay.")
        return redirect('ver_carrito')

    try:
        options = WebpayOptions(
            commerce_code="597055555532",
            api_key="579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C",
            integration_type=IntegrationType.TEST
        )

        tx = Transaction(options)
        response = tx.commit(token)
        status = response.get('status')

        if status == 'AUTHORIZED':
            perfil = request.user.perfilusuario
            carrito = get_object_or_404(Carrito, usuario=perfil)
            total = carrito.total()

            Pedido.objects.create(usuario=perfil, total=total, estado='CONF')
            carrito.itemcarrito_set.all().delete()

            messages.success(request, "Pago exitoso con Webpay 🎉")
        else:
            messages.warning(request, f"El pago no fue autorizado ({status})")

        return render(request, 'catalogo/pago/pago_exitoso.html', {'response': response})
    except Exception as e:
        messages.error(request, f"Error al confirmar el pago: {e}")
        return redirect('ver_carrito')


""" 
Tarjetas
| Tipo                 | Número de tarjeta  | Fecha Exp.        | CVV    | Resultado esperado |
| -------------------- | ------------------ | ----------------- | ------ | ------------------ |
| **Visa**             | `4051885600446623` | Cualquiera futura | `123`  | **Autorizado**     |
| **MasterCard**       | `5186059559590568` | Cualquiera futura | `123`  | **Autorizado**     |
| **American Express** | `373118137707208`  | Cualquiera futura | `1234` | **Autorizado**     |
| **Discover**         | `6011000991300009` | Cualquiera futura | `123`  | **Autorizado**     |
| **Diners Club**      | `305278293371283`  | Cualquiera futura | `123`  | **Autorizado**     |


| Tipo                     | Número de tarjeta  | Resultado esperado |
| ------------------------ | ------------------ | ------------------ |
| **Visa (rechazo)**       | `5186059559590569` | **Rechazado**      |
| **MasterCard (rechazo)** | `5186059559590567` | **Rechazado**      |


Datos autenticacion
| Campo     | Valor          |
| --------- | -------------- |
| **RUT**   | `11.111.111-1` |
| **Clave** | `123`          |
"""
