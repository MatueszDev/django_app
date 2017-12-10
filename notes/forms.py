from django import forms
from models import NoteImage, NoteText

class NoteImageForm(forms.ModelForm):
    class Meta:
        model = NoteImage
        fields = ('name', 'author', 'subject', 'lecture_number',
                'lecture_title', 'image')

class NoteTextForm(forms.ModelForm):
    class Meta:
        model = NoteText
        fields = ('name', 'author', 'subject', 'lecture_number',
                'lecture_title', 'content')

