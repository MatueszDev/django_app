# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .models import Poll, Respond, Vote
from django.contrib.auth.models import User
from django.utils.timezone import now
from .forms import AnsForm, PollForm
from django.urls import reverse
from .apps import PollConfig

# Create your tests here.
class PollTest(TestCase):


    def setUp(self):
        self.user = User.objects.create_user(username='user', email="user@fis.agh.edu.pl", password="12345678",
                                             first_name="user", last_name="user")
        self.poll_object = Poll.objects.create(question="How are you?", description="Feeling question", user=self.user)

    def test_if_data_valid(self):

        self.assertEqual(self.poll_object.question, "How are you?")
        self.assertEqual(self.poll_object.description, "Feeling question")
        self.assertEqual(self.poll_object.user, self.user)
        self.assertLessEqual(self.poll_object.publication_date, now())


class RespondTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user', email="user@fis.agh.edu.pl", password="12345678",
                                             first_name="user", last_name="user")
        self.poll_object = Poll.objects.create(question="How are you?", description="Feeling question", user=self.user)
        self.respond_object = Respond.objects.create(poll=self.poll_object, option="New option" )

    def test_valid_records(self):
        self.assertEqual(self.respond_object.poll, self.poll_object)
        self.assertEqual(self.respond_object.option, "New option")
        self.assertEqual(str(self.respond_object), "New option")

    def test_if_record_exist(self):
        self.assertNotEqual(Respond.number_of_answers(self.poll_object), 0)


class VoteTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user', email="user@fis.agh.edu.pl", password="12345678",
                                             first_name="user", last_name="user")
        self.poll_object = Poll.objects.create(question="How are you?", description="Feeling question", user=self.user)
        self.respond_object = Respond.objects.create(poll=self.poll_object, option="New option" )
        self.vote_object = Vote.objects.create(poll= self.poll_object, choice=self.respond_object, user=self.user)

    def test_if_vote_is_correct(self):
        self.assertEqual(self.vote_object.user, self.user)
        self.assertEqual(self.vote_object.poll, self.poll_object)
        self.assertEqual(self.vote_object.choice, self.respond_object)
        self.assertEqual(str(self.vote_object), "New option")

    def test_number_of_votes_not_equal_0(self):
        self.assertNotEqual(Vote.count_all_votes(), 0)

    def test_number_of_option_votes(self):
        self.assertEqual(Vote.count_option_votes(self.respond_object), 1)

class AnsFormTest(TestCase):

    def test_if_set_answer_is_valid(self):
        form = AnsForm(data={ 'answer': 'Buy more nice staff',})
        self.assertTrue(form.is_valid())
        form = AnsForm(data={'answer': '<script></script>', })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['answer'],'<script></script>' )


class PollFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user', email="user@fis.agh.edu.pl", password="12345678",
                                             first_name="user", last_name="user")

    def test_if_set_poll_is_valid(self):
        self.client.login(username='user', password='12345678')
        form = PollForm(
            data={ 'question': 'What is wrong', 'default_option_1':'life', 'default_option_2':'university'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['question'], 'What is wrong')
        self.assertEqual(form.cleaned_data['default_option_1'], 'life')
        self.assertEqual(form.cleaned_data['default_option_2'], 'university')
        form = PollForm(
            data={'question': '', 'default_option_1': '', 'default_option_2': 'university'})
        self.assertFalse(form.is_valid())


class PollViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user', email="user@fis.agh.edu.pl", password="12345678",
                                             first_name="user", last_name="user")
        self.poll_object = Poll.objects.create(question="How are you?", description="Feeling question", user=self.user)
        self.respond_object = Respond.objects.create(poll=self.poll_object, option="New option")
        self.vote_object = Vote.objects.create(poll=self.poll_object, choice=self.respond_object, user=self.user)
        self.client.login(username='user', password='12345678')

    def test_name_view(self):

        response = self.client.get(reverse('poll:index'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(reverse('poll:poll', kwargs={ 'object_id': 1}), '/poll/1/')
        self.assertEqual(reverse('poll:create_poll'), '/poll/addPoll/')
        self.assertEqual(reverse('poll:vote', kwargs={ 'object_id': 1}), '/poll/1/vote/')
        self.assertEqual(reverse('poll:delete_poll',kwargs={ 'object_id': 1}), '/poll/1/delete/')

    def test_if_post_method(self):
        response = self.client.post('/addPoll', { 'question': 'What is wrong', 'default_option_1':'life', 'default_option_2':'university'}, follow=True)
        self.assertEqual(response.request['REQUEST_METHOD'], 'POST')

    def test_index_view(self):
        response = self.client.get('/poll/', follow=True)
        self.assertTemplateUsed(response, 'poll/polls.html')
        response = self.client.get('/poll/', follow=True)
        self.assertTemplateUsed(response, 'poll/polls.html')

    def test_add_poll_view(self):
        response = self.client.get('/poll/addPoll/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_poll(self):
        self.assertEqual(1, self.poll_object.id)
        response = self.client.get('/poll/%s/'%self.poll_object.id, follow=True)
        self.assertTemplateUsed(response, 'poll/poll.html')

        response = self.client.post('/poll/%s/'% self.poll_object.id, {'answer': 'newly'}, follow=True)
        self.assertTrue(Respond.objects.filter(option='newly').exists())
        for i in range(14):
            self.client.post('/poll/%s/' % self.poll_object.id, {'answer': 'newly_%s' % i}, follow=True)
        response = self.client.post('/poll/%s/'% self.poll_object.id, {'answer': 'brand new'}, follow=True)
        self.assertEqual(response.context['info'], 'Numbers of answers can not be grater than 15, if you want add another answers delete previous one.')

    def test_vote(self):
        text = self.respond_object.option
        response = self.client.get('/poll/%s/vote/?option=%s' %(self.poll_object.id, text), follow=True)
        self.assertTemplateUsed(response, 'poll/poll.html')

    def test_delete_respond(self):
        response = self.client.get('/poll/%s/delete/%s' % (self.poll_object.id, self.respond_object.id), follow=True)
        self.assertTemplateUsed(response, 'poll/poll.html')
        self.assertEqual(response.context['info_2'],"There must stay at least two answers." )

        respond_object_1 = Respond.objects.create(poll=self.poll_object, option="New option1")
        respond_object_2= Respond.objects.create(poll=self.poll_object, option="New option2")
        response = self.client.get('/poll/%s/delete/%s' % (self.poll_object.id, self.respond_object.id), follow=True)
        self.assertEqual(response.context['info_2'], "You can not delete answer when someone voted.")
        self.assertEqual(respond_object_2.id, 3)
        response = self.client.get('/poll/%s/delete/%s' % (self.poll_object.id, respond_object_2.id), follow=True)
        self.assertEqual(response.context['info_2'], None)

    def test_delete_poll(self):
        response = self.client.get('/poll/%s/delete/'% self.poll_object.id, follow = True)
        self.assertTemplateUsed(response, 'poll/polls.html')
        self.assertFalse(Poll.objects.filter(question=self.poll_object).exists())

    def test_create_poll(self):
        response = self.client.post('/poll/addPoll/', {'question': 'ok', 'description': None,'default_option_1': 'first', 'default_option_2':'second'}, follow=True)
        self.assertTemplateUsed(response, 'poll/polls.html')
        self.assertTrue(Poll.objects.filter(question="ok").exists())

class TestPollConf(TestCase):

    def test_name(self):
        self.assertEqual(PollConfig.name, "poll")
