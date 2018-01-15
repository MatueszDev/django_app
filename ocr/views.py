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
from notes.models import Lecture, Note
from notes.forms import NoteImageForm, NoteTextForm, NoteOtherForm
from django.contrib.auth.models import User
if(DJANGO_HOST == "development"):
    from ocr.scripts.ocr_pytesseract import scanner
    from ocr.scripts.scan_for_drawings import scan_for_drawings

@login_required
def index(request): 
    return render(request, 'ocr_main.html')

@login_required
def add_ocr(request,classes,lecture_number):

    if DJANGO_HOST == "development":
        number =  lecture_number
        lectures = Lecture.objects.filter(slug=classes,
            lecture_number=number)
        if request.POST:
            fileform = NoteOtherForm(request.POST, request.FILES)
            for filename,file_ in request.FILES.iteritems():
                if file_.content_type.startswith("image/"):
                    fileform = NoteImageForm(request.POST, request.FILES)
                else :
                    pass
            if fileform.is_valid():
                newfile = fileform.save(commit=False)
                newfile.author = User.objects.get(username=request.user)
                newfile.lecture = lectures[0]
                newfile.save()
                returned = ocr_script_database_helper(newfile.id)
                return render(request, 'show_scanned.html', {'scanned':
                    Note.objects.get(id=returned.id)})
        else:
            fileform = NoteOtherForm(request.POST)
        args = {}
        args.update(csrf(request))
        args['form'] = fileform
        args['classes'] = classes
        args['lecture_number'] = lecture_number
        return render_to_response('add_ocr.html', args)

    else:
        return render(request, 'notavailable.html')

def ocr_script_database_helper(id):
    obj = NoteFileImage.objects.get(id=id)
    img = obj.content
    result = scanner(img)
    note = Note.objects.create(title = obj.title, content = result)
    note.author = obj.author
    note.lecture = obj.lecture
    note.user = obj.user.all()
    note.save()
    return note

@login_required
def add_crop(request,classes,lecture_number):
    if DJANGO_HOST == "development":
        number =  lecture_number
        lectures = Lecture.objects.filter(slug=classes,
            lecture_number=number)
        
        if request.POST:
            fileform = NoteOtherForm(request.POST, request.FILES)
            for filename,file_ in request.FILES.iteritems():
                if file_.content_type.startswith("image/"):
                    fileform = NoteImageForm(request.POST, request.FILES)
                else :
                    pass
                
            if fileform.is_valid():
                newfile = fileform.save(commit=False)
                newfile.author = User.objects.get(username=request.user)
                newfile.lecture = lectures[0]
                newfile.save()
                try:
                    returned = crop_script_database_helper(newfile.id)
                except:
                    return render(request, 'images_not_found.html')
                imgs = list()
                for record in returned:
                    imgs.append(NoteFileImage.objects.get(id=record.id))
                return render(request, 'show_cropped.html', {'cropped': imgs})
        else:
            fileform = NoteOtherForm(request.POST)
        args = {}
        args.update(csrf(request))
        args['form'] = fileform
        args['classes'] = classes
        args['lecture_number'] = lecture_number
        return render_to_response('add_crop.html', args)
    else:
        return render(request, 'notavaliable.html')

def crop_script_database_helper(id):
    obj = NoteFileImage.objects.get(id=id)
    img = obj.content
    result = scan_for_drawings(img)
    crops = result[1] #take crops, the 0 index is base image
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
    return notes_list
