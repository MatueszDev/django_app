from .models import Comment, Post
from django import forms
from django.utils.text import slugify
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5, 'style': 'resize:none;'}),
                           label='Content')

    class Meta:
        model = Post
        fields = ('title', 'body', 'author', 'slug')
        exclude = ["slug", "author"]


class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5, 'style': 'resize:none;'}), label='')

    class Meta:
        model = Comment
        fields = ('body', 'name')
        exclude = ["name"]
