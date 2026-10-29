from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistroUsuarioForm(UserCreationForm):
    # Añadimos el campo de correo y lo hacemos obligatorio
    email = forms.EmailField(required=True, label="Correo (para ignorar tus reclamaciones)")

    class Meta(UserCreationForm.Meta):
        model = User
        # Mantenemos los campos por defecto (usuario y contraseñas) y sumamos el email
        fields = UserCreationForm.Meta.fields + ('email',)