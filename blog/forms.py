from django import forms
from .models import Comentario
from .models import Noticia, Comentario
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Formulario para crear o editar una noticia
class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia  # Modelo base para este formulario
        fields = [
            'titulo',      # Campo para el título de la noticia
            'resumen',     # Campo para un resumen corto de la noticia
            'contenido',   # Campo para el texto completo de la noticia
            'categoria',   # Campo para asignar la noticia a una categoría existente
            'imagen',      # Campo para subir una imagen relacionada a la noticia
            'destacada'    # Campo booleano para marcar si la noticia es destacada o no
        ]

# Formulario para crear o editar un comentario
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario  # Modelo base para este formulario
        fields = ['texto']  # Solo el campo texto es editable por el usuario
        widgets = {
            # Widget para personalizar el textarea del campo texto
            'texto': forms.Textarea(
                attrs={
                    'rows': 3,  # Alto del textarea en filas
                    'placeholder': 'Escribe tu comentario...'  # Texto guía dentro del textarea
                }
            )
        }


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user