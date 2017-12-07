# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import NoteText

def dev_fileview(request):
    objects = NoteText.objects.all()
    return render(request, 'dev_fileview/dev_fileview.html', {'objects': objects})
