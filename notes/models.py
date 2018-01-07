# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from grades.models import Classes

class Lecture(models.Model):
    lecture_number = models.IntegerField()
    lecture_title = models.CharField(max_length=250)
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE, null=True)
    lecture_id = str(classes)+"/"+str(lecture_number)
    
    def __unicode__(self):
        return self.lecture_id

class Note(models.Model):
    '''Model for notes stored as plaintext (default)'''
    name = models.CharField(max_length=250)
    author = models.CharField(max_length=250)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, null=True)
    #subject = models.CharField(max_length=250)
    #lecture_number = models.IntegerField()
    #lecture_title = models.CharField(max_length=250)
    content = models.TextField(max_length=100000)

    def __unicode__(self):
        return self.name


class NoteFile(models.Model):
    '''General model for attached files'''
    name = models.CharField(max_length=250)
    author = models.CharField(max_length=250)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, null=True)
    #subject = models.CharField(max_length=250)
    #lecture_number = models.IntegerField()
    #lecture_title = models.CharField(max_length=250)

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
    
#    def display_file(self):
#        with open(self.content.path,'r') as pdf:
#            response = HttpResponse(pdf.read(), contenttype='application/pdf')
#            response['Content-Disposition'] = 'inline;filename='+self.content.name
#            return response


class NoteFileOther(NoteFile):
    '''Model for files not to be displayed by the browser'''
    content = models.FileField(upload_to='other/')
    


