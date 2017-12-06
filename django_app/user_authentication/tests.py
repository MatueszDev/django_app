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



