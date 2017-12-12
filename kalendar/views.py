# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from .models import Event, EventModelForm
from .utils import Calendar
import datetime
import calendar
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse, reverse_lazy
from .forms import EventForm


def index(request, info=''):

    after_day = request.GET.get('day__gte', None)
    extra_context =  {}

    if not after_day:
        day = datetime.date.today()
    else:
        try:
            split_after_day = after_day.split('-')
            day = datetime.date(year=int(split_after_day[0]), month=int(split_after_day[1]), day=1)
        except:
            day = datetime.date.today()

    previous_month = datetime.date(year=day.year, month=day.month, day=1)
    previous_month -= datetime.timedelta(days=1)
    previous_month = datetime.date(year=previous_month.year, month=previous_month.month, day=1)

    last_day = calendar.monthrange(day.year, day.month)
    next_month = datetime.date(year=day.year, month=day.month, day=last_day[1])  # find last day of current month
    next_month = next_month + datetime.timedelta(days=1)  # forward a single day
    next_month = datetime.date(year=next_month.year, month=next_month.month,
                               day=1)  # find first day of next month

    extra_context['previous_month'] = '?day__gte=' + str(
       previous_month)
    extra_context['next_month'] = '?day__gte=' + str(next_month)
    cal = Calendar(request=request.get_full_path())
    html_calendar = cal.formatmonth(day.year, day.month, withyear=True)
    html_calendar = html_calendar.replace('<td ', '<td width="177" height="110"')
    extra_context['calendar'] = mark_safe(html_calendar)

    extra_context['text'] = request.get_full_path()
    extra_context['info'] = info

    return render(request, "kalendar/calendar.html", extra_context)


def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)

        if form.is_valid():
            #obj = EventModelForm(request.POST)
            obj = Event()
            obj.title = form.cleaned_data['title']
            obj.day = form.cleaned_data['day']
            obj.starting_time = form.cleaned_data['starting_time']
            obj.ending_time = form.cleaned_data['ending_time']
            obj.personal_notes = form.cleaned_data['personal_notes']
            obj.save()

            #text = '<div class="respond"><h3>You successfully added new event </h3></div>'

            return HttpResponseRedirect(reverse('index'))
    else:
        form = EventForm()
    return render(request, "kalendar/addEvent.html", {'form':form})

def modify_event(request, object_id):
    object = Event.objects.get(pk=object_id)
    if request.method == 'POST':
        form = EventForm(request.POST)

        if form.is_valid():

            object.title = form.cleaned_data['title']
            object.day = form.cleaned_data['day']
            object.starting_time = form.cleaned_data['starting_time']
            object.ending_time = form.cleaned_data['ending_time']
            object.personal_notes = form.cleaned_data['personal_notes']
            object.save()

            #text = '<div class="respond"><h3>You successfully modified new event </h3></div>'

            return HttpResponseRedirect(reverse('index'))
    else:
        form = EventForm()
        form.fields['title'].initial = object.title
        form.fields['day'].initial = object.day
        form.fields['starting_time'].initial = object.starting_time
        form.fields['ending_time'].initial = object.ending_time
        form.fields['personal_notes'].initial = object.personal_notes

    return render(request, "kalendar/modifyEvent.html", {'form':form, 'id':object_id})


def delete_event(request, object_id):
    Event.objects.filter(id=object_id).delete()

    return HttpResponseRedirect(reverse('index'))

def all_event_list(request):
    objects = Event.objects.all()
