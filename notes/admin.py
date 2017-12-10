# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Note,NoteFileImage,NoteFileText,NoteFilePdf

# Register your models here.
admin.site.register(Note)
admin.site.register(NoteFileImage)
admin.site.register(NoteFileText)
admin.site.register(NoteFilePdf)
