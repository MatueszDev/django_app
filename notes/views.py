# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from grades.models import Classes
from .models import Lecture, Note, NoteQuestion, NoteReply
from .models import NoteFileText, NoteFileImage, NoteFilePdf, NoteFileOther
from forms import NoteForm, LectureForm, QuestionForm, ReplyForm
from forms import NoteImageForm, NoteTextForm, NotePdfForm, NoteOtherForm
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Max
from ocr.views import ocr_scan, ocr_crop

@login_required
def add_note(request,classes,lecture_number):
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
def add_ocr(request,classes,lecture_number):
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
            returned, rnd = ocr_scan(request, newfile.id)
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

@login_required
def add_crop(request,classes,lecture_number):
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
            returned, rnd = ocr_crop(request, newfile.id)
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

    lectures = Lecture.objects.filter(slug=classes,
        lecture_number=lecture_number)

    notes = Note.objects.filter(lecture=lectures)
    texts = NoteFileText.objects.filter(lecture=lectures)
    imgs = NoteFileImage.objects.filter(lecture=lectures)
    pdfs = NoteFilePdf.objects.filter(lecture=lectures)
    otrs = NoteFileOther.objects.filter(lecture=lectures)
    
    args = {'lectures': lectures, 'notes' : notes,
            'texts' : texts, 'imgs' : imgs,
            'pdfs' : pdfs, 'otrs' : otrs}
    
    return render(request, 'notes_list.html', args)

@login_required
def add_lecture(request):
    
    if request.POST:
        lectureform = LectureForm(request.POST)
        if lectureform.is_valid():
            newlecture = lectureform.save(commit=False)
            course = Classes.objects.filter(classes=newlecture.course)
            lecture = Lecture.objects.filter(course=course[0]).aggregate(
                                                Max('lecture_number'))
            newnumber = ( 1 if not lecture['lecture_number__max'] else
                                            lecture['lecture_number__max']+1 )
            
            newlecture.lecture_number = newnumber
            
            newlecture.save()

            return HttpResponseRedirect('/notes/')
    else:
        lectureform = LectureForm(request.POST)

    args = {}
    args.update(csrf(request))

    args['form'] = lectureform

    return render_to_response('add_lecture.html', args)

@login_required
def add_question(request,classes,lecture_number,noteslug):
    lectures = Lecture.objects.filter(slug=classes,
        lecture_number=lecture_number)
    notes = Note.objects.filter(slug=noteslug)
    
    if request.POST:
        questionform = QuestionForm(request.POST)
        if questionform.is_valid():
            newquestion = questionform.save(commit=False)
            newquestion.author = User.objects.get(username=request.user)
            newquestion.note = notes[0]
            newquestion.save()

            return HttpResponseRedirect('/notes/'+classes+'/'+lecture_number)
    else:
        questionform = QuestionForm(request.POST)

    args = {}
    args.update(csrf(request))

    args['form'] = questionform
    args['classes'] = classes
    args['lecture_number'] = lecture_number
    args['note'] = notes[0]

    return render_to_response('add_question.html', args)

@login_required
def view_question(request,classes,lecture_number,noteslug,qpk):
    lectures = Lecture.objects.filter(slug=classes,
        lecture_number=lecture_number)
    note = Note.objects.filter(slug=noteslug)
    question = NoteQuestion.objects.filter(pk=qpk)
    replies = NoteReply.objects.filter(question=question)
    
    if request.POST:
        replyform = ReplyForm(request.POST)
        if replyform.is_valid():
            newreply = replyform.save(commit=False)
            newreply.author = User.objects.get(username=request.user)
            newreply.question = question[0]
            newreply.save()

            return HttpResponseRedirect('/notes/'+classes+'/'+lecture_number
                                        +'/'+noteslug+'/'+qpk)
    else:
        replyform = ReplyForm(request.POST)

    args = {}
    args.update(csrf(request))
    
    isauthor = (question[0].author == request.user.username) or request.user.is_superuser
    
    isnoteauthor = (note[0].author == request.user.username) or request.user.is_superuser

    args['form'] = replyform
    args['classes'] = lectures[0].course.classes
    args['lectureslug'] = classes
    args['lecture_number'] = lecture_number
    args['note'] = note[0]
    args['question'] = question[0]
    args['replies'] = replies
    args['isauthor'] = isauthor
    args['isnoteauthor'] = isnoteauthor

    return render_to_response('view_question.html', args)

@login_required
def question_okay(request,classes,lecture_number,noteslug,qpk):
    question = NoteQuestion.objects.filter(pk=qpk)
    if request.user.username==question[0].author or request.user.is_superuser:
        question.update(answered=True)
    else:
        return HttpResponseForbidden("You are not permitted to change the status of this question.")
    
    return HttpResponseRedirect('/notes/'+classes+'/'+lecture_number+'/')

@login_required
def question_delete(request,classes,lecture_number,noteslug,qpk):
    question = NoteQuestion.objects.filter(pk=qpk)
    note = Note.objects.filter(slug=noteslug)
    if request.user.username==note[0].author or request.user.is_superuser:
        NoteReply.objects.filter(question=question).delete()
        question.delete()
    else:
        return HttpResponseForbidden("You are not permitted to change the status of this question.")
    
    return HttpResponseRedirect('/notes/'+classes+'/'+lecture_number+'/')

@login_required
def reply_delete(request,classes,lecture_number,noteslug,qpk,rpk):
    question = NoteQuestion.objects.filter(pk=qpk)
    reply = NoteReply.objects.filter(pk=rpk)
    if request.user.username==question[0].author or request.user.is_superuser:
        reply.delete()
    else:
        return HttpResponseForbidden("You are not permitted to change the status of this question.")
    
    return HttpResponseRedirect('/notes/'+classes+'/'+lecture_number+'/'
                            +noteslug+'/'+qpk+'/')

@login_required
def note_bookmark(request,classes,lecture_number,noteslug):
    thisuser = User.objects.get(username=request.user)
    thisnote = Note.objects.filter(slug=noteslug)
    
    if len(thisnote.filter(user=thisuser))==0:
        thisnote[0].user.add(thisuser)
    else:
        thisnote[0].user.remove(thisuser)
    
    return HttpResponseRedirect('/notes/'+classes+'/'+lecture_number+'/')

@login_required
def note_unmark(request,classes,lecture_number,noteslug):
    thisuser = User.objects.get(username=request.user)
    thisnote = Note.objects.filter(slug=noteslug)
    
    if len(thisnote.filter(user=thisuser))==0:
        thisnote[0].user.add(thisuser)
    else:
        thisnote[0].user.remove(thisuser)
    
    return HttpResponseRedirect('/notes/bookmarks/')

@login_required
def file_bookmark(request,classes,lecture_number,filetype,filepk):
    filetypes = {'t': NoteFileText, 'i': NoteFileImage,
                'p': NoteFilePdf, 'o': NoteFileOther}
    thisuser = User.objects.get(username=request.user)
    thisfile = filetypes[filetype].objects.filter(pk=filepk)
    
    if len(thisfile.filter(user=thisuser))==0:
        thisfile[0].user.add(thisuser)
    else:
        thisfile[0].user.remove(thisuser)
    
    return HttpResponseRedirect('/notes/'+classes+'/'+lecture_number+'/')

@login_required
def file_unmark(request,classes,lecture_number,filetype,filepk):
    filetypes = {'t': NoteFileText, 'i': NoteFileImage,
                'p': NoteFilePdf, 'o': NoteFileOther}
    thisuser = User.objects.get(username=request.user)
    thisfile = filetypes[filetype].objects.filter(pk=filepk)
    
    if len(thisfile.filter(user=thisuser))==0:
        thisfile[0].user.add(thisuser)
    else:
        thisfile[0].user.remove(thisuser)
    
    return HttpResponseRedirect('/notes/bookmarks/')

@login_required
def bookmarks(request):
    thisuser = User.objects.get(username=request.user)
    notes = Note.objects.filter(user=thisuser).order_by('lecture','pk')
    texts = NoteFileText.objects.filter(user=thisuser).order_by('lecture','pk')
    imgs = NoteFileImage.objects.filter(user=thisuser).order_by('lecture','pk')
    pdfs = NoteFilePdf.objects.filter(user=thisuser).order_by('lecture','pk')
    otrs = NoteFileOther.objects.filter(user=thisuser).order_by('lecture','pk')
    
    args = { 'notes' : notes, 'texts' : texts,
            'imgs' : imgs, 'pdfs' : pdfs, 'otrs' : otrs}
    
    return render(request, 'bookmarks.html', args)
