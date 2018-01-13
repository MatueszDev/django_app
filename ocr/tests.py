# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

# Create your tests here.

class OcrViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user', email="user@fis.agh.edu.pl", password="12345678", first_name="user", last_name="user")

    def test_views_response(self):
        response = self.client.get(reverse('ocr:index'), follow = True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(reverse('ocr:ocr_scan'), '/ocr/ocr_scan/')
        self.assertEqual(reverse('ocr:ocr_crop'), '/ocr/ocr_crop/')
