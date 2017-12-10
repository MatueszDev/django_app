# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import NoteFileText, NoteFileImage, NoteFilePdf
from forms import NoteImageForm, NoteTextForm, NotePdfForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template.context_processors import csrf

def dev_fileview(request):
    objects = NoteFileText.objects.all()
    return render(request, 'dev_fileview/dev_fileview.html', {'objects': objects})

def dev_imgview(request):
    objects = NoteFileImage.objects.all()
    return render(request, 'dev_fileview/dev_imgview.html', {'objects': objects})

#note: displaying pdfs in a template requires javascript
#you'll have to give me a few moments to figure that one out
#also as of now it only displays the index 0 pdf
def dev_pdfview(request):
    objects = NoteFilePdf.objects.all()
    return render(request, 'dev_fileview/dev_pdfview.html', {'objects': objects})
#   #   the following code is a view for displaying a specific pdf
#    with open(objects[0].content.path,'r') as pdf:
#        response = HttpResponse(pdf.read(), content_type='application/pdf')
#        response['Content-Disposition'] = 'inline;filename='+objects[0].content.name
#        return response

def add_file(request):
    '''test: sorting uploaded files by their type'''
#    if request.POST:
#        for filename,file_ in request.FILES.iteritems():
#            name = request.FILES[filename].name
#
    pass

def add_image(request):
    if request.POST:
        form = NoteImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/notes/dev_imgview')
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
    
def add_pdf(request):
    '''Temporary for testing until add_file is finished'''
    if request.POST:
        form = NotePdfForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/notes/dev_pdfview')
    else:
        form = NotePdfForm(request.POST)

    args = {}
    args.update(csrf(request))

    args['form'] = form

    return render_to_response('add_pdf.html', args)
