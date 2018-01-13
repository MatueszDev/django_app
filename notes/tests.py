# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from .forms import NoteForm, LectureForm, QuestionForm, ReplyForm
from forms import NoteImageForm, NoteTextForm, NotePdfForm, NoteOtherForm
from grades.models import Classes
from .models import Lecture, Note, NoteQuestion, NoteReply, NoteFile
from .models import NoteFileText, NoteFileImage, NoteFilePdf, NoteFileOther
from django.contrib.auth.models import User
from user_authentication.models import Profile
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO

class NoteTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test',
                    email="test@fis.agh.edu.pl", password="azerty47",
                    first_name="test", last_name="test")
        self.profile = Profile.objects.create(user=self.user)
        
        self.user2 = User.objects.create_user(username='test2',
                    email="test2@fis.agh.edu.pl", password="azerty47",
                    first_name="test2", last_name="test2")
        self.profile = Profile.objects.create(user=self.user2)

        self.admin = User.objects.create_superuser(username='admin',
                    email="admin@mail.com", password="correcthorse",
                    first_name="admin", last_name="admin")
        self.profile = Profile.objects.create(user=self.admin)

        self.course = Classes.objects.create(classes='Some Course')
        self.lecture1 = Lecture.objects.create(lecture_title='first',
                                                course=self.course,
                                                lecture_number=1)
        self.note1 = Note.objects.create(title='this is title',
                                        author=self.user.username,
                                        lecture=self.lecture1,
                                        content='big sphinx of quartz')
        self.question1 = NoteQuestion.objects.create(note=self.note1,
                                        title='why happen',
                                        author=self.user.username,
                                        content='I don\'t even')
        self.reply1 = NoteReply.objects.create(question=self.question1,
                                        author=self.user.username,
                                        content='it could be yellow')
        myfile = SimpleUploadedFile("file.txt", b"file_contents")
        self.file1 = NoteFileText.objects.create(title='some file',
                                        author=self.user.username,
                                        lecture=self.lecture1,
                                        content=myfile)

    def test_view_notes_main(self):
        self.client.login(username='test', password='azerty47')
        response = self.client.get("/notes/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "notes_main.html")
    
    def test_view_notes_list(self):
        self.client.login(username='test', password='azerty47')
        path = self.lecture1.slug+"/"+str(self.lecture1.lecture_number)+"/"
        response = self.client.get("/notes/"+path, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "notes_list.html")
    
    def test_view_add_lecture(self):
        self.client.login(username='admin', password='correcthorse')
        response = self.client.get("/notes/add_lecture/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_lecture.html")
    
    def test_view_add_note(self):
        self.client.login(username='test', password='azerty47')
        path = self.lecture1.slug+"/"+str(self.lecture1.lecture_number)+"/"
        response = self.client.get("/notes/"+path+"add_note/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_note.html")
    
    def test_view_add_note(self):
        self.client.login(username='test', password='azerty47')
        path = self.lecture1.slug+"/"+str(self.lecture1.lecture_number)+"/"
        response = self.client.get("/notes/"+path+"add_file/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_file.html")
    
    def test_view_add_question(self):
        self.client.login(username='test', password='azerty47')
        path = self.lecture1.slug+"/"+str(self.lecture1.lecture_number)+"/"
        response = self.client.get("/notes/"+path+self.note1.slug+"/ask/",
                                                                follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_question.html")
    
    def test_view_add_reply(self):
        self.client.login(username='test', password='azerty47')
        path1 = self.lecture1.slug+"/"+str(self.lecture1.lecture_number)+"/"
        path2 = self.note1.slug+"/"+str(self.question1.pk)+"/"
        response = self.client.get("/notes/"+path1+path2, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "view_question.html")
    
    def test_view_mark_answered_not_author(self):
        self.client.login(username='test2', password='azerty47')
        path1 = self.lecture1.slug+"/"+str(self.lecture1.lecture_number)+"/"
        path2 = self.note1.slug+"/"+str(self.question1.pk)+"/ok/"
        response = self.client.get("/notes/"+path1+path2, follow=True)
        self.assertEqual(response.status_code, 403)
    
    def test_view_mark_answered_author(self):
        self.client.login(username='test', password='azerty47')
        path1 = self.lecture1.slug+"/"+str(self.lecture1.lecture_number)+"/"
        path2 = self.note1.slug+"/"+str(self.question1.pk)+"/ok/"
        response = self.client.get("/notes/"+path1+path2, follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_view_mark_answered_superuser(self):
        self.client.login(username='admin', password='correcthorse')
        path1 = self.lecture1.slug+"/"+str(self.lecture1.lecture_number)+"/"
        path2 = self.note1.slug+"/"+str(self.question1.pk)+"/ok/"
        response = self.client.get("/notes/"+path1+path2, follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_view_question_delete_not_author(self):
        self.client.login(username='test2', password='azerty47')
        path1 = self.lecture1.slug+"/"+str(self.lecture1.lecture_number)+"/"
        path2 = self.note1.slug+"/"+str(self.question1.pk)+"/delete/"
        response = self.client.get("/notes/"+path1+path2, follow=True)
        self.assertEqual(response.status_code, 403)
    
    def test_view_question_delete(self):
        self.client.login(username='admin', password='correcthorse')
        path1 = self.lecture1.slug+"/"+str(self.lecture1.lecture_number)+"/"
        path2 = self.note1.slug+"/"+str(self.question1.pk)+"/delete/"
        response = self.client.get("/notes/"+path1+path2, follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_view_reply_delete_not_author(self):
        self.client.login(username='test2', password='azerty47')
        path1 = self.lecture1.slug+"/"+str(self.lecture1.lecture_number)+"/"
        path2 = self.note1.slug+"/"+str(self.question1.pk)+"/"+str(self.reply1.pk)
        response = self.client.get("/notes/"+path1+path2+"/delete/", follow=True)
        self.assertEqual(response.status_code, 403)
    
    def test_view_reply_delete(self):
        self.client.login(username='admin', password='correcthorse')
        path1 = self.lecture1.slug+"/"+str(self.lecture1.lecture_number)+"/"
        path2 = self.note1.slug+"/"+str(self.question1.pk)+"/"+str(self.reply1.pk)
        response = self.client.get("/notes/"+path1+path2+"/delete/", follow=True)
        self.assertEqual(response.status_code, 200)
        
    def test_view_bookmarks(self):
        self.client.login(username='test', password='azerty47')
        response = self.client.get("/notes/bookmarks/", follow=True)
        self.assertEqual(response.status_code, 200)
        
    def test_view_note_bookmark(self):
        self.client.login(username='test', password='azerty47')
        path1 = self.lecture1.slug+"/"+str(self.lecture1.lecture_number)+"/"
        response = self.client.get("/notes/"+path1+self.note1.slug+"/mark/",
                                                                 follow=True)
        self.assertEqual(response.status_code, 200)
        
    def test_view_note_unmark(self):
        self.client.login(username='test', password='azerty47')
        path1 = self.lecture1.slug+"/"+str(self.lecture1.lecture_number)+"/"
        response = self.client.get("/notes/"+path1+self.note1.slug+"/unmark/",
                                                                 follow=True)
        self.assertEqual(response.status_code, 200)

    def test_if_add_note_form_is_valid(self):
        form = NoteForm(data={'title': 'testnote',
                                'author': 'admin',
                                'lecture': self.lecture1,
                                'content': 'volcano bakemeat'})
        self.assertTrue(form.is_valid())
    
    def test_if_add_note_form_is_invalid(self):
        form = NoteForm(data={'title': '',
                                'author': 'admin',
                                'lecture': self.lecture1,
                                'content': 'volcano bakemeat'})
        self.assertFalse(form.is_valid())
        
        form = NoteForm(data={'title': 'testnote',
                                'author': 'admin',
                                'lecture': self.lecture1,
                                'content': ''})
        self.assertFalse(form.is_valid())
        
        form = NoteForm(data={'title': 'testnote',
                                'author': '',
                                'lecture': self.lecture1,
                                'content': 'volcano bakemeat'})
        self.assertTrue(form.is_valid())
        
        form = NoteForm(data={'title': 'testnote',
                                'author': 'admin',
                                'lecture': None,
                                'content': 'volcano bakemeat'})
        self.assertTrue(form.is_valid())
    
    def test_add_note_form_response(self):
        self.client.login(username='admin', password='correcthorse')
        lecture_id = self.lecture1.slug+'/'+str(self.lecture1.lecture_number)
        url = '/notes/'+lecture_id+'/add_note/'
        response = self.client.post(url,
                                {'title': 'testnote',
                                'author': 'admin',
                                'lecture': self.lecture1,
                                'content': 'volcano bakemeat'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes_list.html')

#    def test_if_add_lecture_form_is_valid(self):
#        form = LectureForm(data={'course': self.course,
#                                'lecture_title': 'second'})
#        print form
#        self.assertTrue(form.is_valid())
    
    def test_if_add_lecture_form_is_invalid(self):
        form = LectureForm(data={'course': '',
                                'lecture_title': 'second'})
        self.assertFalse(form.is_valid())
        
        form = LectureForm(data={'course': self.course,
                                'lecture_title': ''})
        self.assertFalse(form.is_valid())
    
    def test_add_lecture_form_response(self):
        self.client.login(username='admin', password='correcthorse')
        response = self.client.post('/notes/add_lecture/',
                                {'course': self.course,
                                'lecture_title': 'second'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_lecture.html')
        
    def test_if_add_question_form_is_valid(self):
        form = QuestionForm(data={'title': 'why',
                                'content': 'why'})
        self.assertTrue(form.is_valid())
        
    def test_if_add_question_form_is_invalid(self):
        form = QuestionForm(data={'title': '',
                                'content': 'why'})
        self.assertFalse(form.is_valid())
        
        form = QuestionForm(data={'title': 'why',
                                'content': ''})
        self.assertFalse(form.is_valid())
    
    def test_add_question_form_response(self):
        self.client.login(username='admin', password='correcthorse')
        lecture_id = self.lecture1.slug+'/'+str(self.lecture1.lecture_number)
        url = '/notes/'+lecture_id+'/'+self.note1.slug+'/ask/'
        response = self.client.post(url,
                                {'title': 'why',
                                'content': 'why'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes_list.html')
        
    def test_if_add_reply_form_is_valid(self):
        form = ReplyForm(data={'content': 'why'})
        self.assertTrue(form.is_valid())
        
    def test_if_add_reply_form_is_invalid(self):
        form = ReplyForm(data={'content': ''})
        self.assertFalse(form.is_valid())
    
    def test_add_reply_form_response(self):
        self.client.login(username='admin', password='correcthorse')
        lecture_id = self.lecture1.slug+'/'+str(self.lecture1.lecture_number)
        url = lecture_id+'/'+self.note1.slug+'/'+str(self.question1.pk)+'/'
        response = self.client.post('/notes/'+url,
                                {'content': 'why'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_question.html')
    
    def test_add_text_file_form_response(self):
        self.client.login(username='admin', password='correcthorse')
        myfile = SimpleUploadedFile("file.txt", b"file_contents")
        lecture_id = self.lecture1.slug+'/'+str(self.lecture1.lecture_number)
        url = '/notes/'+lecture_id+'/add_file/'
        response = self.client.post(url,
                                {'title': 'testfile',
                                'author': 'admin',
                                'lecture': self.lecture1,
                                'content': myfile}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes_main.html')
    
    def test_add_img_file_form_response(self):
        self.client.login(username='admin', password='correcthorse')
        lecture_id = self.lecture1.slug+'/'+str(self.lecture1.lecture_number)
        url = '/notes/'+lecture_id+'/add_file/'
        myfile = SimpleUploadedFile(name='foo.gif', 
                   content=b'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00')
        response = self.client.post(url,
                                {'title': 'testfile',
                                'author': 'admin',
                                'lecture': self.lecture1,
                                'content': myfile}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes_main.html')
    
    def test_add_pdf_file_form_response(self):
        self.client.login(username='admin', password='correcthorse')
        myfile = BytesIO(b'binarydata')
        myfile.name = 'testimg.pdf'
        lecture_id = self.lecture1.slug+'/'+str(self.lecture1.lecture_number)
        url = '/notes/'+lecture_id+'/add_file/'
        response = self.client.post(url,
                                {'title': 'testfile',
                                'author': 'admin',
                                'lecture': self.lecture1,
                                'content': myfile}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes_main.html')
        
    def test_view_file_bookmark(self):
        self.client.login(username='test', password='azerty47')
        path1 = self.lecture1.slug+"/"+str(self.lecture1.lecture_number)+"/"
        response = self.client.get("/notes/"+path1+"t/"+str(self.file1.pk)+
                                    "/mark/", follow=True)
        self.assertEqual(response.status_code, 200)
        
    def test_view_note_unmark(self):
        self.client.login(username='test', password='azerty47')
        path1 = self.lecture1.slug+"/"+str(self.lecture1.lecture_number)+"/"
        response = self.client.get("/notes/"+path1+"t/"+str(self.file1.pk)+
                                    "/mark/", follow=True)
        self.assertIsInstance(self.file1,NoteFileText)
        self.assertEqual(response.status_code, 200)
