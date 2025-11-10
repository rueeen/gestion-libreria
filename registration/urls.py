from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginAuth, name='login'),
    path('registrar/', views.registrar, name='registrar'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]