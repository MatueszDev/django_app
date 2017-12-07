# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth.models import User


class LoginTest(TestCase):
    def test_if_login_form_is_valid(self):
        form = LoginForm(data={'username': 'john', 'password': 'john'})
        self.assertTrue(form.is_valid())

    def test_if_login_form_is_invalid(self):
        form = LoginForm(data={'username': 'john', 'password': ''})
        self.assertFalse(form.is_valid())
        form = LoginForm(data={'username': '', 'password': ''})
        self.assertFalse(form.is_valid())
        form = LoginForm(data={'username': '', 'password': 'john'})
        self.assertFalse(form.is_valid())


class RegistrationTest(TestCase):
    def test_if_registration_form_is_valid(self):
        form = UserRegistrationForm(data={'username': 'john', 'first_name': 'john', 'last_name': 'john',
                                          'email': 'john@fis.agh.edu.pl', 'password': 'johnjohn', 'password2': 'johnjohn'})
        self.assertTrue(form.is_valid())

    def test_if_registration_is_invalid(self):
        form = UserRegistrationForm(data={'username': '', 'first_name': 'john', 'last_name': 'john',
                                          'email': 'john@fis.agh.edu.pl', 'password': 'john', 'password2': 'john'})
        self.assertFalse(form.is_valid())
        form = UserRegistrationForm(data={'username': 'john', 'first_name': '', 'last_name': 'john',
                                          'email': 'john@fis.agh.edu.pl', 'password': 'al', 'password2': 'al'})
        self.assertFalse(form.is_valid())
        form = UserRegistrationForm(data={'username': 'john', 'first_name': 'john', 'last_name': '',
                                          'email': 'john@fis.agh.edu.pl', 'password': 'john', 'password2': 'john'})
        self.assertFalse(form.is_valid())
        form = UserRegistrationForm(data={'username': 'john', 'first_name': 'john', 'last_name': 'john',
                                          'email': 'john@hfh', 'password': 'john', 'password2': 'john'})
        self.assertFalse(form.is_valid())
        form = UserRegistrationForm(data={'username': 'john', 'first_name': 'john', 'last_name': '',
                                          'email': 'john@fis.agh.edu.pl', 'password': 'ss', 'password2': 'fd'})
        self.assertFalse(form.is_valid())


class ViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', email="user@fis.agh.edu.pl", password="12345678",
                                             first_name="user", last_name="user")

    def test_user_log_in(self):
        self.assertTrue(self.client.login(username='user', password='12345678'))
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_page/main_page.html')

    def test_user_not_log_in(self):
        response = self.client.get('/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_user_log_out(self):
        self.client.login(username='user', password='12345678')
        response = self.client.get('/logout/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_user_register(self):
        user_count = User.objects.count()
        response = self.client.post('/register/', {'username': 'user1', 'first_name': 'John', 'last_name': 'John',
                                                   'email': 'john2@fis.agh.edu.pl', 'password': '12345678',
                                                   'password_2': '12345678'}, follow=True)
        self.assertTemplateUsed(response, 'user_authentication/register_done.html')
        self.assertEqual(User.objects.count(), user_count + 1)

    def test_wrong_register(self):
        response = self.client.post('/register/', {'username': '', 'first_name': 'John', 'last_name': 'John',
                                                   'email': 'john2@fis.agh.edu.pl', 'password': '12345',
                                                   'password_2': '12345'}, follow=True)
        self.assertTemplateUsed(response, 'user_authentication/register.html')

        response = self.client.post('/register/', {'username': 'user', 'first_name': 'John', 'last_name': 'John',
                                                   'email': 'john2@fis.agh.edu.pl', 'password': '12345678',
                                                   'password_2': '12345678'}, follow=True)
        self.assertTemplateUsed(response, 'user_authentication/register.html')

        response = self.client.post('/register/', {'username': 'user11', 'first_name': 'John', 'last_name': 'John',
                                                   'email': '', 'password': '12345678',
                                                   'password_2': '12345678'}, follow=True)
        self.assertTemplateUsed(response, 'user_authentication/register.html')
