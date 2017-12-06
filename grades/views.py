# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from .models import Year, Field_of_study, Classes, Grades_group


def choose_group(request):
    years = Year.objects.all()
    fields = Field_of_study.objects.all()
    classes = Classes.objects.all()
    gradesGroups = Grades_group.objects.all()

    return render(request, 'grades/grades.html', {'years': years,
                                                  'fields': fields,
                                                  'classes': classes,
                                                  'gradesGroups': gradesGroups})


def grades_table(request):
    years = Year.objects.all()
    fields = Field_of_study.objects.all()
    classes = Classes.objects.all()


    return render(request, 'grades/grades_table.html', {'years': years,
                                                        'fields': fields,
                                                        'classes': classes})


