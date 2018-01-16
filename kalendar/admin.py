# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import Event
import datetime
import calendar
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from utils import Calendar

class EventAdmin(admin.ModelAdmin):
    list_display = ['title','day', 'starting_time', 'ending_time', 'personal_notes']
    change_list_template = 'admin/kalendar/change_list.html'



admin.site.register(Event, EventAdmin)
