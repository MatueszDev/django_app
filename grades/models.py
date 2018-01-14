# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django import template
register = template.Library()
from django.contrib import admin
import ast


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
    gradesDict = models.CharField(max_length=500, verbose_name='grades dictionary', null=True)

    def save(self, *args, **kwargs):
        super(Grades, self).save(*args, **kwargs)


    def grades_dict(self):
        self.gradesDict = {}
        for subject in self.group.classes.all():
            self.gradesDict.setdefault(subject.classes , {} )
            for usr in self.group.user.all():
                fullName = usr.first_name +'_'+ usr.last_name
                self.gradesDict[subject.classes][fullName] = [2,3,4]
        print self.gradesDict


    def add_grade(self,subject,fullName,value):
        temporaryDict = ast.literal_eval(self.gradesDict)
        temporaryDict[subject][fullName].append(value)
        self.gradesDict = temporaryDict

    @register.filter(name='dict')
    def dict(self):
        return ast.literal_eval(self.gradesDict)


    def __unicode__(self):
        return '{},{}'.format(self.group.fieldOfStudy, self.group.year)


