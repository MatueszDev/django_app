# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
import numpy as np
from django.contrib import admin
from django.db.models.signals import post_save
from django.dispatch import receiver


class Classes(models.Model):
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
    user = models.ManyToManyField(User)
    gradesGroup = str(fieldOfStudy) + " " + str(year)

    def make_grades_group(self):
        self.save()

    def __unicode__(self):
        return self.gradesGroup

    def __str__(self):
        return unicode(self).encode('utf-8')


class Person(models.Model):
    name = models.CharField(max_length=100, verbose_name='full name')

class Grades(models.Model):
    group = models.ForeignKey(Grades_group, on_delete=models.CASCADE, null=True)
    _gradesDict = {}

    @property
    def gradesDict(self):
        for subject in self.group.classes.all():
            self._gradesDict.setdefault(subject.classes , {} )
            for usr in self.group.user.all():
                fullName = usr.first_name +' '+ usr.last_name
                self._gradesDict[subject.classes][fullName] = [2,3,4]
        print self._gradesDict

    @gradesDict.setter
    def gradesDict(self,subject,fullName, grade):
        self._gradesDict[subject][fullName] = grade
