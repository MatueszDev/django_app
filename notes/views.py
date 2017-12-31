# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Note, NoteFileText, NoteFileImage, NoteFilePdf, NoteFileOther
from forms import NoteForm, NoteImageForm, NoteTextForm, NotePdfForm, NoteOtherForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template.context_processors import csrf
from django.db.models import Max

def add_note(request):
    if request.POST:
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/notes')
    else:
        form = NoteForm(request.POST)

    args = {}
    args.update(csrf(request))

    args['form'] = form

    return render_to_response('add_note.html', args)

def add_file(request):
    if request.POST:
        form = NoteOtherForm(request.POST, request.FILES)
        for filename,file_ in request.FILES.iteritems():
            print file_.content_type
            if file_.content_type.startswith("text/"):
                form = NoteTextForm(request.POST, request.FILES)
            elif file_.content_type.startswith("image/"):
                form = NoteImageForm(request.POST, request.FILES)
            elif file_.content_type.startswith("application/pdf"):
                form = NotePdfForm(request.POST, request.FILES)
            
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/notes')
    else:
        form = NoteOtherForm(request.POST)

    args = {}
    args.update(csrf(request))

    args['form'] = form

    return render_to_response('add_file.html', args)

def choose_class(request):
    objects = Note.objects.all()
    
    lectures = objects.values('subject').annotate(Max('lecture_number'))
    
    return render(request, 'notes_main.html', {'lectures': lectures})

def select_lecture(request,subject,lecture_number):
    note = Note.objects.all()
    text = NoteFileText.objects.all()
    image = NoteFileImage.objects.all()
    pdf = NoteFilePdf.objects.all()
    other = NoteFileOther.objects.all()
    
    objects = note.filter(subject=subject, lecture_number=lecture_number)
    text_objs = text.filter(subject=subject, lecture_number=lecture_number)
    img_objs = image.filter(subject=subject, lecture_number=lecture_number)
    pdf_objs = pdf.filter(subject=subject, lecture_number=lecture_number)
    otr_objs = other.filter(subject=subject, lecture_number=lecture_number)
    
    lecture_title = objects[0].lecture_title
    
    return render(request, 'notes_list.html', {'objects': objects,
                                            'subject': subject,
                                            'lecture_number': lecture_number,
                                            'lecture_title': lecture_title,
                                            'text_objs' : text_objs,
                                            'img_objs' : img_objs,
                                            'pdf_objs' : pdf_objs,
                                            'otr_objs' : otr_objs})
