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