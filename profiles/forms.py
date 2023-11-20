from django import forms

from users.models import LitterUser
from core.models import Language


class ProfileForm(forms.ModelForm):
    class Meta:
        model = LitterUser
        fields = ['username', 'bio', 'picture']


class EmailForm(forms.ModelForm):
    class Meta:
        model = LitterUser
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email.lower()


class LanguageTagForm(forms.ModelForm):
    languages = forms.ModelMultipleChoiceField(
        queryset=Language.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = LitterUser
        fields = ['languages']
