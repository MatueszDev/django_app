# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Note(models.Model):
    '''Model for notes stored as plaintext (default)'''
    name = models.CharField(max_length=250)
    author = models.CharField(max_length=250)
    subject = models.CharField(max_length=250)

    def __unicode__(self):
        return self.name


class NoteFile(models.Model):
    '''General model for attached files'''
    name = models.CharField(max_length=250)
    author = models.CharField(max_length=250)
    subject = models.CharField(max_length=250)
    lecture_number = models.IntegerField()
    lecture_title = models.CharField(max_length=250)

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
    


