# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.urls import reverse
from .models import Poll, Respond, Vote

def index(request):

    questions = Poll.objects.all()

    extra_content = {"questions" : questions}

    return render(request, "poll/polls.html", extra_content)

def poll(request, question):


    return render(request, "poll/poll.html")