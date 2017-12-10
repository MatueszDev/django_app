# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import NoteText
from forms import NoteImageForm, NoteTextForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context_processors import csrf

def dev_fileview(request):
    objects = NoteText.objects.all()
    return render(request, 'dev_fileview/dev_fileview.html', {'objects': objects})

def add_image(request):
    if request.POST:
        form = NoteImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/notes/dev_fileview')
    else:
        form = NoteImageForm(request.POST)

    args = {}
    args.update(csrf(request))

    args['form'] = form

    return render_to_response('add_image.html', args)
    
def add_text(request):
    if request.POST:
        form = NoteTextForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/notes/dev_fileview')
    else:
        form = NoteTextForm(request.POST)

    args = {}
    args.update(csrf(request))

    args['form'] = form

    return render_to_response('add_text.html', args)
