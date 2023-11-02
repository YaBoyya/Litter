from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

from .models import LitterUser


class RegisterForm(UserCreationForm):
    class Meta:
        model = LitterUser
        fields = ['usertag', 'email', 'password1', 'password2']

    def clean_usertag(self):
        usertag = self.cleaned_data.get('usertag')
        self.cleaned_data.update({'username': usertag})
        usertag = usertag.lower()
        if (
            usertag and
            self._meta.model.objects.filter(usertag__iexact=usertag).exists()
        ):
            self._update_errors(
                ValidationError(
                    {
                        "usertag": self.instance.unique_error_message(
                            self._meta.model, ['usertag']
                        )
                    }
                )
            )
        else:
            return usertag

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email = email.lower()
        if (
            email and
            self._meta.model.objects.filter(email__iexact=email).exists()
        ):
            self._update_errors(
                ValidationError(
                    {
                        "email": self.instance.unique_error_message(
                            self._meta.model, ['email']
                        )
                    }
                )
            )
        else:
            return email


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = LitterUser
        fields = ['usertag', 'password']
