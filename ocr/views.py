# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from ocr.scripts.ocr_pytesseract import scanner
from ocr.scripts.scan_for_drawings import scan_for_drawings
from django.http import HttpResponseRedirect
from .forms import UploadForm
from django.template.context_processors import csrf
from django.shortcuts import render_to_response
from PIL import Image
from .models import Scanned
from .models import Cropped
import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.decorators import login_required

from notes.models import Note, NoteFileImage

@login_required
def index(request): #test only
    return render(request, 'ocr_main.html', {'scanned': Scanned.objects.all()})

@login_required
def show_cropped(request): #test only
    return render(request, 'show_cropped.html', {'cropped':
        Cropped.objects.all()})

@login_required
def show_test(request): #test only
    return render(request, 'show_test.html', {'img':
        NoteFileImage.objects.get(id=19)})

@login_required
def show_scanned(request): #test only
    return render(request, 'show_scanned.html', {'scanned':
        Note.objects.get(id=id)})

@login_required
def ocr_scan(request, id): 
    obj = NoteFileImage.objects.get(id=id)
    img = obj.content
    result = scanner(img)
    note = Note.objects.create(title = obj.title, content = result)
    note.author = obj.author
    note.lecture = obj.lecture
    note.user = obj.user.all()
    note.save()
    return note, render(request, 'show_scanned.html', {'scanned':
        Note.objects.get(id=note.id)})

@login_required
def ocr_crop(request, id): 
    obj = NoteFileImage.objects.get(id=id)
    img = obj.content
    result = scan_for_drawings(img)
    crops = result[1]
    notes_list = list()
    for crop in crops:
        img_io = StringIO.StringIO()
        Image.fromarray(crop).save(img_io, format='JPEG')
        img_file = InMemoryUploadedFile(img_io, None, 'ocr_image.jpg',
                'images', img_io.len, None)
        note = NoteFileImage.objects.create(title = obj.title, content =
                img_file)
        note.author = obj.author
        note.lecture = obj.lecture
        note.user = obj.user.all()
        note.save()
        notes_list.append(note)
    return notes_list, render(request, 'show_cropped.html')

@login_required
def add_image(request): 
    if request.POST:
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            #ocr 
            tmp = scanner(request.FILES['file'])
            Scanned.objects.create(name = "test", content = tmp)
            return HttpResponseRedirect('/ocr/')
    else:
        form = UploadForm(request.POST)
    args = {}
    args.update(csrf(request))
    args['form'] = form
    return render_to_response('add_image_ocr.html', args)

@login_required
def get_drawings(request): 
    if request.POST:
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
        #in tmp: original image on 1st position (0), list of crops on second(1)
            tmp = scan_for_drawings(request.FILES['file']) 
            crops = tmp[1]
            for crop in crops:
                img_io = StringIO.StringIO()
                Image.fromarray(crop).save(img_io, format='JPEG')
                img_file = InMemoryUploadedFile(img_io, None, 'ocr_image.jpg',
                        'images', img_io.len, None)
                Cropped.objects.create(name="test", content = img_file)
            return HttpResponseRedirect('/ocr/show_cropped')
    else:
        form = UploadForm(request.POST)
    args = {}
    args.update(csrf(request))
    args['form'] = form
    return render_to_response('get_drawings.html', args)

