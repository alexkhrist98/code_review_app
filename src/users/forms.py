from django import forms
from django.contrib.auth.forms import BaseUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser


class CustomUserCreationForm(BaseUserCreationForm):
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput, required=True)
    class Meta:
        model = CustomUser
        fields = ['email', "password1", "password2"]


class LoginForm(AuthenticationForm):
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput, required=True)
    class Meta:
        model = CustomUser
        fields = ["email", "password"]
