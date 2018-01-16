# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.apps import apps 
from ocr.apps import OcrConfig
import numpy as np
from notes.forms import NoteImageForm, NoteOtherForm, NoteForm
from grades.models import Classes
from notes.models import Lecture, NoteFileImage
from ocr.views import ocr_script_database_helper, crop_script_database_helper
from django.core.files.uploadedfile import SimpleUploadedFile
from django_app.settings import DJANGO_HOST

#commented lines in this file are tests that work only locally, commenting to be
#able to merge with master and upload to heroku
if(DJANGO_HOST == "development"):
    import cv2
    from scripts.ocr_pytesseract import scanner
    from scripts.scan_for_drawings import scan_for_drawings

class OcrUrlsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user', email="user@fis.agh.edu.pl", password="12345678", 
                first_name="user", last_name="user")
        self.client.login(username='user', password='12345678')

    def test_views_response(self):
        response = self.client.get(reverse('ocr:index'), follow = True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(reverse('ocr:add_ocr', kwargs = {'classes': 'wot',
            'lecture_number': 2}), '/ocr/wot/2/add_ocr/')
        self.assertEqual(reverse('ocr:add_crop', kwargs = {'classes': 'wot',
            'lecture_number': 2}), '/ocr/wot/2/add_crop/')


class OcrViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user', email="user@fis.agh.edu.pl", password="12345678", 
                first_name="user", last_name="user")
        self.client.login(username='user', password='12345678')
        self.course = Classes.objects.create(classes='wot')
        self.lecture1 = Lecture.objects.create(lecture_title='first',
                                                course=self.course,
                                                lecture_number=1)
        self.path = 'ocr/sample_files/sample_extract.png'
        self.path_bad = 'ocr/sample_files/test_bad_file.jpg'

    def test_main_view(self): 
        response = self.client.get('/ocr/', follow=True)
        self.assertTemplateUsed(response, 'ocr_main.html')

    def test_add_ocr(self):
        response = self.client.get('/ocr/lect/1/add_ocr/', follow=True)
        if(DJANGO_HOST == "development"):
            self.assertTemplateUsed(response, 'add_ocr.html')
        else:
            self.assertTemplateUsed(response, 'notavailable.html')


    def test_add_crop(self):
        response = self.client.get('/ocr/lect/1/add_crop/', follow=True)
        if(DJANGO_HOST == "development"):
            self.assertTemplateUsed(response, 'add_crop.html')
        else:
            self.assertTemplateUsed(response, 'notavailable.html')

    def test_add_ocr_post(self):
        response = self.client.post('/ocr/lect/1/add_ocr/', {'title': 'title',
            'author': 'author', 'Lecture': self.lecture1, 'content': self.path,},
            follow = True)
        if(DJANGO_HOST == "development"):
            self.assertTemplateUsed(response, 'add_ocr.html')
        else:
            self.assertTemplateUsed(response, 'notavailable.html')

    def test_add_crop_post(self):
        response = self.client.post('/ocr/lect/1/add_crop/', {'title': 'title',
            'author': 'author', 'Lecture': self.lecture1, 'content': self.path,},
            follow = True)
        if(DJANGO_HOST == "development"):
            self.assertTemplateUsed(response, 'add_crop.html')
        else:
            self.assertTemplateUsed(response, 'notavailable.html')

    def test_add_ocr_with_file(self):
        with open(self.path) as myfile:
            response = self.client.post('/ocr/wot/1/add_ocr/',
                                    {'title': 'testfile',
                                    'author': 'admin',
                                    'lecture': self.lecture1,
                                    'content': myfile}, follow=True)
        self.assertEqual(response.status_code, 200)
        if(DJANGO_HOST == "development"):
            self.assertTemplateUsed(response, 'show_scanned.html')
        else:
            self.assertTemplateUsed(response, 'notavailable.html')

    def test_add_crop_with_file(self):
        with open(self.path) as myfile:
            response = self.client.post('/ocr/wot/1/add_crop/',
                                    {'title': 'testfile',
                                    'author': 'admin',
                                    'lecture': self.lecture1,
                                    'content': myfile}, follow=True)
        self.assertEqual(response.status_code, 200)
        if(DJANGO_HOST == "development"):
            self.assertTemplateUsed(response, 'show_cropped.html')
        else:
            self.assertTemplateUsed(response, 'notavailable.html')

    def test_add_crop_with_bad_file(self):
        myfile = SimpleUploadedFile(name='foo.jpg', 
                content=b'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00')
        response = self.client.post('/ocr/wot/1/add_crop/',
                                {'title': 'testfile',
                                'author': 'admin',
                                'lecture': self.lecture1,
                                'content': myfile}, follow=True)
        self.assertEqual(response.status_code, 200)
        if(DJANGO_HOST == "development"):
            self.assertTemplateUsed(response, 'images_not_found.html')
        else:
            self.assertTemplateUsed(response, 'notavailable.html')


class Ocr(TestCase):

    def setUp(self):
        self.path = 'ocr/sample_files/sample_text.jpg'

    def test_returned_text(self):
        if(DJANGO_HOST == "development"):
            result = scanner(self.path)
            self.assertEqual(result, "I'm a normal text\nI'm a bold text")
        else:
            pass


class Extract(TestCase):

    def setUp(self):
        self.path = 'ocr/sample_files/sample_extract.png'
        self.path_big = 'ocr/sample_files/sample_big.jpg'
        self.path_text = 'ocr/sample_files/sample_text.jpg'

    def test_returned_images(self):
        if(DJANGO_HOST == "development"):
            results_all = scan_for_drawings(self.path)
            self.assertEqual(len(results_all), 2)
            results_crops = results_all[1]
            self.assertEqual(len(results_crops), 2)
            for result in results_crops:
                self.assertIsInstance(result, np.ndarray)
        else:
            pass

    def test_big_image(self):
        if(DJANGO_HOST == "development"):
            results_all = scan_for_drawings(self.path_big)
            self.assertEqual(len(results_all), 2)
            results_crops = results_all[1]
            self.assertEqual(len(results_crops), 4) #manually upscaled image causes anomalies
            for result in results_crops:
                self.assertIsInstance(result, np.ndarray)
        else:
            pass

    def test_noimg(self):
        if(DJANGO_HOST == "development"):
            self.assertRaises(scan_for_drawings(self.path_text))
        else:
            pass


class AppsTest(TestCase):
    def test_apps(self):
        self.assertEqual(OcrConfig.name, 'ocr')
        self.assertEqual(apps.get_app_config('ocr').name, 'ocr') 
