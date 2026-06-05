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


def get_webpay_transaction():
    from django.conf import settings
    from transbank.common.options import WebpayOptions
    from transbank.common.integration_type import IntegrationType
    from transbank.webpay.webpay_plus.transaction import Transaction

    options = WebpayOptions(
        commerce_code=settings.WEBPAY_COMMERCE_CODE,
        api_key=settings.WEBPAY_API_KEY,
        integration_type=IntegrationType.TEST
    )
    return Transaction(options)
