from django import forms
from models import Note, Lecture, NoteQuestion, NoteReply
from models import NoteFileText, NoteFileImage, NoteFilePdf, NoteFileOther

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('title', 'author', 'lecture', 'content')
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

class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ('course', 'lecture_number', 'lecture_title')
        exclude = ['lecture_number']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = NoteQuestion
        fields = ('note', 'title', 'author', 'content', 'answered')
        exclude = ['note', 'author','answered']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = NoteReply
        fields = ('question', 'author', 'content')
        exclude = ['question', 'author']
