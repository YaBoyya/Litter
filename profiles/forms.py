from django import forms

from users.models import LitterUser


class ProfileForm(forms.ModelForm):
    class Meta:
        model = LitterUser
        fields = ['username', 'bio']
