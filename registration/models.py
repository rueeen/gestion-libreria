from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Rol(models.Model):
    # va a aparecer un campo id auto incremental
    nombre = models.CharField(unique=True)
    
    def __str__(self):
        return self.nombre
    
def rol_default():
    rol, created = Rol.objects.get_or_create(nombre="Cliente")
    return rol.id

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.RESTRICT, default=rol_default)

    def __str__(self):
        return self.user.username