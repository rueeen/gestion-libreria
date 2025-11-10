from django import forms
from .models import Libro, Categoria

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = '__all__'
        
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'
        