from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import LitterUser


# TODO setup cleaning for usertags etc and change to BaseUserCreationForm
class RegisterForm(UserCreationForm):
    class Meta:
        model = LitterUser
        fields = ['usertag', 'email', 'password1', 'password2']


class LoginForm(forms.ModelForm):
    class Meta:
        model = LitterUser
        fields = ['usertag', 'password']
