# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Note,Lecture,NoteQuestion,NoteReply
from .models import NoteFileImage,NoteFileText,NoteFilePdf,NoteFileOther

# Register your models here.
admin.site.register(Lecture)
admin.site.register(Note)
admin.site.register(NoteFileImage)
admin.site.register(NoteFileText)
admin.site.register(NoteFilePdf)
admin.site.register(NoteFileOther)
admin.site.register(NoteQuestion)
admin.site.register(NoteReply)
