# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.db import models
from .models import Grades_group, Grades, Classes, Year, Field_of_study
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Models
class GroupTest(TestCase):

    def create_field(self, fieldOfStudy='Human Resources' ):
        return Field_of_study.objects.create(fieldOfStudy=fieldOfStudy)

    def create_year(self, year='Year 5'):
        return Year.objects.create(year=year)

    def create_class(self, classes='Theology'):
        return Classes.objects.create(classes=classes)


    def test_field_of_study_creation(self):
        test_instance = self.create_field()
        self.assertTrue(isinstance(test_instance, Field_of_study))
        self.assertEqual(test_instance.__unicode__(), test_instance.fieldOfStudy)


    def test_year_creation(self):
        test_instance = self.create_year()
        self.assertTrue(isinstance(test_instance, Year))
        self.assertEqual(test_instance.__unicode__(), test_instance.year)


    def test_class_creation(self):
        test_instance = self.create_class()
        self.assertTrue(isinstance(test_instance, Classes))
        self.assertEqual(test_instance.__unicode__(), test_instance.classes)

    # def test_grades_group_creation(self):
    #     test_instance = self.create_grades_group()
    #     self.assertTrue(isinstance(test_instance.fieldOfStudy, models.fields.related.ForeignKey))
    #     self.assertEqual(test_instance.__unicode__(), test_instance.gradesGroup)

    # def test_if_year_input_is_string(self):
    #     self.assertTrue(isinstance(test_instance, str))
    #
    # def test_if_year_input_is_not_string(self):
    #     self.assertFalse(isinstance(test_instance, str))




#views
    def test_choose_group_view(self):
        response = self.client.get('/grades/', folow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'grades/grades.html')

