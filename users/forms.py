from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import LitterUser


class RegisterForm(UserCreationForm):
    usertag = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': _('Usertag')}))
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={'placeholder': _('Email')}))
    password1 = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password',
                   'placeholder': _('Password')}))
    password2 = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password',
                   'placeholder': _('Confirm password')})
    )

    class Meta:
        model = LitterUser
        fields = ['usertag', 'email', 'password1', 'password2']
        labels = {
            "password2": ""
        }

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = ""

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


class LoginForm(forms.Form):
    usertag = forms.CharField(
        max_length=150,
        label='',
        widget=forms.TextInput(attrs={
            'id': 'usertag',
            'placeholder': _('Usertag')}))
    password = forms.CharField(
        max_length=128,
        label='',
        widget=forms.PasswordInput(attrs={
            'id': 'password',
            'placeholder': _('Password')}))
