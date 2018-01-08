# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from grades.models import Classes
from .models import Lecture, Note
from .models import NoteFileText, NoteFileImage, NoteFilePdf, NoteFileOther
from forms import NoteForm, LectureForm
from forms import NoteImageForm, NoteTextForm, NotePdfForm, NoteOtherForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Max

@login_required
def add_note(request,classes,lecture_number):
   # course = Classes.objects.filter(classes=classes)
    lectures = Lecture.objects.filter(slug=classes,
        lecture_number=lecture_number)
    
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
    #course = Classes.objects.filter(classes=classes)
    number =  lecture_number
    lectures = Lecture.objects.filter(slug=classes,
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
    
    lectures_all = Lecture.objects.order_by('course', 'lecture_number')
    user = User.objects.get(username=request.user)
    user_groups = user.grades_group_set.all()
    classes = []
    for g in user_groups:
        for c in g.classes.all():
            classes.append(c)
    classes = list(set(classes))
    lectures = lectures_all.filter(course__in=classes)
    
    
    return render(request, 'notes_main.html', {'lectures': lectures})

@login_required
def select_lecture(request,classes,lecture_number):

    #course = Classes.objects.filter(classes=classes)
    #number =  lecture_number
    lectures = Lecture.objects.filter(slug=classes,
        lecture_number=lecture_number)

    notes = Note.objects.filter(lecture=lectures)
    texts = NoteFileText.objects.filter(lecture=lectures)
    imgs = NoteFileImage.objects.filter(lecture=lectures)
    pdfs = NoteFilePdf.objects.filter(lecture=lectures)
    otrs = NoteFileOther.objects.filter(lecture=lectures)
    
    return render(request, 'notes_list.html', {'lectures': lectures,
                                            'notes' : notes,
                                            'texts' : texts,
                                            'imgs' : imgs,
                                            'pdfs' : pdfs,
                                            'otrs' : otrs})

@login_required
def add_lecture(request):
#    lecture_numbers = Lecture.objects.values('course').annotate(
#                                                        Max('lecture_number'))
#    lecture_max = {}
#    for d in lecture_numbers:
#        course_name = Classes.objects.get(pk=d['course']).classes
#        lecture_max[course_name] = d['lecture_number__max']
    
    if request.POST:
        lectureform = LectureForm(request.POST)
        if lectureform.is_valid():
            newlecture = lectureform.save(commit=False)
            course = Classes.objects.filter(classes=newlecture.course)
            lecture = Lecture.objects.filter(course=course[0]).aggregate(
                                                Max('lecture_number'))
            newnumber = ( 1 if not lecture['lecture_number__max'] else
                                            lecture['lecture_number__max'] )
            
            newlecture.lecture_number = newnumber
            
            newlecture.save()

            return HttpResponseRedirect('/notes/')
    else:
        lectureform = LectureForm(request.POST)

    args = {}
    args.update(csrf(request))

    args['form'] = lectureform
    #args['lecture_max'] = lecture_max

    return render_to_response('add_lecture.html', args)
