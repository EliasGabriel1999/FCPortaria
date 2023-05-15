from django.contrib.auth.forms import AuthenticationForm
from django import forms

from core.models import Visita


class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': 'Usuário e/ou senha inválidos.',
    }
