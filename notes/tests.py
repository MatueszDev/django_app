# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from .forms import NoteForm, LectureForm, QuestionForm, ReplyForm
from .forms import NoteImageForm, NoteTextForm, NotePdfForm, NoteOtherForm
from .models import Lecture, Note, NoteQuestion, NoteReply
from .models import NoteFileText, NoteFileImage, NoteFilePdf, NoteFileOther
from django.contrib.auth.models import User
from user_authentication.models import Profile
from django.core.urlresolvers import reverse

class ViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test',
                    email="test@fis.agh.edu.pl", password="azerty47",
                    first_name="test", last_name="test")
        self.profile = Profile.objects.create(user=self.user)

        self.admin = User.objects.create_superuser(username='admin',
                    email="admin@mail.com", password="correcthorse",
                    first_name="admin", last_name="admin")
        self.profile = Profile.objects.create(user=self.admin)

#        self.post = Post.objects.create(title='title', slug='title', author=self.admin)

    def test_view_notes_main(self):
        self.client.login(username='test', password='azerty47')
        response = self.client.get("/notes/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "notes_main.html")
