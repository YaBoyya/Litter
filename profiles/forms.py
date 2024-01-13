from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext_lazy as _

from users.models import LitterUser
from core.models import Language


class ProfileForm(forms.ModelForm):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'psettings-username',
                   'placeholder': 'Username'}
        )
    )
    bio = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.Textarea(
            attrs={'class': 'psettings-bio',
                   'plasceholder': 'Bio'}
        )
    )
    picture = forms.ImageField(required=False)
    languages = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Language.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = LitterUser
        fields = ['username', 'bio', 'picture', 'languages']


class EmailForm(forms.ModelForm):
    email = forms.CharField(
        label='',
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

    class Meta:
        model = LitterUser
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email.lower()


class CleanPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password",
                   "autofocus": True,
                   "placeholder": _("Old password")}
        ),
    )
    new_password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password",
                   "placeholder": _("New password")}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password",
                   "placeholder": _("Confirm password")}),
    )


class LanguageTagForm(forms.ModelForm):
    class Meta:
        model = LitterUser
        fields = ['languages']
