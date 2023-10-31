from django import forms

from .models import Post, Comment, Language


# TODO Make it so that it shows up as value but is considered an object
class PostForm(forms.ModelForm):
    languages = forms.ModelMultipleChoiceField(
        queryset=Language.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Post
        fields = ['title', 'text', 'languages', 'difficulty']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
