# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .models import Event
from .forms import EventForm
from django.contrib.auth.models import User
import datetime
# Create your tests here.

class TestEvent(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', email="user@fis.agh.edu.pl", password="12345678",
                                             first_name="user", last_name="user")
        self.form = Event(
            data={'title':'New event', 'user':self.user, 'day': '2018-01-11', 'starting_time': '12:30', 'ending_time':'13:30', 'personal_notes':'I dont have' }
        )



class TestEventForm(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user', email="user@fis.agh.edu.pl", password="12345678",
                                             first_name="user", last_name="user")
        self.form = EventForm(
            data={'title':'New event', 'user':self.user, 'day': '2018-01-11', 'starting_time': '12:30', 'ending_time':'13:30', 'personal_notes':'I dont have' }
        )

    def test_if_data_is_valid(self):
        self.assertTrue(self.form.is_valid())
        self.assertEqual(self.form.cleaned_data['title'], 'New event')
        self.assertEqual(self.form.cleaned_data['day'], datetime.date(2018, 1, 11))
        self.assertEqual(self.form.cleaned_data['starting_time'], datetime.time(12,30))
        self.assertEqual(self.form.cleaned_data['ending_time'], datetime.time(13,30))
        self.assertEqual(self.form.cleaned_data['personal_notes'], 'I dont have')