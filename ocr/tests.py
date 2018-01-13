# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from scripts.ocr_pytesseract import scanner
from scripts.scan_for_drawings import scan_for_drawings

# Create your tests here.

class OcrViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user', email="user@fis.agh.edu.pl", password="12345678", first_name="user", last_name="user")

    def test_views_response(self):
        response = self.client.get(reverse('ocr:index'), follow = True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(reverse('ocr:ocr_scan'), '/ocr/ocr_scan/')
        self.assertEqual(reverse('ocr:ocr_crop'), '/ocr/ocr_crop/')

class ocr_pytesseract(TestCase):

    def setUp(self):
        self.path = 'ocr/sample_files/test_text.jpg'

    def test_returned_text(self):
        result = scanner(self.path)
        self.assertEqual(result, "I'm a normal text\nI'm a bold text")

#class scan_for_drawings(TestCase):
#
#    def setUp(self):
#        self.path = 'ocr/sample_files/testfile_extract.jpg'
#
#    def test_returned_images(self):
#        result = scan_for_drawings(self.path)
#        self.assertEqual(result, "I'm a normal text\nI'm a bold text")
