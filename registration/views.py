from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm
from .models import PerfilUsuario
from django.views.decorators.cache import never_cache


# Create your views here.
@never_cache
def loginAuth(request):
    if request.user.is_authenticated:
        return redirect('libro-list')
     
    form = AuthenticationForm(request, request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            profile, created = PerfilUsuario.objects.get_or_create(user=user)
            messages.success(request, 'Bienvenido')
            return redirect('profile')
        messages.error(request, 'Error al iniciar sesion')
    return render(request, 'registration/login.html', {'form':form})

def registrar(request):
    form = CustomUserCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creada')
            return redirect('login')
        messages.error(request, 'Error al crear cuenta')
    return render(request, 'registration/registrar.html', {'form':form})

def logout_view(request):
    logout(request)
    return redirect('login')

def profile_view(request):
    return render(request, 'registration/profile.html')