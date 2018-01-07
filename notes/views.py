# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from grades.models import Classes
from .models import Lecture, Note
from .models import NoteFileText, NoteFileImage, NoteFilePdf, NoteFileOther
from forms import NoteForm, NoteImageForm, NoteTextForm, NotePdfForm, NoteOtherForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Max

@login_required
def add_note(request,classes,lecture_number):
    course = Classes.objects.filter(classes=classes)
    lectures = Lecture.objects.filter(classes=course,
        lecture_number=lecture_number)
    print classes
    print lecture_number
    print request.user
    
    if request.POST:
        noteform = NoteForm(request.POST)
        if noteform.is_valid():
            newnote = noteform.save(commit=False)
            newnote.author = User.objects.get(username=request.user)
            newnote.lecture = lectures[0]
            newnote.save()

            return HttpResponseRedirect('/notes/'+classes+'/'+lecture_number)
    else:
        noteform = NoteForm(request.POST)

    args = {}
    args.update(csrf(request))

    args['form'] = noteform
    args['classes'] = classes
    args['lecture_number'] = lecture_number

    return render_to_response('add_note.html', args)

@login_required
def add_file(request,classes,lecture_number):
    course = Classes.objects.filter(classes=classes)
    number =  lecture_number
    lectures = Lecture.objects.filter(classes=course,
        lecture_number=number)
    
    if request.POST:
        fileform = NoteOtherForm(request.POST, request.FILES)
        for filename,file_ in request.FILES.iteritems():
            print file_.content_type
            if file_.content_type.startswith("text/"):
                fileform = NoteTextForm(request.POST, request.FILES)
            elif file_.content_type.startswith("image/"):
                fileform = NoteImageForm(request.POST, request.FILES)
            elif file_.content_type.startswith("application/pdf"):
                fileform = NotePdfForm(request.POST, request.FILES)
            
        if fileform.is_valid():
            newfile = fileform.save(commit=False)
            newfile.author = User.objects.get(username=request.user)
            newfile.lecture = lectures[0]
            newfile.save()

            return HttpResponseRedirect('/notes')
    else:
        fileform = NoteOtherForm(request.POST)

    args = {}
    args.update(csrf(request))

    args['form'] = fileform
    args['classes'] = classes
    args['lecture_number'] = lecture_number

    return render_to_response('add_file.html', args)

@login_required
def choose_class(request):
    
#    objects = Note.objects.all()
#    lectures = objects.values('subject').annotate(Max('lecture_number'))
    lectures = Lecture.objects.order_by('classes')
    
    return render(request, 'notes_main.html', {'lectures': lectures})

@login_required
def select_lecture(request,classes,lecture_number):

    course = Classes.objects.filter(classes=classes)
    number =  lecture_number
    lectures = Lecture.objects.filter(classes=course,
        lecture_number=number)
    
#    note = Note.objects.all()
#    text = NoteFileText.objects.all()
#    image = NoteFileImage.objects.all()
#    pdf = NoteFilePdf.objects.all()
#    other = NoteFileOther.objects.all()

    notes = Note.objects.filter(lecture=lectures)
    texts = NoteFileText.objects.filter(lecture=lectures)
    imgs = NoteFileImage.objects.filter(lecture=lectures)
    pdfs = NoteFilePdf.objects.filter(lecture=lectures)
    otrs = NoteFileOther.objects.filter(lecture=lectures)
    
#    objects = note.filter(subject=subject, lecture_number=lecture_number)
#    text_objs = text.filter(subject=subject, lecture_number=lecture_number)
#    img_objs = image.filter(subject=subject, lecture_number=lecture_number)
#    pdf_objs = pdf.filter(subject=subject, lecture_number=lecture_number)
#    otr_objs = other.filter(subject=subject, lecture_number=lecture_number)
    
#    lecture_title = objects[0].lecture_title
    
    return render(request, 'notes_list.html', {'lectures': lectures,
                                            'notes' : notes,
                                            'texts' : texts,
                                            'imgs' : imgs,
                                            'pdfs' : pdfs,
                                            'otrs' : otrs})
