# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.db.models.signals import post_save
from django.dispatch import receiver


class Classes(models.Model):
    CLASSES = (
        ('MMF I', 'Matematyczne Metody Fizyki'),
        ('PP', 'Programowanie Proceduralne'),
        ('MI', 'Matematyka I')
    )
    classes = models.CharField(max_length=30)

    def make_class(self):
        self.save()

    def __unicode__(self):
        return self.classes


class Field_of_study(models.Model):
    fieldOfStudy = models.CharField(max_length=50)

    def make_field_of_study(self):
        self.save()

    def __unicode__(self):
        return self.fieldOfStudy


class Year(models.Model):
    year = models.CharField(max_length=15)

    def make_year(self):
        self.save()

    def __unicode__(self):
        return self.year



class Grades_group(models.Model):

    fieldOfStudy = models.ForeignKey(Field_of_study, on_delete=models.CASCADE, null=True)
    year = models.ForeignKey(Year, on_delete=models.CASCADE, null=True)
    classes = models.ManyToManyField(Classes)
    gradesGroup = str(fieldOfStudy) + " " + str(year)
    user = models.ManyToManyField(User)

    def make_grades_group(self):
        self.save()

    def __unicode__(self):
        return self.gradesGroup
