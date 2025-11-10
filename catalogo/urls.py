from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # urls para Libro
    path('libro/', views.libro_list, name='libro-list'),
    path('libro/create/', views.libro_form, name='libro-create'),
    path('libro/<int:id>/delete/', views.libro_delete, name='libro-delete'),
    path('libro/<int:id>/update/', views.libro_update, name='libro-update'),
    # urls para Categoria
    path('categoria/', views.categoria_list, name='categoria-list'),
    path('categoria/create/', views.categoria_create, name='categoria-create'),
    path('categoria/<int:id>/delete/',
         views.categoria_delete, name='categoria-delete'),
    path('categoria/<int:id>/update/',
         views.categoria_update, name='categoria-update'),
    path('401/', views.error_401, name='401'),
    # urls para carrito
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:libro_id>/',
         views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<int:item_id>/',
         views.eliminar_item, name='eliminar_item'),
    path('carrito/confirmar/', views.confirmar_pedido, name='confirmar_pedido'),
    path('carrito/mas/<int:item_id>/',
         views.incrementar_item, name='incrementar_item'),
    path('carrito/menos/<int:item_id>/',
         views.disminuir_item, name='disminuir_item'),
    # urls para pago
    path('carrito/pagar/', views.iniciar_pago, name='iniciar_pago'),
    path('carrito/pago-exitoso/', views.pago_exitoso, name='pago_exitoso'),
]
