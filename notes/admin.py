# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Note,NoteImage,NoteText

# Register your models here.
admin.site.register(Note)
admin.site.register(NoteImage)
admin.site.register(NoteText)
