from django import forms

from .models import Post, Comment, Language


class PostForm(forms.ModelForm):
    languages = forms.ModelMultipleChoiceField(
        queryset=Language.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )
    picture = forms.FileField(required=False)

    class Meta:
        model = Post
        fields = ['title', 'text', 'picture', 'languages', 'difficulty']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
