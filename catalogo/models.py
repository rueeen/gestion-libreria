from registration.models import PerfilUsuario
from django.db import models


class Autor(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    nacionalidad = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    # Atributos libro
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    anio_publicacion = models.PositiveIntegerField()
    creado = models.DateTimeField(auto_now_add=True)
    actualizo = models.DateTimeField(auto_now=True)
    editorial = models.CharField(max_length=100)
    # Imagen libro
    portada = models.ImageField(upload_to='portadas')
    # Relaciones de libro
    autor = models.ForeignKey(Autor, on_delete=models.PROTECT)
    categoria = models.ManyToManyField(Categoria)

    def __str__(self):
        return f"{self.titulo} ({self.anio_publicacion})"


class Carrito(models.Model):
    usuario = models.OneToOneField(PerfilUsuario, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)

    def total(self):
        total = 0
        for item in self.itemcarrito_set.all():
            total += item.subtotal()
        return total

    def __str__(self):
        return f"Carrito de {self.usuario.user.username}"


class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        # Puedes agregar un campo 'precio' en Libro si deseas cálculos reales
        return self.cantidad * 1  # valor simbólico

    def __str__(self):
        return f"{self.cantidad} x {self.libro.titulo}"


class Pedido(models.Model):
    usuario = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    ESTADOS = [
        ('PEND', 'Pendiente'),
        ('CONF', 'Confirmado'),
        ('CANC', 'Cancelado'),
    ]
    estado = models.CharField(max_length=4, choices=ESTADOS, default='PEND')

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.user.username}"
