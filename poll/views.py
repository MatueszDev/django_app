# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.urls import reverse
from .models import Poll, Respond, Vote
from .forms import PollForm, AnsForm
from django.http import HttpResponseRedirect, HttpResponse

def index(request):

    questions = Poll.objects.all()

    extra_content = {"questions" : questions}

    return render(request, "poll/polls.html", extra_content)

def poll(request, object_id):
    if request.method =='POST':
        form = AnsForm(request.POST)

        if form.is_valid():
            poll = Poll.objects.filter(id=object_id)
            respond_object = Respond()

            number = Respond.number_of_answers(poll[0])

            if number > 11:
                text_info = 'Numbers of answers can not be grater than 15, if you want add another answers delete previous one.'

                answers = Respond.objects.filter(poll=poll)
                form = AnsForm()

                extra_content = {'question': poll, 'answers': answers, 'form': form, 'id': object_id, 'info': text_info}

                return render(request, "poll/poll.html", extra_content)


            respond_object.option = form.cleaned_data['answer']
            respond_object.poll = poll[0]
            respond_object.save()

        return HttpResponseRedirect(reverse('poll', kwargs={ 'object_id': object_id}) )
    else:

        question = Poll.objects.filter(id=object_id)
        answers = Respond.objects.filter(poll=question)
        form = AnsForm()

        extra_content = {'question':question, 'answers':answers, 'form':form, 'id':object_id}


        return render(request, "poll/poll.html", extra_content)

def create_poll(request):
    if request.method == 'POST':
        form = PollForm(request.POST)

        if form.is_valid():
            poll_object = Poll()

            poll_object.question = form.cleaned_data['question']
            poll_object.description = form.cleaned_data['description']
            poll_object.save()

            respond_object_1 = Respond()
            respond_object_1.poll = poll_object
            respond_object_1.option = form.cleaned_data['default_option_1']
            respond_object_1.save()

            respond_object_2 = Respond()
            respond_object_2.poll = poll_object
            respond_object_2.option = form.cleaned_data['default_option_2']
            respond_object_2.save()

        return HttpResponseRedirect(reverse('index'))
    else:
        form = PollForm()

    return render(request, "poll/addPoll.html", {'form': form})

def vote(request,object_id, option=None):
    vote = Vote()
    vote.poll = Poll.objects.filter(id=object_id)[0]
    vote.user = request.user
    vote.choice = Respond.objects.filter(poll=vote.poll, option=option)[0] #you must check it first !!!!!!!
    vote.save()

    return HttpResponseRedirect('/poll/%s/' % object_id)