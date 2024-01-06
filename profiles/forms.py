from django import forms

from users.models import LitterUser
from core.models import Language


class ProfileForm(forms.ModelForm):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'edit-post-title',
                   'placeholder': 'Title'}
        )
    )
    bio = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.Textarea(
            attrs={'class': 'edit-post-description',
                   'plasceholder': 'Description'}
        )
    )
    picture = forms.ImageField(required=False)
    languages = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Language.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )
# TODO cleanup image field and change it to source if possible

    class Meta:
        model = LitterUser
        fields = ['username', 'bio', 'picture', 'languages']


class EmailForm(forms.ModelForm):
    class Meta:
        model = LitterUser
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email.lower()


class LanguageTagForm(forms.ModelForm):
    class Meta:
        model = LitterUser
        fields = ['languages']
