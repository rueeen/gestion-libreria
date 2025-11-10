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
    path('categoria/<int:id>/delete/', views.categoria_delete, name='categoria-delete'),
    path('categoria/<int:id>/update/', views.categoria_update, name='categoria-update'),
    path('401/', views.error_401, name='401'),
]
