# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

class PollForm(forms.Form):

    question = forms.CharField(label="Your's question", max_length=255)

    default_option_1 = forms.CharField(label="first option", max_length=255)
    default_option_2 = forms.CharField(label="second option", max_length=255)
    description = forms.CharField(label="description", max_length=255, required=False)

class AnsForm(forms.Form):

    answer = forms.CharField(label="answer", max_length=255, widget=forms.TextInput({ "placeholder": "New answer" }))