from django import forms
from .models import Noticia, Comentario
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Formulario para crear o editar una noticia
class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = [
            'titulo',
            'resumen',
            'contenido',
            'categoria',
            'imagen',
            'destacada'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título de la noticia'
            }),
            'resumen': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Resumen breve de la noticia'
            }),
            'contenido': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Contenido completo de la noticia'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select'
            }),
            'imagen': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'destacada': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

# Formulario para crear o editar un comentario
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'Escribe tu comentario...',
                    'class': 'form-control'
                }
            )
        }

# Formulario personalizado de registro de usuario
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

from django import forms
from .models import Noticia

class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = ['titulo', 'resumen', 'contenido', 'categoria', 'imagen', 'destacada']
