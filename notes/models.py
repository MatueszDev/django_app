# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Note(models.Model):
    name = models.CharField(max_length=250)
    author = models.CharField(max_length=250)
    subject = models.CharField(max_length=250)

    def __unicode__(self):
        return self.name

#make sure you have the PIL/Pillow package, seems to be part of py2 by default
#(Pillow is a newer fork of PIL, internally still referred to as PIL)
class NoteImage(models.Model):
    name = models.CharField(max_length=250)
    author = models.CharField(max_length=250)
    subject = models.CharField(max_length=250)
    lecture_number = models.IntegerField()
    lecture_title = models.CharField(max_length=250)
    image = models.ImageField(upload_to='images/')
    
    def __unicode__(self):
        return self.name

class NoteText(models.Model):
    name = models.CharField(max_length=250)
    author = models.CharField(max_length=250)
    subject = models.CharField(max_length=250)
    lecture_number = models.IntegerField()
    lecture_title = models.CharField(max_length=250)
    content = models.FileField(upload_to='textfiles/')
    
    def display_file(self):
        with open(self.content.path) as f:
            return f.read()#.replace('\n', '<br>')

    def __unicode__(self):
        return self.name
