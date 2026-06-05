from functools import wraps

from django.shortcuts import render


class RolNombre:
    CLIENTE = "Cliente"
    BIBLIOTECARIO = "Bibliotecario"


def solo_bibliotecario(vista):
    @wraps(vista)
    def wrapper(request, *args, **kwargs):
        if request.user.perfilusuario.rol.nombre != RolNombre.BIBLIOTECARIO:
            return render(request, 'catalogo/error_401.html')
        return vista(request, *args, **kwargs)

    return wrapper
