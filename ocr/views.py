# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from django.shortcuts import render_to_response
from PIL import Image
import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.decorators import login_required
from notes.models import Note, NoteFileImage
from django_app.settings import DJANGO_HOST
if(DJANGO_HOST == "development"):
    from ocr.scripts.ocr_pytesseract import scanner
    from ocr.scripts.scan_for_drawings import scan_for_drawings

@login_required
def index(request): #test only
    return render(request, 'ocr_main.html')

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
