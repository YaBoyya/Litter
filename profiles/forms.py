from django import forms

from users.models import LitterUser


class ProfileForm(forms.ModelForm):
    class Meta:
        model = LitterUser
        fields = ['username', 'bio']


class EmailForm(forms.ModelForm):
    class Meta:
        model = LitterUser
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email.lower()
