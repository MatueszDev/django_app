# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from grades.models import Classes
from django.core.validators import MinValueValidator
from django.utils.text import slugify
from django.utils import timezone

class Lecture(models.Model):
    lecture_number = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    lecture_title = models.CharField(max_length=250)
    course = models.ForeignKey(Classes, on_delete=models.CASCADE, null=True)
    slug = models.SlugField(max_length=250)
    lecture_id = str(slug)+"/"+str(lecture_number)

    def save(self, *args, **kwargs):
        if not self.id:
            slug = slugify(self.course.classes)
            if Lecture.objects.filter(slug=slug).exists():
                self.slug = slugify(self.course.classes) + '-{}'.format(Lecture.objects.count())
            else:
                self.slug = slugify(self.course.classes)
        super(Lecture, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.lecture_id

class Note(models.Model):
    '''Model for notes stored as plaintext (default)'''
    title = models.CharField(max_length=250)
    author = models.CharField(max_length=250)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, null=True)
    content = models.TextField(max_length=100000)
    slug = models.SlugField(max_length=250)

    def save(self, *args, **kwargs):
        if not self.id:
            slug = slugify(self.title)
            if Note.objects.filter(slug=slug).exists():
                self.slug = slugify(self.title) + '-{}'.format(Note.objects.count())
            else:
                self.slug = slugify(self.title)
        super(Note, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

class NoteFile(models.Model):
    '''General model for attached files'''
    name = models.CharField(max_length=250)
    author = models.CharField(max_length=250)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, null=True)

    def __unicode__(self):
        return self.name

class NoteFileText(NoteFile):
    '''Model for files to be treated as text'''
    content = models.FileField(upload_to='textfiles/')
    
    def display_file(self):
        with open(self.content.path,'r') as f:
            return f.read()

#make sure you have the PIL/Pillow package, seems to be part of py2 by default
#(Pillow is a newer fork of PIL, internally still referred to as PIL)
class NoteFileImage(NoteFile):
    '''Model for files to be treated as images'''
    content = models.ImageField(upload_to='images/')

class NoteFilePdf(NoteFile):
    '''Model for files to be treated as pdf'''
    content = models.FileField(upload_to='pdfs/')

class NoteFileOther(NoteFile):
    '''Model for files not to be displayed by the browser'''
    content = models.FileField(upload_to='other/')
    
class NoteQuestion(models.Model):
    note = models.ForeignKey(Note, related_name='questions')
    title = models.CharField(max_length=250)
    publish = models.DateTimeField(default=timezone.now)
    author = models.CharField(max_length=250)
    content = models.TextField(max_length=1000)
    answered = models.BooleanField(default=False)

class NoteReply(models.Model):
    question = models.ForeignKey(NoteQuestion, related_name='replies')
    publish = models.DateTimeField(default=timezone.now)
    author = models.CharField(max_length=250)
    content = models.TextField(max_length=1000)
