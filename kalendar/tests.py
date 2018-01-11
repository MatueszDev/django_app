# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .models import Event
from .forms import EventForm
from django.contrib.auth.models import User
import datetime
from django.core.files.uploadedfile import SimpleUploadedFile
from .utils import Import, Calendar
from django.core.exceptions import ValidationError
# Create your tests here.

class TestEvent(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', email="user@fis.agh.edu.pl", password="12345678",
                                             first_name="user", last_name="user")
        self.event_object = Event(
            title='New event', user=self.user, day='2018-01-11', starting_time='12:30', ending_time='13:30', personal_notes='I dont have'
        )

    def test_if_data_are_equal(self):
        self.assertEqual(self.event_object.title, 'New event')
        self.assertEqual(self.event_object.user, self.user)
        self.assertEqual(self.event_object.day, '2018-01-11')
        self.assertEqual(self.event_object.starting_time, '12:30')
        self.assertEqual(self.event_object.ending_time, '13:30')
        self.assertEqual(self.event_object.personal_notes, 'I dont have')

    def test_get_absolute_url(self):
        link = self.event_object.get_absolute_url(self.user)
        url = '/kalendar/modifyEvent/0/'
        self.assertEqual('<a href="%s">%s%s</a>' % (url, self.event_object.title[:7],'...'), link)

    def test_unicode(self):
        self.assertEqual(str(self.event_object), self.event_object.title)

    def test_overlap(self):
        self.assertTrue(self.event_object.check_overlap(self.event_object.starting_time, self.event_object.ending_time, '12:30', '13:30'))
        self.assertFalse(self.event_object.check_overlap(self.event_object.starting_time, self.event_object.ending_time, '13:30', '15:30'))
        self.assertFalse(self.event_object.check_overlap(self.event_object.starting_time, self.event_object.ending_time, '1:30', '2:00'))

    def test_clean(self):
        self.assertRaises(Event(
            title="T", user=self.user, starting_time="10:00", ending_time="9:00", day='2018-01-11'
        ))

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

    def test_wrong_input(self):
        new_from = EventForm(
            data={'title': 'New event', 'user': self.user, 'day': 'nope date', 'starting_time': 'dsa',
                  'ending_time': '13:30', 'personal_notes': 'I dont have'}
        )
        self.assertFalse(new_from.is_valid())
        new_from = EventForm(
            data={'title': '<>', 'user': self.user, 'day': 'nope date', 'starting_time': 'dsa',
                  'ending_time': '2018-11-11', 'personal_notes': 'I dont have'}
        )
        self.assertFalse(new_from.is_valid())


class CalendarTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user', email="user@fis.agh.edu.pl", password="12345678",
                                             first_name="user", last_name="user")
        self.event_object = Event(
            title='New event', user=self.user, day='2018-01-11', starting_time='12:30', ending_time='13:30',
            personal_notes='I dont have'
        )
        self.calendar_object = Calendar(events=self.event_object, request={'user':self.user})

    def test__init__(self):
        self.assertEqual(self.calendar_object.events, self.event_object)
        self.assertEqual(self.calendar_object.request, {'user':self.user})

    '''def test_formatday(self):
        td = self.calendar_object.formatday(11,1,self.event_object)
        text = ''
        self.assertEqual(text, td)'''


class ImportTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user', email="user@fis.agh.edu.pl", password="12345678",
                                             first_name="user", last_name="user")

        text = b'''"Name","Section","Type","Title","Day Of Week","First Date","Last Date","Published Start","Published End","Location","Capacity","Instructor / Sponsor","Email","Requested Services","Approved",
"FiIS-FT-1 Języki(3rok)","1","Lektorat","Język Obcy (3rok)","Th","11.1.2018",,"11:00","14:00","D-11 SJO","10000",,,,"6.10.2017",'''
        file = SimpleUploadedFile("./static/events.csv", text, content_type='text/csv')
        self.import_object = Import('events.csv', file, self.user)

    def test_check_right_name(self):
        self.assertIsNone(self.import_object.check_right_name())

        file = SimpleUploadedFile("./static/events.csv", b"file_content", content_type='text/csv')
        import_object = Import('wrong', file, self.user)
        try:
            import_object.check_right_name()
        except NameError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)


    def test_check_right_content(self):
        self.assertIsNone(self.import_object.check_right_content())

        file = SimpleUploadedFile("./static/eve.csv", b"file_content", content_type='text/csv')
        import_object = Import('wrong', file, self.user)
        try:
            import_object.check_right_content()
        except IOError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)