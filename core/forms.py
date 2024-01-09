from django import forms
from django.db import models

from .models import Post, Comment, Language


class PostForm(forms.ModelForm):
    title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'edit-post-title',
                   'placeholder': 'Title'}
        )
    )
    text = forms.CharField(
        required=False,
        max_length=500,
        widget=forms.Textarea(
            attrs={'class': 'edit-post-description',
                   'plasceholder': 'Description'}
        )
    )
    picture = forms.FileField(required=False)
    languages = forms.ModelMultipleChoiceField(
        queryset=Language.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )
    # difficulty = forms.ChoiceField(widget=forms.Select())

    class Meta:
        model = Post
        fields = ['title', 'text', 'picture', 'languages', 'difficulty']


class CommentForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Add a comment...'}),
        max_length=200,
        required=True)

    class Meta:
        model = Comment
        fields = ['text']


class SearchForm(forms.ModelForm):
    q = forms.CharField(
        empty_value='',
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Search...'}
            )
    )
    trend = forms.ChoiceField(
        required=False,
        choices=[('New', 'New'), ('Hot', 'Hot')],
        widget=forms.RadioSelect()
    )
    difficulty = forms.ChoiceField(
        required=False,
        choices=[('E', 'Easy'), ('M', 'Medium'), ('H', 'Hard')],
        widget=forms.RadioSelect()
    )
    languages = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Language.objects.annotate(
            post_count=models.Count('post')
            ).order_by('-post_count', 'name').values_list(
                'name', flat=True)[:10],
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = Post
        fields = ['q', 'trend', 'difficulty', 'languages']
