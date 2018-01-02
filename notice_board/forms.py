from .models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5, 'style': 'resize:none;'}), label='')

    class Meta:
        model = Comment
        fields = ('body', 'name')
        exclude = ["name"]
