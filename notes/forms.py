from django import forms
from models import Note, NoteFileText, NoteFileImage, NoteFilePdf, NoteFileOther

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('name', 'author', 'lecture', 'content')
        exclude = ['author','lecture']

class NoteTextForm(forms.ModelForm):
    class Meta:
        model = NoteFileText
        fields = ('name', 'author', 'lecture', 'content')
        exclude = ['author','lecture']

class NoteImageForm(forms.ModelForm):
    class Meta:
        model = NoteFileImage
        fields = ('name', 'author', 'lecture', 'content')
        exclude = ['author','lecture']

class NotePdfForm(forms.ModelForm):
    class Meta:
        model = NoteFilePdf
        fields = ('name', 'author', 'lecture', 'content')
        exclude = ['author','lecture']

class NoteOtherForm(forms.ModelForm):
    class Meta:
        model = NoteFileOther
        fields = ('name', 'author', 'lecture', 'content')
        exclude = ['author','lecture']
